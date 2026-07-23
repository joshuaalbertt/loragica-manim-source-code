from manim import *

OFF_WHITE = "#F5F5F3"
BLACK = "#0A0A0A"
DARK_GRAY = "#1C1C1C"
MID_GRAY = "#555555"
LIGHT_GRAY = "#AAAAAA"
GRID_LINE = "#E2E2E2"


class InequalityFlip(Scene):
    def construct(self):
        self.camera.background_color = OFF_WHITE

        dots = VGroup(*[
            Dot(point=[x, y, 0], radius=0.02, color=GRID_LINE)
            for x in np.arange(-7, 7, 0.7)
            for y in np.arange(-4, 4, 0.7)
        ])
        self.add(dots)

        # ============================================================
        # FASE 1: Hook — satu jawaban vs banyak jawaban (0-12s)
        # ============================================================

        # Persamaan: x + 3 = 7
        eq = MathTex("x + 3 = 7", font_size=44, color=BLACK)
        eq.move_to(UP * 2.5)
        self.play(Write(eq), run_time=1.2)
        self.wait(1)

        # Garis bilangan pertama
        nl1 = NumberLine(
            x_range=[-2, 8, 1], length=8, color=LIGHT_GRAY,
            include_numbers=True, font_size=22,
            decimal_number_config={"color": MID_GRAY}
        )
        nl1.move_to(UP * 0.8)

        self.play(Create(nl1), run_time=1)

        # Dot tunggal di x=4
        dot4 = Dot(nl1.n2p(4), radius=0.12, color=BLACK)
        label_dot = MathTex("x=4", font_size=28, color=BLACK)
        label_dot.next_to(dot4, UP, buff=0.25)

        self.play(FadeIn(dot4), Write(label_dot), run_time=1)
        self.wait(2)

        one_ans = Text("1 jawaban", font_size=20, color=MID_GRAY, font="Arial")
        one_ans.next_to(label_dot, RIGHT, buff=0.5)
        self.play(FadeIn(one_ans), run_time=0.6)
        self.wait(3)

        # ============================================================
        # FASE 2: Solve x + 3 < 7 (12-28s)
        # ============================================================
        self.play(
            FadeOut(VGroup(eq, nl1, dot4, label_dot, one_ans)),
            run_time=0.8
        )

        ineq = MathTex("x", "+", "3", "<", "7", font_size=48, color=BLACK)
        ineq.move_to(UP * 2.5)
        self.play(Write(ineq), run_time=1.2)
        self.wait(1.5)

        # Step: kurangi 3
        step1 = MathTex("x", "<", "7", "-", "3", font_size=42, color=BLACK)
        step1.move_to(UP * 1.3)
        self.play(Write(step1), run_time=1)
        self.wait(1)

        result1 = MathTex("x", "<", "4", font_size=48, color=BLACK)
        result1.move_to(UP * 1.3)
        self.play(Transform(step1, result1), run_time=1)
        self.wait(1.5)

        # Garis bilangan — highlight area kiri 4
        nl2 = NumberLine(
            x_range=[-2, 8, 1], length=8, color=LIGHT_GRAY,
            include_numbers=True, font_size=22,
            decimal_number_config={"color": MID_GRAY}
        )
        nl2.move_to(DOWN * 0.8)

        self.play(Create(nl2), run_time=1)

        # Open circle di 4 (tidak termasuk 4)
        open_circle = Circle(radius=0.12, color=BLACK, stroke_width=2.5)
        open_circle.set_fill(OFF_WHITE, opacity=1)
        open_circle.move_to(nl2.n2p(4))

        # Area highlight ke kiri
        area_left = Line(
            nl2.n2p(-2), nl2.n2p(4),
            color=BLACK, stroke_width=6
        )

        self.play(Create(area_left), FadeIn(open_circle), run_time=1.5)
        self.wait(1)

        many_ans = Text("tak terhingga jawaban", font_size=20, color=MID_GRAY, font="Arial")
        many_ans.next_to(nl2, DOWN, buff=0.5)
        self.play(Write(many_ans), run_time=1)
        self.wait(3)

        # ============================================================
        # FASE 3: The flip — -2x < 6 (28-50s)
        # ============================================================
        self.play(
            FadeOut(VGroup(ineq, step1, nl2, open_circle, area_left, many_ans)),
            run_time=0.8
        )

        ineq2 = MathTex("-2x", "<", "6", font_size=48, color=BLACK)
        ineq2.move_to(UP * 2.5)
        self.play(Write(ineq2), run_time=1.2)
        self.wait(2)

        # Step: bagi -2
        step2a = MathTex(
            "{-2x", r"\over", "-2}", "<", "{6", r"\over", "-2}",
            font_size=42, color=BLACK
        )
        step2a.move_to(UP * 1.2)
        self.play(Write(step2a), run_time=1.3)
        self.wait(2)

        # WARNING — tanda harus balik!
        warning = Text(
            "BAGI NEGATIF → TANDA BALIK!",
            font_size=22, color=BLACK, font="Arial", weight=BOLD
        )
        warning.move_to(UP * 0)
        warning_box = SurroundingRectangle(warning, color=BLACK, buff=0.2, stroke_width=2.5)

        self.play(Write(warning), Create(warning_box), run_time=1.2)
        self.wait(3.5)

        # Animasi tanda < berputar jadi >
        sign_lt = MathTex("<", font_size=60, color=BLACK)
        sign_lt.move_to(DOWN * 1.5)
        self.play(FadeIn(sign_lt), run_time=0.5)
        self.wait(0.5)

        sign_gt = MathTex(">", font_size=60, color=BLACK)
        sign_gt.move_to(DOWN * 1.5)
        self.play(
            Rotate(sign_lt, PI, axis=UP),
            run_time=1
        )
        self.play(Transform(sign_lt, sign_gt), run_time=0.5)
        self.wait(1.5)

        self.play(FadeOut(VGroup(sign_lt, warning, warning_box, step2a)), run_time=0.8)

        # Hasil
        result2 = MathTex("x", ">", "-3", font_size=48, color=BLACK)
        result2.move_to(UP * 1.2)
        self.play(Write(result2), run_time=1)
        self.wait(1.5)

        # Garis bilangan — highlight area KANAN -3
        nl3 = NumberLine(
            x_range=[-6, 4, 1], length=8, color=LIGHT_GRAY,
            include_numbers=True, font_size=22,
            decimal_number_config={"color": MID_GRAY}
        )
        nl3.move_to(DOWN * 0.8)

        self.play(Create(nl3), run_time=1)

        # Open circle di -3
        open_circle2 = Circle(radius=0.12, color=BLACK, stroke_width=2.5)
        open_circle2.set_fill(OFF_WHITE, opacity=1)
        open_circle2.move_to(nl3.n2p(-3))

        # Area highlight ke KANAN (arah terbalik dari sebelumnya)
        area_right = Line(
            nl3.n2p(-3), nl3.n2p(4),
            color=BLACK, stroke_width=6
        )

        self.play(Create(area_right), FadeIn(open_circle2), run_time=1.5)
        self.wait(4)

        # ============================================================
        # FASE 4: Closing — ringkasan visual (50-75s)
        # ============================================================
        self.play(
            FadeOut(VGroup(ineq2, result2, nl3, open_circle2, area_right)),
            run_time=0.8
        )

        # Ringkasan dua contoh side by side
        title_l = Text("Biasa", font_size=22, color=MID_GRAY, font="Arial")
        title_l.move_to(LEFT * 3 + UP * 2.8)
        title_r = Text("Bagi negatif", font_size=22, color=BLACK, font="Arial")
        title_r.move_to(RIGHT * 3 + UP * 2.8)

        self.play(Write(title_l), Write(title_r), run_time=1)

        # Kiri: x+3<7 → x<4
        recap_l1 = MathTex("x+3 < 7", font_size=34, color=MID_GRAY)
        recap_l1.move_to(LEFT * 3 + UP * 1.8)
        recap_l2 = MathTex("x < 4", font_size=34, color=MID_GRAY)
        recap_l2.move_to(LEFT * 3 + UP * 1)
        arrow_l = Arrow(
            recap_l1.get_bottom() + DOWN * 0.05, recap_l2.get_top() + UP * 0.05,
            color=MID_GRAY, stroke_width=2, buff=0.05, max_tip_length_to_length_ratio=0.3
        )

        # Kanan: -2x<6 → x>-3
        recap_r1 = MathTex("-2x < 6", font_size=34, color=BLACK)
        recap_r1.move_to(RIGHT * 3 + UP * 1.8)
        recap_r2 = MathTex(r"x > -3", font_size=34, color=BLACK)
        recap_r2.move_to(RIGHT * 3 + UP * 1)
        arrow_r = Arrow(
            recap_r1.get_bottom() + DOWN * 0.05, recap_r2.get_top() + UP * 0.05,
            color=BLACK, stroke_width=2, buff=0.05, max_tip_length_to_length_ratio=0.3
        )

        self.play(Write(recap_l1), Write(recap_r1), run_time=1.2)
        self.wait(1)
        self.play(Create(arrow_l), Write(recap_l2), run_time=1)
        self.play(Create(arrow_r), Write(recap_r2), run_time=1)
        self.wait(1.5)

        # Tanda tetap vs tanda balik
        keep = Text("tanda tetap", font_size=18, color=MID_GRAY, font="Arial")
        keep.next_to(recap_l2, DOWN, buff=0.4)
        flip = Text("tanda BALIK", font_size=18, color=BLACK, font="Arial", weight=BOLD)
        flip.next_to(recap_r2, DOWN, buff=0.4)

        self.play(Write(keep), Write(flip), run_time=1)
        self.wait(2)

        # Garis bilangan mini side by side
        nl_mini_l = NumberLine(
            x_range=[0, 8, 2], length=3.5, color=LIGHT_GRAY,
            include_numbers=True, font_size=18,
            decimal_number_config={"color": MID_GRAY}
        )
        nl_mini_l.move_to(LEFT * 3 + DOWN * 1.5)

        oc_l = Circle(radius=0.1, color=MID_GRAY, stroke_width=2)
        oc_l.set_fill(OFF_WHITE, opacity=1)
        oc_l.move_to(nl_mini_l.n2p(4))
        area_l = Line(nl_mini_l.n2p(0), nl_mini_l.n2p(4), color=MID_GRAY, stroke_width=5)
        arrow_area_l = Arrow(
            nl_mini_l.n2p(2), nl_mini_l.n2p(0),
            color=MID_GRAY, stroke_width=3, buff=0,
            max_tip_length_to_length_ratio=0.15
        )

        nl_mini_r = NumberLine(
            x_range=[-6, 2, 2], length=3.5, color=LIGHT_GRAY,
            include_numbers=True, font_size=18,
            decimal_number_config={"color": MID_GRAY}
        )
        nl_mini_r.move_to(RIGHT * 3 + DOWN * 1.5)

        oc_r = Circle(radius=0.1, color=BLACK, stroke_width=2)
        oc_r.set_fill(OFF_WHITE, opacity=1)
        oc_r.move_to(nl_mini_r.n2p(-3))
        area_r = Line(nl_mini_r.n2p(-3), nl_mini_r.n2p(2), color=BLACK, stroke_width=5)
        arrow_area_r = Arrow(
            nl_mini_r.n2p(-1), nl_mini_r.n2p(2),
            color=BLACK, stroke_width=3, buff=0,
            max_tip_length_to_length_ratio=0.15
        )

        self.play(
            Create(nl_mini_l), Create(area_l), FadeIn(oc_l), Create(arrow_area_l),
            Create(nl_mini_r), Create(area_r), FadeIn(oc_r), Create(arrow_area_r),
            run_time=1.5
        )
        self.wait(2)

        # Aturan emas
        rule = Text(
            "Kali / bagi negatif → tanda balik",
            font_size=24, color=BLACK, font="Arial", weight=BOLD
        )
        rule.move_to(DOWN * 3)
        rule_box = SurroundingRectangle(rule, color=BLACK, buff=0.25, stroke_width=2.5)

        self.play(Write(rule), Create(rule_box), run_time=1.2)
        self.wait(5)
