import argparse
import os
import time
from glob import glob
from shutil import copy


def frameNumber(frame_path):
    return int(frame_path.split("/")[-1].split(".")[0])

# Parser
parser = argparse.ArgumentParser()
parser.add_argument("--input_folder")
parser.add_argument("--start_frame", type=int)
parser.add_argument("--end_frame", type=int)
args = parser.parse_args()

# Read arguments
input_folder = args.input_folder
frame_paths = sorted(glob(os.path.join(input_folder, "*")))
start_frame = frameNumber(frame_paths[0]) if args.start_frame is None else args.start_frame
end_frame = frameNumber(frame_paths[-1]) if args.end_frame is None else args.end_frame
timestamp = time.strftime("%H%M%S")
output_folder = input_folder.split("_")[0] + f"_removed-frames-{timestamp}"

# Remove every second frame in the range
os.mkdir(output_folder)
for i in range(len(frame_paths)):
    frame_path = frame_paths[i]
    frame_number = frameNumber(frame_path)
    if i % 2 and frame_number > start_frame and frame_number < end_frame:
        continue
    copy(frame_path, os.path.join(output_folder, input_folder.split("/")[-1]))
