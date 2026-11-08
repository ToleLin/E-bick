"""用實際 CAD 幾何算：各車型的滾輪正向力 N（氣壓棒 F1 = 200/250/300 N）、驅動時 dN/dF、
允許的最大驅動力（乾 μ=0.6、濕 μ=0.3）、扳下抬臂桿的最大手力。

執行：cadgen +0.8.3 run src/forces.py
"""
import math

import build123d as bd

import params as P
import unit as U
from bikes import bike_geom, bike_to_housing, solve_arm_angle

M_ARM = 1.23            # 馬達 0.98 + 擺臂 0.20 + 滾輪套 0.05 kg
R_CG = 210.0            # 重心離樞軸
PROG = 0.15             # 氣壓棒全行程壓縮時力量增加 15%（一般規格 10–30%）


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def unit2(v):
    l = math.hypot(*v)
    return (v[0] / l, v[1] / l)


def gs_force(F1, length):
    x = max(0.0, P.GS_LEN - length)
    return F1 * (1 + PROG * x / P.GS_STROKE)


def pin_at(deg):
    _, _, Cc, _ = P.spring_points()
    return (Cc[0] + P.CRANK_R * math.cos(math.radians(deg)), Cc[1] + P.CRANK_R * math.sin(math.radians(deg))), Cc


def analyse(row, F1):
    g = bike_geom(row)
    phi, W = solve_arm_angle(g)
    L = bike_to_housing(g)
    dvec = (L * bd.Location((0, 0, -1))).position - (L * bd.Location((0, 0, 0))).position
    gdir = unit2((dvec.X, dvec.Z))
    Pv = P.PIVOT
    M = P.motor_center(phi)
    d = P.arm_dir(phi)
    B = (Pv[0] + P.SPRING_D * d[0], Pv[1] + P.SPRING_D * d[1])
    pin, _ = pin_at(U.CRANK_ENGAGED_DEG)
    Ls = math.hypot(pin[0] - B[0], pin[1] - B[1])
    Fs = gs_force(F1, Ls)
    fdir = unit2((B[0] - pin[0], B[1] - pin[1]))
    m_spring = cross((B[0] - Pv[0], B[1] - Pv[1]), (Fs * fdir[0], Fs * fdir[1]))
    cg = (Pv[0] + R_CG * d[0], Pv[1] + R_CG * d[1])
    wgt = M_ARM * 9.81
    m_grav = cross((cg[0] - Pv[0], cg[1] - Pv[1]), (wgt * gdir[0], wgt * gdir[1]))
    n = unit2((M[0] - W[0], M[1] - W[1]))
    C = (W[0] + g["R"] * n[0], W[1] + g["R"] * n[1])
    lever = (C[0] - Pv[0], C[1] - Pv[1])
    m_n = cross(lever, n)
    # 胎面運動方向：車往前（主機座標裡大致往 −X），胎頂表面往前 → 切線取讓胎頂往 −X 的方向
    t = unit2((-n[1], n[0]))
    if t[0] > 0:
        t = (-t[0], -t[1])
    m_t = cross(lever, (-t[0], -t[1]))
    N0 = -(m_spring + m_grav) / m_n
    k = -m_t / m_n
    Fmax = {mu: N0 / (1 / mu - k) for mu in (0.6, 0.3)}
    return g["name"], phi, Ls, Fs, N0, k, Fmax


def hand_force(row, F1):
    """從抬起位置扳回工作位置的過程中，把手末端需要的最大力（N）。"""
    g = bike_geom(row)
    phi_c, _ = solve_arm_angle(g)
    d = P.arm_dir(phi_c)
    B = (P.PIVOT[0] + P.SPRING_D * d[0], P.PIVOT[1] + P.SPRING_D * d[1])
    worst = 0.0
    a0 = U.CRANK_ENGAGED_DEG + U.CRANK_TRAVEL_DEG
    for i in range(0, 1861):
        deg = a0 - i * 0.1
        pin, Cc = pin_at(deg)
        Ls = math.hypot(pin[0] - B[0], pin[1] - B[1])
        if Ls >= P.GS_LEN:
            continue                       # 還沒碰到輪胎，氣壓棒沒受壓
        Fs = gs_force(F1, Ls)
        fdir = unit2((pin[0] - B[0], pin[1] - B[1]))      # 氣壓棒推曲柄銷的方向
        tq = cross((pin[0] - Cc[0], pin[1] - Cc[1]), (Fs * fdir[0], Fs * fdir[1]))
        worst = max(worst, abs(tq) / U.HANDLE_LEN)
    return worst


if __name__ == "__main__":
    for F1 in (200.0, 250.0, 300.0):
        print(f"\n氣壓棒 F1 = {F1:.0f} N")
        print("車型            擺臂角  氣壓棒長 推力   正向力N  dN/dF  最大驅動力 乾/濕   扳桿手力")
        for row in P.BIKES:
            name, phi, Ls, Fs, N0, k, Fm = analyse(row, F1)
            hf = hand_force(row, F1)
            print(f"{name:<14} {phi:+6.1f}° {Ls:6.1f}  {Fs:5.0f}  {N0:6.0f}   {k:+.2f}   {Fm[0.6]:4.0f} / {Fm[0.3]:3.0f} N   {hf:4.0f} N")
