import pandas as pd

# Define the function to create a CSV file
def create_csv(answers, file_path):
    # Create a DataFrame with 'Number' column ranging from 1 to 120
    df = pd.DataFrame({'Number': range(1, 121), 'Answer': answers, 'Weight': 1})
    # Ensure 'Answer' list is long enough, repeating if necessary
    df['Answer'] = df['Answer'] * (120 // len(answers) + (120 % len(answers) > 0))
    # Trim 'Answer' list to fit exactly 120 rows
    df['Answer'] = df['Answer'][:120]
    # Save to CSV
    df.to_csv(file_path, index=False)



# Example answer list, replace with the actual list you need

filled_answers_b = ['A', 'B', 'C', 'B', 'C', 'D', 'D', 'D', 'B', 'A',
                    'E', 'B', 'A', 'D', 'B', 'A', 'C', 'A', 'B', 'B',
                    'B', 'D', 'B', 'D', 'A', 'C', 'B', 'C', 'B', 'A',
                    'A', 'C', 'B', 'A', 'D', 'A', 'C', 'D', 'B', 'A',
                    'D', 'B', 'D', 'B', 'D', 'C', 'B', 'C', 'A', 'C',
                    'C', 'B', 'D', 'B', 'A', 'B', 'C', 'B', 'A', 'D',
                    'B', 'B', 'D', 'B', 'A', 'B', 'E', 'A', 'C', 'A',
                    'B', 'D', 'B', 'A', 'E', 'B', 'B', 'A', 'C', 'B',
                    'B', 'D', 'B', 'E', 'C', 'A', 'B', 'D', 'E', 'A',
                    'B', 'C', 'E', 'A', 'C', 'A', 'C', 'A', 'C', 'A',
                    'D', 'B', 'B', 'E', 'A', 'A', 'C', 'B', 'E', 'B',
                    'A', 'D', 'B', 'A', 'B', 'C', 'B', 'A', 'C', 'B']

# spider man
filled_answers_s = ['A', 'C', 'B', 'E', 'B', 'A', 'E', 'A', 'D', 'B',
                    'E', 'B', 'E', 'A', 'E', 'B', 'D', 'A', 'D', 'B',
                    'E', 'B', 'D', 'B', 'E', 'B', 'C', 'A', 'D', 'E',
                    'B', 'D', 'B', 'E', 'A', 'A', 'D', 'B', 'E', 'B',
                    'B', 'E', 'B', 'A', 'E', 'B', 'D', 'B', 'A', 'E',
                    'B', 'D', 'B', 'A', 'D', 'B', 'E', 'B', 'A', 'E',
                    'A', 'C', 'B', 'E', 'B', 'A', 'D', 'C', 'B', 'E',
                    'A', 'B', 'E', 'B', 'B', 'D', 'B', 'C', 'E', 'B',
                    'A', 'D', 'B', 'E', 'A', 'D', 'B', 'E', 'A', 'E',
                    'B', 'D', 'B', 'A', 'D', 'B', 'D', 'B', 'B', 'E',
                    'B', 'D', 'B', 'E', 'B', 'A', 'C', 'E', 'B', 'D',
                    'B', 'D', 'B', 'A', 'D', 'B', 'E', 'B', 'A', 'D']

answers = filled_answers_b
file_path = 'csv/master_answers/master_answer1.csv'
# Call the function to create the CSV file
create_csv(answers,file_path)
