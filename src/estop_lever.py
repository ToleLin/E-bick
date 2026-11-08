"""緊急停止拉桿（車把端，每台車一支）：手指把紅色拉桿往身體方向一拉 → 拉煞車線 → 主機觸發桿把抬臂把手頂過死點
→ 氣壓棒自己把滾輪抬離輪胎。純機械，不靠電。

拉桿自己的座標：車把軸 = X（+X 往內側／龍頭方向），+Y 往前（離開騎士），+Z 往上；原點 = 車把中心、夾具寬度中間。
配置跟一般煞車把相同（拉桿片朝外、線頭在樞軸前方、線管往內側出去），但：
- 夾在龍頭附近的空車把上（現有變速把、煞車把的內側），拉桿片只有 58 mm，不會伸到外側控制件；
- 拉桿平面在車把下方（Z = LEVER_Z），往身體方向拉時從車把下面掃過，不會撞車把；
- 煞車線頭（MTB 圓柱線頭 Ø6×7）立著卡進線頭座；安裝時先把拉桿拉到底，線頭從上板安裝孔放進去，放開後就被上板擋住。
左側用 mirror=True 的版本（鏡像），兩邊各一支 STL。
"""
import math

import build123d as bd
from cadgen import model

BAR_DIAMETERS = (22.2, 23.8, 25.4)
CLAMP_W = 14.0
WALL = 4.5
LEVER_Z = -18.0                  # 拉桿平面（車把中心下方）
BLADE_T = 7.0                    # 拉桿厚（Z）
PLATE_T = 4.0
GAP = 0.4
PIVOT = (-4.0, 22.0)             # 樞軸（X, Y），軸沿 Z，M4×20＋防鬆螺帽
HORN = 26.0                      # 樞軸 → 線頭（往前）
BLADE_LEN = 58.0
BLADE_REST_DEG = 183.0           # 拉桿片靜止方向：朝外（−X）、略朝騎士
PULL_DEG = 33.1                  # 拉到主機觸發需要的轉角（線行程 14.2 mm＝主機 12.7＋線管壓縮/鬆弛 1.5）
STOP_X = (PIVOT[0] + 22.0, PIVOT[0] + 34.0)   # 線管座（內側）
NIPPLE_D, FERRULE_D = 6.6, 6.4
RED = "#d62828"
GREY = "#3a3d42"


def box(x0, x1, y0, y1, z0, z1):
    return bd.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * bd.Box(x1 - x0, y1 - y0, z1 - z0)


