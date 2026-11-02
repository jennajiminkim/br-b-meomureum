import {ASSETS} from './assets.js';
import {WaterMotion,addForestMotion} from './motion.js';
export class SceneMedia {
 constructor(){
  this.screen='home';this.world='water';this.paused=false;this.reduced=false;this.inView=new WeakMap();this.water=new Map();
  this.scenes=[...document.querySelectorAll('.scene')];
  for(const scene of this.scenes){if(scene.classList.contains('scene-water'))this.water.set(scene,new WaterMotion(scene));else addForestMotion(scene);}
  this.observer=new IntersectionObserver(entries=>{for(const entry of entries)this.inView.set(entry.target,entry.isIntersecting);this.refresh();},{threshold:.01});this.scenes.forEach(s=>this.observer.observe(s));
  for(const video of document.querySelectorAll('.scene-video')){
   const asset=ASSETS[video.dataset.world];video.muted=true;
   for(const [type,src]of Object.entries(asset.video)){if(!src)continue;const source=document.createElement('source');source.src=src;source.type=`video/${type}`;video.append(source);}
   video.addEventListener('playing',()=>{video.classList.add('ready');video.parentElement.classList.add('has-video');this.refresh();});
   video.addEventListener('error',()=>{video.classList.remove('ready');video.parentElement.classList.remove('has-video');this.refresh();});
  }
  document.addEventListener('visibilitychange',()=>this.refresh());
  const pref=matchMedia('(prefers-reduced-motion: reduce)');pref.addEventListener('change',()=>this.refresh());
 }
 sync(screen,world,paused,reduced){Object.assign(this,{screen,world,paused,reduced});this.refresh();}
 refresh(){const reduced=this.reduced||matchMedia('(prefers-reduced-motion: reduce)').matches;
  for(const scene of this.scenes){const world=scene.classList.contains('scene-water')?'water':'forest';const selected=this.screen==='home'||world===this.world;const shown=Boolean(scene.closest(`#screen-${this.screen}`))&&selected&&this.inView.get(scene)===true;
   const active=shown&&!this.paused&&!reduced&&!document.hidden&&this.screen!=='end';
   scene.classList.toggle('motion-active',active);scene.classList.toggle('motion-reduced',reduced);
   this.water.get(scene)?.setState(active&&!scene.classList.contains('has-video'),reduced);
   const video=scene.querySelector('video');if(!video)continue;
   if(active&&video.querySelector('source')){if(video.paused)video.play().catch(()=>video.classList.remove('ready'));}else video.pause();
  }
 }
}
