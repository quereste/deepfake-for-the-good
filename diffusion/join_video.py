import os
import subprocess
import sys
import argparse

def combine_images_to_mp4(base_folder):
    # Path to images inside the specified folder
    images_path = os.path.join(base_folder, r"gs\gaussian_white\test\ours_30000\renders")
    
    # Check if the path exists
    if not os.path.exists(images_path):
        raise FileNotFoundError(f"Image path does not exist: {images_path}")
    
    # Folder name and output path for the result
    base_name = os.path.basename(os.path.normpath(base_folder))
    output_folder = os.path.join(os.path.dirname(base_folder))
    output_file = os.path.join(output_folder, f"{base_name}.mp4")
    
    # Create the `ultimate` folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # ffmpeg command to combine images
    ffmpeg_command = [
        "ffmpeg",
        "-hwaccel", "cuda",                    # CUDA hardware acceleration
        "-framerate", "30",                    # Frame rate
        "-start_number", "0",                  # Specify the starting file number
        "-i", os.path.join(images_path, "%05d.png"),  # Input images (00000.png, 00001.png, ...)
        "-c:v", "libx264",                     # H.264 codec (universal)
        "-preset", "fast",                     # Speed preset
        "-pix_fmt", "yuv420p",                 # Pixel format for compatibility
        output_file                            # Output file
]
    # Execute the command
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Video successfully created: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing ffmpeg: {e}")
    except FileNotFoundError:
        print("Error: ffmpeg not found. Make sure it is installed and available in the PATH.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recombine frames back to video")
    parser.add_argument('--target_folder', type=str, required=True, help='Path to the target folder.')
    args = parser.parse_args()

    base_folder = args.target_folder
    combine_images_to_mp4(base_folder)
