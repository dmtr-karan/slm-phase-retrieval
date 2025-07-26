"""
Benchmark test: compare camera acquisition time in streaming (live) vs triggered (single-shot) mode.
"""

from orca.orca_camera import LiveHamamatsu
import time


def test_camera_acquisition_time(live_mode=True, num_frames=5):
    cam = LiveHamamatsu()
    cam.initialize(live_mode=live_mode)

    print(f"Testing camera mode: {'Live streaming' if live_mode else 'Single shot'}")

    start = time.time()
    for _ in range(num_frames):
        cam.capture_frame()
    duration = time.time() - start

    print(f"→ Acquired {num_frames} frames in {duration:.3f} seconds")


if __name__ == "__main__":
    test_camera_acquisition_time(live_mode=True)
    test_camera_acquisition_time(live_mode=False)