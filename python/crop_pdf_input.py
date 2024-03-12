import cv2
import numpy as np
from PIL import Image
import os
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

    rotated_ans = rotated[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)]
    rotated_id = rotated[int(0.47*min(y1, y2)): int(0.93*min(y1, y2)),int(0.76*max(x1, x2)):int(0.99*max(x1, x2))]
    return rotated_ans, rotated_id





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
    rotated_ans,rotated_id = crop(rotated, contours, h, w)

    return rotated_ans,rotated_id





def crop_box(image_pil, start_x, start_y, box_width, box_height):
    end_x = start_x + box_width
    end_y = start_y + box_height
    cropped_image = image_pil.crop((start_x, start_y, end_x, end_y))
    return cropped_image




def crop_id(image_id, output_folder):
    num_id = 9
    start_x,start_y = 0,0
    box_width,box_height = 24, 183
    os.makedirs(output_folder, exist_ok=True)
    for i in range(1, num_id + 1):
        cropped_id = crop_box(image_id, start_x, start_y, box_width, box_height)
        cropped_id.save(os.path.join(output_folder, f"{i}.jpg"))
        start_x += box_width





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
    



def convert_pdf_to_images(pdf_path, dpi=300):
    doc = fitz.open(pdf_path)  # Open the PDF file
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # Load the current page
        pix = page.get_pixmap(dpi=dpi)  # Render page to an image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images





def load_and_scale_images(images, scale_percent):
    scaled_images = []
    for image_pil in images:
        width, height = image_pil.size
        new_width = int(width * scale_percent / 100)
        new_height = int(height * scale_percent / 100)
        # 使用Image.Resampling.LANCZOS替代Image.ANTIALIAS
        image_pil = image_pil.resize((new_width, new_height), Image.Resampling.LANCZOS)
        image_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
        scaled_images.append(image_cv)
    return scaled_images




def main():
    pdf_path = 'pdf/test.pdf'  # PDF文件路径
    output_path = 'images/cropped_answers'  # 输出路径
    output_path_id = 'images/cropped_id'
    scale_percent = 40  # 缩放比例
    num_questions = 120  # 问题数量

    # 使用修改后的函数处理PDF并获取图像列表
    pil_images = convert_pdf_to_images(pdf_path)
    scaled_images_with_names = load_and_scale_images(pil_images, scale_percent)
    
    for i, image in enumerate(scaled_images_with_names):
        deskewed_ans,deskewed_id = deskew(image)
        deskewed_ans = Image.fromarray(cv2.cvtColor(deskewed_ans, cv2.COLOR_BGR2RGB))
        deskewed_id = Image.fromarray(cv2.cvtColor(deskewed_id, cv2.COLOR_BGR2RGB))

        
        # 使用文件名创建对应的子文件夹
        file_name = f"page_{i+1}"
        output_folder = os.path.join(output_path, f"{file_name}_cropped")
        output_folder_id = os.path.join(output_path_id, f"{file_name}_id")
        os.makedirs(output_folder, exist_ok=True)
        os.makedirs(output_folder_id, exist_ok=True)
        
        crop_loop(num_questions, deskewed_ans, output_folder)
        crop_id(deskewed_id, output_folder_id)
        # 如果需要保存deskewed_image，可以在这里进行保存
        # 例如: cv2.imwrite(os.path.join(output_folder, f'{file_name}_deskewed.jpg'), deskewed_image)

if __name__ == '__main__':
    main()

