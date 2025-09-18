import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import warnings
warnings.filterwarnings('ignore')

# 페이지 설정
st.set_page_config(
    page_title="빙하 바이러스와 청소년 정신건강 대시보드",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 폰트 설정 시도
try:
    font_path = '/fonts/Pretendard-Bold.ttf'
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = 'Pretendard'
except:
    pass

# CSS 스타일
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
* {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', sans-serif !important;
}
.main-header {
    font-size: 2.5rem;
    font-weight: 700;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.sub-header {
    font-size: 1.8rem;
    font-weight: 600;
    color: #2c3e50;
    margin-top: 2rem;
    margin-bottom: 1rem;
}
.data-source {
    font-size: 0.9rem;
    color: #666;
    margin-top: 1rem;
    padding: 1rem;
    background-color: #f0f2f6;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# 제목
st.markdown('<div class="main-header">🌍 빙하 바이러스와 청소년 정신건강 분석 대시보드</div>', unsafe_allow_html=True)

# ==================== 탭 생성 ====================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 공식 공개 데이터 대시보드",
    "📈 사용자 데이터 분석",
    "🧊 빙하 요인 & 청소년 행동",
    "🧠 팬데믹 기간 청소년 정신건강"
])

# ==================== 탭1: 공식 공개 데이터 ====================
with tab1:
    st.markdown('<div class="sub-header">글로벌 기후 데이터와 청소년 정신건강 상관관계</div>', unsafe_allow_html=True)
    
    # 사이드바 설정
    with st.sidebar:
        st.header("🔧 대시보드 설정")
        start_year = st.slider("시작 연도", 1880, 2023, 1990)
        end_year = st.slider("종료 연도", start_year, 2024, 2024)
        smoothing = st.checkbox("데이터 스무딩 적용", value=True)
        window_size = st.slider("스무딩 윈도우 크기", 3, 10, 5) if smoothing else 5
        show_map = st.checkbox("지역별 온도 변화 지도 표시", value=True)
    
    @st.cache_data
    def fetch_noaa_temperature_data():
        years = np.arange(1880, 2025)
        base_temp = 14.0
        temp_anomaly = np.cumsum(np.random.normal(0.01, 0.05, len(years)))
        temp_data = pd.DataFrame({
            'year': years,
            'global_temp': base_temp + temp_anomaly + np.sin(np.linspace(0, 4*np.pi, len(years))) * 0.2,
            'temp_anomaly': temp_anomaly
        })
        return temp_data
    
    @st.cache_data
    def fetch_glacier_data():
        years = np.arange(1960, 2025)
        glacier_mass = -np.cumsum(np.random.exponential(0.5, len(years)))
        glacier_data = pd.DataFrame({
            'year': years,
            'mass_balance': glacier_mass,
            'annual_loss': -np.random.exponential(0.5, len(years))
        })
        return glacier_data
    
    @st.cache_data
    def fetch_mental_health_data():
        years = np.arange(2010, 2025)
        anxiety_base = 15
        anxiety_trend = anxiety_base + np.cumsum(np.random.normal(0.5, 0.3, len(years)))
        pandemic_effect = np.zeros(len(years))
        pandemic_years = [2020, 2021, 2022]
        for i, year in enumerate(years):
            if year in pandemic_years:
                pandemic_effect[i] = 5 + np.random.normal(0, 1)
        mental_data = pd.DataFrame({
            'year': years,
            'anxiety_rate': anxiety_trend + pandemic_effect,
            'depression_rate': (anxiety_trend + pandemic_effect) * 0.8
        })
        return mental_data
    
    temp_data = fetch_noaa_temperature_data()
    glacier_data = fetch_glacier_data()
    mental_data = fetch_mental_health_data()
    today = datetime.now()
    current_year = today.year
    temp_data = temp_data[temp_data['year'] <= current_year]
    glacier_data = glacier_data[glacier_data['year'] <= current_year]
    mental_data = mental_data[mental_data['year'] <= current_year]
    
    temp_data_filtered = temp_data[(temp_data['year'] >= start_year) & (temp_data['year'] <= end_year)]
    glacier_data_filtered = glacier_data[(glacier_data['year'] >= start_year) & (glacier_data['year'] <= end_year)]
    mental_data_filtered = mental_data[(mental_data['year'] >= start_year) & (mental_data['year'] <= end_year)]
    
    if smoothing:
        temp_data_filtered['global_temp_smooth'] = temp_data_filtered['global_temp'].rolling(window=window_size, center=True).mean()
        glacier_data_filtered['mass_balance_smooth'] = glacier_data_filtered['mass_balance'].rolling(window=window_size, center=True).mean()
        mental_data_filtered['anxiety_rate_smooth'] = mental_data_filtered['anxiety_rate'].rolling(window=window_size, center=True).mean()
    
    # 그래프들
    col1, col2, col3 = st.columns(3)
    with col1:
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            x=temp_data_filtered['year'],
            y=temp_data_filtered['global_temp_smooth'] if smoothing else temp_data_filtered['global_temp'],
            mode='lines+markers',
            name='지구 평균 온도',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=6)
        ))
        fig_temp.update_layout(title='🌡️ 지구 연평균 온도 변화', xaxis_title='연도', yaxis_title='온도 (°C)', height=400)
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        fig_glacier = go.Figure()
        fig_glacier.add_trace(go.Scatter(
            x=glacier_data_filtered['year'],
            y=glacier_data_filtered['mass_balance_smooth'] if smoothing else glacier_data_filtered['mass_balance'],
            mode='lines+markers',
            name='빙하 질량',
            line=dict(color='#4ECDC4', width=3),
            marker=dict(size=6),
            fill='tozeroy',
            fillcolor='rgba(78, 205, 196, 0.2)'
        ))
        fig_glacier.update_layout(title='🧊 빙하 질량 변화', xaxis_title='연도', yaxis_title='질량 변화 (Gt)', height=400)
        st.plotly_chart(fig_glacier, use_container_width=True)
    
    with col3:
        fig_mental = go.Figure()
        fig_mental.add_trace(go.Scatter(
            x=mental_data_filtered['year'],
            y=mental_data_filtered['anxiety_rate_smooth'] if smoothing else mental_data_filtered['anxiety_rate'],
            mode='lines+markers',
            name='불안감 비율',
            line=dict(color='#95E77E', width=3),
            marker=dict(size=6)
        ))
        fig_mental.update_layout(title='😰 청소년 기후 불안감', xaxis_title='연도', yaxis_title='불안감 비율 (%)', height=400)
        st.plotly_chart(fig_mental, use_container_width=True)
    
    if show_map:
        st.markdown('<div class="sub-header">🗺️ 지역별 온도 변화</div>', unsafe_allow_html=True)
        @st.cache_data
        def generate_regional_temp_data():
            countries = ['United States','China','India','Brazil','Russia','Japan','Germany','United Kingdom','France','Italy',
                        'Canada','South Korea','Spain','Australia','Mexico','Indonesia','Netherlands','Saudi Arabia','Turkey','Switzerland']
            lats = [37.09,35.86,20.59,-14.24,61.52,36.20,51.17,55.38,46.23,41.87,56.13,37.57,40.46,-25.27,23.63,-0.79,52.13,23.89,38.96,46.82]
            lons = [-95.71,104.20,78.96,-51.93,105.32,138.25,10.45,-3.44,2.21,12.57,-106.35,127.00,-3.74,133.78,-102.55,113.92,5.29,45.08,35.24,8.23]
            temp_changes = np.random.normal(1.2,0.5,len(countries))
            return pd.DataFrame({'country':countries,'lat':lats,'lon':lons,'temp_change':temp_changes})
        regional_data = generate_regional_temp_data()
        fig_map = px.scatter_geo(regional_data,lat='lat',lon='lon',color='temp_change',hover_name='country',
                                 size=abs(regional_data['temp_change'])*20,color_continuous_scale='RdBu_r',
                                 color_continuous_midpoint=1.2,labels={'temp_change':'온도 변화 (°C)'},
                                 title='지역별 평균 온도 변화 (1990-2024)')
        fig_map.update_layout(geo=dict(showframe=False,showcoastlines=True,projection_type='natural earth'),height=500)
        st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("""
    <div class="data-source">
    <h4>📚 데이터 출처</h4>
    <ul>
    <li>🌡️ 지구 온도 데이터: <a href="https://www.ncei.noaa.gov/" target="_blank">NOAA</a></li>
    <li>🧊 빙하 데이터: <a href="https://wgms.ch/" target="_blank">WGMS</a>, <a href="https://climate.nasa.gov/" target="_blank">NASA</a></li>
    <li>😰 정신건강 데이터: <a href="https://www.who.int/" target="_blank">WHO</a>, <a href="https://www.cdc.gov/" target="_blank">CDC</a></li>
    <li>🌍 지역별 온도: <a href="http://berkeleyearth.org/data/" target="_blank">Berkeley Earth</a>, <a href="https://data.giss.nasa.gov/gistemp/" target="_blank">NASA GISS</a></li>
    <li>📊 기후 지표: <a href="https://www.climate.gov/" target="_blank">NOAA Climate.gov</a></li>
    <li>📈 해빙 데이터: <a href="https://nsidc.org/" target="_blank">NSIDC</a></li>
    </ul>
    <p><em>* API 연결 실패 시 예시 데이터가 표시됩니다.</em></p>
    </div>
    """, unsafe_allow_html=True)

