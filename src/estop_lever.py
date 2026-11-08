"""緊急停止拉桿（車把端，每台車一支）v0.3 精簡版：手指把紅色拉桿往身體方向一拉 → 拉煞車線 → 主機觸發桿
把抬臂把手頂過死點 → 氣壓棒自己把滾輪抬離輪胎。純機械，不靠電。

拉桿自己的座標：車把軸 = X（+X 往內側／龍頭方向），+Y 往前（離開騎士），+Z 往上；原點 = 車把中心、夾具寬度中間。
配置跟一般煞車把相同（拉桿片朝外、線頭在樞軸前方、線管往內側出去）：
- 夾在龍頭附近的空車把上（現有變速把、煞車把的內側），拉桿片 52 mm，不會伸到外側控制件；
- 拉桿平面在車把下方，往身體方向拉時從車把下面掃過；
- 座子拆成上下兩件，都是平面朝下免支撐列印；
- 煞車線頭（MTB 圓柱線頭 Ø6×7）立著卡進線頭座：先把拉桿拉到底，從上件的安裝孔放進去，放開後被上板擋住。
左側用原版，右側用鏡像版。

公差：使用者的 3D 列印可能有約 0.2 cm 誤差 → 列印件之間會動的地方每邊留 FIT（預設 1.0 mm，合計 2 mm），
螺絲孔、線頭座、線管頭座都放大；印得比較準的話可以把 FIT 改小再匯出。
"""
import math

import build123d as bd
from cadgen import model

# ── 公差（2026-11-08 使用者：列印可能有約 0.2 cm 誤差）──────────────
FIT = 1.0             # 列印件之間會動的配合：每邊間隙
HOLE_M4 = 4.8         # M4 螺絲過孔（印小了用 4.5 mm 鑽頭擴孔）
BAR_FIT = 1.0         # 夾環孔直徑比車把大 1.0 mm，靠上方鎖緊縫收緊
SPLIT = 3.0           # 鎖緊縫寬（可收緊約 1 mm 直徑）
NUT_AF = 7.6          # M4 螺帽槽（對邊 7.0＋公差）
NIPPLE_D = 7.2        # MTB 圓柱線頭 Ø6×7 的座孔
WIRE_SLOT = 3.0       # 內線 Ø1.5 的槽
FERRULE_D = 7.0       # 5 mm 線管頭（外徑約 6）的座孔

# ── 尺寸 ────────────────────────────────────────────────────────
BAR_DIAMETERS = (22.2, 23.8, 25.4)
CLAMP_W = 12.0
WALL = 4.0
PLATE_T = 3.0
BLADE_T = 7.0                     # 拉桿片厚（線頭 Ø6×7 立著放）
PIVOT = (-2.0, 18.0)              # 樞軸（X, Y），軸沿 Z，M4×20＋防鬆螺帽
HORN = 20.0                       # 樞軸 → 線頭（往前）
BLADE_LEN = 52.0
BLADE_REST_DEG = 183.0            # 拉桿片靜止方向：朝外（−X）、略朝騎士
PULL_MM = 14.0                    # 設計拉線行程（主機端需要約 12，另留線管壓縮與鬆弛）
STOP_X = (12.0, 22.0)             # 線管座（內側）
RED = "#d62828"
GREY = "#3a3d42"

_R_O_MAX = max(BAR_DIAMETERS) / 2 + BAR_FIT / 2 + WALL
_HUB_R = 6.5


def _blade_top():
    """拉桿片頂面：最粗車把的夾環底（在樞軸轂最靠近車把那一點）再往下 FIT。"""
    y = PIVOT[1] - _HUB_R
    ring_bottom = -math.sqrt(max(_R_O_MAX ** 2 - y ** 2, 0.0))
    return ring_bottom - FIT


def plate_z():
    bt = _blade_top()
    up = (bt + FIT, bt + FIT + PLATE_T)
    lo = (bt - BLADE_T - FIT - PLATE_T, bt - BLADE_T - FIT)
    return up, lo


LEVER_Z = _blade_top() - BLADE_T / 2


# ── 幾何小工具 ───────────────────────────────────────────────────
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


def pull_deg_for(mm):
    lo, hi = 0.0, 89.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if cable_pull(mid) < mm:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


PULL_DEG = pull_deg_for(PULL_MM)
AY = PIVOT[1] + HORN
JOINT = (STOP_X[0] + 5.0, AY - 8.0)          # 上下件第二支 M4（線管座內，避開線管頭座孔）
POST = (PIVOT[0] + _HUB_R + FIT + 1.8, AY - 6.0)   # 靜止擋：線頭臂靠在這


def plate_outline():
    """夾板外形：樞軸、線頭臂掃過的範圍（含拉到底＋3°）、線管座。"""
    a_full = anchor_at(PULL_DEG + 3.0)
    x_out = a_full[0] - NIPPLE_D / 2 - 3.0
    return [(PIVOT[0] - 8.0, PIVOT[1] - 7.0), (STOP_X[0], PIVOT[1] - 7.0), (STOP_X[1], AY - 10.0),
            (STOP_X[1], AY + 10.0), (x_out, AY + 10.0), (x_out, a_full[1] - 6.0), (PIVOT[0] - 8.0, PIVOT[1] + 2.0)]


