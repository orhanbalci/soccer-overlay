# Soccer Overlay ⚽

**Enrich amateur soccer videos with professional-looking overlays and data**

Transform your raw soccer match recordings into professional broadcasts with dynamic scoreboards, goal notifications, and team lineup displays. Perfect for amateur leagues, youth teams, and local clubs looking to enhance their video content.

## ✨ Features

### 🎯 **Live Score Tracking**
- Dynamic scoreboard overlay that updates throughout the match
- Responsive design that adapts to different video resolutions
- Modern, clean UI with customizable team colors
- Positioned anywhere on the video with configurable margins

### 🎉 **Goal Notifications**
- Animated "GOAL!" notifications when goals are scored
- Customizable notification text, colors, and timing
- Smooth slide-in/slide-out animations with configurable easing
- Automatic or manual notification triggers

### 👥 **Team Lineups**
- Beautiful animated lineup displays at the start of each half
- Shows player numbers, names, and team directors
- Staggered entrance animations for each player
- Fully customizable colors and timing

### 🎬 **Professional Animations**
- Comprehensive animation library with multiple easing functions
- Smooth transitions and overlays
- Configurable animation timing and effects
- Built on MoviePy for reliable video processing

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/orhanbalci/soccer-overlay.git
cd soccer-overlay

# Install required dependencies
pip install moviepy numpy
```

### Basic Usage

```python
from score_overlay import SoccerScoreOverlay

# Define your goals with timestamps
goals = [
    {"time": "08:21", "team": 1},  # Team 1 scores at 8:21
    {"time": "33:23", "team": 2},  # Team 2 scores at 33:23
    {"time": "52:05", "team": 1}   # Team 1 scores at 52:05
]

# Create overlay instance
overlay = SoccerScoreOverlay(
    video_path="match.mp4",
    team1_name="Home Team",
    team2_name="Away Team",
    team1_color="#FF0000",  # Red
    team2_color="#0000FF"   # Blue
)

# Add overlays and export
overlay.add_overlays(
    goals=goals,
    output_path="match_with_overlays.mp4"
)
```

## 📋 Detailed Configuration

### Goal Data Format

Goals can be specified in multiple formats:

```python
# Using MM:SS format
goals = [{"time": "08:21", "team": 1}]

# Using seconds
goals = [{"time": 501, "team": 1}]  # 8 minutes 21 seconds

# Using HH:MM:SS format
goals = [{"time": "01:08:21", "team": 1}]
```

### Team Lineup Configuration

```python
lineups = [
    {
        "time": "00:01",  # Show at video start
        "team": 1,
        "players": [
            {"number": 1, "name": "John Doe"},
            {"number": 9, "name": "Jane Smith"},
            # ... more players
        ],
        "director": "Coach Name",
        "display_duration": 8.0,
        "animation_duration": 0.5
    }
]

overlay.add_overlays(goals=goals, output_path="output.mp4", lineups=lineups)
```

### Custom Notifications

```python
custom_notifications = [
    {
        "time": "08:21",
        "text": "AMAZING GOAL!",
        "color": "#FFD700",
        "text_color": "black",
        "display_duration": 4.0,
        "animation_duration": 1.0
    }
]

overlay.add_overlays(
    goals=goals,
    output_path="output.mp4",
    custom_notifications=custom_notifications
)
```

## ⚙️ Advanced Configuration

### Overlay Positioning

```python
overlay = SoccerScoreOverlay(
    video_path="match.mp4",
    overlay_x_margin=20,  # 20px from left edge
    overlay_y_margin=15   # 15px from top edge
)

# Or change after initialization
overlay.set_overlay_position(x_margin=30, y_margin=25)
```

### Feature Control

```python
# Disable specific features
overlay.enable_scoreboard(False)     # Hide scoreboard
overlay.enable_notifications(False)  # Hide notifications
overlay.enable_lineups(False)       # Hide lineups

# Customize timing
overlay.set_notification_settings(
    display_duration=5.0,    # Show notifications for 5 seconds
    animation_duration=1.5   # 1.5 second animation
)

overlay.set_lineup_settings(
    display_duration=10.0,   # Show lineup for 10 seconds
    animation_duration=0.8,  # 0.8 second per item animation
    stagger_delay=0.3       # 0.3 second delay between items
)
```

### Responsive Design

The overlay automatically adapts to different video resolutions:

- **Low Resolution** (≤720px): Compact overlay with smaller fonts
- **Medium Resolution** (≤1280px): Balanced size and readability
- **High Resolution** (>1280px): Large, detailed overlay for HD/4K videos

## 🎨 Customization

### Colors

All colors support hex format:

```python
overlay = SoccerScoreOverlay(
    video_path="match.mp4",
    team1_color="#A50044",  # Burgundy
    team2_color="#FEBE10",  # Gold
)
```

### Animation Library

The project includes a comprehensive animation library with easing functions:

- Linear
- Quadratic (ease in/out/in-out)
- Cubic (ease in/out/in-out)
- Quartic (ease in/out/in-out)
- Quintic (ease in/out/in-out)
- Bounce effects
- Elastic effects

## 📁 Project Structure

```
soccer-overlay/
├── score_overlay.py    # Main overlay system
├── animation.py        # Animation library with easing functions
├── README.md          # This file
└── LICENSE           # MIT License
```

## 🛠️ Requirements

- Python 3.7+
- MoviePy
- NumPy

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Use Cases

- **Amateur Soccer Leagues**: Add professional touches to match recordings
- **Youth Teams**: Create highlight reels with score tracking
- **Local Clubs**: Enhance live stream recordings
- **Coaches**: Add tactical overlays and player information
- **Sports Content Creators**: Professional-looking soccer content

## 🔧 Troubleshooting

### Common Issues

1. **Video not found**: Ensure the video path is correct and accessible
2. **Slow processing**: Large videos take time; consider reducing resolution for testing
3. **Font issues**: The system uses Arial-Bold; ensure it's available on your system

### Performance Tips

- Test with shorter video clips first
- Use compressed video formats (MP4) for faster processing
- Adjust animation durations for performance vs. quality balance

---

**Made with ⚽ for the soccer community**