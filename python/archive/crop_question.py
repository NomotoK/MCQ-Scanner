from PIL import Image

def crop_box(input_image_path, start_x, start_y, box_width, box_height):
    # open input image
    image = Image.open(input_image_path)
    
    # calculate end coordinates
    end_x = start_x + box_width
    end_y = start_y + box_height
    
    # crop image
    cropped_image = image.crop((start_x, start_y, end_x, end_y))
    
    return cropped_image


def crop_loop(num_questions, start_x, start_y, box_width, box_height):
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
    


if __name__ == '__main__':

    input_image_path = "images/cropped_images/buffer.jpg"  # input image path
    start_x = 40  # start x coordinate
    start_y = 40  # start y coordinate
    box_width = 130  # cropped image width
    box_height = 24  # cropped image height
    num_questions = 120  # number of questions
    crop_loop(num_questions, start_x, start_y, box_width, box_height)



