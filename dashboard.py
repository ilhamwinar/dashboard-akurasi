import streamlit as st
import pandas as pd
from influxdb import DataFrameClient
from datetime import *
import pytz
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns


def convert_to_utc(dt_str):
    Format  = "%Y-%m-%d"
    Format_iso="%Y-%m-%d"
    local_dt = datetime.strptime(dt_str, Format)
    print('Datetime in Local Time zone: ', local_dt)
    dt_utc = local_dt.astimezone(pytz.UTC).isoformat()
    print('Datetime in UTC Time zone: ', dt_utc)
    print(type(dt_utc))
    return dt_utc

def convert_to_utc_hari(dt_str):
#     start=dt_str+" "+"00:00:00"
    start= dt_str
    local_dt = datetime.strptime(start, "%Y-%m-%d")
    td = timedelta(hours=+23, minutes=+59)
    end_dt=local_dt+td
    print('Datetime in start Time zone: ', local_dt)
    print('Datetime in end Time zone: ', end_dt)
    start_dt_utc = local_dt.astimezone(pytz.UTC).isoformat()
    end_dt_utc = end_dt.astimezone(pytz.UTC).isoformat()
    print('Datetime in UTC start Time zone: ', start_dt_utc)
    print('Datetime in UTC end Time zone: ', end_dt_utc)
    return start_dt_utc,end_dt_utc

def shift3(dt_str_start,dt_str_end):
#     start=dt_str+" "+"00:00:00"
    start= dt_str_start
    end= dt_str_end
    local_dt = datetime.strptime(start, "%Y-%m-%d %H-%M-%S")
    end_dt = datetime.strptime(end, "%Y-%m-%d %H-%M-%S")
    print('Datetime in start Time zone: ', local_dt)
    print('Datetime in end Time zone: ', end_dt)
    start_dt_utc = local_dt.astimezone(pytz.UTC).isoformat()
    end_dt_utc = end_dt.astimezone(pytz.UTC).isoformat()
    print('Datetime in UTC start Time zone: ', start_dt_utc)
    print('Datetime in UTC end Time zone: ', end_dt_utc)
    return start_dt_utc,end_dt_utc


st.set_page_config(layout="wide")

st.title ("AKURASI AVC DASHBOARD")
ip = st.text_input("Masukan IP")
httpserver = "http://"+ip+":8080"

today = datetime.today()
start_date = st.date_input('Start date', today)
end_date = st.date_input('End date', today)
try:
    client = DataFrameClient(ip, 8086, '', '', 'avc')
    start = start_date.strftime("%Y-%m-%d")
    end = end_date.strftime("%Y-%m-%d")


    start_time=convert_to_utc(start)
    end_time=convert_to_utc(end)
    # Query String per Hari 
    string_query_select = 'SELECT * FROM "jurnal_data" WHERE time >='
    string_query_time_start = "'" + start_time + "'"
    string_query = " and time <= "
    string_query_time_end = "'" + end_time + "'"
    data = client.query(string_query_select+string_query_time_start+string_query+string_query_time_end)

    df = pd.DataFrame(data["jurnal_data"])
    df['gol_avc'] = df['gol_avc'].replace([6],1)
    # df['gol_avc'] = df['gol_avc'].replace([0],1)
    cam1=[]
    for row,koreksi in zip(df.itertuples(),range(len(df))):
        print(row)
        cam = httpserver+row.cam1_location.replace("..", "")
        print(cam)
        cam1.append(cam)
    df['cam1']=cam1
    st.write(df)
    
except:
    pass

def get_table_download_link_csv(df):
    #csv = df.to_csv(index=False)
    csv = df.to_csv().encode()
    #b64 = base64.b64encode(csv.encode()).decode() 
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{ip}.csv" target="_blank">Download csv file</a>'
    return href

# df = df # your dataframe
st.markdown(get_table_download_link_csv(df), unsafe_allow_html=True)
st.title('Akurasi Matrix')

