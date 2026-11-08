"""8 種代表車型的簡化車架治具（立管、座管束、座管、座墊、後上叉、後輪胎），
以及「座管座＋主機」裝在每台車上的組件。全部換算到主機座標，主機本身完全不動，
只有座管座的款式（傾角／後伸）與夾具高度 s 隨車改變，擺臂角度由滾輪壓到胎面求出。

幾何數字見 params.BIKES（bikeinsights 實車；折疊車為估計）。
"""
import math

import build123d as bd
from cadgen import model

import params as P
import unit as U
from base import base_front_body, base_rear_body, housing_to_post, liner_body

FRAME = "#8a8f96"
RUBBER = "#151515"


def bike_geom(row):
    key, name, bsd, w, cs, drop, sta, st, exposed, post_d, variant, s = row
    R = (bsd + 2 * 0.95 * w) / 2
    W = (math.sqrt(cs ** 2 - drop ** 2), drop)                       # 後軸（五通為原點，X 往後、Z 往上）
    a = math.radians(sta)
    u = (math.cos(a), math.sin(a))
    wv = (math.sin(a), -math.cos(a))
    Q = ((st + s) * u[0], (st + s) * u[1])                           # 夾具中心
    return dict(key=key, name=name, R=R, w=w, W=W, u=u, wv=wv, Q=Q, st=st, exposed=exposed, post_d=post_d,
                variant=variant, s=s, sta=sta)


def bike_to_housing(g):
    """車架座標 → 主機座標 的 Location。"""
    post_in_bike = bd.Location(bd.Plane(origin=(g["Q"][0], 0, g["Q"][1]), x_dir=(g["wv"][0], 0, g["wv"][1]),
                                        z_dir=(g["u"][0], 0, g["u"][1])))
    pitch, reach = P.BASE_VARIANTS[g["variant"]]
    return housing_to_post(pitch, reach).inverse() * post_in_bike.inverse()


def seg_cyl(p0, p1, r):
    v = bd.Vector(*p1) - bd.Vector(*p0)
    return bd.Solid.make_cylinder(r, v.length, bd.Plane(origin=p0, z_dir=v))


def fixture_bike(g):
    """車架座標裡的簡化車架（只畫跟助力器有關的部分）。"""
    u, st, d = g["u"], g["st"], g["post_d"]
    top = (st * u[0], 0, st * u[1])
    seat_tube = seg_cyl((st * 0.55 * u[0], 0, st * 0.55 * u[1]), top, d / 2 + 1.6)
    collar = seg_cyl((top[0] - 18 * u[0], 0, top[2] - 18 * u[1]), top, d / 2 + 6)
    post_top = (top[0] + g["exposed"] * u[0], 0, top[2] + g["exposed"] * u[1])
    post = seg_cyl(top, post_top, d / 2)
    # 座墊：座墊軌道在外露座管頂端，座面約高 45，鼻端朝前
    rx, rz = post_top[0], post_top[2]
    saddle = bd.Pos(rx - 15, 0, rz + 25) * bd.Box(270, 140, 50)
    # 後上叉：立管頂下 25 mm → 後軸，左右分開
    J = (top[0] - 25 * u[0], top[2] - 25 * u[1])
    Wx, Wz = g["W"]
    stays = []
    for sy in (-1, 1):
        stays.append(seg_cyl((J[0], sy * (d / 2 + 6), J[1]), (Wx, sy * 66, Wz), 8.0))
    # 輪胎：圓環，截面半徑 = 胎寬/2
    tire = bd.Pos(Wx, 0, Wz) * bd.Rot(90, 0, 0) * bd.Solid.make_torus(g["R"] - g["w"] / 2, g["w"] / 2)
    parts = {"seat_tube": seat_tube + collar, "seatpost": post, "saddle": saddle, "stay_r": stays[0],
             "stay_l": stays[1], "tire": tire}
    return parts


def solve_arm_angle(g):
    """主機座標裡，滾輪壓到胎面的擺臂角 φ（取胎頂附近那個解）。"""
    L = bike_to_housing(g)
    Wh = L * bd.Location((g["W"][0], 0, g["W"][1]))
    W = (Wh.position.X, Wh.position.Z)
    target = g["R"] + P.ROLLER_R

    def f(phi):
        M = P.motor_center(phi)
        return math.hypot(M[0] - W[0], M[1] - W[1]) - target

    lo, hi = -45.0, 5.0
    if f(lo) * f(hi) > 0:
        raise ValueError(f"{g['name']}：擺臂在 −45°～+5° 碰不到輪胎")
    for _ in range(60):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2, W


def bike_assembly(row):
    g = bike_geom(row)
    L = bike_to_housing(g)
    phi, _ = solve_arm_angle(g)
    unit = U.unit_assembly(phi, engaged=True)
    pitch, reach = P.BASE_VARIANTS[g["variant"]]
    Tinv = housing_to_post(pitch, reach).inverse()
    base = [Tinv * base_front_body(g["post_d"]), Tinv * base_rear_body(g["post_d"], g["variant"]),
            Tinv * liner_body(g["post_d"])]
    for b, lab in zip(base, ("base_front", "base_rear", "liner")):
        b.label = lab
    fx = []
    for lab, shp in fixture_bike(g).items():
        s = L * shp
        s.label = lab
        s.color = RUBBER if lab == "tire" else FRAME
        fx.append(s)
    fixture = bd.Compound(children=fx, label="bike")
    return bd.Compound(children=[unit, bd.Compound(children=base, label="base"), fixture], label=g["key"]), phi


def _m(i):
    asm, _ = bike_assembly(P.BIKES[i])
    return asm


@model
def on_road():
    return _m(0)


@model
def on_gravel():
    return _m(1)


@model
def on_city():
    return _m(2)


@model
def on_mtb29():
    return _m(3)


@model
def on_mtb275():
    return _m(4)


@model
def on_mtb26():
    return _m(5)


@model
def on_minivelo():
    return _m(6)


@model
def on_folding():
    return _m(7)


if __name__ == "__main__":
    for m in (on_road, on_gravel, on_city, on_mtb29, on_mtb275, on_mtb26, on_minivelo, on_folding):
        m()
