# Deepfake for the Good

[arxiv](https://arxiv.org/abs/2402.06390) | [project page](https://quereste.github.io/deepfake-for-the-good/)

We would like depict steps to reproduce outcomes we achieved and described in paper "Deepfake for the Good: Generating Avatars through Face-Swapping with
Implicit Deepfake Generation". In the aforementioned work we show a novel approach to get 3D deepfake representation of a person using a single 2D photo and a set of images of a base face avatar. Below there is an illustrative movie of such attempt's outcome for Ms. Céline Dion.

Result video:

https://github.com/quereste/implicit-deepfake/assets/77748206/0072ebb6-cf71-4f98-95f3-b58a51612815



## 4D ImplicitDeepfake

Now it's possible to use our solution to create 4D deepfake representation. As for 3D version we use single 2D photo and video of a base face avatar. Below we present capabilities of our solution.



Original video: 

https://github.com/quereste/implicit-deepfake/assets/77748206/ec3dc76a-a215-4d2c-87e2-21617200a768



Face to swap with:

![](assets/famous.jpg)


Output video:


https://github.com/quereste/implicit-deepfake/assets/77748206/62675841-220a-467e-8cd7-b1ce76944168




It's also possible to change facial expressions
| Paper              | After ImplicitDeepfake | Changed expression  |
|-----------------|-----------------|-----------------|
| <img src="assets/paper_0001.png" alt="paper_0001" width="300" height="300"> | <img src="assets/original_0001.png" alt="original_0001" width="300" height="300"> | <img src="assets/changed_0001.png" alt="changed_0001" width="300" height="300"> |
| <img src="assets/paper_0002.png" alt="paper_0002" width="300" height="300"> | <img src="assets/original_0002.png" alt="original_0002" width="300" height="300"> | <img src="assets/changed_0002.png" alt="changed_0002" width="300" height="300"> |
| <img src="assets/paper_0003.png" alt="paper_0003" width="300" height="300"> | <img src="assets/original_0003.png" alt="original_0003" width="300" height="300"> | <img src="assets/changed_0003.png" alt="changed_0003" width="300" height="300"> |
| <img src="assets/paper_0004.png" alt="paper_0004" width="300" height="300"> | <img src="assets/original_0004.png" alt="original_0004" width="300" height="300"> | <img src="assets/changed_0004.png" alt="changed_0004" width="300" height="300"> |
| <img src="assets/paper_0005.png" alt="paper_0005" width="300" height="300"> | <img src="assets/original_0005.png" alt="original_0005" width="300" height="300"> | <img src="assets/changed_0005.png" alt="changed_0005" width="300" height="300"> |



## Steps to reproduce for 3D ImplicitDeepfake

1. Download dataset from [link](https://drive.google.com/drive/folders/1ZSUoqH1sv3ln-BuWznnDqSx0-Erg5TZU?usp=sharing)

This dataset consists of CelebA picture of Ms. Céline Dion (file: famous.jpg) and a directory with train, validation and test pictures of a base face avatar. With every subdirectory there is associated a .json file, containing camera positions, from which specific photos were taken. We hereby stress, that the face avatar we use in this example comes from this [link](
https://sketchfab.com/3d-models/tina-head-530fab5eb2aa44f699052624794aeaa9). We are thankful for this piece of work.

2. Convert every photo from the dataset to a 2D deepfake

Use a 2D deepfake of your choice to convert all the pictures from the dataset directory to their deepfake versions, using file famous.jpg as a target photo. For the experiments we conducted in the paper, we used GHOST deepfake (see citations).

3. Pick a 3D rendering model to be rewarded with a 3D deepfake representation of the target person from step 2

Both NeRF and Gaussian Splatting solutions (see citations) work fine, our pipeline does not demand any specific model though. The result from the short illustrative video comes from Gaussian Splatting model.

### Notebook for your convenience

We created a [notebook](https://github.com/quereste/implicit-deepfake/blob/main/demo.ipynb) that covers steps 2 and 3 from above, assuming the use of Gaussian Splatting as the 3D rendering technique. Its content is based on similar notebooks from the repos of the matter. In case of any doubts, feel free to ask us. The notebook needs no further requirements when being run on Google Colab.

## Steps to reproduce for 4D ImplicitDeepfake
1. Download [the dataset](https://kaldir.vc.in.tum.de/nerface/nerface_dataset.zip) (as noted [here](https://github.com/gafniguy/4D-Facial-Avatars/tree/main?tab=readme-ov-file)).

This dataset consists of directory with train, validation and test pictures of a base face avatar. With every subdirectory there is associated a .json file, containing camera positions, from which specific photos were taken.

2. Download [photo famous.jpg](https://drive.google.com/file/d/1Sss9o6v0aVKN6hP0vz6fNNsWNfjb5ajx/view?usp=sharing)

3. Convert every photo from the dataset to a 2D deepfake

Use a 2D deepfake of your choice to convert all the pictures from the dataset directory to their deepfake versions, using file famous.jpg as a target photo. For the experiments we conducted in the paper, we used GHOST deepfake (see citations).

4. Use [4D Facial avatars](https://github.com/gafniguy/4D-Facial-Avatars) to get 4D avatar facial reconstruction.

   Attention this model requires at least 80GB RAM!

## Diffusion ImplicitDeepfake

### Tools

To reproduce the results of this experiment, you will need to install the following tools:
- [Blender](https://www.blender.org/)
- [Gaussian Splatting](https://github.com/graphdeco-inria/gaussian-splatting)
- [Stable Diffusion](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [EbSynth](https://ebsynth.com/)
- [ffmpeg](https://ffmpeg.org/)

### Workflow

1. **Render Images from Blender**  
   Render a series of images from your 3D model in Blender. These images will serve as the input for the diffusion process. We recommend performing 360 degrees video render to ensure consistency while applying diffusion.
   [An example open source 3D model](https://sketchfab.com/3d-models/tina-head-530fab5eb2aa44f699052624794aeaa9)

2. **Apply Diffusion using Stable Diffusion**
   Use Stable Diffusion to apply transformations defined by a prompt to the rendered frames.
   The process of applying Stable Diffusion that ensures the highest consistency of the result across among different angles along with optimal parameters is described [here](https://stable-diffusion-art.com/video-to-video/#Method_5_Temporal_Kit) and requires the use of EbSynth.

3. **Convert Rendered Images to a 3D Model using Gaussian Splatting**  
   Feed the transformed images into the Gaussian Splatting process to generate the final 3D model.

### Results

After completing the experiment, the following results were observed:

![result_0](https://github.com/user-attachments/assets/c5a3b2c6-1c72-4b2a-83a4-c6f61ff258a1)

Used prompts:
- **positive** - "Photo of a bronze bust of a woman, detailed and lifelike, in the style of Auguste Rodin, polished bronze, classical sculpture aesthetics, 32k uhd, timeless and elegant, intricate details, full head and shoulders, museum quality, realistic texture, warm bronze tones, photorealistic, black background."
- **negative** - "Deformed, disfigured, ugly."

![result_1](https://github.com/user-attachments/assets/b35b4082-7efc-4ad8-975a-29bb8ca5dec7)

Used prompts:
- **positive** - "Photo of a head with realistic facial features, hair color changed to vibrant red, smooth and lifelike skin texture, sharp and expressive eyes, natural human proportions, high-definition detail, consistent appearance from all angles (front, side, back view), cinematic composition, trending on ArtStation."
- **negative** - "Unrealistic colors, distorted proportions, blurred details, heavy shadows, lack of detail."

![result_2](https://github.com/user-attachments/assets/75e50f82-d48d-4c38-8341-dadb27d210f1)

Used prompts:
- **positive** - "An elf, with pointed ears, ethereal and elegant features, detailed and lifelike, in the style of Alan Lee, smooth and flawless skin, sharp and expressive eyes, long and flowing hair, otherworldly and mystical appearance, 32k uhd, high-definition detail, wearing simple yet stylish elven attire, black background, cinematic lighting, photorealistic, studio portrait."
- **negative** - "Distorted, disfigured, ugly, human features, unrealistic proportions, poor lighting, low detail."

<!-- ### TODO:
Explore improvements by iteratively applying Stable Diffusion (after the first step, it may be better to use [this approach](https://stable-diffusion-art.com/video-to-video/#Method_2_ControlNet_img2img) along with the DDIM Sampler) and Gaussian Splatting on the resulting models. The hypothesis is that Gaussian Splatting increases consistency between adjacent frames, while Stable Diffusion enhances quality. -->

### Scripts to reproduce the results (only Windows)

1. Install the software mentioned in the **Tools** section (we provide an example dataset in the [link](https://ujchmura-my.sharepoint.com/:f:/g/personal/georgii_stanishevskii_student_uj_edu_pl/Ei93fzknaspDp0sxhWXdLrABSdBNXTFAv_dIHjPHHxWFEA?e=flv8KE), so you don’t need Blender).

2. Copy all scripts from this repository into the `Automatic1111` folder.

3. Run Stable Diffusion with the `--api` parameter.

4. Open the folder in CMD Terminal (PowerShell may not work properly).

5. Activate the virtual environment:  
  ```bash
  .\venv\Scripts\activate.bat
  ```
6. Run the script:
```bash
python loop.py /path/to/main_folder "My Prompt" --start 0 --end 3 [optional params]
```

7. Make sure the main folder contains:  
   - video render of the object  
   - `transforms.json` file

8. The code will generate folders named `iter1`, `iter2`, etc., containing gaussian splatting model and generated frames.

9. Video results (360-degree renders) will appear in the main folder as `iter1.mp4`, `iter2.mp4`, etc.

10. During generation, the program will pause and wait for you to manually use EbSynth to propagate changes from diffusion to all frames.

Results from the second experiment:

![ezgif-2-14c20ef111](https://github.com/user-attachments/assets/a6d14863-d3e4-4e19-ad65-e4184b746dd8)

### Theory behind

#### Stable Diffusion

##### Latent Diffusion Models

![image](https://github.com/user-attachments/assets/60137b42-23e0-4d10-84f4-4e3e1f42be9e)

**Latent Diffusion Models** were introduced by Rombach *et al.* in  
*“High-Resolution Image Synthesis with Latent Diffusion Models”* (arXiv : 2112.10752, 20 Dec 2021). 
The authors propose to embed the diffusion process inside a pretrained auto-encoder so that all noisy forward / denoising reverse steps run **in a much lower-dimensional latent space** rather than in pixel space. This design slashes memory and compute while preserving visual fidelity, and it underpins Stable Diffusion.

**Pipeline overview**

1. **Encode** – an image $x$ is compressed by an encoder $E$ to a latent tensor $z = E(x)$.  
2. **Diffuse & Denoise in Latent Space** – the DDPM/SDE process operates on $z$, training a U-Net to predict noise in the latent domain.  
3. **Decode** – after the reverse diffusion yields $\hat{z}$, a decoder $D$ reconstructs the final high-resolution image $\hat{x}=D(\hat{z})$.  

Because $h\times w \ll H\times W$ (e.g., $64\times64$ vs. $512\times512$), training and inference become tractable on a single GPU while maintaining photorealistic detail. Subsequent work—most notably **Stable Diffusion**—extends this framework with text conditioning and **ControlNet** branches for structural guidance.


##### Text-Prompt Guidance in Diffusion Models

Before introducing **ControlNet**, it is useful to recall that modern diffusion models can already be **steered by natural-language prompts**.  
The mechanism was formalised in the OpenAI paper *“GLIDE: Towards Photorealistic Image Generation and Editing with Text-Guided Diffusion Models”* (Nichol *et al.*, 2022). The authors demonstrate that if you pass a prompt through a text encoder—initially CLIP ViT-L/14—and concatenate the resulting embedding to the U-Net’s latent or cross-attention layers, the denoising process learns to minimise noise *while satisfying the text condition*. 

Two guidance strategies proved especially effective:

| Strategy | Idea |
|----------|------|
| **CLIP Guidance** | During sampling, use the CLIP image encoder to rank intermediate images by semantic similarity to the prompt and nudge the diffusion trajectory towards higher-ranked samples. | 
| **Classifier-Free Guidance (CFG)** | Train the model with and without a prompt (empty string) and, at inference, interpolate between the two predictions to trade diversity for fidelity. | 

This text-conditioning recipe underpins **Stable Diffusion**:  
* v1.x checkpoints inherit the *pre-trained* OpenAI CLIP encoder used in GLIDE and DALL·E 2.  
* v2.x replaces it with **OpenCLIP**—a from-scratch replication trained on the LAION-2B dataset—which improves prompt adherence and removes the need for proprietary weights.

In short, a prompt such as  
`"Photo of a bronze bust, polished, museum lighting"`  
is converted into a CLIP embedding that conditions **every** denoising step, yielding images that match the described content even before any additional control mechanisms (e.g., ControlNet) are applied.

#### ControlNet

![image](https://github.com/user-attachments/assets/a101b591-9108-4b67-a9c9-4c1c7ad652d2)

**ControlNet** adds an *extra, trainable branch* to a **frozen** text-guided Latent Diffusion Model so that generation can be steered by pixel-aligned inputs such as edge maps, depth, pose, or segmentation. 
A duplicate of the U-Net encoder–decoder receives the condition map \(c\); its layers are connected to the frozen backbone through **zero-initialised 1 × 1 convolutions**, which output zeros at the start of training and therefore leave the base model’s behaviour untouched.
During fine-tuning, these “ZeroConvs” gradually learn a residual that injects just enough spatial information to satisfy \(c\), allowing robust training even on datasets as small as 50 k pairs and preventing catastrophic drift. 
Official checkpoints cover Canny edges, depth, OpenPose skeletons, normal maps, and more, and the **ControlNet 1.1** release adds “guess-mode” and cached feature variants for ~45 % faster inference. 

*Role in this repo:* we use ControlNet (edge or depth) to lock geometry across chosen 360° renders which are then being transformed by Stable Diffusion into new images according to the prompt. It takes place before EbSynth propagates style and Gaussian Splatting rebuilds the 3D model, ensuring both structural fidelity and temporal coherence.

#### EbSynth (Example-Based Image Synthesis)

**EbSynth** is a patch-based, example-guided algorithm that propagates an artist-painted key frame across the remaining frames of a video while preserving both local texture details and global temporal coherence. The method was first presented as *“Stylizing Video by Example”* at SIGGRAPH 2019 and builds on earlier work such as *StyLit* (SIGGRAPH 2016) and the PatchMatch family of nearest-neighbour algorithms. 

##### How it works

1. **Key-frame stylisation** – The user paints or edits one (or more) reference frames with any 2D tool.  
2. **Guidance map computation** – Dense correspondences between the key frame(s) and each target frame are estimated (usually with optical flow).  
3. **PatchMatch transfer** – For every patch in the target frame, EbSynth finds the best-matching patch in the key frame and copies its pixels; a confidence map weights the blending. 
4. **Edge-aware blending & refinement** – Overlaps are resolved with guided filtering; an optional temporal pass enforces consistency over successive frames. 

Because the algorithm works in image space, it inherits the exact style of the artist painting—including brush strokes and high-frequency detail—something that neural style-transfer often washes out. The process is fast (real-time or faster per frame) and runs entirely on the GPU.

### Practical tips for this repository

| Step | Recommendation |
|------|---------------|
| Key-frame count | 9 – 16 well-chosen views usually suffice for a 360 ° turntable; add more only when topology changes drastically. |
| Resolution | Keep the rendered frames and painted key frames at the same native resolution to avoid resampling artefacts. |
| Integration with A1111 | The community extension `CiaraStrawberry/TemporalKit` can automate the call from Stable Diffusion to EbSynth if you prefer a single click workflow. |

#### Role in our 3D pipeline

After Stable Diffusion + ControlNet generates high-quality but *per-key-frame* stylised renders, EbSynth sweeps through the sequence and harmonises consistency of transformed frames across time. This step is crucial before we pass the imagery to **Gaussian Splatting**, because temporal consistency directly improves the quality of the reconstructed 3D point-cloud.


## Citation

Another 3D model we used was expertly created by Author [here](https://sketchfab.com/3d-models/micha-3d-photoscanned-human-face-c49a92f2bd6c4ec0a488bdc0e381d31c).

We would like to express our gratitude to the authors of Gaussian Splatting and NeRF model, along with the pytorch representation of the latter. We used Gaussian Splatting and NeRF to achieve 3D rendering results.

```
@misc{mildenhall2020nerf,
    title={NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis},
    author={Ben Mildenhall and Pratul P. Srinivasan and Matthew Tancik and Jonathan T. Barron and Ravi Ramamoorthi and Ren Ng},
    year={2020},
    eprint={2003.08934},
    archivePrefix={arXiv},
    primaryClass={cs.CV}
}
```
```
@misc{lin2020nerfpytorch,
  title={NeRF-pytorch},
  author={Yen-Chen, Lin},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished={\url{https://github.com/yenchenlin/nerf-pytorch/}},
  year={2020}
}
```
```
@Article{kerbl3Dgaussians,
      author       = {Kerbl, Bernhard and Kopanas, Georgios and Leimk{\"u}hler, Thomas and Drettakis, George},
      title        = {3D Gaussian Splatting for Real-Time Radiance Field Rendering},
      journal      = {ACM Transactions on Graphics},
      number       = {4},
      volume       = {42},
      month        = {July},
      year         = {2023},
      url          = {https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/}
}
```
Big thanks to the authors of the 4D Facial Avatars model. We used it to obtain 4D rendering results.

```
@InProceedings{Gafni_2021_CVPR,
    author    = {Gafni, Guy and Thies, Justus and Zollh{\"o}fer, Michael and Nie{\ss}ner, Matthias},
    title     = {Dynamic Neural Radiance Fields for Monocular 4D Facial Avatar Reconstruction},
    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
    month     = {June},
    year      = {2021},
    pages     = {8649-8658}
}
```
Last but not least, we hereby cite the 2D deepfake GHOST work that was used in our original pipeline.

```
@article{9851423,
         author={Groshev, Alexander and Maltseva, Anastasia and Chesakov, Daniil and Kuznetsov, Andrey and Dimitrov, Denis},
         journal={IEEE Access},
         title={GHOST—A New Face Swap Approach for Image and Video Domains},
         year={2022},
         volume={10},
         number={},
         pages={83452-83462},
         doi={10.1109/ACCESS.2022.3196668}
}
```

Thanks also to the authors of Stable Diffusion, ControlNet, and EbSynth for their incredible tools that made this work possible.

```
@misc{rombach2022highresolutionimagesynthesislatent,
      title={High-Resolution Image Synthesis with Latent Diffusion Models}, 
      author={Robin Rombach and Andreas Blattmann and Dominik Lorenz and Patrick Esser and Björn Ommer},
      year={2022},
      eprint={2112.10752},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2112.10752}, 
}
```

```
@misc{zhang2023addingconditionalcontroltexttoimage,
      title={Adding Conditional Control to Text-to-Image Diffusion Models}, 
      author={Lvmin Zhang and Anyi Rao and Maneesh Agrawala},
      year={2023},
      eprint={2302.05543},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2302.05543}, 
}
```

```
@misc{Jamriska2018,
  author = {Jamriska, Ondrej},
  title = {Ebsynth: Fast Example-based Image Synthesis and Style Transfer},
  year = {2018},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/jamriska/ebsynth}},
}
```

