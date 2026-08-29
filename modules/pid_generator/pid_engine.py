#!/usr/bin/env python3
"""
Gtasck P&ID Generator — Motor de geração de P&ID/PFD em SVG
Simbologia ISA-5.1 / ISO 10628 · Tagueamento automático · Lista de linhas/equipamentos

Uso:
    python3 pid_engine.py exemplo_separador.json -o saida.svg
"""
from __future__ import annotations
import json, sys, math, argparse
from dataclasses import dataclass, field
from xml.sax.saxutils import escape as _esc

def esc(s) -> str:
    return _esc(str(s))

# ---------------------------------------------------------------
# Biblioteca de símbolos ISA-5.1 (primitivas SVG)
# ---------------------------------------------------------------
SYMBOLS = {
    "vessel": lambda x, y, w=60, h=120: (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w/2}" '
        f'fill="none" stroke="black" stroke-width="2"/>'),
    "separator_3ph": lambda x, y, w=140, h=60: (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" '
        f'fill="none" stroke="black" stroke-width="2"/>'
        f'<line x1="{x+w*0.55}" y1="{y+6}" x2="{x+w*0.55}" y2="{y+h-6}" stroke="black" stroke-width="1.5"/>'),
    "pump_centrifugal": lambda x, y, r=18: (
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="black" stroke-width="2"/>'
        f'<path d="M {x-r*0.7} {y+r*0.7} L {x+r*0.7} {y} L {x-r*0.7} {y-r*0.7} Z" fill="black"/>'),
    "tank": lambda x, y, w=90, h=70: (
        f'<path d="M {x} {y+10} Q {x+w/2} {y-12} {x+w} {y+10} L {x+w} {y+h} L {x} {y+h} Z" '
        f'fill="none" stroke="black" stroke-width="2"/>'),
    "valve_gate": lambda x, y, s=14: (
        f'<path d="M {x-s} {y-s*0.6} L {x} {y} L {x-s} {y+s*0.6} Z M {x+s} {y-s*0.6} L {x} {y} L {x+s} {y+s*0.6} Z" '
        f'fill="white" stroke="black" stroke-width="1.5"/>'),
    "psv": lambda x, y, s=12: (
        f'<path d="M {x-s} {y} L {x} {y-s} L {x+s} {y} L {x} {y+s} Z" fill="white" stroke="black" stroke-width="1.5"/>'
        f'<text x="{x}" y="{y-s-6}" font-size="10" text-anchor="middle" font-family="Arial">PSV</text>'),
    "instrument_bubble": lambda x, y, tag, r=14: (
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="white" stroke="black" stroke-width="1.5"/>'
        f'<line x1="{x-r}" y1="{y}" x2="{x+r}" y2="{y}" stroke="black" stroke-width="1"/>'
        f'<text x="{x}" y="{y-4}" font-size="9" text-anchor="middle" font-family="Arial">{tag[:2]}</text>'
        f'<text x="{x}" y="{y+9}" font-size="9" text-anchor="middle" font-family="Arial">{tag[2:]}</text>'),
    "heat_exchanger": lambda x, y, r=22: (
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="black" stroke-width="2"/>'
        f'<path d="M {x-r*0.6} {y+r*0.6} L {x} {y-r*0.2} L {x-r*0.3} {y-r*0.2} M {x+r*0.6} {y-r*0.6} L {x} {y+0.2*r} L {x+r*0.3} {y+0.2*r}" '
        f'stroke="black" stroke-width="1.5" fill="none"/>'),
}

@dataclass
class Equipment:
    tag: str
    kind: str
    x: int
    y: int
    label: str = ""

@dataclass
class Line:
    tag: str
    points: list[tuple[int, int]]
    spec: str = ""          # ex.: 6"-150#-CS
    arrow: bool = True

@dataclass
class PID:
    title: str
    revision: str = "A"
    equipment: list[Equipment] = field(default_factory=list)
    lines: list[Line] = field(default_factory=list)
    instruments: list[tuple[str, int, int]] = field(default_factory=list)  # (tag, x, y)

    def to_svg(self) -> str:
        W, H = 1400, 900
        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
            '<rect width="100%" height="100%" fill="white"/>',
            # Carimbo / bloco de título
            f'<rect x="{W-420}" y="{H-90}" width="410" height="80" fill="none" stroke="black" stroke-width="2"/>',
            f'<text x="{W-410}" y="{H-62}" font-size="16" font-weight="bold" font-family="Arial">{esc(self.title)}</text>',
            f'<text x="{W-410}" y="{H-38}" font-size="12" font-family="Arial">Rev. {esc(self.revision)} · ISA-5.1 / ISO 10628</text>',
            f'<text x="{W-410}" y="{H-20}" font-size="11" font-family="Arial">Gerado por Gtasck P&amp;ID Generator</text>',
        ]
        for ln in self.lines:
            pts = " ".join(f"{px},{py}" for px, py in ln.points)
            parts.append(f'<polyline points="{pts}" fill="none" stroke="black" stroke-width="2"/>')
            if ln.arrow and len(ln.points) >= 2:
                (x1, y1), (x2, y2) = ln.points[-2], ln.points[-1]
                ang = math.atan2(y2 - y1, x2 - x1)
                ax, ay = x2, y2
                a1, a2 = ang + 2.6, ang - 2.6
                parts.append(
                    f'<path d="M {ax} {ay} L {ax+12*math.cos(a1):.1f} {ay+12*math.sin(a1):.1f} '
                    f'L {ax+12*math.cos(a2):.1f} {ay+12*math.sin(a2):.1f} Z" fill="black"/>')
            mx, my = ln.points[len(ln.points)//2]
            parts.append(f'<text x="{mx}" y="{my-8}" font-size="11" text-anchor="middle" '
                         f'font-family="Arial" font-style="italic">{esc(ln.tag)} {esc(ln.spec)}</text>')
        for eq in self.equipment:
            sym = SYMBOLS.get(eq.kind)
            if sym:
                parts.append(sym(eq.x, eq.y))
            parts.append(f'<text x="{eq.x}" y="{eq.y-14}" font-size="13" font-weight="bold" '
                         f'text-anchor="middle" font-family="Arial">{esc(eq.tag)}</text>')
            if eq.label:
                parts.append(f'<text x="{eq.x}" y="{eq.y+150}" font-size="10" text-anchor="middle" '
                             f'font-family="Arial">{esc(eq.label)}</text>')
        for tag, x, y in self.instruments:
            parts.append(SYMBOLS["instrument_bubble"](x, y, esc(tag)))
        parts.append("</svg>")
        return "\n".join(parts)

def load_definition(path: str) -> PID:
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    pid = PID(title=d["title"], revision=d.get("revision", "A"))
    for e in d.get("equipment", []):
        pid.equipment.append(Equipment(**e))
    for l in d.get("lines", []):
        pid.lines.append(Line(tag=l["tag"], points=[tuple(p) for p in l["points"]],
                              spec=l.get("spec", "")))
    for i in d.get("instruments", []):
        pid.instruments.append((i["tag"], i["x"], i["y"]))
    return pid

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Gtasck P&ID Generator (ISA-5.1)")
    ap.add_argument("definition", help="JSON com a definição do diagrama")
    ap.add_argument("-o", "--output", default="pid.svg")
    args = ap.parse_args()
    pid = load_definition(args.definition)
    svg = pid.to_svg()
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"P&ID gerado: {args.output} ({len(pid.equipment)} equip., {len(pid.lines)} linhas, {len(pid.instruments)} instr.)")
