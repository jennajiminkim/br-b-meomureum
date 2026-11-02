"""Replace urban-park audio using CC0 recordings explicitly described as traffic-free."""
import os,json,subprocess,hashlib
from pathlib import Path
import numpy as np
r=Path(__file__).resolve().parents[2];src=Path(os.environ['FOREST_SOURCE_DIR']);out=r/'dist/assets/audio';sr=44100

def decode(p,filters='anull'):
 return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-af',filters,'-ar',str(sr),'-ac','2','-f','f32le','pipe:1']),dtype='<f4').reshape(-1,2).copy()
def level(x,rms,peak):
 return x*min(rms/max(float(np.sqrt(np.mean(x*x))),1e-9),peak/max(float(abs(x).max()),1e-9))
def fade(x,seconds):
 n=min(round(seconds*sr),len(x)//2);x[:n]*=np.linspace(0,1,n)[:,None];x[-n:]*=np.linspace(1,0,n)[:,None];return x
def loop(x,seconds=1.5):
 n=round(seconds*sr);t=np.linspace(0,1,n)[:,None];return np.vstack([x[n:-n],x[-n:]*(1-t)+x[:n]*t])
def save(name,x):
 assert np.isfinite(x).all() and 0<abs(x).max()<.95
 subprocess.run(['ffmpeg','-v','error','-f','f32le','-ar',str(sr),'-ac','2','-i','pipe:0','-c:a','libmp3lame','-b:a','192k','-y',str(out/name)],input=x.astype('<f4').tobytes(),check=True)
 a=decode(out/name);assert np.isfinite(a).all() and 0<abs(a).max()<1
 return {'file':name,'duration':len(a)/sr,'peak':float(abs(a).max()),'rms':float(np.sqrt(np.mean(a*a)))}
checks=[]
# Light tree breeze: suppress low motor-like drone and avoid the loudest gust/bee windows.
wind=decode(src/'songforest.mp3','highpass=f=350,lowpass=f=1900')
width=48*sr;hop=sr;starts=range(0,len(wind)-width,hop)
start=min(starts,key=lambda i:float(np.mean(wind[i:i+width]**2)))
breeze=level(loop(wind[start:start+width]),.017,.10)
# A very quiet high insect texture. +5% is a linear gain change, not +5dB.
ins=decode(src/'summer-insects.mp3','highpass=f=6200,lowpass=f=10000')
iwidth=48*sr;istart=min(range(0,len(ins)-iwidth,2*sr),key=lambda i:float(np.max(np.mean(ins[i:i+iwidth].reshape(-1,sr,2)**2,axis=(1,2)))))
insects=level(loop(ins[istart:istart+iwidth]),.08,.30);detail_gain=.07*1.05
bed=breeze+insects[:len(breeze)]*detail_gain
checks.append(save('forest-breeze-bed-v045.mp3',bed))
# Select short high, tonal song phrases (not the old park/crow clip).
song=decode(src/'songforest.mp3','highpass=f=1800,lowpass=f=7200')
mono=song.mean(axis=1);n=2048;hop=1024;frames=np.lib.stride_tricks.sliding_window_view(mono,n)[::hop];spectrum=abs(np.fft.rfft(frames*np.hanning(n),axis=1))**2
hz=np.fft.rfftfreq(n,1/sr);band=spectrum[:,(hz>=1800)&(hz<=6800)];power=band.sum(axis=1);tonality=band.max(axis=1)/np.maximum(power,1e-12)
phrase=round(2.6*sr);candidates=[]
for at in np.arange(1,len(mono)/sr-3,.25):
 i=round(at*sr/hop);j=min(len(power),i+round(2.6*sr/hop));score=float(np.mean(power[i:j]*tonality[i:j]));candidates.append((score,float(at)))
selected=[]
for _,at in sorted(candidates,reverse=True):
 if all(abs(at-t)>8 for t in selected):selected.append(at)
 if len(selected)==3:break
old=decode(out/'forest-bird-soft-v041.mp3');old_rms=float(np.sqrt(np.mean(old*old)))
clips=[]
for idx,at in enumerate(selected):
 a=song[round(at*sr):round(at*sr)+phrase].copy();fade(a,.09);a=level(a,old_rms,.15);clips.append(a);checks.append(save(f'forest-songbird-{idx+1}-v045.mp3',a))
review=bed[:30*sr].copy()
for idx,at in enumerate([1.7,11,22]):
 a=clips[idx];i=round(at*sr);review[i:i+len(a)]+=a*(.65*1.05)
checks.append(save('forest-breeze-songbirds-review-v045.mp3',review*.35))
info={'sources':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [src/'songforest.mp3',src/'summer-insects.mp3']},'breezeStart':start/sr,'insectStart':istart/sr,'birdPhrases':selected,'birdReferenceRms':old_rms,'birdGain':.65*1.05,'insectBaseGain':.07,'insectGain':detail_gain,'detailIncreaseFactor':1.05,'checks':checks}
(r/'docs/forest-breeze-checks.json').write_text(json.dumps(info,indent=2));print(json.dumps(info,indent=2))
