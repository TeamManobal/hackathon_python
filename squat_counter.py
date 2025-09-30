import cv2
import mediapipe as mp
from utils import calculate_angle

class SquatCounter:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils

    def process_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(rgb)

        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark

            # Left leg landmarks
            hip = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            # Calculate knee angle
            angle = calculate_angle(hip, knee, ankle)

            # Squat logic
            if angle > 165:
                self.stage = "up"
            if angle < 95 and self.stage == "up":
                self.stage = "down"
                self.counter += 1

            # Overlay text
            cv2.putText(frame, f'Angle: {int(angle)}', (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            cv2.putText(frame, f'Count: {self.counter}', (50,100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            # Draw skeleton
            self.mp_drawing.draw_landmarks(frame, result.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

        return frame

    def getCounter(self):
        return self.counter