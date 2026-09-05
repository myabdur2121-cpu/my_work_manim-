"""
my_manimlib — ব্যক্তিগত manim helper library (v1.0 | 2026-09-05)

ব্যবহার:
    from manim import *
    import my_manimlib

    class MyAxes(Axes, my_manimlib.MobjectHelper):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

নোট: scene file-এর পাশে (একই folder-এ) এই file টা রাখবেন,
তাহলে `import my_manimlib` যেকোনো সময় কাজ করবে।
"""

from manim import *


class MobjectHelper:
    """Mixin class — Axes/Mobject subclass-এ helper method যোগ করে।"""

    def get_bbox(self, **kwargs):
        """Bounding box-কে দৃশ্যমান Polygon হিসেবে return করে।

        - Axes হলে: plot-area-র চার কোণা (c2p) → lines-এর সাথে হুবহু মিলে,
          center সমান, কোনো shift নেই।
        - অন্য যেকোনো Mobject হলে: fallback = true bbox (get_corner)।

        kwargs = Polygon-এর styling (color, stroke_width, ...)
        """
        if "vertices" not in kwargs:
            if hasattr(self, "c2p") and hasattr(self, "x_range"):
                x0, x1 = self.x_range[0], self.x_range[1]
                y0, y1 = self.y_range[0], self.y_range[1]
                vertices = [
                    self.c2p(x0, y1),  # UL
                    self.c2p(x1, y1),  # UR
                    self.c2p(x1, y0),  # DR
                    self.c2p(x0, y0),  # DL
                ]
            else:
                vertices = [self.get_corner(i) for i in [UL, UR, DR, DL]]
        else:
            vertices = kwargs.pop("vertices")
        self.vertices = vertices
        self.bbox = Polygon(*vertices, **kwargs)
        return self.bbox
