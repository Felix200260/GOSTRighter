import sys
import time

for i in range(100):
    print('привет мир')
    sys.stdout.flush()
    time.sleep(0.1)  # добавим небольшую задержку, чтобы можно было увидеть вывод в реальном времени
