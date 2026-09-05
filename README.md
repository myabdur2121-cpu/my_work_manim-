# my_work_manim

A **testing ground** for [Manim](https://www.manim.community/) code.

Think of it as an exam hall. Code is written, brought here, and put through its
paces in Colab — download it, import it, render it, break it, fix it. Only once
it passes does it move on to whichever main repo it belongs to.

```
write  →  my_work_manim (test here)  →  passes  →  main repo
                    ↑                        |
                    └────────  fix  ─────────┘
```

Nothing here is a destination. Everything here is on its way somewhere.

## Why a separate repo

Main repos have structure — packaging, tests, docs, a public API, a commit
history worth reading. All of that is good for finished code and pure friction
for code you're still arguing with.

So this repo stays flat and disposable on purpose:

| | Main repos | Here |
| --- | --- | --- |
| Layout | packaged, `src/`, docs | one flat `.py` per idea |
| Install | `pip install` | `pip install git+…` **or** `wget` a single file |
| Stability | expected | none promised |
| Lifespan | permanent | until it graduates |
| Half-finished code | no | yes, that's the point |

If you want something dependable, take it from the main repo it graduated to —
not from here.

## How to use the code

Two ways. **Method A** installs the repo as a package (possible since
`pyproject.toml` landed). **Method B** keeps the old single-file flow for
quick bench work.

### A. pip install — the whole repo, one line

```bash
!pip install -q git+https://github.com/myabdur2121-cpu/my_work_manim-.git
```

```python
from instant_project_module import needle_project_lib as my_manimlib
import my_manimlib   # root helper lib (MobjectHelper mixin)
```

`dependencies = ["manim"]` makes pip pull Manim in as well. The *system*
libraries Manim needs (ffmpeg/cairo/pango/TeX) cannot come from pip — see
Requirements for the apt line.

### B. wget a single file — still supported

Every library file here can also be used as a **single standalone `.py`**:
download the one file you want and import it, no packaging involved.

#### 1. Download

For instant download, use this code and change the file name:

```bash
!wget -O /content/my_manimlib.py \
    https://raw.githubusercontent.com/myabdur2121-cpu/my_work_manim-/main/line_intersection_final.py
```

`-O /content/my_manimlib.py` sets the local name. Keeping it fixed means the
import line below never changes, whichever source file is on the bench.

For a file inside a folder, extend the URL with the folder name:

```bash
!wget -O /content/my_manimlib.py \
    https://raw.githubusercontent.com/myabdur2121-cpu/my_work_manim-/main/Line_Intersection/line_intersection_slope_2.py
```

#### 2. Import

`/content` is already on `sys.path` in Colab, so a plain import works:

```python
from my_manimlib import GeometryOperations, ManimGeometryAdapter
```

Or pull in everything, which is usually what you want while testing:

```python
from my_manimlib import *
```

#### 3. Re-download after editing

Python caches modules, so a second `wget` alone won't take effect. Reload it:

```python
import importlib, my_manimlib
importlib.reload(my_manimlib)
from my_manimlib import *
```

If the file changed a lot — new classes, renamed symbols — restart the runtime
instead. Reload doesn't remove names that no longer exist.

#### 4. Render

```python
%%manim -qm -v WARNING SceneName
```

or from the shell:

```bash
!manim -ql /content/my_manimlib.py SceneName
```

## What's on the bench

### Top level

| File | What it is | Status |
| --- | --- | --- |
| [`line_intersection_final.py`](line_intersection_final.py) | `GeometryOperations` — pure-math 2D core: displacement, proportional `t`, line/segment intersection tests and points. Plus `ManimGeometryAdapter`, the same calls bridged to Manim `Mobject`s and 3D points. | ✅ **Passed** — graduated to [manim-extras](https://github.com/myabdur2121-cpu/manim-extras) |
| [`NeedleNeedleExperiment.py`](NeedleNeedleExperiment.py) | Buffon's Needle setup — a `Paper` Mobject (`Rectangle` subclass with vertex labelling) and the `NeedleNeedleExperiment` scene. | 🚧 Still sitting the exam |
| [`my_manimlib.py`](my_manimlib.py) | `MobjectHelper` mixin — `get_bbox()` returns the bounding box as a visible `Polygon`: `c2p` plot-area corners for Axes (equal centres, no shift), `get_corner` fallback for anything else. | ✅ In use |
| [`pyproject.toml`](pyproject.toml) | Makes the repo pip-installable: root module `my_manimlib` + package `instant_project_module`; declares `manim` as a dependency. | 🔧 Tooling |

### `instant_project_module/`

| File | What it is | Status |
| --- | --- | --- |
| [`needle_project_lib.py`](instant_project_module/needle_project_lib.py) | Notebook-paper toolkit v2.0 — `Paper` (cream-filled `Rectangle`, 9:11 aspect), `PaperOps` (`add_axes`, `add_grid`, `add_lines`, `show_vertices`), `CoordinateOps` (`random_point`, `random_points`), enhanced `Axes`/`NumberPlane`. | 🚧 Still sitting the exam |
| [`__init__.py`](instant_project_module/__init__.py) | Makes the folder a package so `pip install git+…` can ship it. | 🔧 Tooling |

### `Line_Intersection/` — the earlier attempts

Three runs at the same problem, kept because the progression is the useful part.
Read them in order:

| File | Approach | Verdict |
| --- | --- | --- |
| [`line_intersection_slope.py`](Line_Intersection/line_intersection_slope.py) | Slope-based. `CoorDinateOperation` + `ManimAdaptor` + `TestScene`. | ❌ Vertical lines have infinite slope — special-casing everywhere. |
| [`line_intersection_slope_2.py`](Line_Intersection/line_intersection_slope_2.py) | Slope again, reworked. `Operation` + `ManimAdaptor` + `AnimationScene`. | ❌ Cleaner, same underlying weakness. |
| [`line_interscetion_cross_product.py`](Line_Intersection/line_interscetion_cross_product.py) | Cross-product / determinant. `Operation` + `ManimAdaptor` + `AnimationScene`. | ✅ No division, so parallel lines fall out as `det = 0`. Became `line_intersection_final.py`. |

Every file here follows the same shape: a **pure-math class** that knows nothing
about Manim, an **adapter class** that converts `Mobject`s to plain numbers and
back, and a **scene** to look at it. That separation is what makes a file easy
to test — the math runs without rendering anything, so a failure is a failure in
the math and not in the animation.

## Requirements

Manim Community, NumPy, and ffmpeg on `PATH`.

On a bare machine or Colab, Manim also needs system libraries (pip cannot
install these):

```bash
!apt-get install -y -qq ffmpeg libcairo2-dev libpango1.0-dev texlive-latex-extra
```

`line_intersection_final.py` uses `TypeAlias` and `X | None` unions, so
**Python ≥ 3.10**. Colab is fine.

## Housekeeping

Rough edges that come with a scratch repo — noted, not urgent:

- `line_interscetion_cross_product.py` defines `AnimationScene` twice (lines 138
  and 149); the second silently wins.
- Same file: *interscetion* → *intersection*.
- Two names for the same role, `ManimAdaptor` vs `ManimGeometryAdapter`. The
  graduated spelling is the keeper.
