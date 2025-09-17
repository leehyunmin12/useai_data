import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import StringIO
import requests
import numpy as np

st.set_page_config(page_title="🌎 기후와 청소년 건강 & 빙하", layout="wide")

# =======================
# 전 세계 평균 기온 + 학생 불안감 데이터
# =======================
CSV_URL = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"

@st.cache_data(ttl=3600)
def load_global_temp_data():
    try:
        response = requests.get(CSV_URL, timeout=10)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text), skiprows=1)
        df = df.iloc[:-1, [0, -1]]
        df.columns = ['Year', 'Temperature']
        df['Year'] = pd.to_datetime(df['Year'], format='%Y')
        df['Temperature'] = df['Temperature'].astype(float)
        return df
    except Exception as e:
        st.error(f"⚠️ 데이터 로딩 실패: {e}")
        # 예시 데이터 생성
        df_example = pd.DataFrame({
            'Year': pd.date_range(start='1980-01-01', periods=44, freq='Y'),
            'Temperature': [i * 0.02 + 14 for i in range(44)]
        })
        return df_example

df_global = load_global_temp_data()

# 학생 불안감 지수 시뮬레이션 (1980~2023)
years = list(range(1980, 2024))
np.random.seed(42)
anxiety_index = np.clip(np.cumsum(np.random.randn(len(years)) * 0.8 + 0.5) + 30, 20, 80)

df_user = pd.DataFrame({
    '연도': pd.to_datetime(years, format='%Y'),
    '학생_불안감_지수': anxiety_index
})

# =======================
# 빙하 녹은 질량 + 바이러스 발생 지수 (시뮬레이션)
# =======================
glacier_mass_loss = np.cumsum(np.random.rand(len(years)) * 15)
virus_index = np.clip(np.cumsum(np.random.randn(len(years)) * 0.5 + 0.8) + 10, 5, 100)

df_glacier = pd.DataFrame({
    '연도': pd.to_datetime(years, format='%Y'),
    '녹은질량': glacier_mass_loss,
    '바이러스_발생지수': virus_index
})

# =======================
# 사이드바: 연도 범위 선택
# =======================
st.sidebar.header("연도 범위 선택")
start_year, end_year = st.sidebar.slider(
    "연도 선택",
    min_value=1980,
    max_value=2023,
    value=(1980, 2023)
)

df_global_filtered = df_global[
    (df_global['Year'].dt.year >= start_year) &
    (df_global['Year'].dt.year <= end_year)
]
df_user_filtered = df_user[
    (df_user['연도'].dt.year >= start_year) &
    (df_user['연도'].dt.year <= end_year)
]
df_glacier_filtered = df_glacier[
    (df_glacier['연도'].dt.year >= start_year) &
    (df_glacier['연도'].dt.year <= end_year)
]

# =======================
# 1. 위 그래프: 전 세계 평균 기온 + 학생 불안감 지수
# =======================
st.title("🌎 전 세계 평균 기온과 학생 불안감 지수 (1980~2023)")
st.markdown("전 세계 평균 기온과 학생 불안감 지수를 한눈에 비교하는 꺾은선 그래프입니다.")

fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=df_global_filtered['Year'],
    y=df_global_filtered['Temperature'],
    mode='lines+markers',
    name='전 세계 평균 기온 (°C)',
    line=dict(color='firebrick', width=3),
    marker=dict(size=6)
))
fig1.add_trace(go.Scatter(
    x=df_user_filtered['연도'],
    y=df_user_filtered['학생_불안감_지수'],
    mode='lines+markers',
    name='학생 불안감 지수',
    yaxis='y2',
    line=dict(color='blue', width=3),
    marker=dict(size=6)
))
fig1.update_layout(
    title="전 세계 평균 기온 vs 학생 불안감 지수",
    xaxis=dict(title="연도"),
    yaxis=dict(
        title="기온 편차 (°C)",
        tickfont=dict(color="firebrick")
    ),
    yaxis2=dict(
        title="학생 불안감 지수",
        tickfont=dict(color="blue"),
        overlaying='y',
        side='right'
    ),
    template="plotly_white",
    font=dict(family="Arial", size=12),
    hovermode="x unified"
)
st.plotly_chart(fig1, use_container_width=True)

# =======================
# 2. 아래 그래프: 빙하 녹은 질량 + 바이러스 발생 지수
# =======================
st.title("❄️ 빙하 녹은 질량과 바이러스 발생 지수")
st.markdown("빙하 녹은 질량과 바이러스 발생 지수를 한눈에 비교하는 꺾은선 그래프입니다.")

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=df_glacier_filtered['연도'],
    y=df_glacier_filtered['녹은질량'],
    mode='lines+markers',
    name='빙하 녹은 질량 (Gt)',
    line=dict(color='cyan', width=3),
    marker=dict(size=6)
))
fig2.add_trace(go.Scatter(
    x=df_glacier_filtered['연도'],
    y=df_glacier_filtered['바이러스_발생지수'],
    mode='lines+markers',
    name='바이러스 발생 지수',
    yaxis='y2',
    line=dict(color='red', width=3),
    marker=dict(size=6)
))
fig2.update_layout(
    title="빙하 녹은 질량 vs 바이러스 발생 지수",
    xaxis=dict(title="연도"),
    yaxis=dict(
        title="빙하 녹은 질량 (Gt)",
        tickfont=dict(color="cyan")
    ),
    yaxis2=dict(
        title="바이러스 발생 지수",
        tickfont=dict(color="red"),
        overlaying='y',
        side='right'
    ),
    template="plotly_white",
    font=dict(family="Arial", size=12),
    hovermode="x unified"
)
st.plotly_chart(fig2, use_container_width=True)
