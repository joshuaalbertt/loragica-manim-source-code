from manim import *

OFF_WHITE = "#F5F5F3"
BLACK = "#0A0A0A"
DARK_GRAY = "#1C1C1C"
MID_GRAY = "#555555"
LIGHT_GRAY = "#AAAAAA"
GRID_LINE = "#E2E2E2"

# Posisi absolut semua node — tidak ada .shift() atau .next_to() berantai
ROOT_POS = UP * 2.5
NODE_L_POS = LEFT * 2.8 + UP * 0.3
NODE_R_POS = RIGHT * 2.8 + UP * 0.3
NUM_L_POS = LEFT * 2.8 + DOWN * 1.0
NUM_R_POS = RIGHT * 2.8 + DOWN * 1.0
CALC_SUM_POS = LEFT * 2.5 + DOWN * 2.5
CALC_PROD_POS = RIGHT * 2.5 + DOWN * 2.5


class FactorTree(Scene):
    def construct(self):
        self.camera.background_color = OFF_WHITE

        # Grid dot
        dots = VGroup(*[
            Dot(point=[x, y, 0], radius=0.02, color=GRID_LINE)
            for x in np.arange(-7, 7, 0.7)
            for y in np.arange(-4, 4, 0.7)
        ])
        self.add(dots)

        # ============================================================
        # FASE 1: Tampilkan trinomial (0-10s)
        # ============================================================
        root = MathTex("x^2", "+", "5x", "+", "6", font_size=52)
        root.set_color(BLACK)
        root.move_to(ROOT_POS)

        self.play(Write(root), run_time=1.5)
        self.wait(4)

        task = Text(
            "Cari 2 angka: ditambah = 5, dikali = 6",
            font_size=22, color=MID_GRAY, font="Arial"
        )
        task.move_to(UP * 1.2)
        self.play(Write(task), run_time=1.5)
        self.wait(3)

        # ============================================================
        # FASE 2: Pohon bercabang (10-22s)
        # ============================================================
        self.play(FadeOut(task), run_time=0.8)

        # Titik cabang
        fork = Dot(ROOT_POS + DOWN * 0.45, radius=0, color=OFF_WHITE)

        # Garis cabang
        line_l = Line(fork.get_center(), NODE_L_POS + UP * 0.35, color=BLACK, stroke_width=2.5)
        line_r = Line(fork.get_center(), NODE_R_POS + UP * 0.35, color=MID_GRAY, stroke_width=2.5)

        self.play(Create(line_l), Create(line_r), run_time=1.5)
        self.wait(1)

        # Node kiri
        node_l = MathTex("(x+2)", font_size=44, color=BLACK)
        node_l.move_to(NODE_L_POS)

        # Node kanan
        node_r = MathTex("(x+3)", font_size=44, color=MID_GRAY)
        node_r.move_to(NODE_R_POS)

        self.play(Write(node_l), run_time=1.2)
        self.wait(0.8)
        self.play(Write(node_r), run_time=1.2)
        self.wait(5)

        # ============================================================
        # FASE 3: Ekstrak angka + highlight "ditambah" (22-38s)
        # ============================================================
        # Panah turun dari tiap node ke angka yang diekstrak
        arrow_l = Arrow(
            NODE_L_POS + DOWN * 0.35, NUM_L_POS + UP * 0.3,
            color=BLACK, stroke_width=2, buff=0.05, max_tip_length_to_length_ratio=0.2
        )
        arrow_r = Arrow(
            NODE_R_POS + DOWN * 0.35, NUM_R_POS + UP * 0.3,
            color=MID_GRAY, stroke_width=2, buff=0.05, max_tip_length_to_length_ratio=0.2
        )

        num_2 = MathTex("2", font_size=52, color=BLACK).move_to(NUM_L_POS)
        num_3 = MathTex("3", font_size=52, color=MID_GRAY).move_to(NUM_R_POS)

        self.play(Create(arrow_l), Write(num_2), run_time=1)
        self.play(Create(arrow_r), Write(num_3), run_time=1)
        self.wait(3.5)

        # Garis lengkung yang menghubungkan 2 dan 3 (di bawah keduanya)
        arc_sum = ArcBetweenPoints(
            NUM_L_POS + DOWN * 0.4, NUM_R_POS + DOWN * 0.4,
            angle=-TAU / 5, color=DARK_GRAY, stroke_width=2
        )
        sum_label = MathTex("2+3=5", font_size=34, color=DARK_GRAY)
        sum_label.move_to(CALC_SUM_POS)

        tag_sum = Text("= koefisien x", font_size=18, color=MID_GRAY, font="Arial")
        tag_sum.next_to(sum_label, RIGHT, buff=0.3)

        self.play(Create(arc_sum), run_time=1.3)
        self.wait(1)
        self.play(Write(sum_label), Write(tag_sum), run_time=1.3)
        self.wait(1)

        # Highlight suku tengah di root
        hl_5x = SurroundingRectangle(root[2], color=DARK_GRAY, buff=0.1, stroke_width=2.5)
        self.play(Create(hl_5x), run_time=0.8)
        self.wait(4.5)

        # ============================================================
        # FASE 4: Highlight "dikali" (38-50s)
        # ============================================================
        arc_prod = ArcBetweenPoints(
            NUM_L_POS + DOWN * 0.4, NUM_R_POS + DOWN * 0.4,
            angle=TAU / 5, color=LIGHT_GRAY, stroke_width=2
        )
        prod_label = MathTex(r"2 \times 3=6", font_size=34, color=DARK_GRAY)
        prod_label.move_to(CALC_PROD_POS)

        tag_prod = Text("= konstanta", font_size=18, color=MID_GRAY, font="Arial")
        tag_prod.next_to(prod_label, RIGHT, buff=0.3)

        self.play(Create(arc_prod), run_time=1.3)
        self.wait(1)
        self.play(Write(prod_label), Write(tag_prod), run_time=1.3)
        self.wait(1)

        # Highlight konstanta di root
        hl_6 = SurroundingRectangle(root[4], color=LIGHT_GRAY, buff=0.1, stroke_width=2.5)
        self.play(Create(hl_6), run_time=0.8)
        self.wait(4.5)

        # ============================================================
        # FASE 5: Closing — hasil faktorisasi (50-60s)
        # ============================================================
        self.play(
            FadeOut(VGroup(
                arc_sum, arc_prod, sum_label, tag_sum,
                prod_label, tag_prod, hl_5x, hl_6,
                arrow_l, arrow_r, num_2, num_3
            )),
            run_time=1
        )

        eq_sign = MathTex("=", font_size=44, color=DARK_GRAY)
        eq_sign.move_to(DOWN * 1.0)

        result = MathTex("(x+2)", "(x+3)", font_size=48)
        result[0].set_color(BLACK)
        result[1].set_color(MID_GRAY)
        result.move_to(DOWN * 1.0 + RIGHT * 0.4)
        eq_sign.next_to(result, LEFT, buff=0.3)

        result_box = SurroundingRectangle(
            VGroup(eq_sign, result), color=BLACK, buff=0.3
        )

        self.play(Write(eq_sign), Write(result), run_time=1.3)
        self.wait(1)
        self.play(Create(result_box), run_time=0.8)
        self.wait(2)

        # ============================================================
        # FASE 6: Zero product → solusi (62-75s)
        # ============================================================
        # Bersihkan pohon, sisakan hasil faktorisasi
        self.play(
            FadeOut(VGroup(root, line_l, line_r, node_l, node_r)),
            VGroup(eq_sign, result, result_box).animate.move_to(UP * 2),
            run_time=1.2
        )
        self.wait(1)

        # Tambah "= 0"
        eq_zero = MathTex("=", "0", font_size=48, color=DARK_GRAY)
        eq_zero.next_to(result, RIGHT, buff=0.3)
        self.play(Write(eq_zero), run_time=0.8)
        self.wait(1.5)

        # Zero product property
        rule = Text(
            "Kalau hasil kali = 0, salah satu harus = 0",
            font_size=22, color=MID_GRAY, font="Arial"
        )
        rule.move_to(UP * 0.5)
        self.play(Write(rule), run_time=1.3)
        self.wait(2)

        # Dua cabang solusi
        sol_l = MathTex("x+2", "=", "0", font_size=40, color=BLACK)
        sol_l.move_to(LEFT * 2.5 + DOWN * 1)

        sol_r = MathTex("x+3", "=", "0", font_size=40, color=MID_GRAY)
        sol_r.move_to(RIGHT * 2.5 + DOWN * 1)

        self.play(Write(sol_l), Write(sol_r), run_time=1.3)
        self.wait(1.5)

        # Hasil akhir
        ans_l = MathTex("x", "=", "-2", font_size=44, color=BLACK)
        ans_l.move_to(LEFT * 2.5 + DOWN * 2.3)

        ans_r = MathTex("x", "=", "-3", font_size=44, color=MID_GRAY)
        ans_r.move_to(RIGHT * 2.5 + DOWN * 2.3)

        arrow_sol_l = Arrow(
            sol_l.get_bottom() + DOWN * 0.1, ans_l.get_top() + UP * 0.1,
            color=BLACK, stroke_width=2, buff=0.05, max_tip_length_to_length_ratio=0.25
        )
        arrow_sol_r = Arrow(
            sol_r.get_bottom() + DOWN * 0.1, ans_r.get_top() + UP * 0.1,
            color=MID_GRAY, stroke_width=2, buff=0.05, max_tip_length_to_length_ratio=0.25
        )

        self.play(Create(arrow_sol_l), Write(ans_l), run_time=1)
        self.play(Create(arrow_sol_r), Write(ans_r), run_time=1)
        self.wait(1)

        # Box final
        final_box = SurroundingRectangle(VGroup(ans_l, ans_r), color=BLACK, buff=0.4)
        atau = Text("atau", font_size=20, color=MID_GRAY, font="Arial")
        atau.move_to((ans_l.get_center() + ans_r.get_center()) / 2)

        self.play(FadeIn(atau), Create(final_box), run_time=1)
        self.wait(4)
