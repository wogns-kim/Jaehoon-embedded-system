import tensorflow as tf
import numpy as np

# 간단한 모델 생성
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, input_shape=(5,)),
    tf.keras.layers.Dense(1)
])

# TFLite로 변환
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# 저장
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)

print("model.tflite 생성 완료!")
