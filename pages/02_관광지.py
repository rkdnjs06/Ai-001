# app.py
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Seoul Top10 for Foreign Visitors", layout="wide")

st.title("🏯 Seoul: Top 10 Attractions Favored by Foreign Visitors")
st.markdown(
    "지도에서 마커를 클릭하면 간단한 설명과 링크(공식 페이지 또는 참고 페이지)를 확인할 수 있습니다."
)

# Top10 장소 리스트 (이름, 위도, 경도, 간단 설명, 링크)
places = [
    {
        "name": "Gyeongbokgung Palace (경복궁)",
        "lat": 37.579617,
        "lon": 126.977041,
        "desc": "Joseon의 대표 궁궐. 수문장 교대식과 한복 체험으로 유명합니다.",
        "url": "https://english.visitkorea.or.kr"
    },
    {
        "name": "Changdeokgung Palace & Secret Garden (창덕궁·비원)",
        "lat": 37.5795,
        "lon": 126.9910,
        "desc": "유네스코 세계유산, 비원(비밀의 정원) 투어가 인기입니다.",
        "url": "https://english.visitkorea.or.kr"
    },
    {
        "name": "Bukchon Hanok Village (북촌한옥마을)",
        "lat": 37.5826,
        "lon": 126.9849,
        "desc": "전통 한옥이 보존된 마을로 사진 촬영과 산책 코스로 인기.",
        "url": "https://english.visitkorea.or.kr"
    },
    {
        "name": "Insadong (인사동)",
        "lat": 37.5740,
        "lon": 126.9820,
        "desc": "전통 공예, 찻집, 기념품 상점이 밀집한 문화거리.",
        "url": "https://english.visitkorea.or.kr"
    },
    {
        "name": "Myeongdong (명동)",
        "lat": 37.5609,
        "lon": 126.9855,
        "desc": "쇼핑과 길거리 음식의 메카. 화장품 샵과 패션 매장 다수.",
        "url": "https://www.tripadvisor.com/Tourism-g294197-Seoul-Vacations.html"
    },
    {
        "name": "N Seoul Tower / Namsan (N서울타워 / 남산)",
        "lat": 37.5512,
        "lon": 126.9882,
        "desc": "서울을 한눈에 볼 수 있는 전망 명소. 연인들의 '자물쇠' 문화로도 유명.",
        "url": "https://en.wikipedia.org/wiki/N_Seoul_Tower"
    },
    {
        "name": "Dongdaemun Design Plaza (DDP / 동대문디자인플라자)",
        "lat": 37.5663,
        "lon": 127.0090,
        "desc": "미래적 건축물, 전시와 야시장, 패션 거리 접근성 우수.",
        "url": "https://english.visitkorea.or.kr"
    },
    {
        "name": "Hongdae / Hongik Univ. area (홍대)",
        "lat": 37.5547,
        "lon": 126.9240,
        "desc": "젊음의 거리, 버스킹·카페·클럽·스트리트 아트가 활발한 지역.",
        "url": "https://www.lonelyplanet.com/south-korea/seoul/hongdae"
    },
    {
        "name": "Namdaemun Market (남대문시장)",
        "lat": 37.5596,
        "lon": 126.9770,
        "desc": "한국 최대의 전통 시장 중 하나로 다양한 상점과 길거리 음식이 있습니다.",
        "url": "https://english.visitkorea.or.kr"
    },
    {
        "name": "Hangang (Yeouido) Park / Han River (여의도 한강공원)",
        "lat": 37.5260,
        "lon": 126.9247,
        "desc": "한강공원은 피크닉, 자전거, 야경으로 유명합니다. 봄엔 벚꽃 명소.",
        "url": "https://english.visitkorea.or.kr"
    },
]

# 기본 지도 (서울 중심 좌표)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12, control_scale=True)

# 마커 추가
for p in places:
    html = f"""
    <h4>{p['name']}</h4>
    <p>{p['desc']}</p>
    <p><a href="{p['url']}" target="_blank">More info</a></p>
    """
    folium.Marker(
        location=[p["lat"], p["lon"]],
        popup=folium.Popup(html, max_width=300),
        tooltip=p["name"],
    ).add_to(m)

# 클러스터(원하면 활성화) - 아래 주석을 해제하면 사용 가능
# from folium.plugins import MarkerCluster
# mc = MarkerCluster().add_to(m)
# for p in places:
#     folium.Marker([p['lat'], p['lon']], popup=p['name']).add_to(mc)

st.sidebar.header("Settings")
show_map_type = st.sidebar.selectbox("Map tiles", options=["OpenStreetMap", "Stamen Terrain", "CartoDB positron"])
if show_map_type == "Stamen Terrain":
    m = folium.Map(location=[37.5665, 126.9780], tiles="Stamen Terrain", zoom_start=12)
elif show_map_type == "CartoDB positron":
    m = folium.Map(location=[37.5665, 126.9780], tiles="CartoDB positron", zoom_start=12)
else:
    m = folium.Map(location=[37.5665, 126.9780], tiles="OpenStreetMap", zoom_start=12)

# 다시 마커 추가 (선택된 타일 적용을 위해)
for p in places:
    html = f"""
    <h4>{p['name']}</h4>
    <p>{p['desc']}</p>
    <p><a href="{p['url']}" target="_blank">More info</a></p>
    """
    folium.Marker(
        location=[p["lat"], p["lon"]],
        popup=folium.Popup(html, max_width=300),
        tooltip=p["name"],
    ).add_to(m)

st.subheader("Interactive map (Folium)")
st.write("지도에서 마커를 클릭하면 상세 팝업이 뜹니다.")
# streamlit_folium 로 Folium 지도를 렌더
st_data = st_folium(m, width=1100, height=650)

st.markdown("---")
st.write("자료 출처: VisitKorea, TripAdvisor, Seoul Government 및 여행 가이드 종합.") 
