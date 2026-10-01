{
// ───────────────────────── «Мастерская» (prefix ws): a craft workbench, materials from everyday life, 16 hand-made things ─────────────────────────
// Materials come from what the player already does (harvest, fishing, watering, guests, forest steps, other add-ons' discoveries);
// paper, thread and paint are free (∞). Blueprints open by milestones; crafting is a 4-second moment with Musya pawing at the bench.
// State: S.ext.craft = {mat:{k:n}, made:{id:ts}, n, kn:[known recipe ids], nw:[new unseen], f:{harvest,fish,forest,guest,water,feather}, seen, last, fn, wd, wn}
// Art: art/workshop_art.py → assets/items/atlas_ws.webp (bench, 13 material icons, 16 things).
const WS_AW=1200,WS_AH=514;
const WS_R={"bench":[0,0,420,250],"m_wara":[126,422,64,64],"m_ha":[192,422,64,64],"m_uroko":[258,422,64,64],"m_kai":[324,422,64,64],"m_eda":[390,422,64,64],"m_koke":[456,422,64,64],"m_donguri":[522,422,64,64],"m_hane":[588,422,64,64],"m_tsuchi":[654,422,64,64],"m_nuno":[720,422,64,64],"m_kami":[786,422,64,64],"m_ito":[852,422,64,64],"m_enogu":[918,422,64,64],
 "ws_chochin":[1090,0,96,168,"t"],"ws_kaeru":[0,422,124,92,"b"],"ws_teru":[512,252,92,150,"t"],"ws_uma":[606,252,164,150,"b"],"ws_wreath":[154,252,156,164,"t"],"ws_shells":[422,0,92,196,"t"],"ws_frame":[0,252,152,168,"t"],"ws_omamori":[312,252,72,152,"t"],"ws_kokeshi":[610,0,84,192,"b"],"ws_sensu":[772,252,196,132,"b"],"ws_kendama":[870,0,104,184,"b"],"ws_kinchaku":[970,252,112,132,"b"],"ws_furin":[516,0,92,196,"t"],"ws_mizuhiki":[386,252,124,152,"t"],"ws_hokora":[696,0,172,192,"b"],"ws_hotaru":[976,0,112,172,"b"]};
// materials: [name, icon fallback, free]
const WS_M={wara:["Солома","🌾"],ha:["Листья","🍁"],uroko:["Чешуя","🐟"],kai:["Ракушки","🐚"],eda:["Веточки","🌿"],koke:["Мох","🌱"],donguri:["Жёлуди","🌰"],hane:["Перья","🪶"],
  tsuchi:["Глина","🟤"],nuno:["Ткань","🧵"],kami:["Бумага васи","📜",1],ito:["Нитки","🧶",1],enogu:["Краски","🎨",1]};
const WS_MK=Object.keys(WS_M);
// unlock milestones: key → [test, «откроется …»]
const WS_U={start:[()=>true,""],harvest:[c=>c.f.harvest,"после первого урожая на огороде"],fish:[c=>c.f.fish,"после первой рыбалки"],
  forest:[c=>c.f.forest,"после первого шага в лес за тории"],guest:[c=>c.f.guest,"когда к воротам придёт гость"],water:[c=>c.f.water,"когда польёшь огород"],
  feather:[c=>c.f.feather,"когда найдётся первое перо"],c3:[c=>c.n>=3,"после трёх поделок"],c5:[c=>c.n>=5,"после пяти поделок"],
  c8:[c=>c.n>=8,"после восьми поделок"],c12:[c=>c.n>=12,"после двенадцати поделок"]};
// recipes: id, name, materials, unlock, a short line
const WS_RC=[
 {id:"ws_kaeru",n:"Оригами-лягушка",m:{kami:1},u:"start",d:"Каэру — «вернуться»: лягушка из бумаги, чтобы всё возвращалось домой."},
 {id:"ws_chochin",n:"Бумажный фонарик",m:{kami:2,eda:2,enogu:1},u:"start",d:"Каркас из веточек, васи и Мусин след сбоку."},
 {id:"ws_teru",n:"Тэру-тэру-бодзу",m:{nuno:1,ito:1},u:"start",d:"Тряпичная куколка у окна просит завтра солнца."},
 {id:"ws_uma",n:"Соломенная лошадка",m:{wara:4,ito:1},u:"harvest",d:"Вара-ума: из соломы с огорода, перевязана красной нитью."},
 {id:"ws_wreath",n:"Венок из листьев",m:{ha:5,eda:1},u:"harvest",d:"Кленовые и травяные листья на гибкой ветке."},
 {id:"ws_shells",n:"Колокольчик из ракушек",m:{kai:3,uroko:1,ito:1},u:"fish",d:"Ракушки на нитке звенят, как вода у берега."},
 {id:"ws_frame",n:"Рамка из веточек",m:{eda:4,koke:1,ha:1,kami:1},u:"forest",d:"Лесной кленовый лист под васи, внизу — мох."},
 {id:"ws_kendama",n:"Кэндама из жёлудя",m:{eda:2,donguri:1,ito:1},u:"forest",d:"Вместо шарика — большой жёлудь. Муся ловит его лапой."},
 {id:"ws_omamori",n:"Омамори из лоскутков",m:{nuno:2,ito:1,enogu:1},u:"guest",d:"Сшит из обрезков гостевых платков, на нём 猫."},
 {id:"ws_kokeshi",n:"Кокэси с ушками",m:{eda:3,enogu:1},u:"c3",d:"Деревянная куколка, похожая на одну знакомую кошку."},
 {id:"ws_sensu",n:"Веер с Мусей",m:{kami:2,eda:2,enogu:1},u:"c3",d:"На бумаге — Муся смотрит на луну."},
 {id:"ws_furin",n:"Глиняный фурин",m:{tsuchi:3,ito:1,kami:1,enogu:1},u:"water",d:"Глина с огорода, обожжённая в очаге. Звенит глухо и тепло."},
 {id:"ws_kinchaku",n:"Мешочек-кинтяку",m:{nuno:3,ito:1},u:"c5",d:"Для сокровищ: пуговицы, сушёная рыбка, блестящий камушек."},
 {id:"ws_mizuhiki",n:"Узел мидзухики",m:{ito:1,kami:1,hane:1},u:"feather",d:"Узел аваҗи-мусуби на удачу, с пёрышком."},
 {id:"ws_hokora",n:"Маленький алтарь",m:{eda:4,koke:2,tsuchi:1,kami:1},u:"c8",d:"Крошечное святилище с мхом на крыше — для доброго ками дома."},
 {id:"ws_hotaru",n:"Светлячковый фонарь",m:{eda:3,uroko:2,kami:1},u:"c12",d:"Чешуйки внутри ловят свет и мерцают, как светлячки."}];
WS_RC.find(r=>r.id==="ws_mizuhiki").d="Узел авадзи-мусуби на удачу, с пёрышком.";
const WS_CAT="Сделано своими лапами";
addItems(WS_RC.map(r=>{const a=WS_R[r.id];const it={id:r.id,n:r.n,c:WS_CAT,w:a[2],h:a[3],a:a[4],p:60,at:["ws",a[0],a[1]],src:"🛠 мастерская",hint:"Это делают в мастерской — 🛠 у верстака"};
  if(r.id==="ws_chochin")it.glow=[48,94];if(r.id==="ws_hotaru")it.glow=[56,100];return it;}),{ws:[WS_AW,WS_AH]});
STAMPS.push(["ws_first","工","Первая поделка","Сделай что-нибудь в мастерской"],["ws_eight","匠","Умелые лапки","Сделай 8 вещей в мастерской"],["ws_all","職","Мастер на все лапы","Сделай все 16 вещей мастерской"]);

let WS_IM=null;ldImg("assets/items/atlas_ws.webp",im=>{WS_IM=im;});
function wsS(){const c=S.ext.craft||(S.ext.craft={mat:{},made:{},n:0,kn:[],nw:[],f:{},seen:0,last:null});for(const k of ["mat","made","f"])c[k]=c[k]||{};c.kn=c.kn||[];c.nw=c.nw||[];return c;}
const wsHave=k=>WS_M[k][2]?Infinity:(wsS().mat[k]||0);
const wsOpenR=r=>!!WS_U[r.u][0](wsS());
const wsCan=r=>Object.entries(r.m).every(([k,n])=>wsHave(k)>=n);
const wsMade=id=>!!wsS().made[id];
const wsReady=()=>WS_RC.filter(r=>wsOpenR(r)&&!wsMade(r.id)&&wsCan(r));
function wsRoom(){const o=(S.ext.rooms&&S.ext.rooms.open)||{};return ROOMX.attic&&o.attic?"attic":ROOMX.kura&&o.kura?"kura":"games";}
const WS_WHERE={attic:"на чердаке",kura:"в куре, у бочек",games:"в комнате игр, у тории"};
const wsWaits=()=>{const c=wsS();return !c.seen||c.nw.length>0;};

// ── notes: one short toast; while a full-screen game/panel is open they wait and come as one summary line ──
let wsPG={},wsPB=[],wsAt=0;
function wsGain(o){const c=wsS();for(const [k,n] of Object.entries(o)){if(!n)continue;c.mat[k]=(c.mat[k]||0)+n;wsPG[k]=(wsPG[k]||0)+n;if(k==="hane")c.f.feather=1;if(k==="tsuchi")c.f.water=1;}
  wsUnlock();save();wsAt=Date.now()+2200;if(panelIs("ws"))wsRender();}
function wsUnlock(){const c=wsS();for(const r of WS_RC)if(!c.kn.includes(r.id)&&wsOpenR(r)){c.kn.push(r.id);if(r.u!=="start"){c.nw.push(r.id);wsPB.push(r.n);}}}
function wsFlush(){const c=wsS(),g=Object.entries(wsPG);wsPG={};const b=wsPB;wsPB=[];if(!c.seen)return;   // before the bench is found: quiet (the 家 dot tells)
  let d=0;if(g.length){let s="🛠 "+g.map(([k,n])=>`${WS_M[k][0]} +${n}`).join(" · ");if(s.length>44)s="🛠 Материалы для мастерской: +"+g.reduce((a,[,n])=>a+n,0);toast(s);d=2200;}
  if(b.length)setTimeout(()=>wsBpToast(b),d);}
function wsBpToast(b){toast(b.length>1?`📐 Новые чертежи в мастерской: ${b.length}`:`📐 Новый чертёж: ${b[0]}`);chime([784,1046]);}

// ── where materials come from ──
const wsP=p=>Math.random()<p?1:0;
hook("ev",(ev,d)=>{const c=wsS();
  if(ev==="harvest"){c.f.harvest=1;wsGain({wara:2,ha:1+wsP(.5),eda:wsP(.3)});}
  else if(ev==="fish"){const f=FISHES.find(x=>x.id===(d&&d.id));c.f.fish=1;wsGain(f&&f.junk?{kai:2}:{uroko:1,kai:wsP(.45)});}
  else if(ev==="water"){const dk=dayKey();if(c.wd!==dk){c.wd=dk;c.wn=0;}if(c.wn<3){c.wn++;wsGain({tsuchi:1});}else{c.f.water=1;}}
  else if(ev==="guest"){c.f.guest=1;wsGain({nuno:1,hane:wsP(.25)});}
  else if(ev==="cook"&&Math.random()<.25)wsGain({wara:1});});
hook("disc",(kind,id)=>{if(kind==="ema")wsGain({nuno:1});else if(kind==="visitor"||kind==="rareguest")wsGain({hane:1});else if(kind==="forest"&&!/^fo_/.test(id))wsGain({hane:wsP(.5),koke:1});});
function wsForest(){const f=S.ext.forest,c=wsS();if(!f)return;const n=f.n||0;if(c.fn==null){c.fn=n;return;}if(n<=c.fn)return;const d=Math.min(10,n-c.fn);c.fn=n;c.f.forest=1;
  const o={eda:0,koke:0,donguri:0,hane:0};for(let i=0;i<d;i++){o.eda++;o.koke+=wsP(.5);o.donguri+=wsP(.45);o.hane+=wsP(.12);}wsGain(o);}
hook("sec",()=>{wsForest();if((Object.keys(wsPG).length||wsPB.length)&&Date.now()>=wsAt&&(!overlaysOpen()||panelIs("ws")))wsFlush();});
hook("boot",()=>{const c=wsS();   // milestones the player already passed before the workshop existed
  if(ST.got.includes("garden1"))c.f.harvest=1;if(Object.keys(S.catch||{}).length)c.f.fish=1;if(S.ext.forest&&S.ext.forest.n)c.f.forest=1;if(Object.keys(S.friends||{}).length)c.f.guest=1;
  if(c.fn==null&&S.ext.forest)c.fn=S.ext.forest.n||0;if(!c.seen)c.kn=[];wsUnlock();if(!c.seen)c.nw=[];});

// ── the bench in the room (attic → kura → games room) ──
const WS_POS={attic:[1180,1150],kura:[690,1150],games:[1440,1160]},WS_BW=370;
function wsBench(){const r=wsRoom();if(S.room!==r||!WS_IM)return null;const p=WS_POS[r];return{x:visX(p[0],WS_BW/2+30),y:p[1]};}
function wsQuad(b){const [x0,y0]=imgToStage(b.x-WS_BW/2,b.y,CAT_D),[x1]=imgToStage(b.x+WS_BW/2,b.y,CAT_D),w=x1-x0,h=w*250/420;return{x:x0,y:y0-h+h*.024,w,h};}
function wsBlit(g,key,cx,by,hh,al=1,sc=1){const a=WS_R[key];if(!a||!WS_IM)return;const k=Math.min(hh/a[3],hh*1.25/a[2])*sc,w=a[2]*k,h=a[3]*k;g.globalAlpha=al;g.drawImage(WS_IM,a[0],a[1],a[2],a[3],cx-w/2,by-h,w,h);g.globalAlpha=1;}
hook("draw",(t,front)=>{if(scene.on)return;const b=wsBench();if(!b||front!==(b.y>catLineY()+6))return;const q=wsQuad(b),a=WS_R.bench;
  ctx.drawImage(WS_IM,a[0],a[1],a[2],a[3],q.x,q.y,q.w,q.h);const c=wsS(),k=q.w/420;
  if(c.last)wsBlit(ctx,c.last,q.x+212*k,q.y+108*k,78*k);
  if(wsWaits()){const al=.45+.35*Math.sin(t*2.6);drawEmoji(ctx,"✨",q.x+q.w*.5,q.y+q.h*.12-6*Math.sin(t*1.3)*k,18*view.s,Math.max(0,al));}});
hook("hit",(x,y)=>{if(scene.on)return;const b=wsBench();if(!b)return;const q=wsQuad(b);if(x<q.x||x>q.x+q.w||y<q.y+q.h*.2||y>q.y+q.h)return;
  audioInit();tone(520,.06,"triangle",.05);if(!petAway())react("😺",1.4);wsOpen();return true;});
hook("tray",(tray,room)=>{if(room!==wsRoom()||(S.trayMode[room]||"play")!=="play"||tray.querySelector('[data-x="ws:open"]'))return;
  const b=`<button class="item wide" data-x="ws:open"><span class="ico">🛠</span><span class="nm">Мастерская</span></button>`,row=tray.querySelector(".items");
  if(row)row.insertAdjacentHTML("afterbegin",b);else tray.querySelector(".glist")?.insertAdjacentHTML("beforebegin",`<div class="items">${b}</div>`);});
hook("hubDot",wsWaits);
hook("tabDot",r=>r===wsRoom()&&wsWaits());
hook("hub",()=>{const c=wsS(),R=wsReady(),nw=c.nw.map(id=>IT[id].n);
  const body=!c.seen?`Муся нашла ${WS_WHERE[wsRoom()]} старый низкий верстак с инструментами. Под ним стоит ящик с обрезками…`
    :`Верстак стоит ${WS_WHERE[wsRoom()]}. Сделано ${c.n} из ${WS_RC.length}.${R.length?` Можно смастерить: ${R.slice(0,2).map(r=>r.n.toLowerCase()).join(", ")}${R.length>2?" и ещё "+(R.length-2):""}.`:""}${nw.length?` Новый чертёж: ${nw.join(", ")}.`:""}`;
  return`<div class="hubc"><h4>🛠 Мастерская <i>工房</i></h4><p>${body}</p><div class="row"><button class="btn" data-x="ws:open">Открыть мастерскую</button></div></div>`;});

// ── the panel: a little scene (canvas) + materials + blueprints ──
const wsIc=(k,s)=>{const a=WS_R["m_"+k],z=s/64;return`<span class="ws-ic" style="width:${s}px;height:${s}px;background-size:${WS_AW*z}px ${WS_AH*z}px;background-position:-${a[0]*z}px -${a[1]*z}px"></span>`;};
let wsFresh=[],wsFirst=false;
function wsCard(r){const c=wsS(),open=c.kn.includes(r.id),made=wsMade(r.id),can=wsCan(r);
  if(!open)return`<div class="ws-r lock"><span class="ws-th">${itemThumb(IT[r.id],56,60)}</span><div class="ws-tx"><b>???</b><small>Чертёж откроется ${WS_U[r.u][1]}.</small></div></div>`;
  const cost=Object.entries(r.m).map(([k,n])=>{const h=wsHave(k);return`<span class="ws-c${h<n?" no":""}">${wsIc(k,22)}${WS_M[k][2]?"":`${Math.min(h,n)}/${n}`}${WS_M[k][2]?"∞":""}</span>`;}).join("");
  return`<div class="ws-r${made?" done":""}"><span class="ws-th">${itemThumb(IT[r.id],56,60)}</span><div class="ws-tx"><b>${r.n}${wsFresh.includes(r.id)?'<span class="ws-new">новый чертёж</span>':""}</b><small>${r.d}</small>${made?"":`<div class="ws-cost">${cost}</div>`}</div>`+
    (made?`<span class="ws-ok">✓ сделано</span>`:`<button class="btn${can?" primary":""}" data-x="ws:make:${r.id}"${can&&!wsA?"":" disabled"}>Сделать</button>`)+`</div>`;}
function wsRender(){const c=wsS(),R=WS_RC,ord=[...R.filter(r=>c.kn.includes(r.id)&&!wsMade(r.id)),...R.filter(r=>wsMade(r.id)),...R.filter(r=>!c.kn.includes(r.id))];
  const mats=WS_MK.map(k=>{const n=wsHave(k);return`<span class="ws-m${n?"":" z"}">${wsIc(k,30)}<span>${WS_M[k][0]} <b>${n===Infinity?"∞":n}</b></span></span>`;}).join("");
  const lead=wsFirst?"Под верстаком нашёлся ящик с обрезками — на первые поделки хватит. Бумага, нитки и краски не кончаются никогда."
    :`Сделано ${c.n} из ${R.length}. Материалы приносит сама жизнь в доме: урожай, рыбалка, полив, гости, прогулки в лес.`;
  openPanel("🛠 Мастерская 工房",`<canvas id="wsCv" class="ws-cv" width="720" height="380"></canvas><p class="lead">${lead}</p>
    <h3 class="bh">Материалы</h3><div class="ws-mats">${mats}</div><h3 class="bh">Чертежи</h3><div class="ws-list">${ord.map(wsCard).join("")}</div>`,"ws");wsKick();}
function wsOpen(){const c=wsS();wsFirst=!c.seen;
  if(!c.seen){c.seen=1;const f=c.f,o={eda:3+(f.forest?3:0),nuno:1+(f.guest?2:0),wara:1+(f.harvest?3:0),ha:2+(f.harvest?3:0),kai:f.fish?3:0,uroko:f.fish?1:0,koke:f.forest?1:0,donguri:f.forest?1:0};
    for(const [k,n] of Object.entries(o))if(n)c.mat[k]=(c.mat[k]||0)+n;c.kn=[];wsUnlock();c.nw=[];wsPG={};wsPB=[];}
  wsFresh=c.nw.slice();c.nw=[];save();hubDot();tabDots();const was=panelIs("ws");wsRender();if(!was)$("xpBody").scrollTop=0;}

// ── crafting: materials fly to the bench, Musya paws at it, taps of the tools, then the thing appears ──
let wsA=null,wsLoop=false;const wsT=()=>performance.now()/1000,WS_DUR=4.2,WS_REV=3.1;
function wsMake(id){const r=WS_RC.find(x=>x.id===id),c=wsS();if(!r||wsA||wsMade(id)||!c.kn.includes(id)||!wsCan(r))return;
  for(const [k,n] of Object.entries(r.m))if(!WS_M[k][2])c.mat[k]-=n;
  c.made[id]=Date.now();c.n=Object.keys(c.made).length;c.last=id;S.owned.add(id);loadItem(id);disc("craft",id);
  S.needs.joy=clamp(S.needs.joy+6,0,100);wsUnlock();wsFresh=c.nw.slice();c.nw=[];save();ui();hubDot();
  wsA={id,t0:wsT(),mats:Object.keys(r.m)};wsSound(wsA.mats.length);wsRender();
  setTimeout(()=>toast(`✨ ${r.n} — в «🧺 Вещи»`),WS_REV*1000+300);
  setTimeout(()=>{wsA=null;if(panelIs("ws"))wsRender();const n=c.n;if(n>=1)award("ws_first");if(n>=8)setTimeout(()=>award("ws_eight"),2200);if(n>=WS_RC.length)setTimeout(()=>award("ws_all"),4400);
    if(wsPB.length){const b=wsPB;wsPB=[];setTimeout(()=>wsBpToast(b),n===1?2200:600);}},WS_DUR*1000+400);}
function wsSound(n){for(let i=0;i<n;i++)setTimeout(()=>tone(660+i*110,.08,"sine",.04),(.25+i*.2)*1000+380);
  [1.1,1.42,1.74,2.06,2.38,2.7].forEach((s,i)=>setTimeout(()=>{tone(i%2?880:620,.05,"triangle",.05);if(i%3===2)tone(1400,.03,"square",.012);},s*1000));
  setTimeout(()=>chime([1046,1318,1568,2093]),WS_REV*1000);}
function wsKick(){if(wsLoop)return;wsLoop=true;requestAnimationFrame(function f(){if(!panelIs("ws")){wsLoop=false;return;}try{wsDraw();}catch(e){console.error(e);}requestAnimationFrame(f);});}
let wsBg=null;
function wsBack(){if(wsBg)return wsBg;const c=document.createElement("canvas");c.width=720;c.height=380;const g=c.getContext("2d"),r=rng(31);
  let gr=g.createLinearGradient(0,0,0,380);gr.addColorStop(0,"#21170f");gr.addColorStop(1,"#0d0906");g.fillStyle=gr;g.fillRect(0,0,720,380);
  for(let x=0;x<720;x+=58){g.fillStyle=`rgba(${40+r()*20|0},${28+r()*12|0},${18+r()*8|0},.55)`;g.fillRect(x,0,56,300);g.fillStyle="rgba(0,0,0,.45)";g.fillRect(x+56,0,2,300);
    for(let i=0;i<6;i++){g.fillStyle="rgba(0,0,0,.12)";g.fillRect(x+r()*50,0,1,300);}}
  g.fillStyle="#1a120c";g.fillRect(0,286,720,94);g.fillStyle="rgba(120,90,60,.18)";g.fillRect(0,286,720,2);
  gr=g.createRadialGradient(110,60,4,110,60,330);gr.addColorStop(0,"rgba(255,190,110,.42)");gr.addColorStop(.35,"rgba(240,160,90,.14)");gr.addColorStop(1,"rgba(240,160,90,0)");g.fillStyle=gr;g.fillRect(0,0,720,380);
  gr=g.createRadialGradient(360,200,120,360,200,470);gr.addColorStop(0,"rgba(0,0,0,0)");gr.addColorStop(1,"rgba(0,0,0,.6)");g.fillStyle=gr;g.fillRect(0,0,720,380);
  return wsBg=c;}
const wsBack2=(e)=>1+2.70158*Math.pow(e-1,3)+1.70158*Math.pow(e-1,2);   // ease-out-back
function wsDraw(){const cv=document.getElementById("wsCv");if(!cv||!WS_IM)return;const g=cv.getContext("2d"),T=wsT(),A=wsA,e=A?T-A.t0:99,c=wsS();
  g.drawImage(wsBack(),0,0);
  const fl=.85+.1*Math.sin(T*6.1)+.05*Math.sin(T*13);g.save();g.globalCompositeOperation="lighter";const lg=g.createRadialGradient(110,60,2,110,60,90);lg.addColorStop(0,`rgba(255,200,120,${.35*fl})`);lg.addColorStop(1,"rgba(255,200,120,0)");g.fillStyle=lg;g.fillRect(0,0,240,180);g.restore();
  const K=1.3,bx=87,by=380-250*K,top=by+104*K,cx=bx+168*K;
  // Musya behind the bench: purrs while waiting, paws at the work while crafting, high-fives the result
  if(!petAway()){let st="purr",f=Math.floor(T*1.6)%8;if(A&&e<WS_REV){st="play";f=Math.floor(e*9)%8;}else if(A&&e<WS_DUR){st="highfive";f=Math.min(7,Math.floor((e-WS_REV)*8));}
    drawCatG(g,st,f,478,326,1.45);}
  const a=WS_R.bench;g.drawImage(WS_IM,a[0],a[1],a[2],a[3],bx,by,420*K,250*K);
  if(!A){if(c.last)wsBlit(g,c.last,cx,top+6,118);else textC(g,"Выбери чертёж ниже",360,40,17,"rgba(232,226,212,.7)",600);return;}
  // materials fly in from below
  A.mats.forEach((k,i)=>{const s0=.25+i*.2,u=clamp((e-s0)/.7,0,1);if(u<=0||u>=1)return;const x0=170+i*120,y0=400,x=x0+(cx-x0)*u,y=y0+(top-40-y0)*u-Math.sin(u*Math.PI)*110,r=WS_R["m_"+k],s=64*(1-.5*u);
    g.globalAlpha=1-u*u*.6;g.drawImage(WS_IM,r[0],r[1],64,64,x-s/2,y-s/2,s,s);g.globalAlpha=1;});
  // the work: a whirl of shavings and paper bits over the bench, small sparks
  if(e>.9&&e<WS_REV+.15){const w=clamp(Math.min((e-.9)/.4,(WS_REV+.15-e)/.3),0,1);
    for(let i=0;i<22;i++){const an=e*(2.2+i%4*.6)+i*2.39,rr=26+(i*13)%50,x=cx+Math.cos(an)*rr*1.5,y=top-34+Math.sin(an)*rr*.45-(i%5)*6;
      g.fillStyle=["rgba(232,214,170,","rgba(214,180,130,","rgba(239,230,212,","rgba(200,60,48,"][i%4]+(.85*w)+")";g.save();g.translate(x,y);g.rotate(an*2);g.fillRect(-4,-1.6,8,3.2);g.restore();}
    if(Math.floor(e*4)%2===0)drawEmoji(g,"✨",cx+Math.sin(e*7)*60,top-60-Math.cos(e*5)*20,20,w);}
  // the reveal
  if(e>=WS_REV){const u=clamp((e-WS_REV)/.55,0,1),fl2=clamp(1-(e-WS_REV)/.6,0,1);
    if(fl2>0){const gg=g.createRadialGradient(cx,top-50,4,cx,top-50,190);gg.addColorStop(0,`rgba(255,236,190,${.85*fl2})`);gg.addColorStop(1,"rgba(255,236,190,0)");g.fillStyle=gg;g.fillRect(cx-200,top-250,400,400);}
    wsBlit(g,A.id,cx,top+6,118,1,Math.max(.01,wsBack2(u)));
    for(let i=0;i<8;i++){const an=i/8*Math.PI*2+e,rr=60+u*40;drawEmoji(g,i%2?"✨":"✦",cx+Math.cos(an)*rr,top-58+Math.sin(an)*rr*.6,14+6*(i%2),clamp(1.4-(e-WS_REV)/.8,0,1));}
    textC(g,"Готово: "+IT[A.id].n,360,36,20,`rgba(242,214,160,${clamp((e-WS_REV)*3,0,1)})`,700);}}

hook("click",(k)=>{if(!k.startsWith("ws:"))return;const [,a,id]=k.split(":");if(a==="open")wsOpen();else if(a==="make")wsMake(id);return true;});
hook("panelClose",id=>{if(id==="ws"){wsFresh=[];wsFirst=false;}});
// reactions to the made things standing in rooms
hook("itemTap",(it,I,t)=>{const id=it.id;if(!/^ws_/.test(id))return;const away=petAway();
  if(id==="ws_kaeru"){tone(180,.09,"square",.03);setTimeout(()=>tone(150,.12,"square",.03),130);if(!away)react("🐸",1.4);return true;}
  if(/furin|shells|mizuhiki/.test(id)){const b=pick([1568,1760,2093]);[0,1,2].forEach(i=>setTimeout(()=>tone(b*pick([1,1.26,1.5]),1.4,"sine",.02),i*160));fxAt(it,["🎐","✨"],2);return true;}
  if(id==="ws_teru"){if(!away)react(weather.on?"🌧":"☀️",1.6);fxAt(it,["☀️"],1);return true;}
  if(/kendama|uma|kinchaku/.test(id)&&!away){walkTo(it,"poke","😸");return true;}
  if(id==="ws_hokora"){chime([659,880]);if(!away)react("🙏",1.4);fxAt(it,["✨"],2);return true;}
  fxAt(it,["✨"],2);tone(700,.12,"sine",.03);if(!away)react("😺",1.2);return true;});

document.head.insertAdjacentHTML("beforeend",`<style>.ws-cv{width:100%;height:auto;aspect-ratio:720/380;display:block;border-radius:12px;margin:2px 0 10px;background:#0d0a08;box-shadow:0 0 0 1px var(--line)}
.ws-mats{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 14px}.ws-m{display:inline-flex;align-items:center;gap:4px;padding:2px 10px 2px 3px;border-radius:999px;border:1px solid var(--line);font-size:13px;color:var(--muted)}.ws-m b{color:var(--paper)}.ws-m.z{opacity:.42}
.ws-ic{display:inline-block;background:url(assets/items/atlas_ws.webp) no-repeat;flex:none}
.ws-list{display:flex;flex-direction:column;gap:8px;margin-bottom:14px}.ws-r{display:flex;align-items:center;gap:10px;border:1px solid var(--line);border-radius:12px;padding:8px 10px;background:var(--ink-2)}
.ws-th{width:58px;height:62px;display:grid;place-items:center;flex:none}.ws-r.lock .ws-th>*{filter:brightness(0);opacity:.5}.ws-r.lock{opacity:.75}.ws-r.done{opacity:.8}
.ws-tx{flex:1;min-width:0}.ws-tx b{display:block;font-size:15px;color:var(--paper)}.ws-tx small{display:block;font-size:12px;color:var(--muted);margin:1px 0 5px;line-height:1.3}
.ws-cost{display:flex;flex-wrap:wrap;gap:4px}.ws-c{display:inline-flex;align-items:center;gap:2px;font-size:12px;padding:1px 7px 1px 1px;border-radius:999px;border:1px solid var(--line);color:var(--paper)}.ws-c.no{border-color:rgba(194,106,90,.75);color:#e09a8a}
.ws-r .btn{flex:none}.ws-new{display:inline-block;color:var(--sakura);font-size:11px;font-weight:600;margin-left:6px}.ws-ok{flex:none;color:var(--sakura);font-size:13px}</style>`);
X.ws={S:wsS,gain:wsGain,make:wsMake,open:wsOpen,room:wsRoom,ready:wsReady,flush:wsFlush,
  tap(){const b=wsBench();if(!b)return false;const q=wsQuad(b);return !!hk("hit",q.x+q.w/2,q.y+q.h*.7);}};
}
