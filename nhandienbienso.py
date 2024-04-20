
import cv2
import imutils
import pytesseract
import tkinter as tk
from tkinter import filedialog


def open_file():
    global last_frame
    file_path = filedialog.askopenfilename()
    cap = cv2.VideoCapture(file_path)
    while True:
        _, frame = cap.read()
        if frame is None:
                break
        #Xu ly Frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if last_frame is None:
            last_frame = gray.copy()
        abs_img = cv2.absdiff(last_frame, gray)
        # 0 - 1 = tran so ///abs(0-1) = 1last_frame = gray
        last_frame = gray.copy()
        _, img_mask = cv2.threshold(abs_img, 30, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) < 900:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)

        cv2.imshow("Window", frame)


        key = cv2.waitKey(15)
        if key & 0xFF == ord('q'):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            break
    cap.release()
    cv2.destroyAllWindows()



def open_camera():
    global last_frame
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)


# Đọc ảnh
image = cv2.imread("car_plate.jpg")

# Chuyển ảnh sang ảnh xám
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Làm mờ ảnh để loại bỏ nhiễu
blurred = cv2.GaussianBlur(gray, (7, 7), 0)

# Phát hiện cạnh trên ảnh đã làm mờ
edged = cv2.Canny(blurred, 50, 150)

# Tìm các đường viền trong ảnh
contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)

# Sắp xếp các đường viền theo diện tích giảm dần
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

# Xác định biển số xe
plate = None

for c in contours:
    # Xấp xỉ đường viền
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * peri, True)

    # Nếu đa giác có 4 đỉnh, giả sử đó là biển số xe
    if len(approx) == 4:
        plate = approx
        break

# Vẽ biển số xe lên ảnh gốc
cv2.drawContours(image, [plate], -1, (0, 255, 0), 2)

# Hiển thị ảnh gốc và biển số xe
cv2.imshow("Original Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Sử dụng pytesseract để nhận dạng văn bản trên biển số xe
if plate is not None:
    # Cắt ảnh chỉ chứa biển số xe
    (x, y, w, h) = cv2.boundingRect(plate)
    roi = gray[y:y + h, x:x + w]

    # Sử dụng pytesseract để nhận dạng văn bản
    text = pytesseract.image_to_string(roi, lang='eng')
    print("License Plate Number:", text)
else:
    print("License plate not found")
