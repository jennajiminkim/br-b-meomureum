/** Original poster + clean water plate. WebGL only distorts water, never ceramics.
 * All state lives in memory. No external libraries, media services or requests.
 */
const NS='http://www.w3.org/2000/svg';
let serial=0;
const VERTEX=`attribute vec2 position;varying vec2 uv;void main(){uv=position*.5+.5;gl_Position=vec4(position,0.,1.);}`;
const FRAGMENT=`precision mediump float;varying vec2 uv;uniform sampler2D photo;uniform float time;uniform vec2 viewport;uniform vec2 imageSize;
void main(){
 float ratio=viewport.x/viewport.y;float source=imageSize.x/imageSize.y;
 vec2 fit=ratio>source?vec2(1.,source/ratio):vec2(ratio/source,1.);
 vec2 p=vec2(.5)+(vec2(uv.x,1.-uv.y)-.5)*fit;
 float wave=sin(p.y*48.+time*.32)+sin(p.x*31.-p.y*19.-time*.24)*.45;
 p.x+=wave*.0018; p.y+=sin(p.x*37.+p.y*25.+time*.27)*.0012;
 vec3 col=texture2D(photo,clamp(p,vec2(.003),vec2(.997))).rgb;
 col+=sin(p.x*26.+p.y*39.-time*.31)*.004;
 gl_FragColor=vec4(col,1.);
}`;
function svgNode(name,attrs={}){const n=document.createElementNS(NS,name);for(const[k,v]of Object.entries(attrs))n.setAttribute(k,v);return n;}
export class WaterMotion {
 constructor(scene){this.scene=scene;this.ready=false;this.failed=false;this.active=false;this.visible=false;this.time=0;this.previous=null;this.frame=0;this.attempted=false;this.disposed=false;
  this.layer=document.createElement('div');this.layer.className='water-motion-layer';this.layer.setAttribute('aria-hidden','true');this.canvas=document.createElement('canvas');this.canvas.className='moving-water';this.layer.append(this.canvas);
  const id='ceramic-'+serial++;const svg=svgNode('svg',{viewBox:'0 0 1672 941',preserveAspectRatio:'xMidYMid slice',class:'floating-ceramics'});const defs=svgNode('defs');svg.append(defs);
  const masks=[
   'M241 413 C231 351 383 277 547 255 C738 225 913 261 1009 324 C1051 352 1077 385 1075 423 C1068 523 950 629 750 665 C558 699 366 655 289 566 C252 521 241 463 241 413 Z',
   'M1052 167 C1055 132 1151 98 1264 95 C1381 90 1466 114 1477 153 C1492 199 1430 265 1330 296 C1228 327 1127 296 1084 252 C1065 232 1053 195 1052 167 Z'
  ];
  this.bowls=masks.map((path,i)=>{const clip=svgNode('clipPath',{id:id+'-'+i,clipPathUnits:'userSpaceOnUse'});clip.append(svgNode('path',{d:path}));defs.append(clip);const g=svgNode('g');g.append(svgNode('image',{href:'./assets/water-poster-aqua.webp',width:'1672',height:'941','clip-path':`url(#${id}-${i})`}));svg.append(g);return g;});
  this.layer.append(svg);scene.append(this.layer);this.resize=new ResizeObserver(()=>this.draw());this.resize.observe(scene);
 }
 async initialize(){if(this.attempted)return;this.attempted=true;
  try{const image=new Image();image.src='./assets/water-surface-aqua.webp';await image.decode();this.image=image;if(this.disposed)return;
   const gl=this.canvas.getContext('webgl',{alpha:false,antialias:false,preserveDrawingBuffer:false,powerPreference:'low-power'});if(!gl)throw new Error('WebGL unavailable');this.gl=gl;
   const shader=(kind,src)=>{const s=gl.createShader(kind);gl.shaderSource(s,src);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw new Error(gl.getShaderInfoLog(s));return s;};
   const vert=shader(gl.VERTEX_SHADER,VERTEX),frag=shader(gl.FRAGMENT_SHADER,FRAGMENT),program=gl.createProgram();gl.attachShader(program,vert);gl.attachShader(program,frag);gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw new Error('water program');gl.deleteShader(vert);gl.deleteShader(frag);gl.useProgram(program);this.program=program;
   const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),gl.STATIC_DRAW);const loc=gl.getAttribLocation(program,'position');gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);
   const texture=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,texture);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGB,gl.RGB,gl.UNSIGNED_BYTE,image);
   this.uTime=gl.getUniformLocation(program,'time');this.uView=gl.getUniformLocation(program,'viewport');gl.uniform2f(gl.getUniformLocation(program,'imageSize'),image.naturalWidth,image.naturalHeight);
   this.renderer='webgl';this.ready=true;this.scene.dataset.motionRenderer='webgl';this.scene.classList.add('water-motion-ready');this.draw();this.play();
   this.canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();this.failed=true;this.active=false;cancelAnimationFrame(this.frame);this.scene.classList.remove('water-motion-ready');});
  }catch(error){this.initialize2D(error);}
 }
 initialize2D(error){try{if(!this.image)throw error;const canvas=document.createElement('canvas');canvas.className='moving-water';this.canvas.replaceWith(canvas);this.canvas=canvas;this.ctx=canvas.getContext('2d',{alpha:false});if(!this.ctx)throw error;this.renderer='canvas2d';this.scene.dataset.motionRenderer='canvas2d';this.ready=true;this.scene.classList.add('water-motion-ready');this.draw();this.play();}catch{this.failed=true;this.scene.classList.remove('water-motion-ready');}}
 setState(active,reduced){this.active=active&&!reduced&&!this.failed;this.scene.classList.toggle('motion-reduced',reduced);if(this.active){this.initialize();this.play();}else{cancelAnimationFrame(this.frame);this.frame=0;this.previous=null;}}
 play(){if(!this.ready||!this.active||this.frame)return;this.frame=requestAnimationFrame(t=>this.tick(t));}
 tick(now){this.frame=0;if(!this.active)return;if(this.previous!==null)this.time+=Math.min((now-this.previous)/1000,.08);this.previous=now;if(!this.lastDraw||now-this.lastDraw>=33){this.draw();this.lastDraw=now;}this.play();}
 draw(){if(!this.ready||this.failed)return;const gl=this.gl,r=this.scene.getBoundingClientRect();if(!r.width||!r.height)return;
  const scale=Math.min(1.25,devicePixelRatio||1,1440/r.width);const w=Math.round(r.width*scale),h=Math.round(r.height*scale);if(this.canvas.width!==w||this.canvas.height!==h){this.canvas.width=w;this.canvas.height=h;if(this.renderer==='webgl')gl.viewport(0,0,w,h);}
  if(this.renderer==='webgl'){gl.uniform1f(this.uTime,this.time);gl.uniform2f(this.uView,w,h);gl.drawArrays(gl.TRIANGLES,0,6);}else{const ctx=this.ctx,im=this.image,fit=Math.max(w/im.width,h/im.height)*1.009,sw=w/fit,sh=h/fit,sx=(im.width-sw)/2,sy=(im.height-sh)/2;for(let y=0;y<h;y+=18){const dh=Math.min(19,h-y),dx=Math.sin(y/h*27+this.time*.32)*1.5,dy=Math.sin(y/h*18-this.time*.25)*.7;ctx.drawImage(im,sx+dx,sy+y/fit+dy,sw,dh/fit,0,y,w,dh);}}
  this.bowls.forEach((g,i)=>{const t=this.time,phase=i*2.2,x=Math.sin(t*.13+phase)*(i?7:10),y=Math.sin(t*.28+phase)*(i?2.8:4.2),angle=Math.sin(t*.17+phase)*.24;g.setAttribute('transform',`translate(${x.toFixed(3)} ${y.toFixed(3)}) rotate(${angle.toFixed(4)} ${i?1265:658} ${i?200:460})`);});
 }
}
export function addForestMotion(scene){
 const layer=document.createElement('div');layer.className='forest-motion-layer';layer.setAttribute('aria-hidden','true');
 layer.innerHTML=`<div class="forest-sunbeam beam-a"></div><div class="forest-sunbeam beam-b"></div><div class="forest-glow"></div><div class="falling-leaf leaf-a"><svg viewBox="0 0 24 40"><path d="M12 2C-2 12 1 31 11 37C23 28 26 12 12 2Z" fill="#a4ad60"/><path d="M12 4L11 36" stroke="#647e47" fill="none"/></svg></div><div class="falling-leaf leaf-b"><svg viewBox="0 0 24 40"><path d="M12 2C-2 12 1 31 11 37C23 28 26 12 12 2Z" fill="#9caa5b"/><path d="M12 4L11 36" stroke="#647e47" fill="none"/></svg></div><div class="forest-birds"><svg viewBox="0 0 130 52"><g class="bird-wing bird-one"><path d="M3 20Q12 8 22 19Q31 9 41 16Q29 16 22 23Q11 15 3 20Z"/></g><g class="bird-wing bird-two"><path d="M50 34Q57 25 65 34Q74 26 83 31Q73 31 65 38Q57 31 50 34Z"/></g><g class="bird-wing bird-three"><path d="M95 13Q101 5 108 13Q115 6 123 10Q114 10 108 17Q101 10 95 13Z"/></g></svg></div>`;
 scene.append(layer);
}
