#here we will write two function one for getting angle btwn the fingers and another one for getting the distance btwn landmark points
import numpy as np

def get_angle(a,b,c): #this function is used to get the angle between the fingers
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])   #this is the formula to get the angle between the fingers
    #here we are calculating angle between bc and x axis and subtracting the angle between ab and x axis
    angle = np.abs(np.degrees(radians)) #convert the angle from radians to degrees
    return angle    #return the angle

def get_distance(landmark_list):    #this function is used to get the distance between the landmark points
    if len(landmark_list) < 2:  #if the length of the landmark list is less than 2 then
        return  
    (x1, y1), (x2, y2) = landmark_list[0], landmark_list[1]  #get the x and y coordinates of the first two landmarks
    L = np.hypot(x2 - x1, y2 - y1)  #this is the formula to get the distance between the two points(hypoit means hypotenuse and is used toi find eucledean distance)
    return np.interp(L, [0, 1], [0, 1000])  #return the distance between the two points(interpolate the distance between 0 and 1 to 0 and 1000)