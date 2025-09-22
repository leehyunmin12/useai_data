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
import random
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
.game-card {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #e9ecef;
    margin: 10px 0;
    color: #000000;
}
.quiz-option {
    background-color: #e3f2fd;
    padding: 10px;
    margin: 5px 0;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s;
}
.quiz-option:hover {
    background-color: #bbdefb;
}
.score-display {
    font-size: 1.5rem;
    font-weight: bold;
    color: #2e7d32;
    text-align: center;
    padding: 10px;
    background-color: #e8f5e8;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# 제목
st.markdown('<div class="main-header">🌍 빙하 바이러스와 청소년 정신건강 분석 대시보드</div>', unsafe_allow_html=True)

# ==================== 탭 생성 ====================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 공식 공개 데이터 대시보드",
    "📈 사용자 데이터 분석",
    "🧊 빙하 요인 & 청소년 행동",
    "🧠 팬데믹 기간 청소년 정신건강",
    "🎮 기후 행동 퀴즈 게임"
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
    st.markdown('<div class="sub-header">📈 사용자 맞춤형 기후 영향 분석</div>', unsafe_allow_html=True)
    
    # 사용자 입력 섹션
    st.markdown("### 🔍 나의 기후 영향도 분석하기")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏠 개인 정보")
        age = st.slider("나이", 13, 19, 16)
        region = st.selectbox("거주 지역", ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"])
        family_size = st.slider("가족 구성원 수", 2, 8, 4)
        
    with col2:
        st.markdown("#### 🚗 생활 패턴")
        transport = st.multiselect("주로 이용하는 교통수단", ["도보", "자전거", "대중교통", "자가용", "오토바이"])
        electricity_usage = st.slider("월평균 전기 사용량 (kWh)", 200, 800, 350)
        waste_separation = st.slider("분리수거 실천도 (1-5점)", 1, 5, 3)
    
    # 기후 인식도 설문
    st.markdown("#### 🌍 기후 변화 인식도")
    climate_concern = st.slider("기후 변화에 대한 걱정 정도 (1-10점)", 1, 10, 7)
    action_willingness = st.slider("환경 보호 행동 의지 (1-10점)", 1, 10, 6)
    future_anxiety = st.slider("미래에 대한 불안감 (1-10점)", 1, 10, 5)
    
    if st.button("📊 내 기후 영향도 분석하기", type="primary"):
        # 탄소 발자국 계산
        carbon_transport = len(transport) * 50 if "자가용" in transport else len(transport) * 20
        carbon_electricity = electricity_usage * 0.5
        carbon_waste = (5 - waste_separation) * 30
        total_carbon = carbon_transport + carbon_electricity + carbon_waste
        
        # 기후 스트레스 지수 계산
        climate_stress = (climate_concern + future_anxiety) / 2
        action_gap = climate_concern - action_willingness
        
        # 결과 표시
        st.markdown("---")
        st.markdown('<div class="sub-header">📊 분석 결과</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🌡️ 월간 탄소 발자국", f"{total_carbon:.1f} kg CO2", 
                     delta=f"{total_carbon-300:.1f}" if total_carbon > 300 else f"{total_carbon-300:.1f}")
        
        with col2:
            st.metric("😰 기후 스트레스 지수", f"{climate_stress:.1f}/10", 
                     delta="높음" if climate_stress > 7 else "보통" if climate_stress > 4 else "낮음")
        
        with col3:
            st.metric("⚡ 행동 의지 갭", f"{action_gap:.1f}점", 
                     delta="개선 필요" if action_gap > 2 else "양호")
        
        # 맞춤형 추천
        st.markdown("### 💡 맞춤형 기후 행동 추천")
        
        # 우선순위별 추천 시스템
        high_priority = []
        medium_priority = []
        low_priority = []
        
        # 탄소 발자국 기반 추천
        if "자가용" in transport:
            high_priority.append({
                "action": "🚌 대중교통 또는 자전거 이용하기",
                "impact": "월 100-150kg CO2 절약",
                "difficulty": "쉬움",
                "detail": "가까운 거리는 걷거나 자전거를, 먼 거리는 지하철/버스 이용"
            })
        
        if electricity_usage > 400:
            high_priority.append({
                "action": "💡 스마트한 전기 절약",
                "impact": "월 50-80kg CO2 절약", 
                "difficulty": "쉬움",
                "detail": "사용하지 않는 전자제품 플러그 뽑기, LED 전구 사용, 에어컨 적정온도 유지"
            })
            
        if waste_separation < 3:
            high_priority.append({
                "action": "♻️ 제대로 된 분리수거와 재활용",
                "impact": "월 30-50kg CO2 절약",
                "difficulty": "쉬움", 
                "detail": "플라스틱 세척 후 분리배출, 종이/캔/병 올바른 분류"
            })
        
        # 정신건강 관련 추천
        if climate_stress > 7:
            high_priority.append({
                "action": "🧘‍♀️ 기후 불안감 완화 활동",
                "impact": "정신건강 개선",
                "difficulty": "보통",
                "detail": "자연에서 시간 보내기, 명상, 요가, 친구들과 감정 나누기"
            })
        
        if action_gap > 3:
            medium_priority.append({
                "action": "👥 동료와 함께하는 기후 행동",
                "impact": "실천률 3배 향상",
                "difficulty": "보통",
                "detail": "학교 환경동아리 참여, 친구들과 챌린지, 가족 기후 회의"
            })
        
        # 연령별 맞춤 추천
        if age <= 15:
            medium_priority.append({
                "action": "📚 또래와 함께하는 기후 교육",
                "impact": "지식 향상 + 네트워크 구축",
                "difficulty": "쉬움",
                "detail": "학교 과학시간 연계, 환경 다큐 시청, 기후 관련 도서 읽기"
            })
        else:
            medium_priority.append({
                "action": "🎯 리더십 발휘하기",
                "impact": "주변인 5-10명 영향",
                "difficulty": "어려움",
                "detail": "환경 동아리 만들기, 캠페인 기획, 지역사회 참여"
            })
        
        # 지역별 맞춤 추천
        if region in ["서울", "인천", "경기"]:
            low_priority.append({
                "action": "🌆 도시형 기후 행동",
                "impact": "지역 환경 개선",
                "difficulty": "보통", 
                "detail": "미세먼지 줄이기, 도시 열섬 완화, 그린 루프 캠페인 참여"
            })
        else:
            low_priority.append({
                "action": "🌄 지역 특성 맞춤 활동",
                "impact": "생태계 보호",
                "difficulty": "보통",
                "detail": "지역 생태계 보호, 농촌형 재생에너지, 지역 특산물 활용"
            })
        
        # 추가 보편적 추천사항
        medium_priority.extend([
            {
                "action": "🌱 식습관 개선",
                "impact": "월 20-40kg CO2 절약",
                "difficulty": "보통",
                "detail": "로컬 푸드 섭취, 음식물 쓰레기 줄이기, 채식 요리 늘리기"
            },
            {
                "action": "🛍️ 의식적인 소비",
                "impact": "월 15-30kg CO2 절약",
                "difficulty": "어려움",
                "detail": "중고품 활용, 내구재 선택, 불필요한 구매 줄이기"
            }
        ])
        
        low_priority.extend([
            {
                "action": "📱 디지털 탄소발자국 줄이기",
                "impact": "월 5-15kg CO2 절약", 
                "difficulty": "쉬움",
                "detail": "스트리밍 시간 줄이기, 클라우드 저장소 정리, 불필요한 앱 삭제"
            },
            {
                "action": "🏡 가정 내 에너지 효율화",
                "impact": "월 30-60kg CO2 절약",
                "difficulty": "어려움",
                "detail": "단열 개선, 고효율 가전 교체, 태양광 패널 설치 (가족과 상의)"
            }
        ])
        
        # 우선순위별 표시
        if high_priority:
            st.markdown("#### 🔥 **즉시 실천 추천** (높은 효과)")
            for i, rec in enumerate(high_priority):
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.success(f"**{rec['action']}**")
                        st.write(f"💡 {rec['detail']}")
                    with col2:
                        st.metric("영향도", rec['impact'])
                    with col3:
                        difficulty_color = {"쉬움": "🟢", "보통": "🟡", "어려움": "🔴"}
                        st.write(f"{difficulty_color[rec['difficulty']]} {rec['difficulty']}")
                    st.markdown("---")
        
        if medium_priority:
            st.markdown("#### 🎯 **단계적 실천 추천** (중간 효과)")
            for rec in medium_priority:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.info(f"**{rec['action']}**")
                        st.write(f"💡 {rec['detail']}")
                    with col2:
                        st.metric("영향도", rec['impact'])
                    with col3:
                        difficulty_color = {"쉬움": "🟢", "보통": "🟡", "어려움": "🔴"}
                        st.write(f"{difficulty_color[rec['difficulty']]} {rec['difficulty']}")
                    st.markdown("---")
        
        if low_priority:
            st.markdown("#### 🌟 **장기 목표 추천** (지속적 효과)")
            for rec in low_priority:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1]) 
                    with col1:
                        st.write(f"**{rec['action']}**")
                        st.write(f"💡 {rec['detail']}")
                    with col2:
                        st.metric("영향도", rec['impact'])
                    with col3:
                        difficulty_color = {"쉬움": "🟢", "보통": "🟡", "어려움": "🔴"}
                        st.write(f"{difficulty_color[rec['difficulty']]} {rec['difficulty']}")
                    st.markdown("---")
        
        # 종합 추천 점수
        total_recommendations = len(high_priority) + len(medium_priority) + len(low_priority)
        st.markdown(f"""
        ### 📋 **당신만의 기후 행동 로드맵**
        
        ✅ **총 {total_recommendations}개 맞춤형 추천사항**  
        🔥 **즉시 실천**: {len(high_priority)}개 (당장 시작 가능)  
        🎯 **단계적 실천**: {len(medium_priority)}개 (1-2주 내 도전)  
        🌟 **장기 목표**: {len(low_priority)}개 (한 달 이상 계획)  
        
        **💪 실천 팁**: 한 번에 모든 것을 하려 하지 말고, 즉시 실천 항목부터 하나씩 차근차근 도전해보세요!
        """)
        
        # 실천 동기부여
        potential_savings = 0
        if "자가용" in transport: potential_savings += 125
        if electricity_usage > 400: potential_savings += 65
        if waste_separation < 3: potential_savings += 40
        potential_savings += 30  # 기본 개선 가능량
        
        st.success(f"""
        🌍 **예상 효과**: 이 추천사항들을 실천하면 **월 약 {potential_savings}kg CO2**를 절약할 수 있어요!  
        이는 **나무 {potential_savings//22}그루**가 1년간 흡수하는 CO2와 같은 양입니다. 🌳
        """)
        
        # 지역별 비교 차트
        st.markdown("### 📍 지역별 기후 영향 비교")
        
        # 가상 지역 데이터
        regional_data = {
            "지역": ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종"],
            "평균_탄소발자국": [320, 280, 290, 310, 270, 285, 340, 260],
            "기후_스트레스": [7.2, 6.8, 6.5, 7.0, 6.3, 6.7, 7.5, 6.0]
        }
        df_regional = pd.DataFrame(regional_data)
        
        fig_regional = go.Figure()
        fig_regional.add_trace(go.Bar(
            name="평균 탄소 발자국",
            x=df_regional["지역"],
            y=df_regional["평균_탄소발자국"],
            yaxis="y",
            offsetgroup=1,
            marker_color='#FF6B6B'
        ))
        fig_regional.add_trace(go.Bar(
            name="기후 스트레스 지수",
            x=df_regional["지역"],
            y=df_regional["기후_스트레스"],
            yaxis="y2",
            offsetgroup=2,
            marker_color='#4ECDC4'
        ))
        
        # 사용자 데이터 표시
        if region in df_regional["지역"].values:
            fig_regional.add_trace(go.Scatter(
                name="내 데이터",
                x=[region],
                y=[total_carbon],
                mode='markers',
                marker=dict(size=15, color='red', symbol='star'),
                yaxis="y"
            ))
        
        fig_regional.update_layout(
            title="지역별 탄소 발자국 및 기후 스트레스 비교",
            xaxis_title="지역",
            yaxis=dict(title="탄소 발자국 (kg CO2)", side="left"),
            yaxis2=dict(title="기후 스트레스 지수", side="right", overlaying="y"),
            height=400
        )
        st.plotly_chart(fig_regional, use_container_width=True)
        
        # 개인화된 행동 계획
        st.markdown("### 📅 30일 기후 행동 계획")
        st.markdown("**체계적인 실천을 위한 주차별 목표를 설정해보세요!**")
        st.markdown("---")
        
        action_plan = {
            "1주차 🌱 기초 다지기": ["대중교통 3회 이상 이용하기", "전기 절약 실천하기 (플러그 뽑기)", "분리수거 완벽하게 실천하기"],
            "2주차 🤝 소통하기": ["친구와 환경 이야기 나누기", "일회용품 사용 줄이기", "에너지 절약형 가전제품 사용하기"],
            "3주차 🌍 확장하기": ["환경 동아리 활동에 참여하기", "지역 환경 캠페인 찾아보기", "가족과 기후 변화 토론하기"],
            "4주차 🎯 도전하기": ["친구들과 기후 행동 챌린지하기", "환경 다큐멘터리 시청하기", "다음 달 실천 계획 세우기"]
        }
        
        import time
        current_time = int(time.time())
        
        col1, col2 = st.columns(2)
        
        for idx, (week, actions) in enumerate(action_plan.items()):
            target_col = col1 if idx % 2 == 0 else col2
            
            with target_col:
                st.markdown(f"#### {week}")
                st.markdown("**이번 주 실천 목표:**")
                
                for action_idx, action in enumerate(actions):
                    unique_key = f"plan_{current_time}_{idx}_{action_idx}_{len(action)}"
                    checkbox_result = st.checkbox(
                        action, 
                        key=unique_key,
                        help=f"{week}의 {action_idx+1}번째 목표입니다."
                    )
                    
                st.markdown("")  # 공백 추가
                if idx < len(action_plan) - 1:  # 마지막 항목이 아닐 때만 구분선 추가
                    st.markdown("---")
    
    # 추가 리소스
    st.markdown("---")
    st.markdown("### 📚 더 알아보기")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🔬 기후 과학 이해하기**
        - [NASA 기후 변화 시뮬레이션](https://climate.nasa.gov)
        - [IPCC 청소년 가이드](https://www.ipcc.ch)
        - [기후변화센터 교육자료](https://climatechange.kr)
        """)
    
    with col2:
        st.markdown("""
        **🌱 실천 가이드**
        - [청소년 환경 행동 매뉴얼](https://example.com)
        - [가정에서 실천하는 탄소중립](https://example.com)
        - [학교 기후 동아리 만들기](https://example.com)
        """)
    
    with col3:
        st.markdown("""
        **🤝 커뮤니티 참여**
        - [청소년 기후행동 단체](https://youthclimatestrike.org)
        - [지역 환경 봉사활동](https://1365.go.kr)
        - [온라인 기후 토론방](https://example.com)
        """)
    
    # 데이터 저장 및 추적 기능 (가상)
    st.markdown("---")
    st.markdown("### 📈 나의 기후 행동 추적")
    
    # 가상의 사용자 진행도 데이터
    progress_data = {
        "월": ["1월", "2월", "3월", "4월", "5월", "6월"],
        "탄소절약량": [20, 35, 45, 60, 70, 85],
        "실천점수": [6.2, 6.8, 7.1, 7.5, 8.0, 8.3]
    }
    df_progress = pd.DataFrame(progress_data)
    
    fig_progress = go.Figure()
    fig_progress.add_trace(go.Scatter(
        x=df_progress["월"],
        y=df_progress["탄소절약량"],
        mode='lines+markers',
        name='월별 탄소 절약량 (kg)',
        line=dict(color='#2ECC71', width=3),
        marker=dict(size=8)
    ))
    
    fig_progress2 = go.Figure()
    fig_progress2.add_trace(go.Scatter(
        x=df_progress["월"],
        y=df_progress["실천점수"],
        mode='lines+markers',
        name='환경 실천 점수',
        line=dict(color='#3498DB', width=3),
        marker=dict(size=8)
    ))
    
    col1, col2 = st.columns(2)
    with col1:
        fig_progress.update_layout(title="월별 탄소 절약량 추이", height=300)
        st.plotly_chart(fig_progress, use_container_width=True)
    
    with col2:
        fig_progress2.update_layout(title="환경 실천 점수 향상", height=300)
        st.plotly_chart(fig_progress2, use_container_width=True)

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

# ==================== 탭5: 기후 행동 퀴즈 게임 ====================
with tab5:
    st.markdown('<div class="sub-header">🎮 기후 행동 퀴즈 게임</div>', unsafe_allow_html=True)
    st.markdown("**아래 퀴즈를 풀며 기후 행동에 대해 더 자세히 알아보세요!**")

    # 게임 상태 초기화
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'quiz_answered' not in st.session_state:
        st.session_state.quiz_answered = []
    if 'current_quiz' not in st.session_state:
        st.session_state.current_quiz = 0

    # 퀴즈 데이터
    quiz_data = [
        {
            "question": "🌍 일상생활에서 탄소 발자국을 가장 효과적으로 줄일 수 있는 방법은?",
            "options": ["에어컨을 항상 가장 낮은 온도로 설정하기", "대중교통이나 자전거 이용하기", "전자제품을 계속 켜두기", "일회용품 많이 사용하기"],
            "correct": 1,
            "explanation": "대중교통이나 자전거를 이용하면 개인 차량 사용을 줄여 CO2 배출량을 크게 감소시킬 수 있습니다. 🚌🚲"
        },
        {
            "question": "🔥 빙하가 빠르게 녹는 주요 원인 중 하나인 '검은탄소'란 무엇인가요?",
            "options": ["석탄 덩어리", "매연과 그을음 입자", "검은색 얼음", "오염된 물"],
            "correct": 1,
            "explanation": "검은탄소(매연)는 빙하 표면에 쌓여서 햇빛을 더 많이 흡수하게 만들어 빙하를 더 빠르게 녹게 합니다. ⚫"
        },
        {
            "question": "🌱 청소년이 기후 변화에 대응하기 위해 할 수 있는 가장 중요한 행동은?",
            "options": ["아무것도 하지 않기", "친구들과 기후 문제에 대해 이야기하고 함께 행동하기", "혼자서만 실천하기", "어른들이 해결하기를 기다리기"],
            "correct": 1,
            "explanation": "친구들과 함께 기후 문제를 공유하고 집단 행동을 통해 더 큰 변화를 만들 수 있습니다! 👫🌍"
        },
        {
            "question": "♻️ 재활용을 올바르게 실천하는 방법은?",
            "options": ["모든 쓰레기를 재활용통에 넣기", "플라스틱을 깨끗이 씻어서 분리배출하기", "재활용 마크만 확인하고 버리기", "종류 상관없이 함께 버리기"],
            "correct": 1,
            "explanation": "플라스틱은 깨끗이 씻어서 올바르게 분리배출해야 실제로 재활용될 수 있습니다. 🧼♻️"
        },
        {
            "question": "🌳 삼림 벌채가 기후 변화에 미치는 영향은?",
            "options": ["기온을 낮춘다", "CO2 흡수량이 줄어들어 온난화가 가속화된다", "빙하가 더 빨리 얼어붙는다", "아무 영향이 없다"],
            "correct": 1,
            "explanation": "나무는 CO2를 흡수하는 중요한 역할을 하는데, 삼림이 줄어들면 대기 중 CO2가 증가해 온난화가 가속화됩니다. 🌲💨"
        }
    ]

    # 점수 표시
    col_score1, col_score2, col_score3 = st.columns([1,2,1])
    with col_score2:
        st.markdown(f'<div class="score-display">🏆 현재 점수: {st.session_state.quiz_score}/5</div>', unsafe_allow_html=True)

    # 게임 리셋 버튼
    if st.button("🔄 게임 다시 시작", key="reset_quiz"):
        st.session_state.quiz_score = 0
        st.session_state.quiz_answered = []
        st.session_state.current_quiz = 0
        st.rerun()

    # 퀴즈 표시
    if st.session_state.current_quiz < len(quiz_data):
        current_q = quiz_data[st.session_state.current_quiz]
        
        st.markdown(f"""
        <div class="game-card">
        <h3>질문 {st.session_state.current_quiz + 1}/5</h3>
        <h4>{current_q['question']}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # 선택지 버튼들
        cols = st.columns(2)
        for i, option in enumerate(current_q['options']):
            col_idx = i % 2
            with cols[col_idx]:
                if st.button(f"{chr(65+i)}. {option}", key=f"option_{st.session_state.current_quiz}_{i}", 
                           use_container_width=True):
                    # 정답 체크
                    if i == current_q['correct']:
                        st.session_state.quiz_score += 1
                        st.success(f"✅ 정답입니다! {current_q['explanation']}")
                    else:
                        correct_answer = current_q['options'][current_q['correct']]
                        st.error(f"❌ 틀렸습니다. 정답: {chr(65+current_q['correct'])}. {correct_answer}")
                        st.info(current_q['explanation'])
                    
                    st.session_state.quiz_answered.append(st.session_state.current_quiz)
                    st.session_state.current_quiz += 1
                    
                    # 다음 문제로 이동
                    if st.session_state.current_quiz < len(quiz_data):
                        if st.button("➡️ 다음 문제", key="next_question"):
                            st.rerun()
                        # 자동으로 다음 문제로 이동
                        st.rerun()
    
    else:
        # 게임 완료
        final_score = st.session_state.quiz_score
        st.balloons()
        
        if final_score == 5:
            st.success("🎉 완벽합니다! 기후 행동 전문가가 되셨네요!")
            st.markdown("🏅 **기후 수호자** 칭호를 획득하셨습니다!")
        elif final_score >= 3:
            st.success("👏 잘하셨어요! 기후 변화에 대한 이해도가 높으시네요!")
            st.markdown("🌱 **기후 지킴이** 칭호를 획득하셨습니다!")
        else:
            st.info("💪 조금 더 노력하면 됩니다! 다시 도전해보세요!")
            st.markdown("🌿 **기후 새싹** 칭호를 획득하셨습니다!")
        
        # 행동 권장사항 표시
        st.markdown("""
        ### 🌍 이제 실제로 행동해볼까요?
        
        **오늘부터 실천할 수 있는 작은 행동들:**
        - 🚶‍♀️ 가까운 거리는 걸어가기 또는 자전거 타기
        - 💡 사용하지 않는 전자제품 플러그 뽑기
        - 🥤 텀블러나 에코백 사용하기
        - 👥 친구들과 기후 변화에 대해 이야기하기
        - 🌱 학교나 지역의 환경 동아리 참여하기
        
        **당신의 작은 행동이 지구를 구합니다! 💚**
        """)

    # 추가 정보 섹션
    st.markdown("""
    ---
    ### 📚 더 알아보고 싶다면?
    
    🔗 **유용한 링크들:**
    - [청소년 기후행동](https://www.youthclimatestrike.org/) - 전 세계 청소년 기후 운동
    - [기후변화센터](https://www.climatechange.kr/) - 기후 변화 정보와 교육 자료
    - [그린피스](https://www.greenpeace.org/korea/) - 환경 보호 캠페인 참여
    - [환경부 청소년 환경교육](https://www.me.go.kr/) - 정부 환경 교육 프로그램
    """)

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