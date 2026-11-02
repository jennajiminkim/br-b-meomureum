"""Soften the CC0 ceramic recording; keep the user-approved water file byte-identical."""
from pathlib import Path
import json,subprocess,hashlib
import numpy as np
r=Path(__file__).resolve().parents[2];out=r/'dist/assets/audio';sr=44100;source=out/'ceramic-clink-v041.mp3';water=out/'water-porcelain-bed-v043.mp3'
def decode(p,filters='anull'):
 return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-af',filters,'-f','f32le','-ar',str(sr),'-ac','2','pipe:1']),dtype='<f4').reshape(-1,2).copy()
def stats(a):
 m=a.mean(axis=1);p=abs(np.fft.rfft(m))**2;hz=np.fft.rfftfreq(len(m),1/sr)
 return {'duration':len(a)/sr,'peak':float(abs(a).max()),'rms':float(np.sqrt(np.mean(a*a))),'above2kEnergyFraction':float(p[hz>2000].sum()/max(p.sum(),1e-12))}
def save(name,a):
 assert np.isfinite(a).all() and 0<abs(a).max()<.9
 subprocess.run(['ffmpeg','-v','error','-f','f32le','-ar',str(sr),'-ac','2','-i','pipe:0','-c:a','libmp3lame','-b:a','192k','-y',str(out/name)],input=a.astype('<f4').tobytes(),check=True)
 b=decode(out/name);assert abs(b).max()<1
 if name.startswith('porcelain-soft'):
  assert stats(b)['above2kEnergyFraction']<.001 and stats(b)['peak']<.3
 return {'file':name,**stats(b)}
checks=[];clips=[]
for name,pitch,fundamental in [('low',.43,245),('middle',.48,275),('high',.53,310)]:
 a=decode(source,f'rubberband=tempo=0.55:pitch={pitch}:formant=shifted,highpass=f=110,lowpass=f=1350:p=2,equalizer=f=470:t=q:w=0.8:g=5,equalizer=f=1200:t=q:w=0.9:g=-7')
 # Slow the impact envelope; retain the recording's lower porcelain resonances.
 attack=round(.08*sr);a[:attack]*=np.sin(np.linspace(0,np.pi/2,attack))[:,None]**2
 # A quiet, short reflection extends the body without repeating a hard contact.
 ir=np.zeros(round(.85*sr));ir[0]=1
 for t,g in [(.047,.12),(.081,.09),(.127,.06),(.193,.035),(.283,.018),(.419,.008)]:ir[round(t*sr)]=g
 n=1<<(len(a)+len(ir)-2).bit_length();a=np.column_stack([np.fft.irfft(np.fft.rfft(a[:,c],n)*np.fft.rfft(ir,n),n)[:len(a)+len(ir)-1] for c in [0,1]])
 tail=round(.4*sr);a[-tail:]*=np.cos(np.linspace(0,np.pi/2,tail))[:,None]**2
 a*=.26/max(abs(a).max(),1e-8)
 # Original, softly excited modal layer: round lower body, quiet inharmonic upper modes.
 # This is disclosed as sound design, not claimed to be an untouched bowl recording.
 t=np.arange(len(a))/sr;ring=np.zeros_like(t)
 for f,amp,decay in [(fundamental,1,.85),(fundamental*2.33,.22,.57),(fundamental*3.71,.055,.34)]:
  ring+=amp*np.sin(2*np.pi*f*t)*np.exp(-t/decay)
 ring*=1-np.exp(-t/.035);ring*=.26/max(abs(ring).max(),1e-8)
 a=a*.22+np.column_stack([ring,ring*.985])*.78
 a[:attack]*=np.sin(np.linspace(0,np.pi/2,attack))[:,None]**2
 a[-tail:]*=np.cos(np.linspace(0,np.pi/2,tail))[:,None]**2
 a*=.26/max(abs(a).max(),1e-8);clips.append(a);checks.append(save(f'porcelain-soft-{name}-v044.mp3',a))
review=decode(water)[:30*sr]
for i,t in enumerate([1.7,7.8,15.3,23.4]):
 a=clips[[1,0,2,1][i]];start=round(t*sr);count=min(len(a),len(review)-start);review[start:start+count]+=a[:count]*.5
checks.append(save('water-and-soft-porcelain-review-v044.mp3',review*.35))
(r/'docs/soft-porcelain-checks.json').write_text(json.dumps({'waterSha256':hashlib.sha256(water.read_bytes()).hexdigest(),'oldMiddle':stats(decode(out/'porcelain-middle-v043.mp3')),'referenceAudioUsed':False,'checks':checks},indent=2));print(json.dumps(checks,indent=2))
