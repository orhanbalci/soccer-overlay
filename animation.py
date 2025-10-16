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
        return -2 ** (10 * t - 10) * np.sin((t * 10 - 10.75) * c4)
    
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
                return ('center', 0)
            progress = easing(t / duration)
            return ('center', -h + h * progress)
        return clip.set_position(pos)
    
    @staticmethod
    def slide_in_from_bottom(clip, duration=0.5, easing=None):
        """Slide in from bottom of screen with easing"""
        if easing is None:
            easing = Easing.ease_out_quad
        
        w, h = clip.size
        def pos(t):
            if t >= duration:
                return ('center', 0)
            progress = easing(t / duration)
            return ('center', lambda screen_h: screen_h - (screen_h - 0) * progress)
        return clip.set_position(pos)
    
    @staticmethod
    def slide_in_from_left(clip, duration=0.5, easing=None):
        """Slide in from left side with easing"""
        if easing is None:
            easing = Easing.ease_out_quad
        
        w, h = clip.size
        def pos(t):
            if t >= duration:
                return (0, 'center')
            progress = easing(t / duration)
            return (-w + w * progress, 'center')
        return clip.set_position(pos)
    
    @staticmethod
    def slide_in_from_right(clip, duration=0.5, easing=None):
        """Slide in from right side with easing"""
        if easing is None:
            easing = Easing.ease_out_quad
        
        w, h = clip.size
        def pos(t):
            if t >= duration:
                return (lambda screen_w: screen_w - w, 'center')
            progress = easing(t / duration)
            return (lambda screen_w: screen_w - w * progress, 'center')
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
                return ('center', 0)
            progress = easing((t - start_time) / duration)
            return ('center', -h * progress)
        return clip.set_position(pos)
    
    @staticmethod
    def slide_out_to_bottom(clip, duration=0.5, easing=None):
        """Slide out to bottom of screen with easing"""
        if easing is None:
            easing = Easing.ease_in_quad
        
        start_time = clip.duration - duration
        def pos(t):
            if t < start_time:
                return ('center', 0)
            progress = easing((t - start_time) / duration)
            return ('center', lambda h: h * progress)
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
                return ('center', 0)
            progress = easing(t / duration)
            return ('center', -h + h * progress)
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
                    return (x + shake_x if not callable(x) else lambda w: x(w) + shake_x,
                            y + shake_y if not callable(y) else lambda h: y(h) + shake_y)
                return base_pos
            return original_pos
        return clip.set_position(pos)
    
    @staticmethod
    def flip_in(clip, duration=0.5, axis='horizontal'):
        """Flip in effect (3D rotation simulation)"""
        def resize(t):
            if t >= duration:
                return 1
            progress = t / duration
            if axis == 'horizontal':
                # Simulate horizontal flip by scaling width
                scale = abs(np.cos(progress * np.pi / 2))
                return (scale if scale > 0.1 else 0.1, 1)
            else:
                # Simulate vertical flip by scaling height
                scale = abs(np.cos(progress * np.pi / 2))
                return (1, scale if scale > 0.1 else 0.1)
        return clip.resize(resize)
    
    @staticmethod
    def wipe_in(clip, duration=0.5, direction='left'):
        """Wipe in effect"""
        w, h = clip.size
        def make_frame(t):
            frame = clip.get_frame(t)
            if t >= duration:
                return frame
            
            progress = t / duration
            if direction == 'left':
                # Wipe from left to right
                mask_width = int(w * progress)
                mask = np.zeros((h, w, 3), dtype=np.uint8)
                mask[:, :mask_width] = 255
                return np.where(mask > 0, frame, 0)
            elif direction == 'right':
                # Wipe from right to left
                mask_width = int(w * progress)
                mask = np.zeros((h, w, 3), dtype=np.uint8)
                mask[:, -mask_width:] = 255
                return np.where(mask > 0, frame, 0)
            return frame
        
        return clip.fl(lambda gf, t: make_frame(t))
    
    @staticmethod
    def combine_animations(clip, *animations):
        """Apply multiple animations in sequence"""
        result = clip
        for animation_func in animations:
            result = animation_func(result)
        return result
    
    @staticmethod
    def goal_notification_sequence(clip, slide_duration=1.2, display_duration=3.0, entrance_easing=None, exit_easing=None):
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
    def slide_down_and_up(clip, slide_duration=1.0, pause_duration=0.5, easing=None, base_position=None):
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
            original_pos = clip.pos if hasattr(clip, 'pos') else (0, 0)
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
        """Smooth fade + slide entrance with easing"""
        if easing is None:
            easing = Easing.ease_out_cubic
        return OverlayAnimations.combine_animations(
            clip,
            lambda c: OverlayAnimations.fade_in(c, duration, easing),
            lambda c: OverlayAnimations.slide_in_from_top(c, duration, easing)
        )
    
    @staticmethod
    def smooth_exit(clip, duration=0.6, easing=None):
        """Smooth fade + slide exit with easing"""
        if easing is None:
            easing = Easing.ease_in_cubic
        return OverlayAnimations.combine_animations(
            clip,
            lambda c: OverlayAnimations.fade_out(c, duration, easing),
            lambda c: OverlayAnimations.slide_out_to_bottom(c, duration, easing)
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
        """Professional slide + fade entrance with easing"""
        if easing is None:
            easing = Easing.ease_out_quad
        return OverlayAnimations.combine_animations(
            clip,
            lambda c: OverlayAnimations.slide_in_from_left(c, duration, easing),
            lambda c: OverlayAnimations.fade_in(c, duration * 0.7, easing)
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
            easing=easing
        )

    """Demo showing how to use animations with easing"""
    from moviepy.editor import TextClip, ColorClip, VideoFileClip
    
    # Create a sample overlay
    overlay = TextClip(
        "Barcelona 2 - 1 Real Madrid",
        fontsize=50,
        color='white',
        bg_color='rgba(0,0,0,0.7)',
        font='Arial-Bold',
        method='label'
    ).set_duration(5).set_position('center')
    
    # Apply different animations with easing
    
    # 1. Smooth entrance with ease-out cubic
    animated_overlay = AnimationPresets.smooth_entrance(
        overlay, 
        duration=0.6, 
        easing=Easing.ease_out_cubic
    )
    
    # 2. Bounce entrance with elastic easing
    animated_overlay = OverlayAnimations.slide_in_from_top(
        overlay,
        duration=0.8,
        easing=Easing.ease_out_elastic
    )
    
    # 3. Custom zoom with back easing (overshoots)
    animated_overlay = OverlayAnimations.zoom_in(
        overlay,
        duration=0.6,
        scale_start=0.3,
        easing=Easing.ease_out_back
    )
    
    # 4. Fade in with exponential easing
    animated_overlay = OverlayAnimations.fade_in(
        overlay,
        duration=0.5,
        easing=Easing.ease_out_expo
    )
    
    # 5. Combine multiple animations with different easings
    animated_overlay = OverlayAnimations.combine_animations(
        overlay,
        lambda c: OverlayAnimations.fade_in(c, 0.5, Easing.ease_out_quad),
        lambda c: OverlayAnimations.slide_in_from_top(c, 0.5, Easing.ease_out_back),
        lambda c: OverlayAnimations.pulse(c, 0.3, easing=lambda t: np.sin(t * np.pi))
    )
    
    return animated_overlay