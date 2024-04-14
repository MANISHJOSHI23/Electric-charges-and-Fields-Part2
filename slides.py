# example.py

from manim import *  # or: from manimlib import *

from manim_slides import Slide

def Item(*str,dot = True,font_size = 35,math=False,pw="8cm",color=WHITE):
    if math:
        tex = MathTex(*str,font_size=font_size,color=color)
    else:
        tex = Tex(*str,font_size=font_size,color=color,tex_environment=f"{{minipage}}{{{pw}}}")
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


class Obj(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : ELECTRIC CHARGES AND FILEDS',color=GREEN)
        self.play(Write(title))
        #self.play(Rotate(title,2*PI))
        self.next_slide()
        Outline = Tex('Learning Objectives :',color=BLUE)
        self.play(Write(Outline))
        self.next_slide()
        self.play(Outline.animate.next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8))
        self.next_slide()
        list = BulletedList('Introduction','Electric Charge','Basic properties of electric charges','Conductors and Insulators','Charging by induction','Coulombs Law',
                            'Forces between multiple charges','Superposition Principle').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        self.play(Write(list[0]))
        self.next_slide()
        self.play(Write(list[1]))
        self.next_slide()
        self.play(Write(list[2]))
        self.next_slide()
        self.play(Write(list[3]))
        self.next_slide()
        self.play(Write(list[4]))
        self.next_slide()
        self.play(Write(list[5]))
        self.next_slide()
        self.play(Write(list[6]))
        self.next_slide()
        self.play(Write(list[7]))
        self.next_slide()
        list2 = BulletedList('Electric filed','Electric Field Lines','Electric Dipole and Dipole moment','Electric Field due to an electric dipole',
                             'Dipole in a Uniform External Field','Electric Flux',"Gauss's Law","Applications of Gauss's Law").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        self.play(Write(list2[0]))
        self.next_slide()
        self.play(Write(list2[1]))
        self.next_slide()
        self.play(Write(list2[2]))
        self.next_slide()
        self.play(Write(list2[3]))
        self.next_slide()
        self.play(Write(list2[4]))
        self.next_slide()
        self.play(Write(list2[5]))
        self.next_slide()
        self.play(Write(list2[6]))
        self.next_slide()
        self.play(Write(list2[7]))
        self.next_slide(loop=True)
        self.play(FocusOn(list[0]))
        self.play(Circumscribe(list[0]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('Introduction', color=BLUE)
        self.play(ReplacementTransform(title,Intro_title))
        self.wait()


class Intro(Slide):
    def construct(self):
        Intro_title = Title('Introduction', color=BLUE)
        self.add(Intro_title)
        Obser = Tex('Daily Observations :',color=BLUE).next_to(Intro_title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.play(Write(Obser))
        self.next_slide()
        list = BulletedList('All of us have the experience of seeing a spark or hearing a crackle when we take off our synthetic clothes or sweater, particularly in dry weather.',
                             'Another common example of electric discharge is the lightning that we see in the sky during thunderstorms.',
                             'We also experience a sensation of an electric shock either while opening the door of a car or holding the iron bar of a bus after sliding from our seat.',
                              'This is due to generation of static electricity', 'Static means anything that does not move or change with time',
                              'Electrostatics deals with the study of forces, fields and potentials arising from static charges.' ).scale(0.7).next_to(Obser,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        self.play(Write(list[0]))
        img1 = ImageMobject('img_1.jpg').next_to(list[0],DOWN).to_corner(RIGHT).scale(0.8)
        self.play(FadeIn(img1))
        self.next_slide()
        self.play(FadeOut(img1))
        self.play(Write(list[1]))
        img2 = ImageMobject('img_2.jpg').next_to(list[0],DOWN, buff=0.5).to_corner(RIGHT).scale(0.8)
        self.play(FadeIn(img2))
        self.next_slide()
        self.play(FadeOut(img2))
        self.play(Write(list[2]))
        img3 = ImageMobject('img_3.jpg').next_to(list[0],DOWN,buff=1).to_corner(RIGHT).scale(0.45)
        self.play(FadeIn(img3))
        self.next_slide()
        self.play(FadeOut(img3))
        self.play(Write(list[3]))
        self.next_slide()
        self.play(Write(list[4]))
        self.next_slide()
        self.play(Write(list[5]))
        self.next_slide()
        

class Charge(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : ELECTRIC CHARGES AND FILEDS',color=GREEN)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.add(Outline)
        list = BulletedList('Introduction','Electric Charge','Basic properties of electric charges','Conductors and Insulators','Charging by induction','Coulombs Law',
                            'Forces between multiple charges','Superposition Principle').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        list2 = BulletedList('Electric filed','Electric Field Lines','Electric Dipole and Dipole moment','Electric Field due to an electric dipole',
                             'Dipole in a Uniform External Field','Electric Flux',"Gauss's Law","Applications of Gauss's Law").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        self.play(FadeIn(title, Outline,list,list2))
        self.next_slide(loop=True)
        self.play(FocusOn(list[1]))
        self.play(Circumscribe(list[1]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Charge_title = Title('Electric Charges and Their Properties ', color=GREEN)
        self.play(ReplacementTransform(title,Charge_title))
        list3 = BulletedList('All matter is made of Atoms.').scale(0.7).next_to(Charge_title,DOWN).to_edge(LEFT).shift(0.5*RIGHT)
        self.play(Write(list3[0]))
        orbit1 = Circle(1,color=YELLOW).shift(3*LEFT)
        orbit2 = Circle(2,color=YELLOW).shift(3*LEFT)
        Atom_txt = Tex('Atom',color=PINK).scale(0.6).next_to(orbit2,DOWN)
        self.play(Create(orbit1),Create(orbit2),Write(Atom_txt))
        point1 =Circle(radius=0.05,color=ORANGE).set_fill(ORANGE, opacity=0.6).shift(3*LEFT)
        point2 =Circle(radius=0.05,color=GREY).set_fill(GREY, opacity=0.6).shift(3*LEFT)
        point3 =Circle(radius=0.05,color=BLUE).set_fill(BLUE, opacity=0.6)
        g1=VGroup(point1.copy().next_to(point1,LEFT,buff=0),point1.copy().next_to(point1,RIGHT,buff=0),point1.copy().next_to(point1,UP,buff=0),point1.copy().next_to(point1,DOWN,buff=0),point2.copy().next_to(point1,UL,buff=0),point2.copy().next_to(point1,DR,buff=0),point2.copy().next_to(point1,UR,buff=0),point2.copy().next_to(point1,DL,buff=0),point2)
        self.play(Create(g1))
        self.play(Create(VGroup(point3.next_to(orbit1,RIGHT,buff=-0.05),point3.copy().next_to(orbit1,LEFT,buff=-0.05),point3.copy().next_to(orbit2,UP,buff=-0.05),point3.copy().next_to(orbit2,DOWN,buff=-0.05))))
        self.next_slide()
        nu=g1.copy()
        self.play(nu.animate.next_to(orbit2,UR).shift(1.5*RIGHT).scale(2))
        nu_txt = Tex('Nucleus',color=RED_C).next_to(nu,DOWN).scale(0.6)
        self.play(Write(nu_txt))
        proton = nu.submobjects[0].copy()
        self.next_slide()
        self.play(proton.animate.next_to(nu, DOWN,buff=1.75))
        self.play(Create(Arrow(nu_txt,proton)))
        proton_txt = Tex('Proton',color=GREEN_D).next_to(nu,DOWN,buff=2).scale(0.6)
        self.play(Write(proton_txt))
        self.next_slide()
        neutron = nu.submobjects[5].copy()
        self.play(neutron.animate.next_to(nu, DOWN,buff=1.75).shift(2.5*RIGHT))
        self.play(Create(Arrow(nu_txt,neutron,max_tip_length_to_length_ratio=0.15)))
        neutron_txt = Tex('Neutron',color=GREEN_D).next_to(nu,DOWN,buff=2).scale(0.6).shift(2.5*RIGHT)
        self.play(Write(neutron_txt))
        self.next_slide()
        electron = point3.copy()
        self.play(electron.animate.next_to(nu, DOWN,buff=1.75).scale(2).shift(5*RIGHT))
        electron_txt = Tex('Electron',color=GREEN_D).next_to(nu,DOWN,buff=2).scale(0.6).shift(5*RIGHT)
        self.play(Write(electron_txt))
        self.next_slide()
        mass_label = MathTex('Mass\ : ').scale(0.4).next_to(proton_txt,DOWN).shift(1.5*LEFT+0.05*DOWN)
        mp = MathTex(r"M_p = 1.67 \times 10^{-27}\ kg ").scale(0.4).next_to(proton_txt, DOWN)
        mn = MathTex(r"M_n = 1.68 \times 10^{-27}\ kg ").scale(0.4).next_to(neutron_txt, DOWN)
        me = MathTex(r"M_e = 9.11 \times 10^{-31}\ kg ").scale(0.4).next_to(electron_txt, DOWN)
        self.play(Write(mass_label),Write(mp))
        self.next_slide()
        self.play(Write(mn))
        self.next_slide()
        self.play(Write(me))   

        charge_label = MathTex('Charge\ : ').scale(0.4).next_to(mass_label,DOWN).shift(0.1*DOWN)
        qp = MathTex(r"q_p = 1.602 \times 10^{-19}\ C ").scale(0.4).next_to(mp, DOWN)
        qn = MathTex(r"q_n = 0 \ C\ (Neutral) ").scale(0.4).next_to(mn, DOWN)
        qe = MathTex(r"q_e = -1.602 \times 10^{-19}\ C ").scale(0.4).next_to(me, DOWN)
        self.next_slide()
        self.play(Write(charge_label),Write(qp))
        self.next_slide()
        self.play(Write(qn))
        self.next_slide()
        self.play(Write(qe))   
        self.wait()

class Charge2(Slide):
    def construct(self):
        Charge_title = Title('Electric Charges and Their Properties', color=GREEN)
        self.add(Charge_title)
        list = BulletedList('Charge is a fundamental property of matter by virtue of which it produces and experience electromagnetic force.','Electromagnetic forces can be attractive or repulsive. In contrast with the gravitational froce between masses which is always attractive. ', "There are two kinds of electric charges which are distinguished form each other by calling one kind as 'posiitve' and the other as 'negative', these names are arbitraily chosen by Benjamin Franklin. ",'Like chagres repel each other and Unlike charges attract each other', ).scale(0.7).next_to(Charge_title,2*DOWN).to_corner(LEFT).shift(RIGHT)
        list2=BulletedList('Charge is a scalar quantitiy.','S.I unit of charge is coulomb (C)', 'C.G.S. unit of charge is esu (electrostatic unit) or static coloumb (stat C or franklin)','1 C $= 3\\times 10^{9}$ stat C','Dimension formula of charge [Q]=[AT]   $(\\because Q=It)$','A charge cannot exist without masss (however a mass can exist without charge e.g. neutron) ').scale(0.7).next_to(Charge_title,2*DOWN).to_corner(LEFT).shift(RIGHT)
        chq_trn_lbl = Tex('Charge is transferable :',color=BLUE).next_to(Charge_title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        list3 =BulletedList('Charge can be transfered from one body to another.','Neutral Body $+$ electron $\\rightarrow$ Negatively charge body','Neutral Body $-$ electron $\\rightarrow$ Positively charge body','When we charge an object, the mass of the body changes because wherever there is charge, there is mass.').scale(0.7).next_to(chq_trn_lbl,DOWN).to_corner(LEFT).shift(RIGHT)
        frc_elc_lbl = Tex('Frictional Electricity :',color=BLUE).next_to(list3,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        list4 =BulletedList('When two bodies are rubbed together under friction electrons are transferred from one body to the other. As a result one body becomes positively charged while the other gets negatively charged.').scale(0.7).next_to(frc_elc_lbl,DOWN).to_corner(LEFT).shift(RIGHT)
        self.play(Write(list[0]))
        self.next_slide()
        self.play(Write(list[1]))
        self.next_slide()
        self.play(Write(list[2]))
        self.next_slide()
        self.play(Write(list[3]))
        self.next_slide()
        self.play(FadeOut(list))
        self.play(Write(list2[0]))
        self.next_slide()
        self.play(Write(list2[1]))
        self.next_slide()
        self.play(Write(list2[2]))
        self.next_slide()
        self.play(Write(list2[3]))
        self.next_slide()
        self.play(Write(list2[4]))
        self.next_slide()
        self.play(Write(list2[5]))
        self.next_slide()
        self.play(FadeOut(list2))
        self.play(Write(chq_trn_lbl))
        self.next_slide()
        self.play(Write(list3[0]))
        self.next_slide()
        self.play(Write(list3[1]))
        self.next_slide()
        self.play(Write(list3[2]))
        self.next_slide()
        self.play(Write(list3[3]))
        self.next_slide()
        self.play(Write(frc_elc_lbl))
        self.next_slide()
        self.play(Write(list4[0]))
        self.next_slide()
        self.play(FadeOut(list3,frc_elc_lbl,list4,chq_trn_lbl))
        self.next_slide()
        add_lbl = Tex('Additivity of Charges :',color=BLUE).next_to(Charge_title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.play(Write(add_lbl))
        list5 =BulletedList(' If a system contains n charges $q_1,\ q_2,\ q_3,\ ..., q_n$ , then the total charge of the system is $q_1 + q_2 + q_3 + ... + q_n$ . i.e., charges add up like real numbers or they are scalars',' Proper signs have to be used while adding the charges in a system.','Example:  Total charge $(Q)=q_1+q_2+q_3+q_4$','$(Q)=5\ C+(-2\ C)+3\ C+(-7\ C)=-1\ C$').scale(0.7).next_to(chq_trn_lbl,DOWN).to_corner(LEFT).shift(RIGHT)
        self.next_slide()
        self.play(Write(list5[0]))
        self.next_slide()
        self.play(Write(list5[1]))
        cir = Circle(1.5).next_to(list5[1],DOWN).to_edge(RIGHT).shift(LEFT)
        q1=Dot(cir.get_center(),color=YELLOW).shift(0.9*LEFT)
        q1_text=Tex('$q_1=5 C$').next_to(q1,DOWN,buff=0).scale(0.5)
        q2=Dot(cir.get_center(),color=ORANGE).shift(0.9*RIGHT)
        q2_text=Tex('$q_2=-2 C$').next_to(q2,DOWN,buff=0).scale(0.5)
        q3=Dot(cir.get_center(),color=PURPLE_A).shift(0.5*DOWN)
        q3_text=Tex('$q_3=3 C$').next_to(q3,DOWN,buff=0).scale(0.5)
        q4=Dot(cir.get_center(),color=GREEN_D).shift(0.8*UP)
        q4_text=Tex('$q_4=-7 C$').next_to(q4,DOWN,buff=0).scale(0.5)
        self.play(Create(cir),Create(VGroup(q1,q2,q3,q4)),Write(VGroup(q1_text,q2_text,q3_text,q4_text)))
        self.next_slide()
        self.play(Write(list5[2]))
        self.next_slide()
        self.play(Write(list5[3]))
        self.next_slide()


class Charge3(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")
        Charge_title = Title('Electric Charges and Their Properties', color=GREEN)
        self.add(Charge_title)
        cons_lbl = Tex('Conservation of Charges :',color=BLUE).next_to(Charge_title,DOWN).to_corner(LEFT).scale(0.8)
        self.play(Write(cons_lbl))
        list =BulletedList('Charge can neither be created nor destroyed; it can only be transferred from place to place, from one object to another.', 'Within an isolated system consisting of many charged bodies, due to interactions among the bodies, charges may get redistributed but it is found that the total charge of the isolated system is always conserved.',' Sometimes nature creates charged particles from an uncharged particle: a neutron turns into a proton and an electron.','Neutron $(q_n =0)$ $\\Rightarrow$ Proton $(q_p=+e)$ $+$ Electron $(q_e=-e)$ ','Pair Production:', 'Gamma Ray photon $(q_\gamma =0)$ $\\Rightarrow$ Positron $(q_{e^{+}}=+e)$ $+$ Electron $(q_e=-e)$').scale(0.7).next_to(cons_lbl,DOWN).to_corner(LEFT).shift(RIGHT)
        self.next_slide()
        self.play(Write(list[0]))
        self.next_slide()
        self.play(Write(list[1]))
        self.next_slide()
        self.play(Write(list[2]))
        self.next_slide()
        self.play(Write(list[3]))
        self.next_slide()
        self.play(Write(list[4]))
        self.next_slide()
        self.play(Write(list[5]))
        self.next_slide()
        self.play(FadeOut(list,cons_lbl))
        self.next_slide()
        quant_lbl = Tex('Quantisation of charge: ',color=BLUE).next_to(Charge_title,DOWN).to_corner(LEFT).scale(0.8)
        self.play(Write(quant_lbl))
        list2 =BulletedList('Quantisation of charge means that electric charge comes in discrete amounts, and there is a smallest possible amount of charge ( $e = 1.602 \\times 10^{-19}$ C ) that an object can have. No free particle can have less charge than this, and, therefore, the charge $(q)$ on any object must be an integer multiple of this amount $(e)$. ').scale(0.7).next_to(cons_lbl,DOWN).to_corner(LEFT).shift(RIGHT)
        form = Tex('$q = ne$   (Where $n=\\pm 1,\ \\pm 2,\ \\pm 3,\ .....$)').next_to(list2,DOWN).scale(0.8)
        self.next_slide()
        self.play(Write(list2[0]))
        self.next_slide()
        self.play(Write(form))
        self.next_slide()
        self.play(Write(BulletedList('For macroscopic charges for which n is a very large number, quantisation of charge can be ignored and charge appears to be continuous.}').next_to(form,DOWN).scale(0.7)))

class Ex1(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 1: If a body has positive charge on it, then it means it has}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        op = VGroup(Tex('(a) Gained some proton').scale(0.7),Tex('(b) Lost some protons').scale(0.7),Tex('(c) Gained some electrons').scale(0.7),Tex('(d) Lost some electrons').scale(0.7) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(op))
        self.next_slide(loop=True)
        self.play(Circumscribe(op.submobjects[3]))

class Ex2(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 2: Which of the following is not true about electric charge }',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        op = VGroup(Tex('\justifying {(a) Charge on a body is always integral muliple of certain charge known as charge of electron}',tex_template=myBaseTemplate).scale(0.7),Tex('\justifying {(b) Charge is a scalar quantity}',tex_template=myBaseTemplate).scale(0.7),Tex('\justifying {(c) Net charge of an isolated system is always conservesd}',tex_template=myBaseTemplate).scale(0.7),Tex('\justifying {(d) Charge can be converted into energy and energy can be converted into charge}',tex_template=myBaseTemplate).scale(0.7) ).arrange_in_grid(4,1,col_alignments='l').next_to(ex_title,DOWN)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(op))
        self.next_slide(loop=True)
        self.play(Circumscribe(op.submobjects[3]))

class Ex3(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 3: Consider three point objects $P,\ Q$ and $R$. $P$ and $Q$ repel each other, while $P$ and $R$ attract. What is the nature of force between $Q$ and $R$? }',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        op = VGroup(Tex('(a) Repulsive force').scale(0.7),Tex('(b) Attractive force ').scale(0.7),Tex('(c) No force').scale(0.7),Tex('(d) None of these').scale(0.7) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(op))
        self.next_slide(loop=True)
        self.play(Circumscribe(op.submobjects[1]))

class Ex4(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 4: When $10^{14}$ electrons are removed from a neutral metal sphere, the charge on the sphere becomes:}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        op = VGroup(Tex('(a) $16\ \mu$ C').scale(0.7),Tex('(b) $-16\ \mu$ C').scale(0.7),Tex('(c) $32\ \mu$ C').scale(0.7),Tex('(d) $-32\ \mu$ C').scale(0.7) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(op))
        sol_label =Tex('Solution :', color=ORANGE).next_to(op,DOWN).to_edge(LEFT).scale(0.8)
        sol = BulletedList('Given: No. of electron removed $n = 10^{14}$', 'Find: Charge on the sphere $q = ?$','Using $q= ne$','$q=10^{14}\\times 1.6 \\times 10^{-19}$ C  $=1.6\\times 10^{-5}$ C ','$q=16\\times 10^{-6}$ C $=16\ \mu$ C',dot_scale_factor=0).scale(0.7).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        self.play(Write(sol_label))
        self.next_slide()
        self.play(Write(sol[0]))
        self.next_slide()
        self.play(Write(sol[1]))
        self.next_slide()
        self.play(Write(sol[2]))
        self.next_slide()
        self.play(Write(sol[3]))
        self.next_slide()
        self.play(Write(sol[4]))
        self.next_slide(loop=True)
        self.play(Circumscribe(op.submobjects[0]))


class Ex5(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 5: A conductor has $14.4\\times 10^{-19}$ C positive charge. The conductor has }',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        op = VGroup(Tex('(a) 9 electron in excess').scale(0.7),Tex('(b) 27 electrons in short').scale(0.7),Tex('(c) 27 electrons in excess').scale(0.7),Tex('(d) 9 electrons in short').scale(0.7) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(op))
        sol_label =Tex('Solution :', color=ORANGE).next_to(op,DOWN).to_edge(LEFT).scale(0.8)
        sol = BulletedList('Given: Charge on conductor $q = 14.4\\times 10^{-19}$ C', 'Find: No. of electrons short or excess $n = ?$','Using $q= ne$  Or $n =\dfrac{q}{e}$','$n=\dfrac{14.4\\times 10^{-19}\ C}{1.6\\times 10^{-19}\ C} = \dfrac{14.4}{1.6}$','$n=9$',dot_scale_factor=0).scale(0.7).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        self.play(Write(sol_label))
        self.next_slide()
        self.play(Write(sol[0]))
        self.next_slide()
        self.play(Write(sol[1]))
        self.next_slide()
        self.play(Write(sol[2]))
        self.next_slide()
        self.play(Write(sol[3]))
        self.next_slide()
        self.play(Write(sol[4]))
        self.next_slide(loop=True)
        self.play(Circumscribe(op.submobjects[3]))

class Ex6(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 6:  If $10^9$ electrons move out of a body to another body every second, how much time is required to get a total charge of 1 C on the other body?}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
    
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        sol = BulletedList('Given: Number of elctrons moved out in 1 s $= 10^9$ ', '$\\therefore$ Charge moved out in 1 s $=ne = 10^9\\times 1.6 \\times 10^{-19} = 1.6\\times 10^{-10}$  C' ,'Time required to get a charge of $1.6 \\times 10^{-10}$ C $= 1$ s','So, time required to get a charge of 1 C $= \\dfrac{1}{1.6\\times 10^{-10}}$ s $= 6.25\\times 10^{9}$ s','Converting this time in s to years we get $t = \dfrac{6.25\\times 10^9}{365\\times 24 \\times 3600} =198.186$ years',dot_scale_factor=0).scale(0.7).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        self.play(Write(sol_label))
        self.next_slide()
        self.play(Write(sol[0]))
        self.next_slide()
        self.play(Write(sol[1]))
        self.next_slide()
        self.play(Write(sol[2]))
        self.next_slide()
        self.play(Write(sol[3]))
        self.next_slide()
        self.play(Write(sol[4]))

class Ex7(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 7: How much positive and negative charge is there in a cup of water (250 g)?. Given molecular mass of water is 18 g.}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
    
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        sol = BulletedList('Given: Mass of a cup of water $M = 250$ g ', 'Molar mass of water $m = 18$ g' ,'Number of water molecules in 1 cup of water$\\\\= \\dfrac{M}{m}\\times N_A = \\dfrac{250}{18}\\times 6.02 \\times 10^{23} =83.64 \\times 10^{23}$','Number of electron or protons in 1 molecule of water = 10','$\\therefore $ Number of electrons or protons in 1 cup of water  $\\\\n=83.64\\times 10^{23}\\times 10 = 83.64\\times 10^{24}$','Now, Amount of positive or negative charge in 1 cup of water $\\\\ q= ne = 83.64\\times 10^{24}\\times 1.6 \\times 10^{-19}$ C  $=133.8 \\times 10^{5}$ C',dot_scale_factor=0).scale(0.7).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        self.play(Write(sol_label))
        self.next_slide()
        self.play(Write(sol[0]))
        self.next_slide()
        self.play(Write(sol[1]))
        self.next_slide()
        self.play(Write(sol[2]))
        self.next_slide()
        self.play(Write(sol[3]))
        self.next_slide()
        self.play(Write(sol[4]))
        self.next_slide()
        self.play(Write(sol[5]))

class Ex8(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 8: A polythene piece rubbed with wool is found to have a negative charge of $3 \\times 10^{-7}$ C.\\\\ (a) Estimate the number of electrons transferred (from which to which?)\\\\ (b) Is there a transfer of mass from wool to polythene?}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
    
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))
        self.play(Write(Tex('Do it yourself !').next_to(sol_label,DOWN).to_edge(LEFT).shift(RIGHT).scale(0.7)))
        self.next_slide()


class Cond(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : ELECTRIC CHARGES AND FILEDS',color=GREEN)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.add(Outline)
        list = BulletedList('Introduction','Electric Charge','Basic properties of electric charges','Conductors and Insulators','Charging by induction','Coulombs Law',
                            'Forces between multiple charges','Superposition Principle').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        list2 = BulletedList('Electric filed','Electric Field Lines','Electric Dipole and Dipole moment','Electric Field due to an electric dipole',
                             'Dipole in a Uniform External Field','Electric Flux',"Gauss's Law","Applications of Gauss's Law").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        self.play(FadeIn(title, Outline,list,list2))
        self.next_slide(loop=True)
        self.play(FocusOn(list[3]))
        self.play(Circumscribe(list[3]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Cond_title = Title('Conductors and Insulators', color=GREEN)
        self.play(ReplacementTransform(title,Cond_title))
        self.next_slide()
        conductors_lbl = Tex('Conductors :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.play(Write(conductors_lbl))
        list3 = BulletedList('Those substances which allow electricity to pass through them easily are called conductors.','In conductors outermost electron are loosely bound to the atoms nucleus that are comparatively free to move inside the material.','Examples: Metals, humans and earth','When some charge is transferred to a conductor, it readily gets distributed over the entire surface of the conductor. ').scale(0.7).next_to(conductors_lbl,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        self.next_slide()
        self.play(Write(list3[0]))
        self.next_slide()
        self.play(Write(list3[1]))
        self.next_slide()
        self.play(Write(list3[2]))
        self.next_slide()
        self.play(Write(list3[3]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list3))
        Insul_lbl = Tex('Insulators :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.play(ReplacementTransform(conductors_lbl,Insul_lbl))
        self.next_slide()
        list4 = BulletedList('Insulators, in contrast, are made from materials that have bounded electrons(they are not free and it is hard to dislodge these elctrons from the atoms)' ,'In insulators charge flows only with great difficulty, if at all.','If some charge is put on an insulator, it stays at the same place.','Examples: Most of the non-metals like glass, porcelain, plastic, nylon, wood offer high resistance to the passage of electricity through them.').scale(0.7).next_to(Insul_lbl,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        self.next_slide()
        self.play(Write(list4[0]))
        self.next_slide()
        self.play(Write(list4[1]))
        self.next_slide()
        self.play(Write(list4[2]))
        self.next_slide()
        self.play(Write(list4[3]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list4))
        Eart_lbl = Tex('Earthing Or Grounding :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.play(ReplacementTransform(Insul_lbl,Eart_lbl))
        self.next_slide()
        list5 = BulletedList('When we bring a charged body in contact with the earth, all the excess charge on the body disappears by causing a momentary current to pass to the ground through the connecting conductor (such as our body)', 'This process of sharing the charges with the earth is called grounding or earthing. ' ).scale(0.7).next_to(Eart_lbl,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        self.next_slide()
        self.play(Write(list5[0]))
        self.next_slide()
        self.play(Write(list5[1]))


class Induc(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : ELECTRIC CHARGES AND FILEDS',color=GREEN)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.add(Outline)
        list = BulletedList('Introduction','Electric Charge','Basic properties of electric charges','Conductors and Insulators','Charging by induction','Coulombs Law',
                            'Forces between multiple charges','Superposition Principle').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        list2 = BulletedList('Electric filed','Electric Field Lines','Electric Dipole and Dipole moment','Electric Field due to an electric dipole',
                             'Dipole in a Uniform External Field','Electric Flux',"Gauss's Law","Applications of Gauss's Law").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        self.play(FadeIn(title, Outline,list,list2))
        self.next_slide(loop=True)
        self.play(FocusOn(list[4]))
        self.play(Circumscribe(list[4]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Cond_title = Title('Charging by Induction', color=GREEN)
        self.play(ReplacementTransform(title,Cond_title))
        self.next_slide()
        Ind_lbl = Tex('Electrostatic Induction :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        img = ImageMobject('ind.png').scale(0.25)
        self.play(Write(Ind_lbl))
        list3 =  LatexItems( r"\item When an electrically charged object is brought   close to the conductor, the charge on the insulator exerts an electric force on the free electrons of the conductor.", 
                            r"\item Since the rod is positively charged, the free electrons  are attracted, flowing toward the rod to the near side of the conductor",  
                            r"\item Now, the conductor is still overall electrically neutral. However, the conductor now has a charge distribution; the near end now has more negative charge than positive charge,",
                            r"\item The result is the formation of what is called an electric dipole.",
                            itemize="itemize" ,page_width="30em").scale(0.7)
        self.next_slide()
        Group(list3,img).arrange(RIGHT).next_to(Ind_lbl,DOWN).shift(RIGHT).to_corner(LEFT)
        self.play(FadeIn(img))
        for item in list3:
            self.play(Write(item))
            self.next_slide()
        self.play(FadeOut(list3,img))
        self.next_slide()
        img2 = ImageMobject('paper.png').scale(0.5)
        list4 =  LatexItems( r"\item Neutral objects can be attracted to any charged object.", 
                            r"\item If you run a plastic comb through your hair, the charged comb can pick up neutral pieces of paper.",  
                            r"\item When a charged comb is brought near a neutral insulator(paper), the distribution of charge in atoms and molecules is shifted slightly.",
                            r"\item Opposite charge is attracted nearer the external charged rod, while like charge is repelled. Since the electrostatic force decreases with distance, the repulsion of like charges is weaker than the attraction of unlike charges, and so there is a net attraction.",
                            itemize="itemize" ,page_width="30em").scale(0.7)
        self.next_slide()
        Group(list4,img2).arrange(RIGHT).next_to(Ind_lbl,DOWN).shift(RIGHT).to_corner(LEFT)
        self.play(FadeIn(img2))
        for item in list4:
            self.play(Write(item))
            self.next_slide()
        

        self.play(FadeOut(list4,img2))
        Cond1_title = Tex('Charging by induction (1st Method)',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.play(ReplacementTransform(Ind_lbl,Cond1_title))
        self.next_slide()
        list5 =  BulletedList( "The process of charging  neutral body by bringing a charged object nearby it without making contact between the two bodies is known as charging by induction ").scale(0.7).next_to(Ind_lbl,DOWN).shift(RIGHT).to_corner(LEFT)
        g1 = Group(ImageMobject('ind1.png'),ImageMobject('ind2.png'),ImageMobject('ind3.png'),ImageMobject('ind4.png')).arrange_in_grid(2,2).next_to(list5,DOWN).scale(0.75)
        self.next_slide()
        self.play(Write(list5))
        for item in g1:
            self.play(FadeIn(item))
            self.next_slide()
        
        self.play(FadeOut(list5,g1))
        Cond2_title = Tex('Charging by induction (2nd Method)',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.play(ReplacementTransform(Cond1_title,Cond2_title))
        self.next_slide()
        g2 = Group(ImageMobject('in1.png'),ImageMobject('in2.png'),ImageMobject('in3.png'),ImageMobject('in4.png')).arrange_in_grid(2,2).next_to(Cond2_title,DOWN).to_corner(LEFT).scale(0.85)
        self.next_slide()
        for item in g2:
            self.play(FadeIn(item))
            self.next_slide()


class Coulm(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : ELECTRIC CHARGES AND FILEDS',color=GREEN)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.add(Outline)
        list = BulletedList('Introduction','Electric Charge','Basic properties of electric charges','Conductors and Insulators','Charging by induction','Coulombs Law',
                            'Forces between multiple charges','Superposition Principle').scale(0.7).next_to(Outline,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        list2 = BulletedList('Electric filed','Electric Field Lines','Electric Dipole and Dipole moment','Electric Field due to an electric dipole',
                             'Dipole in a Uniform External Field','Electric Flux',"Gauss's Law","Applications of Gauss's Law").scale(0.7).next_to(Outline,DOWN).to_corner(RIGHT)
        self.play(FadeIn(title, Outline,list,list2))
        self.next_slide(loop=True)
        self.play(FocusOn(list[5]))
        self.play(Circumscribe(list[5]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Coulm_title = Title("Coulomb's Law", color=GREEN)
        self.play(ReplacementTransform(title,Coulm_title))
        self.next_slide()
        q1=Dot(color=YELLOW).shift(0.9*LEFT)
        q1_text=Tex('$q_1$').next_to(q1,DOWN,buff=0).scale(0.5)
        q2=Dot(color=ORANGE).shift(1.5*RIGHT)
        q2_text=Tex('$q_2$').next_to(q2,DOWN,buff=0).scale(0.5)
        arrow = DoubleArrow(q1.get_center(),q2.get_center(), tip_length=0.2, color=YELLOW,buff=0).shift(0.7*DOWN)
        arrow_text=Tex('$r$').next_to(arrow,UP,buff=0).scale(0.5)
        f1_arrow = Arrow(start=q1.get_right(),end=q1.get_right()+[0.8,0,0],buff=0,color=GREEN_D) 
        f1_tex=Tex('$F_1$').next_to(f1_arrow,UP,buff=0).scale(0.5)
        f2_arrow = Arrow(start=q2.get_left(),end=q2.get_left()-[0.8,0,0],buff=0,color=ORANGE)
        f2_tex=Tex('$F_2$').next_to(f2_arrow,UP,buff=0).scale(0.5)
        g1 = VGroup(q1,q2,q1_text,q2_text,arrow,arrow_text,f1_arrow, f1_tex,f2_tex,f2_arrow)
        list3 =  LatexItems( r"\item Coulomb's law is a quantitative statement about the force between two point charges.", 
                            r"\item Coulomb measured the force between two point charges and found that it varied inversely as the square of the distance between the charges and was directly proportional to the product of the magnitude of the two charges and acted along the line joining the two charges. ",
                            r"\item Mathematically, magnitude of electrostatic force $(F)$  between two stationary charges $(q_1,\ q_2)$ seperated by a distance $r$ in vacuum is\\ \[F\propto \dfrac{\left|q_1q_2\right|}{r^2} \qquad \text{Or}\qquad F = k\dfrac{\left|q_1q_2\right|}{r^2}\]",
                            itemize="itemize" ,page_width="30em").scale(0.7)
        self.next_slide()
        Group(list3,g1).arrange(RIGHT,buff=0.3).next_to(Coulm_title,DOWN).shift(RIGHT).to_corner(LEFT)
        self.play(Create(g1))
        self.next_slide()
        for item in list3:
            self.play(Write(item))
            self.next_slide()

        self.play(FadeOut(list3))       
        list4 =  LatexItems( r"\item  \[F\propto \dfrac{\left|q_1q_2\right|}{r^2} \qquad \text{Or}\qquad F = k\dfrac{\left|q_1q_2\right|}{r^2}\]",
                            r"\item Where, $k$ is a proportionality constant.", 
                            r"\item In S.I. unit $k=\dfrac{1}{4\pi\epsilon_0}=9\times 10^9\ Nm^2C^{-2}$",
                            r"\item Where $\epsilon_0 =8.854 \times 10^{-12}\ C^2N^{-1}m^{-2}$ and is called the permittivity of free space (vacuum)",
                            r"\item If $q_1=q_2=1\ C$ and $r = 1 $ m. Then, $F=9\times 10^9\ N$",
                            r"\item That is, 1 C is the charge that when placed at a distance of 1 m from another charge of the same magnitude in vacuum experiences an electrical force of repulsion of magnitude $9 \times 10^9$ N.",
                            itemize="itemize" ,page_width="30em").scale(0.7)
        Group(list4,g1).arrange(RIGHT,buff=0.3).next_to(Coulm_title,DOWN).shift(RIGHT).to_corner(LEFT)
        for item in list4:
            self.play(Write(item))
            self.next_slide()
        

        self.play(FadeOut(list4,g1)) 
        Per_title = Tex('Absoloute and Relative Permittivity (Dielectric constant) of Medium:',color=BLUE).scale(0.8).next_to(Outline,DOWN).to_edge(LEFT).shift(1.5*UP)
        self.play(ReplacementTransform(Coulm_title,Per_title))
        self.next_slide()
        list5 = BulletedList("If the point charges are  kept in some other medium (say water) then coulomb's law gives \[F=\dfrac{1}{4\pi\epsilon}\dfrac{q_1q_2}{r^2}\]",
                             "Where, $\epsilon$ is absolute permitivity of the medium \[\dfrac{F_{vacuum}}{F_{medium}}=\dfrac{\dfrac{1}{4\pi \epsilon_0}\dfrac{q_1q_2}{r^2}}{\dfrac{1}{4\pi \epsilon}\dfrac{q_1q_2}{r^2}}=\dfrac{\epsilon}{\epsilon_0}= \epsilon_r (or K)\]",
                             "Where, $\epsilon_r$ is called relative permittivity of the medium and also known as Dielectric constant(K) of the medium.").scale(0.7).next_to(Per_title,DOWN).to_corner(LEFT).shift(0.5*RIGHT)
        for item in list5:
            self.play(Write(item))
            self.next_slide()
        

class Coulm_Vec(Slide):
    def construct(self):
        Coulm_title = Title("Coulomb's Law in Vector Form", color=GREEN)
        self.play(Write(Coulm_title))
        self.next_slide()
        ax = Axes(x_range=[0,6],y_range=[0, 6],x_length=10,y_length=8)
        q1 = Dot(ax.coords_to_point(2,5),color=RED).scale(2)
        q2 = Dot(ax.coords_to_point(5,5),color=RED).scale(2)
        q1_text=Tex('$q_1$').next_to(q1,UP,buff=0.2).scale(1.5)
        q2_text=Tex('$q_2$').next_to(q2,UP,buff=0.2).scale(1.5)
        vector_1 = Arrow(ax.coords_to_point(0,0),ax.coords_to_point(2,5),buff=0,color=GREEN)
        vector_2 = Arrow(ax.coords_to_point(0,0),ax.coords_to_point(5,5),buff=0,color=BLUE)
        v1_lbl = MathTex('\\vec{r}_1').scale(1.5).move_to(ax.coords_to_point(0.8,3))
        v2_lbl = Tex('$\\vec{r}_{2}$').scale(1.5).move_to(ax.coords_to_point(3.8,3))
        f1_arrow = Arrow(start=q1.get_left(),end=q1.get_left()-[2.5,0,0],buff=0,color=GREEN_D) 
        f2_arrow = Arrow(start=q2.get_right(),end=q2.get_right()+[2.5,0,0],buff=0)
        f1_lbl = Tex('$\\vec{F}_{12}$').scale(1.5).next_to(f1_arrow,UP)
        f2_lbl = Tex('$\\vec{F}_{21}$').scale(1.5).next_to(f2_arrow,UP)
        vector_3 = Arrow(ax.coords_to_point(2,5),ax.coords_to_point(5,5),buff=0,color=YELLOW)
        v3_lbl = MathTex('\\vec{r}_{21 } ').scale(1.5).move_to(ax.coords_to_point(3.5,5.3))
        vector_4 = Arrow(ax.coords_to_point(5,5),ax.coords_to_point(2,5),buff=0,color=RED).shift(UP)
        v4_lbl = MathTex('\\vec{r}_{12 } ').scale(1.5).next_to(vector_4,UP)
        g1 = VGroup(ax,q1,q2,q1_text,q2_text,vector_1,vector_2,v1_lbl,v2_lbl,f1_arrow,f2_arrow,f1_lbl,f2_lbl,vector_3,v3_lbl,vector_4,v4_lbl).scale(0.45).next_to(Coulm_title,DOWN).to_edge(RIGHT)
        list3 =  LatexItems( r"\item $q_1,\ q_2 \rightarrow$ Two point charges",
                            r"\item $\vec{r}_1,\ \vec{r}_2 \rightarrow$ Position vectors of $q_1$ and $q_2$ ",
                            r"\item $\vec{F}_{12}\rightarrow$ Force on $q_1$ due to $q_2$",
                            r"\item $\vec{F}_{21}\rightarrow$ Force on $q_2$ due to $q_1$",
                            r"\item $\vec{r}_{21}= \vec{r}_{2}-\vec{r}_{1}$ (Vector leading from 1 to 2)",
                            r"\item $\vec{r}_{12}= \vec{r}_{1}-\vec{r}_{2}$ (Vector leading from 2 to 1)",
                            r"\item $\vec{r}_{21}=-\vec{r}_{12}$ and $\left|\vec{r}_{21}\right|=\left|\vec{r}_{12}\right|=r$",
                            r"\item To denote the direction from 1 to 2 (or from 2 to 1), we define the unit vectors:  \\$\hat{r}_{21}=\dfrac{\vec{r}_{21}}{\left|\vec{r}_{21}\right|}$ and $\hat{r}_{12}=\dfrac{\vec{r}_{12}}{\left|\vec{r}_{12}\right|}$  ",
                            itemize="itemize" ,page_width="25em").scale(0.7).next_to(Coulm_title,DOWN).to_edge(LEFT)
        self.next_slide()
        Group(list3,g1).arrange(RIGHT,buff=0.15).next_to(Coulm_title,DOWN).shift(RIGHT).to_corner(LEFT)
        self.play(FadeIn(q1,q2),Write(q1_text),Write(q2_text))
        self.next_slide()
        self.play(Write(list3[0]))
        self.next_slide()
        self.play(Create(VGroup(ax,vector_1,vector_2,v1_lbl,v2_lbl)))
        self.play(Write(list3[1]))
        self.next_slide()
        self.play(Create(VGroup(f1_arrow)),Write(f1_lbl))
        self.play(Write(list3[2]))
        self.next_slide()
        self.play(Create(VGroup(f2_arrow)),Write(f2_lbl))
        self.play(Write(list3[3]))
        self.next_slide()
        self.play(Create(VGroup(vector_3,v3_lbl)))
        self.play(Write(list3[4]))
        self.next_slide()
        self.play(Create(VGroup(vector_4,v4_lbl)))
        self.play(Write(list3[5]))
        self.next_slide()
        self.play(Write(list3[6]))
        self.next_slide()
        self.play(Write(list3[7]))
        self.next_slide()
        self.play(g1.animate().scale(0.8))
        list4 =  LatexItems( r"\item $\vec{F}_{21}=\dfrac{1}{4\pi\epsilon_0}\dfrac{q_1q_2}{|r_{21}|^{2}}\ \hat{r}_{21}$",
                            r"\item $\vec{F}_{12}=\dfrac{1}{4\pi\epsilon_0}\dfrac{q_1q_2}{|r_{12}|^{2}}\ \hat{r}_{12}$",
                            r"\item $\vec{F}_{21}=-\vec{F}_{12}$",
                            itemize="itemize" ,page_width="15em").scale(0.7)
        g2 = Group(g1,list4).arrange(DOWN,buff=0.1).next_to(Coulm_title,DOWN).shift(RIGHT).to_corner(LEFT)
        Group(list3.scale(0.9),g2).arrange(RIGHT,buff=0.15).next_to(Coulm_title,DOWN).shift(RIGHT).to_corner(LEFT)
        self.play(Write(list4[0]))
        self.next_slide()
        self.play(Write(list4[1]))
        self.next_slide()
        self.play(Write(list4[2]))
        
class Ex9(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Exercise 1.1: What is the force between two small charged spheres having charges of $2 \\times 10^{-7} $ C and $3 \\times 10^{-7}$ C placed 30 cm apart in air?}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
    
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        sol = BulletedList('Given: $q_1 = 2\\times 10^{-7} $ C and $q_2 = 3\\times 10^{-7}$ C '," $r = 30 $ cm $=30\\times 10^{-2}$ m $=3\\times 10^{-1}$ m","Find : $F = ?$",
                           "Using  Coulomb's Law $F = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q_1q_2}{r^2}$","$F = 9\\times 10^{9} \\times \\dfrac{2\\times 10^{-7} \\times 3\\times 10^{-7}}{\\left(3\\times 10^{-1}\\right)^{2}}= 9\\times 10^{9}\\times \\dfrac{2\\times 10^{-7} \\times 3\\times 10^{-7}}{9\\times 10^{-2}}$","$F = 10^{9} \\times 2\\times 10^{-7}\\times 3\\times 10^{-7}\\times 10^{2}=6\\times 10^{-3} $ N","This force is repulsive, since the spheres have same charges.",dot_scale_factor=0).scale(0.7).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        self.play(Write(sol_label))
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()


class Ex10(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 9: The sum of two point charges is $7 \ \mu$ C. They repel each other with a force with a force of 1 N when kept at 30 cm apart in free space. Calculate the value of each charge.} ',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
    
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        sol = BulletedList("Given F = 1 N  and $q_1 + q_2 = 7\ \mu$ C", "$r = 30\ cm = 3\\times 10^{-1}$ m","Find: $q_1$ and $q_2$",'Let one of the two charges be $x\ \mu$ C.',"$\\therefore$ Other charge will be $(7-x)\ \mu$ C","Using  Coulomb's Law $F = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q_1q_2}{r^2}$",dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        sol2 = BulletedList("$1 N = 9\\times 10^{9}\ Nm^{2}C^{-2} \\times \\dfrac{x \\times 10^{-6}\\times (7-x)\\times 10^{-6}\ C^2}{(3\\times 10^{-1}\ m)^2} $",
                            "$1 N = 9\\times 10^{9}\ Nm^{2}C^{-2} \\times \\dfrac{x \\times 10^{-6}\\times (7-x)\\times 10^{-6}\ C^2}{9\\times 10^{-2}\ m^2} $",
                            "$1 = 10^9\\times x(7-x) \\times 10^{-12}\\times 10^{2}=  x(7-x) \\times 10^{-1}$","$10 = -x^2 + 7x $ Or $x^2-7x +10 = 0$","$(x-2)(x-5)=0$",
                            "$ x = 2$ Or $x= 5$","$\\therefore $ Two point charges are $2\ \mu$ C and $5\ \mu$C.",dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        line = Line(sol2.get_top(),sol2.get_bottom(),color=GREEN).next_to(sol,RIGHT)
        Group(sol,line,sol2).arrange(RIGHT,buff=0.15).next_to(sol_label,DOWN).to_corner(LEFT)
        self.play(Write(sol_label))
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line))

        for item in sol2:
            self.play(Write(item))
            self.next_slide()
            
            


class Ex11(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Exercise 1.2: The electrostatic force on a small sphere of charge $0.4\ \mu$C due to another small sphere of charge $-0.8\ \mu$C in air is 0.2 N. (a) What is the distance between the two spheres? (b) What is the force on the second sphere due to the first?}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
    
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)

        sol = BulletedList('Given: : $q_1 = 0.4\ \mu$C , $q_2 = -0.8\ \mu$C and $F = 0.2$ N',"Find : (a) Distance between two charged sphere $r = ?$",
                           "Using  Coulomb's Law $F = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q_1q_2}{r^2}$","$r^2 = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q_1q_2}{F}$","$r^2 = 9\\times 10^9 \ Nm^2C^{-2} \\times \\dfrac{0.4\\times 10^{-6}\\times 0.8\\times 10^{-6}\ C^2}{0.2\ N}$",
                           dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        sol2 = BulletedList("$r^2 = 9\\times 10^9 \\times 2\\times 0.8\\times 10^{-12}\ m^2$",
                           "$r^2 = 14.4\\times 10^{-3}\ m^2$","$r^2= 144 \\times 10^{-4}$","$r =\sqrt{144 \\times 10^{-2}\ m^2}$","$r=12\\times 10^{-2}\ m$",dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        line = Line(sol.get_top(),sol.get_bottom(),color=RED).next_to(sol,RIGHT)
        Group(sol,line,sol2).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).to_corner(LEFT)
        self.play(Write(sol_label))
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line))

        for item in sol2:
            self.play(Write(item))
            self.next_slide()


class Ex12(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 10: There are two charges $+2 \ \mu$ C and $-3\ \mu$C. The ratio of forces acting on them will be  }',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        op = VGroup(Tex('(a) $2:3$').scale(0.7),Tex('(b) $1:1$ ').scale(0.7),Tex('(c) $3:2$').scale(0.7),Tex('(d) $4:9$').scale(0.7) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(op))
        self.next_slide(loop=True)
        self.play(Circumscribe(op.submobjects[1]))


class Ex13(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 11: What is the minimum electric force between two charged particles 1 m apart in free space?}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
    
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))
        sol = BulletedList('Given: : $r = 1$ m',"Find : (a) Minimum force between two charged particles","Force will be minimum when the charge on both particle is minimum,",
                           " $i.e., \ q_1 =q_2 =e = 1.6\\times 10^{-19}$ C",
                           "Using  Coulomb's Law $F = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q_1q_2}{r^2}$","$F = 9\\times 10^9 \\times \\dfrac{1.6\\times 10^{-19} \\times 1.6\\times  10^{-19}}{1^2}$","$F = 23.04 \\times 10^{-29}$ N",
                           dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()


class Ex14(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 1.4 :Coulomb's law for electrostatic force between two point charges and Newton's law for gravitational force between two stationary point masses, both have inverse-square dependence on the distance between the charges and masses respectively. \\textbf{(a)} Compare the strength of these forces by determining the ratio of their magnitudes (i) for an electron and a proton and (ii) for two protons. (b) Estimate the accelerations of electron and proton due to the electrical force of their mutual attraction when they are $1 \AA (= 10^{-10}$m) apart? ($m_p = 1.67 \\times 10^{-27}$ kg, $m_e = 9.11 \\times 10^{-31}$ kg)}",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
    
        self.play(Write(ex_title))
        self.next_slide()
        self.play(ex_title.animate.scale(0.55).to_edge(UL))
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))

        sol = BulletedList("(a) (i)  for an electron and a proton:","$q_1=q_2 = e$ and $m_1 = m_e,\ m_2=m_p$", 
                           ' $\\dfrac{F_e}{F_g}=\\dfrac{\\dfrac{1}{4\pi\epsilon_0}\\dfrac{e^2}{r^2}}{G\\dfrac{m_em_p}{r^2}}=\\dfrac{1}{4\pi\epsilon_0}\\dfrac{e^2}{G m_em_p}$',
                           "$\\dfrac{F_e}{F_g}= \\dfrac{9\\times 10^{9} \\times 1.6\\times 10^{-19}\\times 1.6 \\times 10^{-19} }{6.67 \\times 10^{-11}\\times 9.11\\times 10^{-31}\\times 1.67\\times  10^{-27}}$","$\\dfrac{F_e}{F_g}=2.27\\times 10^{39}\\approx 10^{39}$",
                           dot_scale_factor=0).scale(0.6).next_to(sol_label,DOWN,buff=0).to_corner(LEFT).shift(RIGHT)
        sol2 = BulletedList(" (a) (ii)  for two protons:","$q_1=q_2 = e$ and $m_1=m_2 =m_p$", 
                           ' $\\dfrac{F_e}{F_g}=\\dfrac{\\dfrac{1}{4\pi\epsilon_0}\\dfrac{e^2}{r^2}}{G\\dfrac{m_pm_p}{r^2}}=\\dfrac{1}{4\pi\epsilon_0}\\dfrac{e^2}{G m_pm_p}$',
                           "$\\dfrac{F_e}{F_g}= \\dfrac{9\\times 10^{9} \\times 1.6\\times 10^{-19}\\times 1.6 \\times 10^{-19} }{6.67 \\times 10^{-11}\\times 1.67\\times 10^{-27}\\times 1.67\\times  10^{-27}}$","$\\dfrac{F_e}{F_g}=1.24\\times 10^{36}\\approx 10^{36}$",dot_scale_factor=0).scale(0.6).next_to(sol_label,DOWN,buff=0).to_corner(LEFT).shift(RIGHT)
        line = Line(sol2.get_top(),sol2.get_bottom(),color=RED).next_to(sol,RIGHT)
        g2=Group(sol,line,sol2).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).to_corner(LEFT)
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line))

        for item in sol2:
            self.play(Write(item))
            self.next_slide()
        
        self.play(FadeOut(g2))
        self.next_slide()
        sol3 = BulletedList("(b) Given :  $q_1=q_2=e$ and $r=10^{-10} $ m", 
                           ' Find: Acceleration of electron $(a_e)$ and \\\\ proton ($a_p$) due to electric force (F)',
                           "$F_e=F_p = \\dfrac{1}{4\pi\epsilon_0}\\dfrac{e\\times e}{r^2}$",
                           "$F_e=F_p=\\dfrac{9\\times 10^{9} \\times 1.6\\times 10^{-19}\\times 1.6 \\times 10^{-19} }{(10^{-10})^2}$",
                           dot_scale_factor=0).scale(0.6).next_to(sol_label,DOWN,buff=0).to_corner(LEFT).shift(RIGHT)
        sol4 = BulletedList(" $F_e=F_p=23.04\\times 10^{-9}$ N", 
                           "Now, using  $F_e=m_ea_e$ acceleration of electron", "$a_e=\\dfrac{F_e}{m_e}=\\dfrac{23.04\\times 10^{-9}}{9.11\\times 10^{-31}}=2.53\\times 10^{22}\ ms^{-2}$ ",
                           "Similarly, acceleration of proton:","$a_p=\\dfrac{F_p}{m_p}=\\dfrac{23.04\\times 10^{-9}}{1.67\\times 10^{-27}}=13.79\\times 10^{18}\ ms^{-2}$",dot_scale_factor=0).scale(0.6).next_to(sol_label,DOWN,buff=0).to_corner(LEFT).shift(RIGHT)
        line2 = Line(sol3.get_top(),sol3.get_bottom(),color=RED).next_to(sol3,RIGHT)
        g2=Group(sol3,line2,sol4).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).to_corner(LEFT)
        self.next_slide()
        for item in sol3:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line2))

        for item in sol4:
            self.play(Write(item))
            self.next_slide()
        

class Ex15(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 1.5 : A charged metallic sphere A is suspended by a nylon thread. Another charged metallic sphere B held by an insulating handle is brought close to A such that the distance between their centres is 10 cm, as shown in Fig. 1.7(a). The resulting repulsion of A is noted (for example, by shining a beam of light and measuring the deflection of its shadow on a screen). Spheres A and B are touched by uncharged spheres C and D respectively, as shown in Fig. 1.7(b). C and D are then removed and B is brought closer to A to a distance of 5.0 cm between their centres, as shown in Fig. 1.7(c). What is the expected repulsion of A on the basis of Coulomb's law? Spheres A and C and spheres B and D have identical sizes. Ignore the sizes of A and B in comparison to the separation between their centres.}",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
    
        self.play(Write(ex_title),run_time=12)
        self.next_slide()
        img1 = ImageMobject("q1a.png").scale(0.55)
        img2 = ImageMobject("q1b.png").scale(0.55)
        img3 = ImageMobject("q1c.png").scale(0.55)
        g1=Group(img1,img2,img3).arrange(DOWN,buff=0.1).next_to(ex_title,RIGHT).to_corner(RIGHT)
        self.play(ex_title.animate.scale(0.55).to_edge(UL))
        self.next_slide()
        self.play(FadeIn(img1))
        self.next_slide()
        self.play(FadeIn(img2))
        self.next_slide()
        self.play(FadeIn(img3))
        self.play(g1.animate().scale(0.55).next_to(ex_title,RIGHT).to_corner(RIGHT))
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN,buff=0.1).to_edge(LEFT).scale(0.6)
        self.play(Write(sol_label))

        sol = BulletedList('Let, $q_1\\rightarrow$ initial charge on A', ' $q_2\\rightarrow$ initial charge on B', ' $r = 10 \ cm\\rightarrow$ initial seperation b/w A and B',
                           '$\\therefore$ Initial Force $F = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q_1q_2}{r^2}$', "Now, $q'_1 = \\dfrac{q_1}{2}\\rightarrow$  charge on A after touching ",
                           dot_scale_factor=0).scale(0.6).next_to(sol_label,DOWN,buff=0).to_corner(LEFT).shift(RIGHT)
        sol2 = BulletedList(" $q'_2 = \\dfrac{q_2}{2}\\rightarrow$  charge on B after touching ", " $r' =\\dfrac{r}{2}= 5 \ cm\\rightarrow$ final seperation b/w A and B",
                            "$\\therefore$ Final Force $F' = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q'_1q'_2}{r'^2}= \\dfrac{1}{4\pi \epsilon_0}\\dfrac{\\dfrac{q_1}{2}\\dfrac{q_2}{2}}{\\left(\\dfrac{r}{2}\\right)^2}=\\dfrac{1}{4\pi \epsilon_0} \\dfrac{\\dfrac{q_1q_2}{4}}{\\dfrac{r^2}{4}}$","$F' = \\dfrac{1}{4\pi \epsilon_0} \\dfrac{q_1q_2}{r^2}=F$",dot_scale_factor=0).scale(0.6).next_to(sol_label,DOWN,buff=0).to_corner(LEFT).shift(RIGHT)
        line = Line(sol2.get_top(),sol2.get_bottom(),color=RED).next_to(sol,RIGHT)
        Group(sol,line,sol2).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).to_corner(LEFT)
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line))

        for item in sol2:
            self.play(Write(item))
            self.next_slide()

class Ex16(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 12 : Two point charges $q_1$ and $q_2$ exert a force $F$ on each other when kept certain distance apart. If the charge on each particle is halved and  the distance between the two particles is doubled, then the new force between the two particles would be }",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8).shift(0.5*UP)

        op = VGroup(Tex('(a) $\\dfrac{F}{2}$').scale(0.7),Tex('(b) $\\dfrac{F}{4}$').scale(0.7),Tex('(c) $\\dfrac{F}{8}$ ').scale(0.7),Tex('(d) $\\dfrac{F}{16}$').scale(0.7) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(op))
        self.next_slide()
        self.play(op.animate().scale(0.8).shift(0.5*UP))
        sol_label =Tex('Solution :', color=ORANGE).next_to(op,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))
        sol = BulletedList('Let, $q_1\\rightarrow$ initial charge ', ' $q_2\\rightarrow$ initial charge', ' $r \\rightarrow$ initial seperation',
                           '$\\therefore$ Initial Force $F = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q_1q_2}{r^2}$', "Now, $q'_1 = \\dfrac{q_1}{2}\\rightarrow$  charge is halved ",
                           dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN,buff=0.1).to_corner(LEFT).shift(RIGHT)
        sol2 = BulletedList(" $q'_2 = \\dfrac{q_2}{2}\\rightarrow$  charge is halved ", " $r' =2r \\rightarrow$ distance is doubled",
                            "$\\therefore$ Final Force $F' = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q'_1q'_2}{r'^2}= \\dfrac{1}{4\pi \epsilon_0}\\dfrac{\\dfrac{q_1}{2}\\dfrac{q_2}{2}}{\\left(2r\\right)^2}=\\dfrac{1}{4\pi \epsilon_0} \\dfrac{\\dfrac{q_1q_2}{4}}{4r^2}$","$F' = \\dfrac{1}{4\pi \epsilon_0} \\dfrac{q_1q_2}{16r^2}=\\dfrac{F}{16}$",dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN,buff=0.1).to_corner(LEFT).shift(RIGHT)
        line = Line(sol2.get_top(),sol2.get_bottom(),color=RED).next_to(sol,RIGHT)
        Group(sol,line,sol2).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).to_corner(LEFT)
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line))

        for item in sol2:
            self.play(Write(item))
            self.next_slide()
        self.next_slide(loop=True)
        self.play(Circumscribe(op.submobjects[3]))

class Ex17(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 13 : Two point charges having equal charges seperated by 1 m distance experience a force of 8 N. What will be the force experienced by them, if they are held in water, at the same distance? (Given, K$_{water}=80$) }",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)

        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))

        sol = BulletedList("Given $F_{air}= 8$ N and Dielectric constant of water $K_{water}=80$" ,"Find : $F_{water}= ?$",'We know that $\\dfrac{F_{air}}{F_{medium}}=K_{medium}$', "Here, K is the dielectric constant of the medium","$\\dfrac{8}{F_{water}}=80$","$ \\implies F_{water}=\\dfrac{8\ N}{80}=0.1$ N",
                           dot_scale_factor=0).scale(0.7).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()


class Ex18(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 14: Two same balls having equal positive charge $q$ C are suspended by two insulating strings of equal lengths. What would be the effect on the force when a plastic sheet is inserted between the two? }',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))
        sol = BulletedList("From Coulomb's law, electrostatic force between the two charged boides in a medium," ,
                           "$F_{medium}=\\dfrac{1}{4\pi\epsilon}\\dfrac{q_1q_2}{r^2}=\\dfrac{1}{4\pi\epsilon_0 K}\\dfrac{q_1q_2}{r^2} \quad (\\because \\dfrac{\epsilon}{\epsilon_0}=K)$"
                           , "Where, K is the dielectric constant of the medium", "For vacuum, $K=1$", "for plastic, $K>1$","$\\therefore$ after insertion of plastic sheet, the force between the two charge balls will reduce.",
                           dot_scale_factor=0).scale(0.7).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()

class Ex19(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Exercise 1.12: (a) Two insulated charged copper spheres A and B have their centres separated by a distance of 50 cm. What is the mutual force of electrostatic repulsion if the charge on each is $6.5 \\times 10^{-7}$ C? The radii of A and B are negligible compared to the distance of separation.\\\\ (b) What is the force of repulsion if each sphere is charged double the above amount, and the distance between them is halved?}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))
        sol = BulletedList("Given: : $q_1 = q_2 =6.5 \\times 10^{-7} $C" ," $r = 50 \ cm=5\\times 10^{-1}\ m$",
                           "Using  Coulomb's Law $F = \\dfrac{1}{4\pi \epsilon_0}\\dfrac{q_1q_2}{r^2}$","$F = 9\\times 10^9 \ Nm^2C^{-2} \\times \\dfrac{6.5\\times 10^{-7}\\times 6.5\\times 10^{-7}\ C^2}{(5\\times 10^{-1}\ m)^2\ }$",
                           dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        sol2 = BulletedList("$F = 9\\times 10^9 \\times \\dfrac{6.5\\times 6.5\\times 10^{-14}}{25\\times 10^{-2}}\ N$",
                           "$F = 15.21 \\times 10^{-3}\ N$","(b) $F' = \dfrac{1}{4\pi\epsilon_0}\\dfrac{2q_1\\times 2q_2}{\\left(\\dfrac{r}{2}\\right)^2}= \dfrac{1}{4\pi\epsilon_0}\\dfrac{4q_1q_2}{\\dfrac{r^2}{4}}$","$F' = 16 F$",dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        line = Line(sol.get_top(),sol.get_bottom(),color=RED).next_to(sol,RIGHT)
        Group(sol,line,sol2).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).to_corner(LEFT)
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line))

        for item in sol2:
            self.play(Write(item))
            self.next_slide()

class Ex20(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Exercise 1.13: Suppose the spheres A and B in Exercise 1.12 have identical sizes. A third sphere of the same size but uncharged is brought in contact with the first, then brought in contact with the second, and finally removed from both. What is the new force of repulsion between A and B?}',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))
        sol = BulletedList("Given : $q_1 = q_2 =q=6.5 \\times 10^{-7} $C" ," $r = 50 \ cm=5\\times 10^{-1}\ m$",
                           "From previous question $F = 15.21 \\times 10^{-3}\ N$","New charge on A  and C after touching both sphere ", " $q'_1=q'_3=\\dfrac{q}{2}$",
                           dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        sol2 = BulletedList("New charge on B after touching sphere C", "$q'_2=\\dfrac{q_2+q'_3}{2}=\\dfrac{q+\\dfrac{q}{2}}{2}=\\dfrac{3q}{4}$","New force between A and B", "$F' = \dfrac{1}{4\pi\epsilon_0}\\dfrac{q'_1\\times q'_2}{r^2}= \dfrac{1}{4\pi\epsilon_0}\\dfrac{\\dfrac{q}{2}\\times \\dfrac{3q}{4}}{r^2}= \\dfrac{3}{8} F$","$F' =\\dfrac{3}{8}\\times 15.21\\times 10^{-3} N=5.7\\times 10^{-3}\ N$",dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN).to_corner(LEFT).shift(RIGHT)
        line = Line(sol2.get_top(),sol2.get_bottom(),color=RED).next_to(sol,RIGHT)
        Group(sol,line,sol2).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).to_corner(LEFT)
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line))

        for item in sol2:
            self.play(Write(item))
            self.next_slide()



class Ex21(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex('\\justifying {Example 15: Five balls marked $a$ to $e$ are suspended using separated threads. Pair $(b,\ c)$ and $(d,\ e)$ show electrostatic repulsion while pairs $(a,\ b),\ (c,\ e)$ and $(a,\ e)$ show electrostatic attraction. The ball marked $a$ must be }',tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        op = VGroup(Tex('(a) Negatively charged').scale(0.7),Tex('(b) positively charged ').scale(0.7),Tex('(c) Uncharged').scale(0.7),Tex('(d) Any of the above is possible').scale(0.7) ).arrange_in_grid(2,2,buff=(4,0.3),col_alignments='ll').next_to(ex_title,DOWN)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(op))
        sol_label =Tex('Solution :', color=ORANGE).next_to(op,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))
        sol = BulletedList('$\\because$  $(b,\ c)$ repell each other they have same charge ', ' $\\because$  $(d,\ e)$ repell each other they have same charge ',
                           '$(\ b,\ c,\ d$ and $e)$ all are charged particles. ', '$\\because$  $(c,\ e)$ attract each other they have opposite charge ',
                           dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN,buff=0.1).to_corner(LEFT).shift(RIGHT)
        sol2 = BulletedList(" But, $e$ and $b$  both  are oppositely\\\\ charged and attracts $a$ ", " This is only possible when $a$ is neutral",
                            "They are attracting due to indction.",dot_scale_factor=0).scale(0.65).next_to(sol_label,DOWN,buff=0.1).to_corner(LEFT).shift(RIGHT)
        line = Line(sol.get_top(),sol.get_bottom(),color=RED).next_to(sol,RIGHT)
        Group(sol,line,sol2).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).to_corner(LEFT)
        self.next_slide()
        for item in sol:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line))

        for item in sol2:
            self.play(Write(item))
            self.next_slide()
        self.next_slide(loop=True)
        self.play(Circumscribe(op.submobjects[2]))


