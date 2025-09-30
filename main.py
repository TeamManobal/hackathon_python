import cv2
from squat_counter import SquatCounter

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    squat = SquatCounter()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print(squat.getCounter())
            break

        frame = squat.process_frame(frame)
        cv2.imshow("Side View Squat Counter", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break
    cap.release()
    getcounter = squat.getCounter()
    print(f"Squats completed: {getcounter}")

if __name__ == "__main__":
    process_video("squatsdemo.mp4")

