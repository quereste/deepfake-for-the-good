import requests
import base64
import os
import argparse
import io
import json
from PIL import Image, PngImagePlugin
from datetime import datetime

def timestamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def encode_file_to_base64(path):
    with open(path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')

def decode_and_save_base64(base64_str, save_path):
    with open(save_path, "wb") as file:
        file.write(base64.b64decode(base64_str))

def call_img2img_api(payload, output_path, server):
    url = f"http://{server}/sdapi/v1/img2img"
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(payload)

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        result = response.json()
        img_str = result['images'][0]
        img_data = base64.b64decode(img_str)
        image = Image.open(io.BytesIO(img_data))
        if 'info' in result:
            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", result['info'])
            image.save(output_path, pnginfo=pnginfo)
        else:
            image.save(output_path)
        print(f"Processed image saved to {output_path}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def main():
    parser = argparse.ArgumentParser(description="Process an image using Stable Diffusion, ControlNet, and Refiner.")
    parser.add_argument("--target_folder", type=str, required=True, help="Path to the project folder.")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt for image generation.")
    parser.add_argument("--negative_prompt", type=str, default="", help="Negative prompt.")
    parser.add_argument("--server", type=str, default="127.0.0.1:7860", help="Address of the Automatic1111 server.")
    args = parser.parse_args()

    # Define paths
    input_image_path = os.path.join(args.target_folder, "input", "input0.png")
    controlnet_image_path = input_image_path  # Use the same image for ControlNet
    output_dir = os.path.join(args.target_folder, "output")
    output_image_path = os.path.join(output_dir, "00000-input0.png")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Check for the input image
    if not os.path.exists(input_image_path):
        print(f"Input image not found: {input_image_path}")
        return

    # Encode images to base64
    init_image_base64 = encode_file_to_base64(input_image_path)
    controlnet_image_base64 = encode_file_to_base64(controlnet_image_path)

    # Form payload
    payload = {
        "init_images": [init_image_base64],
        "resize_mode": 0,
        "denoising_strength": 0.9,
        "image_cfg_scale": 1.5,
        "mask": None,
        "mask_blur": 4,
        "inpainting_fill": 1,
        "inpaint_full_res": False,
        "inpaint_full_res_padding": 32,
        "inpainting_mask_invert": 0,
        "initial_noise_multiplier": 1,
        "prompt": args.prompt,
        "styles": [],
        "seed": -1,
        "subseed": -1,
        "subseed_strength": 0,
        "seed_resize_from_h": -1,
        "seed_resize_from_w": -1,
        "sampler_name": "DPM++ 2M",
        "batch_size": 1,
        "n_iter": 1,
        "steps": 30,
        "cfg_scale": 9,
        "width": 1536,
        "height": 1536,
        "restore_faces": False,
        "tiling": False,
        "do_not_save_samples": False,
        "do_not_save_grid": False,
        "negative_prompt": args.negative_prompt,
        "eta": 0,
        "s_churn": 0,
        "s_tmax": None,
        "s_tmin": 0,
        "s_noise": 1,
        "override_settings": {
            "samples_filename_pattern": "input0",
            "save_to_dirs": False
        },
        "override_settings_restore_afterwards": True,
        "sampler_index": "DPM++ 2M",
        "script_name": None,
        "send_images": True,
        "save_images": False,
        "alwayson_scripts": {
            "ControlNet": {
                "args": [
                    {
                        "enabled": True,
                        "input_image": controlnet_image_base64,
                        "mask": None,
                        "module": "canny",
                        "model": "control_v11p_sd15_canny [d14c016b]",
                        "weight": 1.0,
                        "resize_mode": "Crop and Resize",
                        "low_vram": True,
                        "processor_res": 512,
                        "threshold_a": 100.0,
                        "threshold_b": 200.0,
                        "guidance_start": 0.0,
                        "guidance_end": 1.0,
                        "control_mode": "ControlNet is more important",
                        "pixel_perfect": True,
                        "advanced_weighting": None,
                        "animatediff_batch": False,
                        "batch_image_files": [],
                        "batch_images": os.path.join(args.target_folder, "input"),
                        "batch_keyframe_idx": None,
                        "batch_mask_dir": None,
                        "batch_modifiers": [],
                        "effective_region_mask": None,
                        "hr_option": "Both",
                        "inpaint_crop_input_image": True,
                        "input_mode": "simple",
                        "ipadapter_input": None,
                        "is_ui": True,
                        "loopback": False,
                        "output_dir": os.path.join(args.target_folder, "output"),
                        "pulid_mode": "Fidelity",
                        "save_detected_map": True
                    }
                ]
            },
            "Refiner": {
                "args": [
                    True,
                    "v1-5-pruned-emaonly.safetensors [6ce016689]",
                    0.8
                ]
            }
        }
    }

    call_img2img_api(payload, output_image_path, args.server)

if __name__ == "__main__":
    main()
