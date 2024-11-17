import streamlit as st
import cv2
import numpy as np
from PIL import Image
from math import hypot
import mediapipe as mp
import cvzone

# Initialize Mediapipe for hand landmarks
initHand = mp.solutions.hands
mainHand = initHand.Hands(min_detection_confidence=0.9, min_tracking_confidence=0.9)  # Increased confidence
draw = mp.solutions.drawing_utils

# Function to determine finger states
def fingers(landmarks):
    fingerTips = []
    tipIds = [4, 8, 12, 16, 20]

    # Thumb
    if landmarks[tipIds[0]][1] > landmarks[tipIds[0] - 1][1]:
        fingerTips.append(1)
    else:
        fingerTips.append(0)

    # Other fingers
    for id in range(1, 5):
        if landmarks[tipIds[id]][2] < landmarks[tipIds[id] - 3][2]:
            fingerTips.append(1)
        else:
            fingerTips.append(0)

    return fingerTips

# Function to detect hand landmarks
def handLandmarks(colorImg):
    landmarkList = []
    landmarkPositions = mainHand.process(colorImg)
    landmarkCheck = landmarkPositions.multi_hand_landmarks

    if landmarkCheck:
        for hand in landmarkCheck:
            draw.draw_landmarks(colorImg, hand, initHand.HAND_CONNECTIONS)
            h, w, c = colorImg.shape
            for index, landmark in enumerate(hand.landmark):
                centerX, centerY = int(landmark.x * w), int(landmark.y * h)
                landmarkList.append([index, centerX, centerY])
    return landmarkList

# Function to process the captured image
def process_image(image):
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    lmList = handLandmarks(imgRGB)

    if len(lmList) != 0:
        # Get coordinates of fingers
        x1, y1 = lmList[4][1:]  # Thumb
        x2, y2 = lmList[8][1:]  # Index
        x3, y3 = lmList[12][1:]  # Middle
        x4, y4 = lmList[16][1:]  # Ring
        x5, y5 = lmList[20][1:]  # Pinky
        finger = fingers(lmList)

        # Draw lines between fingers
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 3)
        cv2.line(image, (x2, y2), (x3, y3), (0, 0, 255), 3)
        cv2.line(image, (x3, y3), (x4, y4), (255, 0, 255), 3)
        cv2.line(image, (x4, y4), (x5, y5), (255, 255, 255), 3)

        # Calculate distances between fingers
        lengththind = hypot(x2 - x1, y2 - y1)
        lengthrinthu = hypot(x4 - x1, y4 - y1)
        lengthmidthu = hypot(x3 - x1, y3 - y1)

        # Mudra detection logic
        mudra = "No hand detected"
        if finger == [1, 1, 1, 1, 1] and lengththind < 150:
            cvzone.putTextRect(image, "Pataka", (50, 150), scale=5, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Pataka"
        elif finger[1] == 1 and finger[2] == 1 and finger[3] == 0 and finger[4] == 1 and lengthrinthu > 40:
            cvzone.putTextRect(image, "Tripataka", (50, 150), scale=5, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Tripataka"
        # Add other mudra detection conditions here...

        return image, mudra
    return image, "No hand detected"

# Mudra information page
def mudra_info():
    st.title("Mudra Detection: Explore Sacred Hand Gestures")
    st.write("Mudras are symbolic hand gestures used in various spiritual practices across cultures, especially in Hinduism and Buddhism.")
    mudra_details = {
        "Pataka": {
            "Description": "All fingers extended and joined, representing a flag.",
            "Symbolism": "Symbol of auspiciousness and divine presence."
        },
        "Tripataka": {
            "Description": "Thumb and little finger extended, others folded.",
            "Symbolism": "Represents creation, preservation, and destruction."
        },
        # Add other mudras here...
    }

    for mudra, details in mudra_details.items():
        st.subheader(mudra)
        st.write(f"**Description**: {details['Description']}")
        st.write(f"**Symbolism**: {details['Symbolism']}")
        st.write("---")

# Mudra detection page
def mudra_detection():
    st.title("Hand Gesture Recognition for Mudra Detection")
    camera_input = st.camera_input("Take a photo")

    if camera_input:
        image = Image.open(camera_input)
        image = np.array(image)  # Convert to NumPy array
        processed_image, mudra = process_image(image)
        st.image(processed_image, caption="Captured Image", channels="RGB")
        st.write(f"Detected Mudra: {mudra}")

# Main function to switch between pages
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Mudra Information", "Mudra Detection"])

    if page == "Mudra Information":
        mudra_info()
    elif page == "Mudra Detection":
        mudra_detection()

if __name__ == "__main__":
    main()
