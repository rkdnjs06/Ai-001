import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Seoul Top 10 Attractions", layout="wide")
st.title("🌏 외국인들이 좋아하는 서울 관광지 TOP 10")

# 서울 인기 관광지 TOP10 (예시 좌표)
locations = [
    ("경복궁", 37.579617, 126.977041),
    ("명동", 37.563757, 126.985302),
    ("남산타워", 37.551169, 126.988227),
    ("홍대", 37.556332, 126.922651),
    ("동대문디자인플라자(DDP)", 37.566916, 127.009556),
    ("롯데월드타워", 37.513068, 127.102492),
    ("청계천", 37.569683, 126.978798),
    ("북촌한옥마을", 37.582604, 126.983998),
    ("이태원", 37.534507, 126.994027),
    ("광장시장", 37.570381, 127.000255)
]

# 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 마커 추가
for name, lat, lon in locations:
    folium.Marker(
        location=[lat, lon],
        popup=name,
        tooltip=name
    ).add_to(m)

# Streamlit에 지도 표시
st_folium(m, width=800, height=600)
