#!/data/data/com.termux/files/usr/bin/python3
"""
7-Symbol Computational Language
Glyphs:
  ●  NODE
  ─  LINK
  ≈  ENERGY
  □  STORE
  →  RETURN
  ○  OBSERVE
  ✧  TRANSFORM

Also models black-core + vacuum temperature differential.
"""

import math, sys, json
from pathlib import Path

GLYPHS = {
    "●": "NODE",
    "─": "LINK",
    "≈": "ENERGY",
    "□": "STORE",
    "→": "RETURN",
    "○": "OBSERVE",
    "✧": "TRANSFORM",
}

# Physical constants
SIGMA = 5.670374419e-8  # Stefan-Boltzmann W/m²K⁴

class Seven:
    def __init__(self):
        self.store = {}          # □ memory
        self.nodes = {}          # ● registry
        self.energy = 1.0        # ≈ current
        self.history = []

    def parse(self, expr: str):
        """Tokenize a 7-symbol expression (spaces or direct glyphs)."""
        tokens = []
        for ch in expr.replace(" ", ""):
            if ch in GLYPHS:
                tokens.append(ch)
            elif ch.isdigit() or ch == ".":
                if tokens and isinstance(tokens[-1], (int, float)):
                    tokens[-1] = float(str(tokens[-1]) + ch)
                else:
                    tokens.append(float(ch) if "." in ch else int(ch))
            else:
                pass  # ignore unknown
        return tokens

    def eval(self, expr: str):
        tokens = self.parse(expr)
        stack = []
        for t in tokens:
            if t == "●":
                stack.append({"type": "NODE", "id": len(self.nodes)})
            elif t == "─":
                if len(stack) >= 2:
                    b, a = stack.pop(), stack.pop()
                    stack.append({"type": "LINK", "a": a, "b": b})
            elif t == "≈":
                val = stack.pop() if stack else self.energy
                self.energy = float(val) if isinstance(val, (int, float)) else self.energy
                stack.append(self.energy)
            elif t == "□":
                val = stack.pop() if stack else None
                key = f"s{len(self.store)}"
                self.store[key] = val
                stack.append(key)
            elif t == "→":
                val = stack.pop() if stack else None
                stack.append({"returned": val})
            elif t == "○":
                # observe → push current state summary
                stack.append({
                    "energy": self.energy,
                    "store_keys": list(self.store.keys()),
                    "nodes": len(self.nodes)
                })
            elif t == "✧":
                # transform: simple phi-scaled compound on energy
                self.energy *= (1.0 + 0.0618)
                stack.append(self.energy)
            elif isinstance(t, (int, float)):
                stack.append(t)
        self.history.append({"expr": expr, "result": stack[-1] if stack else None})
        return stack[-1] if stack else None

    def delta_T(self, T_env=300.0, alpha=0.97, epsilon=0.97, area=1.0, power_in=100.0):
        """
        Approximate steady-state core temperature under vacuum.
        power_in in watts absorbed by black core.
        Returns T_core (K) and ΔT.
        """
        # P_in = ε σ A T^4  →  T = (P_in / (ε σ A)) ** 0.25
        if power_in <= 0:
            return T_env, 0.0
        T_core = (power_in / (epsilon * SIGMA * area)) ** 0.25
        return T_core, T_core - T_env

    def status(self):
        return {
            "glyphs": GLYPHS,
            "energy": self.energy,
            "store": self.store,
            "history_len": len(self.history)
        }

def main():
    s = Seven()
    if len(sys.argv) < 2:
        print(json.dumps(s.status(), indent=2))
        print("\nExamples:")
        print("  python3 seven.py '● ≈ 10 □'")
        print("  python3 seven.py '○ ✧ ✧'")
        print("  python3 seven.py deltaT 150")
        return

    cmd = sys.argv[1]
    if cmd == "deltaT":
        power = float(sys.argv[2]) if len(sys.argv) > 2 else 100.0
        T, dT = s.delta_T(power_in=power)
        print(json.dumps({"T_core_K": round(T, 2), "delta_T_K": round(dT, 2), "power_W": power}, indent=2))
    else:
        # treat whole argv as expression
        expr = " ".join(sys.argv[1:])
        result = s.eval(expr)
        print(json.dumps({"expr": expr, "result": result, "energy": s.energy}, indent=2, default=str))

if __name__ == "__main__":
    main()
