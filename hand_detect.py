import cv2 as cv
import numpy as np
import math

camera = cv.VideoCapture(0)


lower_color = np.array([0, 50, 120], dtype=np.uint8)
upper_color = np.array([180, 150, 250], dtype=np.uint8)

def get_contours(binary_img):
    contours,_ = cv.findContours(binary_img,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

    return contours

def get_contour_center(contour):
    M = cv.moments(contour)
    cx = -1
    cy = -1
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

    return cx,cy

def draw_hand(binary_image,rgb_image,contours,img_no):
    black_image = np.zeros([binary_image.shape[0],binary_image.shape[1],3],np.uint8)

    for c in contours:
        area = cv.contourArea(c)
        perimeter = cv.arcLength(c, True)
        ((x, y), radius) = cv.minEnclosingCircle(c)
        if (area > 130):
            #cv.drawContours(rgb_image, [c], -1, (150, 250, 150), 1)
            #cv.drawContours(black_image, [c], -1, (150, 250, 150), 1)
            cx, cy = get_contour_center(c)
            # cv.circle(rgb_image, (cx, cy), (int)(radius), (0, 0, 255), 1)
            # cv.circle(black_image, (cx, cy), (int)(radius), (0, 0, 255), 1)
            # cv.circle(black_image, (cx, cy), 5, (150, 150, 255), -1)
    #         print('Area: {}, Perimeter: {}'.format(area, perimeter))
    # print('Number of contours in  image {}: {}'.format(img_no,len(contours)))
    cv.imshow('RGB Image Contours in image ', rgb_image)
    # cv.imshow('Black Image Contours ', black_image)


def analyze_defects(cnt,roi):
    epsilon = 0.0005 * cv.arcLength(cnt, True)
    approx = cv.approxPolyDP(cnt, epsilon, True)

    hull = cv.convexHull(approx, returnPoints=False)
    defects = cv.convexityDefects(approx, hull)

    l = 0
    if defects is not None:
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(approx[s][0])
            end = tuple(approx[e][0])
            far = tuple(approx[f][0])
            pt = (100, 180)

            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            s = (a + b + c) / 2
            ar = math.sqrt(s * (s - a) * (s - b) * (s - c))

            d = (2 * ar) / a

            angle = math.acos((b**2 + c**2 - a**2) / (2 * b * c)) * 57

            if angle <= 90 and d > 30:
                print(angle)
                l += 1
                cv.circle(roi, far, 3, [255, 0, 0], -1)
            cv.line(roi, start, end, [0, 255, 0], 2)
    return l

def analyze_contours(frame,cnt,l,img_no):
    hull = cv.convexHull(cnt)

    areahull = cv.contourArea(hull)
    areacnt = cv.contourArea(cnt)

    arearatio = ((areahull - areacnt) / areacnt) * 100

    font = cv.FONT_HERSHEY_SIMPLEX
    if img_no == 1:
        if l == 1:
            if areacnt < 2000:
                cv.putText(frame, 'Put hand in the box', (0, 50), font, 2,(0, 0, 255), 3, cv.LINE_AA)
            else:
                if arearatio < 12:
                    cv.putText(frame, 'Stop', (0, 50), font, 2, (0, 0, 255), 3,cv.LINE_AA)
                # elif arearatio < 17.5:
                #     cv.putText(frame, 'Fixe', (0, 50), font, 2, (0, 0, 255), 3,cv.LINE_AA)
                else:
                    cv.putText(frame, 'Stop', (0, 50), font, 2, (0, 0, 255), 3,cv.LINE_AA)
        # elif l == 2:
        #     cv.putText(frame, '2', (0, 50), font, 2, (0, 0, 255), 3, cv.LINE_AA)
        # elif l == 3:
        #     if arearatio < 27:
        #         cv.putText(frame, '3', (0, 50), font, 2, (0, 0, 255), 3,cv.LINE_AA)
        #     else:
        #         cv.putText(frame, 'ok', (0, 50), font, 2, (0, 0, 255), 3,cv.LINE_AA)
        elif l == 4:
            cv.putText(frame, 'Prev', (0, 50), font, 2, (0, 0, 255), 3, cv.LINE_AA)
        elif l == 5:
            cv.putText(frame, 'Prev', (0, 50), font, 2, (0, 0, 255), 3, cv.LINE_AA)
        else:
            cv.putText(frame, 'reposition', (10, 50), font, 2, (0, 0, 255), 3,cv.LINE_AA)

    else:
        if l == 1:
            if areacnt < 2000:
                cv.putText(frame, 'Put hand in the box', (800, 50), font, 2,(0, 0, 255), 3, cv.LINE_AA)
            else:
                if arearatio < 12:
                    cv.putText(frame, 'Start', (800, 50), font, 2, (0, 0, 255), 3,cv.LINE_AA)
                # elif arearatio < 17.5:
                #     cv.putText(frame, 'Fixe', (800, 50), font, 2, (0, 0, 255), 3,cv.LINE_AA)
                else:
                    cv.putText(frame, 'Start', (800, 50), font, 2, (0, 0, 255), 3,cv.LINE_AA)
        # elif l == 2:
        #     cv.putText(frame, '2', (800, 50), font, 2, (0, 0, 255), 3, cv.LINE_AA)
        # elif l == 3:
        #     if arearatio < 27:
        #         cv.putText(frame, '3', (800, 50), font, 2, (0, 0, 255), 3,cv.LINE_AA)
        #     else:
        #         cv.putText(frame, 'ok', (800, 50), font, 2, (0, 0, 255), 3,cv.LINE_AA)
        elif l == 4:
            cv.putText(frame, 'Next', (800, 50), font, 2, (0, 0, 255), 3, cv.LINE_AA)
        elif l == 5:
            cv.putText(frame, 'Next', (800, 50), font, 2, (0, 0, 255), 3, cv.LINE_AA)
        else:
            cv.putText(frame, 'reposition', (800, 50), font, 2, (0, 0, 255), 3,cv.LINE_AA)

while True:
    _,frame = camera.read()
    frame = cv.resize(frame,(1200,720))
    cv.rectangle(frame,(50, 50), (300, 300),(0,255,0),1)
    cv.rectangle(frame,(800, 50), (1050, 300),(0,255,0),1)
    crop_img_left = frame[50:300,50:300]
    crop_img_right = frame[50:300,800:1050]

    hsv1 = cv.cvtColor(crop_img_left,cv.COLOR_RGB2HSV)
    mask1 = cv.inRange(hsv1,lower_color,upper_color)

    mask1 = cv.dilate(mask1,np.ones((3,3),np.uint8),iterations=3)
    mask1 = cv.erode(mask1,np.ones((3,3),np.uint8),iterations=3)

    mask1 = cv.GaussianBlur(mask1,(5,5),90)

    hsv2 = cv.cvtColor(crop_img_right,cv.COLOR_RGB2HSV)
    mask2 = cv.inRange(hsv2,lower_color,upper_color)

    mask2 = cv.dilate(mask2,np.ones((3,3),np.uint8),iterations=3)
    mask2 = cv.erode(mask2,np.ones((3,3),np.uint8),iterations=3)

    mask2 = cv.GaussianBlur(mask2,(5,5),90)

    contours1 = get_contours(mask1)
    contours2 = get_contours(mask2)

    try:
        cnt1 = max(contours1,key=lambda x: cv.contourArea(x))
        cnt2 = max(contours2,key=lambda x: cv.contourArea(x))
        l1 = analyze_defects(cnt1,crop_img_left)
        l2 = analyze_defects(cnt2,crop_img_right)
        analyze_contours(frame,cnt1,l1+1,1)
        analyze_contours(frame,cnt2,l2+1,2)
    except:
        pass

    draw_hand(mask1,frame,contours1,1)
    #draw_hand(mask2,frame,contours2,2)
    key = cv.waitKey(4)
    if key == ord('q'):
        break

cv.destroyAllWindows()
camera.release()
