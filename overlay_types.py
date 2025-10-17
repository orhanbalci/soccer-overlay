"""
Type definitions and enums for the Soccer Overlay System
"""

from enum import Enum
from typing import Dict, List, Tuple


class PlayerPosition(Enum):
    """
    Enumeration of football/soccer player positions with their abbreviations
    """

    # Goalkeeper
    GOALKEEPER = "GK"

    # Defense (Back Line)
    LEFT_BACK = "LB"
    LEFT_CENTER_BACK = "LCB"
    RIGHT_CENTER_BACK = "RCB"
    RIGHT_BACK = "RB"

    # Midfield (Central Area)
    DEFENSIVE_MIDFIELDER = "CDM"
    DEFENSIVE_MIDFIELDER_ALT = "DM"
    CENTRAL_MIDFIELDER = "CM"
    ATTACKING_MIDFIELDER = "CAM"
    ATTACKING_MIDFIELDER_ALT = "AM"
    LEFT_MIDFIELDER = "LM"
    LEFT_WINGER = "LW"
    RIGHT_MIDFIELDER = "RM"
    RIGHT_WINGER = "RW"

    # Attack (Forward Line)
    SECOND_STRIKER = "SS"
    CENTER_FORWARD = "CF"
    STRIKER = "ST"


class LineupAnimationType(Enum):
    """
    Types of lineup animations available
    """

    LIST = "list"  # Current vertical list animation
    FORMATION = "formation"  # Scatter to field positions


class Formation(Enum):
    """
    Soccer formations with their structure
    """

    FORMATION_4_3_3 = "4-3-3"
    FORMATION_4_4_2 = "4-4-2"
    FORMATION_3_5_2 = "3-5-2"
    FORMATION_4_2_3_1 = "4-2-3-1"
    FORMATION_3_4_3 = "3-4-3"
    FORMATION_5_3_2 = "5-3-2"


# Field position coordinates (as percentage of video dimensions)
# Format: (x_percent, y_percent) where 0,0 is top-left, 100,100 is bottom-right
# Coordinates are for left side of field (will be mirrored for right side)
FORMATION_COORDINATES: Dict[Formation, Dict[str, Tuple[float, float]]] = {
    Formation.FORMATION_4_3_3: {
        # Goalkeeper
        "GK": (15, 50),
        # Defense (4 defenders)
        "LB": (25, 75),
        "LCB": (25, 60),
        "RCB": (25, 40),
        "RB": (25, 25),
        # Midfield (3 midfielders - positioned vertically)
        "CDM": (40, 50),  # Defensive midfielder (deepest)
        "DM": (40, 50),  # Alternative name for defensive midfielder
        "CM": (55, 50),  # Central midfielder (middle)
        "CAM": (70, 50),  # Attacking midfielder (most forward)
        "AM": (70, 50),  # Alternative name for attacking midfielder
        "LM": (55, 65),  # Left midfielder (if used instead of wingers)
        "RM": (55, 35),  # Right midfielder (if used instead of wingers)
        # Attack (3 forwards)
        "LW": (85, 70),  # Left winger
        "ST": (85, 50),  # Striker (center)
        "RW": (85, 30),  # Right winger
        "CF": (85, 50),  # Center forward (same as striker)
        "SS": (80, 50),  # Second striker (slightly behind)
    },
    Formation.FORMATION_4_4_2: {
        # Goalkeeper
        "GK": (15, 50),
        # Defense (4 defenders)
        "LB": (25, 75),
        "LCB": (25, 60),
        "RCB": (25, 40),
        "RB": (25, 25),
        # Midfield (4 midfielders)
        "LM": (50, 75),
        "CDM": (50, 60),
        "CM": (50, 40),
        "RM": (50, 25),
        "DM": (50, 60),
        "CAM": (50, 40),
        "AM": (50, 40),
        # Attack (2 forwards)
        "ST": (75, 40),
        "CF": (75, 60),
        "LW": (75, 65),
        "RW": (75, 35),
        "SS": (70, 50),
    },
    Formation.FORMATION_3_5_2: {
        # Goalkeeper
        "GK": (15, 50),
        # Defense (3 defenders)
        "LCB": (25, 65),
        "RCB": (25, 35),
        "LB": (35, 75),  # Wing back
        "RB": (35, 25),  # Wing back
        # Midfield (5 midfielders)
        "LM": (50, 75),
        "CDM": (40, 60),
        "CM": (50, 50),
        "CAM": (60, 40),
        "RM": (50, 25),
        "DM": (40, 50),
        "AM": (60, 50),
        # Attack (2 forwards)
        "ST": (75, 40),
        "CF": (75, 60),
        "LW": (70, 70),
        "RW": (70, 30),
        "SS": (70, 50),
    },
    Formation.FORMATION_4_2_3_1: {
        # Goalkeeper
        "GK": (15, 50),
        # Defense (4 defenders)
        "LB": (25, 75),
        "LCB": (25, 60),
        "RCB": (25, 40),
        "RB": (25, 25),
        # Midfield (5 midfielders: 2 CDM + 3 AM)
        "CDM": (40, 60),
        "DM": (40, 40),
        "LM": (60, 75),
        "CAM": (60, 50),
        "RM": (60, 25),
        "CM": (50, 50),
        "AM": (60, 50),
        # Attack (1 forward)
        "ST": (80, 50),
        "CF": (80, 50),
        "LW": (65, 70),
        "RW": (65, 30),
        "SS": (75, 50),
    },
    Formation.FORMATION_3_4_3: {
        # Goalkeeper
        "GK": (15, 50),
        # Defense (3 defenders)
        "LCB": (25, 65),
        "RCB": (25, 35),
        "LB": (30, 80),  # Wing back
        "RB": (30, 20),  # Wing back
        # Midfield (4 midfielders)
        "LM": (50, 75),
        "CDM": (45, 60),
        "CM": (45, 40),
        "RM": (50, 25),
        "DM": (45, 50),
        "CAM": (55, 50),
        "AM": (55, 50),
        # Attack (3 forwards)
        "LW": (75, 75),
        "ST": (75, 50),
        "RW": (75, 25),
        "CF": (75, 50),
        "SS": (70, 50),
    },
    Formation.FORMATION_5_3_2: {
        # Goalkeeper
        "GK": (15, 50),
        # Defense (5 defenders)
        "LB": (25, 80),
        "LCB": (25, 65),
        "RCB": (25, 35),
        "RB": (25, 20),
        "CDM": (25, 50),  # Central defender
        # Midfield (3 midfielders)
        "LM": (55, 70),
        "CM": (55, 50),
        "RM": (55, 30),
        "DM": (45, 50),
        "CAM": (65, 50),
        "AM": (65, 50),
        # Attack (2 forwards)
        "ST": (80, 40),
        "CF": (80, 60),
        "LW": (75, 65),
        "RW": (75, 35),
        "SS": (75, 50),
    },
}
