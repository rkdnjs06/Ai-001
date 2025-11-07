# streamlit_app.py


# 기본 검증
if 'Country' not in df.columns:
st.error("CSV에 'Country' 컬럼이 필요합니다.")
st.stop()


mbti_cols = [c for c in df.columns if c != 'Country']


# 국가 선택 UI
countries = df['Country'].astype(str).tolist()
selected = st.selectbox("국가 선택", countries)


row = df[df['Country'].astype(str) == selected]
if row.empty:
st.warning("선택한 국가 데이터가 없습니다.")
st.stop()


row = row.iloc[0]
values = row[mbti_cols].astype(float)


# 정렬 옵션
if sort_by_value:
order = values.sort_values(ascending=False)
types = order.index.tolist()
vals = order.values
else:
types = mbti_cols
vals = values[types].values


# 색상: 1등은 진한 빨강, 나머지는 그라데이션
colorscale = px.colors.sequential.OrRd # 그라데이션 팔레트
n_palette = len(colorscale)
# 정규화
vals_arr = np.array(vals, dtype=float)
minv, maxv = vals_arr.min(), vals_arr.max()
norm = (vals_arr - minv) / (maxv - minv + 1e-9)
colors = [colorscale[int(x * (n_palette - 1))] for x in norm]
# 1등 인덱스 찾기 (원래 정렬을 했다면 0)
idx_max = int(np.argmax(vals_arr))
# 1등을 선명한 빨강으로 지정
colors[idx_max] = '#d62728'


# 막대 그래프 그리기
if orientation == "수직 (기본)":
fig = go.Figure(go.Bar(x=types, y=vals, marker_color=colors, text=[f"{v:.2%}" for v in vals] if show_values else None, textposition='auto'))
fig.update_layout(title=f"{selected} — MBTI 비율", xaxis_title="MBTI 유형", yaxis_title="비율", yaxis_tickformat=',.0%')
else:
fig = go.Figure(go.Bar(x=vals, y=types, orientation='h', marker_color=colors, text=[f"{v:.2%}" for v in vals] if show_values else None, textposition='auto'))
fig.update_layout(title=f"{selected} — MBTI 비율", xaxis_title="비율", xaxis_tickformat=',.0%')


fig.update_traces(hovertemplate='%{x}<br>%{y}<extra></extra>' if orientation != "수평" else '%{x:.2%}<br>%{y}<extra></extra>')


st.plotly_chart(fig, use_container_width=True)


# 하단: 추가 정보
with st.expander("추가 통계/정보 보기"):
st.write(f"선택 국가: **{selected}**")
top_idx = np.argmax(vals_arr)
st.write(f"가장 높은 유형: **{types[top_idx]}** ({vals_arr[top_idx]:.2%})")
if show_raw:
show_df = df.set_index('Country').loc[[selected]][mbti_cols].T
show_df.columns = [selected]
st.dataframe(show_df.style.format('{:.4%}'))


st.caption("CSV 파일 경로: /mnt/data/countriesMBTI_16types.csv — Streamlit Cloud에선 repo 루트에 파일을 올려두세요.")


# 간단한 다운로드 버튼 (CSV가 업로드 된 경우)
if uploaded is not None:
st.download_button("업로드된 CSV 다운로드", data=uploaded, file_name="countriesMBTI_16types.csv")
