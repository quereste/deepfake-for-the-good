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


def prompt_user():
    """
    Prompts the user to continue or exit the process.
    """
    while True:
        choice = input("Do you want to continue with the next steps? (Y/N): ").strip().lower()
        if choice in ['y', 'n']:
            return choice == 'y'
        print("Invalid input. Please enter 'Y' to continue or 'N' to stop.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Automate execution of multiple scripts.")
    # Required parameters
    parser.add_argument("--video_path", type=str, help="Path to the input video.")
    parser.add_argument("--target_folder", type=str, help="Path to the target folder.")
    parser.add_argument("--prompt", type=str, help="Prompt for guiding the process.")

    # Shared optional parameters
    parser.add_argument("--fps", type=int, help="Frames per second.")
    parser.add_argument("--batch_size", type=int, help="Batch size for processing.")
    parser.add_argument("--sides", type=int, help="Sides parameter.")
    parser.add_argument("--resolution", type=int, help="Height resolution for frames.")
    parser.add_argument("--max_frames", type=int, help="Maximum number of frames.")
    parser.add_argument("--border_frames", type=int, help="Number of border frames.")
    parser.add_argument("--ebsynth_mode", type=bool, help="Ebsynth mode toggle.")
    parser.add_argument("--output_resolution", type=int, help="Output resolution for EbSynth.")

    args = parser.parse_args()

    # Paths to scripts
    current_dir = os.path.dirname(os.path.abspath(__file__))
    scripts_phase_1 = [
        os.path.join(current_dir, "preprocess_video.py"),
        os.path.join(current_dir, "process_collage.py"),
        os.path.join(current_dir, "prepare_ebsynth.py"),
    ]
    scripts_phase_2 = [
        os.path.join(current_dir, "recombine_ebsynth.py"),
        os.path.join(current_dir, "cut_alpha_split.py"),
        os.path.join(current_dir, "gs.bat"),
        os.path.join(current_dir, "join_video.py"),
    ]

    # Shared parameters
    shared_params = {
        "fps": args.fps,
        "batch_size": args.batch_size,
        "sides": args.sides,
        "resolution": args.resolution,
        "max_frames": args.max_frames,
        "border_frames": args.border_frames,
        "ebsynth_mode": args.ebsynth_mode,
    }
    shared_params = {k: v for k, v in shared_params.items() if v is not None}  # Remove None values

    # Run phase 1 scripts
    for script in scripts_phase_1:
        script_args = []
        if "preprocess_video.py" in script:
            script_args.extend(["--video_path", args.video_path, "--target_folder", args.target_folder])
        elif "process_collage.py" in script:
            script_args.extend(["--target_folder", args.target_folder, "--prompt", args.prompt])
        elif "prepare_ebsynth.py" in script:
            script_args.extend(["--target_folder", args.target_folder])
            if args.output_resolution:
                script_args.extend(["--output_resolution", str(args.output_resolution)])
        # Add shared parameters
        for key, value in shared_params.items():
            script_args.extend([f"--{key}", str(value)])
        run_script(script, script_args)

    # Ask the user whether to proceed with phase 2
    if not prompt_user():
        print("Process terminated by the user.")
        sys.exit(0)

    # Run phase 2 scripts
    for script in scripts_phase_2:
        script_args = []
        if "cut_alpha_split.py" in script or "recombine_ebsynth.py" in script or "join_video.py" in script:
            script_args.extend(["--target_folder", args.target_folder])
        elif "gs.bat" in script:
            script_args.append(args.target_folder)
        run_script(script, script_args, shell=True if script.endswith(".bat") else False)

    print("All scripts executed successfully.")


if __name__ == "__main__":
    main()