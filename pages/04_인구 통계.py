import streamlit as st
import pandas as pd
import plotly.express as px
import pathlib # 파일 경로 확인을 위한 라이브러리

# 1. 데이터 로드 및 전처리 함수 (파일 존재 및 인코딩 문제 해결 강화)
@st.cache_data
def load_and_preprocess_data():
    file_path = pathlib.Path("aaasd.csv")
    
    # 1. 파일 존재 여부 확인
    if not file_path.exists():
        # 파일이 없으면 명확한 메시지를 리턴하여 main 함수에서 출력
        return "FILE_NOT_FOUND" 
    
    # 2. 인코딩 시도: 가장 흔한 인코딩들을 순차적으로 시도합니다.
    encodings = ['utf-8', 'euc-kr', 'cp949', 'latin1']
    df = None
    successful_encoding = None

    for encoding in encodings:
        try:
            # 파일을 해당 인코딩으로 읽어오기 시도
            df = pd.read_csv(file_path, encoding=encoding)
            successful_encoding = encoding
            break
        except Exception:
            # 실패하면 다음 인코딩 시도
            continue 

    if df is None:
        # 모든 인코딩 시도 실패 시
        return "ENCODING_FAILURE"
        
    # ------------------ 데이터 전처리 ------------------

    # 1. 컬럼 이름 정리
    df['행정구역'] = df['행정구역'].astype(str).str.replace(r'\s+\(.*?\)', '', regex=True)

    # '계' 데이터 컬럼만 선택
    base_cols = ['행정구역', '2025년10월_계_총인구수']
    # 연령구간인구수 컬럼을 제외하고 '~'가 포함된 연령대 컬럼만 선택
    age_cols = [col for col in df.columns if col.startswith('2025년10월_계_') and '~' in col and '연령구간인구수' not in col]
    
    df_filtered = df[base_cols + age_cols].copy()
    
    # 2. 수치 데이터 타입 정리 (쉼표 제거 및 정수형 변환)
    numeric_cols = df_filtered.columns.drop('행정구역')
    for col in numeric_cols:
        if df_filtered[col].dtype == 'object':
            # 쉼표, 따옴표, 공백 제거 후 숫자로 변환 (변환 불가 시 NaN 처리)
            df_filtered[col] = df_filtered[col].astype(str).str.replace(r'[," ]', '', regex=True)
            df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce').astype('Int64')
        else:
            df_filtered[col] = df_filtered[col].astype('Int64')
            
    # 데이터 변환 중 발생한 결측치(NaN)가 포함된 행 삭제
    df_filtered.dropna(inplace=True) 

    # '전국' 데이터 제외
    df_filtered = df_filtered[df_filtered['행정구역'] != '전국']
    
    # 3. Wide-to-Long 형식으로 데이터 변환
    df_long = pd.melt(
        df_filtered, 
        id_vars=['행정구역'],
        value_vars=age_cols, 
        var_name='연령대',
        value_name='인구수'
    )
    
    # 4. 연령대 컬럼 정제
    df_long['연령대'] = df_long['연령대'].str.replace('2025년10월_계_', '')
    
    # 성공적으로 로드된 DataFrame과 성공 인코딩 정보를 튜플로 반환
    return (df_long, successful_encoding)

# 2. Plotly 그래프 생성 함수
def create_population_chart(df_data, selected_region):
    df_region = df_data[df_data['행정구역'] == selected_region]
    age_order = df_region['연령대'].unique().tolist()
    
    fig = px.line(
        df_region,
        x='연령대',
        y='인구수',
        title=f"📈 {selected_region}의 연령별 인구 분포 (2025년 10월)",
        markers=True,
        text='인구수'
    )

    fig.update_traces(texttemplate='%{text:,}', textposition='top center')
    
    fig.update_layout(
        xaxis_title="연령대",
        yaxis_title="인구수",
        hovermode="x unified",
        font=dict(family="Pretendard, sans-serif", size=12),
        margin=dict(l=20, r=20, t=50, b=20)
    )

    fig.update_xaxes(categoryorder='array', categoryarray=age_order)
    
    return fig

# 3. Streamlit 메인 함수
def main():
    st.set_page_config(
        page_title="행정구역별 인구 분포 분석",
        layout="wide"
    )

    st.title("🗺️ 행정구역별 연령별 인구 분포 시각화")
    st.markdown("---")
    
    # 데이터 로드 시도 및 오류 진단
    data_result = load_and_preprocess_data()
    
    if data_result == "FILE_NOT_FOUND":
        st.error("❌ 데이터 로드 실패: 'aaasd.csv' 파일을 찾을 수 없습니다.")
        st.info("💡 **진단:** Streamlit Cloud에서 파일 경로 인식이 실패했을 수 있습니다. 파일명이 **대소문자를 포함하여 정확히** `aaasd.csv` 인지, 그리고 `app.py`와 **같은 폴더**에 있는지 확인해 주세요.")
        return
        
    if data_result == "ENCODING_FAILURE":
        st.error("❌ 데이터 로드 실패: 지원되는 인코딩으로 파일을 읽을 수 없습니다.")
        st.info("💡 **진단:** `utf-8`, `euc-kr`, `cp949`, `latin1` 인코딩으로도 파일을 열 수 없습니다. 파일이 깨지지 않았는지 또는 특이한 인코딩을 사용하고 있는지 확인해 주세요.")
        return
    
    # 성공적으로 데이터를 로드한 경우
    df_long, successful_encoding = data_result
    
    # 사이드바에 성공 메시지 출력
    st.sidebar.success(f"데이터 로드 성공 (인코딩: {successful_encoding})")

    # 사이드바에 지역 선택 위젯 생성
    region_list = sorted(df_long['행정구역'].unique().tolist())
    selected_region = st.sidebar.selectbox(
        "🔎 **행정구역을 선택하세요**",
        region_list,
        index=
