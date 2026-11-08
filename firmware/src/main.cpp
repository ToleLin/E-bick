// PostRoller — 快拆摩擦助力器 控制韌體
//
// 硬體：ESP32-C3 SuperMini ←UART→ VESC（COMM 埠：5V / GND / RX / TX）
//       藍牙踏頻感測器（標準 Cycling Speed & Cadence，例如 Magene S3+ 踏頻模式），用橡皮圈綁在曲柄上
//
// 邏輯（踏板輔助，不是油門）：
//   有在踩（收到新的曲柄圈數且踏頻 ≥ CADENCE_MIN）而且車速 ≥ MIN_SPEED → 依段位給 VESC 固定電流
//   停止踩踏 PEDAL_TIMEOUT_MS 內電流歸零；車速 TAPER_START → SPEED_LIMIT 線性遞減到 0（台灣電動輔助自行車 25 km/h）
//   感測器斷線、VESC 通訊中斷、電池低壓 → 電流歸零
//
// 車速不必知道輪徑：摩擦驅動時滾輪表面速度 = 胎面速度 = 車速，所以 車速 = 馬達轉速 × 滾輪周長。
//
// 按鍵（電控艙右側 12 mm 按鍵，接 GPIO4 與 GND）：
//   短按：段位 0 → 1 → 2 → 3 → 0（0 = 關閉輔助）
//   長按 1.5 s：段位歸 0
//   長按 6 s：忘記已配對的感測器（下一個廣播踏頻服務的感測器會被記住）
// 指示燈（艙壁 5 mm LED 接 GPIO3，串 330 Ω 到 GND；板載 LED GPIO8 同步）：每 2 秒閃「段位」次；找感測器時快閃。
//
// 狀態：尚未接實機測試。第一次上路前請先把車架起來、後輪離地空轉測試。

#include <Arduino.h>
#include <NimBLEDevice.h>
#include <Preferences.h>
#include <VescUart.h>

// ───── 可調參數（依實際零件修改）──────────────────────────────
static const float ROLLER_DIA_MM   = 63.0f + 2 * 2.5f;  // 滾輪外徑：6374 外殼 Ø63 ＋ 2.5 mm 止滑套
static const int   MOTOR_POLE_PAIRS = 7;                // 6374 / 6354：14 極 = 7 對極
static const float SPEED_LIMIT_KMH  = 25.0f;            // 輔助上限
static const float TAPER_START_KMH  = 22.0f;            // 從這裡開始遞減
static const float MIN_SPEED_KMH    = 3.0f;             // 低於這個速度不出力（無感測馬達起步需要先轉起來）
static const float LEVEL_AMPS[4]    = {0.0f, 10.0f, 18.0f, 28.0f}; // 各段馬達相電流 (A)；6374 170KV：28 A ≈ 1.6 N·m ≈ 46 N 推力
static const float RAMP_UP_APS      = 25.0f;            // 加電流斜率 A/s（避免打滑）
static const float RAMP_DOWN_APS    = 120.0f;           // 減電流斜率 A/s
static const float CADENCE_MIN_RPM  = 15.0f;
static const uint32_t PEDAL_TIMEOUT_MS = 1200;          // 超過這段時間沒有新的曲柄圈數 → 視為停止踩踏
static const int   CELLS            = 5;                // 牧田 18V = 5S
static const float CUTOFF_START_V   = 3.25f * CELLS;    // 開始降功率
static const float CUTOFF_END_V     = 3.05f * CELLS;    // 完全停止
static const uint32_t VESC_TIMEOUT_MS = 800;

// ───── 腳位（ESP32-C3 SuperMini）──────────────────────────────
static const int PIN_VESC_RX = 20;   // 接 VESC 的 TX
static const int PIN_VESC_TX = 21;   // 接 VESC 的 RX
static const int PIN_BUTTON  = 4;    // 外接按鍵（GPIO9 是開機腳，不用）
static const int PIN_LED     = 8;    // 板載藍色 LED，低電位亮
static const int PIN_LED_EXT = 3;    // 艙壁 LED，高電位亮

// ───── BLE CSC ──────────────────────────────────────────────
static NimBLEUUID CSC_SERVICE((uint16_t)0x1816);
static NimBLEUUID CSC_MEASUREMENT((uint16_t)0x2A5B);

static NimBLEAdvertisedDevice* g_found = nullptr;
static volatile bool g_doConnect = false;
static volatile bool g_connected = false;
static NimBLEClient* g_client = nullptr;
static Preferences g_prefs;
static String g_savedAddr;

