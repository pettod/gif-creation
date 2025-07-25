import argparse
import os


# Parser
parser = argparse.ArgumentParser()
parser.add_argument("--video_path")
args = parser.parse_args()

# Create folder and extract frames
video_path = args.video_path
video_name = video_path.split("/")[-1].split(".")[0] + "_all-frames"
os.makedirs(video_name, exist_ok=True)
os.system("ffmpeg -i {} {}/%05d.png".format(video_path, video_name))
