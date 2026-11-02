"""Original arrangement of CC0 recordings. No uploaded/reference-video audio is used."""
from pathlib import Path
import subprocess,json,hashlib,random
import numpy as np
root=Path(__file__).resolve().parents[2];out=root/'dist/assets/audio';sr=44100;rng=random.Random(4301)
def decode(p,filters='anull'):
 return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-af',filters,'-ar',str(sr),'-ac','2','-f','f32le','pipe:1']),dtype='<f4').reshape(-1,2).copy()
def fade(x,t=.04):
 n=min(round(t*sr),len(x)//2);x[:n]*=np.linspace(0,1,n)[:,None];x[-n:]*=np.linspace(1,0,n)[:,None];return x
def save(name,x):
 assert np.isfinite(x).all() and 0<abs(x).max()<.95
 subprocess.run(['ffmpeg','-v','error','-f','f32le','-ar',str(sr),'-ac','2','-i','pipe:0','-c:a','libmp3lame','-b:a','192k','-y',str(out/name)],input=x.astype('<f4').tobytes(),check=True)
 decoded=decode(out/name);assert abs(decoded).max()<1
 return {'file':name,'duration':len(decoded)/sr,'peak':float(abs(decoded).max()),'rms':float(np.sqrt(np.mean(decoded**2)))}
checks=[];ceramic_source=out/'ceramic-clink-v041.mp3';water_source=out/'water-lapping-v041.mp3';variants=[]
for name,pitch in [('small',1.12),('middle',1.0),('large',.86)]:
 x=decode(ceramic_source,f'rubberband=pitch={pitch}:formant=shifted,highpass=f=280,equalizer=f=1250:t=q:w=0.8:g=2,lowpass=f=7400')
 # Short, damped reflection field, derived from the recording rather than a sine bell.
 ir=np.zeros(round(.8*sr));ir[0]=1
 for i in range(1,105):
  t=.012+(i/104)**1.4*.71;ir[min(round(t*sr),len(ir)-1)]+=rng.choice([-1,1])*.045*np.exp(-t/0.22)
 n=1<<(len(x)+len(ir)-2).bit_length();wet=np.column_stack([np.fft.irfft(np.fft.rfft(x[:,c],n)*np.fft.rfft(ir,n),n)[:len(x)+len(ir)-1] for c in [0,1]])
 fade(wet,.006);wet=np.tanh(wet*5)/5;wet*=.46/max(abs(wet).max(),1e-7);variants.append(wet)
 checks.append(save(f'porcelain-{name}-v043.mp3',wet))
pair=np.zeros((max(len(variants[2]),len(variants[0])+round(.28*sr)),2));pair[:len(variants[2])]+=variants[2]*.76;idx=round(.28*sr);pair[idx:idx+len(variants[0])]+=variants[0]*.51;pair*=min(1,.46/max(abs(pair).max(),1e-7));checks.append(save('porcelain-pair-v043.mp3',pair))
# Reuse the licensed water-only material, not the artwork's soundtrack.
original=decode(water_source,'highpass=f=100,lowpass=f=2300');segments=[original[round(a*sr):round(b*sr)] for a,b in [(0,2.3),(7,11.2),(15,17.7),(23,26.1)]]
water=np.zeros((64*sr,2));at=.25;events=[]
while at<63:
 x=segments[rng.randrange(len(segments))].copy();fade(x,.24);x*=rng.uniform(.85,1.2);pan=rng.uniform(-.12,.12);x[:,0]*=1-pan;x[:,1]*=1+pan
 idx=round(at*sr)
 # wrap at loop boundary, so the final lapping tail continues at the beginning
 end=idx+len(x)
 if end<=len(water):water[idx:end]+=x
 else:water[idx:]+=x[:len(water)-idx];water[:end-len(water)]+=x[len(water)-idx:]
 events.append(round(at,2));at+=rng.uniform(2.5,4.6)
# Gentle transient control, then a restrained level under ceramic and narration.
water=np.tanh(water*5)/5;water*=.13/max(abs(water).max(),1e-7)
# Circular smoothing of 25ms only around the splice, keeping energy on both sides.
n=round(.025*sr);bridge=np.linspace(water[-n],water[n],2*n);water[-n:]=bridge[:n];water[:n]=bridge[n:]
checks.append(save('water-porcelain-bed-v043.mp3',water))
# Review mix: representative 30 seconds at the app's default ambient gain.
review=water[:30*sr].copy()
for i,at in enumerate([1.7,6.8,13.5,21.1,27.0]):
 clip=decode(out/['porcelain-middle-v043.mp3','porcelain-small-v043.mp3','porcelain-pair-v043.mp3','porcelain-large-v043.mp3'][i%4]);idx=round(at*sr);k=min(len(clip),len(review)-idx);review[idx:idx+k]+=clip[:k]*1.1
checks.append(save('water-and-porcelain-review-v043.mp3',review*.35))
(root/'docs/porcelain-water-checks.json').write_text(json.dumps({'inputHashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ceramic_source,water_source]},'referenceAudioUsed':False,'waterEvents':events,'checks':checks},indent=2));print(json.dumps(checks,indent=2))
