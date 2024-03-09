from PIL import Image

def crop_image(input_image_path, start_x, start_y, box_width, box_height):
    # 打开输入图片
    image = Image.open(input_image_path)
    
    # 计算裁剪框的边界
    end_x = start_x + box_width
    end_y = start_y + box_height
    
    # 裁剪图片
    cropped_image = image.crop((start_x, start_y, end_x, end_y))
    
    return cropped_image




# 示例用法
input_image_path = "images/deskewed.jpg"  # 输入图片路径
start_x = 15  # 起始横坐标
start_y = 30  # 起始纵坐标
box_width = 140  # 截图窗口宽度
box_height = 20  # 截图窗口高度

cropped_image = crop_image(input_image_path, start_x, start_y, box_width, box_height)

# 保存裁剪后的图片
cropped_image.save("images/cropped_questions/cropped_image.jpg")
