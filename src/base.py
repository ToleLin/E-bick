"""座管座（每台車留一個）＋ TPU 內襯。

座標：座管軸 = Z，夾具中心 = 原點，+X 往車尾，+Y 車左。
後半帶燕尾公頭；燕尾所在的「主機座標」相對座管座標 = T(pitch, reach)：
    繞燕尾根部中心 (DOVE_ROOT_X + reach, 0, 0) 轉 pitch（機尾往下為正），再往後挪 reach。
主機由下往上滑進燕尾，頂到主機母槽的封閉頂端（上止擋）；母槽下方插一支 Ø6 球鎖快拆銷擋住燕尾底面防掉。
"""
import build123d as bd
from cadgen import model

from params import (BACKING_W, BASE_H, BASE_VARIANTS, BASE_WALL, BOLT_Z, BORE_CLR, DOVE_DEPTH, DOVE_LEN,
                    DOVE_ROOT_X, DOVE_W_ROOT, DOVE_W_TIP, EAR_EXTRA, EAR_X, LINER_T, M5_CLR, M5_HEAD_D,
                    M5_HEAD_H, M5_NUT_AF, M5_NUT_T, SPLIT_GAP)

PETG_CF = "#3a3d42"
TPU = "#2f6f9f"
BACKING_T = 8.0


def housing_to_post(pitch, reach):
    """主機座標 → 座管座標。"""
    return (bd.Pos(DOVE_ROOT_X + reach, 0, 0) * bd.Rot(0, pitch, 0) * bd.Pos(-DOVE_ROOT_X, 0, 0))


def bore_r(d):
    return d / 2 + LINER_T + BORE_CLR


def box(x0, x1, y0, y1, z0, z1):
    return bd.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * bd.Box(x1 - x0, y1 - y0, z1 - z0)


