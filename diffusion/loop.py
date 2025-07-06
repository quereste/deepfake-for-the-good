import subprocess
import os
import sys


def run_script(script_path, args, shell=False):
    """
    Executes a Python script or batch file with the specified arguments.
    """
    if script_path.endswith(".py"):
        command = [sys.executable, script_path] + args
    else:  # Assume it's a batch file
        command = [script_path] + args
    try:
        subprocess.run(command, check=True, shell=shell)
        print(f"Successfully executed: {script_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_path}: {e}")
        sys.exit(1)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Automate iterative execution of a script.")
    # Required parameters
    parser.add_argument("--main_folder", type=str, help="Main folder for storing iterations.")
    parser.add_argument("--prompt", type=str, help="Prompt for guiding the process.")
    # Optional parameters
    parser.add_argument("--start", type=int, default=0, help="Starting iteration index (default: 0).")
    parser.add_argument("--end", type=int, default=1, help="Ending iteration index (default: 1).")
    parser.add_argument("--fps", type=int, help="Frames per second.")
    parser.add_argument("--batch_size", type=int, help="Batch size for processing.")
    parser.add_argument("--sides", type=int, help="Sides parameter.")
    parser.add_argument("--resolution", type=int, help="Height resolution for frames.")
    parser.add_argument("--max_frames", type=int, help="Maximum number of frames.")
    parser.add_argument("--border_frames", type=int, help="Number of border frames.")
    parser.add_argument("--ebsynth_mode", type=bool, help="Ebsynth mode toggle.")
    parser.add_argument("--output_resolution", type=int, help="Output resolution for EbSynth.")

    args = parser.parse_args()

    # Path to the original script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    original_script = os.path.join(current_dir, "automate_process.py")

    # Shared optional parameters
    shared_params = {
        "fps": args.fps,
        "batch_size": args.batch_size,
        "sides": args.sides,
        "resolution": args.resolution,
        "max_frames": args.max_frames,
        "border_frames": args.border_frames,
        "ebsynth_mode": args.ebsynth_mode,
        "output_resolution": args.output_resolution,
    }
    shared_params = {k: v for k, v in shared_params.items() if v is not None}  # Remove None values

    # Perform iterations
    for i in range(args.start + 1, args.end + 1):
        video_path = os.path.join(args.main_folder, f"iter{i - 1}.mp4")
        target_folder = os.path.join(args.main_folder, f"iter{i}")

        # Check if the video exists
        if not os.path.exists(video_path):
            print(f"Error: Video file {video_path} does not exist. Skipping iteration {i}.")
            continue

        # Build arguments for the original script
        script_args = [
            "--video_path", video_path,
            "--target_folder", target_folder,
            "--prompt", args.prompt,
        ]
        for key, value in shared_params.items():
            script_args.extend([f"--{key}", str(value)])

        print(f"\nStarting iteration {i}...")
        print(f"Video Path: {video_path}")
        print(f"Target Folder: {target_folder}")

        # Execute the original script
        run_script(original_script, script_args)

    print(f"\nAll iterations from {args.start} to {args.end} completed successfully.")


if __name__ == "__main__":
    main()
