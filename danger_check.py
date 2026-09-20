import math

from streamlit import image
from ultralytics import YOLO
import cv2 as cv

model = YOLO("yolov8n.pt")
results = model("baseball-team.jpg")
image = cv.imread("baseball-team.jpg")
print(image)
boxes = results[0].boxes
names = model.names
person =[]
bags =[]
for box in boxes:
    class_id = int(box.cls[0])
    label = names[class_id]
    if label == "person":
        person.append(box)
    elif label == "backpack" or label == "handbag":
        bags.append(box)

print(f"Found {len(person)} people and {len(bags)} bags.")

def get_center(box):
    x1,y1,x2,y2 = box.xyxy[0]
    center_x = (x1 + x2)/ 2
    center_y = (y1 + y2)/2 
    return center_x ,center_y

for bag in bags:
    bag_x,bag_y = get_center(bag)
    is_near_person = False 
    for p in person:
        person_x, person_y = get_center(p)
        distance = math.sqrt((bag_x - person_x)**2 + (bag_y - person_y)**2)
        if distance < 200:
            is_near_person = True 
    x1,y1,x2,y2 = map(int, bag.xyxy[0])
    if is_near_person:
        color = (0, 255,0)
        label_text ="Safe bag"
    else:
        color = (0,0,255)
        label_text = "SUSPICIOUS"

    cv.rectangle(image,(x1,y1),(x2,y2),color,3)
    cv.putText(image, label_text,(x1,y1-10),cv.FONT_HERSHEY_SIMPLEX,0.8,color,2)

for p in person:
    x1,y1,x2,y2 = map(int,p.xyxy[0])
    width=x2 -x1
    height = y2 -y1
    aspect_ratio = width/height

    if aspect_ratio > 1.4:
        fall_label = "POSSIBLE FALL"
        fall_color=(0,0,255)
    else:
        fall_label ="Standing"
        fall_color =(0,255,0)
    cv.rectangle(image,(x1,y1),(x2,y2),fall_color,2)
    cv.putText(image, fall_label,(x1,y1-10),cv.FONT_HERSHEY_SIMPLEX,0.6,fall_color,2)
cv.imwrite("result.jpg",image)
print("Saved result.jpg - open it to see the marked image!")