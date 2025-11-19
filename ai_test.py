import cv2
import numpy as np
# tflite 런타임 불러오기 (설치된 라이브러리에 따라 다를 수 있음)
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    import tensorflow.lite as tflite

print("🧠 AI 모델을 로딩 중입니다...")

# 1. 모델과 라벨 파일 경로 설정
model_path = "model/mobilenet_v1_1.0_224_quant.tflite"
label_path = "model/labels_mobilenet_quant_v1_224.txt"

# 2. 라벨(이름표) 읽어오기
with open(label_path, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# 3. AI 모델 준비 (Interpreter)
interpreter = tflite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# 입력/출력 정보 가져오기
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# 4. 분석할 이미지 불러오기 (아까 찍은 사진)
image_path = "test_photo.jpg"
img = cv2.imread(image_path)

if img is None:
    print(f"❌ {image_path} 파일이 없습니다! 카메라 테스트를 먼저 해서 사진을 찍어주세요.")
    exit()

# 5. 이미지를 AI가 이해할 수 있는 크기(224x224)로 변형
input_shape = input_details[0]['shape']
img_resized = cv2.resize(img, (input_shape[1], input_shape[2]))
input_data = np.expand_dims(img_resized, axis=0)

# 6. AI에게 질문 던지기 (Inference)
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()

# 7. 결과 받기
output_data = interpreter.get_tensor(output_details[0]['index'])
results = np.squeeze(output_data)

# 가장 높은 확률의 정답 찾기
top_index = results.argsort()[-1]
accuracy = results[top_index] / 255.0 * 100  # 확률 계산

print(f"\n🔍 분석 결과: 이 사진은 '{labels[top_index]}' 입니다!")
print(f"📊 확신도: {accuracy:.2f}%")