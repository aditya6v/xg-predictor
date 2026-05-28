import numpy as np

GOAL_X = 120
GOAL_Y = 40
POST_LEFT = 36.34
POST_RIGHT = 43.66

def calculate_distance(x, y):
    distance = np.sqrt((GOAL_X - x)**2 + (GOAL_Y - y)**2)
    return distance


def calculate_angle(x, y):
    
    d_left = np.sqrt((GOAL_X - x)**2 + (POST_LEFT - y)**2)
    d_right = np.sqrt((GOAL_X - x)**2 + (POST_RIGHT - y)**2)
    
    goal_width = 7.32
    
    cos_angle = (d_left**2 + d_right**2 - goal_width**2) / (2 * d_left * d_right)
    angle = np.degrees(np.arccos(cos_angle))
    
    return angle


def get_goalkeeper_position(freeze_frame):
    for player in freeze_frame:
        if player["teammate"] == False and player["position"]["name"] == "Goalkeeper":
            return player["location"][0], player["location"][1]
    return None, None

def get_goalkeeper_distance_to_goal(freeze_frame):
    gk_x, gk_y = get_goalkeeper_position(freeze_frame)
    if gk_x is None:
        return None
    distance = calculate_distance(gk_x, gk_y)
    return distance

def count_defenders_in_path(freeze_frame, shot_x, shot_y):
    count = 0
    for player in freeze_frame:
        if player["teammate"] == False and player["position"]["name"] != "Goalkeeper":
            def_x = player["location"][0]
            def_y = player["location"][1]
            
            # Check if defender is between shot and goal
            if def_x > shot_x and def_x < GOAL_X:
                # Check if defender is within the angle cone
                if def_y > min(POST_LEFT, shot_y) and def_y < max(POST_RIGHT, shot_y):
                    count += 1
    return count