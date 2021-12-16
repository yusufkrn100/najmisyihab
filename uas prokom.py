#panggil beberapa library yang dibutuhkan

import streamlit as st
import time
import numpy as np
import pandas as pd
import altair as alt

import inspect
import textwrap
from collections import OrderedDict
import streamlit as st
from streamlit.logger import get_logger

from PIL import Image

background = ''' <style> body {
background-image: url("https://images.unsplash.com/photo-1629196911514-cfd8d628ba26?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=699&q=80");
background-size: cover; } </style>
'''

st.markdown(background, unsafe_allow_html=True)

#-------create function def-------------

# baca data json dan csv
df1 = pd.read_json("kode_negara_lengkap.json")
df2 = pd.read_csv("produksi_minyak_mentah.csv")
df = pd.merge(df2,df1,left_on='kode_negara',right_on='alpha-3')

list_negara = df["name"].unique().tolist()
list_negara.sort()

#No 1.A
def no1a():

    data_negara = df["name"].unique().tolist()
    data_negara.sort()

    negara = st.sidebar.selectbox("Pilih Negara", data_negara)

    kode = df1[(df1["name"] == negara)]["alpha-3"].to_list()[0]
    df_states = df2[(df2.kode_negara == kode)].copy().set_index("tahun")
    st.subheader(f'Berikut adalah grafik dari negara {negara}.')

    origin = df[(df["name"] == negara)]
    
    chart = alt.Chart(origin).mark_bar(opacity=1).encode(
        x='tahun:N',
        y='produksi'
    )
    st.altair_chart(chart, use_container_width=True)

    a = origin.set_index("tahun").rename(columns={"produksi": "Produksi"})["Produksi"]

#No 1.B
def no1b():

    #command control streamlit
    jumlah_negara = st.sidebar.selectbox("Pilih negara", range(1, len(list_negara)), 9)
    tahun = st.sidebar.selectbox("Pilih tahun", range(1971, 2016), 44)

    st.subheader(f'{jumlah_negara} besar negara dengan jumlah produksi terbesar pada tahun {tahun}')

    res = df[(df.tahun == tahun)][["name", "produksi"]].sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
    res.index += 1

    source = res.iloc[:jumlah_negara]
    
    #making graph with altair
    bars = alt.Chart(source).mark_bar().encode(
        x='produksi',
        y=alt.Y(
                "name",
                sort=alt.EncodingSortField(field="produksi", order="descending"),
                title="Negara"))

    text = bars.mark_text(
        align='left',
        baseline='middle',
        color='black',
        dx=3 
    ).encode(
        text='produksi'
    )
    chart = (bars).configure_view(
    strokeWidth=10
)
    
    st.altair_chart(chart, use_container_width=True)
    

#No 1.C
def no1c():

    #command control streamlit
    jumlah_negara = st.sidebar.selectbox("Pilih negara", range(1, len(list_negara)), 9)

    st.subheader(f'{jumlah_negara} besar negara dengan jumlah produksi keseluruhan terbesar')

    res = df[["name", "produksi"]].groupby(['name'])['produksi'].sum().reset_index().sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
    res.index += 1

    source = res.iloc[:jumlah_negara]
    
    #making graph with altair
    bars = alt.Chart(source).mark_bar().encode(
        x='produksi',
        y=alt.Y(
                "name",
                sort=alt.EncodingSortField(field="produksi", order="descending"),
                title="Negara",
            )
    )

    text = bars.mark_text(
        align='left',
        baseline='middle',
        color='white',
        dx=3 
    ).encode(
        text='produksi'
    )
    chart = (bars+text).configure_view(
    strokeWidth=0
)
    
    st.altair_chart(chart, use_container_width=True)
    st.dataframe(source.rename(columns={"name": "Negara", "produksi":"Total Produksi"}))


