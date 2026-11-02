import {NARRATION} from './narration-assets.js';
export class NarrationEngine {
 constructor({getContext,unlock=async()=>{},report=()=>{},activity=()=>{},fetcher=globalThis.fetch?.bind(globalThis)}={}){
  Object.assign(this,{getContext,unlock,report,activity,fetcher});this.volume=.85;this.buffers=new Map();this.loads=new Map();this.token=0;this.current=null;this.key='';this.source=null;this.events=[];
 }
 log(event,details={}){this.events.push({event,...details});if(this.events.length>30)this.events.shift();}
 configure(practice,minutes){this.key=`${practice}-${minutes}`;this.config=NARRATION[this.key];return this.config;}
 get recorded(){return this.config?.status==='ready';}
 async preload(){if(!this.recorded)throw new Error('NARRATION_NOT_READY: '+this.key);await Promise.all(Object.values(this.config.clips).map(clip=>this.load(clip.src)));}
 async load(src){if(this.buffers.has(src))return this.buffers.get(src);if(this.loads.has(src))return this.loads.get(src);
  const p=(async()=>{const r=await this.fetcher(src);if(!r.ok)throw new Error(`HTTP_${r.status}`);const buffer=await this.getContext().decodeAudioData(await r.arrayBuffer());this.buffers.set(src,buffer);return buffer;})();this.loads.set(src,p);try{return await p;}finally{this.loads.delete(src);}
 }
 setVolume(value){this.volume=Math.max(0,Math.min(1,value));if(this.gain)this.gain.gain.setTargetAtTime(this.volume,this.getContext().currentTime,.03);}
 stop(){++this.token;this.current=null;if(this.source){this.source.onended=null;try{this.source.stop();this.source.disconnect();}catch{}this.source=null;}if(this.gain){try{this.gain.disconnect();}catch{}this.gain=null;}this.activity(false);}
 fail(code,detail=''){this.log('error',{code,detail});this.report({type:'error',code,message:`한국어 안내를 재생하지 못했습니다. (${code})`,detail});this.activity(false);}
 play(cue,elapsed=cue.at){this.stop();const token=this.token;this.current=cue.id;
  if(this.volume===0){this.report({type:'error',code:'VOICE_MUTED',message:'안내 음량이 0%입니다. 설정에서 안내 음량을 높여 주세요.'});return;}
  if(this.recorded){this.playFile(cue,elapsed,token);return;}
  this.fail('NARRATION_NOT_READY',this.key);
 }
 async playFile(cue,elapsed,token){const clip=this.config.clips[cue.id];if(!clip?.src){this.fail('CLIP_MISSING',cue.id);return;}
  try{await this.unlock();const ctx=this.getContext();const buffer=await this.load(clip.src);if(token!==this.token)return;
   const offset=Math.max(0,elapsed-cue.at);if(offset>=buffer.duration)return;
   if(ctx.state!=='running'){this.fail('CONTEXT_'+ctx.state,'다시 듣기 버튼을 눌러 주세요.');return;}
   const source=ctx.createBufferSource(),gain=ctx.createGain();source.buffer=buffer;gain.gain.value=this.volume;source.connect(gain).connect(ctx.destination);this.source=source;this.gain=gain;
   source.onended=()=>{if(token!==this.token||this.source!==source)return;this.source=null;source.disconnect();gain.disconnect();this.gain=null;this.log('file-ended',{cue:cue.id});this.activity(false);};
   source.start(0,offset);this.activity(true);this.log('file-start',{cue:cue.id,offset,duration:buffer.duration});this.report({type:'started',source:'사전 제작 내레이션',cue:cue.id});
  }catch(e){if(token===this.token)this.fail('FILE_PLAY_FAILED',`${clip.src}: ${e.message}`);}
 }
 diagnostics(){return {session:this.key,source:this.recorded?'recorded':'unavailable',voiceId:this.config?.voiceId,pitchSemitones:this.config?.settings?.pitchSemitones,active:Boolean(this.source),volume:this.volume,events:this.events};}
}
