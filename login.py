import streamlit as st
from streamlit_login_auth_ui.widgets import __login__

from io import StringIO
from pathlib import Path
import streamlit as st
import time
from detect import detect
import os
import sys
import argparse
from PIL import Image
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit_authenticator as stauth
__login__obj = __login__(auth_token = "courier_auth_token", 
                    company_name = "Shims",
                    width = 200, height = 250, 
                    logout_button_name = '登出', hide_menu_bool = False, 
                    hide_footer_bool = False, 
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN == True:

    # st.markdown("Your Streamlit Application Begins here!")
    st.title('YOLOv4 荔枝识别系统')

    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str,
                        default='D:/YOLO/yolov4-pytorch/model_data/2100_epoch', help='model.pt path(s)')
    parser.add_argument('--source', type=str,
                        default='data/images', help='source')
    parser.add_argument('--img-size', type=int, default=640,
                        help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float,
                        default=0.35, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float,
                        default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='',
                        help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true',
                        help='display results')
    parser.add_argument('--save-txt', action='store_true',
                        help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true',
                        help='save confidences in --save-txt labels')
    parser.add_argument('--nosave', action='store_true',
                        help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int,
                        help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true',
                        help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true',
                        help='augmented inference')
    parser.add_argument('--update', action='store_true',
                        help='update all models')
    parser.add_argument('--project', default='runs/detect',
                        help='save results to project/name')
    parser.add_argument('--name', default='exp',
                        help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true',
                        help='existing project/name ok, do not increment')
    opt = parser.parse_args()
    print(opt)


    # 地图展示
    # 方式1：设置表格属性，每一列的宽度相等
    # col_1, col_2, col_3 = st.columns(3)
    tab1, tab2 = st.tabs(["荔枝生长阶段检测", "荔枝数据可视化"])
    # tab1.write("this is tab 1")
    # tab2.write("this is tab 2")
    with tab1:
        # tab1.write("this is tab 1")
        # 图片检测
        source = ("图片检测", "视频检测")
        source_index = st.sidebar.selectbox("选择输入", range(
            len(source)), format_func=lambda x: source[x])
            

        if source_index == 0:
            uploaded_file = st.sidebar.file_uploader(
                "上传图片", type=['png', 'jpeg', 'jpg'])
            if uploaded_file is not None:
                is_valid = True
                with st.spinner(text='资源加载中...'):
                    st.sidebar.image(uploaded_file)
                    picture = Image.open(uploaded_file)
                    picture = picture.save(f'D:/YOLO/yolov4-pytorch/img/{uploaded_file.name}')
                    opt.source = f'D:/YOLO/yolov4-pytorch/img/{uploaded_file.name}'
            else:
                is_valid = False
        else:
            uploaded_file = st.sidebar.file_uploader("上传视频", type=['mp4'])
            if uploaded_file is not None:
                is_valid = True
                with st.spinner(text='资源加载中...'):
                    st.sidebar.video(uploaded_file)
                    with open(os.path.join("data", "videos", uploaded_file.name), "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    opt.source = f'data/videos/{uploaded_file.name}'
            else:
                is_valid = False

        if is_valid:
            print('valid')
            if st.button('开始检测'):

                image = detect(opt)
                st.balloons()
                st.image(image, caption='结果图像', use_column_width=True)
                # 用于在 Streamlit 页面上显示检测结果的图像。如果 source_index 等于0，则表示用户选择了检测结果文件夹作为图片源。
                # 接下来，使用 os.listdir 函数获取指定路径下的所有文件和目录的列表，对于列表中的每个文件，使用 st.image 函数将其显示在 Streamlit 页面上。
                # 最后，使用 st.balloons() 函数弹出一个气球，表示完成了图像的准备工作。
                # if source_index == 0:
                #     with st.spinner(text='Preparing Images'):
                #         for img in os.listdir(get_detection_folder()):
                #             st.image(str(Path(f'{get_detection_folder()}') / img))

                #         st.balloons()
                # else:
                #     with st.spinner(text='Preparing Video'):
                #         for vid in os.listdir(get_detection_folder()):
                #             st.video(str(Path(f'{get_detection_folder()}') / vid))

                #         st.balloons()

    with tab2:
        # 1、设置页面
        df = pd.read_csv("trees.csv")
        

        # 2、侧边栏：根据字段caretaker过滤数据
        owners = st.multiselect(
            "Tree owner filter : ",
            df['caretaker'].unique()
        )
        st.write("当前树的拥有者是：{}".format(owners))
        if owners:
            # 根据选择caretaker进行过滤
            df = df[df['caretaker'].isin(owners)]
        st.header("果树分布")
        # st.line_chart(df_groupby_dbh_count)
        st.subheader("根据经纬度，显示地图")
        # 清理'经度'和'维度'中的NaN
        new_df = df.dropna(subset=['longitude', 'latitude'])
        # 随机选择500个样本
        if len(new_df) > 500:
            new_df = new_df.sample(n=500)  # 如果行数大于 500，则展示抽样
        # st.map
        st.map(new_df)

        # 3、数据可视化
        st.markdown("### 默认显示前5行")
        st.write("df shape : ", df.shape)
        st.write(df.head())
        st.markdown("### 根据字段dbh分组统计")
        df_groupby_dbh_count = pd.DataFrame(df.groupby(['dbh']).count()['tree_id'].sort_values(ascending=False))
        df_groupby_dbh_count.columns = ['tree_count'] # 修改列名
        st.write(df_groupby_dbh_count)