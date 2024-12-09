import pandas as pd
from sklearn.cluster import KMeans
from geopy.distance import geodesic
from scipy.spatial import distance
import folium
import os
current_directory = os.getcwd()
print(current_directory)
new_directory = os.path.join(current_directory, 'testing', 'AI1208')
print(new_directory)


# Step 1: 加載數據
station_data = pd.read_csv("Taipei.csv")  # 替換為您的站點數據檔案
registration_data = pd.read_csv("______0____________.csv")  # 替換為您的登記數據檔案

# Step 2: 計算現有站點間的距離，建議刪除站點
removal_candidates = []
threshold_km_removal = 0.5  # 距離閾值：500米
for i, station1 in station_data.iterrows():
    for j, station2 in station_data.iterrows():
        if i != j:
            dist_km = geodesic((station1['lat'], station1['lon']), (station2['lat'], station2['lon'])).kilometers
            if dist_km < threshold_km_removal:
                removal_candidates.append({
                    'Station A': station1['sitename'],
                    'Station B': station2['sitename'],
                    'Distance (km)': dist_km
                })
removal_df = pd.DataFrame(removal_candidates).drop_duplicates()
removal_stations = removal_df['Station A'].unique()

# Step 3: 聚類分析，建議新增站點
latest_period = registration_data['Statistical Period'].max()
latest_registration = registration_data[registration_data['Statistical Period'] == latest_period]
latest_registration = latest_registration.iloc[:, 1:]  # 排除時間列

# 匯總行政區登記數量
district_totals = latest_registration.sum().reset_index()
district_totals.columns = ['District', 'Registration Count']
station_data['dist'] = station_data['dist'].str.strip()
district_totals['District'] = district_totals['District'].str.replace('_新增數量', '').str.strip()
district_coords = station_data.groupby('dist').agg({'lat': 'mean', 'lon': 'mean'}).reset_index()
district_data = pd.merge(district_coords, district_totals, left_on='dist', right_on='District', how='inner')

# K-Means 聚類
n_clusters = 5
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
district_data['Cluster'] = kmeans.fit_predict(district_data[['lat', 'lon']])
centroids = kmeans.cluster_centers_

# 未覆蓋區域分析
uncovered_centroids = []
threshold_km_addition = 2.0  # 距離閾值：2公里
for idx, centroid in enumerate(centroids):
    distances = distance.cdist([centroid], station_data[['lat', 'lon']].values, metric='euclidean')
    min_distance = distances.min() * 111
    if min_distance > threshold_km_addition:
        uncovered_centroids.append((idx, centroid[0], centroid[1], min_distance))

# Step 4: 在地圖上可視化
map_center = [station_data['lat'].mean(), station_data['lon'].mean()]
combined_map = folium.Map(location=map_center, zoom_start=12)

# 現有站點（藍色）
for _, station in station_data.iterrows():
    folium.Marker(
        location=[station['lat'], station['lon']],
        popup=f"現有站點: {station['sitename']}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(combined_map)

# 建議刪除站點（紅色）
for _, row in removal_df.iterrows():
    station_a = station_data[station_data['sitename'] == row['Station A']].iloc[0]
    folium.Marker(
        location=[station_a['lat'], station_a['lon']],
        popup=f"建議刪除: {row['Station A']}，與 {row['Station B']} 距離: {row['Distance (km)']:.2f} 公里",
        icon=folium.Icon(color='red', icon='remove')
    ).add_to(combined_map)

# 建議新增站點（黃色）
for idx, (cluster_id, lat, lon, dist) in enumerate(uncovered_centroids):
    folium.Marker(
        location=[lat, lon],
        popup=f"建議新增站點 (群組: {cluster_id}, 距離最近站點: {dist:.2f} 公里)",
        icon=folium.Icon(color='yellow', icon='plus')
    ).add_to(combined_map)

# 保存地圖
map_file_path = r"C:\Users\user\Documents\1204"
combined_map.save(map_file_path)

print(f"地圖已保存至 {map_file_path}")
