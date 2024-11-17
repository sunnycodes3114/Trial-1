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

def fingers(landmarks):
    fingerTips = []  
    tipIds = [4, 8, 12, 16, 20] 
    
    if landmarks[tipIds[0]][1] > landmarks[tipIds[0] - 1][1]:
        fingerTips.append(1)
    else:
        fingerTips.append(0)
    
    for id in range(1, 5):
        if landmarks[tipIds[id]][2] < landmarks[tipIds[id] - 3][2]: 
            fingerTips.append(1)
        else:
            fingerTips.append(0)

    return fingerTips

def handLandmarks(colorImg):
    landmarkList = []  
    landmarkPositions = mainHand.process(colorImg)  
    landmarkCheck = landmarkPositions.multi_hand_landmarks  
    if landmarkCheck: 
        for hand in landmarkCheck:  
            for index, landmark in enumerate(hand.landmark): 
                draw.draw_landmarks(colorImg, hand, initHand.HAND_CONNECTIONS)  
                h, w, c = colorImg.shape  
                centerX, centerY = int(landmark.x * w), int(landmark.y * h)  
                landmarkList.append([index, centerX, centerY])  
    return landmarkList

# Function to process the captured image
import cv2
import numpy as np
from math import hypot
import cvzone

# Function to process the captured image
def process_image(image):
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    lmList = handLandmarks(imgRGB)

    if len(lmList) != 0:
        # Get coordinates of the fingers
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
        lengththind = hypot(x2 - x1, y2 - y1)  # Distance from thumb to index
        lengthindmid = hypot(x3 - x2, y3 - y2)  # Distance from index to middle
        lengthmidrin = hypot(x4 - x3, y4 - y3)  # Distance from middle to ring
        lengthrinpin = hypot(x5 - x4, y5 - y4)  # Distance from ring to pinky
        lengthrinthu = hypot(x4 - x1, y4 - y1)  # Distance from ring to thumb
        lengthmidthu = hypot(x3 - x1, y3 - y1)  # Distance from middle to thumb

        # Print out the calculated distances
        print("Calculation for Thumb to Index")
        print("The average distance", np.mean(lengththind))
        print("The Minimum Value", np.min(lengththind))
        print("The Maximum Value", np.max(lengththind))

        # Mudra detection logic based on finger positions and distances
        mudra = "No hand detected"
        if finger[1] == 1 and finger[0] == 1 and finger[2] == 1 and finger[3] == 1 and finger[4] == 1 and lengththind < 150:
            cvzone.putTextRect(image, "Pataka", (50, 150), scale=5, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Pataka"
        elif finger[1] == 1 and finger[2] == 1 and finger[3] == 0 and finger[4] == 1 and lengthrinthu > 40:
            cvzone.putTextRect(image, "Tripataka", (50, 150), scale=5, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Tripataka"
        elif finger[0] == 1 and finger[1] == 0 and finger[2] == 0 and finger[3] == 0 and finger[4] == 0:
            cvzone.putTextRect(image, "Shikaram", (50, 150), scale=4, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Shikaram"
        elif finger[0] == 0 and finger[1] == 1 and finger[2] == 1 and finger[3] == 0 and finger[4] == 0:
            cvzone.putTextRect(image, "Ardhapataka", (50, 150), scale=4, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Ardhapataka"
        elif finger[0] == 0 and finger[1] == 1 and finger[2] == 1 and finger[3] == 0 and finger[4] == 0 and 19 <= lengthindmid <= 94:
            cvzone.putTextRect(image, "Kartharimukha", (50, 150), scale=4, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Kartharimukha"
        elif finger[1] == 1 and finger[2] == 1 and finger[3] == 0 and finger[4] == 1 and 12 <= lengthrinthu <= 40:
            cvzone.putTextRect(image, "Mayura", (50, 150), scale=4, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Mayura"
        elif finger[1] == 1 and finger[0] == 1 and finger[2] == 1 and finger[3] == 1 and finger[4] == 1 and 150 <= lengththind <= 300:
            cvzone.putTextRect(image, "Ardhachandra", (50, 150), scale=5, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Ardhachandra"
        elif finger[1] == 0 and finger[0] == 1 and finger[2] == 1 and finger[3] == 1 and finger[4] == 1:
            cvzone.putTextRect(image, "Arala", (50, 150), scale=5, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Arala"
        elif finger[3] == 1 and finger[4] == 1 and 7 <= lengthmidthu <= 40 and 5 <= lengththind <= 30 and 10 <= lengthindmid <= 33:
            cvzone.putTextRect(image, "Katakamukaha", (50, 150), scale=5, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Katakamukaha"
        elif finger[1] == 1 and finger[4] == 1 and 3 <= lengthrinthu <= 30 and 1 <= lengthmidthu <= 15 and 1 <= lengthmidrin <= 25:
            cvzone.putTextRect(image, "Simhamukaha", (50, 150), scale=5, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Simhamukaha"
        elif finger[2] == 0 and finger[3] == 0 and finger[4] == 0 and finger[0] == 1 and 10 <= lengththind <= 40:
            cvzone.putTextRect(image, "Kapitha", (50, 150), scale=5, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Kapitha"
        elif finger[1] == 0 and finger[0] == 0 and finger[2] == 0 and finger[3] == 0 and finger[4] == 0 and 3 <= lengththind <= 15:
            cvzone.putTextRect(image, "Mushti", (50, 150), scale=5, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Mushti"
        elif finger[1] == 1 and finger[0] == 0 and finger[2] == 0 and finger[3] == 0 and finger[4] == 0:
            cvzone.putTextRect(image, "Soochi", (50, 150), scale=5, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Soochi"
        elif finger[1] == 1 and finger[0] == 1 and finger[2] == 0 and finger[3] == 0 and finger[4] == 0:
            cvzone.putTextRect(image, "Chandrakala", (50, 150), scale=5, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Chandrakala"
        elif finger[1] == 0 and finger[0] == 1 and finger[2] == 0 and finger[3] == 0 and finger[4] == 1:
            cvzone.putTextRect(image, "Mrigashirsha", (50, 150), scale=5, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Mrigashirsha"
        elif finger[1] == 1 and finger[0] == 1 and finger[2] == 1 and finger[3] == 1 and finger[4] == 0 and 30 <= lengththind <= 155 and 20 <= lengthindmid <= 70 and 10 <= lengthmidrin <= 120:
            cvzone.putTextRect(image, "Alapadmakam", (50, 150), scale=5, thickness=5, colorR=(0, 200, 0), offset=20)
            mudra = "Alapadmakam"

        return image, mudra
    return image, "No hand detected"

def mudra_info():
    st.title("Mudra Detection: Explore Sacred Hand Gestures")
    st.write("Mudras are symbolic hand gestures used in various spiritual practices across cultures, especially in Hinduism and Buddhism.")
    st.write("Below is the list of Mudras detected by this app:")

    mudra_details = {
        "Pataka": {
            "Description": "This mudra is made with all fingers extended and joined, representing the flag of the universe. It is used for offerings, rituals, and prayers.",
            "Symbolism": "A symbol of auspiciousness and divine presence. It is said to evoke the energy of the divine."
        },
        "Tripataka": {
            "Description": "The thumb and little finger are extended, while the other fingers remain folded.",
            "Symbolism": "Often used in rituals to invoke blessings and represent the three aspects of creation: creation, preservation, and destruction."
        },
        "Shikaram": {
            "Description": "The thumb is raised while the other fingers are folded.",
            "Symbolism": "Represents the peak of meditation and spiritual wisdom. It symbolizes the pinnacle of self-realization."
        },
        "Ardhapataka": {
            "Description": "The index finger and thumb are raised while the other fingers are folded.",
            "Symbolism": "A gesture of communication with the universe and a representation of the connection between the material and spiritual realms."
        },
        "Kartharimukha": {
            "Description": "The index and middle fingers are extended with the thumb and ring fingers folded, and the pinky finger extended.",
            "Symbolism": "Represents the destructive energy of the universe, used to ward off negative forces."
        },
        "Mayura": {
            "Description": "The index and pinky fingers are extended while the thumb, middle, and ring fingers are folded.",
            "Symbolism": "Represents the beauty and grace of a peacock, symbolizing strength, renewal, and beauty."
        },
        "Ardhachandra": {
            "Description": "The thumb and pinky are extended, while the other fingers are folded.",
            "Symbolism": "Symbolizes the moon and its phases, representing calmness and balance."
        },
        "Arala": {
            "Description": "The thumb and little finger are extended while the other fingers are folded.",
            "Symbolism": "Represents kindness, goodwill, and the sharing of knowledge."
        },
        "Katakamukaha": {
            "Description": "The index and middle fingers are extended, and the other fingers are folded, with the palms facing outwards.",
            "Symbolism": "Represents a ring or ornament, symbolizing protection, beauty, and purity."
        },
        "Simhamukaha": {
            "Description": "The index and pinky fingers are extended while the other fingers are folded.",
            "Symbolism": "This mudra is known to symbolize the lion's face, invoking courage and strength."
        },
        "Kapitha": {
            "Description": "The index finger is extended while the other fingers are folded, forming a fist.",
            "Symbolism": "Represents the flower, symbolizing purity, strength, and the blossoming of new ideas."
        },
        "Mushti": {
            "Description": "All fingers are curled into a fist.",
            "Symbolism": "Symbolizes control and focus, often used to build inner strength and willpower."
        },
        "Soochi": {
            "Description": "The index finger is extended while the other fingers are folded.",
            "Symbolism": "Represents a needle, used for focus, precision, and detail."
        },
        "Chandrakala": {
            "Description": "The thumb and index finger are extended, while the other fingers are folded.",
            "Symbolism": "Represents the crescent moon, symbolizing grace, balance, and spiritual awakening."
        },
        "Mrigashirsha": {
            "Description": "The thumb, index, and pinky fingers are extended.",
            "Symbolism": "Represents the deer’s head, symbolizing gentleness, peace, and the pursuit of the unattainable."
        },
        "Alapadmakam": {
            "Description": "The thumb and pinky are extended, while the other fingers are folded.",
            "Symbolism": "Represents the blooming of the lotus flower, symbolizing beauty, awakening, and spiritual enlightenment."
        }
    }

    # Display each mudra with its description and symbolism
    for mudra, details in mudra_details.items():
        st.subheader(mudra)
        st.write(f"**Description**: {details['Description']}")
        st.write(f"**Symbolism**: {details['Symbolism']}")
        st.write("---")

# Detection Page for Mudra Recognition
def mudra_detection():
    st.title("Hand Gesture Recognition for Mudra Detection")
    
    camera_input = st.camera_input("Take a photo")
    
    if camera_input:
        # Process the captured photo
        image = Image.open(camera_input)
        image = np.array(image)  # Convert to NumPy array

        # Process image and identify mudra
        processed_image, mudra = process_image(image)

        # Show the processed image and identified mudra
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



