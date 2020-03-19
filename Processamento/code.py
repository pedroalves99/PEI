import cv2
import numpy as np
cap = cv2.VideoCapture('HENRIQUE03.wmv')

if not cap.isOpened():
    print("Erro")
    exit()

_, p_frame = cap.read() #p_frame sao os valores no array. o true é ignorado pelo. cap.read() so tem valores quando se cria um ponto verde. senao é [0,0,0]
old_frame = cv2.cvtColor(p_frame, cv2.COLOR_BGR2GRAY)

#Lukas Kanade params
lk_params = dict(winSize = (15, 15),
                 maxLevel = 4,
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

point_selected = False
flag = 1
close = 1 ##

#Mouse Function
def addPoint(x, y):
    global old_points, origin_points
    a_point = np.array([[x, y]], dtype=np.float32)
    old_points = np.append(a_point, old_points, axis=0)
    origin_points = np.append(a_point, origin_points, axis=0)

def select_point(event, x, y, flags, params):
    global point, point_selected, old_points, flag, origin_points
    if event == cv2.EVENT_LBUTTONDOWN:
        point_selected = True
        if flag == 1:
            old_points = np.array([[x,y]], dtype=np.float32)
            origin_points = np.array([[x,y]], dtype=np.float32)
            flag+=1
        else: addPoint(x,y)
        cv2.circle(p_frame, (x, y), 5, (0, 255, 0), -1)
        print(old_points)

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", select_point) #quando se carrega no rato


while True:
    cv2.imshow('Frame', p_frame)

    if cv2.waitKey(27) & 0xFF == ord('p'): #vai buscar os ultimos 8 bits da tecla pressionada e no codigo ascii transforma numa letra. ord(p) dá o codigo ascii da letra
            break

while True:

    check ,frame = cap.read()

    if not check:
        print("Error buffering")

        cap1 = cv2.VideoCapture('HENRIQUE03.wmv')

        if not cap1.isOpened():
            print("Erro")
            exit()

        _, p_frame = cap1.read()  # p_frame sao os valores no array. o true é ignorado pelo. cap.read() so tem valores quando se cria um ponto verde. senao é [0,0,0]
        old_frame = cv2.cvtColor(p_frame, cv2.COLOR_BGR2GRAY)

        _, frame1 = cap1.read()
        gray_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        cap = cap1
        frame = frame1
        old_points = origin_points


    else:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if point_selected is True:
        #cv2.circle(frame,point, 5, (0,0,255), 2)

        new_points, status, error = cv2.calcOpticalFlowPyrLK(old_frame, gray_frame, old_points, None, **lk_params)
        #print(new_points)
        old_frame = gray_frame.copy()

        old_points = new_points

        for x,y in new_points:
            cv2.circle(frame, (x,y), 5, (0,255,0), 2)


    cv2.imshow("Frame", frame)
    key = cv2.waitKey(100)

    if key == 27: #ESC
        break
        close += 1


cap.release()
cv2.destroyAllWindows()