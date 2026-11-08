"""匯出所有列印件的 STL（已轉成列印擺放方向、貼床 Z=0），以及主機組件 STEP。

STL 用 build123d 自己網格化（公差 0.02 mm），軸承孔才準；cadgen 的網格精度是零件尺寸的 0.25%，太粗。

執行：cadgen +0.8.3 run src/export_print.py
輸出：STL/<分類>/*.stl、STEP/postroller_unit.step
"""
import os
import shutil
import tempfile
from pathlib import Path

import build123d as bd

import params as P
import estop_lever as L
import unit as U
from base import base_front_body, base_rear_body, liner_body

ROOT = Path(__file__).resolve().parent.parent
TOL, ANG = 0.02, 0.1


def to_bed(shape):
    bb = shape.bounding_box()
    return bd.Pos(-(bb.min.X + bb.max.X) / 2, -(bb.min.Y + bb.max.Y) / 2, -bb.min.Z) * shape


def write(shape, rel):
    path = ROOT / "STL" / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    s = to_bed(shape)
    # OCC 的 STL 寫入器不吃中文路徑 → 先寫到暫存資料夾再搬
    fd, tmp = tempfile.mkstemp(suffix=".stl")
    os.close(fd)
    bd.export_stl(s, tmp, tolerance=TOL, angular_tolerance=ANG)
    assert os.path.getsize(tmp) > 1000, rel
    shutil.move(tmp, path)
    bb = s.bounding_box()
    print(f"{rel:<48} {bb.size.X:6.1f} × {bb.size.Y:6.1f} × {bb.size.Z:6.1f} mm  體積 {s.volume / 1000:6.1f} cm³")
    return path


X_DOWN = bd.Rot(0, -90, 0)      # +X → +Z：前端面（或接合面）貼床
YMAX_DOWN = bd.Rot(-90, 0, 0)   # +Y → −Z：+Y 那一面貼床
YMAX_UP = bd.Rot(90, 0, 0)      # +Y → +Z：−Y 那一面貼床


def main():
    # 主機（PETG-CF）
    write(X_DOWN * U.front_housing_body(), "unit/01_housing_front_PETG-CF.stl")
    write(X_DOWN * U.rear_housing_body(), "unit/02_housing_rear_PETG-CF.stl")
    write(bd.Rot(180, 0, 0) * U.bay_lid_body(), "unit/03_bay_lid_PETG-CF.stl")
    write(bd.Rot(0, 0, 25) * YMAX_DOWN * U.arm_body(), "unit/04_swing_arm_PETG-CF.stl")   # 斜 25° 才放得進 256 盤
    inner, outer, handle, _ = U.crank_parts()
    write(YMAX_UP * inner, "unit/05_lift_crank_inner_PETG-HF.stl")
    write(YMAX_UP * outer, "unit/06_lift_crank_outer_PETG-HF.stl")       # 曲柄片貼床，轂與六角榫朝上
    write(YMAX_UP * handle, "unit/08_lift_handle_PETG-HF.stl")
    for sp, n in zip(U.spacers(), ("1", "2", "2", "1")):
        write(sp, f"unit/09_{sp.label}_x{n}_PETG-HF.stl")
    write(YMAX_UP * U.sleeve_body(), "unit/07_roller_sleeve_TPU95A.stl")
    # 緊急停止：主機上的觸發桿（內側面貼床，線頭座朝上）
    write(YMAX_UP * U.kicker_body(), "unit/10_estop_kicker_PETG-HF.stl")
    # 緊急停止：車把拉桿（每台車一支）。設計是裝在車把左半邊；右半邊用鏡像版
    for side in ("L", "R"):
        mir = (lambda s: s) if side == "L" else (lambda s: bd.mirror(s, about=bd.Plane.YZ))
        write(mir(L.mount_lower_body()), f"estop_lever/{side}/estop_lever_lower_{side}_PETG-CF.stl")
        write(mir(L.blade_body()), f"estop_lever/{side}/estop_lever_blade_{side}_PETG-HF.stl")
        for d in L.BAR_DIAMETERS:
            tag = f"{d:.1f}".replace(".", "p")
            write(mir(L.mount_upper_body(d)), f"estop_lever/{side}/estop_lever_upper_bar{tag}_{side}_PETG-CF.stl")
    # 座管座（每台車一組）
    for d in P.POST_DIAMETERS:
        tag = f"{d:.1f}".replace(".", "p")
        write(base_front_body(d), f"base/D{tag}/base_front_D{tag}_PETG-CF.stl")
        write(liner_body(d), f"base/D{tag}/liner_D{tag}_TPU95A.stl")
        for variant in P.BASE_VARIANTS:
            write(base_rear_body(d, variant), f"base/D{tag}/base_rear_D{tag}_{variant}_PETG-CF.stl")
    # 組件 STEP（含外購件佔位）
    (ROOT / "STEP").mkdir(exist_ok=True)
    bd.export_step(U.unit_assembly(), str(ROOT / "STEP" / "postroller_unit.step"))
    print("STEP/postroller_unit.step")


if __name__ == "__main__":
    main()