def zcyl(r, z0, z1, x=0.0, y=0.0):
    return bd.Pos(x, y, z0) * bd.Cylinder(r, z1 - z0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def xcyl(r, x0, x1, y=0.0, z=0.0):
    c = bd.Cylinder(r, x1 - x0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return bd.Pos(x0, y, z) * bd.Rot(0, 90, 0) * c


def ycyl(r, y0, y1, x=0.0, z=0.0):
    c = bd.Cylinder(r, y1 - y0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return bd.Pos(x, y1, z) * bd.Rot(90, 0, 0) * c


def ccw(pts):
    """頂點排成逆時針：擠出方向才會照 +Z（順時針會擠到反方向）。"""
    area = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
    return list(pts) if area > 0 else list(pts)[::-1]


def xy_prism(pts, z0, z1):
    return bd.Pos(0, 0, z0) * bd.extrude(bd.Polygon(*ccw(pts), align=None), z1 - z0)


def taper(a, ra, b, rb, z0, z1):
    d = (b[0] - a[0], b[1] - a[1])
    L = math.hypot(*d)
    n = (-d[1] / L, d[0] / L)
    pts = [(a[0] + n[0] * ra, a[1] + n[1] * ra), (b[0] + n[0] * rb, b[1] + n[1] * rb),
           (b[0] - n[0] * rb, b[1] - n[1] * rb), (a[0] - n[0] * ra, a[1] - n[1] * ra)]
    return xy_prism(pts, z0, z1) + zcyl(ra, z0, z1, *a) + zcyl(rb, z0, z1, *b)


def rot(v, deg):
    """繞 Z 逆時針轉 deg（從上往下看）。往身體方向拉＝逆時針（拉桿片朝 −X，尖端往 −Y）。"""
    a = math.radians(deg)
    return (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a))


def anchor_at(pull_deg=0.0):
    r = rot((0.0, HORN), pull_deg)
    return (PIVOT[0] + r[0], PIVOT[1] + r[1])


def cable_pull(pull_deg):
    """線頭離開線管座方向的位移（mm）。"""
    s = (STOP_X[1], PIVOT[1] + HORN)
    a0, a = anchor_at(0.0), anchor_at(pull_deg)
    return math.hypot(a[0] - s[0], a[1] - s[1]) - math.hypot(a0[0] - s[0], a0[1] - s[1])


def plate_z():
    zc = LEVER_Z
    up = (zc + BLADE_T / 2 + GAP, zc + BLADE_T / 2 + GAP + PLATE_T)
    lo = (zc - BLADE_T / 2 - GAP - PLATE_T, zc - BLADE_T / 2 - GAP)
    return up, lo


JOINT = (STOP_X[0] + 3.0, PIVOT[1] + HORN + 5.0)   # 上下件第二支 M4（線管座內）


def plate_outline():
    ay = PIVOT[1] + HORN
    return [(PIVOT[0] - 10.0, PIVOT[1] - 8.0), (STOP_X[1], PIVOT[1] - 8.0), (STOP_X[1], ay + 10.0),
            (PIVOT[0] - 22.0, ay + 10.0), (PIVOT[0] - 22.0, PIVOT[1] + 12.0)]


def mount_upper_body(bar_d=22.2):
    """上件：夾環＋鎖緊耳＋上夾板。夾環底部切平在上板底面，上板朝下就能免支撐列印。"""
    r_i = bar_d / 2 + 0.2
    r_o = r_i + WALL
    up, _ = plate_z()
    ring = xcyl(r_o, -CLAMP_W / 2, CLAMP_W / 2)
    ears = box(-CLAMP_W / 2, CLAMP_W / 2, -5.5, 5.5, r_i - 1.0, r_o + 8.5)
    neck = box(-CLAMP_W / 2, CLAMP_W / 2, 6.0, PIVOT[1] + 4.0, up[0], -r_i + 3.0)
    body = ring + ears + neck + xy_prism(plate_outline(), *up)
    body &= box(-80, 80, -80, 80, up[0], 80)                              # 切平
    body -= xcyl(r_i, -60, 60)                                            # 車把孔
    body -= box(-CLAMP_W, CLAMP_W, -0.8, 0.8, 0.0, r_o + 20)              # 上方開口（鎖緊）
    zb = r_o + 4.0
    body -= ycyl(2.2, -10, 10, z=zb)                                      # M4×16 鎖緊螺絲
    body -= bd.Pos(0, 5.5 - 3.4, zb) * bd.Rot(-90, 0, 0) * bd.extrude(
        bd.RegularPolygon(7.2 / 2, 6, major_radius=False), 4.0)          # 螺帽槽
    body -= zcyl(2.2, up[0] - 1, up[1] + 1, *PIVOT)                       # M4 樞軸
    body -= zcyl(2.2, up[0] - 1, up[1] + 1, *JOINT)                       # M4 接合
    # 安裝孔：拉到底時線頭的位置（放開後線頭被上板擋住，不會掉）
    a_full = anchor_at(PULL_DEG + 3.0)
    body -= zcyl(NIPPLE_D / 2 + 0.6, up[0] - 1, up[1] + 1, *a_full)
    body.label = "estop_lever_mount_upper"
    body.color = GREY
    return body


def mount_lower_body():
    """下件：下夾板＋線管座＋前牆＋靜止柱，高度到上板底面；下板朝下免支撐列印。"""
    up, lo = plate_z()
    ay = PIVOT[1] + HORN
    stop_blk = box(STOP_X[0], STOP_X[1], ay - 6.0, ay + 10.0, lo[0], up[0])
    front_wall = box(PIVOT[0] - 22.0, STOP_X[1], ay + 6.5, ay + 10.0, lo[0], up[0])
    post = zcyl(1.8, lo[0], up[0], x=PIVOT[0] + 8.4, y=ay - 2.0)          # 靜止擋：線頭臂靠在這
    body = xy_prism(plate_outline(), *lo) + stop_blk + front_wall + post
    body -= zcyl(2.2, lo[0] - 1, up[0] + 1, *PIVOT)                       # M4 樞軸
    body -= zcyl(2.2, lo[0] - 1, up[0] + 1, *JOINT)                       # M4 接合（防鬆螺帽在下板外側）
    # 線管座：線管頭從內側頂住，內線往外穿到線頭
    zc = LEVER_Z
    body -= xcyl(FERRULE_D / 2, STOP_X[1] - 6.0, STOP_X[1] + 1, y=ay, z=zc)
    body -= xcyl(1.1, STOP_X[0] - 1, STOP_X[1] - 5.9, y=ay, z=zc)
    body.label = "estop_lever_mount_lower"
    body.color = GREY
    return body


def mount_body(bar_d=22.2):
    """上下件合起來（檢查用）。"""
    m = mount_upper_body(bar_d) + mount_lower_body()
    m.label = "estop_lever_mount"
    m.color = GREY
    return m


def blade_body(pull_deg=0.0):
    """拉桿片（紅色）：樞軸轂、往外的手指拉片、往前的線頭臂。"""
    zc = LEVER_Z
    z0, z1 = zc - BLADE_T / 2, zc + BLADE_T / 2
    d = rot((1.0, 0.0), BLADE_REST_DEG + pull_deg)
    tip = (PIVOT[0] + d[0] * BLADE_LEN, PIVOT[1] + d[1] * BLADE_LEN)
    A = anchor_at(pull_deg)
    blade = taper(PIVOT, 7.0, tip, 6.0, z0, z1) + taper(PIVOT, 7.0, A, 6.0, z0, z1)
    blade -= zcyl(2.2, z0 - 1, z1 + 1, *PIVOT)
    blade -= zcyl(NIPPLE_D / 2, z0 - 1, z1 + 1, *A)
    # 內線從線頭往線管座（+X）穿出；整個行程都要讓得開 → 本體座標 0° 到 −38° 扇形開口
    for a in (0.0, -13.0, -26.0, -38.0):
        u = rot((1.0, 0.0), a + pull_deg)
        mid = (A[0] + u[0] * 6.0, A[1] + u[1] * 6.0)
        blade -= bd.Pos(mid[0], mid[1], zc) * bd.Rot(0, 0, math.degrees(math.atan2(u[1], u[0]))) * bd.Box(12.0, 2.2, BLADE_T + 2)
    # 手指止滑紋（拉桿片朝騎士那一側）
    n = rot((0.0, -1.0), BLADE_REST_DEG + 180.0 + pull_deg)
    for k in range(5):
        s = 26.0 + 6.5 * k
        c = (PIVOT[0] + d[0] * s + n[0] * 6.2, PIVOT[1] + d[1] * s + n[1] * 6.2)
        blade -= bd.Pos(c[0], c[1], zc) * bd.Rot(0, 0, BLADE_REST_DEG + pull_deg) * bd.Box(2.0, 1.6, BLADE_T + 2)
    blade.label = "estop_lever_blade"
    blade.color = RED
    return blade


def bar_stub(bar_d=22.2):
    b = xcyl(bar_d / 2, -120, 60)
    b.label = "handlebar"
    b.color = "#9aa3ad"
    return b


def lever_assembly(bar_d=22.2, pull_deg=0.0):
    return bd.Compound(children=[mount_upper_body(bar_d), mount_lower_body(), blade_body(pull_deg), bar_stub(bar_d)],
                       label="estop_lever")


@model
def estop_lever_222():
    return lever_assembly(22.2)


@model
def estop_lever_222_pulled():
    return lever_assembly(22.2, PULL_DEG)


if __name__ == "__main__":
    print(f"拉 {PULL_DEG}° → 線行程 {cable_pull(PULL_DEG):.1f} mm")
    estop_lever_222()
    estop_lever_222_pulled()
