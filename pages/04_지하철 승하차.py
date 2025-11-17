import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime

# --- 1. 데이터 로드 및 전처리 ---
@st.cache_data
def load_data(file_path):
    """데이터를 로드하고 기본 전처리를 수행합니다."""
    try:
        # 한글 인코딩 문제 해결을 위해 euc-kr 시도
        df = pd.read_csv(file_path, encoding='euc-kr')
    except:
        # euc-kr 실패 시 cp949 시도
        df = pd.read_csv(file_path, encoding='cp949')

    # 컬럼 이름 조정 및 필요한 타입으로 변환
    df.columns = ['사용일자', '호선명', '역명', '승차총승객수', '하차총승객수']
    df['사용일자'] = df['사용일자'].astype(str)
    
    # 승차총승객수, 하차총승객수를 합산한 '총승객수' 컬럼 생성
    df['총승객수'] = df['승차총승객수'] + df['하차총승객수']
    
    return df

DATA_FILE = "sv.csv"
df = load_data(DATA_FILE)

# --- 2. Streamlit 앱 설정 ---
st.set_page_config(
    page_title="서울 지하철 이용객 상위 10개 역 분석",
    layout="wide"
)

st.title("🚇 지하철 이용객 상위 10개 역 분석 (2025년 10월)")
st.markdown("선택한 날짜와 호선에서 승차/하차 총 승객수가 가장 많은 **상위 10개 역**을 시각화합니다.")

# 데이터프레임에서 '사용일자' 컬럼의 고유값을 Date 객체로 변환하여 사용
df_dates = pd.to_datetime(df['사용일자'], format='%Y%m%d').dt.date
unique_dates = sorted(df_dates.unique())

# 2025년 10월 데이터만 필터링
df_oct = df[df['사용일자'].str.startswith('202510')].copy()
if df_oct.empty:
    st.error("데이터 파일에 2025년 10월 데이터가 없습니다.")
    st.stop()

# 2025년 10월의 유니크한 날짜 목록 (Date 객체)
oct_dates = sorted(pd.to_datetime(df_oct['사용일자'].unique(), format='%Y%m%d').tolist(), reverse=True)
if not oct_dates:
    st.error("2025년 10월의 유효한 날짜 데이터를 찾을 수 없습니다.")
    st.stop()

# --- 3. 사이드바 사용자 입력 ---
with st.sidebar:
    st.header("🔍 필터 설정")
    
    # 3-1. 날짜 선택 (2025년 10월 중)
    # oct_dates가 datetime 객체 리스트이므로, date 객체로 변환
    oct_date_only = [d.date() for d in oct_dates]
    
    selected_date = st.selectbox(
        "날짜를 선택하세요 (2025년 10월):",
        options=oct_date_only,
        index=0
    )
    
    # 선택된 날짜에 해당하는 호선 목록 추출
    date_str = selected_date.strftime('%Y%m%d')
    available_lines = sorted(df_oct[df_oct['사용일자'] == date_str]['호선명'].unique().tolist())
    
    # 3-2. 호선 선택
    selected_line = st.selectbox(
        "호선을 선택하세요:",
        options=['전체 호선'] + available_lines,
        index=0
    )

# --- 4. 데이터 필터링 및 계산 ---
filtered_df = df_oct[df_oct['사용일자'] == date_str].copy()

if selected_line != '전체 호선':
    filtered_df = filtered_df[filtered_df['호선명'] == selected_line].copy()

if filtered_df.empty:
    st.warning(f"선택하신 {selected_date} ({selected_line})의 데이터가 없습니다. 다른 날짜 또는 호선을 선택해주세요.")
else:
    # 역별 총 승객수 합산
    station_summary = filtered_df.groupby('역명')['총승객수'].sum().reset_index()
    
    # 상위 10개 역 추출
    top_10_stations = station_summary.nlargest(10, '총승객수').sort_values(by='총승객수', ascending=True)

    # --- 5. Plotly 그래프 생성 및 시각화 ---
    st.subheader(f"{selected_date} - {selected_line} : 총 승객수 상위 10개 역")

    # 5-1. 색상 그라데이션 설정
    num_bars = len(top_10_stations)
    if num_bars > 0:
        # 1등은 빨간색
        colors = ['#FF0000'] 
        
        # 2등부터 나머지 (파란색에서 흐려지는 그라데이션)
        # 2등은 진한 파란색, 마지막은 연한 파란색
        # 나머지 9개 (num_bars - 1)에 대한 색상 스케일 생성
        if num_bars > 1:
            blue_scale = px.colors.sample_colorscale('Blues', [i / (num_bars - 2) for i in range(num_bars - 1)], low=0.4, high=0.8)
            colors.extend(blue_scale[::-1]) # 뒤집어서 진한 파랑(2등) -> 연한 파랑(10등) 순서로 적용

        # 색상 리스트는 항상 [10등 색, 9등 색, ..., 2등 색, 1등 색] 순서로 적용됨 (막대그래프가 오름차순 정렬되어 있기 때문)
        # top_10_stations는 오름차순 정렬 (가장 작은 값(10등)이 먼저 나옴)
        
        # 5-2. Plotly Figure 생성
        fig = go.Figure(
            data=[go.Bar(
                x=top_10_stations['총승객수'],
                y=top_10_stations['역명'],
                orientation='h', # 수평 막대 그래프
                marker_color=colors[::-1], # 1등부터 10등 순서로 색상 적용하기 위해 리스트를 뒤집음
                text=top_10_stations['총승객수'].apply(lambda x: f'{x:,} 명'),
                textposition='outside',
            )]
        )

        # 5-3. 레이아웃 설정
        fig.update_layout(
            title_text='역별 총 승객수 (승차 + 하차)',
            xaxis_title="총 승객수 (명)",
            yaxis_title="역명",
            hovermode="y unified",
            height=600,
            uniformtext_minsize=8, 
            uniformtext_mode='hide'
        )

        # 5-4. 그래프 출력
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("데이터를 찾을 수 없습니다.")
