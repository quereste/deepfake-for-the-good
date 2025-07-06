import argparse
import os
import shutil
import sys

# Add the TemporalKit directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, "extensions", "TemporalKit")))
sys.path.append(os.path.abspath(os.path.join(current_dir, "extensions", "TemporalKit", "scripts")))

from scripts.Ebsynth_Processing import sort_into_folders

from extensions.TemporalKit.scripts.Berry_Method import generate_squares_to_folder

def preprocess_video(video_path, target_folder, fps, batch_size, sides, resolution, max_frames, border_frames, ebsynth_mode, max_frames_to_save):
    # Create target folder if it doesn't exist
    os.makedirs(target_folder, exist_ok=True)

    # Copy input video to the target folder
    target_video_path = os.path.join(target_folder, "input_video.mp4")
    shutil.copy(video_path, target_video_path)

    print("Generating squares and saving them in the appropriate directories...")
    generate_squares_to_folder(
        video_path=target_video_path,
        fps=fps,
        batch_size=batch_size,
        resolution=resolution,
        size_size=sides,
        max_frames=max_frames,
        output_folder=target_folder,
        border=border_frames,
        ebsynth_mode=ebsynth_mode,
        max_frames_to_save=max_frames_to_save
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", type=str, help="Path to the video to be pre-processed")
    parser.add_argument("--target_folder", type=str, required=True, help="Target folder to save pre-processed frames")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second")
    parser.add_argument("--batch_size", type=int, default=8, help="Frames per keyframe")
    parser.add_argument("--sides", type=int, default=4, help="Sides parameter")
    parser.add_argument("--resolution", type=int, default=1536, help="Height resolution for frames")
    parser.add_argument("--max_frames", type=int, default=144, help="Maximum number of frames")
    parser.add_argument("--border_frames", type=int, default=2, help="Number of border frames")
    parser.add_argument("--ebsynth_mode", type=bool, default=True, help="Ebsynth Mode")
    parser.add_argument("--max_frames_to_save", type=int, default=None, help="Maximum number of frames to save")

    args = parser.parse_args()
    preprocess_video(args.video_path, args.target_folder, args.fps, args.batch_size, args.sides, args.resolution, args.max_frames, args.border_frames, args.ebsynth_mode, args.max_frames_to_save)
