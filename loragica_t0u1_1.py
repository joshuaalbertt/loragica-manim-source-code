"""
Neraca Persamaan Linear — 3x + 7 = 22  ->  x = 5
Manim Community Edition (v0.18+).  ·  Palet: Loragica Brand Guidelines.

Palet (monokrom, tanpa gradasi, tanpa warna aksen di luar palet):
    Off-White #F5F5F3  — background/kanvas
    Black     #0A0A0A  — elemen penting: neraca, persamaan, hasil
    Mid Gray  #555555  — struktur sekunder (tali, tumpuan), status
    Light Gray#AAAAAA  — caption
    Grid line #E2E2E2  — grid dot pattern (elemen khas Loragica)

Sinyal benar/miring dibuat TANPA warna (sesuai brand): kemiringan neraca,
tanda ≠, dan efek goyang (Wiggle) untuk keadaan tak seimbang.

=====================================================================
NASKAH VOICE-OVER (Bahasa Indonesia) + TIMECODE  |  total ~39 detik
=====================================================================
[00:00–00:08]  SETUP
  "Anggap persamaan ini sebagai neraca. Di kiri: tiga-x tambah tujuh.
   Di kanan: dua puluh dua. Dan keduanya harus selalu setara."
[00:08–00:18]  MIRING (kontras — operasi tak seimbang)
  "Sekarang, kalau kita curang — kurangi tujuh hanya di ruas kanan —
   neracanya langsung miring. Kiri jadi lebih berat, dan kesetaraan
   pun rusak."
[00:18–00:26]  BENAR 1 (kurangi 7 di kedua ruas)
  "Aturannya: perlakukan kedua ruas sama. Kurangi tujuh di kiri dan
   kanan — neraca tetap datar, jadi tiga-x sama dengan lima belas."
[00:26–00:33]  BENAR 2 (bagi 3 di kedua ruas)
  "Terakhir, bagi kedua ruas dengan tiga. Neraca tetap seimbang —
   dan kita dapat x sama dengan lima."
[00:33–00:39]  HASIL
  "x sama dengan lima. Selama tiap langkah menjaga dua ruas setara,
   neraca tak pernah bohong."
=====================================================================

Render:
    manim -pqh neraca_persamaan_linear.py NeracaPersamaanLinear
Butuh LaTeX terpasang (untuk MathTex).
"""

import numpy as np
from manim import *

# ----- palet brand Loragica -----
BG = "#F5F5F3"
INK = "#0A0A0A"
MID = "#555555"
LIGHT = "#AAAAAA"
GRID = "#E2E2E2"

# ----- geometri -----
BEAM_Y = 1.2
SPAN = 2.7
PIVOT = np.array([0, BEAM_Y, 0])
L_LABEL = np.array([-SPAN, 0.12, 0])
R_LABEL = np.array([SPAN, 0.12, 0])
BASE_Y = -2.6
TAG_Y = -0.9


def make_pan(cx):
    """String kiri-kanan + mangkuk piring (outline hitam, tanpa isi warna)."""
    s1 = Line([cx, BEAM_Y, 0], [cx - 0.7, 0.35, 0], color=MID, stroke_width=2)
    s2 = Line([cx, BEAM_Y, 0], [cx + 0.7, 0.35, 0], color=MID, stroke_width=2)
    bowl = Polygon(
        [cx - 0.8, 0.35, 0], [cx + 0.8, 0.35, 0],
        [cx + 0.55, -0.28, 0], [cx - 0.55, -0.28, 0],
        color=INK, fill_opacity=0, stroke_width=3.5,
    )
    return VGroup(s1, s2, bowl)


