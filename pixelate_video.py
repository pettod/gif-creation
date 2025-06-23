import cv2
import os
import subprocess
import tempfile

# === SETTINGS ===
input_path = 'input.mp4'
output_path = input_path.replace(".mp4", "_pixelated.mp4")
pixel_size = 10  # Larger = blockier pixelation
debug = False
use_ffmpeg = True  # Set to True for better compression

# Start values for the pixelation
x0 = 1214
x1 = 2233
y0 = 1418
y1 = 1451
step = (y1 - y0) + 8

# Format: [[frame start index, frame end index], (x1, y1, x2, y2)]
frame_regions = [
    [[2635, 2709], (x0, y0, x1, y1)],
    [[2710, 2871], (x0, y0 - 1*step, x1, y1 - 1*step)],
    [[2872, 2872], (x0, y0 - 2*step, x1, y1 - 2*step)],
    [[2873, 2921], (x0, y0 - 3*step, x1, y1 - 3*step)],
    [[2922, 3069], (x0, y0 - 4*step, x1, y1 - 4*step)],
]

def pixelate_region(image, x1, y1, x2, y2, pixel_size):
    roi = image[y1:y2, x1:x2]
    h, w = roi.shape[:2]
    temp = cv2.resize(roi, (w // pixel_size, h // pixel_size), interpolation=cv2.INTER_LINEAR)
    pixelated = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
    if debug:
        pixelated = cv2.rectangle(pixelated, (0, 0), (x2-x1, y2-y1), (0, 0, 255), -1)
    image[y1:y2, x1:x2] = pixelated
    return image

def is_frame_in_range(frame_num, frame_ranges):
    """Check if current frame number is within any of the specified ranges"""
    for frame_range, coords in frame_ranges:
        start_frame, end_frame = frame_range
        if start_frame <= frame_num <= end_frame:
            return True, coords
    return False, None

def process_with_ffmpeg():
    """Process video using FFmpeg for optimal compression"""
    print("Processing with FFmpeg for optimal compression...")
    
    # Create temporary directory for frames
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract and process frames
        cap = cv2.VideoCapture(input_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        frame_num = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Check if current frame needs pixelation
            should_pixelate, coords = is_frame_in_range(frame_num, frame_regions)
            
            if should_pixelate:
                x1, y1, x2, y2 = coords
                frame = pixelate_region(frame, x1, y1, x2, y2, pixel_size)
                print(f"Pixelating frame {frame_num}: ({x1}, {y1}, {x2}, {y2})")

            # Save frame as image
            frame_path = os.path.join(temp_dir, f"frame_{frame_num:06d}.jpg")
            cv2.imwrite(frame_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
            frame_num += 1

        cap.release()
        
        # Use FFmpeg to create compressed video
        input_pattern = os.path.join(temp_dir, "frame_%06d.jpg")
        ffmpeg_cmd = [
            'ffmpeg', '-y',  # Overwrite output
            '-framerate', str(fps),
            '-i', input_pattern,
            '-c:v', 'libx264',  # H.264 codec
            '-preset', 'slower',  # Better compression preset
            '-crf', '28',  # Higher CRF for more compression (was 23)
            '-maxrate', '2M',  # Maximum bitrate
            '-bufsize', '4M',  # Buffer size
            '-pix_fmt', 'yuv420p',  # Pixel format for compatibility
            output_path
        ]
        
        print("Running FFmpeg compression...")
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ FFmpeg compression completed successfully!")
        else:
            print(f"❌ FFmpeg error: {result.stderr}")
            return False
    
    return True

def main():
    if use_ffmpeg:
        # Check if FFmpeg is available
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            if process_with_ffmpeg():
                return
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("FFmpeg not found, falling back to OpenCV...")
    
    # === OPEN INPUT VIDEO ===
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Use H.264 codec for better compression
    if use_ffmpeg:
        fourcc = cv2.VideoWriter_fourcc(*'H264')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # If H.264 is not available, try other codecs
        if not out.isOpened():
            print("H.264 not available, trying XVID...")
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_path.replace('.mp4', '.avi'), fourcc, fps, (width, height))
        
        if not out.isOpened():
            print("XVID not available, trying mp4v...")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        if not out.isOpened():
            print("Error: Could not open video writer")
            return

        print(f"Video properties: {width}x{height} @ {fps}fps")
        print(f"Using codec: {chr(fourcc & 0xFF) + chr((fourcc >> 8) & 0xFF) + chr((fourcc >> 16) & 0xFF) + chr((fourcc >> 24) & 0xFF)}")

    # === PROCESS VIDEO ===
    frame_num = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Check if current frame needs pixelation
        should_pixelate, coords = is_frame_in_range(frame_num, frame_regions)
        
        if should_pixelate:
            x1, y1, x2, y2 = coords
            frame = pixelate_region(frame, x1, y1, x2, y2, pixel_size)
            print(f"Pixelating frame {frame_num}: ({x1}, {y1}, {x2}, {y2})")

        out.write(frame)
        frame_num += 1

    cap.release()
    out.release()
    print("✅ Done! Pixelated frames saved to:", output_path)

main()
