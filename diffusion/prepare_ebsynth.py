import argparse
import os
import sys
import re
import numpy as np
from PIL import Image

# Add the TemporalKit directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, "extensions", "TemporalKit")))
sys.path.append(os.path.abspath(os.path.join(current_dir, "extensions", "TemporalKit", "scripts")))

# Import necessary modules from TemporalKit
import Ebsynth_Processing as ebsynth
import berry_utility as sd_utility

def update_settings_from_file(folderpath):
    read_path = os.path.join(folderpath, "batch_settings.txt")
    border = None
    print(f"batch settings exists = {os.path.exists(read_path)}")
    if not os.path.exists(read_path):
        read_path = os.path.join(folderpath, "0", "batch_settings.txt")
        video_path = os.path.join(folderpath, "main_video.mp4")
        transition_data_path = os.path.join(folderpath, "transition_data.txt")
        if os.path.exists(transition_data_path):
            with open(transition_data_path, "r") as b:
                merge = str(b.readline().strip())
                border_line = b.readline().strip()
                if border_line == 'None':
                    border = None
                else:
                    border = int(border_line)
    else:
        video_path = os.path.join(folderpath, "input_video.mp4")
    print(f"reading path at {read_path}")
    with open(read_path, "r") as f:
        fps_line = f.readline().strip()
        sides_line = f.readline().strip()
        batch_size_line = f.readline().strip()
        video_path_in_settings = f.readline().strip()
        max_frames_line = f.readline().strip()
        border_line = f.readline().strip()

        # Convert strings to the appropriate types, handling 'None'
        fps = int(fps_line) if fps_line != 'None' else None
        sides = int(sides_line) if sides_line != 'None' else None
        batch_size = int(batch_size_line) if batch_size_line != 'None' else None
        max_frames = int(max_frames_line) if max_frames_line != 'None' else None
        if border is None:
            border = int(border_line) if border_line != 'None' else None
    return fps, sides, batch_size, video_path, max_frames, border

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]

def read_images_folder(folder_path):
    images = []
    filenames = os.listdir(folder_path)
    
    # Sort files based on the order of numbers in their names
    filenames.sort(key=natural_keys)

    for filename in filenames:
        # Check if the file is an image
        if (filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg')) and (not re.search(r'-\d', filename)):
            if re.match(r".*(input).*", filename):
                img = Image.open(os.path.join(folder_path, filename))
                images.append(np.array(img))
            else:
                print(f"[{filename}] File name must contain \"input\". Skipping.")
    return images

def post_process_ebsynth(input_folder, video, fps, per_side, output_resolution, batch_size, max_frames, border_frames):
    input_images_folder = os.path.join(input_folder, "output")
    images = read_images_folder(input_images_folder)
    print(f"Number of images: {len(images)}")
    split_mode = os.path.join(input_folder, "keys")
    if os.path.exists(split_mode):
        ebsynth.sort_into_folders(
            video_path=video,
            fps=fps,
            per_side=per_side,
            batch_size=batch_size,
            _smol_resolution=output_resolution,
            square_textures=images,
            max_frames=max_frames,
            output_folder=input_folder,
            border=border_frames
        )
    else:
        img_folder = os.path.join(input_folder, "output")
        pattern = r'^\d+$'
        all_dirs = os.listdir(input_folder)
        numeric_dirs = sorted([d for d in all_dirs if re.match(pattern, d)], key=lambda x: int(x))
        if max_frames is not None:
            max_frames += border_frames
        for d in numeric_dirs:
            img_names = []
            folder_video = os.path.join(input_folder, d, "input_video.mp4")
            for img_file in os.listdir(img_folder):
                if re.match(f"^{d}and\d+.*\.png$", img_file):
                    img_names.append(img_file)
            print(f"Processing: {os.path.dirname(folder_video)}")
            square_textures = []
            for img_name in sorted(img_names, key=lambda x: int(re.search(r'and(\d+)', img_name).group(1))):
                img = Image.open(os.path.join(input_images_folder, img_name))
                print(f"Saving {os.path.join(input_images_folder, img_name)}")
                square_textures.append(np.array(img))
            ebsynth.sort_into_folders(
                video_path=folder_video,
                fps=fps,
                per_side=per_side,
                batch_size=batch_size,
                _smol_resolution=output_resolution,
                square_textures=square_textures,
                max_frames=max_frames,
                output_folder=os.path.dirname(folder_video),
                border=border_frames
            )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_folder", type=str, required=True, help="Path to the project folder")
    parser.add_argument("--output_resolution", type=int, default=512, help="Output resolution for EbSynth")
    args = parser.parse_args()

    # Read settings from the saved file
    fps, per_side, batch_size, video_path, max_frames, border_frames = update_settings_from_file(args.target_folder)
    output_resolution = args.output_resolution

    input_video = os.path.join(args.target_folder, "input_video.mp4")

    # Run the preparation function
    post_process_ebsynth(
        input_folder=args.target_folder,
        video=input_video,
        fps=fps,
        per_side=per_side,
        output_resolution=output_resolution,
        batch_size=batch_size,
        max_frames=max_frames,
        border_frames=border_frames
    )
