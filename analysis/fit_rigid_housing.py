"""主機剛性固定在座管座上＋短擺臂。找樞軸位置與臂長，讓所有車型：
- 接觸角在胎頂前 −12°～+14°
- |k| ≤ 0.5（驅動力幾乎不改變正向力）
- 樞軸與馬達都在後上叉連線（立管頂 J → 後軸 W）的後上方，留間隙（避免撞後上叉）
並使全部車型需要的擺臂角度範圍最小。
"""
import math
from contact_mechanics import *
import fit_optimizer as fo

R_ROLL = 34.5
CMIN, CMAX = -12.0, 14.0
KABS = 0.5
CLR_M, CLR_P = 42.0, 20.0     # 馬達中心、樞軸到後上叉線的最小距離（側視）
J_BELOW_COLLAR = 25.0         # 後上叉接在立管上緣下方約 25 mm

def side_of_stays(pt, J, W):
    """正值 = 在後上叉線的後上方（安全側），數值 = 垂直距離。"""
    d = unit(sub(W, J))
    v = sub(pt, J)
    return cross(d, v)          # J→W 往後下；左手側（後上）為正

def evaluate(bp, dp, L, bikes=fo.BIKES):
    per = []
    for name, bsd, w, cs, drop, sta, st, exposed in bikes:
        R, W, u, wv = bike_frame(bsd, w, cs, drop, sta)
        J = ((st - J_BELOW_COLLAR) * u[0], (st - J_BELOW_COLLAR) * u[1])
        ok = []
        s = fo.S_LO
        while s <= exposed - fo.TOP_RESERVE + 1e-6:
            Q = ((st + s) * u[0], (st + s) * u[1])
            P = add(add(Q, mul(wv, bp)), mul(u, -dp))
            M = solve_contact(P, L, W, R, R_ROLL)
            if M:
                f = forces(P, M, W, R)
                if (CMIN <= f["contact_deg"] <= CMAX and abs(f["k"]) <= KABS
                        and side_of_stays(M, J, W) >= CLR_M and side_of_stays(P, J, W) >= CLR_P):
                    phi = fo.angle_from(sub(M, P), wv, u)
                    ok.append((s, f["contact_deg"], phi, f["k"], P, M))
            s += 2.0
        per.append((name, ok))
    return per

if __name__ == "__main__":
    import sys
    skip_minivelo = "--no-minivelo" in sys.argv
    bikes = [b for b in fo.BIKES if not (skip_minivelo and b[0].startswith("小徑"))]
    res, cover = [], None
    for bp in range(40, 261, 10):
        for dp in range(-40, 221, 10):
            for L in range(90, 201, 10):
                per = evaluate(bp, dp, L, bikes)
                n = sum(1 for _, ok in per if ok)
                if cover is None or n > cover[0]:
                    cover = (n, bp, dp, L)
                sc = fo.score([(a, [o[:4] for o in b]) for a, b in per])
                if sc:
                    res.append((round(sc[0], 1), L, bp, dp, sc[1]))
    res.sort()
    print("最多涵蓋：", cover, "／", len(bikes))
    print(len(res), "組全部可行；前 6：", res[:6])
    if res:
        span, L, bp, dp, c = res[0]
        for name, ok in evaluate(bp, dp, L, bikes):
            pick = min(ok, key=lambda o: abs(o[2] - c))
            ss = [o[0] for o in ok]
            print(f"  {name:<24} s={min(ss):.0f}–{max(ss):.0f}；選 s={pick[0]:.0f} 接觸 {pick[1]:+.0f}° 擺角 {pick[2]:+.1f}° k={pick[3]:+.2f}")