def mount_upper_body(bar_d=22.2):
    """上件：夾環＋鎖緊耳＋上夾板。平面朝下免支撐列印。"""
    r_i = bar_d / 2 + BAR_FIT / 2
    r_o = r_i + WALL
    up, _ = plate_z()
    ring = xcyl(r_o, -CLAMP_W / 2, CLAMP_W / 2)
    ears = box(-CLAMP_W / 2, CLAMP_W / 2, -(SPLIT / 2 + 4.0), SPLIT / 2 + 4.0, r_i - 1.0, r_o + 7.0)
    neck = box(-CLAMP_W / 2, CLAMP_W / 2, 4.0, PIVOT[1] - 1.0, up[0], -r_i + 1.0)
    body = ring + ears + neck + xy_prism(plate_outline(), *up)
    body &= box(-80, 80, -80, 80, up[0], 80)                              # 底面切平
    body -= xcyl(r_i, -60, 60)                                            # 車把孔
    body -= box(-CLAMP_W, CLAMP_W, -SPLIT / 2, SPLIT / 2, 0.0, r_o + 20)  # 上方鎖緊縫
    zb = r_o + 3.5
    body -= ycyl(HOLE_M4 / 2, -12, 12, z=zb)                              # M4×16 鎖緊螺絲
    body -= bd.Pos(0, SPLIT / 2 + 4.0 - 3.4, zb) * bd.Rot(-90, 0, 0) * bd.extrude(
        bd.RegularPolygon(NUT_AF / 2, 6, major_radius=False), 4.0)       # 螺帽槽
    body -= zcyl(HOLE_M4 / 2, up[0] - 1, up[1] + 1, *PIVOT)               # M4 樞軸
    body -= zcyl(HOLE_M4 / 2, up[0] - 1, up[1] + 1, *JOINT)               # M4 接合
    a_full = anchor_at(PULL_DEG + 3.0)                                    # 線頭安裝孔
    body -= zcyl(NIPPLE_D / 2 + 0.6, up[0] - 1, up[1] + 1, *a_full)
    body.label = "estop_lever_mount_upper"
    body.color = GREY
    return body


def mount_lower_body():
    """下件：下夾板＋線管座＋前牆＋靜止柱，高度到上板底面。平面朝下免支撐列印。"""
    up, lo = plate_z()
    x_out = plate_outline()[4][0]
    stop_blk = box(STOP_X[0], STOP_X[1], AY - 12.0, AY + 10.0, lo[0], up[0])
    front_wall = box(x_out, STOP_X[1], AY + 7.0, AY + 10.0, lo[0], up[0])
    post = zcyl(1.8, lo[0], up[0], *POST)
    body = xy_prism(plate_outline(), *lo) + stop_blk + front_wall + post
    body -= zcyl(HOLE_M4 / 2, lo[0] - 1, up[0] + 1, *PIVOT)               # M4 樞軸
    body -= zcyl(HOLE_M4 / 2, lo[0] - 1, up[0] + 1, *JOINT)               # M4 接合
    # 線管座：線管頭從內側頂住，內線往外穿到線頭
    zc = LEVER_Z
    body -= xcyl(FERRULE_D / 2, STOP_X[1] - 6.0, STOP_X[1] + 1, y=AY, z=zc)
    body -= xcyl(WIRE_SLOT / 2, STOP_X[0] - 1, STOP_X[1] - 5.9, y=AY, z=zc)
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
    bt = _blade_top()
    z0, z1 = bt - BLADE_T, bt
    zc = (z0 + z1) / 2
    d = rot((1.0, 0.0), BLADE_REST_DEG + pull_deg)
    tip = (PIVOT[0] + d[0] * BLADE_LEN, PIVOT[1] + d[1] * BLADE_LEN)
    A = anchor_at(pull_deg)
    blade = taper(PIVOT, _HUB_R, tip, 5.0, z0, z1) + taper(PIVOT, _HUB_R, A, 6.0, z0, z1)
    blade -= zcyl(HOLE_M4 / 2, z0 - 1, z1 + 1, *PIVOT)
    blade -= zcyl(NIPPLE_D / 2, z0 - 1, z1 + 1, *A)
    # 內線從線頭往線管座（+X）穿出；整個行程都要讓得開 → 本體座標 0° 到 −(行程＋5°) 扇形開口
    span = PULL_DEG + 5.0
    for k in range(5):
        a = -span * k / 4
        u = rot((1.0, 0.0), a + pull_deg)
        mid = (A[0] + u[0] * 6.0, A[1] + u[1] * 6.0)
        blade -= bd.Pos(mid[0], mid[1], zc) * bd.Rot(0, 0, math.degrees(math.atan2(u[1], u[0]))) * bd.Box(
            12.0, WIRE_SLOT, BLADE_T + 2)
    # 手指止滑紋（拉桿片朝騎士那一側）
    n = rot((0.0, -1.0), BLADE_REST_DEG + 180.0 + pull_deg)
    for k in range(4):
        s = 24.0 + 6.5 * k
        c = (PIVOT[0] + d[0] * s + n[0] * 5.6, PIVOT[1] + d[1] * s + n[1] * 5.6)
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
    up, lo = plate_z()
    print(f"拉 {PULL_DEG:.1f}° → 線行程 {cable_pull(PULL_DEG):.1f} mm；上板 Z {up[0]:.1f}~{up[1]:.1f}、拉桿片 Z {LEVER_Z - BLADE_T / 2:.1f}~{LEVER_Z + BLADE_T / 2:.1f}、下板 Z {lo[0]:.1f}~{lo[1]:.1f}")
    estop_lever_222()
    estop_lever_222_pulled()
