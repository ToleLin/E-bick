"""緊急停止拉桿（機械式）檢查：觸發桿轉動時把手被頂到幾度、各零件干涉、休止擋間隙、主機端拉線行程。

執行：cadgen +0.8.3 run src/check_estop.py
"""
import itertools
import math

from cadgen.geometry import closest_points, overlap_volume

import params as P
import unit as U

HALF, RP = 7.0, P.ESTOP_PAD_R


def rot_cw(v, deg):
    a = math.radians(deg)
    return (v[0] * math.cos(a) + v[1] * math.sin(a), -v[0] * math.sin(a) + v[1] * math.cos(a))


def handle_angle(theta):
    """觸發桿轉 theta 時，把手被頂到的角度（相對工作位置，度）。"""
    _, _, Cc, _ = P.spring_points()
    q = rot_cw(P.ESTOP_PAD, theta)
    Q = (P.ESTOP_K[0] + q[0], P.ESTOP_K[1] + q[1])
    qx, qz = Q[0] - Cc[0], Q[1] - Cc[1]
    R = math.hypot(qx, qz)
    a = math.atan2(qz, qx) + math.asin((HALF + RP) / R)
    return max(0.0, math.degrees(a))


def cable_pull(theta):
    S = (P.ESTOP_STOP_X[1], P.ESTOP_CABLE_Z)
    c0 = (P.ESTOP_K[0], P.ESTOP_K[1] - P.ESTOP_ARM)
    c = rot_cw((0.0, -P.ESTOP_ARM), theta)
    C = (P.ESTOP_K[0] + c[0], P.ESTOP_K[1] + c[1])
    return math.hypot(c0[0] - S[0], c0[1] - S[1]) - math.hypot(C[0] - S[0], C[1] - S[1])


def overlaps(asm, focus=None):
    parts = [(p.label, p) for p in asm.children]
    bad = []
    for (la, a), (lb, b) in itertools.combinations(parts, 2):
        if focus and focus not in (la, lb):
            continue
        if {la, lb} == {"roller_sleeve", "motor_6374"}:
            continue
        ba, bb = a.bounding_box(), b.bounding_box()
        if (ba.max.X < bb.min.X or bb.max.X < ba.min.X or ba.max.Y < bb.min.Y or bb.max.Y < ba.min.Y
                or ba.max.Z < bb.min.Z or bb.max.Z < ba.min.Z):
            continue
        v = overlap_volume(a, b)
        if v > 0.5:
            bad.append((la, lb, round(v, 1)))
    return bad


if __name__ == "__main__":
    print("觸發桿轉角 → 把手角度、主機端拉線行程")
    for th in (0, 5, 10, 15, 20, 25, 30, P.ESTOP_TRIP_DEG, 36, 40):
        print(f"  {th:5.1f}° → 把手 {handle_angle(th):5.1f}°（過死點 {handle_angle(th) - 6:+5.1f}°）  拉線 {cable_pull(th):5.1f} mm")
    print("\n干涉（觸發桿相關，重疊 > 0.5 mm³）")
    for th in (0.0, 10.0, 20.0, P.ESTOP_TRIP_DEG):
        a = handle_angle(th)
        asm = U.unit_assembly(crank_deg=U.CRANK_ENGAGED_DEG + a, kicker_deg=th)
        print(f"  觸發桿 {th:4.1f}°／把手 {a:4.1f}°：", overlaps(asm, "estop_kicker") or "無")
    # 已停止：曲柄到抬起死點、擺臂抬起，拉桿還握著
    asm = U.unit_assembly(P.ARM_PHI0 - P.ARM_LIFT_DEG, engaged=False, kicker_deg=P.ESTOP_TRIP_DEG)
    print("  已停止（把手抬起、拉桿仍握著）：", overlaps(asm, "estop_kicker") or "無")
    # 全部零件（工作位置、觸發桿休止）
    asm = U.unit_assembly()
    print("  工作位置全部零件：", overlaps(asm) or "無")
    parts = {p.label: p for p in asm.children}
    k = parts["estop_kicker"]
    print(f"\n間隙：觸發桿↔後段殼 {closest_points(k, parts['housing_rear']).distance:.2f} mm、"
          f"觸發桿↔擺臂 {closest_points(k, parts['swing_arm']).distance:.2f} mm、"
          f"觸發桿↔把手 {closest_points(k, parts['lift_handle']).distance:.2f} mm")
