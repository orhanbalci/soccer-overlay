"""
Type definitions and enums for the Soccer Overlay System
"""

from enum import Enum

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
