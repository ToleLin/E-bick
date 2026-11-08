"""各車型：座管夾位置 → 後輪胎頂的幾何關係（側視圖，X 往後為正、Z 往上，原點 = 五通中心）。

用途：決定擺臂長度、擺角範圍、座管夾可裝的高度。數字是各類車的典型幾何（M 號／成人），
不是某一台車的實測；實際車子請量「座管夾上緣到胎頂的距離」對照 docs 的適用範圍表。
"""
import math

# name, 胎 BSD(mm), 胎寬(mm), 後下叉長 CS, 五通下沉 drop(+ = 五通低於後軸), 座管角 STA(deg),
#       座管長 ST(五通中心到立管上緣), 座墊高 SH(五通中心到座墊面)
BIKES = [
    ("公路 700x28",      622, 28, 410, 70, 73.5, 520, 720),
    ("礫石 700x40",      622, 40, 425, 72, 73.0, 500, 720),
    ("城市 700x35",      622, 35, 450, 65, 72.0, 500, 700),
    ("登山 29x2.3",      622, 58, 435, 55, 75.0, 430, 720),
    ("登山 27.5x2.4",    584, 61, 430, 30, 75.0, 420, 710),
    ("老式登山 26x1.95", 559, 50, 430, 30, 73.0, 430, 700),
    ("折疊 20x1.75",     406, 44, 400, -30, 70.0, 360, 700),
    ("小徑 16x1.35",     349, 35, 380, -40, 70.0, 330, 680),
]

def tire_od(bsd, w):
    # 胎高約 = 胎寬 × 0.95（氣壓正常、未受壓）
    return bsd + 2 * 0.95 * w

def analyse(clamp_above_collar=45.0):
    rows = []
    for name, bsd, w, cs, drop, sta, st, sh in BIKES:
        R = tire_od(bsd, w) / 2
        ax = math.sqrt(cs**2 - drop**2)          # 後軸水平距離
        az = drop                                 # 後軸高度（相對五通）
        a = math.radians(sta)
        u = (math.cos(a), math.sin(a))            # 座管方向（往後上）
        s_clamp = st + clamp_above_collar         # 座管夾中心沿座管的位置
        qx, qz = s_clamp * u[0], s_clamp * u[1]
        exposed = sh - st - 45                     # 外露座管（座墊面到軌道約 45 mm）
        # 胎頂點
        tx, tz = ax, az + R
        dx, dz = tx - qx, qz - tz                  # 夾中心 → 胎頂：往後 dx、往下 dz
        # 座管到輪胎最近距離（座管線到輪心距離 − R）
        # 點到直線距離：|cross(u, C)|
        dist_line = abs(u[0] * az - u[1] * ax)
        gap_st = dist_line - R
        D = math.hypot(ax - qx, az - qz)           # 夾中心到輪心
        rows.append((name, R, exposed, dx, dz, D - R, gap_st))
    return rows

if __name__ == "__main__":
    print(f"{'車型':<16}{'胎半徑':>7}{'外露座管':>8}{'夾→胎頂 後':>10}{'下':>6}{'夾→胎面最近':>11}{'座管-胎間隙':>10}")
    for r in analyse():
        print(f"{r[0]:<16}{r[1]:7.0f}{r[2]:8.0f}{r[3]:10.0f}{r[4]:6.0f}{r[5]:11.0f}{r[6]:10.0f}")
