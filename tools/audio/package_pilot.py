import json,subprocess
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[2];wav=Path(__import__('os').environ['PILOT_WAV_DIR']);out=root/'dist/assets/audio/narration/breath-5';out.mkdir(parents=True,exist_ok=True)
rows=json.loads((root/'docs/guide-timelines.json').read_text())['breath-5'];full=np.zeros(300*44100,dtype=np.float32);clips={};checks=[]
for row in rows:
 name=row['id'];dest=out/(name+'.mp3')
 subprocess.run(['ffmpeg','-v','error','-i',str(wav/(name+'.wav')),'-af','highpass=f=60,loudnorm=I=-19:TP=-3:LRA=7','-ar','44100','-ac','1','-codec:a','libmp3lame','-b:a','128k','-y',str(dest)],check=True)
 data=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(dest),'-f','f32le','-ar','44100','-ac','1','pipe:1']),dtype='<f4');duration=len(data)/44100;idx=rows.index(row);next_at=rows[idx+1]['at'] if idx+1<len(rows) else 300
 assert duration<next_at-row['at']-3,(name,duration)
 start=round(row['at']*44100);full[start:start+len(data)]+=data
 clips[name]={'src':'./assets/audio/narration/breath-5/'+dest.name,'duration':duration,'text':row['text']}
 checks.append({'cue':name,'at':row['at'],'duration':duration,'peak':float(abs(data).max()),'rms':float(np.sqrt(np.mean(data**2)))})
 subprocess.run(['ffmpeg','-v','error','-f','f32le','-ar','44100','-ac','1','-i','pipe:0','-codec:a','libmp3lame','-b:a','128k','-y',str(out/'breath-5-full-preview.mp3')],input=full.tobytes(),check=True)
config={'breath-5':{'status':'ready','voice':'MeloTTS Korean KR · 청취 검증 전 초안','verification':{'mobile':'pending','human_listening':'pending'},'clips':clips}}
(root/'dist/narration-assets.js').write_text('export const NARRATION='+json.dumps(config,ensure_ascii=False,indent=2)+';\n')
(root/'docs/narration-audio-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2));print(json.dumps(checks,ensure_ascii=False,indent=2))
