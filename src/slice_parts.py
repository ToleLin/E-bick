"""Bambu Studio CLI 無頭切片：估每個列印件的克數與時間（A1、紋理 PEI）。

PETG-CF：0.6 硬化鋼噴嘴、0.24 Optimal（層高改 0.2）、6 道牆、上下 5 層、gyroid。
TPU 95A HF：0.4 噴嘴、0.2 Standard、3 道牆。
執行（一般 Python，不用 cadgen）：python src/slice_parts.py [--all-bases]
輸出：PRINT/<零件>.gcode.3mf、PRINT/切片結果.json
"""
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "Onshape建模"))
from bambu_slice import STUDIO, flatten  # noqa: E402

CF = dict(machine="Bambu Lab A1 0.6 nozzle", process="0.24mm Optimal @BBL A1 0.6 nozzle",
          filament="Bambu PETG-CF @BBL A1 0.8 nozzle", machine_ov={"nozzle_type": ["hardened_steel"]},
          process_ov={"layer_height": "0.2", "initial_layer_print_height": "0.2", "wall_loops": "6",
                      "top_shell_layers": "5", "bottom_shell_layers": "5", "sparse_infill_pattern": "gyroid",
                      "sparse_infill_density": "40%", "brim_type": "outer_only", "brim_width": "5"})
HF = dict(CF, filament="Bambu PETG HF @BBL A1 0.8 nozzle")
TPU = dict(machine="Bambu Lab A1 0.4 nozzle", process="0.20mm Standard @BBL A1", filament="Bambu TPU 95A HF @BBL A1",
           machine_ov={}, process_ov={"wall_loops": "3", "sparse_infill_density": "20%", "brim_type": "no_brim"})
SUPPORT = {"enable_support": "1", "support_type": "tree(auto)", "support_threshold_angle": "40"}

JOBS = [  # 檔案, 設定, 額外覆寫
    ("unit/01_housing_front_PETG-CF.stl", CF, {**SUPPORT, "sparse_infill_density": "25%"}),
    ("unit/02_housing_rear_PETG-CF.stl", CF, {**SUPPORT, "sparse_infill_density": "25%"}),
    ("unit/03_bay_lid_PETG-CF.stl", CF, {"brim_type": "no_brim"}),
    ("unit/04_swing_arm_PETG-CF.stl", CF, {**SUPPORT, "sparse_infill_density": "60%"}),
    ("unit/05_lift_crank_inner_PETG-HF.stl", HF, {"sparse_infill_density": "100%", "sparse_infill_pattern": "zig-zag"}),
    ("unit/06_lift_crank_outer_PETG-HF.stl", HF, {"sparse_infill_density": "100%", "sparse_infill_pattern": "zig-zag"}),
    ("unit/08_lift_handle_PETG-HF.stl", HF, {"sparse_infill_density": "100%", "sparse_infill_pattern": "zig-zag"}),
    ("unit/09_spacer_pivot_x1_PETG-HF.stl", HF, {"sparse_infill_density": "100%", "sparse_infill_pattern": "zig-zag", "brim_type": "no_brim"}),
    ("unit/09_spacer_eye_top_x2_PETG-HF.stl", HF, {"sparse_infill_density": "100%", "sparse_infill_pattern": "zig-zag", "brim_type": "no_brim"}),
    ("unit/09_spacer_eye_low_x2_PETG-HF.stl", HF, {"sparse_infill_density": "100%", "sparse_infill_pattern": "zig-zag", "brim_type": "no_brim"}),
    ("unit/07_roller_sleeve_TPU95A.stl", TPU, {}),
    ("unit/10_estop_kicker_PETG-HF.stl", HF, {"sparse_infill_density": "100%", "sparse_infill_pattern": "zig-zag"}),
    ("unit/09_spacer_kicker_x1_PETG-HF.stl", HF, {"sparse_infill_density": "100%", "sparse_infill_pattern": "zig-zag", "brim_type": "no_brim"}),
    ("estop_lever/L/estop_lever_upper_bar22p2_L_PETG-CF.stl", CF, {"sparse_infill_density": "60%"}),
    ("estop_lever/L/estop_lever_lower_L_PETG-CF.stl", CF, {"sparse_infill_density": "60%"}),
    ("estop_lever/L/estop_lever_blade_L_PETG-HF.stl", HF, {"sparse_infill_density": "100%", "sparse_infill_pattern": "zig-zag"}),
    ("base/D27p2/base_front_D27p2_PETG-CF.stl", CF, {}),
    ("base/D27p2/base_rear_D27p2_std_PETG-CF.stl", CF, {"sparse_infill_density": "60%"}),
    ("base/D27p2/liner_D27p2_TPU95A.stl", TPU, {}),
]


def slice_one(stl, cfg, extra):
    work = Path(tempfile.mkdtemp(prefix="bslice_"))
    files = {}
    pov = {"curr_bed_type": "Textured PEI Plate", **cfg["process_ov"], **extra}
    for kind, name, ov in (("machine", cfg["machine"], cfg["machine_ov"]), ("process", cfg["process"], pov),
                           ("filament", cfg["filament"], None)):
        f = work / f"{kind}.json"
        f.write_text(json.dumps(flatten(name, ov), ensure_ascii=False, indent=1), encoding="utf-8")
        files[kind] = f
    # 中文路徑保險起見，STL 先複製到暫存資料夾
    src = work / "part.stl"
    shutil.copy(stl, src)
    out = work / "out.gcode.3mf"
    cmd = [str(STUDIO), "--slice", "0", "--arrange", "1", "--load-settings", f"{files['machine']};{files['process']}",
           "--load-filaments", str(files["filament"]), "--allow-newer-file", "--skip-useless-pick",
           "--outputdir", str(work), "--export-3mf", out.name, str(src)]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=2700)
    if not out.exists():
        raise RuntimeError(f"{stl} 切片失敗 (exit {proc.returncode})\n{proc.stdout[-1500:]}")
    with zipfile.ZipFile(out) as z:
        info = z.read("Metadata/slice_info.config").decode("utf-8")
    g = sum(float(w) for w in re.findall(r'<filament [^>]*used_g="([\d.]+)"', info))
    t = re.search(r'key="prediction" value="(\d+)"', info)
    return round(g, 1), round(int(t.group(1)) / 60) if t else None, out, work


def main():
    jobs = list(JOBS)
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    if only:
        jobs = [j for j in jobs if any(o in j[0] for o in only)]
    if "--all-bases" in sys.argv:
        jobs = [(str(p.relative_to(ROOT / "STL")).replace("\\", "/"), TPU if "TPU" in p.name else CF,
                 {} if "TPU" in p.name else {"sparse_infill_density": "60%"})
                for p in sorted((ROOT / "STL" / "base").rglob("*.stl"))]
    (ROOT / "PRINT").mkdir(exist_ok=True)
    res = {}
    resf = ROOT / "PRINT" / "切片結果.json"
    if resf.exists():
        res = json.loads(resf.read_text(encoding="utf-8"))
    for rel, cfg, extra in jobs:
        g, mins, out, work = slice_one(ROOT / "STL" / rel, cfg, extra)
        dst = ROOT / "PRINT" / (Path(rel).stem + ".gcode.3mf")
        shutil.copy(out, dst)
        shutil.rmtree(work, ignore_errors=True)
        res[rel] = {"g": g, "min": mins, "filament": cfg["filament"]}
        print(f"{rel:<48} {g:7.1f} g  {mins:5d} min")
        resf.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