class Ex22(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 16: Plot a graph showing the variation of magnitude of Coulomb's force (F) versus $\\dfrac{1}{r^2}$, where $r$ is the distance between the two charges of each pair of charges $(1\ \mu C,\ 2\ \mu C)$ and $(1\ \mu C,\ -3\ \mu C)$. Interpret the graphs obtained }",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))


class Super(Slide):
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
        self.play(FocusOn(Group(list[6],list[7])))
        self.play(Circumscribe(Group(list[6],list[7])))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        super_title = Title("Forces between multiple charges and Superposition Principle",match_underline_width_to_text=True, color=GREEN)
        self.play(ReplacementTransform(title,super_title))
        self.next_slide()
        Super_lbl = Tex('The superposition principle :',color=BLUE).next_to(title,DOWN,buff=0.5).to_corner(LEFT).scale(0.8)
        self.play(Write(Super_lbl))
        ax = Axes(x_range=[0,6],y_range=[0, 6],x_length=10,y_length=8)
        q1 = Dot(ax.coords_to_point(5,5),color=YELLOW).scale(2.5)
        q2 = Dot(ax.coords_to_point(1,3),color=YELLOW).scale(2.5)
        q3 = Dot(ax.coords_to_point(5,2),color=YELLOW).scale(2.5)
        q1_text=Tex('$q_1$').next_to(q1,DR,buff=0.2).scale(1.5)
        q2_text=Tex('$q_2$').next_to(q2,UP,buff=0.2).scale(1.5)
        q3_text=Tex('$q_3$').next_to(q3,RIGHT,buff=0.2).scale(1.5)
        vector_1 = Arrow(ax.coords_to_point(0,0),ax.coords_to_point(5,5),buff=0,color=BLUE)
        vector_2 = Arrow(ax.coords_to_point(0,0),ax.coords_to_point(1,3),buff=0,color=BLUE)
        vector_3 = Arrow(ax.coords_to_point(0,0),ax.coords_to_point(5,2),buff=0,color=BLUE)
        v1_lbl = MathTex('\\vec{r}_1').scale(1.5).move_to(ax.coords_to_point(3.8,3))
        v2_lbl = Tex('$\\vec{r}_{2}$').scale(1.5).move_to(ax.coords_to_point(0.2,2))
        v3_lbl = Tex('$\\vec{r}_{3}$').scale(1.5).move_to(ax.coords_to_point(3.8,1))
        vector_12 = Arrow(ax.coords_to_point(1,3),ax.coords_to_point(5,5),buff=0,color=RED)
        v12_lbl = MathTex('\\vec{r}_{12 } ').scale(1.5).move_to(ax.coords_to_point(3.5,5.3))
        vector_13 = Arrow(start=ax.coords_to_point(5,2),end=ax.coords_to_point(5,5),buff=0,color=RED)
        v13_lbl = MathTex('\\vec{r}_{13 } ').scale(1.5).next_to(vector_13,RIGHT)
        f12_arrow = Arrow(start=q1.get_center(),end=q1.get_center()+[3,1.5,0],buff=0,color=GREEN_D) 
        f13_arrow = Arrow(start=q1.get_center(),end=q1.get_center()+[0,3,0],buff=0,color=PINK)
        f12_lbl = Tex('$\\vec{F}_{12}$').scale(1.5).move_to(ax.coords_to_point(6,5))
        f13_lbl = Tex('$\\vec{F}_{13}$').scale(1.5).next_to(f13_arrow,LEFT)
        f12_line = DashedLine(start=q1.get_center()+[3,1.5,0],end=q1.get_center()+[3,4.5,0],buff=0,color=PINK)
        f13_line = DashedLine(start=q1.get_center()+[3,4.5,0],end=q1.get_center()+[0,3,0],buff=0,color=GREEN_D)
        f1_arrow = Arrow(start=q1.get_center(),end=q1.get_center()+[3,4.5,0],buff=0,color=YELLOW) 
        f1_lbl = Tex('$\\vec{F}_{1}$').scale(1.5).move_to(ax.coords_to_point(6.2,6.5))
        g1 = VGroup(ax,q1,q2,q3,q1_text,q2_text,q3_text,vector_1,vector_2,v1_lbl,v2_lbl,vector_12,v12_lbl,f12_arrow,f13_arrow,f12_lbl,f13_lbl,vector_3,v3_lbl,vector_13,v13_lbl,f12_line,f13_line,f1_arrow,f1_lbl).scale(0.45).next_to(Super_lbl,DOWN).to_edge(RIGHT)
        

        list3 =  LatexItems( r"\item This pricnciple tells us that if charge $q_1$ is acted upon by several charges $q_2,\ q_3, ......, \ q_n$, then the force on $q_1$ can be found out by calculating separately the force $\vec{F}_{12},\ \vec{F}_{13},\ ...,\ \vec{F}_{1n}$ exerted by $q_2,\ q_3,\ ...,\ q_n$, respenctively on $q_1$, then adding these forces vectorially.",
                            r"\item Their resultant $\vec{F}_1$ is that total force on $q_1$ due to the collection of charges.\[\vec{F}_1=\vec{F}_{12}+\vec{F}_{13}+....\vec{F}_{1n}\]",
                            itemize="itemize" ,page_width="25em").scale(0.7).next_to(Super_lbl,DOWN).to_edge(LEFT)
        self.next_slide()
        g2=Group(list3,g1).arrange(RIGHT,buff=0.15).next_to(Super_lbl,DOWN).shift(RIGHT).to_corner(LEFT)
        for item in list3:
            self.play(Write(item))
            self.next_slide()
        self.play(FadeIn(q1,q2,q3),Write(q1_text),Write(q2_text),Write(q3_text))
        self.next_slide()
        self.play(Create(VGroup(ax,vector_1,vector_2,vector_3,v1_lbl,v3_lbl,v2_lbl)))
        self.next_slide()
        self.play(Create(VGroup(vector_12,v12_lbl)))
        self.next_slide()
        self.play(Create(VGroup(vector_13,v13_lbl)))
        self.next_slide()
        self.play(Create(VGroup(f12_arrow)),Write(f12_lbl))
        self.next_slide()
        self.play(Create(VGroup(f13_arrow)),Write(f13_lbl))
        self.next_slide()
        self.play(Create(VGroup(f1_arrow,f13_line,f12_line)),Write(f1_lbl))
        self.next_slide()
        list3.scale(0.7)
        g1.scale(0.7)
        list4 =  LatexItems( r"\item\[ \vec{F}_1=\dfrac{1}{4\pi\epsilon_0}\dfrac{q_1q_2}{|\vec{r}_{12}|^2} \hat{r}_{12}+\dfrac{1}{4\pi\epsilon_0}\dfrac{q_1q_3}{|\vec{r}_{13}|^2} \hat{r}_{13}+....+\dfrac{1}{4\pi\epsilon_0}\dfrac{q_1q_n}{|\vec{r}_{1n}|^2 }\hat{r}_{1n}\]",r"\item \[\vec{F}_{1}=\dfrac{q_1}{4\pi\epsilon_0}\left[\dfrac{q_2}{|\vec{r}_{12}|^2} \hat{r}_{12} + \dfrac{q_3}{|\vec{r}_{13}|^2} \hat{r}_{13}+....+\dfrac{q_n}{|\vec{r}_{1n}|^2 }\hat{r}_{1n} \right]\]",r"\item\[\vec{F}_1=\dfrac{q_1}{4\pi\epsilon_0}\left[\sum_{i=2}^{n} \dfrac{q_i}{|\vec{r}_{1i}|^2} \hat{r}_{1i}\right]\]",
                            itemize="itemize" ,page_width="30em").scale(0.7).next_to(g2,DOWN).scale(0.8).align_to(g2,LEFT)
        
        self.play(FadeOut(super_title))
        g3 = Group(g1,list4).arrange(DOWN).next_to(list3,RIGHT)
        Group(list3,g3).arrange(RIGHT)
        for item in list4:
            self.play(Write(item))
            self.next_slide()

class Ex23(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 17: Point charges $q_1 = 50\ \mu$ C and $q_2 = -25\ \mu$C are placed 1.0 m apart. What is the force on a third charge $q_3 = 20\ \mu$C placed midway between $q_1$ and $q_2$ ? }",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))
        self.next_slide()
        q1=Dot(color=YELLOW)
        q1_text=Tex('$q_1$').next_to(q1,DOWN,buff=0).scale(0.5)
        q2=Dot(color=ORANGE).shift(4*RIGHT)
        q2_text=Tex('$q_2$').next_to(q2,DOWN,buff=0).scale(0.5)
        q3=Dot(color=RED).shift(2*RIGHT)
        q3_text=Tex('$q_3$').next_to(q3,DOWN,buff=0).scale(0.5)
        arrow = DoubleArrow(q1.get_center(),q2.get_center(), tip_length=0.2, color=YELLOW,buff=0).shift(0.7*DOWN)
        arrow_text=Tex('$1$ m').next_to(arrow,UP,buff=0).scale(0.5)
        f1_arrow = Arrow(start=q3.get_right(),end=q3.get_right()+[0.8,0,0],buff=0,color=GREEN_D) 
        f1_tex=Tex('$\\vec{F}_{31}$').next_to(f1_arrow,UR,buff=0).scale(0.5)
        f2_arrow = Arrow(start=q3.get_right(),end=q3.get_right()+[0.4,0,0],buff=0,color=ORANGE,max_tip_length_to_length_ratio=0.5,max_stroke_width_to_length_ratio=10)
        f2_tex=Tex('$\\vec{F}_{32}$').next_to(f2_arrow,UP,buff=0).scale(0.5)
        g1 = VGroup(q1,q2,q3,q1_text,q2_text,q3_text,arrow,arrow_text,f1_arrow, f1_tex,f2_tex,f2_arrow)
        list3 =  LatexItems( r"\item Given: $q_1=50\ \mu$ C $=50\times 10^{-6}$ C", r"\item $q_2=-25\ \mu$ C $=-25\times 10^{-6}$ C", r"\item  $q_3=20\ \mu$ C $=20\times 10^{-6}$ C", r"\item  $|\vec{r}_{12}|=1$ m", r"\item  $\therefore |\vec{r}_{31}|=|\vec{r}_{32}|=0.5$ m", r"\item Find: Force on charge $q_3$, $F_3=?$",r"\item In the fig. forces $\vec{F}_{31}$ and $\vec{F}_{32}$ are\\ acting in the same direction.",
                            itemize="itemize" ,page_width="20em").scale(0.65)
        
        list4 =  LatexItems( r"\item $\therefore $ The magnitude of $\vec{F}_3$ \[|\vec{F}_3|=|\vec{F}_{31}|+|\vec{F}_{32}|=\dfrac{q_3}{4\pi\epsilon_0}\left[\dfrac{q_1}{|\vec{r}_{31}|^2}+\dfrac{q_2}{|\vec{r}_{32}|^2}\right]\] \[|\vec{F}_3|=9\times 10^{9}\times 20\times 10^{-6}\left[\dfrac{50\times 10^{-6}}{(5\times10^{-1})^2}+\dfrac{25\times 10^{-6}}{(5\times10^{-1})^2}\right]\] \[|\vec{F}_3|=180\times 10^{3}\left[\dfrac{75\times 10^{-6}}{25\times10^{-2}}\right]= 18\times 10^{4}\times 3\times 10^{-4}=54\ N\]",
                            itemize="itemize" ,page_width="25em").scale(0.65)
        self.next_slide
        g2 = Group(g1,list4).arrange(DOWN,buff=0.1).next_to(list3,RIGHT)
        line = Line(g2.get_top(),g2.get_bottom(),color=RED).next_to(list3,RIGHT)
        Group(list3,line,g2).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).shift(RIGHT).to_corner(LEFT)
        self.play(Create(g1))
        self.next_slide()
        for item in list3:
            self.play(Write(item))
            self.next_slide()
        
        self.play(Create(line))
        for item in list4:
            self.play(Write(item))
            self.next_slide()


