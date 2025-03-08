import cv2  #this is used to capture the video
import random   #this is used to generate random numbers
import mediapipe as mp  #this is used to detect the hands
import pyautogui    #this is used to control the mouse

from pynput.mouse import Button, Controller  #this is used to control the mouse
mouse=Controller()  #creating an object for the mouse

import util    #importing the util file

screen_width,screen_height=pyautogui.size()  #get the screen width and height


mpHands = mp.solutions.hands    #creating an object for hands
hands=mpHands.Hands(
    static_image_mode=False,    #this is for static image mode(model treats input as 
                                #a video stream and if true it wil treat input as a single image)
    model_complexity=1,   #this is for model complexity(can be 0,1 or 2)
    min_detection_confidence=0.7,   #this is for minimum detection confidence(higher value means lower detection rate)
    min_tracking_confidence=0.7,    #this is for minimum tracking confidence(higher value means lower tracking rate)
                                    # both the above values are in the range of 0 to 1
    max_num_hands=1  #this is for maximum number of hands
)

def find_finger_tip(processed): #this function is used to find the tip of the index finger
    if processed.multi_hand_landmarks: #if there are multiple hands
        hand_landmarks=processed.multi_hand_landmarks[0] #get the landmarks of the first hand
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP] #return the index finger tip
    
    return None #return None if there are no hands


def move_mouse(index_finger_tip):   #this function is used to move the mouse
    if index_finger_tip is not None:
        x=int(index_finger_tip.x*screen_width)  #get the x coordinate of the index finger tip
        y=int(index_finger_tip.y*screen_height) #get the y coordinate of the index finger tip
        pyautogui.moveTo(x,y)  #move the mouse to the x and y coordinates(moveTo is a function in pyautogui to move the mouse to the given coordinates)


def is_left_click(landmarks_list,thumb_index_dist):  #this function is used to check if the left click is pressed
    return (util.get_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8])<50 and 
            util.get_angle(landmarks_list[9],landmarks_list[10],landmarks_list[12])>90 and
            thumb_index_dist>50)
            #here we are checking if index finger is bent,middle finger is straight and the thumb finger is open
            
            
def is_right_click(landmarks_list,thumb_index_dist):     #this function is used to check if the right click is pressed
    return (util.get_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8])>90 and 
            util.get_angle(landmarks_list[9],landmarks_list[10],landmarks_list[12])<50 and
            thumb_index_dist>50)
            #here we are checking if index finger is straight,middle finger is bent and the thumb finger is open 
            
            
def is_double_click(landmarks_list,thumb_index_dist):   #this function is used to check if the double click is pressed
    return (util.get_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8])<50 and 
            util.get_angle(landmarks_list[9],landmarks_list[10],landmarks_list[12])<50 and
            thumb_index_dist>50)
            #here we are checking if index finger and middle finger are bent and the thumb finger is open
            
            
def is_screenshot(landmarks_list,thumb_index_dist):    #this function is used to check if the screen shot is taken
    return (util.get_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8])<50 and 
            util.get_angle(landmarks_list[9],landmarks_list[10],landmarks_list[12])<50 and
            thumb_index_dist<50)
            #here we are checking if index finger and middle finger are bent and the thumb finger is also closed
            
            
def detect_gestures(frame,landmarks_list,processed):  #this function is used to detect the gestures of the hand
    if len(landmarks_list)>=21:    #if the length of the landmark list is greater than or equal to 21
        index_finger_tip=find_finger_tip(processed) #get the index finger tip
        
        thumb_index_dist=util.get_distance([landmarks_list[4],landmarks_list[5]])  #get the distance between the thumb and index finger
        
        if thumb_index_dist<50 and util.get_angle(landmarks_list[5],landmarks_list[6],landmarks_list[8])>90:    #checking if thumb is closed and the index finger is uprigth
            move_mouse(index_finger_tip)    #move the mouse according to the index finger tip
            
        elif is_left_click(landmarks_list,thumb_index_dist):    #if the left click is pressed
            mouse.press(Button.left)    #press the left button of the mouse
            mouse.release(Button.left)  #release the left button of the mouse
            
            cv2.putText(frame,'Left Click',(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2,cv2.LINE_AA)  #put the text "Left Click" on the frame
            
        elif is_right_click(landmarks_list,thumb_index_dist):   #if the right click is pressed
            mouse.press(Button.right)   #press the right button of the mouse    
            mouse.release(Button.right) #release the right button of the mouse
            
            cv2.putText(frame,'Right Click',(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2,cv2.LINE_AA) #put the text "Right Click" on the frame
            
        elif is_double_click(landmarks_list,thumb_index_dist): #if the double click is pressed
            pyautogui.doubleClick() #double click the mouse
            
            cv2.putText(frame,'Double Click',(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2,cv2.LINE_AA)   #put the text "Double Click" on the frame 
            
        elif is_screenshot(landmarks_list,thumb_index_dist):    #if the screen shot is taken
            im1=pyautogui.screenshot()  #take the screenshot
            label=random.randint(1,1000)    #generate a random number between 1 and 1000
            im1.save(f'screenshot{label}.png')   #save the screenshot with the name "screenshot" and the random number generated
            
            cv2.putText(frame,'Screenshot Taken',(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2,cv2.LINE_AA)    #put the text "Screenshot Taken" on the frame
            

def main():
    #this part is for capturing the video by using opencv
    cap=cv2.VideoCapture(0)  #here 0 represents number of cameras(here 1 camera)
    draw=mp.solutions.drawing_utils  #this is for drawing the landmarks on the hand

    try:
        while cap.isOpened():
            ret, frame=cap.read() #checks whether its possible to read the frame of the screen

            if not ret:
                break  #break out if you cannot read the frame
            frame=cv2.flip(frame,1)   #flips the frame so that it looks like we are seing in a mirror
            
            #mediapipe requires the image to be in RGB format
            frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)  #converts the frame from BGR to RGB
            
            processed=hands.process(frameRGB)  #process the frame
            
            landmarks_list=[]  #this is to store the landmarks of the hand
            if processed.multi_hand_landmarks:  #if there are multiple hands
                hand_landmarks=processed.multi_hand_landmarks[0]  #get the landmarks of the first hand
                draw.draw_landmarks(frame,hand_landmarks,mpHands.HAND_CONNECTIONS)  #draw the landmarks on the hand
                
                #HAND_CONNECTIONS is used to connect the landmarks with lines
                
                for lm in hand_landmarks.landmark:  #take individual landmark in the hand and push it to the list
                    landmarks_list.append((lm.x,lm.y))  #append the x and y coordinates of the landmark
                    #for each frame it will create a list of 21 tuples where each tuple contains the x and y coordinates of the landmark
            
            detect_gestures(frame,landmarks_list,processed)  #this is to detect the gestures of the hand
                
            cv2.imshow('Frame',frame)  #show the captured frame by the name "Frame"
            if (cv2.waitKey(1) & 0xFF==ord('q')):  #this is to close the window
                break  #wait for 1ms after each frame read and break if q is pressed in the keyboard
    finally:
        cap.release()  #release all the captures
        cv2.destroyAllWindows()  #destroy all the winsows created by opencv


if __name__=='__main__':
    main()