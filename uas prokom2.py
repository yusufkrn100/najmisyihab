import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

data_minyak = pd.read_csv('produksi_minyak_mentah.csv')
data_negara = pd.read_json('kode_negara_lengkap.json')
kode = pd.DataFrame(dict(kode_negara=list(data_negara['alpha-3']),nama_negara=list(data_negara['name'])))
data_minyak=data_minyak.merge(kode,how='left')

list_negara = data_minyak['nama_negara'].drop_duplicates().tolist()
list_tahun = data_minyak['tahun'].drop_duplicates().tolist()

st.title("Aplikasi Data Minyak Seluruh Dunia")
st.write("Aplikasi ini dapat menampilkan data produksi minyak dari seluruh dunia")
st.header("Bagian A")
st.write("Menampilkan grafik produksi minyak mentah suatu negara sepanjang tahun 1971-2015")
pilih_negara = st.selectbox("Pilih negara",list_negara)
pilih_jenis_plot = st.selectbox("Pilih jenis plot : ",['Bar Plot','Line Plot'])
batas_tahun = st.slider("Pilih batas tahun maksimal :",min_value = 1971,max_value=2015,value=2015)
batas_tahun = int(batas_tahun)
## A
selected_data_a = data_minyak[data_minyak['nama_negara']==pilih_negara]
selected_data_a = selected_data_a[selected_data_a['tahun']<=batas_tahun]
x_plot = selected_data_a['tahun']
y_plot = selected_data_a['produksi']

fig1,ax1 = plt.subplots(figsize=(8,6),dpi=200)
if pilih_jenis_plot == 'Line Plot' :
    ax1.set_title("Produksi Minyak " + pilih_negara + " Sepanjang 1971-2015" )
    ax1.plot(x_plot,y_plot)
    ax1.set_xlabel('Tahun')
    ax1.set_ylabel('Produksi')
else :
    ax1.set_title("Produksi Minyak " + pilih_negara + " Sepanjang 1971-2105")
    ax1.bar(x_plot,y_plot)
    ax1.set_xlabel('Tahun')
    ax1.set_ylabel('Produksi')

#Plotting GUI A
st.pyplot(fig1)

#GUI B
st.header("Bagian B & C")
st.write("Menampilkan grafik negara dengan produksi minyak sepanjang tahun dan pada tahun tertentu")
T = st.selectbox("Pilih tahun",list_tahun)
B = st.number_input("Masukkan jumlah negara yang ingin ditampilkan",min_value=1,max_value=None,value=5)
B = int(B)

## B
selected_data_b = data_minyak[data_minyak['tahun']==T]
selected_data_b = selected_data_b.dropna()
selected_data_b = selected_data_b.drop('tahun',axis=1)

data_b = selected_data_b.nlargest(B,'produksi')

fig2,ax2 = plt.subplots(figsize=(10,6),dpi=200)
sns.barplot(ax=ax2,data=data_b,x='kode_negara',y='produksi')
ax2.set_xlabel('Kode Negara')
ax2.set_ylabel('Produksi')
ax2.set_title(str(B)+" negara dengan produksi minyak mentah terbanyak pada tahun "+str(T))
st.pyplot(fig2)

## C

selected_data_c = data_minyak.groupby('nama_negara').sum()
selected_data_c = selected_data_c.drop('tahun',axis=1)
selected_data_c = selected_data_c.reset_index()

data_c = selected_data_c.nlargest(B,'produksi')


data_c = data_c.reset_index()
data_c = data_c.merge(kode,how='left')

fig3,ax3 = plt.subplots(figsize=(10,6),dpi=200)
sns.barplot(ax=ax3,data=data_c,x='kode_negara',y='produksi')
ax3.set_xlabel('Kode Negara')
ax3.set_ylabel('Produksi')
ax3.set_title(str(B)+" negara dengan produksi minyak mentah terbanyak sepanjang tahun 1971-2015 ")
st.pyplot(fig3)

## D

terbesar_tahun = data_negara.loc[data_negara['alpha-3']==data_b.loc[data_b['produksi'].idxmax()]['kode_negara']].drop(['alpha-2','country-code','iso_3166-2','intermediate-region','region-code','sub-region-code','intermediate-region-code'],axis=1)
terbesar_semua = data_negara.loc[data_negara['name']==data_c.loc[data_c['produksi'].idxmax()]['nama_negara']].drop(['alpha-2','country-code','iso_3166-2','intermediate-region','region-code','sub-region-code','intermediate-region-code'],axis=1)

selected_data_b_without_0 = selected_data_b[selected_data_b.produksi!=0]
selected_data_c_without_0 = selected_data_c[selected_data_c.produksi!=0]

terkecil_tahun = data_negara.loc[data_negara['alpha-3']==selected_data_b_without_0.loc[selected_data_b_without_0['produksi'].idxmin()]['kode_negara']].drop(['alpha-2','country-code','iso_3166-2','intermediate-region','region-code','sub-region-code','intermediate-region-code'],axis=1)

terkecil_semua = data_negara.loc[data_negara['name']==selected_data_c_without_0.loc[selected_data_c_without_0['produksi'].idxmin()]['nama_negara']].drop(['alpha-2','country-code','iso_3166-2','intermediate-region','region-code','sub-region-code','intermediate-region-code'],axis=1)

selected_data_b_0 = selected_data_b[selected_data_b.produksi==0]
selected_data_c_0 = selected_data_c[selected_data_c.produksi==0]

negara_nol_tahun = data_negara.loc[data_negara['alpha-3'].isin(selected_data_b_0['kode_negara'].tolist())].drop(['alpha-2','country-code','iso_3166-2','intermediate-region','region-code','sub-region-code','intermediate-region-code'],axis=1)
negara_nol_semua = data_negara.loc[data_negara['name'].isin(selected_data_c_0['nama_negara'].tolist())].drop(['alpha-2','country-code','iso_3166-2','intermediate-region','region-code','sub-region-code','intermediate-region-code'],axis=1)

st.header("Bagian D")
st.write("Negara dengan produksi minyak mentah terbesar pada tahun " + str(T))
st.dataframe(terbesar_tahun)
st.write("Negara dengan produksi minyak mentah terbesar sepanjang tahun 1971-2015")
st.dataframe(terbesar_semua)
st.write("Negara dengan produksi minyak mentah terkecil pada tahun " + str(T))
st.dataframe(terkecil_tahun)
st.write("Negara dengan produksi minyak mentah terkecil sepanjang tahun 1971-2015")
st.dataframe(terkecil_semua)
st.write("Negara tanpa produksi minyak mentah pada tahun " + str(T))
st.dataframe(negara_nol_tahun)
st.write("Negara tanpa produksi minyak mentah sepanjang tahun 1971-2015 ")
st.dataframe(negara_nol_tahun)