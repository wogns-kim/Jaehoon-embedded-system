import time
import cv2
import numpy as np
import board
import adafruit_dht
import pygame
import os

# --- [설정] ---
# 여기에 아까 성공한 MP3 파일 이름을 적어주세요!
MP3_FILE = "test_sound.mp3"  
DHT_PIN = board.D4     # 센서 핀 번호 (GPIO 4)

# --- [초기화] ---
print("🚀 시스템을 초기화 중입니다...")
pygame.mixer.init()
dhtDevice = adafruit_dht.DHT11(DHT_PIN)

# --- [함수 정의] ---

def get_brightness():
    """카메라로 사진을 찍어 밝기를 계산합니다 (0~255)"""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return 0
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        return 0
        
    # 흑백으로 변환하여 평균 밝기 계산
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray)
    return avg_brightness

def play_music(file_name):
    """음악을 재생합니다"""
    if not os.path.exists(file_name):
        print(f"❌ 음악 파일({file_name})이 없습니다!")
        return

    if not pygame.mixer.music.get_busy(): # 이미 재생 중이 아니면
        try:
            pygame.mixer.music.load(file_name)
            pygame.mixer.music.play()
            print(f"🎵 음악 재생 시작: {file_name}")
        except Exception as e:
            print(f"음악 재생 오류: {e}")

# --- [메인 루프] ---
print("✅ 시스템 준비 완료! 감성 큐레이션을 시작합니다.")

try:
    while True:
        try:
            # 1. 센서 데이터 읽기
            temp = dhtDevice.temperature
            humi = dhtDevice.humidity
            
            # 2. 카메라 밝기 읽기
            brightness = get_brightness()
            
            # 3. 현재 상태 판단 및 출력
            status_msg = f"🌡️ 온도: {temp}°C | 💧 습도: {humi}% | ☀️ 밝기: {brightness:.1f}"
            print(status_msg)

            # --- [감성 큐레이션 로직] ---
            # 시나리오 1: 어두우면(밤이면) 무조건 음악 틀기
            if brightness < 80: 
                print("🌙 어두운 밤이네요. 감성적인 음악을 틉니다.")
                play_music(MP3_FILE)
            
            # 시나리오 2: 덥고 습하면 음악 틀기 (예시)
            elif temp is not None and temp > 28:
                print("🥵 너무 더워요! 시원한 음악을 틉니다.")
                play_music(MP3_FILE)
                
            else:
                print("😊 쾌적한 상태입니다. (음악 대기 중)")
                # 음악을 끄고 싶으면 아래 주석을 해제하세요
                # pygame.mixer.music.stop()

        except RuntimeError as error:
            # 센서 읽기 에러는 무시하고 넘어감
            time.sleep(1)
            continue
            
        except Exception as error:
            dhtDevice.exit()
            raise error

        # 3초마다 반복
        time.sleep(3)

except KeyboardInterrupt:
    print("\n시스템을 종료합니다. 안녕히 가세요! 👋")
    dhtDevice.exit()