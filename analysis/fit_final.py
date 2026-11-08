"""最終幾何最佳化：座管座（每台車）可選傾角 pitch、後伸 reach、夾具高度 s；主機固定樞軸與臂長。
限制：接觸角 −12～+14°、|k|≤0.5、避開後上叉、樞軸離胎面 ≥ 25 mm、擺臂（樞軸→馬達前緣）離胎面 ≥ 15 mm。
目標：所有車型擺臂工作角一致（最大偏差最小），再取主機最短。"""
import math
from contact_mechanics import *
import fit_optimizer as fo
import fit_rigid_housing as fr
import fit_with_pitch as fp

GAP_P, GAP_ARM = 25.0, 15.0

def evaluate(bp, dp, L, pitch, reach, bikes=fo.BIKES):
    per = []
    for name, bsd, w, cs, drop, sta, st, exposed in bikes:
        R, W, u, wv = bike_frame(bsd, w, cs, drop, sta)
        uu, ww = fp.rot(u, -pitch), fp.rot(wv, -pitch)
        J = ((st - fr.J_BELOW_COLLAR) * u[0], (st - fr.J_BELOW_COLLAR) * u[1])
        ok = []
        s = fo.S_LO
        while s <= exposed - fo.TOP_RESERVE + 1e-6:
            Q = ((st + s) * u[0], (st + s) * u[1])
            O = add(Q, mul(wv, 27 + reach))
            P = add(add(O, mul(ww, bp - 27)), mul(uu, -dp))
            if norm(sub(P, W)) - R >= GAP_P:
                M = solve_contact(P, L, W, R, fr.R_ROLL)
                if M:
                    f = forces(P, M, W, R)
                    tip = L - fr.R_ROLL - 5          # 擺臂到馬達前緣為止
                    arm_gap = min(norm(sub(add(P, mul(unit(sub(M, P)), t * tip / 12)), W)) - R for t in range(13))
                    if (fr.CMIN <= f["contact_deg"] <= fr.CMAX and abs(f["k"]) <= fr.KABS and arm_gap >= GAP_ARM
                            and fr.side_of_stays(M, J, W) >= fr.CLR_M and fr.side_of_stays(P, J, W) >= fr.CLR_P):
                        phi = fo.angle_from(sub(M, P), ww, uu)
                        ok.append((phi, s, pitch, reach, f["contact_deg"], f["k"], norm(sub(P, W)) - R, arm_gap))
            s += 2.0
        per.append((name, ok))
    return per

def options(bp, dp, L):
    out = {}
    for p in fp.PITCHES:
        for r in fp.REACHES:
            for name, ok in evaluate(bp, dp, L, p, r):
                out.setdefault(name, []).extend(ok)
    return out

if __name__ == "__main__":
    res = []
    for bp in range(50, 151, 10):
        for dp in range(0, 101, 10):
            for L in range(140, 241, 10):
                b = fp.best_target(options(bp, dp, L))
                if b and b[0] <= 4.0:
                    length = bp + L * math.cos(math.radians(-b[1])) + 34.5
                    res.append((round(length), round(b[0], 1), L, bp, dp, b[1]))
    res.sort()
    print(len(res), "組偏差≤4°；依長度前 8（長度、偏差、L、bp、dp、目標角）")
    for r in res[:8]:
        print(r)
    if res:
        length, dev, L, bp, dp, t = res[0]
        for name, v in options(bp, dp, L).items():
            o = min(v, key=lambda o: (round(abs(o[0] - t)), abs(o[2]), o[3]))
            print(f"  {name:<24} pitch={o[2]:+3d}° reach={o[3]:>2} s={o[1]:.0f}  擺角 {o[0]:+.1f}°  接觸 {o[4]:+.0f}°  k={o[5]:+.2f}  樞軸離胎 {o[6]:.0f}  臂離胎 {o[7]:.0f}")
