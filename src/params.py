"""PostRoller 共用尺寸（mm）。

主機座標系（所有主機零件都用這個座標建模）：
  原點 = 座管座夾具中心（位於座管軸線上，傾角 0、後伸 0 的座管座）
  +X = 垂直座管、往車尾；+Z = 沿座管往上；+Y = 車子左側（右手座標）
座管座的燕尾面在 X = DOVE_ROOT_X。傾角 pitch（機尾往下為正）與後伸 reach 由座管座決定，
主機本身在各車都一樣；所以換車時主機不用調整。

幾何來源：analysis/fit_final.py（8 種車型，擺臂工作角一致在 ARM_PHI0 ± 2.5°）。
"""
import math

# ── 座管座（每台車一個）──────────────────────────────────────────
POST_DIAMETERS = (25.4, 27.2, 28.6, 30.9, 31.6, 33.9, 34.9)
LINER_T = 1.0            # TPU 內襯厚
BORE_CLR = 0.15          # 內襯外的半徑間隙
BASE_H = 50.0            # 夾具高度（沿座管）
BASE_WALL = 6.0          # 圓筒壁厚
SPLIT_GAP = 0.75         # 前後半在 X=0 各退 0.75（共 1.5 mm 鎖緊餘量）
EAR_X = 12.0             # 鎖耳沿 X 的深度（每半）
EAR_EXTRA = 7.0          # 鎖耳超出孔中心的量
BOLT_Z = (-14.0, 14.0)   # 4×M5 的高度
M5_CLR, M5_HEAD_D, M5_HEAD_H = 5.4, 9.6, 5.2
M5_NUT_AF, M5_NUT_T = 8.2, 4.4

# 燕尾（公頭在座管座，母槽在主機）沿 Z 滑動；主機由下往上滑入，頂端封閉＝上止擋
DOVE_ROOT_X = 27.0       # 燕尾根部（座管座後面）
DOVE_DEPTH = 8.0
DOVE_W_TIP = 40.0        # 燕尾外側最寬處
DOVE_ANGLE = 45.0        # 斜面與底面夾角（45°：主機前段立著印時燕尾槽免支撐）
DOVE_W_ROOT = DOVE_W_TIP - 2 * DOVE_DEPTH / math.tan(math.radians(DOVE_ANGLE))
DOVE_LEN = BASE_H
DOVE_CLR = 0.3           # 母槽每邊間隙
BACKING_W = 52.0         # 燕尾背板寬（Y）
QR_PIN_D = 6.3          # Ø6 球鎖快拆銷孔（燕尾底面下方橫穿母槽）
QR_PIN_X = DOVE_ROOT_X + 4.0
QR_PIN_Z = -DOVE_LEN / 2 - 3.6

# 座管座的傾角/後伸組合（analysis/fit_final.py 的結果）
BASE_VARIANTS = {
    "std": (0.0, 0.0),        # 公路、礫石、城市、26 吋
    "mtb": (-10.0, 0.0),      # 29 / 27.5 吋登山（斜上管、胎頂離座管遠又低）
    "fold": (10.0, 0.0),      # 20 吋折疊
    "minivelo": (30.0, 40.0), # 20 吋小徑（五通高於後軸）
}

# ── 擺臂與馬達（主機座標）────────────────────────────────────────
PIVOT = (110.0, -80.0)   # 擺臂樞軸 (X, Z)
ARM_L = 230.0            # 樞軸 → 馬達軸
ARM_PHI0 = -20.0         # 工作角：臂相對 +X 往上 20°（各車 ±2.5°）
ARM_LIFT_DEG = 9.0       # 抬起時再往上轉的角度（約 36 mm）

def arm_dir(phi_deg=ARM_PHI0):
    a = math.radians(-phi_deg)          # φ 負值 = 往 +Z 轉
    return (math.cos(a), math.sin(a))

def motor_center(phi_deg=ARM_PHI0):
    d = arm_dir(phi_deg)
    return (PIVOT[0] + ARM_L * d[0], PIVOT[1] + ARM_L * d[1])

# 馬達 6374（Flipsky 圖面）：安裝面在 +Y（車左），外殼往 −Y
MOTOR_D, MOTOR_LEN = 63.0, 74.0
MOTOR_FACE_Y = 37.0                 # 安裝面
MOTOR_CAN_Y = (-37.0, 35.0)         # 轉子外殼範圍
SHAFT_D, SHAFT_STEP_D, SHAFT_STEP_L, SHAFT_OUT = 8.0, 10.0, 8.0, 34.0
MOTOR_PCD, MOTOR_SCREW = 44.0, 4.0
MOTOR_PCD_SLOT = (30.0, 46.0)       # 副廠孔距不同 → 長孔
SLEEVE_T = 3.0                      # TPU 滾輪套
ROLLER_R = MOTOR_D / 2 + SLEEVE_T   # 34.5

# 608 軸承
BRG_OD, BRG_ID, BRG_W = 22.0, 8.0, 7.0
BRG_FIT = 0.10                      # 軸承座直徑過盈/間隙補償（印出來孔偏小 → +0.1）

