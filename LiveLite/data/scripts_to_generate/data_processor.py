"""
   This module is to clean teh NHANES combined raw data
   and preprocess data for Machine Leanring Model.

   Functions:
    - process_smoking()
    - process_sleeping()
    - process_general_1_5()
    - process_general_0_3()
    - process_activity()
    - process_ethnicity()
    - process_gender()
    - data_process()
    """
import pandas as pd
import numpy as np

def process_smoking(row):
    """
    This function handles invalid values in the Smoking factor.
    Args:
        row (pandas.series): A row from a dataframe.
    Returns:
        int: Processed value for the Smoking factor.
    """
    if row['SMQ040'] == 3:
        return 0
    if row['SMQ040'] in [1, 2]:
        return 1
    # Column applicable only for age above 18
    if row['RIDAGEYR'] > 18:
        return np.random.choice([0, 1])
    return 0


# Handle invalid values in Sleeping hours feature
def process_sleeping(row):
    """
    This function handles invalid values in the sleeping hours factor.
    Args:
        row (pandas.series): A row from a dataframe.
    Returns:
        int: Processed value for sleeping hours factor.
    """
    if pd.isnull(row['SLD012']):
        # Column applicable only for age above 10
        if row['RIDAGEYR'] < 10:
            return np.random.choice(np.arange(8, 14.6, 0.5))
        return np.random.choice(np.arange(2, 10.1, 0.5))
    return row['SLD012']

def process_general_1_5(row, column_name):
    """
    This function handles invalid values in any factor
    that ranges from category 1 to 5.
    Args:
        row (pandas.series): A row from a dataframe.
        column_name (str): The name of the column to process.
    Returns:
        int: Processed value the specified column.
    """
    # 7 & 9 are considered unknown or missing that needs to be handled.
    if row[column_name] in [7, 9] or pd.isnull(row[column_name]):
        return np.random.choice([1, 2, 3, 4, 5])
    return row[column_name]

def process_general_0_3(row, column_name):
    """
    This function handles invalid values in any factor
    that ranges from category 0 to 3.
    Args:
        row (pandas.series): A row from a dataframe.
        column_name (str): The name of the column to process.
    Returns:
        int: Processed value the specified column.
    """
    # 7 & 9 are considered unknown or missing that needs to be handled.
    if row[column_name] in [7, 9] or pd.isnull(row[column_name])\
    or row[column_name] not in [0, 1, 2, 3]:
        # Column applicable only for age above 16
        if row['RIDAGEYR'] <= 16:
            return 0
        return np.random.choice([0, 1, 2, 3])
    return row[column_name]

# Handle invalid values in Physical activity level feature
def process_activity(row):
    """
    This function handles invalid values in the sleeping hours factor.
    Args:
        row (pandas.series): A row from a dataframe.
    Returns:
        int: Processed value for sleeping hours factor.
    """
    if row['PAQ670'] in [77, 99] or pd.isnull(row['PAQ670'])\
    or row['PAQ670'] not in [1, 2, 3, 4, 5, 6, 7]:
        # Column applicable only for age above 12
        if row['RIDAGEYR'] <= 12:
            processed_value = 7
        processed_value = np.random.choice([1, 2, 3, 4, 5, 6, 7])
    processed_value = row['PAQ670']

    # Manually encode the values to match the tool activity dictionary,
    # sedentary to extremely active.
    if processed_value == 1:
        return 1
    if processed_value in [2, 3]:
        return 2
    if processed_value == 4:
        return 3
    if processed_value in [5, 6]:
        return 4
    return 5

# Handle invalid values ethnicity feature
def process_ethnicity(row):
    """
    This function handles invalid values in the ethnicity factor.
    Args:
        row (pandas.series): A row from a dataframe.
    Returns:
        int: Processed value for ethnicity factor.
    """
    if pd.isnull(row['RIDRETH3']) or row['RIDRETH3']\
    not in [1, 2, 3, 4, 6, 7]:
        return np.random.choice([1, 2, 3, 4, 6, 7])
    return row['RIDRETH3']


# Convert Gender column into binary.
def process_gender(row):
    """
    This function handles invalid values in the gender factor.
    Args:
        row (pandas.series): A row from a dataframe.
    Returns:
        int: Processed value for gender factor.
    """
    if row['RIAGENDR'] == 2:
        return 0
    return row['RIAGENDR']

def data_process(inputfile, outputfile):
    """
    This function reads and processes every record for selected columns.
    Args:
        inputfile (str): full path to the raw input file.
        outputfile (str): full path to the output file.
    Returns:
       None
    """
    # Columns for model training
    columns_to_read = [
        'SEQN',
        'BMXHT',
        'BMXWT',
        'RIDAGEYR',
        'DPQ020',
        'DPQ050',
        'SLD012',
        'PAQ670',
        'DBQ700',
        'HUQ010',
        'RIAGENDR',
        'RIDRETH3',
        'SMQ040',
        'INDFMPIR'
    ]

    df = pd.read_csv(inputfile, usecols=columns_to_read)

    # Drop rows with blank height or weight
    df.dropna(subset=['BMXHT', 'BMXWT'], inplace=True)

    # BMI = weight (kg) / (height (m) ^ 2)
    df['BMI'] = df['BMXWT'] / ((df['BMXHT'] / 100) ** 2)

    # Add a new binary column 'Is_obese' based on BMI
    df['IsObese'] = (df['BMI'] >= 30).astype(int)

    df.drop(columns=['BMI'], inplace=True)

    # For each feature, apply the specific function to process null or invalid values.
    df['RIAGENDR'] = df.apply(process_gender, axis=1)
    df['SMQ040'] = df.apply(process_smoking, axis=1)
    df['SLD012'] = df.apply(process_sleeping, axis=1)
    df['HUQ010'] = df.apply(lambda row: process_general_1_5(row, 'HUQ010'), axis=1)
    df['DBQ700'] = df.apply(lambda row: process_general_1_5(row, 'DBQ700'), axis=1)
    df['DPQ050'] = df.apply(lambda row: process_general_0_3(row, 'DPQ050'), axis=1)
    df['DPQ020'] = df.apply(lambda row: process_general_0_3(row, 'DPQ020'), axis=1)
    df['PAQ670'] = df.apply(process_activity, axis=1)
    df['RIDRETH3'] = df.apply(process_ethnicity, axis=1)

    df.to_csv(outputfile, index=False)
    print(f"DF has been saved to '{outputfile}'.")

if __name__ == '__main__':
    IP = 'nhanes_obesity_factors.csv'
    OP = 'ml_input.csv'
    data_process(IP, OP)