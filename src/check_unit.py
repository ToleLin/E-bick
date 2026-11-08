"""主機干涉檢查：擺臂從工作角兩側到抬起位置，逐角度算零件兩兩重疊體積，並核對氣壓棒長度。

執行：cadgen +0.8.3 run src/check_unit.py
"""
import itertools
import math

import build123d as bd
from cadgen.geometry import overlap_volume

import params as P
import unit as U

INTENDED = {frozenset(p) for p in [("roller_sleeve", "motor_6374")]}   # TPU 套過盈套在外殼上


def solids_of(compound):
    out = []
    for part in compound.children:
        out.append((part.label, part))
    return out


def check(phi, engaged, verbose=True):
    asm = U.unit_assembly(phi, engaged)
    parts = solids_of(asm)
    bad = []
    for (la, a), (lb, b) in itertools.combinations(parts, 2):
        if frozenset((la, lb)) in INTENDED:
            continue
        ba, bb = a.bounding_box(), b.bounding_box()
        if (ba.max.X < bb.min.X or bb.max.X < ba.min.X or ba.max.Y < bb.min.Y or bb.max.Y < ba.min.Y
                or ba.max.Z < bb.min.Z or bb.max.Z < ba.min.Z):
            continue
        v = overlap_volume(a, b)
        if v > 1.0:
            bad.append((la, lb, round(v, 1)))
    return bad


def spring_len(phi, engaged):
    d = P.arm_dir(phi)
    B = (P.PIVOT[0] + P.SPRING_D * d[0], P.PIVOT[1] + P.SPRING_D * d[1])
    _, _, Cc, _ = P.spring_points()
    deg = U.CRANK_ENGAGED_DEG + (0 if engaged else U.CRANK_TRAVEL_DEG)
    pin = (Cc[0] + P.CRANK_R * math.cos(math.radians(deg)), Cc[1] + P.CRANK_R * math.sin(math.radians(deg)))
    return math.hypot(pin[0] - B[0], pin[1] - B[1])


if __name__ == "__main__":
    lo = P.GS_LEN - P.GS_STROKE
    print(f"氣壓棒可用長度 {lo:.0f}–{P.GS_LEN:.0f} mm")
    for phi in (-17.5, -20.0, -22.5):
        L = spring_len(phi, True)
        print(f"  工作 φ={phi:+.1f}°：氣壓棒 {L:.1f} mm（壓縮 {P.GS_LEN - L:.1f}）{'OK' if lo <= L <= P.GS_LEN else '超出行程!'}")
    # 抬起：曲柄到另一個死點時，氣壓棒伸到全長 → 擺臂角
    for phi_c in (-17.5, -20.0, -22.5):
        # 找擺臂角讓氣壓棒 = 全長
        best = min((abs(spring_len(p / 10, False) - P.GS_LEN), p / 10) for p in range(-450, -100))
        print(f"  抬起（任一車）：氣壓棒全長時擺臂角 {best[1]:+.1f}°；該車工作角 {phi_c:+.1f}° → 滾輪抬起約 "
              f"{P.ARM_L * math.radians(phi_c - best[1]):.0f} mm")
        break
    print("\n干涉檢查（重疊 > 1 mm³ 的零件對）")
    cases = [(-14.0, True), (-17.5, True), (-20.0, True), (-22.5, True), (-25.0, True),
             (-29.0, False), (-31.0, False)]
    for phi, eng in cases:
        bad = check(phi, eng)
        state = "工作" if eng else "抬起"
        print(f"  φ={phi:+.1f}° {state}：", "無" if not bad else bad)
