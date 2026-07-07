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

class LoragicaMegahScene(ThreeDScene):
    def construct(self):
        self.camera.background_color = COLOR_NAVY_BLUE
        self.wait(0.3)

        flash = Flash(ORIGIN, color=COLOR_GOLD, flash_radius=2.5, line_length=0.8)
        self.play(flash, run_time=0.4)

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
            gold_dot.animate.scale(1.8).move_to(ORIGIN),
            run_time=1.5
        )
        self.wait(0.3)

        math_axes = Axes(
            x_range=[-3, 3, 1], y_range=[-2, 4, 1],
            x_length=7, y_length=4,
            axis_config={"color": COLOR_NAVY_BLUE}
        ).center().shift(DOWN * 0.5)

        func = math_axes.plot(
            lambda x: 0.5 * x**2 + 0.5,
            color=COLOR_NAVY_BLUE, stroke_width=3
        )
        self.play(Create(math_axes), Create(func),
                  gold_dot.animate.move_to(math_axes.c2p(-1.5, 0.5*(-1.5)**2 + 0.5)),
                  run_time=1.5)

        t_tracker = ValueTracker(-1.5)
        gold_dot.add_updater(
            lambda d: d.move_to(
                math_axes.c2p(t_tracker.get_value(),
                              0.5 * t_tracker.get_value()**2 + 0.5)
            )
        )
        tangent_line = always_redraw(
            lambda: math_axes.plot(
                lambda x: t_tracker.get_value() * (x - t_tracker.get_value())
                          + 0.5 * t_tracker.get_value()**2 + 0.5,
                x_range=[max(-3, t_tracker.get_value() - 1.5),
                         min(3, t_tracker.get_value() + 1.5)],
                color=COLOR_DEEP_RED, stroke_width=4
            )
        )
        self.play(Create(tangent_line))

        self.play(t_tracker.animate.set_value(2), run_time=1.2, rate_func=linear)
        self.wait(0.1)

        gold_dot.clear_updaters()
        self.play(Flash(gold_dot, color=COLOR_GOLD, line_length=0.3), run_time=0.3)
        self.wait(0.3)

        self.move_camera(phi=65 * DEGREES, theta=-45 * DEGREES, run_time=2, rate_func=smooth)

        axes_3d = ThreeDAxes(
            x_range=[-4, 4, 1], y_range=[-4, 4, 1], z_range=[-2, 2, 1],
            x_length=6, y_length=6, z_length=3,
            axis_config={"color": BLACK, "stroke_width": 2}
        ).center()

        physics_wave = ParametricFunction(
            lambda t: axes_3d.c2p(t, np.sin(2 * t), np.cos(2 * t)),
            t_range=[-np.pi, np.pi],
            color=COLOR_DEEP_RED, stroke_width=4
        )
        gold_start_wave = axes_3d.c2p(-np.pi, np.sin(-2*np.pi), np.cos(-2*np.pi))
        self.play(
            ReplacementTransform(math_axes, axes_3d),
            ReplacementTransform(func, physics_wave),
            FadeOut(tangent_line),
            gold_dot.animate.move_to(gold_start_wave),
            run_time=2
        )

        wave_tracker = ValueTracker(-np.pi)
        gold_dot.add_updater(
            lambda d: d.move_to(
                axes_3d.c2p(wave_tracker.get_value(),
                            np.sin(2*wave_tracker.get_value()),
                            np.cos(2*wave_tracker.get_value()))
            )
        )
        self.play(wave_tracker.animate.set_value(np.pi), run_time=3, rate_func=linear)
        self.wait(0.2)

        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(1.5)
        self.stop_ambient_camera_rotation()

        gold_dot.clear_updaters()
        self.play(
            physics_wave.animate.scale(1.2).set_stroke(width=8),
            run_time=0.5
        )
        self.play(physics_wave.animate.scale(0.8), run_time=0.3)
        self.wait(0.2)

        dna_group, gold_dna_dot = self.create_dna_with_gold(
            COLOR_NAVY_BLUE, COLOR_DEEP_RED, COLOR_GOLD,
            num_steps=24, radius=1.2, height_step=0.2
        )
        dna_group.center().shift(axes_3d.get_center() - ORIGIN)

        self.play(
            FadeOut(axes_3d), FadeOut(physics_wave),
            GrowFromCenter(dna_group),
            ReplacementTransform(gold_dot, gold_dna_dot),
            run_time=2
        )
        self.wait(0.2)

        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=1.5)
        self.move_camera(zoom=1.1, run_time=4)
        self.play(
            Rotate(dna_group, angle=2 * np.pi, axis=OUT),
            run_time=4, rate_func=linear
        )
        self.move_camera(zoom=1.0, run_time=0.5)
        self.wait(0.3)

        gold_center = gold_dna_dot.get_center()
        self.play(
            Rotate(dna_group, angle=4*PI, rate_func=linear, run_time=1.5),
            dna_group.animate.scale(0.3).move_to(gold_center),
        )
        self.wait(0.1)

        nucleus = VGroup(
            Dot(color=COLOR_DEEP_RED, radius=0.15).shift(UP*0.05 + RIGHT*0.05),
            Dot(color=COLOR_NAVY_BLUE, radius=0.15).shift(DOWN*0.05 + LEFT*0.05),
            Dot(color=COLOR_NAVY_BLUE, radius=0.15).shift(UP*0.07 + LEFT*0.06),
            Dot(color=COLOR_DEEP_RED, radius=0.15).shift(DOWN*0.07 + RIGHT*0.06)
        ).move_to(gold_center)

        orbit1 = Ellipse(width=5.0, height=1.5, stroke_color=COLOR_NAVY_BLUE, stroke_width=1.5).rotate(15 * DEGREES).move_to(gold_center)
        orbit2 = Ellipse(width=5.0, height=1.5, stroke_color=COLOR_NAVY_BLUE, stroke_width=1.5).rotate(-45 * DEGREES).move_to(gold_center)
        orbit3 = Ellipse(width=5.0, height=1.5, stroke_color=COLOR_NAVY_BLUE, stroke_width=1.5).rotate(75 * DEGREES).move_to(gold_center)
        orbits = VGroup(orbit1, orbit2, orbit3)

        self.play(
            ReplacementTransform(dna_group, nucleus),
            Create(orbits),
            run_time=1.5
        )

        e_tracker = ValueTracker(0)
        electron_gold = always_redraw(
            lambda: Dot(orbit1.point_from_proportion(e_tracker.get_value() % 1.0),
                        color=COLOR_GOLD, radius=0.12)
        )
        electron_red = always_redraw(
            lambda: Dot(orbit2.point_from_proportion((e_tracker.get_value() + 0.3) % 1.0),
                        color=COLOR_DEEP_RED, radius=0.12)
        )
        electron_green = always_redraw(
            lambda: Dot(orbit3.point_from_proportion((e_tracker.get_value() + 0.6) % 1.0),
                        color=COLOR_SOFT_GREEN, radius=0.12)
        )

        self.play(
            FadeIn(electron_gold), FadeIn(electron_red), FadeIn(electron_green),
            run_time=0.5
        )
        self.play(e_tracker.animate.set_value(1), run_time=1.5, rate_func=linear)
        self.wait(0.2)

        self.play(e_tracker.animate.set_value(8), run_time=1.0, rate_func=linear)
        self.play(
            FadeOut(nucleus), FadeOut(orbits),
            FadeOut(electron_red), FadeOut(electron_green),
            run_time=0.5
        )
        electron_gold.clear_updaters()
        last_pos = electron_gold.get_center()

        layer_sizes = [3, 4, 2]
        neurons, connections, neuron_positions = self.create_neural_network(layer_sizes)

        self.play(
            LaggedStart(
                *[GrowFromCenter(n) for n in neurons],
                lag_ratio=0.1,
                run_time=1.5
            ),
            Create(connections, run_time=1.5),
            electron_gold.animate.move_to(neuron_positions[0][0]),
            run_time=2
        )

        signal_path = self.get_signal_path(neuron_positions, 0, 0)
        for _ in range(4):
            self.play(MoveAlongPath(electron_gold, signal_path), run_time=0.5)
        self.wait(0.2)

        self.play(FadeOut(neurons), FadeOut(connections), run_time=1)

        econ_axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 6, 1],
            x_length=5, y_length=5,
            axis_config={"color": COLOR_NAVY_BLUE}
        ).center().shift(DOWN * 0.3)
        axis_labels = econ_axes.get_axis_labels(x_label="Q", y_label="P")

        demand_curve = econ_axes.plot(
            lambda x: -x + 5, x_range=[0.5, 4.5],
            color=COLOR_DEEP_RED, stroke_width=4
        )
        demand_label = MathTex("D", color=COLOR_DEEP_RED).next_to(demand_curve.get_end(), UR, buff=0.1)

        s_tracker = ValueTracker(1.0)
        supply_curve = always_redraw(
            lambda: econ_axes.plot(
                lambda x: x + s_tracker.get_value(),
                x_range=[0.5, 4.5],
                color=COLOR_SOFT_GREEN, stroke_width=4
            )
        )
        equilibrium_dot = always_redraw(
            lambda: Dot(
                econ_axes.c2p((5 - s_tracker.get_value()) / 2,
                               (5 + s_tracker.get_value()) / 2),
                color=COLOR_GOLD, radius=0.15
            )
        )

        self.play(
            Create(econ_axes), FadeIn(axis_labels),
            Create(demand_curve), Write(demand_label),
            Create(supply_curve),
            ReplacementTransform(electron_gold, equilibrium_dot),
            run_time=2
        )
        self.wait(0.2)

        self.play(s_tracker.animate.set_value(-0.5), run_time=3.5, rate_func=linear)
        self.play(Flash(equilibrium_dot, color=COLOR_GOLD, line_length=0.2), run_time=0.3)
        self.wait(0.6)

        self.play(
            FadeOut(econ_axes), FadeOut(axis_labels),
            FadeOut(demand_curve), FadeOut(demand_label),
            FadeOut(supply_curve),
            equilibrium_dot.animate.scale(10),
            run_time=1.5
        )

        self.camera.background_color = COLOR_OFF_WHITE
        flash2 = Flash(ORIGIN, color=COLOR_OFF_WHITE, flash_radius=5)
        self.play(flash2, run_time=0.5)
        self.remove(equilibrium_dot, logo_opening)

        quote_line1 = Text(
            "MATH IS VISUAL.", font=FONT_TITLE, weight=BOLD,
            font_size=46, color=COLOR_NAVY_BLUE
        ).center().shift(UP * 0.5)
        quote_line2 = Text(
            "WE PROVE IT.", font=FONT_TITLE, weight=BOLD,
            font_size=54, color=COLOR_DEEP_RED
        ).next_to(quote_line1, DOWN, buff=0.4)

        self.play(Write(quote_line1, run_time=1.5))
        self.play(Write(quote_line2, run_time=1.5))
        quote_group = VGroup(quote_line1, quote_line2)
        self.play(quote_group.animate.scale(1.08), rate_func=wiggle, run_time=1.5)
        self.wait(1)

        final_logo = get_loragica_logo(scale_factor=1.0).center().shift(DOWN * 1.5)
        tagline = Text(
            "LEARN · SEE · CONNECT", font=FONT_TAGLINE, weight=MEDIUM,
            font_size=16, color=COLOR_NAVY_BLUE
        ).next_to(final_logo, DOWN, buff=0.4)

        self.play(
            quote_line1.animate.shift(UP * 1.0).scale(0.8),
            quote_line2.animate.shift(UP * 1.0).scale(0.8),
            LaggedStart(
                *[DrawBorderThenFill(sq) if sq.fill_opacity > 0 else Create(sq)
                  for sq in final_logo],
                run_time=1.5,
                lag_ratio=0.2
            ),
            FadeIn(tagline, shift=UP * 0.2, run_time=1.5)
        )
        self.wait(4)

    def create_dna_with_gold(self, color1, color2, gold_color, num_steps, radius, height_step):
        dna = VGroup()
        gold_pos = None
        for i in range(num_steps):
            angle = i * 0.4
            z = (i - num_steps/2) * height_step
            x1 = radius * np.cos(angle)
            y1 = radius * np.sin(angle)
            x2 = radius * np.cos(angle + np.pi)
            y2 = radius * np.sin(angle + np.pi)
            p1 = np.array([x1, y1, z])
            p2 = np.array([x2, y2, z])
            dot1 = Dot3D(point=p1, color=color1, radius=0.08)
            dot2 = Dot3D(point=p2, color=color2, radius=0.08)
            rung = Line(p1, p2, stroke_color=COLOR_GOLD, stroke_width=2, stroke_opacity=0.6)
            dna.add(dot1, dot2, rung)
            if i == num_steps//2:
                gold_pos = (p1 + p2) / 2
        gold_dot = Dot3D(point=gold_pos, color=gold_color, radius=0.12)
        dna.add(gold_dot)
        return dna, gold_dot

    def create_neural_network(self, layer_sizes):
        neurons = VGroup()
        connections = VGroup()
        neuron_positions = []
        for i, size in enumerate(layer_sizes):
            x = (i - 1) * 2.5
            layer_neurons = []
            for j in range(size):
                y = (j - (size - 1) / 2) * 1.2
                pos = np.array([x, y, 0])
                layer_neurons.append(pos)
                dot = Dot(point=pos, color=COLOR_NAVY_BLUE, radius=0.15)
                neurons.add(dot)
            neuron_positions.append(layer_neurons)
        for i in range(len(layer_sizes) - 1):
            for p1 in neuron_positions[i]:
                for p2 in neuron_positions[i+1]:
                    line = Line(p1, p2, stroke_color=COLOR_GRID_DOT, stroke_width=2)
                    connections.add(line)
        return neurons, connections, neuron_positions

    def get_signal_path(self, neuron_positions, from_layer, from_idx):
        p1 = neuron_positions[from_layer][from_idx]
        p2 = neuron_positions[from_layer+1][0]
        return Line(p1, p2, stroke_color=COLOR_GOLD, stroke_width=4)
