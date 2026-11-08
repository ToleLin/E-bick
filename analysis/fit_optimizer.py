"""找主機的擺臂樞軸位置與臂長，讓一台主機適用多種車型。

車型幾何：bikeinsights 實際車款（研究報告 bike_standards.md 2-2），折疊車為估計。
座管座（夾具）可以裝在外露座管的任意高度 s（夾具中心離立管上緣的距離）。
在主機座標（u = 沿座管往上、wv = 垂直座管往後）裡，樞軸位置 = 夾具中心 + bp·wv − dp·u。
要求：接觸角 θ 在胎頂前 CONTACT_MIN～CONTACT_MAX 度（避開後上叉／框煞橋，又不越過「樞軸–輪軸」線）。
輸出：每台車可用的夾具高度範圍、擺臂角度；全部車型需要的擺角範圍越小越好。
"""
import math
from contact_mechanics import *

R_ROLL = 34.5
CONTACT_MIN, CONTACT_MAX = -8.0, 14.0
# name, BSD, 胎寬, CS, drop, STA(實際座管角), ST(C-T), 外露座管
BIKES = [
    ("公路 Allez56 700x28", 622, 28, 425, 76, 73.25, 530, 143),
    ("礫石 Grizl M 700x40", 622, 40, 435, 75, 73.5, 522, 124),
    ("城市 FX2 M 700x35", 622, 35, 450, 65, 74.0, 445, 200),
    ("29 Marlin7 M 29x2.3", 622, 58, 438, 60, 72.0, 420, 220),
    ("27.5 Marlin7 S 27.5x2.4", 584, 61, 438, 48, 72.0, 368, 220),
    ("26 Hardrock M 26x1.95", 559, 50, 424.5, 41, 73.0, 444, 200),
    ("小徑 D20 L 20x1.75", 406, 44, 390, -30, 73.0, 460, 180),
    ("折疊 估計 20x1.75", 406, 44, 400, -30, 70.0, 360, 295),
]
S_LO = 40.0            # 夾具中心至少離立管上緣 40 mm
TOP_RESERVE = 75.0     # 夾具中心以上要留給主機頂部與座墊的空間

def angle_from(v, ref, up):
    """v 相對 ref 的角度，往 −up（往下）轉為正。"""
    a = math.atan2(cross(ref, v), ref[0]*v[0] + ref[1]*v[1])
    return -math.degrees(a) if cross(ref, up) > 0 else math.degrees(a)

def evaluate(bp, dp, L, verbose=False):
    per = []
    for b in BIKES:
        name, bsd, w, cs, drop, sta, st, exposed = b
        R, W, u, wv = bike_frame(bsd, w, cs, drop, sta)
        ok = []
        s = S_LO
        while s <= exposed - TOP_RESERVE + 1e-6:
            Q = (( st + s) * u[0], (st + s) * u[1])
            P = add(add(Q, mul(wv, bp)), mul(u, -dp))
            M = solve_contact(P, L, W, R, R_ROLL)
            if M:
                f = forces(P, M, W, R)
                if CONTACT_MIN <= f["contact_deg"] <= CONTACT_MAX:
                    phi = angle_from(sub(M, P), wv, u)
                    ok.append((s, f["contact_deg"], phi, f["k"]))
            s += 2.0
        per.append((name, ok))
    return per

def score(per):
    if any(not ok for _, ok in per):
        return None
    # 每台車選讓擺角最接近共同中心的夾具高度：用貪婪法求最小擺角範圍
    phis = [sorted(o[2] for o in ok) for _, ok in per]
    lo = max(p[0] for p in phis); hi = min(p[-1] for p in phis)
    if lo <= hi:
        return 0.0, (lo + hi) / 2
    # 沒有共同角度 → 需要的範圍 = 把每台車拉到最近的區間
    best = None
    cands = sorted(set(x for p in phis for x in p))
    for c in cands:
        need_lo = min(min(p, key=lambda x: abs(x - c)) for p in phis)
        need_hi = max(min(p, key=lambda x: abs(x - c)) for p in phis)
        span = need_hi - need_lo
        if best is None or span < best[0]:
            best = (span, c)
    return best

if __name__ == "__main__":
    best = None
    for bp in range(30, 91, 10):
        for dp in range(-20, 81, 10):
            for L in range(140, 321, 10):
                sc = score(evaluate(bp, dp, L))
                if sc is None:
                    continue
                key = (round(sc[0], 1), L)
                if best is None or key < best[0]:
                    best = (key, bp, dp, L, sc[1])
    (span, L), bp, dp, L, centre = best
    print(f"最佳：樞軸在座管後 {bp} mm、夾具中心下 {dp} mm，臂長 {L} mm；全部車型需要擺角範圍 {span:.1f}°（中心 {centre:.1f}°）")
    for name, ok in evaluate(bp, dp, L):
        ss = [o[0] for o in ok]
        pick = min(ok, key=lambda o: abs(o[2] - centre))
        print(f"  {name:<24} 夾具高 s={min(ss):.0f}–{max(ss):.0f} mm；選 s={pick[0]:.0f}：接觸 {pick[1]:+.0f}°、擺角 {pick[2]:+.1f}°、k={pick[3]:+.2f}")