class Ex24(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 18: Point charges $Q_1 = 2.0\ \mu$C and $Q_2 = 4.0\ \mu$C are located at $\\vec{r}_1=\\left( 4\hat{i}-2\hat{j}+5\hat{k}\\right)$m and  $\\vec{r}_2=\\left( 8\hat{i}+5\hat{j}-9\hat{k}\\right)$m. What is the force of $Q_2$ on $Q_1$ ? }",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        list3 =  LatexItems( r"\item Given: $Q_1=2\ \mu$ C $=2\times 10^{-6}$ C", r"\item $Q_2=45\ \mu$ C $=4\times 10^{-6}$ C", r"\item  $\vec{r}_{1}=\left( 4\hat{i}-2\hat{j}+5\hat{k}\right)$ m ", r"\item  $\vec{r}_2=\left( 8\hat{i}+5\hat{j}-9\hat{k}\right)$m", r"\item Find: Force on charge $Q_1$ \\due to $Q_2$, $\vec{F}_{12}=?$", r"\item $\vec{F}_{12}=\dfrac{1}{4\pi\epsilon_0}\dfrac{Q_1Q_2}{|\vec{r}_{12}|^2}\ \hat{r}_{12}$",
                            itemize="itemize" ,page_width="20em").scale(0.65).next_to(sol_label,DOWN).shift(RIGHT).to_corner(LEFT)
        list4 =  LatexItems(r"\item $\vec{r}_{12}= \vec{r}_1-\vec{r}_2= \left( 4\hat{i}-2\hat{j}+5\hat{k}\right)$ m $-\left( 8\hat{i}+5\hat{j}-9\hat{k}\right)$ m ",r"\item  $\vec{r}_{12}= (-4\ \hat{i} -7\ \hat{j} +14\ \hat{k})$ m", r"\item $|\vec{r}_{12}|=\sqrt{(-4)^2+(-7)^2+(14)^2}=\sqrt{261}$ m ",r"\item $\hat{r}_{12}=\dfrac{\vec{r}_{12}}{|\vec{r}_{12}|}=\dfrac{(-4\ \hat{i} -7\ \hat{j} +14\ \hat{k})}{\sqrt{261}}$",r"\item $\vec{F}_{12}=9\times 10^{9}\times \dfrac{2\times 10^{-6}\times 4\times 10^{-6}}{261}\dfrac{(-4\ \hat{i} -7\ \hat{j} +14\ \hat{k})}{\sqrt{261}}$",r"\item  $\vec{F}_{12}=72\times 10^{-3}\times \dfrac{(-4\ \hat{i} -7\ \hat{j} +14\ \hat{k})}{261\times\sqrt{261}}$",
                            itemize="itemize" ,page_width="30em").scale(0.65)
        line = Line(list4.get_top(),list4.get_bottom(),color=RED).next_to(list3,RIGHT)
        g1 = Group(sol_label,list3).next_to(ex_title,DOWN).to_edge(LEFT)
        Group(g1,line,list4).arrange(RIGHT,buff=0.1).next_to(ex_title,DOWN).shift(RIGHT).to_corner(LEFT)
        self.play(Write(ex_title))
        self.next_slide()
        self.play(Write(sol_label))
        self.next_slide()
        for item in list3:
            self.play(Write(item))
            self.next_slide()
        
        self.play(Create(line))
        for item in list4:
            self.play(Write(item))
            self.next_slide()


