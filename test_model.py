import tensorflow as tf

# TFLite 모델 로드
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# 입력/출력 정보
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("모델 로드 성공!")
print(f"입력 shape: {input_details[0]['shape']}")
print(f"출력 shape: {output_details[0]['shape']}")
