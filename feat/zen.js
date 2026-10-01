{
// ───────────────────────── «Сад камней» (karesansui): rake white gravel, set the stones, smooth it all again ─────────────────────────
// S.ext.zen = {o:[[key,x,y]…] moss+stones in garden units (600×900), st:[strokes] the raked pattern (replayed on open),
//   days: gardens finished on different days, last: dayKey of the last one, th: small jpeg of the garden for the courtyard patch}
// strokes: ["r",x,y,x,y…] a rake pass (centre line) · ["c",x,y,r] ripples round a stone · ["p",x,y,dir…] Musya's paw prints
const ZN_R={s1:[274,0,304,260],s2:[220,274,236,204],s3:[0,486,198,162],s4:[402,486,162,146],s5:[720,274,268,180],s6:[566,486,144,128],s7:[0,274,218,210],s8:[712,486,112,100],m1:[580,0,336,228],m2:[458,274,260,188],m3:[200,486,200,156],lt:[0,0,272,272]};
const ZN_A=1.6,ZN_GW=600,ZN_GH=900,ZN_N=4,ZN_SP=11,ZN_GV=3.6,ZN_O=1.25,ZN_MAX=7;   // atlas px per garden unit, garden size, tines, tine step, groove width, emboss offset
const ZN_HR={s1:56,s2:42,s3:34,s4:28,s5:40,s6:24,s7:39,s8:18,m1:84,m2:62,m3:46};    // hit / ripple radius of each thing
const ZN_DEF=[["m1",188,300],["m2",420,652],["s1",190,284],["s4",262,344],["s5",452,214],["s7",428,640],["s6",140,724]];
const ZN_LT=[84,86];   // the stone lantern stands in the top-left corner (sprite centre)
const ZN_LINES=["Гравий помнит каждое движение граблей.","Камни стоят, как острова в белом море.","Тихо. Только ветер в колокольчике.","Муся смотрит на круги, как на воду.","Ни счёта, ни времени — только шорох гравия."];
let ZN_IM=null,znSc=null,znNz=null,znThIm=null;
function znLoad(){if(!ZN_IM)ldImg("assets/items/atlas_zn.webp",im=>{ZN_IM=im;});}
function znS(){return S.ext.zen||(S.ext.zen={o:ZN_DEF.map(a=>a.slice()),st:null,days:0,last:null});}
const znStone=k=>k[0]==="s",znCount=()=>znS().o.filter(a=>znStone(a[0])).length;
function znWord(n){const a=n%10,b=n%100;return n+" "+(a===1&&b!==11?"камень":a>=2&&a<=4&&(b<12||b>14)?"камня":"камней");}
function znDefSt(){const st=[];for(let y=24;y<ZN_GH;y+=ZN_N*ZN_SP)st.push(["r",-30,y,ZN_GW+30,y]);
  for(const [k,x,y] of ZN_DEF)if(k!=="s1"&&k!=="s4"&&k!=="s7")st.push(["c",x,y,ZN_HR[k]+12]);return st;}

// ── sounds: gravel scratch (looping filtered noise that follows the rake speed), a wooden clack, a wind chime
function znNoise(c){if(znNz)return znNz;const b=c.createBuffer(1,c.sampleRate*1.5|0,c.sampleRate),d=b.getChannelData(0);for(let i=0;i<d.length;i++)d[i]=(Math.random()*2-1)*(Math.random()<.07?1:.3);return znNz=b;}
function znScrape(on){if(!snd.on||!snd.ctx)return;const c=snd.ctx;
  if(on&&!znSc){const s=c.createBufferSource();s.buffer=znNoise(c);s.loop=true;const f=c.createBiquadFilter();f.type="bandpass";f.frequency.value=2400;f.Q.value=.7;const h=c.createBiquadFilter();h.type="highpass";h.frequency.value=700;
    const g=c.createGain();g.gain.value=0;s.connect(f);f.connect(h);h.connect(g);g.connect(c.destination);s.start();znSc={s,f,g};}
  if(!on&&znSc){const z=znSc;znSc=null;z.g.gain.setTargetAtTime(0,c.currentTime,.07);setTimeout(()=>{try{z.s.stop();}catch(e){}},500);}}
function znVol(v){if(znSc&&snd.ctx){const n=snd.ctx.currentTime;znSc.g.gain.setTargetAtTime(clamp(v,0,1)*.1,n,.04);znSc.f.frequency.setTargetAtTime(1900+clamp(v,0,1)*1900,n,.06);}}
function znSweepSnd(){znScrape(true);znVol(.25);setTimeout(()=>znVol(.55),300);setTimeout(()=>znVol(.3),1000);setTimeout(()=>znScrape(false),1450);}
function znClack(){tone(1180,.05,"triangle",.07);setTimeout(()=>tone(820,.09,"triangle",.05),55);}
function znChime(){const b=pick([1568,1760,2093]);[0,1,2].forEach(i=>setTimeout(()=>{const f=b*pick([1,1.26,1.5,2]);tone(f,2.2,"sine",.016);tone(f*2.76,.7,"sine",.005);},i*rand(130,280)));}

// ── carved grooves: a band of fresh gravel, then each line stroked lit (bottom-right), shaded (top-left) and filled with gravel again
function znPoly(g,p,i0=1){g.moveTo(p[i0],p[i0+1]);for(let i=i0+2;i<p.length;i+=2)g.lineTo(p[i],p[i+1]);}
function znTines(P){const n=(P.length-1)/2,T=[];for(let j=0;j<ZN_N;j++)T.push([0]);
  for(let i=0;i<n;i++){const a=Math.max(0,i-2),b=Math.min(n-1,i+2);let dx=P[1+b*2]-P[1+a*2],dy=P[2+b*2]-P[2+a*2];const L=Math.hypot(dx,dy)||1;dx/=L;dy/=L;
    for(let j=0;j<ZN_N;j++){const o=(j-(ZN_N-1)/2)*ZN_SP;T[j].push(P[1+i*2]-dy*o,P[2+i*2]+dx*o);}}return T;}
function znCarve(g,pat,lines,band,fill){g.save();g.lineCap="round";g.lineJoin="round";
  if(band){g.beginPath();band.fn(g);g.strokeStyle=pat;g.lineWidth=band.w;g.stroke();}
  const go=(o,st)=>{g.save();g.translate(o,o);g.beginPath();lines(g);if(fill){g.fillStyle=st;g.fill();}else{g.strokeStyle=st;g.lineWidth=ZN_GV;g.stroke();}g.restore();};
  go(ZN_O,"rgba(255,251,238,.62)");go(-ZN_O,"rgba(26,28,38,.6)");
  g.beginPath();lines(g);if(fill){g.fillStyle=pat;g.fill();g.fillStyle="rgba(64,66,78,.26)";g.fill();}else{g.lineWidth=ZN_GV-.5;g.strokeStyle=pat;g.stroke();g.strokeStyle="rgba(64,66,78,.24)";g.stroke();}
  g.restore();}
function znRake(g,pat,P){if(P.length<5)return;const T=znTines(P);znCarve(g,pat,gg=>{for(const p of T)znPoly(gg,p);},{w:(ZN_N-1)*ZN_SP+ZN_GV+8,fn:gg=>znPoly(gg,P)});}
function znRipple(g,pat,x,y,r0,a=1){const A0=-Math.PI/2,A1=A0+Math.PI*2*a,rb=r0+1.5*ZN_SP-6;
  znCarve(g,pat,gg=>{for(let j=0;j<ZN_N;j++){const r=r0+j*ZN_SP;gg.moveTo(x+r*Math.cos(A0),y+r*Math.sin(A0));gg.arc(x,y,r,A0,A1);}},
    {w:(ZN_N-1)*ZN_SP+ZN_GV+20,fn:gg=>{gg.moveTo(x+rb*Math.cos(A0),y+rb*Math.sin(A0));gg.arc(x,y,rb,A0,A1);}});}
function znPrints(g,pat,P){znCarve(g,pat,gg=>{for(let i=1;i+2<P.length;i+=3){const x=P[i],y=P[i+1],d=P[i+2];gg.moveTo(x+4.6,y);gg.ellipse(x,y,4.6,3.9,0,0,Math.PI*2);
    for(const a of [-.95,-.32,.32,.95]){const tx=x+d*Math.cos(a)*6.8,ty=y+Math.sin(a)*5.6;gg.moveTo(tx+1.9,ty);gg.arc(tx,ty,1.9,0,Math.PI*2);}}},null,true);}
function znStroke(g,pat,s){if(s[0]==="r")znRake(g,pat,s);else if(s[0]==="c")znRipple(g,pat,s[1],s[2],s[3]);else if(s[0]==="p")znPrints(g,pat,s);}
function znPush(q,s){const z=znS();(z.st||(z.st=[])).push(s);let n=z.st.reduce((a,b)=>a+b.length,0);while(n>30000&&z.st.length>1)n-=z.st.shift().length;q.dirty=1;q.acts++;}

// ── layout: the garden (600×900 units) fits above the tool row; Musya sits on the engawa above it (phone) or beside it (wide)
function znLay(G){const s=G.s,W=G.W,H=G.H,TB=58*s,F=13*s,side=W>H*.9,top=side?16*s:88*s,
  k=Math.min((W-2*F-(side?260*s:14*s))/ZN_GW,(H-TB-top-2*F-12*s)/ZN_GH),gw=ZN_GW*k,gh=ZN_GH*k,gx=(W-gw)/2,gy=H-TB-10*s-F-gh;
  const sit=side?{x:gx+gw+F+90*s,y:gy+gh*.42,sc:.6*s}:{x:gx+gw*.76,y:gy-F+8*s,sc:.44*s};return{s,W,H,TB,F,k,gw,gh,gx,gy,side,sit};}
function znBtns(L){const s=L.s,n=4,gap=8*s,bw=Math.min(150*s,(L.W-gap*(n+1))/n),x0=(L.W-(bw*n+gap*(n-1)))/2,y=L.H-L.TB+2*s,h=L.TB-12*s;
  return[["rake","Грабли"],["stone","Камни"],["smooth","Разровнять"],["done","Готово"]].map(([id,n],i)=>({id,n,x:x0+i*(bw+gap),y,w:bw,h}));}
function znBuild(G){const q=G.st,L=znLay(G),d=Math.min(2,devicePixelRatio||1),w=Math.max(2,Math.round(L.gw*d)),h=Math.max(2,Math.round(L.gh*d));q.L=L;q.lw=G.W;q.lh=G.H;
  // white gravel: fine grain, a few dark and bright pebbles, moonlight falling from the top-left
  const b=document.createElement("canvas");b.width=w;b.height=h;const bg=b.getContext("2d"),im=bg.createImageData(w,h),D=im.data,r=rng(77),cw=(w>>1)+1,cell=new Float32Array(cw*((h>>1)+1));
  for(let i=0;i<cell.length;i++)cell[i]=(r()-.5)*22;
  for(let y=0;y<h;y++)for(let x=0;x<w;x++){const i=(y*w+x)*4,u=x/w,v=y/h,p=r();let l=214-30*(u*.4+v*.6)+cell[(y>>1)*cw+(x>>1)]+(r()-.5)*16;
    if(p<.012)l-=40+50*r();else if(p>.994)l+=26;D[i]=l*.985;D[i+1]=l*.99;D[i+2]=l*.975+3;D[i+3]=255;}
  bg.putImageData(im,0,0);q.base=b;
  q.pat=bg.createPattern(b,"no-repeat");q.pat.setTransform(new DOMMatrix([1/(L.k*d),0,0,1/(L.k*d),0,0]));
  const c=document.createElement("canvas");c.width=w;c.height=h;q.sc=c;q.sg=c.getContext("2d");q.sg.setTransform(L.k*d,0,0,L.k*d,0,0);znReplay(q);
  // the frame's shadow on the gravel + a soft vignette
  const sh=document.createElement("canvas");sh.width=w;sh.height=h;const sg=sh.getContext("2d");sg.setTransform(L.k*d,0,0,L.k*d,0,0);
  let gr=sg.createLinearGradient(0,0,0,26);gr.addColorStop(0,"rgba(8,8,12,.55)");gr.addColorStop(1,"rgba(8,8,12,0)");sg.fillStyle=gr;sg.fillRect(0,0,ZN_GW,26);
  gr=sg.createLinearGradient(0,0,22,0);gr.addColorStop(0,"rgba(8,8,12,.45)");gr.addColorStop(1,"rgba(8,8,12,0)");sg.fillStyle=gr;sg.fillRect(0,0,22,ZN_GH);
  gr=sg.createRadialGradient(ZN_GW*.4,ZN_GH*.4,ZN_GH*.3,ZN_GW*.5,ZN_GH*.5,ZN_GH*.78);gr.addColorStop(0,"rgba(6,8,14,0)");gr.addColorStop(1,"rgba(6,8,14,.4)");sg.fillStyle=gr;sg.fillRect(0,0,ZN_GW,ZN_GH);q.shade=sh;
  // the engawa around the garden: dark planks and the wooden frame
  const B=document.createElement("canvas");B.width=G.W*d;B.height=G.H*d;const g=B.getContext("2d");g.setTransform(d,0,0,d,0,0);const W=G.W,H=G.H,s=L.s,rr=rng(5);
  g.fillStyle="#17120e";g.fillRect(0,0,W,H);const ph=34*s;
  for(let y=0,j=0;y<H;y+=ph,j++){g.fillStyle=`rgb(${30+rr()*10|0},${23+rr()*7|0},${17+rr()*5|0})`;g.fillRect(0,y,W,ph-1.5);for(let i=0;i<18;i++){g.fillStyle=`rgba(${rr()<.5?0:90},${rr()<.5?0:70},${rr()<.5?0:50},.12)`;g.fillRect(rr()*W,y+rr()*ph,40+rr()*160,1);}
    g.fillStyle="rgba(0,0,0,.5)";g.fillRect(0,y+ph-1.5,W,1.5);g.fillStyle="rgba(0,0,0,.35)";g.fillRect(((j*137)%7)/7*W,y,1.5,ph);}
  gr=g.createRadialGradient(W*.15,0,0,W*.3,H*.2,Math.max(W,H));gr.addColorStop(0,"rgba(150,170,200,.12)");gr.addColorStop(1,"rgba(0,0,0,.35)");g.fillStyle=gr;g.fillRect(0,0,W,H);
  const {gx,gy,gw,gh,F}=L;g.fillStyle="rgba(0,0,0,.5)";g.fillRect(gx-F+5*s,gy-F+7*s,gw+2*F,gh+2*F);
  const fr=(x,y,w,h,v)=>{const q2=g.createLinearGradient(x,y,v?x+w:x,v?y:y+h);q2.addColorStop(0,"#6b5038");q2.addColorStop(.45,"#4a3424");q2.addColorStop(1,"#2a1c12");g.fillStyle=q2;g.fillRect(x,y,w,h);
    for(let i=0;i<10;i++){g.fillStyle=`rgba(20,12,6,${.15+rr()*.2})`;v?g.fillRect(x+rr()*w,y,1,h):g.fillRect(x,y+rr()*h,w,1);}};
  fr(gx-F,gy-F,gw+2*F,F,false);fr(gx-F,gy+gh,gw+2*F,F,false);fr(gx-F,gy,F,gh,true);fr(gx+gw,gy,F,gh,true);
  g.strokeStyle="rgba(210,180,140,.28)";g.lineWidth=1;g.strokeRect(gx-F+.5,gy-F+.5,gw+2*F-1,gh+2*F-1);g.strokeStyle="rgba(0,0,0,.6)";g.strokeRect(gx-.5,gy-.5,gw+1,gh+1);
  for(const [x,y] of [[gx-F,gy-F],[gx+gw,gy-F],[gx-F,gy+gh],[gx+gw,gy+gh]]){g.fillStyle="#2a1c12";g.fillRect(x+F*.3,y+F*.3,F*.4,F*.4);}
  q.bg=B;}
function znReplay(q){const g=q.sg;g.save();g.setTransform(1,0,0,1,0,0);g.drawImage(q.base,0,0);g.restore();const z=znS();if(!z.st)z.st=znDefSt();for(const s of z.st)znStroke(g,q.pat,s);}
function znObjs(){const o=znS().o;return[...o.map((a,i)=>i).filter(i=>!znStone(o[i][0])),...o.map((a,i)=>i).filter(i=>znStone(o[i][0])).sort((a,b)=>o[a][2]-o[b][2])];}
function znHit(u,v,stonesOnly){const o=znS().o,L=znObjs().reverse();for(const i of L){const [k,x,y]=o[i];if(stonesOnly&&!znStone(k))continue;const r=ZN_HR[k],dx=(u-x)/(znStone(k)?1:1.25),dy=(v-y)/(znStone(k)?1:.8);if(dx*dx+dy*dy<(r+6)*(r+6))return i;}return-1;}
function znBlit(g,k,x,y,al=1){const r=ZN_R[k];if(!r||!ZN_IM)return;g.globalAlpha=al;g.drawImage(ZN_IM,r[0],r[1],r[2],r[3],x-r[2]/ZN_A/2,y-r[3]/ZN_A/2,r[2]/ZN_A,r[3]/ZN_A);g.globalAlpha=1;}
function znThumb(q){if(!q.sc)return;const c=document.createElement("canvas");c.width=96;c.height=144;const g=c.getContext("2d");g.drawImage(q.sc,0,0,96,144);g.save();g.scale(96/ZN_GW,144/ZN_GH);
  for(const i of znObjs()){const [k,x,y]=znS().o[i];znBlit(g,k,x,y);}znBlit(g,"lt",...ZN_LT);g.restore();try{znS().th=c.toDataURL("image/jpeg",.72);}catch(e){}}

// ── the game
function znTool(G,b,t){const q=G.st;q.cb=null;znClack();
  if(b.id==="rake"||b.id==="stone"){q.tool=b.id;q.sel=-1;return;}
  if(b.id==="smooth"){if(q.sw)return;q.sw=t;q.rip=null;znSweepSnd();return;}
  if(b.id==="done")znFinish(G);}
function znFinish(G){const q=G.st,z=znS(),dk=dayKey();if(q.dirty)znThumb(q);q.first=q.acts>0&&z.last!==dk;
  if(q.first){z.last=dk;z.days=(z.days||0)+1;}if(q.acts>0)award("zn_first");if((z.days||0)>=7)award("zn_week");
  chime([1568,2093,2637]);gEnd();   // gEnd adds the usual joy and takes 8 energy: meditation gives energy back instead
  S.needs.joy=clamp(S.needs.joy+(q.first?8:2),0,100);S.needs.energy=clamp(S.needs.energy+(q.first?16:11),0,100);save();}
function znSit(q){return q.L.sit;}
const ZEN={id:"zn_garden",hidden:true,n:"Сад камней",tag:"枯山水 · Карэсансуй",bg:"room",lives:null,time:null,icon:"🪨",lore:"",how:"",
 init(G,t){znLoad();G.score=0;Object.assign(G.st,{tool:"rake",sel:-1,live:null,cb:null,rip:null,sw:0,walk:null,acts:0,dirty:0,thT:t,
   nextWalk:t+rand(12,20),nextChime:t+1.5,back:-9,bub:null,groom:0,nextGroom:t+rand(8,14)});znBuild(G);},
 step(G,t,dt){const q=G.st;if(q.lw!==G.W||q.lh!==G.H)znBuild(G);
   if(q.sw&&t-q.sw>1.45){q.sw=0;znS().st=[];znReplay(q);q.dirty=1;q.acts++;q.bub={e:"😌",t};}
   if(q.rip&&t-q.rip.t0>1.15){const r=q.rip;q.rip=null;znRipple(q.sg,q.pat,r.x,r.y,r.r0);znPush(q,["c",Math.round(r.x),Math.round(r.y),r.r0]);znScrape(false);if(Math.random()<.6)q.bub={e:pick(["😌","😺"]),t};}
   if(!q.walk&&!petAway()&&t>q.nextWalk&&!q.sw){const dir=Math.random()<.5?1:-1;q.walk={dir,x:dir>0?-60:ZN_GW+60,y:rand(250,820),lx:dir>0?-60:ZN_GW+60,side:1,s:null};}
   if(q.walk){const w=q.walk;w.x+=w.dir*64*dt;
     if(Math.abs(w.x-w.lx)>=20){w.lx=w.x;w.side=-w.side;const px=Math.round(w.x-w.dir*12),py=Math.round(w.y-3+w.side*5);
       if(px>8&&px<ZN_GW-8){if(!w.s){w.s=["p"];znPush(q,w.s);q.acts--;}w.s.push(px,py,w.dir);znPrints(q.sg,q.pat,["p",px,py,w.dir]);q.dirty=1;}}
     if(w.x<-70||w.x>ZN_GW+70){q.walk=null;q.nextWalk=t+rand(40,70);q.back=t;}}
   if(t>q.nextGroom&&!q.walk){q.groom=t+3.2;q.nextGroom=t+rand(14,24);}
   if(t>q.nextChime){znChime();q.nextChime=t+rand(24,48);}
   if(q.dirty&&t-q.thT>3){q.dirty=0;q.thT=t;znThumb(q);}},
 draw(G,g,t){const q=G.st,L=q.L;if(!L)return;const {k,gx,gy,gw,gh,s}=L,o=znS().o;
   g.drawImage(q.bg,0,0,G.W,G.H);g.drawImage(q.sc,gx,gy,gw,gh);
   g.save();g.beginPath();g.rect(gx,gy,gw,gh);g.clip();g.translate(gx,gy);g.scale(k,k);
   if(q.live)znRake(g,q.pat,q.live);
   if(q.rip)znRipple(g,q.pat,q.rip.x,q.rip.y,q.rip.r0,smooth((t-q.rip.t0)/1.1));
   if(q.sw){const u=clamp((t-q.sw)/1.4,0,1),y=u*(ZN_GH+60)-30;g.fillStyle=q.pat;g.fillRect(0,0,ZN_GW,Math.max(0,y-4));
     g.fillStyle="rgba(0,0,0,.25)";g.fillRect(-10,y+2,ZN_GW+20,9);g.fillStyle="#5a412b";g.fillRect(-10,y-6,ZN_GW+20,10);g.fillStyle="rgba(230,200,150,.35)";g.fillRect(-10,y-6,ZN_GW+20,2);}
   for(const i of znObjs()){const [kk,x,y]=o[i];znBlit(g,kk,x,y);
     if(i===q.sel&&(q.tool==="stone"||q.selT>t)){g.save();g.strokeStyle=`rgba(238,163,187,${.55+.25*Math.sin(t*4)})`;g.lineWidth=2.4/k*.7;g.setLineDash([7,6]);g.beginPath();g.arc(x,y,ZN_HR[kk]+8,0,Math.PI*2);g.stroke();g.restore();}}
   znBlit(g,"lt",...ZN_LT);
   if(q.live&&q.live.length>=5){const n=q.live.length,x=q.live[n-2],y=q.live[n-1],a=Math.atan2(y-q.live[n-3>0?n-3:2],x-q.live[n-4>0?n-4:1]);   // the rake head under the finger
     g.save();g.translate(x,y);g.rotate(a);g.fillStyle="rgba(0,0,0,.3)";g.fillRect(-2,-24,70,4);g.fillStyle="#6b4e33";g.fillRect(4,-3,70,5);g.fillStyle="rgba(0,0,0,.3)";g.fillRect(-2,-(ZN_N-1)*ZN_SP/2-7,9,(ZN_N-1)*ZN_SP+14);
     g.fillStyle="#7a5a3a";g.fillRect(-4,-(ZN_N-1)*ZN_SP/2-8,7,(ZN_N-1)*ZN_SP+16);g.fillStyle="rgba(240,210,160,.4)";g.fillRect(-4,-(ZN_N-1)*ZN_SP/2-8,2,(ZN_N-1)*ZN_SP+16);g.restore();}
   g.restore();
   // night (or day) light over the whole garden, the frame's shadow, the lantern's warm flicker
   const night=dayTint()[1];g.save();g.globalCompositeOperation="multiply";g.fillStyle=night?"#9ca3b5":"#f2e9d8";g.fillRect(gx,gy,gw,gh);g.restore();g.drawImage(q.shade,gx,gy,gw,gh);
   if(night){const lx=gx+(ZN_LT[0]-11)*k,ly=gy+(ZN_LT[1]-11)*k,R=230*k,fl=.85+.1*Math.sin(t*7.3)+.05*Math.sin(t*13.1),gr=g.createRadialGradient(lx,ly,8*k,lx,ly,R);
     gr.addColorStop(0,`rgba(255,196,120,${.55*fl})`);gr.addColorStop(.18,`rgba(250,170,96,${.3*fl})`);gr.addColorStop(.5,`rgba(240,160,90,${.1*fl})`);gr.addColorStop(1,"rgba(240,160,90,0)");g.save();g.globalCompositeOperation="lighter";g.fillStyle=gr;g.fillRect(gx,gy,Math.min(gw,R+lx-gx),Math.min(gh,R+ly-gy));g.restore();}
   // Musya: sits on the engawa and watches; now and then she walks across and leaves paw prints
   if(!petAway()){const S0=znSit(q);
     if(q.walk){const w=q.walk;drawCatG(g,w.dir>0?"moveRight":"moveLeft",Math.floor(t*10)%8,gx+w.x*k,gy+w.y*k,.52*k);}
     else{const al=clamp((t-q.back)/.8,0,1),fl=S0.y;let st="rest",fi=Math.floor(t*2)%2;
       if(q.live&&q.live.length>2){const n=q.live.length,tx=gx+q.live[n-2]*k,ty=gy+q.live[n-1]*k,gi=gazeIndex(tx-S0.x,(fl-150*S0.sc)-ty);st=gi<8?"gaze9":"gaze10";fi=gi%8;}
       else if(q.groom>t){st="groom";fi=Math.floor(t*8)%8;}
       drawCatG(g,st,fi,S0.x,fl,S0.sc,al);
       if(q.bub){const e=t-q.bub.t;if(e<2.2)drawEmoji(g,q.bub.e,S0.x+46*S0.sc,fl-200*S0.sc-e*8*s,22*s,clamp(Math.min(e*4,(2.2-e)*2),0,1));else q.bub=null;}}}
   // hints and buttons
   const hint=q.tool==="stone"?(q.sel>=0?"Тяни, чтобы передвинуть":"Тяни камни и мох · нажми на гравий — новый камень"):q.acts===0&&!q.live?"Веди пальцем по гравию — это грабли":"";
   if(hint&&!q.sw){g.save();g.font=`600 ${12.5*s}px ${getComputedStyle(document.body).fontFamily}`;const tw=g.measureText(hint).width+24*s,hy=gy+gh-22*s;g.fillStyle="rgba(10,12,14,.62)";g.beginPath();g.roundRect(G.W/2-tw/2,hy-13*s,tw,26*s,13*s);g.fill();g.restore();textC(g,hint,G.W/2,hy,12.5*s,"#e8e2d4",600);}
   q.cb=null;
   if(q.sel>=0&&o[q.sel]&&(q.tool==="stone"?znStone(o[q.sel][0]):q.selT>t)){const [kk,x,y]=o[q.sel],bx=gx+x*k,by=gy+(y-ZN_HR[kk]-8)*k-34*s,w=q.tool==="stone"?104*s:96*s;
     q.cb={x:clamp(bx-w/2,4,G.W-w-4),y:Math.max(4,by),w,h:30*s,fn:q.tool==="stone"?"del":"rip"};btnRect(g,q.cb.x,q.cb.y,w,30*s,q.tool==="stone"?"✕ Убрать":"◎ Круги",true);}
   for(const b of znBtns(L))btnRect(g,b.x,b.y,b.w,b.h,b.n,b.id===q.tool);},
 down(G,x,y,t){const q=G.st,L=q.L;if(!L)return;
   const b=znBtns(L).find(b=>x>=b.x&&x<=b.x+b.w&&y>=b.y&&y<=b.y+b.h);if(b){znTool(G,b,t);return;}
   const o=znS().o;
   if(q.cb&&x>=q.cb.x&&x<=q.cb.x+q.cb.w&&y>=q.cb.y&&y<=q.cb.y+q.cb.h){const i=q.sel,[kk,sx,sy]=o[i];q.cb=null;
     if(q.tool==="stone"){if(znCount()<=3){toast("Меньше трёх камней — уже не сад");return;}o.splice(i,1);q.sel=-1;znClack();q.dirty=1;q.acts++;return;}
     q.selT=0;q.rip={x:sx,y:sy,r0:ZN_HR[kk]+12,t0:t};znScrape(true);znVol(.45);return;}
   const S0=L.sit;if(!q.walk&&!petAway()&&Math.abs(x-S0.x)<70*S0.sc&&y<S0.y&&y>S0.y-190*S0.sc){q.bub={e:pick(["😌","😽","💤"]),t};tone(220,.3,"sine",.03);return;}
   const u=(x-L.gx)/L.k,v=(y-L.gy)/L.k;if(u<-8||v<-8||u>ZN_GW+8||v>ZN_GH+8||q.sw)return;
   if(q.tool==="stone"){const i=znHit(u,v);if(i>=0){q.sel=i;q.drag={i,dx:o[i][1]-u,dy:o[i][2]-v};tone(300,.06,"triangle",.04);return;}
     if(znCount()>=ZN_MAX){toast("Семь камней — больше саду не нужно");q.sel=-1;return;}
     const used=new Set(o.map(a=>a[0])),free=["s2","s3","s8","s5","s6","s4","s7","s1"].filter(k=>!used.has(k)),kk=free[0]||pick(["s3","s6","s8","s4"]);
     o.push([kk,Math.round(clamp(u,30,ZN_GW-30)),Math.round(clamp(v,30,ZN_GH-30))]);q.sel=o.length-1;znClack();q.dirty=1;q.acts++;return;}
   q.sel=-1;q.down={i:znHit(u,v,true)};q.live=["r",Math.round(u),Math.round(v)];q.su=u;q.sv=v;q.mt=t;znScrape(true);},
 move(G,x,y){const q=G.st,L=q.L;if(!L||!G.held)return;const u=(x-L.gx)/L.k,v=(y-L.gy)/L.k,o=znS().o;
   if(q.drag){const a=o[q.drag.i];if(a){a[1]=Math.round(clamp(u+q.drag.dx,20,ZN_GW-20));a[2]=Math.round(clamp(v+q.drag.dy,20,ZN_GH-20));q.drag.mv=1;}return;}
   if(!q.live)return;q.su+=(u-q.su)*.5;q.sv+=(v-q.sv)*.5;const n=q.live.length,dx=q.su-q.live[n-2],dy=q.sv-q.live[n-1],dd=Math.hypot(dx,dy);
   if(dd>=4){q.live.push(Math.round(q.su),Math.round(q.sv));const t=now(),sp=dd/Math.max(.016,t-q.mt);q.mt=t;znVol(sp/700);}},
 up(G){const q=G.st;
   if(q.drag){if(q.drag.mv){znClack();q.dirty=1;q.acts++;}q.drag=null;return;}
   if(!q.live)return;const P=q.live;q.live=null;znScrape(false);
   if(P.length>=7){znRake(q.sg,q.pat,P);znPush(q,P);}
   else if(q.down&&q.down.i>=0){q.sel=q.down.i;q.selT=now()+5;}},
 stat:G=>`🪨 ${znWord(znCount())}`,
 card(G){const q=G.st,z=znS();return`<div class="card"><p class="tag">枯山水 · Карэсансуй</p><h3>${q.first?"Мысли улеглись, как песок":"Сад готов"}</h3><p class="lore">${pick(ZN_LINES)}</p>
   <p>${q.first?"Первый сад за день: Муся спокойна и отдохнула.":"Муся посидела с тобой в тишине."} Дней в саду: ${z.days||0}.</p>
   <div class="row"><button class="btn" id="gHome">Домой</button><button class="btn primary" id="gAgain">Вернуться в сад</button></div></div>`;},
 after(){ui();}};
GAMES.push(ZEN);
function znOpen(){if(G.id)return;closePanel();znLoad();openPlace("zn_garden");}
STAMPS.push(["zn_first","石","Сад камней","Разровняй гравий граблями и нажми «Готово» в саду камней"],["zn_week","禅","Семь дней тишины","Делай сад камней семь разных дней"]);

// ── the courtyard: the tray button (after the sakura's) and the saved garden as a small flat patch on the ground
hook("tray",(tray,room)=>{if(room!=="courtyard"||(S.trayMode[room]||"play")!=="play")return;const el=tray.querySelector(".items");if(!el)return;
  const h=`<button class="item wide" data-x="zn:open"><span class="ico">🪨</span><span class="nm">Сад камней</span></button>`,sk=[...el.querySelectorAll('[data-x^="sk:"]')].pop();
  if(sk)sk.insertAdjacentHTML("afterend",h);else el.insertAdjacentHTML("afterbegin",h);});
hook("click",k=>{if(!k.startsWith("zn:"))return;if(k==="zn:open")znOpen();return true;});
const ZN_P={x:665,y0:1196,y1:1272,w:200};
function znQuad(){const cx=visX(ZN_P.x,ZN_P.w*.5+40),x0=cx-ZN_P.w/2,x1=cx+ZN_P.w/2,oc=curRow;curRow=null;const Q=[[x0,ZN_P.y0],[x1,ZN_P.y0],[x1,ZN_P.y1],[x0,ZN_P.y1]].map(([a,b])=>imgToStage(a,b,CAT_D));curRow=oc;return Q;}
function znPatchIm(){const th=znS().th;if(!th)return null;if(!znThIm||znThIm.s0!==th){znThIm=new Image();znThIm.s0=th;znThIm.src=th;}return znThIm.complete&&znThIm.naturalWidth?znThIm:null;}
hook("draw",(t,front)=>{if(front||S.room!=="courtyard"||!S.ext.zen||scene.on)return;const im=znPatchIm();if(!im)return;const Q=znQuad(),n=8;
  ctx.save();ctx.beginPath();Q.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();ctx.fillStyle="rgba(0,0,0,.45)";ctx.lineWidth=7*BGM.k;ctx.strokeStyle="rgba(0,0,0,.35)";ctx.stroke();
  for(let j=0;j<n;j++){const a=j/n,b=(j+1)/n,L0=[mix(Q[0][0],Q[3][0],a),mix(Q[0][1],Q[3][1],a)],R0=[mix(Q[1][0],Q[2][0],a),mix(Q[1][1],Q[2][1],a)],L1=[mix(Q[0][0],Q[3][0],b),mix(Q[0][1],Q[3][1],b)];
    ctx.save();ctx.transform(R0[0]-L0[0],R0[1]-L0[1],L1[0]-L0[0],L1[1]-L0[1],L0[0],L0[1]);ctx.globalAlpha=dayTint()[1]?.78:.92;ctx.drawImage(im,0,im.height*a,im.width,Math.min(im.height/n+.5,im.height*(1-a)),0,0,1,1.04);ctx.restore();}
  ctx.beginPath();Q.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();ctx.lineWidth=Math.max(2,9*BGM.k);ctx.strokeStyle="#3a2818";ctx.stroke();ctx.lineWidth=Math.max(1,2*BGM.k);ctx.strokeStyle="rgba(200,160,110,.35)";ctx.stroke();ctx.restore();});
function znIn(Q,x,y){let s=0;for(let i=0;i<4;i++){const [ax,ay]=Q[i],[bx,by]=Q[(i+1)%4],c=(bx-ax)*(y-ay)-(by-ay)*(x-ax);if(c===0)continue;if(s===0)s=Math.sign(c);else if(Math.sign(c)!==s)return false;}return true;}
hook("hit",(x,y)=>{if(S.room!=="courtyard"||!znPatchIm()||scene.on)return;if(!znIn(znQuad(),x,y))return;audioInit();znClack();znOpen();return true;});
hook("hub",()=>{const z=znS(),done=z.last===dayKey();
  return`<div class="hubc"><h4>🪨 Сад камней <i>枯山水</i></h4><p>${done?"Сегодня гравий уже разровнен — мысли улеглись.":"Белый гравий, камни во мху и грабли. Ни счёта, ни времени."}${z.days?` Дней в саду: ${z.days}.`:""}</p><div class="row"><button class="btn" data-x="zn:open">Открыть сад</button></div></div>`;});
hook("boot",()=>{if(S.ext.zen)znLoad();});
hook("sec",()=>{if(znSc&&G.id!=="zn_garden")znScrape(false);});
X.zn={open:znOpen,st:znS,
  // tests: drag the rake along garden-unit points, tap a garden point, ripple a stone, smooth, send Musya walking, finish
  rake(pts){if(G.id!=="zn_garden")return;const L=G.st.L,sx=u=>L.gx+u*L.k,sy=v=>L.gy+v*L.k;G.held=true;G.def.down(G,sx(pts[0][0]),sy(pts[0][1]),now());for(const [u,v] of pts.slice(1))for(let i=0;i<4;i++)G.def.move(G,sx(u),sy(v));G.held=false;G.def.up(G);},
  tap(u,v){const L=G.st.L;G.held=true;G.def.down(G,L.gx+u*L.k,L.gy+v*L.k,now());G.held=false;G.def.up(G);},
  btn(id){const b=znBtns(G.st.L).find(b=>b.id===id);G.def.down(G,b.x+b.w/2,b.y+b.h/2,now());},
  ripple(i){const q=G.st,[k,x,y]=znS().o[i];q.rip={x,y,r0:ZN_HR[k]+12,t0:now()};},
  walk(){G.st.nextWalk=0;},cb(){return G.st.cb;},quad:znQuad};
}
