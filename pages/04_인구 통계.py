import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 데이터 로드 및 전처리 함수 (인코딩 문제 해결)
@st.cache_data
def load_and_preprocess_data():
    file_path = "aaasd.csv"
    
    # **인코딩 문제 해결을 위해 여러 인코딩을 순차적으로 시도합니다.**
    encodings = ['utf-8', 'euc-kr', 'cp949']
    df = None
    
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            # st.success(f"✅ 파일을 '{encoding}' 인코딩으로 성공적으로 로드했습니다.")
            break
        except FileNotFoundError:
            st.error(f"⚠️ '{file_path}' 파일을 찾을 수 없습니다. 파일을 'app.py'와 같은 폴더에 넣어주세요.")
            return None
        except Exception:
            # 다음 인코딩 시도를 위해 오류를 무시하고 진행
            continue 

    if df is None:
        st.error("❌ 파일 로드에 실패했습니다. 'utf-8', 'euc-kr', 'cp949' 중 맞는 인코딩이 없거나 데이터에 문제가 있습니다.")
        return None
        
    # ------------------ 데이터 전처리 ------------------

    # 1. 컬럼 이름 정리 (지역 코드 제거 및 '계' 인구만 필터링)
    df['행정구역'] = df['행정구역'].astype(str).str.replace(r'\s+\(.*?\)', '', regex=True)

    # 계(총 인구) 데이터 컬럼만 선택 ('연령구간인구수'는 제외)
    base_cols = ['행정구역', '2025년10월_계_총인구수']
    age_cols_raw = [col for col in df.columns if col.startswith('2025년10월_계_') and '~' in col]
    
    df_filtered = df[base_cols + age_cols_raw].copy()
    
    # 2. 수치 데이터 타입 정리 (쉼표 제거 및 정수형 변환)
    numeric_cols = df_filtered.columns.drop('행정구역')
    for col in numeric_cols:
        # 데이터에 쉼표가 포함되어 object 타입일 경우 처리
        if df_filtered[col].dtype == 'object':
            # 쉼표와 따옴표 제거 후 숫자로 변환
            df_filtered[col] = df_filtered[col].astype(str).str.replace(r'[," ]', '', regex=True)
            df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce').astype('Int64')
        else:
            df_filtered[col] = df_filtered[col].astype('Int64')
            
    # '전국' 데이터는 선택지에서 제외 (분석의 편의를 위해)
    df_filtered = df_filtered[df_filtered['행정구역'] != '전국']
    
    # 3. Wide-to-Long 형식으로 데이터 변환 (Plotly 시각화를 위해)
    df_long = pd.melt(
        df_filtered, 
        id_vars=['행정구역'],
        value_vars=age_cols_raw,
        var_name='연령대',
        value_name='인구수'
    )
    
    # 4. 연령대 컬럼 정제 (예: '2025년10월_계_0~9세' -> '0~9세')
    df_long['연령대'] = df_long['연령대'].str.replace('2025년10월_계_', '')

    return df_long

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

# 3. Streamlit 메인 함수 (변화 없음)
def main():
    st.set_page_config(
        page_title="행정구역별 인구 분포 분석",
        layout="wide"
    )

    st.title("🗺️ 행정구역별 연령별 인구 분포 시각화")
    st.markdown("---")
    
    # 데이터 로드 시도
    df_long = load_and_preprocess_data()
    
    if df_long is None:
        return

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