class Ex25(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 19: A charge $q_3 = 2.0\ \mu$C is placed at the point P shown below. What is the force on $q_3$? }",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        img = ImageMobject('ex25.png').scale(0.6).next_to(ex_title,DOWN)
        self.play(Write(ex_title))
        self.play(FadeIn(img))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(img,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))
        self.next_slide()
        q1=Dot(color=YELLOW)
        q1_text=Tex('$q_1$').next_to(q1,DOWN,buff=0).scale(0.5)
        q2=Dot(color=ORANGE).shift(2.6*RIGHT)
        q2_text=Tex('$q_2$').next_to(q2,DOWN,buff=0).scale(0.5)
        q3=Dot(color=RED).shift(3.9*RIGHT)
        q3_text=Tex('$q_3$').next_to(q3,DOWN,buff=0).scale(0.5)
        arrow = DoubleArrow(q1.get_center(),q2.get_center(), tip_length=0.2, color=YELLOW,buff=0).shift(0.7*DOWN)
        arrow_text=Tex('2 m').next_to(arrow,UP,buff=0).scale(0.5)
        arrow2 = DoubleArrow(q2.get_center(),q3.get_center(), tip_length=0.2, color=YELLOW,buff=0).shift(0.7*DOWN)
        arrow2_text=Tex('1 m').next_to(arrow2,UP,buff=0).scale(0.5)
        f1_arrow = Arrow(start=q3.get_right(),end=q3.get_right()+[0.4,0,0],buff=0,color=GREEN_D,max_tip_length_to_length_ratio=0.5,max_stroke_width_to_length_ratio=10) 
        f1_tex=Tex('$\\vec{F}_{31}$').next_to(f1_arrow,UR,buff=0).scale(0.5)
        f2_arrow = Arrow(start=q3.get_right(),end=q3.get_right()-[0.8,0,0],buff=0,color=ORANGE)
        f2_tex=Tex('$\\vec{F}_{32}$').next_to(f2_arrow,UP,buff=0).scale(0.5)
        g1 = VGroup(q1,q2,q3,q1_text,q2_text,q3_text,arrow,arrow_text,arrow2,arrow2_text,f1_arrow, f1_tex,f2_tex,f2_arrow)
        list3 =  LatexItems( r"\item Given: $q_1=1\ \mu$ C $=10^{-6}$ C", r"\item $q_2=-3\ \mu$ C $=-3\times 10^{-6}$ C", r"\item  $q_3=2\ \mu$ C $=2\times 10^{-6}$ C", r"\item  $|\vec{r}_{31}|=3$ m,\ $|\vec{r}_{32}|=1$ m", r"\item Find: Force on charge $q_3$, $F_3=?$",r"\item In the fig. forces $\vec{F}_{31}$ and $\vec{F}_{32}$ are\\ acting in the opposite direction.",
                            itemize="itemize" ,page_width="20em").scale(0.65)
        
        list4 =  LatexItems( r"\item $\therefore $ The magnitude of $\vec{F}_3$ \[|\vec{F}_3|=|\vec{F}_{32}|-|\vec{F}_{31}|=\dfrac{q_3}{4\pi\epsilon_0}\left[\dfrac{q_2}{|\vec{r}_{32}|^2}+\dfrac{q_1}{|\vec{r}_{31}|^2}\right]\] \[|\vec{F}_3|=9\times 10^{9}\times 2\times 10^{-6}\left[\dfrac{3\times 10^{-6}}{(1)^2}+\dfrac{ 10^{-6}}{(3)^2}\right]\] \[|\vec{F}_3|=18\times 10^{3}\left[3-\dfrac{1}{9}\right]\times 10^{-6}= 18\times 10^{-3}\times \dfrac{28}{9}\]",r"\item $|\vec{F}_3|=56\times 10^{-3}$ N (Along -ve x-axis)",
                            itemize="itemize" ,page_width="25em").scale(0.65)
        self.next_slide
        g2 = Group(img,g1).arrange(RIGHT,buff=0.1).next_to(ex_title,DOWN)
        line = Line(list4.get_top(),list4.get_bottom(),color=RED).next_to(list3,RIGHT)
        Group(list3,line,list4).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).shift(RIGHT).to_corner(LEFT)
        self.play(Create(g1))
        self.next_slide()
        for item in list3:
            self.play(Write(item))
            self.next_slide()
        
        self.play(Create(line))
        for item in list4:
            self.play(Write(item))
            self.next_slide()



