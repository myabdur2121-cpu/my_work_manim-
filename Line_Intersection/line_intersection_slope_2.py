from manim import *
from typing import TypeAlias

Point2D: TypeAlias = list[float]
Line2D: TypeAlias = list[Point2D]

Point3D: TypeAlias = Point2D
Line3D: TypeAlias = Line2D

class Operation:
    @staticmethod
    def displacement(point1: Point2D, point2: Point2D) -> Point2D:
        x1,y1 = point1
        x2,y2 = point2

        displacement = [x2-x1,y2-y1]
        return displacement

    @staticmethod
    def get_proputional_value(line1: Line2D , line2: Line2D , proportion_to: Line2D) -> float:
        A,B = line1
        C,D = line2

        AB = Operation.displacement(A,B)
        CD = Operation.displacement(C,D)
        AC = Operation.displacement(A,C)



        if proportion_to is line1:
            matrix1 = np.array([AC,CD])
            matrix2 = np.array([AB,CD])
        else:
            matrix1 = np.array([AC,AB])
            matrix2 = np.array([AB,CD])

        t = np.linalg.det(matrix1)/np.linalg.det(matrix2)
        return t

    @staticmethod
    def get_point_by_proportion(line: Line2D, proportional_t: float) -> Point2D:
        point1,point2 = line
        x1,y1 = point1
        x2,y2 = point2

        x = x1 + proportional_t*(x2-x1)
        y = y1 + proportional_t*(y2-y1)

        return [x,y]


    @staticmethod
    def interscetion(line1: Line2D, line2: Line2D) -> bool:
        interpolate_value = Operation.get_proputional_value(line1,line2,line1)

        if interpolate_value<=1 and interpolate_value>=0:
            return True
        else:
            return False

class ManimAdaptor:
    @staticmethod
    def convert_line_3d_to_2d(line: Mobject) -> Line2D:
        line = [line.get_start()[:2],line.get_end()[:2]]
        return line
    @staticmethod
    def convert_point_3d_to_2d(point: Mobject) -> Point2D:
        point = point.get_center()[:2]
        return point
    @staticmethod
    def convert_point_2d_to_3d(point: Point) -> Point3D:
        point.append(0)
        point = np.array(point)
        return point
    @staticmethod
    def convert_line_2d_to_3d(line: Line2D) -> Line3D:
        line = [ManimAdaptor.convert_point_2d_to_3d(line[0]),ManimAdaptor.convert_point_2d_to_3d(line[1])]
        return line

    @staticmethod
    def displacement3D(point1: Mobject, point2: Mobject) -> Point3D:
        point1 = ManimAdaptor.convert_point_3d_to_2d(point1)
        point2 = ManimAdaptor.convert_point_3d_to_2d(point2)
        displacement = Operation.displacement(point1,point2)
        displacement = ManimAdaptor.convert_point_2d_to_3d(displacement)
        return displacement
    @staticmethod
    def displacement2D(line1: Mobject, line2: Mobject) -> Line2D:
        line1 = ManimAdaptor.convert_line_3d_to_2d(line1)
        line2 = ManimAdaptor.convert_line_3d_to_2d(line2)
        displacement = Operation.displacement(line1,line2)
        return displacement
    
    @staticmethod
    def get_proputional_value(self, line1: Mobject , line2: Mobject , proportion_to: Mobject) -> float:
        line1 = ManimAdaptor.convert_line_3d_to_2d(line1)
        line2 = ManimAdaptor.convert_line_3d_to_2d(line2)
        proportion_to = ManimAdaptor.convert_line_3d_to_2d(proportion_to)
        return Operation.get_proputional_value(line1,line2,proportion_to)

    def get_point_by_proportion(self, line: Mobject, proportional_t: float) -> Point3D:
        line = ManimAdaptor.convert_line_3d_to_2d(line)
        point = Operation.get_point_by_proportion(line,proportional_t)
        point = ManimAdaptor.convert_point_2d_to_3d(point)
        return point

    @staticmethod
    def interscetion(line1: Mobject, line2: Mobject) -> bool:
        line1 = ManimAdaptor.convert_line_3d_to_2d(line1)
        line2 = ManimAdaptor.convert_line_3d_to_2d(line2)
        return Operation.interscetion(line1,line2)

    @staticmethod
    def intersectionpoint(line1: Mobject, line2: Mobject) -> Point3D:
        point = ManimAdaptor.get_point_by_proportion(line1,line2)
        return point


class AnimationScene(Scene):
    def construct(self):
        pass
%manim -v WARNING -ql AnimationScene
