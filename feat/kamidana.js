{
// ───────────────────────── «Камидана»: the household Shinto altar high on the kitchen wall ─────────────────────────
// A shelf with a shinmei-style miniature shrine, a mirror, a shimenawa with shide, sakaki in two vases and a tiny candle
// (always lit). Every morning (5:00–11:00, grace till noon) the player taps the shelf → a small sheet at the bottom of the
// stage (the room stays visible): put rice, water, salt (+ fresh sakaki every 10 days, optional sake) → the ritual
// 二礼二拍手一礼 (bow, bow, clap, clap, bow — in order) → the day's blessing card (one of 6, small effects inside this
// block). Streak milestones 3/7/30 → things «Камидана» + stamps. Musya comes closer and watches (😌 at the end).
// Art: art/kamidana_art.py → assets/items/atlas_kmd.webp.
// State: S.ext.kamidana = {d:last offering day, st:streak, best, n:total, sk:sakaki day, bl:blessing of day d, pd/put:today's
//   offerings in progress, nk:sake count, seen:{blessing:1}, ms:[milestones], told:morning toast day, gd:guest bonus day, fd:find day}
const KMD_AT={"shelf":[186,0,380,228],"sk":[152,234,84,134],"skw":[238,234,84,134],"rice":[450,234,44,34],"salt":[408,234,40,36],"water":[376,234,30,38],
 "sake":[324,234,26,52],"candle":[352,234,22,48]},KMD_AW=[720,410],KMD_C="Камидана";
const KM=S.ext.kamidana||(S.ext.kamidana={d:"",st:0,best:0,n:0,sk:"",bl:"",pd:"",put:{},nk:0,seen:{},ms:[],told:""});
KM.seen=KM.seen||{};KM.ms=KM.ms||[];KM.put=KM.put||{};
addItems([
 {id:"kmd_sakaki",n:"Сакаки в вазочках",c:KMD_C,w:150,h:176,a:"b",p:0,at:["kmd",0,234],src:"⛩ камидана",hint:"Делай утреннее подношение у камиданы 3 дня подряд"},
 {id:"kmd_ofuda",n:"Офуда Исэ",c:KMD_C,w:110,h:214,a:"b",p:0,at:["kmd",568,0],src:"⛩ камидана",hint:"Делай утреннее подношение у камиданы 7 дней подряд"},
 {id:"kmd_shime",n:"Новогодний симэкадзари",c:KMD_C,w:184,h:232,a:"t",p:0,at:["kmd",0,0],src:"⛩ камидана",hint:"Делай утреннее подношение у камиданы 30 дней подряд"}],{kmd:KMD_AW});
STAMPS.push(["kmd_1","礼","Первое подношение","Сделай утреннее подношение у камиданы на кухне"],["kmd_7","誠","Неделя у камиданы","Делай подношение у камиданы 7 дней подряд"],
 ["kmd_30","神","Месяц у камиданы","Делай подношение у камиданы 30 дней подряд"]);
const KMD_MS=[[3,"kmd_sakaki",null],[7,"kmd_ofuda","kmd_7"],[30,"kmd_shime","kmd_30"]];
const KMD_BL=[
 {id:"gar",i:"🌱",n:"Удача в огороде",t:"Грядки во дворике сегодня растут на четверть быстрее."},
 {id:"syt",i:"🍙",n:"Сытость держится дольше",t:"Сегодня Муся проголодается почти на треть медленнее."},
 {id:"joy",i:"💗",n:"Радость Муси",t:"Радости сразу прибавилось, а у камиданы весь день тёплый свет."},
 {id:"gst",i:"⛩",n:"Улыбка гостей",t:"Гость у ворот, которого ты сегодня угостишь, оставит ещё и сладость."},
 {id:"tih",i:"🌙",n:"Тихий дом",t:"В доме спокойно: Муся спит крепче, и силы возвращаются быстрее."},
 {id:"nah",i:"🍀",n:"Находчивость",t:"Удача на стороне Муси: сегодня она что-нибудь найдёт."}];
const KMD_P={x:1125},KMD_S=1.25;   // the shelf on the kitchen wall (d .5) above the shelf with bowls; max sprite scale (y: kmLay)
const KMD_SEQ=["b","b","c","c","b"];

// ── time and state
const kmDD=(a,b)=>Math.round((new Date(b+"T12:00:00")-new Date(a+"T12:00:00"))/864e5);
const kmDone=()=>KM.d===dayKey(),kmBl=()=>kmDone()?KM.bl:"",kmBD=id=>KMD_BL.find(b=>b.id===id);
const kmWin=()=>{const h=hourNow();return h>=5&&h<12;};          // 5:00–11:00 officially, grace till noon
const kmWait=()=>kmWin()&&!kmDone();
const kmStreak=()=>KM.d&&kmDD(KM.d,dayKey())<=1?KM.st:0;
const kmSkAge=()=>KM.sk?kmDD(KM.sk,dayKey()):99,kmSkNeed=()=>kmSkAge()>=10;
function kmPut(){if(KM.pd!==dayKey()){KM.pd=dayKey();KM.put={};}return KM.put;}
const kmReqOk=()=>{const P=kmPut();return P.rice&&P.water&&P.salt&&(P.sakaki||!kmSkNeed());};
function kmPick(){const pool=KMD_BL.filter(b=>b.id!==KM.bl),un=pool.filter(b=>!KM.seen[b.id]);return un.length&&Math.random()<.6?pick(un):pick(pool);}
function kmNext(){const st=kmStreak();for(const [m,id] of KMD_MS)if(!KM.ms.includes(m))return[m-st,IT[id].n];return null;}

// ── sounds
function kmClap(){if(!snd.on||!snd.ctx)return;const c=snd.ctx,N=Math.floor(c.sampleRate*.14);
  const B=kmClap.b||(kmClap.b=(()=>{const b=c.createBuffer(1,N,c.sampleRate),d=b.getChannelData(0);for(let i=0;i<N;i++)d[i]=(Math.random()*2-1)*Math.pow(1-i/N,5);return b;})());
  for(const [dt,v] of [[0,.9],[.07,.16],[.15,.06]]){const s=c.createBufferSource(),f=c.createBiquadFilter(),g=c.createGain();s.buffer=B;f.type="bandpass";f.frequency.value=1250;f.Q.value=.8;g.gain.value=v;
    s.connect(f);f.connect(g);g.connect(c.destination);s.start(c.currentTime+dt);}}
const kmBowSnd=()=>{tone(196,.7,"sine",.05);tone(294,.5,"sine",.018);};

// ── the sheet over the bottom tray (the whole room — the shelf and Musya — stays visible above it)
document.body.insertAdjacentHTML("beforeend",'<div class="kmd-sh" id="kmdSh" hidden></div>');
const kmSh=$("kmdSh");let kmMode="",kmI=0,kmMsg="",kmGot=null;const kmFx={put:{},bow:-9,clap:-9,fin:-9};
function kmOpen(m){kmMode=m;kmI=0;kmMsg="";kmGot=null;kmSh.hidden=false;kmRender();
  if(m!=="card"&&!petAway()&&pet.action!=="sleep"&&!scene.on)walkTo({x:KMD_P.x-240},"idle","👀");}
function kmClose(){if(kmSh.hidden)return;kmSh.hidden=true;kmMode="";}
const kmBtn=(k,i,n,cls="",dis=false)=>`<button class="kmd-b ${cls}" data-k="${k}"${dis?" disabled":""}><i>${i}</i><span>${n}</span></button>`;
function kmPlace(){const st=$("stage").getBoundingClientRect(),tr=$("tray").getBoundingClientRect();kmSh.style.left=st.left+"px";kmSh.style.width=st.width+"px";kmSh.style.bottom=Math.max(0,innerHeight-Math.max(tr.bottom,st.bottom))+"px";}
addEventListener("resize",()=>{if(!kmSh.hidden)kmPlace();});
function kmRender(){if(kmSh.hidden)return;kmPlace();const P=kmPut(),need=kmSkNeed();let h="";
  if(kmMode==="put"){const d=today().getDate(),tx=kmMsg||(`Поставь на полку рис, воду и соль${need?(KM.sk?", а увядшие сакаки смени на свежие":" и веточки сакаки"):""}.`+(d===1||d===15?` Сегодня ${d}-е — хорошо поднести и сакэ.`:""));
    h=`<div class="kmd-hd"><b>⛩ Утреннее подношение</b><button class="kmd-x" data-k="x" aria-label="Закрыть">✕</button></div><div class="kmd-tx">${tx}</div><div class="kmd-row">`+
      [["rice","🍚","Рис"],["water","💧","Вода"],["salt","🧂","Соль"]].map(([k,i,n])=>kmBtn(k,i,P[k]?"✓ "+n:n,P[k]?"on":"")).join("")+
      (need?kmBtn("sakaki","🌿",P.sakaki?"✓ Сакаки":"Сакаки",P.sakaki?"on":""):kmBtn("sk0","🌿","свежие","on",true))+
      kmBtn("sake","🍶",P.sake?"✓ Сакэ":"Сакэ",P.sake?"on":"opt")+kmBtn("pray","🙏","Молитва","pr",!kmReqOk())+`</div>`;}
  else if(kmMode==="rit"){const tip=["Сначала — поклон","Ещё один поклон","Теперь хлопок в ладоши","Ещё хлопок","И последний, глубокий поклон"][kmI];
    h=`<div class="kmd-hd"><b>⛩ Два поклона, два хлопка, поклон</b><button class="kmd-x" data-k="x" aria-label="Закрыть">✕</button></div>
     <div class="kmd-tx c">${kmMsg||tip}</div>
     <div class="kmd-row">${kmBtn("b","🙇","Поклон","big")}<div class="kmd-seq">${KMD_SEQ.map((s,i)=>`<span class="${i<kmI?"on":""}">${s==="b"?"礼":"拍"}</span>`).join("")}</div>${kmBtn("c","👏","Хлопок","big")}</div>`;}
  else if(kmMode==="card"){const b=kmBD(KM.bl)||KMD_BL[0],st=kmStreak(),nx=kmNext();
    h=`<div class="kmd-hd"><b>⛩ Благословение дня</b><button class="kmd-x" data-k="x" aria-label="Закрыть">✕</button></div>
     <div class="kmd-row"><div class="kmd-card"><i>${b.i}</i><div><b>${b.n}</b><small>${b.t}</small></div></div>${kmBtn("ok","🙏","Хорошо","pr")}</div>
     <div class="kmd-tx">${kmGot?`🎁 За ${daysWord(st)} подряд — «${kmGot.n}» (🧺 Вещи → ${KMD_C}). `:""}Подношения подряд: ${st}.${nx&&!kmGot?` До «${nx[1]}» — ещё ${daysWord(Math.max(1,nx[0]))}.`:""} Завтра утром — снова к камидане.</div>`;}
  kmSh.innerHTML=h;}
kmSh.addEventListener("click",e=>{const b=e.target.closest("[data-k]");if(!b||b.disabled)return;audioInit();kmAct(b.dataset.k);});
function kmAct(k){const P=kmPut();
  if(k==="x"||k==="ok"){kmClose();return;}
  if(kmMode==="put"&&["rice","water","salt","sakaki","sake"].includes(k)){if(P[k])return;P[k]=1;kmFx.put[k]=now();if(k==="sakaki")KM.sk=dayKey();
    tone(k==="sake"?740:880,.09,"triangle",.04);setTimeout(()=>tone(1320,.12,"sine",.02),70);kmMsg=kmReqOk()?"Всё на месте. Теперь — молитва 🙏":"";save();kmRender();return;}
  if(k==="pray"&&kmMode==="put"&&kmReqOk()){kmMode="rit";kmI=0;kmMsg="";kmRender();return;}
  if(kmMode==="rit"&&kmI<KMD_SEQ.length&&(k==="b"||k==="c"))kmPress(k);}
function kmPress(k){if(k!==KMD_SEQ[kmI]){kmI=0;kmMsg="Не по порядку. Заново: два поклона, два хлопка и поклон.";tone(150,.25,"sine",.05);kmRender();return;}
  kmI++;kmMsg="";if(k==="b"){kmFx.bow=now();kmBowSnd();}else{kmFx.clap=now();kmClap();}
  if(kmI>=KMD_SEQ.length){kmMsg="🙏";setTimeout(kmFinish,650);}kmRender();}
function kmFinish(){if(kmDone()){kmMode="card";kmRender();return;}const k=dayKey(),P=kmPut();KM.st=KM.d&&kmDD(KM.d,k)===1?KM.st+1:1;KM.best=Math.max(KM.best||0,KM.st);KM.n=(KM.n||0)+1;KM.d=k;if(P.sake)KM.nk=(KM.nk||0)+1;
  const b=kmPick();KM.bl=b.id;KM.seen[b.id]=1;disc("kamidana","b_"+b.id);award("kmd_1");
  kmGot=null;for(const [m,id,st] of KMD_MS)if(KM.st>=m&&!KM.ms.includes(m)){KM.ms.push(m);S.owned.add(id);disc("kamidana","d"+m);if(st)award(st);kmGot=IT[id];}
  S.needs.joy=clamp(S.needs.joy+(P.sake?6:3)+(b.id==="joy"?15:0),0,100);
  kmFx.fin=now();chime([523,659,784,1046]);
  if(kmBox){const x=(kmBox[0]+kmBox[2])/2,y=kmBox[1]+(kmBox[3]-kmBox[1])*.45;for(let i=0;i<3;i++)floatFx.push({g:"✨",x:x+(i-1)*24,y:y-i*6,t:now()});}
  if(!petAway()&&pet.action!=="sleep"){react("😌",3);if(b.id==="joy")setTimeout(()=>burst(10),600);}
  save();ui();hubDot();tabDots();kmMode="card";kmRender();}
function kmTap(){audioInit();
  if(kmDone()){kmOpen("card");return;}
  const h=hourNow();if(h<5){toast("⛩ Подношение — утром, с 5:00 до 11:00");tone(330,.3,"sine",.03);return;}
  if(h>=12){toast("Утреннее подношение пропущено — завтра утром");tone(262,.3,"sine",.03);return;}
  kmOpen("put");}

// ── in the room: the shelf on the wall at the wall's depth, offerings, the candle, ritual effects
let kmIm=null,kmBox=null,kmFit={key:""};const kmC={};
// fit the shelf between the top of the visible wall and the bowls below it (wide screens crop the top of the painting):
// shide tips stay at image y≈440 (just over the bowls), the scale shrinks from 1.25 to .85 when the top of the wall is cut off
// (measured once per stage size, after the 3D camera's room-entry swing has settled; until then the last/default fit)
function kmLay(){const key=view.W+"x"+view.H+(G3.on?"g":"");if(kmFit.key===key)return kmFit;if(G3.on&&now()-cam.trans<2.2)return kmFit.s?kmFit:{s:KMD_S,y:355};
  const a=imgToStage(KMD_P.x,300,.5)[1],b=imgToStage(KMD_P.x,500,.5)[1],vt=b>a?300-a*200/(b-a):0,s=clamp((400-vt)/228,.85,KMD_S);
  return kmFit={key,s,y:440-68*s,vt};}
hook("boot",()=>atlasImg("kmd",im=>{kmIm=im;}));
function kmSpr(k,n){const key=k+(n?"n":"d");if(kmC[key])return kmC[key];const r=KMD_AT[k],cv=document.createElement("canvas");cv.width=r[2];cv.height=r[3];
  const g=cv.getContext("2d");g.drawImage(kmIm,r[0],r[1],r[2],r[3],0,0,r[2],r[3]);g.globalCompositeOperation="source-atop";g.fillStyle=n?"rgba(16,12,20,.36)":"rgba(40,22,10,.2)";g.fillRect(0,0,r[2],r[3]);return kmC[key]=cv;}
function kmFlame(x,y,s,t,ph){const f=1+.13*Math.sin(t*9+ph)+.07*Math.sin(t*23+ph*2),sw=.6*Math.sin(t*5.3+ph);
  ctx.save();ctx.globalCompositeOperation="lighter";const g=ctx.createRadialGradient(x,y-4*s,0,x,y-4*s,16*s*f);g.addColorStop(0,"rgba(255,190,110,.45)");g.addColorStop(1,"rgba(255,150,60,0)");
  ctx.fillStyle=g;ctx.fillRect(x-17*s,y-21*s,34*s,34*s);ctx.restore();
  ctx.fillStyle="rgba(255,160,60,.92)";ctx.beginPath();ctx.ellipse(x+sw*s*.4,y-4.4*s*f,2.2*s,5*s*f,sw*.05,0,7);ctx.fill();
  ctx.fillStyle="rgba(255,248,215,.96)";ctx.beginPath();ctx.ellipse(x+sw*s*.3,y-3.2*s*f,1.1*s,2.6*s*f,0,0,7);ctx.fill();}
hook("draw",(t,front)=>{if(front)return;kmBox=null;if(S.room!=="kitchen"||scene.on||!kmIm)return;curRow=null;
  const L=kmLay(),[x,y]=imgToStage(KMD_P.x,L.y,.5),k=L.s*(imgToStage(KMD_P.x+100,L.y,.5)[0]-x)/100,n=dayTint()[1],T=now(),P=KM.pd===dayKey()?KM.put:{},bl=kmBl();
  const fin=clamp((T-kmFx.fin)/2.4,0,1),finA=fin<1?Math.sin(Math.PI*fin):0;
  // warm candle light on the wall behind the shelf
  const fl=.88+.08*Math.sin(t*7.3)+.04*Math.sin(t*17.1),ga=(n?.2:.1)*fl+(bl==="joy"?.08:0)+.18*finA,gr=ctx.createRadialGradient(x,y-60*k,0,x,y-60*k,230*k);
  gr.addColorStop(0,`rgba(255,190,110,${ga})`);gr.addColorStop(1,"rgba(255,170,90,0)");ctx.fillStyle=gr;ctx.fillRect(x-230*k,y-290*k,460*k,460*k);
  ctx.drawImage(kmSpr("shelf",n),x-190*k,y-160*k,380*k,228*k);
  const spr=(id,dx,flip,sc=1)=>{const r=KMD_AT[id],w=r[2]*k*sc,h=r[3]*k*sc,cx=x+dx*k;
    if(flip){ctx.save();ctx.translate(cx,0);ctx.scale(-1,1);ctx.drawImage(kmSpr(id,n),-w/2,y-h,w,h);ctx.restore();}else ctx.drawImage(kmSpr(id,n),cx-w/2,y-h,w,h);};
  const pop=id=>{const e=clamp((T-(kmFx.put[id]||-9))/.35,0,1);return e>=1?1:e*(1+.5*Math.sin(Math.PI*e));};
  if(KM.sk){const w=kmSkAge()>=10?"skw":"sk",s=P.sakaki?pop("sakaki"):1;spr(w,-160,false,s);spr(w,160,true,s);}
  spr("candle",-126,false);spr("candle",126,true);
  for(const [id,dx] of [["sake",-92],["sake",92],["salt",-44],["water",44],["rice",0]])if(P[id])spr(id,dx,false,pop(id));
  const s=Math.max(k*1.3,.55);kmFlame(x-126*k,y-44*k,s*(1+.5*finA),t,0);kmFlame(x+126*k,y-44*k,s*(1+.5*finA),t,2.1);
  // the ritual: claps send a ring from the mirror, the last bow makes the mirror glint
  const mx=x,my=y-42*k,ce=(T-kmFx.clap)/.8;
  if(ce>=0&&ce<1){ctx.strokeStyle=`rgba(255,240,210,${.55*(1-ce)})`;ctx.lineWidth=2;ctx.beginPath();ctx.arc(mx,my,(16+120*ce)*k,0,7);ctx.stroke();}
  if(finA>0){ctx.save();ctx.globalCompositeOperation="lighter";const R=60*k*finA,g=ctx.createRadialGradient(mx,my,0,mx,my,R);g.addColorStop(0,`rgba(255,250,225,${.7*finA})`);g.addColorStop(1,"rgba(255,220,160,0)");
    ctx.fillStyle=g;ctx.fillRect(mx-R,my-R,R*2,R*2);ctx.strokeStyle=`rgba(255,250,230,${.8*finA})`;ctx.lineWidth=1.4;const L=34*k*finA;
    ctx.beginPath();ctx.moveTo(mx-L,my);ctx.lineTo(mx+L,my);ctx.moveTo(mx,my-L);ctx.lineTo(mx,my+L);ctx.stroke();ctx.restore();}
  // tap zone + a soft pulse while the morning offering waits
  if(kmWait()&&kmSh.hidden){const a=.1+.08*Math.sin(t*2.2),g=ctx.createRadialGradient(x,y-70*k,40*k,x,y-70*k,170*k);g.addColorStop(0,"rgba(255,215,150,0)");g.addColorStop(.7,`rgba(255,215,150,${a})`);g.addColorStop(1,"rgba(255,215,150,0)");
    ctx.fillStyle=g;ctx.fillRect(x-170*k,y-240*k,340*k,340*k);}
  const hw=Math.max(190*k,40),top=Math.min(y-170*k,y-60);kmBox=[x-hw,top,x+hw,y+Math.max(68*k,24)];});
hook("overlay",()=>{const e=(now()-kmFx.bow)/1.1;if(e<0||e>=1||S.room!=="kitchen")return;ctx.fillStyle=`rgba(6,4,2,${.22*Math.sin(Math.PI*e)})`;ctx.fillRect(0,0,view.W,view.H);});
hook("hit",(x,y)=>{if(!kmBox||S.room!=="kitchen"||scene.on)return;const [x0,y0,x1,y1]=kmBox;if(x<x0||x>x1||y<y0||y>y1)return;kmTap();return true;});

// ── blessings at work (small, only today)
let kmLk=0;
hook("sec",()=>{if(!kmSh.hidden&&(S.room!=="kitchen"||scene.on||overlaysOpen()))kmClose();
  const b=kmBl(),away=petAway();
  if(b==="syt"&&!away&&S.needs.food>0)S.needs.food=clamp(S.needs.food+2.2/60*.3,0,100);
  if(b==="tih"&&!away&&pet.action==="sleep")S.needs.energy=clamp(S.needs.energy+(S.lampOff?30:14)/60*.3,0,100);
  if(b==="gar")for(const q of S.garden)if(q&&q.t0&&bedP(q)<1)q.t0-=250;
  const free=!overlaysOpen()&&!scene.on&&!$("toast").classList.contains("on");
  if(b==="nah"&&KM.fd!==dayKey()&&!away&&free&&++kmLk>150){const id=pick(["i_azuki","i_mochigome","i_sugar","i_egg"]);KM.fd=dayKey();give(id,1);save();
    toast(`🍀 Находчивость: Муся нашла «${FOOD[id].n}»`);sfx("coin");if(pet.action!=="sleep")react("😸",1.8);}
  if(kmWait()&&KM.told!==dayKey()&&free){KM.told=dayKey();save();toast("⛩ Утро: камидана ждёт подношения");chime([784,988]);hubDot();tabDots();}});
hook("ev",(e,d)=>{if(e!=="guest"||kmBl()!=="gst"||KM.gd===dayKey())return;KM.gd=dayKey();const id=pick(["ds_dango","ds_mochi","ds_daifuku"]);give(id,1);save();
  setTimeout(()=>toast(`⛩ Гость оставил ещё и «${FOOD[id].n}»`),2600);});
hook("room",()=>{if(S.room!=="kitchen")kmClose();});

// ── 家 hub card, dots, album
hook("hub",()=>{const h=hourNow(),b=kmBD(kmBl()),st=kmStreak(),nx=kmNext(),age=kmSkAge();
  const p=kmDone()?`Сегодня подношение сделано: благословение — «${b.n}»`:h<5?"Подношение делают утром — с 5:00 до 11:00":h<11?"Утреннее подношение ждёт (до 11:00)":h<12?"Утреннее подношение ждёт — успей до полудня":"Утреннее подношение уже пропущено — завтра утром";
  const sk=!KM.sk?"Веточки сакаки поставишь при первом подношении.":age<10?`Сакаки свежие — менять через ${daysWord(10-age)}.`:"Сакаки увяли — смени их при подношении.";
  return`<div class="hubc"><h4>⛩ Камидана <i>神棚</i></h4><p>${p}</p>
   ${b?`<div class="kmd-card"><i>${b.i}</i><div><b>${b.n}</b><small>${b.t}</small></div></div>`:""}
   <p>Домашний алтарь высоко на стене кухни. Утром — рис, вода и соль, потом два поклона, два хлопка и поклон.</p>
   <p>Подношения подряд: ${st}${KM.best?` · рекорд: ${KM.best}`:""}${KM.n?` · всего: ${KM.n}`:""}.${nx?` До «${nx[1]}» — ещё ${daysWord(Math.max(1,nx[0]))} подряд.`:""} ${sk}</p>
   <div class="row"><button class="btn" data-x="kmd:go">⛩ К камидане</button></div></div>`;});
hook("click",key=>{if(key!=="kmd:go")return;closePanel();const go=()=>{if(S.room==="kitchen")kmTap();};if(S.room!=="kitchen"){goRoom("kitchen");setTimeout(go,800);}else go();return true;});
hook("hubDot",()=>kmWait());
hook("tabDot",r=>r==="kitchen"&&kmWait());
hook("album",el=>{el.insertAdjacentHTML("beforeend",`<h3 class="bh">⛩ Камидана</h3><p class="lead">${KM.n?`Подношений: ${KM.n} · лучшая серия: ${daysWord(KM.best)} подряд${KM.nk?` · сакэ подносили ${KM.nk} раз`:""}. Благословения дня:`:"Подношений пока не было. Камидана — на стене кухни, подойди к ней утром."}</p>
  <div class="coll">${KMD_BL.map(b=>{const on=KM.seen[b.id];return`<div class="ci ${on?"on":""}"><span class="kmd-ai">${on?b.i:"❔"}</span><small>${on?b.n:"???"}</small></div>`;}).join("")}</div>`);});

X.kamidana=X.kmd={get luck(){return kmBl()==="nah";},lay:()=>kmFit,quiet:()=>kmBl()==="tih",bless:kmBl,st:KM,open:kmTap,act:kmAct,fin:kmFinish,box:()=>kmBox,
  tap(){if(!kmBox)return false;return !!hk("hit",(kmBox[0]+kmBox[2])/2,(kmBox[1]+kmBox[3])/2);},
  reset(){Object.assign(KM,{d:"",st:0,bl:"",pd:"",put:{},told:""});kmClose();}};

document.head.insertAdjacentHTML("beforeend",`<style>
.kmd-sh{position:fixed;z-index:8;box-sizing:border-box;padding:10px 12px 12px;background:linear-gradient(#141210,#0b0a09);border:1px solid rgba(201,162,74,.35);border-bottom:0;border-radius:14px 14px 0 0;box-shadow:0 -10px 24px rgba(0,0,0,.55);color:#ece5d4}
.kmd-hd{display:flex;align-items:center;gap:8px;font:700 16px/1.2 var(--display);color:var(--sakura);margin-bottom:3px}.kmd-hd b{flex:1}
.kmd-x{background:none;border:0;color:#a9a294;font-size:17px;padding:2px 6px;cursor:pointer}
.kmd-tx{font:15px/1.35 var(--display);color:#e6dcc8;margin-bottom:8px;text-wrap:pretty}.kmd-tx.c{text-align:center}
.kmd-row{display:flex;gap:6px;justify-content:center;align-items:center}
.kmd-b{flex:1 1 0;min-width:0;max-width:84px;height:56px;border-radius:12px;background:var(--ink-2);border:1px solid var(--line);color:#ece5d4;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;font:11.5px/1.1 system-ui,sans-serif;cursor:pointer;padding:0 2px;white-space:nowrap}
.kmd-b i{font-style:normal;font-size:21px;line-height:1}.kmd-b.on{border-color:rgba(201,162,74,.7);background:#26200f;color:#f0dfae}.kmd-b.opt{border-style:dashed}
.kmd-b.pr{border-color:#c9a24a;background:#4a2418}.kmd-b:disabled{opacity:.38;cursor:default}.kmd-b.big{max-width:120px;height:58px;font-size:13px}.kmd-b.pr:not(.big){flex:none;width:76px;height:56px}
.kmd-seq{display:flex;justify-content:center;gap:5px;flex:none}
.kmd-seq span{width:31px;height:34px;border-radius:9px;border:1px solid var(--line);display:grid;place-items:center;font:20px/1 "Noto Serif JP",serif;color:#5d584e;background:#0d0c0b}
.kmd-seq span.on{color:#f3e2b0;border-color:#c9a24a;background:#2a2316;box-shadow:0 0 10px rgba(255,200,120,.25)}
.kmd-card{display:flex;gap:10px;align-items:center;padding:8px 10px;border-radius:12px;background:linear-gradient(#2a2216,#17130d);border:1px solid #6a5634;margin:2px 0 8px}.kmd-row>.kmd-card{flex:1;margin:0}.kmd-row+.kmd-tx{margin:8px 0 0}
.kmd-card>i{font-style:normal;font-size:30px;line-height:1}:is(.kmd-sh,.hubc) .kmd-card b{display:block;font:700 16px/1.25 var(--display);color:#f3e2b0}
:is(.kmd-sh,.hubc) .kmd-card small{display:block;font-size:12.5px;line-height:1.3;color:#d8ccb4}
.ci .kmd-ai{font-size:30px;line-height:52px;height:52px;filter:grayscale(1) opacity(.4)}.ci.on .kmd-ai{filter:none}
</style>`);
}
