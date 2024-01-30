import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from streamlit_option_menu import option_menu

df_all = pd.read_csv("data_all.csv")

df_all["dteday"] = pd.to_datetime(df_all["dteday"])
df_all.sort_values(by="dteday", inplace=True)
df_all.reset_index(inplace=True)


def hr(df):
    df_hr_daily = df.resample(rule="D", on="dteday").agg({
        "hr" : "sum",
        "season_x" : "unique",
        "temp_x" : "sum",
        "atemp_x" : "sum",
        "hum_x" : "sum",
        "windspeed_x" : "sum",
        "cnt_x" : "sum",
        "casual_x" : "sum",
        "registered_x" : "sum",
        "workingday_x" : "unique",
        "weathersit_x" : "unique"
    })
    df_hr_daily = df_hr_daily.reset_index()
    df_hr_daily.rename(columns={
        "hr" : "hour",
        "season_x" : "season",
        "temp_x" : "temperature",
        "atemp_x" : "temperature_f",
        "hum_x" : "humidity",
        "windspeed_x" : "wind",
        "cnt_x" : "total_rent",
        "casual_x" : "casual",
        "registered_x" : "registered",
        "workingday_x" : "day",
        "weathersit_x" : "weathersit"
    },inplace=True)
    return df_hr_daily

def hr_m(df):
    df_hr_month = df.resample(rule="M", on="dteday").agg({
        "hr" : "sum",
        "season_x" : "unique",
        "temp_x" : "sum",
        "atemp_x" : "sum",
        "hum_x" : "sum",
        "windspeed_x" : "sum",
        "cnt_x" : "sum",
        "casual_x" : "sum",
        "registered_x" : "sum",
        "workingday_x" : "unique",
        "weathersit_x" : "unique"
    })
    df_hr_month.index = df_hr_month.index.strftime("%Y-%m")
    df_hr_month = df_hr_month.reset_index()
    df_hr_month.rename(columns={
        "hr" : "hour",
        "season_x" : "season",
        "temp_x" : "temperature",
        "atemp_x" : "temperature_f",
        "hum_x" : "humidity",
        "windspeed_x" : "wind",
        "cnt_x" : "total_rent",
        "casual_x" : "casual",
        "registered_x" : "registered",
        "workingday_x" : "day",
        "weathersit_x" : "weathersit"
    },inplace=True)
    return df_hr_month


def season_change(x):
    if x==1:
        return "Springer"
    elif x==2:
        return "Summer"
    elif x==3:
        return "Fall"
    else:
        return "Winter"
    
def working_day(x):
    if x==0:
        return "weekend"
    else:
        return "weekday"

def weath(x):
    if x==1:
        return "Sunny"
    elif x==2:
        return "Mist and Cloudy"
    elif x==3:
        return "Light Snow or Light Rain"
    else:
        return "Heavy Rain with thunderstrom or Mist with Snow"



# sidebar
date_min = df_all["dteday"].min()
date_max = df_all["dteday"].max()


with st.sidebar:
    st.image("https://png.pngtree.com/png-vector/20191028/ourlarge/pngtree-logo-mountain-bike-cycling-mtb-isolated-vector-silhouette-downhill-cyclist-png-image_1908266.jpg")
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Report"]
    )


