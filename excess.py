#!/usr/bin/env python
# coding: utf-8

# In[11]:

import pandas as pd
import streamlit as st
import base64
from io import BytesIO

def process_files(files):
    df_list = []

    for file in files:
        df = pd.read_excel(file, skiprows=5)
        df_list.append(df)

    combined_df1 = pd.concat(df_list, ignore_index=True)

    combined_df1 = combined_df1.rename(columns={
        'Buyer Division': 'Buyer Division',
        'Warehouse': 'Warehouse',
        'Item Group': 'Item Group',
        'Item Code': 'Item Code',
    })

    grouped_df1 = combined_df1.groupby(['Item Group', 'Item Code', 'Buyer Division', 'Prod Group', 'Proc Group', 'Description', 'Colour Size']).agg({
        'Tot Req': 'sum',
        'Order Qty': 'sum',
        'GRN Qty': 'sum',
        'PUT Qty': 'sum',
        'REC in Qty': 'sum',
        'REC out Qty': 'sum',
        'MO Issue Quantity': 'sum',
        'RO Issue Quantity': 'sum',
        'Balance Qty': 'sum'
    }).reset_index()

    grouped_df1 = grouped_df1.loc[:, ~grouped_df1.columns.str.startswith('Unnamed')]

    grouped_df1['Excess Order'] = grouped_df1['Order Qty'] - grouped_df1['Tot Req']
    grouped_df1['Excess Recieved'] = grouped_df1['GRN Qty'] - grouped_df1['Order Qty']
    grouped_df1['Production Savings'] = grouped_df1['Tot Req'] + (grouped_df1['MO Issue Quantity'] + grouped_df1['RO Issue Quantity'])
    grouped_df1['Net Reclassification'] = grouped_df1['REC in Qty'] + grouped_df1['REC out Qty']

    return grouped_df1

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    val = to_excel(df)
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="stylereco_output.xlsx">Download processed file</a>'

def main():
    st.set_page_config(page_title='Excess RM Reasoning', page_icon=':bar_chart:', layout='wide')

    st.title('Excess RM Reasoning')

    # Show an info box to explain what the app does
    st.info('Upload multiple Excel files and combine them into a single DataFrame. Perform various data transformations and aggregations, and generate a downloadable Excel output file.')

    # Allow users to upload multiple files
    uploaded_files = st.file_uploader("Choose Excel files", type=['xlsx'], accept_multiple_files=True)

    if uploaded_files:
        # Process the uploaded files
        df = process_files(uploaded_files)

        # Display the processed DataFrame
        st.subheader('Processed Data')
        st.dataframe(df)

        # Provide a download link for the processed file
        st.subheader('Download Processed File')
        st.markdown(get_table_download_link(df), unsafe_allow_html=True)
    else:
        # Prompt users to upload files
        st.warning('Please upload files.')

if __name__ == '__main__':
    main()






# In[ ]:




