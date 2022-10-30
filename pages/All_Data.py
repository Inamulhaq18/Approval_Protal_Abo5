import psycopg2
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

conn=psycopg2.connect("postgres://ue0bragorjpsfg:p3401de69df0671d626efa0688fbb4b255afe17a00d95341e8504b5442c3516f3@ec2-52-18-7-194.eu-west-1.compute.amazonaws.com:5432/d1en285kafvdds") 
curr=conn.cursor()


#loading the data
sql = "SELECT * FROM master_product_table"
dat = pd.read_sql_query(sql,conn)

AgGrid(dat)
