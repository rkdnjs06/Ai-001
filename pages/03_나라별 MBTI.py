import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Countries MBTI Explorer", layout='wide')

st.title("🌍 Countries MBTI Explorer")
st.markdown("국가를 선택하면 해당 국가의 MBTI 비율을 대화형 막대그래프로 보여줍니다.")

# 기본 파일 경로 (Streamlit Cloud에선 repo 루트에 파일을 올려두세요)
DEFAULT_PATH = "countriesMBTI_16types.csv"

@st.cache_data
def load_data(path=None, uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv(path)
    df = df.rename(columns={c: c.strip() for c in df.columns})
    return df

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 설정")
    uploaded = st.file_uploader("CSV 파일 업로드 (선택)", type=["csv"]) 
    sort_by_value = st.checkbox("막대를 비율 내림차순 정렬", value=False)
    orientation = st.radio("막대 방향", ("수직 (기본)", "수평"))
    show_values = st.checkbox("수치 표시(막대 위)", value=True)
    show_raw = st.checkbox("원본 데이터 보기", value=False)

# 데이터 로드
try:
    df = load_data(DEFAULT_PATH, uploaded)
except Exception as e:
    st.error(f"데이터 로드에 실패했습니다: {e}")
    st.stop()

if 'Country' not in df.columns:
    st.error("CSV에 'Country' 컬럼이 필요합니다.")
    st.stop()

mbti_cols = [c for c in df.columns if c != 'Country']

# 국가 선택
countries = df['Country'].astype(str).tolist()
selected = st.selectbox("국가 선택", countries)

row = df[df['Country'].astype(str) == selected]
if row.empty:
    st.warning("선택한 국가 데이터가 없습니다.")
    st.stop()

row = row.iloc[0]
values = row[mbti_cols].astype(float)

# 정렬
if sort_by_value:
    order = values.sort_values(ascending=False)
    types = order.index.tolist()
    vals = order.values
else:
    types = mbti_cols
    vals = values[types].values

# 색상 설정: 1등은 빨강, 나머지는 그라데이션
colorscale = px.colors.sequential.OrRd
n_palette = len(colorscale)
vals_arr = np.array(vals, dtype=float)
minv, maxv = vals_arr.min(), vals_arr.max()
norm = (vals_arr - minv) / (maxv - minv + 1e-9)
colors = [colorscale[int(x * (n_palette - 1))] for x in norm]
idx_max = int(np.argmax(vals_arr))
colors[idx_max] = '#d62728'

# 막대그래프 그리기
if orientation == "수직 (기본)":
    fig = go.Figure(go.Bar(
        x=types, y=vals,
        marker_color=colors,
        text=[f"{v:.2%}" for v in vals] if show_values else None,
        textposition='auto'
    ))
    fig.update_layout(
        title=f"{selected} — MBTI 비율",
        xaxis_title="MBTI 유형",
        yaxis_title="비율",
        yaxis_tickformat=',.0%'
    )
else:
    fig = go.Figure(go.Bar(
        x=vals, y=types,
        orientation='h',
        marker_color=colors,
        text=[f"{v:.2%}" for v in vals] if show_values else None,
        textposition='auto'
    ))
    fig.update_layout(
        title=f"{selected} — MBTI 비율",
        xaxis_title="비율",
        xaxis_tickformat=',.0%'
    )

fig.update_traces(
    hovertemplate='%{x}<br>%{y}<extra></extra>' if orientation != "수평" else '%{x:.2%}<br>%{y}<extra></extra>'
)
st.plotly_chart(fig, use_container_width=True)

# 추가 정보
with st.expander("📊 추가 통계/정보 보기"):
    st.write(f"선택 국가: **{selected}**")
    top_idx = np.argmax(vals_arr)
    st.write(f"가장 높은 유형: **{types[top_idx]}** ({vals_arr[top_idx]:.2%})")
    if show_raw:
        show_df = df.set_index('Country').loc[[selected]][mbti_cols].T
        show_df.columns = [selected]
        st.dataframe(show_df.style.format('{:.4%}'))

# 다운로드 버튼
if uploaded is not None:
    st.download_button("업로드된 CSV 다운로드", data=uploaded, file_name="countriesMBTI_16types.csv")

st.caption("💡 CSV 파일은 Streamlit Cloud 리포지토리 루트에 넣으면 자동 인식됩니다.")
