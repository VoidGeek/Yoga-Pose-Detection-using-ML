import cv2 
import numpy as np 
import mediapipe as mp 
from keras.models import load_model 
import pygame
pygame.init()
def inFrame(lst):
    if lst[28].visibility > 0.6 and lst[27].visibility > 0.6 and lst[15].visibility > 0.6 and lst[16].visibility > 0.6:
        return True 
    return False

model = load_model("model.h5")
label = np.load("labels.npy")

holistic = mp.solutions.pose
holis = holistic.Pose()
drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
desired_width = 1280
desired_height = 920
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

while True:
    lst = []

    _, frm = cap.read()

    window = np.zeros((960, 960, 3), dtype="uint8")

    frm = cv2.flip(frm, 1)

    res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

    frm = cv2.blur(frm, (4, 4))
    if res.pose_landmarks and inFrame(res.pose_landmarks.landmark):
        for i in res.pose_landmarks.landmark:
            lst.append(i.x - res.pose_landmarks.landmark[0].x)
            lst.append(i.y - res.pose_landmarks.landmark[0].y)

        lst = np.array(lst).reshape(1, -1)

        p = model.predict(lst)
        pred = label[np.argmax(p)]

        if p[0][np.argmax(p)] > 0.75:
            cv2.putText(window, pred, (180, 180), cv2.FONT_ITALIC, 1.3, (0, 255, 0), 4)
            my_sound = pygame.mixer.Sound('sucess.mp3')
            my_sound.play()
        else:
             cv2.putText(window, " Wrong  Yoga Postion ", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 165, 255), 3, cv2.LINE_AA)
             my_sound = pygame.mixer.Sound('warning.mp3')
             my_sound.play()

    else: 
      
        cv2.putText(window, "Wrong Yoga postion", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 165, 255), 3, cv2.LINE_AA)
        
    drawing.draw_landmarks(frm, res.pose_landmarks, holistic.POSE_CONNECTIONS,
                            connection_drawing_spec=drawing.DrawingSpec(color=(255, 255, 255), thickness=6),
                            landmark_drawing_spec=drawing.DrawingSpec(color=(0, 0, 255), circle_radius=3, thickness=3))

    # Resize the frame to fit into the window
    resized_frame = cv2.resize(frm, (640, 480))

    # Calculate the position to place the frame at the center of the window
    start_x = (window.shape[1] - resized_frame.shape[1]) // 2
    start_y = (window.shape[0] - resized_frame.shape[0]) // 2
    end_x = start_x + resized_frame.shape[1]
    end_y = start_y + resized_frame.shape[0]

    # Position the resized frame at the calculated location in the window
    window[start_y:end_y, start_x:end_x, :] = resized_frame

    cv2.imshow("window", window)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        cap.release()
        break