# main page
if selected == "Home":
    st.title(selected)
    tab1, tab2 = st.tabs(["Daily","Recap"])

    with tab1:
        st.header("Rent a Bicycle")
        start_date, end_date = st.date_input(label="Range Date" ,min_value=date_min, max_value=date_max, value=[date_min, date_max])
        
        df_main = df_all[(df_all["dteday"]>=str(start_date))& (df_all["dteday"]<=str(end_date))]

        df_hr = hr(df_main)
        df_hr["season"] = df_hr["season"].apply(season_change)
        df_hr["day"] = df_hr["day"].apply(working_day)
        df_hr["weathersit"] = df_hr["weathersit"].apply(weath)


        st.subheader("Rent Count")
        col1, col2, col3 = st.columns(3)
        with col1:
            total_sewa= df_hr["total_rent"].sum()
            st.metric(label="Total Rent :bicyclist:", value=total_sewa)

        with col2:
            total_register = df_hr["registered"].sum()
            st.metric(label="Total Rent Registered :bicyclist:", value=total_register)

        with col3:
            total_casual = df_hr["casual"].sum()
            st.metric(label="Total Rent Casual :bicyclist:", value=total_casual)


        fig, ax = plt.subplots(figsize=(45,30))
        ax.plot(df_hr["dteday"], df_hr["total_rent"], marker='o', linewidth=4.5,)
        ax.tick_params(axis='y', labelsize=40)
        ax.tick_params(axis='x', labelsize=40)
        st.pyplot(fig)


        st.subheader("Rent by the hour")
        col1, col2 = st.columns(2)
        with col1:
            total_waktu = df_hr["hour"].sum()
            st.metric(label="Total Time(hours) :clock10:", value=total_waktu)

        with col2:
            avg_waktu = round(df_hr["hour"].mean(),2)
            st.metric(label="Avg Time(hours) :clock10:", value=avg_waktu)


        fig, ax = plt.subplots(figsize=(45,30))
        ax.plot(df_hr["dteday"], df_hr["hour"], marker='o', linewidth=4.5,)
        ax.tick_params(axis='y', labelsize=40)
        ax.tick_params(axis='x', labelsize=40)
        st.pyplot(fig)

        st.subheader("Temperature")
        col1, col2 = st.columns(2)
        with col1:
            avg_temp = round(df_hr["temperature"].mean(),2)
            st.metric(label="Avg Normalized Temperature(°C) :thermometer:", value=avg_temp, delta=round(avg_temp/41,2))

        with col2:
            avg_temp_f = round(df_hr["temperature_f"].mean(),2)
            st.metric(label="Avg Normalized Feeling temperature(°C) :thermometer:", value=avg_temp_f, delta=round(avg_temp_f/50,2))


        fig, ax = plt.subplots(figsize=(45,30))
        ax.plot(df_hr["dteday"], df_hr["temperature"], marker='o', linewidth=4.5, label="Normalized Temperature(°C)")
        ax.plot(df_hr["dteday"], df_hr["temperature_f"], marker='o', linewidth=4.5, label="Normalized Feeling Temperature(°C)")
        ax.legend(fontsize="40")
        ax.tick_params(axis='y', labelsize=40)
        ax.tick_params(axis='x', labelsize=40)
        st.pyplot(fig)

        st.subheader("Humidity & Windspeed")
        col1, col2 = st.columns(2)
        with col1:
            avg_hum = round(df_hr["humidity"].mean(),2)
            st.metric(label="Avg Humidity(%) :snow_cloud:", value=avg_hum, delta=round(avg_hum/100,2))

        with col2:
            avg_wind = round(df_hr["wind"].mean(),2)
            st.metric(label="Avg Wind Speed(mph) :fog:", value=avg_wind, delta=round(avg_wind/67,2))


        fig, ax = plt.subplots(figsize=(45,30))
        ax.plot(df_hr["dteday"], df_hr["humidity"], marker='o', linewidth=4.5, label="Humidity(%)")
        ax.plot(df_hr["dteday"], df_hr["wind"], marker='o', linewidth=4.5, label="Wind Speed(mph)")
        ax.legend(fontsize="40")
        ax.tick_params(axis='y', labelsize=40)
        ax.tick_params(axis='x', labelsize=40)
        st.pyplot(fig)

    with tab2:
        st.header("Recap Rent")
        st.subheader("Rent by Season")
        df_season = hr(df_all)
        df_season["day"] = df_season["day"].apply(working_day)
        df_season["weathersit"] = df_season["weathersit"].apply(weath)

        season_select = st.selectbox(
            label="Select Season",
            options=('springer', 'summer', 'fall','winter'),
            # index=None,
            # placeholder="Select Season...",
            )
        
        df_season = df_season[df_season["season"]== str(season_select)]
    
        with st.container(border=True):
            colors = ["#72BCD4", "#D3D3D3"] 

            fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(45, 10))
            sns.barplot(data=df_season, x="weathersit", y="total_rent",hue="day",palette=colors, errorbar=None,ax=ax[0])
            ax[0].set_ylabel(None)
            ax[0].set_xlabel(None)
            ax[0].legend(fontsize=40)
            ax[0].set_title("Total Rent", loc="center", fontsize=45)
            ax[0].tick_params(axis ='x', labelsize=40, rotation=45)
            ax[0].tick_params(axis ='y', labelsize=38)

            sns.barplot(data=df_season, x="weathersit", y="registered",hue="day",palette=colors, errorbar=None,ax=ax[1])
            ax[1].set_ylabel(None)
            ax[1].set_xlabel(None)
            ax[1].legend(fontsize=40)
            ax[1].set_title("Total Register", loc="center", fontsize=45)
            ax[1].tick_params(axis ='x', labelsize=40, rotation=45)
            ax[1].tick_params(axis ='y', labelsize=38)

            sns.barplot(data=df_season, x="weathersit", y="casual",hue="day",palette=colors, errorbar=None,ax=ax[2])
            ax[2].set_ylabel(None)
            ax[2].set_xlabel(None)
            ax[2].legend(fontsize=40)
            ax[2].set_title("Total Casual", loc="center", fontsize=45)
            ax[2].tick_params(axis ='x', labelsize=40, rotation=45)
            ax[2].tick_params(axis ='y', labelsize=38)

            st.pyplot(fig)

            with st.expander("See explanation"):
                st.write(
                f""" - The total rent is {df_season["total_rent"].sum()} with registered users of 
                {df_season["registered"].sum()} and casual users of {df_season["casual"].sum()}"""
                )
                st.write(
                """ - Total bicycle rentals, total registered users and casual users based on 
                weather conditions on weekends or weekdays""")

        with st.container(border=True):
            
            fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(45, 10))
            sns.barplot(data=df_season, x="day", y="temperature",hue="weathersit",palette=colors, errorbar=None,ax=ax[0])
            ax[0].set_ylabel(None)
            ax[0].set_xlabel(None)
            ax[0].legend(fontsize=25)
            ax[0].set_title("Temperature by Weathersit", loc="center", fontsize=45)
            ax[0].tick_params(axis ='x', labelsize=40)
            ax[0].tick_params(axis ='y', labelsize=38)

            sns.barplot(data=df_season, x="day", y="humidity",hue="weathersit",palette=colors, errorbar=None,ax=ax[1])
            ax[1].set_ylabel(None)
            ax[1].set_xlabel(None)
            ax[1].legend(fontsize=25)
            ax[1].set_title("Humidity by Weathersit", loc="center", fontsize=45)
            ax[1].tick_params(axis ='x', labelsize=40)
            ax[1].tick_params(axis ='y', labelsize=38)

            sns.barplot(data=df_season, x="day", y="wind",hue="weathersit",palette=colors, errorbar=None,ax=ax[2])
            ax[2].set_ylabel(None)
            ax[2].set_xlabel(None)
            ax[2].legend(fontsize=25)
            ax[2].set_title("Windspeed by Weathersit", loc="center", fontsize=45)
            ax[2].tick_params(axis ='x', labelsize=40)
            ax[2].tick_params(axis ='y', labelsize=38)
            
            st.pyplot(fig)

            with st.expander("See explanation"):
                st.write(
                """ Temperature, humidity and wind speed conditions are based on weather 
                in 1 season on weekends or weekdays""")

        with st.container(border=True):  
            fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(45, 10))
            sns.scatterplot(data=df_season, x="temperature", y="total_rent", hue="day",ax=ax[0])
            ax[0].set_ylabel(None)
            ax[0].set_xlabel(None)
            ax[0].legend(fontsize=25)
            ax[0].set_title("Temperature", loc="center", fontsize=45)
            ax[0].tick_params(axis ='x', labelsize=40)
            ax[0].tick_params(axis ='y', labelsize=38)

            sns.scatterplot(data=df_season, x="humidity", y="total_rent", hue="day",ax=ax[1])
            ax[1].set_ylabel(None)
            ax[1].set_xlabel(None)
            ax[1].legend(fontsize=25)
            ax[1].set_title("Humidity", loc="center", fontsize=45)
            ax[1].tick_params(axis ='x', labelsize=40)
            ax[1].tick_params(axis ='y', labelsize=38)

            sns.scatterplot(data=df_season, x="wind", y="total_rent", hue="day",ax=ax[2])
            ax[2].set_ylabel(None)
            ax[2].set_xlabel(None)
            ax[2].legend(fontsize=25)
            ax[2].set_title("Windspeed", loc="center", fontsize=45)
            ax[2].tick_params(axis ='x', labelsize=40)
            ax[2].tick_params(axis ='y', labelsize=38)
            
            st.pyplot(fig)

            with st.expander("See explanation"):
                st.write(
                """Distribution of temperature, humidity and wind speed data with total bicycle rentals. 
                The distribution between data creates different patterns that define relationships between data""")

        with st.container(border=True): 
            colors = ('#8B4513', '#FFF8DC', '#93C572')
            fig, ax = plt.subplots(ncols=2, figsize=(45, 10))
            ax[0].pie(
                x=df_season["weathersit"].value_counts(normalize=False).to_frame('perc').reset_index()["perc"],
                labels=df_season["weathersit"].unique(),
                textprops={'fontsize': 30},
                autopct='%1.2f%%',
                colors=colors,
                explode=(0.1, 0, 0.1)
            )

            ax[1].pie(
                x=df_season["day"].value_counts(normalize=False).to_frame('perc').reset_index()["perc"],
                labels=df_season["day"].unique(),
                textprops={'fontsize': 30},
                autopct='%1.2f%%',
                colors=colors,
                explode=(0.1, 0)
            )
            st.pyplot(fig)

            with st.expander("See explanation"):
                st.write(
                """Percentage of weather conditions, weekends and weekdays in 1 season""")


        

