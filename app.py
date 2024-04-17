from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory
import os
import subprocess
import csv

app = Flask(__name__)

# 设定文件上传的目标文件夹
UPLOAD_FOLDER = 'pdf'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/results')
def results():
    try:
        # 定位 score_visualization.py 脚本的路径
        visualization_script_path = os.path.join(os.path.dirname(__file__), 'python', 'score_visualization.py')
        # 使用 subprocess 执行脚本
        subprocess.run(['python', visualization_script_path], check=True)
        # 渲染结果页面（假设脚本执行成功后有相关结果可以在页面上显示）
        csv_file_path = os.path.join(os.path.dirname(__file__), 'csv', 'output', 'student_scores.csv')
        # 读取CSV文件内容
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            csv_data = list(reader)  # 将CSV文件内容转换为列表

        return render_template('results.html',csv_data=csv_data)
    except subprocess.CalledProcessError as e:
        # 如果脚本执行失败，返回错误信息（或者可以选择渲染一个包含错误信息的页面）
        return jsonify({'message': 'Error executing visualization script', 'error': str(e)}), 500





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
    
    



@app.route('/upload_pdf', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return redirect(request.url)
    
    files = request.files.getlist('files[]')
    
    if not files or files[0].filename == '':
        return 'No selected file'
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return 'Files uploaded successfully'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'






@app.route('/upload_master_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        base_path = os.path.join('pdf_master')
        os.makedirs(base_path, exist_ok=True)
        filepath = os.path.join(base_path, file.filename)
        file.save(filepath)

        # 执行 get_master_answer.py 脚本
        try:
            script_path = os.path.join(os.path.dirname(__file__), 'python', 'get_master_answer.py')
            subprocess.run(['python', script_path, filepath], check=True)
            
            # 提供下载链接
            return jsonify({'message': 'File uploaded and script executed successfully', 'download_url': '/download_master_answer'})
        except subprocess.CalledProcessError:
            return jsonify({'message': 'Script execution failed'}), 500
    else:
        return jsonify({'message': 'Invalid file type'}), 400







@app.route('/download_master_answer', methods=['GET'])
def download_master_answer():
    directory = os.path.join(os.path.dirname(__file__), 'csv', 'master_answers')
    return send_from_directory(directory, 'master_answer.csv', as_attachment=True)






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






@app.route('/upload_student_info', methods=['POST'])
def upload_student_info():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and file.filename.endswith('.csv'):
        base_path = os.path.join('csv', 'student_info')
        os.makedirs(base_path, exist_ok=True)
        file.save(os.path.join(base_path, file.filename))
        return 'File uploaded successfully', 200
    else:
        return 'Invalid file type', 400





@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        # 确定 send_email.py 的路径
        send_email_path = os.path.join(os.path.dirname(__file__), 'python', 'send_email.py')
        # 使用 subprocess 运行 send_email.py
        subprocess.run(['python', send_email_path], check=True)
        return jsonify({'message': 'Email sent successfully'})
    except subprocess.CalledProcessError:
        return jsonify({'message': 'Failed to send email'}), 500

if __name__ == '__main__':
    app.run(debug=True)
