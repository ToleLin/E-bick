"""每台車的座管座可選「後伸量」reach（燕尾往後挪），搭配夾具高度 s，
讓所有車型的擺臂接觸角度都接近同一個目標角 → 主機氣壓棒行程與壓力在各車一致。"""
import math
import fit_rigid_housing as fr
import fit_optimizer as fo

REACHES = (0, 20, 40, 60)

def options(bp, dp, L):
    """每台車 → [(φ, s, reach, contact, k)]"""
    out = {}
    for reach in REACHES:
        for name, ok in fr.evaluate(bp + reach, dp, L):
            out.setdefault(name, []).extend((o[2], o[0], reach, o[1], o[3]) for o in ok)
    return out

def best_target(opts):
    if any(not v for v in opts.values()):
        return None
    cands = sorted(set(round(o[0]) for v in opts.values() for o in v))
    best = None
    for t in cands:
        dev = max(min(abs(o[0] - t) for o in v) for v in opts.values())
        if best is None or dev < best[0]:
            best = (dev, t)
    return best

if __name__ == "__main__":
    res = []
    for bp in range(60, 141, 10):
        for dp in range(20, 101, 10):
            for L in range(150, 221, 10):
                b = best_target(options(bp, dp, L))
                if b:
                    res.append((round(b[0], 1), L, bp, dp, b[1]))
    res.sort()
    print("前 8（最大偏差°、臂長、樞軸後移、下移、目標角）", res[:8])
    dev, L, bp, dp, t = res[0]
    opts = options(bp, dp, L)
    for name, v in opts.items():
        o = min(v, key=lambda o: (abs(o[0] - t), o[2]))
        print(f"  {name:<24} reach={o[2]:>2}  s={o[1]:.0f}  擺角 {o[0]:+.1f}°  接觸 {o[3]:+.0f}°  k={o[4]:+.2f}")
