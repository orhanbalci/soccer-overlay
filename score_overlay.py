"""
Soccer Score Overlay System
Overlays score information onto soccer match videos based on goal times

Player positions are available through the PlayerPosition enum in overlay_types.py.
See overlay_types.PlayerPosition for all available position abbreviations.
"""

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
from datetime import timedelta
from animation import OverlayAnimations, Easing
from overlay_types import PlayerPosition

class SoccerScoreOverlay:
    # ========== CONFIGURATION PARAMETERS ==========
    # All customizable parameters are defined here for easy modification
    
    # Responsive design breakpoints
    LOW_RES_THRESHOLD = 720     # Video width <= 720px
    MEDIUM_RES_THRESHOLD = 1280 # Video width <= 1280px
    
    # Scoreboard dimensions (for different resolutions)
    # Format: {resolution: (height, team_box_width, score_box_width, accent_width)}
    DIMENSIONS = {
        'low': (36, 100, 80, 4),      # Low resolution (≤720px)
        'medium': (46, 120, 100, 5),  # Medium resolution (≤1280px) 
        'high': (58, 160, 140, 6)     # High resolution (>1280px)
    }
    
    # Font sizes (for different resolutions)
    # Format: {resolution: (team_name_size, score_size)}
    FONT_SIZES = {
        'low': (16, 24),     # Low resolution
        'medium': (20, 30),  # Medium resolution
        'high': (28, 40)     # High resolution
    }
    
    # Colors
    TEAM_BOX_COLOR = (40, 0, 70)      # Dark purple background for team boxes
    SCORE_BOX_COLOR = (56, 226, 196)  # Cyan/teal color for score box
    TEXT_COLOR_TEAM = 'white'         # Team name text color
    TEXT_COLOR_SCORE = 'black'        # Score text color
    FONT_FAMILY = 'Arial-Bold'        # Font family for all text
    
    # Layout spacing
    TEXT_MARGIN_FROM_ACCENT = {'low': 10, 'medium': 20, 'high': 20}  # Distance from accent bar to text
    
    # Notification settings
    NOTIFICATION_BACKGROUND_COLOR = (255, 215, 0)  # Gold color for notifications
    NOTIFICATION_TEXT_COLOR = 'black'              # Text color for notifications
    NOTIFICATION_DISPLAY_DURATION = 3.0            # How long to show notifications (seconds)
    NOTIFICATION_ANIMATION_DURATION = 3.0          # Duration for slide animations (seconds)
    
    # Lineup overlay settings
    LINEUP_BACKGROUND_COLOR = (0, 0, 0, 200)       # Semi-transparent black background
    LINEUP_NAME_BOX_COLOR = (56, 226, 196)         # Color for player name boxes (defaults to SCORE_BOX_COLOR)
    LINEUP_TEAM_TEXT_COLOR = 'white'               # Team name text color
    LINEUP_PLAYER_TEXT_COLOR = 'white'             # Player text color
    LINEUP_DIRECTOR_TEXT_COLOR = 'white'          # Director text color
    LINEUP_NUMBER_BOX_COLOR = (40, 0, 70)          # Color for player number boxes (defaults to TEAM_BOX_COLOR)
    LINEUP_DISPLAY_DURATION = 8.0                  # How long to show lineup (seconds)
    LINEUP_ANIMATION_DURATION = 0.5                # Duration for each item slide animation (seconds)
    LINEUP_STAGGER_DELAY = 0.2                     # Delay between each item animation (seconds)
    
    def __init__(self, video_path, team1_name="Team A", team2_name="Team B",
                 team1_color="#FF0000", team2_color="#0000FF",
                 overlay_x_margin=10, overlay_y_margin=10,
                 show_scoreboard=True, show_notifications=True, show_lineups=True):
        """
        Initialize Soccer Score Overlay
        
        Args:
            video_path: Path to the video file
            team1_name: Name of team 1
            team2_name: Name of team 2
            team1_color: Color for team 1 (hex format)
            team2_color: Color for team 2 (hex format)
            overlay_x_margin: Distance from left edge of video
            overlay_y_margin: Distance from top edge of video
            show_scoreboard: Whether to show the scoreboard overlay
            show_notifications: Whether to show notifications
            show_lineups: Whether to show lineup overlays
        """
        self.video_path = video_path
        self.team1_name = team1_name
        self.team2_name = team2_name
        self.team1_color = team1_color
        self.team2_color = team2_color
        self.overlay_x_margin = overlay_x_margin
        self.overlay_y_margin = overlay_y_margin
        self.show_scoreboard = show_scoreboard
        self.show_notifications = show_notifications
        self.show_lineups = show_lineups
        self.video = VideoFileClip(video_path)
        
    def parse_goal_data(self, goals):
        """
        Parse goal data and create score timeline
        
        Args:
            goals: List of dicts with format:
                   [{"time": "12:34", "team": 1}, {"time": "45:20", "team": 2}, ...]
                   or [{"time": 754, "team": 1}, ...] (seconds)
        
        Returns:
            List of (timestamp_seconds, team1_score, team2_score) tuples
        """
        score_timeline = [(0, 0, 0)]  # Start with 0-0
        team1_score = 0
        team2_score = 0
        
        # Sort goals by time
        sorted_goals = sorted(goals, key=lambda x: self._to_seconds(x['time']))
        
        for goal in sorted_goals:
            timestamp = self._to_seconds(goal['time'])
            
            if goal['team'] == 1:
                team1_score += 1
            else:
                team2_score += 1
            
            score_timeline.append((timestamp, team1_score, team2_score))
        
        return score_timeline
    
    def _to_seconds(self, time_str):
        """Convert time string (MM:SS or seconds) to seconds"""
        if isinstance(time_str, (int, float)):
            return float(time_str)
        
        # Handle MM:SS format
        if ':' in str(time_str):
            parts = str(time_str).split(':')
            return int(parts[0]) * 60 + int(parts[1])
        
        return float(time_str)
    
    def create_score_overlay(self, team1_score, team2_score):
        """
        Create a score overlay text clip with team colors
        
        Args:
            team1_score: Score for team 1
            team2_score: Score for team 2
        """
        return self._create_modern_score_overlay(team1_score, team2_score)
    
    def create_notification(self, score_box_width, scoreboard_height, res_category, 
                           notification_text="GOAL", background_color=None, text_color=None, 
                           base_position=None, display_duration=None, animation_duration=None):
        """
        Create a generic notification overlay that appears below the score box
        
        Args:
            score_box_width: Width of the score box
            scoreboard_height: Height of the scoreboard
            res_category: Resolution category ('low', 'medium', 'high')
            notification_text: Text to display in the notification
            background_color: Background color (hex format or RGB tuple). If None, uses default
            text_color: Text color. If None, uses white for better contrast
            base_position: (x, y) tuple for the base position of the animation
            display_duration: How long to show notification (seconds). If None, uses default
            animation_duration: Duration for slide animations (seconds). If None, uses default
        
        Returns:
            Animated clip with notification
        """
        # Get font size for notification text (use score font size)
        _, fontsize_score = self.FONT_SIZES[res_category]
        
        # Use custom durations or fall back to defaults
        disp_duration = display_duration if display_duration is not None else self.NOTIFICATION_DISPLAY_DURATION
        anim_duration = animation_duration if animation_duration is not None else self.NOTIFICATION_ANIMATION_DURATION
        
        # Total duration for the notification
        total_duration = disp_duration + 2 * anim_duration
        
        # Determine background color
        if background_color is None:
            bg_color = self.NOTIFICATION_BACKGROUND_COLOR
        elif isinstance(background_color, str):
            bg_color = self._hex_to_rgb(background_color)
        else:
            bg_color = background_color
        
        # Determine text color
        if text_color is None:
            txt_color = 'white'  # Use white for better contrast
        else:
            txt_color = text_color
        
        # Create notification background
        notification_background = ColorClip(
            size=(score_box_width, scoreboard_height),
            color=bg_color
        ).set_duration(total_duration)
        
        # Create notification text
        notification_text_clip = TextClip(
            notification_text,
            fontsize=fontsize_score,
            color=txt_color,
            font=self.FONT_FAMILY,
            method='label'
        ).set_duration(total_duration)
        
        # Center the text on the background
        text_x = (score_box_width - notification_text_clip.w) // 2
        text_y = (scoreboard_height - notification_text_clip.h) // 2
        text_positioned = notification_text_clip.set_position((text_x, text_y))
        
        # Composite the background and text
        notification_overlay = CompositeVideoClip([
            notification_background,
            text_positioned
        ], size=(score_box_width, scoreboard_height))
        
        # Use the slide down and up animation with the base position
        notification_overlay = OverlayAnimations.slide_down_and_up(
            notification_overlay,
            slide_duration=anim_duration,
            pause_duration=disp_duration,
            easing=Easing.ease_out_bounce,
            base_position=base_position
        )
        
        print(f"Created notification '{notification_text}': duration={total_duration}s, animation_duration={anim_duration}s")
        
        return notification_overlay
    
    def create_lineup_overlay(self, team_name, players, director, team_color, 
                             display_duration=None, animation_duration=None, stagger_delay=None):
        """
        Create a lineup overlay that shows team name, players, and director with staggered animations
        Each item has its own background rectangle styled like the scoreboard
        
        Args:
            team_name: Name of the team
            players: List of dicts with format [{"number": 1, "name": "Player Name", "position": "GK"}, ...]
                    position is optional and should use PlayerPosition enum values (e.g., PlayerPosition.GOALKEEPER.value)
            director: Name of the director/coach
            team_color: Team color (hex format or RGB tuple)
            display_duration: How long to show lineup (seconds). If None, uses default
            animation_duration: Duration for each item slide animation (seconds). If None, uses default
            stagger_delay: Delay between each item animation (seconds). If None, uses default
        
        Returns:
            Animated clip with lineup overlay
        """
        # Use custom durations or fall back to defaults
        disp_duration = display_duration if display_duration is not None else self.LINEUP_DISPLAY_DURATION
        anim_duration = animation_duration if animation_duration is not None else self.LINEUP_ANIMATION_DURATION
        stagger = stagger_delay if stagger_delay is not None else self.LINEUP_STAGGER_DELAY
        
        # Get video dimensions for positioning
        video_width = self.video.w
        video_height = self.video.h
        res_category = self._get_resolution_category(video_width)
        
        # Get scoreboard-style dimensions
        scoreboard_height, team_box_width, score_box_width, accent_width = self.DIMENSIONS[res_category]
        text_margin = self.TEXT_MARGIN_FROM_ACCENT[res_category]
        
        # Calculate dimensions based on resolution
        if res_category == 'low':
            team_font_size = 24
            player_font_size = 18
            director_font_size = 20
            lineup_width = 350
            item_height = scoreboard_height
            padding = 0
            number_box_width = 40
            name_box_width = lineup_width - number_box_width - accent_width
        elif res_category == 'medium':
            team_font_size = 30
            player_font_size = 22
            director_font_size = 26
            lineup_width = 400
            item_height = scoreboard_height
            padding = 0
            number_box_width = 50
            name_box_width = lineup_width - number_box_width - accent_width
        else:  # high
            team_font_size = 38
            player_font_size = 28
            director_font_size = 32
            lineup_width = 500
            item_height = scoreboard_height
            padding = 0
            number_box_width = 60
            name_box_width = lineup_width - number_box_width - accent_width
        
        # Calculate total items and duration
        total_items = 1 + len(players) + 1  # team name + players + director
        total_animation_time = (total_items - 1) * stagger + anim_duration
        total_duration = total_animation_time + disp_duration + anim_duration
        
        lineup_height = (total_items * item_height) + ((total_items - 1) * padding)
        
        # Position the lineup (center of screen)
        lineup_x = (video_width - lineup_width) // 2
        lineup_y = (video_height - lineup_height) // 2
        
        # Determine team color
        if isinstance(team_color, str):
            team_accent_color = self._hex_to_rgb(team_color)
        else:
            team_accent_color = team_color
        
        clips = []
        current_y = 0
        item_index = 0
        
        # Create team name item (with empty number box for consistency)
        team_item = self._create_lineup_player_item(
            player_number="",  # Empty number for team name
            player_name=team_name.upper(),  # Convert to upper case
            player_font_size=team_font_size,
            number_box_width=number_box_width,
            name_box_width=name_box_width,
            height=item_height,
            accent_color=team_accent_color,
            accent_width=accent_width,
            text_margin=text_margin,
            total_duration=total_duration,
            name_text_color=self.LINEUP_TEAM_TEXT_COLOR,
            player_position=""  # No position for team name
        )
        
        team_positioned = team_item.set_position((0, current_y))
        team_animated = self._create_lineup_item_animation(
            team_positioned, lineup_width, current_y,
            item_index * stagger, anim_duration, disp_duration, total_animation_time
        )
        clips.append(team_animated)
        
        current_y += item_height + padding
        item_index += 1
        
        # Create player items (separate number and name boxes)
        for player in players:
            player_position = player.get('position', '')  # Get position or empty string if not provided
            player_item = self._create_lineup_player_item(
                player_number=str(player['number']),
                player_name=self._format_name(player['name']),  # Format with title case first name, upper case surname
                player_position=player_position,  # Add position parameter
                player_font_size=player_font_size,
                number_box_width=number_box_width,
                name_box_width=name_box_width,
                height=item_height,
                accent_color=team_accent_color,
                accent_width=accent_width,
                text_margin=text_margin,
                total_duration=total_duration
            )
            
            player_positioned = player_item.set_position((0, current_y))
            player_animated = self._create_lineup_item_animation(
                player_positioned, lineup_width, current_y,
                item_index * stagger, anim_duration, disp_duration, total_animation_time
            )
            clips.append(player_animated)
            
            current_y += item_height + padding
            item_index += 1
        
        # Create director item (with TD in number box)
        director_item = self._create_lineup_player_item(
            player_number="TD",  # TD for Technical Director
            player_name=self._format_name(director),  # Format with title case first name, upper case surname
            player_font_size=director_font_size,
            number_box_width=number_box_width,
            name_box_width=name_box_width,
            height=item_height,
            accent_color=team_accent_color,
            accent_width=accent_width,
            text_margin=text_margin,
            total_duration=total_duration,
            name_text_color=self.LINEUP_DIRECTOR_TEXT_COLOR,
            player_position=""  # No position for director
        )
        
        director_positioned = director_item.set_position((0, current_y))
        director_animated = self._create_lineup_item_animation(
            director_positioned, lineup_width, current_y,
            item_index * stagger, anim_duration, disp_duration, total_animation_time
        )
        clips.append(director_animated)
        
        # Composite all elements
        lineup_overlay = CompositeVideoClip(clips, size=(lineup_width, lineup_height))
        
        # Position the entire lineup on screen
        lineup_overlay = lineup_overlay.set_position((lineup_x, lineup_y))
        
        print(f"Created lineup for '{team_name}': {len(players)} players, duration={total_duration}s")
        
        return lineup_overlay
    
    def _create_lineup_item_animation(self, clip, container_width, final_y, start_delay, 
                                    anim_duration, display_duration, total_animation_time):
        """
        Create slide-in animation for a lineup item
        
        Args:
            clip: The text clip to animate
            container_width: Width of the container
            final_y: Final Y position of the item
            start_delay: When to start the animation
            anim_duration: Duration of the slide animation
            display_duration: How long to display after all animations complete
            total_animation_time: Total time for all items to animate in
        
        Returns:
            Animated clip
        """
        # Get the final x position from the clip (where it should end up)
        if hasattr(clip, 'pos') and clip.pos is not None:
            if callable(clip.pos):
                # If pos is a function, evaluate it at t=0 to get initial position
                initial_pos = clip.pos(0)
                if isinstance(initial_pos, tuple):
                    final_x = initial_pos[0]
                else:
                    final_x = 0
            else:
                # If pos is a tuple
                if isinstance(clip.pos, tuple):
                    final_x = clip.pos[0]
                else:
                    final_x = 0
        else:
            final_x = 0
        
        def position_function(t):
            # Phase 1: Wait for start delay
            if t < start_delay:
                # Start off-screen to the left
                start_x = -container_width - 100  # Start off-screen left
                return (start_x, final_y)
            
            # Phase 2: Slide in animation from left
            elif t < start_delay + anim_duration:
                progress = (t - start_delay) / anim_duration
                eased_progress = Easing.ease_out_bounce(progress)
                start_x = -container_width - 100
                current_x = start_x + (final_x - start_x) * eased_progress
                return (current_x, final_y)
            
            # Phase 3: Stay in position during display
            elif t < total_animation_time + display_duration:
                return (final_x, final_y)
            
            # Phase 4: Slide out animation to the left
            else:
                exit_progress = (t - (total_animation_time + display_duration)) / anim_duration
                exit_progress = min(1.0, exit_progress)
                eased_progress = Easing.ease_in_quad(exit_progress)
                end_x = -container_width - 100  # Exit off-screen left
                current_x = final_x + (end_x - final_x) * eased_progress
                return (current_x, final_y)
        
        return clip.set_position(position_function)
    
    def _create_lineup_item_with_background(self, text, fontsize, text_color, width, height, 
                                          accent_color, accent_width, text_margin, center_text=False, 
                                          total_duration=1.0):
        """
        Create a lineup item with background and accent bar (for team name and director)
        
        Args:
            text: Text to display
            fontsize: Font size for the text
            text_color: Color of the text
            width: Width of the item
            height: Height of the item
            accent_color: Color of the accent bar
            accent_width: Width of the accent bar
            text_margin: Margin from accent bar to text
            center_text: Whether to center the text horizontally
            total_duration: Duration for the clip
        
        Returns:
            Composite clip with background and text
        """
        # Create background
        background = ColorClip(
            size=(width, height),
            color=self.LINEUP_NAME_BOX_COLOR  # Use configurable name box color
        ).set_duration(total_duration)
        
        # Create accent bar
        accent_bar = ColorClip(
            size=(accent_width, height),
            color=accent_color
        ).set_duration(total_duration)
        
        # Create text
        text_clip = TextClip(
            text,
            fontsize=fontsize,
            color=text_color,
            font=self.FONT_FAMILY,
            method='label'
        ).set_duration(total_duration)
        
        # Position elements
        accent_positioned = accent_bar.set_position((0, 0))
        
        if center_text:
            text_x = (width - text_clip.w) // 2
        else:
            text_x = accent_width + text_margin
        
        text_y = (height - text_clip.h) // 2
        text_positioned = text_clip.set_position((text_x, text_y))
        
        # Composite all elements
        return CompositeVideoClip([
            background,
            accent_positioned,
            text_positioned
        ], size=(width, height))
    
    def _create_lineup_player_item(self, player_number, player_name, player_font_size, 
                                 number_box_width, name_box_width, height, accent_color, 
                                 accent_width, text_margin, total_duration=1.0, name_text_color=None,
                                 player_position=""):
        """
        Create a player item with separate number and name boxes
        
        Args:
            player_number: Player number as string
            player_name: Player name
            player_font_size: Font size for player text
            number_box_width: Width of the number box
            name_box_width: Width of the name box
            height: Height of the item
            accent_color: Color of the accent bar
            accent_width: Width of the accent bar
            text_margin: Margin from accent bar to text
            total_duration: Duration for the clip
            name_text_color: Custom color for name text (if None, uses default player color)
            player_position: Player position abbreviation (e.g., "GK", "ST", "CM")
        
        Returns:
            Composite clip with number box and name box
        """
        total_width = number_box_width + name_box_width + accent_width
        
        # Create background for the entire item
        background = ColorClip(
            size=(total_width, height),
            color=self.LINEUP_NUMBER_BOX_COLOR  # Use configurable number box color
        ).set_duration(total_duration)
        
        # Create accent bar
        accent_bar = ColorClip(
            size=(accent_width, height),
            color=accent_color
        ).set_duration(total_duration)
        
        # Create number box background (use name box color)
        number_bg_color = self.LINEUP_NAME_BOX_COLOR
        number_background = ColorClip(
            size=(number_box_width, height),
            color=number_bg_color
        ).set_duration(total_duration)
        
        # Create player number text (only if number is not empty)
        if player_number:
            number_text = TextClip(
                player_number,
                fontsize=player_font_size,
                color='black',  # Use black for number text
                font=self.FONT_FAMILY,
                method='label'
            ).set_duration(total_duration)
        else:
            number_text = None
        
        # Create player name text with position (if provided)
        display_name = player_name
        if player_position:
            display_name = f"{player_name} ({player_position})"
        
        text_color = name_text_color if name_text_color is not None else self.LINEUP_PLAYER_TEXT_COLOR
        name_text = TextClip(
            display_name,
            fontsize=player_font_size,
            color=text_color,
            font=self.FONT_FAMILY,
            method='label'
        ).set_duration(total_duration)
        
        # Position elements
        accent_positioned = accent_bar.set_position((0, 0))
        
        number_bg_positioned = number_background.set_position((accent_width, 0))
        
        # Center number text in number box (only if number exists)
        if number_text:
            number_x = accent_width + (number_box_width - number_text.w) // 2
            number_y = (height - number_text.h) // 2
            number_positioned = number_text.set_position((number_x, number_y))
        
        # Position name text in name box
        name_x = accent_width + number_box_width + text_margin
        name_y = (height - name_text.h) // 2
        name_positioned = name_text.set_position((name_x, name_y))
        
        # Composite all elements
        elements = [
            background,
            accent_positioned,
            number_bg_positioned,
            name_positioned
        ]
        
        # Add number text only if it exists
        if number_text:
            elements.insert(-1, number_positioned)  # Insert before name_positioned
        
        return CompositeVideoClip(elements, size=(total_width, height))
    
    def _get_resolution_category(self, video_width):
        """Determine resolution category based on video width"""
        if video_width <= self.LOW_RES_THRESHOLD:
            return 'low'
        elif video_width <= self.MEDIUM_RES_THRESHOLD:
            return 'medium'
        else:
            return 'high'
    
    def _create_modern_score_overlay(self, team1_score, team2_score):
        """Create modern style with centered design and team accent bars"""
        
        # Get video dimensions and determine resolution category
        video_width = self.video.w
        video_height = self.video.h
        res_category = self._get_resolution_category(video_width)
        
        # Get dimensions and font sizes for this resolution
        scoreboard_height, team_box_width, score_box_width, accent_width = self.DIMENSIONS[res_category]
        fontsize_name, fontsize_score = self.FONT_SIZES[res_category]
        text_margin = self.TEXT_MARGIN_FROM_ACCENT[res_category]
        
        total_width = team_box_width + score_box_width + team_box_width
        
        # Position using configured margins
        x_pos = self.overlay_x_margin
        y_pos = self.overlay_y_margin
        
        # Create team 1 box (using configured background color)
        team1_box = ColorClip(
            size=(team_box_width, scoreboard_height),
            color=self.TEAM_BOX_COLOR
        )
        
        # Create team 2 box (using configured background color)
        team2_box = ColorClip(
            size=(team_box_width, scoreboard_height),
            color=self.TEAM_BOX_COLOR
        )
        
        # Create center score box (using configured score box color)
        score_box = ColorClip(
            size=(score_box_width, scoreboard_height),
            color=self.SCORE_BOX_COLOR
        )
        
        # Create team accent bars (using team colors)
        team1_accent = ColorClip(
            size=(accent_width, scoreboard_height),
            color=self._hex_to_rgb(self.team1_color)
        )
        
        team2_accent = ColorClip(
            size=(accent_width, scoreboard_height),
            color=self._hex_to_rgb(self.team2_color)
        )
        
        # Create text elements using configured fonts and colors
        team1_name_text = TextClip(
            self.team1_name,
            fontsize=fontsize_name,
            color=self.TEXT_COLOR_TEAM,
            font=self.FONT_FAMILY,
            method='label'
        )
        
        team2_name_text = TextClip(
            self.team2_name,
            fontsize=fontsize_name,
            color=self.TEXT_COLOR_TEAM,
            font=self.FONT_FAMILY,
            method='label'
        )
        
        score_text = TextClip(
            f"{team1_score} - {team2_score}",
            fontsize=fontsize_score,
            color=self.TEXT_COLOR_SCORE,
            font=self.FONT_FAMILY,
            method='label'
        )
        
        # Calculate positions
        # Center text vertically within the scoreboard height
        team_text_y_center = (scoreboard_height - team1_name_text.h) // 2
        score_text_y_center = (scoreboard_height - score_text.h) // 2
        
        # Team 1 positions (left side)
        team1_box_x = 0
        team1_accent_x = 0  # Left border of team 1 box
        team1_text_x = accent_width + text_margin  # Offset from accent bar using configured margin
        
        # Score box positions (center)
        score_box_x = team_box_width
        score_text_x = team_box_width + (score_box_width - score_text.w) // 2
        
        # Team 2 positions (right side)
        team2_box_x = team_box_width + score_box_width
        team2_accent_x = team_box_width + score_box_width + team_box_width - accent_width  # Right border of team 2 box
        team2_text_x = team_box_width + score_box_width + text_margin  # Offset from left edge using configured margin
        
        # Position all elements
        team1_box_positioned = team1_box.set_position((team1_box_x, 0))
        team1_accent_positioned = team1_accent.set_position((team1_accent_x, 0))
        team1_name_positioned = team1_name_text.set_position((team1_text_x, team_text_y_center))
        
        score_box_positioned = score_box.set_position((score_box_x, 0))
        score_text_positioned = score_text.set_position((score_text_x, score_text_y_center))
        
        team2_box_positioned = team2_box.set_position((team2_box_x, 0))
        team2_accent_positioned = team2_accent.set_position((team2_accent_x, 0))
        team2_name_positioned = team2_name_text.set_position((team2_text_x, team_text_y_center))
        
        # Composite all elements into a single overlay
        overlay = CompositeVideoClip([
            team1_box_positioned,
            team2_box_positioned,
            score_box_positioned,
            team1_name_positioned,
            team2_name_positioned,
            score_text_positioned,
            team1_accent_positioned,
            team2_accent_positioned
        ], size=(total_width, scoreboard_height))
        
        # Set final position (centered horizontally)
        return overlay.set_position((x_pos, y_pos))
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _format_name(self, full_name):
        """
        Format name with first name in title case and surname in upper case
        
        Args:
            full_name: Full name string (e.g., "john doe")
        
        Returns:
            Formatted name (e.g., "John DOE")
        """
        name_parts = full_name.strip().split()
        if len(name_parts) == 0:
            return full_name
        elif len(name_parts) == 1:
            # Single name - treat as surname (uppercase)
            return name_parts[0].upper()
        else:
            # Multiple parts - first name(s) in title case, last name in upper case
            first_names = name_parts[:-1]
            surname = name_parts[-1]
            formatted_first = ' '.join([name.title() for name in first_names])
            return f"{formatted_first} {surname.upper()}"
    
    @staticmethod
    def get_all_positions():
        """
        Get all available player positions
        
        Returns:
            List of all position abbreviations
        """
        return [position.value for position in PlayerPosition]
    
    @staticmethod
    def is_valid_position(position):
        """
        Check if a position abbreviation is valid
        
        Args:
            position: Position abbreviation to validate
        
        Returns:
            True if position is valid, False otherwise
        """
        return position in [pos.value for pos in PlayerPosition]
    
    def set_overlay_position(self, x_margin, y_margin):
        """
        Set the position of overlays
        
        Args:
            x_margin: Distance from left edge of video
            y_margin: Distance from top edge of video
        """
        self.overlay_x_margin = x_margin
        self.overlay_y_margin = y_margin
    
    def enable_scoreboard(self, enabled=True):
        """
        Enable or disable the scoreboard overlay
        
        Args:
            enabled: True to show scoreboard, False to hide
        """
        self.show_scoreboard = enabled
    
    def enable_notifications(self, enabled=True):
        """
        Enable or disable notifications
        
        Args:
            enabled: True to show notifications, False to hide
        """
        self.show_notifications = enabled
    
    def set_notification_settings(self, display_duration=None, animation_duration=None):
        """
        Configure notification timing
        
        Args:
            display_duration: How long to show notifications (seconds)
            animation_duration: Duration for slide animations (seconds)
        """
        if display_duration is not None:
            self.NOTIFICATION_DISPLAY_DURATION = display_duration
        if animation_duration is not None:
            self.NOTIFICATION_ANIMATION_DURATION = animation_duration
    
    def enable_lineups(self, enabled=True):
        """
        Enable or disable lineup overlays
        
        Args:
            enabled: True to show lineups, False to hide
        """
        self.show_lineups = enabled
    
    def set_lineup_settings(self, display_duration=None, animation_duration=None, stagger_delay=None):
        """
        Configure lineup timing
        
        Args:
            display_duration: How long to show lineup (seconds)
            animation_duration: Duration for each item slide animation (seconds)
            stagger_delay: Delay between each item animation (seconds)
        """
        if display_duration is not None:
            self.LINEUP_DISPLAY_DURATION = display_duration
        if animation_duration is not None:
            self.LINEUP_ANIMATION_DURATION = animation_duration
        if stagger_delay is not None:
            self.LINEUP_STAGGER_DELAY = stagger_delay
    
    def set_lineup_colors(self, background_color=None, name_box_color=None, team_text_color=None, 
                         player_text_color=None, director_text_color=None, 
                         number_box_color=None):
        """
        Configure lineup colors
        
        Args:
            background_color: Background color for lineup overlay (RGB tuple with alpha)
            name_box_color: Background color for name boxes (RGB tuple)
            team_text_color: Color for team name text
            player_text_color: Color for player text
            director_text_color: Color for director text
            number_box_color: Color for player number boxes (RGB tuple)
        """
        if background_color is not None:
            self.LINEUP_BACKGROUND_COLOR = background_color
        if name_box_color is not None:
            self.LINEUP_NAME_BOX_COLOR = name_box_color
        if team_text_color is not None:
            self.LINEUP_TEAM_TEXT_COLOR = team_text_color
        if player_text_color is not None:
            self.LINEUP_PLAYER_TEXT_COLOR = player_text_color
        if director_text_color is not None:
            self.LINEUP_DIRECTOR_TEXT_COLOR = director_text_color
        if number_box_color is not None:
            self.LINEUP_NUMBER_BOX_COLOR = number_box_color
    
    def add_overlays(self, goals, output_path, custom_notifications=None, lineups=None):
        """
        Add score overlays to the video
        
        Args:
            goals: List of goal dictionaries with 'time' and 'team' keys
            output_path: Path to save the output video
            custom_notifications: Optional list of custom notification dictionaries with format:
                                [{"time": "12:34", "text": "GOAL", "color": "#FF0000"}, ...]
                                If None, will auto-generate goal notifications
            lineups: Optional list of lineup dictionaries with format:
                    [{"time": "00:30", "team": 1, "players": [{"number": 1, "name": "Player"}], "director": "Coach Name"}, ...]
        """
        print("Processing video and adding overlays...")
        
        score_timeline = self.parse_goal_data(goals)
        clips = [self.video]
        
        # Get video dimensions and resolution category for notifications
        video_width = self.video.w
        video_height = self.video.h
        res_category = self._get_resolution_category(video_width)
        _, team_box_width, score_box_width, _ = self.DIMENSIONS[res_category]
        scoreboard_height = self.DIMENSIONS[res_category][0]
        
        # Collect all clips with proper layering order
        lineup_overlays = []
        notifications = []
        score_overlays = []
        
        # Add score overlays for each segment
        for i in range(len(score_timeline)):
            start_time, team1_score, team2_score = score_timeline[i]
            
            # Determine end time
            if i < len(score_timeline) - 1:
                end_time = score_timeline[i + 1][0]
            else:
                end_time = self.video.duration
            
            duration = end_time - start_time
            
            # Create score overlay only if enabled
            if self.show_scoreboard:
                score_clip = (self.create_score_overlay(team1_score, team2_score)
                             .set_start(start_time)
                             .set_duration(duration))
                score_overlays.append(score_clip)
            
            # Add goal notification for score changes (skip the initial 0-0) only if enabled
            if self.show_notifications and i > 0 and custom_notifications is None:  # Auto-generate goal notifications
                print(f"Adding goal notification at time {start_time}s for goal {i}")
                
                # Determine which team scored by comparing current and previous scores
                prev_team1_score, prev_team2_score = score_timeline[i-1][1], score_timeline[i-1][2]
                scoring_team = 1 if team1_score > prev_team1_score else 2
                team_color = self.team1_color if scoring_team == 1 else self.team2_color
                
                # Calculate the position for the notification
                notification_x = self.overlay_x_margin + team_box_width  # Same x as score box
                notification_y = self.overlay_y_margin  # Start at the same level as the score box
                
                # Create goal notification
                notification = self.create_notification(
                    score_box_width, 
                    scoreboard_height, 
                    res_category,
                    notification_text="GOAL",
                    background_color=team_color,
                    base_position=(notification_x, notification_y)
                )
                
                # Add to timeline with start time
                notification_positioned = notification.set_start(start_time)
                notifications.append(notification_positioned)
        
        # Add custom notifications if provided
        if self.show_notifications and custom_notifications:
            for custom_notif in custom_notifications:
                notif_time = self._to_seconds(custom_notif['time'])
                notif_text = custom_notif.get('text', 'NOTIFICATION')
                notif_color = custom_notif.get('color', None)
                notif_text_color = custom_notif.get('text_color', None)
                notif_display_duration = custom_notif.get('display_duration', None)
                notif_animation_duration = custom_notif.get('animation_duration', None)
                
                print(f"Adding custom notification '{notif_text}' at time {notif_time}s")
                
                # Calculate the position for the notification
                notification_x = self.overlay_x_margin + team_box_width
                notification_y = self.overlay_y_margin
                
                # Create custom notification
                notification = self.create_notification(
                    score_box_width,
                    scoreboard_height,
                    res_category,
                    notification_text=notif_text,
                    background_color=notif_color,
                    text_color=notif_text_color,
                    base_position=(notification_x, notification_y),
                    display_duration=notif_display_duration,
                    animation_duration=notif_animation_duration
                )
                
                # Add to timeline with start time
                notification_positioned = notification.set_start(notif_time)
                notifications.append(notification_positioned)
        
        # Add lineup overlays if provided
        if self.show_lineups and lineups:
            for lineup_data in lineups:
                lineup_time = self._to_seconds(lineup_data['time'])
                team_num = lineup_data['team']
                players = lineup_data['players']
                director = lineup_data['director']
                
                # Get team info
                if team_num == 1:
                    team_name = self.team1_name
                    team_color = self.team1_color
                else:
                    team_name = self.team2_name
                    team_color = self.team2_color
                
                # Get custom settings if provided
                lineup_display_duration = lineup_data.get('display_duration', None)
                lineup_animation_duration = lineup_data.get('animation_duration', None)
                lineup_stagger_delay = lineup_data.get('stagger_delay', None)
                
                print(f"Adding lineup for {team_name} at time {lineup_time}s")
                
                # Create lineup overlay
                lineup_overlay = self.create_lineup_overlay(
                    team_name=team_name,
                    players=players,
                    director=director,
                    team_color=team_color,
                    display_duration=lineup_display_duration,
                    animation_duration=lineup_animation_duration,
                    stagger_delay=lineup_stagger_delay
                )
                
                # Add to timeline with start time
                lineup_positioned = lineup_overlay.set_start(lineup_time)
                lineup_overlays.append(lineup_positioned)
        
        # Add clips in proper layering order (bottom to top)
        if self.show_lineups:
            clips.extend(lineup_overlays)  # Lineups at the bottom
        if self.show_notifications:
            clips.extend(notifications)    # Notifications in the middle
        if self.show_scoreboard:
            clips.extend(score_overlays)   # Scoreboard on top
        
        # Composite all clips
        print("Compositing video layers...")
        final = CompositeVideoClip(clips)
        
        print(f"Writing video to {output_path}...")
        final.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            fps=self.video.fps
        )
        
        print("Done! Video saved successfully.")
        self.video.close()

