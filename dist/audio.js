import {ASSETS} from './assets.js';
import {AUDIO_MIX,nextAccentDelay} from './audio-mix.js';
/** Decoded field-recording beds and isolated accent buses. No noise fallback. */
export class SoundEngine {
  constructor({report=()=>{}}={}){this.report=report;this.events=[];this.retiring=new Set();this.ctx=null;this.session=null;this.preview=null;this.sessionWorld='water';this.volume=.35;this.paused=false;this.nextEventAt=0;this.recentEventAt=-999;this.ambientTimeouts=[];this.generation=0;this.previewGeneration=0;this.duckLevel=1;this.buffers=new Map();}
  ensureContext(){
    if(!this.ctx){const Context=window.AudioContext||window.webkitAudioContext;if(!Context)throw new Error('Web Audio 미지원');this.ctx=new Context();this.ctx.onstatechange=()=>{this.events.push({event:'context-state',state:this.ctx.state});if(this.events.length>15)this.events.shift();if(this.session&&this.ctx.state!=='running'&&!this.paused)this.report({code:'AUDIO_CONTEXT_'+this.ctx.state,message:'오디오가 일시 중단되었습니다. 다시 듣기를 눌러 주세요.'});};}return this.ctx;
  }
  async unlock(){const ctx=this.ensureContext();if(ctx.state!=='running')await ctx.resume();if(ctx.state!=='running')throw new Error('AudioContext '+ctx.state);return true;}
  diagnostics(){return {world:this.sessionWorld,preview:Boolean(this.preview),session:Boolean(this.session),paused:this.paused,ambientVolume:this.volume,duck:this.duckLevel,events:this.events};}
  makeAmbient(world,volume){
    const bus=this.ctx.createGain();bus.gain.value=0;bus.connect(this.ctx.destination);
    const stopFns=[];const fx=this.ctx.createGain();fx.connect(bus);
    if(this.buffers.has(ASSETS[world].audio.bed)){const source=this.ctx.createBufferSource();source.buffer=this.buffers.get(ASSETS[world].audio.bed);source.loop=true;source.connect(bus);source.start(0,world==='water'?Math.random()*source.buffer.duration:0);stopFns.push(()=>{source.stop();source.disconnect();});}
    else throw new Error('자연음 파일이 준비되지 않았습니다: '+world);
    const t=this.ctx.currentTime;bus.gain.setValueAtTime(0,t);bus.gain.linearRampToValueAtTime(volume,t+1.4);
    return {bus,fx,stopFns,accents:new Set(),stopped:false};
  }
  fadeStop(amb,fade=.4){if(!amb||amb.stopped)return;amb.stopped=true;this.retiring.add(amb);for(const source of amb.accents??[])try{source.stop();}catch{}amb.fx.disconnect();const t=this.ctx.currentTime;amb.bus.gain.cancelScheduledValues(t);amb.bus.gain.setTargetAtTime(0,t,Math.max(.03,fade/3));setTimeout(()=>{for(const stop of amb.stopFns)stop();this.retiring.delete(amb);try{amb.bus.disconnect()}catch{}},fade*1000+450)}
  accent(world,amb,forced=false){if(!amb||amb.stopped||!this.ctx||amb.accents?.size)return;const asset=ASSETS[world].audio.accent,paths=Array.isArray(asset)?asset:[asset];const choices=paths.filter(path=>path!==amb.lastAccentPath);const path=forced?paths[0]:(choices.length?choices:paths)[Math.floor(Math.random()*(choices.length||paths.length))];const clip=this.buffers.get(path);if(!clip)return;amb.lastAccentPath=path;const source=this.ctx.createBufferSource(),gain=this.ctx.createGain(),pan=this.ctx.createStereoPanner?this.ctx.createStereoPanner():this.ctx.createGain();source.buffer=clip;if('pan'in pan)pan.pan.value=forced?0:(Math.random()*2-1)*AUDIO_MIX[world].pan;const variation=AUDIO_MIX[world].gainRange;gain.gain.value=AUDIO_MIX[world].accentGain*(forced||!variation?1:variation[0]+Math.random()*(variation[1]-variation[0]));source.connect(gain).connect(pan).connect(amb.fx);amb.accents.add(source);source.start();this.events.push({event:'accent-start',world,path});if(this.events.length>15)this.events.shift();source.onended=()=>{amb.accents.delete(source);source.disconnect();gain.disconnect();pan.disconnect();};}
  async loadRecordings(world){
    this.ensureContext();await Promise.all(Object.values(ASSETS[world].audio).flat().filter(path=>typeof path==='string'&&path).map(async path=>{
      if(this.buffers.has(path))return;
      try{const response=await fetch(path);if(!response.ok)throw new Error('audio');this.buffers.set(path,await this.ctx.decodeAudioData(await response.arrayBuffer()));}
      catch(e){this.events.push({event:'asset-error',path,message:e.message});throw new Error(path+': '+e.message);}
    }));
  }
  async startPreview(world,onEnd){
    this.stopPreview();const token=this.previewGeneration;await this.unlock();await this.loadRecordings(world);
    if(token!==this.previewGeneration)return;
    const amb=this.makeAmbient(world,.3);this.preview=amb;
    amb.timeouts=[setTimeout(()=>{if(this.preview===amb)this.accent(world,amb,true);},1700),setTimeout(()=>{if(this.preview===amb&&world==='water'){this.accent(world,amb,false);}},5200),setTimeout(()=>{if(this.preview===amb){this.stopPreview();onEnd?.();}},8000)];
  }
  stopPreview(){this.previewGeneration++;if(!this.preview)return;for(const id of this.preview.timeouts||[])clearTimeout(id);this.fadeStop(this.preview,.2);this.preview=null;}
  async startSession(world,volume=.35,elapsed=0){
    this.stopPreview();this.stopSession();const token=this.generation;this.volume=volume;this.paused=false;this.duckLevel=1;
    await this.unlock();await this.loadRecordings(world);if(token!==this.generation)return;
    this.sessionWorld=world;this.session=this.makeAmbient(world,this.paused?0:volume*this.duckLevel);this.nextEventAt=elapsed+nextAccentDelay(world,true);
  }
  stopSession(){this.generation++;if(this.session){this.fadeStop(this.session,.35);this.session=null;}}
  applyVolume(){if(!this.session||this.session.stopped)return;const t=this.ctx.currentTime;this.session.bus.gain.cancelScheduledValues(t);this.session.bus.gain.setTargetAtTime(this.paused?0:this.volume*this.duckLevel,t,.13);}
  setVolume(level){this.volume=level;this.applyVolume();}
  pause(){this.paused=true;for(const source of this.session?.accents??[])try{source.stop();}catch{}for(const amb of this.retiring){amb.bus.gain.cancelScheduledValues(this.ctx.currentTime);amb.bus.gain.setValueAtTime(0,this.ctx.currentTime);}this.applyVolume();}
  resume(){this.paused=false;this.applyVolume();}
  async switchWorld(world,elapsed){
    const token=++this.generation;await this.unlock();await this.loadRecordings(world);
    if(token!==this.generation)return;
    if(this.session){this.fadeStop(this.session,.9);this.session=null;}
    this.sessionWorld=world;this.session=this.makeAmbient(world,this.paused?0:this.volume*this.duckLevel);this.nextEventAt=elapsed+nextAccentDelay(world,true);
  }
  tick(elapsed){if(!this.session||this.paused)return;if(elapsed>=this.nextEventAt){this.accent(this.sessionWorld,this.session);this.nextEventAt=elapsed+nextAccentDelay(this.sessionWorld);}}
  duck(value){this.duckLevel=value;this.applyVolume();}
  destroy(){this.stopSession();this.stopPreview();}
}