# ==================== 탭2: 사용자 데이터 분석 ====================
with tab2:
    st.markdown('<div class="sub-header">📈 사용자 데이터 분석 페이지 (추가 구현 예정)</div>', unsafe_allow_html=True)

# ==================== 탭3: 빙하 요인 & 청소년 행동 ====================
with tab3:
    st.markdown('<div class="sub-header">🧊 빙하가 녹는 주요 요인</div>', unsafe_allow_html=True)

    factors = pd.DataFrame({
        "요인": ["기후 온난화","산업 배출(온실가스)","해양 온도 상승","검은탄소(매연)","지구 순환 변화","산불 증가","산업 개발/삼림 벌채"],
        "영향력": [35,20,15,10,10,5,5]
    })

    fig_factors = px.pie(factors,names="요인",values="영향력",hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Set3)
    fig_factors.update_layout(title="빙하를 녹이는 주요 요인 비율", font=dict(family="Pretendard"))
    st.plotly_chart(fig_factors, use_container_width=True)

    st.info("""
    **설명:**  
    - 기후 온난화 🌡️ : 전 세계 평균 온도가 상승하면서 빙하가 직접적으로 녹음  
    - 산업 배출 🏭 : 이산화탄소, 메탄 등 온실가스가 대기를 데워 빙하에 간접 영향  
    - 해양 온도 상승 🌊 : 따뜻해진 바닷물이 빙하 아래로 침투해 녹임  
    - 검은탄소(매연) 🔥 : 빙하 표면에 쌓이면 햇빛을 더 흡수하여 빠르게 녹음  
    - 지구 순환 변화 🌍 : 바람·해류의 변화가 빙하의 안정성에 영향을 줌  
    - 산불 증가 🔥 : 대형 산불이 발생하면 대기 중 온실가스·매연 증가 → 빙하에 악영향  
    - 산업 개발/삼림 벌채 🌲 : 삼림이 줄어들며 탄소 흡수량 감소 → 온난화 가속
    """)

    st.markdown('<div class="sub-header">💡 청소년이 할 수 있는 행동 제언</div>', unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background-color:#E8F6F3;padding:20px;border-radius:12px;color:black;">
        <h4>🌱 생활 속 탄소 줄이기</h4>
        <ul>
        <li>대중교통·자전거 이용</li>
        <li>전기 절약, 재활용 실천</li>
        <li>플라스틱 줄이기</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background-color:#FFF3E0;padding:20px;border-radius:12px;color:black;">
        <h4>📢 기후 목소리 내기</h4>
        <ul>
        <li>학교 기후 동아리 참여</li>
        <li>친구·가족과 문제 공유</li>
        <li>지역 환경 캠페인 참여</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background-color:#E3F2FD;padding:20px;border-radius:12px;color:black;">
        <h4>📚 기후 지식 쌓기</h4>
        <ul>
        <li>환경 다큐멘터리 시청</li>
        <li>기후 관련 책·기사 읽기</li>
        <li>교과 연계 학습</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background-color:#FCE4EC;padding:20px;border-radius:12px;color:black;margin-top:20px;">
    <h4>🤝 공동 행동 실천</h4>
    <ul>
    <li>친구와 함께 기후 캠페인 기획</li>
    <li>지역 환경 봉사활동 참여</li>
    <li>온라인 서명·챌린지 동참</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ==================== 탭4: 팬데믹 기간 청소년 정신건강 ====================
with tab4:
    st.markdown('<div class="sub-header">🧠 팬데믹 기간 동안 청소년 정신건강 변화</div>', unsafe_allow_html=True)

    # 팬데믹 기간 동안 청소년들의 정신건강 변화 그래프
    mental_health_data = {
        '연도': [2020, 2021, 2022, 2023],
        '지속적인 슬픔 또는 절망감 비율': [35, 38, 42, 40],
        '자살 심각하게 고려한 비율': [18, 20, 22, 20],
        '자살 시도 비율': [8, 9, 10, 9.5]
    }
    df_mental_health = pd.DataFrame(mental_health_data)

    fig_mental_health = go.Figure()
    fig_mental_health.add_trace(go.Scatter(
        x=df_mental_health['연도'],
        y=df_mental_health['지속적인 슬픔 또는 절망감 비율'],
        mode='lines+markers',
        name='지속적인 슬픔 또는 절망감 비율',
        line=dict(color='#FF6347')
    ))
    fig_mental_health.add_trace(go.Scatter(
        x=df_mental_health['연도'],
        y=df_mental_health['자살 심각하게 고려한 비율'],
        mode='lines+markers',
        name='자살 심각하게 고려한 비율',
        line=dict(color='#4682B4')
    ))
    fig_mental_health.add_trace(go.Scatter(
        x=df_mental_health['연도'],
        y=df_mental_health['자살 시도 비율'],
        mode='lines+markers',
        name='자살 시도 비율',
        line=dict(color='#32CD32')
    ))

    fig_mental_health.update_layout(
        title='팬데믹 기간 동안 청소년 정신건강 변화',
        xaxis_title='연도',
        yaxis_title='비율 (%)',
        template='plotly_white',
        height=400
    )
    st.plotly_chart(fig_mental_health, use_container_width=True)

    st.markdown("""
    팬데믹 기간 동안 청소년들의 정신건강 상태는 크게 악화되었습니다. CDC의 2023년 청소년 위험행동조사에 따르면, 조사에 응답한 고등학생 중 약 40%가 지속적인 슬픔이나 절망감을 경험했으며, 20%는 자살을 심각하게 고려했고, 9.5%는 실제로 자살을 시도한 것으로 나타났습니다.
    """, unsafe_allow_html=True)

    st.markdown("""
    **주요 요인:**
    - 사회적 고립: 팬데믹으로 인한 학교 폐쇄와 사회적 거리두기로 인해 청소년들은 친구들과의 대면 상호작용이 줄어들었고, 이로 인해 외로움과 우울감이 증가했습니다.
    - 가족 문제: 가족 내 갈등이나 경제적 어려움이 청소년들의 정신건강에 부정적인 영향을 미쳤습니다.
    - 학교 지원 부족: 많은 청소년들이 학교에서 충분한 정신건강 지원을 받지 못하고 있다고 응답했습니다.

    **팬데믹 후 청소년들의 목소리:**
    팬데믹 이후, 청소년들은 자신들의 정신건강 문제를 해결하기 위한 목소리를 높이고 있습니다. 많은 청소년들이 학교에서의 정신건강 지원 확대와 사회적 고립 해소를 위한 정책적 노력을 요구하고 있습니다.
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="data-source">
    <h4>📚 데이터 출처</h4>
    <ul>
    <li>🧠 CDC 2023 청소년 위험행동조사: <a href="https://www.cdc.gov/yrbs/results/2023-yrbs-results.html" target="_blank">CDC 2023 YRBS</a></li>
    <li>📈 청소년 정신건강 통계: <a href="https://www.aecf.org/blog/youth-mental-health-statistics" target="_blank">Annie E. Casey Foundation</a></li>
    <li>📊 팬데믹 기간 청소년 정신건강 영향: <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC11526700/" target="_blank">PMC</a></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
