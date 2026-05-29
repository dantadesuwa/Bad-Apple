import cv2
import json
import numpy as np
import math

def bake_video():
    video_path = 'bad_apple.mp4'
    output_path = 'frames.json'
    
    print(f"Opening '{video_path}'...")
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Calculate dimensions
    width = 110
    orig_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    orig_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    height = int((width / orig_w) * orig_h * 0.5)
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames_data = {
        "cols": width,
        "rows": height,
        "frames": []
    }

    print(f"Processing {total_frames} frames. This might take a minute...")
    
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Resize and convert to ASCII blocks
        small = cv2.resize(frame, (width, height))
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
        
        chars = np.where(thresh > 127, '█', ' ')
        ascii_frame = '\n'.join(''.join(row) for row in chars)
        
        frames_data["frames"].append(ascii_frame)
        
        count += 1
        if count % 300 == 0:
            print(f"Processed {count}/{total_frames} frames...")

    cap.release()
    
    print("Writing to frames.json...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(frames_data, f)
        
    print(f"Done! Successfully baked {len(frames_data['frames'])} frames into {output_path}.")

if __name__ == '__main__':
    bake_video()