# GIF and MP4 Creation

Tools to make high quality GIF from video file. The used tool is called [gifski](https://gif.ski/).

## Installation

```bash
snap install ffmpeg gifski
pip install opencv-python tqdm
```

## Run

### Process frames

1. `python video_to_frames.py --video_path <path>`: Extract .png frames from video file.
1. `python crop_frames.py --input_folder <folder> --crop_left <x1_coordinate> --crop_top <y1_coordinate> --crop_right <x2_coordinate> --crop_bottom <y2_coordinate>`: Optional to crop. x2 and y2 can be negative.
1. `python remove_frames.py --input_folder <folder> --start_frame <start_frame_number> --end_frame <end_frame_number>`: Remove every second frame from video between start frame and end frame. You can iterate this step multiple times.

### Create GIF

```bash
gifski -o file.gif frames_folder/* --height 540 --fps 20 --quality 100
```

### Create MP4

```bash
ffmpeg -y -pattern_type glob -framerate 20 -f image2 -i 'frames/*' -vf format=yuv420p,scale='-1:1080' -c:v libx264 -profile:v high -crf:v 18 video.mp4
```
