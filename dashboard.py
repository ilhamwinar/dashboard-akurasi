import streamlit as st
import pandas as pd
from influxdb import DataFrameClient
from datetime import *
import pytz
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def convert_to_utc(dt_str):
    Format  = "%Y-%m-%d"
    Format_iso="%Y-%m-%d"
    local_dt = datetime.strptime(dt_str, Format)
    # print('Datetime in Local Time zone: ', local_dt)
    dt_utc = local_dt.astimezone(pytz.UTC).isoformat()
    # print('Datetime in UTC Time zone: ', dt_utc)
    # print(type(dt_utc))
    return dt_utc

def convert_to_utc_hari(dt_str):
#     start=dt_str+" "+"00:00:00"
    start= dt_str
    local_dt = datetime.strptime(start, "%Y-%m-%d")
    td = timedelta(hours=+23, minutes=+59)
    end_dt=local_dt+td
    # print('Datetime in start Time zone: ', local_dt)
    # print('Datetime in end Time zone: ', end_dt)
    start_dt_utc = local_dt.astimezone(pytz.UTC).isoformat()
    end_dt_utc = end_dt.astimezone(pytz.UTC).isoformat()
    # print('Datetime in UTC start Time zone: ', start_dt_utc)
    # print('Datetime in UTC end Time zone: ', end_dt_utc)
    return start_dt_utc,end_dt_utc

def shift3(dt_str_start,dt_str_end):
#     start=dt_str+" "+"00:00:00"
    start= dt_str_start
    end= dt_str_end
    local_dt = datetime.strptime(start, "%Y-%m-%d %H-%M-%S")
    end_dt = datetime.strptime(end, "%Y-%m-%d %H-%M-%S")
    # print('Datetime in start Time zone: ', local_dt)
    # print('Datetime in end Time zone: ', end_dt)
    start_dt_utc = local_dt.astimezone(pytz.UTC).isoformat()
    end_dt_utc = end_dt.astimezone(pytz.UTC).isoformat()
    # print('Datetime in UTC start Time zone: ', start_dt_utc)
    # print('Datetime in UTC end Time zone: ', end_dt_utc)
    return start_dt_utc,end_dt_utc


st.set_page_config(layout="wide")

st.title ("AKURASI AVC DASHBOARD")
st.text('Visualisasi data akurasi AVC Tahap 2, dengan memilih kode gerbang, didapatkan hasil akurasi AVC jika dibandingkan dengan data store (Data Transaksi) GTO. ')

option = st.selectbox(
     'Masukan Nama Gerbang!',
     ('Cikunir4_5', 'Cikunir4_6', 'Cikunir2_5',
     'Cikunir2_6', 'Cikunir2_7', 'Cakung1_3',
     'Cakung1_4','Bintara 3','Bintara 4',
     'PGB1','Bekasi_Barat16','Bekasi_Barat18',
     'Karawang_barat1_1','Karawang_barat1_3','Karawang_timur2_10',
     'Kalihurip1_8','Kalihurip1_10','Kalihurip2_1',
     'Kalihurip2_3','Cikatama1_1','Cikatama1_3',
     'Cikatama1_5','Cikatama1_7','Cikatama5_35',
     'Cikatama5_37','Cikatama5_39','Cikatama5_41',
     'Karawang_Barat2_13ON','Karawang_Barat2_13OFF','GunungPutri_5',
     'GunungPutri_6','GunungPutri_7','GunungPutri_8',
     'Citereup1_6','Citereup1_8','Citereup2_1','Citereup2_3',
     'Sentul1_6','Sentul1_8','Sentul2_1','Sentul2_3',
     'Sentul_selatan_5','Sentul_selatan_7',
     'Ciawi1_12','Ciawi1_14','Ciawi1_16','Ciawi1_18',
     'Ciawi2_11','Ciawi2_13','Ciawi2_15',
     ))