# Parse AI data from Cam Location
gol_avc_ai = df['cam1_location'].str[26:27].replace("0", "1")
# Add Gol AI to Data Frame 
df['gol_avc_ai'] = gol_avc_ai
# Combine AI and PulTol
gol_kombinasi = df['gol_trans'].apply(str) + df['cam1_location'].str[26:27].replace("0", "1").replace("8", "1")
# Add Combine Gol to Data Frame
df['gol_kombinasi'] = gol_kombinasi
# Count Combine Gol
gol_11 = df[df.gol_kombinasi=='11'].count()["gol_kombinasi"]
gol_12 = df[df.gol_kombinasi=='12'].count()["gol_kombinasi"]
gol_13 = df[df.gol_kombinasi=='13'].count()["gol_kombinasi"]
gol_14 = df[df.gol_kombinasi=='14'].count()["gol_kombinasi"]
gol_15 = df[df.gol_kombinasi=='15'].count()["gol_kombinasi"]
gol_21 = df[df.gol_kombinasi=='21'].count()["gol_kombinasi"]
gol_22 = df[df.gol_kombinasi=='22'].count()["gol_kombinasi"]
gol_23 = df[df.gol_kombinasi=='23'].count()["gol_kombinasi"]
gol_24 = df[df.gol_kombinasi=='24'].count()["gol_kombinasi"]
gol_25 = df[df.gol_kombinasi=='25'].count()["gol_kombinasi"]
gol_31 = df[df.gol_kombinasi=='31'].count()["gol_kombinasi"]
gol_32 = df[df.gol_kombinasi=='32'].count()["gol_kombinasi"]
gol_33 = df[df.gol_kombinasi=='33'].count()["gol_kombinasi"]
gol_34 = df[df.gol_kombinasi=='34'].count()["gol_kombinasi"]
gol_35 = df[df.gol_kombinasi=='35'].count()["gol_kombinasi"]
gol_41 = df[df.gol_kombinasi=='41'].count()["gol_kombinasi"]
gol_42 = df[df.gol_kombinasi=='42'].count()["gol_kombinasi"]
gol_43 = df[df.gol_kombinasi=='43'].count()["gol_kombinasi"]
gol_44 = df[df.gol_kombinasi=='44'].count()["gol_kombinasi"]
gol_45 = df[df.gol_kombinasi=='45'].count()["gol_kombinasi"]
gol_51 = df[df.gol_kombinasi=='51'].count()["gol_kombinasi"]
gol_52 = df[df.gol_kombinasi=='52'].count()["gol_kombinasi"]
gol_53 = df[df.gol_kombinasi=='53'].count()["gol_kombinasi"]
gol_54 = df[df.gol_kombinasi=='54'].count()["gol_kombinasi"]
gol_55 = df[df.gol_kombinasi=='55'].count()["gol_kombinasi"]

# Create Data Frame Confussion Matrix
df_confusion_matrix = pd.DataFrame({'1': [gol_11, gol_21, gol_31, gol_41, gol_51],'2': [gol_12, gol_22, gol_32, gol_42, gol_52],'3': [gol_13, gol_23, gol_33, gol_43, gol_53],'4': [gol_14, gol_24, gol_34, gol_44, gol_54],'5': [gol_15, gol_25, gol_35, gol_45, gol_55]})
df_confusion_matrix.index = df_confusion_matrix.index + 1
st.dataframe(df_confusion_matrix)

# Count Total Gol
total_gol_1 = gol_11 + gol_12 + gol_13 + gol_14 + gol_15
total_gol_2 = gol_21 + gol_22 + gol_23 + gol_24 + gol_25
total_gol_3 = gol_31 + gol_32 + gol_33 + gol_34 + gol_35
total_gol_4 = gol_41 + gol_42 + gol_43 + gol_44 + gol_45
total_gol_5 = gol_51 + gol_52 + gol_53 + gol_54 + gol_55

