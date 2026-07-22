from manim import *

# === Loragica Color System ===
OFF_WHITE = "#F5F5F3"
BLACK = "#0A0A0A"
DARK_GRAY = "#1C1C1C"
MID_GRAY = "#555555"
LIGHT_GRAY = "#AAAAAA"
GRID_LINE = "#E2E2E2"


class SimplifyTermsFull(Scene):
    def construct(self):
        # Background off-white, bukan putih murni
        self.camera.background_color = OFF_WHITE

        # Grid dot pattern subtle di background (elemen khas Loragica)
        dots = VGroup(*[
            Dot(point=[x, y, 0], radius=0.02, color=GRID_LINE)
            for x in np.arange(-7, 7, 0.7)
            for y in np.arange(-4, 4, 0.7)
        ])
        self.add(dots)

        # === FASE 1: Intro (0-8s) ===
        expr = MathTex("3x", "+", "5", "+", "2x", "-", "1", font_size=60)
        expr.set_color(BLACK)
        expr[0].set_color(BLACK)      # 3x — kelompok "suku x": hitam (otoritas)
        expr[4].set_color(BLACK)      # 2x
        expr[2].set_color(MID_GRAY)   # 5 — kelompok "konstanta": mid gray
        expr[6].set_color(MID_GRAY)   # -1
        expr.move_to(ORIGIN)
        self.play(Write(expr), run_time=1.5)
        self.wait(4)

        # === FASE 2: Analogi (8-20s) — pakai bentuk geometris, bukan emoji ===
        self.play(expr.animate.scale(0.6).move_to(UP * 3))

        def make_shape(shape_cls, color):
            return shape_cls(color=color, fill_color=color, fill_opacity=1).scale(0.25)

        squares = VGroup(*[make_shape(Square, BLACK) for _ in range(3)]).arrange(RIGHT, buff=0.3)
        plus1 = Text("+", color=BLACK, font_size=32)
        circles_pos = VGroup(*[make_shape(Circle, MID_GRAY) for _ in range(5)]).arrange(RIGHT, buff=0.25)

        row1 = VGroup(squares, plus1, circles_pos).arrange(RIGHT, buff=0.4)
        analogy_label = Text(
            "3 persegi + 5 lingkaran + 2 persegi - 1 lingkaran",
            font_size=26, color=DARK_GRAY, font="Arial"
        )

        self.play(FadeIn(row1), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(row1), Write(analogy_label), run_time=1.5)
        self.wait(2.5)

        note = Text(
            "Persegi cuma bisa gabung sama persegi.\nLingkaran cuma bisa gabung sama lingkaran.",
            font_size=22, color=MID_GRAY, font="Arial"
        )
        note.next_to(analogy_label, DOWN, buff=0.5)
        self.play(Write(note), run_time=1.5)
        self.wait(4.5)
        self.play(FadeOut(analogy_label), FadeOut(note))

        # === FASE 3: Highlight suku sejenis (20-30s) ===
        self.play(expr.animate.scale(1 / 0.6).move_to(ORIGIN), run_time=1.5)
        self.wait(1)

        box_x = SurroundingRectangle(VGroup(expr[0], expr[4]), color=BLACK, buff=0.15)
        box_const = SurroundingRectangle(VGroup(expr[2], expr[6]), color=MID_GRAY, buff=0.15)

        label_x = Text("suku x", font_size=24, color=BLACK, font="Arial").next_to(box_x, UP)
        label_const = Text("konstanta", font_size=24, color=MID_GRAY, font="Arial").next_to(box_const, DOWN)

        self.play(Create(box_x), Write(label_x), run_time=1.2)
        self.wait(1.5)
        self.play(Create(box_const), Write(label_const), run_time=1.2)
        self.wait(3.5)
        self.play(FadeOut(box_x), FadeOut(box_const), FadeOut(label_x), FadeOut(label_const), run_time=1)
        self.wait(1.5)

        # === FASE 4: Perpindahan fisik (30-42s) ===
        # Target absolut: kelompok x di kiri, kelompok konstanta di kanan
        target_x_group_center = LEFT * 2
        target_const_group_center = RIGHT * 2.5

        self.play(
            expr[0].animate.move_to(target_x_group_center + LEFT * 0.4),
            expr[4].animate.move_to(target_x_group_center + RIGHT * 0.4),
            expr[2].animate.move_to(target_const_group_center + LEFT * 0.4),
            expr[6].animate.move_to(target_const_group_center + RIGHT * 0.4),
            FadeOut(expr[1]), FadeOut(expr[3]), FadeOut(expr[5]),  # tanda +/- lama disembunyikan
            run_time=3.5
        )
        self.wait(5.5)

        # === FASE 5: Operasi penjumlahan (42-52s) — mono untuk notasi ===
        sum_x = MathTex("3+2=5", font_size=40, color=BLACK)
        sum_x.move_to(target_x_group_center + DOWN * 1.5)
        sum_c = MathTex("5-1=4", font_size=40, color=MID_GRAY)
        sum_c.move_to(target_const_group_center + DOWN * 1.5)

        self.play(Write(sum_x), run_time=1.2)
        self.wait(1.5)
        self.play(Write(sum_c), run_time=1.2)
        self.wait(2.5)

        # === FASE 6: Hasil akhir (52-60s) ===
        result = MathTex("5x", "+", "4", font_size=70)
        result[0].set_color(BLACK)
        result[1].set_color(DARK_GRAY)   # tanda "+" — wajib diwarnai, default putih tak kelihatan di bg off-white
        result[2].set_color(MID_GRAY)
        result.move_to(ORIGIN)

        # remaining_terms (4 elemen: 3x,2x,5,-1) ditransform HANYA ke angka/x hasil (result[0], result[2])
        # tanda "+" sumbernya cuma satu: result[1] itu sendiri, tidak ada plus_sign terpisah
        remaining_terms = VGroup(expr[0], expr[4], expr[2], expr[6])
        result_numbers = VGroup(result[0], result[2])

        self.play(
            FadeOut(sum_x), FadeOut(sum_c),
            Transform(remaining_terms, result_numbers),
            FadeIn(result[1]),
            run_time=1.5
        )
        self.wait(1)

        # Checkmark custom (bukan emoji) — dua garis tegas warna hitam
        check = VMobject(color=BLACK, stroke_width=6)
        check.set_points_as_corners([
            [-0.15, 0, 0], [0, -0.15, 0], [0.3, 0.2, 0]
        ])
        final_group = VGroup(remaining_terms, result[1])
        check.next_to(final_group, RIGHT, buff=0.6)

        final_box = SurroundingRectangle(final_group, color=BLACK, buff=0.3)
        self.play(Create(final_box), Create(check), run_time=1)
        self.wait(4.5)
