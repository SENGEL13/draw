import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
#import matplotlib.pyplot as plt
import altair as alt
import plotly.graph_objects as go

def data_input():#数据输入
    import_option = st.sidebar.selectbox(
        '数据导入方式?(手动输入 or 文件导入)',
        ['手动输入','文件导入'][::-1])
    if import_option == '手动输入':
        cs = hand_input()
        return cs
    elif import_option == "文件导入":
        cs = file_input()
        return cs
    

def hand_input():#手动输入数据
    labels_input = st.text_input('输入标签',help="以空格为间隔，如:a b c")
    labels = None
    data = None
    df = None
    if labels_input!="":
        labels = labels_input.split()
    if labels != None:
        data_input = st.text_input('输入数据',help="格式如:(1,2,3) (4,5,6)")
        if data_input!="":
            data_tag = list(map(eval,data_input.split()))
            data = None
            if type(data_tag[0])==type(1):
                data = data_tag
                length_judge = 0
            else:
                data = list(map(list,data_tag))
                length_judge = 1
            df_ahead = {}
            for i in range(len(labels)):
                if length_judge==0:
                    df_ahead[labels[i]] = [data[i]]
                elif length_judge==1:
                    df_ahead[labels[i]] = data[i]
                
            df = pd.DataFrame(df_ahead)
            st.dataframe(df)
            labels_select = st.multiselect("数据选择",df.columns,default=df.columns.values.tolist())
            return df,labels_select

def file_input():#文件导入数据
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
        labels_select = st.multiselect("数据选择",dataframe.columns,default=dataframe.columns.values.tolist())
        return dataframe,labels_select

def line_plot(cs=None):#折线图
    st.subheader('折线图')

    st.sidebar.info('导入与输入数据格式统一且固定，举例如下：')
    st.sidebar.write('不包含x数据:')
    data1 = pd.DataFrame({'a':[1,2,3,4],'b':[5,6,7,8]})
    st.sidebar.dataframe(data1)
    st.sidebar.info('其中标签个数和值可变')
    st.sidebar.write('包含x数据:')
    data2 = pd.DataFrame({'x':[1,2,3,4],'y':[5,6,7,8],'symbol':['a','a','b','b']})
    st.sidebar.dataframe(data2)
    st.sidebar.info('其中标签个数和值不可变')

    if cs != None:
        xexist_option = st.selectbox(
            '是否有一列为X取值?(若选择没有则以索引作为x的值)',
            ['有','没有'])
        if xexist_option=='没有':
            df = cs[0]
            labels = cs[1]
            st.write('图:')
            st.line_chart(df[labels])
        elif xexist_option=='有':
            c = alt.Chart(cs[0]).mark_line().encode(
                x='x',
                y='y',
                color='symbol',
                strokeDash='symbol',
            )
            st.altair_chart(c, use_container_width=True)

def area_plot(cs=None):#面积图
    st.subheader('面积图')

    st.sidebar.info('导入与输入数据格式与折线图中的不包含x值数据格式相同')

    if cs != None:
        df = cs[0]
        labels = cs[1]
        st.write('图:')
        st.area_chart(df[labels])

def hist_plot(cs=None):#条形图
    st.subheader('条形图')

    st.sidebar.info('导入与输入数据格式与折线图中的不包含x值数据格式相同')

    if cs != None:
        df = cs[0]
        labels = cs[1]
        st.write('图:')
        st.bar_chart(df[labels])

def pie_plot(cs=None):
    st.subheader('饼图')

    st.sidebar.info('数据格式举例如下')
    st.sidebar.dataframe(pd.DataFrame({'a':[40],'b':[60]}))
    st.sidebar.info('其中标签个数和值可变')

    if cs != None:
        hole_size = st.slider('洞的大小:',max_value=1.,min_value=0.,step=0.1)
        labels = cs[1]
        data = cs[0].values.tolist()[0]

        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=data, hole=float(hole_size))])
        st.plotly_chart(fig, use_container_width=True)



def main():
    st.title("我叫嘿嘿，我的作用是画图")

    option = st.sidebar.selectbox(
        'Which number do you like best?',
        ['主页','折线图','面积图','条形图','饼图'])

    if option == '主页':
        st.write("这是主页，还没想好放什么")
    elif option=='折线图':
        cs = data_input()
        line_plot(cs)
    elif option=='面积图':
        cs = data_input()
        area_plot(cs)
    elif option=='条形图':
        cs = data_input()
        hist_plot(cs)
    elif option=='饼图':
        cs = data_input()
        pie_plot(cs)

main()



