import cv2
import numpy as np

class Car:
    def __init__(self, car_id, x, y, max_age=5):
        self.id = car_id
        self.x, self.y = x, y
        self.tracks = [[x, y]]
        self.done = False
        self.state = '0'  
        self.age = 0
        self.max_age = max_age
        self.dir = None

    def update_coords(self, x, y):
        self.age = 0
        self.tracks.append([x, y])
        self.x, self.y = x, y

    def is_timed_out(self):
        return self.age > self.max_age

    def check_direction(self, line_down, line_up):
        if len(self.tracks) >= 2:
            if self.state == '0':
                if self.tracks[-1][1] < line_up and self.tracks[-2][1] >= line_up:
                    self.dir = 'up'
                    self.state = '1'
                    return 'up'
                elif self.tracks[-1][1] > line_down and self.tracks[-2][1] <= line_down:
                    self.dir = 'down'
                    self.state = '1'
                    return 'down'
        return None
    
cap = cv2.VideoCapture("./test/test_1.mp4")
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False, history=200, varThreshold=90)
kernalOp = np.ones((3, 3), np.uint8)
kernalCl = np.ones((11, 11), np.uint8)

cars = []
cnt_up, cnt_down = 0, 0
line_up, line_down = 400, 250
up_limit, down_limit = 230, int(4.5 * (500 / 5))
car_id = 1

if not cap.isOpened():
    print("Error opening video stream")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (900, 500))
    fgmask = fgbg.apply(frame)
    ret, mask = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernalOp)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernalCl)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for car in cars:
        car.age += 1

    for cnt in contours:
        if cv2.contourArea(cnt) > 300:
            x, y, w, h = cv2.boundingRect(cnt)
            cx, cy = int(x + w / 2), int(y + h / 2)

            matched_car = None
            for car in cars:
                if abs(cx - car.x) <= w and abs(cy - car.y) <= h:
                    matched_car = car
                    car.update_coords(cx, cy)
                    direction = car.check_direction(line_down, line_up)
                    if direction == 'up':
                        cnt_up += 1
                        cv2.imwrite(f"./detected_vehicles/vehicleUP{cnt_up}.png", frame[y:y + h, x:x + w])
                    elif direction == 'down':
                        cnt_down += 1
                        cv2.imwrite(f"./detected_vehicles/vehicleDOWN{cnt_down}.png", frame[y:y + h, x:x + w])
                    break

            if matched_car is None and up_limit < cy < down_limit:
                cars.append(Car(car_id, cx, cy))
                car_id += 1

    cars = [car for car in cars if not car.is_timed_out()]
    cv2.line(frame, (0, line_up), (frame.shape[1], line_up), (255, 0, 0), 2)  
    cv2.line(frame, (0, line_down), (frame.shape[1], line_down), (0, 0, 255), 2)  
    
    cv2.putText(frame, f'DOWN: {cnt_down}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, f'UP: {cnt_up}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
    
    cv2.imshow('Frame', frame)
    if cv2.waitKey(10) & 0xFF == 27:  
        break

cap.release()
cv2.destroyAllWindows()
