import numpy as np
import cv2

import mediapipe as mp

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose

# Function to calculate the angle between three points
def calculate_angle(A, B, C):
    AB = np.array([A[0] - B[0], A[1] - B[1]])  # Vector AB
    BC = np.array([C[0] - B[0], C[1] - B[1]])  # Vector BC
    
    # Calculate cosine of the angle using dot product formula
    cos_angle = np.dot(AB, BC) / (np.linalg.norm(AB) * np.linalg.norm(BC))
    angle = np.degrees(np.arccos(cos_angle))  # Convert to degrees
    return angle


def assess_posture(landmarks, image):
    # Access landmarks using the 'landmark' attribute of the 'landmarks' object
    shoulder = (landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y)
    elbow = (landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y)
    wrist = (landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y)

    left_hip = (landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y)
    left_knee = (landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].y)
    left_ankle = (landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].y)

    right_hip = (landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x, landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y)
    right_knee = (landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].x, landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].y)
    right_ankle = (landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].x, landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].y)

    # Calculate joint angles
    left_elbow_angle = calculate_angle(shoulder, elbow, wrist)
    left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
    hip_angle = calculate_angle(left_hip, left_knee, right_hip)

    # Determine exercise
    exercise = "Rest"  # Default

    """
    body_horizontal = abs(left_hip[1] - left_ankle[1]) < 0.1 and abs(left_hip[1] - shoulder[1]) < 0.1
    arms_straight = left_elbow_angle > 150
    hands_above_head = wrist[1] < shoulder[1] and left_knee_angle > 150
    """

    # Movement threshold to detect significant arm/leg movement
    elbow_flexion_threshold = 90  # Angle for bicep curl detection
    knee_flexion_threshold = 90  # Angle for squat or lunge detection
    movement_tolerance = 0.05    # Small tolerance for minimal movements

    """
    print(f"left_elbow_angle: {left_elbow_angle}, shoulder[1]: {shoulder[1]}, elbow[1]: {elbow[1]}, wrist[0]: {wrist[0]}, elbow[0]: {elbow[0]}")
    print(f"left_hip[1]: {left_hip[1]}, left_ankle[1]: {left_ankle[1]}, shoulder[1]: {shoulder[1]}, left_elbow_angle: {left_elbow_angle}")
    print(f"wrist[1]: {wrist[1]}, shoulder[1]: {shoulder[1]}, left_hip[0]: {left_hip[0]}, left_knee[0]: {left_knee[0]}, left_hip[1]: {left_hip[1]}")
    print(f"left_knee_angle: {left_knee_angle},  left_hip[1]: {left_hip[1]}, shoulder[1]: {shoulder[1]}")
    print(f"left_elbow_angle: {left_elbow_angle}, left_hip[1]: {left_hip[1]}, left_knee[1]: {left_knee[1]}")
    """

    # Bicep Curl: Tightened logic
    if left_elbow_angle < elbow_flexion_threshold and shoulder[1] > elbow[1] and abs(wrist[0] - elbow[0]) < movement_tolerance:
        exercise = "Bicep Curl"
    # Plank: Body alignment and straight arms
    elif abs(left_hip[1] - left_ankle[1]) < 0.1 and abs(left_hip[1] - shoulder[1]) < 0.1 and left_elbow_angle > 150:
        exercise = "Plank"
    # Jumping Jacks: Arms above head and feet apart
    elif wrist[1] < shoulder[1] and abs(left_hip[0] - left_knee[0]) > 0.1 and abs(left_hip[1] - shoulder[1]) > 0.1:
        exercise = "Jumping Jack"
    # Squat: Knee angle less than threshold
    elif left_knee_angle < knee_flexion_threshold and abs(left_hip[1] - shoulder[1]) > movement_tolerance:
        exercise = "Squat"
    # Push-Up: Elbow flexion and straight legs
    elif left_elbow_angle < elbow_flexion_threshold and abs(left_hip[1] - left_knee[1]) < 0.1:
        exercise = "Push-Up"
    else:
        exercise = "Rest"
    # Default: N/A if no clear exercise is detected

    # Display the exercise name on the image
    cv2.putText(image, f'Exercise: {exercise}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Color joints based on posture
    def color_based_on_angle(angle):
        if 90 <= angle <= 150:
            return (0, 255, 0)  # Green
        elif angle < 90:
            return (0, 0, 255)  # Red
        else:
            return (255, 0, 255)  # Purple

    elbow_color = color_based_on_angle(left_elbow_angle)
    knee_color = color_based_on_angle(left_knee_angle)

    # Draw colored joints
    cv2.circle(image, (int(elbow[0] * image.shape[1]), int(elbow[1] * image.shape[0])), 5, elbow_color, -1)
    cv2.circle(image, (int(left_knee[0] * image.shape[1]), int(left_knee[1] * image.shape[0])), 5, knee_color, -1)

    return image