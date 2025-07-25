import cv2
import os
import argparse
import glob

class FrameViewer:
    def __init__(self, frames_path):
        self.frames_path = frames_path
        self.frame_files = sorted(glob.glob(os.path.join(frames_path, "*.png")))
        
        if not self.frame_files:
            raise ValueError(f"No PNG frames found in {frames_path}")
        
        self.current_frame_idx = 0
        self.total_frames = len(self.frame_files)
        self.mouse_x = 0
        self.mouse_y = 0
        
        print(f"Loaded {self.total_frames} frames from {frames_path}")
        print("Controls:")
        print("  'o' - Forward 100 frames")
        print("  'u' - Backward 100 frames")
        print("  'j' - Backward 10 frames")
        print("  'l' - Forward 10 frames")
        print("  Left/Right arrows - Forward/Backward 1 frame")
        print("  'q' or ESC - Quit")
        print("  Click - Print frame number and coordinates")
    
    def mouse_callback(self, event, x, y, flags, param):
        self.mouse_x = x
        self.mouse_y = y
        
        if event == cv2.EVENT_LBUTTONDOWN:
            frame_number = self.current_frame_idx + 1
            print(f"Frame: {frame_number}, Coordinates: ({x}, {y})")
    
    def load_frame(self):
        frame_path = self.frame_files[self.current_frame_idx]
        frame = cv2.imread(frame_path)
        if frame is None:
            raise ValueError(f"Could not load frame: {frame_path}")
        return frame
    
    def draw_overlays(self, frame):
        # Create a copy to avoid modifying original
        display_frame = frame.copy()
        
        # Frame number in top left
        frame_number = self.current_frame_idx + 1
        frame_text = f"Frame: {frame_number}/{self.total_frames}"
        cv2.putText(display_frame, frame_text, (10, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        
        # Mouse coordinates in top right
        coord_text = f"({self.mouse_x}, {self.mouse_y})"
        text_size = cv2.getTextSize(coord_text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
        text_x = display_frame.shape[1] - text_size[0] - 10
        cv2.putText(display_frame, coord_text, (text_x, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        
        return display_frame
    
    def navigate_frames(self, step):
        self.current_frame_idx = (self.current_frame_idx + step) % self.total_frames
    
    def run(self):
        cv2.namedWindow('Frame Viewer', cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback('Frame Viewer', self.mouse_callback)
        
        while True:
            # Load and display current frame
            frame = self.load_frame()
            display_frame = self.draw_overlays(frame)
            cv2.imshow('Frame Viewer', display_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == 27:  # 'q' or ESC
                break
            elif key == ord('q'):  # Backward 100 frames
                self.navigate_frames(-100)
            elif key == ord('e'):  # Forward 100 frames
                self.navigate_frames(100)
            elif key == ord('s'):  # Backward 10 frames
                self.navigate_frames(-10)
            elif key == ord('w'):  # Forward 10 frames
                self.navigate_frames(10)
            elif key == ord('a'):  # Backward 1 frame
                self.navigate_frames(-1)
            elif key == ord('d'):  # Forward 1 frame
                self.navigate_frames(1)
        
        cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description='Navigate through video frames')
    parser.add_argument('--frames_path', required=True, 
                       help='Path to directory containing frame images')
    args = parser.parse_args()
    
    if not os.path.exists(args.frames_path):
        print(f"Error: Path {args.frames_path} does not exist")
        return
    
    try:
        viewer = FrameViewer(args.frames_path)
        viewer.run()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 