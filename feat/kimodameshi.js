{
// ───────────────────────── «Кимодамэси» (肝試し) — the summer-night test of courage ─────────────────────────
// A hidden full-screen game: Musya takes a small paper lantern and walks the dark corridor of the old house, out through
// the garden to the little shrine, leaves an ofuda there and walks back (shorter). Side-scrolling parallax drawn
// procedurally; the candle is the only light (a radial mask). Hold to walk, release to stop. Events in random order from
// a pool of 11 (MON pictures reused): a lantern blinks an eye, a hand from the shōji, a figure behind the paper, eyes in
// the shōji, giggles, an eye in a stone lantern, a rokurokubi neck over the wall, a falling umbrella, the bean washer,
// cold wind (tap to shield the flame; if it dies — 3 taps to relight), footsteps behind («Обернуться?» costs courage).
// Courage → rank (Трусишка / Храбрая кошка / Без страха), keepsakes, stamps. S.scary off → gentle, no jump scares.
// Entry: bedroom tray at night (21:00–04:00) + the 家 card. S.ext.kimo={n,best,rank,met:[],last}
const KM=S.ext.kimo||(S.ext.kimo={n:0,best:0,rank:-1,met:[]});KM.met=KM.met||[];if(KM.rank==null)KM.rank=-1;
const kmNight=()=>{const h=hourNow();return h>=21||h<4;};
// assets/items/atlas_km.webp (art/kimodameshi_art.py)
const KMR={"km_ofuda":[0,0,90,250],"km_lantern":[94,0,150,230],"km_omamori":[248,0,100,190],"km_juzu":[352,0,190,120]};
const KMC="Кимодамэси",kmIt=(id,n,a,hint)=>({id,n,c:KMC,w:KMR[id][2],h:KMR[id][3],a,p:0,at:["km",KMR[id][0],KMR[id][1]],src:"🕯 кимодамэси",hint});
addItems([kmIt("km_ofuda","Офуда храбрости","t","Ночью дойди до святилища и вернись — кимодамэси"),kmIt("km_lantern","Свеча в бумажном фонаре","b","Пройди кимодамэси так, чтобы свеча ни разу не погасла"),
  kmIt("km_omamori","Амулет омамори","t","Заслужи в кимодамэси звание «Храбрая кошка»"),kmIt("km_juzu","Чётки дзюдзу","b","Пройди кимодамэси «Без страха»")],{km:[542,250]});
STAMPS.push(["km_first","肝","Первое кимодамэси","Ночью дойди до святилища и вернись"],["km_noturn","背","Не оглянулась","Пройди кимодамэси, ни разу не обернувшись"],["km_candle","灯","Свеча не погасла","Пройди кимодамэси, не дав свече погаснуть"]);
const KM_RK=[["coward","Трусишка","🙀"],["brave","Храбрая кошка","😼"],["fearless","Без страха","🏮"]];
// event: [zone h(house)|g(garden)|a, seconds, name, scary line, gentle line]
const KM_EV={
 chochin:["h",4.6,"Тётин-обакэ","…Я всё вижу.","Подмигну — и светить станет веселее!"],
 hand:["h",4,"Рука из-за сёдзи","Отдай… огонёк…","Привет-привет! Я просто машу."],
 yurei:["h",5.2,"Тень за бумагой","Куда ты так поздно, котёнок?","Тс-с… Все спят, иди тихонько."],
 eyes:["h",4.6,"Мокумокурэн","Мы все на тебя смотрим…","Мы присмотрим, чтобы ты не споткнулась."],
 warashi:["h",4.2,"Дзасики-вараси","Хи-хи-хи… Поиграй со мной…","Хи-хи! Догоняй!"],
 toro:["g",4.4,"Глаз в каменном фонаре","Здесь давно никто не ходил…","Я каменный фонарь. Мигаю для красоты!"],
 rokuro:["g",5.2,"Рокурокуби","Какой тёплый огонёк… Дай погреться.","Ой, я просто вытянула шею — посмотреть, кто идёт!"],
 karakasa:["g",4.4,"Каса-обакэ","Бэ-э-э!","Прыг-скок! Возьмёшь меня в дождь?"],
 azuki:["g",5.2,"Адзуки-арай","Фасоль помыть или котёнка съесть? Сёки-сёки…","Сёки-сёки… Мою фасоль к завтраку."],
 wind:["a",3.8,"Холодный ветер"],
 steps:["a",7,"Шаги за спиной"]};
const KM_SPD=105,KM_DOOR=1500,KM_SHR=3000,KM_HOME=1580,KM_TORO=[1800,2300,2760];
const kmH=(i,s=0)=>{const x=Math.sin(i*127.1+s*311.7)*43758.5453;return x-Math.floor(x);};
let KM_FF="";const kmFF=()=>KM_FF||(KM_FF=getComputedStyle(document.body).fontFamily);
const kmU=G=>clamp(Math.min(G.W/480,G.H/820),.6,1.7);

// ── a walk: 4 yōkai + wind/footsteps out, the other one + a garden yōkai back ──
function kmPlan(){
  const shuf=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
  const hs=shuf(Object.keys(KM_EV).filter(k=>KM_EV[k][0]==="h")),gs=shuf(Object.keys(KM_EV).filter(k=>KM_EV[k][0]==="g"));
  const [A,B]=shuf(["wind","steps"]),slots=[[400,"h"],[950,"h"],[1350,"h"],[1950,"g"],[2500,"g"]],ai=Math.floor(Math.random()*slots.length),evs=[];
  slots.forEach(([x,z],i)=>evs.push({k:i===ai?A:z==="h"?hs.pop():gs.pop(),x,dir:1}));
  const back=shuf([B,gs.pop()]);evs.push({k:back[0],x:2650,dir:-1},{k:back[1],x:2150,dir:-1});
  for(const e of evs)e.D=KM_EV[e.k][1];return evs;
}
let KM_SIL=null;   // the dark silhouette of a yūrei, for the paper screens
function kmSil(){if(KM_SIL)return KM_SIL;const c=document.createElement("canvas");c.width=180;c.height=360;const g=c.getContext("2d");drawYurei(g,90,4,350,1,false,false);
  g.globalCompositeOperation="source-in";g.fillStyle="#0a0909";g.fillRect(0,0,180,360);return KM_SIL=c;}
function kmMon(g,id,x,yb,h,alpha=1,flip=false,rot=0){const im=MIMG[id];if(!im||!im.width)return;const w=h*im.width/im.height;g.save();g.globalAlpha*=alpha;g.translate(x,yb);if(rot)g.rotate(rot);if(flip)g.scale(-1,1);g.drawImage(im,-w/2,-h,w,h);g.restore();}

// ── scenery ──
function kmToro(g,x,fy,s){g.save();const st="#3f403a",lt="#55564d";
  g.fillStyle=st;g.fillRect(x-26*s,fy-12*s,52*s,12*s);g.fillRect(x-8*s,fy-72*s,16*s,62*s);g.fillStyle=lt;g.fillRect(x-24*s,fy-84*s,48*s,12*s);
  g.fillStyle=st;g.fillRect(x-17*s,fy-114*s,34*s,30*s);g.fillStyle="#0b0b0a";g.fillRect(x-9*s,fy-108*s,18*s,18*s);
  g.fillStyle=lt;g.beginPath();g.moveTo(x-38*s,fy-110*s);g.quadraticCurveTo(x-20*s,fy-118*s,x-12*s,fy-134*s);g.lineTo(x+12*s,fy-134*s);g.quadraticCurveTo(x+20*s,fy-118*s,x+38*s,fy-110*s);g.closePath();g.fill();
  g.fillStyle=st;g.beginPath();g.arc(x,fy-140*s,7*s,0,7);g.fill();g.restore();}
function kmShrine(g,x,fy,s,ofuda,atl){g.save();
  g.fillStyle="#34352f";g.fillRect(x-62*s,fy-26*s,124*s,26*s);g.fillStyle="#44453d";g.fillRect(x-50*s,fy-44*s,100*s,18*s);
  g.fillStyle="#3a2618";g.fillRect(x-38*s,fy-128*s,76*s,84*s);g.fillStyle="#24170f";g.fillRect(x-28*s,fy-116*s,56*s,66*s);
  g.strokeStyle="#4a3322";g.lineWidth=2*s;for(let i=1;i<6;i++){g.beginPath();g.moveTo(x-28*s,fy-116*s+i*11*s);g.lineTo(x+28*s,fy-116*s+i*11*s);g.stroke();}
  g.beginPath();g.moveTo(x,fy-116*s);g.lineTo(x,fy-50*s);g.stroke();
  g.fillStyle="#1d1712";g.beginPath();g.moveTo(x-62*s,fy-124*s);g.lineTo(x,fy-170*s);g.lineTo(x+62*s,fy-124*s);g.lineTo(x+54*s,fy-118*s);g.lineTo(x,fy-156*s);g.lineTo(x-54*s,fy-118*s);g.fill();
  g.strokeStyle="#8f8466";g.lineWidth=4*s;g.beginPath();g.moveTo(x-44*s,fy-126*s);g.quadraticCurveTo(x,fy-112*s,x+44*s,fy-126*s);g.stroke();
  g.fillStyle="#d9d2bd";for(const d of[-24,0,24]){g.beginPath();g.moveTo(x+d*s,fy-120*s);g.lineTo(x+(d+5)*s,fy-110*s);g.lineTo(x+d*s,fy-106*s);g.lineTo(x+(d+5)*s,fy-96*s);g.lineTo(x+(d+1)*s,fy-96*s);g.lineTo(x+(d-4)*s,fy-106*s);g.lineTo(x+(d+1)*s,fy-110*s);g.fill();}
  if(ofuda){if(atl)g.drawImage(atl,0,0,90,250,x-9*s,fy-104*s,18*s,50*s);else{g.fillStyle="#e4dcc6";g.fillRect(x-7*s,fy-100*s,14*s,44*s);}}
  g.restore();}
function kmTorii(g,x,fy,s){g.save();g.fillStyle="#3d1611";for(const d of[-58,58])g.fillRect(x+d*s-6*s,fy-196*s,12*s,196*s);
  g.fillRect(x-70*s,fy-160*s,140*s,9*s);g.beginPath();g.moveTo(x-90*s,fy-196*s);g.quadraticCurveTo(x,fy-186*s,x+90*s,fy-196*s);g.lineTo(x+86*s,fy-208*s);g.quadraticCurveTo(x,fy-198*s,x-86*s,fy-208*s);g.fill();g.restore();}

function kmScene(G,g,q,u){
  const W=G.W,H=G.H,fy=H*.74,cam=q.cam,X=wx=>(wx-cam)*u,gx=clamp(X(KM_DOOR),-1,W+1),c=q.clk;
  if(gx>0){g.save();g.beginPath();g.rect(0,0,gx,H);g.clip();                       // the house: shōji corridor
    g.fillStyle="#100c09";g.fillRect(0,0,gx,H*.2);g.fillStyle="#1d150e";g.fillRect(0,H*.1-4*u,gx,8*u);
    g.strokeStyle="rgba(70,52,36,.6)";g.lineWidth=2*u;
    const k0=Math.floor(cam/300)-1,k1=Math.ceil((cam+W/u)/300);
    for(let k=k0;k<=k1&&k*300<=KM_DOOR;k++){const b0=X(k*300),bw=300*u;
      for(let j=0;j<14;j++){const xx=b0+(j+.5)*bw/14;g.beginPath();g.moveTo(xx,H*.12);g.lineTo(xx,H*.19);g.stroke();}   // ranma slats
      if(k*300>=KM_DOOR)continue;
      for(const p of[0,1]){const px0=b0+10*u+p*140*u,pw=140*u,py0=H*.2,ph=fy-36*u-py0;
        g.fillStyle=(k+p)%3===1?"#8a8068":"#958b72";g.fillRect(px0,py0,pw,ph);
        g.strokeStyle="#2b1f15";g.lineWidth=2.2*u;for(let i=1;i<3;i++){g.beginPath();g.moveTo(px0+pw*i/3,py0);g.lineTo(px0+pw*i/3,py0+ph);g.stroke();}
        for(let i=1;i<6;i++){g.beginPath();g.moveTo(px0,py0+ph*i/6);g.lineTo(px0+pw,py0+ph*i/6);g.stroke();}
        g.lineWidth=5*u;g.strokeRect(px0,py0,pw,ph);
        if(kmH(k*2+p,3)<.25){g.fillStyle="rgba(40,30,20,.35)";g.fillRect(px0+pw*kmH(k,4)*.6,py0+ph*.7,pw*.18,ph*.08);}}   // an old tear
      g.fillStyle="#1b130d";g.fillRect(b0,fy-36*u,bw,36*u);}
    g.fillStyle="#120d09";g.fillRect(X(-1200),H*.1,(-1200-(-40))*-u,fy-H*.1);       // far end of the corridor
    for(let k=k0;k<=k1&&k*300<=KM_DOOR;k++){const x=X(k*300);g.fillStyle="#22170f";g.fillRect(x-10*u,H*.1,20*u,fy-H*.1+4*u);g.fillStyle="rgba(120,90,60,.25)";g.fillRect(x-10*u,H*.1,3*u,fy-H*.1);}
    g.restore();}
  if(gx<W){g.save();g.beginPath();g.rect(gx,0,W-gx,H);g.clip();                     // the garden
    const sk=g.createLinearGradient(0,0,0,fy);sk.addColorStop(0,"#0a101b");sk.addColorStop(.6,"#18212b");sk.addColorStop(1,"#1e2620");g.fillStyle=sk;g.fillRect(gx,0,W-gx,fy);
    g.fillStyle="rgba(220,225,235,.55)";for(let i=0;i<40;i++){const sx=((kmH(i,1)*1600-cam*.03*u)%W+W)%W,sy=kmH(i,2)*H*.35;if(sx>gx)g.fillRect(sx,sy,1.4,1.4);}
    const tp=.35,i0=Math.floor(cam*tp/120)-2,i1=i0+Math.ceil(W/u/120)+4;
    for(let i=i0;i<=i1;i++){const tx=(i*120+kmH(i,5)*70-cam*tp)*u,th=(150+kmH(i,6)*170)*u,ty=H*.52;
      g.fillStyle=i%3?"#0d1411":"#101814";g.beginPath();g.moveTo(tx-34*u,ty);g.lineTo(tx,ty-th);g.lineTo(tx+34*u,ty);g.fill();}
    g.fillStyle="#0e1311";g.fillRect(gx,H*.52,W-gx,fy-H*.52);
    const w0=X(KM_DOOR+170),w1=X(2860);                                                // the earthen wall
    if(w1>gx&&w0<W){g.fillStyle="#2e2a22";g.fillRect(w0,H*.44,w1-w0,H*.18);g.fillStyle="#1a1a1e";g.fillRect(w0-6*u,H*.405,w1-w0+12*u,H*.04);
      g.fillStyle="#26262b";for(let x=w0;x<w1;x+=18*u)g.fillRect(x,H*.405,9*u,H*.04);g.fillStyle="#23201b";g.fillRect(w0,H*.6,w1-w0,H*.02);}
    for(let i=Math.floor(cam/90);i<(cam+W/u)/90+1;i++){if(i*90<KM_DOOR+120)continue;const bx=X(i*90+kmH(i,7)*40),br=(26+kmH(i,8)*22)*u;
      g.fillStyle=i%2?"#141c16":"#18211a";g.beginPath();g.ellipse(bx,H*.66,br*1.4,br,0,Math.PI,0);g.fill();}
    const gr=g.createLinearGradient(0,fy,0,H);gr.addColorStop(0,"#2b2b26");gr.addColorStop(1,"#121210");g.fillStyle=gr;g.fillRect(gx,fy,W-gx,H-fy);
    g.fillStyle="#1c1c19";for(let i=0;i<120;i++){const sx=((kmH(i,9)*2400-cam*u)%(W*1.2)+W*1.2)%(W*1.2),sy=fy+kmH(i,10)*(H-fy);if(sx>gx)g.fillRect(sx,sy,2*u,1.5*u);}
    for(let i=Math.floor(cam/120);i<(cam+W/u)/120+1;i++){if(i*120<KM_DOOR+150)continue;const sx=X(i*120+kmH(i,11)*20);g.fillStyle="#3b3b35";g.beginPath();g.ellipse(sx,fy+30*u,40*u,11*u,0,0,7);g.fill();g.fillStyle="#45453e";g.beginPath();g.ellipse(sx-4*u,fy+27*u,30*u,6*u,0,0,7);g.fill();}
    const v=X(KM_DOOR);g.fillStyle="#24180f";g.fillRect(v,fy,X(KM_DOOR+110)-v,22*u);g.fillStyle="#1a110b";g.fillRect(v,fy+22*u,X(KM_DOOR+110)-v,H);   // veranda edge + eave
    g.fillStyle="#0c0907";g.beginPath();g.moveTo(v,0);g.lineTo(X(KM_DOOR+190),0);g.lineTo(X(KM_DOOR+150),H*.07);g.lineTo(v,H*.09);g.fill();
    g.fillStyle="#3a3a35";g.beginPath();g.ellipse(X(KM_DOOR+150),fy+16*u,34*u,10*u,0,0,7);g.fill();
    for(const tx of KM_TORO){const x=X(tx);if(x>-80*u&&x<W+80*u)kmToro(g,x,fy+4*u,u);}
    kmTorii(g,X(2930),fy+6*u,u);kmShrine(g,X(KM_SHR+90),fy+8*u,u,q.ofuda!=null,q.atl);
    g.restore();}
  g.fillStyle="#1f150e";if(gx>0){const fg=g.createLinearGradient(0,fy,0,H);fg.addColorStop(0,"#2a1c12");fg.addColorStop(1,"#0f0a07");g.fillStyle=fg;g.fillRect(0,fy,Math.min(gx,W),H-fy);
    g.strokeStyle="rgba(8,5,3,.8)";g.lineWidth=1.5*u;for(let i=Math.floor(cam/90);i*90<Math.min(KM_DOOR,cam+W/u);i++){const x=X(i*90);g.beginPath();g.moveTo(x,fy);g.lineTo(x-(x-W/2)*.25,H);g.stroke();}
    g.fillStyle="rgba(150,110,70,.18)";g.fillRect(0,fy,Math.min(gx,W),2*u);}
}
function kmFront(G,g,q,u){const W=G.W,H=G.H,p=1.4,cam=q.cam;g.save();
  for(let i=Math.floor(cam*p/700)-1;i<=Math.floor((cam*p+W/u)/700)+1;i++){const lx=i*700+250,x=(lx-cam*p)*u,wx=lx/p;
    if(wx<KM_DOOR){g.fillStyle="#050403";g.fillRect(x-15*u,0,30*u,H);}
    else{g.strokeStyle="#060806";g.lineCap="round";for(let j=0;j<3;j++){const bx=x+j*26*u;g.lineWidth=(9-j*2)*u;g.beginPath();g.moveTo(bx,H);g.quadraticCurveTo(bx+8*u,H*.6,bx+(14+j*6)*u,H*.25);g.stroke();}
      g.fillStyle="#050705";for(let j=0;j<9;j++){g.beginPath();g.moveTo(x-40*u+j*12*u,H);g.lineTo(x-34*u+j*12*u+kmH(i*9+j,12)*14*u,H-(30+kmH(i*9+j,13)*40)*u);g.lineTo(x-28*u+j*12*u,H);g.fill();}}}
  g.restore();}

// ── yōkai events: draw under the light mask (lit by the candle) and over it (things that glow) ──
function kmBubble(g,txt,x,y,u,W,scary,alpha){if(alpha<=0)return;g.save();g.globalAlpha=alpha;const fs=Math.round(13.5*u);g.font=`600 ${fs}px ${kmFF()}`;
  const words=txt.split(" "),lines=[];let l="";for(const w of words){const t=l?l+" "+w:w;if(g.measureText(t).width>190*u&&l){lines.push(l);l=w;}else l=t;}lines.push(l);
  const bw=Math.max(...lines.map(s=>g.measureText(s).width))+22*u,bh=lines.length*fs*1.3+14*u,bx=clamp(x-bw/2,8,W-bw-8),by=Math.max(48*u,y-bh);
  g.fillStyle=scary?"rgba(12,10,12,.86)":"rgba(236,229,210,.94)";g.strokeStyle=scary?"rgba(200,190,170,.35)":"rgba(80,60,40,.35)";g.lineWidth=1.2;g.beginPath();g.roundRect(bx,by,bw,bh,10*u);g.fill();g.stroke();
  g.fillStyle=scary?"#d8d2c3":"#2a211a";g.textAlign="center";g.textBaseline="middle";lines.forEach((s,i)=>g.fillText(s,bx+bw/2,by+7*u+fs*.65+i*fs*1.3));g.restore();}
function kmEv(G,g,q,e,u,over){
  const W=G.W,H=G.H,fy=H*.74,X=wx=>(wx-q.cam)*u,el=q.clk-e.t0,D=e.D,fin=clamp((D-el)/.6,0,1),fade=clamp(el/.5,0,1)*fin,sc=S.scary,d=q.dir,x=X(e.wx);
  let bub=null;const line=KM_EV[e.k][sc?3:4];
  switch(e.k){
  case "chochin":{const lit=clamp((el-.9)/.4,0,1),sw=Math.sin(el*2.2)*.14+(sc&&el>1.4&&el<1.9?Math.sin((el-1.4)*20)*.12:0),h=118*u,top=H*.1+30*u;
    g.save();g.translate(x,H*.1);g.rotate(sw);g.strokeStyle="#1a120c";g.lineWidth=2*u;g.beginPath();g.moveTo(0,0);g.lineTo(0,30*u);g.stroke();
    if(over){g.globalAlpha=fade*lit;const gl=g.createRadialGradient(0,30*u+h*.5,0,0,30*u+h*.5,h);gl.addColorStop(0,"rgba(255,170,80,.35)");gl.addColorStop(1,"rgba(255,170,80,0)");g.fillStyle=gl;g.fillRect(-h,30*u-h*.5,2*h,2*h);g.globalAlpha=fade*(.25+.6*lit);}else g.globalAlpha=fade;
    const im=MIMG.m_obake;if(im&&im.width){const w=h*im.width/im.height;g.drawImage(im,-w/2,30*u,w,h);
      const bl=[1.7,2.75,3.6].some(b=>el>b&&el<b+.18);if(bl){g.fillStyle="#d4c7a2";g.beginPath();g.ellipse(0,30*u+h*.375,w*.17,h*.075,0,0,7);g.fill();g.strokeStyle="#3a2416";g.lineWidth=2*u;g.beginPath();g.moveTo(-w*.15,30*u+h*.38);g.quadraticCurveTo(0,30*u+h*.41,w*.15,30*u+h*.38);g.stroke();}}
    g.restore();if(over&&el>1.2)bub=[x,top-6*u];break;}
  case "hand":{const pil=(d>0?Math.ceil((e.wx-20)/300):Math.floor((e.wx+20)/300))*300,px0=X(pil)-d*10*u,ext=clamp(el/1.1,0,1)*clamp((D-.3-el)/.8,0,1),len=(20+150*ext)*u,wave=sc?Math.sin(el*9)*.05:Math.sin(el*7)*.35*ext;
    if(sc&&el>1.05&&!e.jolt){e.jolt=1;q.shk=q.clk;scareSound();}
    g.save();g.translate(px0,H*.46);g.scale(-d,1);g.globalAlpha=over?.4*fin:fin;
    if(!over){g.fillStyle="#070504";g.fillRect(-2*u,-60*u,5*u,120*u);}
    const sl=Math.min(len*.32,46*u),sg=g.createLinearGradient(0,-16*u,0,18*u);sg.addColorStop(0,"#e6e6df");sg.addColorStop(1,"#9fa19b");g.fillStyle=sg;
    g.beginPath();g.moveTo(0,-15*u);g.lineTo(sl,-9*u);g.lineTo(sl+2*u,8*u);g.quadraticCurveTo(sl+4*u,38*u,sl*.45,44*u);g.quadraticCurveTo(0,44*u,0,30*u);g.closePath();g.fill();
    g.strokeStyle="rgba(90,92,88,.5)";g.lineWidth=1.2*u;g.beginPath();g.moveTo(sl*.35,-11*u);g.quadraticCurveTo(sl*.55,14*u,sl*.3,40*u);g.stroke();
    g.rotate(wave);g.lineCap="round";g.strokeStyle="#a9a596";g.lineWidth=11*u;g.beginPath();g.moveTo(sl-2*u,0);g.lineTo(len*.9,-2*u);g.stroke();
    g.strokeStyle="#d3cfc0";g.lineWidth=8*u;g.beginPath();g.moveTo(sl-2*u,-1*u);g.lineTo(len*.9,-3*u);g.stroke();
    g.fillStyle="#cdc8b6";g.beginPath();g.ellipse(len*.94,-2*u,10*u,7.5*u,0,0,7);g.fill();
    for(let i=0;i<4;i++){const a=-.55+i*.3+(sc?0:Math.sin(el*8+i)*.08),L=(sc?27:19)*u,ex=len*.96+Math.cos(a)*L,ey=-2*u+Math.sin(a)*L,kx=len*.96+Math.cos(a)*L*.5,ky=-2*u+Math.sin(a)*L*.5+1.5*u;
      g.strokeStyle="#a9a596";g.lineWidth=3.6*u;g.beginPath();g.moveTo(len*.96,-2*u);g.quadraticCurveTo(kx,ky,ex,ey);g.stroke();g.strokeStyle="#d6d1c2";g.lineWidth=2.2*u;g.beginPath();g.moveTo(len*.96,-2*u);g.quadraticCurveTo(kx,ky,ex,ey);g.stroke();
      if(sc){g.fillStyle="#3a2a24";g.beginPath();g.arc(ex,ey,1.7*u,0,7);g.fill();}}
    g.strokeStyle="#cfcabb";g.lineWidth=3*u;g.beginPath();g.moveTo(len*.92,3*u);g.lineTo(len*.92+9*u,14*u);g.stroke();g.restore();if(over&&ext>.8)bub=[x-d*90*u,H*.46-24*u];break;}
  case "yurei":{if(!over)break;const bay=Math.floor(e.wx/300)*300;if(bay>=KM_DOOR)break;const x0=X(bay)+10*u,py0=H*.2,ph=fy-36*u-py0,sx=X(e.wx+(60-clamp(el/(D-1.6),0,1)*170)*d),a=fade;
    g.save();g.beginPath();g.rect(x0,py0,280*u,ph);g.clip();const gl=g.createRadialGradient(sx,py0+ph*.45,0,sx,py0+ph*.45,ph*.7);gl.addColorStop(0,`rgba(200,210,215,${.38*a})`);gl.addColorStop(1,"rgba(200,210,215,0)");g.fillStyle=gl;g.fillRect(x0,py0,280*u,ph);
    const sh=ph*.92,lean=el>D-1.8&&sc?Math.sin((el-D+1.8)*3)*.12:0;g.globalAlpha=.85*a;g.translate(sx,py0+ph*.05);g.rotate(lean);g.drawImage(kmSil(),-sh*.25,0,sh*.5,sh);g.restore();
    g.save();g.strokeStyle=`rgba(20,14,10,${.8*a})`;g.lineWidth=2.2*u;for(const p of[0,1]){const px0=x0+p*140*u;for(let i=1;i<3;i++){g.beginPath();g.moveTo(px0+140*u*i/3,py0);g.lineTo(px0+140*u*i/3,py0+ph);g.stroke();}for(let i=1;i<6;i++){g.beginPath();g.moveTo(px0,py0+ph*i/6);g.lineTo(px0+140*u,py0+ph*i/6);g.stroke();}}g.restore();
    if(el>1.4)bub=[sx,py0+ph*.1];break;}
  case "eyes":{const bay=Math.floor(e.wx/300)*300;if(bay>=KM_DOOR)break;const x0=X(bay)+10*u,py0=H*.2,ph=fy-36*u-py0,im=MIMG.m_vs_mokumokuren;if(!im||!im.width)break;
    const op=clamp((el-.3)/1.2,0,1)*fin,ww=280*u,hh=Math.min(ph,ww*im.height/im.width);g.save();g.globalAlpha=op*(over?.5:1);g.drawImage(im,x0,py0+(ph-hh)/2,ww,hh);g.restore();
    if(over&&el>1.3)bub=[x0+ww/2,py0+(ph-hh)/2];break;}
  case "warashi":{const run=clamp(el/D,0,1),wx=X(e.wx+(80+run*360)*d),bob=Math.abs(Math.sin(el*9))*6*u;
    kmMon(g,"m_warashi_back",wx,fy-4*u-bob,150*u,fade*(over?.45:1)*(1-run*.5),d<0);if(over&&el>.8&&el<3.2)bub=[wx,fy-160*u];break;}
  case "toro":{const s=u,fx=x,ty=fy+4*u;if(!over){if(!e.fixed)kmToro(g,fx,ty,s);break;}
    const op=clamp((el-.6)/.5,0,1)*fin,bl=[1.9,3].some(b=>el>b&&el<b+.2),cx=fx,cy=ty-99*s;
    g.save();g.globalAlpha=op;const gl=g.createRadialGradient(cx,cy,0,cx,cy,40*s);gl.addColorStop(0,"rgba(180,220,170,.45)");gl.addColorStop(1,"rgba(180,220,170,0)");g.fillStyle=gl;g.fillRect(cx-40*s,cy-40*s,80*s,80*s);
    g.fillStyle="#ddd8c2";g.beginPath();g.ellipse(cx,cy,8*s,bl?1:5.5*s,0,0,7);g.fill();if(!bl){const lk=clamp((X(q.x)-cx)/(200*u),-1,1);g.fillStyle="#1b120c";g.beginPath();g.arc(cx+lk*3.5*s,cy,3.4*s,0,7);g.fill();g.fillStyle="#c53b2a";g.beginPath();g.arc(cx+lk*3.5*s,cy,1.3*s,0,7);g.fill();}
    g.restore();if(el>1.2)bub=[cx,cy-50*s];break;}
  case "rokuro":{const grow=clamp(el/2,0,1),dart=sc&&el>2.4&&el<3.2?Math.sin((el-2.4)/.8*Math.PI):0,bx=x+30*u*d,by=H*.43;
    if(sc&&el>2.4&&!e.jolt){e.jolt=1;q.shk=q.clk;scareSound();}
    const hx=bx-d*(70+60*dart)*u*grow+Math.sin(el*1.6)*10*u,hy=by-(40+170*grow)*u+dart*120*u+Math.cos(el*1.3)*6*u;
    g.save();if(over){g.beginPath();g.rect(0,0,W,H*.405);g.clip();}g.globalAlpha=fin*(over?.55:1);g.lineCap="round";const nk=()=>{g.beginPath();g.moveTo(bx,by+10*u);g.bezierCurveTo(bx,by-120*u*grow,hx+d*80*u,hy-60*u,hx,hy+30*u);g.stroke();};
    g.strokeStyle="#7d786c";g.lineWidth=20*u;nk();g.strokeStyle="#d8d3c6";g.lineWidth=15*u;nk();
    kmMon(g,"m_rokuro",hx,hy+40*u,96*u,1,d>0,Math.sin(el*1.3)*.12);g.restore();
    if(!over){g.fillStyle="#1a1a1e";g.fillRect(bx-34*u,H*.405,68*u,H*.04);g.fillStyle="#26262b";for(let i=-2;i<2;i++)g.fillRect(bx+i*18*u,H*.405,9*u,H*.04);}                      // the wall's roof hides the root of the neck
    if(over&&el>1.6)bub=[hx,hy-50*u];break;}
  case "karakasa":{const fall=clamp(el/.6,0,1),land=fall>=1,hop=land?Math.abs(Math.sin((el-.6)*4.2))*42*u:0,go=clamp((el-2.8)/(D-2.8),0,1),cx=x+go*220*u*d,cy=-120*u+(fy+6*u+120*u)*fall*fall-hop;
    if(land&&!e.thud){e.thud=1;tone(58,.35,"sine",.1);if(sc)q.shk=q.clk;}
    kmMon(g,"m_vs_karakasa",cx,cy,150*u,fin*(over?.35:1),d<0,land?Math.sin(el*4.2)*.12:fall*.6);if(over&&land&&el<3.6)bub=[cx,cy-160*u];break;}
  case "azuki":{const cx=x,cy=fy+6*u,up=sc&&el>2.6?clamp((el-2.6)/.3,0,1):0;
    if(!over){g.fillStyle="rgba(60,80,90,.6)";g.beginPath();g.ellipse(cx+d*20*u,cy+18*u,70*u,12*u,0,0,7);g.fill();g.strokeStyle="rgba(170,190,200,.35)";g.lineWidth=1.2*u;for(let i=0;i<3;i++){const r=((el*1.3+i/3)%1);g.beginPath();g.ellipse(cx+d*20*u,cy+18*u,70*u*r,12*u*r,0,0,7);g.stroke();}}
    kmMon(g,"m_vs_azuki",cx,cy+Math.sin(el*10)*2*u,(110+18*up)*u,fade*(over?.3:1),d>0);if(over&&el>1)bub=[cx,cy-125*u];break;}
  case "wind":{if(!over)break;const a=clamp(el/.4,0,1)*fin;g.save();g.strokeStyle=`rgba(200,210,220,${.22*a})`;g.lineWidth=1.3*u;
    for(let i=0;i<34;i++){const sp=(600+kmH(i,20)*500)*u,yy=kmH(i,21)*H,len=(40+kmH(i,22)*90)*u,xx=W-((el*sp+kmH(i,23)*W*2)%(W*1.6));const sx=d>0?xx:W-xx;g.beginPath();g.moveTo(sx,yy);g.lineTo(sx+len*(d>0?1:-1),yy+6*u);g.stroke();}
    g.fillStyle=`rgba(90,70,40,${.6*a})`;for(let i=0;i<7;i++){const xx=W-((el*(350+i*40)*u+i*170*u)%(W*1.3)),sx=d>0?xx:W-xx,yy=H*(.3+kmH(i,24)*.5)+Math.sin(el*5+i)*20*u;g.save();g.translate(sx,yy);g.rotate(el*6+i);g.fillRect(-5*u,-2*u,10*u,4*u);g.restore();}
    g.restore();break;}
  case "steps":{if(!over)break;const bx=X(q.x)-d*130*u,a=fade*(e.turned?0:1);
    if(a>0){g.save();g.globalAlpha=.55*a*(.6+.4*Math.sin(el*11.4));textC(g,sc?"топ… топ…":"тип… тип…",bx,fy-30*u,13*u,"#b9b2a2",500);g.restore();}
    if(e.turned){const te=q.clk-e.turned;if(!sc){const sa=clamp(te/.3,0,1)*clamp((2.6-te)/.4,0,1);kmMon(g,"m_vs_yosuzume",bx,fy+4*u-Math.abs(Math.sin(te*8))*10*u,70*u,sa);if(te>.3&&te<2.4)bub=[bx,fy-80*u];}}
    break;}}
  const tl=e.k==="steps"?"Чи-чи! Это всего лишь я!":line;if(bub&&tl)kmBubble(g,tl,bub[0],bub[1],u,W,sc,clamp((el-.2)/.3,0,1)*fin);
}
function kmLantern(q,u,cx,fy,face){const sc=.72*u,mx=cx+face*64*sc,my=fy-84*sc,sh=q.clk<q.shield?1:0;q.shl=(q.shl||0)+(sh-(q.shl||0))*.2;
  const wind=q.cur&&q.cur.k==="wind"?Math.sin(q.clk*9)*.25:0,sw=(Math.sin(q.clk*3)*.1*(q.mv?1:.4)+wind*(1-q.shl))*face,tx=mx+face*(32-24*q.shl)*sc,ty=my-(24-10*q.shl)*sc;
  return {mx,my,tx,ty,lx:tx+Math.sin(sw)*28*sc,ly:ty+Math.cos(sw)*28*sc,sc,sw};}
function kmDrawLantern(g,q,L){const {mx,my,tx,ty,lx,ly,sc}=L;g.save();g.strokeStyle="#5b3d24";g.lineWidth=3*sc;g.lineCap="round";g.beginPath();g.moveTo(mx,my);g.lineTo(tx,ty);g.stroke();
  g.strokeStyle="#1a120c";g.lineWidth=1.2*sc;g.beginPath();g.moveTo(tx,ty);g.lineTo(lx,ly-15*sc);g.stroke();
  const f=q.out?0:q.fl,col=q.out?"#4a3f33":`rgb(${Math.round(120+130*f)},${Math.round(80+80*f)},${Math.round(40+30*f)})`;g.fillStyle=col;g.beginPath();g.ellipse(lx,ly,12*sc,15*sc,0,0,7);g.fill();
  g.strokeStyle="rgba(60,30,10,.45)";g.lineWidth=1*sc;for(let i=-2;i<=2;i++){const yy=ly+i*5*sc,w=12*sc*Math.sqrt(1-(i/3)**2);g.beginPath();g.moveTo(lx-w,yy);g.lineTo(lx+w,yy);g.stroke();}
  if(!q.out){g.fillStyle=`rgba(255,240,190,${.5+.5*f})`;g.beginPath();g.ellipse(lx+Math.sin(q.clk*13)*1.2*sc,ly+2*sc,3.5*sc,(4+3*f)*sc,0,0,7);g.fill();}
  g.fillStyle="#140d09";g.fillRect(lx-7*sc,ly-17*sc,14*sc,4*sc);g.fillRect(lx-7*sc,ly+13*sc,14*sc,4*sc);g.restore();}

// ── the game ──
function kmFace(q){return q.ph==="flee"?-1:q.clk-q.turnT<1.2?-q.dir:q.dir;}
function kmCam(G,q,u){return q.x-(q.dir>0?.36:.64)*G.W/u;}
function kmStart(q,e){e.t0=q.clk;e.wk=0;e.wx=q.x+q.dir*(e.k==="steps"?-150:e.k==="hand"?120:175);if(KM_EV[e.k][0]==="h")e.wx=Math.min(e.wx,KM_DOOR-160);
  if(e.k==="toro"){const t=(q.dir>0?KM_TORO:KM_TORO.slice().reverse()).find(t=>q.dir>0?t>q.x+80:t<q.x-80);if(t!=null&&Math.abs(t-q.x)<450){e.wx=t;e.fixed=1;}}q.cur=e;if(!q.met.includes(e.k)&&e.k!=="wind"&&e.k!=="steps")q.met.push(e.k);
  q.cour-=S.scary?6:3;if(S.scary&&e.k!=="wind")q.emo=["🙀",q.clk];
  if(e.k==="wind")for(let i=0;i<6;i++)setTimeout(()=>tone(rand(260,520),.6,"sine",.012),i*130);
  if(e.k==="warashi")[0,.15,.3,1.6,1.75,2.8,2.95].forEach((s,i)=>setTimeout(()=>tone([1500,1750,1400][i%3],.08,"triangle",.022),s*1000));
  if(e.k==="azuki")for(let i=0;i<10;i++)setTimeout(()=>tone(rand(2200,3200),.04,"square",.008),400+i*380+(i%2)*90);
  if(e.k==="chochin"||e.k==="toro")setTimeout(()=>tone(S.scary?196:660,.5,"sine",.03),1200);
  if(e.k==="yurei"&&S.scary)setTimeout(()=>tone(110,1.6,"sine",.03),900);}
function kmStop(q,e){q.cur=null;e.done=1;if(e.wk>=e.D*.55&&!e.turned){q.cour+=8;q.emo=["😼",q.clk];}
  if(e.k==="steps"&&!e.turned)q.note=["Шаги отстали. Это был Бэтобэто-сан: ему просто нужно уступить дорогу.",q.clk];}
function kmOut(q){q.out=true;q.wasOut=true;q.rel=0;q.fl=0;q.cour-=12;q.emo=["😿",q.clk];tone(180,.5,"sine",.04);}
function kmFinish(G,fled){const q=G.st;if(q.fin)return;q.fin=1;const cour=Math.round(clamp(q.cour,0,100)),r=fled?0:cour>=75&&!q.turned?2:cour>=40?1:0,got=[],st=[];
  const give=id=>{if(!S.owned.has(id)){S.owned.add(id);got.push(id);}},stamp=id=>{if(!ST.got.includes(id))st.push(id);award(id);};
  if(!fled){KM.n++;KM.best=Math.max(KM.best,cour);KM.rank=Math.max(KM.rank,r);KM.last=dayKey();disc("kimo",KM_RK[r][0]);
    stamp("km_first");give("km_ofuda");if(!q.turned)stamp("km_noturn");if(!q.wasOut){stamp("km_candle");give("km_lantern");}if(r>=1)give("km_omamori");if(r>=2)give("km_juzu");
    S.needs.joy=clamp(S.needs.joy+10,0,100);}
  for(const k of q.met)if(!KM.met.includes(k))KM.met.push(k);q.res={r,cour,fled,got,st,met:q.met.slice(),turned:q.turned,out:q.wasOut};G.score=fled?0:cour;q.cour=cour;$("gStat").textContent=KM_GAME.stat(G);save();gEnd();}
function kmKey(G,q,k){q.btns=[];
  if(k==="turn"){const e=q.cur;if(!e||e.k!=="steps"||e.turned)return;e.turned=q.clk;q.turned=true;q.turnT=q.clk;q.cour-=S.scary?25:15;q.emo=["🙀",q.clk];
    if(S.scary){scare(now());q.note=["Позади никого… Только шаги стихли.",q.clk+.6];}else{tone(2400,.06,"triangle",.03);setTimeout(()=>tone(2700,.06,"triangle",.03),120);}
    e.D=Math.min(e.D,q.clk-e.t0+2.8);}
  if(k==="ofuda"&&q.ph==="shrine"){q.ph="turn";q.ofuda=q.clk;chime([784,988,1175,1568]);q.emo=["🙏",q.clk];q.note=["Офуда оставлена. Теперь домой — и не оглядывайся!",q.clk];}}
const KM_GAME={id:"km_walk",hidden:true,scary:true,n:"Кимодамэси",tag:"肝試し · испытание храбрости",bg:"room",lives:null,time:null,icon:"🕯",
 lore:"Кимодамэси — «испытание печени», то есть храбрости. Летними ночами японские дети по одному идут страшной дорогой — к кладбищу или старому святилищу, оставляют там знак и возвращаются. А ёкаи, конечно, не упускают случая подшутить. Муся возьмёт фонарик со свечой и пройдёт тёмным коридором и садом к маленькому святилищу.",
 get how(){return"Держи палец на экране — Муся идёт, отпусти — стоит. Подолгу не стой: храбрость тает. Подует ветер — тапай, чтобы прикрыть свечу; погаснет — коснись три раза. Шаги за спиной? Не оборачивайся! У святилища оставь офуда и возвращайся."+(S.scary?"":" Страшилки выключены — ёкаи будут добрыми.");},
 init(G,t){const u=kmU(G);G.st={clk:0,x:60,dir:1,ph:"out",walk:0,mv:false,idle:0,cour:70,fl:1,out:false,rel:0,shield:-9,turnT:-9,turned:false,wasOut:false,evs:kmPlan(),cur:null,met:[],btns:[],emo:null,note:null,shk:-9,moved:false,sparks:[]};
   const q=G.st;q.cam=kmCam(G,q,u);atlasImg("km",im=>{q.atl=im;});},
 step(G,t,dt){const q=G.st,u=kmU(G);q.clk+=dt;const c=q.clk;
   const walkPh=q.ph==="out"||q.ph==="back";q.mv=walkPh&&G.held&&!q.noWalk&&!q.out&&c-q.turnT>1.2;
   if(q.mv){q.x+=q.dir*KM_SPD*dt;q.walk+=dt*8.5;q.idle=0;q.moved=true;q.cour=Math.min(100,q.cour+.3*dt);if(q.cur)q.cur.wk+=dt;if(Math.floor(q.walk/4)!==q.stp){q.stp=Math.floor(q.walk/4);tone(95,.08,"sine",.02);}}
   else if(walkPh&&q.moved){q.idle+=dt;if(q.idle>2.5)q.cour-=4*dt;}
   if(q.ph==="flee"){q.x-=KM_SPD*3*dt;q.walk+=dt*20;if(c-q.fleeT>1.6)kmFinish(G,true);}
   if(walkPh&&q.cour<=0){q.cour=0;q.ph="flee";q.fleeT=c;q.emo=["🙀",c];}
   if(q.out)q.cour-=3*dt;else if(!(q.cur&&q.cur.k==="wind"))q.fl=Math.min(1,q.fl+.2*dt);
   if(q.cur&&q.cur.k==="wind"&&!q.out){if(c<q.shield)q.fl=Math.min(1,q.fl+.25*dt);else q.fl-=.6*dt;if(q.fl<=0)kmOut(q);}
   if(q.cur&&q.cur.k==="steps"&&!q.cur.turned&&Math.floor((c-q.cur.t0)/.55)!==q.cur.st){q.cur.st=Math.floor((c-q.cur.t0)/.55);tone(S.scary?62:140,.13,"sine",S.scary?.07:.03);}
   if(q.cur&&c-q.cur.t0>=q.cur.D)kmStop(q,q.cur);
   if(!q.cur&&walkPh){const e=q.evs.find(e=>e.t0==null&&e.dir===q.dir&&(q.dir>0?q.x>=e.x:q.x<=e.x));if(e)kmStart(q,e);}
   if(q.ph==="out"&&q.x>=KM_SHR){q.x=KM_SHR;q.ph="shrine";}
   if(q.ph==="turn"&&c-q.ofuda>1.5){q.ph="back";q.dir=-1;}
   if(q.ph==="back"&&q.x<=KM_HOME){q.ph="end";q.endT=c;q.emo=["😸",c];chime([523,659,784]);}
   if(q.ph==="end"&&c-q.endT>1.2)kmFinish(G,false);
   q.cour=clamp(q.cour,0,100);const tc=kmCam(G,q,u);q.cam+=(tc-q.cam)*Math.min(1,dt*2.5);},
 draw(G,g,t){const q=G.st,u=kmU(G),W=G.W,H=G.H,fy=H*.74,c=q.clk;q.btns=[];
   g.save();if(S.scary&&c-q.shk<.35){const k=(1-(c-q.shk)/.35)*7*u;g.translate((Math.random()-.5)*k,(Math.random()-.5)*k);}
   g.fillStyle="#050404";g.fillRect(-10,-10,W+20,H+20);kmScene(G,g,q,u);
   if(q.cur)kmEv(G,g,q,q.cur,u,false);
   const face=kmFace(q),cx=(q.x-q.cam)*u,cf=fy+14*u,L=kmLantern(q,u,cx,cf,face);
   drawCatG(g,face>0?"moveRight":"moveLeft",q.mv||q.ph==="flee"?Math.floor(q.walk)%8:0,cx,cf,.72*u,q.ph==="flee"?clamp(1-(c-q.fleeT)/1.4,0,1):1);
   kmDrawLantern(g,q,L);kmFront(G,g,q,u);
   // the light: one radial mask around the lantern; the moon thins the dark in the garden
   const gar=clamp((q.x-1450)/250,0,1),A=.95-.1*gar,fl=q.out?0:q.fl,R=(fl>0?(150+110*fl):40)*u*(1+.05*Math.sin(c*13)+.03*Math.sin(c*29.7));
   const m=g.createRadialGradient(L.lx,L.ly,0,L.lx,L.ly,R);m.addColorStop(0,`rgba(0,0,0,${q.out?A*.9:0})`);m.addColorStop(.4,`rgba(0,0,0,${q.out?A:.12})`);m.addColorStop(.75,`rgba(0,0,0,${q.out?A:A*.7})`);m.addColorStop(1,`rgba(0,0,0,${A})`);
   g.fillStyle=m;g.fillRect(-10,-10,W+20,H+20);
   if(!q.out){g.save();g.globalCompositeOperation="lighter";const w=g.createRadialGradient(L.lx,L.ly,0,L.lx,L.ly,R*.8);w.addColorStop(0,`rgba(255,160,70,${.22*fl})`);w.addColorStop(1,"rgba(255,160,70,0)");g.fillStyle=w;g.fillRect(L.lx-R,L.ly-R,2*R,2*R);g.restore();}
   const gx=(KM_DOOR-q.cam)*u;if(gx<W){g.save();g.beginPath();g.rect(Math.max(0,gx),0,W,H);g.clip();const mx=(480-q.cam*.06)*u,my=H*.13,mr=24*u;   // the moon over the garden
     const mg=g.createRadialGradient(mx,my,0,mx,my,mr*4);mg.addColorStop(0,"rgba(210,220,235,.35)");mg.addColorStop(1,"rgba(210,220,235,0)");g.fillStyle=mg;g.fillRect(mx-mr*4,my-mr*4,mr*8,mr*8);
     g.fillStyle="#d9dccf";g.beginPath();g.arc(mx,my,mr,0,7);g.fill();g.fillStyle="rgba(150,155,150,.35)";g.beginPath();g.arc(mx-7*u,my-5*u,6*u,0,7);g.arc(mx+8*u,my+6*u,4*u,0,7);g.fill();g.restore();}
   if(q.cur)kmEv(G,g,q,q.cur,u,true);
   for(const s of q.sparks){const a=1-(c-s.t)/.5;if(a<=0)continue;g.fillStyle=`rgba(255,200,120,${a})`;g.fillRect(L.lx+s.dx*(1-a)*30*u,L.ly+s.dy*(1-a)*30*u,2.5*u,2.5*u);}
   if(q.emo&&c-q.emo[1]<1.6&&q.ph!=="flee")drawEmoji(g,q.emo[0],cx+face*22*u,cf-165*u,26*u,clamp((1.6-(c-q.emo[1]))/.4,0,1));
   g.restore();
   // HUD: courage bar, the route, hints, buttons
   const bw=W*.42;g.fillStyle="rgba(0,0,0,.5)";g.beginPath();g.roundRect(16,12,bw,9*u,5*u);g.fill();
   const cg=g.createLinearGradient(16,0,16+bw,0);cg.addColorStop(0,"#8a2a22");cg.addColorStop(.5,"#c48a3a");cg.addColorStop(1,"#e8d49a");g.fillStyle=cg;g.beginPath();g.roundRect(16,12,Math.max(4,bw*q.cour/100),9*u,5*u);g.fill();
   g.save();g.font=`600 ${11*u}px ${kmFF()}`;g.textBaseline="top";
   const rp=clamp((q.x-60)/(KM_SHR-60),0,1),r0=W*.52,r1=W-30,ry=12+4.5*u;g.strokeStyle="rgba(216,210,195,.3)";g.lineWidth=2;g.beginPath();g.moveTo(r0,ry);g.lineTo(r1,ry);g.stroke();
   g.fillStyle=q.ofuda!=null?"#e8d49a":"#d8d2c3";g.beginPath();g.arc(r0+(r1-r0)*rp,ry,4*u,0,7);g.fill();g.textAlign="left";g.textBaseline="middle";g.fillStyle="rgba(216,210,195,.7)";g.fillText("⛩",r1+4,ry);g.restore();
   let hint="";const ce=q.cur,ce_el=ce?c-ce.t0:0;
   if(q.out)hint=`Темно! Коснись три раза — зажечь свечу (${q.rel}/3)`;
   else if(ce&&ce.k==="wind"&&ce_el<ce.D)hint="Ветер! Тапай — прикрой свечу";
   else if(ce&&ce.k==="steps"&&!ce.turned)hint="Сзади шаги… Не оборачивайся — иди дальше";
   else if(q.ph==="shrine")hint="Святилище. Оставь офуда";
   else if(q.note&&c-q.note[1]<3.6&&c>q.note[1])hint=q.note[0];
   else if(!q.moved)hint="Держи палец на экране — Муся пойдёт";
   else if(q.idle>2.5&&(q.ph==="out"||q.ph==="back"))hint="Не стой подолгу — храбрость тает";
   if(hint)kmBubble(g,hint,W/2,H-24*u,u*1.02,W,true,1);
   if(ce&&ce.k==="steps"&&!ce.turned&&ce_el>.8){const w=150*u,h=40*u,x=W-w-16,y=48*u;btnRect(g,x,y,w,h,"Обернуться?",false);q.btns.push({x,y,w,h,k:"turn"});}
   if(q.ph==="shrine"){const w=200*u,h=48*u,x=W/2-w/2,y=H*.82;btnRect(g,x,y,w,h,"🙏 Оставить офуда",true);q.btns.push({x,y,w,h,k:"ofuda"});}},
 down(G,x,y,t){const q=G.st;q.noWalk=false;
   for(const b of q.btns)if(x>=b.x&&x<=b.x+b.w&&y>=b.y&&y<=b.y+b.h){q.noWalk=true;kmKey(G,q,b.k);return;}
   if(q.out){q.noWalk=true;q.rel++;for(let i=0;i<6;i++)q.sparks.push({t:q.clk,dx:rand(-1,1),dy:rand(-1,.3)});q.sparks=q.sparks.slice(-30);tone(1800+q.rel*200,.04,"square",.02);
     if(q.rel>=3){q.out=false;q.fl=.6;q.emo=["😺",q.clk];tone(660,.3,"sine",.03);}return;}
   if(q.cur&&q.cur.k==="wind"&&q.clk-q.cur.t0<q.cur.D){q.shield=q.clk+.6;}},
 up(G){G.st.noWalk=false;},
 stat:G=>`🕯 Храбрость ${Math.round(G.st.cour)}`,
 card(G,rec){const R=G.st.res||{r:0,cour:0,fled:true,got:[],st:[],met:[]},rk=KM_RK[R.r],sc=S.scary;
   const met=R.met.map(k=>KM_EV[k][2]).join(", "),stn=R.st.map(id=>{const s=STAMPS.find(x=>x[0]===id);return s?`${s[1]} ${s[2]}`:"";}).filter(Boolean).join(" · ");
   const lines=R.fled?"Храбрость кончилась, и Муся со всех лап убежала домой. Ничего: в следующую ночь получится!":[R.out?"Свеча гасла, но Муся её зажгла.":"Свеча ни разу не погасла.",R.turned?"Муся обернулась на шаги за спиной.":"Муся ни разу не обернулась.","Офуда осталась у святилища."].join(" ");
   return`<div class="card"><p class="tag">肝試し · Кимодамэси${sc?"":" · добрая версия"}</p><h3>${R.fled?"🙀 Муся убежала домой":rk[2]+" "+rk[1]}</h3><div class="big">${R.cour}</div><p>храбрость из 100</p><p>${lines}</p>${met?`<p>Встретились: ${met}.</p>`:""}
    ${R.got.length?`<div class="row" style="justify-content:center;gap:10px">${R.got.map(id=>`<span title="${IT[id].n}">${itemThumb(IT[id],56,64)}</span>`).join("")}</div><p>Новое в «🧺 Вещах»: ${R.got.map(id=>IT[id].n).join(", ")}.</p>`:""}${stn?`<p>Штампы: ${stn}</p>`:""}
    <div class="row"><button class="btn" id="gHome">Домой</button><button class="btn primary" id="gAgain">Ещё раз</button></div></div>`;}};
GAMES.push(KM_GAME);
function kmOpen(){if(G.id)return;if(!kmNight()){toast("Кимодамэси начинается после 21:00");return;}if(petAway()){toast("Муся сейчас в путешествии");return;}closePanel();openGame("km_walk");}

// ── entry points ──
hook("tray",(tray,room)=>{if(room!=="bedroom"||(S.trayMode[room]||"play")!=="play"||!kmNight())return;const row=tray.querySelector(".items");if(!row||row.querySelector('[data-x="km:open"]'))return;
  const b=`<button class="item wide" data-x="km:open"><span class="ico">🕯</span><span class="nm">Кимодамэси</span></button>`,kd=row.querySelector('[data-x="kg:open"]')||row.querySelector("[data-kaidan]");if(kd)kd.insertAdjacentHTML("afterend",b);else row.insertAdjacentHTML("beforeend",b);});
hook("click",k=>{if(k==="km:open"){kmOpen();return true;}return false;});
hook("hub",()=>{const nt=kmNight(),rk=KM.rank>=0?KM_RK[KM.rank]:null;
  const st=nt?(rk?`Ночь — дорога к святилищу открыта · звание: ${rk[1]}`:"Ночь — дорога к святилищу открыта"):`Кимодамэси начинается после 21:00${rk?" · звание: "+rk[1]:""}`;
  return`<div class="hubc"><h4>🕯 Кимодамэси <i>肝試し</i></h4><p>${st}</p>
   <p>Летними ночами японские дети по одному идут страшной дорогой — к кладбищу или старому святилищу, оставляют там знак и возвращаются. Муся возьмёт фонарик и пройдёт тёмным коридором и садом к маленькому святилищу. Пройдено: ${KM.n}${KM.n?` · лучшая храбрость: ${KM.best}`:""}. ${S.scary?"":"Страшилки выключены — ёкаи будут добрыми."}</p>
   <div class="row">${nt?`<button class="btn primary" data-x="km:open">🕯 Идти к святилищу</button>`:`<button class="btn" disabled>🌙 Ждём ночи</button>`}</div></div>`;});

// test handles
X.km={K:KM,open:kmOpen,begin(){closePanel();openPlace("km_walk");},q:()=>G.st,
  at(x,k,el=1.5,dir=1){const q=G.st,u=kmU(G);q.x=x;q.dir=dir;q.ph=dir>0?"out":"back";q.moved=true;q.cur=null;q.cam=kmCam(G,q,u);
    if(k){const e={k,x,dir,D:KM_EV[k][1]};q.evs.push(e);kmStart(q,e);e.t0=q.clk-el;}return q.cur&&q.cur.k;},
  ff(sec,held=true){const q=G.st;G.held=held;for(let i=0;i<sec*30;i++)KM_GAME.step(G,now(),1/30);G.held=false;return [Math.round(q.x),q.ph,Math.round(q.cour),q.cur&&q.cur.k];},
  auto(sec){for(let i=0;i<sec*30&&!G.over;i++){const s=G.st;G.held=!s.out&&s.ph!=="shrine";if(s.cur&&s.cur.k==="wind"&&i%15===0){KM_GAME.up(G);KM_GAME.down(G,5,G.H*.5,now());}
    if(s.out&&i%8===0){KM_GAME.down(G,5,G.H*.5,now());KM_GAME.up(G);}if(s.ph==="shrine")kmKey(G,s,"ofuda");KM_GAME.step(G,now(),1/30);}G.held=false;return G.st.res||[G.st.x,G.st.ph];},
  key:k=>kmKey(G,G.st,k),tap(){KM_GAME.down(G,5,G.H*.5,now());KM_GAME.up(G);},plan:kmPlan};
}
