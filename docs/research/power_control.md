# 研究報告：power_control

# 電池與操控子系統研究報告：無油門、免在每台車佈線的座管摩擦驅動

## 0. 結論與建議架構

**電池：第一版用牧田 18V LXT 電池，主機內做一個 3D 列印的牧田電池座。第二版可升級成兩顆串聯的 36V，或自組 10S 電池。**
- 牧田電池在台灣容易取得，原廠充電器 45 分鐘就能充滿，換電池只要一秒。
- 代價是能量少：一顆 5Ah 約只能跑 10–15 km，而且 18V 系統電流大。
- 開源底座建議用兩個公有領域（CC0）的模型當基礎，自己的專案才能自由授權：
  - fablab.ee 的電池座（Printables 74366）
  - axel 的列印端子（Printables 200596）

**操控：建議「全無線、只有踏板輔助、沒有油門」。**
- 主機裡放一片 ESP32-C3，用 UART 送 `setCurrent` 指令給 VESC。
- 踏頻來源分兩階段：
  - 第一階段：Magene S3+ 藍牙踏頻器（NT$399–460），用橡皮圈綁在曲柄上。
  - 第二階段：自製「曲柄陀螺儀模組」，停止踩踏時能在 0.2 秒內斷電。
- 把手上放一個 ESP-NOW 小按鈕盒（ESP32-C3 加按鈕，可加煞車磁簧開關）。
- 緊急斷電做三層，任一層觸發就把電流歸零：
  1. VESC 通訊逾時
  2. 磁吸安全鑰匙（跑步機款）加拉繩接到騎士身上
  3. 主機後方的實體總開關

---

## 1. 電池

### 1.1 三種方案比較

