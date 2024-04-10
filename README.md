# MCQ-Scnner
[**🇨🇳Chinese**](./README_CN.md) | [**🌐English**](./README.md)

<p align="center">
<img alt="Static Badge" src="https://img.shields.io/badge/Version-1.3-blue">
<img alt="Static Badge" src="https://img.shields.io/badge/Licence-MIT-yellow">
</p>

## Introduction
MCQ-Scanner is a web app that allows you to upload answer sheets and sample answers to your test papers for automatic scoring. The results will be downloaded as a csv file.You can also preview the results of the analysis, including the average score, the highest and lowest scores, and the questions with the highest error rate, etc.

### The currently implemented functions are as follows:

- Upload files: Users can upload files in pdf format for analysis
- Upload standard answers: standard answers for scoring, currently only supports csv format.
- One-click analysis: Click "Analyze" to get the scores of each test paper in the PDF file, as well as data such as wrong questions and accuracy. The results will be stored in a csv file.
- Preview results: On the results analysis page, you can view the average score, highest and lowest scores, accuracy rate, and questions with the highest error rate.The complete analysis results will be displayed on the right side of the screen.

### Homepage
<img width="1470" alt="hompage" src="https://github.com/NomotoK/MCQ-Scanner/assets/99944622/b51a21a9-06a4-45ce-bf2d-d66dc1b8d725">

### Results Preview Page
<img width="1470" alt="results" src="https://github.com/NomotoK/MCQ-Scanner/assets/99944622/d9113cfe-8b80-4381-acd8-e3e73c387eeb">


## How To Use

### Install dependencies

```shell
conda activate MCQ-Scanner
conda install flask
conda install torch,cv2,matplotlib,seaborn,pandas,fitz,numpy,scikit-learn
```

### Run app
```shell
flask run
```

### File Tree

```shell

MCQ-Scanner
├─ python
│  ├─ misc
│  │  ├─ create_csv.py
│  │  ├─ model_eval.py
│  │  ├─ crop_id.py
│  │  ├─ move_files.py
│  │  └─ file_rename.py
│  ├─ models.py
│  ├─ archive
│  │  ├─ crop_question.py
│  │  ├─ chenwei.py
│  │  ├─ img_pixel_count.py
│  │  ├─ bin.py
│  │  ├─ image_crop_test.py
│  │  ├─ chenwei_main.py
│  │  ├─ crop_arcive.py
│  │  └─ pdf_conversion.py
│  ├─ crop_pdf_input.py
│  ├─ crop_image_input.py
│  ├─ score_visualization.py
│  ├─ models
│  │  ├─ cnn_id.pt
│  │  ├─ cnn_enhanced.pt
│  │  ├─ cnn1.pt
│  │  └─ cnn.pt
│  ├─ __pycache__
│  │  ├─ train.cpython-311.pyc
│  │  ├─ crop_pdf_input.cpython-311.pyc
│  │  ├─ models.cpython-311.pyc
│  │  ├─ ans_eval.cpython-311.pyc
│  │  └─ validation.cpython-311.pyc
│  ├─ train.py
│  ├─ main.py
│  ├─ ans_eval.py
│  └─ validation.py
├─ images
│  ├─ Figure_2.png
│  ├─ pdf_converted
│  │  ├─ page_2.jpg
│  │  ├─ page_3.jpg
│  │  ├─ page_1.jpg
│  │  ├─ page_4.jpg
│  │  ├─ page_5.jpg
│  │  ├─ page_7.jpg
│  │  ├─ page_6.jpg
│  │  ├─ page_18.jpg
│  │  ├─ page_10.jpg
│  │  ├─ page_11.jpg
│  │  ├─ page_13.jpg
│  │  ├─ page_12.jpg
│  │  ├─ page_16.jpg
│  │  ├─ page_17.jpg
│  │  ├─ page_15.jpg
│  │  ├─ page_14.jpg
│  │  ├─ page_8.jpg
│  │  └─ page_9.jpg
│  ├─ Figure_1.png
│  └─ Figure_enhanced.png
├─ __pycache__
│  ├─ flask.cpython-39.pyc
│  ├─ flasktest.cpython-311.pyc
│  └─ app.cpython-311.pyc
├─ README.md
├─ static
│  ├─ css
│  │  ├─ results_style.css
│  │  └─ style.css
│  ├─ images
│  │  ├─ clipboard.png
│  │  └─ output
│  │     ├─ bar_chart.png
│  │     └─ pie_chart.png
│  └─ js
│     └─ script.js
├─ csv
│  └─ output
│     └─ student_scores.csv
├─ app.py
├─ templates
│  ├─ index.html
│  └─ results.html
├─ test_run
│  ├─ sample_answer.pdf
│  ├─ testpdf
│  │  ├─ ans_train_E.pdf
│  │  ├─ ans_train_D.pdf
│  │  ├─ id_train_9.pdf
│  │  ├─ id_train_8.pdf
│  │  ├─ ans_train_C.pdf
│  │  ├─ ans_train_null.pdf
│  │  ├─ ans_train_B.pdf
│  │  ├─ ans_test.pdf
│  │  ├─ ans_train_A.pdf
│  │  ├─ sample_answer.pdf
│  │  ├─ test2.pdf
│  │  ├─ test1.pdf
│  │  ├─ id_test.pdf
│  │  ├─ id_train_3.pdf
│  │  ├─ id_train_2.pdf
│  │  ├─ id_train_0.pdf
│  │  ├─ id_train_1.pdf
│  │  ├─ id_train_5.pdf
│  │  ├─ id_train_4.pdf
│  │  ├─ id_train_6.pdf
│  │  └─ id_train_7.pdf
│  └─ master_answer.csv
└─ data
   ├─ description.json
   ├─ answer_data
   │  ├─ test...
   │  ├─ train...
   ├─ id_data
   │  ├─ test...
   │  ├─ train...

```

# v1.3 Beta

## What's New:
- New results preview page: You can now click the "view results" button after generating the results to preview the results of each analysis, including statistical charts of students' highest scores, lowest scores, average scores and accuracy rates, as well as the five questions with the highest error rates pie chart, and a preview window of the final result csv file.
- The neural network model used for answer recognition has been replaced with a more complex model for recognition, and the accuracy has been greatly improved.
- Added confusion matrix printing function.

## Improvements

- File upload now supports multiple pdf files.

## Bug Fixes:
- Fixed some display issues



