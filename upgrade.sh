#!/bin/bash
export MODEL_BASE_PATH="/stable-diffusion-webui"
export EMBEDDINGS_PATH="/stable-diffusion-webui/EMBEDDINGS_PATH"
export HYPERNETWORKS_PATH="/stable-diffusion-webui/HYPERNETWORKS_PATH"
export STABLE_DIFFUSION_PATH="/stable-diffusion-webui/STABLE_DIFFUSION_PATH"
export LORA_PATH="/stable-diffusion-webui/LORA_PATH"
export OTHERS_PATH="/stable-diffusion-webui/OTHERS_PATH"
python ./upgrade_script.py