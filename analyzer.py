from ultralytics import YOLO
import cv2 as cv
import math

model = YOLO("yolov8n.pt")

# COCO class names used to classify detections
PERSON_CLASS = "person"
BAG_CLASSES = {"backpack", "handbag", "suitcase"}

DISTANCE_THRESHOLD = 200   # pixels; bag counted as "safe" if within this of a person
FALL_ASPECT_RATIO = 1.4    # width/height above this = person likely fallen


def get_center(box):
    x1, y1, x2, y2 = box.xyxy[0]
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return center_x, center_y


def classify_boxes(boxes, names):
    """Split detected boxes into person and bag lists based on class name."""
    person = []
    bags = []
    for box in boxes:
        cls_id = int(box.cls[0])
        label = names[cls_id]
        if label == PERSON_CLASS:
            person.append(box)
        elif label in BAG_CLASSES:
            bags.append(box)
    return person, bags


def is_bag_near_person(bag, person):
    bag_x, bag_y = get_center(bag)
    for p in person:
        person_x, person_y = get_center(p)
        distance = math.sqrt((bag_x - person_x) ** 2 + (bag_y - person_y) ** 2)
        if distance <= DISTANCE_THRESHOLD:
            return True
    return False


def person_aspect_ratio(p):
    x1, y1, x2, y2 = map(int, p.xyxy[0])
    width = x2 - x1
    height = y2 - y1
    return (width / height) if height > 0 else 0


def build_findings(person, bags):
    """Compute safe/suspicious bags and standing/fall persons."""
    findings = []

    for bag in bags:
        near_person = is_bag_near_person(bag, person)
        findings.append({
            "type": "bag",
            "status": "safe" if near_person else "suspicious"
        })

    for p in person:
        ratio = person_aspect_ratio(p)
        findings.append({
            "type": "person",
            "status": "possible_fall" if ratio > FALL_ASPECT_RATIO else "standing"
        })

    return findings


def analyze_image(image_path):
    """Run detection and return findings only (no image written to disk)."""
    results = model(image_path)
    boxes = results[0].boxes
    names = model.names

    person, bags = classify_boxes(boxes, names)
    findings = build_findings(person, bags)

    return {
        "people_count": len(person),
        "bags_count": len(bags),
        "findings": findings,
    }


def analyze_and_draw(image_path, output_path="output.jpg"):
    """Run detection, draw annotated boxes, save the image, and return findings."""
    results = model(image_path)
    boxes = results[0].boxes
    names = model.names

    person, bags = classify_boxes(boxes, names)
    findings = build_findings(person, bags)

    image = cv.imread(image_path)

    for bag in bags:
        near_person = is_bag_near_person(bag, person)
        x1, y1, x2, y2 = map(int, bag.xyxy[0])
        color = (0, 255, 0) if near_person else (0, 0, 255)
        label_text = "Safe bag" if near_person else "SUSPICIOUS"
        cv.rectangle(image, (x1, y1), (x2, y2), color, 3)
        cv.putText(image, label_text, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    for p in person:
        ratio = person_aspect_ratio(p)
        x1, y1, x2, y2 = map(int, p.xyxy[0])
        is_fall = ratio > FALL_ASPECT_RATIO
        fall_label = "POSSIBLE FALL" if is_fall else "Standing"
        fall_color = (0, 0, 255) if is_fall else (0, 255, 0)
        cv.rectangle(image, (x1, y1), (x2, y2), fall_color, 2)
        cv.putText(image, fall_label, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.6, fall_color, 2)

    cv.imwrite(output_path, image)

    return {
        "output_path": output_path,
        "people_count": len(person),
        "bags_count": len(bags),
        "findings": findings,
    }


if __name__ == "__main__":
    # Example usage
    result = analyze_and_draw("input.jpg", "output.jpg")
    print(result)