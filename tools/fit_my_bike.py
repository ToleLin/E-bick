"""我的車能不能裝？該印哪一款座管座、夾具裝多高？

兩種用法（單位 mm，角度 度）：

1) 直接量（推薦，捲尺＋水平尺即可）：
   python tools/fit_my_bike.py measure --post 27.2 --sta 73 --H 250 --V 140 --tire 622x35 --exposed 150
   --H   座管中心線在「立管上緣（座管束頂面）」那一點 → 後輪胎最高點，水平往後的距離
   --V   立管上緣 → 後輪胎最高點，往下的垂直距離（胎頂比立管上緣低為正）
   --exposed 立管上緣 → 座墊軌道（座墊下方夾座墊的兩根鋼條）沿座管的長度

2) 用廠商幾何表：
   python tools/fit_my_bike.py geometry --post 31.6 --sta 73.5 --st 420 --cs 438 --drop 60 --tire 622x58 --exposed 220
   --st 立管長（五通中心到立管上緣，C-T）  --cs 後下叉長  --drop 五通下沉（五通低於後軸為正）

--tire 胎圈直徑 x 胎寬：700C/29" = 622、27.5" = 584、26" = 559、20" = 406、16" = 349

輸出：可用的座管座款式（std / mtb / fold / minivelo）、夾具中心離立管上緣的高度 s、擺臂角、接觸角。
主機本身各車通用；擺臂工作角越接近 −20° 越好（氣壓棒在行程中段，壓力一致、抬臂行程足）。
"""
import argparse
import math
import sys

# ── 與 src/params.py 一致的主機幾何（主機座標：+X 垂直座管往後、+Z 沿座管往上，原點＝夾具中心）──
DOVE_ROOT_X = 27.0
PIVOT = (110.0, -80.0)
ARM_L = 230.0
ARM_PHI0 = -20.0
PHI_TOL = 3.0
ROLLER_R = 34.5
VARIANTS = {"std": (0.0, 0.0), "mtb": (-10.0, 0.0), "fold": (10.0, 0.0), "minivelo": (30.0, 40.0)}
S_LO, TOP_RESERVE = 40.0, 75.0
CMIN, CMAX = -12.0, 14.0
GAP_P, GAP_ARM, CLR_M, CLR_P = 25.0, 15.0, 42.0, 20.0
J_BELOW_COLLAR = 25.0


def add(a, b, s=1.0):
    return (a[0] + s * b[0], a[1] + s * b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def norm(a):
    return math.hypot(*a)


def unit(a):
    n = norm(a)
    return (a[0] / n, a[1] / n)


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def rot(v, deg):
    a = math.radians(deg)
    return (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a))


def circle_hit(c0, r0, c1, r1):
    d = norm(sub(c1, c0))
    if d > r0 + r1 or d < abs(r0 - r1) or d == 0:
        return []
    a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(max(r0 ** 2 - a ** 2, 0.0))
    ex = unit(sub(c1, c0))
    p = add(c0, ex, a)
    perp = (-ex[1], ex[0])
    return [add(p, perp, h), add(p, perp, -h)]