class Ex26(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 20: Two charges $+3\ \mu$C and $+12\ \mu$C are fixed 1 m apart, with the second one to the right. Find the magnitude and direction of the net force on a $-2$ nC charge when placed at the following locations: (a) halfway between the two (b) half a meter to the left of the $+3\ \mu$C charge (c) half a meter above the $+12\ \mu$C charge in a direction perpendicular to the line joining the two fixed charges? }",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        list3 =  LatexItems( r"\item Given: $q_1=+3\ \mu$ C $=3\times 10^{-6}$ C", r"\item $q_2=+12\ \mu$ C $=12\times 10^{-6}$ C", r"\item  $q_3=-2\ $ nC $=-2\times 10^{-9}$ C", r"\item  $|\vec{r}_{12}|=1$ m",r"\item (a) $|\vec{r}_{32}|=|\vec{r}_{31}|=0.5$ m", r"\item $|\vec{F}_{31}|=2.16\times 10^{-4}$ N (to the left)", r"\item $|\vec{F}_{32}|=8.63\times 10^{-4}$ N (to the right)",
                            itemize="itemize" ,page_width="20em").scale(0.65)
        
        list4 =  LatexItems(  r"\item $|\vec{F}_{net}|=6.47\times 10^{-4}$ N (to the right)",r"\item (b) $|\vec{r}_{32}|=1.5$ m , $ |\vec{r}_{31}|=0.5$ m", r"\item $|\vec{F}_{31}|=2.16\times 10^{-4}$ N (to the right)", r"\item $|\vec{F}_{32}|=0.96\times 10^{-4}$ N (to the right)", r"\item $|\vec{F}_{net}|=3.12\times 10^{-4}$ N (to the right)",
                            itemize="itemize" ,page_width="25em").scale(0.65)
        line = Line(list4.get_top(),list4.get_bottom(),color=RED).next_to(list3,RIGHT)
        g1 = Group(sol_label,list3).arrange(DOWN,buff=0.1).next_to(ex_title,DOWN).to_edge(LEFT)
        Group(g1,line,list4).arrange(RIGHT,buff=0.1).next_to(ex_title,DOWN).shift(RIGHT).to_corner(LEFT)
        self.play(Write(sol_label))
        self.next_slide()
        for item in list3:
            self.play(Write(item))
            self.next_slide()
        
        self.play(Create(line))
        for item in list4:
            self.play(Write(item))
            self.next_slide()

        self.next_slide()
        self.play(ReplacementTransform(list3,list4))

        list5 =  LatexItems(r"\item  (c) $\vec{F}_{31}=-3.86\times 10^{-5}\ \hat{i}-0.193\times 10^{-5}\ \hat{j}$ N ", r"\item  $\vec{F}_{31}=-8.63\times 10^{-5}\ \hat{j}$ N ", r"\item  $\vec{F}_{net}=-3.86\times 10^{-5}\ \hat{i}-8.82\times 10^{-5}\ \hat{j}$ N ",
                            itemize="itemize" ,page_width="25em").scale(0.65)
        
        g2 = Group(sol_label,list4).arrange(DOWN,buff=0.1).next_to(ex_title,DOWN).to_edge(LEFT)
        Group(g2,line,list5).arrange(RIGHT,buff=0.1).next_to(ex_title,DOWN).shift(RIGHT).to_corner(LEFT)
        for item in list5:
            self.play(Write(item))
            self.next_slide()
        

class Ex27(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 21: The charges $q_1 = 2.0 \\times 10^{-7}$ C, $q_2 = -4.0 \\times 10^{-7}$ C, and $q_3 = -1.0 \\times 10^{-7}$ C are placed at the corners of the triangle shown below. What is the force on $q_1$ ? }",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        img = ImageMobject('ex27.png').scale(0.5).next_to(ex_title,DR).to_edge(RIGHT)
        self.play(Write(ex_title))
        self.play(FadeIn(img))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        list3 =  LatexItems( r"\item  Let us cosinder the origin at $q_3$", r"\item Position Vector of $q_1, q_2,$ and $q_3$ \\ $\vec{r}_1 = 0\ \hat{i} + 3\ \hat{j}$ \\ $\vec{r}_2 = 4\ \hat{i} + 0\ \hat{j}$ \\ $\vec{r}_3 = 0\ \hat{i} + 0\ \hat{j}$",r"\item $\vec{r}_{12}=\vec{r}_{1}-\vec{r}_2 = -4\ \hat{i} + 3\ \hat{j}$",r"\item $\vec{r}_{13}=\vec{r}_{1}-\vec{r}_3 = 0\ \hat{i} + 3\ \hat{j}$",r"\item $|\vec{r}_{12}|=\sqrt{(-4)^2+3^2}=\sqrt{25}=5$",r"\item $|\vec{r}_{13}|=\sqrt{(0)^2+3^2}=\sqrt{9}=3$",
                            itemize="itemize" ,page_width="20em").scale(0.65).next_to(sol_label,DOWN).shift(RIGHT).to_corner(LEFT)
        list4 =  LatexItems(r"\item $\hat{r}_{12}=\dfrac{\vec{r}_{12}}{|\vec{r}_{12}|}=\dfrac{-4\ \hat{i} + 3\ \hat{j}}{5}$",
                            r"\item $\hat{r}_{13}=\dfrac{\vec{r}_{13}}{|\vec{r}_{13}|}=\dfrac{0\ \hat{i} + 3\ \hat{j}}{3}$\\ \\ $\hat{r}_{13}=\hat{j}$",r"\item $\vec{F}_{1}=\vec{F}_{12}+\vec{F}_{13}=\dfrac{q_1}{4\pi\epsilon_0}\left[\dfrac{q_2}{|\vec{r}_{12}|^2}\ \hat{r}_{12}+\dfrac{q_3}{|\vec{r}_{13}|^2}\ \hat{r}_{13}\right]$",
                            itemize="itemize" ,page_width="30em").scale(0.65)
        line = Line(list4.get_top(),list4.get_bottom(),color=RED).next_to(list3,RIGHT)
        g1 = Group(sol_label,list3).next_to(ex_title,DOWN).to_edge(LEFT)
        Group(g1,line,list4).arrange(RIGHT,buff=0.1).next_to(ex_title,DOWN).shift(RIGHT).to_corner(LEFT)
        self.next_slide()
        self.play(Write(sol_label))
        self.next_slide()
        for item in list3:
            self.play(Write(item))
            self.next_slide()
        
        self.play(Create(line))
        for item in list4:
            self.play(Write(item))
            self.next_slide()

