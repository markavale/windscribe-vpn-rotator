from windscribe_singleton import WindscribeSingleton
import time
import random

def main():
    app = WindscribeSingleton()
    app.connect()
    for _ in range(20):
        app.reboot()
        time.sleep(random.uniform(0.5, 1.5))


if __name__ == "__main__":
    main()