elif selected =="Report":
    st.title(selected)
    df_report_work= hr_m(df_all[df_all["workingday_x"]==1])
    df_report_nwork= hr_m(df_all[df_all["workingday_x"]==0])

    df_report = hr(df_all)
    df_report["day"] = df_report["day"].apply(working_day)
    df_report["weathersit"] = df_report["weathersit"].apply(weath)


    st.header("Rent by Month")
    with st.container(border=True):
        fig, ax = plt.subplots(figsize=(45, 10))
        ax.plot(df_report_work["dteday"], df_report_work["total_rent"], marker='o', linewidth=4.5, label="weekday")
        ax.plot(df_report_nwork["dteday"], df_report_nwork["total_rent"], marker='o', linewidth=4.5, label="weekend")
        plt.legend(fontsize=40)
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.legend(fontsize=35)
        ax.set_title("Total Rent", loc="center", fontsize=45)
        ax.tick_params(axis ='x', labelsize=40, rotation=45)
        ax.tick_params(axis ='y', labelsize=38)

        st.pyplot(fig)

        with st.expander("See explanation"):
                st.write(
           f"""- The highest total bicycle rentals on weekdays occurred in the 8th month of 2012, 
            namely {df_report_work["total_rent"].max()} and the smallest occurred in the 1st month of 2011, namely {df_report_work["total_rent"].min()}
            """
            )
                st.write(
           f"""- Total bicycle rentals on weekdays, Month 8 is the highest total bicycle rentals in each year, 
           namely 2011 and 2012 with the total number of rentals being {df_report_work["total_rent"].max()} 
           and {df_report_work[df_report_work["dteday"]=="2011-08"]["total_rent"].max()} respectively.
           Month 1 of 2011 and month 12 of 2012 are the times when the total number of bicycle rentals is the lowest per weekday 
           year with the total number of rentals being {df_report_work["total_rent"].min()} and {df_report_work[df_report_work["dteday"]=="2012-12"]["total_rent"].min()} respectively
            """
            )
                st.write(
            f"""- The highest total bicycle rentals on weekends occurred in the 9th month of 2012, 
            namely {df_report_nwork["total_rent"].max()} and the smallest occurred in the 1st month of 2011, namely {df_report_nwork["total_rent"].min()}
            """
            )
                st.write(
           f"""- The total bicycle rentals on weekends, Month 6 of 2011 and month 9 of 2012 were 
           the highest total bicycle rentals with the total number of rentals being {df_report_nwork[df_report_nwork["dteday"]=="2011-06"]["total_rent"].max()} and {df_report_nwork["total_rent"].max()} respectively. 
           Month 1 of 2011 and month 2 of 2012 were the times when the total number of bicycle rentals was 
           the lowest with the number The total rentals are {df_report_nwork["total_rent"].min()} and {df_report_nwork[df_report_nwork["dteday"]=="2012-02"]["total_rent"].min()} respectively

            """
            )
                
    st.header("Rent by Hours")
    with st.container(border=True):
        fig, ax = plt.subplots(figsize=(45, 10))
        ax.plot(df_report_work["dteday"], df_report_work["hour"], marker='o', linewidth=4.5, label="weekday")
        ax.plot(df_report_nwork["dteday"], df_report_nwork["hour"], marker='o', linewidth=4.5, label="weekend")
        plt.legend(fontsize=40)
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.legend(fontsize=35)
        ax.set_title("Time Rent", loc="center", fontsize=45)
        ax.tick_params(axis ='x', labelsize=40, rotation=45)
        ax.tick_params(axis ='y', labelsize=38)

        st.pyplot(fig)

        with st.expander("See explanation"):
                st.write(
           f"""- The highest number of bicycle rental times on weekdays in 2011 was in month 3 and the lowest was in month 1, 
           namely {df_report_work[df_report_work["dteday"]=="2011-03"]["hour"].max()} and {df_report_work[df_report_work["dteday"]=="2011-01"]["hour"].min()} respectively. Meanwhile in 2012, the longest number of rental times occurred 
           in month 8 and the shortest was in month 9, 
           namely respectively. {df_report_work[df_report_work["dteday"]=="2012-08"]["hour"].max()} and {df_report_work[df_report_work["dteday"]=="2012-09"]["hour"].min()} respectively.

            """
            )
                st.write(
           f"""- The highest number of bicycle rental times on weekends in 2011 was in month 7 and the lowest was in month 8, 
           namely {df_report_nwork[df_report_nwork["dteday"]=="2011-07"]["hour"].max()} and {df_report_work[df_report_work["dteday"]=="2011-08"]["hour"].min()}, respectively. Meanwhile, in 2012, 
           the longest number of rental times occurred in month 9 and the shortest was in month 8, 
           namely respectively. {df_report_work[df_report_work["dteday"]=="2012-09"]["hour"].max()} and {df_report_work[df_report_work["dteday"]=="2012-08"]["hour"].min()} respectively
            """
            )

    st.header("Rent by Season")
    def season_change_2(x):
        if x=="spinger":
            return "Springer"
        elif x=="summer":
            return "Summer"
        elif x=="fall":
            return "Fall"
        else:
            return "Winter"
    df_report["season"] = df_report["season"].apply(season_change_2)
    with st.container(border=True):
        fig, ax = plt.subplots(ncols=2, figsize=(45, 10))
        colors = ["#D3D3D3","#72BCD4"] 
        sns.barplot(data=df_report, x="season",y="total_rent", hue="day",palette=colors, errorbar=None, ax=ax[0])
        ax[0].set_ylabel(None)
        ax[0].set_xlabel(None)
        ax[0].legend(fontsize=35)
        ax[0].set_title("Weekend & Weekday", loc="center", fontsize=45)
        ax[0].tick_params(axis ='x', labelsize=40)
        ax[0].tick_params(axis ='y', labelsize=38)


        colors = ["#D3D3D3", "#72BCD4", "#D3D3D3"] 
        sns.barplot(data=df_report, x="season",y="total_rent", hue="weathersit", palette=colors,errorbar=None, ax=ax[1])
        ax[1].set_ylabel(None)
        ax[1].set_xlabel(None)
        ax[1].legend(fontsize=35)
        ax[1].set_title("Weathersit", loc="center", fontsize=45)
        ax[1].tick_params(axis ='x', labelsize=40)
        ax[1].tick_params(axis ='y', labelsize=38)

        st.pyplot(fig)

        with st.expander("See explanation"):
                st.write(
            """- The total bicycle rentals in the 4 seasons vary, 
            the total bicycle rentals in the summer season on weekends are smaller than on weekdays. 
            On the other hand, in seasons other than summer, the total rentals on weekdays are more than on weekends.
            """
            )
                st.write(
            """- In sunny weather, the total number of bicycle rentals is more than in other weather in each season.
            The lowest total bicycle rentals occur during Light Snow or Light Rain weather in each season and 
            the difference in total bicycle rentals in sunny weather and Light Snow or Light Rain is quite significant.
            """
            )


