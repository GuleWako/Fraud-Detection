import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def load_data(docs):
    Credit_Card = pd.read_csv(f'{docs}/creditcard.csv')
    Fraud_Data = pd.read_csv(f'{docs}/Fraud_Data.csv')
    IP_Address_To_Country = pd.read_csv(f'{docs}/IpAddress_to_Country.csv')
    return Credit_Card, Fraud_Data, IP_Address_To_Country