#No 1.D
def no1d():

    tahun = st.sidebar.selectbox("Pilih tahun", range(1971, 2016), 44)

    total_produksi = df.groupby(['name', 'kode_negara', 'region', 'sub-region'])['produksi'].sum().reset_index().sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
    total_produksi_max = total_produksi[(total_produksi["produksi"] > 0)].iloc[0]
    total_produksi_min = total_produksi[(total_produksi["produksi"] > 0)].iloc[-1]
    total_produksi_nol = total_produksi[(total_produksi["produksi"] == 0)].sort_values(by=['name']).reset_index(drop=True)
    total_produksi_nol.index += 1

    produksi_tahun = df[(df["tahun"] == tahun)][['name', 'kode_negara', 'region', 'sub-region', 'produksi']].sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
    produksi_tahun_max = produksi_tahun[(produksi_tahun["produksi"] > 0)].iloc[0]
    produksi_tahun_min = produksi_tahun[(produksi_tahun["produksi"] > 0)].iloc[-1]
    produksi_tahun_nol = produksi_tahun[(produksi_tahun["produksi"] == 0)].sort_values(by=['name']).reset_index(drop=True)
    produksi_tahun_nol.index += 1

    
    st.markdown(
        f"""
        #### Negara dengan total produksi keseluruhan tahun terbesar
        Negara: {total_produksi_max["name"]}\n
        Kode negara: {total_produksi_max["kode_negara"]}\n
        Region: {total_produksi_max["region"]}\n
        Sub-region: {total_produksi_max["sub-region"]}\n
        Jumlah produksi: {total_produksi_max["produksi"]}\n

        #### Negara dengan jumlah produksi terbesar pada tahun {tahun}  
        Negara: {produksi_tahun_max["name"]}\n
        Kode negara: {produksi_tahun_max["kode_negara"]}\n
        Region: {produksi_tahun_max["region"]}\n
        Sub-region: {produksi_tahun_max["sub-region"]}\n
        Jumlah produksi: {produksi_tahun_max["produksi"]}\n

        #### Negara dengan total produksi keseluruhan tahun terkecil
        Negara: {total_produksi_min["name"]}\n
        Kode negara: {total_produksi_min["kode_negara"]}\n
        Region: {total_produksi_min["region"]}\n
        Sub-region: {total_produksi_min["sub-region"]}\n
        Jumlah produksi: {total_produksi_min["produksi"]}\n

        #### Negara dengan jumlah produksi terkecil pada tahun {tahun}  
        Negara: {produksi_tahun_min["name"]}\n
        Kode negara: {produksi_tahun_min["kode_negara"]}\n
        Region: {produksi_tahun_min["region"]}\n
        Sub-region: {produksi_tahun_min["sub-region"]}\n
        Jumlah produksi: {produksi_tahun_min["produksi"]}\n
    """
    )
    st.markdown(
        """
        #### Negara dengan total produksi keseluruhan tahun sama dengan nol
        
    """
    )
    total_produksi_nol = total_produksi_nol.drop(['produksi'], axis=1).rename(columns={"name":"Negara", "kode_negara":"Kode Negara", "region":"Region", "sub-region":"Sub Region"})
    st.dataframe(total_produksi_nol)
    st.markdown(
        f"""
        #### Negara dengan jumlah produksi sama dengan nol pada tahun {tahun}
        
    """
    )
    produksi_tahun_nol = produksi_tahun_nol.drop(['produksi'], axis=1).rename(columns={"name":"Negara", "kode_negara":"Kode Negara", "region":"Region", "sub-region":"Sub Region"})
    st.dataframe(produksi_tahun_nol)

#home
def home():

    st.markdown("<h1 style='text-align: center; color: black;'> Nama Kamu </h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: black;'> Streamlit produksi minyak mentah </h2>", unsafe_allow_html=True)

#fungsi di panggil dibawah

LOGGER = get_logger(__name__)


FITUR = OrderedDict(
    [
        ("HOME", (home, None)),
        (
            "Fitur 1.a",
            (
                no1a,
                """
                Grafik jumlah produksi minyak mentah terhadap waktu (tahun) dari suatu negara N, dimana nilai
                N dapat dipilih oleh user secara interaktif. Nama negara N dituliskan secara lengkap bukan kode
                negaranya.
                """,
            ),
        ),
        (
            "Fitur 1.b",
            (
                no1b,
                """
                Grafik yang menunjukan B-besar negara dengan jumlah produksi terbesar pada tahun T, dimana
                nilai B dan T dapat dipilih oleh user secara interaktif.
                """,
            ),
        ),
        (
            "Fitur 1.c",
            (
                no1c,
                """
                Grafik yang menunjukan B-besar negara dengan jumlah produksi terbesar secara kumulatif
                keseluruhan tahun, dimana nilai B dapat dipilih oleh user secara interaktif.
                """,
            ),
        ),
        (
            "Fitur 1.d",
            (
                no1d,
                """
                Informasi yang menyebutkan: (1) nama lengkap negara, kode negara, region, dan sub-region dengan jumlah produksi terbesar pada tahun T dan keseluruhan tahun. (1) nama lengkap negara, kode negara, region, dan sub-region dengan jumlah produksi terkecil (tidak sama dengan nol) pada tahun T dan keseluruhan tahun. (1) nama lengkap negara, kode negara, region, dan subregion dengan jumlah produksi sama dengan nol pada tahun T dan keseluruhan tahun.
                """,
            ),
        ),

    ]
)


def run():
    demo_name = st.sidebar.selectbox("Silahkan fitur yang kamu pilih", list(FITUR.keys()), 0)

    demo = FITUR[demo_name][0]
    if demo_name == "HOME":
        pass
    else:
        st.markdown("# %s" % demo_name)
        description = FITUR[demo_name][1]
        if description:
            st.write(description)

        for i in range(10):
            st.empty()

    demo()

if __name__ == "__main__":
    run()