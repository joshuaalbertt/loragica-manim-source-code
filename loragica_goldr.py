from manim import *
import numpy as np

COLOR_OFF_WHITE  = "#FAFBFC"
COLOR_NAVY_BLUE  = "#1D3557"
COLOR_DEEP_RED   = "#E63946"
COLOR_GOLD       = "#F4C620"
COLOR_SOFT_GREEN = "#2A9D8F"
COLOR_GRID_DOT   = "#E2E2E2"

FONT_TITLE   = "Poppins"
FONT_TAGLINE = "Inter"

GOLDEN_RATIO = (1 + np.sqrt(5)) / 2

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02X}{:02X}{:02X}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def interpolate_hex(color1, color2, t):
    c1 = np.array(hex_to_rgb(color1), dtype=float)
    c2 = np.array(hex_to_rgb(color2), dtype=float)
    res = c1 + (c2 - c1) * t
    return rgb_to_hex(np.round(res).astype(int))

class LoragicaGoldenRatioScene(Scene):
    def construct(self):
        self.camera.background_color = COLOR_OFF_WHITE

        grid = NumberPlane(
            x_range=[-10, 10, 1],
            y_range=[-6, 6, 1],
            background_line_style={
                "stroke_color": COLOR_GRID_DOT,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        )
        self.add(grid)

        def get_loragica_logo(scale_factor=1.0):
            logo = VGroup()
            square_positions = [
                (UL, "outline", COLOR_NAVY_BLUE),
                (UR, "filled",  COLOR_NAVY_BLUE),
                (DL, "filled",  COLOR_SOFT_GREEN),
                (DR, "outline", COLOR_NAVY_BLUE)
            ]
            for pos, style, color in square_positions:
                sq = RoundedRectangle(
                    corner_radius=0.15,
                    width=1.2,
                    height=1.2,
                    stroke_width=6 if style == "outline" else 0,
                    stroke_color=color if style == "outline" else None,
                    fill_color=color if style == "filled" else None,
                    fill_opacity=1.0 if style == "filled" else 0.0
                ).shift(pos * 0.7)
                logo.add(sq)
            return logo.scale(scale_factor)

        logo_opening = get_loragica_logo(scale_factor=1.2).center()
        logo_opening.scale(0)

        self.play(logo_opening.animate.scale(1.3), run_time=0.15)
        self.play(logo_opening.animate.scale(1.0), run_time=0.15)
        self.wait(0.2)

        gold_dot = Dot(color=COLOR_GOLD, radius=0.12).move_to(logo_opening[2])
        self.play(TransformFromCopy(logo_opening[2], gold_dot), run_time=0.8)

        self.play(
            logo_opening.animate.scale(0.3).to_corner(UR, buff=0.5),
            gold_dot.animate.scale(1.5).move_to(ORIGIN),
            run_time=1.5
        )
        self.wait(0.3)

        golden_rect = self.create_golden_rectangle(scale=2.4).center()
        self.play(Create(golden_rect, run_time=1.5))
        self.play(gold_dot.animate.move_to(golden_rect.get_corner(DL)), run_time=0.5)

        squares, arcs = self.create_fibonacci_tiling(golden_rect)

        for sq, arc in zip(squares, arcs):
            self.play(
                Create(sq, run_time=0.4),
                gold_dot.animate.move_to(sq.get_center()),
                run_time=0.6
            )
            self.play(
                Create(arc, run_time=0.4),
                gold_dot.animate.move_to(arc.get_end()),
                run_time=0.6
            )

        self.play(Flash(gold_dot, color=COLOR_GOLD, line_length=0.3), run_time=0.4)
        self.wait(0.4)

        all_spiral = VGroup(golden_rect, *squares, *arcs)
        nature_items = self.create_nature_examples()

        self.play(
            FadeOut(grid, run_time=1),
            all_spiral.animate.scale(0.6).to_edge(LEFT, buff=0.5),
            gold_dot.animate.move_to(all_spiral.get_center()),
            run_time=2
        )
        self.wait(0.3)

        for item, label in nature_items:
            self.play(
                FadeIn(item, shift=RIGHT * 0.4),
                Write(label, run_time=0.5),
                run_time=0.8
            )
        self.wait(0.5)

        self.play(
            FadeOut(all_spiral),
            FadeOut(*[item for item, _ in nature_items]),
            FadeOut(*[label for _, label in nature_items]),
            FadeOut(gold_dot),
            run_time=1
        )

        quote = Text(
            "φ = 1.618", font=FONT_TITLE, weight=BOLD,
            font_size=58, color=COLOR_NAVY_BLUE
        ).center().shift(UP * 0.5)
        subquote = Text(
            "Nature's hidden proportion", font=FONT_TAGLINE, weight=MEDIUM,
            font_size=24, color=COLOR_DEEP_RED
        ).next_to(quote, DOWN, buff=0.3)

        self.play(Write(quote, run_time=1.2))
        self.play(FadeIn(subquote, shift=UP * 0.2), run_time=1)
        self.wait(1)

        final_logo = get_loragica_logo(scale_factor=1.0).center().shift(DOWN * 1.5)
        tagline = Text(
            "LEARN · SEE · CONNECT", font=FONT_TAGLINE, weight=MEDIUM,
            font_size=16, color=COLOR_NAVY_BLUE
        ).next_to(final_logo, DOWN, buff=0.4)

        self.play(
            quote.animate.shift(UP * 1.2).scale(0.8),
            subquote.animate.shift(UP * 1.2).scale(0.8),
            LaggedStart(
                *[DrawBorderThenFill(sq) if sq.fill_opacity > 0 else Create(sq)
                  for sq in final_logo],
                run_time=1.5,
                lag_ratio=0.2
            ),
            FadeIn(tagline, shift=UP * 0.2, run_time=1.5)
        )
        self.wait(4)

    def create_golden_rectangle(self, scale=1.0):
        width = scale
        height = scale * GOLDEN_RATIO
        rect = Rectangle(
            width=width, height=height,
            stroke_color=COLOR_NAVY_BLUE, stroke_width=3,
            fill_color=COLOR_NAVY_BLUE, fill_opacity=0.05
        )
        return rect

    def create_fibonacci_tiling(self, outer_rect):
        squares = VGroup()
        arcs = VGroup()

        w = outer_rect.get_width()
        h = outer_rect.get_height()
        origin = outer_rect.get_corner(DL)

        side = min(w, h)
        sides = [side]
        directions = [RIGHT, UP, LEFT, DOWN]
        points = [origin]

        for i in range(10):
            side = sides[-1]
            if i >= 2:
                side = sides[-1] + sides[-2]
            sides.append(side)
            if i == 0:
                side = min(w, h)

            dir_idx = i % 4
            dir_vec = directions[dir_idx]
            start_pt = points[-1]
            end_pt = start_pt + dir_vec * side

            sq = Square(
                side_length=side,
                stroke_color=COLOR_NAVY_BLUE,
                stroke_width=2,
                fill_color=COLOR_GOLD,
                fill_opacity=0.12
            ).move_to(start_pt + dir_vec * (side / 2), aligned_edge=DL)
            squares.add(sq)

            arc_center = sq.get_center()
            if dir_idx == 0:
                start_angle = PI
                arc_center = sq.get_corner(DL)
            elif dir_idx == 1:
                start_angle = PI / 2
                arc_center = sq.get_corner(DR)
            elif dir_idx == 2:
                start_angle = 0
                arc_center = sq.get_corner(UR)
            else:
                start_angle = 3 * PI / 2
                arc_center = sq.get_corner(UL)

            arc = Arc(
                radius=side,
                start_angle=start_angle,
                angle=PI / 2,
                color=COLOR_DEEP_RED,
                stroke_width=4
            ).move_arc_center_to(arc_center)
            arcs.add(arc)

            points.append(end_pt)

            if end_pt[0] > origin[0] + w + 0.01 or end_pt[1] > origin[1] + h + 0.01:
                break

        return squares, arcs

    def create_nature_examples(self):
        items = []

        sunflower = self.create_sunflower(radius=0.8)
        sunflower_label = Text("Sunflower seeds", font=FONT_TAGLINE, font_size=14, color=COLOR_NAVY_BLUE).next_to(sunflower, DOWN, buff=0.15)
        items.append((sunflower, sunflower_label))

        nautilus = self.create_nautilus(scale=0.9)
        nautilus_label = Text("Nautilus shell", font=FONT_TAGLINE, font_size=14, color=COLOR_NAVY_BLUE).next_to(nautilus, DOWN, buff=0.15)
        items.append((nautilus, nautilus_label))

        parthenon = self.create_parthenon()
        parthenon_label = Text("Parthenon facade", font=FONT_TAGLINE, font_size=14, color=COLOR_NAVY_BLUE).next_to(parthenon, DOWN, buff=0.15)
        items.append((parthenon, parthenon_label))

        layout = VGroup(
            VGroup(sunflower, sunflower_label),
            VGroup(nautilus, nautilus_label),
            VGroup(parthenon, parthenon_label)
        ).arrange(RIGHT, buff=1.2).center().to_edge(RIGHT, buff=0.8)

        return [(sunflower, sunflower_label), (nautilus, nautilus_label), (parthenon, parthenon_label)]

    def create_sunflower(self, radius=0.7, center=ORIGIN):
        dots = VGroup()
        n = 200
        golden_angle = 2 * PI * (1 - 1 / GOLDEN_RATIO)
        for i in range(n):
            theta = i * golden_angle
            r = radius * np.sqrt(i) / np.sqrt(n)
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            t = i / n
            color_hex = interpolate_hex(COLOR_GOLD, COLOR_DEEP_RED, t)
            dot = Dot(
                point=center + np.array([x, y, 0]),
                radius=0.02,
                color=color_hex
            )
            dots.add(dot)
        return dots

    def create_nautilus(self, scale=1.0):
        spiral = ParametricFunction(
            lambda t: np.array([
                scale * 0.35 * np.exp(0.18 * t) * np.cos(t),
                scale * 0.35 * np.exp(0.18 * t) * np.sin(t),
                0
            ]),
            t_range=[0, 4.5 * PI],
            color=COLOR_SOFT_GREEN,
            stroke_width=3
        )
        return spiral

    def create_parthenon(self):
        width = 2.2
        height = width / GOLDEN_RATIO
        base = Rectangle(
            width=width, height=height,
            stroke_color=COLOR_NAVY_BLUE,
            stroke_width=2,
            fill_color=COLOR_NAVY_BLUE,
            fill_opacity=0.08
        )
        pediment_height = height * 0.4
        triangle = Polygon(
            base.get_corner(UL),
            base.get_corner(UR),
            base.get_top() + UP * pediment_height,
            stroke_color=COLOR_DEEP_RED,
            stroke_width=2,
            fill_color=COLOR_DEEP_RED,
            fill_opacity=0.15
        )
        return VGroup(base, triangle)
