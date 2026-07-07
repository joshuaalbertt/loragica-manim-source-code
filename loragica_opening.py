from manim import *
from manim.utils.rate_functions import ease_out_back

class LoragicaLogo(Scene):
    def construct(self):
        COLOR_OFF_WHITE = "#FAFBFC"
        COLOR_NAVY_BLUE = "#1D3557"
        COLOR_SOFT_GREEN = "#2A9D8F"

        self.camera.background_color = COLOR_OFF_WHITE

        sq_size = 1.5
        gap = 0.3
        step = sq_size + gap
        radius = 0.2
        stroke_w = 6

        pos_tl = UP * step/2 + LEFT * step/2
        pos_tr = UP * step/2 + RIGHT * step/2
        pos_bl = DOWN * step/2 + LEFT * step/2
        pos_br = DOWN * step/2 + RIGHT * step/2

        ol_tl = RoundedRectangle(
            width=sq_size, height=sq_size, corner_radius=radius,
            color=COLOR_NAVY_BLUE, stroke_width=stroke_w, fill_opacity=0
        ).move_to(pos_tl)

        ol_br = RoundedRectangle(
            width=sq_size, height=sq_size, corner_radius=radius,
            color=COLOR_NAVY_BLUE, stroke_width=stroke_w, fill_opacity=0
        ).move_to(pos_br)

        ol_tr = RoundedRectangle(
            width=sq_size, height=sq_size, corner_radius=radius,
            color=COLOR_NAVY_BLUE, stroke_width=stroke_w, fill_opacity=0
        ).move_to(pos_tr)

        ol_bl = RoundedRectangle(
            width=sq_size, height=sq_size, corner_radius=radius,
            color=COLOR_NAVY_BLUE, stroke_width=stroke_w, fill_opacity=0
        ).move_to(pos_bl)

        fl_tl = RoundedRectangle(
            width=sq_size, height=sq_size, corner_radius=radius,
            fill_color=COLOR_NAVY_BLUE, fill_opacity=1, stroke_width=0
        ).move_to(pos_tl)

        fl_br = RoundedRectangle(
            width=sq_size, height=sq_size, corner_radius=radius,
            fill_color=COLOR_SOFT_GREEN, fill_opacity=1, stroke_width=0
        ).move_to(pos_br)

        self.play(
            FadeIn(ol_tl, run_time=0.25, rate_func=smooth),
            FadeIn(ol_br, run_time=0.25, rate_func=smooth),
        )
        self.play(
            GrowFromCenter(fl_tl, run_time=0.6, rate_func=ease_out_back),
            GrowFromCenter(fl_br, run_time=0.6, rate_func=ease_out_back),
        )

        self.wait(0.35)

        self.play(
            fl_tl.animate.scale(0.5),
            fl_br.animate.scale(0.5),
            run_time=0.35,
            rate_func=smooth
        )

        self.wait(0.25)

        self.play(
            Create(ol_tr),
            Create(ol_bl),
            run_time=0.8,
            rate_func=smooth
        )

        self.wait(0.1)

        self.play(
            fl_tl.animate.move_to(pos_tr),
            fl_br.animate.move_to(pos_bl),
            run_time=0.7,
            rate_func=smooth
        )

        self.wait(0.05)

        self.play(
            fl_tl.animate.scale(2),
            fl_br.animate.scale(2),
            run_time=0.45,
            rate_func=ease_out_back
        )

        self.wait(1.5)
