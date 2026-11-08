"""8 種車型裝車檢查：主機與座管座各零件到車架治具的最小間隙、重疊，滾輪壓胎，擺臂角與氣壓棒長度。

執行：cadgen +0.8.3 run src/check_bikes.py
"""
import math

from cadgen.geometry import closest_points, overlap_volume

import params as P
from bikes import bike_assembly, bike_geom, solve_arm_angle


def leaves(node, parent=None):
    import build123d as bd
    here = (bd.Location() if parent is None else parent) * node.location
    if node.children:
        for c in node.children:
            yield from leaves(c, here)
    else:
        yield node.located(here)


# 刻意接觸的配對（不算干涉）
CONTACT_OK = {("liner", "seatpost"), ("roller_sleeve", "tire")}
SKIP_FIXTURE = {"saddle"}      # 座墊另外算垂直間隙


def main():
    rows = []
    for row in P.BIKES:
        g = bike_geom(row)
        asm, phi = bike_assembly(row)
        parts = list(leaves(asm))
        fx = [p for p in parts if p.label in ("seat_tube", "seatpost", "saddle", "stay_r", "stay_l", "tire")]
        mine = [p for p in parts if p not in fx and p.label not in ("makita_battery_18v",)]
        batt = [p for p in parts if p.label == "makita_battery_18v"]
        worst = []
        for f in fx:
            if f.label in SKIP_FIXTURE:
                continue
            for m in mine + batt:
                if (m.label, f.label) in CONTACT_OK:
                    continue
                d = closest_points(m, f).distance
                if d < 8.0:
                    v = overlap_volume(m, f) if d == 0 else 0.0
                    worst.append((round(d, 1), m.label, f.label, round(v, 1)))
        tire = [f for f in fx if f.label == "tire"][0]
        sleeve = [m for m in mine if m.label == "roller_sleeve"][0]
        d_roll = closest_points(sleeve, tire).distance
        v_roll = overlap_volume(sleeve, tire)
        saddle = [f for f in fx if f.label == "saddle"][0]
        d_saddle = min(closest_points(m, saddle).distance for m in mine + batt)
        rows.append((g["name"], g["variant"], g["s"], phi, d_roll, v_roll, d_saddle, sorted(worst)[:6]))
    print("車型 | 座管座款式 | 夾具高 s | 擺臂角 | 滾輪-胎間隙/重疊 | 主機離座墊 | 8 mm 內的接近點")
    for name, var, s, phi, dr, vr, ds, worst in rows:
        print(f"{name:<14} {var:<9} s={s:>3}  φ={phi:+6.1f}°  滾輪 {dr:.2f} mm/{vr:.0f} mm³  座墊 {ds:5.1f} mm")
        for w in worst:
            print(f"      {w[1]} ↔ {w[2]}：{w[0]} mm" + (f"（重疊 {w[3]} mm³）" if w[3] else ""))


if __name__ == "__main__":
    main()
