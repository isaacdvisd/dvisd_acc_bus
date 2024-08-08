import pandas as pd
from datetime import datetime, timedelta


# Load the CSV file
def main():
    df = pd.read_csv('2024enrollment.csv')

    student_ids = set(df['HS ID#'])
    print(len(student_ids))
    print(len(df['HS ID#']))


if __name__ == "__main__":
    main()
