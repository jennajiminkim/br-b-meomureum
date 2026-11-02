import subprocess,wave,io,json
from pathlib import Path
import numpy as np
r=Path(__import__('os').environ['NATURE_SOURCE_DIR']);out=Path(__file__).resolve().parents[2]/'dist/assets/audio';out.mkdir(exist_ok=True)
def decoded(path,filters,seconds=None,start=None):
 args=['ffmpeg','-v','error']
 if start is not None:args+=['-ss',str(start)]
 args+=['-i',str(path)]
 if seconds:args+=['-t',str(seconds)]
 args+=['-af',filters,'-ar','44100','-ac','2','-f','f32le','pipe:1']
 return np.frombuffer(subprocess.check_output(args),dtype='<f4').reshape(-1,2).copy()
def save(name,data):
 data=np.clip(data,-.95,.95).astype('<f4');dest=out/name
 subprocess.run(['ffmpeg','-v','error','-f','f32le','-ar','44100','-ac','2','-i','pipe:0','-codec:a','libmp3lame','-b:a','128k','-y',str(dest)],input=data.tobytes(),check=True)
 print(name,'duration',len(data)/44100,'peak',float(abs(data).max()))
def loop(data,seconds=1.5):
 n=int(seconds*44100);t=np.linspace(0,1,n)[:,None];return np.vstack([data[n:-n],data[-n:]*(1-t)+data[:n]*t])
water=decoded(r/'stream-waterfall/stream1.ogg','highpass=f=65,lowpass=f=4000,loudnorm=I=-24:TP=-6:LRA=7',30)
forest=decoded(r/'park_ambience_birds.wav','highpass=f=100,lowpass=f=9500,loudnorm=I=-25:TP=-6:LRA=9',36,8)
save('water-bed.mp3',loop(water));save('forest-bed.mp3',loop(forest))
# A strong bird-call segment from the actual field recording, not a synthetic chirp.
birds=decoded(r/'park_ambience_birds.wav','highpass=f=1700,lowpass=f=7500',50,8)
window=2*44100;step=4410;energies=[np.mean(birds[i:i+window]**2) for i in range(0,len(birds)-window,step)];idx=int(np.argmax(energies))*step
clip=birds[idx:idx+window];clip*=.22/max(.0001,float(abs(clip).max()));fade=round(.04*44100);clip[:fade]*=np.linspace(0,1,fade)[:,None];clip[-fade:]*=np.linspace(1,0,fade)[:,None];save('forest-bird.mp3',clip)
# Original ceramic-like resonator. Clearly labelled synthetic, not field-recorded.
sr=44100;t=np.arange(3*sr)/sr;signal=np.zeros_like(t)
for f,a,d in [(520,1,1.3),(712.4,.42,.95),(1289.6,.18,.65),(1944.8,.05,.45)]:signal+=a*np.sin(2*np.pi*f*t)*np.exp(-t/d)
signal*=np.minimum(t/.008,1);signal*=.21/max(abs(signal));stereo=np.column_stack([signal,signal*.94]);save('ceramic-tone.mp3',stereo)
(r/'bird-extract.json').write_text(json.dumps({'source':'park_ambience_birds.wav','start_seconds':8+idx/sr,'length':2},indent=2))
