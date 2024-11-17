import streamlit as st
import cv2
import numpy as np
from PIL import Image
from math import hypot
import cvzone
import mediapipe

# Initialize Mediapipe for hand landmarks
initHand = mediapipe.solutions.hands
mainHand = initHand.Hands(min_detection_confidence=0.9, min_tracking_confidence=0.9)  # Increased confidence
draw = mediapipe.solutions.drawing_utils

# Function to check finger states (open/closed)
def fingers(landmarks):
    fingerTips = []  
    tipIds = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips

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
    results = mainHand.process(colorImg)  
    handLandmarks = results.multi_hand_landmarks  

    if handLandmarks:
        for hand in handLandmarks:
            for index, landmark in enumerate(hand.landmark):
                draw.draw_landmarks(colorImg, hand, initHand.HAND_CONNECTIONS)  
                h, w, c = colorImg.shape  
                centerX, centerY = int(landmark.x * w), int(landmark.y * h)  
                landmarkList.append([index, centerX, centerY])  

    return landmarkList

# Function to process a single frame
def process_image(image):
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    lmList = handLandmarks(imgRGB)

    if len(lmList) != 0:
        # Get coordinates of fingers
        finger = fingers(lmList)
        mudra = "No hand detected"

        # Add mudra detection logic here...
        # Example for Pataka:
        if finger[1] == 1 and finger[0] == 1 and finger[2] == 1 and finger[3] == 1 and finger[4] == 1:
            cvzone.putTextRect(image, "Pataka", (50, 150), scale=5, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Pataka"

        return image, mudra

    return image, "No hand detected"

# Mudra Information Page
def mudra_info():
    st.title("Mudra Detection: Explore Sacred Hand Gestures")
    st.write("Mudras are symbolic hand gestures used in various spiritual practices across cultures, especially in Hinduism and Buddhism.")
    st.write("---")

    # Example Mudra Information
    mudra_details = {
        "Pataka": {
            "Description": "All fingers extended and joined, symbolizing a flag.",
            "Symbolism": "Represents auspiciousness and divine presence."
        }
    }

    for mudra, details in mudra_details.items():
        st.subheader(mudra)
        st.write(f"**Description**: {details['Description']}")
        st.write(f"**Symbolism**: {details['Symbolism']}")
        st.write("---")

# Mudra Detection with Live Webcam Feed
def mudra_detection_live():
    st.title("Live Hand Gesture Recognition for Mudra Detection")

    # Start webcam
    cap = cv2.VideoCapture(0)
    stframe = st.empty()  # Placeholder for live frame display

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            st.write("Failed to access the webcam.")
            break

        # Process the frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
        processed_frame, mudra = process_image(frame)

        # Display the processed frame and detected mudra
        stframe.image(processed_frame, caption=f"Detected Mudra: {mudra}", channels="RGB", use_column_width=True)

        # Stop the stream with a Streamlit button
        if st.button("Stop Webcam"):
            break

    cap.release()
    cv2.destroyAllWindows()

# Main function to handle navigation
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Mudra Information", "Mudra Detection (Live)"])

    if page == "Mudra Information":
        mudra_info()
    elif page == "Mudra Detection (Live)":
        mudra_detection_live()

# Entry point
if __name__ == "__main__":
    main()
