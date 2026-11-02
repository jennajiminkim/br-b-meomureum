import json,hashlib,shutil,time,os,gc,ctypes
from pathlib import Path
import torch
from melo.api import TTS
root=Path(__file__).resolve().parents[2];out=Path(os.environ['UNIFIED_WAV_DIR']);out.mkdir(exist_ok=True)
rows=json.loads((root/'docs/guide-timelines.json').read_text());unique={hashlib.sha256(c['text'].encode()).hexdigest()[:20]:c['text'] for cues in rows.values() for c in cues}
for c in rows['breath-5']:
 p=Path(os.environ.get('PILOT_WAV_DIR','/nonexistent-pilot-cache'))/(c['id']+'.wav');key=hashlib.sha256(c['text'].encode()).hexdigest()[:20]
 if p.exists():shutil.copyfile(p,out/(key+'.wav'))
print('unique',len(unique),'cached',len(list(out.glob('*.wav'))),flush=True)
torch.set_num_threads(4)
model=TTS(language='KR',device='cpu');speaker=model.hps.data.spk2id['KR'];print('model-ready',flush=True);generated=0
for idx,(key,text) in enumerate(unique.items()):
 dest=out/(key+'.wav')
 if dest.exists():continue
 torch.manual_seed(int(key[:8],16));started=time.time()
 model.tts_to_file(text,speaker,str(dest),speed=.98,noise_scale=.45,quiet=True)
 gc.collect();ctypes.CDLL('libc.so.6').malloc_trim(0);generated+=1
 print(json.dumps({'done':idx+1,'total':len(unique),'seconds':round(time.time()-started,1),'text':text},ensure_ascii=False),flush=True)
 if generated>=int(os.environ.get('MAX_GENERATE_BATCH','8')):break
print('ALL_GENERATED' if all((out/(h+'.wav')).exists() for h in unique) else 'BATCH_GENERATED; repeat to continue',flush=True)
