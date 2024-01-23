import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

df_all = pd.read_csv("data_all.csv")

df_all["dteday"] = pd.to_datetime(df_all["dteday"])
df_all.sort_values(by="dteday", inplace=True)
df_all.reset_index(inplace=True)


def hr(df):
    df_hr_daily = df.resample(rule="D", on="dteday").agg({
    "hr" : "sum",
    "cnt_x" : "sum",
    "casual_x" : "sum",
    "registered_x" : "sum"  
    })
    df_hr_daily = df_hr_daily.reset_index()
    df_hr_daily.rename(columns={
    "hr" : "hour",
    "cnt_x" : "total_sewa",
    "casual_x" : "casual",
    "registered_x" : "registered"
    },inplace=True)
    return df_hr_daily

def hr_working(df):
    df_hr_month = df.resample(rule="M", on="dteday").agg({
    "hr" : "sum",
    "cnt_x" : "sum",
    "casual_x" : "sum",
    "registered_x" : "sum"  
    })
    df_hr_month.index = df_hr_month.index.strftime("%Y-%m")
    df_hr_month = df_hr_month.reset_index()
    df_hr_month.rename(columns={
    "hr" : "hour",
    "cnt_x" : "total_sewa",
    "casual_x" : "casual",
    "registered_x" : "registered"
    },inplace=True)
    return df_hr_month


def sn(df):
    df_season = df.groupby(by="season_x").agg({
    "cnt_x" : "sum",
    "casual_x" : "sum",
    "registered_x" : "sum",
    }).sort_values(by="cnt_x", ascending=False).reset_index()
    df_season.rename(columns={
    "season_x" : "season",
    "cnt_x" : "total_sewa",
    "casual_x" : "casual",
    "registered_x" : "registered",
    },inplace=True)
    return df_season


tab1, tab2, tab3 = st.tabs(["Waktu Harian","Season", "Waktu Working Day"])


# sidebar
date_min = df_all["dteday"].min()
date_max = df_all["dteday"].max()


with st.sidebar:
    st.image("https://png.pngtree.com/png-vector/20191028/ourlarge/pngtree-logo-mountain-bike-cycling-mtb-isolated-vector-silhouette-downhill-cyclist-png-image_1908266.jpg")

# main page

with tab1:
    start_date, end_date = st.date_input(label="Range Date" ,min_value=date_min, max_value=date_max, value=[date_min, date_max])
    
    df_main = df_all[(df_all["dteday"]>=str(start_date))& (df_all["dteday"]<=str(end_date))]

    df_hr = hr(df_main)

    st.header("Sewa Sepeda")

    col1, col2 = st.columns(2)
    with col1:
        total_waktu = df_hr["hour"].sum()
        st.metric(label="Total waktu(jam)", value=total_waktu)

        total_casual = df_hr["casual"].sum()
        st.metric(label="Total casual", value=total_casual)

    with col2:
        avg_waktu = round(df_hr["hour"].mean(),2)
        st.metric(label="Rata-rata waktu(jam)", value=avg_waktu)

        total_register = df_hr["registered"].sum()
        st.metric(label="Total register", value=total_register)

    fig, ax = plt.subplots(figsize=(45,30))
    ax.plot(df_hr["dteday"], df_hr["hour"], marker='o', linewidth=4.5,)
    ax.tick_params(axis='y', labelsize=35)
    ax.tick_params(axis='x', labelsize=35)
    st.pyplot(fig)

with tab2:
    df_season = sn(df_all)
    st.header("Data Season Sewa Sepeda")
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"] 
    fig1, ax1 = plt.subplots(figsize=(45,30))
    sns.barplot(data=df_season, x="season", y="total_sewa",palette=colors)
    ax1.set_xlabel(None)
    ax1.set_ylabel(None)
    ax1.tick_params(axis='y', labelsize=30)
    ax1.tick_params(axis='x', labelsize=35)
    st.pyplot(fig1)

with tab3:
    df_work_h = df_all[df_all["workingday_x"]==1]
    df_work_h = hr_working(df_work_h)
    st.header("Data Waktu Sewa Sepeda Working Day")
    fig, ax = plt.subplots(figsize=(45,30))
    ax.plot(df_work_h["dteday"], df_work_h["hour"], marker='o', linewidth=4.5,)
    ax.tick_params(axis='y', labelsize=35)
    ax.tick_params(axis='x', labelsize=35, rotation=45)
    st.pyplot(fig)