"""
MoviePy Overlay Animations Library
Pre-defined animations for overlays, perfect for soccer score graphics
"""

import numpy as np
from moviepy.editor import VideoClip, CompositeVideoClip


class Easing:
    """Easing functions for smooth animations"""

    @staticmethod
    def linear(t):
        """Linear easing (no easing)"""
        return t

    @staticmethod
    def ease_in_quad(t):
        """Quadratic ease in (slow start)"""
        return t * t

    @staticmethod
    def ease_out_quad(t):
        """Quadratic ease out (slow end)"""
        return t * (2 - t)

    @staticmethod
    def ease_in_out_quad(t):
        """Quadratic ease in-out (slow start and end)"""
        return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t

    @staticmethod
    def ease_in_cubic(t):
        """Cubic ease in"""
        return t * t * t

    @staticmethod
    def ease_out_cubic(t):
        """Cubic ease out"""
        return (t - 1) * (t - 1) * (t - 1) + 1

    @staticmethod
    def ease_in_out_cubic(t):
        """Cubic ease in-out"""
        return 4 * t * t * t if t < 0.5 else (t - 1) * (2 * t - 2) * (2 * t - 2) + 1

    @staticmethod
    def ease_in_quart(t):
        """Quartic ease in"""
        return t * t * t * t

    @staticmethod
    def ease_out_quart(t):
        """Quartic ease out"""
        t_minus_1 = t - 1
        return 1 - t_minus_1 * t_minus_1 * t_minus_1 * t_minus_1

    @staticmethod
    def ease_in_out_quart(t):
        """Quartic ease in-out"""
        if t < 0.5:
            return 8 * t * t * t * t
        else:
            t_minus_1 = t - 1
            return 1 - 8 * t_minus_1 * t_minus_1 * t_minus_1 * t_minus_1

    @staticmethod
    def ease_in_expo(t):
        """Exponential ease in"""
        return 0 if t == 0 else 2 ** (10 * (t - 1))

    @staticmethod
    def ease_out_expo(t):
        """Exponential ease out"""
        return 1 if t == 1 else 1 - 2 ** (-10 * t)

    @staticmethod
    def ease_in_out_expo(t):
        """Exponential ease in-out"""
        if t == 0 or t == 1:
            return t
        if t < 0.5:
            return 2 ** (20 * t - 10) / 2
        return (2 - 2 ** (-20 * t + 10)) / 2

    @staticmethod
    def ease_in_back(t):
        """Back ease in (overshoots then returns)"""
        c1 = 1.70158
        c3 = c1 + 1
        return c3 * t * t * t - c1 * t * t

    @staticmethod
    def ease_out_back(t):
        """Back ease out (overshoots then returns)"""
        c1 = 1.70158
        c3 = c1 + 1
        return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)

    @staticmethod
    def ease_in_out_back(t):
        """Back ease in-out"""
        c1 = 1.70158
        c2 = c1 * 1.525
        if t < 0.5:
            return (pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2
        return (pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2

    @staticmethod
    def ease_in_elastic(t):
        """Elastic ease in (spring effect)"""
        c4 = (2 * np.pi) / 3
        if t == 0 or t == 1:
            return t
        return -(2 ** (10 * t - 10)) * np.sin((t * 10 - 10.75) * c4)

    @staticmethod
    def ease_out_elastic(t):
        """Elastic ease out (spring effect)"""
        c4 = (2 * np.pi) / 3
        if t == 0 or t == 1:
            return t
        return 2 ** (-10 * t) * np.sin((t * 10 - 0.75) * c4) + 1

    @staticmethod
    def ease_in_out_elastic(t):
        """Elastic ease in-out"""
        c5 = (2 * np.pi) / 4.5
        if t == 0 or t == 1:
            return t
        if t < 0.5:
            return -(2 ** (20 * t - 10) * np.sin((20 * t - 11.125) * c5)) / 2
        return (2 ** (-20 * t + 10) * np.sin((20 * t - 11.125) * c5)) / 2 + 1

    @staticmethod
    def ease_out_bounce(t):
        """Bounce ease out"""
        n1 = 7.5625
        d1 = 2.75
        if t < 1 / d1:
            return n1 * t * t
        elif t < 2 / d1:
            t = t - 1.5 / d1
            return n1 * t * t + 0.75
        elif t < 2.5 / d1:
            t = t - 2.25 / d1
            return n1 * t * t + 0.9375
        else:
            t = t - 2.625 / d1
            return n1 * t * t + 0.984375

    @staticmethod
    def ease_in_bounce(t):
        """Bounce ease in"""
        return 1 - Easing.ease_out_bounce(1 - t)

    @staticmethod
    def ease_in_out_bounce(t):
        """Bounce ease in-out"""
        if t < 0.5:
            return (1 - Easing.ease_out_bounce(1 - 2 * t)) / 2
        return (1 + Easing.ease_out_bounce(2 * t - 1)) / 2


class OverlayAnimations:
    """Collection of reusable animations for MoviePy clips"""

    @staticmethod
    def fade_in(clip, duration=0.5, easing=None):
        """Fade in animation with easing support"""
        if easing is None:
            easing = Easing.linear

        def opacity(t):
            if t >= duration:
                return 1
            progress = easing(t / duration)
            return progress

        return clip.set_opacity(opacity)

    @staticmethod
    def fade_out(clip, duration=0.5, easing=None):
        """Fade out animation with easing support"""
        if easing is None:
            easing = Easing.linear

        start_time = clip.duration - duration

        def opacity(t):
            if t < start_time:
                return 1
            progress = easing((t - start_time) / duration)
            return 1 - progress

        return clip.set_opacity(opacity)

    @staticmethod
    def slide_in_from_top(clip, duration=0.5, easing=None):
        """Slide in from top of screen with easing"""
        if easing is None:
            easing = Easing.ease_out_quad

        w, h = clip.size

        def pos(t):
            if t >= duration:
                return ("center", 0)
            progress = easing(t / duration)
            return ("center", -h + h * progress)

        return clip.set_position(pos)

    @staticmethod
    def slide_in_from_bottom(clip, duration=0.5, easing=None):
        """Slide in from bottom of screen with easing"""
        if easing is None:
            easing = Easing.ease_out_quad

        w, h = clip.size

        def pos(t):
            if t >= duration:
                return ("center", 0)
            progress = easing(t / duration)
            return ("center", lambda screen_h: screen_h - (screen_h - 0) * progress)

        return clip.set_position(pos)

    @staticmethod
    def slide_in_from_left(clip, duration=0.5, easing=None):
        """Slide in from left side with easing"""
        if easing is None:
            easing = Easing.ease_out_quad

        w, h = clip.size

        def pos(t):
            if t >= duration:
                return (0, "center")
            progress = easing(t / duration)
            return (-w + w * progress, "center")

        return clip.set_position(pos)

    @staticmethod
    def slide_in_from_right(clip, duration=0.5, easing=None):
        """Slide in from right side with easing"""
        if easing is None:
            easing = Easing.ease_out_quad

        w, h = clip.size

        def pos(t):
            if t >= duration:
                return (lambda screen_w: screen_w - w, "center")
            progress = easing(t / duration)
            return (lambda screen_w: screen_w - w * progress, "center")

        return clip.set_position(pos)

    @staticmethod
    def slide_out_to_top(clip, duration=0.5, easing=None):
        """Slide out to top of screen with easing"""
        if easing is None:
            easing = Easing.ease_in_quad

        w, h = clip.size
        start_time = clip.duration - duration

        def pos(t):
            if t < start_time:
                return ("center", 0)
            progress = easing((t - start_time) / duration)
            return ("center", -h * progress)

        return clip.set_position(pos)

    @staticmethod
    def slide_out_to_bottom(clip, duration=0.5, easing=None):
        """Slide out to bottom of screen with easing"""
        if easing is None:
            easing = Easing.ease_in_quad

        start_time = clip.duration - duration

        def pos(t):
            if t < start_time:
                return ("center", 0)
            progress = easing((t - start_time) / duration)
            return ("center", lambda h: h * progress)

        return clip.set_position(pos)

    @staticmethod
    def zoom_in(clip, duration=0.5, scale_start=0.5, easing=None):
        """Zoom in effect with easing"""
        if easing is None:
            easing = Easing.ease_out_cubic

        def resize(t):
            if t >= duration:
                return 1
            progress = easing(t / duration)
            scale = scale_start + (1 - scale_start) * progress
            return scale

        return clip.resize(resize)

    @staticmethod
    def zoom_out(clip, duration=0.5, scale_end=0.5, easing=None):
        """Zoom out effect with easing"""
        if easing is None:
            easing = Easing.ease_in_cubic

        start_time = clip.duration - duration

        def resize(t):
            if t < start_time:
                return 1
            progress = easing((t - start_time) / duration)
            scale = 1 - (1 - scale_end) * progress
            return scale

        return clip.resize(resize)

    @staticmethod
    def bounce_in(clip, duration=0.8, easing=None):
        """Bounce in effect with easing (uses bounce easing by default)"""
        if easing is None:
            easing = Easing.ease_out_bounce

        w, h = clip.size

        def pos(t):
            if t >= duration:
                return ("center", 0)
            progress = easing(t / duration)
            return ("center", -h + h * progress)

        return clip.set_position(pos)

    @staticmethod
    def pulse(clip, duration=0.5, scale_max=1.1, easing=None):
        """Pulse/heartbeat effect with easing"""
        if easing is None:
            # Use custom sine wave for natural pulse
            easing = lambda t: np.sin(t * np.pi)

        def resize(t):
            if t >= duration:
                return 1
            progress = easing(t / duration)
            scale = 1 + (scale_max - 1) * progress
            return scale

        return clip.resize(resize)

    @staticmethod
    def shake(clip, duration=0.3, intensity=5):
        """Shake effect (good for goal notifications)"""
        original_pos = clip.pos

        def pos(t):
            if t < duration:
                # Random shake
                shake_x = np.random.randint(-intensity, intensity)
                shake_y = np.random.randint(-intensity, intensity)
                if callable(original_pos):
                    base_pos = original_pos(t)
                else:
                    base_pos = original_pos

                if isinstance(base_pos, tuple):
                    x = base_pos[0] if not callable(base_pos[0]) else base_pos[0]
                    y = base_pos[1] if not callable(base_pos[1]) else base_pos[1]
                    return (
                        x + shake_x if not callable(x) else lambda w: x(w) + shake_x,
                        y + shake_y if not callable(y) else lambda h: y(h) + shake_y,
                    )
                return base_pos
            return original_pos

        return clip.set_position(pos)

    @staticmethod
    def flip_in(clip, duration=0.5, axis="horizontal"):
        """Flip in effect (3D rotation simulation)"""

        def resize(t):
            if t >= duration:
                return 1
            progress = t / duration
            if axis == "horizontal":
                # Simulate horizontal flip by scaling width
                scale = abs(np.cos(progress * np.pi / 2))
                return (scale if scale > 0.1 else 0.1, 1)
            else:
                # Simulate vertical flip by scaling height
                scale = abs(np.cos(progress * np.pi / 2))
                return (1, scale if scale > 0.1 else 0.1)

        return clip.resize(resize)

    @staticmethod
    def wipe_in(clip, duration=0.5, direction="left"):
        """Wipe in effect"""
        w, h = clip.size

        def make_frame(t):
            frame = clip.get_frame(t)
            if t >= duration:
                return frame

            progress = t / duration
            if direction == "left":
                # Wipe from left to right
                mask_width = int(w * progress)
                mask = np.zeros((h, w, 3), dtype=np.uint8)
                mask[:, :mask_width] = 255
                return np.where(mask > 0, frame, 0)
            elif direction == "right":
                # Wipe from right to left
                mask_width = int(w * progress)
                mask = np.zeros((h, w, 3), dtype=np.uint8)
                mask[:, -mask_width:] = 255
                return np.where(mask > 0, frame, 0)
            return frame

        return clip.fl(lambda gf, t: make_frame(t))

    @staticmethod
    def combine_animations(clip, *animation_configs):
        """
        Apply multiple animations in sequence, waiting for each to finish before starting the next

        Args:
            clip: The clip to animate
            *animation_configs: Tuples of (animation_function, duration, **kwargs) or just animation_function
                               If just function, duration defaults to 0.5 seconds

        Example:
            combine_animations(
                clip,
                (OverlayAnimations.fade_in, 0.5, {'easing': Easing.ease_out_quad}),
                (OverlayAnimations.slide_in_from_top, 0.8, {'easing': Easing.ease_out_bounce}),
                (OverlayAnimations.pulse, 0.3, {'scale_max': 1.2})
            )
        """
        if not animation_configs:
            return clip

        # Parse animation configurations
        parsed_configs = []
        total_duration = 0

        for config in animation_configs:
            if callable(config):
                # Just a function, use default duration
                parsed_configs.append((config, 0.5, {}))
                total_duration += 0.5
            elif isinstance(config, tuple) and len(config) >= 2:
                func, duration = config[0], config[1]
                kwargs = config[2] if len(config) > 2 else {}
                parsed_configs.append((func, duration, kwargs))
                total_duration += duration
            else:
                raise ValueError(
                    "Animation config must be callable or tuple (func, duration, kwargs)"
                )

        # Create a new clip with the total duration
        result_clip = clip.set_duration(total_duration)

        # Apply animations sequentially by time segments
        current_time = 0

        for i, (animation_func, duration, kwargs) in enumerate(parsed_configs):
            # Create a temporary clip for this animation segment
            segment_clip = clip.set_duration(duration)

            # Apply the animation to the segment
            animated_segment = animation_func(segment_clip, duration=duration, **kwargs)

            # Set the timing for this segment
            animated_segment = animated_segment.set_start(current_time)

            if i == 0:
                # First animation becomes the base
                result_clip = animated_segment
            else:
                # Composite subsequent animations
                from moviepy.editor import CompositeVideoClip

                result_clip = CompositeVideoClip([result_clip, animated_segment])

            current_time += duration

        return result_clip

    @staticmethod
    def goal_notification_sequence(
        clip,
        slide_duration=1.2,
        display_duration=3.0,
        entrance_easing=None,
        exit_easing=None,
    ):
        """
        Complete goal notification animation: slide down, stay, slide up

        Args:
            clip: The clip to animate
            slide_duration: Duration for slide in/out animations
            display_duration: Duration to display in static position
            entrance_easing: Easing function for entrance (default: ease_out_bounce)
            exit_easing: Easing function for exit (default: ease_in_back)
        """
        if entrance_easing is None:
            entrance_easing = Easing.ease_out_bounce
        if exit_easing is None:
            exit_easing = Easing.ease_in_back

        w, h = clip.size
        total_duration = 2 * slide_duration + display_duration

        def goal_position(t):
            if t <= slide_duration:
                # Phase 1: Slide down from top
                progress = t / slide_duration
                eased_progress = entrance_easing(progress)
                y_offset = -h * (1 - eased_progress)
                return (0, y_offset)
            elif t <= (slide_duration + display_duration):
                # Phase 2: Stay in position
                return (0, 0)
            else:
                # Phase 3: Slide up and disappear
                slide_start = slide_duration + display_duration
                progress = (t - slide_start) / slide_duration
                progress = min(1.0, progress)
                eased_progress = exit_easing(progress)
                y_offset = -h * eased_progress
                return (0, y_offset)

        return clip.set_position(goal_position)

    @staticmethod
    def slide_down_and_up(
        clip, slide_duration=1.0, pause_duration=0.5, easing=None, base_position=None
    ):
        """
        Slide clip down by its own height, pause, then slide back up

        Args:
            clip: The clip to animate
            slide_duration: Duration for each slide movement (down and up)
            pause_duration: Duration to pause at the bottom position
            easing: Easing function for both movements (default: ease_in_out_quad)
            base_position: Base position (x, y) to animate from. If None, uses clip's current position

        Returns:
            Animated clip that slides down and back up
        """
        if easing is None:
            easing = Easing.ease_in_out_quad

        w, h = clip.size
        total_duration = 2 * slide_duration + pause_duration

        # Use provided base position or fall back to clip's current position
        if base_position is not None:
            base_x, base_y = base_position
        else:
            original_pos = clip.pos if hasattr(clip, "pos") else (0, 0)
            if callable(original_pos):
                # For callable positions, we'll evaluate at t=0 to get the base
                base_x, base_y = original_pos(0)
            else:
                base_x, base_y = original_pos

        def slide_down_up_position(t):
            if t <= slide_duration:
                # Phase 1: Slide down
                progress = t / slide_duration
                eased_progress = easing(progress)
                y_offset = h * eased_progress  # Move down by clip height
                return (base_x, base_y + y_offset)

            elif t <= (slide_duration + pause_duration):
                # Phase 2: Pause at bottom
                return (base_x, base_y + h)

            else:
                # Phase 3: Slide back up
                slide_up_start = slide_duration + pause_duration
                progress = (t - slide_up_start) / slide_duration
                progress = min(1.0, progress)
                eased_progress = easing(progress)
                y_offset = h * (1 - eased_progress)  # Move from bottom back to original
                return (base_x, base_y + y_offset)

        return clip.set_position(slide_down_up_position).set_duration(total_duration)


class AnimationPresets:
    """Pre-configured animation combinations for common use cases"""

    @staticmethod
    def smooth_entrance(clip, duration=0.6, easing=None):
        """Smooth fade + slide entrance with easing (sequential)"""
        if easing is None:
            easing = Easing.ease_out_cubic

        # Use sequential animations - first fade in, then slide in
        return OverlayAnimations.combine_animations(
            clip,
            (
                lambda c, **kw: OverlayAnimations.fade_in(c, easing=easing, **kw),
                duration * 0.4,
            ),
            (
                lambda c, **kw: OverlayAnimations.slide_in_from_top(
                    c, easing=easing, **kw
                ),
                duration * 0.6,
            ),
        )

    @staticmethod
    def smooth_entrance_parallel(clip, duration=0.6, easing=None):
        """Smooth fade + slide entrance with easing (parallel - old behavior)"""
        if easing is None:
            easing = Easing.ease_out_cubic
        return OverlayAnimations.combine_animations_parallel(
            clip,
            lambda c: OverlayAnimations.fade_in(c, duration, easing),
            lambda c: OverlayAnimations.slide_in_from_top(c, duration, easing),
        )

    @staticmethod
    def smooth_exit(clip, duration=0.6, easing=None):
        """Smooth fade + slide exit with easing (sequential)"""
        if easing is None:
            easing = Easing.ease_in_cubic

        # Use sequential animations - first slide out, then fade out
        return OverlayAnimations.combine_animations(
            clip,
            (
                lambda c, **kw: OverlayAnimations.slide_out_to_bottom(
                    c, easing=easing, **kw
                ),
                duration * 0.6,
            ),
            (
                lambda c, **kw: OverlayAnimations.fade_out(c, easing=easing, **kw),
                duration * 0.4,
            ),
        )

    @staticmethod
    def score_change_animation(clip, duration=0.8, easing=None):
        """Animation for when score changes (pulse with easing)"""
        if easing is None:
            # Sine wave provides natural pulse
            easing = lambda t: np.sin(t * np.pi)
        return OverlayAnimations.pulse(clip, duration, scale_max=1.15, easing=easing)

    @staticmethod
    def goal_celebration(clip, duration=1.0, easing=None):
        """Exciting goal animation (bounce with easing)"""
        if easing is None:
            easing = Easing.ease_out_bounce
        return OverlayAnimations.bounce_in(clip, duration, easing=easing)

    @staticmethod
    def professional_entrance(clip, duration=0.5, easing=None):
        """Professional slide + fade entrance with easing (sequential)"""
        if easing is None:
            easing = Easing.ease_out_quad

        # Use sequential animations
        return OverlayAnimations.combine_animations(
            clip,
            (
                lambda c, **kw: OverlayAnimations.slide_in_from_left(
                    c, easing=easing, **kw
                ),
                duration * 0.7,
            ),
            (
                lambda c, **kw: OverlayAnimations.fade_in(c, easing=easing, **kw),
                duration * 0.3,
            ),
        )

    @staticmethod
    def peek_down_animation(clip, slide_duration=0.8, pause_duration=0.3, easing=None):
        """
        Convenient preset for peek-down effect
        Slide down by clip height, pause briefly, then slide back up
        """
        if easing is None:
            easing = Easing.ease_in_out_cubic
        return OverlayAnimations.slide_down_and_up(
            clip,
            slide_duration=slide_duration,
            pause_duration=pause_duration,
            easing=easing,
        )


def demo_animations():
    """Demo showing how to use animations with easing"""
    from moviepy.editor import TextClip, ColorClip, VideoFileClip

    # Create a sample overlay
    overlay = (
        TextClip(
            "Barcelona 2 - 1 Real Madrid",
            fontsize=50,
            color="white",
            bg_color="rgba(0,0,0,0.7)",
            font="Arial-Bold",
            method="label",
        )
        .set_duration(5)
        .set_position("center")
    )

    # Apply different animations with easing

    # 1. Smooth entrance with ease-out cubic
    animated_overlay = AnimationPresets.smooth_entrance(
        overlay, duration=0.6, easing=Easing.ease_out_cubic
    )

    # 2. Bounce entrance with elastic easing
    animated_overlay = OverlayAnimations.slide_in_from_top(
        overlay, duration=0.8, easing=Easing.ease_out_elastic
    )

    # 3. Custom zoom with back easing (overshoots)
    animated_overlay = OverlayAnimations.zoom_in(
        overlay, duration=0.6, scale_start=0.3, easing=Easing.ease_out_back
    )

    # 4. Fade in with exponential easing
    animated_overlay = OverlayAnimations.fade_in(
        overlay, duration=0.5, easing=Easing.ease_out_expo
    )

    # 5. Sequential animations with the new combine_animations
    animated_overlay = OverlayAnimations.combine_animations(
        overlay,
        (
            lambda c, **kw: OverlayAnimations.fade_in(
                c, easing=Easing.ease_out_quad, **kw
            ),
            0.5,
        ),
        (
            lambda c, **kw: OverlayAnimations.slide_in_from_top(
                c, easing=Easing.ease_out_back, **kw
            ),
            0.5,
        ),
        (
            lambda c, **kw: OverlayAnimations.pulse(
                c, easing=lambda t: np.sin(t * np.pi), **kw
            ),
            0.3,
        ),
    )

    # 6. Parallel animations (old behavior)
    animated_overlay_parallel = OverlayAnimations.combine_animations_parallel(
        overlay,
        lambda c: OverlayAnimations.fade_in(c, 0.5, Easing.ease_out_quad),
        lambda c: OverlayAnimations.slide_in_from_top(c, 0.5, Easing.ease_out_back),
    )

    return animated_overlay
