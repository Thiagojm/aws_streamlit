import boto3
import streamlit as st
import pandas as pd
import os, re


def find_interval(filename):
    match_i = re.search(r"_i(\d+).", filename)
    interval = int(match_i.group(1))
    return interval

def find_bit_count(filename):
    match = re.search(r"_s(\d+)_i", filename)
    bit_count = int(match.group(1))
    return bit_count

def list_csv_files(s3, bucket_name, folder_path):
    try:
        # List objects in the specified folder
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)

        # Iterate through the objects and filter for .csv files
        # csv_files = [obj['Key'] for obj in response['Contents'] if obj['Key'].lower().endswith('.csv')]
        csv_files = [os.path.splitext(obj['Key'].split('/')[-1])[0] for obj in response['Contents'] if obj['Key'].lower().endswith('.csv')]
        return csv_files
    
    except Exception as e:
        print(f"Error accessing S3 bucket: {e}")
    

def create_s3_client():
    # AWS Credentials
    access_key = st.secrets['AWS_ACCESS_KEY']
    secret_key = st.secrets['AWS_SECRET_KEY']
    
    # Create an S3 client
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    return s3

def csv_to_df(df, bit_count):
    df.dropna(inplace=True)
    df = df.reset_index()
    df['index'] = df['index'] + 1
    df = df.rename(columns={'index': 'Sample'})
    df['Sum'] = df['Ones'].cumsum()
    df['Average'] = df['Sum'] / (df['Sample'])
    df['Zscore'] = (df['Average'] - (bit_count / 2)) / (((bit_count / 4) ** 0.5) / (df['Sample'] ** 0.5))
    return df


def read_csv_aws(s3, bucket_name, folder_path, file_name):
    # Specify the bucket name and file path
    file_path = os.path.join(folder_path, file_name)

    try:
        # Download the file to a local path
        s3.download_file(bucket_name, file_path, 'src/temp/local_file.csv')
        
        # Read the contents of the file into a Pandas dataframe
        df = pd.read_csv('src/temp/local_file.csv', sep=' ', names=["Time", "Ones"])
        return df
    
    except Exception as e:
        st.error(f"Error accessing S3 bucket: {e}")