# 擺臂的左側箱型樑
ARM_Y = (40.0, 76.0)                # 箱型樑 Y 範圍（外側與轂端齊平，平放列印）
ARM_H = 28.0                        # 箱型樑高（垂直臂方向）
HUB_D = 32.0                        # 樞軸轂
HUB_Y = (31.0, 76.0)                # 兩顆 608 分別在兩端
CHEEK_T = 6.0
CHEEK_Y_IN = (HUB_Y[0] - 0.5 - CHEEK_T, HUB_Y[0] - 0.5)     # 內側耳板
CHEEK_Y_OUT = (HUB_Y[1] + 0.5, HUB_Y[1] + 0.5 + CHEEK_T)    # 外側耳板

# ── 氣壓棒與抬臂偏心 ──────────────────────────────────────────────
SPRING_D = 180.0         # 下端在擺臂上離樞軸的距離
GS_LEN, GS_STROKE = 100.0, 30.0     # 眼到眼全長、行程（250 N）
GS_WORK = 88.0           # 工作位置長度（壓縮 12 mm，各車 ±8）
GS_BODY_D, GS_ROD_D, GS_EYE_W = 15.0, 6.0, 8.0
SPRING_Y = 53.0          # 氣壓棒中心面
CRANK_R = 17.0           # 偏心半徑：抬起行程 34 mm

def spring_points(phi_deg=ARM_PHI0):
    """回傳 (B 下端, A0 上端工作位置, Cc 偏心中心, n 方向)。"""
    d = arm_dir(phi_deg)
    n = (-d[1], d[0])
    B = (PIVOT[0] + SPRING_D * d[0], PIVOT[1] + SPRING_D * d[1])
    d0 = arm_dir(ARM_PHI0)
    n0 = (-d0[1], d0[0])
    B0 = (PIVOT[0] + SPRING_D * d0[0], PIVOT[1] + SPRING_D * d0[1])
    A0 = (B0[0] + GS_WORK * n0[0], B0[1] + GS_WORK * n0[1])
    Cc = (A0[0] + CRANK_R * n0[0], A0[1] + CRANK_R * n0[1])
    return B, A0, Cc, n0

# ── 主機殼 ───────────────────────────────────────────────────────
RECV_X = (DOVE_ROOT_X + 0.5, 48.0)  # 燕尾母槽座
RECV_Y = (-46.0, 36.0)               # 燕尾座 Y 範圍（與電控艙同寬，立著印不懸空）
RECV_Z = (-BASE_H / 2 - 2, BASE_H / 2 + 8)
BAY_X = (45.0, 215.0)                # 電控艙
BAY_Y = (-46.0, 36.0)
BAY_Z = (-22.0, 28.0)
WALL = 3.0
JOINT_X = 215.0                      # 前段／後段接合面
REAR_X_END = 372.0
DECK_Z = 70.0                        # 擋泥罩頂面下緣（抬起時馬達頂約 63）
BATT_WALL_Y = (-52.0, -46.0)         # 右側電池座牆
MAKITA_DOCK = (91.6, 71.0, 26.3)     # CC0 牧田座外形（長、寬、厚）
MAKITA_HOLES = ((-34.1, 18.7), (-33.9, -18.8), (27.9, -24.6), (27.9, 24.5))   # 相對座中心（沿長、沿寬）

# 電子零件
VESC_DIM = (67.0, 39.0, 20.0)        # Makerbase MINI V6.7
ESP_DIM = (22.5, 18.0, 4.0)          # ESP32-C3 SuperMini

# ── 車型（analysis/fit_final.py 的輸入與結果）─────────────────────
# name, BSD, 胎寬, 後下叉 CS, 五通下沉 drop, 座管角 STA, 立管 ST(C-T), 外露座管, 座管徑, 座管座款式, 夾具高 s
BIKES = [
    ("road_700x28",    "公路 700x28",    622, 28, 425,   76, 73.25, 530, 143, 27.2, "std",      40),
    ("gravel_700x40",  "礫石 700x40",    622, 40, 435,   75, 73.5,  522, 124, 27.2, "std",      46),
    ("city_700x35",    "城市 700x35",    622, 35, 450,   65, 74.0,  445, 200, 27.2, "std",     110),
    ("mtb29_2.3",      "登山 29x2.3",    622, 58, 438,   60, 72.0,  420, 220, 31.6, "mtb",     124),
    ("mtb275_2.4",     "登山 27.5x2.4",  584, 61, 438,   48, 72.0,  368, 220, 30.9, "mtb",     140),
    ("mtb26_1.95",     "老登山 26x1.95", 559, 50, 424.5, 41, 73.0,  444, 200, 27.2, "std",      74),
    ("minivelo_20",    "小徑 20x1.75",   406, 44, 390,  -30, 73.0,  460, 180, 27.2, "minivelo", 40),
    ("folding_20",     "折疊 20x1.75",   406, 44, 400,  -30, 70.0,  360, 295, 33.9, "fold",     72),
]