| 項目 | (a) 電動工具電池＋底座（牧田 LXT） | (b) 自組 10S 36V 電池＋保護板（BMS） | (c) 主機內建電池（像參考商品） |
|---|---|---|---|
| 能量 | BL1850B 90 Wh、BL1860B 108 Wh（18V×Ah 推算）；兩顆串聯成 36V 為 180–216 Wh | 10S1P Molicel P45B 為 162 Wh；10S2P 為 324 Wh（推算） | 參考：Risun 18V 10Ah 內建約 180 Wh，200W、2 kg、305×100×117 mm、宣稱 50 km、21V 2A 充電約 5 小時。[risunmotor](https://www.risunmotor.com/products/super-light-18v-200w-rear-friction-ebike-motor-kits-with-18v-10ah-built-in-battery) |
| 重量 | BL1850B 約 600–630 g（零售商標示）。[mysky-shop](https://mb.mysky-shop.pl/MAKITA-Battery-18V-5-0Ah-LI-ION-BL1850B-p18217) | P45B 每顆最重 70 g，10 顆電芯約 0.7 kg。[Molicel datasheet](https://www.imrbatteries.com/content/molicel_p45b.pdf)<br>成品參考：LiTech 36V 5Ah 10S2P（180 Wh）約 1180 g，持續放電 10A。[litech](https://litechpower.com/?p=3443) | 視電芯數而定 |
| 價格 | BL1860B 台灣牧田公司貨 NT$4,085（原價 4,300），另見 NT$3,495。[Yahoo](https://tw.buy.yahoo.com/brands/41169422)<br>換算約 NT$32–38/Wh | 蝦皮 10S 15A 保護板很多（價格見第 3 節）。<br>台灣比價站有 36V 10S2P「10Ah」標價 NT$281，價格不合理，極可能虛標容量。[findprice](https://www.findprice.com.tw/a/10ah) | 電芯加保護板加 USB-C 模組 |
| 充電 | 原廠充電器，BL1850B 45 分鐘充滿。[makitatools](https://makitatools.com/products/details/BL1850B) | 42V 充電器（DC 或 XT 接頭） | USB-C：IP2368 模組標稱 2–5S、100W，但有買家說 5S 要改板、實際約 90W。[onbuy](https://www.onbuy.com/gb/p/new-ip2368-bidirectional-charger-pd100w-fast-charge-module-type-c-interface-support-2-5s-lithium-battery~p255081981/)<br>10S 無法直接用 PD 充，要另外升壓。 |
| 換車速度 | 最佳：電池和主機分開拔 | 要另外固定電池盒 | 整機一起搬 |
| 主要風險 | 牧田未公布持續放電電流（UNVERIFIED）；電池卡榫原本是為工具設計，震動下要加第二道固定 | 自組電池的電芯焊接、保護板品質 | 主機變重；座管負重；USB-C 充電功率低 |

**牧田電池的過放保護：**
- 原廠只說有 Star Protection（防過載、過放、過熱）。[makitatools](https://makitatools.com/products/details/BL1850B)
- ZED Supplies 說電池內部會自行斷開，這是賣家說法，未獲原廠證實。[zedsupplies](https://zedsupplies.com/blogs/news/makita-18v-to-12v-battery-adapter)
- Partsbuilt 賣的轉接座另外加了低電壓斷電板，並警告插著不拔會慢慢耗電；但它最大只有 3.5A，不適合馬達。[partsbuilt](https://partsbuilt.com/makita-18v-battery-adapter)
- 結論：一定要在 VESC 設定低電壓斷電（見 1.3）。

**兩顆牧田串聯成 36V 的注意事項（我的推論）：**
- 兩顆電池的保護各自獨立，VESC 只看得到總電壓。
- 建議 ESP32 用分壓電阻量中點電壓，任一顆過低就斷電。
- 兩顆電池的容量與電量要相近。

### 1.2 續航估算（每公里耗電）

實際量測與廠商數據：

| 來源 | 數據 | 換算 |
|---|---|---|
| Endless-Sphere ferias77 的前輪摩擦驅動（躺式車，7S 25.9V，40 mm 滾輪） | 207 km、均速 30.5 km/h | 6.4 Wh/km |
| 同上 | 22 km 通勤 | 6.5 Wh/km（同車用輪轂馬達為 8 Wh/km）[ES](https://endless-sphere.com/sphere/threads/front-wheel-friction-drive.71252/) |
| Rubbee X | 每個模組 36V 93.6 Wh，約 12–16 km [pedelecs](https://pedelecs.co.uk/forum/threads/rubbee-x-introduction.29838/post-411714) | 約 5.9–7.8 Wh/km |
| 牧田 BBY180 | BL1830（約 54 Wh），第 3 段輔助、75 kg，約 8.5 km [notice-facile](https://www.notice-facile.com/en/manual/1272522/makita+bby180) | 約 6.4 Wh/km |
| Risun 18V 宣稱 | 180 Wh / 50 km | 3.6 Wh/km，偏樂觀 |

以 **5–8 Wh/km**、可用能量 85% 估算：

| 電池 | 可用能量 | 估計續航 |
|---|---|---|
| BL1850B | 約 76 Wh | 約 10–15 km |
| BL1860B | 約 92 Wh | 約 11–18 km |
| 2×BL1860B 串聯 36V | 約 184 Wh | 約 23–37 km |
| 10S1P P45B | 約 138 Wh | 約 17–28 km |
| 10S2P P45B | 約 275 Wh | 約 34–55 km |

參考商品宣稱的「18V 跑 50 km」需要約 250–400 Wh，在 18V 下相當於 14–22Ah。目前查到的只有 Risun 的 10Ah；eBay 原頁面打不開（403），所以這個宣稱標為 UNVERIFIED。[eBay](https://www.ebay.com/itm/127654453389)（US$339）

### 1.3 電池電流如何限制馬達功率（VESC 設定）

**原理：**
- VESC 對「電池電流上限」（`l_in_current_max`，韌體預設 99A）和「馬達電流」是分開限制的。[mcconf_default.h](https://github.com/vedderb/bldc/blob/master/motor/mcconf_default.h)
- 低速時馬達電流可以大於電池電流（扭力大）；但輸入功率 ≈ 電池電壓 × 電池電流上限。

**建議數值（工程假設，未經牧田官方數據驗證）：**

| 電池 | 電池電流上限 | 對應輸入功率 |
|---|---|---|
| BL1850B | 約 20A | 約 360W |
| BL1860B | 約 25A | 約 450W |
| 10S 15A 保護板 | 12A（保護板額定的 80%） | 約 430W |

- 約 250W 的輔助在 18V 下大約 15A，可以跑得動。

**其他必設參數：**
- **回充電流**：預設 −60A，必須改成 0 到 −1A，避免回灌充電電動工具電池。
- **低電壓斷電**：`BATTERY_CUT_START/END`。建議 5S 設 16.0/15.0V，10S 設 32/30V（約每芯 3.2/3.0V）。這是我的工程建議值。
- **接頭**：XT30 持續只有 15A，18V 系統不夠用。XT60 為持續 30A、瞬間 60A，建議用 XT60。[CMU xt60.pdf](https://mrsdprojects.ri.cmu.edu/2025teamb/wp-content/uploads/sites/84/2025/05/xt60.pdf)、[unmannedtech](https://www.unmannedtechshop.co.uk/de/blogs/knowledge-base/fpv-drone-battery-connector-guide-xt30-xt60-xt90-ratings)

### 1.4 開源可列印的牧田電池座與端子

授權是我透過 Printables 官方 API 逐一查到的：

| 模型 | 作者 | 授權 | 重點 |
|---|---|---|---|
| [Makita 18V battery adapter (74366)](https://www.printables.com/model/74366-makita-18v-battery-adapter) | fablab.ee | **CC0** | 原始版，5 mm 螺絲孔，需支撐 |
| [battery terminal for Makita 18V battery adapter REMIX (200596)](https://www.printables.com/model/200596-battery-terminal-for-makita-18v-battery-adapter-re) | axel | **CC0** | 列印的端子座，插 6.3 mm 平插端子（Faston）。作者自己說是撐到原廠端子寄到前的暫用品 |
| [Improved Makita LXT 18V Battery Terminal (1080441)](https://www.printables.com/model/1080441-improved-makita-lxt-18v-battery-terminal-643852-2) | Muffelkraft | CC BY-NC-SA | 3-pin 相容、配 6.35×0.8 mm 平插端子，建議 PETG-V0、壁厚 >3 mm |
| [remix for 3mm bolts (134967)](https://www.printables.com/model/134967-makita-18v-adapter-remix-for-3mm-bolts) | ltlowe | CC BY-NC-SA | M3 孔，52×58 mm 孔距，用原廠 643852-2 端子 |
| [Makita LXT 18V Battery Mount V4 (187090)](https://www.printables.com/model/187090) | Wiseone | CC BY-NC | 卡入有確實的「喀」聲，原廠端子用環氧樹脂黏住，需支撐 |
| [Cheap Makita 18V battery holder (947440)](https://www.printables.com/model/947440-cheap-makita-18v-battery-holder) | Kobyax | CC BY-NC-SA | 只是收納座 |
| [MakerWorld 2421970](https://makerworld.com/en/models/2421970) | – | Standard Digital File License（不是開源授權） | 用 40×18×1 mm 不鏽鋼片當接點 |

**授權建議：**
- 專案以 74366 和 200596（皆 CC0）為基礎重新設計，可以自由選擇開源授權。
- 採用 NC-SA 授權的檔案，衍生作品也會被綁成非商用且要同樣授權。

**端子取得：**
- 原廠 643852-2：Zoro 約 US$5.45，Tooled-Up £2.75。[Zoro](https://zoro.com/makita-terminal-part-mp643852-2/i/G602127935)、[Tooled-Up](https://www.tooled-up.com/makita-genuine-643852-2-battery-terminal-battery-connector-yellow/prod/771641/)
- 蝦皮和淘寶上找不到原廠件（UNVERIFIED）。
- 蝦皮有「牧田款 21V 銅鍍鎳插腳 DIY」（見第 3 節）。
- 6.3 mm 平插端子能承受的電流沒有查證，正式版建議用原廠端子或銅插腳。

---

## 2. 操控（不改裝車子）

### (a) 電動滑板遙控器

**Flipsky 官方價格**：[flipsky.net](https://flipsky.net/collections/remote)

| 型號 | 價格 |
|---|---|
| VX1 | US$29 |
| VX1 Pro | US$34 |
| VX2 Pro | US$43 |
| VX4 Pro | US$71 |
| VX5（IP68） | US$208–259 |

**規格與相容性：**
- VX4 有 240×240 彩色螢幕，支援 PPM 和 UART，有三段速度與定速。[atbshop](https://www.atbshop.co.uk/electric-board-accessories/flipsky-vx4-remote-controller-for-esk8-boards)
- 舊團購資訊說 VX2 只能走 UART，VX1 可走 PPM。[esk8.news](https://forum.esk8.news/t/global-closed-flipsky-vx2-vx1-remote-group-buy-post-order-discussion/16358)
- 斷訊時的保護行為（failsafe）查不到官方說明（UNVERIFIED）。

**能不能裝在把手上：**
- 找不到現成的把手夾具。
- 社群的 CoViX2 是 VX2 改殼，可選 GoPro 座，接 M5 螺絲。[esk8.news](https://forum.esk8.news/t/covix2-a-flipsky-vx2-mod/23295)
- Printables 只有 VX4 的接收器盒。[815788](https://www.printables.com/model/815788-flipsky-24ghz-remote-vx4-mounting-box)
- 結論：要自己列印夾具或用矽膠綁帶固定。

**缺點：**
- 本質是油門，與「只做踏板輔助」的目標衝突。
- 接收器會佔用 VESC 的 UART 或 PPM 腳位。
- 不建議當主要操控。

### (b) 藍牙踏頻器 → ESP32 → VESC（UART）

**踏頻器通訊協定：**
- 藍牙標準的 CSC 服務 0x1816，量測特徵值 0x2A5B。
- 內容是 flags 位元組加上「累計曲柄圈數 uint16」和「最後一次曲柄事件時間 uint16，單位 1/1024 秒，約 64 秒歸零一次」。
- 通知頻率實測大約每秒一次，這是觀察值，不是規範。[Nordic DevZone](https://devzone.nordicsemi.com/f/nordic-q-a/68100/question-regarding-cscs-demo-measurement-values/279507)
- 影響：起步要約 1–2 秒才給力；**停止踩踏要約 1.5–2.5 秒才能判斷**（我的推論）。

**踏頻器型號：**
- Magene S3+：藍牙加 ANT+，CR2032 電池，約 9 g，附曲柄用小橡皮圈，裝電池的方式切換速度或踏頻模式。有買家反映會意外跳回速度模式。[evelostore](https://evelostore.com/products/magene-s3-speed-cadence-dual-mode-sensor)
- iGPSport CAD70：藍牙 5.0 加 ANT+，IPX7，€32.60。[lemona](https://www.lemona-electronics.eu/igpsport-cad70-cadence-sensor-igpsport.html)
- Wahoo RPM、XOSS：台灣價格未查到。

**現有開源程式（沒有找到一個完整的「藍牙踏頻 → VESC」專案，需要自己組合）：**

| Repo | 授權 | 用途 |
|---|---|---|
| [SolidGeek/VescUart](https://github.com/SolidGeek/VescUart) | GPL-3.0 | 有 `setCurrent`、`setBrakeCurrent`、`setRPM`、`setDuty`、`sendKeepalive`、`getVescValues`，支援 CAN 轉發 |
| [av1d/BLE-CSC decode](https://github.com/av1d/BLE-Cycling-Speed-and-Cadence-Service-examples-decode-data) | MIT | 完整連線範例，連上 CSC 裝置並解碼（ArduinoBLE 函式庫） |
| [jamesmontemagno/mycadence-arduino](https://github.com/jamesmontemagno/mycadence-arduino) | CC BY-NC-SA 4.0 | 自動掃描連 Magene/Wahoo/Garmin，用 nkolban BLE 函式庫 |
| [haditim/ESP32-VESC-eBike](https://github.com/haditim/ESP32-VESC-eBike) | GPL-2.0 | ESP32 用 VescUart 分支控制 VESC |
| [techfoundrynz/VESC-BLE-ESP32](https://github.com/techfoundrynz/VESC-BLE-ESP32) | – | ESP32 當 VESC 的藍牙模組（走 UART） |
| ESP-IDF [nimble/blecsc](https://github.com/espressif/esp-idf/tree/master/examples/bluetooth/nimble/blecsc) | – | 踏頻器端（伺服器）範例，可參考資料格式 |
| Tshibous/ebike-controller | – | 搜尋結果出現過（ESP32 加 VescUart、25 km/h、250W、煞車與逾時斷電），但目前 404，已不可用 |

**另一條路線：VESC Express（[vedderb/vesc_express](https://github.com/vedderb/vesc_express)）**
- 它的 LispBM 腳本有藍牙「主控端」功能：可掃描、連線、訂閱通知，最多同時 4 個外部裝置，也支援 HID 主機。[BLE README](https://github.com/vedderb/vesc_express/blob/main/main/ble/README.md)
- 有 ESP-NOW 收發範例。
- 有「Devkit C3」硬體設定，透過 UART（TX21/RX20，115200）連 VESC。[hw_devkit_c3.h](https://github.com/vedderb/vesc_express/blob/main/main/hwconf/devkits/hw_devkit_c3.h)
- 好處：手機 VESC Tool 可以直接當儀表。
- 缺點：「LispBM 下指令控制馬達電流」這條路沒有實測過（UNVERIFIED）。

### (c) VESC 韌體內建的 PAS 功能

- **只支援一種感測器**：`PAS_SENSOR_TYPE_QUADRATURE`，也就是雙霍爾、兩條訊號線的踏頻感測器。[datatypes.h](https://github.com/vedderb/bldc/blob/master/datatypes.h)
- **控制模式**：無／踏頻／扭力／扭力加踏頻逾時。扭力模式需要硬體支援 `HW_HAS_PAS_TORQUE_SENSOR`。[app_pas.c](https://github.com/vedderb/bldc/blob/master/applications/app_pas.c)
- **預設值**：[appconf_default.h](https://github.com/vedderb/bldc/blob/master/applications/appconf_default.h)
  - 磁鐵數 24（一般 12 磁感測器要改成 12）
  - 起始 10 rpm、滿載 180 rpm
  - 增力 0.6 秒、減力 0.3 秒
  - 更新頻率 500 Hz
- **腳位衝突**：PAS 預設用的就是 UART 的 RX/TX 腳。[hw.h](https://github.com/vedderb/bldc/blob/master/hwconf/hw.h)
  - 也就是說，接了實體 PAS 就不能再用 UART 接 ESP32。
  - VESCTouchDisplay 專案就是因此改用 CAN。[mih722](https://github.com/mih722/VESCTouchDisplay)
- 便宜的單霍爾三線 PAS 不支援，只有社群分支 [doh38/bldc](https://www.github.com/doh38/bldc) 有加。

### (d) 有線 PAS 與油門為什麼不利於快速換車

- 每台車都要裝磁環。分體式（如 KT-D12L）可以不拆中軸，但仍是每台車一套。[AliExpress wiki](https://www.aliexpress.com/s/wiki-ssr/article/split-pass)
- 要拉一條約 1 m 的線到座管。
- 同樣是 12 磁的感測器，不同款常常不相容。[pedelecs](https://www.pedelecs.co.uk/forum/threads/motor-controller-doesnt-work-with-kt-v12l-pas-sensor.42808)
- 油門不只要佈線，還不符合「人力為主、電力為輔」。

### (e) 把手上的藍牙按鈕與小螢幕

- 藍牙自拍遙控器（YUNTENG L01，NT$99）是藍牙 HID 裝置。ESP32-C3 可以當 HID 主機，ESP-IDF 有 `esp_hid_host` 範例並列出支援 C3。[esp_hid_host](https://github.com/espressif/esp-idf/tree/master/examples/bluetooth/esp_hid_host)
- 這種按鈕只適合切換輔助段數，**不可當緊急停止**：它省電時可能斷線，這點 UNVERIFIED。
- 螢幕：用手機加 VESC Tool（需走 VESC Express 路線），或自製 ESP-NOW 按鈕盒加 0.96" OLED。

### (f) 推薦的操控架構

**台灣法規背景：**
- 電動輔助自行車要經型式審驗合格，人力為主、電力為輔，最高時速 25 km/h 以下，車重 40 kg 以下。
- 自行加裝的套件沒有審驗合格標章，所以只能做到「接近合法」（legal-ish）。[koc](https://www.koc.com.tw/?p=349614)
- 參考 EN 15194 的二手說法：停止踩踏後輔助要在 2 m 內停止（有煞車斷電開關可放寬到 5 m）。[avdweb](https://avdweb.nl/solar-bike/misc/solar-bike-regulation-and-limitations)
  - 以 22.5 km/h 計，2 m 只有約 0.32 秒。
  - **只用藍牙踏頻器達不到**；改用曲柄陀螺儀模組才有機會。

**互鎖條件：ESP32 每 20–50 Hz 送一次 `setCurrent`，以下全部成立才給正電流：**
1. 踏頻向前且大於 20–30 rpm。
2. 把手按鈕盒的心跳訊號在 300 ms 內有收到（若有啟用）。
3. 磁吸安全鑰匙還插著。
4. 車速低於 25 km/h（由 VESC 的轉速換算）。
5. 沒有煞車事件：可以是把手的磁簧開關，或「正在出力但輪速仍急降」的推估（我的推論）。

**電流變化**：增力約 0.5 秒漸進，斷電要立即歸零。

**VESC 逾時設定**：預設 1000 ms，建議改成 200–300 ms，逾時煞車電流設 0。[appconf_default.h](https://github.com/vedderb/bldc/blob/master/applications/appconf_default.h)

**曲柄陀螺儀模組（第二階段）：**
- 選項一：XIAO nRF52840 Sense（內建 LSM6DS3TR-C 六軸感測器、BQ25101 充電、待機 <5 µA）。[Seeed wiki](https://wiki.seeedstudio.com/XIAO_BLE/)
- 選項二：ESP32-C3 加 MPU6050，用 ESP-NOW 傳。論壇實測 ESP-NOW 最小來回延遲約 6 ms。[esp32.com](https://esp32.com/viewtopic.php?p=151325)
- 陀螺儀直接量曲柄角速度，不必等轉完一圈，還能分辨倒踩。

**緊急斷電三層（硬體）：**
1. 跑步機款磁吸安全鑰匙，拉繩接到騎士身上，主機內放磁簧或霍爾感測器。
2. 防火花總開關（Flipsky 200A，特價 US$32，規格 3S–14S 等）。[flipsky](https://flipsky.net/products/anti-spark-switch-aluminum-pcb-case-v1-0-200a)
3. 電池正極加 30A 汽車插片保險絲。

**如果一定要接線**：只讓訊號線走一顆磁吸連接器（pogo pin 每 pin 額定 2A），電源永遠不經過它。目前找不到可靠的 20–30A 磁吸電源連接器。

---

## 3. 採購清單（蝦皮／露天實際看到的商品）

| 品項 | 商品標題（節錄）與網址 | 價格 |
|---|---|---|
| 牧田轉 XT60 底座 | 大藝牧田電池轉XT60/DC輸出底座 https://shopee.tw/大藝牧田電池轉XT60-DC輸出底座電動工具電池取電器電池轉接底座-i.4786768.44618612510 | NT$238–258 |
| 4 聯底座 | 牧田威克士得偉…4聯電池轉接底座轉XT60 10A https://shopee.tw/全新商品-牧田-威克士-得偉-大兿-博世-泉友款4聯電池轉接底座-DIY電動工具電池底座轉XT60-DC輸出-10A-i.1625204199.57158010313 | 未見；標示只有 10A，不夠用 |
| 帶保險絲座的轉接 | 適配器帶保險座…通用牧田18V(20V) https://shopee.tw/適配器-帶保險座轉換連接輸出線-通用-牧田-18V(20V)-鋰電池-DIY轉換器-電子線輸出用改裝(不含電池)-i.2381215.15194341339 | 未見 |
| 端子插腳 | 牧田款21V…銅鍍鎳插腳 https://shopee.tw/牧田款-21-V-電動工具鋰電池-銅鍍鎳-插腳-電池鏈接件-插頭-接口-充電-取電-DIY配件-i.16473545.26618842582 | 未見 |
| 自組牧田規格電池外殼 | 電動工具電池套料F款…10串 https://shopee.tw/電動工具電池套料-F款-通用-牧田18V(21V)-10串-鋰電池套料-鋰電池電路板-BL1830B-BL1860B-i.2381215.19891060827 | 未見 |
| 3D 列印牧田座 | [現貨]Makita 牧田18V BL系列電池轉接座 https://shopee.tw/-現貨-Makita-牧田-18V-BL系列-電池轉接座-DIY改裝-牧田電池座-創意改裝-i.214719556.21336601824<br>露天同款：https://www.ruten.com.tw/item/22233117054437/ | 未見 |
| 10S 保護板 | 10S 36V 15A 18650…保護板 https://shopee.tw/10S-36V-15A-18650-鋰離子鋰電池充電保護板-PCB-PCM-通用端口-用於電動滑板車電動自行車充電-i.164937240.42833398418<br>博志10串 15A https://shopee.tw/【臺灣熱賣】博志10串36V鋰電池保護板-18650三元聚合物電動自行車保護板15A-噹噹-i.1382906033.55964880502 | 未見 |
| 踏頻器 | 邁金S3+ 公司貨 https://shopee.tw/現貨供應-公司貨-邁金-S3-Magene-速度-踏頻-迴轉速-感測器-Garmin-Bryton-ZWIFT-可使用-i.2264886.8370414966<br>列表頁 https://shopee.tw/list/踏頻感測器 | NT$460（列表最低 NT$399） |
| ESP32-C3 SuperMini | 【環島科技】 https://shopee.tw/【環島科技】ESP32-C3-開發板-ESP32-SuperMini-台灣現貨-開發板ESP32-迷你開發板-MINI板-i.280233910.24001423519<br>[RWG] https://shopee.tw/-RWG-ESP32-C3-ESP32C3-SuperMini-開發板-i.14363185.28858902036 | NT$90–100；NT$38–84 |
| 藍牙按鈕 | YUNTENG 雲騰 L01 https://shopee.tw/YUNTENG-雲騰-通用-充電型-藍芽自拍遙控器-L01-藍牙自拍器-自拍控制器-藍牙遠端控制器-遙控自拍按鈕-自拍器-i.5645645.4554877955 | NT$99（2 件 NT$179） |
| 磁吸安全鑰匙 | 跑步機安全開關安全鎖 磁性開關 https://shopee.tw/跑步機安全開關安全鎖-磁性開關電動跑步機啟動鑰匙-i.64117056.2579850569 | 未見 |
| XT60 帶線 | [菜鳥飛行DIY] XT60 12AWG https://shopee.tw/-菜鳥飛行DIY-XT60-接頭帶線-公-母-12AWG-矽膠線-連接線-電源線-航模插頭-XT60H帶護套-i.5198380.59927987 | 未見 |
| XT60 面板座 | XT60E-F 帶固定孔 https://shopee.tw/XT60母頭帶固定孔航模電池接口XT60E-F公母連接器電機電調插頭-i.1198375562.45521234510 | 未見 |
| 保險絲 | 保險絲30A 附防水座 https://shopee.tw/台灣在地-保險絲30A(A61)-附保險絲座-汽車百貨-燈-座防水-外接式保險絲-保險絲防水盒-LED汽車保險絲座-i.10606691.14357288334<br>防水帶線插片座 30A/40A 10 套 https://shopee.tw/【防水帶線】汽車保險絲插片座-車用改裝插座-防水保險絲座-帶30CM線-30A-40A保險絲-10套-i.16466944.45420961752 | 未見 |
| 磁吸 pogo（僅限訊號） | 磁吸接頭 8PIN（每 pin 2.0A，<36V） https://shopee.tw/【現貨秒發】1pc-磁吸接頭公母座8PIN-黃銅充電觸點彈簧頂針-pogopin連接器-i.279812180.28334765372 | 未見 |
| 大電流快拆 | Anderson 50A https://shopee.tw/Anderson安德森接頭-600V-50A-安德森接頭鋰鐵電池接頭單極連接器-大電流-快接-端子-接頭-電動機車-i.111033364.7117332783 | NT$40／個 |

**淘寶**：搜尋引擎沒有收錄淘寶商品頁，以下僅提供關鍵字（UNVERIFIED）：
- 「牧田电池转接座 带线」
- 「牧田 电池 接线端子」
- 「10串36V 18650 电池组 定制」
- 「迈金 S3+ 踏频」
- 「跑步机 安全钥匙 磁吸」
- 「防打火开关 电滑」

---

## 4. 未能驗證（UNVERIFIED）清單

- 牧田 BL1850B／BL1860B 的持續放電電流、內部是否有斷電 MOSFET、電芯型號。
- Flipsky 遙控器斷訊時的保護行為，以及在台灣的通路價格。
- 6.3 mm 平插端子能承受的電流。
- 台灣電商上的原廠 643852-2 端子。
- 自拍遙控器省電斷線的行為。
- 參考商品的 USB-C 充電與實際電池容量（只有一篇 AliExpress 文章提到，[連結](https://www.aliexpress.com/s/wiki-ssr/article/electric-bike-conversion-kit-18v-brushless-motor-friction-drive-ebike-review)）。
- VESC Express 用 LispBM 控制馬達電流的實作細節。
- 部分頁面因 403 擋爬蟲、firecrawl 與 GitHub API 次數用完，無法讀取原文。


---

# 查證結果：power_control

# 事實查核結果：電池與操控子系統研究報告

**總結：** 報告裡跟韌體、授權、規格有關的說法大致可信。有兩處要改：台灣法規那段寫得太寬鬆，Flipsky 防火花開關的規格也寫錯了。還有一個重大缺口：沒經過型式審驗的電動輔助自行車騎上路，會被直接沒收，不只是「接近合法」。

ESP-NOW 延遲那一項沒查完，因為這一輪的 WebSearch 次數已經用完；要補查得另外再跑一次。

## 一、逐項查核

**1. Printables 74366（fablab.ee）與 200596（axel）都是 CC0 → CONFIRMED**
- 用 Printables 的 GraphQL API（api.printables.com/graphql）查到，兩者授權都是「Creative Commons — Public Domain（CC0）」。
- 200596 的說明寫明它是替 fablab.ee 那款底座做的端子，配 6.3 mm 平插端子，作者也說只是暫用品。兩者都是 CC0，沒有授權衝突。
- 另外四款的授權也都對：1080441 與 134967 是 CC-BY-NC-SA，187090 是 CC-BY-NC。

**2. VESC 內建 PAS 只支援雙霍爾（quadrature）感測器 → CONFIRMED**
- datatypes.h 裡的列舉只有 `PAS_SENSOR_TYPE_QUADRATURE = 0` 一項。
- app_pas.c 會讀 PAS1、PAS2 兩支腳，再用查表判斷踩踏方向。
- https://github.com/vedderb/bldc/blob/master/datatypes.h

**3. PAS 預設佔用 UART 的 RX/TX 腳 → CONFIRMED（有附註）**
- hw.h 裡寫的是：沒有另外定義時，`HW_PAS1_PORT` 用 `HW_UART_RX_PORT`，`HW_PAS2_PORT` 用 `HW_UART_TX_PORT`。
- 附註：這只是預設值，個別硬體設定檔可以另外指定腳位。要看實際買的那片 ESC 的 hwconf 才能確定。
- https://github.com/vedderb/bldc/blob/master/hwconf/hw.h

**4. VESC 的預設參數 → CONFIRMED**
- appconf_default.h：
  - 通訊逾時 `APPCONF_TIMEOUT_MSEC 1000`，逾時煞車電流 0.0
  - PAS 磁鐵數 24
  - 起始 10 rpm、滿載 180 rpm
  - 增力 0.6 秒、減力 0.3 秒
  - 更新頻率 500 Hz
- mcconf_default.h：
  - 電池電流上限 `L_IN_CURRENT_MAX 99.0`，電池回充下限 `L_IN_CURRENT_MIN -60.0`
  - 馬達電流範圍 ±60A
  - 低電壓斷電預設只有 10V／8V，一定要改
- https://github.com/vedderb/bldc/blob/master/applications/appconf_default.h
- https://github.com/vedderb/bldc/blob/master/motor/mcconf_default.h

**5. VESC Express 的 Devkit C3 走 UART TX21／RX20、115200 → CONFIRMED**
- vesc_express 是 GPL-3.0。
- https://github.com/vedderb/vesc_express/blob/main/main/hwconf/devkits/hw_devkit_c3.h

**6. 牧田 BL1850B 45 分鐘充滿，原廠未公布放電電流 → CONFIRMED**
- 官方頁面寫「45 minutes or less」。
- 頁面上沒有放電電流額定，也沒有電池本體重量。
- 重量看零售商最常標 630 g，也有 634、650 g。報告寫的「600–630 g」偏低，建議改成約 630–650 g。
- https://makitatools.com/products/details/BL1850B

**7. 台灣電動輔助自行車定義（25 km/h、40 kg、須經型式審驗）→ CONFIRMED，但結論要修正**
- 第 69 條的原文跟報告一致。
- 現行條文的「電動自行車」已改稱「微型電動二輪車」：以電力為主，限速 25 km/h，車重不含電池 40 kg 以下，或含電池 60 kg 以下。
- 要修正的是第 71 條第 2 項：「未經型式審驗合格之電動輔助自行車，於道路行駛者，沒入之。」所以這種車上路是會被沒收車輛，不是「接近合法」。
- https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=K0040012&flno=69
- https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=K0040012&flno=71

**8. EN 15194「停止踩踏後 2 m 內斷電」，所以「只用藍牙踏頻器達不到」→ CORRECTED**
- 2 m／5 m 這組數字有查到出處，但只是二手整理（avdweb）。
- 台灣自己的標準更寬鬆：「電動輔助自行車安全檢測基準」第三點之一，刊在行政院公報第 030 卷第 182 期（2024-09-26），兩個條件擇一符合即可：
  - 7.3.1：踏板停止踩踏後 **3 秒內**停止動力輸出
  - 7.3.2：煞車把手有斷電開關時 5 m 內停止，沒有時 2 m 內停止
- 因此藍牙踏頻器約 1.5–2.5 秒的判斷時間，在台灣標準下有機會符合 3 秒的選項。報告的結論需要修正。
- 來源：https://www.rootlaw.com.tw/Attach/L-Doc/A040110051015600-1130926-1000-005.pdf

**9. XT60 持續 30A／瞬間 60A，XT30 持續 15A → CONFIRMED**
- 多個零售商與技術文章引用的 Amass 規格都是這個數字（XT30 為 15A／30A）。
- 報告引用的 CMU PDF 現在連不上（網域解析不到）。
- https://www.unmannedtechshop.co.uk/de/blogs/knowledge-base/fpv-drone-battery-connector-guide-xt30-xt60-xt90-ratings

**10. Molicel P45B 每顆最重 70 g → CONFIRMED**
- 資料表寫「70 g (Max)」，持續放電 45A。
- https://www.imrbatteries.com/content/molicel_p45b.pdf

**11. Flipsky 防火花開關 200A，特價 US$32，規格 3S–14S → CORRECTED**
- 價格對：特價 US$32，原價 US$68，有現貨。
- 報告給的網址已失效（404），正確網址是：https://flipsky.net/products/flipsky-anti-spark-switch-aluminum-pcb-case-v1-0-200a-for-electric-skateboard-ebike-scooter-robots
- 規格要改：最高 20S（90V，安全使用到 80V），持續電流 80A（200A 不是持續值），尺寸 68×34×9.5 mm，10AWG 線。

**12. Magene S3+ 價格 NT$399–460 → 部分 CONFIRMED**
- BigGo 2026 年 10 月有一筆標「公司貨」的 S3+ 賣 NT$460。
- 近期常見價格在 NT$450–550。最低 NT$399 這個數字查不到。
- https://biggo.com.tw/s/magene+s3/

**13. 程式碼授權 → CONFIRMED**
- 經 GitHub API 與 README 查證：
  - VescUart：GPL-3.0
  - av1d：MIT
  - haditim：GPL-2.0
  - mycadence-arduino：README 寫 CC BY-NC-SA 4.0（倉庫裡沒有 LICENSE 檔）
- techfoundrynz/VESC-BLE-ESP32：完全沒有授權聲明（報告寫「–」）。沒有授權就等於保留所有權利，不能拿來改作再散布。

**14. Risun 參考商品規格 → CONFIRMED**
- 18V 200W、內建 10Ah、淨重 2 kg、305×100×117 mm、約 50 km、21V 2A 充電約 5 小時、最高 25 km/h。
- 目前售價 US$359.99。
- https://www.risunmotor.com/products/super-light-18v-200w-rear-friction-ebike-motor-kits-with-18v-10ah-built-in-battery

**15. XIAO nRF52840 Sense 規格 → CONFIRMED**
- LSM6DS3TR-C 六軸、BQ25101 充電（50 或 100 mA）、待機 <5 µA。
- 待機電流是整個系列的共通規格，不是 Sense 版另外量的。
- https://wiki.seeedstudio.com/XIAO_BLE/

**16. ESP-NOW 最小來回延遲約 6 ms → UNVERIFIABLE**
- esp32.com 的頁面被機器人檢查擋住，讀不到內容。
- 這一輪的 WebSearch 次數用完了，沒辦法再找其他來源。

## 二、報告漏掉的重要缺口

1. **沒審驗的車上路會被沒收（第 71 條第 2 項）。** 設計文件和開源專案的說明應該寫清楚：只供私人場地、研究用。

2. **台灣檢測基準還有幾條硬性規定會影響設計**（同上，行政院公報 2024-09-26）：
   - 7.2 功率：最大輸出 <400W，或連續額定 ≤250W。報告建議 BL1860B 的電池電流上限 25A，約 450W 輸入，可能超過 400W，建議 18V 時 ≤20A、36V 時 ≤10A。
   - 7.3：倒踩時馬達不可以出力。
   - 7.4：超過 25 km/h 要在 3 秒內斷電；新型式要在 25 km/h ±10% 內斷電。
   - 7.5：煞車訊號線短路或斷線時，3 秒內要斷電。
   - 7.6：牽車輔助最高 6 km/h，而且要騎士持續操作才會作動。
   - 7.1.1：鋰電池最高工作電壓要低於 60V。
   - 第 5 點：韌體要有防止竄改速度上限的封印。用 VESC 自製的系統原理上做不到這點。

3. **牧田電池的保護可能是靠工具端執行的。** 論壇說法（未經原廠證實）是：電池用信號腳通知工具停止，工具才會斷電。只接正負極的轉接座會失去過放、過流、過熱三種保護，不只是報告提到的過放。
   - 建議 ESP32 讀取電池的信號腳，或另外加過流、過熱斷電。
   - https://ukworkshop.co.uk/threads/dewalt-to-makita-battery-adapter.150908/post-1788767

4. **授權會限制整個專案。**
   - 韌體如果連結 VescUart（GPL-3.0），ESP32 的韌體就必須用 GPL-3.0 開源。
   - mycadence-arduino（NC-SA）不能用在允許商用的專案。
   - techfoundrynz 的程式沒有授權，不能用。
   - 建議藍牙踏頻解碼用 MIT 的 av1d，或自己寫。

5. **VESC 內建 PAS 停止踩踏的判斷時間。**
   - 在扭力模式，`MAX_MS_WITHOUT_CADENCE` 是 1000 ms。
   - 在踏頻模式，是「沒有脈衝的時間超過最大脈衝週期」就判定停止。
   - 這可以當作自製互鎖邏輯的參考值。

6. **馬達端的煞車電流也要調低。** VESC 預設馬達電流下限 −60A。摩擦驅動在逾時或煞車時如果反拖，滾輪會打滑、磨耗輪胎。報告只提到電池的回充電流，馬達的 `l_current_min` 也要調小。

7. **座管尺寸要相容。** 參考商品 Risun 標示適用座管 25.4、27.2、28.6、30.4、30.8、31.6 mm。快拆夾具應該涵蓋這些常見尺寸，可以做成可換的墊片。
