import cv2
import numpy as np
import os
from PIL import Image


def edge_detect(image):
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 高斯滤波
    blurred = cv2.GaussianBlur(gray, (5, 5), 0) # 灰度图像, 高斯核大小, 标准差
    # 边缘检测
    edged = cv2.Canny(blurred, 50, 150)
    return edged




def find_contours(image):# 轮廓检测
    # 边缘检测
    edged = edge_detect(image)
    # 轮廓检测
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


# 裁剪图像
def crop(rotated, contours, h, w):
        # 矩形四角坐标
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

    # 裁剪出矩形答题区域
    rotated = rotated[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)]
    return rotated



# 旋转图像
def deskew(image):
    # 获取图像大小
    (h, w) = image.shape[:2]
    # 轮廓检测
    contours = find_contours(image)
    # 找到最大的轮廓
    c = max(contours, key=cv2.contourArea)
    # 矩形拟合
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.intp(box)
    # 旋转矩形, 窄边为水平
    angle = rect[2] # 获取旋转角度
    if rect[1][0] > rect[1][1]:
        angle = 90 + angle
    # 旋转图像
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0) # 获取旋转矩阵
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE) # 旋转图像
    # 裁剪图像
    rotated = crop(rotated, contours, h, w)
        # 将学号区域转换为灰度图像，并应用二值化
    gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # 轮廓检测
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 最小轮廓面积
    min_area = 20
    contours = [c for c in contours if cv2.contourArea(c) > min_area]


    return rotated



def crop_box(buffer_path, start_x, start_y, box_width, box_height):
    
    image = Image.open(buffer_path)
    # 计算裁剪框的边界
    end_x = start_x + box_width
    end_y = start_y + box_height
    # 裁剪图片
    cropped_image = image.crop((start_x, start_y, end_x, end_y))
    return cropped_image



def crop_loop(num_questions, input_image_path):
    start_x = 40  # 起始横坐标
    start_y = 40  # 起始纵坐标
    box_width = 130  # 截图窗口宽度
    box_height = 24  # 截图窗口高度
    for i in range(1, num_questions + 1):
        if i % 5 == 0: 
            if i % 30 == 0:
                cropped_image = crop_box(input_image_path, start_x, start_y, box_width, box_height)
                cropped_image.save(f"images/cropped_questions/{i}.jpg")
                start_y = 40
                start_x += box_width + 110
            else:
                cropped_image = crop_box(input_image_path, start_x, start_y, box_width, box_height)
                cropped_image.save(f"images/cropped_questions/{i}.jpg")
                start_y += box_height + 35
        else:
            cropped_image = crop_box(input_image_path, start_x, start_y, box_width, box_height)
            cropped_image.save(f"images/cropped_questions/{i}.jpg")
            start_y += box_height




def load_and_scale_image(file_path, scale_percent):
    # Load the image
    image = cv2.imread(file_path)
    # Check if the image was successfully loaded
    if image is None:
        raise FileNotFoundError(f"No image found at the specified path: {file_path}")
    # Calculate the new dimensions
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    # Scale the image
    scaled_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return scaled_image





# Use the function in your main code
if __name__ == '__main__':
    input_path = 'images/pdf_converted/0001.jpg'
    buffer_path = 'images/cropped_images/buffer.jpg'
    scale_percent = 40
    num_questions = 120
    image = load_and_scale_image(input_path, scale_percent)

    cv2.imwrite(buffer_path, deskew(image))
    # Load and scale the image
    crop_loop(num_questions, buffer_path)

 

