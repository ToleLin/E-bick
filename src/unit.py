"""主機（換車共用的那一台）：前段殼、後段殼、電控艙蓋、擺臂、抬臂偏心桿、TPU 滾輪套，
以及外購件的佔位模型（6374 馬達、氣壓棒、608 軸承、VESC、ESP32、牧田電池與座）。

全部用主機座標（見 params.py）：+X 往車尾、+Z 沿座管往上、+Y 車左。
"""
import math

import build123d as bd
from cadgen import model

import params as P
from params import (ARM_H, ARM_PHI0, ARM_Y, BAY_X, BAY_Y, BAY_Z, BRG_FIT, BRG_OD, BRG_W, CHEEK_Y_IN, CHEEK_Y_OUT,
                    CRANK_R, DECK_Z, DOVE_ANGLE, DOVE_CLR, DOVE_DEPTH, DOVE_LEN, DOVE_ROOT_X, DOVE_W_ROOT,
                    DOVE_W_TIP, GS_BODY_D, GS_EYE_W, GS_ROD_D, HUB_D, HUB_Y, JOINT_X, M5_CLR, M5_HEAD_D,
                    M5_NUT_AF, M5_NUT_T, MOTOR_CAN_Y, MOTOR_D, MOTOR_FACE_Y, MOTOR_PCD_SLOT, PIVOT, QR_PIN_D,
                    QR_PIN_X, QR_PIN_Z, REAR_X_END, RECV_X, RECV_Y, RECV_Z, ROLLER_R, SHAFT_D, SHAFT_OUT,
                    SHAFT_STEP_D, SHAFT_STEP_L, SLEEVE_T, SPRING_Y, WALL)

PETG_CF = "#3a3d42"
PETG_HF = "#c9d44a"      # 亮綠黃，抬臂桿與擋泥罩重點色
TPU = "#2f6f9f"
METAL = "#9aa3ad"
BLACK = "#202020"


# ── 幾何小工具 ───────────────────────────────────────────────────
def box(x0, x1, y0, y1, z0, z1):
    return bd.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * bd.Box(x1 - x0, y1 - y0, z1 - z0)


