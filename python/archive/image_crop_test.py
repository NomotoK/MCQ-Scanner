import cv2
import numpy as np
import os



def edge_detect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    return edged



def find_contours(image):
    edged = edge_detect(image)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours




def crop_answer_area(rotated, contours, h, w):
    contours = find_contours(rotated)
    c = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.intp(box)
    x1, y1 = box[0]
    x2, y2 = box[2]

    if y1 < h - y2:
        rotated = cv2.rotate(rotated, cv2.ROTATE_180)
        x1, y1 = w - x1, h - y1
        x2, y2 = w - x2, h - y2

    rotated = rotated[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)]
    return rotated




def deskew(image):
    (h, w) = image.shape[:2]
    contours = find_contours(image)
    c = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.intp(box)
    angle = rect[2]
    if rect[1][0] > rect[1][1]:
        angle = 90 + angle

    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    rotated = crop_answer_area(rotated, contours, h, w)
    return rotated




def process_images_in_folder(folder_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)

            scale_percent = 40  # percent of original size
            width = int(image.shape[1] * scale_percent / 100)
            height = int(image.shape[0] * scale_percent / 100)
            dim = (width, height)

            image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            deskewed = deskew(image)

            output_path = os.path.join(output_folder, f"deskewed_{filename}")
            cv2.imwrite(output_path, deskewed)
            print(f"Processed and saved: {output_path}")





if __name__ == '__main__':
    input_folder = 'images/pdf_converted'  # Specify the input folder path here
    output_folder = 'cropped_images'  # Specify the output folder path here
    process_images_in_folder(input_folder, output_folder)
