from manim import *

OFF_WHITE = "#F5F5F3"
BLACK = "#0A0A0A"
DARK_GRAY = "#1C1C1C"
MID_GRAY = "#555555"
LIGHT_GRAY = "#AAAAAA"
GRID_LINE = "#E2E2E2"


class QuadraticFormula(Scene):
    def construct(self):
        self.camera.background_color = OFF_WHITE

        dots = VGroup(*[
            Dot(point=[x, y, 0], radius=0.02, color=GRID_LINE)
            for x in np.arange(-7, 7, 0.7)
            for y in np.arange(-4, 4, 0.7)
        ])
        self.add(dots)

        # ============================================================
        # FASE 1: Kapan pakai? (0-8s)
        # ============================================================
        context = Text(
            "Kalau faktorisasi susah, ada rumus yang selalu kerja.",
            font_size=24, color=MID_GRAY, font="Arial"
        )
        context.move_to(UP * 1)

        general = MathTex("ax^2", "+", "bx", "+", "c", "=", "0", font_size=48)
        general.set_color(BLACK)
        general[2].set_color(DARK_GRAY)
        general[4].set_color(MID_GRAY)
        general.move_to(DOWN * 0.5)

        self.play(Write(context), run_time=1.3)
        self.wait(2)
        self.play(Write(general), run_time=1.3)
        self.wait(2.5)

        self.play(FadeOut(context), run_time=0.8)

        # ============================================================
        # FASE 2: Formula muncul (8-20s)
        # ============================================================
        self.play(general.animate.scale(0.6).move_to(UP * 3.2), run_time=1)

        formula = MathTex(
            "x", "=", "{-b", r"\pm", r"\sqrt{", "b^2", "-", "4ac}",
            r"\over", "2a}",
            font_size=52
        )
        formula.set_color(BLACK)
        formula.move_to(UP * 1)

        # Box di belakang formula
        formula_bg = SurroundingRectangle(formula, color=BLACK, buff=0.35, stroke_width=2)

        self.play(Write(formula), run_time=2.5)
        self.wait(1.5)
        self.play(Create(formula_bg), run_time=0.8)
        self.wait(2.5)

        disc_group = VGroup(formula[5], formula[6], formula[7])
        disc_box = SurroundingRectangle(disc_group, color=MID_GRAY, buff=0.08, stroke_width=2)

        label_disc = Text("diskriminan", font_size=16, color=MID_GRAY, font="Arial")
        label_disc.next_to(formula_bg, RIGHT, buff=0.5)

        arrow_disc = Arrow(
            label_disc.get_left(), disc_box.get_right() + RIGHT * 0.05,
            color=MID_GRAY, stroke_width=1.5, buff=0.05,
            max_tip_length_to_length_ratio=0.3
        )

        self.play(Create(disc_box), run_time=0.8)
        self.play(Write(label_disc), Create(arrow_disc), run_time=1)
        self.wait(2)

        self.play(FadeOut(label_disc), FadeOut(arrow_disc), FadeOut(disc_box), run_time=0.6)

        # ============================================================
        # FASE 3: Contoh soal (20-32s)
        # ============================================================
        self.play(
            VGroup(formula, formula_bg).animate.scale(0.55).move_to(UP * 3.2 + RIGHT * 2.5),
            FadeOut(general),
            run_time=1
        )

        example = MathTex("2x^2", "+", "3x", "-", "2", "=", "0", font_size=50)
        example.set_color(BLACK)
        example[2].set_color(DARK_GRAY)
        example[4].set_color(MID_GRAY)
        example.move_to(UP * 1.5)

        self.play(Write(example), run_time=1.3)
        self.wait(2)

        # Identifikasi a, b, c
        id_a = MathTex("a", "=", "2", font_size=38, color=BLACK)
        id_b = MathTex("b", "=", "3", font_size=38, color=DARK_GRAY)
        id_c = MathTex("c", "=", "-2", font_size=38, color=MID_GRAY)

        ids = VGroup(id_a, id_b, id_c).arrange(RIGHT, buff=1.2)
        ids.move_to(UP * 0.2)

        # Highlight tiap koefisien di soal saat muncul
        box_a = SurroundingRectangle(example[0], color=BLACK, buff=0.08, stroke_width=2)
        self.play(Create(box_a), Write(id_a), run_time=1)
        self.wait(0.5)

        box_b = SurroundingRectangle(example[2], color=DARK_GRAY, buff=0.08, stroke_width=2)
        self.play(Create(box_b), Write(id_b), run_time=1)
        self.wait(0.5)

        box_c = SurroundingRectangle(example[4], color=MID_GRAY, buff=0.08, stroke_width=2)
        self.play(Create(box_c), Write(id_c), run_time=1)
        self.wait(2)

        self.play(FadeOut(VGroup(box_a, box_b, box_c)), run_time=0.6)

        # ============================================================
        # FASE 4: Substitusi step by step (32-52s)
        # ============================================================
        self.play(
            example.animate.scale(0.55).move_to(UP * 3.2 + LEFT * 2.5),
            ids.animate.scale(0.55).move_to(UP * 2.5 + LEFT * 2.5),
            run_time=1
        )

        # Step 1: substitusi mentah
        step1 = MathTex(
            "x", "=", "{-(3)", r"\pm", r"\sqrt{", "(3)^2", "-", "4(2)(-2)}",
            r"\over", "2(2)}",
            font_size=40
        )
        step1.set_color(BLACK)
        step1.move_to(UP * 0.8)

        self.play(Write(step1), run_time=2)
        self.wait(2.5)

        # Step 2: hitung dalam akar
        step2 = MathTex(
            "x", "=", "{-3", r"\pm", r"\sqrt{", "9", "+", "16}",
            r"\over", "4}",
            font_size=40
        )
        step2.set_color(BLACK)
        step2.move_to(DOWN * 0.5)

        self.play(Write(step2), run_time=1.5)
        self.wait(2)

        # Step 3: simplifikasi akar
        step3 = MathTex(
            "x", "=", "{-3", r"\pm", r"\sqrt{", "25}",
            r"\over", "4}",
            font_size=40
        )
        step3.set_color(BLACK)
        step3.move_to(DOWN * 1.8)

        self.play(Write(step3), run_time=1.3)
        self.wait(1)

        step3b = MathTex(
            "x", "=", "{-3", r"\pm", "5",
            r"\over", "4}",
            font_size=40
        )
        step3b.set_color(BLACK)
        step3b.move_to(DOWN * 1.8)

        self.play(Transform(step3, step3b), run_time=1)
        self.wait(2)

        # ============================================================
        # FASE 5: Hasil akhir (52-75s)
        # ============================================================
        self.play(
            FadeOut(VGroup(step1, step2, example, ids, formula, formula_bg)),
            step3.animate.move_to(UP * 2),
            run_time=1
        )
        self.wait(1)

        # Dua cabang: + dan -
        branch_plus = MathTex(
            "x", "=", "{-3", "+", "5", r"\over", "4}",
            font_size=40, color=BLACK
        )
        branch_plus.move_to(LEFT * 2.8 + UP * 0.3)

        branch_minus = MathTex(
            "x", "=", "{-3", "-", "5", r"\over", "4}",
            font_size=40, color=MID_GRAY
        )
        branch_minus.move_to(RIGHT * 2.8 + UP * 0.3)

        self.play(Write(branch_plus), Write(branch_minus), run_time=1.5)
        self.wait(2)

        # Hasil
        ans_plus = MathTex(
            "x", "=", "{2", r"\over", "4}", "=", r"\frac{1}{2}",
            font_size=40, color=BLACK
        )
        ans_plus.move_to(LEFT * 2.8 + DOWN * 1.3)

        ans_minus = MathTex(
            "x", "=", "{-8", r"\over", "4}", "=", "-2",
            font_size=40, color=MID_GRAY
        )
        ans_minus.move_to(RIGHT * 2.8 + DOWN * 1.3)

        arrow_l = Arrow(
            branch_plus.get_bottom() + DOWN * 0.1, ans_plus.get_top() + UP * 0.1,
            color=BLACK, stroke_width=2, buff=0.05, max_tip_length_to_length_ratio=0.25
        )
        arrow_r = Arrow(
            branch_minus.get_bottom() + DOWN * 0.1, ans_minus.get_top() + UP * 0.1,
            color=MID_GRAY, stroke_width=2, buff=0.05, max_tip_length_to_length_ratio=0.25
        )

        self.play(Create(arrow_l), Write(ans_plus), run_time=1.2)
        self.wait(1)
        self.play(Create(arrow_r), Write(ans_minus), run_time=1.2)
        self.wait(1.5)

        # Box final + "atau"
        final_ans_l = MathTex(r"x = \frac{1}{2}", font_size=48, color=BLACK)
        final_ans_l.move_to(LEFT * 2 + DOWN * 3)
        final_ans_r = MathTex("x = -2", font_size=48, color=MID_GRAY)
        final_ans_r.move_to(RIGHT * 2 + DOWN * 3)
        atau = Text("atau", font_size=20, color=MID_GRAY, font="Arial")
        atau.move_to(DOWN * 3)

        final_box = SurroundingRectangle(
            VGroup(final_ans_l, final_ans_r), color=BLACK, buff=0.35
        )

        self.play(
            Write(final_ans_l), Write(final_ans_r), FadeIn(atau),
            run_time=1.3
        )
        self.play(Create(final_box), run_time=0.8)
        self.wait(4)
