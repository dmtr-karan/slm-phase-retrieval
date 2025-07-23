import time
from slm.slm_hamamatsu import SlmDisplay
import numpy as np

def main():
    slm = SlmDisplay()
    slm.connect()

    dummy_phase = np.random.randint(0, 198, size=(1024, 1272), dtype='uint8')
    start_time = time.time()
    for _ in range(10):
        slm.load_phase(dummy_phase)
    end_time = time.time()

    print("Loaded phase 10 times in {:.2f} seconds".format(end_time - start_time))

if __name__ == "__main__":
    main()