try:
    if option == 'Cikunir4_5':  
        ip='10.0.3.2'     
    if option == 'Cikunir4_6':  
        ip='10.0.4.2'
    if option == 'Cikunir2_5':  
        ip='10.0.5.2'
    if option == 'Cikunir2_6':  
        ip='10.0.6.2'
    if option == 'Cikunir2_7':
        ip='10.0.7.2'
    if option == 'Cakung1_3':
        ip='10.0.8.2'
    if option == 'Cakung1_4':
        ip='10.0.9.2'
    if option == 'Bintara 3':
        ip='10.0.53.2'
    if option == 'Bintara 4':
        ip='10.0.54.2'
    if option == 'PGB1':
        ip='10.0.12.2'
    if option == 'Bekasi_Barat16':
        ip='10.0.13.2'
    if option == 'Bekasi_Barat18':
        ip='10.0.14.2'
    if option == 'Karawang_barat1_1':
        ip='10.0.15.2'
    if option == 'Karawang_barat1_3':
        ip='10.0.16.2'
    if option == 'Karawang_timur2_10':
        ip='10.0.17.2'
    if option == 'Kalihurip1_8':
        ip='10.0.18.2'
    if option == 'Kalihurip1_10':
        ip='10.0.19.2'
    if option == 'Kalihurip2_1':
        ip='10.0.20.2'
    if option == 'Kalihurip2_3':
        ip='10.0.21.2'
    if option == 'Cikatama1_1':
        ip='10.0.22.2'
    if option == 'Cikatama1_3':
        ip='10.0.23.2'
    if option == 'Cikatama1_5':
        ip='10.0.24.2'
    if option == 'Cikatama1_7':
        ip='10.0.25.2'
    if option == 'Cikatama5_35':
        ip='10.0.26.2'
    if option == 'Cikatama5_37':
        ip='10.0.27.2'
    if option == 'Cikatama5_39':
        ip='10.0.28.2'
    if option == 'Cikatama5_41':
        ip='10.0.29.2'
    if option == 'Karawang_Barat2_13ON':
        ip='10.0.51.2'
    if option == 'Karawang_Barat2_13OFF':
        ip='10.0.52.2'
    if option == 'GunungPutri_5':
        ip='172.20.6.125'
    if option == 'GunungPutri_6':
        ip='172.20.6.126'
    if option == 'GunungPutri_7':
        ip='172.20.6.127'
    if option == 'GunungPutri_8':
        ip='172.20.6.128'
    if option == 'Citereup1_6':
        ip='172.20.5.126'
    if option == 'Citereup1_8':
        ip='1172.20.5.128'
    if option == 'Citereup2_1':
        ip='172.20.5.121'
    if option == 'Citereup2_3':
        ip='172.20.5.123'
    if option == 'Sentul1_6':
        ip='172.20.4.126'
    if option == 'Sentul1_8':
        ip='1172.20.4.128'
    if option == 'Sentul2_1':
        ip='172.20.4.121'
    if option == 'Sentul2_3':
        ip='172.20.4.123'
    if option == 'Sentul_selatan_5':
        ip='172.20.3.125'
    if option == 'Sentul_selatan_7':
        ip='172.20.3.127'
    if option == 'Ciawi1_12':
        ip='172.20.1.132'
    if option == 'Ciawi1_14':
        ip='172.20.1.134'
    if option == 'Ciawi1_16':
        ip='172.20.1.136'
    if option == 'Ciawi1_18':
        ip='172.20.1.138'
    if option == 'Ciawi2_11':
        ip='172.20.16.131'
    if option == 'Ciawi2_13':
        ip='172.20.16.133'
    if option == 'Ciawi2_15':
        ip='172.20.16.135'
except:
    pass


# ip = st.text_input("Masukan IP")
print(type(ip))
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
        # print(row)
        cam = httpserver+row.cam1_location.replace("..", "")
        # print(cam)
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
st.title('Akurasi Total')

# Parse AI data from Cam Location
df['gol_avc_ai'] = df['gol_avc'].replace("6", "1")

# Add Gol AI to Data Frame 
df= df[df['gol_avc_ai'] != 0]
df= df[df['gol_etoll'] != 0]

actual=list(df['gol_etoll'])
pred=list(df['gol_avc_ai'])
y_true_all= pd.Series(actual)
y_pred_all= pd.Series(pred)

tab=pd.crosstab(y_true_all, y_pred_all,rownames=['GTO'], colnames=['AVC'])
akurasi=np.diag(tab).sum() / tab.to_numpy().sum()
error =1-akurasi
st.success("Accuracy: " +str(akurasi*100)+" %")
st.error("Accuracy: " +str(error*100)+" %")
print("Akurasi: "+ str(akurasi))
print("error: "+ str(error))


st.title('Akurasi Confution Matrix')
fig = plt.figure(figsize=(4, 2))
sns.set(font_scale=0.6)
sns.heatmap(tab,label=['AVC', 'GTO'], annot=True,fmt='g', cmap='Blues')
st.pyplot(fig)

confusion_matrix_pcntg = pd.crosstab(y_true_all, y_pred_all, rownames=['GTO'], colnames=['AVC'], normalize='index')
fig2=plt.figure(figsize=(4, 2))
# sns.set(font_scale=1.5)
sns.heatmap(confusion_matrix_pcntg, cmap='rocket_r', annot=True, fmt=".2%")
st.pyplot(fig2)





