"""
paper_lib — নোটবুক-পেপার স্টাইল chart toolkit
Updated v2.0 | 2026-09-05

Logical inheritance map:
    manim.Rectangle   + PaperOps       -> Paper
    manim.Axes        + CoordinateOps  -> Axes
    manim.NumberPlane + CoordinateOps  -> NumberPlane

পুরনো নাম -> নতুন নাম:
    PublicOperation         -> PaperOps
    CordianteBasedOperation -> CoordinateOps
    "standart"              -> "standard"
"""

from typing import Literal

import numpy as np
from manim import *
from manim import Axes as _ManimAxes
from manim import NumberPlane as _ManimNumberPlane


class CoordinateOps:
    """Axes/NumberPlane-এর mixin: random point tools (এখন instance method)।"""

    def random_point(self, x_range=None, y_range=None, **kwargs):
        """একটা random Dot — default range = object-এর নিজের range।"""
        x_min, x_max = (x_range[0], x_range[1]) if x_range else (self.x_range[0], self.x_range[1])
        y_min, y_max = (y_range[0], y_range[1]) if y_range else (self.y_range[0], self.y_range[1])
        x = np.random.uniform(x_min, x_max)
        y = np.random.uniform(y_min, y_max)
        kwargs.setdefault("color", BLACK)
        return Dot(self.c2p(x, y), **kwargs)

    def random_points(self, points=10, **kwargs):
        """points সংখ্যক random Dot-এর VGroup; self.dots-এও save হয়।"""
        self.dots = VGroup(*(self.random_point(**kwargs) for _ in range(points)))
        return self.dots


class PaperOps:
    """Rectangle/Paper-এর mixin: axes, grid, ruled lines, vertex labels।"""

    @staticmethod
    def _plot_center(coord):
        """Plot-area-র center — c2p anchor (bbox নয়, তাই shift-গ্লিচ নেই)।"""
        xm = (coord.x_range[0] + coord.x_range[1]) / 2
        ym = (coord.y_range[0] + coord.y_range[1]) / 2
        return coord.c2p(xm, ym)

    def add_axes(self, **kwargs):
        base = dict(
            x_range=[-5, 5, 1],
            y_range=[-10, 10, 1],
            x_length=self.width,
            y_length=self.height,
            axis_config={"color": BLACK, "include_tip": False},
        )
        base.update(kwargs)
        ax = Axes(**base)
        ax.shift(self.get_center() - self._plot_center(ax))
        return ax

    def add_grid(self, **kwargs):
        base = dict(
            x_range=[-5, 5, 1],
            y_range=[-10, 10, 1],
            x_length=self.width,
            y_length=self.height,
            axis_config={"color": BLACK, "include_tip": False},
        )
        base.update(kwargs)
        grid = NumberPlane(**base)
        grid.shift(self.get_center() - self._plot_center(grid))
        return grid

    def add_lines(self, lines=10, visual_lines=True, buff=0.2, **kwargs):
        """অনুভূমিক ruled lines; buff = কাগজের ধার থেকে ভিতরের দিকে ফাঁকা।"""
        kwargs.setdefault("color", BLACK)
        kwargs.setdefault("stroke_width", 1)
        left_x = self.get_left()[0] + buff
        right_x = self.get_right()[0] - buff
        ys = np.linspace(self.get_top()[1], self.get_bottom()[1], lines)
        group = VGroup(*(Line([left_x, y, 0], [right_x, y, 0], **kwargs) for y in ys))
        if visual_lines and len(group) > 2:
            group.remove(group[0], group[-1])  # প্রথম-শেষ line কাগজের edge-এর সাথে মিলে যেতো
        return group

    def show_vertices(self, vertex_index=None, position_scale_factor=1.2, **kwargs):
        """Vertex গুলো label করে; int / list / None তিনটাই চলে; যেকোনো অবস্থানে কাজ করে।"""
        verts = self.get_vertices()
        if vertex_index is None:
            chosen = list(range(len(verts)))
        elif isinstance(vertex_index, (int, np.integer)):
            chosen = [int(vertex_index)]
        else:
            chosen = [int(i) for i in vertex_index]
        center = self.get_center()
        labels = VGroup()
        for vi in chosen:
            target = center + (verts[vi] - center) * position_scale_factor
            try:
                label = MathTex(str(vi), **kwargs)
            except Exception:
                label = Text(str(vi), **kwargs)
            labels.add(label.move_to(target))
        self.add(labels)
        return labels


class Axes(_ManimAxes, CoordinateOps):
    """manim Axes + random point tools।"""


class NumberPlane(_ManimNumberPlane, CoordinateOps):
    """manim NumberPlane + random point tools।"""


class Paper(Rectangle, PaperOps):
    """নোটবুক-পেপার: cream fill + সঠিক aspect ratio (width = height × 9/11)।"""

    def __init__(self, mode: Literal["standard"] | None = "standard", **kwargs):
        self.mode = mode
        if mode == "standard":
            height = kwargs.get("height", 6)
            kwargs.setdefault("height", height)
            if "width" not in kwargs:
                kwargs["width"] = height * (9 / 11)
            kwargs.setdefault("fill_color", "#F8F5E9")
            kwargs.setdefault("fill_opacity", 1)
            kwargs.setdefault("stroke_color", "#3B3B3B")
        super().__init__(**kwargs)
