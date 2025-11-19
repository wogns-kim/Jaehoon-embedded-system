import time
import board
import adafruit_dht

# GPIO 4번 핀에 연결된 DHT11 센서 설정
# (만약 센서가 DHT22라면 아래 DHT11을 DHT22로만 바꾸면 됩니다)
dhtDevice = adafruit_dht.DHT11(board.D4)

print("온습도 측정을 시작합니다... (종료하려면 Ctrl+C)")

while True:
    try:
        # 센서에서 온도와 습도 읽기
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        
        print(f"온도: {temperature_c:.1f}°C / 습도: {humidity}%")

    except RuntimeError as error:
        # 센서 읽기 실패 시 에러 메시지 출력 (자주 발생할 수 있음)
        # DHT 센서는 타이밍이 민감해서 가끔 읽기 실패가 뜸 (정상)
        print(f"센서 읽기 실패 (재시도 중): {error.args[0]}")
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)