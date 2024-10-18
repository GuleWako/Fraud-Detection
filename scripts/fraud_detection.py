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

def univariate_analysis(credit_card_data, credit_card_data_columns):
    for column in credit_card_data_columns:
        sns.histplot(credit_card_data[column], kde=True)
        plt.title(f'{column} Value Distribution')
        plt.show()
def bivariate_analysis(numerical_columns_data):
    plt.figure(figsize=(10,10))
    sns.heatmap(numerical_columns_data.corr(), annot=True, cmap='coolwarm')
    plt.title('Correlation between numerical columns')
    plt.show()
    
def merge_fraud_ip_address_data(fraud_data,ip_address_country):
    fraud_data = fraud_data.sort_values('ip_address')
    ip_address_country = ip_address_country.sort_values('lower_bound_ip_address')
    merged_fraud_data = pd.merge_asof(
        fraud_data, 
        ip_address_country, 
        left_on='ip_address', 
        right_on='lower_bound_ip_address', 
        direction='backward'
    )
    merged_fraud_data = merged_fraud_data[
        (merged_fraud_data['ip_address'] >= merged_fraud_data['lower_bound_ip_address']) & 
        (merged_fraud_data['ip_address'] <= merged_fraud_data['upper_bound_ip_address'])
    ]
    return merged_fraud_data