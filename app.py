import os
import math
import gradio as gr
import torch
import librosa
import pandas as pd
import numpy as np

from sonics import HFAudioClassifier


# Constants
MODEL_IDS = {
    "SpecTTTra-α (5s)": "awsaf49/sonics-spectttra-alpha-5s",
    "SpecTTTra-β (5s)": "awsaf49/sonics-spectttra-beta-5s",
    "SpecTTTra-γ (5s)": "awsaf49/sonics-spectttra-gamma-5s",
    "SpecTTTra-α (120s)": "awsaf49/sonics-spectttra-alpha-120s",
    "SpecTTTra-β (120s)": "awsaf49/sonics-spectttra-beta-120s",
    "SpecTTTra-γ (120s)": "awsaf49/sonics-spectttra-gamma-120s",
}


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_cache = {}


def load_model(model_name):
    """Load model if not already cached"""
    if model_name not in model_cache:
        model_id = MODEL_IDS[model_name]
        model = HFAudioClassifier.from_pretrained(model_id)
        model = model.to(device)
        model.eval()
        model_cache[model_name] = model
    return model_cache[model_name]


def process_audio(audio_path, model_name):
    """Process audio file and return prediction"""
    try:
        # Load model
        model = load_model(model_name)

        # Get max time from model config
        max_time = model.config.audio.max_time

        # Load and process audio
        audio, sr = librosa.load(audio_path, sr=16000)
        duration = len(audio) / sr

        # Calculate chunk size and middle position
        chunk_samples = int(max_time * sr)
        total_chunks = len(audio) // chunk_samples
        middle_chunk_idx = total_chunks // 2
        
        # Extract middle chunk
        start = middle_chunk_idx * chunk_samples
        end = start + chunk_samples
        chunk = audio[start:end]

        # Pad if needed (shouldn't be necessary for middle chunk)
        if len(chunk) < chunk_samples:
            chunk = np.pad(chunk, (0, chunk_samples - len(chunk)))

        # Convert to tensor and get prediction
        with torch.no_grad():
            chunk = torch.from_numpy(chunk).float().to(device)
            pred = model(chunk.unsqueeze(0))
            prob = torch.sigmoid(pred).cpu().numpy()[0]

        # Get prediction
        output = {"Real": 1 - prob, "Fake": prob}

        return output

    except Exception as e:
        return {
            "Duration": "Error",
            "Prediction": f"Error: {str(e)}",
            "Confidence": "N/A",
        }


def predict(audio_file, model_name):
    """Gradio interface function"""
    if audio_file is None:
        return {
            "Duration": "No file",
            "Prediction": "Please upload an audio file",
            "Confidence": "N/A",
        }

    return process_audio(audio_file, model_name)


# Create Gradio interface
css = """
.heading {
    text-align: center;
    margin-bottom: 2rem;
}
.logo {
    max-width: 250px;
    margin: 0 auto;
    display: block;
}
"""

with gr.Blocks(css=css) as demo:
    gr.HTML(
        """
        <div class="heading">
            <img src="https://i.postimg.cc/3Jx3yZ5b/real-vs-fake-sonics-w-logo.jpg" class="logo">
            <h1>SONICS: Synthetic Or Not - Identifying Counterfeit Songs</h1>
            <h3><span style="color:red;"><b>ICLR 2025 [Poster]</b></span></h3>
        </div>
    """
    )

    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(label="Upload Audio", type="filepath")
            model_dropdown = gr.Dropdown(
                choices=list(MODEL_IDS.keys()),
                value="SpecTTTra-γ (5s)",
                label="Select Model",
            )
            submit_btn = gr.Button("Predict")

        with gr.Column():
            output = gr.Label(label="Result", num_top_classes=2)

    submit_btn.click(fn=predict, inputs=[audio_input, model_dropdown], outputs=[output])

    gr.Markdown(
        """
    ## Resources
    - 📄 [Paper](https://openreview.net/forum?id=PY7KSh29Z8)
    - 🎵 [Dataset](https://huggingface.co/datasets/awsaf49/sonics)
    - 🔬 [ArXiv](https://arxiv.org/abs/2408.14080)
    - 💻 [GitHub](https://github.com/awsaf49/sonics)
    """
    )

demo.launch()
