from manim import *
from typing import Literal


class Paper(Rectangle):
    def __init__(self, mode : Literal["standart"] | None =None, **kwargs):
        self.mode = mode
        if self.mode == "standart":
            height = kwargs.get("height",6)
            kwargs["height"] = height
            kwargs["width"] = height*(9/11)
            kwargs["fill_color"]="#F8F5E9"
            kwargs["fill_opacity"]=1
        super().__init__(**kwargs)

    def get_height(self):
        height = self.get_top()[1] - self.get_bottom()[1]
        return height

    def get_width(self):
        width = self.get_right()[0]-self.get_left()[0]
        return width

    def add_vertices_lable(self,vertices_index=None,label_ver_dis = 0.5,**kwargs):
        if vertices_index is None:
            vertices_index = [0,1,2,3]
        vertices = self.get_vertices()
        ver_labels = VGroup()
        show_vertices = VGroup()
        for ver , label , pos  in zip(vertices,["0","1","2","3"],[UR,UL,DL,DR]):
            try:
                ver_label = Tex(label,**kwargs).move_to(ver+pos*label_ver_dis)
            except:
                ver_label = Text(label,**kwargs).move_to(ver+pos*label_ver_dis)
            ver_labels.add(ver_label)
        for i in vertices_index:
            show_vertices.add(ver_labels[i])
        self.add(show_vertices)
        return show_vertices

class NeedleNeedleExperiment(Scene):
    def construct(self):
        paper = Paper(mode="standart")
        paper.add_vertices_lable(color=BLUE, font_size=50,label_ver_dis=0.2)
        self.add(paper)
        self.wait(2)

%manim -v WARNING -ql NeedleNeedleExperiment
