import pygame
import time
import os

# 1. 믹서 초기화 (소리 낼 준비)
pygame.mixer.init()

# 파일 경로 설정
sound_file = "test_sound.mp3"

# 파일이 진짜 있는지 확인
if not os.path.exists(sound_file):
    print(f"❌ {sound_file} 파일이 없습니다! wget 명령어로 다운로드 했나요?")
    exit()

try:
    # 2. 음악 파일 로드
    pygame.mixer.music.load(sound_file)
    
    print(f"🎵 {sound_file} 재생을 시작합니다...")
    print("볼륨을 조절하려면 터미널에서 'alsamixer'를 사용하세요.")

    # 3. 재생 시작
    pygame.mixer.music.play()

    # 4. 음악이 끝날 때까지 대기 (이거 없으면 바로 프로그램 꺼져서 소리 안 남)
    while pygame.mixer.music.get_busy():
        time.sleep(1)
        
    print("✅ 재생 완료!")

except Exception as e:
    print(f"❌ 재생 중 오류 발생: {e}")