# Example usage
def main():
    
    video_file_path = "/Users/orhanbalci/Downloads/test.mp4"

    # Define goals with times (can use MM:SS format or seconds)
    goals = [
        # {"time": "08:20", "team": 1},
        # {"time": "33:22", "team": 2},
        # {"time": "39:08", "team": 1},
        # {"time": "52:04", "team": 1}
    ]

    # goals = [
    #     {"time": "00:10", "team": 1},
    #     {"time": "00:20", "team": 2}
    # ]
    
    # Optional: Define lineup overlays
    lineups = [
        {
            "time": "00:05",
            "team": 1,  # AFKA
            "players": [
                {"number": 1, "name": "Önder Özen", "position": PlayerPosition.GOALKEEPER.value},
                {"number": 2, "name": "Onur Çapan", "position": PlayerPosition.RIGHT_BACK.value},
                {"number": 3, "name": "Ramazan Günay", "position": PlayerPosition.RIGHT_CENTER_BACK.value},
                {"number": 4, "name": "Hakan Köroğlu", "position": PlayerPosition.LEFT_CENTER_BACK.value},
                {"number": 5, "name": "Cüneyt Taşyürek", "position": PlayerPosition.LEFT_BACK.value},
                {"number": 6, "name": "Necati Yatkak", "position": PlayerPosition.DEFENSIVE_MIDFIELDER.value},
                {"number": 7, "name": "Şükrü Karadirek", "position": PlayerPosition.CENTRAL_MIDFIELDER.value},
                {"number": 8, "name": "Gökhan Uysal", "position": PlayerPosition.ATTACKING_MIDFIELDER.value},
                {"number": 9, "name": "Süleyman Demirel", "position": PlayerPosition.STRIKER.value},
                {"number": 10, "name": "Yusuf Uyar", "position": PlayerPosition.LEFT_WINGER.value},
                {"number": 11, "name": "Fatih Manga", "position": PlayerPosition.RIGHT_WINGER.value}
            ],
            "director": "Ramazan Üçkuyulu",
            "display_duration": 6.0,
            "animation_duration": 0.4,
            "stagger_delay": 0.15
        },
        {
            "time": "00:15",
            "team": 2,  # AFYON
            "players": [
                {"number": 1, "name": "Süleyman Şahin", "position": PlayerPosition.GOALKEEPER.value},
                {"number": 2, "name": "Esma Çevik", "position": PlayerPosition.RIGHT_BACK.value},
                {"number": 3, "name": "Osman Savsar", "position": PlayerPosition.RIGHT_CENTER_BACK.value},
                {"number": 4, "name": "Arif Yılmaz", "position": PlayerPosition.LEFT_CENTER_BACK.value},
                {"number": 5, "name": "Hüseyin Coşkun", "position": PlayerPosition.LEFT_BACK.value},
                {"number": 6, "name": "Ali Çaltepe", "position": PlayerPosition.DEFENSIVE_MIDFIELDER.value},
                {"number": 7, "name": "Önder Özen", "position": PlayerPosition.CENTRAL_MIDFIELDER.value},
                {"number": 8, "name": "Onur Çapan", "position": PlayerPosition.ATTACKING_MIDFIELDER.value},
                {"number": 9, "name": "Ramazan Günay", "position": PlayerPosition.STRIKER.value},
                {"number": 10, "name": "Hakan Köroğlu", "position": PlayerPosition.LEFT_WINGER.value},
                {"number": 11, "name": "Cüneyt Taşyürek", "position": PlayerPosition.RIGHT_WINGER.value}
            ],
            "director": "Necati Yatkak",
            "display_duration": 6.0,
            "animation_duration": 0.4,
            "stagger_delay": 0.15
        }
    ]
    
    # Optional: Define custom notifications (replaces auto-generated goal notifications)
    custom_notifications = [
        # {"time": "08:21", "text": "GOLL!", "color": "#A50044", "text_color": "white", 
        #  "display_duration": 3.0, "animation_duration": 1.2},
        # {"time": "08:26", "text": "MVLUT", "color": "#A50044", "text_color": "white", 
        #  "display_duration": 3.0, "animation_duration": 1.2},
        # {"time": "33:23", "text": "GOLL!", "color": "#FEBE10", "text_color": "white", 
        #  "display_duration": 3.0, "animation_duration": 1.2},
        # {"time": "39:09", "text": "GOLL!", "color": "#A50044", "text_color": "white", 
        #  "display_duration": 3.0, "animation_duration": 1.2},
        # {"time": "39:14", "text": "SALIH", "color": "#A50044", "text_color": "white", 
        #  "display_duration": 3.0, "animation_duration": 1.2},
        # {"time": "52:05", "text": "GOLL!", "color": "#A50044", "text_color": "white", 
        #  "display_duration": 3.0, "animation_duration": 1.2},
        # {"time": "52:10", "text": "SALIH", "color": "#A50044", "text_color": "white", 
        #  "display_duration": 3.0, "animation_duration": 1.2},
    ]
    
    # Initialize with video path, team names, colors, and overlay settings
    overlay = SoccerScoreOverlay(
        video_path=video_file_path,
        team1_name="AFKA",
        team2_name="AFYON",
        team1_color="#A50044",  # Barcelona red/burgundy
        team2_color="#FEBE10",  # Real Madrid gold
        overlay_x_margin=20,    # Custom position - 20px from left
        overlay_y_margin=15,    # Custom position - 15px from top
        show_scoreboard=True,   # Enable scoreboard
        show_notifications=True,  # Enable notifications
        show_lineups=True       # Enable lineup overlays
    )
    
    import os
    base_name = os.path.splitext(video_file_path)[0]
    output_path = f"{base_name}_with_score.mp4"

  
    overlay.add_overlays(
        goals=goals,
        output_path=output_path,
        custom_notifications=custom_notifications,
        lineups=lineups
    )

if __name__ == "__main__":
    main()