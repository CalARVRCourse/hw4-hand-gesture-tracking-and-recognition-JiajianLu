import numpy as np
import cv2
import pyautogui
max_value = 255
max_type = 4
max_binary_value = 255
trackbar_type = 'Type: \n 0: Binary \n 1: Binary Inverted \n 2: Truncate \n 3: To Zero \n 4: To Zero Inverted'
trackbar_value = 'Value'
trackbar_blur = 'Blur kernel size'
window_name = 'Threshold Demo'
isColor = False

def nothing(x):
    pass
cam = cv2.VideoCapture(0)


#
def preprocess_img(frame):
    lower_HSV = np.array([0, 40, 0], dtype="uint8")
    upper_HSV = np.array([25, 255, 255], dtype="uint8")

    convertedHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    skinMaskHSV = cv2.inRange(convertedHSV, lower_HSV, upper_HSV)

    lower_YCrCb = np.array((0, 138, 67), dtype="uint8")
    upper_YCrCb = np.array((255, 173, 133), dtype="uint8")

    convertedYCrCb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    skinMaskYCrCb = cv2.inRange(convertedYCrCb, lower_YCrCb, upper_YCrCb)

    skinMask = cv2.add(skinMaskHSV, skinMaskYCrCb)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    skinMask = cv2.erode(skinMask, kernel, iterations=2)
    skinMask = cv2.dilate(skinMask, kernel, iterations=2)

    # blur the mask to help remove noise, then apply the
    # mask to the frame
    skinMask = cv2.GaussianBlur(skinMask, (3,3), 0)
    skin = cv2.bitwise_and(frame, frame, mask=skinMask)

    return skin

def get_connected_components(frame):
    ret, markers, stats, centroids = cv2.connectedComponentsWithStats(frame, ltype=cv2.CV_16U)
    markers = np.array(markers, dtype=np.uint8)
    label_hue = np.uint8(179 * markers / np.max(markers))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
    labeled_img[label_hue == 0] = 0
    return ret, labeled_img, stats

# part 1
while(True):
    # Capture frame-by-frame
    ret, frame = cam.read()
    if not ret:
        print("NO VIDEO")
    # Our operations on the frame come here
    frame = preprocess_img(frame)

    src_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #ret, thresholdedHandImage = cv2.threshold(src_gray, 0, max_binary_value, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # Display the resulting frame
    cv2.imshow('frame',src_gray)
    #cv2.imshow('frame',thresholdedHandImage)
    k = cv2.waitKey(1)  # k is the key pressed
    if k == 27 or k == 113:  # 27, 113 are ascii for escape and q respectively
        cv2.destroyAllWindows()
        cam.release()

# part 2

