import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. 데이터 로드 및 전처리 함수
# 'aaasd.csv' 파일을 직접 읽어오는 함수 (Streamlit Cloud에서 실행 가능하도록)
@st.cache_data
def load_and_preprocess_data():
    # 사용자가 제공한 파일의 스니펫을 기반으로 가상의 CSV 데이터 생성
    # 실제로는 이 부분을 Streamlit Cloud에 배포 시 파일 경로를 지정해야 함
    # 여기서는 예시로 파일 스니펫의 일부를 사용해 DataFrame을 생성합니다.
    # **중요:** 실제 Streamlit Cloud 배포 시에는 'aaasd.csv' 파일을 앱 폴더에 함께 업로드해야 합니다.
    
    # ---------------------------------------------------------------------------------
    # 파일 로드 (여기서는 예시를 위해 파일명을 직접 지정합니다. 실제 배포 시 동일 폴더에 있어야 합니다.)
    try:
        df = pd.read_csv("aaasd.csv", encoding='utf-8')
    except FileNotFoundError:
        st.error("⚠️ 'aaasd.csv' 파일을 찾을 수 없습니다. 파일을 'app.py'와 같은 폴더에 넣어주세요.")
        return None
    except Exception as e:
        st.error(f"⚠️ 파일 로드 중 오류가 발생했습니다: {e}")
        return None
    # ---------------------------------------------------------------------------------

    # 컬럼 이름 정리 (지역 코드 제거 및 '계' 인구만 필터링)
    # '행정구역' 컬럼에서 괄호 안의 지역 코드 제거
    df['행정구역'] = df['행정구역'].str.replace(r'\s+\(.*?\)', '', regex=True)

    # 계(총 인구) 데이터 컬럼만 선택
    base_cols = ['행정구역', '2025년10월_계_총인구수']
    age_cols = [col for col in df.columns if col.startswith('2025년10월_계_') and '~' in col]
    
    df_filtered = df[base_cols + age_cols].copy()
    
    # 수치 데이터 컬럼의 쉼표(,) 제거 및 정수형 변환
    numeric_cols = df_filtered.columns.drop('행정구역')
    for col in numeric_cols:
        if df_filtered[col].dtype == 'object':
            df_filtered[col] = df_filtered[col].str.replace(',', '').astype(float).astype('Int64')
        else:
            df_filtered[col] = df_filtered[col].astype('Int64')
            
    # '전국' 데이터는 선택지에서 제외 (분석의 편의를 위해)
    df_filtered = df_filtered[df_filtered['행정구역'] != '전국']
    
    # Wide-to-Long 형식으로 데이터 변환 (Plotly 시각화를 위해)
    df_long = pd.melt(
        df_filtered, 
        id_vars=['행정구역'],
        value_vars=age_cols,
        var_name='연령대',
        value_name='인구수'
    )
    
    # 연령대 컬럼 정제 (예: '2025년10월_계_0~9세' -> '0~9세')
    df_long['연령대'] = df_long['연령대'].str.replace('2025년10월_계_', '')

    return df_long

# 2. Plotly 그래프 생성 함수
def create_population_chart(df_data, selected_region):
    # 선택된 지역 데이터 필터링
    df_region = df_data[df_data['행정구역'] == selected_region]
    
    # 연령대 순서 정렬을 위한 카테고리 설정
    # 컬럼에서 추출한 순서대로 정렬
    age_order = df_region['연령대'].unique().tolist()
    
    # Plotly 꺾은선 그래프 생성
    fig = px.line(
        df_region,
        x='연령대',
        y='인구수',
        title=f"📈 {selected_region}의 연령별 인구 분포 (2025년 10월)",
        markers=True, # 꺾은선에 마커 표시
        text='인구수' # 데이터 포인트 위에 인구수 텍스트 표시
    )

    # 텍스트 포맷을 인구수에 맞게 조정
    fig.update_traces(texttemplate='%{text:,}', textposition='top center')
    
    # 레이아웃 커스터마이징
    fig.update_layout(
        xaxis_title="연령대",
        yaxis_title="인구수",
        hovermode="x unified",
        font=dict(family="Pretendard, sans-serif", size=12),
        margin=dict(l=20, r=20, t=50, b=20)
    )

    # X축 (연령대) 순서 강제 지정
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
    
    df_long = load_and_preprocess_data()
    
    if df_long is None:
        return # 데이터 로드 실패 시 종료

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
