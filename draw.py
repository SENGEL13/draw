import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO


st.title("我叫嘿嘿，我的作用是画图")

option = st.sidebar.selectbox(
    'Which number do you like best?',
     ['折线图','面积图','直方图'])

def import_file():
    uploaded_file = st.file_uploader("选择文件")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("gb18030"))
        # To read file as string:
        string_data = stringio.read()
        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write('数据:')
        st.dataframe(dataframe)
        labels = st.multiselect("数据选择",dataframe.columns,default=['a','b','c'])
        return dataframe,labels

def line_plot():#折线图
    st.subheader('折线图')
    cs = import_file()
    if cs != None:
        df = cs[0]
        labels = cs[1]
        st.write('图:')
        st.line_chart(df[labels])

def area_plot():#面积图
    st.subheader('面积图')
    cs = import_file()
    if cs != None:
        df = cs[0]
        labels = cs[1]
        st.write('图:')
        st.area_chart(df[labels])

def hist_plot():#直方图
    st.subheader('直方图(条形图)')
    cs = import_file()
    if cs != None:
        df = cs[0]
        labels = cs[1]
        st.write('图:')
        st.bar_chart(df[labels])


if option=='折线图':
    line_plot()
elif option=='面积图':
    area_plot()
elif option=='直方图':
    hist_plot()



