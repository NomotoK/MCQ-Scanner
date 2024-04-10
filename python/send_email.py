import pandas as pd
import smtplib
import glob
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def load_data():
    # 加载所有学生信息的csv文件
    students_files = glob.glob('csv/student_info/*.csv')
    students_df_list = [pd.read_csv(f) for f in students_files]
    students_df = pd.concat(students_df_list, ignore_index=True)

    # 加载所有成绩信息的csv文件
    grades_files = glob.glob('csv/output/*.csv')
    grades_df_list = [pd.read_csv(f) for f in grades_files]
    grades_df = pd.concat(grades_df_list, ignore_index=True)

    # 假设每个学生在每个数据集中都是唯一的，并使用适当的键进行合并
    # 这里使用的是'Student ID'和'ID'，但你可能需要根据实际情况调整这些键
    merged_df = pd.merge(students_df, grades_df, left_on='ID', right_on='ID')

    return merged_df


def send_email():

    merged_df = load_data()
    # SMTP服务器设置
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # 对于TLS
    smtp_user = "sghxie4@gmail.com"
    smtp_password = "uvsf ydyb qicc dkoc"

    # 创建SMTP服务器连接
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)


    for index, row in merged_df.iterrows():
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = row['Email_Address']
        msg['Subject'] = 'Your Exam Feedback'

        # 构建邮件内容
        body = f"""
        Dear {row['Full_Name']},

        Here are your exam results:

        Grade: {row['Grade']}
        Incorrect Answers: {row['Incorrect_Answers']}
        Part 1: {row['Part_1']}
        Part 2: {row['Part_2']}
        Part 3: {row['Part_3']}
        Part 4: {row['Part_4']}
        Part 5: {row['Part_5']}

        Best,
        Your Teacher
        """
        msg.attach(MIMEText(body, 'plain'))
        # 发送邮件
        server.sendmail(smtp_user, row['Email_Address'], msg.as_string())

def main():
    send_email()

if __name__ == '__main__':
    main()