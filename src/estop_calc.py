"""緊急停止（拉桿觸發過死點偏心）的力學計算。

1. 各車型：工作位置把曲柄往回推過死點需要的力矩（＝觸發力矩）；
2. 過死點後氣壓棒只會把曲柄往「抬起」方向推（不會自己回去）＝自鎖在停止狀態；
3. 氣壓棒伸到全長（正向力歸零）時曲柄已轉幾度；
執行：cadgen +0.8.3 run src/estop_calc.py
"""
import math

import params as P
import unit as U
from bikes import bike_geom, solve_arm_angle
from forces import gs_force, cross, unit2

F1 = 250.0


def crank_torque(deg, B):
    _, _, Cc, _ = P.spring_points()
    pin = (Cc[0] + P.CRANK_R * math.cos(math.radians(deg)), Cc[1] + P.CRANK_R * math.sin(math.radians(deg)))
    Ls = math.hypot(pin[0] - B[0], pin[1] - B[1])
    if Ls >= P.GS_LEN:
        return 0.0, Ls
    Fs = gs_force(F1, Ls)
    f = unit2((pin[0] - B[0], pin[1] - B[1]))
    return cross((pin[0] - Cc[0], pin[1] - Cc[1]), (Fs * f[0], Fs * f[1])) / 1000.0, Ls   # N·m，正＝逆時針（往抬起）


if __name__ == "__main__":
    e = U.CRANK_ENGAGED_DEG
    print("車型            觸發力矩(N·m)  死點角   過死點後最小推力矩  氣壓棒全長時曲柄已轉")
    for row in P.BIKES:
        g = bike_geom(row)
        phi, _ = solve_arm_angle(g)
        d = P.arm_dir(phi)
        B = (P.PIVOT[0] + P.SPRING_D * d[0], P.PIVOT[1] + P.SPRING_D * d[1])
        hold = -min(crank_torque(e + i * 0.1, B)[0] for i in range(0, 61))       # 工作位置附近最大的鎖緊力矩
        dead = None
        prev = crank_torque(e, B)[0]
        for i in range(1, 400):
            t = crank_torque(e + i * 0.05, B)[0]
            if prev < 0 <= t:
                dead = e + i * 0.05
                break
            prev = t
        # 過死點後到氣壓棒伸到全長：推力矩都要 > 0（自動往抬起走）
        free = None
        tmin = 1e9
        a = dead + 0.2
        while a < e + U.CRANK_TRAVEL_DEG:
            t, Ls = crank_torque(a, B)
            if Ls >= P.GS_LEN:
                free = a
                break
            tmin = min(tmin, t)
            a += 0.2
        print(f"{g['name']:<14} {hold:8.3f}       {dead:+6.1f}°   {tmin:+.3f} N·m        {free - e:5.1f}°")
