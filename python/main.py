import crop_pdf_input
import ans_eval
import time

def main():
    start_time = time.time()

    folder_path = 'pdf'
    crop_pdf_input.main(folder_path)
    ans_eval.main()

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")


if __name__ == '__main__':
    main()

