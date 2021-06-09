import argparse
import cv2
import os
from glob import glob
from tqdm import tqdm


# Parser
parser = argparse.ArgumentParser()
parser.add_argument("--video_path")
args = parser.parse_args()

# Create folder and extract frames
video_path = args.video_path
video_name = video_path.split("/")[-1].split(".")[0] + "_all-frames"
os.mkdir(video_name)
os.system("ffmpeg -i vid.webm {}/%05d.png".format(video_name))
