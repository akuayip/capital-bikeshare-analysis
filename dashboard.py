import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def create_bike_rentals_by_season(df):
    season_mapping = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
    }
    by_season_df = df.groupby(by="season").cnt.sum().sort_values(ascending=False).reset_index()
    by_season_df['season'] = by_season_df['season'].map(season_mapping)
    by_season_df.rename(columns={
        "cnt": "rental_count"
    }, inplace=True)
    return by_season_df

def create_bike_rentals_by_weathersit(df):
    weathersit_mapping = {
    1: 'Clear/Partly Cloudy',
    2: 'Mist/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Heavy Rain/Snow'
    }
    by_weathersit_df = all_df.groupby(by="weathersit").cnt.sum().sort_values(ascending=False).reset_index()
    by_weathersit_df['weathersit'] = by_weathersit_df['weathersit'].map(weathersit_mapping)
    by_weathersit_df.rename(columns={
        "cnt": "rental_count"
    }, inplace=True)
    return by_weathersit_df

def create_bike_rentals_by_weekday(df):
    weekday_mapping = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
    }
    by_weekday_df = hour_df.groupby(by="weekday")['cnt'].sum().sort_values(ascending=False).reset_index()
    by_weekday_df['weekday'] = by_weekday_df['weekday'].map(weekday_mapping)
    by_weekday_df.rename(columns={
        "cnt": "rental_count"
    }, inplace=True)
    return by_weekday_df

def create_bike_rentals_by_year(df):
    yr_mapping = {
    0: "2011",
    1: "2012"
    }
    by_year_df = all_df.groupby(by="yr").cnt.sum().sort_values(ascending=False).reset_index()
    by_year_df['yr'] = by_year_df['yr'].map(yr_mapping)
    by_year_df.rename(columns={
        "cnt": "rental_count"
    }, inplace=True)
    return by_year_df

def create_yearly_perfome_rentals(df):
    year_all_df = all_df.resample(rule='M', on='dteday').agg({
        "cnt": "sum"
    }).reset_index()
    
    year_all_df['year'] = year_all_df['dteday'].dt.year
    year_all_df['month'] = year_all_df['dteday'].dt.strftime('%B')
    year_all_df.rename(columns={
        "cnt": "total_rental"  # Menghitung total penyewaan
    }, inplace=True)

    data_2011 = year_all_df[year_all_df['year'] == 2011]
    data_2012 = year_all_df[year_all_df['year'] == 2012]

    return data_2011, data_2012

def create_cluster_rentals(df):
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    all_df['season_cluster'] = all_df['season'].map(season_mapping)

    weathersit_mapping = {
        1: 'Clear/Partly Cloudy',
        2: 'Mist/Cloudy',
        3: 'Light Snow/Rain',
        4: 'Heavy Rain/Snow'
    }
    all_df['weathersit_cluster'] = all_df['weathersit'].map(weathersit_mapping)

    clustering_summary = all_df.groupby(['season_cluster', 'weathersit_cluster']).agg({
        'cnt': 'mean',  # Rata-rata jumlah penyewaan
        'temp': 'mean',  # Rata-rata suhu
        'hum': 'mean',   # Rata-rata kelembapan
        'windspeed': 'mean'  # Rata-rata kecepatan angin
    }).reset_index()
    return clustering_summary

