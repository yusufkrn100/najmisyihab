#Nama : Yusuf Kurniawan
#NIM : 12220089
#UAS Pemrograman Komputer 2021/2022
#https://github.com/yusufkrn100/uas_12220089
#https://share.streamlit.io/yusufkrn100/uas_12220089/main/uas_12220089.py


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import streamlit as st

############### header image ###############
st.set_page_config(layout="wide")
st.image("refinery.jpg")

############### login ###############
def kata_login():
    st.header('Selamat Datang di "Statistik Produksi Minyak Mentah"')
    st.markdown('*Silahkan login terlebih dahulu... *')
    st.markdown('Gunakan akun email ITB Anda ( **name@itb.ac.id** ) dengan password ( **name** ), Contoh :')
    st.markdown('- email : **yusuf@itb.ac.id**')
    st.markdown('- password : **yusuf**')

############### sidebar for login ###############
st.sidebar.image("SPE.png")
st.sidebar.title("Login")
email=st.sidebar.text_input('Masukkan email :')
email1=email.lower()
email2=email1.strip()
if email2.endswith("@itb.ac.id"):
    atpos = int(email2.find('@'))
    nama = email2[0:atpos]
    if nama != "":
        password=st.sidebar.text_input('Masukkan password :')
        passwo=password.lower()
        passw=passwo.strip()
        if passw == nama:
            login=st.sidebar.checkbox('Login')
            if login==True:
                st.sidebar.write(f'Hi {nama.capitalize()}, Anda telah berhasil login')

                ############### title ###############
                st.title("Statistik Produksi Minyak Mentah")
                st.markdown("*Sumber data berasal dari [produksi_minyak_mentah.csv](https://raw.githubusercontent.com/yusufkrn100/UAS/main/produksi_minyak_mentah.csv)*")
                
                ############### membuka file ###############
                df=pd.read_csv('produksi_minyak_mentah.csv')
                df1=pd.read_json('kode_negara_lengkap.json')

                ############### fungsi konversi ###############             
                def nama(kode_negara):
                    index = (df1[df1['alpha-3']==kode_negara].index.values)
                    nama = df1.iloc[index[0]]['name']
                    return(nama)

                def region(kode_negara):
                    index = (df1[df1['alpha-3']==kode_negara].index.values)
                    region = df1.iloc[index[0]]['region']
                    return(region)

                def sub_region(kode_negara):
                    index = (df1[df1['alpha-3']==kode_negara].index.values)
                    subregion = df1.iloc[index[0]]['sub-region']
                    return(subregion)  
  
                ############### list kode negara dan list kode gabungan negara ###############
                list_negara=[]
                gabungan_negara=[]
                kode_unik=df["kode_negara"].unique() 

                for kode in kode_unik:
                    if kode in df1['alpha-3'].values:
                        negara=nama(kode)
                        list_negara.append(negara)
                    else:
                        gabungan_negara.append(kode)
                list_negara.sort()

                ############### sidebar for setting ###############
                st.sidebar.title("Pengaturan Tampilan")
                grafik = st.sidebar.radio("Pilih Jenis Grafik",('Grafik jumlah produksi suatu negara', 'Grafik jumlah produksi terbesar'))

                ############### Fitur Jumlah Produksi Suatu Negara ###############
                if grafik == 'Grafik jumlah produksi suatu negara':
                    N = st.sidebar.selectbox("Nama Negara", list_negara)
                    
                    index = (df1[df1['name']==N].index.values)
                    kode = df1.iloc[index[0]]['alpha-3']
                    subregion = df1.iloc[index[0]]['sub-region']
                    region = df1.iloc[index[0]]['region']

                    df2=df.loc[df['kode_negara']==kode]
                    sum=0
                    count=0
                    maks=max(df2['produksi'])
                    mins=min(df2['produksi'])
                    index_maks = (df[df['produksi']==maks].index.values)
                    tahun_maks = df.iloc[index_maks[0]]['tahun']
                    index_mins = (df[df['produksi']==mins].index.values)
                    tahun_mins = df.iloc[index_mins[0]]['tahun']

                    for produksi in df2['produksi']:
                        if produksi != 0 :
                            count = count+1
                            sum = sum+produksi
                    if sum > 0 :
                        rata = sum/count
                        rata = round(rata,4)
                    else:
                        rata=0          

                    ############### Grafik Jumlah Produksi Suatu Negara ###############
                    st.subheader(f'{N}')
                    st.write(f'{N} [{kode}] merupakan suatu negara yang terletak di kawasan region *{region}* atau lebih tepatnya di sub-region *{subregion}*. Merujuk pada data statistik jumlah produksi minyak mentah tahun 1971-2015 diketahui bahwa :')
                    st.write(f'- Rata-rata produksi minyak mentah {N}  adalah sebesar {rata}')
                    st.write(f'- Jumlah produksi minimun minyak mentah {N} adalah sebesar {mins} yang terjadi pada tahun {tahun_mins}') 
                    st.write(f'- Jumlah produksi maksimum minyak mentah {N} adalah sebesar {maks} yang terjadi pada tahun {tahun_maks}') 
                    left_col, mid_col, right_col= st.columns([2.5,0.1,1])
                    left_col.subheader(f'Grafik Jumlah Produksi Minyah Mentah {N}')
                    fig, ax = plt.subplots(figsize=(10,5))
                    ax.plot(df2['tahun'], df2['produksi'],color='b')
                    ax.set_xlabel('Tahun',fontsize=12)
                    ax.set_ylabel('Jumlah Produksi',fontsize=12)
                    left_col.pyplot(fig)

                    ############### Tabel Jumlah Produksi Suatu Negara ###############
                    right_col.subheader('Tabel Data')
                    df3=df2[['tahun','produksi']].set_index('tahun')
                    right_col.dataframe(df3)
                        
                ############### Fitur Jumlah Produksi Terbesar ###############
                elif grafik == 'Grafik jumlah produksi terbesar':
                    list_tahun=[]
                    for t in df["tahun"]:
                        if t not in list_tahun:
                            list_tahun.append(t)
                    list_tahun.insert(0,'Kumulatif')

                    T = st.sidebar.selectbox("Tahun", list_tahun)
                    
                    ############### Fitur Jumlah Produksi Kumulatif Terbesar ###############
                    if T=='Kumulatif':
                        df4=df.groupby('kode_negara',as_index=False,sort=False)['produksi'].sum()
                        df4=df4[~df4['kode_negara'].isin(x for x in gabungan_negara)]
                        df5=df4.sort_values(['produksi'],ascending=False).reset_index()
                        
                        ############### Sidebar ###############
                        sum_negara=0
                        for x in df5['produksi']:
                            if x > 0:
                                sum_negara=sum_negara+1
                        B = st.sidebar.slider("Jumlah Negara", min_value=1, max_value=sum_negara, value=20)         
                        
                        ############### List negara dengan produksi terbesar dan terkecil ###############
                        kode_kum=[]
                        produksi_kum=[]
                        negara_kum=[]

                        for i in range (B) :
                            kode=df5.iloc[i]['kode_negara']
                            jumlah = df5.iloc[i]['produksi']
                            produksi_kum.append(jumlah)
                            kode_kum.append(kode)

                        for kode in kode_kum:
                            index = (df1[df1['alpha-3']==kode].index.values)
                            negara = df1.iloc[index[0]]['name']
                            negara_kum.append(negara)
                    
                        terkecil_kum=max(df5['produksi'])
                        for y in df5['produksi']:
                            if y>0 :
                                if y < terkecil_kum:
                                    terkecil_kum=y

                        index_terkecil_kum = (df5[df5['produksi']==terkecil_kum].index.values)
                        kode_terkecil_kum = df5.iloc[index_terkecil_kum[0]]['kode_negara']

                        ############### Grafik Jumlah Produksi Kumulatif Terbesar ###############                            
                        st.subheader(f'Grafik {B} Besar Negara dengan Jumlah Produksi Minyah Mentah Kumulatif Terbesar Tahun 1971-2015')
                        cmap_name = 'tab10'
                        left_col, right_col= st.columns([6,1])
                        cmap = cm.get_cmap(cmap_name)
                        colors = cmap.colors[:B]
                        fig, ax = plt.subplots(figsize=[5,B/5])
                        ax.barh(negara_kum, produksi_kum, color=colors)
                        ax.set_xlabel('Produksi',fontsize=12)
                        ax.set_ylabel('Negara',fontsize=12)
                        ax.set_yticklabels(negara_kum, fontsize=10)
                        ax.invert_yaxis()
                        left_col.pyplot(fig)

                        ############### Tabel Jumlah Produksi Kumulatif Terbesar ###############
                        st.subheader('Tabel Representasi Data')
                        df6=pd.DataFrame({"Negara": negara_kum, "Produksi": produksi_kum}) 
                        st.dataframe(df6, width=390)

                        ############### SUMMARY ###############
                        st.subheader(f'SUMMARY')
                        left_col, right_col= st.columns(2)
                        left_col.markdown(f'Negara dengan Jumlah Produksi Minyah Mentah Kumulatif Terbesar :')
                        left_col.markdown(f'- Nama Negara : **{negara_kum[0]}**')
                        left_col.markdown(f'- Kode Negara : **{kode_kum[0]}**')
                        left_col.markdown(f'- Region : **{region(kode_kum[0])}**')
                        left_col.markdown(f'- Sub-region : **{sub_region(kode_kum[0])}**')
                        left_col.markdown(f'- Jumlah produksi kumulatif : **{produksi_kum[0]}**')

                        right_col.markdown(f'Negara dengan Jumlah Produksi Minyah Mentah Kumulatif Terkecil :')
                        right_col.markdown(f'- Nama Negara : **{nama(kode_terkecil_kum)}**')
                        right_col.markdown(f'- Kode Negara : **{kode_terkecil_kum}**')
                        right_col.markdown(f'- Region : **{region(kode_terkecil_kum)}**')
                        right_col.markdown(f'- Sub-region : **{sub_region(kode_terkecil_kum)}**')
                        right_col.markdown(f'- Jumlah produksi kumulatif : **{terkecil_kum}**')
                    
                    ############### Fitur Jumlah Produksi Selain Kumulatif Terbesar ###############
                    else:
                        df7=df.loc[df['tahun']==T]
                        df7=df7[~df7['kode_negara'].isin(x for x in gabungan_negara)]
                        df8=df7.sort_values(['produksi'],ascending=False).reset_index()

                        ############### Sidebar ###############
                        sum_negara=0
                        for x in df8['produksi']:
                            if x > 0:
                                sum_negara=sum_negara+1
                        B = st.sidebar.slider("Jumlah Negara", min_value=1, max_value=sum_negara, value=20)

                        ############### List negara dengan produksi terbesar dan terkecil ###############
                        kode_=[]
                        produksi_=[]
                        negara_=[]

                        for i in range (B) :
                            code = df8.iloc[i]['kode_negara']
                            jumlahh = df8.iloc[i]['produksi']
                            produksi_.append(jumlahh)
                            kode_.append(code)

                        for kode in kode_:
                            index = (df1[df1['alpha-3']==kode].index.values)
                            negara = df1.iloc[index[0]]['name']
                            negara_.append(negara)

                        terkecil=max(df8['produksi'])
                        for x in df8['produksi']:
                            if x > 0:
                                if x < terkecil:
                                        terkecil=x
                              
                        index_terkecil = (df8[df8['produksi']==terkecil].index.values)
                        kode_terkecil = df8.iloc[index_terkecil[0]]['kode_negara']

                        ############### Grafik Jumlah Produksi Selain Kumulatif Terbesar ###############
                        st.subheader(f'Grafik {B} Besar Negara dengan Jumlah Produksi Minyah Mentah Terbesar pada Tahun {T}')
                        left_col, right_col= st.columns([6,1])
                        cmap_name = 'tab10'
                        cmap = cm.get_cmap(cmap_name)
                        colors = cmap.colors[:B]
                        fig, ax = plt.subplots(figsize=[5,B/5])
                        ax.barh(negara_, produksi_, color=colors)
                        ax.set_xlabel('Produksi',fontsize=12)
                        ax.set_ylabel('Negara',fontsize=12)
                        ax.set_yticklabels(negara_, fontsize=10)
                        ax.invert_yaxis()
                        left_col.pyplot(fig)

                        ############### Tabel Jumlah Produksi Selain Kumulatif Terbesar ###############
                        st.subheader('Tabel Representasi Data')
                        df9=pd.DataFrame({"Negara": negara_, "Produksi": produksi_}) 
                        st.dataframe(df9, width=390)

                        ############### SUMMARY ###############
                        st.subheader(f'SUMMARY')
                        left_col, right_col= st.columns(2)
                        left_col.markdown(f'Negara dengan Jumlah Produksi Minyah Mentah Terbesar Tahun {T} :')
                        left_col.markdown(f'- Nama Negara : **{negara_[0]}**')
                        left_col.markdown(f'- Kode Negara : **{kode_[0]}**')
                        left_col.markdown(f'- Region : **{region(kode_[0])}**')
                        left_col.markdown(f'- Sub-region : **{sub_region(kode_[0])}**')
                        left_col.markdown(f'- Jumlah produksi tahun {T} : **{produksi_[0]}**')

                        right_col.markdown(f'Negara dengan Jumlah Produksi Minyah Mentah Terkecil Tahun {T} :')
                        right_col.markdown(f'- Nama Negara : **{nama(kode_terkecil)}**')
                        right_col.markdown(f'- Kode Negara : **{kode_terkecil}**')
                        right_col.markdown(f'- Region : **{region(kode_terkecil)}**')
                        right_col.markdown(f'- Sub-region : **{sub_region(kode_terkecil)}**')
                        right_col.markdown(f'- Jumlah produksi tahun {T} : **{terkecil}**')
                                   
            else:
                st.subheader('Email dan Password Anda telah **BENAR**, silahkan login!')
        else:
            st.sidebar.write('Password invalid')
            kata_login()
    else:
        st.sidebar.write("Email Anda invalid silahkan ketik email.")
        kata_login()
elif '@' in email2:
     st.sidebar.write("Email Anda tidak terdaftar")
     kata_login()
else:
     st.sidebar.write("Email Anda invalid silahkan ketik email.")
     kata_login()
