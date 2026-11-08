"""擺臂式摩擦驅動的接觸力學（側視 2D，X 往後、Z 往上，原點 = 五通中心）。

座標慣例：車往 −X 前進，後輪逆時針轉（CCW），胎頂表面往前（−X）移動。
滾輪推胎面沿切線 t 前進 → 胎面對滾輪的反作用 = −F·t。
整個「擺臂＋馬達」當一個剛體：馬達定子與轉子之間的扭矩是內力，只看接觸點、樞軸、彈簧、重力。

k = dN/dF：驅動力每增加 1 N，正向力改變多少。k < 0 表示驅動時滾輪被「抬起」（拖曳臂），
需要彈簧預壓多留 F·(1/μ − k) 的餘裕；k > 0 表示自緊（越出力壓越緊）。
"""
import math

def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def mul(a, s):
    return (a[0] * s, a[1] * s)

def norm(a):
    return math.hypot(*a)

def unit(a):
    n = norm(a)
    return (a[0] / n, a[1] / n)

def circle_intersections(c0, r0, c1, r1):
    d = norm(sub(c1, c0))
    if d > r0 + r1 or d < abs(r0 - r1) or d == 0:
        return []
    a = (r0**2 - r1**2 + d**2) / (2 * d)
    h = math.sqrt(max(r0**2 - a**2, 0.0))
    ex = unit(sub(c1, c0))
    p = add(c0, mul(ex, a))
    perp = (-ex[1], ex[0])
    return [add(p, mul(perp, h)), add(p, mul(perp, -h))]

def bike_frame(bsd, w, cs, drop, sta, tire_h_ratio=0.95):
    R = (bsd + 2 * tire_h_ratio * w) / 2
    W = (math.sqrt(cs**2 - drop**2), drop)
    a = math.radians(sta)
    u = (math.cos(a), math.sin(a))          # 沿座管往上（往後上）
    wv = (math.sin(a), -math.cos(a))        # 垂直座管、往後（往後下）
    return R, W, u, wv

def solve_contact(P, L, W, R, r):
    """擺臂繞 P、臂長 L，滾輪半徑 r 壓在半徑 R、圓心 W 的輪胎上 → 滾輪中心 M（取較高的解）。"""
    sols = circle_intersections(P, L, W, R + r)
    if not sols:
        return None
    sols = [s for s in sols if s[1] > W[1]]   # 只要輪心以上
    if not sols:
        return None
    return max(sols, key=lambda s: s[1])

def forces(P, M, W, R):
    n = unit(sub(M, W))                       # 胎 → 滾輪的法向
    C = add(W, mul(n, R))                     # 接觸點
    rc = sub(C, W)
    t = unit((-rc[1], rc[0]))                 # 胎面運動方向（CCW 切線）
    lever = sub(C, P)
    m_n = cross(lever, n)                     # 單位正向力對樞軸的力矩
    m_t = cross(lever, mul(t, -1))            # 單位驅動反力對樞軸的力矩
    k = -m_t / m_n                            # dN/dF
    contact_deg = math.degrees(math.atan2(-(C[0] - W[0]), C[1] - W[1]))  # 0 = 胎頂、正 = 胎頂前方
    return dict(C=C, n=n, t=t, m_n=m_n, k=k, contact_deg=contact_deg)
