import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import LabelEncoder

def load_data(docs):
    Credit_Card = pd.read_csv(f'{docs}/creditcard.csv')
    Fraud_Data = pd.read_csv(f'{docs}/Fraud_Data.csv')
    IP_Address_To_Country = pd.read_csv(f'{docs}/IpAddress_to_Country.csv')
    return Credit_Card, Fraud_Data, IP_Address_To_Country

def find_missing_values(df):
    null_counts = df.isnull().sum()
    missing_value = null_counts
    percent_of_missing_value = 100 * null_counts / len(df)
    data_type = df.dtypes

    missing_data_summary = pd.concat([missing_value, percent_of_missing_value, data_type], axis=1)
    missing_data_summary_table = missing_data_summary.rename(columns={0: "Missing values", 1: "Percent of Total Values", 2: "DataType"})
    missing_data_summary_table = missing_data_summary_table[missing_data_summary_table.iloc[:, 1] != 0].sort_values('Percent of Total Values', ascending=False).round(1)

    print(f"From {df.shape[1]} columns selected, there are {missing_data_summary_table.shape[0]} columns with missing values.")

    return missing_data_summary_table

def encodingCategoricalVariables(dataframe):
    categorical_columns = ['device_id','source','browser','country']
    encoder = LabelEncoder()
    for col in categorical_columns:
        dataframe[col + '_encoded'] = encoder.fit_transform(dataframe[col])
    dataframe.drop(columns=categorical_columns, inplace=True)
    
    return dataframe