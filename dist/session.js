// Memory only. Time is measured from a monotonic clock; pausing never advances a cue.
export class SessionClock {
  constructor(){this.reset();}
  reset(){this.elapsed=0;this.total=0;this.status='idle';this.reason=null;this.previous=null;}
  start(minutes){this.reset();this.total=minutes*60;this.status='running';}
  step(now){if(this.status!=='running'){this.previous=null;return false;}if(this.previous!==null)this.elapsed=Math.min(this.total,this.elapsed+Math.max(0,(now-this.previous)/1000));this.previous=now;if(this.elapsed>=this.total){this.status='ended';this.reason='complete';return true;}return false;}
  pause(){if(this.status==='running'){this.status='paused';this.previous=null;}}
  resume(){if(this.status==='paused'){this.status='running';this.previous=null;}}
  end(){if(this.reason!=='complete')this.reason='early';this.status='ended';this.previous=null;}
}
