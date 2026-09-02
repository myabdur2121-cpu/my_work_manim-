from manim import *
from typing import TypeAlias

class CoorDinateOperation:
    Point: TypeAlias = list[float]
    Line: TypeAlias = list[Point]
    @staticmethod
    def slope(line: Line) -> float:
        A,B = line

        x1,y1 = A
        x2,y2 = B

        slope = (y2-y1)/(x2-x1)
        return slope

    @staticmethod
    def constant(line: Line) -> float:
        A,B = line

        x1,y1 = A
        x2,y2 = B

        constant = y1 - CoorDinateOperation.slope(line)*x1
        return constant

    @staticmethod
    def intersectionpoint(line1: Line, line2: Line) -> list[float]:

        slope1 = CoorDinateOperation.slope(line1)
        slope2 = CoorDinateOperation.slope(line2)

        constant1 = CoorDinateOperation.constant(line1)
        constant2 = CoorDinateOperation.constant(line2)

        x = (constant2-constant1)/(slope1-slope2)
        y = slope1*x + constant1

        return [x,y]

class ManimAdaptor:
    @staticmethod
    def intersectionpoint(line1: Mobject,line2 : Mobject) -> list[float]:
        line1 = [line1.get_start()[:2],line1.get_end()[:2]]
        line2 = [line2.get_start()[:2],line2.get_end()[:2]]
        point = CoorDinateOperation.intersectionpoint(line1,line2)
        point.append(0)
        point = np.array(point)
        return point

class TestScene(Scene):
    def construct(self):
        line1 = Line(LEFT * 3, RIGHT * 4)
        line2 = Line(DOWN * 2, UP * 2).rotate(30 * DEGREES)

        self.add(line1, line2)

        int_point = ManimAdaptor.intersectionpoint(line1, line2)

        dot = Dot(int_point).set_color(RED)
        self.add(dot)


%manim -v WARNING -ql TestScene