class Ex28(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 22: Two fixed charges $+4q$ and $+1q$ are at a distance 3 m apart. At what point between the charges, a third charge $+q$ must be placed to keep it in equilibrium? }",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label))         


class Ex29(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 23: Four charges $Q,\ q,\ Q,$ and $q$ are kept at the four corners of a square as shown below. What is the relation between $Q$ and $q$ so that the net force on a charge $q$ is zero. }",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label)) 
        self.next_slide()
        sq= Square(2,color=RED)
        q1=Dot(color=BLUE).move_to(sq.get_corner(UL))
        q1_text=Tex('$Q$').next_to(q1,UP,buff=0).scale(0.7)
        q2=Dot(color=GREEN).move_to(sq.get_corner(UR))
        q2_text=Tex('$q$').next_to(q2,UP,buff=0).scale(0.7)
        q3=Dot(color=BLUE).move_to(sq.get_corner(DR))
        q3_text=Tex('$Q$').next_to(q3,DOWN,buff=0).scale(0.7)
        q4=Dot(color=GREEN).move_to(sq.get_corner(DL))
        q4_text=Tex('$q$').next_to(q4,DOWN,buff=0).scale(0.7)
        arrow = DoubleArrow(q1.get_center(),q4.get_center(), tip_length=0.2, color=YELLOW,buff=0).shift(0.7*LEFT)
        arrow_text=Tex('a').next_to(arrow,LEFT,buff=0).scale(0.7)
        dia = Line(q4.get_center(),q2.get_center(),color=RED)
        f1_arrow = Arrow(start=q2.get_center(),end=q2.get_center()+[0.8,0,0],buff=0,color=GREEN_D) 
        f1_tex=Tex('$\\vec{F}_{21}$').next_to(f1_arrow,RIGHT,buff=0).scale(0.5)
        f2_arrow = Arrow(start=q2.get_center(),end=q2.get_center()+[0,0.8,0],buff=0,color=GREEN_D) 
        f2_tex=Tex('$\\vec{F}_{23}$').next_to(f2_arrow,UP,buff=0).scale(0.5)
        f3_arrow = Arrow(start=q2.get_center(),end=q2.get_center()+[0.6,0.6,0],buff=0,color=YELLOW) 
        f3_tex=Tex('$\\vec{F}_{24}$').next_to(f3_arrow,RIGHT,buff=0).scale(0.5)

        f11_arrow = Arrow(start=q2.get_center(),end=q2.get_center()-[0.8,0,0],buff=0,color=GREEN_D) 
        f11_tex=Tex('$\\vec{F}_{21}$').next_to(f11_arrow,LEFT,buff=0).scale(0.5)
        f22_arrow = Arrow(start=q2.get_center(),end=q2.get_center()-[0,0.8,0],buff=0,color=GREEN_D) 
        f22_tex=Tex('$\\vec{F}_{23}$').next_to(f22_arrow,DR,buff=0).scale(0.5)
        f33_arrow = Arrow(start=q2.get_center(),end=q2.get_center()+[0.6,0.6,0],buff=0,color=YELLOW) 
        f33_tex=Tex('$\\vec{F}_{24}$').next_to(f33_arrow,RIGHT,buff=0).scale(0.5)
        g1 = VGroup(sq,q1,q1_text,q2,q2_text,q3,q3_text,q4,q4_text,arrow,arrow_text,dia,f1_arrow,f1_tex,f1_arrow,f2_tex,f2_arrow,f3_tex,f3_arrow,f11_arrow,f11_tex,f22_arrow,f22_tex,f33_arrow,f33_tex).next_to(ex_title,DOWN).to_edge(RIGHT).shift(0.4*UP)
        self.play(Create(g1[0:12]))
        list3 =  LatexItems( r"\item Case 1: $Q$ and $q$ are of same sign",r"\item This case is not possible since the forces never cancel out each other.",r"\item Case 2: $Q$ and $q$ are of opposite sign",r"\item $\vec{F}_{21}=\dfrac{1}{4\pi\epsilon_0}\dfrac{Qq}{a^2}\ (-\hat{i})$",r"\item $\vec{F}_{23}=\dfrac{1}{4\pi\epsilon_0}\dfrac{Qq}{a^2}\ (-\hat{j})$",r"\item $\vec{F}_{24}=\dfrac{1}{4\pi\epsilon_0}\dfrac{qq}{2a^2}\ \dfrac{(\hat{i}+\hat{j})}{\sqrt{2}}$",
                            itemize="itemize" ,page_width="20em").scale(0.65).next_to(sol_label,DOWN).shift(RIGHT).to_corner(LEFT)
        
        list4 =  LatexItems( r"\item $\vec{F}_{net}=\vec{F}_{21}+\vec{F}_{23}+\vec{F}_{24}$",
                            r"\item $\vec{F}_{net}=\dfrac{q}{4\pi\epsilon_0}\left[-\dfrac{Q}{a^2}\ \hat{i}-\dfrac{Q}{a^2}\ \hat{j}+\dfrac{q}{2a^2}\ \dfrac{(\hat{i}+\hat{j})}{\sqrt{2}}\right]$",
                            r"\item $\vec{F}_{net}=\dfrac{q}{4\pi\epsilon_0\times a^2}\left[-2\sqrt{2}Q\ \hat{i}-2\sqrt{2}Q\ \hat{j}+q\hat{i}+q\hat{j}\right]$",
                            r"\item $0=\dfrac{q}{4\pi\epsilon_0\times a^2}\left[(q-2\sqrt{2}Q)\ \hat{i}+(q-2\sqrt{2}Q)\ \hat{j}\right]\quad (\because \vec{F}_{net}=0)$",
                            r"\item $(q-2\sqrt{2}Q)\ \hat{i}+(q-\sqrt{2}Q)\ \hat{j}$",r"\item $q-2\sqrt{2}Q=0$ OR $q=2\sqrt{2}Q$", r"\item $\therefore$ $Q$ and $q$ must have opposite sign and $q=2\sqrt{2}Q$",
                            itemize="itemize" ,page_width="27em").scale(0.65)
        self.next_slide()
        #g2 = Group(g1,list4).arrange(DOWN).next_to(ex_title,DOWN).to_edge(RIGHT)
        line = Line(list4.get_top(),list4.get_bottom(),color=RED).next_to(list3,RIGHT)
        self.next_slide()
        self.play(Write(list3[0]))
        self.play(Create(g1[12:18]))
        self.next_slide()
        self.play(Write(list3[1]))
        self.play(FadeOut(g1[12:18]))
        self.next_slide()
        self.play(Write(list3[2]))
        self.play(Create(g1[18:25]))
        self.next_slide()
        self.play(Write(list3[3]))
        self.next_slide()
        self.play(Write(list3[4]))
        self.next_slide()
        self.play(FadeOut(ex_title))
        self.play(Group(sol_label,list3).animate.shift(2*UP))
        self.play(Write(list3[5]))
        self.next_slide()
        self.play(FadeOut(g1))
        Group(list3,line,list4).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).shift(RIGHT).to_corner(LEFT)
        
        
        self.play(Create(line))
        
        for item in list4:
            self.play(Write(item))
            self.next_slide()



class Ex30(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("\\justifying {Example 24: Find the force on the charge $q$ kept at the centre of a square of side 'd'. The charges on the four corners of the square are $Q,\ 2Q,\ 3Q,$ and $4Q$ respectively as shown in the figure below:}",tex_template=myBaseTemplate, color=BLUE_C).to_corner(UP).scale(0.8)
        self.play(Write(ex_title))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label)) 
        self.next_slide()
        sq= Square(3,color=RED)
        q1=Dot(color=BLUE).move_to(sq.get_corner(UL))
        q1_text=Tex('$Q$').next_to(q1,UP,buff=0).scale(0.7)
        q2=Dot(color=GREEN).move_to(sq.get_corner(UR))
        q2_text=Tex('$2Q$').next_to(q2,UP,buff=0).scale(0.7)
        q3=Dot(color=BLUE).move_to(sq.get_corner(DR))
        q3_text=Tex('$3Q$').next_to(q3,DOWN,buff=0).scale(0.7)
        q4=Dot(color=GREEN).move_to(sq.get_corner(DL))
        q4_text=Tex('$4Q$').next_to(q4,DOWN,buff=0).scale(0.7)
        q5=Dot(color=YELLOW).move_to(sq.get_center())
        q5_text=Tex('$q$').next_to(q5,DOWN,buff=0).scale(0.7)
        arrow = DoubleArrow(q1.get_center(),q4.get_center(), tip_length=0.2, color=YELLOW,buff=0).shift(0.7*LEFT)
        arrow_text=Tex('d').next_to(arrow,LEFT,buff=0).scale(0.7)
        #dia = Line(q4.get_center(),q2.get_center(),color=RED)
        f1_arrow = Arrow(start=q5.get_center(),end=q5.get_center()+[0.3,-0.3,0],buff=0,tip_length=0.2,max_stroke_width_to_length_ratio=4,max_tip_length_to_length_ratio=1,stroke_width=6,color=GREEN_D) 
        f1_tex=Tex('$\\vec{F}_{51}$').next_to(f1_arrow,DR,buff=0).scale(0.5)
        f2_arrow = Arrow(start=q5.get_center(),end=q5.get_center()+[-0.6,-0.6,0],buff=0,tip_length=0.2,max_stroke_width_to_length_ratio=3,max_tip_length_to_length_ratio=1,stroke_width=6,color=GREEN_D) 
        f2_tex=Tex('$\\vec{F}_{52}$').next_to(f2_arrow,DL,buff=0).scale(0.5)
        f3_arrow = Arrow(start=q5.get_center(),end=q5.get_center()+[-0.9,0.9,0],buff=0,tip_length=0.2,max_stroke_width_to_length_ratio=2,max_tip_length_to_length_ratio=1,stroke_width=6,color=YELLOW) 
        f3_tex=Tex('$\\vec{F}_{53}$').next_to(f3_arrow,UL,buff=0).scale(0.5)
        f4_arrow = Arrow(start=q5.get_center(),end=q5.get_center()+[1.2,1.2,0],buff=0,tip_length=0.2,max_stroke_width_to_length_ratio=1,max_tip_length_to_length_ratio=1,stroke_width=6,color=YELLOW) 
        f4_tex=Tex('$\\vec{F}_{54}$').next_to(f3_arrow,UR,buff=0).scale(0.5)
        g1 = VGroup(sq,q1,q1_text,q2,q2_text,q3,q3_text,q4,q4_text,q5,q5_text,arrow,arrow_text,f1_arrow,f1_tex,f1_arrow,f2_tex,f2_arrow,f3_tex,f3_arrow,f4_arrow,f4_tex).next_to(ex_title,DOWN).to_edge(RIGHT).shift(0.4*UP)
        self.play(Write(g1))

        list3 =  LatexItems( r"\item $|\vec{F}_{51}|=\dfrac{1}{4\pi\epsilon_0}\dfrac{Qq}{r^2}=F$",
                             r"\item $|\vec{F}_{52}|=\dfrac{1}{4\pi\epsilon_0}\dfrac{2Qq}{r^2}=2F$",
                             r"\item $|\vec{F}_{53}|=\dfrac{1}{4\pi\epsilon_0}\dfrac{3Qq}{r^2}=3F$",
                             r"\item $|\vec{F}_{54}|=\dfrac{1}{4\pi\epsilon_0}\dfrac{4Qq}{r^2}=4F$",
                             r"\item We can see, $\vec{F}_{51}$ and $\vec{F}_{53}$ are exactly opposite to each other so its net effect will be $2F$ towards $Q$",
                            itemize="itemize" ,page_width="16em").scale(0.65)
        
        list4 =  LatexItems(  r"\item Also, $\vec{F}_{52}$ and $\vec{F}_{54}$ are exactly opposite to each other so its net effect will be $2F$ towards $2Q$",
                            r"\item So, the resultant force of $2F$ and $2F$ will be (using Pythagoras theorem) $2\sqrt{2} F$  ",
                            r"\item Magnitude of resultant force $=\dfrac{2\sqrt{2}}{4\pi\epsilon_0}\dfrac{Qq}{(d/\sqrt{2})^2}=\dfrac{4\sqrt{2}}{4\pi\epsilon_0}\dfrac{Qq}{d^2}$",
                            itemize="itemize" ,page_width="30em").scale(0.65).next_to(g1,DOWN)
        self.next_slide()
        #g2 = Group(g1,list4).arrange(DOWN).next_to(ex_title,DOWN).to_edge(RIGHT)
        line = Line(list3.get_top(),list3.get_bottom(),color=RED).next_to(list3,RIGHT)
        Group(list3,line,list4).arrange(RIGHT,buff=0.1).next_to(sol_label,DOWN).shift(RIGHT).to_corner(LEFT)
        self.next_slide()

        for item in list3:
            self.play(Write(item))
            self.next_slide()

        self.play(Create(line))
        self.play(g1.animate.scale(0.7).shift(UP))
        self.next_slide()

        for item in list4:
            self.play(Write(item))
            self.next_slide()


class Ex31(Slide):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        ex_title = Tex("Example 1.6:  Consider three charges $q_1,\ q_2,\ q_3$ each equal to $q$ at the vertices of an equilateral triangle of side $l$. What is the force on a charge $Q$ (with the same sign as $q$) placed at the centroid of the triangle, as shown in Fig.? ",tex_environment="{minipage}{10cm}",font_size=35, color=BLUE_C).to_corner(UP)
        img = ImageMobject('Ex31.png').scale(0.6).next_to(ex_title,DR).to_edge(RIGHT)
        self.play(Write(ex_title))
        self.play(FadeIn(img))
        self.next_slide()
        sol_label =Tex('Solution :', color=ORANGE).next_to(ex_title,DOWN).to_edge(LEFT).scale(0.8)
        self.play(Write(sol_label)) 


