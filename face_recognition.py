########################################### IMPORT WORKING FINE

import cv2 as cv
import face_recognition
from tkinter import *
import os
import numpy as np
########################################### CALLING FUNCTION WORKING FiNE

def name1():
    d = 'pic_storage/' + entry.get()
    cv.imwrite(d + '.jpg', frame)
    return None

########################################### WELCOME PAGE
a = cv.imread('space.jpg')
a = cv.resize(a, (1000, 700))
font = cv.FONT_HERSHEY_SIMPLEX
org = (50, 400)
fontScale = 6
color = (255, 0, 255)
thickness = 4
image = cv.putText(a, 'WELCOME!', org, font, fontScale, color, thickness, cv.LINE_AA)



cv.imshow('frame', image)
cv.waitKey(1000)

############################################ FILE SAVING PATH
s = r'C:\Users\Divyanshu Nautiyal\Desktop\New folder\pic_storage'
if not os.path.exists(s):
    os.makedirs(s)
############################################ EXTRATION OF IMAGE
listimg = os.listdir(s)
name = list()
image = list()
c=0
for cl in listimg:
    curimg = cv.imread(s+'\\'+cl)
    image.append(curimg)
    name.append(cl.split('.')[0])
    c=c+1
print(name)
############################################ FILE SAVING PATH
def findEncode(images):
    encolist = list()

    for img in images:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        facecurrs = face_recognition.face_locations(img)
        encode = face_recognition.face_encodings(img, facecurrs)[0]
        print(type(encode))
        encolist.append(encode)
    return encolist
encode_list = findEncode(image)

###################################### VIDEO ACTIVATION

vid = cv.VideoCapture(0)
while (True):

    ret, frame = vid.read()
    faces = cv.resize(frame, (0, 0), None, 0.25, 0.25)
    img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    facecurr = face_recognition.face_locations(img)
    ####################################################### CALCULATING FACE LOCATION
    if len(facecurr) != 0:

        encodecurr = face_recognition.face_encodings(img, facecurr)[0]

        matches = face_recognition.compare_faces(encode_list, encodecurr)
        faceDis = face_recognition.face_distance(encode_list, encodecurr)
        print(faceDis.shape)
        matchindex = np.argmin(faceDis)
        print(matchindex)
        matchindex  =matchindex % c
        if (matches[matchindex]).any():
            curname = name[matchindex].upper()
            y1, x2, y2, x1 = facecurr[0]
            cv.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 1)
            cv.putText(frame, curname, (x1 + 2, y2 - 2), font, .75 , color, 1)
        else:
            y1, x2, y2, x1 = facecurr[0]
            cv.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 1)
            cv.putText(frame, "not found", (x1 + 2, y2 - 2), font, .75, color, 1)
    image = cv.putText(frame, 'PRESS space bar to exit OR q to save new image', (10, 50), font, 0.5, (0, 0, 255), 1, cv.LINE_AA)
    cv.imshow('frame', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
 ####################################################### GRAPICAL WINDOW TO SAVE IMAGE
        root = Tk()
        root.title('SAVE IMAGE')
        root.geometry('200x200')
        entry = Entry(root, width=20)
        entry.pack()
        Button(root, text="SAVE", command=name1).pack()
        Button(root, text="CLOSE", command=root.destroy).pack()
        root.mainloop()

    if cv.waitKey(1) & 0xFF == ord(' '):
        break
vid.release()
cv.destroyAllWindows()