# Load cleaned data
day_df = pd.read_csv("day_data.csv")
hour_df = pd.read_csv("hour_data.csv")
all_df = pd.read_csv("all_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("capitalbike.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

# st.dataframe(main_df)
bike_rentals_by_season_df = create_bike_rentals_by_season(main_df)
bike_rentals_by_weathersit_df = create_bike_rentals_by_weathersit(main_df)
bike_rentals_by_weekday_df = create_bike_rentals_by_weekday(main_df)
bike_rentals_by_year_df = create_bike_rentals_by_year(main_df)
data_2011, data_2012 = create_yearly_perfome_rentals(main_df)
clustering_summary = create_cluster_rentals(main_df)

# CAPITAL BIKESHARE DASHBOARD
st.image("capitalbikeshare.jpg")
st.header('Capital Bikeshare Dashboard :sparkles:')
with st.expander("Abuout us"):
    st.write(
        """The Capital Bikeshare Dashboard is a visual interface designed to present 
        data and insights related to the operations of the "Capital Bikeshare" bike-sharing system. 
        This dashboard presents various statistics related to Capital Bikeshare.
        Its primary purpose is to facilitate data-driven decision-making and 
        enhance the user experience when accessing bike-sharing services.  
        """
    )

# All Record
st.subheader('Records 👇🏻')
col1, col2 = st.columns(2)

with col1:
    total_record = day_df.instant.nunique()
    st.metric("Total Record", value=total_record)

with col2:
    total_rent = day_df.cnt.sum()
    st.metric("Total rent bikes", value=total_rent)

# visual for bike by_season
st.subheader('The Most Popular Season for Bike Rentals')
col1, col2 = st.columns(2)

with col1:
    most_popular_season = bike_rentals_by_season_df.iloc[0]
    season = most_popular_season['season']
    st.metric("Season", value=season)

with col2:
    total_rentals = most_popular_season['rental_count']
    st.metric("Total rentals", value=f"{total_rentals:,}")
    
plt.figure(figsize=(10, 5))
bars = plt.bar(bike_rentals_by_season_df['season'], bike_rentals_by_season_df['rental_count'], color='skyblue')
plt.title('Bike Rentals by Season', fontsize=16)
plt.xlabel('Season', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
st.pyplot(plt)

with st.expander("See Explanation"):
    st.markdown(
        """
        - Musim dengan Penyewaan Sepeda Terbanyak:Penyewaan sepeda paling tinggi terjadi pada musim gugur (Fall), dengan total penyewaan sebanyak 1.061.129.
        - Musim dengan Penyewaan Sepeda Tersedikit:Penyewaan sepeda paling rendah terjadi pada musim semi (Spring), dengan total penyewaan sebanyak 471.348.
        """
    )


# Demografi
# visual for bike by_weathersi
st.subheader('Bike Rental Demographics')
col1, col2 = st.columns(2)

with col1:
    plt.figure(figsize=(8,5))
    bars = plt.bar(bike_rentals_by_weathersit_df['weathersit'], bike_rentals_by_weathersit_df['rental_count'], color='skyblue')
    plt.title('Bike Rentals by Weather Condition', fontsize=16)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    st.pyplot(plt)

with col2:
    plt.figure(figsize=(8,5))
    bars = plt.bar(bike_rentals_by_year_df['yr'], bike_rentals_by_year_df['rental_count'], color='skyblue')
    plt.title('Bike Rentals on Years', fontsize=16)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    st.pyplot(plt)

# visual for bike by_weathersit
plt.figure(figsize=(10, 5))
bars = plt.bar(bike_rentals_by_weekday_df['weekday'], bike_rentals_by_weekday_df['rental_count'], color='skyblue')
plt.title('Bike Rentals by Weekday Condition',fontsize=16)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
st.pyplot(plt)

with st.expander("See Explanation"):
    st.markdown(
    """
    ### Grafik 1: Bike Rentals by Weather Condition
    - **Penyewaan sepeda paling banyak** terjadi pada kondisi cuaca Cerah dengan total **2.257.952**.
    - Penyewaan menurun secara signifikan pada kondisi cuaca **Berawan (996.858)** dan sangat rendah pada **Salju ringan (37.869)**.
    
    ### Grafik 2 Bike Rentals on Years
    - Penyewaan sepeda meningkat secara signifikan pada tahun **2012** dibandingkan tahun **2011**.
    - Dengan jumlah **2.049.576** di tahun **2012** dan **1.243.103** di tahun **2011**.

    ### Grafik 3: Bike Rentals by Weekday Condition 
    - Penyewaan sepeda cukup merata sepanjang minggu, dengan jumlah tertinggi pada **hari Sabtu (487.790)** dan terendah pada **hari Senin (444.027)**.
    """
)

#visual for perfome bike rentals of year
st.subheader('Rental Performance 2011 vs 2012')
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

axs[0].plot(data_2011["month"], data_2011["total_rental"], marker='o', linewidth=2, color="blue")
axs[0].set_title("Number of Rentals in 2011", fontsize=16)
axs[0].grid(True, linestyle='--', alpha=0.7)
axs[0].set_xticks(data_2011["month"])
axs[0].set_xticklabels(data_2011["month"], rotation=45, fontsize=10)
axs[0].set_ylim(0)

axs[1].plot(data_2012["month"], data_2012["total_rental"], marker='o', linewidth=2, color="green")
axs[1].set_title("Number of Rentals in 2012", fontsize=16)
axs[1].grid(True, linestyle='--', alpha=0.7)
axs[1].set_xticks(data_2012["month"])
axs[1].set_xticklabels(data_2012["month"], rotation=45, fontsize=10)
axs[1].set_ylim(0)

plt.tight_layout()
st.pyplot(fig)

with st.expander("See Explanation"):
    st.markdown(
        """
        - Penyewaan sepeda menunjukkan tren musiman yang kuat, dengan performa terbaik terjadi pada musim semi dan awal musim panas.
        - Tahun 2012 menunjukkan pertumbuhan signifikan dalam performa penyewaan dibandingkan tahun 2011, mencerminkan peningkatan popularitas atau penggunaan layanan penyewaan sepeda.
        - Namun, penyewaan menurun drastis selama musim dingin, menunjukkan bahwa cuaca memiliki dampak besar terhadap performa penyewaan.
        """
    )
    
#clustering
st.subheader('Bie Rtal Ptterns')
plt.figure(figsize=(12, 6))
palette = sns.color_palette("coolwarm", n_colors=len(clustering_summary['weathersit_cluster'].unique()))

sns.barplot(
    data=clustering_summary,
    x='season_cluster',
    y='cnt',
    hue='weathersit_cluster',
    palette=palette
)

plt.title('Average Bike Rentals by Season and Weather Condition', fontsize=18, fontweight='bold')
plt.xlabel('Season', fontsize=14)
plt.ylabel('Average Rentals', fontsize=14)

plt.legend(
    title='Weather Condition',
    title_fontsize=12,
    fontsize=10,
    loc='upper left',
    bbox_to_anchor=(1, 1)
)
plt.xlabel('')
plt.ylabel('')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(plt)

with st.expander("See Explanation"):
    st.markdown(
        """
        - **Penyewaan sepeda mencapai rata-rata tertinggi** pada musim Fall dengan kondisi cuaca Clear/Partly Cloudy.
        - **Rata-rata penyewaan sepeda terendah** terjadi pada musim Spring dengan kondisi cuaca Heavy Rain/Snow.
        """
    )

st.caption('Copyright © Repesented by M. Arief Rahman Hakim (Dicoding2024)')