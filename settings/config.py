from pathlib import Path

import dotenv

import torch
import os


BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

language = os.environ['LANGUAGE']
model_id = os.environ['MODEL_ID']
sample_rate = int(os.environ['SAMPLE_RATE'])
speaker = os.environ['SPEAKER']
device = torch.device(os.environ['DEVICE'])
model_speach = os.environ["MODEL"]

text = 'ЛОХ'

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
model.to(device)
