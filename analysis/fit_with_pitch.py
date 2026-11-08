"""座管座參數（每台車各印一個）：燕尾傾角 pitch、後伸 reach；安裝時選夾具高度 s。
主機（換車共用）固定：樞軸 (bp, dp)、臂長 L。目標：所有車型的擺臂工作角都落在同一個角度附近。"""
import math
from contact_mechanics import *
import fit_optimizer as fo
import fit_rigid_housing as fr

PITCHES = (-10, 0, 10, 20, 30)      # 正 = 主機機尾往下轉（順時針，從右側看）
REACHES = (0, 20, 40)

def rot(v, deg):
    a = math.radians(deg)
    return (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a))

def evaluate(bp, dp, L, pitch, reach, bikes=fo.BIKES):
    per = []
    for name, bsd, w, cs, drop, sta, st, exposed in bikes:
        R, W, u, wv = bike_frame(bsd, w, cs, drop, sta)
        uu, ww = rot(u, -pitch), rot(wv, -pitch)          # 主機座標轉 pitch（機尾往下）
        J = ((st - fr.J_BELOW_COLLAR) * u[0], (st - fr.J_BELOW_COLLAR) * u[1])
        ok = []
        s = fo.S_LO
        while s <= exposed - fo.TOP_RESERVE + 1e-6:
            Q = ((st + s) * u[0], (st + s) * u[1])
            O = add(Q, mul(wv, 27 + reach))                  # 燕尾面（座管座後伸 reach）
            P = add(add(O, mul(ww, bp - 27)), mul(uu, -dp))
            M = solve_contact(P, L, W, R, fr.R_ROLL)
            if M:
                f = forces(P, M, W, R)
                if (fr.CMIN <= f["contact_deg"] <= fr.CMAX and abs(f["k"]) <= fr.KABS
                        and fr.side_of_stays(M, J, W) >= fr.CLR_M and fr.side_of_stays(P, J, W) >= fr.CLR_P):
                    phi = fo.angle_from(sub(M, P), ww, uu)
                    ok.append((phi, s, pitch, reach, f["contact_deg"], f["k"]))
            s += 2.0
        per.append((name, ok))
    return per

def options(bp, dp, L):
    out = {}
    for p in PITCHES:
        for r in REACHES:
            for name, ok in evaluate(bp, dp, L, p, r):
                out.setdefault(name, []).extend(ok)
    return out

def best_target(opts):
    if any(not v for v in opts.values()):
        return None
    best = None
    for t in range(-40, 21):
        dev = max(min(abs(o[0] - t) for o in v) for v in opts.values())
        if best is None or dev < best[0]:
            best = (dev, t)
    return best

if __name__ == "__main__":
    res = []
    for bp in range(70, 131, 10):
        for dp in range(20, 101, 10):
            for L in range(160, 221, 10):
                b = best_target(options(bp, dp, L))
                if b:
                    res.append((round(b[0], 1), L, bp, dp, b[1]))
    res.sort()
    print("前 6（最大偏差°、臂長、bp、dp、目標角）", res[:6])
    dev, L, bp, dp, t = res[0]
    for name, v in options(bp, dp, L).items():
        o = min(v, key=lambda o: (round(abs(o[0] - t)), abs(o[2]), o[3]))
        print(f"  {name:<24} pitch={o[2]:+3d}° reach={o[3]:>2} s={o[1]:.0f}  擺角 {o[0]:+.1f}°  接觸 {o[4]:+.0f}°  k={o[5]:+.2f}")