// 踏頻狀態（在 BLE 回呼裡更新）
static volatile uint16_t g_lastCrankRevs = 0;
static volatile uint16_t g_lastCrankTime = 0;   // 1/1024 s
static volatile bool     g_haveCrank = false;
static volatile uint32_t g_lastRevMillis = 0;   // 最後一次「曲柄圈數有增加」的本機時間
static volatile float    g_cadenceRpm = 0.0f;

VescUart g_vesc;

static int g_level = 0;
static float g_cmdAmps = 0.0f;
static bool g_vescOk = false;
static uint32_t g_lastVescMs = 0;
static float g_speedKmh = 0.0f, g_battV = 0.0f;

// ───── BLE 回呼 ─────────────────────────────────────────────
static void onCscNotify(NimBLERemoteCharacteristic*, uint8_t* d, size_t len, bool) {
  if (len < 1) return;
  uint8_t flags = d[0];
  size_t i = 1;
  if (flags & 0x01) i += 6;                 // 輪圈資料：uint32 圈數 + uint16 時間
  if (!(flags & 0x02) || len < i + 4) return;  // 沒有曲柄資料（感測器在「速度模式」）
  uint16_t revs = d[i] | (d[i + 1] << 8);
  uint16_t t    = d[i + 2] | (d[i + 3] << 8);
  if (g_haveCrank) {
    uint16_t dRev = revs - g_lastCrankRevs;           // uint16 自動處理溢位
    uint16_t dT   = t - g_lastCrankTime;
    if (dRev > 0 && dRev < 20 && dT > 0) {
      g_cadenceRpm = dRev * 60.0f * 1024.0f / dT;
      g_lastRevMillis = millis();
    }
  }
  g_lastCrankRevs = revs;
  g_lastCrankTime = t;
  g_haveCrank = true;
}

class ClientCB : public NimBLEClientCallbacks {
  void onDisconnect(NimBLEClient*) override {
    g_connected = false;
    g_haveCrank = false;
    g_cadenceRpm = 0;
  }
};
static ClientCB g_clientCB;

class ScanCB : public NimBLEAdvertisedDeviceCallbacks {
  void onResult(NimBLEAdvertisedDevice* dev) override {
    if (!dev->isAdvertisingService(CSC_SERVICE)) return;
    if (g_savedAddr.length() && g_savedAddr != String(dev->getAddress().toString().c_str())) return;
    NimBLEDevice::getScan()->stop();
    g_found = dev;
    g_doConnect = true;
  }
};
static ScanCB g_scanCB;

static void startScan() {
  NimBLEScan* s = NimBLEDevice::getScan();
  s->setAdvertisedDeviceCallbacks(&g_scanCB, false);
  s->setActiveScan(true);
  s->setInterval(100);
  s->setWindow(90);
  s->start(0, nullptr, false);   // 0 = 一直掃到找到為止
}

static bool connectSensor() {
  if (!g_client) {
    g_client = NimBLEDevice::createClient();
    g_client->setClientCallbacks(&g_clientCB, false);
    g_client->setConnectTimeout(5);
  }
  if (!g_client->connect(g_found)) return false;
  NimBLERemoteService* svc = g_client->getService(CSC_SERVICE);
  if (!svc) { g_client->disconnect(); return false; }
  NimBLERemoteCharacteristic* chr = svc->getCharacteristic(CSC_MEASUREMENT);
  if (!chr || !chr->canNotify() || !chr->subscribe(true, onCscNotify)) { g_client->disconnect(); return false; }
  String addr = g_found->getAddress().toString().c_str();
  if (g_savedAddr != addr) {               // 第一次連到的感測器記起來，避免騎車時連到別人的
    g_savedAddr = addr;
    g_prefs.putString("sensor", addr);
  }
  g_connected = true;
  return true;
}

// ───── 按鍵與 LED ──────────────────────────────────────────
static void handleButton() {
  static bool was = false;
  static uint32_t downAt = 0;
  static bool longDone = false, forgetDone = false;
  bool now = digitalRead(PIN_BUTTON) == LOW;
  uint32_t ms = millis();
  if (now && !was) { downAt = ms; longDone = forgetDone = false; }
  if (now && !longDone && ms - downAt > 1500) { g_level = 0; longDone = true; }
  if (now && !forgetDone && ms - downAt > 6000) {
    g_prefs.remove("sensor");
    g_savedAddr = "";
    if (g_client && g_client->isConnected()) g_client->disconnect();
    forgetDone = true;
  }
  if (!now && was && ms - downAt > 30 && ms - downAt < 1500) g_level = (g_level + 1) % 4;
  was = now;
}

