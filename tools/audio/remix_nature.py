"""v0.4.1. Requires ffmpeg + numpy. See docs/AUDIO_REMIX.md for source rights."""
import os,subprocess,json
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[2];src=Path(os.environ['REMIX_SOURCE_DIR']);out=root/'dist/assets/audio';sr=44100

def decode(path,filters='anull'):
 return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-af',filters,'-f','f32le','-ar',str(sr),'-ac','2','pipe:1']),dtype='<f4').reshape(-1,2).copy()
def fade(a,seconds=.06):
 n=min(int(seconds*sr),len(a)//2);a[:n]*=np.linspace(0,1,n)[:,None];a[-n:]*=np.linspace(1,0,n)[:,None];return a
def save(name,a):
 assert np.isfinite(a).all() and abs(a).max()<.95
 subprocess.run(['ffmpeg','-v','error','-f','f32le','-ar',str(sr),'-ac','2','-i','pipe:0','-c:a','libmp3lame','-b:a','128k','-y',str(out/name)],input=a.astype('<f4').tobytes(),check=True)
 return {'file':name,'duration':len(a)/sr,'peak':float(abs(a).max()),'rms':float(np.sqrt(np.mean(a*a)))}
# Each real splash keeps a quiet gap; no steady stream layer, zero-valued loop seam.
water=np.zeros((48*sr,2));placements=[(1,0,.15),(2,7,.12),(4,15,.14),(3,23,.11),(1,31,.13),(4,40,.12)]
for i,at,peak in placements:
 a=decode(src/f'wave_0{i}_cc0-11505__transitking__wavesound.flac','atempo=0.8,highpass=f=90,lowpass=f=3400')
 a*=peak/max(abs(a).max(),1e-6);fade(a,.14);start=round(at*sr);water[start:start+len(a)]+=a
# Existing field recording, filtered without loudness renormalizing birds back up.
forest=decode(out/'forest-bed.mp3','lowpass=f=1100:p=2,volume=0.7')
# Shorter, quieter single phrase, instead of the old 2s dense call cluster.
bird=decode(out/'forest-bird.mp3')[:int(.9*sr)];bird*=.13/max(abs(bird).max(),1e-6);fade(bird,.07)
# Real ceramic cups touching, CC0 kikuchiyo. No synthetic resonator added.
ceramic=decode(src/'ceramic-real.mp3','highpass=f=150,lowpass=f=9000');ceramic*=.52/max(abs(ceramic).max(),1e-6);fade(ceramic,.004)
checks=[save('water-lapping-v041.mp3',water),save('forest-bed-soft-v041.mp3',forest),save('forest-bird-soft-v041.mp3',bird),save('ceramic-clink-v041.mp3',ceramic)]
(root/'docs/audio-remix-checks.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
