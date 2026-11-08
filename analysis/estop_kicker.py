"""觸發桿（kicker）2D 幾何：拉線往前拉 → 觸發桿順時針轉 → 頂墊從下面把抬臂把手頂起 ≥ 22°。
主機座標（X 往後、Z 往上，Y 為法線），把手：繞 Cc，工作位置朝 +X 水平、下緣在中心線下 7 mm。
找：觸發桿軸 K、頂墊位置、拉線臂，使
  - 把手轉到 ≥ 22°（過死點 16°，氣壓棒推力矩 ≥ 2 倍摩擦）時，觸發桿轉角 ≤ 45°、頂墊仍在把手上
  - 頂墊在整個行程都在支架前緣之前（不撞支架）
  - 拉線行程 ≤ 14 mm（把手側拉桿 3:1、行程 30° 可以提供）
  - 拉線張力最小
"""
import math
import itertools

Cc = (243.15, 80.23)          # params.spring_points() 的偏心中心
HALF = 7.0                    # 把手半厚
RP = 3.0                      # 頂墊圓角半徑
GAP = 0.6                     # 靜止時頂墊與把手下緣的間隙
TAU = 1.1                     # 需要推動把手的力矩（觸發 0.55＋摩擦 0.5，N·m）
TARGET = 22.0                 # 把手要被頂到的角度（度）
S = (232.0, 40.0)             # 線管座（塔外牆下方）


def rot_cw(v, deg):
    a = math.radians(deg)
    return (v[0] * math.cos(a) + v[1] * math.sin(a), -v[0] * math.sin(a) + v[1] * math.cos(a))


def handle_angle(Q):
    """頂墊中心 Q 碰到把手下緣時的把手角（度）；把手可被往上頂，不能往下。"""
    qx, qz = Q[0] - Cc[0], Q[1] - Cc[1]
    R = math.hypot(qx, qz)
    beta = math.atan2(qz, qx)
    a = beta + math.asin((HALF + RP) / R)
    return max(0.0, math.degrees(a)), R * math.cos(a - beta)     # 角度、接觸點沿把手的距離


def evaluate(K, p0, c0, bracket_front):
    best = None
    q0 = (K[0] + p0[0], K[1] + p0[1])
    a0, _ = handle_angle((q0[0], q0[1] + GAP))
    if a0 > 0.01:
        return None                                   # 靜止時就頂到了
    C0 = (K[0] + c0[0], K[1] + c0[1])
    L0 = math.hypot(C0[0] - S[0], C0[1] - S[1])
    worstT = 0.0
    for i in range(1, 451):
        th = i * 0.1
        q = rot_cw(p0, th)
        Q = (K[0] + q[0], K[1] + q[1])
        if Q[0] + RP > bracket_front - 0.5:
            return None
        a, s = handle_angle(Q)
        if a <= 0:
            continue
        if not (20.0 <= s <= 95.0):
            return None
        # 頂墊推力（垂直把手）與觸發桿力矩
        n = (-math.sin(math.radians(a)), math.cos(math.radians(a)))
        Fp = TAU * 1000.0 / s
        r = (Q[0] - K[0], Q[1] - K[1])
        tq_pad = r[0] * (-Fp * n[1]) - r[1] * (-Fp * n[0])        # 把手反推觸發桿
        c = rot_cw(c0, th)
        C = (K[0] + c[0], K[1] + c[1])
        u = ((S[0] - C[0]), (S[1] - C[1]))
        Lu = math.hypot(*u)
        u = (u[0] / Lu, u[1] / Lu)
        arm = c[0] * u[1] - c[1] * u[0]
        if arm >= -1e-6:
            return None                                   # 拉線不再產生順時針力矩
        T = -tq_pad / arm
        worstT = max(worstT, T)
        if a >= TARGET:
            pull = L0 - Lu
            return dict(theta=th, pull=pull, T=worstT, s=s)
    return None


if __name__ == "__main__":
    res = []
    for kx, kz in itertools.product(range(296, 326, 2), range(44, 66, 2)):
        for px, pz in itertools.product(range(-34, -6, 2), range(6, 30, 2)):
            if kz + pz > 73.2 - HALF + 20:          # 頂墊不能在把手中心線上方
                continue
            for cl in (14, 16, 18, 20, 22, 24):
                c0 = (0.0, -cl)
                r = evaluate((kx, kz), (px, pz), c0, bracket_front=kx - 6)
                if r and r["pull"] <= 14.0:
                    res.append((round(r["T"], 1), r["pull"], r["theta"], (kx, kz), (px, pz), cl, r["s"]))
    res.sort()
    print(len(res), "組可行；張力最小前 8：（拉線張力 N、拉線行程 mm、觸發桿轉角、K、頂墊相對 K、拉線臂長、接觸點離軸）")
    for r in res[:8]:
        print(r)
