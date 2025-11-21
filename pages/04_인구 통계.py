import streamlit as st
import pandas as pd
import plotly.express as px
import pathlib 
import os # 파일 목록 확인을 위한 라이브러리 추가

# 1. 데이터 로드 및 전처리 함수 (변화 없음)
@st.cache_data
def load_and_preprocess_data():
    file_path = pathlib.Path("aaasd.csv")
    
    if not file_path.exists():
        return "FILE_NOT_FOUND" 
    
    encodings = ['utf-8', 'euc-kr', 'cp949', 'latin1']
    df = None
    successful_encoding = None

    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            successful_encoding = encoding
            break
        except Exception:
            continue 

    if df is None:
        return "ENCODING_FAILURE"
        
    # ------------------ 데이터 전처리 ------------------

    df['행정구역'] = df['행정구역'].astype(str).str.replace(r'\s+\(.*?\)', '', regex=True)

    base_cols = ['행정구역', '2025년10월_계_총인구수']
    age_cols = [col for col in df.columns if col.startswith('2025년10월_계_') and '~' in col and '연령구간인구수' not in col]
    
    df_filtered = df[base_cols + age_cols].copy()
    
    numeric_cols = df_filtered.columns.drop('행정구역')
    for col in numeric_cols:
        if df_filtered[col].dtype == 'object':
            df_filtered[col] = df_filtered[col].astype(str).str.replace(r'[," ]', '', regex=True)
            df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce').astype('Int64')
        else:
            df_filtered[col] = df_filtered[col].astype('Int64')
            
    df_filtered.dropna(inplace=True) 

    df_filtered = df_filtered[df_filtered['행정구역'] != '전국']
    
    df_long = pd.melt(
        df_filtered, 
        id_vars=['행정구역'],
        value_vars=age_cols, 
        var_name='연령대',
        value_name='인구수'
    )
    
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
    
    # ------------------- ✨ 진단 코드: 파일 리스트 출력 ✨ -------------------
    st.sidebar.subheader("📄 File Path 진단")
    try:
        # 서버가 현재 디렉토리에서 인식하는 파일 목록 출력
        current_files = os.listdir(pathlib.Path.cwd())
        st.sidebar.info(f"**현재 폴더 파일:** {', '.join(current_files)}")
    except Exception as e:
        st.sidebar.error(f"Failed to list files: {e}")
    st.sidebar.markdown("---")
    # -------------------------------------------------------------------------
    
    # 데이터 로드 시도 및 오류 진단
    data_result = load_and_preprocess_data()
    
    if data_result == "FILE_NOT_FOUND":
        st.error("❌ 데이터 로드 실패: 'aaasd.csv' 파일을 찾을 수 없습니다.")
        st.info("💡 **진단:** 사이드바에 출력된 **'현재 폴더 파일'** 목록을 확인해 주십시오. 목록에 `aaasd.csv`가 없다면 GitHub 커밋/푸시가 누락되었거나, 파일명이 틀린 것입니다.")
        return
        
    if data_result == "ENCODING_FAILURE":
        st.error("❌ 데이터 로드 실패: 지원되는 인코딩으로 파일을 읽을 수 없습니다.")
        st.info("💡 **진단:** 파일 인코딩 문제이거나, 데이터 자체가 손상되었을 수 있습니다.")
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
