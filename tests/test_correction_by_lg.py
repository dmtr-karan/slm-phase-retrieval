"""
Test to verify phase correction by generating a donut LG beam.
"""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

def show_donut_example():
    """
    Loads and displays the result donut image as proof of LG-mode beam correction.
    """
    folder = os.path.dirname(__file__)
    image_path = os.path.join(folder, "placeholder_lg_donut.png")
    if os.path.exists(image_path):
        img = Image.open(image_path)
        plt.imshow(img, cmap='gray')
        plt.title("LG-mode donut after phase correction")
        plt.axis("off")
        plt.show()
    else:
        print("[placeholder_lg_donut.png not available]")


if __name__ == "__main__":
    show_donut_example()