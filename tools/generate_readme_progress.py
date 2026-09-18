#!/usr/bin/env python3
"""Generate/check SWIR Progress SVG PRO assets for Message Sender.

This legacy utility has no authoritative product roadmap or verified denominator,
so product progress is intentionally N/A. Release readiness is separate.
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "readme"

CARD = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="180" viewBox="0 0 1200 180" role="img" aria-labelledby="title desc">
  <title id="title">Message Sender product progress</title>
  <desc id="desc">Product progress is not available because this legacy utility has no authoritative measurable roadmap.</desc>
  <defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#02050A"/><stop offset="1" stop-color="#07111C"/></linearGradient><linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#0088FF"/><stop offset="1" stop-color="#62E5FF"/></linearGradient><pattern id="grid" width="26" height="26" patternUnits="userSpaceOnUse"><path d="M26 0H0V26" fill="none" stroke="#62E5FF" stroke-opacity=".05"/></pattern></defs>
  <rect x="1" y="1" width="1198" height="178" rx="24" fill="url(#bg)" stroke="#62E5FF" stroke-opacity=".22"/><rect x="1" y="1" width="1198" height="178" rx="24" fill="url(#grid)"/>
  <text x="50" y="46" fill="#62E5FF" font-family="Segoe UI, Arial, sans-serif" font-size="18" font-weight="700" letter-spacing="4">SWIR PROGRESS</text>
  <text x="50" y="82" fill="#F4FAFF" font-family="Segoe UI, Arial, sans-serif" font-size="30" font-weight="800">MESSAGE SENDER</text>
  <text x="50" y="108" fill="#8DA8B8" font-family="Segoe UI, Arial, sans-serif" font-size="15">Measured scope: product roadmap</text>
  <text x="1100" y="82" text-anchor="end" fill="#F4FAFF" font-family="Segoe UI, Arial, sans-serif" font-size="34" font-weight="800">N/A</text>
  <text x="1100" y="108" text-anchor="end" fill="#62E5FF" font-family="Segoe UI, Arial, sans-serif" font-size="15" font-weight="600" letter-spacing="1.2">NO AUTHORITATIVE ROADMAP</text>
  <rect x="50" y="126" width="1100" height="24" rx="12" fill="#08131F" stroke="#62E5FF" stroke-opacity=".14"/>
  <path d="M50 138H1150" stroke="url(#accent)" stroke-opacity=".18" stroke-width="2"/>
  <text x="50" y="168" fill="#8DA8B8" font-family="Segoe UI, Arial, sans-serif" font-size="13">Counter: N/A — no verified denominator</text>
  <text x="1150" y="168" text-anchor="end" fill="#8DA8B8" font-family="Segoe UI, Arial, sans-serif" font-size="13">Release readiness tracked separately</text>
</svg>
'''

MINI = '''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="72" viewBox="0 0 900 72" role="img" aria-labelledby="title desc">
  <title id="title">Message Sender compact product progress</title>
  <desc id="desc">Product progress N/A because no authoritative measurable roadmap exists.</desc>
  <defs><linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#0088FF"/><stop offset="1" stop-color="#62E5FF"/></linearGradient></defs>
  <rect x="1" y="1" width="898" height="70" rx="18" fill="#02050A" stroke="#62E5FF" stroke-opacity=".22"/>
  <text x="24" y="27" fill="#62E5FF" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="700" letter-spacing="2">PRODUCT ROADMAP</text>
  <text x="24" y="52" fill="#F4FAFF" font-family="Segoe UI, Arial, sans-serif" font-size="20" font-weight="800">N/A</text>
  <rect x="170" y="24" width="700" height="20" rx="10" fill="#08131F"/>
  <path d="M170 34H870" stroke="url(#accent)" stroke-opacity=".18" stroke-width="2"/>
  <text x="870" y="59" text-anchor="end" fill="#8DA8B8" font-family="Segoe UI, Arial, sans-serif" font-size="12">No verified denominator</text>
</svg>
'''

EXPECTED = {"progress-card.svg": CARD, "progress-mini.svg": MINI}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    ASSETS.mkdir(parents=True, exist_ok=True)
    stale = []
    for name, content in EXPECTED.items():
        path = ASSETS / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(name)
        else:
            path.write_text(content, encoding="utf-8")
    if stale:
        print("stale progress assets: " + ", ".join(stale))
        return 1
    print("progress assets are current" if args.check else "progress assets generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
