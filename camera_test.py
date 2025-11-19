import cv2

print("카메라를 찾는 중...")

# 0번 카메라 장치 열기
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ 카메라를 열 수 없습니다! 연결을 확인해주세요.")
    exit()

print("찰칵! 📸 사진을 찍습니다.")

# 프레임(이미지) 한 장 읽기
ret, frame = cap.read()

if ret:
    # 이미지 파일로 저장하기
    filename = 'test_photo.jpg'
    cv2.imwrite(filename, frame)
    print(f"✅ 성공! '{filename}' 파일이 저장되었습니다.")
    print("왼쪽 파일 탐색기에서 사진을 클릭해 확인해보세요.")
else:
    print("❌ 프레임을 읽어오지 못했습니다.")

# 카메라 자원 해제
cap.release()