import {test} from 'node:test';
import assert from 'node:assert/strict';
import {SessionClock} from '../dist/session.js';
import {timeline,cueAt,ANCHOR} from '../dist/guides.js';
import {SoundEngine} from '../dist/audio.js';
test('all 9 programs end once, with intentional silent intervals and one common anchor',()=>{
 for(const program of ['breath','body','thought'])for(const minutes of [3,5,10]){
  const cues=timeline(program,minutes);assert(cues.some(c=>c.text===ANCHOR));assert.equal(cueAt(cues,0)?.id,cues[0].id);
  for(let i=0;i<cues.length;i++){const c=cues[i];assert(c.until>c.at);assert(c.until<=(cues[i+1]?.at??minutes*60)-3);assert.equal(cueAt(cues,c.until),null);}
  const clock=new SessionClock();clock.start(minutes);clock.step(0);assert.equal(clock.step(minutes*60000),true);assert.equal(clock.reason,'complete');assert.equal(clock.step(minutes*60000+1000),false);clock.end();assert.equal(clock.reason,'complete');
 }
});
test('pauses exclude elapsed time; switching scene cannot restart the clock',()=>{
 const c=new SessionClock();c.start(3);c.step(0);c.step(17000);c.pause();c.step(90000);assert.equal(c.elapsed,17);c.resume();c.step(95000);c.step(98000);assert.equal(c.elapsed,20);c.end();assert.equal(c.reason,'early');c.reset();assert.equal(c.reason,null);
});
function fakeEngine(){const e=new SoundEngine();e.ctx={currentTime:0};e.unlock=async()=>{};e.loadRecordings=async()=>{};e.makeAmbient=(world,volume)=>({world,volume,bus:{},fx:{},stopped:false});e.fadeStop=a=>{a.stopped=true;};return e;}
test('ending while audio unlock is pending cannot start orphaned playback',async()=>{
 const e=fakeEngine();let release;e.unlock=()=>new Promise(r=>release=r);const pending=e.startSession('water');e.destroy();release();await pending;assert.equal(e.session,null);
});
test('rapid scene switches accept only the latest asynchronous result',async()=>{
 const e=fakeEngine();await e.startSession('water');let releases=[];e.unlock=()=>new Promise(r=>releases.push(r));const a=e.switchWorld('forest',40),b=e.switchWorld('water',40);releases[1]();await b;releases[0]();await a;assert.equal(e.sessionWorld,'water');assert.equal(e.session.world,'water');
});
test('preview cancellation while unlocking cannot leak sound into setup',async()=>{
 const e=fakeEngine();let release;e.unlock=()=>new Promise(r=>release=r);const pending=e.startPreview('forest');e.stopPreview();release();await pending;assert.equal(e.preview,null);
});
test('8 second preview schedules representative accent and ends cleanly',async t=>{
 t.mock.timers.enable({apis:['setTimeout']});const e=fakeEngine();let accent=null,ended=false;e.accent=(world,_amb,forced)=>accent={world,forced};e.bird=()=>{};await e.startPreview('forest',()=>ended=true);t.mock.timers.tick(1700);assert.deepEqual(accent,{world:'forest',forced:true});t.mock.timers.tick(6300);assert.equal(ended,true);assert.equal(e.preview,null);
});
