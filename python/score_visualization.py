import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter


def load_student_scores(student_scores_path):
    df = pd.read_csv(student_scores_path)
    return df

def bar_chart(df):


    df['Accuracy'] = df['Accuracy'].str.rstrip('%').astype('float') / 100
    df['Grade'] = df['Grade'].str.rstrip('%').astype('float')


    # 计算最高分、最低分、平均分和平均准确率
    max_grade = df['Grade'].max()
    min_grade = df['Grade'].min()
    average_grade = df['Grade'].mean()
    average_accuracy = df['Accuracy'].mean()

    # 使用matplotlib绘制统计数据的图表
    fig, ax = plt.subplots(figsize=(8, 6))

    # 绘制条形图
    categories = ['Max Grade', 'Min Grade', 'Average Grade', 'Average Accuracy']
    values = [max_grade, min_grade, average_grade, average_accuracy * 100]  # 将平均准确率转换为百分比

    bars = ax.bar(categories, values, color=['lightblue', 'salmon', 'lavender', 'gold'])

    # 添加标题和标签
    ax.set_title('Student Grade Statistics')
    ax.set_ylabel('Value')
    ax.set_ylim(0, 110)  # 确保y轴范围能够展示百分比

        # 在每个条形图顶部显示数值
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., 1.002*height,
                '%.2f' % height,
                ha='center', va='bottom')

    image_path = 'static/images/output/bar_chart.png'
    plt.savefig(image_path)  # 保存图表为文件
    return image_path  # 返回图像文件的路径



def pie_chart(df):
    
    # 确保所有Incorrect_Answers都是字符串类型，忽略NaN值
    all_incorrect_answers_str = ';'.join(df['Incorrect_Answers'].dropna().astype(str)).split(';')

    # 重新计算每道题被答错的次数
    answer_counts_fixed = Counter(all_incorrect_answers_str)

    # 选择错误次数最多的5道题，重新计算
    most_common_answers_fixed = answer_counts_fixed.most_common(5)
    labels_fixed = [item[0] for item in most_common_answers_fixed]  # 题号
    sizes_fixed = [item[1] for item in most_common_answers_fixed]  # 答错次数
    total_incorrect_fixed = sum(answer_counts_fixed.values())
    sizes_percentage_fixed = [size / total_incorrect_fixed * 100 for size in sizes_fixed]  # 转换为百分比

    # 绘制修正后的饼状图
    fig, ax = plt.subplots()
    colors_custom = ['lightblue', 'lightgreen', 'salmon', 'lavender', 'gold']
    ax.pie(sizes_percentage_fixed, labels=labels_fixed, autopct='%1.1f%%', startangle=90, colors=colors_custom)
    ax.axis('equal')  # 确保饼图是圆形的

    # 添加标题
    ax.set_title('Top 5 Most Incorrect Answers (Fixed)')

    image_path = 'static/images/output/pie_chart.png'
    plt.savefig(image_path)  # 保存图表为文件
    return image_path  # 返回图像文件的路径

def main():
    student_scores_path = 'csv/output/student_scores.csv'
    df = load_student_scores(student_scores_path)
    bar_chart_path = bar_chart(df)
    pie_chart_path = pie_chart(df)
    print(f"Bar chart saved to: {bar_chart_path}")
    print(f"Pie chart saved to: {pie_chart_path}")

if __name__ == '__main__':
    main()