class NeracaPersamaanLinear(Scene):
    def construct(self):
        self.camera.background_color = BG

        # grid dot pattern (elemen khas Loragica) — subtle, statis di belakang
        dots = VGroup(*[
            Dot([x, y, 0], radius=0.018, color=GRID, fill_opacity=1)
            for x in np.arange(-7.0, 7.01, 0.6)
            for y in np.arange(-4.0, 4.01, 0.6)
        ])
        self.add(dots)

        # ============================================================
        # [00:00–00:08] SETUP
        # ============================================================
        base = Line([-1.4, BASE_Y, 0], [1.4, BASE_Y, 0], color=MID, stroke_width=6)
        support = Polygon(
            [-0.6, BASE_Y, 0], [0.6, BASE_Y, 0], [0, BEAM_Y - 0.1, 0],
            color=MID, fill_opacity=0.12, stroke_width=2,
        )
        pivot = Dot(PIVOT, color=INK, radius=0.07)

        beam = Line([-SPAN, BEAM_Y, 0], [SPAN, BEAM_Y, 0], color=INK, stroke_width=8)
        left_pan = make_pan(-SPAN)
        right_pan = make_pan(SPAN)
        arm = VGroup(beam, left_pan, right_pan)

        self.play(Create(base), Create(support), run_time=0.7)
        self.play(Create(beam), FadeIn(pivot), run_time=0.5)
        self.play(Create(left_pan), Create(right_pan), run_time=0.7)

        eq = MathTex("3x + 7 = 22", font_size=54, color=INK).to_edge(UP)
        llab = MathTex("3x + 7", font_size=44, color=INK).move_to(L_LABEL)
        rlab = MathTex("22", font_size=44, color=INK).move_to(R_LABEL)

        self.play(Write(eq), run_time=0.8)
        self.play(FadeIn(llab, shift=DOWN * 0.2), FadeIn(rlab, shift=DOWN * 0.2), run_time=1.0)
        status = MathTex(r"\text{SEIMBANG}", font_size=26, color=MID).to_edge(DOWN)
        self.play(FadeIn(status), run_time=0.8)
        self.wait(3.5)

        # ============================================================
        # [00:08–00:18] MIRING (kontras — operasi tak seimbang)
        # ============================================================
        rbad = MathTex("15", font_size=44, color=INK).move_to(R_LABEL)
        eq_bad = MathTex("3x + 7", r"\neq", "15", font_size=54, color=INK).to_edge(UP)
        note = MathTex(r"-7 \ \text{hanya di ruas kanan}", font_size=28, color=MID).to_edge(DOWN)

        self.play(
            ReplacementTransform(rlab, rbad),
            ReplacementTransform(eq, eq_bad),
            FadeOut(status), FadeIn(note),
            run_time=1.0,
        )
        rlab = rbad
        # neraca oleng: ruas kiri lebih berat -> kiri turun (rotasi +)
        self.play(Rotate(VGroup(arm, llab, rlab), angle=9 * DEGREES, about_point=PIVOT),
                  run_time=0.8)
        self.play(Wiggle(eq_bad, scale_value=1.12), run_time=1.2)  # goyang = "salah" tanpa warna
        self.wait(2.5)

        # kembalikan ke seimbang
        self.play(Rotate(VGroup(arm, llab, rlab), angle=-9 * DEGREES, about_point=PIVOT),
                  run_time=0.7)
        rback = MathTex("22", font_size=44, color=INK).move_to(R_LABEL)
        eq = MathTex("3x + 7 = 22", font_size=54, color=INK).to_edge(UP)
        self.play(
            ReplacementTransform(rlab, rback),
            ReplacementTransform(eq_bad, eq),
            FadeOut(note),
            run_time=1.0,
        )
        rlab = rback
        self.wait(2.8)

        # ============================================================
        # [00:18–00:26] BENAR 1 — kurangi 7 di KEDUA ruas
        # ============================================================
        tag_l = MathTex("-7", font_size=36, color=INK).move_to([-SPAN, TAG_Y, 0])
        tag_r = MathTex("-7", font_size=36, color=INK).move_to([SPAN, TAG_Y, 0])
        self.play(FadeIn(tag_l, shift=UP * 0.2), FadeIn(tag_r, shift=UP * 0.2), run_time=0.8)

        eq_step1 = MathTex("3x + 7 - 7 = 22 - 7", font_size=52, color=INK).to_edge(UP)
        self.play(ReplacementTransform(eq, eq_step1), run_time=1.2)
        self.wait(2.0)

        llab2 = MathTex("3x", font_size=44, color=INK).move_to(L_LABEL)
        rlab2 = MathTex("15", font_size=44, color=INK).move_to(R_LABEL)
        eq2 = MathTex("3x = 15", font_size=54, color=INK).to_edge(UP)
        self.play(
            ReplacementTransform(llab, llab2),
            ReplacementTransform(rlab, rlab2),
            ReplacementTransform(eq_step1, eq2),
            FadeOut(tag_l), FadeOut(tag_r),
            run_time=1.2,
        )
        llab, rlab, eq = llab2, rlab2, eq2
        self.wait(2.8)

        # ============================================================
        # [00:26–00:33] BENAR 2 — bagi 3 di KEDUA ruas
        # ============================================================
        tag_l = MathTex(r"\div 3", font_size=36, color=INK).move_to([-SPAN, TAG_Y, 0])
        tag_r = MathTex(r"\div 3", font_size=36, color=INK).move_to([SPAN, TAG_Y, 0])
        self.play(FadeIn(tag_l, shift=UP * 0.2), FadeIn(tag_r, shift=UP * 0.2), run_time=0.8)

        eq_step2 = MathTex(r"\frac{3x}{3} = \frac{15}{3}", font_size=52, color=INK).to_edge(UP)
        self.play(ReplacementTransform(eq, eq_step2), run_time=1.2)
        self.wait(1.5)

        llab3 = MathTex("x", font_size=48, color=INK).move_to(L_LABEL)
        rlab3 = MathTex("5", font_size=48, color=INK).move_to(R_LABEL)
        eq3 = MathTex("x = 5", font_size=60, color=INK).to_edge(UP)
        self.play(
            ReplacementTransform(llab, llab3),
            ReplacementTransform(rlab, rlab3),
            ReplacementTransform(eq_step2, eq3),
            FadeOut(tag_l), FadeOut(tag_r),
            run_time=1.2,
        )
        llab, rlab, eq = llab3, rlab3, eq3
        self.wait(2.3)

        # ============================================================
        # [00:33–00:39] HASIL
        # ============================================================
        done = MathTex(r"\text{SEIMBANG \& SELESAI}", font_size=26, color=INK).to_edge(DOWN)
        self.play(FadeIn(done), run_time=0.8)
        self.play(
            Indicate(llab, color=INK, scale_factor=1.5),
            Indicate(rlab, color=INK, scale_factor=1.5),
            run_time=1.4,
        )
        self.play(Circumscribe(eq, color=INK, buff=0.2, run_time=1.6))
        self.wait(2.2)
