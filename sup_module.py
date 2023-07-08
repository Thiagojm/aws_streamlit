import boto3
import streamlit as st
import pandas as pd

def csv_to_df(df, bit_count):
    df.dropna(inplace=True)
    df = df.reset_index()
    df['index'] = df['index'] + 1
    df = df.rename(columns={'index': 'Sample'})
    df['Sum'] = df['Ones'].cumsum()
    df['Average'] = df['Sum'] / (df['Sample'])
    df['Zscore'] = (df['Average'] - (bit_count / 2)) / (((bit_count / 4) ** 0.5) / (df['Sample'] ** 0.5))
    return df


def read_csv_aws():
    # AWS Credentials
    access_key = st.secrets['AWS_ACCESS_KEY']
    secret_key = st.secrets['AWS_SECRET_KEY']
    bucket_name = st.secrets['BUCKET_NAME']
    
    # Create an S3 client
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    # Specify the bucket name and file path
    file_path = 'rngs/test_rng/20230701-154643_pseudo_s2048_i1.csv'

    try:
        # Download the file to a local path
        s3.download_file(bucket_name, file_path, 'src/temp/local_file.csv')
        
        # Read the contents of the file into a Pandas dataframe
        df = pd.read_csv('src/temp/local_file.csv', sep=' ', names=["Time", "Ones"])
        return df
    
    except Exception as e:
        st.error(f"Error accessing S3 bucket: {e}")
