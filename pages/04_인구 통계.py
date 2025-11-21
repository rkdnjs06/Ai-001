import streamlit as st
import pandas as pd
import plotly.express as px
import pathlib 

# 1. 데이터 로드 및 전처리 함수 (모든 파일명/인코딩 조합 시도)
@st.cache_data
def load_and_preprocess_data():
    
    # 1. 파일 이름 및 인코딩 조합 정의
    file_names_to_try = ["aaasd.csv", "AAASD.csv", "aaasd.CSV", "AAASD.CSV"]
    encodings = ['utf-8', 'euc-kr', 'cp949', 'latin1']
    
    df = None
    successful_encoding = None
    
    # 모든 가능한 파일 이름과 인코딩 조합을 시도합니다.
    for file_name in file_names_to_try:
        file_path = pathlib.Path(file_name)
        
        # 파일이 존재하는지 확인
        if not file_path.exists():
            continue # 다음 파일 이름 시도

        # 존재하는 파일에 대해 모든 인코딩 시도
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                successful_encoding = encoding
                
                # 성공 시, 즉시 중단
                break
            except Exception:
                continue # 다음 인코딩 시도
        
        # 인코딩 성공 시, 바깥 루프도 중단
        if df is not None:
            break

    # 파일 또는 인코딩 로드 실패 최종 판단
    if df is None:
        # 파일은 존재했으나 모든 인코딩 실패
        if pathlib.Path("aaasd.csv").exists() or pathlib.Path("AAASD.csv").exists():
             return "ENCODING_FAILURE"
        # 파일 자체가 존재하지 않음
        else:
             return "FILE_NOT_FOUND" 

    # ------------------ 데이터 전처리 ------------------

    # 1. 컬럼 이름 정리
    df['행정구역'] = df['행정구역'].astype(str).str.replace(r'\s+\(.*?\)', '', regex=True)

    base_cols = ['행정구역', '2025년10월_계_총인구수']
    age_cols = [col for col in df.columns if col.startswith('2025년10월_계_') and '~' in col and '연령구간인구수' not in col]
    
    df_filtered = df[base_cols + age_cols].copy()
    
    # 2. 수치 데이터 타입 정리 (쉼표 제거 및 정수형 변환)
    numeric_cols = df_filtered.columns.drop('행정구역')
    for col in numeric_cols:
        if df_filtered[col].dtype == 'object':
            df_filtered[col] = df_filtered[col].astype(str).str.replace(r'[," ]', '', regex=True)
            df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce').astype('Int64')
        else:
            df_filtered[col] = df_filtered[col].astype('Int64')
            
    df_filtered.dropna(inplace=True) 

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
    
    return (df_long, successful_encoding)

# 2. Plotly 그래프 생성 함수 (변화 없음)
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
    
    data_result = load_and_preprocess_data()
    
    if data_result == "FILE_NOT_FOUND":
        st.error("❌ 최종 데이터 로드 실패: 'aaasd.csv' 파일을 찾을 수 없습니다.")
        st.info("💡 **최종 진단:** `app.py`, `requirements.txt`, **그리고 `aaasd.csv`** 이 세 파일이 GitHub 저장소의 **같은 루트 폴더**에 있는지 **반드시** 확인하시고, **커밋 및 푸시**가 모두 완료되었는지 확인해 주십시오.")
        return
        
    if data_result == "ENCODING_FAILURE":
        st.error("❌ 최종 데이터 로드 실패: 지원되는 인코딩으로 파일을 읽을 수 없습니다.")
        st.info("💡 **최종 진단:** 파일명/경로는 찾았으나, 파일 자체의 데이터가 손상되었거나 파이썬/판다스에서 지원하지 않는 특수한 인코딩일 가능성이 높습니다.")
        return
    
    # 성공적으로 데이터를 로드한 경우
    df_long, successful_encoding = data_result
    
    st.sidebar.success(f"데이터 로드 성공 (인코딩: {successful_encoding})")

    # 사이드바에 지역 선택 위젯 생성
    region_list = sorted(df_long['행정구역'].unique().tolist())
    selected_region = st.sidebar.selectbox(
        "🔎 **행정구역을 선택하세요**",
        region_list,
        index=region_list.index('서울특별시') if '서울특별시' in region_list else 0
    )

    # 메인 화면에 설명 출력
    st.header(f"**선택 지역:** {selected_region}")
    st.write("선택하신 지역의 연령대별 인구수(남녀 합산)를 보여주는 꺾은선 그래프입니다.")
    
    # 그래프 생성 및 표시
    fig = create_population_chart(df_long, selected_region)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📊 데이터 정보")
    st.dataframe(df_long[df_long['행정구역'] == selected_region].rename(columns={'인구수': '인구수 (명)'}), use_container_width=True)
    st.caption("데이터 출처: 2025년 10월 기준 인구 통계 (가정)")


if __name__ == "__main__":
    main()
