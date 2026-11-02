"""Package one Korean speaker for all 9 sessions. Raw WAVs keyed by SHA256(text)[:20]."""
import os,json,hashlib,subprocess,math,shutil,time
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[2];raw=Path(os.environ['UNIFIED_WAV_DIR']);out=root/'dist/assets/audio/narration/ko-kr-v042';out.mkdir(parents=True,exist_ok=True)
rows=json.loads((root/'docs/guide-timelines.json').read_text());semitones=-.6;ratio=2**(semitones/12);cache={};manifest={};checks=[];full=np.zeros(300*44100,dtype=np.float32)
for key,cues in rows.items():
 config={'status':'ready','voiceId':'meomureum-kr-v042','voice':'동일한 한국어 안내 목소리','settings':{'speaker':'MeloTTS Korean KR','speed':.98,'pitchSemitones':semitones,'pitchRatio':ratio,'integratedLufs':-19},'verification':{'mobile':'pending-after-pitch-change','human_listening':'pending'},'clips':{}}
 for idx,c in enumerate(cues):
  h=hashlib.sha256(c['text'].encode()).hexdigest()[:20];dest=out/(h+'.mp3')
  if h not in cache:
   source=raw/(h+'.wav');deadline=time.monotonic()+180
   while not source.exists() or time.time()-source.stat().st_mtime<.4:
    if time.monotonic()>deadline:raise TimeoutError('Missing completed WAV: '+h)
    time.sleep(.2)
   subprocess.run(['ffmpeg','-v','error','-i',str(raw/(h+'.wav')),'-af',f'rubberband=pitch={ratio}:formant=preserved,highpass=f=60,loudnorm=I=-19:TP=-3:LRA=7','-ar','44100','-ac','1','-c:a','libmp3lame','-b:a','128k','-y',str(dest)],check=True)
   a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(dest),'-f','f32le','-ar','44100','-ac','1','pipe:1']),dtype='<f4');assert np.isfinite(a).all() and 0<abs(a).max()<1
   cache[h]=a
  a=cache[h];duration=len(a)/44100;next_at=cues[idx+1]['at'] if idx+1<len(cues) else int(key.split('-')[-1])*60
  assert duration<next_at-c['at']-3,(c['id'],duration,next_at-c['at'])
  config['clips'][c['id']]={'src':'./assets/audio/narration/ko-kr-v042/'+dest.name,'duration':duration,'text':c['text']}
  checks.append({'cue':c['id'],'at':c['at'],'duration':duration,'peak':float(abs(a).max()),'rms':float(np.sqrt(np.mean(a*a)))})
  if key=='breath-5':start=round(c['at']*44100);full[start:start+len(a)]+=a
 manifest[key]=config
subprocess.run(['ffmpeg','-v','error','-f','f32le','-ar','44100','-ac','1','-i','pipe:0','-c:a','libmp3lame','-b:a','128k','-y',str(out/'breath-5-full-preview.mp3')],input=full.tobytes(),check=True)
(root/'dist/narration-assets.js').write_text('export const NARRATION='+json.dumps(manifest,ensure_ascii=False,indent=2)+';\n')
(root/'docs/narration-audio-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
print(json.dumps({'sessions':len(manifest),'cues':len(checks),'uniqueClips':len(cache),'pitchSemitones':semitones,'pitchRatio':ratio},indent=2))
