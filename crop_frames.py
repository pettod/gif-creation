import argparse
import cv2
import os
from glob import glob
from tqdm import tqdm


# Parser
parser = argparse.ArgumentParser()
parser.add_argument("--input_folder")
parser.add_argument("--crop_left", type=int, default=0)
parser.add_argument("--crop_top", type=int, default=0)
parser.add_argument("--crop_right", type=int, default=100000000)
parser.add_argument("--crop_bottom", type=int, default=100000000)
args = parser.parse_args()

# Crop
frame_paths = glob(os.path.join(args.input_folder, "*"))
x1 = args.crop_left
y1 = args.crop_top
x2 = args.crop_right
y2 = args.crop_bottom
image = cv2.imread(frame_paths[0])
print("Original image shape: {}".format(image.shape))
print("Croppped image shape: {}".format(image[y1:y2, x1:x2].shape))
for frame_path in tqdm(frame_paths):
    cv2.imwrite(frame_path, cv2.imread(frame_path)[y1:y2, x1:x2])
