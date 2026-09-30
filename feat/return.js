{
// ───────────────────────── «Пока тебя не было»: a painted diary page on return + Musya's finds ─────────────────────────
// Away ≥ 45 min → one postcard: how long, what Musya did (narrator, she never talks), news from other systems (hook "away"),
// and a find she dragged home (guaranteed from 1 h, rare ~12%). Shorter absences: nothing pops up.
const RET=S.ext.ret||(S.ext.ret={n:0,cnt:{}});RET.cnt=RET.cnt||{};
const RET_MIN=45*60e3;
// [id, name, w, h, atlasX, atlasY, rare, where-she-found-it, seasonMonths|null, glow]
const FD=[
 ["fd_crow","Вороново перо",80,180,102,0,0,"Под старой сосной, где по утрам спорят вороны.",null],
 ["fd_pebble","Гладкий речной камешек",120,80,876,232,0,"Из ручья у водопада — ещё мокрый и прохладный.",null],
 ["fd_button","Старая латунная пуговица",90,70,0,334,0,"Из-под половиц в гардеробе. Кто её там потерял?",null],
 ["fd_mon","Старинная монетка мон",100,100,0,232,0,"Из щели у ворот храма. Такие ходили при сёгунах.",null],
 ["fd_tsuru","Бумажный журавлик",140,110,680,0,0,"Кто-то сложил его и оставил на камне у пруда.",null],
 ["fd_momiji","Кленовый лист",130,130,262,0,0,"Сорвала с ветки в прыжке — и очень этим гордится.",[9,10,11]],
 ["fd_cone","Сосновая шишка",90,120,482,0,0,"Прикатила лапой через весь дворик.",[9,10,11,12]],
 ["fd_acorn","Желудь",80,100,102,232,0,"Добыча, отбитая у белки. Почти честно.",[9,10,11]],
 ["fd_shard","Осколок синей глазури",120,90,424,232,0,"Из земли у кухни — наверное, от бабушкиной чашки.",null],
 ["fd_bell","Колокольчик без язычка",84,104,920,0,0,"Лежал у каменного фонаря. Язычок потерялся давно.",null],
 ["fd_thread","Моток красной нити",120,90,546,232,0,"Говорят, красная нить связывает тех, кому суждено встретиться.",null],
 ["fd_shell","Расписная ракушка",120,96,184,232,0,"Половинка из игры каи-авасэ. Где-то есть её пара.",null],
 ["fd_hotaru","Светлячок в бутылочке",76,136,184,0,0,"Светит всю ночь, а утром его отпустят в сад.",[6,7,8],[38,88]],
 ["fd_semi","Шкурка цикады",100,84,774,232,0,"Уцусэми — «пустая скорлупка» из старинных стихов.",[7,8,9]],
 ["fd_hane","Волан для ханэцуки",86,126,394,0,0,"Кто-то запустил его ракеткой через забор.",[12,1,2]],
 ["fd_tsubaki","Цветок камелии",116,96,306,232,0,"Камелия опадает целым цветком — Муся поймала его на лету.",[12,1,2,3]],
 ["fd_tengu","Перо тэнгу",100,230,0,0,1,"Тэнгу живут на вершинах криптомерий. Как она его достала?",null],
 ["fd_magatama","Магатама из нефрита",96,110,822,0,1,"Древняя бусина-запятая. Таким больше тысячи лет.",null],
 ["fd_moon","Лунный камешек",104,86,668,232,1,"Светится в темноте, как луна сквозь туман.",null,[52,46]],
 ["fd_ryu","Чешуйка дракона",104,116,574,0,1,"Переливается, как вода в пруду. Где Муся встретила дракона?",null,[52,56]]
];
const FDW={};for(const f of FD)FDW[f[0]]=f;
addItems(FD.map(([id,n,w,h,x,y,rare,,,glow])=>Object.assign({id,n,c:"Находки Муси",w,h,a:"b",p:0,at:["fd",x,y],src:"🐾 находка Муси",
  hint:rare?"Редкая находка — Муся приносит её нечасто":"Муся приносит находки, пока тебя нет"},glow?{glow}:{})),{fd:[1024,404]});

document.head.insertAdjacentHTML("beforeend",`<style>
.ret-card{position:relative;max-width:27em;margin:4px auto 18px;padding:22px 20px 18px;border-radius:5px;color:#2b2119;transform:rotate(-.5deg);
 background:radial-gradient(60% 40% at 80% 90%,rgba(150,110,60,.18),transparent),radial-gradient(50% 30% at 10% 15%,rgba(255,250,235,.5),transparent),radial-gradient(120% 90% at 35% 25%,#efe5cf,#e0d0ad 62%,#c9b48b);
 box-shadow:0 14px 34px rgba(0,0,0,.6),inset 0 0 46px rgba(110,80,40,.38)}
.ret-card::before{content:"";position:absolute;inset:0;border-radius:5px;pointer-events:none;opacity:.5;
 background:repeating-linear-gradient(8deg,rgba(90,66,36,.06) 0 1px,transparent 1px 4px),repeating-linear-gradient(97deg,rgba(90,66,36,.05) 0 1px,transparent 1px 7px)}
.ret-card::after{content:"";position:absolute;left:50%;top:-9px;width:88px;height:20px;margin-left:-44px;background:rgba(214,196,160,.75);transform:rotate(2deg);box-shadow:0 1px 3px rgba(0,0,0,.25)}
.ret-date{font-family:var(--display);font-size:14px;letter-spacing:.04em;color:#7a6146}
.ret-h{font-family:var(--display);font-size:25px;font-weight:700;line-height:1.15;margin:4px 64px 10px 0;color:#2b1d14;text-wrap:balance}
.ret-seal{position:absolute;right:16px;top:18px;width:46px;height:46px;border-radius:6px;display:grid;place-items:center;writing-mode:vertical-rl;font-family:var(--jp);font-size:17px;line-height:1;color:#f6e9dc;background:radial-gradient(circle at 40% 35%,#c4473b,#962a20);transform:rotate(9deg);opacity:.88;box-shadow:inset 0 0 6px rgba(60,10,5,.6)}
.story-body .ret-card p{color:#2b2119;margin:0 0 8px}
.story-body .ret-card .ret-p{font-family:var(--display);font-size:18px;line-height:1.45;font-style:italic}
.ret-hr{height:2px;margin:14px 6px;background:linear-gradient(90deg,transparent,rgba(70,46,24,.45) 20%,rgba(70,46,24,.3) 80%,transparent);border-radius:2px}
.ret-li{display:flex;gap:10px;align-items:flex-start;font-size:14.5px;line-height:1.4;margin:6px 0;color:#34281e}.ret-li i{font-style:normal;font-size:17px;width:22px;flex:none;text-align:center}
.ret-find{display:flex;flex-direction:column;align-items:center;text-align:center;gap:6px;margin-top:4px}
.ret-find .ret-k{font-family:var(--display);font-size:15px;color:#8a3a2a;letter-spacing:.03em}
.ret-find .ret-k.rare{color:#9a6a10}
.ret-pic{position:relative;display:grid;place-items:center;width:190px;height:170px}
.ret-pic::before{content:"";position:absolute;inset:6px;border-radius:50%;background:radial-gradient(circle,rgba(255,244,210,.95),rgba(255,236,190,.4) 50%,transparent 70%)}
.ret-pic.rare::before{background:radial-gradient(circle,rgba(255,236,160,1),rgba(250,200,90,.45) 50%,transparent 72%)}
.ret-pic>span{position:relative;filter:drop-shadow(0 4px 6px rgba(60,40,20,.45))}
.ret-find b{font-family:var(--display);font-size:22px;color:#2b1d14}
.story-body .ret-find small{font-size:13.5px;color:#5e4a36;line-height:1.35;max-width:22em}
.ret-card .ret-btn{margin-top:8px;padding:10px 26px;border-radius:999px;background:#2b2119;color:#f0e6d0;font-weight:700;border:0;box-shadow:0 3px 10px rgba(0,0,0,.35)}
.ret-paw{position:absolute;right:16px;bottom:12px;font-size:18px;opacity:.35;transform:rotate(-12deg)}
</style>`);

// ── Russian words ──
function rPl(n,a,b,c){n=Math.abs(n)%100;const m=n%10;return n>10&&n<20?c:m===1?a:m>=2&&m<=4?b:c;}
function rN(n,w){return n+" "+rPl(n,...w);}
const W_MIN=["минуту","минуты","минут"],W_H=["час","часа","часов"],W_D=["день","дня","дней"],W_WK=["неделю","недели","недель"],W_MO=["месяц","месяца","месяцев"];
function awayText(ms){
  const min=ms/6e4,h=min/60,d=h/24;
  if(min<55)return rN(Math.max(5,Math.round(min/5)*5),W_MIN);
  if(min<65)return min<60?"почти час":"целый час";
  if(h<6){let H=Math.floor(h),M=Math.round((min-H*60)/10)*10;if(M===60){H++;M=0;}
    if(H===1&&M===30)return"полтора часа";if(!M)return H===1?"целый час":rN(H,W_H);if(M>=50)return"почти "+rN(H+1,W_H);return rN(H,W_H)+" "+rN(M,W_MIN);}
  if(h<20)return h%1>.7?"почти "+rN(Math.ceil(h),W_H):rN(Math.floor(h),W_H);
  if(h<24)return"почти сутки";if(h<30)return"сутки";if(h<44)return"больше суток";if(h<48)return"почти двое суток";
  if(d<7)return d%1>.8?"почти "+rN(Math.ceil(d),W_D):rN(Math.floor(d),W_D);
  if(d<14)return d<8?"целую неделю":"больше недели";if(d<30)return rN(Math.floor(d/7),W_WK);if(d<60)return"больше месяца";return rN(Math.floor(d/30),W_MO);
}
const MON_G=["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"];
function partOf(h){return h<5||h>=22?"night":h<10?"morning":h<17?"day":"evening";}
const PART_RU={night:"ночь",morning:"утро",day:"день",evening:"вечер"};
function list(a){return a.length<2?a.join(""):a.slice(0,-1).join(", ")+" и "+a[a.length-1];}

// ── what Musya did (the narrator speaks; she only meows) ──
const DOING={
 night:["Ночью Муся спала на футоне, свернувшись калачиком, и во сне шевелила усами.","Ночью она сидела у сёдзи и смотрела, как по бумаге ползёт лунная тень.","Ночью Муся дважды обошла дом — всё ли на месте — и уснула у твоей подушки."],
 morning:["Утром Муся смотрела, как вороны делят что-то на крыше храма.","На рассвете она гоняла солнечный зайчик по татами — и победила.","Утром Муся долго и очень старательно умывалась на веранде."],
 day:["Днём она дремала на тёплых досках веранды, подставив солнцу живот.","Днём Муся караулила карпов в пруду, но так и не решилась намочить лапу.","Днём она спала в коробке — снаружи торчал только хвост."],
 evening:["Вечером Муся сидела у двери и ждала: уши поворачивались на каждый шорох.","В сумерках она смотрела, как в саду загорается каменный фонарь.","Вечером Муся слушала фурин и тихонько мурлыкала ему в ответ."],
 rain:["Шёл дождь. Муся слушала, как капли стучат по черепице, и не решалась выйти на веранду."],
 short:["Сначала Муся поскучала у порога, потом умылась и сделала вид, что вовсе не ждала.","Муся проверила миску, проверила подушку и на всякий случай ещё раз проверила миску."],
 long:["Первый день Муся ждала у двери. Потом решила, что ты обязательно вернёшься, и стала спать на твоей подушке.","Она обошла весь дом, заглянула в каждую комнату и в каждую коробку — тебя нигде не было."],
 vlong:["Муся считала дни по воронам на крыше. Кажется, она немного обиделась — но это ненадолго."],
 season:{win:"За окном падал снег, и Муся грела лапы у жаровни.",spr:"Ветер приносил из сада лепестки, и Муся ловила их на веранде.",sum:"Было душно, и Муся лежала в тени, растянувшись во всю длину.",aut:"Ветер заносил на веранду кленовые листья, и Муся ловила каждый."}
};
function seasonKey(){const m=today().getMonth()+1;return m===12||m<3?"win":m<6?"spr":m<9?"sum":"aut";}
function doing(ms){
  const h=ms/36e5,out=[];
  if(petAway())return["Муся ещё в пути — в доме непривычно тихо. Будем ждать её вместе."];
  if(h>=72)out.push(pick(DOING.vlong));else if(h>=20)out.push(pick(DOING.long));
  else{const mid=((hourNow()-h/2)%24+24)%24;out.push(weather.on&&h<3?DOING.rain[0]:pick(DOING[h<2&&Math.random()<.4?"short":partOf(mid)]));}
  if(h>=3){const s=DOING.season[seasonKey()],p2=pick(DOING[partOf(((hourNow()-.5)%24+24)%24)]);out.push(Math.random()<.5&&!out.includes(s)?s:out.includes(p2)?s:p2);}
  return out;
}

// ── news from the house ──
function news(ms){
  const L=hkAll("away",ms).filter(x=>x&&x.t);
  const q=S.guest,gd=typeof guestDef==="function"?guestDef():null;
  if(gd&&q.state==="here")L.push({i:"⛩",t:`У ворот ждёт ${gd.n}. Загляни во «Вход».`});
  else if(q&&q.state==="coming"&&q.day===dayKey())L.push({i:"⛩",t:"Кажется, к воротам уже кто-то идёт…"});
  const ripe=S.garden.filter(b=>b&&bedP(b)>=1).map(b=>(CROPS.find(c=>c.id===b.c)||{n:""}).n.toLowerCase()).filter(Boolean);
  if(ripe.length)L.push({i:"🌱",t:`На огороде поспело: ${list([...new Set(ripe)])}. Загляни во «Дворик».`});
  const F=festNow();if(F)L.push({i:F.icon||"🎐",t:`Сегодня праздник — ${F.n}${F.sub?" ("+F.sub.toLowerCase()+")":""}. Всё о нём в календаре 暦.`});
  if(!petAway()){const n=S.needs,low=[];if(n.food<30)low.push("проголодалась");if(n.clean<30)low.push("запылилась");if(n.joy<30)low.push("заскучала");
    if(low.length)L.push({i:"🍚",t:`Муся ${list(low)} — самое время о ней позаботиться.`});}
  return L;
}

// ── the find ──
function pickFind(ms){
  if(petAway())return null;
  const h=ms/36e5;if(ms<60*60e3&&Math.random()>.4)return null;
  const m=today().getMonth()+1,wt=f=>f[8]&&f[8].includes(m)?3:1;
  const wpick=a=>{let s=0;for(const f of a)s+=wt(f);let r=Math.random()*s;for(const f of a){r-=wt(f);if(r<=0)return f[0];}return a[a.length-1][0];};
  const rares=FD.filter(f=>f[6]&&!S.owned.has(f[0])),commons=FD.filter(f=>!f[6]&&!S.owned.has(f[0]));
  if(rares.length&&Math.random()<Math.min(.25,.12+Math.max(0,h-24)/24*.03))return wpick(rares);
  if(commons.length)return wpick(commons);
  if(rares.length)return wpick(rares);
  return wpick(FD.filter(f=>!f[6]));   // everything owned: a repeat find
}
function bigThumb(i,mw,mh){const a=IATL[i.at[0]],k=Math.min(mw/i.w,mh/i.h,1.5),f=v=>(v*k).toFixed(1);
  return`<span style="display:inline-block;width:${f(i.w)}px;height:${f(i.h)}px;background:url(assets/items/atlas_${i.at[0]}.webp) -${f(i.at[1])}px -${f(i.at[2])}px/${f(a[0])}px ${f(a[1])}px no-repeat"></span>`;}

const R={pending:false,shown:false,find:null,rep:false};
function show(ms){
  R.pending=false;R.shown=true;const t=today(),hn=hourNow();
  const id=pickFind(ms),f=id&&FDW[id];let findHtml="";
  if(f){const rep=S.owned.has(id);R.find=id;R.rep=rep;RET.cnt[id]=(RET.cnt[id]||0)+1;
    if(!rep){S.owned.add(id);disc("find",id);}else S.needs.joy=clamp(S.needs.joy+10,0,100);
    findHtml=`<div class="ret-hr"></div><div class="ret-find"><span class="ret-k ${f[6]?"rare":""}">${rep?"Муся снова кое-что принесла":f[6]?"✦ Редкая находка ✦":"Муся принесла находку"}</span>
      <span class="ret-pic ${f[6]?"rare":""}">${bigThumb(IT[id],170,150)}</span><b>${f[1]}</b>
      <small>${rep?`Такая у тебя уже есть, но Муся так гордится, что радости хватит на двоих.`:f[7]}</small>
      <button class="ret-btn" data-x="ret:take">${rep?"Погладить Мусю":"Забрать"}</button></div>`;}
  const lines=news(ms);
  const html=`<div class="ret-card"><div class="ret-date">${t.getDate()} ${MON_G[t.getMonth()]} · ${PART_RU[partOf(hn)]}</div><div class="ret-seal">留守</div>
    <div class="ret-h">Тебя не было ${awayText(ms)}</div>${doing(ms).map(p=>`<p class="ret-p">${p}</p>`).join("")}
    ${lines.length?`<div class="ret-hr"></div>`+lines.map(l=>`<div class="ret-li"><i>${l.i||"·"}</i><span>${l.t}</span></div>`).join(""):""}
    ${findHtml||`<div class="ret-find" style="margin-top:12px"><button class="ret-btn" data-x="ret:ok">${petAway()?"Ждём Мусю":"Здравствуй, Муся"}</button></div>`}<span class="ret-paw">🐾</span></div>`;
  RET.n++;RET.last=Date.now();save();
  openPanel("Пока тебя не было",html,"ret");chime([784,988,1175]);
}
function tryShow(ms,t0){
  R.pending=true;
  const go=()=>{if(scene.on||overlaysOpen()||(typeof drag!=="undefined"&&drag.active)||now()-t0<2.5){setTimeout(go,700);return;}show(ms);};
  setTimeout(go,2500);
}
function take(){
  const f=R.find&&FDW[R.find];closePanel();
  if(f){toast(R.rep?"Муся мурлычет от гордости":"🐾 Находка лежит в 🧺 Вещах");chime([1046,1318,1568]);}
  if(!petAway()){react(f?"😸":"😺",2.2);S.needs.joy=clamp(S.needs.joy+5,0,100);if(f)burst(6);}
  R.find=null;save();
}
hook("boot",()=>{const ms=saved.t?Date.now()-saved.t:0;if(ms>=RET_MIN)tryShow(ms,now());});
// the page stayed open in the background (phones): the same card when the player comes back after 45 min
let hidAt=0;document.addEventListener("visibilitychange",()=>{if(document.hidden){hidAt=Date.now();return;}
  const ms=hidAt?Date.now()-hidAt:0;hidAt=0;if(ms>=RET_MIN&&!R.pending&&!panelIs("ret"))tryShow(ms,now());});
hook("click",k=>{if(k==="ret:take"){take();return true;}if(k==="ret:ok"){closePanel();if(!petAway())react("😺",2);return true;}});
hook("panelClose",id=>{if(id==="ret")R.find=null;});
X.ret={show,awayText,pickFind,news,doing,R,FD};
}
