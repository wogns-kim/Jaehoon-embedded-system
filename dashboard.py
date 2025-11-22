import streamlit as st
import json
import time
import os

# 페이지 기본 설정
st.set_page_config(page_title="AI 스마트홈", page_icon="🏠", layout="wide")

st.title("🏠 AI 감성 맞춤형 스마트홈")
st.subheader("실시간 환경 모니터링 시스템")

# 데이터 읽어오는 함수
def load_data():
    if not os.path.exists("status.json"):
        return None
    try:
        with open("status.json", 'r') as f:
            return json.load(f)
    except:
        return None

# 화면 레이아웃 (3단 구성)
col1, col2, col3 = st.columns(3)
temp_metric = col1.empty()
humi_metric = col2.empty()
bright_metric = col3.empty()

st.divider() # 구분선
mood_area = st.empty()

# 자동 새로고침 루프
while True:
    data = load_data()
    
    if data:
        # 숫자 표시 (Metric)
        temp_metric.metric(label="🌡️ 온도", value=f"{data['temperature']} °C")
        humi_metric.metric(label="💧 습도", value=f"{data['humidity']} %")
        bright_metric.metric(label="☀️ 밝기", value=f"{data['brightness']:.1f}")
        
        # 무드 표시
        mood = data['mood']
        if "Night" in mood:
            mood_area.info(f"🌙 현재 상태: {mood} - 조명이 어두워 감성적인 음악을 재생합니다.")
        elif "Hot" in mood:
            mood_area.warning(f"🥵 현재 상태: {mood} - 온도가 높아 시원한 음악을 재생합니다.")
        else:
            mood_area.success(f"😊 현재 상태: {mood} - 쾌적한 환경입니다.")
            
    else:
        mood_area.error("데이터 수신 대기 중... (main.py를 실행해주세요!)")
        
    time.sleep(1) # 1초마다 화면 갱신