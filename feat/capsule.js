{
// ───────────────────────── «Капсула времени»: a letter to the future, sealed in a kiri box ─────────────────────────
// The player writes a letter (≤800 chars) to her future self and picks when it opens: in a month, half a year or a year
// (calendar dates from today(), so ?date= works). Optionally a snapshot goes in too: trust, days together, candles, the
// kitten, Musya's favourite room, her outfit, the number of things. Sealing plays a short scene in the panel: the letter
// folds into a kiri box, the lid shuts, Musya pats it, the box leaves for a small shelf high on the kura wall (buried in
// the courtyard while the kura is closed). Up to 3 wait at once; the hub shows the countdown, the letter stays unreadable.
// On the day: a dot on 家 and on the room tab, one toast, «Открыть» in the hub → the letter, «тогда → сейчас», a narrator.
// Art: art/capsule_art.py → assets/items/atlas_tc.webp (closed / opened / empty box, tied letters, the wall shelf).
// State: S.ext.capsule = {list:[{id,t,made,open,sp,f,w,op}], rt:{room:sec}, draft, sp, f, told, n}
const TC_AT={"box":[424,0,180,140],"open":[0,0,210,160],"empty":[212,0,210,160],"letters":[0,162,180,116],"shelf":[182,162,240,64]},TC_AW=[606,278];
const TC=S.ext.capsule||(S.ext.capsule={list:[],rt:{},draft:"",sp:"m",f:1,told:"",n:0});TC.list=TC.list||[];TC.rt=TC.rt||{};
const TC_C="Капсула времени";
addItems([
 {id:"tc_box",n:"Шкатулка из павловнии",c:TC_C,w:180,h:140,a:"b",p:0,at:["tc",424,0],src:"📦 капсула",hint:"Запечатай капсулу времени: «家 Дом» → Капсула времени"},
 {id:"tc_open",n:"Открытая шкатулка с письмом",c:TC_C,w:210,h:160,a:"b",p:0,at:["tc",0,0],src:"📦 капсула",hint:"Открой капсулу времени, когда придёт её день"},
 {id:"tc_letters",n:"Перевязанные письма",c:TC_C,w:180,h:116,a:"b",p:0,at:["tc",0,162],src:"📦 капсула",hint:"Запечатай три капсулы времени"}],{tc:TC_AW});
STAMPS.push(["tc_s1","封","Письмо в будущее","Запечатай первую капсулу времени"],["tc_o1","開","Привет из прошлого","Открой капсулу времени"],["tc_y1","年","Год спустя","Открой капсулу, которая пролежала год"]);

// ── dates
const TC_SP={m:[1,"месяц","Через месяц"],h:[6,"полгода","Через полгода"],y:[12,"год","Через год"]};
const tcD=k=>new Date(k+"T12:00:00"),tcDiff=(a,b)=>Math.round((tcD(b)-tcD(a))/864e5),tcDays=k=>tcDiff(dayKey(),k);
function tcAdd(k,mo){const d=tcD(k),day=d.getDate();d.setDate(1);d.setMonth(d.getMonth()+mo);d.setDate(Math.min(day,new Date(d.getFullYear(),d.getMonth()+1,0).getDate()));return dayKey(d);}
function tcDate(k,yr){const d=tcD(k);return d.getDate()+" "+MON_G[d.getMonth()]+(yr||d.getFullYear()!==today().getFullYear()?" "+d.getFullYear():"");}
function tcIn(k){const n=tcDays(k);return n<=0?"сегодня":n===1?"завтра":"через "+daysWord(n);}
const tcWait=()=>TC.list.filter(c=>!c.op).sort((a,b)=>a.open<b.open?-1:1),tcReady=c=>!c.op&&dayKey()>=c.open;
const tcPl=(n,f)=>{const a=n%10,b=n%100;return n+" "+(a===1&&b!==11?f[0]:a>=2&&a<=4&&(b<12||b>14)?f[1]:f[2]);};
let tcTestW=null;
const tcWhere=()=>tcTestW||(ROOMX.kura&&S.ext.rooms&&S.ext.rooms.open&&S.ext.rooms.open.kura?"kura":"courtyard");

// ── the snapshot «как всё сейчас» and its comparison with now
const tcRN=id=>"«"+((ROOMS.find(r=>r.id===id)||{}).ru||id)+"»";
const tcTN=l=>X.ts?X.ts.name(l):"уровень "+l;
function tcFav(){let b=null,v=0;for(const k in TC.rt)if(TC.rt[k]>v&&ROOMS.some(r=>r.id===k)){b=k;v=TC.rt[k];}return b||S.room;}
function tcWear(){return Object.keys(S.wear).map(sl=>S.wear[sl]&&WEAR[sl]&&(WEAR[sl].find(w=>w.id===S.wear[sl])||{}).n).filter(Boolean);}
function tcFacts(){const f={room:tcFav(),wear:tcWear(),own:S.owned.size},T=S.ext.trust,B=S.ext.bd,P=S.ext.pet2;
  if(T&&T.lv)f.tr=T.lv;if(B&&B.start)f.days=Math.max(0,tcDiff(B.start,dayKey()));if(X.cd)f.cd=X.cd.n();if(P&&P.name)f.pet=P.name;return f;}
function tcFactLine(f){const L=[];if(f.tr)L.push(`доверие «${tcTN(f.tr)}»`);if(f.days!=null)L.push(f.days?daysWord(f.days)+" вместе":"первый день вместе");
  if(f.cd!=null)L.push(tcPl(f.cd,["свеча","свечи","свечей"])+" из 100");L.push(f.pet?"котёнок "+f.pet:"котёнка пока нет");L.push("любимая комната — "+tcRN(f.room));
  L.push(f.wear.length?"наряд: "+f.wear.join(", "):"без нарядов");L.push(tcPl(f.own,["вещь","вещи","вещей"])+" в доме");return L.join(", ");}
function tcCmp(f){const n=tcFacts(),L=[],B=s=>`<b>${s}</b>`;
  if(f.tr&&n.tr)L.push(f.tr===n.tr?`Доверие Муси: «${tcTN(f.tr)}» — как и тогда`:`Доверие: тогда «${tcTN(f.tr)}» → сейчас ${B("«"+tcTN(n.tr)+"»")}`);
  const dw=d=>d?daysWord(d):"первый день";if(f.days!=null&&n.days!=null)L.push(`Вместе: тогда ${dw(f.days)} → сейчас ${B(dw(n.days))}`);
  if(f.cd!=null&&n.cd!=null)L.push(f.cd===n.cd?`Свечей: ${f.cd} из 100 — столько же, сколько тогда`:`Свечей: тогда ${f.cd} из 100 → сейчас ${B(n.cd)}`);
  if(f.pet||n.pet)L.push(f.pet?(n.pet?`Тогда в доме жил котёнок ${f.pet} — ${n.pet===f.pet?"он и сейчас рядом":"а теперь ещё и "+n.pet}`:`Тогда в доме жил котёнок ${f.pet}`):`Тогда котёнка ещё не было → сейчас с вами живёт ${B(n.pet)}`);
  L.push(f.room===n.room?`Любимая комната Муси — ${tcRN(f.room)}, как и тогда`:`Любимая комната: тогда ${tcRN(f.room)} → сейчас ${B(tcRN(n.room))}`);
  const w=a=>a.length?a.join(", "):"без нарядов";L.push(w(f.wear)===w(n.wear)?`Наряд тот же: ${w(n.wear)}`:`Наряд: тогда ${w(f.wear)} → сейчас ${B(w(n.wear))}`);
  L.push(f.own===n.own?`Вещей в доме: ${f.own}, как и тогда`:`Вещей в доме: тогда ${f.own} → сейчас ${B(n.own)}`);return L;}
const TC_NAR={
 m:["Всего месяц — а будто целая луна прошла над крышей. Муся обнюхивает листок: пахнет павловнией и немного тем вечером.",
    "Месяц письмо ждало своего дня. Муся смотрит на старые строчки так, словно помнит тот вечер лучше тебя."],
 h:["Полгода. Сменились времена года, Муся подросла, а письмо всё ждало — терпеливо, как умеют ждать только вещи из павловнии.",
    "Полгода назад эти строчки писались для сегодняшнего дня. Муся трогает бумагу лапой, будто здоровается с тем вечером."],
 y:["Целый год. Тот же дом, та же луна над двором — и всё-таки всё по-другому. Муся мурлычет так громко, будто тоже всё помнит.",
    "Год прошёл по дому — от снега до светлячков и обратно. Письмо дождалось, и Муся по-прежнему рядом. Это главное."]};
const tcNar=c=>{const a=TC_NAR[c.sp]||TC_NAR.m;return a[(parseInt(c.id.slice(1))||0)%a.length];};

// ── panels: writing, the sealing scene, reading, the list of opened letters
function tcWrite(msg){const W=tcWait();
  if(W.length>=3){openPanel("Капсула времени",`<p class="lead">На полке уже три шкатулки — больше не поместится. Новое письмо можно будет запечатать, когда откроется ближайшая: ${tcDate(W[0].open,1)}.</p><div class="row"><button class="btn" data-x="tc:hub">К дому</button></div>`,"tc");return;}
  const sp=TC.sp||"m",k=dayKey(),d=TC.draft||"";
  openPanel("Капсула времени",`<p class="lead">Напиши письмо себе в будущее. Пока не придёт срок, его не прочитать — даже тебе.</p>
   <div class="tc-paper"><textarea id="tcTxt" maxlength="800" placeholder="Привет из прошлого! Сегодня Муся…">${esc(d)}</textarea><small id="tcCnt">${d.length} / 800</small></div>
   <h4 class="tc-h">Когда открыть</h4><div class="tc-sp">${Object.keys(TC_SP).map(s=>`<button class="tc-o ${s===sp?"on":""}" data-x="tc:sp:${s}"><b>${TC_SP[s][2]}</b><small>${tcDate(tcAdd(k,TC_SP[s][0]),1)}</small></button>`).join("")}</div>
   <button class="tc-f ${TC.f?"on":""}" data-x="tc:f"><span>${TC.f?"☑":"☐"}</span><div><b>Положить в капсулу, как всё сейчас</b><small>${tcFactLine(tcFacts())}</small></div></button>
   ${msg?`<p class="tc-msg">${msg}</p>`:""}<div class="row"><button class="btn primary" data-x="tc:seal">🔒 Запечатать</button></div>`,"tc");}
$("xpBody").addEventListener("input",ev=>{if(ev.target.id!=="tcTxt")return;TC.draft=ev.target.value.slice(0,800);const c=$("tcCnt");if(c)c.textContent=TC.draft.length+" / 800";});
function tcSeal(){const v=(TC.draft||"").trim();if(!v){tcWrite("Сначала напиши хотя бы пару строк — шкатулке нечего хранить.");return;}if(tcWait().length>=3){tcWrite();return;}
  const k=dayKey(),sp=TC.sp||"m";TC.n=(TC.n||0)+1;
  const c={id:"c"+TC.n+"_"+k.replace(/-/g,""),t:v.slice(0,800),made:k,open:tcAdd(k,TC_SP[sp][0]),sp,f:TC.f?tcFacts():null,w:tcWhere(),op:null};
  TC.list.push(c);TC.draft="";S.owned.add("tc_box");if(TC.list.length>=3)S.owned.add("tc_letters");save();ui();award("tc_s1");tcSealAnim(c);}
let tcRaf=0,tcFix=null;
const tcEz=p=>p<=0?0:p>=1?1:p*p*(3-2*p),tcSeg=(e,a,b)=>tcEz((e-a)/(b-a));
function tcSealAnim(c){const kura=c.w==="kura";
  openPanel("Капсула времени",`<canvas id="tcCv" class="tc-cv"></canvas><div id="tcEnd" class="tc-end" style="visibility:hidden"><p class="lead">Шкатулка ${kura?"стоит на высокой полке в куре":"закопана во дворике, под плоским камнем"}. Откроется ${tcDate(c.open,1)} — ${tcIn(c.open)}. До тех пор письмо не прочитать — даже тебе.</p>
   <div class="row"><button class="btn primary" data-x="tc:go:${c.w}">${kura?"Посмотреть на полку":"Пойти во дворик"}</button><button class="btn" data-x="tc:hub">К дому</button></div></div>`,"tc");$("xpBody").scrollTop=0;
  const cv=$("tcCv"),dpr=Math.min(2,devicePixelRatio||1),W=Math.max(280,cv.clientWidth||400),H=320,g=cv.getContext("2d"),t0=performance.now(),away=petAway(),T=7.2;
  cv.width=W*dpr;cv.height=H*dpr;cancelAnimationFrame(tcRaf);
  [[.5,()=>tone(1400,.04,"triangle",.015)],[1.1,()=>tone(1200,.04,"triangle",.015)],[2.2,()=>tone(260,.08,"sine",.04)],[2.75,()=>tone(140,.14,"triangle",.09)],[3.1,()=>chime([784,988])],
   [4.4,()=>{if(!away)tone(520,.12,"sine",.03);}],[6.6,()=>chime([659,784,988,1318])]].forEach(([s,f])=>setTimeout(()=>{if(panelIs("tc")&&cv.isConnected)f();},s*1000));
  const step=()=>{if(!cv.isConnected)return;const e=tcFix!=null?tcFix:(performance.now()-t0)/1000;g.setTransform(dpr,0,0,dpr,0,0);tcFrame(g,W,H,Math.min(e,T),c,away);
    if(e>=T)$("tcEnd").style.visibility="visible";if(e<T||tcFix!=null)tcRaf=requestAnimationFrame(step);};
  tcRaf=requestAnimationFrame(step);}
function tcBlit(g,k,x,y,s,a=1){const r=TC_AT[k];if(!tcIm||a<=0)return;g.globalAlpha=a;g.drawImage(tcIm,r[0],r[1],r[2],r[3],x,y,r[2]*s,r[3]*s);g.globalAlpha=1;}
function tcFrame(g,W,H,e,c,away){const cx=W/2,fl=H-30,s=Math.min(1.05,W/430),BX=cx-95*s,rim=fl-56*s;
  g.fillStyle="#0d0b09";g.fillRect(0,0,W,H);
  let gr=g.createRadialGradient(cx-20*s,fl-110*s,10,cx-20*s,fl-110*s,W*.75);gr.addColorStop(0,"rgba(240,180,110,.24)");gr.addColorStop(1,"rgba(240,180,110,0)");g.fillStyle=gr;g.fillRect(0,0,W,H);
  g.fillStyle="#1e1711";g.fillRect(0,fl-6,W,H);g.fillStyle="rgba(255,220,170,.07)";g.fillRect(0,fl-6,W,2);
  // the box flies off to its place at the end
  const fly=tcSeg(e,5.7,6.7),fx=fly*W*.42,fy=-fly*H*.6,fs=1-fly*.75;
  g.save();g.translate(cx-20*s+fx,fl+fy);g.scale(fs,fs);g.translate(-(cx-20*s),-fl);
  const shut=tcSeg(e,2.3,2.8);
  tcBlit(g,"empty",BX-20*s,fl-146*s,s,tcSeg(e,0,.4)*(1-tcSeg(e,2.45,2.8)));
  // the letter: flat with lines → folded in three → in half → down into the box
  if(e<2.4){const p1=tcSeg(e,.45,1.05),p2=tcSeg(e,1.1,1.55),dr=tcSeg(e,1.6,2.3),lw=150*s*(1-.5*p2)*(1-.08*dr),lh=104*s*(1-.66*p1),
      lx=cx-28*s,ly=fl-196*s+dr*(rim-(fl-196*s)+lh*.2);
    g.save();g.beginPath();g.rect(0,0,W,rim+(dr>0?0:H));g.clip();g.globalAlpha=tcSeg(e,0,.3);
    g.shadowColor="rgba(0,0,0,.45)";g.shadowBlur=10*s;g.shadowOffsetY=4*s;g.fillStyle="#efe4cc";g.fillRect(lx-lw/2,ly-lh/2,lw,lh);g.shadowColor="transparent";
    if(p1<.6){g.strokeStyle=`rgba(50,36,26,${.7*(1-p1/.6)})`;g.lineWidth=1.2*s;for(let i=0;i<6;i++){const yy=ly-lh/2+12*s+i*14*s*(1-.66*p1);if(yy>ly+lh/2-6*s)break;g.beginPath();g.moveTo(lx-lw/2+12*s,yy);g.lineTo(lx+lw/2-(i%3?14:40)*s,yy);g.stroke();}}
    if(p1>0&&p1<1){const fh=lh/2*Math.abs(Math.cos(p1*Math.PI)),up=Math.cos(p1*Math.PI)<0;g.fillStyle=up?"#ddcdae":"rgba(120,90,60,.18)";g.fillRect(lx-lw/2,up?ly+lh/2-fh:ly+lh/2,lw,up?fh:Math.min(fh,8*s));}
    if(p1>.9){g.fillStyle="rgba(120,90,60,.22)";g.fillRect(lx-lw/2,ly-1,lw,1.4*s);}
    if(p2>.95){g.fillStyle="rgba(120,90,60,.25)";g.fillRect(lx-1,ly-lh/2,1.4*s,lh);}
    g.restore();g.globalAlpha=1;}
  tcBlit(g,"box",BX-20*s,fl-126*s-(1-shut)*18*s,s,shut);
  if(e>2.8&&e<3.6){g.globalAlpha=1-tcSeg(e,3.1,3.6);g.font=`${16*s}px serif`;g.textAlign="center";for(let i=0;i<3;i++)g.fillText("✨",BX+73*s+Math.cos(i*2.1+e*3)*26*s,fl-118*s+Math.sin(i*2.1)*10*s-(e-2.8)*20*s);g.globalAlpha=1;}
  g.restore();
  // Musya walks in and pats the box (or she is away travelling)
  if(!away){const mx=cx+86*s,sc=.62*s;
    if(e>2.9&&e<4){const k=tcSeg(e,2.9,4);drawCatG(g,"moveLeft",Math.floor(e*10)%8,W+70*s+(mx-W-70*s)*k,fl+4*s,sc);}
    else if(e>=4&&e<5.7)drawCatG(g,"play",[1,2,2,1,0,1,2,2][Math.floor(e*6)%8],mx,fl+4*s,sc);   // the paw reaches left: pat-pat on the lid
    else if(e>=5.7)drawCatG(g,"purr",3,mx,fl+4*s,sc);
    g.font=`${15*s}px serif`;g.textAlign="center";for(const k of [4.3,4.85,5.35])if(e>k&&e<k+1.3){g.globalAlpha=1-(e-k)/1.3;g.fillText("💗",BX+40*s+(k-4.3)*50*s,fl-140*s-(e-k)*40*s);}g.globalAlpha=1;}
  else if(e>3.2&&e<5.8){g.globalAlpha=tcSeg(e,3.2,3.6)*(1-tcSeg(e,5.4,5.8));textC(g,"Муся в путешествии — погладит шкатулку потом",cx,40*s,13*s,"#d8d2c3",400);g.globalAlpha=1;}
  if(e>6.3){g.globalAlpha=tcSeg(e,6.3,6.9);textC(g,"🔒 до "+tcDate(c.open,1),cx,H*.42,19*s,"#efe4cc",600);textC(g,c.w==="kura"?"на высокой полке в куре":"во дворике, под плоским камнем",cx,H*.42+26*s,13*s,"#a99f8c",400);g.globalAlpha=1;}}
function tcRead(c){
  if(!c.op){c.op=dayKey();disc("capsule",c.id);S.owned.add("tc_open");save();ui();award("tc_o1");if(c.sp==="y")award("tc_y1");hubDot();tabDots();if(!petAway())react("😻",2.4);chime([784,988,1318,1568]);}
  const n=tcDiff(c.made,c.op),r=TC_AT.open,W=tcWait().length;
  openPanel("Капсула времени",`<div class="tc-hd">${itemThumb({at:["tc",r[0],r[1]],w:r[2],h:r[3]},110,84)}<div><b>Письмо от ${tcDate(c.made,1)}</b><small>Пролежало ${n>=360?"целый год":n>=170?"полгода":daysWord(n)} ${c.w==="kura"?"на полке в куре":"под камнем во дворике"} · открыто ${tcDate(c.op,1)}</small></div></div>
   <div class="tc-letter">${esc(c.t)}</div>
   ${c.f?`<h4 class="tc-h">Тогда → сейчас</h4><ul class="tc-cmp">${tcCmp(c.f).map(s=>`<li>${s}</li>`).join("")}</ul>`:""}
   <p class="tc-nar">${tcNar(c)}</p><div class="row">${W<3?'<button class="btn primary" data-x="tc:write">✍️ Написать новое письмо</button>':""}<button class="btn" data-x="tc:hub">К дому</button></div>`,"tcr");$("xpBody").scrollTop=0;}
function tcListHtml(){const op=TC.list.filter(c=>c.op).reverse(),W=tcWait();
  return`<div class="tc-alb">${op.map(c=>`<button class="tc-al" data-x="tc:read:${c.id}"><b>✉️ ${tcDate(c.made,1)} → ${tcDate(c.op,1)}</b><small>${esc(c.t.slice(0,80))}${c.t.length>80?"…":""}</small></button>`).join("")}${W.map(c=>`<div class="tc-al lk"><b>🔒 ${tcDate(c.made,1)} → ${tcDate(c.open,1)}</b><small>${tcReady(c)?"Пришло время — открой в «家 Дом»":"Ещё не время: "+tcIn(c.open)}</small></div>`).join("")}</div>`;}

// ── 家 hub card, album, dots, toast, the postcard
hook("hub",()=>{const W=tcWait(),R=W.filter(tcReady),op=TC.list.filter(c=>c.op).length;
  const st=R.length?`📦 Пришло время открыть капсулу от ${tcDate(R[0].made)}!`:W.length?`Откроется ${tcDate(W[0].open)} — ${tcIn(W[0].open)}`:"Напиши письмо себе в будущее и спрячь его в шкатулку";
  const rows=W.map(c=>tcReady(c)?`<div class="tc-row go"><span>📦</span><div><b>Письмо от ${tcDate(c.made)}</b><small>Пришло время!</small></div><button class="btn primary" data-x="tc:open:${c.id}">Открыть</button></div>`
    :`<div class="tc-row"><span>🔒</span><div><b>Письмо от ${tcDate(c.made)}</b><small>Откроется ${tcDate(c.open)} — ${tcIn(c.open)}</small></div></div>`).join("");
  const wh=tcWhere()==="kura"?"Шкатулки стоят на высокой полке в куре.":"Пока кура закрыта, шкатулки закапывают во дворике под плоским камнем.";
  return`<div class="hubc"><h4>📦 Капсула времени <i>手紙</i></h4><p>${st}</p>${rows}<p class="tc-wh">${W.length>=3?"На полке уже три шкатулки — новую можно будет запечатать, когда откроется ближайшая.":"Письмо себе через месяц, полгода или год. "+wh}</p>
   <div class="row">${W.length<3?'<button class="btn" data-x="tc:write">✍️ Написать письмо</button>':""}${op?`<button class="btn" data-x="tc:list">Открытые письма · ${op}</button>`:""}</div></div>`;});
hook("album",el=>{const op=TC.list.filter(c=>c.op).length,W=tcWait().length;
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Капсулы времени</h3><p class="lead">${op||W?`Открыто писем: ${op}${W?` · ждут своего дня: ${W}`:""}.`:"Писем в будущее пока нет. Напиши первое: «家 Дом» → Капсула времени."}</p>${tcListHtml()}`);});
hook("hubDot",()=>tcWait().some(tcReady));
hook("tabDot",room=>tcWait().some(c=>tcReady(c)&&c.w===room));
hook("away",()=>tcWait().some(tcReady)?{i:"📦",t:"Пришло время открыть капсулу времени — она ждёт в «家 Дом»"}:null);
hook("sec",()=>{if(!document.hidden&&!overlaysOpen()&&!scene.on)TC.rt[S.room]=(TC.rt[S.room]||0)+1;
  if(TC.told!==dayKey()&&!overlaysOpen()&&!scene.on&&tcWait().some(tcReady)){TC.told=dayKey();save();toast("📦 Пришло время открыть капсулу");chime([659,784,988]);}});
hook("click",key=>{if(!key.startsWith("tc:"))return;const [,a,v]=key.split(":"),c=v&&TC.list.find(q=>q.id===v);
  if(a==="write")tcWrite();else if(a==="sp"&&TC_SP[v]){TC.sp=v;tcWrite();}else if(a==="f"){TC.f=TC.f?0:1;tcWrite();}else if(a==="seal")tcSeal();
  else if((a==="open"||a==="read")&&c&&(c.op||tcReady(c)))tcRead(c);
  else if(a==="list")openPanel("Капсулы времени",`<p class="lead">Письма, которые уже дождались своего дня. Нажми, чтобы перечитать.</p>${tcListHtml()}`,"tca");
  else if(a==="hub")openHub();
  else if(a==="go"){closePanel();if(S.room!==v)goRoom(v);if(!petAway())setTimeout(()=>{if(S.room===v&&!scene.on)walkTo({x:v==="kura"?1130:1000},"peek","📦");},900);}
  return true;});

// ── in the room: a small shelf high on the kura wall (or little mounds in the courtyard) with the waiting boxes
let tcIm=null,tcHits=[];
hook("boot",()=>atlasImg("tc",im=>{tcIm=im;}));
function tcSpr(k){if(!tcIm)return null;const C=tcSpr.c||(tcSpr.c={});if(C[k])return C[k];const r=TC_AT[k],cv=document.createElement("canvas");cv.width=r[2];cv.height=r[3];
  const g=cv.getContext("2d");g.drawImage(tcIm,r[0],r[1],r[2],r[3],0,0,r[2],r[3]);g.globalCompositeOperation="source-atop";g.fillStyle="rgba(24,16,8,.2)";g.fillRect(0,0,r[2],r[3]);return C[k]=cv;}
const TC_SH={x:1135,y:760},TC_MD={x:1090,y:1318};   // kura: the shelf on the free wall right of the lantern; courtyard: in front, by the flat stone
function tcGlow(x,y,r,t){const a=.5+.2*Math.sin(t*2.4),gr=ctx.createRadialGradient(x,y,0,x,y,r);gr.addColorStop(0,`rgba(255,200,120,${a})`);gr.addColorStop(1,"rgba(255,200,120,0)");ctx.fillStyle=gr;ctx.fillRect(x-r,y-r,r*2,r*2);}
hook("draw",(t,front)=>{if(!front)tcHits=[];if(scene.on||!tcIm)return;const room=S.room;if(room==="kura"?front:room!=="courtyard"||!front)return;
  const W=tcWait().filter(c=>c.w===room);if(room==="kura"&&!TC.list.some(c=>c.w==="kura"))return;if(room==="courtyard"&&!W.length)return;
  if(room==="kura"){const [sx,sy]=imgToStage(TC_SH.x,TC_SH.y,.4),k=(imgToStage(TC_SH.x+100,TC_SH.y,.4)[0]-sx)/100,sh=tcSpr("shelf"),bx=tcSpr("box"),bs=.55*k;
    ctx.drawImage(sh,sx-165*k,sy-10*k,330*k,70*k);
    W.slice(0,3).forEach((c,i)=>{const x=sx+(i-(W.length-1)/2)*104*k;if(tcReady(c))tcGlow(x,sy-38*k,90*k,t);ctx.drawImage(bx,x-93*bs,sy-126*bs,180*bs,140*bs);
      const hw=Math.max(24,52*k),hh=Math.max(24,44*k);tcHits.push([c,x-hw,sy-hh*2,x+hw,sy+6]);});return;}
  W.slice(0,3).forEach((c,i)=>{const ix=visX(TC_MD.x,60)+(i-(W.length-1)/2)*78,[x,y]=imgToStage(ix,TC_MD.y,CAT_D),k=(imgToStage(ix+100,TC_MD.y,CAT_D)[0]-x)/100;
    if(tcReady(c))tcGlow(x,y-14*k,90*k,t);const m=1.6*k;
    ctx.fillStyle="rgba(0,0,0,.4)";ctx.beginPath();ctx.ellipse(x,y+3*m,40*m,10*m,0,0,7);ctx.fill();
    ctx.fillStyle="#3a3027";ctx.beginPath();ctx.ellipse(x,y,36*m,12*m,0,Math.PI,0);ctx.fill();ctx.fillStyle="#4a3e31";ctx.beginPath();ctx.ellipse(x,y-2*m,30*m,7*m,0,0,7);ctx.fill();
    ctx.fillStyle="#7c7a74";ctx.beginPath();ctx.ellipse(x+3*m,y-5*m,20*m,7*m,-.1,0,7);ctx.fill();ctx.fillStyle="rgba(215,220,225,.3)";ctx.beginPath();ctx.ellipse(x,y-8*m,12*m,3*m,-.1,0,7);ctx.fill();
    ctx.fillStyle="#7a5c40";ctx.fillRect(x-26*m,y-36*m,3.4*m,34*m);ctx.fillStyle="#efe6d0";ctx.fillRect(x-23.5*m,y-32*m,10*m,14*m);ctx.fillStyle="#3a2a20";ctx.fillRect(x-20*m,y-29*m,1.6*m,8*m);
    const hw=Math.max(24,40*m);tcHits.push([c,x-hw,y-40*m-10,x+hw,y+12]);});});
hook("hit",(x,y)=>{for(const [c,x0,y0,x1,y1] of tcHits){if(x<x0||x>x1||y<y0||y>y1)continue;
  if(tcReady(c)){tcRead(c);return true;}toast(`📦 Откроется ${tcDate(c.open)} — ${tcIn(c.open)}`);tone(180,.1,"triangle",.04);if(!petAway())react("👀",1.4);return true;}});

document.head.insertAdjacentHTML("beforeend",`<style>
.tc-paper{position:relative;margin:4px 0 12px}.tc-paper textarea{width:100%;box-sizing:border-box;min-height:200px;resize:vertical;padding:12px 14px 24px;border-radius:12px;border:1px solid var(--line);
 background:#ece2cc linear-gradient(transparent 27px,rgba(90,60,30,.13) 28px) 0 11px/100% 28px;color:#2a1f16;font:17px/28px var(--display),serif;outline:none}
.tc-paper textarea::placeholder{color:#8a7a64}.tc-paper small{position:absolute;right:12px;bottom:8px;font-size:12px;color:#7a6a58}
.tc-h{font-family:var(--display);font-size:16px;margin:10px 0 8px;color:var(--paper)}
.tc-sp{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px}
.tc-o{border:1px solid var(--line);border-radius:12px;background:var(--ink-2);color:var(--muted);padding:9px 4px;font:inherit;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:2px}
.tc-o b{color:var(--paper);font-size:14px;font-weight:600}.tc-o small{font-size:11.5px}.tc-o.on{border-color:var(--sakura);background:rgba(238,163,187,.12)}
.tc-f{display:flex;gap:10px;align-items:flex-start;text-align:left;width:100%;border:1px solid var(--line);border-radius:12px;background:var(--ink-2);color:var(--muted);padding:10px 12px;font:inherit;cursor:pointer;margin-bottom:12px}
.tc-f>span{font-size:18px;color:var(--paper);line-height:1.1}.tc-f b{display:block;color:var(--paper);font-size:14px;margin-bottom:3px}.tc-f small{font-size:12.5px;line-height:1.45;display:block}.tc-f.on{border-color:rgba(238,163,187,.45)}
.tc-msg{border-left:3px solid var(--sakura);padding:4px 10px;color:var(--paper);font-size:14px}
.tc-cv{width:100%;height:320px;display:block;border-radius:14px;margin:0 0 12px;background:#0d0b09}
.hubc .tc-row{display:flex;gap:10px;align-items:center;padding:8px 0;border-top:1px solid var(--line);margin:0}.tc-row>span{font-size:20px}.tc-row>div{flex:1;min-width:0}.tc-row b{display:block;font-size:14px;color:var(--paper)}.tc-row small{color:var(--muted);font-size:12.5px}
.tc-row.go small{color:#f3d9a0}.hubc p.tc-wh{color:var(--muted);font-size:13px}
.tc-hd{display:flex;gap:12px;align-items:center;margin-bottom:8px}.tc-hd b{display:block;font-family:var(--display);font-size:18px;color:var(--paper)}.tc-hd small{color:var(--muted);font-size:13px;line-height:1.4;display:block}
.tc-letter{background:#ece2cc;color:#2a1f16;border-radius:6px;padding:16px 18px;font:17px/1.6 var(--display),serif;white-space:pre-wrap;overflow-wrap:anywhere;box-shadow:0 6px 20px rgba(0,0,0,.45);transform-origin:top;animation:tcUnf 1s ease-out both;margin:6px 0 16px}
@keyframes tcUnf{from{transform:perspective(700px) rotateX(-75deg);opacity:0}to{transform:none;opacity:1}}
.tc-cmp{list-style:none;padding:0;margin:0 0 14px;display:grid;gap:7px}.tc-cmp li{font-size:14px;line-height:1.45;color:var(--paper);padding-left:18px;position:relative}
.tc-cmp li::before{content:"◆";position:absolute;left:0;top:3px;color:var(--sakura);font-size:10px}.tc-cmp b{color:#f3d9a0;font-weight:600}
.tc-nar{font-style:italic;color:#d9cdb6;font-size:14.5px;line-height:1.55;border-left:2px solid rgba(243,217,160,.4);padding:2px 0 2px 12px;margin:0 0 14px}
.tc-al{display:block;width:100%;text-align:left;border:1px solid var(--line);border-radius:12px;background:var(--ink-2);color:var(--paper);padding:9px 12px;margin:0 0 8px;font:inherit;cursor:pointer}
.tc-al b{display:block;font-size:14px;font-weight:600}.tc-al small{color:var(--muted);font-size:12.5px;display:block;margin-top:2px}.tc-al.lk{opacity:.6;cursor:default}
</style>`);
X.capsule={st:TC,write:tcWrite,seal(txt,sp,f=1){TC.draft=txt;TC.sp=sp||"m";TC.f=f;tcSeal();},read:id=>tcRead(TC.list.find(c=>c.id===id)||tcWait()[0]),
  fix(e){tcFix=e;},where(w){tcTestW=w;},hits:()=>tcHits,add:tcAdd,facts:tcFacts};
}
