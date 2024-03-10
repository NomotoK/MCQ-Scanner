import cv2
import numpy as np
from PIL import Image
import os
import glob
import fitz


def edge_detect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    return edged





def find_contours(image):
    edged = edge_detect(image)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours





def crop(rotated, contours, h, w):
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
    rotated = crop(rotated, contours, h, w)

    return rotated





def crop_box(image_pil, start_x, start_y, box_width, box_height):
    end_x = start_x + box_width
    end_y = start_y + box_height
    cropped_image = image_pil.crop((start_x, start_y, end_x, end_y))
    return cropped_image





def crop_loop(num_questions, image_pil, output_folder):
    start_x, start_y = 40, 40
    box_width, box_height = 130, 24
    gap_x, gap_y = 110, 35  # Additional gaps for specific conditions
    os.makedirs(output_folder, exist_ok=True)
    for i in range(1, num_questions + 1):
        cropped_image = crop_box(image_pil, start_x, start_y, box_width, box_height)
        cropped_image.save(os.path.join(output_folder, f"{i}.jpg"))
        
        # Update coordinates for the next question's position
        if i % 30 == 0:
            start_x += box_width + gap_x
            start_y = 40  # Reset to the first row
        elif i % 5 == 0:
            start_y += box_height + gap_y  # Move down with an extra gap every 5th question
        else:
            start_y += box_height  # Move down to the next position
    




def load_and_scale_images(input_path, scale_percent):
    scaled_images = []
    image_paths = glob.glob(os.path.join(input_path, '*.jpg')) + glob.glob(os.path.join(input_path, '*.png'))
    for file_path in image_paths:
        image = cv2.imread(file_path)
        if image is None:
            continue
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        scaled_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        # 获取不包含路径和扩展名的文件名
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        scaled_images.append((scaled_image, file_name))
    return scaled_images




def main():
    input_path = 'images/pdf_converted'
    output_path = 'images/cropped_answers'
    scale_percent = 40
    num_questions = 120

    scaled_images_with_names = load_and_scale_images(input_path, scale_percent)
    for image, file_name in scaled_images_with_names:
        deskewed_image = deskew(image)
        deskewed_image_pil = Image.fromarray(cv2.cvtColor(deskewed_image, cv2.COLOR_BGR2RGB))
        
        # 使用文件名创建对应的子文件夹
        output_folder = os.path.join(output_path, f"{file_name}_cropped")
        os.makedirs(output_folder, exist_ok=True)
        
        crop_loop(num_questions, deskewed_image_pil, output_folder)
        # 如果需要保存deskewed_image，可以在这里进行保存
        # 例如: cv2.imwrite(os.path.join(output_folder, f'{file_name}_deskewed.jpg'), cv2.cvtColor(deskewed_image_pil, cv2.COLOR_RGB2BGR))

if __name__ == '__main__':
    main()

