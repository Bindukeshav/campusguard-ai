from ultralytics import YOLO
import cv2 as cv
import math

model = YOLO("yolov8n.pt")


def get_center(box):
    x1, y1, x2, y2 = box.xyxy[0]
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return center_x, center_y


def analyze_image(image_path):
    results = model(image_path)
    boxes = results[0].boxes
    names = model.names
    person = []
    bags = []

    for box in boxes:
        class_id = int(box.cls[0])
        label = names[class_id]
        if label == "person":
            person.append(box)
        elif label in ("backpack", "handbag"):
            bags.append(box)

    findings = []

    for bag in bags:
        bag_x, bag_y = get_center(bag)
        is_near_person = False
        for p in person:
            person_x, person_y = get_center(p)
            distance = math.sqrt((bag_x - person_x) ** 2 + (bag_y - person_y) ** 2)
            if distance <= 200:
                is_near_person = True
                break
        findings.append({
            "type": "bag",
            "status": "safe" if is_near_person else "suspicious"
        })

    for p in person:
        x1, y1, x2, y2 = map(int, p.xyxy[0])
        width = x2 - x1
        height = y2 - y1
        aspect_ratio = width / height if height > 0 else 0
        findings.append({
            "type": "person",
            "status": "possible_fall" if aspect_ratio > 1.4 else "standing"
        })

    return {
        "people_count": len(person),
        "bags_count": len(bags),
        "findings": findings
    } 
    