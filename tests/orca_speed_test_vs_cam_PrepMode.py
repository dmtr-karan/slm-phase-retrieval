import time
from orca.orca_autonoma import LiveHamamatsu

def main():
    cam = LiveHamamatsu(initCam=True, came_numb=0, trig_mODe=1, exposure=0.05)
    cam.num = 1
    cam.prep_acq()

    start = time.time()
    cam.take_image()
    end = time.time()

    print("Time for one image acquisition: {:.3f} s".format(end - start))

if __name__ == "__main__":
    main()