# Count Percentage
percentage_gol_11 = (df[df.gol_kombinasi=='11'].count()["gol_kombinasi"]/total_gol_1)*100
percentage_gol_12 = (df[df.gol_kombinasi=='12'].count()["gol_kombinasi"]/total_gol_1)*100
percentage_gol_13 = (df[df.gol_kombinasi=='13'].count()["gol_kombinasi"]/total_gol_1)*100
percentage_gol_14 = (df[df.gol_kombinasi=='14'].count()["gol_kombinasi"]/total_gol_1)*100
percentage_gol_15 = (df[df.gol_kombinasi=='15'].count()["gol_kombinasi"]/total_gol_1)*100
percentage_gol_21 = (df[df.gol_kombinasi=='21'].count()["gol_kombinasi"]/total_gol_2)*100
percentage_gol_22 = (df[df.gol_kombinasi=='22'].count()["gol_kombinasi"]/total_gol_2)*100
percentage_gol_23 = (df[df.gol_kombinasi=='23'].count()["gol_kombinasi"]/total_gol_2)*100
percentage_gol_24 = (df[df.gol_kombinasi=='24'].count()["gol_kombinasi"]/total_gol_2)*100
percentage_gol_25 = (df[df.gol_kombinasi=='25'].count()["gol_kombinasi"]/total_gol_2)*100
percentage_gol_31 = (df[df.gol_kombinasi=='31'].count()["gol_kombinasi"]/total_gol_3)*100
percentage_gol_32 = (df[df.gol_kombinasi=='32'].count()["gol_kombinasi"]/total_gol_3)*100
percentage_gol_33 = (df[df.gol_kombinasi=='33'].count()["gol_kombinasi"]/total_gol_3)*100
percentage_gol_34 = (df[df.gol_kombinasi=='34'].count()["gol_kombinasi"]/total_gol_3)*100
percentage_gol_35 = (df[df.gol_kombinasi=='35'].count()["gol_kombinasi"]/total_gol_3)*100
percentage_gol_41 = (df[df.gol_kombinasi=='41'].count()["gol_kombinasi"]/total_gol_4)*100
percentage_gol_42 = (df[df.gol_kombinasi=='42'].count()["gol_kombinasi"]/total_gol_4)*100
percentage_gol_43 = (df[df.gol_kombinasi=='43'].count()["gol_kombinasi"]/total_gol_4)*100
percentage_gol_44 = (df[df.gol_kombinasi=='44'].count()["gol_kombinasi"]/total_gol_4)*100
percentage_gol_45 = (df[df.gol_kombinasi=='45'].count()["gol_kombinasi"]/total_gol_4)*100
percentage_gol_51 = (df[df.gol_kombinasi=='51'].count()["gol_kombinasi"]/total_gol_5)*100
percentage_gol_52 = (df[df.gol_kombinasi=='52'].count()["gol_kombinasi"]/total_gol_5)*100
percentage_gol_53 = (df[df.gol_kombinasi=='53'].count()["gol_kombinasi"]/total_gol_5)*100
percentage_gol_54 = (df[df.gol_kombinasi=='54'].count()["gol_kombinasi"]/total_gol_5)*100
percentage_gol_55 = (df[df.gol_kombinasi=='55'].count()["gol_kombinasi"]/total_gol_5)*100

# Create Data Frame Confussion Matrix Percentage
df_confusion_matrix_percentage = pd.DataFrame({'1': [percentage_gol_11, percentage_gol_21, percentage_gol_31, percentage_gol_41, percentage_gol_51],'2': [percentage_gol_12, percentage_gol_22, percentage_gol_32, percentage_gol_42, percentage_gol_52],'3': [percentage_gol_13, percentage_gol_23, percentage_gol_33, percentage_gol_43, percentage_gol_53],'4': [percentage_gol_14, percentage_gol_24, percentage_gol_34, percentage_gol_44, percentage_gol_54],'5': [percentage_gol_15, percentage_gol_25, percentage_gol_35, percentage_gol_45, percentage_gol_55]})
# Add Data Frame Index + 1
df_confusion_matrix_percentage.index = df_confusion_matrix_percentage.index + 1


st.dataframe(df_confusion_matrix_percentage)
total = total_gol_1 + total_gol_2 + total_gol_3 + total_gol_4 + total_gol_5
ok = gol_11 + gol_22 + gol_33 + gol_44 + gol_55
error = total - ok
accuracy = (ok/total)*100
error = (error/total)*100

st.success("Accuracy: " +str(accuracy)+" %")
st.error("Accuracy: " +str(error)+" %")





