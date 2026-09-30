{
// ───────────────────────── «Сны Муси» (prefix dr): a thought bubble over sleeping Musya opens her dream ─────────────────────────
// Six dream worlds drawn on the mini-game canvas (static layers cached per open), glowing fragments to catch, nightmare shadows
// that steal them and Baku the dream-eater who eats the shadows when called. Dream-only things «Из снов», the «Сонник» in the album.
const DR_SPR={moon:[0,0,400,400],shrine:[402,0,460,280],torii:[0,402,300,270],furinA:[302,402,84,200],furinB:[388,402,84,200],furinC:[474,402,84,200],bubble:[560,402,230,170],
 fishR:[792,402,210,150],fishW:[0,674,210,150],fishG:[212,674,210,150],cloudA:[424,674,330,150],cloudB:[756,674,260,120],cloudC:[0,826,220,110],boat:[222,826,300,110],puff:[524,826,56,44]};
let drSheet=null;ldImg("assets/bg/dr_sprites.webp",im=>{drSheet=im;});
MON.m_dr_baku=[460,400];
const DR_HINT="Такое можно найти только во сне…",DR_SRC="💭 из снов Муси";
addItems([{id:"dr_fish",n:"Рыба-фонарик",w:170,h:190,a:"t",glow:[72,104],at:["dr",592,0]},{id:"dr_jar",n:"Банка с сонными огоньками",w:120,h:160,a:"b",glow:[60,104],at:["dr",0,232]},
 {id:"dr_pillow",n:"Облачная подушка",w:210,h:120,a:"b",at:["dr",324,232]},{id:"dr_key",n:"Лунный ключ",w:100,h:220,a:"t",at:["dr",196,0]},
 {id:"dr_door",n:"Бумажная дверца",w:140,h:210,a:"b",glow:[70,104],at:["dr",298,0]},{id:"dr_hglass",n:"Песочные часы с лунным песком",w:110,h:180,a:"b",at:["dr",764,0]},
 {id:"dr_furin",n:"Стеклянный фурин из сна",w:96,h:230,a:"t",at:["dr",0,0]},{id:"dr_bell",n:"Колокольчик тишины",w:130,h:180,a:"b",at:["dr",876,0]},
 {id:"dr_boat",n:"Звёздная лодочка",w:210,h:110,a:"b",at:["dr",536,232]},{id:"dr_feather",n:"Перо сна",w:96,h:230,a:"b",at:["dr",98,0]},
 {id:"dr_torii",n:"Храм в чаше",w:200,h:150,a:"b",at:["dr",122,232]},{id:"dr_baku",n:"Маска Баку",w:150,h:200,a:"t",at:["dr",440,0]}]
 .map(i=>Object.assign(i,{c:"Из снов",p:0,src:DR_SRC,hint:DR_HINT})),{dr:[1024,392]});
const DR_ITEMS=["dr_fish","dr_jar","dr_pillow","dr_key","dr_door","dr_hglass","dr_furin","dr_bell","dr_boat","dr_feather","dr_torii","dr_baku"];
BESTIARY.push(["dr_baku","m_dr_baku","Баку","Пожиратель снов: хобот слона, лапы тигра, хвост быка. В старину его имя писали на листке и клали под подушку, чтобы он съел дурной сон."]);
STAMPS.push(["dr_dream","夢","Сновидица","Загляни в сон спящей Муси"],["dr_all","枕","Сонник","Посмотри все шесть снов Муси"],["dr_bakufr","獏","Друг Баку","Баку съел пять кошмаров"]);
// the six dreams: title, a line for the dream book, the things that can be found there, Musya's tint, the fragments' light
const DRK=[
 {id:"fish",n:"Рыбы-фонари",jp:"金魚提灯",line:"Над спящим городом плыли бумажные рыбы, и в каждой горела свеча.",items:["dr_fish","dr_jar"],tint:"rgba(70,60,130,.3)",glow:"255,196,120",pv:"fishR"},
 {id:"moon",n:"Лестница к луне",jp:"月の階",line:"Облака сложились в ступени, а на луне заяц толок в ступке моти.",items:["dr_pillow","dr_key"],tint:"rgba(80,90,160,.28)",glow:"214,226,255",pv:"moon"},
 {id:"doors",n:"Тысяча дверей",jp:"千の襖",line:"Коридор без конца. За каждой дверью кто-то был — но только тенью.",items:["dr_door","dr_hglass"],tint:"rgba(90,50,40,.26)",glow:"255,206,140",pv:"door"},
 {id:"furin",n:"Сад колокольчиков",jp:"風鈴の庭",line:"Ветер перебирал стеклянные фурин, и каждый звенел своим голосом.",items:["dr_furin","dr_bell"],tint:"rgba(40,90,120,.3)",glow:"170,236,240",pv:"furinA"},
 {id:"river",n:"Звёздная река",jp:"天の川",line:"Муся плыла по Млечному Пути в лодочке из бамбукового листа.",items:["dr_boat","dr_feather"],tint:"rgba(60,60,150,.32)",glow:"236,232,255",pv:"boat"},
 {id:"temple",n:"Затонувший храм",jp:"水底の社",line:"Над храмом, ушедшим под воду, шёл тихий дождь из лепестков.",items:["dr_torii"],tint:"rgba(80,60,130,.3)",glow:"255,182,206",pv:"torii"}];
const DRK_BY=Object.fromEntries(DRK.map(k=>[k.id,k]));
const drS=()=>S.ext.dream||(S.ext.dream={n:0,seen:{},frag:0,eaten:0});
document.head.insertAdjacentHTML("beforeend",`<style>.dr-book{display:grid;gap:8px;margin-bottom:12px}.dr-d{border:1px solid var(--line);border-radius:12px;padding:10px 12px;background:#0b0d16}.dr-d b{font-family:var(--display);font-size:17px;color:var(--paper)}.dr-d i{font-style:normal;font-family:var(--jp);color:var(--sakura);font-size:13px;margin-left:6px}.dr-d p{margin:4px 0 6px;font-size:13px;color:var(--muted);line-height:1.45}.dr-d.off{opacity:.55}.dr-its{display:flex;gap:10px;align-items:flex-end}.dr-its .ath{filter:brightness(0) opacity(.35)}.dr-its .on .ath{filter:none}.dr-its>span{display:flex;flex-direction:column;align-items:center;gap:2px;font-size:10.5px;color:var(--muted)}.dr-card .dish{min-height:90px;align-items:center}</style>`);

// ───── helpers: canvases, sprites, glows ─────
function drCv(W,H){const c=document.createElement("canvas"),d=Math.min(2,devicePixelRatio||1);c.width=Math.max(1,W*d|0);c.height=Math.max(1,H*d|0);const g=c.getContext("2d");g.setTransform(d,0,0,d,0,0);return[c,g];}
function drGlowSp(rgb){const c=document.createElement("canvas");c.width=c.height=64;const g=c.getContext("2d"),gr=g.createRadialGradient(32,32,0,32,32,32);gr.addColorStop(0,`rgba(${rgb},1)`);gr.addColorStop(.3,`rgba(${rgb},.38)`);gr.addColorStop(1,`rgba(${rgb},0)`);g.fillStyle=gr;g.fillRect(0,0,64,64);return c;}
const DR_GL={},drGl=rgb=>DR_GL[rgb]||(DR_GL[rgb]=drGlowSp(rgb));
function drSmoke(){if(drSmoke.c)return drSmoke.c;const c=document.createElement("canvas");c.width=c.height=96;const g=c.getContext("2d"),gr=g.createRadialGradient(48,48,0,48,48,48);gr.addColorStop(0,"rgba(4,2,10,.92)");gr.addColorStop(.55,"rgba(10,6,20,.55)");gr.addColorStop(1,"rgba(10,6,20,0)");g.fillStyle=gr;g.fillRect(0,0,96,96);return drSmoke.c=c;}
// a sprite from the sheet, centred at x,y, width w
function drSp(g,n,x,y,w,a=1,rot=0,flip=false,ay=.5){const r=DR_SPR[n];if(!drSheet||!r||a<=0)return;const h=w*r[3]/r[2];g.save();g.globalAlpha=a;g.translate(x,y);if(rot)g.rotate(rot);if(flip)g.scale(-1,1);g.drawImage(drSheet,r[0],r[1],r[2],r[3],-w/2,-h*ay,w,h);g.restore();}
function drGlow(g,rgb,x,y,r,a){if(a<=0)return;g.save();g.globalCompositeOperation="lighter";g.globalAlpha=Math.min(1,a);g.drawImage(drGl(rgb),x-r,y-r,r*2,r*2);g.restore();}
// soft painterly nebula: a tiny random grid blown up with smoothing
function drNeb(g,W,H,rgb,n,seed,alpha){const r=rng(seed),c=document.createElement("canvas");c.width=n;c.height=Math.max(2,Math.round(n*H/W));const x=c.getContext("2d"),im=x.createImageData(c.width,c.height);
  for(let i=0;i<im.data.length;i+=4){im.data[i]=rgb[0];im.data[i+1]=rgb[1];im.data[i+2]=rgb[2];im.data[i+3]=Math.pow(r(),2.4)*255*alpha;}x.putImageData(im,0,0);g.save();g.imageSmoothingEnabled=true;g.imageSmoothingQuality="high";g.drawImage(c,0,0,W,H);g.restore();}
function drStars(g,W,H,n,seed,y1=1){const r=rng(seed);for(let i=0;i<n;i++){const x=r()*W,y=r()*H*y1,a=.15+r()*.75,big=r()<.07;g.fillStyle=`rgba(236,232,255,${a})`;if(big){drGlow(g,"220,220,255",x,y,6,.5);g.fillRect(x-.9,y-.9,1.8,1.8);}else{const z=.5+r();g.fillRect(x,y,z,z);}}}
function drVig(g,W,H,a=.6){const v=g.createRadialGradient(W/2,H*.55,Math.min(W,H)*.3,W/2,H*.55,Math.max(W,H)*.78);v.addColorStop(0,"rgba(0,0,0,0)");v.addColorStop(1,`rgba(3,2,12,${a})`);g.fillStyle=v;g.fillRect(0,0,W,H);}
function drSky(g,W,H,stops){g.fillStyle=vGrad(g,0,H,stops);g.fillRect(0,0,W,H);}
function drRidge(g,W,y,amp,seed,col,H){const r=rng(seed);g.fillStyle=col;g.beginPath();g.moveTo(0,H);let x=0;g.lineTo(0,y);while(x<W){x+=20+r()*50;g.lineTo(x,y-r()*amp-Math.sin(x*.01+seed)*amp*.5);}g.lineTo(W,H);g.fill();}
// Musya, tinted to the dream's light (one small offscreen canvas, reused every frame)
const drCatC=document.createElement("canvas");drCatC.width=384;drCatC.height=416;const drCatG=drCatC.getContext("2d");
function drCat(g,tint,st,f,x,floor,sc,a=1,axis=0){const im=IMG[st];if(!im||a<=0)return;const c=drCatG;c.globalCompositeOperation="source-over";c.clearRect(0,0,384,416);c.drawImage(im,f*384,0,384,416,0,0,384,416);
  c.globalCompositeOperation="source-atop";c.fillStyle=tint;c.fillRect(0,0,384,416);c.globalCompositeOperation="source-over";
  g.save();g.globalAlpha=a;if(axis){g.translate(0,axis*2);g.scale(1,-1);}g.drawImage(drCatC,x-96*sc,floor-195*sc,192*sc,208*sc);g.restore();}
// shadow puppets for the paper doors: silhouettes of the house's yōkai, blurred as if behind shoji
function drSil(){if(drSil.l)return drSil.l;drSil.l=[];for(const id of["m_kitsune","m_tanuki","m_nekomata","m_kappa","m_warashi","m_obake"]){const im=MIMG[id];if(!im)continue;const c=document.createElement("canvas");c.width=im.width/2+20;c.height=im.height/2+20;const g=c.getContext("2d");
  g.filter="blur(3px)";g.drawImage(im,10,10,im.width/2,im.height/2);g.filter="none";g.globalCompositeOperation="source-in";g.fillStyle="rgba(28,14,20,.8)";g.fillRect(0,0,c.width,c.height);drSil.l.push(c);}return drSil.l;}

// ───── the six worlds: static layer (bg), live layers behind/in front of Musya, where fragments are born, where Musya is ─────
const DRW={
fish:{bg(g,W,H,s){drSky(g,W,H,[[0,"#070a26"],[.55,"#1a1846"],[.86,"#34295a"],[1,"#120e24"]]);drNeb(g,W,H,[120,90,190],14,3,.55);drNeb(g,W,H,[70,110,200],40,4,.25);drStars(g,W,H,170,5,.8);
   const hz=H*.88,gl=g.createLinearGradient(0,hz-H*.2,0,hz);gl.addColorStop(0,"rgba(200,150,190,0)");gl.addColorStop(1,"rgba(200,150,190,.22)");g.fillStyle=gl;g.fillRect(0,hz-H*.2,W,H*.2);
   const r=rng(8);g.fillStyle="#08081a";let x=-10;while(x<W+10){const w=(40+r()*60)*s,h=(26+r()*44)*s,y=hz+r()*10*s;g.fillRect(x,y-h*.55,w,H);g.beginPath();g.moveTo(x-8*s,y-h*.5);g.quadraticCurveTo(x+w*.5,y-h*1.05,x+w+8*s,y-h*.5);g.quadraticCurveTo(x+w*.5,y-h*.72,x-8*s,y-h*.5);g.fill();
     if(r()<.55){g.fillStyle=`rgba(255,190,110,${.35+r()*.4})`;g.fillRect(x+w*(.2+r()*.5),y-h*.3,5*s,6*s);g.fillStyle="#08081a";}x+=w+r()*6*s;}
   const px=W*.8,py=hz;for(let i=0;i<5;i++){const w=(70-i*11)*s,y=py-(i+1)*26*s;g.fillRect(px-w*.3,y,w*.6,26*s);g.beginPath();g.moveTo(px-w*.7,y+4*s);g.quadraticCurveTo(px,y-10*s,px+w*.7,y+4*s);g.lineTo(px+w*.4,y+8*s);g.lineTo(px-w*.4,y+8*s);g.fill();}g.fillRect(px-1.5*s,py-170*s,3*s,40*s);
   g.fillRect(0,hz+18*s,W,H);drVig(g,W,H,.5);},
 init(q,G){const r=rng(11),W=G.W,H=G.H;q.fish=[];for(let i=0;i<7;i++){const z=.35+r()*.75,dir=r()<.5?-1:1;q.fish.push({sp:["fishR","fishW","fishG"][i%3],x:r()*W,y:H*(.1+r()*.55),z,dir,v:(10+16*z)*G.s,ph:r()*6});}q.fish.sort((a,b)=>a.z-b.z);},
 step(q,G,t,dt){const W=G.W;for(const f of q.fish){f.x+=f.dir*f.v*dt;if(f.x<-120*G.s&&f.dir<0)f.x=W+110*G.s;if(f.x>W+120*G.s&&f.dir>0)f.x=-110*G.s;}},
 fishDraw(g,f,t,s){const w=150*f.z*s,y=f.y+Math.sin(t*.8+f.ph)*9*s;drGlow(g,"255,170,100",f.x,y,w*.9,.45+.1*Math.sin(t*3+f.ph));drSp(g,f.sp,f.x,y,w,.95,Math.sin(t*1.3+f.ph)*.06,f.dir>0);f.sy=y;},
 back(q,G,g,t){for(const f of q.fish)if(f.z<.95)this.fishDraw(g,f,t,G.s);},
 front(q,G,g,t){for(const f of q.fish)if(f.z>=.95)this.fishDraw(g,f,t,G.s);},
 spawn(q,G){const f=pick(q.fish.filter(f=>f.x>20&&f.x<G.W-20))||q.fish[0];const w=150*f.z*G.s;return{x:f.x-f.dir*w*.45,y:(f.sy||f.y)+w*.1,vx:f.dir*6*G.s,vy:16*G.s,amp:18*G.s};},
 cat(q,G,t){return{st:"sleep",f:7,x:G.W*(.5+.16*Math.sin(q.e*.21)),y:G.H*(.66+.035*Math.sin(q.e*.5)),sc:0.72}}},
moon:{bg(g,W,H,s){drSky(g,W,H,[[0,"#05071c"],[.5,"#15164a"],[1,"#2c2656"]]);drNeb(g,W,H,[110,100,200],12,21,.5);drStars(g,W,H,200,22,.9);
   const mx=W*.68,my=H*.2,R=Math.min(W*.34,H*.19);drGlow(g,"200,200,255",mx,my,R*3.2,.55);drGlow(g,"255,250,230",mx,my,R*1.6,.5);drSp(g,"moon",mx,my,R*2);
   for(const [n,x,y,w,a] of [["cloudB",W*.15,H*.3,W*.5,.35],["cloudC",W*.9,H*.42,W*.4,.3],["cloudA",W*.35,H*.52,W*.7,.28]])drSp(g,n,x,y,w,a);
   const sea=g.createLinearGradient(0,H*.8,0,H);sea.addColorStop(0,"rgba(90,84,150,0)");sea.addColorStop(1,"rgba(90,84,150,.5)");g.fillStyle=sea;g.fillRect(0,H*.8,W,H*.2);drVig(g,W,H,.45);},
 init(q,G){const W=G.W,H=G.H;q.steps=[];for(let i=0;i<7;i++){const u=i/6;q.steps.push({x:W*(.26+u*.36)+(i%2?1:-1)*W*.13*(1-u*.5),y:H*(.88-u*.54),w:Math.min(W*.5,300*G.s)*(1-u*.52),n:["cloudA","cloudB","cloudC"][i%3],ph:i*1.7});}},
 stepAt(q,i,t){const c=q.steps[i];return[c.x,c.y+Math.sin(t*.7+c.ph)*5*q.s];},
 back(q,G,g,t){for(let i=6;i>=0;i--){const c=q.steps[i],[x,y]=this.stepAt(q,i,t);drSp(g,c.n,x,y,c.w,.95);}},
 front(q,G,g,t){const W=G.W,H=G.H;drSp(g,"cloudA",W*.12+Math.sin(t*.1)*20,H*1.0,W*.8,.6);drSp(g,"cloudB",W*.92-Math.sin(t*.12)*20,H*.99,W*.6,.55);},
 spawn(q,G){const cur=this.cur(q);if(Math.random()<.35)return{x:G.W*rand(.1,.9),y:-10,vx:-8*G.s,vy:22*G.s,amp:10*G.s};const i=Math.min(6,cur+1+Math.floor(Math.random()*3)),c=q.steps[i];return{x:c.x+rand(-.3,.3)*c.w,y:c.y-c.w*.12,vx:0,vy:0,amp:0,step:i};},
 cur(q){return Math.min(6,Math.floor(q.e/(q.dur/7)));},
 cat(q,G,t){const T=q.dur/7,i=this.cur(q),u=(q.e-i*T)/.9,[x1,y1]=this.stepAt(q,i,t),c=q.steps[i];let x=x1,y=y1-c.w*.06;
   if(i>0&&u<1){const [x0,y0]=this.stepAt(q,i-1,t),cp=q.steps[i-1];x=mix(x0,x1,smooth(u));y=mix(y0-cp.w*.06,y1-c.w*.06,smooth(u))-Math.sin(Math.PI*clamp(u,0,1))*50*G.s;}
   return{st:"rest",f:Math.floor(q.e/2.6)%2,x,y,sc:0.74-.3*i/6}}},
doors:{bg(g,W,H,s){g.fillStyle="#0a070c";g.fillRect(0,0,W,H);const vx=W/2,vy=H*.44;drGlow(g,"255,196,120",vx,vy,Math.max(W,H)*.45,.35);drGlow(g,"255,226,170",vx,vy,W*.18,.8);
   const fl=g.createLinearGradient(0,vy,0,H);fl.addColorStop(0,"#3a2616");fl.addColorStop(1,"#120a06");g.fillStyle=fl;g.beginPath();g.moveTo(vx,vy);g.lineTo(-W,H);g.lineTo(W*2,H);g.fill();
   g.strokeStyle="rgba(0,0,0,.35)";g.lineWidth=1;for(let i=-8;i<=8;i++){g.beginPath();g.moveTo(vx,vy);g.lineTo(vx+i*W*.18,H);g.stroke();}
   const ce=g.createLinearGradient(0,0,0,vy);ce.addColorStop(0,"#0c0808");ce.addColorStop(1,"#2a1a12");g.fillStyle=ce;g.beginPath();g.moveTo(vx,vy);g.lineTo(-W,0);g.lineTo(W*2,0);g.fill();drVig(g,W,H,.35);},
 init(q,G){q.sil=drSil();},
 geo(G){const W=G.W,H=G.H;return{vx:W/2,vy:H*.44,span:Math.max(W*.62,H*.3),top:H*.5,bot:H*.42};},
 back(q,G,g,t){const o=this.geo(G),adv=q.e*.32,off=adv%1,base=Math.floor(adv);q.open=[];
   for(let i=11;i>=0;i--){const z0=.5+(i-off)*.5,z1=z0+.5;if(z0<.3)continue;const s0=1/z0,s1=1/z1,fog=clamp(1.2-z0*.19,.06,1),id=i+base,h=Math.abs(Math.sin(id*12.9898)*43758.5453)%1;
     for(const sd of[-1,1]){const xa=o.vx+sd*o.span*s1,xb=o.vx+sd*o.span*s0,ta=o.vy-o.top*s1,tb=o.vy-o.top*s0,ba=o.vy+o.bot*s1,bb=o.vy+o.bot*s0,kind=(h+(sd>0?.5:0))%1;
       const P=[[xa,ta],[xb,tb],[xb,bb],[xa,ba]];g.beginPath();P.forEach(([x,y],k)=>k?g.lineTo(x,y):g.moveTo(x,y));g.closePath();
       g.fillStyle=`rgba(${226*fog+14|0},${196*fog+10|0},${148*fog+12|0},1)`;g.fill();
       const lerp=(u,v)=>{const zz=1/mix(s1,s0,u),x=o.vx+sd*o.span/zz,y=o.vy+mix(-o.top,o.bot,v)/zz;return[x,y];};
       if(kind<.14&&z0<5){g.save();g.clip();const [cx,cy]=lerp(.5,.35),sil=q.sil[id%Math.max(1,q.sil.length)];if(sil){const hh=(o.top+o.bot)*mix(s1,s0,.5)*.7,ww=hh*sil.width/sil.height,sx=cx+Math.sin(t*.6+id)*ww*.35;g.globalAlpha=fog;g.drawImage(sil,sx-ww/2,cy-hh*.35,ww,hh);}g.restore();}
       else if(kind>.86&&z0<6){const [x1,y1]=lerp(.25,0),[x2,y2]=lerp(.25,1),[x3,y3]=lerp(.6,1),[x4,y4]=lerp(.6,0);g.fillStyle=`rgba(255,${200+30*fog|0},150,${.9*fog})`;g.beginPath();g.moveTo(x1,y1);g.lineTo(x4,y4);g.lineTo(x3,y3);g.lineTo(x2,y2);g.fill();q.open.push({x:(x1+x3)/2,y:(y1+y3)/2,z:z0,sd});}
       g.strokeStyle=`rgba(30,18,12,${.5+.5*fog})`;g.lineWidth=Math.max(1,3.2*s0);g.beginPath();for(const v of[.33,.66]){const [x1,y1]=lerp(0,v),[x2,y2]=lerp(1,v);g.moveTo(x1,y1);g.lineTo(x2,y2);}const [m1,n1]=lerp(.5,0),[m2,n2]=lerp(.5,1);g.moveTo(m1,n1);g.lineTo(m2,n2);g.stroke();
       g.lineWidth=Math.max(1.4,7*s0);g.strokeStyle=`rgba(24,14,10,${.7+.3*fog})`;g.beginPath();g.moveTo(xb,tb);g.lineTo(xb,bb);g.moveTo(xa,ta);g.lineTo(xb,tb);g.moveTo(xa,ba);g.lineTo(xb,bb);g.stroke();}
     g.fillStyle=`rgba(24,14,10,${.8*Math.min(1,fog+.2)})`;const ty=o.vy-o.top*s0;g.fillRect(o.vx-o.span*s0,ty-6*s0,o.span*s0*2,10*s0);
     g.strokeStyle=`rgba(0,0,0,${.4*fog})`;g.lineWidth=Math.max(1,2*s0);g.beginPath();g.moveTo(o.vx-o.span*s0,o.vy+o.bot*s0);g.lineTo(o.vx+o.span*s0,o.vy+o.bot*s0);g.stroke();}},
 front(){},
 spawn(q,G){const d=pick(q.open||[]);if(d)return{x:d.x,y:d.y,vx:d.sd*14*G.s,vy:6*G.s,amp:8*G.s};return{x:G.W*rand(.3,.7),y:G.H*.44,vx:rand(-20,20)*G.s,vy:10*G.s,amp:10*G.s};},
 cat(q,G,t){return{st:"sleep",f:7,x:G.W*(.5+.1*Math.sin(q.e*.3)),y:G.H*(.72+.025*Math.sin(q.e*.7)),sc:0.77}}},
furin:{bg(g,W,H,s){drSky(g,W,H,[[0,"#06111e"],[.6,"#0f2434"],[1,"#0a1a22"]]);drNeb(g,W,H,[60,140,160],12,31,.4);drStars(g,W,H,120,32,.6);drGlow(g,"200,230,255",W*.2,H*.12,70*s,.5);g.fillStyle="#d8e8f0";g.beginPath();g.arc(W*.2,H*.12,15*s,0,Math.PI*2);g.fill();
   const r=rng(33);for(const side of[0,1])for(let i=0;i<5;i++){const x=side?W-(8+i*16+r()*10)*s:(8+i*16+r()*10)*s,w=(4+r()*5)*s;g.fillStyle=`rgba(4,12,16,${.7+i*.06})`;g.fillRect(x-w/2,0,w,H);for(let y=r()*40;y<H;y+=(60+r()*40)*s){g.fillRect(x-w*.8,y,w*1.6,2*s);if(r()<.5){g.beginPath();g.ellipse(x+(side?-1:1)*14*s,y+6*s,16*s,3*s,(side?1:-1)*.5,0,Math.PI*2);g.fill();}}}
   const gy=H*.82;g.fillStyle=vGrad(g,gy,H,[[0,"#0a1a1c"],[1,"#040b0c"]]);g.beginPath();g.moveTo(0,gy);for(let x=0;x<=W;x+=24*s)g.lineTo(x,gy-Math.abs(Math.sin(x*.05))*14*s-r()*6*s);g.lineTo(W,H);g.lineTo(0,H);g.fill();
   for(const [x,y,w] of[[W*.5,H*.9,70],[W*.28,H*.95,54],[W*.74,H*.94,58]]){g.fillStyle="#223034";g.beginPath();g.ellipse(x,y,w*s,w*.28*s,0,0,Math.PI*2);g.fill();g.fillStyle="rgba(190,220,230,.18)";g.beginPath();g.ellipse(x-w*.1*s,y-w*.1*s,w*.7*s,w*.12*s,0,0,Math.PI*2);g.fill();}
   const mi=g.createLinearGradient(0,H*.6,0,H*.85);mi.addColorStop(0,"rgba(150,200,210,0)");mi.addColorStop(1,"rgba(150,200,210,.14)");g.fillStyle=mi;g.fillRect(0,H*.6,W,H*.25);drVig(g,W,H,.5);},
 init(q,G){const W=G.W,H=G.H,r=rng(34);q.bells=[];[[5,.02,1],[6,.1,.8],[7,.17,.62]].forEach(([n,y,z],row)=>{for(let i=0;i<n;i++)q.bells.push({x:W*(i+.5+(row%2?.3:0))/n,y:H*y,L:(30+r()*70)*G.s*z,z,sp:["furinA","furinB","furinC"][(i+row)%3],ph:r()*6,row});});q.bells.sort((a,b)=>a.z-b.z);q.gust=0;q.nextGust=q.t0+4;q.wind=[];},
 step(q,G,t,dt){q.gust=Math.max(0,q.gust-dt*.35);if(t>q.nextGust&&!q.end){q.gust=1;q.nextGust=t+rand(5,7.5);for(let i=0;i<5;i++)q.wind.push({y:G.H*rand(.1,.7),x:-60,v:rand(260,380)*G.s,l:rand(60,140)*G.s});
   [1568,1760,2093,2349].slice(0,2+Math.floor(Math.random()*2)).forEach((f,i)=>setTimeout(()=>tone(f*(Math.random()<.5?1:1.5),1.4,"sine",.018),i*170+Math.random()*120));for(let k=0;k<2;k++)drFrag(q,G,t,this.spawn(q,G));}
   for(const w of q.wind)w.x+=w.v*dt;q.wind=q.wind.filter(w=>w.x<G.W+200);},
 bellAt(b,t,q,s){const a=.09*Math.sin(t*1.1+b.ph)+q.gust*.32*Math.sin(t*2.7+b.ph)*b.z;return[b.x+Math.sin(a)*b.L,b.y+Math.cos(a)*b.L,a];},
 back(q,G,g,t){const s=G.s;g.strokeStyle="rgba(200,220,230,.25)";g.lineWidth=1;g.beginPath();for(const row of[0,1,2]){const b=q.bells.find(b=>b.row===row);g.moveTo(0,b.y);g.quadraticCurveTo(G.W/2,b.y+10*s,G.W,b.y);}g.stroke();
   for(const b of q.bells){const [x,y,a]=this.bellAt(b,t,q,s),w=62*b.z*s;g.strokeStyle="rgba(210,220,225,.35)";g.beginPath();g.moveTo(b.x,b.y);g.lineTo(x,y);g.stroke();drGlow(g,"170,230,240",x,y+w*.4,w*.9,.18+.25*q.gust);drSp(g,b.sp,x,y,w,.4+.6*b.z,a*.9,false,.15);b.sx=x;b.sy=y+w*1.5;}
   g.strokeStyle="rgba(220,240,255,.18)";g.lineWidth=1.2;for(const w of q.wind){g.beginPath();g.moveTo(w.x,w.y);g.quadraticCurveTo(w.x+w.l*.5,w.y-8*s,w.x+w.l,w.y);g.stroke();}},
 front(){},
 spawn(q,G){const b=pick(q.bells.filter(b=>b.z>.7));return{x:b.sx||b.x,y:b.sy||b.y+b.L,vx:rand(-10,10)*G.s,vy:20*G.s,amp:24*G.s};},
 cat(q,G,t){return{st:"play",f:Math.floor(q.e*2.2)%8,x:G.W*.5,y:G.H*.9,sc:0.72}}},
river:{C(G,u){const W=G.W,H=G.H,a=[W*.2,H*.3],c=[W*1.05,H*.5],b=[W*.35,H*1.08],x=(1-u)*(1-u)*a[0]+2*(1-u)*u*c[0]+u*u*b[0],y=(1-u)*(1-u)*a[1]+2*(1-u)*u*c[1]+u*u*b[1],dx=2*(1-u)*(c[0]-a[0])+2*u*(b[0]-c[0]),dy=2*(1-u)*(c[1]-a[1])+2*u*(b[1]-c[1]),l=Math.hypot(dx,dy)||1;return{x,y,nx:-dy/l,ny:dx/l,w:W*(.05+.95*Math.pow(u,1.5))*.55};},
 pt(G,u,v){const c=this.C(G,u);return[c.x+c.nx*v*c.w,c.y+c.ny*v*c.w,c];},
 bg(g,W,H,s){drSky(g,W,H,[[0,"#03051a"],[.5,"#0b0e30"],[1,"#15123a"]]);drNeb(g,W,H,[90,80,190],12,41,.45);drStars(g,W,H,220,42,1);
   drRidge(g,W,H*.36,28*s,43,"#0b0c26",H);drRidge(g,W,H*.42,22*s,44,"#08091f",H);g.fillStyle=vGrad(g,H*.45,H,[[0,"rgba(30,30,80,0)"],[1,"rgba(40,36,96,.45)"]]);g.fillRect(0,H*.45,W,H*.55);drStars(g,W,H,60,47,1);
   const G_={W,H};g.save();g.beginPath();for(let i=0;i<=40;i++){const [x,y]=this.pt(G_,i/40,-1);i?g.lineTo(x,y):g.moveTo(x,y);}for(let i=40;i>=0;i--){const [x,y]=this.pt(G_,i/40,1);g.lineTo(x,y);}g.closePath();
   const rg=g.createLinearGradient(0,H*.3,0,H);rg.addColorStop(0,"rgba(120,130,230,.22)");rg.addColorStop(1,"rgba(150,140,240,.34)");g.fillStyle=rg;g.filter=`blur(${10*s}px)`;g.fill();g.filter="none";g.globalCompositeOperation="lighter";g.lineWidth=18*s;g.strokeStyle="rgba(90,90,200,.12)";g.filter=`blur(${14*s}px)`;g.stroke();g.filter="none";g.globalCompositeOperation="source-over";g.clip();drNeb(g,W,H,[210,200,255],30,45,.45);
   const r=rng(46);for(let i=0;i<900;i++){const u=Math.pow(r(),.8),v=(r()*2-1)*(.4+.6*r()),[x,y]=this.pt(G_,u,v);g.fillStyle=`rgba(240,238,255,${.25+r()*.6})`;const z=(.4+u*1.6)*(r()<.1?2:1);g.fillRect(x,y,z,z);}g.restore();drVig(g,W,H,.45);},
 init(q,G){q.flow=[];for(let i=0;i<70;i++)q.flow.push({u:Math.random(),v:rand(-1,1)});q.mag=null;q.nextMag=q.t0+7;},
 step(q,G,t,dt){for(const p of q.flow){p.u+=dt*(.02+.05*p.u);if(p.u>1){p.u=0;p.v=rand(-1,1);}}for(const f of q.frags)if(f.u!=null&&!f.got){f.u+=dt*(.016+.04*f.u);if(f.u>1.02)f.life=0;}
   if(t>q.nextMag&&!q.mag){q.mag={t0:t,y:G.H*rand(.08,.22),dir:Math.random()<.5?-1:1};q.nextMag=t+rand(10,16);}if(q.mag&&t-q.mag.t0>9)q.mag=null;},
 back(q,G,g,t){const s=G.s;g.save();g.globalCompositeOperation="lighter";for(const p of q.flow){const [x,y]=this.pt(G,p.u,p.v),z=(.6+p.u*2.2)*s;g.fillStyle=`rgba(220,220,255,${.35+.4*Math.sin(t*3+p.v*9)})`;g.fillRect(x,y,z,z);}g.restore();
   if(q.mag){const e=t-q.mag.t0,W=G.W;for(let k=0;k<3;k++){const x=q.mag.dir>0?-40+e*70*s-k*26*s:W+40-e*70*s+k*26*s,y=q.mag.y+k*10*s+Math.sin(e*2+k)*6*s,fl=Math.sin(t*9+k)*6*s;g.strokeStyle="rgba(10,10,24,.9)";g.lineWidth=2.4*s;g.beginPath();g.moveTo(x-10*s,y-fl);g.quadraticCurveTo(x-4*s,y-2*s,x,y);g.quadraticCurveTo(x+4*s,y-2*s,x+10*s,y-fl);g.stroke();g.fillStyle="rgba(10,10,24,.9)";g.beginPath();g.ellipse(x,y+1*s,4*s,2*s,0,0,Math.PI*2);g.fill();}}},
 boatPos(q,G,t){const [x,y,c]=this.pt(G,.74,.12*Math.sin(q.e*.18));return[x,y+Math.sin(t*1.2)*3*G.s,c];},
 front(q,G,g,t){const [x,y]=this.boatPos(q,G,t),w=185*G.s;drSp(g,"boat",x,y+10*G.s,w,1,Math.sin(t*.9)*.03);g.save();g.globalCompositeOperation="lighter";g.fillStyle="rgba(200,200,255,.08)";g.beginPath();g.ellipse(x,y+26*G.s,w*.55,8*G.s,0,0,Math.PI*2);g.fill();g.restore();},
 spawn(q,G){return{u:rand(.05,.3),v:rand(-.8,.8),x:0,y:0,vx:0,vy:0,amp:0};},
 cat(q,G,t){const [x,y]=this.boatPos(q,G,t);return{st:"rest",f:Math.floor(q.e/2.8)%2,x,y:y+14*G.s,sc:.6,boat:1}}},
temple:{wl:H=>H*.58,
 bg(g,W,H,s){const wl=H*.58;drSky(g,W,H,[[0,"#0a0d24"],[.45,"#1c1c44"],[.58,"#302a58"],[1,"#07101e"]]);drNeb(g,W,H*.6,[170,120,190],12,51,.45);drStars(g,W,H,120,52,.45);
   drRidge(g,W,wl-40*s,30*s,53,"#141432",H);drRidge(g,W,wl-12*s,16*s,54,"#0d0e26",H);
   const sw=Math.min(W*.86,440*s),sh=sw*280/460,sx=W*.6,sy=wl+sh*.12;drGlow(g,"255,200,150",sx,wl-sh*.3,sw*.6,.25);
   const tw=Math.min(W*.42,200*s),th=tw*270/300,tx=W*.2,ty=wl+th*.2;
   g.save();g.beginPath();g.rect(0,0,W,wl);g.clip();drSp(g,"shrine",sx,sy-sh/2,sw);drSp(g,"torii",tx,ty-th/2,tw);g.restore();
   g.save();g.beginPath();g.rect(0,wl,W,H);g.clip();g.globalAlpha=.3;g.translate(0,wl*2);g.scale(1,-1);drSp(g,"shrine",sx,sy-sh/2,sw);drSp(g,"torii",tx,ty-th/2,tw);g.restore();
   const wa=g.createLinearGradient(0,wl,0,H);wa.addColorStop(0,"rgba(40,50,100,.55)");wa.addColorStop(.4,"rgba(12,20,44,.8)");wa.addColorStop(1,"rgba(4,8,18,.95)");g.fillStyle=wa;g.fillRect(0,wl,W,H-wl);
   g.save();g.beginPath();g.rect(0,wl,W,H);g.clip();g.globalAlpha=.35;drSp(g,"shrine",sx,sy+sh*.35,sw*.98);drSp(g,"torii",tx,ty+th*.3,tw);g.restore();
   g.fillStyle="rgba(8,14,30,.55)";g.fillRect(0,wl+H*.06,W,H);
   g.save();g.globalCompositeOperation="lighter";for(let i=0;i<4;i++){const x=W*(.15+i*.25),gr=g.createLinearGradient(0,0,0,wl);gr.addColorStop(0,"rgba(220,200,255,.07)");gr.addColorStop(1,"rgba(220,200,255,0)");g.fillStyle=gr;g.beginPath();g.moveTo(x,0);g.lineTo(x+40*s,0);g.lineTo(x+120*s,wl);g.lineTo(x+40*s,wl);g.fill();}g.restore();
   g.fillStyle="rgba(210,210,255,.25)";g.fillRect(0,wl-1,W,1.5);drVig(g,W,H,.5);},
 init(q,G){q.pet=[];for(let i=0;i<46;i++)q.pet.push({x:Math.random()*G.W,y:Math.random()*G.H,vy:rand(18,40)*G.s,vx:rand(-8,14)*G.s,rot:rand(0,6),vr:rand(-2,2),sz:rand(4,8)*G.s,ph:rand(0,6)});q.rip=[];},
 step(q,G,t,dt){const wl=this.wl(G.H);for(const p of q.pet){p.x+=(p.vx+Math.sin(t+p.ph)*10*G.s)*dt;p.y+=p.vy*dt;p.rot+=p.vr*dt;if(p.y>wl+p.ph*G.H*.07){if(Math.random()<.25)q.rip.push({x:p.x,y:p.y,t});p.y=-10;p.x=Math.random()*G.W;}}
   for(const f of q.frags)if(!f.got&&f.y>wl+8*G.s&&!f.sank){f.sank=1;f.vy=4*G.s;f.life=Math.min(f.life,1.2);q.rip.push({x:f.x,y:f.y,t,big:1});}q.rip=q.rip.filter(r=>t-r.t<2);},
 back(q,G,g,t){const wl=this.wl(G.H),s=G.s;for(const r of q.rip){const e=(t-r.t)/2;g.strokeStyle=`rgba(220,200,255,${.35*(1-e)})`;g.lineWidth=1;g.beginPath();g.ellipse(r.x,r.y,(6+e*(r.big?60:30))*s,(2+e*(r.big?12:6))*s,0,0,Math.PI*2);g.stroke();}
   g.fillStyle="rgba(210,210,255,.12)";for(let i=0;i<9;i++){const x=(i*97+t*12)%G.W,y=wl+(i*23%60)*s;g.fillRect(x,y,24*s,1);}for(const p of q.pet)if(p.sz<6*s)drawPetal(g,p.x,p.y,p.sz,p.rot,.75);},
 front(q,G,g,t){for(const p of q.pet)if(p.sz>=6*G.s)drawPetal(g,p.x,p.y,p.sz,p.rot,.85);},
 spawn(q,G){return{x:G.W*rand(.1,.9),y:-12,vx:rand(-6,10)*G.s,vy:rand(20,30)*G.s,amp:26*G.s,petal:1};},
 cat(q,G,t){return{st:"sleep",f:7,x:G.W*(.46+.12*Math.sin(q.e*.2)),y:this.wl(G.H)-26*G.s+Math.sin(q.e*.8)*6*G.s,sc:.67,mirror:this.wl(G.H)}}}
};

// ───── the dream as a hidden mini-game ─────
let drRun=null,drNap=-1,drNext=null;
const DR_PENT=[523,587,659,784,880,1046,1175,1318,1568,1760];
const DR_BAKU_HI=["Опять эта тень? Позови меня.","Чую горький сон… Только позови.","Я рядом. Нажми на меня."],DR_BAKU_EAT=["Ням. Страшные сны — самые сытные.","Горько… но я привык.","Спи, маленькая. Я посторожу.","Вот и нет кошмара."];
function drPickKind(){const D=drS(),un=DRK.filter(k=>!D.seen[k.id]);return(un.length?pick(un):pick(DRK.filter(k=>k.id!==D.last)||DRK)).id;}
function drFrag(q,G,t,o){if(!o)return;q.frags.push(Object.assign({t0:t,life:o.u!=null?30:rand(6.5,8.5),ph:rand(0,6),sw:rand(1,2)},o));}
function drSay(q,txt,t,d=3.6){q.say={txt,t,d};}
function drBakuOn(q,t,sh){const G_=G,side=sh.x<G_.W/2?1:-1;q.baku={x:side>0?G_.W+90*G_.s:-90*G_.s,y:G_.H*.3,tx:G_.W*(.5+side*.26),ty:G_.H*.3,state:"in",t0:t,sh,face:-side};
  if(!ST.seen.includes("dr_baku")){ST.seen.push("dr_baku");drSay(q,"Я Баку. Позови меня — и я съем её дурной сон.",t,4.5);setTimeout(()=>toast("Новая запись в бестиарии"),1200);save();}else drSay(q,pick(DR_BAKU_HI),t);chime([392,494,587]);}
function drMusya(q,G,t){const c=DRW[q.k.id].cat(q,G,t);if(q.play&&t-q.play<.9&&c.st!=="sleep"){c.st="play";c.f=Math.floor((t-q.play)*9)%8;}return c;}
const DREAM={id:"dream",hidden:true,n:"Сон Муси",tag:"夢 · Юмэ",bg:"dr",lives:null,time:null,icon:"💭",lore:"",how:"",
 init(G,t){const q=G.st,K=DRK_BY[(drRun&&drRun.kind)||drPickKind()];Object.assign(q,{k:K,t0:t,e:0,dur:56,s:G.s,frags:[],fx:[],sh:[],baku:null,got:0,lost:0,eaten:0,nextFrag:t+1.6,nextSh:t+rand(9,12),say:null,play:0,hurt:-9,end:0,W:0});
   drSay(q,"Лови светящиеся осколки сна",t+3,3.4);drBuild(q,G);$("gTitle").textContent=K.n;chime([523,659,784,1046]);},
 step(G,t,dt){const q=G.st,W=G.W,H=G.H,s=G.s,Wd=DRW[q.k.id];q.e=t-q.t0;q.s=s;if(q.W!==W||q.H!==H)drBuild(q,G);G.bgc=q.bg;if(Wd.step)Wd.step(q,G,t,dt);
   if(!q.end&&q.e>=q.dur){q.end=t;drFinish(q);}if(q.end&&t-q.end>2.6){gEnd();return;}
   if(!q.end&&q.e>2.5&&t>q.nextFrag){drFrag(q,G,t,Wd.spawn(q,G));q.nextFrag=t+rand(1.5,2.3);}
   for(const f of q.frags){if(f.got){f.k=Math.min(1,f.k+dt*2.2);continue;}if(f.u==null){f.x+=(f.vx+Math.sin(t*f.sw+f.ph)*f.amp)*dt;f.y+=f.vy*dt;}f.life-=dt;}
   q.frags=q.frags.filter(f=>f.got?f.k<1:f.life>0&&f.y<H+30);
   for(const p of q.fx){p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=p.g*dt;p.life-=dt;}q.fx=q.fx.filter(p=>p.life>0);
   const cat=drMusya(q,G,t);q.cat=cat;const cy=cat.y-60*cat.sc*s;
   // nightmare shadows creep toward loose fragments or toward Musya
   if(!q.end&&t>q.nextSh&&q.e<q.dur-7&&q.sh.filter(h=>h.st!=="flee").length<(q.e>30?2:1)){const L=Math.random()<.5;const sh={x:L?-50*s:W+50*s,y:H*rand(.55,.85),st:"creep",carry:0,t0:t,ph:rand(0,6),push:0,r:34*s};q.sh.push(sh);q.nextSh=t+rand(10,14);
     tone(65,.9,"sawtooth",.025);const D=drS();if(!q.baku&&(!q.shN||Math.random()<.75))setTimeout(()=>{if(G.id==="dream"&&!q.baku&&sh.st==="creep")drBakuOn(q,now(),sh);},1400);else if(!q.shN)drSay(q,"Тень крадёт осколки! Нажми на неё",t);q.shN=(q.shN||0)+1;}
   for(const h of q.sh){if(h.st==="eaten")continue;let tx,ty;
     if(h.st==="flee"){tx=h.x<W/2?-400*s:W+400*s;ty=h.y;}else{let best=null,bd=1e9;for(const f of q.frags){if(f.got)continue;const fx=f.sx??f.x,fy=f.sy??f.y,d=Math.hypot(fx-h.x,fy-h.y);if(d<bd){bd=d;best=f;}}
       if(best&&bd<W*.6){tx=best.sx??best.x;ty=best.sy??best.y;if(bd<h.r*.8){best.life=0;best.stolen=1;h.carry++;q.lost++;tone(90,.4,"triangle",.04);}}else{tx=cat.x;ty=cy;if(Math.hypot(cat.x-h.x,cy-h.y)<52*s){if(q.got>0){q.got--;h.carry++;q.lost++;q.hurt=t;tone(80,.5,"sawtooth",.04);}h.st="flee";}}}
     const d=Math.hypot(tx-h.x,ty-h.y)||1,v=(h.st==="flee"?110:36)*s*(t<h.push?-.8:1);h.x+=(tx-h.x)/d*v*dt;h.y+=(ty-h.y)/d*v*dt+Math.sin(t*1.7+h.ph)*8*s*dt;h.r=(34+h.carry*4)*s;}
   q.sh=q.sh.filter(h=>h.st!=="eaten"&&h.x>-160*s&&h.x<W+160*s);
   // Baku: floats in, waits to be called, eats the shadow, leaves
   const b=q.baku;if(b){const e=t-b.t0;
     if(b.state==="in"){b.x=mix(b.x,b.tx,dt*2.2);b.y=mix(b.y,b.ty,dt*2.2);if(e>1.2){b.state="wait";b.t0=t;}}
     else if(b.state==="wait"){b.y=b.ty+Math.sin(t*1.4)*8*s;if(e>8||!q.sh.includes(b.sh)||b.sh.st!=="creep"){b.state="out";b.t0=t;}}
     else if(b.state==="go"){const h=b.sh,mx=h.x-b.face*70*s,my=h.y-30*s,d=Math.hypot(mx-b.x,my-b.y);b.x+=(mx-b.x)*Math.min(1,dt*4);b.y+=(my-b.y)*Math.min(1,dt*4);if(d<20*s||e>1.4){b.state="eat";b.t0=t;tone(110,.6,"triangle",.07);tone(220,.4,"sine",.03);}}
     else if(b.state==="eat"){const h=b.sh,[tx,ty]=[b.x+b.face*62*s,b.y+34*s];h.x=mix(h.x,tx,dt*3);h.y=mix(h.y,ty,dt*3);h.r=Math.max(2,h.r-dt*30*s);
       if(e>1.3){h.st="eaten";const n=h.carry+1;for(let i=0;i<n;i++)drFrag(q,G,t,{x:tx,y:ty,vx:rand(-60,60)*s,vy:rand(-40,10)*s,amp:14*s});q.eaten++;drSay(q,pick(DR_BAKU_EAT),t);chime([659,784,988]);b.state="out";b.t0=t;}}
     else if(b.state==="out"){b.y-=dt*90*s;b.x+=b.face*dt*40*s;if(e>2)q.baku=null;}}},
 draw(G,g,t){const q=G.st,W=G.W,H=G.H,s=G.s,Wd=DRW[q.k.id],cat=q.cat;if(!cat)return;
   Wd.back&&Wd.back(q,G,g,t);
   // shadows under everything that glows
   for(const h of q.sh){const sm=drSmoke(),a=h.st==="flee"?.7:.9;drGlow(g,"120,60,150",h.x,h.y,h.r*2.4,.35*a);g.save();g.globalAlpha=a;for(let i=0;i<6;i++){const ox=Math.sin(t*1.3+i*2+h.ph)*h.r*.45,oy=Math.cos(t*1.1+i*1.7)*h.r*.3,r=h.r*(1.1-i*.08);g.drawImage(sm,h.x+ox-r,h.y+oy-r,r*2,r*2);}
     g.strokeStyle="rgba(8,4,14,.6)";g.lineWidth=3*s;for(let i=0;i<4;i++){const a0=i*1.6+h.ph,L=h.r*(1.2+.4*Math.sin(t*2+i));g.beginPath();g.moveTo(h.x,h.y);g.quadraticCurveTo(h.x+Math.cos(a0+t*.7)*L*.6,h.y+Math.sin(a0+t)*L*.5,h.x+Math.cos(a0)*L,h.y+Math.sin(a0)*L*.7+h.r*.3);g.stroke();}
     if(Math.sin(t*1.9+h.ph)>-.92&&h.r>8*s){g.fillStyle="rgba(255,120,100,.85)";for(const sd of[-1,1]){g.beginPath();g.ellipse(h.x+sd*h.r*.22,h.y-h.r*.1,3.2*s,1.8*s,0,0,Math.PI*2);g.fill();}}g.restore();}
   // Musya, softly glowing, drifting
   const hurt=clamp(1-(t-q.hurt)/1.2,0,1),ca=(1-.5*hurt*(Math.sin(t*30)>0?1:0));drGlow(g,"190,180,255",cat.x,cat.y-70*cat.sc*s,150*cat.sc*s,.35);
   if(cat.mirror)drCat(g,q.k.tint,cat.st,cat.f,cat.x,cat.y,cat.sc*s,.18,cat.mirror);
   drCat(g,q.k.tint,cat.st,cat.f,cat.x,cat.y,cat.sc*s,ca);
   Wd.front&&Wd.front(q,G,g,t);
   // fragments: a glow and a little four-pointed crystal
   for(const f of q.frags){let x=f.x,y=f.y,sc=1;if(f.u!=null){const [px_,py_]=DRW.river.pt(G,f.u,f.v);x=px_;y=py_;sc=.55+f.u*.8;}
     if(f.got){const k=smooth(f.k);x=mix(f.gx,cat.x,k);y=mix(f.gy,cat.y-60*cat.sc*s,k);sc*=1-k*.7;}f.sx=x;f.sy=y;
     const a=f.got?1:clamp(Math.min((t-f.t0)/.6,f.life/1),0,1),pul=.8+.2*Math.sin(t*4+f.ph),r=19*s*sc*pul;drGlow(g,q.k.glow,x,y,r*3,a);drGlow(g,"255,255,245",x,y,r*.9,a*.8);
     g.save();g.globalAlpha=a;g.translate(x,y);g.rotate(Math.sin(t+f.ph)*.4);g.fillStyle=`rgba(${q.k.glow},1)`;g.beginPath();for(let i=0;i<8;i++){const ang=i*Math.PI/4,rr=i%2?r*.22:r*.62;g.lineTo(Math.cos(ang)*rr,Math.sin(ang)*rr);}g.fill();
     g.fillStyle="#fffdf4";g.beginPath();g.arc(0,0,r*.16,0,Math.PI*2);g.fill();g.restore();}
   for(const p of q.fx){g.save();g.globalAlpha=clamp(p.life/p.L,0,1);g.fillStyle=`rgba(${q.k.glow},1)`;g.fillRect(p.x-1.2*s,p.y-1.2*s,2.4*s,2.4*s);g.restore();}
   // Baku
   const b=q.baku;if(b&&MIMG.m_dr_baku){const h=150*s,w=h*460/400,e=t-b.t0,a=b.state==="out"?clamp(1-e/1.6,0,1):b.state==="in"?clamp(e/.6,0,1):1,bob=b.state==="wait"?1+.03*Math.sin(t*2.2):1;
     drGlow(g,"200,190,255",b.x,b.y,h*.95,.45*a*(b.state==="wait"?.8+.2*Math.sin(t*3):1));g.save();g.globalAlpha=a;g.translate(b.x,b.y);g.scale(b.face*bob,bob);g.drawImage(MIMG.m_dr_baku,-w/2,-h/2,w,h);g.restore();b.hx=b.x;b.hy=b.y;b.hw=w;b.hh=h;
     if(b.state==="eat"){const h2=b.sh;g.strokeStyle="rgba(200,190,255,.35)";g.lineWidth=2*s;for(let k=0;k<4;k++){const u=((t*1.8+k/4)%1);g.beginPath();g.arc(mix(h2.x,b.x+b.face*62*s,u),mix(h2.y,b.y+34*s,u),(1-u)*16*s+3*s,0,Math.PI*2);g.stroke();}}
     if(b.state==="wait"){const u=(t*.8)%1;g.strokeStyle=`rgba(220,210,255,${.55*(1-u)})`;g.lineWidth=2*s;g.beginPath();g.ellipse(b.x,b.y,w*(.42+u*.2),h*(.4+u*.2),0,0,Math.PI*2);g.stroke();}}
   // caption (Baku speaks; hints)
   if(q.say&&t>q.say.t&&t-q.say.t<q.say.d){const a=clamp(Math.min((t-q.say.t)/.4,(q.say.d-(t-q.say.t))/.5),0,1);g.save();g.globalAlpha=a;g.font=`600 ${Math.round(14*s)}px ${getComputedStyle(document.body).fontFamily}`;const tw=Math.min(W-24,g.measureText(q.say.txt).width+28);
     g.fillStyle="rgba(10,10,26,.72)";g.beginPath();g.roundRect(W/2-tw/2,H*.06,tw,30*s,15*s);g.fill();g.restore();g.save();g.globalAlpha=a;textC(g,q.say.txt,W/2,H*.06+15*s,Math.min(14*s,(W-40)/q.say.txt.length*1.9),"#ece6ff",600);g.restore();}
   // fade in from sleep, title card; fade out when the dream melts
   const e=q.e;if(e<3.2){g.save();g.globalAlpha=clamp(1-e/1.4,0,1);g.fillStyle="#05040c";g.fillRect(0,0,W,H);g.globalAlpha=clamp(Math.min(e/.6,(3.2-e)/.8),0,1);jpText(g,q.k.jp,W/2,H*.4,26*s,"rgba(238,163,187,.9)");textC(g,q.k.n,W/2,H*.4+34*s,22*s,"#ece6ff",600);g.restore();}
   if(q.end){const u=clamp((t-q.end)/2.4,0,1);g.save();g.fillStyle=`rgba(226,222,248,${u*.9})`;g.fillRect(0,0,W,H);g.globalAlpha=clamp(u*2-.4,0,1);textC(g,"Сон тает…",W/2,H*.45,20*s,"#3a3460",600);g.restore();}
   if(hurt>0){g.fillStyle=`rgba(20,0,20,${.25*hurt})`;g.fillRect(0,0,W,H);}},
 down(G,x,y,t){const q=G.st,s=G.s;if(q.end||q.e<1)return;const b=q.baku;
   if(b&&(b.state==="wait"||b.state==="in")&&b.hw&&Math.abs(x-b.hx)<b.hw*.5&&Math.abs(y-b.hy)<b.hh*.5){b.state="go";b.t0=t;b.face=b.sh.x<b.x?-1:1;tone(330,.2,"sine",.05);return;}
   let best=null,bd=40*s;for(const f of q.frags){if(f.got||f.sx==null)continue;const d=Math.hypot(x-f.sx,y-f.sy);if(d<bd){bd=d;best=f;}}
   if(best){best.got=1;best.k=0;best.gx=best.sx;best.gy=best.sy;q.got++;q.play=t;tone(DR_PENT[Math.min(DR_PENT.length-1,q.got%DR_PENT.length)],1,"sine",.04);
     for(let i=0;i<9;i++){const a=i/9*6.28;q.fx.push({x:best.sx,y:best.sy,vx:Math.cos(a)*70*s,vy:Math.sin(a)*70*s-20*s,g:60*s,life:.7,L:.7});}return;}
   for(const h of q.sh)if(h.st==="creep"&&Math.hypot(x-h.x,y-h.y)<h.r*1.3){h.push=t+.9;tone(120,.2,"triangle",.04);return;}},
 stat:G=>{const q=G.st;return q.k?`✦ ${q.got} · ${Math.max(0,Math.ceil(q.dur-q.e))} с`:""},
 card(G){const q=G.st,K=q.k,it=q.prize&&IT[q.prize];S.needs.energy=clamp(Math.max(S.needs.energy+8,drRun?drRun.en:0),0,100);
   return`<div class="card dr-card"><p class="tag">夢 · ${K.jp}</p><h3>${K.n}</h3><p class="lore">${K.line}</p><p>Осколков сна: <b>${q.got}</b>${q.eaten?` · Баку съел кошмаров: <b>${q.eaten}</b>`:""}</p>
    ${it?`<div class="dish">${itemThumb(it,150,120)}</div><p>Муся принесла из сна: <b>${it.n}</b>. Её можно поставить в любой комнате — «🧺 Вещи» → «Из снов».</p>`:`<p>Сон растаял и ничего не оставил… ${q.got<8?"Чем больше осколков, тем вернее из сна что-то вынесешь.":"Может, в следующий раз."}</p>`}
    <div class="row"><button class="btn primary" id="gHome">Пусть спит дальше</button><button class="btn" id="gAgain" style="display:none"></button></div></div>`;},
 after(G){}};
GAMES.push(DREAM);
// static layer of the current world, rebuilt only when the field size changes
function drBuild(q,G){const [c,g]=drCv(G.W,G.H);DRW[q.k.id].bg(g,G.W,G.H,G.s);q.bg=c;q.W=G.W;q.H=G.H;G.bgc=c;if(DRW[q.k.id].init)DRW[q.k.id].init(q,G);}
// the reward: Baku's mask for a well-guarded dream, else one of the dream's own things (the first dream always gives one)
function drFinish(q){const D=drS(),K=q.k,own=id=>S.owned.has(id);D.n++;D.seen[K.id]=(D.seen[K.id]||0)+1;D.frag+=q.got;D.eaten+=q.eaten;D.last=K.id;
  let prize=null;if(q.eaten>=2&&!own("dr_baku"))prize="dr_baku";
  else if(D.n===1||Math.random()<clamp(.3+q.got*.025,.3,.8)){let pool=K.items.filter(i=>!own(i));if(!pool.length&&Math.random()<.5)pool=DR_ITEMS.filter(i=>!own(i)&&i!=="dr_baku");if(pool.length)prize=pick(pool);}
  q.prize=prize;if(prize){S.owned.add(prize);disc("dream",prize);}disc("dream","scene_"+K.id);
  award("dr_dream");if(DRK.every(k=>D.seen[k.id]))award("dr_all");if(D.eaten>=5)award("dr_bakufr");G.score=0;save();}

// ───── in the room: the thought bubble over sleeping Musya ─────
const drB={a:0,r:null};
function drAvail(){return !petAway()&&!scene.on&&pet.action==="sleep"&&now()-pet.start>3.5&&drNap!==pet.start&&!drRun;}
function drOpen(kind){if(!kind&&!drAvail())return false;drNap=pet.start;drNext=drNext||drPickKind();drRun={kind:kind||drNext,en:S.needs.energy};drNext=null;if(pet.action==="sleep"&&pet.napUntil)pet.napUntil=Math.max(pet.napUntil,now()+200);closePanel();openPlace("dream");return true;}
hook("tick",(t,dt)=>{const on=drAvail();if(on&&!drNext)drNext=drPickKind();drB.a+=((on?1:0)-drB.a)*Math.min(1,dt*(on?1.4:3));
  if(drRun&&G.id!=="dream"){if(pet.action==="sleep"&&pet.napUntil)pet.napUntil=now()+rand(14,24);drRun=null;}});
hook("overlay",t=>{if(drB.a<.02||petAway()){drB.r=null;return;}const s=view.s,a=drB.a,[hx,hy]=cellToStage(66,120),pul=1+.035*Math.sin(t*1.7),bw=112*s*pul,bh=bw*170/230;
  const bx=clamp(hx-58*s,bw/2+6,view.W-bw/2-6),by=hy-78*s+Math.sin(t*1.1)*3*s;
  for(const [k,cx,cy,w] of[[0,mix(hx,bx,.18),hy-14*s+Math.sin(t*1.3)*1.5*s,12*s],[1,mix(hx,bx,.42),hy-34*s+Math.sin(t*1.2+1)*2*s,19*s]]){drGlow(ctx,"200,190,255",cx,cy,w*1.4,.25*a);drSp(ctx,"puff",cx,cy,w,a*clamp((t%3.2)/.4+.6-k*.3,.55,.9));}
  drGlow(ctx,"200,190,255",bx,by,bw*.95,.35*a);drSp(ctx,"bubble",bx,by,bw,.9*a);
  const K=DRK_BY[drNext];if(K){ctx.save();ctx.beginPath();ctx.ellipse(bx,by+2*s,bw*.36,bh*.3,0,0,Math.PI*2);ctx.clip();const bob=Math.sin(t*1.5)*2*s,ps=bh*.52;
    if(K.pv==="door"){ctx.globalAlpha=.75*a;ctx.fillStyle="#f0d8a8";ctx.fillRect(bx-ps*.3,by-ps*.42+bob,ps*.6,ps*.84);ctx.strokeStyle="#4a3424";ctx.lineWidth=1.5*s;ctx.strokeRect(bx-ps*.3,by-ps*.42+bob,ps*.6,ps*.84);ctx.beginPath();ctx.moveTo(bx,by-ps*.42+bob);ctx.lineTo(bx,by+ps*.42+bob);ctx.moveTo(bx-ps*.3,by+bob);ctx.lineTo(bx+ps*.3,by+bob);ctx.stroke();}
    else drSp(ctx,K.pv,bx+(K.pv==="fishR"?Math.sin(t*.9)*6*s:0),by+bob,K.pv==="moon"?ps*.95:K.pv==="furinA"?ps*.42:ps*1.25,.72*a,Math.sin(t*.8)*.08);ctx.restore();}
  drB.r=[bx-bw/2,by-bh/2,bw,bh];});
hook("hit",(x,y)=>{const r=drB.r;if(!r||drB.a<.5||!drAvail())return false;if(x>r[0]&&x<r[0]+r[2]&&y>r[1]&&y<r[1]+r[3]){audioInit();drOpen();return true;}return false;});
hook("sleepTap",()=>drB.a>.3&&drAvail()?drOpen():false);
hook("hubDot",()=>drB.a>.5&&drAvail());
hook("hub",()=>{const D=drS(),n=DRK.filter(k=>D.seen[k.id]).length,av=drAvail();
  return`<div class="hubc"><h4>💭 Сны Муси <i>夢</i></h4><p>${av?"Муся спит, и над ней плывёт облачко сна — можно заглянуть.":pet.action==="sleep"?"Муся спит без снов… Облачко появится в следующий раз.":"Уложи Мусю спать: погаси андон в спальне."} Снов увидено: ${n} из ${DRK.length}.</p><div class="row">${av?`<button class="btn primary" data-x="dr:open">Заглянуть в сон</button>`:pet.action!=="sleep"&&S.room!=="bedroom"?`<button class="btn" data-x="dr:bed">В спальню</button>`:""}</div></div>`;});
hook("click",k=>{if(k==="dr:open"){closePanel();drOpen();return true;}if(k==="dr:bed"){closePanel();goRoom("bedroom");return true;}});
hook("album",el=>{const D=drS(),n=DRK.filter(k=>D.seen[k.id]).length;
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Сонник</h3><p class="lead">Сны Муси: ${n} из ${DRK.length}. Осколков сна собрано: ${D.frag}.${D.eaten?` Баку съел кошмаров: ${D.eaten}.`:""} Уложи Мусю спать и нажми на облачко над ней.</p><div class="dr-book">${DRK.map(K=>{const on=D.seen[K.id];
   return`<div class="dr-d ${on?"":"off"}"><b>${on?K.n:"???"}</b>${on?`<i>${K.jp}</i>`:""}<p>${on?K.line+(on>1?` Снился ${on} раза.`:""):"Этот сон Муся ещё не видела."}</p><div class="dr-its">${K.items.map(id=>{const o=S.owned.has(id);return`<span class="${o?"on":""}">${itemThumb(IT[id],56,52)}${o?IT[id].n:"???"}</span>`;}).join("")}</div></div>`;}).join("")}</div>`);});
X.dream={next:k=>{drNext=k;},open:k=>{drRun=null;drNap=pet.start;drRun={kind:k||drPickKind(),en:S.needs.energy};openPlace("dream");},avail:drAvail,bubble:drB,kinds:DRK.map(k=>k.id),end:()=>{if(G.id==="dream"){G.st.e=G.st.dur;G.st.t0=now()-G.st.dur;}}};
}
