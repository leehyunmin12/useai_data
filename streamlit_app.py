import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import requests
from io import StringIO
from datetime import datetime, timedelta

# 폰트 설정 (Codespaces 환경에서 Pretendard 폰트가 없으면 기본 폰트로 대체)
# API 호출 실패 시 예시 데이터로 대체
example_data = {
    'date': pd.to_datetime(pd.date_range(start='1950-01-01', periods=100, freq='Y')),
    'value': [0.1, 0.2, 0.15, 0.3, 0.4, 0.35, 0.5, 0.6, 0.7, 0.8, 0.75, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9.0, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9]
}
try:
    plt.rc('font', family='Pretendard')
    st.markdown("""
        <style>
        @font-face {
            font-family: 'Pretendard';
            src: url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.6/dist/web/static/woff2/Pretendard-Bold.woff2') format('woff2');
            font-weight: 700;
            font-style: normal;
        }
        body {
            font-family: 'Pretendard', sans-serif;
        }
        </style>
    """, unsafe_allow_html=True)
except:
    pass

# --- 1. 공개 데이터 대시보드 ---
st.title('🧊 빙하 해빙과 기후 변화 데이터 대시보드')
st.markdown("이 대시보드는 **NOAA 공식 데이터**를 사용하여 기후 변화의 심각성을 시각적으로 보여줍니다.")

@st.cache_data(ttl=3600)
def load_noaa_data():
    """NOAA 글로벌 기온 데이터셋을 불러오고 전처리합니다."""
    # 출처: NOAA Global Time Series (https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/land_ocean/all/1/1850-2023.csv)
    url = "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/land_ocean/all/1/1850-2023.csv"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # HTTP 에러 발생 시 예외 처리
        csv_data = StringIO(response.text)
        
        # 데이터 전처리
        df = pd.read_csv(csv_data, skiprows=4)
        df.columns = ['date', 'value']
        df['date'] = pd.to_datetime(df['date'], format='%Y%m')
        df['value'] = df['value'] / 100 # 단위 변환
        df = df[df['date'] <= datetime.now().date()] # 미래 데이터 제거
        return df
    except requests.exceptions.RequestException:
        st.error("⚠️ NOAA 데이터 로딩에 실패했습니다. 예시 데이터로 대체합니다.")
        # API 호출 실패 시 예시 데이터로 대체
        example_data = {
            'date': pd.to_datetime(pd.date_range(start='1950-01-01', periods=100, freq='Y')),
            'value': [0.1, 0.2, 0.15, 0.3, 0.4, 0.35, 0.5, 0.6, 0.7, 0.8, 0.75, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9.0]
        }
        df_example = pd.DataFrame(example_data)
        return df_example

# 데이터 불러오기
df_noaa = load_noaa_data()

# 사이드바 설정
st.sidebar.header('대시보드 설정')
start_year, end_year = st.sidebar.slider(
    '기간 필터',
    min_value=int(df_noaa['date'].dt.year.min()),
    max_value=int(df_noaa['date'].dt.year.max()),
    value=(int(df_noaa['date'].dt.year.min()), int(df_noaa['date'].dt.year.max()))
)
df_filtered = df_noaa[(df_noaa['date'].dt.year >= start_year) & (df_noaa['date'].dt.year <= end_year)]

# 꺾은선 그래프 (Plotly)
st.subheader('🌎 전지구 평균 기온 변화')
st.markdown("지구의 육지와 해양 평균 기온 변화를 꺾은선 그래프로 보여줍니다. (1950년 기준)")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_filtered['date'], y=df_filtered['value'], mode='lines', name='기온 편차'))
fig.update_layout(
    title='지구 평균 기온 변화 (1950년 대비 ℃)',
    xaxis_title='연도',
    yaxis_title='기온 편차 (℃)',
    font=dict(family="Pretendard", size=12)
)
st.plotly_chart(fig, use_container_width=True)

# 다운로드 버튼
st.download_button(
    label="전처리된 데이터 다운로드 (CSV)",
    data=df_filtered.to_csv(index=False).encode('utf-8'),
    file_name='noaa_global_temperature.csv',
    mime='text/csv'
)

# --- 2. 사용자 입력 데이터 대시보드 ---
st.markdown("---")
st.title('🧠 빙하 바이러스와 청소년의 마음 건강')
st.markdown("미림마이스터고 1학년 학생 대상 가상 데이터 분석 결과입니다.")

# 2-1. 폭염일수와 정신 건강 상관관계 (꺾은선/막대 그래프)
st.subheader('📈 폭염과 청소년의 마음 건강 상관관계')
# 가상 데이터
data_user = {
    '연도': list(range(2018, 2024)),
    '전국_폭염일수': [18, 15, 20, 25, 22, 28],
    '학생_불안감_지수': [40, 35, 50, 65, 55, 75]
}
df_user = pd.DataFrame(data_user)
df_user['연도'] = pd.to_datetime(df_user['연도'], format='%Y')

st.markdown("지난 5년간 **폭염일수**와 **학생 불안감 지수**의 변화를 비교합니다.")
fig_user = go.Figure()
fig_user.add_trace(go.Scatter(x=df_user['연도'], y=df_user['전국_폭염일수'], mode='lines+markers', name='전국 폭염일수', yaxis='y1'))
fig_user.add_trace(go.Scatter(x=df_user['연도'], y=df_user['학생_불안감_지수'], mode='lines+markers', name='학생 불안감 지수', yaxis='y2'))
fig_user.update_layout(
    xaxis=dict(title='연도'),
    yaxis=dict(title='폭염일수 (일)', side='left', showgrid=False),
    yaxis2=dict(title='학생 불안감 지수', side='right', overlaying='y', showgrid=False),
    title='폭염일수와 학생 불안감 지수 변화',
    font=dict(family="Pretendard", size=12)
)
st.plotly_chart(fig_user, use_container_width=True)


# 2-2. 지역별 폭염일수 (지도 시각화)
st.subheader('🗺️ 지역별 폭염일수와 심리적 영향')
st.markdown("2023년 기준 주요 도시의 폭염일수와 그로 인한 심리적 영향을 분석합니다.")
# 지도 시각화는 GeoJSON 파일이 필요해 코딩 초보에게는 복잡합니다.
# 대신 테이블과 Plotly bar 차트로 지역별 데이터를 보여줍니다.
data_map = {
    '지역': ['서울', '부산', '대구', '광주'],
    '폭염일수 (2023년)': [25, 28, 32, 29],
    '심리적_영향_설명': ['코로나19 경험으로 인한 높은 불안감', '복합적인 기후 위기(해수면+폭염)', '기록적 폭염으로 가장 높은 불안감', '폭염과 더불어 높은 습도로 인한 스트레스']
}
df_map = pd.DataFrame(data_map)

fig_bar = go.Figure(data=[go.Bar(x=df_map['지역'], y=df_map['폭염일수 (2023년)'])])
fig_bar.update_layout(
    title='2023년 주요 도시별 폭염일수',
    xaxis_title='지역',
    yaxis_title='폭염일수 (일)',
    font=dict(family="Pretendard", size=12)
)
st.plotly_chart(fig_bar, use_container_width=True)

with st.expander("📍 각 지역의 심리적 영향 더보기"):
    for index, row in df_map.iterrows():
        st.write(f"**{row['지역']}**: {row['심리적_영향_설명']}")

# CSV 다운로드
st.download_button(
    label="사용자 데이터 다운로드 (CSV)",
    data=df_user.to_csv(index=False).encode('utf-8'),
    file_name='student_anxiety_data.csv',
    mime='text/csv'
)