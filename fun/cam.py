"""
Hand Finger Counter using OpenCV and MediaPipe
Counts the number of fingers shown to the camera in real-time.
"""

import cv2
import mediapipe as mp


class HandFingerCounter:
    def __init__(self):
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

        # Finger tip landmark indices
        self.tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

    def count_fingers(self, hand_landmarks, handedness):
        """Count the number of raised fingers on a hand."""
        fingers = []

        # Get hand label (Left or Right)
        hand_label = handedness.classification[0].label

        # Thumb - check horizontal position
        # For right hand: thumb tip should be to the right of thumb IP
        # For left hand: thumb tip should be to the left of thumb IP
        if hand_label == "Right":
            if hand_landmarks.landmark[self.tip_ids[0]].x < hand_landmarks.landmark[self.tip_ids[0] - 1].x:
                fingers.append(1)
            else:
                fingers.append(0)
        else:  # Left hand
            if hand_landmarks.landmark[self.tip_ids[0]].x > hand_landmarks.landmark[self.tip_ids[0] - 1].x:
                fingers.append(1)
            else:
                fingers.append(0)

        # Other 4 fingers - check if tip is above PIP joint (lower y = higher on screen)
        for id in range(1, 5):
            if hand_landmarks.landmark[self.tip_ids[id]].y < hand_landmarks.landmark[self.tip_ids[id] - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        return sum(fingers)

    def run(self):
        """Main loop to capture video and count fingers."""
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open camera.")
            return

        print("Hand Finger Counter Started!")
        print("Show your hand(s) to the camera to count fingers.")
        print("Press 'q' to quit.")

        while True:
            success, frame = cap.read()
            if not success:
                print("Error: Could not read frame.")
                break

            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)

            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame
            results = self.hands.process(rgb_frame)

            total_fingers = 0

            if results.multi_hand_landmarks and results.multi_handedness:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    # Draw hand landmarks
                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                        self.mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)
                    )

                    # Count fingers for this hand
                    finger_count = self.count_fingers(hand_landmarks, handedness)
                    total_fingers += finger_count

                    # Get hand label and display per-hand count
                    hand_label = handedness.classification[0].label

                    # Get wrist position for text placement
                    wrist = hand_landmarks.landmark[0]
                    h, w, _ = frame.shape
                    cx, cy = int(wrist.x * w), int(wrist.y * h)

                    cv2.putText(
                        frame,
                        f"{hand_label}: {finger_count}",
                        (cx - 30, cy - 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 0),
                        2
                    )

            # Display total finger count
            cv2.rectangle(frame, (10, 10), (200, 80), (0, 0, 0), -1)
            cv2.putText(
                frame,
                f"Fingers: {total_fingers}",
                (20, 55),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                3
            )

            # Display instructions
            cv2.putText(
                frame,
                "Press 'q' to quit",
                (10, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                1
            )

            # Show the frame
            cv2.imshow("Hand Finger Counter", frame)

            # Check for quit key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        self.hands.close()
        print("Hand Finger Counter stopped.")


def main():
    counter = HandFingerCounter()
    counter.run()


if __name__ == "__main__":
    main()