class Ex32(Slide):
    def construct(self):

        ex_title = Tex("Example 1.7:  Consider the charges $q,\ q,$ and $-q$ placed at the vertices of an equilateral triangle, as shown in Fig. . What is the force on each charge? ",substrings_to_isolate=":",tex_environment="{minipage}{8cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title.set_color_by_tex("Example",GREEN)
        ex_title.set_color_by_tex(":",GREEN)
        img = ImageMobject('Ex32.png').scale_to_fit_width(4).next_to(ex_title,RIGHT,buff=1).align_to(ex_title,UP)
        img_rect= SurroundingRectangle(img)
        self.play(Write(ex_title))
        self.play(FadeIn(img,img_rect))
        self.next_slide()
        sol_label =Tex('Solution :',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 
        list4 =  LatexItems(r"\item[(a)]  Calculation for Force on  $q_1\ (F_1)$",
                            r"\item[] $|\vec{F}_{12}|=|\vec{F}_{13}|=\dfrac{1}{4\pi\epsilon_0}\dfrac{q^2}{l^2}=F$",
                            r"\item[] Magnitude of net force on $q_1$ $(|\vec{F}_{1}|)$ is",
                            r"\item[] $|\vec{F}_{1}|=\sqrt{|\vec{F}_{12}|^2+|\vec{F}_{13}|^2+2|\vec{F}_{12}||\vec{F}_{13}|\cos\theta}$",
                            r"\item[] $|\vec{F}_{1}|=\sqrt{F^2+F^2+2F^2\cos(120)}$",
                            r"\item[] $|\vec{F}_{1}|=\sqrt{2F^2-2F^2\times\dfrac{1}{2}}=\sqrt{2F^2-F^2}$\\$|\vec{F}_{1}|=F$",
                            font_size=35,itemize="itemize" ,page_width="8cm").next_to(sol_label,DOWN).align_to(sol_label,LEFT)
        line = Line([0,sol_label.get_y(UP),0],[0,config.bottom[1],0],color=RED).next_to(list4,RIGHT).align_to(sol_label,UP)
        list5=  LatexItems(r"\item[(b)]  Similarly, Magnitude of net force \\ on $q_2$ $|\vec{F}_{2}|=F$",
                           r"\item[(c)]  Calculation for Force on  $q_3\ (F_3)$",
                            r"\item[] $|\vec{F}_{31}|=|\vec{F}_{32}|=F$",
                            r"\item[] Magnitude of net force on $q_3$ is",
                            r"\item[] $|\vec{F}_{3}|=\sqrt{F^2+F^2+2F^2\cos(60)}$\\ $|\vec{F}_{3}|=\sqrt{3}F$",
                            font_size=35,itemize="itemize" ,page_width="7cm").next_to(line,RIGHT).align_to([0,img_rect.get_y(DOWN),0],UP).shift(0.1*DOWN)
        self.next_slide()
        for item in list4:
            self.play(Write(item))
            self.next_slide()
        self.play(Write(line))
        self.next_slide()
        for item in list5:
            self.play(Write(item))
            self.next_slide()


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
        ef_int_def =  LatexItems(r"\item[]  The intensity of electric field at any point P is defined as the electric force on a unit positive test charge placed at the point P.",
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
        ef_for = AlignTex(r"\vec{E}&=\displaystyle{\lim_{q_0\to 0}\dfrac{\vec{F} }{q_0} }",r"=\displaystyle{\lim_{q_0\to 0}\dfrac{1}{4\pi\epsilon_0}\dfrac{Qq_0}{r^2 \times q_0}}\hat{r}",r"=\dfrac{1}{4\pi\epsilon_0}\dfrac{Q}{r^2 }\hat{r}",page_width="7cm", color=ORANGE).next_to(ef_int_def,DOWN).align_to(ef_int_lbl,LEFT).shift(0.6*RIGHT)
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
                            r"\item[] Force due to electric field in upward direction:",
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
                            r"\item[] Since electric field intensity is zero at P",
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

class Ex39(Slide):
    def construct(self):

        ex_title = Tex(r"Exercise 1.14 :", r"Figure shows tracks of three charged particles in a uniform electrostatic field. Give the signs of the three charges. ", r"Which particle has the highest charge to mass ratio?",tex_environment="{minipage}{8 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        pline = MyLabeledLine(Tex(r"$\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +\ +$",font_size=20),pos=0.1*UP,start=2.5*LEFT,end=2*RIGHT,color=RED)
        nline = MyLabeledLine(Tex(r"$\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -\ -$",font_size=20),pos=0.1*DOWN,start=2.5*LEFT,end=2*RIGHT,color=BLUE).shift(3*DOWN)
        pt = pline.get_left()+1.5*DOWN
        cline1 = ArcBetweenPoints( pt+0.5*UP,pt+1.2*UP+4.5*RIGHT,radius=13,color=GREEN)
        cline2 = ArcBetweenPoints( pt,pt+0.5*UP+4.5*RIGHT,radius=15,color=GREEN)
        cline3 = ArcBetweenPoints( pt+1.5*DOWN+4.5*RIGHT,pt+0.5*DOWN,radius=11,color=GREEN)
        dline1 = DashedLine(start=pt+0.5*UP,end=pt+0.5*UP+4.5*RIGHT,color=GREY_A)
        dline2 = DashedLine(start=pt,end=pt+4.5*RIGHT,color=GREY_A)
        dline3 = DashedLine(start=pt+0.5*DOWN,end=pt+0.5*DOWN+4.5*RIGHT,color=GREY_A)
        q1 = MyLabeledDot(Tex("1",font_size=20,color=BLACK),color=PINK).move_to(cline1.get_start())
        q2 = MyLabeledDot(Tex("2",font_size=20,color=BLACK),color=PINK).move_to(cline2.get_start())
        q3 = MyLabeledDot(Tex("3",font_size=20,color=BLACK),color=PINK).move_to(cline3.get_end())
        v = MyLabeledArrow(Tex(r"$\vec{v}$",font_size=30),start= 0.5*LEFT,end=0.5*RIGHT,pos=0.2*UP,rot=False,color=YELLOW).next_to(q1,0.5*UP)
        img = VGroup(pline,nline,cline1,cline2,cline3,q1,q2,q3,dline1,dline2,dline3,v).next_to(ex_title,RIGHT).align_to(ex_title,UP)

        self.play(Write(ex_title),Write(img))
        self.next_slide()
        self.play(MoveAlongPath(q1,cline1),run_time=4)
        self.next_slide()
        self.play(MoveAlongPath(q2,cline2),run_time=4)
        self.next_slide()
        self.play(MoveAlongPath(q3,cline3.reverse_points()),run_time=4)
        self.next_slide()
        sol_label =Tex('Solution :',font_size=35, color=ORANGE).next_to(ex_title,DOWN).align_to(ex_title,LEFT)
        self.play(Write(sol_label)) 

        sol_1 =  ItemList( Item(r"Particles 1 and 2 have negative charges because they are being deflected towards the positive plate of the electrostatic field."),
                          Item(r"Particle 3 has positive charge because it is being deflected towards the negative plate."),
                          Item(r"Deflection(d) of charged particle in y-direction is"),
                           Item(r"$d = \dfrac{1}{2}\dfrac{qE}{m}\dfrac{l^2}{v^2}$ OR $d\propto \dfrac{q}{m}$", dot=False),
                           Item(r"As the particle 3 suffers maximum deflection in y-direction, so it has highest charge to mass $\dfrac{q}{m}$ ratio."),
                            buff=MED_SMALL_BUFF).next_to(sol_label,DOWN).align_to(ex_title,LEFT)
        self.next_slide()
        for item in sol_1:
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
        
        q3 = MyLabeledDot(Tex("$+$",font_size=35,color=BLACK),color=BLUE).shift(2*LEFT)
        q4 = MyLabeledDot(Tex("$-$",font_size=35,color=BLACK),color=GREEN).shift(3*RIGHT)

        c1 = VGroup()
        c1.add(CurvedRay(q3.get_center(),0.5*RIGHT+1.3*DOWN,radius=2.5*1.2,color=RED),CurvedRay(0.9*RIGHT+1.25*DOWN,q4.get_center(),radius=2.5*1.2,color=RED))
        c1.add(CurvedRay(q4.get_center(),q3.get_center(),radius=2.5*1.2,color=RED,rev=True))
        c1.add(q3,q4)
        c1.next_to(prop5,DOWN)
        cross2 = Cross(VGroup(c1[0],c1[1]),scale_factor=0.4)

        anm = [Write(prop5[0][0].set_color(ORANGE)), Write(VGroup(prop5[0][1],c1)),Write(cross2),FadeOut(prop5,c1,cross2)]

        
        for item in anm:
            self.play(item)
            self.wait()
            self.next_slide()

        prop6= ItemList(Item(r" (6) ", r"Electric field lines do not form close loops.", r" This follows from the conservative nature of electric field.", pw="13 cm"), buff=MED_LARGE_BUFF
                       ).next_to(new_title,DOWN,buff=0.8).to_corner(LEFT,buff=0.1)
        
        q3 = MyLabeledDot(Tex("$+$",font_size=35,color=BLACK),color=BLUE).shift(2*LEFT)
        q4 = MyLabeledDot(Tex("$-$",font_size=35,color=BLACK),color=GREEN).shift(3*RIGHT)

        c1 = VGroup()
        c1.add(CurvedRay(q3.get_center(),q4.get_center(),radius=2.5*1.2,color=RED,rev=True))
        c1.add(CurvedRay(q4.get_center(),q3.get_center(),radius=2.5*1.2,color=RED,rev=True))
        c1.add(q3,q4)
        c1.next_to(prop6,DOWN)
        cross2 = Cross(c1,scale_factor=0.4)

        anm = [Write(prop6[0][0].set_color(ORANGE)), Write(VGroup(prop6[0][1],c1)), Write(prop6[0][2]),Write(cross2),FadeOut(prop6,cross2,c1)]
        
        for item in anm:
            self.play(item)
            self.wait()
            self.next_slide()

        prop7= ItemList(Item(r" (7) ", r"Two field lines can never cross each other. ", r"Because, if they did the electric field at the point of intersection will have two directions, which is not possible." ,pw="13 cm"), buff=MED_LARGE_BUFF
                       ).next_to(new_title,DOWN,buff=0.8).to_corner(LEFT,buff=0.1)
        

        ef3 = CurvedRay(2*LEFT,2*RIGHT+3*UP,radius=9,color=RED)
        ef4 = CurvedRay(2*LEFT+3*UP,4*RIGHT+DOWN,radius=10,color=GREEN)
        tan1=TangentLine(ef3[0],0.42,color=ORANGE,length=2)
        a1 = MyLabeledArrow(Tex(r"$\vec{E}$",font_size=25),start= tan1.get_center(),end=tan1.get_center()+2*tan1.get_unit_vector(),pos=0.2*DOWN,tip_shape=StealthTip,tip_length=0.1)
        tan2=TangentLine(ef4[0],0.38,color=GOLD,length=2)
        a2 = MyLabeledArrow(Tex(r"$\vec{E}$",font_size=25),start= tan2.get_center(),end=tan2.get_center()+2*tan2.get_unit_vector(),pos=0.2*DOWN,tip_shape=StealthTip,tip_length=0.1)
        dot = Dot(a1.get_start(),radius=0.04)


        
        img6 = VGroup(ef3,ef4,dot,a1,a2).next_to(prop7,DOWN)
        cross = Cross(img6,scale_factor=0.3,color=YELLOW)
        nplbl = Tex("Not Possible ",font_size=30, color=YELLOW).next_to(cross,RIGHT)
        anm = [Write(prop7[0][0].set_color(ORANGE)), Write(prop7[0][1]),Write(prop7[0][2]),Write(ef3),Write(VGroup(ef4,dot)),Write(a1),Write(a2),Write(VGroup(cross,nplbl)),FadeOut(prop7,img6,cross,nplbl)]
        
        for item in anm:
            self.play(item)
            self.wait()
            self.next_slide()

        prop8= ItemList(Item(r" (8) ", r"Field lines are always perpendicular at the surface of a conductor ", r"but they never enter inside the conductor because there is no electrostatic field inside the conductor." ,pw="13 cm"), buff=MED_LARGE_BUFF
                       ).next_to(new_title,DOWN,buff=0.8).to_corner(LEFT,buff=0.1)
        
        prop8[0][0].set_color(ORANGE)

        img1 = ImageMobject("cond1.png").scale(0.6).next_to(prop8,DOWN)
        img2 = ImageMobject("cond2.png").scale(0.6).next_to(prop8,DOWN)
        img3 = ImageMobject("cond3.png").scale(0.6).next_to(prop8,DOWN)
        ig  = Group(img1,img2,img3)

        
        
        for i in range(3):
            self.play(Write(prop8[0][i]))
            self.play(FadeIn(ig[i]))
            self.wait()
            self.next_slide()

class Ex40(Slide):
    def construct(self):

        ex_title = Tex(r"Example 29 :", r"Which among the curves shown in Figure cannot possibly represent electrostatic field lines?",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)
        self.play(Write(ex_title)) 


        self.next_slide()
        img = Group(ImageMobject("ex39a.png").next_to(ex_title,DOWN),ImageMobject("ex39b.png").scale(0.9).next_to(ex_title,DOWN),ImageMobject("ex39c.png").next_to(ex_title,DOWN),ImageMobject("ex39d.png").next_to(ex_title,DOWN),ImageMobject("ex39e.png").next_to(ex_title,DOWN))

        for item in img:
            self.play(FadeIn(item))
            self.next_slide()
            self.play(FadeOut(item))


class Dipole(Slide):
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
        self.play(FocusOn(list2[2]))
        self.play(Circumscribe(list2[2]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        cur_title = Title(" Electric Dipole and Dipole moment ",match_underline_width_to_text=True, color=GREEN)
        self.play(ReplacementTransform(title,cur_title))
        self.next_slide()

        steps1 = ItemList(Item(r"Electric Dipole: ",r"An electric dipole is a pair of two equal and opposite point charges $(+q,-q)$ seperated by a very small distance ($2a$)."),
                         Item(r"Practically, it is an atom or molecule in which centre of positive charge does not coincides with the centre of negative charge."),
                         Item(r"Example of polar molecules - HCl, H$_2$O molecules "),
                        buff=MED_LARGE_BUFF).next_to(cur_title,DOWN,buff=0.3).to_corner(LEFT,buff=0.1)
        
        steps1[0][0].set_color(ORANGE)

        q1 = MyLabeledDot(label_in=Tex("$+$",font_size=35,color=BLACK),label_out=Tex("$+q$",font_size=30,color=BLUE),color=BLUE).shift(2*LEFT)
        q2 = MyLabeledDot(label_in=Tex("$-$",font_size=35,color=BLACK),label_out=Tex("$-q$",font_size=30,color=GREEN),color=GREEN).shift(3*RIGHT)
        lin = Line(q1[0].get_right(),q2[0].get_left())
        pt = MyLabeledDot(label_out=Tex("O",font_size=30),point=lin.get_center())
        a1 = CurvedArrow(pt.get_top(),pt.get_top()+RIGHT+UP,tip_length=0.1,color=GOLD)
        a1lbl = Tex("Centre of dipole", font_size=30).move_to(a1.get_tip()).shift(0.2*UP)
        a2 = MyDoubLabArrow(Tex(r"$a$",font_size=30),start= q1[0].get_right(),end=lin.get_center(),tip_length=0.1,opacity=1).shift(0.2*DOWN)
        a3 = MyDoubLabArrow(Tex(r"$a$",font_size=30),start= lin.get_center(),end=q2[0].get_left(),tip_length=0.1,opacity=1).shift(0.2*DOWN)

        fig1 = VGroup(q1,q2,lin,pt,a1,a2,a3,a1lbl).next_to(steps1,RIGHT)
        a4 = MyDoubLabArrow(Tex(r"$2a$",font_size=30),start= q1[0].get_right(),end=q2[0].get_left(),tip_length=0.1,opacity=1).shift(0.2*DOWN)
        phat = MyLabeledArrow(Tex(r"$\hat{p}$",font_size=30),pos=0.2*UP,start=RIGHT,end=ORIGIN).next_to(fig1,UP,buff=0)

        self.play(Write(fig1))
        self.next_slide()
        for item in steps1:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        
        self.play(FadeOut(steps1,a1,a1lbl,pt,a3,a2),Write(a4),Write(phat))
        self.next_slide()

        steps2 = ItemList(Item(r"Dipole Moment $(\vec{p})$ : ",r"The strength of an electric dipole is measured by a \textbf{vector quantity} known as electric dipole moment ($\vec{p}$)"),
                         Item(r"Which is the  product of the charge ($q$) and separation ($2a$) between the charges."),
                         Item(r"$\vec{p} = q\times 2a\ \hat{p} $",dot=False),
                         Item(r"The \textbf{direction} of electric dipole moment is along the axis of the dipole \textbf{pointing from the negative charge to the positve charge} $(\hat{p})$",pw="13 cm"), 
                         Item(r"S.I unit of $\vec{p} :$ C m"),
                         Item(r"Dimensions: $[\vec{p}]=$ [ATL]"),
                        buff=MED_LARGE_BUFF).next_to(cur_title,DOWN,buff=0.3).to_corner(LEFT,buff=0.1)
        
        steps2[0][0].set_color(ORANGE)
        steps2[2][0].set_color(YELLOW)
        for item in steps2:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()
        

class DipoleField(Slide):
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
        self.play(FocusOn(list2[3]))
        self.play(Circumscribe(list2[3]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        cur_title = Title(" Electric Field Due to An Electric Dipole ",match_underline_width_to_text=True, color=GREEN)
        self.play(ReplacementTransform(title,cur_title))
        self.next_slide()
        first_title = Tex(r"(i) ", r"For Points on the Axis : ",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).next_to(cur_title,DOWN).to_corner(LEFT,buff=0.2)
        first_title[0].set_color(GREEN)
        ul = Underline(first_title[1])
        self.play(Write(first_title),Write(ul)) 
        self.next_slide()
        q1 = MyLabeledDot(label_in=Tex("$-$",font_size=35,color=BLACK),label_out=Tex("$-q$",font_size=30,color=BLUE),color=BLUE).shift(2*LEFT)
        q2 = MyLabeledDot(label_in=Tex("$+$",font_size=35,color=BLACK),label_out=Tex("$+q$",font_size=30,color=GREEN),color=GREEN).shift(2*RIGHT)
        lin = Line(q1[0].get_right(),q2[0].get_left())
        pt = MyLabeledDot(label_out=Tex("O",font_size=30),point=lin.get_center(),radius=0.06)
        a1 = MyDoubLabArrow(Tex(r"$2a$",font_size=30),start= q1[0].get_center(),end=q2[0].get_center(),tip_length=0.1,opacity=1,color=GOLD).shift(0.3*UP)
        P = MyLabeledDot(label_out=Tex("P",font_size=30),color=RED_C,radius=0.06).shift(4*RIGHT)
        a3 = MyDoubLabArrow(Tex(r"$a$",font_size=30),start= q1[0].get_center(),end=pt[0].get_center(),tip_length=0.1,opacity=1,color=GOLD).shift(0.2*DOWN)
        a4 = MyDoubLabArrow(Tex(r"$a$",font_size=30),start= pt[0].get_center(),end=q2[0].get_center(),tip_length=0.1,opacity=1,color=GOLD).shift(0.2*DOWN)
        phat = MyLabeledArrow(Tex(r"$\hat{p}$",font_size=30,color=RED),pos=0.2*UP,start=ORIGIN,end=RIGHT,color=RED).next_to(lin,UP).shift(0.3*UP)
        dline =  DashedLine(start=q2[0].get_right(),end=P[0].get_left(),stroke_width=0.8)
        E1 = MyLabeledArrow(label=Tex(r"$\vec{E}_{-q}$",font_size=30),start=P[0].get_left(),end=P[0].get_left()+0.5*LEFT,pos=0.25*UP,color=BLUE,tip_length=0.15)
        E2 = MyLabeledArrow(label=Tex(r"$\vec{E}_{+q}$",font_size=30),start=P[0].get_right(),end=P[0].get_right()+1.2*RIGHT,pos=0.25*UP,color=GREEN,tip_length=0.15)
        a2 = MyDoubLabArrow(Tex(r"$r$",font_size=30),start= pt.get_center(),end=P.get_center(),tip_length=0.1,opacity=1,color=GOLD).shift(0.6*DOWN)
        fig1 = VGroup(q1,q2,lin,pt,a1,a3,a4,phat,dline,P,E1,E2,a2).next_to(first_title,RIGHT).align_to(first_title,UP).to_edge(RIGHT,buff=0.1).shift(0.1*UP)
        rect = SurroundingRectangle(fig1)

        steps1 = ItemList(Item(r"Consider an electric dipole ($-q,+q$) of length $(2a)$.",pw="5 cm"),
                         Item(r"Let, P be a point on the axis ", r"at a\\ distance $r$ from  the centre ($O$) of the dipole. ",pw="7 cm"),
                         Item(r"We have to determine the electric field $(\vec{E}_{ax})$ at point P. ",pw="7 cm"),
                         Item(r"Electric field at P due to $(-q)$",pw="6.5 cm"),
                         Item(r"$\vec{E}_{-q}=\dfrac{1}{4\pi\epsilon_0}\dfrac{q}{(r+a)^2}\ (-\hat{p})$",pw="7 cm",dot=False),
                        buff=MED_LARGE_BUFF).next_to(first_title,DOWN,buff=0.3).to_corner(LEFT,buff=0.1)
        
        line = line = Line([0,steps1[1].get_y(UP),0],[0,config.bottom[1],0],color=RED).next_to(steps1,0.3*RIGHT).align_to(steps1[1],UP)
        
        steps2 = ItemList(Item(r"Electric field at P due to $(+q)$"),
                         Item(r"$\vec{E}_{+q}=\dfrac{1}{4\pi\epsilon_0}\dfrac{q}{(r-a)^2}\ (\hat{p})$",dot=False),
                         Item(r"The resultant field $(\vec{E}_{ax})$ at P will be"),
                         Item(r"$\vec{E}_{ax} = \vec{E}_{+q} + \vec{E}_{-q}$ ",dot=False),
                         Item(r"$\vec{E}_{ax} = \dfrac{q}{4\pi\epsilon_0}\left(\dfrac{1}{(r-a)^2}-\dfrac{1}{(r+a)^2}\right)\ \hat{p}$",dot=False),
                        buff=MED_SMALL_BUFF).next_to(steps1[2],RIGHT).align_to(steps1[1],UP).shift(0.1*DOWN)
        
        steps3 = ItemList(Item(r"$\vec{E}_{ax} = \dfrac{q}{4\pi\epsilon_0}\left(\dfrac{1}{(r-a)^2}-\dfrac{1}{(r+a)^2}\right)\ \hat{p}$",dot=False),
                         Item(r"$\vec{E}_{ax} = \dfrac{q}{4\pi\epsilon_0}\left(\dfrac{(r+a)^2-(r-a)^2}{(r-a)^2\times (r+a)^2}\right)\ \hat{p}$",dot=False),
                         Item(r"$\vec{E}_{ax} = \dfrac{q}{4\pi\epsilon_0}\left(\dfrac{(r^2+a^2+2ar)-(r^2+a^2-2ar)}{(r^2-a^2)^2}\right)\ \hat{p}$",dot=False),
                         Item(r"$\vec{E}_{ax} = \dfrac{q}{4\pi\epsilon_0}\left(\dfrac{r^2+a^2+2ar-r^2-a^2+2ar}{(r^2-a^2)^2}\right)\ \hat{p}$",dot=False),
                         Item(r"$\vec{E}_{ax} = \dfrac{q}{4\pi\epsilon_0}\left(\dfrac{4ar}{(r^2-a^2)^2}\right)\ \hat{p}$ ", r"$ = \dfrac{1}{4\pi\epsilon_0}\left(\dfrac{2\times q\times 2a\times \hat{p} \times r}{(r^2-a^2)^2}\right)$",dot=False,pw="10 cm"),
                        buff=MED_SMALL_BUFF).next_to(first_title,DOWN,buff=0.3).to_corner(LEFT,buff=0.1)
        
        anm = [rect,VGroup(steps1[0], q1,q2,lin,pt,a1,phat), VGroup(steps1[1][0],P,dline),VGroup(steps1[1][1],a2),steps1[2],VGroup(steps1[3],E1),VGroup(steps1[4],a3),
               line,VGroup(steps2[0],E2),VGroup(steps2[1],a4),steps2[2],steps2[3],steps2[4]]

        for item in anm:
            self.play(Write(item))
            self.next_slide()
        
        self.play(FadeOut(steps1,line))
        self.play(FadeOut(steps2),FadeIn(steps3[0]))
        self.next_slide()
        for i in range(1, len(steps3)):
            self.play(Write(steps3[i][0]))
            self.next_slide()

        self.play(Write(steps3[-1][1]))
        self.next_slide()    
        self.play(FadeIn(line.next_to(steps3,0.3*RIGHT).align_to(steps1[1],UP)))

        steps4 = ItemList(Item(r"$(\because \vec{p}=q\times 2a \ \hat{p}) \\ \\ \vec{E}_{ax} = \dfrac{1}{4\pi\epsilon_0}\left(\dfrac{2 \vec{p}\times  r}{(r^2-a^2)^2}\right) $",dot=False),
                          Item(r"For point dipole $(r>>a)$"),
                          Item(r"$(r^2-a^2) \approx r^2$",dot=False),
                          Item(r"$\vec{E}_{ax} = \dfrac{1}{4\pi\epsilon_0}\left(\dfrac{2 \vec{p}}{r^3}\right)$",dot=False),
                        buff=MED_SMALL_BUFF).next_to(steps3,RIGHT).align_to(steps1[1],UP).shift(0.1*DOWN)
        
        for item in steps4:
            self.play(Write(item))
            self.next_slide()

        sr = SurroundingRectangle(steps4[-1],color=RED)
        self.play(Write(sr))
        self.next_slide(0)
        self.play(FadeOut(sr,steps4,fig1,rect,line,steps3))

        second_title = Tex(r"(ii) ", r"For Points on the Equitorial Plane : ",tex_environment="{minipage}{13 cm}",font_size=35, color=BLUE_C).next_to(cur_title,DOWN).to_corner(LEFT,buff=0.2)
        second_title[0].set_color(GREEN)
        second_title = VGroup(second_title,Underline(second_title[1]))
        self.play(ReplacementTransform(VGroup(first_title,ul),second_title)) 
        self.next_slide()

        q1 = MyLabeledDot(label_in=Tex(r"$\mathbf{+}$",font_size=35,color=BLACK),label_out= Tex("$+q$",font_size=35),color=DARK_BROWN)
        q2 = MyLabeledDot(label_in=Tex(r"$\mathbf{-}$",font_size=35,color=BLACK),label_out= Tex("$-q$",font_size=35),color=MAROON).shift(4*RIGHT)
        A = MyLabeledDot(label_out= Tex("$O$",font_size=30),color=BLUE,point=2*RIGHT)
        C = MyLabeledDot(label_out= Tex("$P$",font_size=30),color=BLUE,pos=LEFT,point=2*RIGHT+3.464*UP)
        A1 = MyDoubLabArrow(label=Tex("$a$",font_size=30),start=q1[0].get_right(),end=A[0].get_left(),pos=0.2*DOWN,tip_length=0.1)
        A2 = MyDoubLabArrow(label=Tex("$a$",font_size=30),start=A[0].get_right(),end=q2[0].get_left(),pos=0.2*DOWN,tip_length=0.1)
        C1 = MyDashLabeledLine(label=Tex(r"$\sqrt{r^2+a^2}$",font_size=30),start=q1[0].get_top(),end=C[0].get_bottom(),pos=0.3*LEFT)
        C2 = MyDashLabeledLine(label=Tex(r"$\sqrt{r^2+a^2}$",font_size=30),start=q2[0].get_top(),end=C[0].get_bottom(),pos=0.3*RIGHT)
        dline =  MyDashLabeledLine(label=Tex("$r$",font_size=30),start=A[0].get_top(),end=C[0].get_bottom(),stroke_width=1,rot=False)
        EC1 = MyLabeledArrow(label=Tex(r"$\vec{E}_{+q}$",font_size=30),start=C[0].get_top(),end=C[0].get_top()+1*C1[0].get_unit_vector(),pos=0.4*LEFT,rel_pos=1,tip_length=0.2,color=RED)
        EC2 = MyLabeledArrow(label=Tex(r"$\vec{E}_{-q}$",font_size=30),start=C[0].get_bottom(),end=C[0].get_bottom()-1*C2[0].get_unit_vector(),pos=0.3*LEFT,rel_pos=1,tip_length=0.2,color=GOLD)
        cdline = DashedLine(start=C[0].get_right(),end= C[0].get_right()+RIGHT,stroke_width=1)
        EC = MyLabeledArrow(label=Tex(r"$\vec{E}_{eq}$",font_size=30),start=C[0].get_right(),end=C[0].get_right()+1*RIGHT,pos=0.2*RIGHT,rel_pos=1,tip_length=0.2,color=ORANGE)
        ang = Angle(C2[0],A2[0],color=ORANGE,radius=0.5,quadrant=(1,-1))
        ang2 = Angle(EC2[0],cdline,color=ORANGE,radius=0.5,quadrant=(1,1))
        ang3 = Angle(cdline,EC1[0],color=PINK,radius=0.5,quadrant=(1,1))
        anglbl = Tex(r"$\theta$",font_size=30).next_to(ang,LEFT,buff=0)
        anglbl2 = Tex(r"$\theta$",font_size=30).next_to(ang2,RIGHT,buff=0)
        anglbl3= Tex(r"$\theta$",font_size=30).next_to(ang3,RIGHT,buff=0)
        phat = MyLabeledArrow(Tex(r"$\hat{p}$",font_size=30,color=RED),pos=0.2*UP,start=RIGHT,end=ORIGIN,color=RED).next_to(C,UP).shift(UP)
        
        img2 = VGroup(q1,q2,A,C,A1,A2,C1,C2,dline,EC1,EC2,EC,ang,anglbl,ang2,ang3,cdline,anglbl2,anglbl3,phat).next_to(second_title,RIGHT,buff=0.2).align_to(second_title,UP).to_corner(DR,buff=0.15).shift(2*LEFT)
        c = MyLabeledDot(label_out= Tex("$P$",font_size=30),color=BLUE,pos=LEFT,point=2*RIGHT+3.464*UP)
        ec1 = MyLabeledArrow(label=Tex(r"$\vec{E}_{+q}$",font_size=30),start=c[0].get_top(),end=c[0].get_top()+2*C1[0].get_unit_vector(),pos=0.4*LEFT,rel_pos=1,tip_length=0.2,color=RED)
        ec2 = MyLabeledArrow(label=Tex(r"$\vec{E}_{-q}$",font_size=30),start=c[0].get_bottom(),end=c[0].get_bottom()-2*C2[0].get_unit_vector(),pos=0.3*LEFT,rel_pos=1,tip_length=0.2,color=GOLD)
        cdline2 = DashedLine(start=c[0].get_top(),end= c[0].get_top()+1.5*RIGHT,stroke_width=1.2)
        cdline3 = DashedLine(start=c[0].get_bottom(),end= c[0].get_bottom()+1.5*RIGHT,stroke_width=1.2)
        ec1h = MyLabeledArrow(label=Tex(r"",font_size=30),start=c[0].get_top(),end=cdline2.get_projection(ec1[0].get_end()),pos=0.3*DOWN,rel_pos=1,tip_length=0.2,color=RED)
        ec1v = MyLabeledArrow(label=Tex(r"$|\vec{E}_{+q}| \sin\theta$",font_size=30),start=cdline2.get_projection(ec1[0].get_end()),end=ec1.get_end(),pos=0.2*RIGHT,rel_pos=0.5,tip_length=0.2,color=RED)
        ec2h = MyLabeledArrow(label=Tex(r"",font_size=30),start=c[0].get_bottom(),end=cdline3.get_projection(ec2[0].get_end()),pos=0.3*DOWN,rel_pos=1,tip_length=0.2,color=GOLD)
        ec2v = MyLabeledArrow(label=Tex(r"$|\vec{E}_{-q}| \sin\theta$",font_size=30),start=cdline3.get_projection(ec2[0].get_end()),end=ec2.get_end(),pos=0.2*RIGHT,rel_pos=0.5,tip_length=0.2,color=GOLD)
        ag2 = Angle(ec2[0],cdline3,color=ORANGE,radius=0.4,quadrant=(1,1))
        ag3 = Angle(cdline2,ec1[0],color=PINK,radius=0.4,quadrant=(1,1))
        aglbl2 = Tex(r"$\theta$",font_size=30).next_to(ag2,RIGHT,buff=0)
        aglbl3= Tex(r"$\theta$",font_size=30).next_to(ag3,RIGHT,buff=0)

        sclimg = VGroup(c,ec1,ec2,cdline2,cdline3,ag2,ag3,aglbl2,aglbl3,ec1h,ec1v,ec2h,ec2v).next_to(title,RIGHT).align_to(second_title,UP)
        sr2 = SurroundingRectangle(VGroup(img2,sclimg))

        steps1 = ItemList(Item(r"In this case, the point P is situated at point P on equitorial plane at a distance r from centre of dipole(O).",pw="6.7 cm"),
                         Item(r"The distance of point P from each charge is $(\sqrt{r^2+a^2})$",pw="6.7 cm"),
                         Item(r"We have to determine the electric field $(\vec{E}_{eq})$ at point P. ",pw="6.7 cm"),
                         Item(r"Magnitude of Electric field at P due to $(+q)$ and $(-q)$",pw="6.7 cm"),
                         Item(r"$|\vec{E}_{+q}|=|\vec{E}_{-q}|=\dfrac{1}{4\pi\epsilon_0}\dfrac{q}{(r^2+a^2)}$ ", r" = E",pw="6.7 cm",dot=False),
                        buff=MED_SMALL_BUFF).next_to(first_title,DOWN,buff=0.3).to_corner(LEFT,buff=0.1)
        
        steps2 = ItemList(Item(r"On resolving $\vec{E}_{+q}$ and  $\vec{E}_{-q}$ into two components.",pw="6.7 cm"),
                         Item(r"The components perpndicular to the dipole axis $(|\vec{E}_{+q}| \sin\theta$ and $|\vec{E}_{-q}| \sin\theta)$ cancel each other.",pw="6.7 cm"),
                         Item(r"The components along the dipole axis $(|\vec{E}_{+q}| \cos\theta$ and $|\vec{E}_{-q}| \cos\theta)$, being in the same direction, add up. ",pw="6.7 cm"),
                         Item(r"The total electric field $\vec{E}_{eq}$ is opposite to $\hat{p}$ ",pw="6.7 cm"),
                         Item(r"\vec{E}_{eq}&=\left(|\vec{E}_{+q}|\cos\theta+|\vec{E}_{-q}|\cos\theta\right) (-\hat{p}) \\" ,r" &=-2 E\cos\theta\ \hat{p} ",math=True,pw= "6.7 cm",dot=False),
                        buff=MED_SMALL_BUFF).next_to(first_title,DOWN,buff=0.3).to_corner(LEFT,buff=0.1)

        steps3 = ItemList(Item(r"\vec{E}_{eq}&=\left(|\vec{E}_{+q}|\cos\theta+|\vec{E}_{-q}|\cos\theta\right) (-\hat{p}) \\" ,
                               r" &=-2 E\cos\theta\ \hat{p} \\",
                               r" &= -2\times \dfrac{1}{4\pi\epsilon_0}\dfrac{q}{(r^2+a^2)}\times \dfrac{a}{\sqrt{r^2+a^2}}\ \hat{p} \\",
                               r" &= \dfrac{1}{4\pi\epsilon_0}\dfrac{-2qa\ \hat{p} }{(r^2+a^2)^{3/2}}\\",
                               r" &= \dfrac{1}{4\pi\epsilon_0}\dfrac{-\vec{p} }{(r^2+a^2)^{3/2}}\quad (\because \vec{p}=q\times 2a\ \hat{p})", math=True,pw= "6.7 cm",dot=False),
                            Item(r"For point dipole $(r>>a)  (\therefore r^2+a^2\approx r^2)$",pw= "6.7 cm"),
                            Item(r"$\vec{E}_{eq}= \dfrac{1}{4\pi\epsilon_0}\dfrac{-\vec{p} }{r^3}$",dot=False,pw= "6.7 cm"),
                            buff=MED_SMALL_BUFF).next_to(first_title,DOWN,buff=0.15).to_corner(LEFT,buff=0.1)
        steps4 = ItemList(Item(r"For point dipole Or $r>>a$",color=YELLOW,pw="13 cm"),
                         Item(r"$\vec{E}_{ax}= \dfrac{1}{4\pi\epsilon_0}\dfrac{2\vec{p}}{r^3}$", r" and  $\vec{E}_{eq}= \dfrac{1}{4\pi\epsilon_0}\dfrac{-\vec{p}}{r^3}$",pw="13 cm",dot=False),
                         Item(r"$\vec{E}_{ax}=-2\times\vec{E}_{eq}$ ",color=PINK,pw="13 cm",dot=False),
                         Item(r"Notice the important point that the dipole field at large distances falls off not as $\dfrac{1}{r^2}$ but as $\dfrac{1}{r^3}.$",pw="13 cm"),
                         Item(r"The magnitude and the direction of the dipole field depends not only on the distance $r$ but also on the angle between the position vector $\vec{r}$ and the dipole moment $\vec{p}$.",pw= "13 cm"),
                        buff=MED_SMALL_BUFF).next_to(first_title,DOWN,buff=0.3).to_corner(LEFT,buff=0.1)
        anm = [VGroup(sr2,q1,q2,A1,A2,A),VGroup(steps1[0],C,dline),VGroup(steps1[1],C1,C2,ang,anglbl),steps1[2],VGroup(steps1[3],EC1,EC2),steps1[4][0],steps1[4][1],VGroup(cdline,anglbl2,ang2),VGroup(anglbl3,ang3)]
        for item in anm:
            self.play(Write(item))
            self.next_slide()
        
        self.play(FadeOut(steps1))

        anm2 = [VGroup(c,ec1,ec2,cdline2,cdline3,ag2,aglbl2,ag3,aglbl3),steps2[0],ec1h,ec1v,ec2h,ec2v,steps2[1],steps2[2],VGroup(steps2[3],phat,EC),steps2[4][0],steps2[4][1]]

        for item in anm2:
            self.play(Write(item))
            self.next_slide()

        
        self.play(FadeOut(steps2))
        self.add(steps3[0][0:2])
        self.wait(1)
        self.next_slide()
        for item in steps3[0][2:5]:
            self.play(Write(item))
            self.next_slide()
        
        self.play(Write(steps3[1]))
        self.next_slide()
        sr3 = SurroundingRectangle(steps3[2])
        self.play(Write(steps3[2]),Write(sr3))
        self.play(FadeOut(steps3,img2,sclimg,sr2,sr3,second_title))
        self.wait(2)
        self.next_slide()

        for item in steps4:
            for subitem in item:
                self.play(Write(subitem))
                self.next_slide()

class Ex41(Slide):
    def construct(self):

        ex_title = Tex(r"Example 30 :", r" Two charges $\pm 10 \mu$C are placed 5.0 mm apart. Determine the electric field at ", r" (a) a point P on the axis of the dipole 15 cm away from its centre O on the side of the positive charge, as shown in Fig. ", r" and (b) a point Q, 15 cm away from O on a line passing through O and normal to the axis of the dipole, as shown in Fig.",tex_environment="{minipage}{8 cm}",font_size=35, color=BLUE_C).to_corner(UP,buff=0.2).to_corner(LEFT,buff=0.2)
        ex_title[0].set_color(GREEN)

        for item in ex_title:
            self.play(Write(item))
            self.next_slide()
        


class Try(Slide):
    def construct(self):     
        a1 = ArcBetweenPoints(3*RIGHT,2*LEFT+2*UP,radius=3,arc_center=ORIGIN)
        a2 = ArcBetweenPoints(a1.get_start()+2*DOWN+RIGHT,a1.get_start(),radius=2,arc_center=ORIGIN)
        a3 = ArcBetweenPoints(a1.get_end(),a2.get_start(),radius=4,arc_center=ORIGIN)
        img = VGroup(a1,a3)
        dot = Dot(color=RED)
        g2 = VGroup(dot,img,a2)

        for i in range(0,a2.get_num_points(),4):
            point = a2.get_all_points()[i]
            ray = Ray(start=point,end=1.2*point,color=RED)
            t = TangentLine(a2,4*i/a2.get_num_points(),length=0.3,color=BLUE)
            g2.add(ray,t)


        for point in img.get_all_points():
            ray = Ray(start=point,end=1.2*point,color=RED)
            g2.add(ray)

        self.play(Create(g2))
        self.wait(2)
