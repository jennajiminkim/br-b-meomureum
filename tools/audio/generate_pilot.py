import json,sys
from pathlib import Path
import torch
from melo.api import TTS
root=Path(__file__).resolve().parents[2]
out=Path(__import__('os').environ['PILOT_WAV_DIR']);out.mkdir(exist_ok=True)
torch.set_num_threads(4)
print('loading-model',flush=True)
model=TTS(language='KR',device='cpu')
rows=json.loads((root/'docs/guide-timelines.json').read_text())['breath-5']
for c in rows:
 dest=out/(c['id']+'.wav')
 if not dest.exists():
  print('generating',c['id'],flush=True)
  model.tts_to_file(c['text'],model.hps.data.spk2id['KR'],str(dest),speed=.98,noise_scale=.45,quiet=True)
 print('saved',c['id'],flush=True)
