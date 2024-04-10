# example.py

from manim import *  # or: from manimlib import *

from manim_slides import Slide


def Item(*str,dot = True,font_size = 35,math=False,pw="8cm"):
    if math:
        tex = MathTex(*str,font_size=font_size)
    else:
        tex = Tex(*str,font_size=font_size,tex_environment=f"{{minipage}}{{{pw}}}")
    if dot:
        dot = MathTex("\\cdot").scale(2)
        dot.next_to(tex[0][0], LEFT, SMALL_BUFF)
        tex[0].add_to_back(dot)
    else:
        dot = MathTex("\\cdot",color=BLACK).scale(2)
        dot.next_to(tex[0], LEFT, SMALL_BUFF)
        tex[0].add_to_back(dot)
    g2 = VGroup()
    for item in tex:
        g2.add(item)

    return(g2)


def ItemList(*item,buff=MED_SMALL_BUFF):
    list = VGroup(*item).arrange(DOWN, aligned_edge=LEFT,buff=buff)
    return(list)

def MyLabeledDot(label_in:Tex| None = None,label_out:Tex| None = None,pos:Vector = DOWN,shift=[0,0,0], point=ORIGIN,radius: float = DEFAULT_DOT_RADIUS,color = WHITE):
        if isinstance(label_in, Tex):
            radius = 0.02 + max(label_in.width, label_in.height) / 2
        
        dot = Dot(point=point,radius=radius,color=color)
        g1 = VGroup(dot)
        if isinstance(label_in, Tex):
            label_in.move_to(dot.get_center())
            g1.add(label_in)
        if isinstance(label_out, Tex):
            label_out.next_to(dot,pos)
            label_out.shift(shift)
            g1.add(label_out)

        return g1


