import streamlit as st
import pandas as pd
import plotly.express as px

# 앱 제목
st.title("📊 지역별 연령대 인구 꺾은선 그래프")
st.write("원하는 지역을 선택하면 나이별 인구 분포를 확인할 수 있어요!")

# CSV 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    try:
        # 인코딩 자동 감지
        try:
            df = pd.read_csv(uploaded_file, encoding="utf-8")
        except:
            df = pd.read_csv(uploaded_file, encoding="cp949")

        st.success("✅ 데이터가 성공적으로 업로드되었습니다!")

        # 데이터 미리보기
        st.subheader("📋 데이터 미리보기")
        st.dataframe(df.head())

        # 컬럼 이름 추정 (자동으로 감지)
        cols = df.columns.tolist()

        # 지역, 나이, 인구 컬럼 선택
        with st.expander("⚙️ 컬럼 설정 (필요시 조정)"):
            region_col = st.selectbox("지역(구)", cols, index=0)
            age_col = st.selectbox("나이", cols, index=1)
            pop_col = st.selectbox("인구수", cols, index=2)

        # 지역 선택
        regions = df[region_col].unique()
        selected_region = st.selectbox("지역을 선택하세요", sorted(regions))

        # 선택한 지역 데이터 필터링
        filtered_df = df[df[region_col] == selected_region]

        # 그래프 그리기
        fig = px.line(
            filtered_df,
            x=age_col,
            y=pop_col,
            title=f"📈 {selected_region} 지역의 나이별 인구 분포",
            markers=True,
            template="plotly_white"
        )

        fig.update_layout(
            xaxis_title="나이",
            yaxis_title="인구수",
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ 파일을 불러오는 중 오류 발생: {e}")

else:
    st.info("👆 먼저 CSV 파일을 업로드해주세요!")
