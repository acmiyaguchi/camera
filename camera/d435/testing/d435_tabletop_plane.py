"""

    @brief:     The demo of the tabletop plane estimator on the Realsense d435

    @author:    Yiye Chen
    @date:      10/26/2021

"""

from struct import error
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import cv2

import camera.d435.d435_runner as d435
import camera.tabletop.tabletop_plane as tabletop_plane
from camera.utils.display import display_rgb_dep_plt

import camera.utils.display as display

# The D435 starter
d435_configs = d435.D435_Configs(
    W_dep=1280,
    H_dep=720,
    W_color=1920,
    H_color=1080,
    exposure = 100,
    gain = 50
)

d435_starter = d435.D435_Runner(d435_configs)

# The tabletop plane estimator
tpEstimator = tabletop_plane.tabletopPlaneEstimator(
    intrinsic=d435_starter.intrinsic_mat
)

# get started
while(True):
    rgb, dep, success = d435_starter.get_frames()
    #print("The camera gain: {}. The camera exposure: {}".format(d435_starter.get("gain"), d435_starter.get("exposure")))
    if not success:
        print("Cannot get the camera signals. Exiting...")
        exit()

    display.display_rgb_dep_cv(rgb, dep, ratio=0.5, \
        window_name="THe camera signals. (color-scaled depth). Press \'q\' to exit")

    opKey = cv2.waitKey(1)
    if opKey == ord('q'):
        break
    elif opKey == ord('c'):
        error_map = tpEstimator.measure_plane(depth_map=dep)
        tpEstimator.vis_plane(rgb=rgb) 

        # visualize the error map
        plt.figure()
        plt.title("The error map")
        ax = plt.subplot()
        im = ax.imshow(error_map)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im, cax=cax)
        plt.show()

        exit()
