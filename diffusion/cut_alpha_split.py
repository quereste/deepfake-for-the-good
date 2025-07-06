import os
import subprocess
from PIL import Image
import random
import json
import shutil
import argparse

def main():
    parser = argparse.ArgumentParser(description="Process video and prepare data for training.")
    parser.add_argument('--target_folder', type=str, required=True, help='Path to the target folder.')
    args = parser.parse_args()

    target_folder = args.target_folder
    project_folder = os.path.abspath(os.path.join(target_folder, '..'))  # One folder above the target_folder

    crossfade_video = os.path.join(target_folder, 'crossfade.mp4')
    gs_folder = os.path.join(target_folder, 'gs')
    train_main_folder = os.path.join(gs_folder, 'train_main')

    # Ensure that the gs/train_main folder exists
    os.makedirs(train_main_folder, exist_ok=True)

    # Step 1: Split video into frames
    print("Splitting crossfade.mp4 into frames...")
    ffmpeg_command = [
        'ffmpeg',
        '-hwaccel', 'cuda',  # Use 'cuda' or 'nvdec' depending on your system and ffmpeg build
        '-i', crossfade_video,
        '-vf', 'fps=30',
        '-start_number', '0',  # Numbering starts from 0
        os.path.join(train_main_folder, 'r_%d.png')  # Use %d without leading zeros
    ]

    # Run the command
    subprocess.run(ffmpeg_command)
    print("Frames extracted.")

    # Step 2: Copy alpha channels
    print("Copying alpha channels...")
    source_dir = os.path.join(project_folder, 'train_main')  # Source images with alpha channel
    dest_dir = train_main_folder  # Extracted frames

    # Ensure that the destination folder exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # List all PNG files in the destination folder (extracted frames)
    png_files = [f for f in os.listdir(dest_dir) if f.endswith('.png')]

    for file_name in png_files:
        source_path = os.path.join(source_dir, file_name)
        dest_path = os.path.join(dest_dir, file_name)

        # Check if the source image exists
        if not os.path.exists(source_path):
            print(f"Source image not found: {source_path}")
            continue

        # Open the source and destination images
        source_image = Image.open(source_path).convert("RGBA")
        dest_image = Image.open(dest_path).convert("RGBA")

        # Extract the alpha channel from the source image
        source_alpha = source_image.split()[-1]

        # Replace the alpha channel in the destination image
        dest_image.putalpha(source_alpha)

        # Save the updated image
        dest_image.save(dest_path)

    print("Alpha channels copied successfully.")

    # Step 3: Split data into train, val, and test sets
    print("Splitting data into train, val, and test sets...")
    base_dir = train_main_folder  # Folder gs/train_main

    train_dir = os.path.join(gs_folder, "train")
    test_dir = os.path.join(gs_folder, "test")
    val_dir = os.path.join(gs_folder, "val")

    # Define proportions
    train_prop = 0.8
    test_prop = 0.05
    val_prop = 0.15  # Proportions must sum up to 1

    # Get all PNG files from the train_main folder
    png_files = [f for f in os.listdir(base_dir) if f.endswith('.png')]
    total_files = len(png_files)

    # Shuffle the file list for random distribution
    random.shuffle(png_files)

    # Calculate the number of files for each set
    train_count = int(total_files * train_prop)
    test_count = int(total_files * test_prop)
    val_count = total_files - train_count - test_count  # Remaining files go to val

    # Split files according to proportions
    train_files = png_files[:train_count]
    test_files = png_files[train_count:train_count + test_count]
    val_files = png_files[train_count + test_count:]

    # Function to copy files from source to destination directory
    def copy_files(file_list, source_dir, dest_dir):
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        for file in file_list:
            shutil.copy(os.path.join(source_dir, file), os.path.join(dest_dir, file))

    # Copy files to respective directories
    copy_files(train_files, base_dir, train_dir)  # Copy files to train folder
    copy_files(test_files, base_dir, test_dir)    # Copy files to test folder
    copy_files(val_files, base_dir, val_dir)      # Copy files to val folder

    # Function to create new JSON files for train, test, and val sets
    def create_json(json_path, new_file_list, folder_name, main_json_path):
        # Load data from the main JSON file
        with open(main_json_path, 'r') as file:
            data = json.load(file)
        
        # Remove '.png' extension from the file list to match paths in JSON
        new_file_list_no_ext = [os.path.splitext(f)[0] for f in new_file_list]
        
        # Filter frames to include only those present in the new file list
        new_frames = [frame for frame in data['frames'] if os.path.basename(frame['file_path']) in new_file_list_no_ext]

        # Update file paths in JSON data to point to the new folder
        for frame in new_frames:
            frame['file_path'] = f"./{folder_name}/" + os.path.basename(frame['file_path'])
        
        # Create a new JSON data structure
        new_data = {
            "camera_angle_x": data.get('camera_angle_x', 0.6911112070083618),
            "frames": new_frames
        }

        # Write new data to the JSON file
        with open(json_path, 'w') as file:
            json.dump(new_data, file, indent=4)

    # Path to the main JSON file
    main_json_path = os.path.join(project_folder, "transforms_train_main.json")

    # Create new JSON files for train, test, and val sets
    create_json(os.path.join(gs_folder, "transforms_train.json"), train_files, 'train', main_json_path)
    create_json(os.path.join(gs_folder, "transforms_test.json"), test_files, 'test', main_json_path)
    create_json(os.path.join(gs_folder, "transforms_val.json"), val_files, 'val', main_json_path)

    print("Files copied and JSON files created successfully.")

if __name__ == "__main__":
    main()
