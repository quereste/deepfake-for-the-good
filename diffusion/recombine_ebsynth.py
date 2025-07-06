import argparse
import os
import sys
import re

# Add the TemporalKit directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, "extensions", "TemporalKit")))
sys.path.append(os.path.abspath(os.path.join(current_dir, "extensions", "TemporalKit", "scripts")))

# Import necessary modules
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

        # Convert strings to appropriate types, handling 'None'
        fps = int(fps_line) if fps_line != 'None' else None
        sides = int(sides_line) if sides_line != 'None' else None
        batch_size = int(batch_size_line) if batch_size_line != 'None' else None
        max_frames = int(max_frames_line) if max_frames_line != 'None' else None
        if border is None:
            border = int(border_line) if border_line != 'None' else None
    return fps, sides, batch_size, video_path, max_frames, border

def recombine_ebsynth(input_folder, fps, border_frames, batch_size):
    if os.path.exists(os.path.join(input_folder, "keys")):
        output_video = ebsynth.crossfade_folder_of_folders(
            input_folder,
            fps=fps,
            return_generated_video_path=True
        )
        print(f"Generated video: {output_video}")
    else:
        generated_videos = []
        pattern = r'^\d+$'
        all_dirs = os.listdir(input_folder)
        numeric_dirs = sorted([d for d in all_dirs if re.match(pattern, d)], key=lambda x: int(x))
        for d in numeric_dirs:
            folder_loc = os.path.join(input_folder, d)
            new_video = ebsynth.crossfade_folder_of_folders(folder_loc, fps=fps)
            generated_videos.append(new_video)
        overlap_data_path = os.path.join(input_folder, "transition_data.txt")
        with open(overlap_data_path, "r") as f:
            merge = str(f.readline().strip())
        overlap_indices = []
        int_list = eval(merge)
        for num in int_list:
            overlap_indices.append(int(num))
        output_video = sd_utility.crossfade_videos(
            video_paths=generated_videos,
            fps=fps,
            overlap_indexes=overlap_indices,
            num_overlap_frames=border_frames,
            output_path=os.path.join(input_folder, "output.mp4")
        )
        print(f"Generated video: {output_video}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_folder", type=str, required=True, help="Path to the project folder")
    args = parser.parse_args()

    # Read settings from the saved file
    fps, per_side, batch_size, video_path, max_frames, border_frames = update_settings_from_file(args.target_folder)

    # Check values for None and set default values if necessary
    if fps is None:
        fps = 30  # Set a default value or raise an error
    if border_frames is None:
        border_frames = 0  # Or set a default value

    # Run the recombination function
    recombine_ebsynth(
        input_folder=args.target_folder,
        fps=fps,
        border_frames=border_frames,
        batch_size=batch_size
    )
