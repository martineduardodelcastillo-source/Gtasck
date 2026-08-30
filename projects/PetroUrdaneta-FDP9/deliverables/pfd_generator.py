#!/usr/bin/env python3
"""
Gtasck FDP-9 · Gerador de PFDs esquemáticos para as 12 correntes (S-01 a S-12)
Gera um PFD por corrente + um PFD geral do campo, em SVG (ISA-5.1).
"""
from __future__ import annotations
import json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = "/home/ubuntu/Gtasck/modules/pid_generator/pid_engine.py"
OUT = os.path.join(HERE, "pfds")
os.makedirs(OUT, exist_ok=True)

# Definição das 12 correntes com equipamentos, linhas e instrumentos
STREAMS = {
    "S-01": {
        "title": "PFD S-01 · Poço → EPF Manifold",
        "equipment": [
            {"tag": "W-01", "kind": "vessel", "x": 120, "y": 300, "label": "Poço (wellhead)"},
            {"tag": "XV-101", "kind": "valve_gate", "x": 260, "y": 360, "label": "Wing valve"},
            {"tag": "SCSSV", "kind": "valve_gate", "x": 200, "y": 360, "label": "SCSSV"},
            {"tag": "M-01", "kind": "vessel", "x": 420, "y": 300, "label": "EPF manifold"},
        ],
        "lines": [
            {"tag": "S-01", "points": [[120, 360], [200, 360]], "spec": "3\"-150#-CS"},
            {"tag": "S-01", "points": [[200, 360], [260, 360]], "spec": "3\"-150#-CS"},
            {"tag": "S-01", "points": [[260, 360], [420, 360]], "spec": "3\"-150#-CS"},
        ],
        "instruments": [
            {"tag": "PSV101", "x": 330, "y": 320},
            {"tag": "PI101", "x": 330, "y": 400},
        ],
    },
    "S-02": {
        "title": "PFD S-02 · EPF Manifold → Booster VFD",
        "equipment": [
            {"tag": "M-01", "kind": "vessel", "x": 120, "y": 300, "label": "EPF manifold"},
            {"tag": "P-01", "kind": "pump_centrifugal", "x": 420, "y": 360, "label": "Booster VFD"},
        ],
        "lines": [
            {"tag": "S-02", "points": [[120, 360], [420, 360]], "spec": "4\"-150#-CS"},
        ],
        "instruments": [
            {"tag": "PSV102", "x": 260, "y": 320},
            {"tag": "LAHH102", "x": 260, "y": 400},
            {"tag": "ESD102", "x": 340, "y": 320},
        ],
    },
    "S-03": {
        "title": "PFD S-03 · Booster VFD → Trunkline",
        "equipment": [
            {"tag": "P-01", "kind": "pump_centrifugal", "x": 120, "y": 360, "label": "Booster VFD"},
            {"tag": "XV-103", "kind": "valve_gate", "x": 260, "y": 360, "label": "Check valve"},
            {"tag": "TL-01", "kind": "vessel", "x": 420, "y": 300, "label": "Trunkline"},
        ],
        "lines": [
            {"tag": "S-03", "points": [[120, 360], [260, 360]], "spec": "4\"-150#-CS"},
            {"tag": "S-03", "points": [[260, 360], [420, 360]], "spec": "4\"-150#-CS"},
        ],
        "instruments": [
            {"tag": "PSV103", "x": 200, "y": 320},
            {"tag": "ESD103", "x": 330, "y": 320},
        ],
    },
    "S-04": {
        "title": "PFD S-04 · Trunkline → FSB Pig Receiver",
        "equipment": [
            {"tag": "TL-01", "kind": "vessel", "x": 120, "y": 300, "label": "Trunkline"},
            {"tag": "PR-01", "kind": "vessel", "x": 420, "y": 300, "label": "Pig receiver"},
        ],
        "lines": [
            {"tag": "S-04", "points": [[120, 360], [420, 360]], "spec": "6\"-150#-CS"},
        ],
        "instruments": [
            {"tag": "PSV104", "x": 260, "y": 320},
            {"tag": "ESD104", "x": 340, "y": 320},
            {"tag": "PS104", "x": 260, "y": 400},
        ],
    },
    "S-05": {
        "title": "PFD S-05 · Pig Receiver → Vaso de Slug",
        "equipment": [
            {"tag": "PR-01", "kind": "vessel", "x": 120, "y": 300, "label": "Pig receiver"},
            {"tag": "SV-01", "kind": "vessel", "x": 420, "y": 300, "label": "Vaso de slug"},
        ],
        "lines": [
            {"tag": "S-05", "points": [[120, 360], [420, 360]], "spec": "6\"-150#-CS"},
        ],
        "instruments": [
            {"tag": "PSV105", "x": 260, "y": 320},
            {"tag": "LAHH105", "x": 260, "y": 400},
            {"tag": "ESD105", "x": 340, "y": 320},
        ],
    },
    "S-06": {
        "title": "PFD S-06 · Vaso de Slug → Separador Trifásico",
        "equipment": [
            {"tag": "SV-01", "kind": "vessel", "x": 120, "y": 300, "label": "Vaso de slug"},
            {"tag": "S-3PH", "kind": "separator_3ph", "x": 420, "y": 300, "label": "Separador trifásico"},
        ],
        "lines": [
            {"tag": "S-06", "points": [[120, 360], [420, 360]], "spec": "6\"-150#-CS"},
        ],
        "instruments": [
            {"tag": "PSV106", "x": 260, "y": 320},
            {"tag": "LAHH106", "x": 260, "y": 400},
            {"tag": "LALL106", "x": 340, "y": 400},
            {"tag": "ESD106", "x": 340, "y": 320},
        ],
    },
    "S-07": {
        "title": "PFD S-07 · Separador → Compressão (Gás)",
        "equipment": [
            {"tag": "S-3PH", "kind": "separator_3ph", "x": 120, "y": 300, "label": "Separador trifásico"},
            {"tag": "C-01", "kind": "pump_centrifugal", "x": 420, "y": 360, "label": "Compressor"},
        ],
        "lines": [
            {"tag": "S-07", "points": [[120, 330], [420, 330]], "spec": "4\"-150#-CS"},
        ],
        "instruments": [
            {"tag": "PSV107", "x": 260, "y": 290},
            {"tag": "ESD107", "x": 340, "y": 290},
            {"tag": "AS107", "x": 260, "y": 370},
        ],
    },
    "S-08": {
        "title": "PFD S-08 · Separador → EFB Storage (Óleo)",
        "equipment": [
            {"tag": "S-3PH", "kind": "separator_3ph", "x": 120, "y": 300, "label": "Separador trifásico"},
            {"tag": "TK-01", "kind": "tank", "x": 420, "y": 300, "label": "EFB storage"},
        ],
        "lines": [
            {"tag": "S-08", "points": [[120, 360], [420, 360]], "spec": "6\"-150#-CS"},
        ],
        "instruments": [
            {"tag": "PSV108", "x": 260, "y": 320},
            {"tag": "LAHH108", "x": 260, "y": 400},
            {"tag": "ESD108", "x": 340, "y": 320},
        ],
    },
    "S-09": {
        "title": "PFD S-09 · Separador → Tratamento de Água",
        "equipment": [
            {"tag": "S-3PH", "kind": "separator_3ph", "x": 120, "y": 300, "label": "Separador trifásico"},
            {"tag": "WT-01", "kind": "vessel", "x": 420, "y": 300, "label": "Tratamento de água"},
        ],
        "lines": [
            {"tag": "S-09", "points": [[120, 390], [420, 390]], "spec": "4\"-150#-CS"},
        ],
        "instruments": [
            {"tag": "PSV109", "x": 260, "y": 350},
            {"tag": "LAHH109", "x": 260, "y": 430},
            {"tag": "ESD109", "x": 340, "y": 350},
        ],
    },
    "S-10": {
        "title": "PFD S-10 · Compressão → Fuel Gas / Gas Lift / Boscan",
        "equipment": [
            {"tag": "C-01", "kind": "pump_centrifugal", "x": 120, "y": 360, "label": "Compressor"},
            {"tag": "FG-01", "kind": "vessel", "x": 420, "y": 240, "label": "Fuel gas"},
            {"tag": "GL-01", "kind": "vessel", "x": 420, "y": 360, "label": "Gas lift"},
            {"tag": "BX-01", "kind": "vessel", "x": 420, "y": 480, "label": "Boscan export"},
        ],
        "lines": [
            {"tag": "S-10", "points": [[120, 360], [420, 240]], "spec": "3\"-150#-CS"},
            {"tag": "S-10", "points": [[120, 360], [420, 360]], "spec": "3\"-150#-CS"},
            {"tag": "S-10", "points": [[120, 360], [420, 480]], "spec": "3\"-150#-CS"},
        ],
        "instruments": [
            {"tag": "PSV110", "x": 260, "y": 320},
            {"tag": "ESD110", "x": 340, "y": 320},
            {"tag": "AS110", "x": 260, "y": 400},
        ],
    },
    "S-11": {
        "title": "PFD S-11 · EFB Storage → LACT → Palmarejo",
        "equipment": [
            {"tag": "TK-01", "kind": "tank", "x": 120, "y": 300, "label": "EFB storage"},
            {"tag": "LACT", "kind": "vessel", "x": 300, "y": 300, "label": "LACT"},
            {"tag": "TK-02", "kind": "tank", "x": 480, "y": 300, "label": "Palmarejo"},
        ],
        "lines": [
            {"tag": "S-11", "points": [[120, 360], [300, 360]], "spec": "6\"-150#-CS"},
            {"tag": "S-11", "points": [[300, 360], [480, 360]], "spec": "6\"-150#-CS"},
        ],
        "instruments": [
            {"tag": "PSV111", "x": 210, "y": 320},
            {"tag": "ESD111", "x": 390, "y": 320},
        ],
    },
    "S-12": {
        "title": "PFD S-12 · Tratamento → Reinjeção (Água)",
        "equipment": [
            {"tag": "WT-01", "kind": "vessel", "x": 120, "y": 300, "label": "Tratamento de água"},
            {"tag": "WI-01", "kind": "vessel", "x": 420, "y": 300, "label": "Reinjeção"},
        ],
        "lines": [
            {"tag": "S-12", "points": [[120, 360], [420, 360]], "spec": "4\"-150#-CS"},
        ],
        "instruments": [
            {"tag": "PSV112", "x": 260, "y": 320},
            {"tag": "LAHH112", "x": 260, "y": 400},
            {"tag": "ESD112", "x": 340, "y": 320},
        ],
    },
}

def gerar_pfd(stream_id: str, defn: dict) -> str:
    json_path = os.path.join(OUT, f"{stream_id}.json")
    svg_path = os.path.join(OUT, f"{stream_id}.svg")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(defn, f, indent=2, ensure_ascii=False)
    subprocess.run(["python3", ENGINE, json_path, "-o", svg_path], check=True, capture_output=True)
    return svg_path

if __name__ == "__main__":
    print("=== GERANDO PFDs ESQUEMÁTICOS (S-01 a S-12) ===\n")
    for sid, defn in STREAMS.items():
        svg = gerar_pfd(sid, defn)
        print(f"  {sid}: {svg}")
    print(f"\nTotal: {len(STREAMS)} PFDs gerados em {OUT}")
