
# chdir C:\Users\user\PycharmProjects\pet_projects\Lib
# python real_time_detect.py -p="C:\Users\user\Desktop\learn models\real_time_detecting\MobileNetSSD_deploy.prototxt.txt" -m="C:\Users\user\Desktop\learn models\real_time_detecting\MobileNetSSD_deploy.caffemodel"

from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2


ap = argparse.ArgumentParser()
ap.add_argument('-p', '--prototxt', required=True, help='path to Caffe "deploy" prototxt file')
ap.add_argument('-m', '--model', required=True, help='path to Caffe pre-trained model')
ap.add_argument('-c', '--confidence', type=float, default=0.2, help='minimum probability to filter weak detections')
args = vars(ap.parse_args())

CLASSES = ['background', 'aeroplane', 'bicycle', 'bird',
           'boat', 'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse', 'motorbike',
           'person', 'pottedplant', 'sheep', 'sofa', 'train',
           'tvmonitor']
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3)) #цвета для классов

print('[INFO] loading model...')
net = cv2.dnn.readNetFromCaffe(args['prototxt'], args['model'])

print('[INFO] starting video stream')
vs = VideoStream(scr=0).start()
time.sleep(2.0)
fps = FPS().start()

while True:
    frame = vs.read()  # берем изображение из потока
    frame = imutils.resize(frame, width=800)  # изменяем ширину кадра

    h, w = frame.shape[:2]  # забираем высоту и ширину кадра
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (224, 224)), 0.007843, (224, 224), 127.5)
    # получили блоб, что делают цифири - хз

    net.setInput(blob)
    detections = net.forward()

    # Фильтрация объектов

    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]  # достали вероятность итого объекта
        if confidence > args['confidence']:
            idx = int(detections[0, 0, i, 1])  # индекс класса
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])  # вершины прямоугольника
            x_s, y_s, x_e, y_e = box.astype('int')
            label = '{}: {:.2f}%'.format(CLASSES[idx], confidence * 100)

            # отрисовка прямоугольника
            cv2.rectangle(frame, (x_s, y_s), (x_e, y_e), COLORS[idx], 2)  # 2- толщина
            y = y_s - 15 if y_s - 15 > 15 else y_s + 15
            cv2.putText(frame, label, (x_s, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    cv2.imshow('Frame', frame)  # имя Frame, frame - изображение
    key = cv2.waitKey(1) & 0xFF  # 1 если нажата клавиша q - 0xFF её номер в  ASCII
    if key == ord('q'): break

    fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
cv2.destroyAllWindows()
vs.stop()