class MyDashLabeledLine(DashedLine):
    def __init__(self,label: Tex|MathTex, pos = None, rel_pos: float = 0.5,bg = BLACK, opacity:float= 0.7,rot: bool =True  , *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # calculating the vector for the label position
        line_start, line_end = self.get_start_and_end()
        new_vec = (line_end - line_start) * rel_pos
        label_coords = line_start + new_vec
        label.move_to(label_coords)
        
        if rot:
            ang=angle_of_vector(self.get_unit_vector())
            if ang < -PI/2:
                ang =  ang+PI
            elif ang > PI/2:
                ang=ang-PI

            label.rotate(ang)

        if pos is None:
            mask  = Line(label.get_center()-0.6*label.width*self.get_unit_vector(),label.get_center()+0.6*label.width*self.get_unit_vector(),color=bg,stroke_width=self.get_stroke_width()+1,stroke_opacity=opacity)
            self.add(mask)
        else:
            label.shift(pos)
        self.add(label)

class MyLabeledLine(Line):
    def __init__(self,label: Tex|MathTex, pos = None, rel_pos: float = 0.5,bg = BLACK, opacity:float= 0.7,rot: bool =True , *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # calculating the vector for the label position
        line_start, line_end = self.get_start_and_end()
        new_vec = (line_end - line_start) * rel_pos
        label_coords = line_start + new_vec
        label.move_to(label_coords)
        if pos is None:
            if rot:
                mask  = Line(label.get_center()-0.65*label.width*self.get_unit_vector(),label.get_center()+0.65*label.width*self.get_unit_vector(),color=bg,stroke_width=self.get_stroke_width()+1,stroke_opacity=opacity)
            else:
                mask  = Line(label.get_center()-0.65*label.height*self.get_unit_vector(),label.get_center()+0.65*label.height*self.get_unit_vector(),color=bg,stroke_width=self.get_stroke_width()+1,stroke_opacity=opacity)
            self.add(mask)
        else:
            label.shift(pos)
        
        if rot:
            ang=angle_of_vector(self.get_unit_vector())
            if ang < -PI/2:
                ang =  ang+PI
            elif ang > PI/2:
                ang=ang-PI

            label.rotate(ang)
        self.add(label)


class MyLabeledArrow(MyLabeledLine, Arrow):

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(buff=0,*args, **kwargs)

class MyDoubLabArrow(MyLabeledLine, DoubleArrow):

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(buff=0,*args, **kwargs)

def Ray(start,end,ext:float=0,eext:float = 0,pos:float=0.5,color=BLUE):
    dir_lin = Line(start=start,end=end)
    dir = dir_lin.get_length()*ext*dir_lin.get_unit_vector()
    edir = dir_lin.get_length()*eext*dir_lin.get_unit_vector()
    lin = Line(start=start-edir,end=end+dir,color=color)
    arrow_start = lin.get_start()+pos*lin.get_length()*lin.get_unit_vector()
    arrow = Arrow(start=arrow_start-0.1*lin.get_unit_vector(),end=arrow_start+0.1*lin.get_unit_vector(),tip_shape=StealthTip,max_tip_length_to_length_ratio=0.75,color=color)
    ray = VGroup(lin,arrow)
    return ray

def CurvedRay(start,end,ext:float=0,radius=2,color=RED,rev = False):
    arc = ArcBetweenPoints(start=start,end=end,radius=radius,color=color)
    n = int(len(arc.get_all_points())/2)
    pt = arc.get_all_points()[n]
    pt2 = arc.get_all_points()[n+1]
    if rev:
        arrow = Arrow(start=pt2,end=pt,tip_shape=StealthTip,max_tip_length_to_length_ratio=0.75,color=color)
    else:
        arrow = Arrow(start=pt,end=pt2,tip_shape=StealthTip,max_tip_length_to_length_ratio=0.75,color=color)
    ray = VGroup(arc,arrow)
    return ray


def ir(a,b): # inclusive range, useful for TransformByGlyphMap
    return list(range(a,b+1))


class LatexItems(Tex):
    def __init__(self, *args, page_width="15em", itemize="itemize",font_size=35, **kwargs):
        template = TexTemplate()
        template.body = (r"\documentclass[preview]{standalone}\usepackage[english]{babel}"
                         r"\usepackage{amsmath}\usepackage{amssymb}\begin{document}"
                         rf"\begin{{minipage}}{{{page_width}}}"
                         rf"\begin{{{itemize}}}YourTextHere\end{{{itemize}}}"
                         r"\end{minipage}\end{document}"
        )
        super().__init__(*args, tex_template=template, tex_environment=None,font_size=font_size, **kwargs)


class AlignTex(Tex):
    def __init__(self, *args, page_width="15em",align="align*",font_size=35, **kwargs):
        template = TexTemplate()
        template.body = (r"\documentclass[preview]{standalone}\usepackage[english]{babel}"
                         r"\usepackage{amsmath}\usepackage{amssymb}\usepackage{cancel}\begin{document}"
                         rf"\begin{{minipage}}{{{page_width}}}"
                         rf"\begin{{{align}}}YourTextHere\end{{{align}}}"
                         r"\end{minipage}\end{document}"
        )
        super().__init__(*args,font_size=font_size, tex_template=template, tex_environment=None, **kwargs)


class TransformByGlyphMap(AnimationGroup):
    def __init__(self, mobA, mobB, *glyph_map, replace=True, from_copy=True, show_indices=False, **kwargs):
		# replace=False does not work properly
        if from_copy:
            self.mobA = mobA.copy()
            self.replace = True
        else:
            self.mobA = mobA
            self.replace = replace
        self.mobB = mobB
        self.glyph_map = glyph_map
        self.show_indices = show_indices

        animations = []
        mentioned_from_indices = []
        mentioned_to_indices = []
        for from_indices, to_indices in self.glyph_map:
            print(from_indices, to_indices)
            if len(from_indices) == 0 and len(to_indices) == 0:
                self.show_indices = True
                continue
            elif len(to_indices) == 0:
                animations.append(FadeOut(
                    VGroup(*[self.mobA[0][i] for i in from_indices]),
                    shift = self.mobB.get_center()-self.mobA.get_center()
                ))
            elif len(from_indices) == 0:
                animations.append(FadeIn(
                    VGroup(*[self.mobB[0][j] for j in to_indices]),
                    shift = self.mobB.get_center() - self.mobA.get_center()
                ))
            else:
                animations.append(Transform(
                    VGroup(*[self.mobA[0][i].copy() if i in mentioned_from_indices else self.mobA[0][i] for i in from_indices]),
                    VGroup(*[self.mobB[0][j] for j in to_indices]),
                    replace_mobject_with_target_in_scene=self.replace
                ))
            mentioned_from_indices.extend(from_indices)
            mentioned_to_indices.extend(to_indices)

        print(mentioned_from_indices, mentioned_to_indices)
        remaining_from_indices = list(set(range(len(self.mobA[0]))) - set(mentioned_from_indices))
        remaining_from_indices.sort()
        remaining_to_indices = list(set(range(len(self.mobB[0]))) - set(mentioned_to_indices))
        remaining_to_indices.sort()
        print(remaining_from_indices, remaining_to_indices)
        if len(remaining_from_indices) == len(remaining_to_indices) and not self.show_indices:
            for from_index, to_index in zip(remaining_from_indices, remaining_to_indices):
                animations.append(Transform(
                    self.mobA[0][from_index],
                    self.mobB[0][to_index],
                    replace_mobject_with_target_in_scene=self.replace
                ))
            super().__init__(*animations, **kwargs)
        else:
            print(f"From indices: {len(remaining_from_indices)}    To indices: {len(remaining_to_indices)}")
            print("Showing indices...")
            super().__init__(
                Create(index_labels(self.mobA[0], color=PINK)),
                FadeIn(self.mobB.next_to(self.mobA, DOWN), shift=DOWN),
                Create(index_labels(self.mobB[0], color=PINK)),
                Wait(5),
                lag_ratio=0.5
                )

class Elec_Fld(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : ELECTRIC CHARGES AND FILEDS',color=GREEN,match_underline_width_to_text=True )
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.add(Outline)
        list = BulletedList('Introduction','Electric Charge','Basic properties of electric charges','Conductors and Insulators','Charging by induction','Coulombs Law',
                            'Forces between multiple charges','Superposition Principle').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        list2 = BulletedList('Electric filed','Electric Field Lines','Electric Dipole and Dipole moment','Electric Field due to an electric dipole',
                             'Dipole in a Uniform External Field','Electric Flux',"Gauss's Law","Applications of Gauss's Law").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        self.play(FadeIn(title, Outline,list,list2))
        self.next_slide(loop=True)
        self.play(FocusOn(Group(list2[0])))
        self.play(Circumscribe(Group(list2[0])))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        cur_title = Title(" Electric Field  ",match_underline_width_to_text=True, color=GREEN)
        self.play(ReplacementTransform(title,cur_title))
        self.next_slide()
        q1 = LabeledDot(Tex("$Q$",font_size=25,color=BLACK), color=RED_A)
        q2 = LabeledDot(Tex("$q$",font_size=25,color=BLACK), color=GOLD).shift(3*RIGHT)
        arrow = DoubleArrow(q1.get_center(),q2.get_center(), tip_length=0.2, color=YELLOW,buff=0).shift(0.5*DOWN)
        arrow_text=Tex('r',font_size=25).next_to(arrow,DOWN,buff=0)
        f1_arrow = Arrow(start=q2.get_right(),end=q2.get_right()+[1,0,0],buff=0,tip_length=0.2,color=GREEN_D) 
        f1_tex=Tex('$\\vec{F}$',font_size=25).next_to(f1_arrow,DOWN,buff=0)
        ques = Tex('P ?',font_size=25).move_to(q2.get_center())
        ef_intro =  LatexItems(r"\item[]   If charge q is removed, then what is left in the surrounding? Is there nothing?",
                               r"\item[]  If there is nothing at the point P, then how does a force act when we place the charge $q$ at P. ", 
                            font_size=35,itemize="itemize" ,page_width="9cm").next_to(cur_title,DOWN).to_edge(LEFT).shift(0.2*RIGHT)
        
        ef_intro2 =  LatexItems(r"\item[] In order to answer such questions, the early scientists introduced the concept of field.",
                               r"\item[] According to this, we say that the charge Q produces an electric field everywhere in the surrounding. When another charge q is brought at some point P, the field there acts on it and produces a force.",
                               r"\item[]   The term field in physics generally refers to a quantity that is defined at every point in space and may vary from point to point.",
                               r"\item[] Temperature, for example, is a scalar field, which we write as $T (x, y, z)$.",
                            font_size=35,itemize="itemize" ,page_width="13cm").next_to(ef_intro,DOWN).align_to(ef_intro,LEFT)
        
        fig_1 = VGroup(q2,f1_arrow,f1_tex,q1,arrow,arrow_text,ques).next_to(ef_intro,RIGHT).align_to(ef_intro,UP)
        
        ef_label = Tex("Electric Field: ", color=BLUE,font_size=40).next_to(cur_title,DOWN).to_corner(LEFT)
        ef_def =  LatexItems(r"\item[]  Electric field is the region of space around a charge in which its influence (force) can be experienced by other charges.",
                            font_size=35,itemize="itemize" ,page_width="13cm").next_to(ef_label,DOWN).align_to(ef_label,LEFT).shift(0.2*RIGHT)
        
        ef_int_lbl = Tex("Electric Field Intensity : ", color=BLUE,font_size=40).next_to(ef_def,DOWN).align_to(ef_label,LEFT)
        ef_int_def =  LatexItems(r"\item[]  The intensity of electric field at any point P is defined as the elctric force on a unit positive test charge placed at the point P.",
                            font_size=35,itemize="itemize" ,page_width="8cm").next_to(ef_int_lbl,DOWN).align_to(ef_int_lbl,LEFT).shift(0.2*RIGHT)
        
        q3 = LabeledDot(Tex("$+Q$",color=BLACK,font_size=25), color=RED_A)
        q4 = LabeledDot(Tex("$q_0$",color=BLACK,font_size=25), color=GOLD).shift(3*RIGHT)
        q5 = LabeledDot(Tex("$-Q$",color=BLACK,font_size=25), color=RED_A)
        line = Arrow(q3.get_right(),q4.get_left(), color=LIGHT_GREY,tip_length=0.3,buff=0)
        line_text=Tex('$\\vec{r}$',font_size=25).next_to(line,DOWN,buff=0.2)
        f_arrow = Arrow(start=q4.get_right(),end=q4.get_right()+[0.7,0,0],buff=0,tip_length=0.2,color=ORANGE) 
        f_tex=Tex('$\\vec{F}$',font_size=25).next_to(f_arrow,DR,buff=0)
        f2_arrow = Arrow(start=q4.get_left(),end=q4.get_left()-[0.7,0,0],buff=0,tip_length=0.2,color=ORANGE) 
        f2_tex=Tex('$\\vec{F}$',font_size=25).next_to(f2_arrow,DL,buff=0)
        q3_lbl = Tex('Source charge',font_size=25).next_to(q3,DOWN)
        q4_lbl = Tex('Test charge',font_size=25).next_to(q4,DOWN)
        g1 = VGroup(line,q4,line_text,q3_lbl,q4_lbl)
        fig_2= g1.copy().add(q3,f_arrow,f_tex).next_to(ef_int_lbl,RIGHT).to_edge(RIGHT).align_to(ef_int_lbl,UP)
        fig_3=g1.copy().add(q5,f2_arrow,f2_tex).next_to(fig_2,DOWN,buff=0.5).align_to(fig_2,LEFT)
        rec1 = SurroundingRectangle(VGroup(fig_2))
        rec2= SurroundingRectangle(VGroup(fig_3))
        ef_for = AlignTex(r"\vec{E}&=\displaystyle{\lim_{q_0\to 0}\dfrac{\vec{F} }{q_0 } }",r"=\displaystyle{\lim_{q_0\to 0}\dfrac{1}{4\pi\epsilon_0}\dfrac{Qq_0}{r^2 \times q_0} }\hat{r}",r"=\dfrac{1}{4\pi\epsilon_0}\dfrac{Q}{r^2 }\hat{r}",page_width="7cm", color=ORANGE).next_to(ef_int_def,DOWN).align_to(ef_int_lbl,LEFT).shift(0.6*RIGHT)
        test_chrg =  LatexItems(r"\item  A test charge $(q_0)$ is a charge of small magnitude such that it does not disturb the Source charge $(Q)$ which produces the electric filed .",
                                r"\item Though, $\vec{E} =(\vec{F}/q_0)$, but $\vec{E}$ does not depend on test charge $q_0$.",
                                page_width="13cm").next_to(ef_for,DOWN).align_to(ef_int_lbl,LEFT).shift(0.2*RIGHT)

        self.play(Write(fig_1[0:-1]))
        self.next_slide()
        self.play(Write(ef_intro[0]),FadeOut(q2,f1_arrow,f1_tex),Write(ques))
        self.next_slide()
        self.play(Write(ef_intro[1]))
        self.next_slide()
        for item in ef_intro2:
            self.play(Write(item))
            self.next_slide()

        self.play(FadeOut(ef_intro2,ef_intro,fig_1[3:8]))
        self.play(Write(ef_label))
        self.next_slide()
        self.play(Write(ef_def[0]))
        self.next_slide()
        self.play(Write(ef_int_lbl))
        self.next_slide()
        self.play(Write(ef_int_def[0]))
        self.next_slide()
        self.play(Create(rec1),Write(fig_2))
        self.next_slide()
        self.play(Create(rec2),Write(fig_3))
        self.next_slide()
        for item in ef_for:
            self.play(Write(item))
            self.next_slide()
        self.play(Write(test_chrg[0]))
        self.next_slide()
        self.play(Write(test_chrg[1]))
        self.next_slide()
        self.play(FadeOut(*self.mobjects))

class Elec_Fld2(Slide):
    def construct(self):
        ef_unit =  LatexItems(r"\item Electric Field is a vector quantity and its S.I unit : NC$^{-1}$",
                              r"\item For a positive charge, the electric field will be directed radially outwards from the charge.",
                              r"\item if the source charge is negative, the electric field vector, at each point, points radially inwards.",
                              r"\item At equal distances from the charge Q, the magnitude of its electric field $E$ is same.  The magnitude of electric field E due to a point charge is thus same on a sphere with the point charge at its centre; in other words, it has a spherical symmetry. ",
                            font_size=35,itemize="itemize" ,page_width="8.5cm").to_corner(UL)
        
        cir = Circle(1.5,color=GREY)
        q1 = LabeledDot(AlignTex("\mathbf{+}",font_size=20),radius=0.1,color=RED).move_to(cir.get_center())
        line1 = MyDashLabeledLine(AlignTex('r'),rel_pos=0.3,start=q1.get_right(),end=cir.get_right(),color=GREEN_B)
        line2 = MyDashLabeledLine(AlignTex('r'),rel_pos=0.3,start=q1.get_top(),end=cir.get_top(),color=GREEN_B)
        line3 = MyDashLabeledLine(AlignTex('r'),rel_pos=0.3,start=q1.get_bottom(),end=cir.get_bottom(),color=GREEN_B)
        line4 = MyDashLabeledLine(AlignTex('r'),rel_pos=0.3,start=q1.get_left(),end=cir.get_left(),color=GREEN_B)
        a1 = MyLabeledArrow(Tex("$\\vec{E}$",font_size=25), start=cir.get_right(),end=cir.get_right()+[0.8,0,0],color=BLUE,pos=0.3*UP)
        a2 = Arrow(cir.get_top(),cir.get_top()+[0,0.8,0],color=BLUE,buff=0)
        a3 = Arrow(cir.get_bottom(),cir.get_bottom()+[0,-0.8,0],color=BLUE,buff=0)
        a4 = Arrow(cir.get_left(),cir.get_left()+[-0.8,0,0],color=BLUE,buff=0)
        img1 = VGroup(q1,cir,line1,line2,line3,line4,a1,a2,a3,a4).scale(0.9).next_to(ef_unit,RIGHT).align_to(ef_unit,UP)
        q2 = LabeledDot(AlignTex("\mathbf{-}",font_size=20),radius=0.1,color=PINK).move_to(cir.get_center())
        a5 = MyLabeledArrow(Tex("$\\vec{E}$",font_size=25),start=cir.get_right(),end=cir.get_right()+[-0.8,0,0],color=BLUE,pos=0.3*UP)
        a6 = Arrow(cir.get_top(),cir.get_top()+[0,-0.8,0],color=BLUE,buff=0)
        a7 = Arrow(cir.get_bottom(),cir.get_bottom()+[0,+0.8,0],color=BLUE,buff=0)
        a8 = Arrow(cir.get_left(),cir.get_left()+[0.8,0,0],color=BLUE,buff=0)
        img2= VGroup(q2,cir.copy(),line1.copy(),line2.copy(),line3.copy(),line4.copy(),a5,a6,a7,a8).next_to(img1,DOWN)
        
        self.play(Write(ef_unit[0]))
        self.next_slide()
        self.play(Write(ef_unit[1]))
        self.next_slide()
        self.play(Write(img1))
        self.next_slide()
        self.play(Write(ef_unit[2]))
        self.next_slide()
        self.play(Write(img2))
        self.next_slide()
        self.play(Write(ef_unit[3]))
        self.next_slide()
        self.play(FadeOut(*self.mobjects))

        ef_sys_label = Tex("Electric Field due to a system of charge:", color=BLUE,font_size=40).to_corner(UL,buff=0.2)
        ef_sys =  Tex(r"Suppose we have to find the electric field $\vec{E}$ at point P due to point charges $q_1,\ q_2,...,\ q_n$,", r"with position vectors $r_1, r_2, ..., r_n$",
                            font_size=35,tex_environment="{minipage}{7cm}",).next_to(ef_sys_label,DOWN).align_to(ef_sys_label,LEFT)
        
        ef_sys1 =  LatexItems(r"\item[] Electric filed $\vec{E}_{P1}$ at $P$ due to $q_1$:",
                              r"\item[] $\vec{E}_{P1} = \dfrac{1}{4\pi\epsilon_0} \dfrac{q_1}{|\vec{r}_{P1}|^2}\ \hat{r}_{P1} $",
                              r"\item[] Electric filed $\vec{E}_{P2}$ at $P$ due to $q_2$:",
                              r"\item[] $\vec{E}_{P2} = \dfrac{1}{4\pi\epsilon_0} \dfrac{q_2}{|\vec{r}_{P2}|^2}\ \hat{r}_{P2} $",
                              r"\item[] Electric filed $\vec{E}_{Pn}$ at $P$ due to $q_n$:",
                              r"\item[] $\vec{E}_{Pn} = \dfrac{1}{4\pi\epsilon_0} \dfrac{q_n}{|\vec{r}_{Pn}|^2}\ \hat{r}_{Pn} $",
                            font_size=35,itemize="itemize" ,page_width="6cm").next_to(ef_sys,DOWN).align_to(ef_sys,LEFT)
        
        ax = Axes(x_range=[0,6],y_range=[0, 6],x_length=10,y_length=8)
        q1 = Dot(ax.coords_to_point(0.5,5),color=YELLOW).scale(2.5)
        q2 = Dot(ax.coords_to_point(1.5,3),color=YELLOW).scale(2.5)
        q3 = Dot(ax.coords_to_point(5,2),color=YELLOW).scale(2.5)
        P =LabeledDot(Tex('P',font_size=50,color=BLACK),color=GOLD).move_to(ax.coords_to_point(5,5))
        q1_text=Tex('$q_1$').next_to(q1,DR,buff=0.2).scale(1.5)
        q2_text=Tex('$q_2$').next_to(q2,UP,buff=0.2).scale(1.5)
        q3_text=Tex('$q_n$').next_to(q3,RIGHT,buff=0.2).scale(1.5)
        vector_1 = MyLabeledArrow( MathTex('\\vec{r}_1',font_size=60),start=ax.coords_to_point(0,0),end=ax.coords_to_point(0.5,5),color=BLUE)
        vector_2 = MyLabeledArrow( MathTex('\\vec{r}_2',font_size=60),start=ax.coords_to_point(0,0),end=ax.coords_to_point(1.5,3),color=BLUE)
        vector_3 = MyLabeledArrow( MathTex('\\vec{r}_n',font_size=60),start=ax.coords_to_point(0,0),end=ax.coords_to_point(5,2),color=BLUE)
        vector_4 = MyLabeledArrow( MathTex('\\vec{r}_P',font_size=60),start=ax.coords_to_point(0,0),end=ax.coords_to_point(5,5),color=BLUE)
        vector_P1 =  MyLabeledArrow( MathTex('\\vec{r}_{P1}',font_size=60),start=ax.coords_to_point(0.5,5),end=ax.coords_to_point(5,5),color=RED)
        vector_P2 =  MyLabeledArrow( MathTex('\\vec{r}_{P2}',font_size=60),start=ax.coords_to_point(1.5,3),end=ax.coords_to_point(5,5),color=RED) 
        vector_Pn =  MyLabeledArrow( MathTex('\\vec{r}_{Pn}',font_size=60),start=ax.coords_to_point(5,2),end=ax.coords_to_point(5,5),color=RED)
        EP1_arrow =  MyLabeledArrow( MathTex('\\vec{E}_{P1}',font_size=50),start=P.get_center(),end=P.get_center()+2*vector_P1.get_unit_vector(),pos=0.7*DOWN,color=PINK)
        EP2_arrow = MyLabeledArrow( MathTex('\\vec{E}_{P2}',font_size=50),start=P.get_center(),end=P.get_center()+3*vector_P2.get_unit_vector(),color=YELLOW)
        EPn_arrow = MyLabeledArrow( MathTex('\\vec{E}_{Pn}',font_size=50),start=P.get_center(),end=P.get_center()+3*vector_Pn.get_unit_vector(),pos=0.7*LEFT,color=GRAY_B)
        EP2_line = DashedLine(start=EP1_arrow.get_end(),end=EP1_arrow.get_end()+3*vector_P2.get_unit_vector(),color=YELLOW)
        EPn_line = DashedLine(start=EP2_line.get_end(),end=EP2_line.get_end()+3*vector_Pn.get_unit_vector(),color=GREY_B)
        EP_arrow = MyLabeledArrow( MathTex('\\vec{E}_{P}',font_size=50),start=EP1_arrow.get_start(),end=EPn_line.get_end(),pos=0.7*UP,color=GOLD)

        g1= VGroup(ax,q1,q2,q3,P,q1_text,q2_text,q3_text,vector_1,vector_2,vector_4,vector_P1,EP1_arrow,EP2_arrow,EPn_arrow,vector_3,vector_P2,vector_Pn,EP2_line,EPn_line,EP_arrow).scale(0.45).next_to(ef_sys_label,RIGHT).to_edge(RIGHT).align_to(ef_sys_label,UP)
        ef_sys_2 = LatexItems(r"\item[] By the superposition principle, the electric field $\vec{E}_P$ at P:",
                            font_size=35,itemize="itemize" ,page_width="8.5 cm").next_to(g1,DOWN,buff=0.1).align_to(ef_sys1.get_right(),LEFT).shift(0.25*RIGHT)
        ef_sum = AlignTex(r"\vec{E}_P &=\vec{E}_{P1}+\vec{E}_{P2}",r"+\vec{E}_{Pn}\\",r"\vec{E}_P &=\dfrac{1}{4\pi\epsilon_0}\left[\dfrac{q_1}{|\vec{r}_{P1}|^2}\hat{r}_{P1}+\dfrac{q_2}{|\vec{r}_{P2}|^2}\hat{r}_{P2}+ ... +\dfrac{q_n}{|\vec{r}_{Pn}|^2}\hat{r}_{Pn}\right]",page_width="8.5cm").next_to(ef_sys_2,DOWN).align_to(ef_sys_2,LEFT)
        line = Line([0,ef_sys_2.get_y(UP),0],[0,config.bottom[1],0],color=RED).next_to(ef_sys1,RIGHT,buff=0.1).align_to(ef_sys_2,UP)
        self.play(Write(ef_sys_label))
        self.next_slide()
        self.play(Write(ef_sys[0]))
        self.play(Write(VGroup(q1,q2,q3,q1_text,q2_text,q3_text,P)))
        self.next_slide()
        self.play(Write(ef_sys[1]))
        self.play(Write(VGroup(vector_1,vector_2,vector_3,vector_4,ax)))
        self.next_slide()
        self.play(Write(VGroup(vector_P1,vector_P2,vector_Pn)))
        self.next_slide()
        self.play(Write(ef_sys1[0]))
        self.play(Write(EP1_arrow))
        self.next_slide()
        self.play(Write(ef_sys1[1]))
        self.next_slide()
        self.play(Write(ef_sys1[2]))
        self.play(Write(EP2_arrow))
        self.next_slide()
        self.play(Write(ef_sys1[3]))
        self.next_slide()
        self.play(Write(ef_sys1[4]))
        self.play(Write(EPn_arrow))
        self.next_slide()
        self.play(Write(ef_sys1[5]))
        self.next_slide()
        self.play(Write(line))
        self.play(Write(ef_sys_2[0]))
        self.next_slide()
        self.play(Write(ef_sum[0]))
        self.play(ReplacementTransform(EP2_arrow.copy(),EP2_line))
        self.next_slide()
        self.play(Write(ef_sum[1]))
        self.play(ReplacementTransform(EPn_arrow.copy(),EPn_line))
        self.next_slide()
        self.play(Write(ef_sum[2]))
        self.play(ReplacementTransform(VGroup(EP1_arrow,EP2_line,EPn_line).copy(),EP_arrow))


class Ex33(Slide):
    def construct(self):

        ex_title = Tex("{{Example 25 :}}  A negatively charged oil drop is suspended in uniform field of $3\\times 10^4$ N/C, so that it neither falls not rises. The charge on the drop will be: (given the mass of the oil drop $m= 9.9\\times 10^{-15}$ kg and $g=10\ \\text{ms}^{-2} $)",substrings_to_isolate=":",tex_environment="{minipage}{10cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        pline = MyLabeledLine(Tex(r"$\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +$",font_size=20),pos=0.1*UP,start=LEFT,end=2*RIGHT,color=RED)
        nline = MyLabeledLine(Tex(r"$\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -$",font_size=20),pos=0.1*DOWN,start=LEFT,end=2*RIGHT,color=BLUE).shift(3*DOWN)
        oil = LabeledDot(Tex("-q",font_size=20),color=PINK).move_to(pline.get_center()).shift(1.5*DOWN)
        E = MyLabeledArrow(Tex(r"$\vec{E}$",font_size=20),start= 0.5*UP,end=0.5*DOWN,pos=0.2*RIGHT).next_to(oil,RIGHT).shift(0.5*RIGHT)
        FE = MyLabeledArrow(Tex(r"$\vec{F}_e=-q\vec{E}$",font_size=20),start= oil.get_top(),end=oil.get_top()+1*UP,color=BLUE,rot=False,opacity=0.3)
        Fg = MyLabeledArrow(Tex(r"$\vec{F}_g=mg$",font_size=20),start= oil.get_bottom(),end=oil.get_bottom()+1*DOWN,color=GREEN,rot=False,opacity=0.3)
        img = VGroup(pline,nline,oil,E,FE,Fg).next_to(ex_title,RIGHT).align_to(ex_title,UP)
        img_rect= SurroundingRectangle(img)
        self.play(Write(ex_title))
        self.play(Write(img[0:4]),Create(img_rect))
        self.next_slide()
        sol_label =Tex('Solution :',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 
        sol_1 =  LatexItems(r"\item[] Given: $E = 3\times 10^4$ N/C,\\ $m= 9.9\times 10^{-15}$ kg, and $g=10\ \text{ms}^{-2} $",
                            r"\item[] Find: Charge on the oil drop $q = ?$",
                            r"\item[] There are two force acting on the oil drop:",
                            r"\item[] Force due to elctric field in upward direction:",
                            r"\item[] $|\vec{F}_e| = qE$",
                            r"\item[] Gravitational force in downward direction:",
                            r"\item[] $|\vec{F}_g| = mg$",
                            font_size=35,itemize="itemize" ,page_width="7.8cm").next_to(sol_label,DOWN).align_to(sol_label,LEFT)
        line = Line([0,sol_label.get_y(UP),0],[0,config.bottom[1],0],color=RED).next_to(sol_1,RIGHT).align_to(sol_label,UP)
        sol_2 = LatexItems(r"\item[] Since, the oil drop is neither falling or rising :",
                            font_size=35,itemize="itemize" ,page_width="7cm").next_to(line,RIGHT).align_to([0,img_rect.get_y(DOWN),0],UP).shift(0.1*DOWN)
        sol_3=  AlignTex(
                         r" \therefore\ |\vec{F}_e|&=|\vec{F}_g|\\",
                         r"qE &=mg\\",
                         r"q &=\dfrac{mg}{E}", r"=\dfrac{\cancel{9.9}\times 10^{-15} \times 10}{\cancel{3}\times 10^4}\\",
                         r" &=3.3\times 10^{-14}\times 10^{-4}\\",
                         r"q &=3.3\times 10^{-18}\ \text{C}\\"
                         ,page_width="7cm").next_to(sol_2,DOWN).align_to(sol_2,LEFT)
        self.next_slide()
        for item in sol_1[0:3]:
            self.play(Write(item))
            self.next_slide()
        self.play(Write(sol_1[3]),Write(FE))
        self.next_slide()
        self.play(Write(sol_1[4]))
        self.next_slide()
        self.play(Write(sol_1[5]),Write(Fg))
        self.next_slide()
        self.play(Write(sol_1[6]))
        self.play(Write(line))
        self.play(Write(sol_2))
        self.next_slide()
        for item in sol_3:
            self.play(Write(item))
            self.next_slide()
        self.play(Create(SurroundingRectangle(sol_3[-1])))
        self.wait()


class Ex34(Slide):
    def construct(self):

        ex_title = Tex("{{Example 26 :}}  How many electrons should be removed from a coin of mass 1.6 g, so that it may float in an electric field of intensity $10^9$ N/C directed upward? (take g = 9.8 ms$^2$)",substrings_to_isolate=":",tex_environment="{minipage}{10cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        op = VGroup(Tex('(a) $9.8\\times  10^7$',font_size=35), Tex('(b) $9.8\\times  10^5$',font_size=35),Tex('(c) $9.8\\times  10^3$',font_size=35),Tex('(d) $9.8\\times  10^1$',font_size=35) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)
        pline = MyLabeledLine(Tex(r"$\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +$",font_size=20),pos=0.1*UP,start=LEFT,end=2*RIGHT,color=RED).shift(3*DOWN)
        nline = MyLabeledLine(Tex(r"$\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -$",font_size=20),pos=0.1*DOWN,start=LEFT,end=2*RIGHT,color=BLUE)
        oil = LabeledDot(Tex("q=ne",font_size=20),color=PINK).move_to(nline.get_center()).shift(1.5*DOWN)
        E = MyLabeledArrow(Tex(r"$\vec{E}$",font_size=20),start= 0.5*DOWN,end=0.5*UP,pos=0.2*RIGHT).next_to(oil,RIGHT).shift(0.5*RIGHT)
        FE = MyLabeledArrow(Tex(r"$\vec{F}_e=q\vec{E}$",font_size=20),start= oil.get_top(),end=oil.get_top()+1*UP,color=BLUE,rot=False,opacity=0.3)
        Fg = MyLabeledArrow(Tex(r"$\vec{F}_g=mg$",font_size=20),start= oil.get_bottom(),end=oil.get_bottom()+1*DOWN,color=GREEN,rot=False,opacity=0.3)
        img = VGroup(pline,nline,oil,E,FE,Fg).next_to(ex_title,RIGHT).align_to(ex_title,UP)
        img_rect= SurroundingRectangle(img)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(op))
        self.play(Write(img),Create(img_rect))
        self.next_slide()
        sol_label =Tex('Solution :',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 
        sol_1 =  LatexItems(r"\item[] Given: $E =10^9$ N/C,\\ $m= 1.6\ \text{g}=1.6\times 10^{-3}$ kg, and $g=9.8\ \text{ms}^{-2} $",
                            r"\item[] Number of electron removed $n = ?$",
                            r"\item[] There are two force acting on the oil drop:",
                            r"\item[] Since, the oil drop is neither falling or rising :",
                            r" \item[] $\therefore\ |\vec{F}_e|=|\vec{F}_g|$",
                            font_size=35,itemize="itemize" ,page_width="7.8cm").next_to(sol_label,DOWN).align_to(sol_label,LEFT)
        line = Line([0,sol_label.get_y(UP),0],[0,config.bottom[1],0],color=RED).next_to(sol_1,RIGHT).align_to(sol_label,UP)
        sol_3=  AlignTex(r"neE &=mg\\",
                         r"n&=\dfrac{mg}{eE}", r"=\dfrac{\cancel{1.6}\times 10^{-3} \times 9.8}{\cancel{1.6}\times 10^{-19}\times 10^{9}}\\",
                         r" &=9.8\times 10^{-3}\times 10^{10}\\",
                         r"n &=9.8\times 10^{7}"
                         ,page_width="7cm").next_to(line,RIGHT).align_to([0,img_rect.get_y(DOWN),0],UP).shift(0.1*DOWN)
        self.next_slide()
        for item in sol_1:
            self.play(Write(item))
            self.next_slide()
        self.play(Write(line))  
        for item in sol_3:
            self.play(Write(item))
            self.next_slide()
        self.play(Create(SurroundingRectangle(sol_3[-1])))
        self.next_slide(loop=True)
        self.play(Wiggle(op[0]))
        self.wait()


class Ex35(Slide):
    def construct(self):

        ex_title = Tex("{{Example 27 :}}  The distance between the two charges 25 $\mu$ C and 36 $\mu$ C is 11 cm. At what point on the line joining the two charges the intensity will be zero at a distance of",substrings_to_isolate=":",tex_environment="{minipage}{9.2cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        op = VGroup(Tex('(a) 4 cm from 36 $\mu$ C',font_size=35), Tex('(b) 4 cm from 25 $\mu$ C',font_size=35),Tex('(c) 5 cm from 36 $\mu$ C',font_size=35),Tex('(d) 5 cm from 25 $\mu$ C',font_size=35) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        q1 = LabeledDot(Tex("$q_1$",font_size=25),color=PINK)
        q2 = LabeledDot(Tex("$q_2$",font_size=25),color=RED).shift(3*RIGHT)
        line = MyLabeledLine(Tex("11 cm",font_size=25),start= q1.get_right(),end=q2.get_left(),pos=0.3*UP,color=BLUE)
        P = Dot(1.3*RIGHT)
        P_lab =Tex("P",font_size=30).next_to(P,DOWN)
        P1 = MyDoubLabArrow(Tex("x",font_size=30),start=q1.get_right(),end=P.get_left(), tip_length=0.1).shift(0.5*DOWN)
        P2 = MyDoubLabArrow(Tex("11-x",font_size=30),start=P.get_right(),end=q2.get_left(), tip_length=0.1).shift(0.5*DOWN)
        img = VGroup(q1,q2,line,P,P_lab,P1,P2).next_to(ex_title,RIGHT)
        img_rect= SurroundingRectangle(img)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(op))
        self.play(Write(img),Create(img_rect))
        self.next_slide()
        sol_label =Tex('Solution :',font_size=35, color=ORANGE).next_to(op,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 
        sol_1 =  LatexItems(r"\item[] Given: $q_1=25\ \mu$ C, $q_2=36\ \mu$ C, and $r = 11$ cm",
                            r"\item[] Let the distance of point P (from q1=25 $\mu$C) where the intensity will zero  be $r_{P1}=x$ cm",
                            r"\item[] So, the distance of point P from $q_2$, \\$r_{P2}=11-x$ cm"
                            r"\item[] Since elctric filed intensity is zero at P",
                            r"\item[] $\therefore |\vec{E}_{P1}| =|\vec{E}_{P2}|$",
                            font_size=35,itemize="itemize" ,page_width="8.5cm").next_to(sol_label,DOWN).align_to(sol_label,LEFT)
        line = Line([0,sol_label.get_y(UP),0],[0,config.bottom[1],0],color=RED).next_to(sol_1,RIGHT).align_to(sol_label,UP)
        sol_3=  AlignTex(r" \cancel{\dfrac{1}{4\pi\epsilon_0}} \dfrac{q_1}{r_{P1}^2} &=\cancel{\dfrac{1}{4\pi\epsilon_0}} \dfrac{q_2}{r_{P2}^2}  \\",
                         r"\dfrac{25\ \cancel{\mu C}}{x^2\ \cancel{cm^2}}&=\dfrac{36\ \cancel{\mu C}}{(11-x)^2\ \cancel{cm^2}} \\",
                         r"\dfrac{5}{x}&=\dfrac{6}{11-x}  \\",
                         r"55-5x&=6x  \\",
                          r"55&=6x+5x  \\",
                         r"x&=5 \\",
                         page_width="7cm").next_to(line,RIGHT).shift(0.1*DOWN)
        self.next_slide()
        for item in sol_1:
            self.play(Write(item))
            self.next_slide()
        self.play(Write(line))  
        for item in sol_3:
            self.play(Write(item))
            self.next_slide()
        self.play(Create(SurroundingRectangle(sol_3[-1])))
        self.next_slide(loop=True)
        self.play(Wiggle(op[3]))
        self.wait()


class Ex36(Slide):
    def construct(self):

        ex_title = Tex(r"Example 1.8 :", r"An electron falls through a distance of 1.5 cm in a uniform electric field of magnitude $2.0 \times 10^4\ \text{NC}^{-1}$ [Fig. 1.13(a)].", r" The direction of the field is reversed keeping its magnitude unchanged and a proton falls through the same distance [Fig. 1.13(b)]. Compute the time of fall in each case. Contrast the situation with that of 'free fall under gravity'.",tex_environment="{minipage}{10cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        pline = MyLabeledLine(Tex(r"$\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +$",font_size=20),pos=0.1*UP,start=LEFT,end=2*RIGHT,color=RED).shift(3*DOWN)
        nline = MyLabeledLine(Tex(r"$\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -$",font_size=20),pos=0.1*DOWN,start=LEFT,end=2*RIGHT,color=BLUE)
        darrow = MyDoubLabArrow(Tex("d",font_size=30),start=nline.get_left(),end=pline.get_left(),opacity=1,rot=False,tip_length=0.1)
        oil = LabeledDot(Tex("-e",font_size=20),color=PINK).move_to(nline.get_center()).shift(1.5*DOWN)
        oil2 = LabeledDot(Tex("e",font_size=20),color=PINK).move_to(nline.get_center()).shift(1.5*DOWN)
        fig1_lbl = Tex("Fig 1.13(a) ",font_size=30,color=GOLD).next_to(pline,DOWN,buff=0.2)
        fig2_lbl = Tex("Fig 1.13(b) ",font_size=30,color=GOLD).next_to(pline,DOWN,buff=0.3)
        E = MyLabeledArrow(Tex(r"$\vec{E}$",font_size=20),start= 0.5*DOWN,end=0.5*UP,pos=0.2*RIGHT).next_to(oil,RIGHT,buff=0.7)
        FE = MyLabeledArrow(Tex(r"$\vec{F}_e=-e\vec{E}$",font_size=20),start= oil.get_bottom(),end=oil.get_bottom()+1*DOWN,color=BLUE,rot=False,opacity=0.3)
        FE2 = MyLabeledArrow(Tex(r"$\vec{F}_e=eE$",font_size=20),start= oil.get_bottom(),end=oil.get_bottom()+1*DOWN,color=GREEN,rot=False,opacity=0.3)
        img2 =VGroup(pline.copy().shift(3*UP),nline.copy().shift(3*DOWN),oil2,E.copy().rotate(PI),FE2,darrow.copy(),fig2_lbl)
        img = VGroup(pline,nline,oil,E,FE,darrow,fig1_lbl).next_to(ex_title,RIGHT).align_to(ex_title,UP)
        img2.next_to(img,DOWN,buff=0.2)
        img_rect2 = SurroundingRectangle(img2[0:-1])
        img_rect = SurroundingRectangle(img[0:-1])
        self.play(Write(ex_title[0:2]))
        self.play(Write(img),Create(img_rect))
        self.next_slide()
        self.play(Write(ex_title[2]))
        self.play(Write(img2),Create(img_rect2))
        self.next_slide()
        sol_label =Tex('Solution :',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 
        sol_1 =  LatexItems(r"\item[] Given: $E =2\times 10^4$ N/C,\\ $d= 1.5\ \text{cm}=1.5\times 10^{-2}$ m",
                            r"\item[] Find: Time of fall of elctron $(t_e)$ and proton $(t_p)$ ",
                            r"\item[] Force on electron $F_e=e\times E$",
                            r"\item[] $m_ea_e=eE \quad (\because F=ma)$",
                            font_size=35,itemize="itemize" ,page_width="5.1cm").next_to(sol_label,DOWN).align_to(sol_label,LEFT)
        line = Line([0,sol_label.get_y(UP),0],[0,config.bottom[1],0],color=RED).next_to(sol_1,RIGHT).align_to(sol_label,UP)
        sol_3=  AlignTex(r"a_e &=\dfrac{eE}{m_e}=\dfrac{1.6\times 10^{-19}\times 2\times 10^4}{9.11\times 10^{-31}}\\",
                         r"a_e &=3.51\times 10^{15}\ \text{ms}^{-2}\\",
                         r"S &= ut+\dfrac{1}{2}at^2 \text{(2nd eq. of motion)}\\",
                         r"d&=0\times t + \dfrac{1}{2}a_et_e^2\\",
                         r"t_e &=\sqrt{\dfrac{2d}{a_e}}",r"=\sqrt{\dfrac{2\times 1.5\times 10^{-2}}{3.51\times 10^{15}}}\\",
                         r"t_e &=2.96\times10^{-9}\ s\\",
                         page_width="7cm").next_to(line,RIGHT).shift(0.1*UP)
        self.next_slide()
        for item in sol_1:
            self.play(Write(item))
            self.next_slide()
        self.play(Write(line))  
        for item in sol_3:
            self.play(Write(item))
            self.next_slide()
        self.play(Create(SurroundingRectangle(sol_3[-1])))
        self.wait()

class Ex37(Slide):
    def construct(self):

        ex_title = Tex(r"Example 1.8 :", r"Two point charges $q_1$ and $q_2$, of magnitude $+10^{-8}$ C and $-10^{-8}$ C, respectively, are placed 0.1 m apart.", r"Calculate the electric fields at points A", r", B ", r"and C shown in Fig. 1.14.",tex_environment="{minipage}{7.2cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        q1 = MyLabeledDot(label_in=Tex(r"$\mathbf{+}$",font_size=35,color=PINK),label_out= Tex("$q_1$",font_size=35),color=DARK_BROWN)
        q2 = MyLabeledDot(label_in=Tex(r"$\mathbf{-}$",font_size=35,color=BLUE),label_out= Tex("$q_2$",font_size=35),color=MAROON).shift(4*RIGHT)
        A = MyLabeledDot(label_out= Tex("$A$",font_size=35),color=BLUE,point=2*RIGHT)
        B = MyLabeledDot(label_out= Tex("$B$",font_size=35),color=GREEN,point=2*LEFT)
        C = MyLabeledDot(label_out= Tex("$C$",font_size=35),color=BLUE,pos=LEFT,point=2*RIGHT+3.464*UP)
        A1 = MyDoubLabArrow(label=Tex("0.05 m",font_size=35),start=q1[0].get_right(),end=A[0].get_left(),pos=0.2*DOWN,tip_length=0.1)
        A2 = MyDoubLabArrow(label=Tex("0.05 m",font_size=35),start=A[0].get_right(),end=q2[0].get_left(),pos=0.2*DOWN,tip_length=0.1)
        B1 = MyDoubLabArrow(label=Tex("0.05 m",font_size=35),start=B[0].get_right(),end=q1[0].get_left(),pos=0.2*DOWN,tip_length=0.1)
        C1 = MyDashLabeledLine(label=Tex("0.1 m",font_size=35),start=q1[0].get_top(),end=C[0].get_bottom(),pos=0.2*LEFT)
        C2 = MyDashLabeledLine(label=Tex("0.1 m",font_size=35),start=q2[0].get_top(),end=C[0].get_bottom(),pos=0.2*RIGHT)
        EA1 = MyLabeledArrow(label=Tex("$E_{A1}$",font_size=35),start=A[0].get_right(),end=A[0].get_right()+RIGHT,pos=0.2*UP,tip_length=0.2,color=RED).shift(0.5*UP)
        EA2 = MyLabeledArrow(label=Tex("$E_{A2}$",font_size=35),start=A[0].get_right(),end=A[0].get_right()+RIGHT,pos=0.2*UP,tip_length=0.2,color=GOLD).shift(1.2*UP)
        EA = MyLabeledArrow(label=Tex("$E_{A}$",font_size=35),start=A[0].get_right(),end=A[0].get_right()+2*RIGHT,pos=0.2*UP,tip_length=0.2,color=ORANGE).shift(0.3*UP)

        EB1 = MyLabeledArrow(label=Tex("$E_{B1}$",font_size=35),start=B[0].get_left()+RIGHT,end=B[0].get_left(),pos=0.2*UP,tip_length=0.2,color=RED).shift(0.3*UP)
        EB2 = MyLabeledArrow(label=Tex("$E_{B2}$",font_size=35),start=B[0].get_right()+RIGHT,end=B[0].get_right()+10*RIGHT/9,pos=0.2*UP,tip_length=0.2,max_stroke_width_to_length_ratio=45,max_tip_length_to_length_ratio=2.25,color=GOLD).shift(0.3*UP)
        EB = MyLabeledArrow(label=Tex("$E_{B}$",font_size=35),start=B[0].get_left()+0.89*RIGHT,end=B[0].get_left(),pos=0.2*UP,tip_length=0.2,color=ORANGE).shift(0.3*UP)
        img = VGroup(q1,q2,A,B,C,A1,A2,B1,C1,C2,EA1,EA2,EA,EB1,EB2,EB).next_to(ex_title,RIGHT,buff=0.2).align_to(ex_title,UP)
        self.play(Write(ex_title[0:2]))
        self.play(Write(VGroup(q1,q2,A[0],A1,A2)))
        self.next_slide()
        self.play(Write(ex_title[2]))
        self.play(Write(VGroup(A[1])))
        self.next_slide()
        self.play(Write(ex_title[3]))
        self.play(Write(VGroup(B,B1)))
        self.next_slide()
        self.play(Write(ex_title[4]))
        self.play(Write(VGroup(C,C1,C2)))
        self.next_slide()
        sol_label =Tex('Solution :',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 
        sol_1 =  LatexItems(r"\item[] Given: $q_1 = +10^{-8}$ C and $q_2 = -10^{-8}$ C",
                            r"\item[] Find: Electric field at Point A, B and C",
                            font_size=35,itemize="itemize" ,page_width="7.5cm").next_to(sol_label,DOWN).align_to(sol_label,LEFT)
        self.next_slide()
        for item in sol_1:
            self.play(Write(item))
            self.next_slide()
        self.play(FadeOut(ex_title),VGroup(sol_label,sol_1).animate.to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2))
        sol_2 =  LatexItems(r"\item[(i)] Magnitude of Electric field at A due to $q_1$",
                            r"\item[] $E_{A1} = \dfrac{1}{4\pi\epsilon_0}\dfrac{q_1}{r_{A1}^2}=\dfrac{9\times 10^9\times10^{-8}}{(5\times10^{-2})^2}$",
                            r"\item[] $E_{A1} = \dfrac{9\times 10^1}{25\times 10^{-4}}=3.6\times 10^4$ N/C\\ (Directed toward Right)",
                            r"\item[] Similarly, magnitude of Electric field at A due to $q_2$",
                            r"\item[] $E_{A2}= \dfrac{1}{4\pi\epsilon_0}\dfrac{q_1}{r_{A2}^2}=E_{A1}=3.6\times 10^4$ N/C\\ (Directed toward Right)",
                            font_size=35,itemize="itemize" ,page_width="7.5cm").next_to(sol_1,DOWN).align_to(sol_1,LEFT)
        line = Line([0,sol_label.get_y(UP),0],[0,config.bottom[1],0],color=RED).next_to(sol_2,RIGHT).align_to(sol_1,UP)
        sol_3=  LatexItems(r"\item[] Magnitude of total electric field at A",
                         r"\item[] $E_A = E_{A1}+E_{A2}=7.2\times 10^{4}$ N/C \\ (Directed toward Right)",
                         font_size=35,itemize="itemize" ,page_width="6.5cm").next_to(img,DOWN).align_to(img,LEFT).shift(0.2*RIGHT)
        
        self.play(FadeOut(VGroup(B,B1,C,C1,C2)))
        self.next_slide(loop=True)
        self.play(Flash(A))
        self.next_slide()
        self.play(Write(sol_2[0]))
        self.play(Write(EA1))
        self.next_slide()
        self.play(Write(sol_2[1]))
        self.next_slide()
        self.play(Write(sol_2[2]))
        self.next_slide()
        self.play(Write(sol_2[3]))
        self.play(Write(EA2))
        self.next_slide()
        self.play(Write(sol_2[4]))
        self.play(Write(line))  
        self.next_slide()
        self.play(Write(sol_3[0]))
        self.next_slide()
        self.play(ReplacementTransform(VGroup(EA1,EA2),EA))
        self.play(Write(sol_3[1]))
        self.next_slide(loop=True)
        self.play(Wiggle(sol_3[-1]))
        self.wait()
        self.next_slide()
        self.play(FadeOut(sol_2,sol_3,EA,line))
        self.play(FadeIn(B,B1))
        self.next_slide(loop=True)
        self.play(Flash(B))

        sol_4 =  LatexItems(r"\item[(ii)] Magnitude of Electric field at B due to $q_1$",
                            r"\item[] $E_{B1} = \dfrac{1}{4\pi\epsilon_0}\dfrac{q_1}{r_{B1}^2}=\dfrac{9\times 10^9\times10^{-8}}{(5\times10^{-2})^2}$",
                            r"\item[] $E_{B1} = \dfrac{9\times 10^1}{25\times 10^{-4}}=3.6\times 10^4$ N/C\\ (Directed toward Left)",
                            r"\item[] Similarly, magnitude of Electric field at B due to $q_2$",
                            r"\item[] $E_{B2}= \dfrac{1}{4\pi\epsilon_0}\dfrac{q_1}{r_{B2}^2}=\dfrac{9\times 10^9\times10^{-8}}{(15\times10^{-2})^2}$",
                            font_size=35,itemize="itemize" ,page_width="7.3cm").next_to(sol_1,DOWN).align_to(sol_1,LEFT)
        line = Line([0,sol_label.get_y(UP),0],[0,config.bottom[1],0],color=RED).next_to(sol_4,RIGHT).align_to(sol_1,UP)
        sol_5=  LatexItems(r"\item[] $E_{B2} = \dfrac{9\times 10^1}{225\times 10^{-4}}=0.4\times 10^4$ N/C\\ (Directed toward Right)",
                           r"\item[] Magnitude of total electric field at B",
                         r"\item[] $E_B = E_{B1}-E_{B2}=3.2\times 10^{4}$ N/C \\ (Directed toward Left)",
                         font_size=35,itemize="itemize" ,page_width="6.5cm").next_to(img,DOWN).align_to(img,LEFT).shift(0.2*RIGHT)
        
        self.next_slide()
        self.play(Write(sol_4[0]))
        self.play(Write(EB1))
        self.next_slide()
        self.play(Write(sol_4[1]))
        self.next_slide()
        self.play(Write(sol_4[2]))
        self.next_slide()
        self.play(Write(sol_4[3]))
        self.play(Write(EB2))
        self.next_slide()
        self.play(Write(sol_4[4]))
        self.play(Write(line))  
        self.next_slide()
        self.play(Write(sol_5[0]))
        self.next_slide()
        self.play(Write(sol_5[1]))
        self.next_slide()
        self.play(ReplacementTransform(VGroup(EB1,EB2),EB))
        self.play(Write(sol_5[2]))
        self.next_slide(loop=True)
        self.play(Wiggle(sol_5[-1]))
        self.wait()
        self.next_slide()
        self.play(FadeOut(sol_1,sol_4,sol_5,EB,line,B,B1))

        EC1 = MyLabeledArrow(label=Tex("$E_{C1}$",font_size=35),start=C[0].get_top(),end=C[0].get_top()+1*C1[0].get_unit_vector(),pos=0.2*LEFT,tip_length=0.2,color=RED)
        EC2 = MyLabeledArrow(label=Tex("$E_{C2}$",font_size=35),start=C[0].get_bottom(),end=C[0].get_bottom()-1*C2[0].get_unit_vector(),pos=0.2*LEFT,tip_length=0.2,color=GOLD)
        EC = MyLabeledArrow(label=Tex("$E_{C}$",font_size=35),start=C[0].get_right(),end=C[0].get_right()+1*RIGHT,pos=0.2*UP,tip_length=0.2,color=ORANGE)
        img.add(EC1,EC2,EC).next_to(sol_1,RIGHT).align_to(sol_1,UP).shift(RIGHT)

        self.play(Write(VGroup(C,C1,C2)))
        self.next_slide(loop=True)
        self.play(Flash(C))

        sol_6 =  LatexItems(r"\item[(iii)] Magnitude of Electric field at C due to $q_1$",
                            r"\item[] $E_{C1} = \dfrac{1}{4\pi\epsilon_0}\dfrac{q_1}{r_{C1}^2}=\dfrac{9\times 10^9\times10^{-8}}{(10^{-1})^2}= \dfrac{9\times 10^1}{10^{-2}}$",
                            r"\item[] $E_{C1} =E =9\times 10^3$ N/C (Direction indicated in fig.)",
                            r"\item[] Magnitude of Electric field at C due to $q_2$",
                            r"\item[] $E_{C2}= E=9\times 10^3$ N/C (Direction indicated in fig.)",
                            r"\item[] Magnitude of total electric field at C",
                            r"\item[] $E_C=\sqrt{E_{C1}^2+E_{C2}^2+2E_{C1}E_{C2}\cos(120^\circ)}$",
                            r"\item[] $E_C =\sqrt{E^2+E^2-2E^2\times\dfrac{1}{2}}=\sqrt{2E^2-E^2}=\sqrt{E^2}=E$",
                            r"\item[] $E_C=9\times 10^{3}$ N/C (Directed towards Right)",
                            font_size=35,itemize="itemize" ,page_width="9.5 cm").next_to(sol_label,DOWN).align_to(sol_label,LEFT)
        
        self.next_slide()
        self.play(Write(sol_6[0]))
        self.play(Write(EC1))
        self.next_slide()
        self.play(Write(sol_6[1]))
        self.next_slide()
        self.play(Write(sol_6[2]))
        self.next_slide()
        self.play(Write(sol_6[3]))
        self.play(Write(EC2))
        self.next_slide()
        self.play(Write(sol_6[4]))
        self.next_slide()
        self.play(Write(sol_6[5]))
        self.play(Write(EC))
        self.next_slide()
        self.play(Write(sol_6[6]))
        self.next_slide()
        self.play(Write(sol_6[7]))
        self.next_slide()
        self.play(Write(sol_6[8]))
        self.next_slide(loop=True)
        self.play(Wiggle(sol_6[-1]))
        self.wait()


class Ex38(Slide):
    def construct(self):

        ex_title = Tex(r"Example 28 :", r"A proton enters the uniform electric field produced by the two charged plates shown below. The magnitude of the electric field is $4.0 \times 10^5$ N/C, and the speed of the proton when it enters is $1.5 \times 10^7$ m/s. What distance $d$ has the proton been deflected downward when it leaves the plates?",tex_environment="{minipage}{8 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)

        pline = MyLabeledLine(Tex(r"$\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +$",font_size=20),pos=0.1*UP,start=2.5*LEFT,end=2*RIGHT,color=RED)
        nline = MyLabeledLine(Tex(r"$\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -$",font_size=20),pos=0.1*DOWN,start=2.5*LEFT,end=2*RIGHT,color=BLUE).shift(3*DOWN)
        darrow = MyDoubLabArrow(Tex("12 cm",font_size=30),start=pline.get_start(),end=pline.get_end(),opacity=1,tip_length=0.1).next_to(pline,UP)
        proton = MyLabeledDot(Tex("+e",font_size=20,color=BLACK),color=PINK).move_to(pline.get_left()).shift(1.5*DOWN)
        dline = DashedLine(start=pline.get_left()+0.2*LEFT,end=pline.get_right(),color=GREY_A).shift(1.5*DOWN)
        cline = DashedVMobject(ArcBetweenPoints( dline.get_end()+DOWN,dline.get_start(),radius=11,color=GREEN))
        dline2 = MyDoubLabArrow(Tex("d",font_size=30),start=dline.get_end(),end=dline.get_end()+DOWN,opacity=1,tip_length=0.1,rot=False).shift(0.2*RIGHT)
        E = MyLabeledArrow(Tex(r"$\vec{E}$",font_size=20),start= 0.5*UP,end=0.5*DOWN,pos=0.2*RIGHT,rot=False,color=RED).next_to(pline,RIGHT).shift(LEFT+0.8*DOWN)
        v = MyLabeledArrow(Tex(r"$\vec{v}$",font_size=30),start= 0.5*LEFT,end=0.5*RIGHT,pos=0.2*UP,rot=False,color=YELLOW).next_to(proton,0.5*UP)
        img = VGroup(pline,nline,E,darrow,dline,cline,proton,v,dline2).next_to(ex_title,RIGHT).align_to(ex_title,UP)
        path = ArcBetweenPoints( dline.get_end()+DOWN,dline.get_start(),radius=11,color=GREEN)

        self.play(Write(ex_title),Write(img))
        self.next_slide()
        self.play(MoveAlongPath(proton,path.reverse_points()),run_time=4)
        self.next_slide()
        sol_label =Tex('Solution :',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 
        sol_1 =  ItemList(Item(r" Given: $E = 4.0 \times 10^5$ N/C, $v = 1.5 \times 10^7$ m/s, ",r"and\\ Plate Length $l=12 $ cm $= 12\times 10^{-2}$ m"),
                            Item(r"Find: Downward deflection $d=?$"),
                            Item(r"Motion along x-axis:"),
                            Item(r"$x_0=0, $ ",r"$u_x = v, $, ", r"$a_x = 0 (\because F_x=0)$",dot=False),
                            Item(r"$x-x_0 = u_x\times t + \dfrac{1}{2}a_xt^2$ (Using 2nd eq. of Motion)",dot=False),
                            Item(r"$x = v\times t$ ", r" Or $t=\dfrac{x}{v}$ ....(1)", dot=False),
                            buff=MED_SMALL_BUFF).next_to(sol_label,DOWN).align_to(sol_label,LEFT)
        
        sol_2 =  ItemList( Item(r"Motion along y-axis:"),
                            Item(r"$y_0=0, $ ",r"$u_y = 0, $", r" $a_y = \dfrac{eE}{m} (\because F_y=eE)$",dot=False),
                            Item(r"$y-y_0 = u_y\times t + \dfrac{1}{2}a_yt^2$ (Using 2nd eq. of Motion)",dot=False),
                            buff=MED_SMALL_BUFF)
        
        sol_3 =  ItemList( Item(r"$y = \dfrac{1}{2}\dfrac{eE}{m}t^2$ ....(2)", dot=False,pw="6 cm"),
                          Item(r"Put Value of t from eq(1) to eq(2)",pw="6 cm"),
                            Item(r"$y = \dfrac{1}{2}\dfrac{eE}{m}\dfrac{x^2}{v^2}$ (eqn of Parabola)", dot=False,pw="6 cm"),
                            Item(r"$d = \dfrac{1}{2}\dfrac{eE}{m}\dfrac{l^2}{v^2}$", dot=False,pw="6 cm"),
                            buff=MED_SMALL_BUFF).next_to(img,DOWN).align_to(img,LEFT)
        self.next_slide()
        for item in sol_1:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        self.play(FadeOut(ex_title))
        self.play(VGroup(sol_label,sol_1).animate.to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2))
        sol_2.next_to(sol_1,DOWN).align_to(sol_1,LEFT)
        line = Line([0,sol_label.get_y(UP),0],[0,config.bottom[1],0],color=RED).next_to(sol_1,0.1*RIGHT).align_to(sol_1,UP)
        self.next_slide()
            
        for item in sol_2:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        
        self.play(Write(line))
        for item in sol_3:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        

class ElecFldLines(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : ELECTRIC CHARGES AND FILEDS',color=GREEN,match_underline_width_to_text=True )
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.add(Outline)
        list = BulletedList('Introduction','Electric Charge','Basic properties of electric charges','Conductors and Insulators','Charging by induction','Coulombs Law',
                            'Forces between multiple charges','Superposition Principle').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        list2 = BulletedList('Electric filed','Electric Field Lines','Electric Dipole and Dipole moment','Electric Field due to an electric dipole',
                             'Dipole in a Uniform External Field','Electric Flux',"Gauss's Law","Applications of Gauss's Law").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        self.play(FadeIn(title, Outline,list,list2))
        self.next_slide(loop=True)
        self.play(FocusOn(list2[1]))
        self.play(Circumscribe(list2[1]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        cur_title = Title(" Electric Field  Lines",match_underline_width_to_text=True, color=GREEN)
        self.play(ReplacementTransform(title,cur_title))
        self.next_slide()

        steps = ItemList(Item(r"As mentioned earlier, the charge on an object (the source charge) alters space in the region around it in such a way that when another charged object (the test charge) is placed in that region of space, that test charge experiences an electric force.", r"This region of space around any charge is called Electric Field"),
                         Item(r"But, How to  pictorially visualize the field?"),
                        buff=MED_LARGE_BUFF).next_to(cur_title,DOWN,buff=0.3).to_corner(LEFT,buff=0.1)
        
        steps2 = ItemList(Item(r" Let us try to represent $\vec{E}$ due to a point charge pictorially."),
                         Item(r"Draw vectors pointing along the direction of the electric field with their lengths proportional to the strength (magnitude) of the field at each point."),
                         Item(r"The vector gets shorter as one goes away from the origin, always pointing radially outward"),
                         Item(r"There is a more useful way to present the same information.", r" Rather than drawing a large number of increasingly smaller vector arrows,", r"we instead connect all of them together, forming continuous lines and curves"),
                        buff=MED_LARGE_BUFF).next_to(cur_title,DOWN,buff=0.3).to_corner(LEFT,buff=0.1)

        q1 = MyLabeledDot(Tex("+",font_size=35,color=BLACK),color=BLUE)
        c1 = Circle(1)
        g1 = VGroup()
        g2 = VGroup()
        g3 = VGroup()
        g4 = VGroup()

        for point in c1.get_all_points():
            uv = Line(point,2*point).get_unit_vector()
            a1=Arrow(start=point,end=point+uv,buff=0,color=RED)
            pt = Dot(point,radius=0.02,color=GREEN_A)
            #a1.move_to(point).shift(0.5*point)
            g1.add(a1,pt)
        
        c2 = Circle(2)

        for point in c2.get_all_points():
            uv = Line(point,2*point).get_unit_vector()
            a2=Arrow(start=point,end=point+0.25*uv,buff=0,color=RED)
            pt = Dot(point,radius=0.02,color=GREEN_A)
            g2.add(a2,pt)
        
        c3 = Circle(2.25)
        
        for point in c3.get_all_points():
            uv = Line(point,2*point).get_unit_vector()
            a2=Arrow(start=point,end=point+1/5.0625*uv,buff=0,color=RED)
            pt = Dot(point,radius=0.02,color=GREEN_A)
            g3.add(a2,pt)
        
        c4 = Circle(2.25+1/5.0625)
        
        for point in c4.get_all_points():
            uv = Line(point,2*point).get_unit_vector()
            a2=Arrow(start=point,end=point+1/5.99*uv,buff=0,color=RED)
            pt = Dot(point,radius=0.02,color=GREEN_A)
            g4.add(a2,pt)

        g6 = VGroup(q1.copy())
        for point in c1.get_all_points():
            ray = Ray(start=point,end=2.5*point,color=RED,eext=0.55)
            g6.add(ray)
        
        g5 = VGroup(q1,g1,g2,g3,g4).next_to(cur_title,DOWN).to_edge(RIGHT)
        fvlbl= Tex(" The vector field of a Positive point charge",font_size=35,tex_environment="{minipage}{5 cm}").next_to(g5,DOWN)
        fllbl= Tex(" The electric field line diagram of a positive point charge",font_size=35,tex_environment="{minipage}{4.5 cm}").next_to(g6,DOWN).to_edge(LEFT)

        self.play(Write(q1))
        self.next_slide()
        for item in steps:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        self.play(FadeOut(steps))

        anm = [steps2[0],VGroup(steps2[1],g1[1]),g1[0],g2[1],VGroup(steps2[2],g2[0]),VGroup(g3[0],g3[1]),VGroup(g4[0],g4[1]),g5,steps2[3][0],steps2[3][1],steps2[3][2]]

        for i in anm:
            self.play(Write(i))
            self.next_slide()

        self.play(FadeOut(steps2))
        self.play(Write(g6.to_edge(LEFT)),Write(fvlbl),Write(fllbl))
        self.next_slide()
        self.play(FadeOut(VGroup(g5,fvlbl)),VGroup(g6,fllbl).animate.to_edge(RIGHT,buff=0.1))

        steps3 = ItemList(Item(r" Have we lost the information about the strength or magnitude of the field now, because it was contained in the length of the arrow?"),
                         Item(r"No. Now the magnitude of the field is represented by the density of field lines."),
                         Item(r"E is strong near the charge, so the density of field lines is more near the charge and the lines are closer."),
                         Item(r"Away from the charge, field gets weaker and the density of field lines is less, resulting in well-separated lines."),
                        buff=MED_LARGE_BUFF).next_to(cur_title,DOWN,buff=0.3).to_corner(LEFT,buff=0.1)
        
        steps4 = ItemList(Item(r" In Figure., the same number of field lines passes through both surfaces (S and S'),",pw="6.5 cm"),
                         Item(r"but the surface S is larger than surface S' ",pw="6.5 cm"),
                         Item(r" Therefore, the density of field lines (number of lines per unit area) is larger at the location of S', ", r"indicating that the electric field is stronger at the location of S' than at S.",pw="6.5 cm"),
                        buff=MED_LARGE_BUFF).next_to(cur_title,DOWN,buff=0.3).to_corner(LEFT,buff=0.1)
        img = ImageMobject("eflines.png",).scale(0.8).next_to(cur_title,DOWN).to_corner(RIGHT,buff=0.1)
        img2 = ImageMobject("eflines2.png").scale(0.9).next_to(cur_title,DOWN).to_corner(RIGHT,buff=0.1)

        steps5 = ItemList(Item(r" Plane Angle ", r"$\theta = \dfrac{\text{arc}}{\text{radius}}$", r"$=\dfrac{\Delta l}{r}$",pw="6.5 cm"),
                         Item(r"Solid Angle  ", r"$\Delta \Omega = \dfrac{\text{Plane area}}{\text{radius}^2}$", r"$= \dfrac{\Delta S}{r^2}$",pw="6.5 cm"),
                         buff=MED_LARGE_BUFF).next_to(cur_title,DOWN,buff=0.3).to_corner(LEFT,buff=0.1)

        steps6 = ItemList(Item(r"Electric Filed at $P_1$: ", r"$E_{P_1}\propto \dfrac{n}{\Delta S_1}$","$\propto \dfrac{n}{\Delta \Omega\  r_{1}^2} $"),
                         Item(r"Electric Filed at $P_2$: ", r"$E_{P_2}\propto \dfrac{n}{\Delta S_2}$","$\propto \dfrac{n}{\Delta \Omega\ r_{2}^2} $"),
                         Item(r"Since $n$ and  $\Delta \Omega$ are common, the strength of the field clearly has a $\dfrac{1}{r^2}$ dependence.",pw="6.5 cm"),
                         buff=MED_LARGE_BUFF).next_to(steps5,DOWN).to_corner(LEFT,buff=0.1)
        
        arc = Arc(3,30*DEGREES,-30*DEGREES,color=BLUE)
        arclbl = Tex(r"$\Delta l$",font_size = 35).next_to(arc,RIGHT)
        line1 = Line(ORIGIN,arc.get_end(),color=BLUE)
        linelbl = Tex("$r$",font_size = 35).next_to(line1,DOWN)
        line2 = Line(ORIGIN,arc.get_start(),color=BLUE)
        ang = Angle(line1,line2,radius=0.8)
        anglbl = Tex(r"$\theta$",font_size = 35).next_to(ang,RIGHT)
        ag = VGroup(line1,line2,arc,ang,arclbl,linelbl,anglbl).next_to(cur_title,DOWN).to_edge(RIGHT)

        el = Ellipse(0.4,2,color=GREEN,fill_opacity=0.6)
        e2 = Ellipse(0.08,0.4,color=BLUE).shift(12/5*LEFT)
        elbl =  Tex(r"$\Delta S$",font_size = 35).next_to(el,RIGHT)
        line3 = Line(3*LEFT,el.get_top())
        line4 = Line(3*LEFT,el.get_bottom())
        slbl = Tex(r"$\Delta \Omega$",font_size = 35).move_to(2*LEFT+0.1*UP)
        line4lbl = Tex("$r$",font_size = 35).next_to(line4,DOWN,buff=0).shift(0.2*UP)
        sag = VGroup(el,e2, line3,line4,line4lbl,elbl,slbl).rotate(20*DEGREES).next_to(ag,DOWN)

        anm2 = [VGroup(steps5[0][0],ag),steps5[0][1],steps5[0][2],VGroup(steps5[1][0],sag),steps5[1][1],steps5[1][2]]

        for item in steps3:
            self.play(Write(item))
            self.next_slide()

        self.play(FadeOut(steps3,g6,fllbl))
        self.play(FadeIn(img))

        for item in steps4:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        
        self.play(FadeOut(steps4,img))
        self.next_slide()
        for item in anm2:
            self.play(Write(item))
            self.next_slide()

        self.play(FadeIn(img2))
        self.play(FadeOut(ag,sag))
        for item in steps6:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()

        self.play(FadeOut(steps6,img2,steps5))
        self.next_slide()

        eflines = ItemList(Item(r"The picture of field lines was invented by Faraday", r" to develop an intuitive non-mathematical way of visualising electric fields around charged configurations. ", r" Faraday called them lines of force",pw="13 cm"),
                         Item(r"Electric field lines are thus a way of pictorially mapping (visualising) the electric field around a configuration of charges.",pw="13 cm"),
                         Item(r"An electric field line is, in general a curve drawn in such a way that the tangent to it at each point is in the direction of the net field at that point.",pw="13 cm"),
                         Item(r"The arrow specify the direction of electric field from the two possible directions indicated by a tangent",pw="13 cm"),
                         Item(r"The denser the electric field line, the stronger the electric field.",pw="13 cm"),
                         buff=MED_LARGE_BUFF).next_to(cur_title,DOWN,buff=0.3).to_corner(LEFT,buff=0.1)
        
        for item in eflines:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        

        self.wait(2)


class ElecFldLines2(Slide):
    def construct(self):
        cur_title = Title(" Electric Field  Lines",match_underline_width_to_text=True, color=GREEN)
        self.add(cur_title)
        q1 = MyLabeledDot(Tex("$+$",font_size=35,color=BLACK),color=BLUE)
        q2 = MyLabeledDot(Tex("$-$",font_size=35,color=BLACK),color=GREEN)
        c1 = Circle(1)

        g1 = VGroup(q1)
        for point in c1.get_all_points():
            ray = Ray(start=point,end=2.5*point,color=RED,eext=0.55)
            g1.add(ray)
        
        g1.to_edge(LEFT)
        
        g1lbl = Tex(r"(1) The field lines of a single positive charge are radially outward",tex_environment="{minipage}{5 cm}",font_size = 35).next_to(g1,DOWN)
        sr1=SurroundingRectangle(VGroup(g1,g1lbl))

        self.play(Write(g1),Write(sr1),run_time=4)
        self.play(Write(g1lbl))
        self.next_slide()
        
        g2 = VGroup(q2)
        for point in c1.get_all_points():
            ray = Ray(start=2.5*point,end=point,color=RED,ext=0.55)
            g2.add(ray)
        g2.to_edge(RIGHT)
        g2lbl = Tex(r"(2) The field lines of a single negative charge are radially inward",tex_environment="{minipage}{5 cm}",font_size = 35).next_to(g2,DOWN)
        sr2=SurroundingRectangle(VGroup(g2,g2lbl))
        self.play(Write(g2),Write(sr2),run_time=4)
        self.play(Write(g2lbl))
        self.next_slide()
        self.play(FadeOut(g1,g2,g1lbl,g2lbl,sr1,sr2))
        self.next_slide()

        q3 = MyLabeledDot(Tex("$+$",font_size=35,color=BLACK),color=BLUE).shift(2*LEFT)
        q4 = MyLabeledDot(Tex("$-$",font_size=35,color=BLACK),color=GREEN).shift(3*RIGHT)

        c1 = VGroup()

        for r in [1.2,1.4,1.8,2.4]:
            c1.add(CurvedRay(q3.get_center(),q4.get_center(),radius=2.5*r,color=RED))
            c1.add(CurvedRay(q4.get_center(),q3.get_center(),radius=2.5*r,color=RED,rev=True))
        
        c1.add(Ray(q3.get_center(),q4.get_center(),color=RED))
        c1.add(Ray(q3.get_center(),q3.get_center()+LEFT,color=RED))
        c1.add(Ray(q4.get_center()+RIGHT,q4.get_center(),color=RED))

        c1.add(CurvedRay(q3.get_center()+2*UP+0.5*RIGHT,q3.get_center(),radius=2,color=RED,rev=True))
        c1.add(CurvedRay(q3.get_center(),q3.get_center()+2*DOWN+0.5*RIGHT,radius=2,color=RED))
        c1.add(CurvedRay(q3.get_center()+2*UP-0.5*RIGHT,q3.get_center(),radius=2,color=RED,rev=True))
        c1.add(CurvedRay(q3.get_center(),q3.get_center()+2*DOWN-0.5*RIGHT,radius=2,color=RED))
        c1.add(CurvedRay(q3.get_center()+2*UP+1.5*RIGHT,q3.get_center(),radius=2,color=RED,rev=True))
        c1.add(CurvedRay(q3.get_center(),q3.get_center()+2*DOWN+1.5*RIGHT,radius=2,color=RED))
        c1.add(CurvedRay(q4.get_center(),q4.get_center()+2*UP+0.5*RIGHT,radius=2,color=RED,rev=True))
        c1.add(CurvedRay(q4.get_center()+2*DOWN+0.5*RIGHT,q4.get_center(),radius=2,color=RED))
        c1.add(CurvedRay(q4.get_center(),q4.get_center()+2*UP-0.5*RIGHT,radius=2,color=RED,rev=True))
        c1.add(CurvedRay(q4.get_center()+2*DOWN-0.5*RIGHT,q4.get_center(),radius=2,color=RED))
        c1.add(CurvedRay(q4.get_center(),q4.get_center()+2*UP-1.5*RIGHT,radius=2,color=RED,rev=True))
        c1.add(CurvedRay(q4.get_center()+2*DOWN-1.5*RIGHT,q4.get_center(),radius=2,color=RED))

        c1.add(q3,q4).to_edge(LEFT)

        q5 = MyLabeledDot(Tex("$+$",font_size=35,color=BLACK),color=BLUE).shift(LEFT)
        q6 = MyLabeledDot(Tex("$+$",font_size=35,color=BLACK),color=BLUE).shift(RIGHT)

        c2 = VGroup()

        for r in [1,1.7,2.5]:
            c2.add(CurvedRay(q6.get_center(),q6.get_center()+1.5*RIGHT+r*DOWN,radius=2,color=RED))
            c2.add(CurvedRay(q6.get_center()+1.5*RIGHT+r*UP,q6.get_center(),radius=2,color=RED,rev=True))
            c2.add(CurvedRay(q5.get_center(),q5.get_center()+1.5*LEFT+r*UP,radius=2,color=RED))
            c2.add(CurvedRay(q5.get_center()+1.5*LEFT+r*DOWN,q5.get_center(),radius=2,color=RED,rev=True))
        
        for r in [0.3,0.8]:
            c2.add(CurvedRay(q6.get_center(),q6.get_center()+r*LEFT+2.5*DOWN,radius=4,color=RED))
            c2.add(CurvedRay(q6.get_center()+r*LEFT+2.5*UP,q6.get_center(),radius=4,color=RED,rev=True))
            c2.add(CurvedRay(q5.get_center(),q5.get_center()+r*RIGHT+2.5*UP,radius=4,color=RED))
            c2.add(CurvedRay(q5.get_center()+r*RIGHT+2.5*DOWN,q5.get_center(),radius=4,color=RED,rev=True))
        

        c2.add(Ray(q5.get_center(),q5.get_center()+1.5*LEFT,color=RED))
        c2.add(Ray(q6.get_center(),q6.get_center()+1.5*RIGHT,color=RED))
        c2.add(q5,q6).to_edge(RIGHT)
        c1lbl = Tex(r"(3) The field lines of a A dipole (Two equal an opposite charges)",tex_environment="{minipage}{5 cm}",font_size = 35).next_to(c1,DOWN)
        c2lbl = Tex(r"(4) The field lines of Two identical charges",tex_environment="{minipage}{5 cm}",font_size = 35).next_to(c2,DOWN)
        sr3=SurroundingRectangle(VGroup(c1,c1lbl))
        sr4=SurroundingRectangle(VGroup(c2,c2lbl))

        self.play(Write(c1),run_time=4)
        self.play(Write(c1lbl),Write(sr3))
        self.next_slide()
        self.play(Write(c2),run_time=4)
        self.play(Write(c2lbl),Write(sr4))
        self.next_slide()
        self.play(FadeOut(c1,c2,c1lbl,c2lbl,sr3,sr4))
        new_title = Title("Properties of Electric Field  Lines",match_underline_width_to_text=True, color=GREEN)
        self.play(ReplacementTransform(cur_title,new_title))
        self.next_slide()

        prop1= ItemList(Item(r" (1) ", r" Field lines starts from positive charge and end at negative charge.",r" If there is a single charge, they may start or end at infinity.",pw="13 cm"), buff=MED_LARGE_BUFF
                       ).next_to(new_title,DOWN,buff=0.8).to_corner(LEFT,buff=0.1)
        
        group1  = VGroup(c1,g1,g2).scale(0.7).arrange(RIGHT).next_to(prop1,DOWN)
        anm = [prop1[0][0].set_color(ORANGE), VGroup(prop1[0][1],c1),VGroup(prop1[0][2],g1,g2)]
        
        for item in anm:
            self.play(Write(item))
            self.wait()
            self.next_slide()

        self.play(FadeOut(prop1,group1))
        self.next_slide()

        prop2= ItemList(Item(r" (2) ", r"Magnitude of electric field is repersented by the density of Filed lines." ,r" The denser the electric field line, the stronger the electric field.",pw="13 cm"), buff=MED_LARGE_BUFF
                       ).next_to(new_title,DOWN,buff=0.8).to_corner(LEFT,buff=0.1)
        
        img = ImageMobject("eflines.png",).scale(0.7).next_to(prop2,DOWN)
        anm = [Write(prop2[0][0].set_color(ORANGE)), Write(prop2[0][1]),FadeIn(img), Write(prop2[0][2]),FadeOut(prop2,img)]
        
        for item in anm:
            self.play(item)
            self.wait()
            self.next_slide()

        prop3= ItemList(Item(r" (3) ", r"The tangent at any point of a field line gives the direction of net field at that point." ,pw="13 cm"), buff=MED_LARGE_BUFF
                       ).next_to(new_title,DOWN,buff=0.8).to_corner(LEFT,buff=0.1)
        
        efl = CurvedRay(2*LEFT,2*RIGHT+3*UP,radius=4,color=RED)
        tan=TangentLine(efl[0],0.25,color=GREEN,length=2).add_tip(tip_shape=StealthTip,tip_length=0.1)
        dot = Dot(tan.get_center(),radius=0.04)

        
        img = VGroup(efl,tan,dot,Tex(r"$\vec{E}$",font_size=30).next_to(tan.get_end(),DOWN)).next_to(prop3,DOWN)
        anm = [Write(prop3[0][0].set_color(ORANGE)), Write(prop3[0][1]),Write(efl),Write(dot),Write(VGroup(tan,img[-1])),FadeOut(prop3,img)]
        
        for item in anm:
            self.play(item)
            self.wait()
            self.next_slide()

        prop4= ItemList(Item(r" (4) ", r"When drawing lines, the number of lines is proportional to the amount of electric charge." ,pw="13 cm"), buff=MED_LARGE_BUFF
                       ).next_to(new_title,DOWN,buff=0.8).to_corner(LEFT,buff=0.1)
        
        c1 = Circle(1)
        q5 = MyLabeledDot(Tex("$+q$",font_size=35,color=BLACK),color=BLUE)
        img3 = VGroup(q5)
        for i in range(0,8):
            ray = Ray(start=c1.get_all_points()[4*i],end=2.2*c1.get_all_points()[4*i],color=RED,eext=0.52)
            img3.add(ray)

        q6 = MyLabeledDot(Tex("$+2q$",font_size=35,color=BLACK),color=BLUE)
        img4 = VGroup(q6)
        for i in range(16):
            pt = np.cos(i*PI/8)*RIGHT+np.sin(i*PI/8)*UP
            ray = Ray(start=pt,end=2.2*pt,color=RED,eext=0.52)
            img4.add(ray)


        
        img3.next_to(prop4,DOWN).to_edge(LEFT)
        img4.next_to(prop4,DOWN).to_edge(RIGHT)
        anm = [Write(prop4[0][0].set_color(ORANGE)), Write(prop4[0][1]),Write(img3),Write(img4),FadeOut(prop4,img3,img4)]
        
        for item in anm:
            self.play(item)
            self.wait()
            self.next_slide()

        
        prop5= ItemList(Item(r" (5) ", r"In a charge-free region, electric field lines can be taken to be continuous curves without any breaks." ,pw="13 cm"), buff=MED_LARGE_BUFF
                       ).next_to(new_title,DOWN,buff=0.8).to_corner(LEFT,buff=0.1)
        anm = [Write(prop5[0][0].set_color(ORANGE)), Write(prop5[0][1]),FadeOut(prop5)]
        
        for item in anm:
            self.play(item)
            self.wait()
            self.next_slide()

        prop6= ItemList(Item(r" (6) ", r"Electric field lines do not form close loops.", r" This indicates that +ve and -ve charge can  exist seperately.", pw="13 cm"), buff=MED_LARGE_BUFF
                       ).next_to(new_title,DOWN,buff=0.8).to_corner(LEFT,buff=0.1)
        anm = [Write(prop6[0][0].set_color(ORANGE)), Write(prop6[0][1]), Write(prop6[0][2]),FadeOut(prop6)]
        
        for item in anm:
            self.play(item)
            self.wait()
            self.next_slide()

        prop7= ItemList(Item(r" (7) ", r"Two field lines can never cross each other. ", r"Because, if they did the electric field at the point of intersection will have two directions, which is not possible." ,pw="13 cm"), buff=MED_LARGE_BUFF
                       ).next_to(new_title,DOWN,buff=0.8).to_corner(LEFT,buff=0.1)
        

        ef3 = CurvedRay(2*LEFT,2*RIGHT+3*UP,radius=9,color=RED)
        ef4 = CurvedRay(2*LEFT+3*UP,4*RIGHT+DOWN,radius=10,color=GREEN)
        tan1=TangentLine(ef3[0],0.4,color=ORANGE,length=2).add_tip(tip_shape=StealthTip,tip_length=0.1)
        tan2=TangentLine(ef4[0],0.4,color=GOLD,length=2).add_tip(tip_shape=StealthTip,tip_length=0.1)

        
        pi = Intersection(ef3,ef4).get_center()
        dot = Dot(pi,radius=0.04)

        
        img6 = VGroup(ef3,ef4,tan1,tan2,dot,Tex(r"$\vec{E}$",font_size=30).next_to(tan1.get_end(),DOWN)).next_to(prop7,DOWN)
        anm = [Write(prop7[0][0].set_color(ORANGE)), Write(prop7[0][1]),Write(prop7[0][2]),Write(ef3),Write(ef4),Write(dot),Write(VGroup(tan1,tan2,img6[-1])),FadeOut(prop7,img6)]
        
        for item in anm:
            self.play(item)
            self.wait()
            self.next_slide()


        