def zcyl(r, z0, z1, x=0.0, y=0.0):
    return bd.Pos(x, y, z0) * bd.Cylinder(r, z1 - z0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def xcyl(r, x0, x1, y=0.0, z=0.0):
    c = bd.Cylinder(r, x1 - x0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return bd.Pos(x0, y, z) * bd.Rot(0, 90, 0) * c


def dovetail_male():
    """主機座標裡的燕尾公頭＋背板（背板往前延伸到 x0，之後由呼叫端裁切）。"""
    h = DOVE_LEN / 2
    prof = bd.Polygon((DOVE_ROOT_X - 0.01, -DOVE_W_ROOT / 2), (DOVE_ROOT_X + DOVE_DEPTH, -DOVE_W_TIP / 2),
                      (DOVE_ROOT_X + DOVE_DEPTH, DOVE_W_TIP / 2), (DOVE_ROOT_X - 0.01, DOVE_W_ROOT / 2), align=None)
    dove = bd.Pos(0, 0, -h) * bd.extrude(prof, DOVE_LEN)
    # 底端兩側導角 2 mm，主機好對準
    for sy in (-1, 1):
        cut = bd.Pos(DOVE_ROOT_X + DOVE_DEPTH, sy * DOVE_W_TIP / 2, -h) * bd.Rot(0, 0, 45) * bd.Box(4, 4, 6)
        dove -= cut
    return dove


def ear_bolts(r_i, front):
    """鎖耳的 4 個 M5 孔；前半有沉頭座，後半有側推式螺帽槽。"""
    y_b = r_i + 5.0
    cut = []
    for sy in (-1, 1):
        for z in BOLT_Z:
            cut.append(xcyl(M5_CLR / 2, -EAR_X - 1, EAR_X + 1, y=sy * y_b, z=z))
            if front:
                cut.append(xcyl(M5_HEAD_D / 2, -EAR_X - 1, -EAR_X + M5_HEAD_H, y=sy * y_b, z=z))
            else:
                x0 = 4.0
                y_out = sy * (r_i + 5.0 + EAR_EXTRA + 1)
                cut.append(box(x0, x0 + M5_NUT_T, min(sy * y_b, y_out), max(sy * y_b, y_out),
                               z - M5_NUT_AF / 2, z + M5_NUT_AF / 2))
    return cut


def clamp_ring(r_i):
    r_o = r_i + BASE_WALL
    ring = zcyl(r_o, -BASE_H / 2, BASE_H / 2)
    y_e = r_i + 5.0 + EAR_EXTRA
    ears = box(-EAR_X, EAR_X, -y_e, y_e, -BASE_H / 2, BASE_H / 2)
    return ring + ears


def base_front_body(d):
    r_i = bore_r(d)
    r_o = r_i + BASE_WALL
    part = clamp_ring(r_i) & box(-60, -SPLIT_GAP, -60, 60, -BASE_H, BASE_H)
    # 魔鬼氈扣環（前方），帶子往上綁座墊弓防止整組繞座管轉
    loop = box(-r_o - 8, -r_o + 2, -18, 18, -11, 11) - box(-r_o - 5, -r_o - 1.5, -13.5, 13.5, -20, 20)
    part = part + loop
    part -= zcyl(r_i, -BASE_H, BASE_H)
    for c in ear_bolts(r_i, front=True):
        part -= c
    part.label = "base_front"
    part.color = PETG_CF
    return part


def base_rear_body(d, variant="std"):
    pitch, reach = BASE_VARIANTS[variant]
    r_i = bore_r(d)
    T = housing_to_post(pitch, reach)
    clamp = clamp_ring(r_i) & box(SPLIT_GAP, 60, -60, 60, -BASE_H, BASE_H)
    h = DOVE_LEN / 2
    if reach == 0:
        # 背板往前一路延伸穿過座管位置，裁掉前半與管孔即可
        backing = box(-12, DOVE_ROOT_X, -BACKING_W / 2, BACKING_W / 2, -h, h)
        mount = T * (backing + dovetail_male())
    else:
        # 後伸款：夾具後面與傾斜背板之間用 loft 接起來
        plate = box(DOVE_ROOT_X - BACKING_T, DOVE_ROOT_X, -BACKING_W / 2, BACKING_W / 2, -h, h)
        front_face = (T * plate).faces().sort_by(bd.Axis.X)[0]
        x_c = r_i + 2.0
        rect = bd.Plane.YZ.offset(x_c) * bd.Rectangle(BACKING_W, BASE_H)
        bridge = bd.loft([rect, front_face])
        mount = T * (plate + dovetail_male()) + bridge
    part = clamp + mount
    part &= box(SPLIT_GAP, 300, -100, 100, -200, 200)
    part -= zcyl(r_i, -BASE_H * 3, BASE_H * 3)
    for c in ear_bolts(r_i, front=False):
        part -= c
    part.label = f"base_rear_{variant}"
    part.color = PETG_CF
    return part


def liner_body(d):
    """1 mm TPU 內襯，縱向開 1.5 mm 縫好包上座管。"""
    sleeve = zcyl(d / 2 + LINER_T, -BASE_H / 2, BASE_H / 2) - zcyl(d / 2, -BASE_H, BASE_H)
    sleeve -= box(-d, -d / 2 + 0.5, -0.75, 0.75, -BASE_H, BASE_H)   # 縫在正前方
    sleeve.label = "liner"
    sleeve.color = TPU
    return sleeve


def base_assembly(d, variant):
    front, rear, liner = base_front_body(d), base_rear_body(d, variant), liner_body(d)
    return bd.Compound(children=[front, rear, liner], label=f"base_{d}_{variant}")


@model
def base_272_std():
    return base_assembly(27.2, "std")


@model
def base_316_mtb():
    return base_assembly(31.6, "mtb")


@model
def base_272_minivelo():
    return base_assembly(27.2, "minivelo")


if __name__ == "__main__":
    base_272_std()
    base_316_mtb()
    base_272_minivelo()