def evaluate(W, R, sta, exposed):
    """座標：原點＝立管上緣中心，X 往後、Z 往上。回傳所有可行 (偏差, 款式, s, φ, 接觸角, k)。"""
    a = math.radians(sta)
    u, wv = (math.cos(a), math.sin(a)), (math.sin(a), -math.cos(a))
    J = (-J_BELOW_COLLAR * u[0], -J_BELOW_COLLAR * u[1])
    out = []
    for name, (pitch, reach) in VARIANTS.items():
        uu, ww = rot(u, -pitch), rot(wv, -pitch)
        s = S_LO
        while s <= exposed - TOP_RESERVE + 1e-6:
            Q = (s * u[0], s * u[1])
            O = add(Q, wv, DOVE_ROOT_X + reach)
            P = add(add(O, ww, PIVOT[0] - DOVE_ROOT_X), uu, PIVOT[1])      # PIVOT[1] = −80：沿座管往下
            s += 2.0
            if norm(sub(P, W)) - R < GAP_P:
                continue
            hits = [h for h in circle_hit(P, ARM_L, W, R + ROLLER_R) if h[1] > W[1]]
            if not hits:
                continue
            M = max(hits, key=lambda h: h[1])
            n = unit(sub(M, W))
            C = add(W, n, R)
            th = math.degrees(math.atan2(-(C[0] - W[0]), C[1] - W[1]))
            t = unit((-(C[1] - W[1]), C[0] - W[0]))     # 胎面切線（與 analysis/contact_mechanics.py 同）
            lever = sub(C, P)
            k = -cross(lever, (-t[0], -t[1])) / cross(lever, n)
            tip = ARM_L - ROLLER_R - 5
            arm_gap = min(norm(sub(add(P, unit(sub(M, P)), i * tip / 12), W)) - R for i in range(13))
            side = lambda pt: cross(unit(sub(W, J)), sub(pt, J))
            if not (CMIN <= th <= CMAX and abs(k) <= 0.5 and arm_gap >= GAP_ARM and side(M) >= CLR_M
                    and side(P) >= CLR_P):
                continue
            v = sub(M, P)
            ang = math.atan2(cross(ww, v), ww[0] * v[0] + ww[1] * v[1])
            phi = -math.degrees(ang) if cross(ww, uu) > 0 else math.degrees(ang)
            out.append((abs(phi - ARM_PHI0), name, s - 2.0, phi, th, k))
    prio = {"std": 0, "mtb": 1, "fold": 2, "minivelo": 3}
    # 擺臂角差不多（≤1.5°）時優先推薦標準款，其次才是特殊款
    return sorted(out, key=lambda r: (r[0] > 1.5, prio[r[1]] if r[0] <= 1.5 else 0, r[0]))


def parse_tire(t):
    bsd, w = t.lower().split("x")
    return float(bsd), float(w)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="mode", required=True)
    m = sp.add_parser("measure")
    m.add_argument("--H", type=float, required=True)
    m.add_argument("--V", type=float, required=True)
    g = sp.add_parser("geometry")
    g.add_argument("--st", type=float, required=True)
    g.add_argument("--cs", type=float, required=True)
    g.add_argument("--drop", type=float, required=True)
    for p in (m, g):
        p.add_argument("--post", type=float, required=True, help="座管直徑")
        p.add_argument("--sta", type=float, default=73.0, help="座管角（實際角度，不是有效座管角）")
        p.add_argument("--tire", required=True, help="例如 622x35")
        p.add_argument("--exposed", type=float, required=True)
    a = ap.parse_args()
    bsd, w = parse_tire(a.tire)
    R = (bsd + 2 * 0.95 * w) / 2
    if a.mode == "measure":
        W = (a.H, -a.V - R)
    else:
        ang = math.radians(a.sta)
        C0 = (a.st * math.cos(ang), a.st * math.sin(ang))
        Wb = (math.sqrt(a.cs ** 2 - a.drop ** 2), a.drop)
        W = sub(Wb, C0)
        print(f"（換算）胎頂在立管上緣後方 {W[0]:.0f} mm、下方 {-(W[1] + R):.0f} mm")
    if a.post < 25.0 or a.post > 35.0:
        print(f"座管 Ø{a.post} 不在 25.4–34.9 範圍內，座管座要另外改尺寸。")
    res = evaluate(W, R, a.sta, a.exposed)
    if not res:
        print("找不到可行的裝法：外露座管太短、或後輪離座管太遠／太近。請把量測值與車子照片附到專案的 issue。")
        sys.exit(1)
    best = res[0]
    print(f"\n建議：座管座 款式 {best[1]}（座管 Ø{a.post}），夾具中心離立管上緣 s = {best[2]:.0f} mm"
          f"（夾具下緣離立管上緣 {best[2] - 25:.0f} mm）")
    print(f"      擺臂角 {best[3]:+.1f}°（理想 −20°）、滾輪接觸在胎頂{'前' if best[4] >= 0 else '後'} {abs(best[4]):.0f}°、"
          f"驅動對正向力影響 k={best[5]:+.2f}")
    if best[0] > PHI_TOL:
        print(f"  ⚠ 擺臂角偏離理想值 {best[0]:.1f}°：氣壓棒會在行程端點附近，壓力差約 ±10%，抬臂量會變小。")
    print("\n其他可行組合（款式、s、擺臂角）：")
    seen = set()
    for r in res[1:]:
        key = (r[1], round(r[2] / 10))
        if key in seen:
            continue
        seen.add(key)
        print(f"  {r[1]:<9} s={r[2]:4.0f}  φ={r[3]:+.1f}°")
        if len(seen) >= 6:
            break


if __name__ == "__main__":
    main()
