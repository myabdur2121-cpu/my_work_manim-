from manim import *
from typing import TypeAlias, Literal
import numpy as np

Point2D: TypeAlias = list[float]
Line2D: TypeAlias = list[Point2D]
Point3D: TypeAlias = np.ndarray
Line3D: TypeAlias = list[Point3D]

class GeometryOperations:
    @staticmethod
    def displacement(point1: Point2D, point2: Point2D) -> Point2D:
        x1, y1 = point1
        x2, y2 = point2
        return [x2 - x1, y2 - y1]

    @staticmethod
    def get_proportional_value(line1: Line2D, line2: Line2D, proportion_to: Literal[1, 2]) -> float:
        A, B = line1
        C, D = line2
        AB = GeometryOperations.displacement(A, B)
        CD = GeometryOperations.displacement(C, D)
        AC = GeometryOperations.displacement(A, C)
        denominator = np.linalg.det(np.array([AB, CD]))
        if np.isclose(denominator, 0):
            raise ValueError("Lines are parallel or coincident.")
        if proportion_to == 1:
            numerator = np.linalg.det(np.array([AC, CD]))
        elif proportion_to == 2:
            numerator = np.linalg.det(np.array([AC, AB]))
        else:
            raise ValueError("proportion_to must be 1 or 2.")
        return numerator / denominator

    @staticmethod
    def get_point_by_proportion(line: Line2D, proportional_t: float) -> Point2D:
        A, B = line
        return [A[0] + proportional_t * (B[0] - A[0]), A[1] + proportional_t * (B[1] - A[1])]

    @staticmethod
    def lines_intersect(line1: Line2D, line2: Line2D) -> bool:
        GeometryOperations.get_proportional_value(line1, line2, 1)
        return True

    @staticmethod
    def segments_intersect(line1: Line2D, line2: Line2D) -> bool:
        t = GeometryOperations.get_proportional_value(line1, line2, 1)
        u = GeometryOperations.get_proportional_value(line1, line2, 2)
        return 0 <= t <= 1 and 0 <= u <= 1

    @staticmethod
    def intersection_point(line1: Line2D, line2: Line2D) -> Point2D:
        t = GeometryOperations.get_proportional_value(line1, line2, 1)
        return GeometryOperations.get_point_by_proportion(line1, proportional_t=t)

    @staticmethod
    def segment_intersection_point(line1: Line2D, line2: Line2D) -> Point2D | None:
        if not GeometryOperations.segments_intersect(line1, line2):
            return None
        return GeometryOperations.intersection_point(line1, line2)

class ManimGeometryAdapter:
    @staticmethod
    def convert_line_3d_to_2d(line: Mobject) -> Line2D:
        return [line.get_start()[:2].tolist(), line.get_end()[:2].tolist()]

    @staticmethod
    def convert_point_3d_to_2d(point: Mobject) -> Point2D:
        return point.get_center()[:2].tolist()

    @staticmethod
    def convert_point_2d_to_3d(point: Point2D) -> Point3D:
        return np.array([point[0], point[1], 0.0])

    @staticmethod
    def convert_line_2d_to_3d(line: Line2D) -> Line3D:
        return [ManimGeometryAdapter.convert_point_2d_to_3d(line[0]), ManimGeometryAdapter.convert_point_2d_to_3d(line[1])]

    @staticmethod
    def displacement_2d(point1: Mobject, point2: Mobject) -> Point2D:
        point1 = ManimGeometryAdapter.convert_point_3d_to_2d(point1)
        point2 = ManimGeometryAdapter.convert_point_3d_to_2d(point2)
        return GeometryOperations.displacement(point1, point2)

    @staticmethod
    def displacement_3d(point1: Mobject, point2: Mobject) -> Point3D:
        displacement = ManimGeometryAdapter.displacement_2d(point1, point2)
        return ManimGeometryAdapter.convert_point_2d_to_3d(displacement)

    @staticmethod
    def get_proportional_value(line1: Mobject, line2: Mobject, proportion_to: Literal[1, 2]) -> float:
        line1 = ManimGeometryAdapter.convert_line_3d_to_2d(line1)
        line2 = ManimGeometryAdapter.convert_line_3d_to_2d(line2)
        return GeometryOperations.get_proportional_value(line1, line2, proportion_to)

    @staticmethod
    def get_point_by_proportion(line: Mobject, proportional_t: float) -> Point3D:
        line = ManimGeometryAdapter.convert_line_3d_to_2d(line)
        point = GeometryOperations.get_point_by_proportion(line, proportional_t)
        return ManimGeometryAdapter.convert_point_2d_to_3d(point)

    @staticmethod
    def lines_intersect(line1: Mobject, line2: Mobject) -> bool:
        line1 = ManimGeometryAdapter.convert_line_3d_to_2d(line1)
        line2 = ManimGeometryAdapter.convert_line_3d_to_2d(line2)
        return GeometryOperations.lines_intersect(line1, line2)

    @staticmethod
    def segments_intersect(line1: Mobject, line2: Mobject) -> bool:
        line1 = ManimGeometryAdapter.convert_line_3d_to_2d(line1)
        line2 = ManimGeometryAdapter.convert_line_3d_to_2d(line2)
        return GeometryOperations.segments_intersect(line1, line2)

    @staticmethod
    def intersection_point(line1: Mobject, line2: Mobject) -> Point3D:
        t = ManimGeometryAdapter.get_proportional_value(line1, line2, 1)
        return ManimGeometryAdapter.get_point_by_proportion(line1, proportional_t=t)

    @staticmethod
    def segment_intersection_point(line1: Mobject, line2: Mobject) -> Point3D | None:
        if not ManimGeometryAdapter.segments_intersect(line1, line2):
            return None
        return ManimGeometryAdapter.intersection_point(line1, line2)

