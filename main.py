import time
import cv2
import numpy as np
import board
import adafruit_dht
import pygame
import os
import json  # <--- 데이터를 파일로 저장하기 위해 추가됨

# --- [설정] ---
MP3_FILE = "test_sound.mp3"    # 아까 성공했던 mp3 파일 이름!
DHT_PIN = board.D4
STATUS_FILE = "status.json" # 데이터를 공유할 파일 이름

# --- [초기화] ---
print("🚀 시스템(Backend)을 시작합니다...")
try:
    pygame.mixer.init()
except:
    print("오디오 장치 초기화 실패 (무시하고 진행)")

dhtDevice = adafruit_dht.DHT11(DHT_PIN)

def get_brightness():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened(): return 0
    ret, frame = cap.read()
    cap.release()
    if not ret: return 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return float(np.mean(gray))

def play_music(file_name):
    if not os.path.exists(file_name): return
    try:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(file_name)
            pygame.mixer.music.play()
    except: pass

def save_status(temp, humi, bright, mood):
    """현재 상태를 json 파일로 저장하는 함수"""
    data = {
        "temperature": temp,
        "humidity": humi,
        "brightness": bright,
        "mood": mood,
        "timestamp": time.time()
    }
    try:
        with open(STATUS_FILE, 'w') as f:
            json.dump(data, f)
    except:
        pass

# --- [메인 루프] ---
try:
    while True:
        try:
            # 1. 데이터 수집
            temp = dhtDevice.temperature
            humi = dhtDevice.humidity
            brightness = get_brightness()
            
            # 센서 에러 시 재시도
            if temp is None or humi is None:
                time.sleep(0.5)
                continue

            # 2. 감성 판단 로직
            current_mood = "Cozy (쾌적)"
            if brightness < 50: # 밝기 기준 (테스트를 위해 80->50 조절 가능)
                current_mood = "Night (밤/감성)"
                play_music(MP3_FILE)
            elif temp > 28:
                current_mood = "Hot (더움/신남)"
                play_music(MP3_FILE)
            
            # 3. 상태 저장 (대시보드가 읽을 수 있게!)
            save_status(temp, humi, brightness, current_mood)
            print(f"저장됨: {temp}°C, {humi}%, 밝기:{brightness:.1f}, 무드:{current_mood}")

        except RuntimeError:
            time.sleep(0.5)
            continue
        except Exception as e:
            print(f"에러 발생: {e}")
            break

        time.sleep(2) # 2초마다 갱신

except KeyboardInterrupt:
    print("시스템 종료")
    dhtDevice.exit()