import cv2
import mediapipe as mp
import numpy as np
import base64
import argparse
import os
from good_angle import assess_posture 

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def process_frame(frame_file_path):
    try:
        # Read the base64 string from the file
        with open(frame_file_path, 'r') as file:
            base64_frame = file.read()

        # Ensure proper padding
        base64_frame += '=' * (-len(base64_frame) % 4)

        # Decode the base64 frame to an image
        nparr = np.frombuffer(base64.b64decode(base64_frame), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Process the frame
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            if results.pose_landmarks:
                # Assess posture and color-code joints
                image = assess_posture(results.pose_landmarks, image)

                # Optionally, draw landmarks on the image (before or after the assessment)
                mp_drawing.draw_landmarks(
                    image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                )

            # Convert the processed frame back to base64
            _, buffer = cv2.imencode('.jpg', image)
            return base64.b64encode(buffer).decode('utf-8')
    except Exception as e:
        print(f"Error processing frame: {e}")
        return None

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('--frameFile', type=str, required=True, help="Path to the file containing base64 encoded frame")
args = parser.parse_args()

processed_frame = process_frame(args.frameFile)
if processed_frame:
    print(processed_frame)
else:
    print("Failed to process frame")
