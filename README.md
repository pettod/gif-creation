# GIF Creation

Tools to make high quality GIF from video file. Used tool is `gifski`. Read more details from [https://gif.ski/](https://gif.ski/).

## Installation

```bash
snap install ffmpeg gifski
pip install opencv-python
```

## Run Steps

1. `python video_to_frames.py --video_path <path>`: Extract .png frames from video file.
1. `python crop_frames.py --input_folder <folder> --crop_left <x1 coordinate> --crop_top <y1 coordinate> --crop_right <x2 coordinate> --crop_bottom <y2 coordinate>`: Optional to crop. x2 and y2 can be negative.
1. `python remove_frames.py --input_folder <folder> --start_frame <start_frame_number> --end_frame <end_frame_number>`: Remove every second frame from video between start frame and end frame. You can iterate this step multiple times.
1. `gifski -o file.gif frames_folder/* --height 540 --fps 20 --quality 80`
