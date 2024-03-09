from PIL import Image

def crop_box(input_image_path, start_x, start_y, box_width, box_height):
    # 打开输入图片
    image = Image.open(input_image_path)
    
    # 计算裁剪框的边界
    end_x = start_x + box_width
    end_y = start_y + box_height
    
    # 裁剪图片
    cropped_image = image.crop((start_x, start_y, end_x, end_y))
    
    return cropped_image





if __name__ == '__main__':
    # 示例用法
    input_image_path = "pdf/deskewed.jpg"  # 输入图片路径
    start_x = 15  # 起始横坐标
    start_y = 30  # 起始纵坐标
    box_width = 150  # 截图窗口宽度
    box_height = 24  # 截图窗口高度

    for i in range(1, 121):

        if i % 5 == 0: 
            if i % 30 == 0:
                cropped_image = crop_box(input_image_path, start_x, start_y, box_width, box_height)
                cropped_image.save(f"images/cropped_questions/cropped_image_{i}.jpg")
                start_y = 30
                start_x += box_width + 87
            else:
                cropped_image = crop_box(input_image_path, start_x, start_y, box_width, box_height)
                cropped_image.save(f"images/cropped_questions/cropped_image_{i}.jpg")
                start_y += box_height + 35
        else:
            cropped_image = crop_box(input_image_path, start_x, start_y, box_width, box_height)
            cropped_image.save(f"images/cropped_questions/cropped_image_{i}.jpg")
            start_y += box_height