# cv2.namedWindow(window_name)
# cv2.createTrackbar(trackbar_type, window_name, 3, max_type, nothing)
# # Create Trackbar to choose Threshold value
# cv2.createTrackbar(trackbar_value, window_name, 0, max_value, nothing)
# # Call the function to initialize
# cv2.createTrackbar(trackbar_blur, window_name, 1, 20, nothing)
# # create switch for ON/OFF functionality
# color_switch = 'Color'
# cv2.createTrackbar(color_switch, window_name, 0, 1, nothing)
# cv2.createTrackbar('Contours', window_name, 0, 1, nothing)
#
#
#
# while True:
#     ret, frame = cam.read()
#     if not ret:
#         break
#
#     # 0: Binary
#     # 1: Binary Inverted
#     # 2: Threshold Truncated
#     # 3: Threshold to Zero
#     # 4: Threshold to Zero Inverted
#     frame = preprocess_img(frame)
#     threshold_type = cv2.getTrackbarPos(trackbar_type, window_name)
#     threshold_value = cv2.getTrackbarPos(trackbar_value, window_name)
#     blur_value = cv2.getTrackbarPos(trackbar_blur, window_name)
#     blur_value = blur_value + (blur_value % 2 == 0)
#     isColor = (cv2.getTrackbarPos(color_switch, window_name) == 1)
#     findContours = (cv2.getTrackbarPos('Contours', window_name) == 1)
#
#     # convert to grayscale
#     src_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     ret, dst = cv2.threshold(src_gray, 0, max_binary_value, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
#     #blur = cv2.GaussianBlur(dst, (blur_value, blur_value), 0)
#     ret, labeled_img, stats = get_connected_components(dst)
#     if (ret>2):
#         try:
#             statsSortedByArea = stats[np.argsort(stats[:, 4])]
#             roi = statsSortedByArea[-3][0:4]
#             x, y, w, h = roi
#             subImg = labeled_img[y:y + h, x:x + w]
#             subImg = cv2.cvtColor(subImg, cv2.COLOR_BGR2GRAY);
#             _, contours, _ = cv2.findContours(subImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#             maxCntLength = 0
#             for i in range(0, len(contours)):
#                 cntLength = len(contours[i])
#                 if (cntLength > maxCntLength):
#                     cnt = contours[i]
#                     maxCntLength = cntLength
#             if (maxCntLength >= 5):
#                 ellipseParam = cv2.fitEllipse(cnt)
#                 (x, y), (MA, ma), angle = ellipseParam
#                 subImg = cv2.cvtColor(subImg, cv2.COLOR_GRAY2RGB);
#                 subImg = cv2.ellipse(subImg, ellipseParam, (0, 255, 0), 2)
#
#             subImg = cv2.resize(subImg, (0, 0), fx=3, fy=3)
#             cv2.imshow("ROI " + str(2), subImg)
#             #cv2.waitKey(1)
#             k = cv2.waitKey(1)  # k is the key pressed
#             if k == 27 or k == 113:  # 27, 113 are ascii for escape and q respectively
#                 # exit
#                 cv2.destroyAllWindows()
#                 cam.release()
#                 break
#         except:
#             print("No hand found")
#     cv2.imshow(window_name, labeled_img)
#     k = cv2.waitKey(1)  # k is the key pressed
#     if k == 27 or k == 113:  # 27, 113 are ascii for escape and q respectively
#         # exit
#         cv2.destroyAllWindows()
#         cam.release()
#         break
#
# # blur = 149
# # blur_kernel_size = 3
# # #to zero
# # type = 3
#
# #part 3
# while True:
#     ret, frame = cam.read()
#     if not ret:
#         break
#
#     frame = preprocess_img(frame)
#     src_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     ret, thresholdedHandImage = cv2.threshold(src_gray, 0, max_binary_value, cv2.THRESH_OTSU)
#     _, contours, _ = cv2.findContours(thresholdedHandImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     contours = sorted(contours, key=cv2.contourArea, reverse=True)
#     if len(contours) > 1:
#         largestContour = contours[0]
#         hull = cv2.convexHull(largestContour, returnPoints=False)
#         thresholdedHandImage = cv2.cvtColor(thresholdedHandImage, cv2.COLOR_GRAY2BGR)
#         thresholdedHandImage_no_filter = thresholdedHandImage.copy()
#         defects = cv2.convexityDefects(largestContour, hull)
#         if (not isinstance(defects, type(None))):
#             fingerCount = 0
#             fingerCount_no_filter = 0
#             for i in range(defects.shape[0]):
#                 s, e, f, d = defects[i, 0]
#                 start = tuple(largestContour[s][0])
#                 end = tuple(largestContour[e][0])
#                 far = tuple(largestContour[f][0])
#
#                 c_squared = (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2
#                 a_squared = (far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2
#                 b_squared = (end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2
#                 angle = np.arccos((a_squared + b_squared - c_squared) / (2 * np.sqrt(a_squared * b_squared)))
#                 fingerCount_no_filter += 1
#                 if angle <= np.pi / 3:
#                     fingerCount += 1
#                     cv2.circle(thresholdedHandImage, far, 4, [0, 0, 255], -1)
#                 cv2.circle(thresholdedHandImage_no_filter, far, 4, [0, 0, 255], -1)
#                 cv2.line(thresholdedHandImage, start, end, [0, 255, 0], 2)
#                 cv2.line(thresholdedHandImage_no_filter, start, end, [0, 255, 0], 2)
#             if fingerCount > 0:
#                 fingerCount += 1
#             if fingerCount_no_filter > 0:
#                 fingerCount_no_filter += 1
#             cv2.putText(thresholdedHandImage, str(fingerCount), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2, cv2.LINE_AA)
#             cv2.putText(thresholdedHandImage_no_filter, str(fingerCount_no_filter), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2,
#                         cv2.LINE_AA)
#     cv2.imshow(window_name, thresholdedHandImage)
#     cv2.imshow('no_filter', thresholdedHandImage_no_filter)
#     k = cv2.waitKey(1)  # k is the key pressed
#     if k == 27 or k == 113:  # 27, 113 are ascii for escape and q respectively
#         # exit
#         cv2.destroyAllWindows()
#         cam.release()
#         break
#
# #part 4
# screenX = 1920
# screenY = 1200
# imageX = 640
# imageY = 480
# offsetX = 0
# offsetY = 0
# scaleX = screenX / imageX
# scaleY = screenY / imageY
# XYbuffer = []
# angle_buffer = []
# area_buffer = []
# finger_buffer = []
# num_frames = 0
#
# def move_mouse(X, Y):
#     pyautogui.moveTo(X, Y, duration=0.02, tween=pyautogui.easeInOutQuad)
#
# def ZoomIn():
#     pyautogui.hotkey('ctrl', '+')
#
#
# def ZoomOut():
#     pyautogui.hotkey('ctrl', '-')
#
#
# def RotateRight():
#     pyautogui.hotkey('ctrl', 'r')
#
#
# def RotateLeft():
#     pyautogui.hotkey('ctrl', 'r')
#     pyautogui.hotkey('ctrl', 'r')
#     pyautogui.hotkey('ctrl', 'r')
#
#
# def isIncreased(handRingArea, prevHandRingArea, threshold=5):
#     return (handRingArea > prevHandRingArea + threshold)
#
#
# def isDecreased(handRingArea, prevHandRingArea, threshold=5):
#     return (handRingArea < prevHandRingArea - threshold)
#
# prevHandRingArea = None
# prevAngle = None
# while True:
#     ret, frame = cam.read()
#     if not ret:
#         break
#     num_frames += 1
#     frame = preprocess_img(frame)
#     src_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     ret, thresholdedHandImage = cv2.threshold(src_gray, 0, max_binary_value, cv2.THRESH_OTSU)
#
#     _, contours, _ = cv2.findContours(thresholdedHandImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     contours = sorted(contours, key=cv2.contourArea, reverse=True)
#     if len(contours) > 1:
#         largestContour = contours[0]
#         M = cv2.moments(largestContour)
#         cX = offsetX + scaleX * int(M["m10"] / M["m00"])
#         cY = offsetY + scaleY * int(M["m01"] / M["m00"])
#         XYbuffer.append([cX,cY])
#         hull = cv2.convexHull(largestContour, returnPoints=False)
#         defects = cv2.convexityDefects(largestContour, hull)
#         thresholdedHandImage = cv2.cvtColor(thresholdedHandImage, cv2.COLOR_GRAY2BGR)
#         if (not isinstance(defects, type(None))):
#             fingerCount = 0
#             for i in range(defects.shape[0]):
#                 s, e, f, d = defects[i, 0]
#                 start = tuple(largestContour[s][0])
#                 end = tuple(largestContour[e][0])
#                 far = tuple(largestContour[f][0])
#
#                 c_squared = (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2
#                 a_squared = (far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2
#                 b_squared = (end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2
#                 angle = np.arccos((a_squared + b_squared - c_squared) / (2 * np.sqrt(a_squared * b_squared)))
#
#                 if angle <= np.pi / 3:
#                     fingerCount += 1
#                     cv2.circle(thresholdedHandImage, far, 4, [0, 0, 255], -1)
#
#                 cv2.line(thresholdedHandImage, start, end, [0, 255, 0], 2)
#             if fingerCount > 0:
#                 fingerCount += 1
#             cv2.putText(thresholdedHandImage, str(fingerCount), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0),
#                         2, cv2.LINE_AA)
#             finger_buffer.append(fingerCount)
#     # cv2.imshow(window_name, thresholdedHandImage)
#     # k = cv2.waitKey(1)  # k is the key pressed
#     # if k == 27 or k == 113:  # 27, 113 are ascii for escape and q respectively
#     #     # exit
#     #     cv2.destroyAllWindows()
#     #     cam.release()
#     #     break
#     ret, dst = cv2.threshold(src_gray, 0, max_binary_value, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#     ret, labeled_img, stats = get_connected_components(dst)
#     if (ret>2):
#         try:
#             statsSortedByArea = stats[np.argsort(stats[:, 4])]
#             handRingArea = statsSortedByArea[-3][2] * statsSortedByArea[-3][3]
#
#             roi = statsSortedByArea[-3][0:4]
#             x, y, w, h = roi
#             subImg = labeled_img[y:y + h, x:x + w]
#             subImg = cv2.cvtColor(subImg, cv2.COLOR_BGR2GRAY)
#             _, contours, _ = cv2.findContours(subImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#             maxCntLength = 0
#             for i in range(0, len(contours)):
#                 cntLength = len(contours[i])
#                 if (cntLength > maxCntLength):
#                     cnt = contours[i]
#                     maxCntLength = cntLength
#             if (maxCntLength >= 5):
#
#                 ellipseParam = cv2.fitEllipse(cnt)
#                 subImg = cv2.cvtColor(subImg, cv2.COLOR_GRAY2RGB);
#                 subImg = cv2.ellipse(subImg, ellipseParam, (0, 255, 0), 2)
#                 (X, Y), (MA, ma), angle = ellipseParam
#                 area_buffer.append(handRingArea)
#                 angle_buffer.append(angle)
#             subImg = cv2.resize(subImg, (0, 0), fx=3, fy=3)
#             cv2.imshow("ROI " + str(2), subImg)
#             #cv2.waitKey(1)
#             k = cv2.waitKey(1)  # k is the key pressed
#             if k == 27 or k == 113:  # 27, 113 are ascii for escape and q respectively
#                 # exit
#                 cv2.destroyAllWindows()
#                 cam.release()
#                 break
#         except:
#             print('no hand found')
#     number_pressed = False
#     spacePressed = False
#     if num_frames > 15:
#
#
#         XYbuffer.pop(0)
#         finger_buffer.pop(0)
#         angle_buffer.pop(0)
#         area_buffer.pop(0)
#
#
#     if num_frames % 60 == 0:
#
#     #part4.3 complex gestures
#         mean_Angle = np.mean(angle_buffer)
#         mean_handRingArea = np.mean(area_buffer)
#         print('prev_angle: ', prevAngle, ' cur_angle: ', mean_Angle)
#
#         print('prev_area: ', prevHandRingArea, ' cur_area: ', mean_handRingArea)
#
#         if prevHandRingArea is None:
#             prevHandRingArea = mean_handRingArea
#         else:
#             if (isIncreased(mean_handRingArea, prevHandRingArea, 2000)):
#                 print('I')
#                 ZoomIn()
#             elif (isDecreased(mean_handRingArea, prevHandRingArea, 2000)):
#                 print('O')
#                 ZoomOut()
#             prevHandRingArea = mean_handRingArea
#         if prevAngle is None:
#             prevAngle = mean_Angle
#         else:
#             if (isIncreased(mean_Angle, prevAngle, 50)):
#                 print('r')
#                 RotateRight()
#             elif (isDecreased(mean_Angle, prevAngle, 50)):
#                 print('l')
#                 RotateLeft()
#             prevAngle = mean_Angle
#     #part4.2: simple gestures
#         mean = np.mean(XYbuffer, axis=0)
#         meanX = mean[0]
#         meanY = mean[1]
#         move_mouse(meanX, meanY)
#         mean_finger_count = int(np.round(np.mean(finger_buffer), 0))
#         if mean_finger_count > 0 and not number_pressed:
#             pyautogui.press(str(mean_finger_count))
#             number_pressed = True
#             spacePressed = False
#         elif mean_finger_count == 0 and not spacePressed:
#             pyautogui.press('space')
#             spacePressed = True
#             number_pressed = False
#         cv2.imshow(window_name, thresholdedHandImage)
#