static void updateLed() {
  uint32_t ms = millis();
  bool on;
  if (!g_connected) {
    on = (ms / 100) % 2;                                // 找感測器：快閃
  } else {
    uint32_t phase = ms % 2000;                         // 每 2 秒閃段位次數
    uint32_t k = phase / 250;
    on = (k < (uint32_t)(g_level * 2)) && (k % 2 == 0);
  }
  digitalWrite(PIN_LED, on ? LOW : HIGH);
  digitalWrite(PIN_LED_EXT, on ? HIGH : LOW);
}

// ───── 輔助電流計算 ─────────────────────────────────────────
static float targetAmps() {
  if (!g_connected || !g_vescOk || g_level == 0) return 0;
  bool pedaling = g_haveCrank && (millis() - g_lastRevMillis < PEDAL_TIMEOUT_MS) && g_cadenceRpm >= CADENCE_MIN_RPM;
  if (!pedaling || g_speedKmh < MIN_SPEED_KMH) return 0;
  float a = LEVEL_AMPS[g_level];
  if (g_speedKmh >= SPEED_LIMIT_KMH) return 0;
  if (g_speedKmh > TAPER_START_KMH) a *= (SPEED_LIMIT_KMH - g_speedKmh) / (SPEED_LIMIT_KMH - TAPER_START_KMH);
  if (g_battV < CUTOFF_END_V) return 0;
  if (g_battV < CUTOFF_START_V) a *= (g_battV - CUTOFF_END_V) / (CUTOFF_START_V - CUTOFF_END_V);
  return a;
}

void setup() {
  pinMode(PIN_BUTTON, INPUT_PULLUP);
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_LED_EXT, OUTPUT);
  digitalWrite(PIN_LED, HIGH);
  Serial.begin(115200);
  Serial1.begin(115200, SERIAL_8N1, PIN_VESC_RX, PIN_VESC_TX);
  g_vesc.setSerialPort(&Serial1);

  g_prefs.begin("postroller", false);
  g_savedAddr = g_prefs.getString("sensor", "");

  NimBLEDevice::init("PostRoller");
  NimBLEDevice::setPower(ESP_PWR_LVL_P9);
  startScan();
}

void loop() {
  static uint32_t lastCtl = 0, lastVescPoll = 0, lastLog = 0;
  uint32_t ms = millis();

  handleButton();
  updateLed();

  if (g_doConnect) {
    g_doConnect = false;
    if (!connectSensor()) startScan();
  }
  if (!g_connected && !NimBLEDevice::getScan()->isScanning() && !g_doConnect) startScan();

  if (ms - lastVescPoll >= 100) {                       // 10 Hz 讀 VESC 狀態
    lastVescPoll = ms;
    if (g_vesc.getVescValues()) {
      g_lastVescMs = ms;
      g_battV = g_vesc.data.inpVoltage;
      float rollerRpm = fabsf(g_vesc.data.rpm) / MOTOR_POLE_PAIRS;
      g_speedKmh = rollerRpm * PI * ROLLER_DIA_MM / 1000.0f * 60.0f / 1000.0f;
    }
    g_vescOk = (ms - g_lastVescMs) < VESC_TIMEOUT_MS;
  }

  if (ms - lastCtl >= 20) {                             // 50 Hz 控制迴圈
    float dt = (ms - lastCtl) / 1000.0f;
    lastCtl = ms;
    float target = targetAmps();
    if (target > g_cmdAmps) g_cmdAmps = min(target, g_cmdAmps + RAMP_UP_APS * dt);
    else                    g_cmdAmps = max(target, g_cmdAmps - RAMP_DOWN_APS * dt);
    g_vesc.setCurrent(g_cmdAmps);                       // 0 A = 滑行（不煞車）；持續送指令，VESC 逾時會自動停
  }

  if (ms - lastLog >= 1000) {
    lastLog = ms;
    Serial.printf("lvl=%d sensor=%d cad=%.0f rpm v=%.1f km/h batt=%.2f V cmd=%.1f A vesc=%d\n",
                  g_level, (int)g_connected, g_cadenceRpm, g_speedKmh, g_battV, g_cmdAmps, (int)g_vescOk);
  }
}