def ycyl(r, y0, y1, x=0.0, z=0.0):
    c = bd.Cylinder(r, y1 - y0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return bd.Pos(x, y1, z) * bd.Rot(90, 0, 0) * c


def xcyl(r, x0, x1, y=0.0, z=0.0):
    c = bd.Cylinder(r, x1 - x0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return bd.Pos(x0, y, z) * bd.Rot(0, 90, 0) * c


def zcyl(r, z0, z1, x=0.0, y=0.0):
    return bd.Pos(x, y, z0) * bd.Cylinder(r, z1 - z0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def ccw(pts):
    """頂點排成逆時針：擠出方向才會照面法線 +Z（順時針會擠到反方向）。"""
    area = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
    return list(pts) if area > 0 else list(pts)[::-1]


def xz_prism(pts, y0, y1):
    """XZ 平面上的多邊形（點 = (x, z)），沿 Y 從 y0 擠到 y1。"""
    face = bd.Polygon(*ccw(pts), align=None)
    return bd.Pos(0, y1, 0) * bd.Rot(90, 0, 0) * bd.extrude(face, y1 - y0)


def xz_stadium(c0, c1, r, y0, y1):
    """兩圓心 c0、c1、半徑 r 的長圓形板（XZ），沿 Y 擠出。"""
    dx, dz = c1[0] - c0[0], c1[1] - c0[1]
    L = math.hypot(dx, dz)
    ang = math.degrees(math.atan2(dz, dx))
    s = ycyl(r, y0, y1, *c0) + ycyl(r, y0, y1, *c1)
    mid = ((c0[0] + c1[0]) / 2, (c0[1] + c1[1]) / 2)
    bar = bd.Pos(mid[0], (y0 + y1) / 2, mid[1]) * bd.Rot(0, -ang, 0) * bd.Box(L, y1 - y0, 2 * r)
    return s + bar


def rot_xz(v, deg):
    a = math.radians(deg)
    return (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a))


def add(a, b, s=1.0):
    return (a[0] + s * b[0], a[1] + s * b[1])


# ── 燕尾母槽 ─────────────────────────────────────────────────────
def dovetail_slot():
    slope = (DOVE_W_TIP - DOVE_W_ROOT) / 2 / DOVE_DEPTH      # 每 1 mm 深度半寬增加量
    x0, x1 = DOVE_ROOT_X - 1.0, DOVE_ROOT_X + DOVE_DEPTH + DOVE_CLR
    hw0 = DOVE_W_ROOT / 2 - slope * 1.0 + DOVE_CLR / math.sin(math.radians(DOVE_ANGLE))
    hw1 = DOVE_W_TIP / 2 + DOVE_CLR / math.sin(math.radians(DOVE_ANGLE))
    prof = bd.Polygon((x0, -hw0), (x1, -hw1), (x1, hw1), (x0, hw0), align=None)
    z_top = DOVE_LEN / 2 + 0.2
    return bd.Pos(0, 0, -80) * bd.extrude(prof, 80 + z_top)


# ── 主機前段：燕尾母槽＋電控艙＋樞軸耳板 ──────────────────────────
def front_housing_body():
    x_r0, x_r1 = RECV_X
    z_r0 = QR_PIN_Z - 9.0
    recv = box(x_r0, x_r1, RECV_Y[0], RECV_Y[1], z_r0, RECV_Z[1])
    bay_outer = box(BAY_X[0], BAY_X[1], BAY_Y[0], BAY_Y[1], BAY_Z[0], BAY_Z[1])
    # 樞軸支架：內外兩片耳板＋上方橫樑（跨過擺臂轂）
    px, pz = PIVOT
    cheeks = None
    for y0, y1 in (CHEEK_Y_IN, CHEEK_Y_OUT):
        c = xz_stadium((px, pz), (px, BAY_Z[0] + 5), 18.0, y0, y1)
        cheeks = c if cheeks is None else cheeks + c
    bridge = box(px - 22, px + 22, CHEEK_Y_IN[0], CHEEK_Y_OUT[1], -42.0, BAY_Z[0] + 6)
    body = recv + bay_outer + cheeks + bridge
    # 電控艙挖空（頂部開口給艙蓋）
    body -= box(BAY_X[0] + WALL, BAY_X[1] - WALL, BAY_Y[0] + WALL, BAY_Y[1] - WALL, BAY_Z[0] + WALL, BAY_Z[1] + 5)
    # 擺臂轂與箱型樑的活動空間（耳板之間）
    body -= box(px - 40, px + 60, CHEEK_Y_IN[1], CHEEK_Y_OUT[0], -120, -42.0)
    body -= ycyl(HUB_D / 2 + 1.5, CHEEK_Y_IN[1], CHEEK_Y_OUT[0], px, pz)
    # 燕尾母槽與快拆銷
    body -= dovetail_slot()
    body -= ycyl(QR_PIN_D / 2, RECV_Y[0] - 5, RECV_Y[1] + 5, QR_PIN_X, QR_PIN_Z)
    body -= box(x_r0 - 1, x_r1 + 1, RECV_Y[0] - 1, -24.0, z_r0 - 1, BAY_Z[0])     # 右側凹口放銷頭 → 有效長 60 mm
    # 樞軸 M8 孔
    body -= ycyl(8.3 / 2, CHEEK_Y_IN[0] - 5, CHEEK_Y_OUT[1] + 5, px, pz)
    # 馬達線穿線孔（艙底靠樞軸處）、開關孔（右側牆）
    body -= zcyl(7.0, BAY_Z[0] - 30, BAY_Z[0] + WALL + 1, x=px + 34, y=22.0)
    body -= ycyl(8.1, BAY_Y[0] - 2, BAY_Y[0] + WALL + 2, x=75.0, z=5.0)     # 16 mm 輔助總開關（切 ESP32 5V）
    body -= ycyl(6.1, BAY_Y[0] - 2, BAY_Y[0] + WALL + 2, x=102.0, z=5.0)    # 12 mm 段位按鍵
    body -= ycyl(2.6, BAY_Y[0] - 2, BAY_Y[0] + WALL + 2, x=122.0, z=5.0)    # 5 mm 指示燈
    # 後接合面 4×M5（螺絲頭在艙內）
    for y, z in joint_holes():
        body -= xcyl(M5_CLR / 2, BAY_X[1] - WALL - 2, BAY_X[1] + 2, y=y, z=z)
    body -= xcyl(6.0, BAY_X[1] - WALL - 2, BAY_X[1] + 2, y=-28.0, z=4.0)     # 電池線穿過接合牆
    # 艙蓋 M3 熱壓螺母柱（6 處）
    for x, y in lid_screws():
        body += zcyl(4.5, BAY_Z[0] + WALL, BAY_Z[1], x=x, y=y)
        body -= zcyl(2.0, BAY_Z[1] - 8, BAY_Z[1] + 1, x=x, y=y)
    # VESC 束帶槽（艙底）
    for x in (130.0, 175.0):
        for y in (-42.0, -0.5):
            body -= box(x - 2, x + 2, y - 1.5, y + 1.5, BAY_Z[0] - 1, BAY_Z[0] + WALL + 1)
    # 緊急停止線管扣（外耳板外側）：每台車的線管從座管這邊卡進來，再往後接到塔外牆的線管座
    clip = box(120.0, 130.0, CHEEK_Y_OUT[1] - 0.01, CHEEK_Y_OUT[1] + 9.0, -37.0, -23.0)
    clip -= xcyl(2.8, 119.0, 131.0, y=CHEEK_Y_OUT[1] + 5.0, z=-30.0)
    clip -= box(119.0, 131.0, CHEEK_Y_OUT[1] + 2.9, CHEEK_Y_OUT[1] + 7.1, -30.0, -22.0)     # 4.2 寬開口，Ø5 線管壓入
    body += clip
    body.label = "housing_front"
    body.color = PETG_CF
    return body


def joint_holes():
    return ((-38.0, -12.0), (-38.0, 18.0), (26.0, -12.0), (26.0, 18.0))


def lid_screws():
    x0, x1 = RECV_X[1] + 5.5, BAY_X[1] - 8
    y0, y1 = BAY_Y[0] + 7.5, BAY_Y[1] - 7.5
    xm = (x0 + x1) / 2
    return ((x0, y0), (x0, y1), (xm, y1), (x1, y0), (x1, y1))      # 右側中間留給 VESC


def bay_lid_body():
    lid = box(RECV_X[1], BAY_X[1], BAY_Y[0], BAY_Y[1], BAY_Z[1], BAY_Z[1] + 3.0)
    lip = box(BAY_X[0] + WALL + 0.3, BAY_X[1] - WALL - 0.3, BAY_Y[0] + WALL + 0.3, BAY_Y[1] - WALL - 0.3,
              BAY_Z[1] - 2.0, BAY_Z[1] + 0.01)
    lip -= box(BAY_X[0] + WALL + 2.3, BAY_X[1] - WALL - 2.3, BAY_Y[0] + WALL + 2.3, BAY_Y[1] - WALL - 2.3,
               BAY_Z[1] - 3.0, BAY_Z[1] + 0.1)
    for x, y in lid_screws():
        lip -= zcyl(5.2, BAY_Z[1] - 3, BAY_Z[1] + 0.1, x=x, y=y)
    lid += lip
    for x, y in lid_screws():
        lid -= zcyl(1.7, BAY_Z[1] - 5, BAY_Z[1] + 5, x=x, y=y)
        lid -= zcyl(3.1, BAY_Z[1] + 1.5, BAY_Z[1] + 5, x=x, y=y)
    lid.label = "bay_lid"
    lid.color = PETG_CF
    return lid


# ── 主機後段：接合凸緣、擋泥罩、偏心塔、右側電池牆 ────────────────
TOWER_IN, TOWER_OUT = (32.0, 38.0), (68.0, 74.0)
DECK_T = 4.0
DECK_Y = (P.BATT_WALL_Y[0], TOWER_OUT[1])
BATT_X = (228.0, 366.0)
BATT_Z = (-46.0, DECK_Z + DECK_T)      # 牧田座高 71、中心 Z −6 → 下緣 −41.5
DOCK_C = (300.0, -6.0)          # 牧田座中心 (X, Z)，貼在電池牆外側


def rear_housing_body():
    _, _, Cc, n0 = P.spring_points()
    x0 = JOINT_X
    flange = box(x0, x0 + 6, P.BATT_WALL_Y[0], BAY_Y[1], BAY_Z[0], BAY_Z[1])
    # 斜面：凸緣頂 → 擋泥罩
    slope = xz_prism([(x0, BAY_Z[1] - 4), (x0 + 6, BAY_Z[1] - 4), (262.0, DECK_Z), (262.0, DECK_Z + DECK_T),
                      (x0, BAY_Z[1])], DECK_Y[0], DECK_Y[1])
    deck = box(262.0 - 0.01, REAR_X_END, DECK_Y[0], DECK_Y[1], DECK_Z, DECK_Z + DECK_T)
    batt_wall = box(BATT_X[0], BATT_X[1], P.BATT_WALL_Y[0], P.BATT_WALL_Y[1], BATT_Z[0], BATT_Z[1])
    # 電池牆的肋（垂直於牆、在牆外側之外不影響電池座）
    rib = xz_prism([(x0 + 6, BAY_Z[0]), (BATT_X[0], BATT_Z[0]), (BATT_X[0] + 10, BATT_Z[0]), (BATT_X[0] + 10, DECK_Z),
                    (x0 + 6, BAY_Z[1])], P.BATT_WALL_Y[0], P.BATT_WALL_Y[0] + 6)
    # 偏心塔：兩片牆繞偏心中心
    tower = None
    for y0, y1 in (TOWER_IN, TOWER_OUT):
        t = xz_stadium((Cc[0], Cc[1]), (Cc[0] + 10, DECK_Z), 30.0, y0, y1) + box(x0, Cc[0], y0, y1, BAY_Z[1] - 4, Cc[1] + 33)
        tower = t if tower is None else tower + t
    roof = box(Cc[0] - 30, Cc[0] + 30, TOWER_IN[0], TOWER_OUT[1], Cc[1] + 29, Cc[1] + 33)
    # 抬臂桿擋塊（工作位置時桿子靠在這）＋緊急停止觸發桿支架與休止擋；塔外牆的拉線線管座
    stop = estop_bracket(Cc)
    body = flange + slope + deck + batt_wall + rib + tower + roof + stop + estop_cable_stop()
    # 氣壓棒穿過的開口、偏心桿與塔之間的空間
    body -= box(x0 + 6.01, 300.0, TOWER_IN[1], TOWER_OUT[0], -40.0, Cc[1] + 28.9)
    # 偏心軸 M8（穿內牆），外牆開 Ø23 給轂
    body -= ycyl(8.4 / 2, TOWER_IN[0] - 2, TOWER_IN[1] + 1, Cc[0], Cc[1])
    body -= ycyl(22.6 / 2, TOWER_OUT[0] - 1, TOWER_OUT[1] + 1, Cc[0], Cc[1])
    # 接合面 4×M5 螺帽槽
    for y, z in joint_holes():
        body -= xcyl(M5_CLR / 2, x0 - 1, x0 + 12, y=y, z=z)
        body -= box(x0 + 6 - 0.01, x0 + 6 + M5_NUT_T + 0.5, y - M5_NUT_AF / 2, y + M5_NUT_AF / 2, z - 5, z + 5)
    body -= xcyl(6.0, x0 - 1, x0 + 7, y=-28.0, z=4.0)                          # 電池線穿過接合牆
    # 牧田座 4×M5（座中心在 DOCK_C，長邊沿 X）
    for a, b in P.MAKITA_HOLES:
        body -= ycyl(M5_CLR / 2, P.BATT_WALL_Y[0] - 1, P.BATT_WALL_Y[1] + 1, DOCK_C[0] + a, DOCK_C[1] + b)
    # 電池線穿孔
    body -= ycyl(6.0, P.BATT_WALL_Y[0] - 1, P.BATT_WALL_Y[1] + 7, BATT_X[0] + 18, 30.0)
    # 觸發桿軸：M4 熱壓螺母（Ø5.6 × 8），M4×14 從觸發桿外側鎖進來當軸
    kx, kz = P.ESTOP_K
    body -= ycyl(5.6 / 2, P.ESTOP_Y[0] - 8.5, P.ESTOP_Y[0] + 0.01, kx, kz)
    body = estop_cable_stop_cuts(body)
    body.label = "housing_rear"
    body.color = PETG_CF
    return body


# ── 緊急停止（機械式）：主機側 ─────────────────────────────────────
STOP_X = (321.0, 334.0)          # 抬臂把手擋塊：把手工作位置靠在頂面


def estop_bracket(Cc):
    """觸發桿支架（軸在內側、觸發桿在外側的同一平面轉動）、把手擋塊、拉線臂休止擋。"""
    kx, kz = P.ESTOP_K
    y0, y1 = P.ESTOP_Y
    top = Cc[1] - 7.2                                                    # 把手下緣（Cc − 7）再低 0.2
    inboard = box(kx - 6.0, STOP_X[0] + 0.01, 62.0, y0 - 0.5, 56.0, DECK_Z + 0.01)
    stopblk = box(STOP_X[0], STOP_X[1], 62.0, y1, 56.0, top)
    # 休止擋：拉線端的線頭座往後靠在這（沒接線時觸發桿也不會亂晃），觸發時往前離開
    lug = box(kx + 6.8, STOP_X[0] + 3.0, y0, y1, 34.0, 46.0) + box(STOP_X[0], STOP_X[0] + 3.0, y0, y1, 45.9, 56.01)
    return inboard + stopblk + lug


def estop_cable_stop():
    x0, x1 = P.ESTOP_STOP_X
    y, z = P.ESTOP_CABLE_Y, P.ESTOP_CABLE_Z
    return box(x0, x1, TOWER_OUT[1] - 0.01, y + 4.0, z - 6.0, z + 6.0)


def estop_cable_stop_cuts(body):
    """線管頭 Ø6.4 從前方頂住，內線往後穿出；兩段都從外側開縫，線不用拆就能卡進去。"""
    x0, x1 = P.ESTOP_STOP_X
    y, z = P.ESTOP_CABLE_Y, P.ESTOP_CABLE_Z
    body -= xcyl(P.FERRULE_D / 2, x0 - 1, x0 + 6.0, y=y, z=z)
    body -= xcyl(1.1, x0 + 5.9, x1 + 1, y=y, z=z)
    body -= box(x0 - 1, x0 + 6.0, y, y + 10, z - 2.9, z + 2.9)           # 5.8 寬：線管頭 6.0–6.4 壓進去卡住
    body -= box(x0 + 5.9, x1 + 1, y, y + 10, z - 0.8, z + 0.8)           # 內線縫
    return body


def kicker_body(theta=0.0):
    """觸發桿：順時針轉 theta 度。頂墊從下面推抬臂把手，下端拉線臂接剎車線頭（從外側放入）。"""
    K = P.ESTOP_K
    y0, y1 = P.ESTOP_Y

    def rot(v):
        a = math.radians(theta)
        return (v[0] * math.cos(a) + v[1] * math.sin(a), -v[0] * math.sin(a) + v[1] * math.cos(a))

    pad = add(K, rot(P.ESTOP_PAD))
    C1 = add(K, rot((0.0, -P.ESTOP_ARM)))

    def taper(a, ra, b, rb):
        d = (b[0] - a[0], b[1] - a[1])
        L = math.hypot(*d)
        nrm = (-d[1] / L, d[0] / L)
        poly = [add(a, nrm, ra), add(b, nrm, rb), add(b, nrm, -rb), add(a, nrm, -ra)]
        return xz_prism(poly, y0, y1) + ycyl(ra, y0, y1, *a) + ycyl(rb, y0, y1, *b)

    k = taper(K, 6.5, pad, P.ESTOP_PAD_R) + taper(K, 6.5, C1, 5.0)
    k += ycyl(6.6, P.ESTOP_NIPPLE_Y[0], P.ESTOP_NIPPLE_Y[1], *C1)
    k -= ycyl(6.4 / 2, y0 - 1, y1 + 1, *K)          # 套 Ø6×6.0 墊管轉動；M4×14 夾住墊管，不夾觸發桿
    # 線頭槽：Ø6.6 沿 Y、從外側放入；內線從槽往前穿出。扇形開口涵蓋整個轉角（本體座標 180°–216°）
    k -= ycyl(P.NIPPLE_D / 2, P.ESTOP_CABLE_Y - P.NIPPLE_L / 2, P.ESTOP_NIPPLE_Y[1] + 1, *C1)
    ys = (P.ESTOP_CABLE_Y - 1.0 + P.ESTOP_NIPPLE_Y[1] + 1.0) / 2
    yl = P.ESTOP_NIPPLE_Y[1] + 1.0 - (P.ESTOP_CABLE_Y - 1.0)
    for a in (180.0, 192.0, 204.0, 216.0):
        u = rot((math.cos(math.radians(a)), math.sin(math.radians(a))))
        mid = add(C1, u, 6.0)
        ang = math.degrees(math.atan2(u[1], u[0]))
        k -= bd.Pos(mid[0], ys, mid[1]) * bd.Rot(0, -ang, 0) * bd.Box(12.0, yl, 2.2)
    k.label = "estop_kicker"
    k.color = "#d62828"
    return k


# ── 擺臂 ─────────────────────────────────────────────────────────
def arm_body(phi=ARM_PHI0):
    px, pz = PIVOT
    d = P.arm_dir(phi)
    n = (-d[1], d[0])
    M = P.motor_center(phi)
    ang = math.degrees(math.atan2(d[1], d[0]))
    beam_len = P.ARM_L - 40.0
    mid = add(PIVOT, d, beam_len / 2)
    beam = bd.Pos(mid[0], sum(ARM_Y) / 2, mid[1]) * bd.Rot(0, -ang, 0) * bd.Box(beam_len, ARM_Y[1] - ARM_Y[0], ARM_H)
    hub = ycyl(HUB_D / 2, HUB_Y[0], HUB_Y[1], px, pz)
    motor_plate = ycyl(35.0, MOTOR_FACE_Y, MOTOR_FACE_Y + 6.0, *M)
    outer_plate = ycyl(20.0, 61.0, ARM_Y[1], *M)
    # 外側軸承板 ← 樑末端：斜撐
    web = xz_stadium(add(PIVOT, d, beam_len - 10), M, 14.0, 61.0, ARM_Y[1])
    web2 = xz_stadium(add(PIVOT, d, beam_len - 10), M, 14.0, MOTOR_FACE_Y, MOTOR_FACE_Y + 6.0)
    arm = beam + hub + motor_plate + outer_plate + web + web2
    # 樞軸：兩端 608 軸承座＋中間通孔
    arm -= ycyl((BRG_OD + BRG_FIT) / 2, HUB_Y[0] - 1, HUB_Y[0] + BRG_W, px, pz)
    arm -= ycyl((BRG_OD + BRG_FIT) / 2, HUB_Y[1] - BRG_W, HUB_Y[1] + 1, px, pz)
    arm -= ycyl(12.0 / 2, HUB_Y[0], HUB_Y[1], px, pz)
    # 馬達安裝：中心孔、4 條徑向長孔（PCD 30–46，相對臂軸 45°）、外側 608
    arm -= ycyl(14.0, MOTOR_FACE_Y - 1, MOTOR_FACE_Y + 7, *M)
    for k in range(4):
        a = ang + 45 + 90 * k
        u = (math.cos(math.radians(a)), math.sin(math.radians(a)))
        c0 = add(M, u, MOTOR_PCD_SLOT[0] / 2)
        c1 = add(M, u, MOTOR_PCD_SLOT[1] / 2)
        arm -= xz_stadium(c0, c1, 2.2, MOTOR_FACE_Y - 1, MOTOR_FACE_Y + 7)
        arm -= xz_stadium(c0, c1, 4.2, MOTOR_FACE_Y + 6.0 - 0.01, 61.0 - 0.01)   # 螺絲頭/扳手空間
    arm -= ycyl((BRG_OD + BRG_FIT) / 2, 61.0 - 0.01, 61.0 + BRG_W, *M)
    arm -= ycyl(6.5, 60.0, ARM_Y[1] + 1, *M)
    # 氣壓棒下端：樑頂開槽＋M8 銷孔
    B = add(PIVOT, d, P.SPRING_D)
    slot_c = add(B, n, 6.0)
    arm -= bd.Pos(slot_c[0], SPRING_Y, slot_c[1]) * bd.Rot(0, -ang, 0) * bd.Box(26.0, 17.0, ARM_H)
    arm -= ycyl(8.3 / 2, ARM_Y[0] - 1, ARM_Y[1] + 1, *B)
    arm.label = "swing_arm"
    arm.color = PETG_CF
    return arm


# ── 抬臂偏心桿（左右兩片曲柄，中間不穿軸，讓氣壓棒本體在抬起位置能穿過軸心）──
CRANK_ENGAGED_DEG = -76.0        # 工作位置：曲柄銷角度（過死點 6°，氣壓棒把桿子壓在擋塊上）
CRANK_TRAVEL_DEG = 186.0         # 往抬起位置（另一個死點）轉的角度（XZ 平面逆時針）
HANDLE_OFFSET = 76.0             # 把手方向 = 曲柄銷方向 + 76°（工作時朝後水平靠在擋塊上）
HANDLE_LEN = 105.0
CHEEK_IN_Y = (38.5, 43.5)        # 內曲柄片
CHEEK_OUT_Y = (62.5, 67.5)       # 外曲柄片（帶轂與把手）
HANDLE_Y = (TOWER_OUT[1] + 1.0, TOWER_OUT[1] + 6.5)
HEX_AF = 16.0


def hex_y(af, y0, y1, c, rot_deg=0.0):
    """沿 Y 的六角柱（對邊 af），中心 c=(x, z)；轉角跟著曲柄，裝把手時方向唯一對應。"""
    hx = bd.extrude(bd.RegularPolygon(af / 2, 6, major_radius=False), y1 - y0)
    return bd.Pos(c[0], y1, c[1]) * bd.Rot(90, 0, 0) * bd.Rot(0, 0, rot_deg) * hx


def crank_parts(pin_deg=CRANK_ENGAGED_DEG):
    _, _, Cc, _ = P.spring_points()
    u = (math.cos(math.radians(pin_deg)), math.sin(math.radians(pin_deg)))
    pin_c = add(Cc, u, CRANK_R)
    # 內片：圓盤＋曲柄銷耳，中心埋 M8 螺帽，M8×16 從塔內牆外側鎖進來當短軸
    inner = ycyl(13.0, *CHEEK_IN_Y, *Cc) + xz_stadium(Cc, pin_c, 9.0, *CHEEK_IN_Y)
    inner -= ycyl(8.4 / 2, CHEEK_IN_Y[0] - 1, CHEEK_IN_Y[1] + 1, *Cc)
    inner -= bd.Pos(Cc[0], CHEEK_IN_Y[1] - 3.2, Cc[1]) * bd.Rot(90, 0, 0) * bd.extrude(
        bd.RegularPolygon(13.2 / 2, 6, major_radius=False), -3.4)
    inner -= ycyl(8.4 / 2, CHEEK_IN_Y[0] - 1, CHEEK_IN_Y[1] + 1, *pin_c)
    inner.label = "lift_crank_inner"
    inner.color = PETG_HF
    # 外片：圓盤＋銷耳＋穿過塔外牆的 Ø22 轂，轂端六角榫（對邊 16）伸出牆外接把手
    outer = ycyl(13.0, *CHEEK_OUT_Y, *Cc) + xz_stadium(Cc, pin_c, 9.0, *CHEEK_OUT_Y)
    outer += ycyl(11.0, CHEEK_OUT_Y[1] - 0.01, TOWER_OUT[1] + 0.5, *Cc)
    outer += hex_y(HEX_AF, TOWER_OUT[1] + 0.49, HANDLE_Y[1], Cc, pin_deg)
    outer -= ycyl(8.4 / 2, CHEEK_OUT_Y[0] - 1, HANDLE_Y[1] + 1, *Cc)
    outer -= ycyl(8.4 / 2, CHEEK_OUT_Y[0] - 1, CHEEK_OUT_Y[1] + 1, *pin_c)
    # 內側面埋 M8 螺帽（把手的 M8×16 鎖進來，螺絲不會凸進兩片曲柄之間擋到氣壓棒）
    outer -= bd.Pos(Cc[0], CHEEK_OUT_Y[0] + 6.6, Cc[1]) * bd.Rot(90, 0, 0) * bd.extrude(
        bd.RegularPolygon(13.2 / 2, 6, major_radius=False), 6.7)
    outer.label = "lift_crank_outer"
    outer.color = PETG_HF
    # 把手（獨立一件）：六角孔套在轂端，M8×40 從把手外側穿過轂鎖到內側
    h = (math.cos(math.radians(pin_deg + HANDLE_OFFSET)), math.sin(math.radians(pin_deg + HANDLE_OFFSET)))
    tip = add(Cc, h, HANDLE_LEN)
    handle = ycyl(13.0, HANDLE_Y[0], HANDLE_Y[1], *Cc) + xz_stadium(Cc, tip, 7.0, *HANDLE_Y)
    handle += ycyl(9.0, HANDLE_Y[0], HANDLE_Y[1] + 6.0, *tip)
    handle -= hex_y(HEX_AF + 0.3, HANDLE_Y[0] - 1, HANDLE_Y[1] + 1, Cc, pin_deg)
    handle.label = "lift_handle"
    handle.color = PETG_HF
    return inner, outer, handle, pin_c


# ── 列印墊片 ─────────────────────────────────────────────────────
def spacer(od, length, label, bore=8.4):
    s = zcyl(od / 2, 0, length) - zcyl(bore / 2, -1, length + 1)
    s.label = label
    s.color = PETG_HF
    return s


def spacers():
    """樞軸兩顆 608 內圈之間的墊管、氣壓棒上眼兩側（曲柄片間距 19、眼寬 8）、下眼兩側（槽寬 17）。"""
    pivot_len = (HUB_Y[1] - P.BRG_W) - (HUB_Y[0] + P.BRG_W)
    top = (CHEEK_OUT_Y[0] - CHEEK_IN_Y[1] - GS_EYE_W) / 2 - 0.2
    low = (17.0 - GS_EYE_W) / 2 - 0.2
    kick = spacer(6.0, P.ESTOP_Y[1] - P.ESTOP_Y[0] + 0.5, "spacer_kicker", bore=4.4)
    return [spacer(11.5, pivot_len - 0.1, "spacer_pivot"), spacer(12.0, top, "spacer_eye_top"),
            spacer(12.0, low, "spacer_eye_low"), kick]


# ── TPU 滾輪套 ───────────────────────────────────────────────────
def sleeve_body(center=(0.0, 0.0)):
    y0, y1 = MOTOR_CAN_Y[0] + 3.0, MOTOR_CAN_Y[1] - 3.0
    r_in = MOTOR_D / 2 - 0.25
    s = ycyl(ROLLER_R, y0, y1, *center) - ycyl(r_in, y0 - 1, y1 + 1, *center)
    # 30 條軸向排水溝 1.5 寬 × 1 深
    for k in range(30):
        a = 360.0 / 30 * k
        u = (math.cos(math.radians(a)), math.sin(math.radians(a)))
        c = add(center, u, ROLLER_R)
        s -= bd.Pos(c[0], (y0 + y1) / 2, c[1]) * bd.Rot(0, -a, 0) * bd.Box(2.0, y1 - y0 + 2, 1.5)
    s.label = "roller_sleeve"
    s.color = TPU
    return s


# ── 外購件佔位 ───────────────────────────────────────────────────
def motor_6374(center):
    can = ycyl(MOTOR_D / 2, MOTOR_CAN_Y[0], MOTOR_CAN_Y[1], *center)
    stator = ycyl(MOTOR_D / 2 - 1, MOTOR_CAN_Y[1], MOTOR_FACE_Y, *center)
    step = ycyl(SHAFT_STEP_D / 2, MOTOR_FACE_Y, MOTOR_FACE_Y + SHAFT_STEP_L, *center)
    shaft = ycyl(SHAFT_D / 2, MOTOR_FACE_Y, MOTOR_FACE_Y + SHAFT_OUT, *center)
    boss = bd.Pos(center[0], MOTOR_FACE_Y - 4, center[1]) * bd.Rot(0, -180 - 20, 0) * bd.Pos(MOTOR_D / 2, 0, 0) * bd.Box(12, 8, 14)
    m = can + stator + step + shaft + boss
    m.label = "motor_6374"
    m.color = "#5b6470"
    return m


def bearing_608(c, y0):
    b = ycyl(BRG_OD / 2, y0, y0 + BRG_W, *c) - ycyl(4.0, y0 - 1, y0 + BRG_W + 1, *c)
    b.label = "bearing_608"
    b.color = METAL
    return b


def gas_spring(A, B):
    """A = 上眼、B = 下眼（XZ），中心面 Y = SPRING_Y。"""
    dx, dz = A[0] - B[0], A[1] - B[1]
    L = math.hypot(dx, dz)
    u = (dx / L, dz / L)
    ang = math.degrees(math.atan2(dz, dx))
    body_len = 52.0
    def seg(p0, p1, r):
        m = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
        l = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        return bd.Pos(m[0], SPRING_Y, m[1]) * bd.Rot(0, 90 - ang, 0) * bd.Cylinder(r, l)
    eye_b = ycyl(7.0, SPRING_Y - GS_EYE_W / 2, SPRING_Y + GS_EYE_W / 2, *B) - ycyl(4.0, 0, 100, *B)
    eye_a = ycyl(7.0, SPRING_Y - GS_EYE_W / 2, SPRING_Y + GS_EYE_W / 2, *A) - ycyl(4.0, 0, 100, *A)
    p_body0 = add(B, u, 8.0)
    p_body1 = add(B, u, 8.0 + body_len)
    gs = eye_b + eye_a + seg(p_body0, p_body1, GS_BODY_D / 2) + seg(p_body1, add(A, u, -7.0), GS_ROD_D / 2)
    gs.label = "gas_spring"
    gs.color = BLACK
    return gs


def vesc_box():
    v = box(120.0, 120.0 + P.VESC_DIM[0], -41.0, -41.0 + P.VESC_DIM[1], BAY_Z[0] + WALL, BAY_Z[0] + WALL + P.VESC_DIM[2])
    v.label = "vesc_mks_mini67"
    v.color = "#1d4fa0"
    return v


def esp_board():
    e = box(58.0, 58.0 + P.ESP_DIM[0], -40.0, -40.0 + P.ESP_DIM[1], BAY_Z[0] + WALL + 2, BAY_Z[0] + WALL + 2 + P.ESP_DIM[2])
    e.label = "esp32_c3_supermini"
    e.color = "#2a7d3c"
    return e


def makita_dock_and_battery():
    L, W, T = P.MAKITA_DOCK
    y0 = P.BATT_WALL_Y[0]
    dock = box(DOCK_C[0] - L / 2, DOCK_C[0] + L / 2, y0 - T, y0, DOCK_C[1] - W / 2, DOCK_C[1] + W / 2)
    dock.label = "makita_dock_cc0"
    dock.color = PETG_CF
    batt = box(DOCK_C[0] - 115 / 2, DOCK_C[0] + 115 / 2, y0 - T - 68, y0 - T, DOCK_C[1] - 38, DOCK_C[1] + 38)
    batt.label = "makita_battery_18v"
    batt.color = "#0f8f8f"
    return dock, batt


# ── 主機組件 ─────────────────────────────────────────────────────
def unit_assembly(phi=ARM_PHI0, engaged=True, crank_deg=None, kicker_deg=0.0):
    """phi：擺臂角度（工作位置 ARM_PHI0，抬起 ARM_PHI0 − ARM_LIFT_DEG）；
    crank_deg：直接指定曲柄銷角度（預設依 engaged）；kicker_deg：緊急停止觸發桿順時針轉角。"""
    M = P.motor_center(phi)
    d = P.arm_dir(phi)
    B = add(PIVOT, d, P.SPRING_D)
    _, _, Cc, _ = P.spring_points()
    pin_deg = CRANK_ENGAGED_DEG if engaged else CRANK_ENGAGED_DEG + CRANK_TRAVEL_DEG
    if crank_deg is not None:
        pin_deg = crank_deg
    crank_in, crank_out, handle, pin_c = crank_parts(pin_deg)
    front, rear, lid = front_housing_body(), rear_housing_body(), bay_lid_body()
    arm = arm_body(phi)
    sleeve = sleeve_body(M)
    motor = motor_6374(M)
    gs = gas_spring(pin_c, B)
    brg = [bearing_608(PIVOT, HUB_Y[0]), bearing_608(PIVOT, HUB_Y[1] - P.BRG_W), bearing_608(M, 61.0)]
    dock, batt = makita_dock_and_battery()
    parts = [front, rear, lid, arm, crank_in, crank_out, handle, sleeve, motor, gs, *brg, vesc_box(), esp_board(), dock, batt,
             kicker_body(kicker_deg)]
    return bd.Compound(children=parts, label="postroller_unit")


@model
def unit():
    return unit_assembly()


@model
def unit_lifted():
    return unit_assembly(ARM_PHI0 - P.ARM_LIFT_DEG, engaged=False)


@model
def unit_estop_tripped():
    """緊急停止拉桿拉到底的瞬間：觸發桿轉 32.4°，把手被頂到過死點 16°（之後氣壓棒會自己把它推到抬起）。"""
    return unit_assembly(crank_deg=CRANK_ENGAGED_DEG + P.ESTOP_HANDLE_DEG, kicker_deg=P.ESTOP_TRIP_DEG)


if __name__ == "__main__":
    unit()
    unit_lifted()
    unit_estop_tripped()
