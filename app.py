from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory
import os
import subprocess

app = Flask(__name__)

# 设定文件上传的目标文件夹
UPLOAD_FOLDER = 'pdf'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and file.filename.endswith('.csv'):
        base_path = os.path.join('csv', 'master_answers')
        os.makedirs(base_path, exist_ok=True)
        file.save(os.path.join(base_path, file.filename))
        return 'File uploaded successfully', 200
    else:
        return 'Invalid file type', 400
    
    

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f'File {filename} uploaded successfully'
    return 'File type not allowed'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'




def check_files_exist():
    pdf_path = os.path.join(os.path.dirname(__file__), 'pdf')
    csv_path = os.path.join(os.path.dirname(__file__), 'csv', 'master_answers')

    # 检查文件夹中是否有文件
    if not os.listdir(pdf_path):
        return False, 'Please upload pdf'
    if not os.listdir(csv_path):
        return False, 'Please upload master answer'

    return True, ''

@app.route('/analyse_mcq', methods=['POST'])
def analyse_mcq():
    files_exist, message = check_files_exist()
    if not files_exist:
        return jsonify({'message': message}), 400
    
    try:
        main_py_path = os.path.join(os.path.dirname(__file__), 'python', 'main.py')
        result = subprocess.run(['python', main_py_path], capture_output=True, text=True, check=True)
        return jsonify({'message': 'Analysis completed successfully', 'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'message': 'Error during analysis', 'error': str(e)}), 500
    

@app.route('/download_scores', methods=['GET'])
def download_scores():
    directory = os.path.join(os.path.dirname(__file__), 'csv', 'output')
    return send_from_directory(directory=directory, path='student_scores.csv', as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
