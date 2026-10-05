{
// ───────────────────────── «Прятки с Мусей»: she runs off and hides in another open room ─────────────────────────
// Start: the 🙈 button on the veranda, the 家 card, or Musya's own invitation (once a day, daytime: «hide» pose + 🙈, tap her).
// The round lives in memory only (kb): a reload, travel or a story scene always brings her back. 3 min → she comes out, offended.
const KB=S.ext.hide||(S.ext.hide={n:0,best:0,f:0,spots:{},inv:""});delete KB.round;
// spots: [id, room, where, image x, image y (null = Musya's floor line), layer depth, tell, side, scale vs Musya]
// tells: tail — a tail tip out of an edge; ears — ears and eyes over an edge; box — her cardboard box; leaves — a pile of momiji
const KB_SP=[
 ["e_torii","entrance","за столбом тории",1168,1000,.38,"tail",1,.65],["e_leaves","entrance","в куче листьев",760,null,.8,"leaves",1,1],
 ["g_hedge","engawa","в кустах за верандой",720,1010,.42,"ears",1,.6],["g_box","engawa","в коробке на веранде",650,null,.8,"box",1,.85],["g_toro","engawa","за каменным фонарём",1115,1090,.42,"tail",-1,.6],
 ["c_rock","courtyard","за валуном у пруда",1130,880,.55,"ears",1,.7],["c_leaves","courtyard","в куче листьев у пруда",1010,null,.8,"leaves",1,1],["c_rock3","courtyard","за камнем в заводи",905,1035,.55,"tail",-1,.7],
 ["k_box","kitchen","в коробке на кухне",700,null,.8,"box",1,.85],["k_pot","kitchen","в горшке на полке",1030,640,.5,"ears",1,.45],["k_bowls","kitchen","за пиалами на верхней полке",1200,425,.5,"ears",1,.4],
 ["o_rock","onsen","за камнями купели",760,1150,.55,"ears",1,.7],["o_stone","onsen","за плоским камнем",1000,1290,.82,"ears",1,.9],["o_fence","onsen","на бамбуковом заборе",1000,770,.28,"ears",1,.45],
 ["b_futon","bedroom","за свёрнутым футоном",640,1240,.8,"ears",1,.8],["b_andon","bedroom","за андоном",408,1300,.8,"tail",1,.8],["b_box","bedroom","в коробке в спальне",900,null,.8,"box",1,.85],
 ["w_box","wardrobe","в коробке среди кимоно",760,null,.8,"box",1,.85],["w_screen","wardrobe","за складной ширмой",1161,1120,.8,"tail",1,.7],
 ["y_torii","games","за столбом тории",1200,1104,.45,"tail",1,.6],["y_torii2","games","за левым столбом тории",600,1104,.45,"tail",-1,.6],["y_leaves","games","в куче листьев у тории",900,null,.8,"leaves",1,1],
 ["r_bales","kura","на рисовых тюках",652,885,.4,"ears",1,.5],["r_barrel","kura","за бочками сакэ",1130,895,.4,"ears",1,.55],["r_box","kura","в коробке в кладовой",900,null,.8,"box",1,.85],
 ["a_basket","attic","в плетёной корзине",710,1050,.4,"ears",1,.5],["a_box","attic","в коробке на чердаке",950,null,.8,"box",1,.85],
 ["t_alcove","chashitsu","в нише токономы",760,1100,.5,"ears",1,.6],["t_post","chashitsu","за столбом токономы",1000,1140,.5,"tail",1,.6],
 ["h_fox","hokora","за каменной лисой",1180,1104,.45,"tail",1,.6],["h_tree","hokora","у корней священного дерева",600,1100,.45,"tail",1,.6],["h_leaves","hokora","в куче листьев у святилища",900,null,.8,"leaves",1,1]
].map(([id,room,n,x,y,d,k,dir,sc])=>({id,room,n,x,y,d,k,dir,sc}));
STAMPS.push(["kb_first","隠","Прятки","Найди спрятавшуюся Мусю"],["kb_fast","速","Зоркий глаз","Найди Мусю быстрее чем за 30 секунд"],["kb_ten","探","Знаток укромных мест","Найди Мусю в 10 разных местах"]);
let kb=null,kbInv=0,kbBoot=now();const kbDbg={on:false};
const kbHid=()=>!!(kb&&kb.ph==="hide"&&!scene.on&&!petAway());
const kbSec=()=>kb?Math.max(0,Math.round((Date.now()-kb.t0)/1000)):0;
const kbPl=(n,a,b,c)=>{const x=n%10,y=n%100;return x===1&&y!==11?a:x>=2&&x<=4&&(y<12||y>14)?b:c;};
const kbFmt=s=>Math.floor(s/60)+":"+String(s%60).padStart(2,"0");
const kbTime=s=>s<60?`${s} ${kbPl(s,"секунду","секунды","секунд")}`:kbFmt(s);
const kbRoomOk=id=>ROOMS.some(r=>r.id===id)&&!hk("tabLock",id);
const kbIdx=id=>ROOMS.findIndex(r=>r.id===id);

// ── sound: soft meow and rustle, panned towards the hiding room's tab ──
function kbOut(g,pan){const c=snd.ctx;if(pan&&c.createStereoPanner){const p=c.createStereoPanner();p.pan.value=pan;g.connect(p);p.connect(c.destination);}else g.connect(c.destination);}
function kbMeow(pan=0,vol=.05){if(!snd.on||!snd.ctx)return;const c=snd.ctx,t=c.currentTime,o=c.createOscillator(),f=c.createBiquadFilter(),g=c.createGain();
  o.type="sawtooth";o.frequency.setValueAtTime(540,t);o.frequency.linearRampToValueAtTime(840,t+.18);o.frequency.linearRampToValueAtTime(590,t+.58);
  f.type="bandpass";f.Q.value=3;f.frequency.setValueAtTime(950,t);f.frequency.linearRampToValueAtTime(1600,t+.2);f.frequency.linearRampToValueAtTime(820,t+.58);
  g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(vol,t+.07);g.gain.setValueAtTime(vol,t+.4);g.gain.exponentialRampToValueAtTime(.0001,t+.62);
  o.connect(f);f.connect(g);kbOut(g,pan);o.start(t);o.stop(t+.66);}
function kbRustle(pan=0,vol=.06){if(!snd.on||!snd.ctx)return;const c=snd.ctx,n=c.sampleRate*.55|0,b=c.createBuffer(1,n,c.sampleRate),d=b.getChannelData(0);
  for(let i=0;i<n;i++){const u=i/n;d[i]=(Math.random()*2-1)*Math.max(0,Math.sin(u*Math.PI*4))*(1-u)*(Math.random()<.35?1:.3);}
  const s=c.createBufferSource(),f=c.createBiquadFilter(),g=c.createGain();s.buffer=b;f.type="highpass";f.frequency.value=2300;g.gain.value=vol;s.connect(f);f.connect(g);kbOut(g,pan);s.start();}
function kbBell(){chime([2349,2794]);setTimeout(()=>chime([2637,2349]),360);}
function kbClue(){if(S.wear&&S.wear.neck==="suzu")kbBell();else kbRustle(0,.07);}

// ── the tells: pieces of her real sprite frames, tinted like the room ──
const kbW=document.createElement("canvas");kbW.width=384;kbW.height=416;const kbG=kbW.getContext("2d");
function kbFrame(st,f){const g=kbG;g.globalCompositeOperation="source-over";g.clearRect(0,0,384,416);frameImg(st,f,g);drawWear(g,st,f,2);const tint=kbTint();if(tint){g.globalCompositeOperation="source-atop";g.fillStyle=tint;g.fillRect(0,0,384,416);g.globalCompositeOperation="source-over";}}
// a pile of momiji leaves, painted once (cells ×2), tinted copies cached per room light
let kbPile=null;const kbPileT={};
const kbTint=()=>S.room==="bedroom"&&S.lampOff?"rgba(8,10,20,.62)":TINT[S.room]||(ROOMX[S.room]||{}).tint||"";
function kbLeaf(g,x,y,r,a,col){g.save();g.translate(x,y);g.rotate(a);g.fillStyle=col;g.beginPath();
  for(let i=0;i<10;i++){const an=-Math.PI/2+i*Math.PI/5,rr=i%2?r*.45:r;g.lineTo(Math.cos(an)*rr,Math.sin(an)*rr);}g.closePath();g.fill();
  g.strokeStyle="rgba(50,18,6,.4)";g.lineWidth=Math.max(1,r*.09);g.beginPath();g.moveTo(0,0);g.lineTo(0,r*1.25);g.stroke();g.restore();}
const KB_COL=["#9c4026","#b4582c","#843620","#bf7f37","#74552a","#a94a28","#c48a3c","#6a4424","#8f5a2c"];
function kbMakePile(){const c=document.createElement("canvas");c.width=380;c.height=170;const g=c.getContext("2d"),cx=190,base=162;let sd=7;const rnd=()=>(sd=(sd*16807)%2147483647)/2147483647;
  const gr=g.createRadialGradient(cx,base-20,10,cx,base-10,190);gr.addColorStop(0,"rgba(70,36,16,.95)");gr.addColorStop(1,"rgba(40,22,10,0)");g.fillStyle=gr;g.beginPath();g.ellipse(cx,base-26,178,58,0,Math.PI,0);g.lineTo(cx+178,base);g.lineTo(cx-178,base);g.fill();
  for(let i=0;i<190;i++){const u=rnd()*2-1,h=Math.sqrt(Math.max(0,1-u*u)),x=cx+u*170,y=base-rnd()*h*118-4,dark=1-(base-y)/150;
    const col=KB_COL[(rnd()*KB_COL.length)|0];g.globalAlpha=.9;kbLeaf(g,x,y,9+rnd()*9,rnd()*6.3,col);g.globalAlpha=dark*.25;g.fillStyle="#140a04";g.beginPath();g.arc(x,y,8,0,7);g.fill();}
  g.globalAlpha=1;return c;}
function kbPileImg(){if(!kbPile)kbPile=kbMakePile();const tint=kbTint(),k=tint;if(kbPileT[k])return kbPileT[k];
  const c=document.createElement("canvas");c.width=380;c.height=170;const g=c.getContext("2d");g.drawImage(kbPile,0,0);if(tint){g.globalCompositeOperation="source-atop";g.fillStyle=tint;g.fillRect(0,0,380,170);}return kbPileT[k]=c;}
// where a spot is on the stage now
function kbPos(sp){const cr=curRow;curRow=null;const iy=sp.y??catLineY()+(sp.k==="box"?16:22),[ex,fy]=imgToStage(visX(sp.x,70),iy,sp.d);curRow=cr;return{ex,fy,u:view.s*sp.sc};}
function kbCenter(sp){const {ex,fy,u}=kbPos(sp);return sp.k==="tail"?[ex+sp.dir*30*u,fy-14*u,Math.max(46*u,38)]:sp.k==="ears"?[ex,fy-30*u,Math.max(55*u,40)]:sp.k==="box"?[ex,fy-55*u,Math.max(70*u,44)]:[ex,fy-40*u,Math.max(85*u,46)];}
function kbShadow(x,y,rx,u){ctx.fillStyle="rgba(0,0,0,.3)";ctx.beginPath();ctx.ellipse(x,y+2*u,rx,8*u,0,0,7);ctx.fill();}
// ears and eyes over an edge at stage y ey; p 0..1 = how far she peeks
function kbPeek(ex,ey,u,p,t,clipY=ey){const f=Math.sin(t*.7)>.93?4:Math.sin(t*.37)>.6?6:0;kbFrame("rest",f);const y0=ey-(40+40*p)*u;
  ctx.save();ctx.beginPath();ctx.rect(ex-130*u,y0-10*u,260*u,clipY-y0+10*u);ctx.clip();ctx.drawImage(kbW,ex-97*u,y0,192*u,208*u);ctx.restore();
  if(dayTint()[1]&&p>.55&&f!==4){ctx.save();ctx.globalCompositeOperation="lighter";for(const ox of [85,110]){const x=ex+(ox-97)*u,y=y0+63*u,gr=ctx.createRadialGradient(x,y,0,x,y,6*u);gr.addColorStop(0,`rgba(190,230,120,${.55*(p-.5)})`);gr.addColorStop(1,"rgba(190,230,120,0)");ctx.fillStyle=gr;ctx.fillRect(x-6*u,y-6*u,12*u,12*u);}ctx.restore();}}
// a tail tip out of a vertical edge at (ex, fy), dir = which side it sticks out to
// drawn on a small canvas whose edge side fades out, so the tip seems to come from behind the thing
const kbT=document.createElement("canvas"),kbTG=kbT.getContext("2d");
function kbTail(ex,fy,u,dir,t){kbFrame("rest",0);const out=.6+.4*Math.sin(t*.9),sw=.13*Math.sin(t*2.1)+(Math.sin(t*.53)>.85?.25*Math.sin(t*14):0),k=2,W=Math.ceil(90*u*k),H=Math.ceil(80*u*k);
  if(kbT.width!==W||kbT.height!==H){kbT.width=W;kbT.height=H;}const g=kbTG;g.setTransform(1,0,0,1,0,0);g.globalCompositeOperation="source-over";g.clearRect(0,0,W,H);
  g.setTransform(k,0,0,k,0,60*u*k);g.rotate(-sw);g.drawImage(kbW,-(118+(1-out)*26)*u,-(200-8)*u,192*u,208*u);
  g.setTransform(1,0,0,1,0,0);g.globalCompositeOperation="destination-in";const gr=g.createLinearGradient(0,0,12*u*k,0);gr.addColorStop(0,"rgba(0,0,0,0)");gr.addColorStop(1,"#000");g.fillStyle=gr;g.fillRect(0,0,W,H);
  ctx.save();ctx.translate(ex,fy-8*u);ctx.scale(dir,1);ctx.drawImage(kbT,0,-60*u,W/k,H/k);ctx.restore();}
function kbDrawSpot(sp,t){const {ex,fy,u}=kbPos(sp);
  if(sp.k==="tail")kbTail(ex,fy,u,sp.dir,t);
  else if(sp.k==="ears"){const p=clamp(.5+.75*Math.sin(t*.8),0,1);kbPeek(ex,fy,u,p,t);}
  else if(sp.k==="box"){const seq=[5,5,6,6,4,5,6,7,6,5],f=seq[Math.floor(t/.75)%seq.length];kbShadow(ex,fy,62*u,u);kbFrame("box",f);ctx.drawImage(kbW,ex-96*u,fy-196*u,192*u,208*u);}
  else{const p=clamp(.4+.7*Math.sin(t*.7),0,1),top=fy-64*u;kbPeek(ex,top+18*u,u,p,t,fy-40*u);const im=kbPileImg(),w=190*u,h=85*u,jig=Math.sin(t*.53)>.8?Math.sin(t*30)*1.2*u:0;kbShadow(ex,fy,90*u,u);ctx.drawImage(im,ex-w/2+jig,fy-h+4*u,w,h);}}

// ── a round ──
function kbPick(){const rooms=[...new Set(KB_SP.map(s=>s.room))].filter(r=>r!==S.room&&kbRoomOk(r));if(!rooms.length)return null;
  const fresh=KB_SP.filter(s=>rooms.includes(s.room)&&!KB.spots[s.id]),pool=fresh.length&&Math.random()<.6?fresh:KB_SP.filter(s=>rooms.includes(s.room));return pick(pool);}
function kbStart(src){audioInit();if(kb){toast("🙈 Муся уже прячется — ищи её!");return;}
  if(petAway()){toast("Муся в путешествии — скоро вернётся");return;}if(scene.on)return;
  if(pet.action==="sleep"){toast("Муся спит — поиграете, когда проснётся");return;}
  const sp=kbPick();if(!sp){toast("Сейчас ей негде спрятаться");return;}
  kbInv=0;const ci=kbIdx(S.room),ti=kbIdx(sp.room),side=ti>ci?1:-1,s=view.s;
  kb={sp,room:sp.room,ph:"run",t0:Date.now(),st:now(),tease:0,rus:0,side,src};
  start("idle",true);react("🙈",1.6);pet.walkTarget=side>0?view.W+150*s:-150*s;pet.walkAfter="idle";setTimeout(()=>{if(kb&&kb.ph==="run"){start("walkto",true);pet.heading=side;}},650);
  toast("🙈 Муся убежала прятаться — ищи её!");sfx("pop");ui();hubDot();}
function kbGone(){if(!kb||kb.ph!=="run")return;kb.ph="hide";start("idle",true);pet.x=view.W/2;pet.home=pet.x;}
function kbOut2(face,after){const s=view.s,side=Math.random()<.5?-1:1;pet.x=side<0?-90*s:view.W+90*s;pet.home=pet.x;pet.walkTarget=clamp(view.W/2+rand(-40,40)*s,96*s,view.W-96*s);pet.walkAfter=after;start("walkto",true);pet.heading=-side;react(face,3);}
function kbEnd(how){const r=kb;if(!r)return;const sec=kbSec();kb=null;
  if(how==="found"){const sp=r.sp,[cx,cy]=kbCenter(sp),[ox]=camOff(CAT_D);
    KB.n++;KB.f=(KB.f||0)+1;const bs=Math.max(1,sec);if(!KB.best||bs<KB.best)KB.best=bs;KB.spots[sp.id]=1;disc("hide","spot_"+sp.id);
    pet.x=clamp(cx-ox,Math.max(96*view.s,view.W*.22),Math.min(view.W-96*view.s,view.W*.78));pet.home=pet.x;start("highfive");react("😹",2.4);S.needs.joy=clamp(S.needs.joy+15,0,100);
    floatFx.push({g:"✨",x:cx,y:cy,t:now()});chime([988,1318,1568]);toast(`😹 Муся нашлась за ${kbTime(sec)}!`);
    setTimeout(()=>{award("kb_first");if(sec<30)award("kb_fast");if(Object.keys(KB.spots).length>=10)award("kb_ten");},2300);}
  else if(how==="timeout"){KB.n++;if(!petAway()&&!scene.on){kbOut2("😾","sulk");toast("😾 Муся вышла сама — немного обиделась");}}
  else if(how==="give"){KB.n++;if(!petAway()&&!scene.on){kbOut2("😸","highfive");toast(`😸 Муся пряталась ${r.sp.n}`);}}
  else if(!petAway()){pet.x=view.W/2;pet.home=pet.x;}   // cancelled by travel or a story scene
  save();ui();hubDot();}
// her own invitation: once a day, daytime, idle, nobody busy
function kbInvite(force){if(KB.inv===dayKey()||dayTint()[1]||pet.action!=="idle"||petAway()||scene.on||overlaysOpen()||drag.active)return;
  if(!force&&(now()-kbBoot<45||now()-pet.lastInput<12||Math.random()>1/120))return;
  KB.inv=dayKey();save();start("hide",true);react("🙈",5);kbInv=now();setTimeout(()=>{if(kbInv&&!$("toast").classList.contains("on"))toast("🙈 Муся зовёт в прятки — нажми на неё");},1200);}
function kbFound(){if(kb&&kb.ph==="hide")kbEnd("found");}

// ── hooks ──
hook("hideCat",kbHid);
hook("boot",()=>{kb=null;kbInv=0;delete KB.round;
  const h=HK.hit||[],i=h.indexOf(kbHit);if(i>0)h.unshift(h.splice(i,1)[0]);});   // a tap on her hiding spot wins over things standing in front of it
hook("tick",t=>{if(!kb)return;
  if(kb.ph==="run"){const s=view.s;if(pet.x<-110*s||pet.x>view.W+110*s||now()-kb.st>5.5)kbGone();return;}
  if(kbHid()){if(pet.action!=="idle")start("idle",true);nextAuto=t+30;}});
hook("sec",()=>{
  if(kbInv&&(now()-kbInv>16||kb||petAway()))kbInv=0;
  if(!kb){kbInvite(false);return;}
  if(petAway()||scene.on){kbEnd("cancel");return;}
  const sec=kbSec();if(sec>=180){kbEnd("timeout");return;}
  if(kb.ph!=="hide")return;
  if(S.room===kb.room){if(sec-kb.rus>=8&&Math.random()<.35){kb.rus=sec;kbRustle(0,.035);}}
  else if(sec>=60&&sec-kb.tease>=30&&!overlaysOpen()){kb.tease=sec;const pan=kbIdx(kb.room)>kbIdx(S.room)?.85:-.85;kbMeow(pan);
    floatFx.push({g:"♪",x:pan>0?view.W-28:28,y:view.H*.42,t:now()});}
});
hook("room",id=>{if(!kb)return;if(kb.ph==="run")kbGone();if(id===kb.room&&kb.ph==="hide")setTimeout(()=>{if(kb&&S.room===kb.room)kbClue();},700);});
hook("ev",(ev,d)=>{if(ev==="act"&&kbHid()&&d!=="idle")setTimeout(()=>toast("🙈 Муся спряталась — сначала найди её"),40);});
hook("draw",(t,front)=>{
  if(kbDbg.on){if(front)return;for(const sp of KB_SP)if(sp.room===S.room){kbDrawSpot(sp,t);const [cx,cy,r]=kbCenter(sp);ctx.strokeStyle="#ff0";ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(cx,cy,r,0,7);ctx.stroke();ctx.fillStyle="#ff0";ctx.font="11px sans-serif";ctx.fillText(sp.id,cx-r,cy-r-3);}return;}
  if(!kbHid()||S.room!==kb.room)return;const sp=kb.sp,fr=sp.d>=CAT_D-.01&&(sp.y??catLineY()+20)>catLineY()+6;if(fr!==front)return;kbDrawSpot(sp,t);});
function kbHit(x,y){
  if(kbInv&&!kb&&hitCat(x,y)){kbStart("inv");return true;}
  if(!kbHid()||S.room!==kb.room)return false;const [cx,cy,r]=kbCenter(kb.sp);if(Math.hypot(x-cx,y-cy)>r)return false;kbFound();return true;}
hook("hit",kbHit);
hook("tray",(tray,room)=>{if(room!=="engawa"||(S.trayMode[room]||"play")!=="play")return;const el=tray.querySelector(".items");if(!el||el.querySelector('[data-x^="kb:"]'))return;const wd=[...el.querySelectorAll(".item.wide")].pop();
  (wd||el).insertAdjacentHTML(wd?"afterend":"afterbegin",kb?`<button class="item wide" data-x="kb:give"><span class="ico">🏳️</span><span class="nm">Сдаться</span></button>`:`<button class="item wide" data-x="kb:go"><span class="ico">🙈</span><span class="nm">Прятки</span></button>`);});
hook("click",k=>{if(!k.startsWith("kb:"))return;if(k==="kb:go"){closePanel();kbStart("btn");}else if(k==="kb:give"){closePanel();if(kb)kbEnd("give");}return true;});
hook("hubDot",()=>!!kb);
hook("hub",()=>{const n=Object.keys(KB.spots).length,sec=kbSec();
  const st=kb?`Муся спряталась! Ищи… ${kbFmt(sec)}`:KB.n?`Сыграно: ${KB.n}, лучшее время: ${KB.best?kbFmt(KB.best):"—"}`:"Муся ждёт: она ещё ни разу не пряталась";
  return`<div class="hubc"><h4>🙈 Прятки <i>隠れん坊</i></h4><p>${st}</p><p>Муся убегает в другую открытую комнату и прячется. Ищи кончик хвоста, ушки над коробкой, слушай колокольчик и шорох. Через минуту она начнёт тихонько мяукать с той стороны, где спряталась, а через три минуты выйдет сама.</p><p>Найдено укромных мест: ${n} из ${KB_SP.length}.</p>
   <div class="row">${kb?`<button class="btn" data-x="kb:give">🏳️ Сдаться</button>`:`<button class="btn primary" data-x="kb:go">🙈 Играть в прятки</button>`}</div></div>`;});
X.kb={st:()=>kb,K:KB,spots:KB_SP,start:kbStart,found:kbFound,end:kbEnd,dbg:kbDbg,sec:kbSec,hid:kbHid,center:id=>kbCenter(KB_SP.find(s=>s.id===id)),
  // test: put her into a given spot right away
  put(id){const sp=KB_SP.find(s=>s.id===id);kb={sp,room:sp.room,ph:"hide",t0:Date.now(),st:now(),tease:0,rus:0,side:1,src:"test"};ui();hubDot();},
  age(s){if(kb)kb.t0-=s*1000;},invite(){KB.inv="";kbInvite(true);return kbInv>0;}};
}
