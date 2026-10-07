#!/usr/bin/env python3
"""Emit gnuplot commands for a 2D linear-transformation animation.

Usage: ``python mat_anim.py --frame 20 | gnuplot``.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass


def multiply(a: tuple[float, float, float, float], v: tuple[float, float]) -> tuple[float, float]:
    return a[0] * v[0] + a[1] * v[1], a[2] * v[0] + a[3] * v[1]


def at_time(a: tuple[float, float, float, float], t: float) -> tuple[float, float, float, float]:
    return (1 + t * (a[0] - 1), t * a[1], t * a[2], 1 + t * (a[3] - 1))


@dataclass
class Gnuplot:
    color: int = 3
    width: int = 2

    def line(self, p: tuple[float, float], q: tuple[float, float], arrow: bool = False) -> None:
        head = "head" if arrow else "nohead"
        print(f"set arrow from {p[0]:.6f}, {p[1]:.6f} to {q[0]:.6f}, {q[1]:.6f} {head} lt {self.color} lw {self.width}")

    def frame(self, a: tuple[float, float, float, float], grid: int) -> None:
        print("set noarrow")
        for i in range(grid + 1):
            value = -1 + 2 * i / grid
            self.line(multiply(a, (value, -1)), multiply(a, (value, 1)))
            self.line(multiply(a, (-1, value)), multiply(a, (1, value)))
        self.color, self.width = 1, 5
        self.line((0, 0), multiply(a, (1, 0)), True)
        self.line((0, 0), multiply(a, (0, 1)), True)
        print("plot [-2:2][-2:2] 1/0 title ''")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frame", "-f", type=int, default=50)
    parser.add_argument("--matrix", "-a", default="1,-0.3,-0.7,0.6", help="four comma-separated entries")
    parser.add_argument("--grid", type=int, default=10)
    args = parser.parse_args()
    entries = tuple(float(x) for x in args.matrix.split(","))
    if len(entries) != 4 or args.frame < 1 or args.grid < 1:
        parser.error("matrix needs four values; frame and grid must be positive")
    for index in range(args.frame + 1):
        Gnuplot().frame(at_time(entries, index / args.frame), args.grid)


if __name__ == "__main__":
    main()
