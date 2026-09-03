from manim import *
from typing import TypeAlias,Literal

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
    def get_proputional_value(line1: Line2D , line2: Line2D , proportion_to: Literal[1, 2]) -> float:
        A,B = line1
        C,D = line2
        AB = Operation.displacement(A,B)
        CD = Operation.displacement(C,D)
        AC = Operation.displacement(A,C)
        den = np.linalg.det(np.array([AB,CD]))
        if np.isclose(den,0):
            raise ValueError("Lines are parallel or coincident.")
        elif proportion_to == 1:
            nom = np.linalg.det(np.array([AC,CD]))
        elif proportion_to ==2:
            nom = np.linalg.det(np.array([AC,AB]))
        else:
            raise ValueError("proportion_to must be 1 or 2.")
        t = nom/den
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
        interpolate_value = Operation.get_proputional_value(line1,line2,1)

        if interpolate_value<=1 and interpolate_value>=0:
            return True
        else:
            return False

    @staticmethod
    def intersectionpoint(line1: Line2D, line2: Line2D) -> Point2D:
        t = Operation.get_proputional_value(line1,line2,1)
        point = Operation.get_point_by_proportion(line1,proportional_t=t)
        return point

    def sediment_interscetionpoint(line1: Line2D, line2: Line2D) -> Point2D | None:
        point = Operation.intersectionpoint(line1,line2)
        expectation = Operation.interscetion(line1,line2)
        if expectation:
            return point
        else:
            return None

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
    def displacement2D(point1: Mobject, point2: Mobject) -> Line2D:
        point1 = ManimAdaptor.convert_point_3d_to_2d(point1)
        point2 = ManimAdaptor.convert_point_3d_to_2d(point2)
        displacement = Operation.displacement(point1,point2)
        return displacement

    @staticmethod
    def get_proputional_value(line1: Mobject , line2: Mobject , proportion_to: Literal[1,2]) -> float:
        line1 = ManimAdaptor.convert_line_3d_to_2d(line1)
        line2 = ManimAdaptor.convert_line_3d_to_2d(line2)
        return Operation.get_proputional_value(line1,line2,proportion_to)
    @staticmethod
    def get_point_by_proportion(line: Mobject, proportional_t: float) -> Point3D:
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
        t = ManimAdaptor.get_proputional_value(line1,line2,1)
        point = ManimAdaptor.get_point_by_proportion(line1,proportional_t=t)
        return point

    @staticmethod
    def sediment_interscetionpoint(line1: Mobject, line2: Mobject) -> Point2D | None:
        point = ManimAdaptor.intersectionpoint(line1,line2)
        expectation = ManimAdaptor.interscetion(line1,line2)
        if expectation:
            return point
        else:
            return None


class AnimationScene(Scene):
    def construct(self):
        line1 = Line()
        line2 = Line().shift(DOWN*2).rotate(50*DEGREES)
        self.add(line1,line2)
        dot = ManimAdaptor.sediment_interscetionpoint(line1,line2)
        dot = Dot(dot)
        self.add(dot)
%manim -v WARNING -ql AnimationScene
    

class AnimationScene(Scene):
    def construct(self):
        pass 
%manim -v WARNING -ql AnimationScene
