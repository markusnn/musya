// ───────────────────────── Доска эма: three small wishes a day from yōkai Musya knows ─────────────────────────
// A wooden ema rack stands in the entrance (left of the torii, behind the travel post box). Every dayKey() three known
// yōkai hang a plaque with a wish; game events (hook ev) fulfil them; done plaques glow; the player collects small gifts
// (pantry food, joy, a ♥ for gate guests, sometimes a thing «Дары с доски эма»). All three → a bonus; streak stamps 3 / 7.
// State: S.ext.ema = {day, w:[{t,p,y,n,need,done,got,r,q}], prev, bonus, streak, last, best, n}
{
const EM_A={rack:[0,0,250,400],p0:[668,402,66,64],p1:[736,402,66,64]},EM_HK=[[62,214],[125,210],[188,214]];
const EM_X=590,EM_FY=965,EM_H=420;             // rack: image x, floor line, height (image px)
const EM_C="Дары с доски эма",EM_ITEMS=["em_uma","em_kitsune","em_daruma","em_tanzaku","em_senba","em_kumade","em_suzuri","em_inu"];
{const A={em_uma:[314,402,160,140,"t"],em_kitsune:[172,402,140,150,"t"],em_daruma:[738,0,160,176,"b"],em_tanzaku:[384,0,170,300,"b"],
   em_senba:[252,0,130,330,"t"],em_kumade:[556,0,180,270,"b"],em_suzuri:[476,402,190,120,"b"],em_inu:[0,402,170,160,"b"]},
  row=(id,n)=>({id,n,c:EM_C,w:A[id][2],h:A[id][3],a:A[id][4],p:0,at:["em",A[id][0],A[id][1]],src:"🎴 доска эма",hint:"Исполняй желания на доске эма у ворот"});
 addItems([row("em_uma","Эма с белым конём"),row("em_kitsune","Лисья эма Инари"),row("em_daruma","Дарума исполненного желания"),row("em_tanzaku","Бамбук с танзаку"),
  row("em_senba","Гирлянда журавликов"),row("em_kumade","Кумадэ на удачу"),row("em_suzuri","Кисть и тушечница"),row("em_inu","Собачка инухарико")],{em:[1000,562]});}
STAMPS.push(["em_first","願","Первое желание","Исполни желание с доски эма у ворот"],["em_s3","絵","Три дня желаний","Три дня подряд исполняй все желания с доски эма"],
 ["em_s7","馬","Неделя желаний","Семь дней подряд исполняй все желания с доски эма"]);

// who writes: gate guests (befriended), rare guests (met), night visitors (met); fallback — the first gate guests
const EM_YK={
 kappa:{n:"Каппа",m:"m_kappa",tl:"Кап-кап!",lk:["garden","fish","pond"]},
 kitsune:{n:"Лиса-невеста",m:"m_kitsune",tl:"Только тихо, по-лисьи.",lk:["shrine","food","night"]},
 tanuki:{n:"Тануки",m:"m_tanuki",tl:"Пом-пом!",lk:["food","game","put"]},
 nekomata:{n:"Нэкомата",m:"m_nekomata",tl:"Мяу, сестрёнка.",lk:["fish","play","night"]},
 akaname:{n:"Аканамэ",m:"m_akaname",tl:"Чтобы чисто-чисто!",lk:["clean","food"]},
 obake:{n:"Тётин-обакэ",m:"m_obake",tl:"Хи-хи, я посвечу.",lk:["night","game"]},
 warashi:{n:"Дзасики-вараси",m:"m_warashi",tl:"А я спрячусь и погляжу!",lk:["put","play","game"]},
 yuki:{n:"Юки-онна",m:"m_rg_yuki",tl:"Пока не растаял иней.",lk:["clean","pond","shrine"]},
 kodama:{n:"Кодама",m:"m_rg_kodama",tl:"Лес ответит эхом.",lk:["garden","pond"]},
 amabie:{n:"Амабиэ",m:"m_rg_amabie",tl:"И пусть никто не хворает.",lk:["fish","pond","shrine"]},
 usagi:{n:"Цуки-но усаги",m:"m_rg_usagi",tl:"Луна всё видит.",lk:["food","play"]},
 karakasa:{n:"Каракаса-обакэ",m:"m_vs_karakasa",tl:"Прыг-скок!",lk:["play","game"]},
 kamaitachi:{n:"Кама-итати",m:"m_vs_kamaitachi",tl:"Вжух — и готово.",lk:["garden","play"]},
 bakezori:{n:"Бакэ-дзори",m:"m_vs_bakezori",tl:"Топ-топ!",lk:["clean","put"]},
 kozo:{n:"Хитоцумэ-кодзо",m:"m_vs_kozo",tl:"Я посмотрю одним глазком.",lk:["game","night"]},
 azuki:{n:"Адзуки-арай",m:"m_vs_azuki",tl:"Шурх-шурх…",lk:["food","pond"]},
 nuppeppo:{n:"Нуппэппо",m:"m_vs_nuppeppo",tl:"Шлёп-шлёп…",lk:["clean","food"]},
 yosuzume:{n:"Ёсудзумэ",m:"m_vs_yosuzume",tl:"Чи-чи-чи!",lk:["garden","night"]},
 moku:{n:"Мокумокурэн",m:"m_vs_mokumokuren",tl:"Все глаза смотрят.",lk:["put","night"]}};
const EM_BASIC=["kappa","kitsune","tanuki","nekomata","akaname","obake"];
const EM_RN={entrance:"Вход",engawa:"Веранда",courtyard:"Дворик",kitchen:"Кухня",onsen:"Онсэн",bedroom:"Спальня"};
const EM_ACC={kyuri:"огурец",edamame:"эдамамэ",negi:"зелёный лук",daikon:"дайкон",ichigo:"клубнику"};
const EM_ACT={yarn:"поиграй с Мусей клубком",butterfly:"покажи Мусе бабочку",highfive:"попроси у Муси лапку",purr:"погладь Мусю",
 zoomies:"устрой с Мусей тыгыдык",box:"дай Мусе посидеть в коробке",firefly:"поймай с Мусей светлячка",music:"позвони для Муси в фурин"};
const emFish=d=>!!d&&!!FOOD[d.id]&&FOOD[d.id].k==="fish",emPl=a=>d=>d===a;
const emCook=()=>RECIPES.filter(R=>R.need.every(i=>have(i)>0)).map(R=>R.id);
const emCats=()=>[...new Set([...S.owned].map(id=>IT[id]&&IT[id].c).filter(c=>c&&c!==EM_C))];
const emGames=()=>["daruma","kagome","kitsunebi","tsukumo","kappa","karuta","fire","mice","okiku","hyakki"].filter(id=>GAMES.some(g=>g.id===id&&!g.hidden));
// wish templates: k = kind (for the yōkai's taste), ev = qev name, n = how many times, ok = possible now, par = parameter
const EM_T=[
 {id:"crop",k:"garden",ev:"harvest",par:r=>emPick(r,Object.keys(EM_ACC)),t:p=>`вырасти ${EM_ACC[p]} и собери урожай`,w:"Дворик → 🌱 Огород: посади, полей, собери",test:(d,p)=>!!d&&d.id==="v_"+p},
 {id:"harv2",k:"garden",ev:"harvest",n:2,t:()=>"собери на огороде два урожая",w:"Дворик → 🌱 Огород"},
 {id:"plant",k:"garden",ev:"plant",n:2,ok:()=>S.garden.filter(b=>!b).length>=2,t:()=>"посади на огороде две грядки",w:"Дворик → 🌱 Огород"},
 {id:"water",k:"garden",ev:"water",n:2,t:()=>"полей на огороде две грядки",w:"Дворик → 🌱 Огород → лейка"},
 {id:"sakura",k:"garden",ev:"sakura",ok:()=>{const T=S.ext.tree;return !!T&&T.days<30&&T.last!==dayKey();},t:()=>"полей свою сакуру",w:"Дворик → 🌸 Полить сакуру"},
 {id:"cookr",k:"food",ev:"cook",ok:()=>emCook().length>0,par:r=>emPick(r,emCook()),t:p=>`приготовь на кухне «${(RECIPES.find(R=>R.id===p)||{n:"блюдо"}).n}»`,w:"Кухня → 🍳 Готовить",test:(d,p)=>!!d&&d.id===p},
 {id:"cook",k:"food",ev:"cook",t:()=>"приготовь на кухне любое блюдо",w:"Кухня → 🍳 Готовить"},
 {id:"fish",k:"fish",ev:"fish",test:emFish,t:()=>"поймай в пруду любую рыбу",w:"Дворик → 🎣 Рыбалка"},
 {id:"fish3",k:"fish",ev:"fish",n:3,test:emFish,t:()=>"налови в пруду три рыбы",w:"Дворик → 🎣 Рыбалка"},
 {id:"eat",k:"food",ev:"eat",ok:()=>pantryEats().length>0,t:()=>"угости Мусю блюдом из кладовой",w:"Кухня → кладовая: дай Мусе блюдо"},
 {id:"food",k:"food",ev:"food",t:()=>"накорми Мусю чем-нибудь вкусным",w:"Кухня: угощения внизу"},
 {id:"bath",k:"clean",ev:"bath",t:()=>"искупай Мусю в онсэне",w:"Онсэн: намыль и смой из ковша"},
 {id:"towel",k:"clean",ev:"towel",t:()=>"вытри Мусю полотенцем после купания",w:"Онсэн → 🧺 Вытереть полотенцем"},
 {id:"wash",k:"clean",ev:"place",test:emPl("wash_paws"),t:()=>"омой Мусе лапки у ворот",w:"Вход → 💧 Омыть лапки"},
 {id:"putc",k:"put",ev:"put",ok:()=>emCats().length>0,par:r=>emPick(r,emCats()),t:p=>`поставь в доме что-нибудь из «${p}»`,w:"Любая комната → 🧺 Вещи",test:(d,p)=>!!d&&d.c===p},
 {id:"putr",k:"put",ev:"put",ok:()=>S.owned.size>0,par:r=>emPick(r,["engawa","bedroom","kitchen","courtyard","onsen"]),t:p=>`поставь любую вещь в комнату «${EM_RN[p]}»`,w:p=>`«${EM_RN[p]}» → 🧺 Вещи`,test:(d,p)=>!!d&&d.room===p},
 {id:"game",k:"game",ev:"game",test:d=>{const g=GAMES.find(x=>x.id===(d&&d.id));return !!g&&!g.hidden;},t:()=>"сыграй с Мусей в любую игру",w:"Вкладка «Игры»"},
 {id:"gameid",k:"game",ev:"game",ok:()=>emGames().length>0,par:r=>emPick(r,emGames()),t:p=>`сыграй в «${(GAMES.find(g=>g.id===p)||{n:"игру"}).n}»`,w:"Вкладка «Игры»",test:(d,p)=>!!d&&d.id===p},
 {id:"kaidan",k:"night",ev:"kaidan",t:()=>"прочитай Мусе кайдан на ночь",w:"Спальня → 📜 Кайдан на ночь"},
 {id:"lamp",k:"night",ev:"lamp",test:d=>d===true,t:()=>"погаси андон — пусть Муся вздремнёт",w:"Спальня → 🏮 Погасить андон"},
 {id:"lantern",k:"night",ev:"lantern",test:d=>d===true,t:()=>"зажги каменный фонарь у ворот",w:"Вход → 🏮 Зажечь фонарь"},
 {id:"pray",k:"shrine",ev:"place",test:emPl("pray"),t:()=>"помолись у храма у ворот",w:"Вход → 🙏 Помолиться"},
 {id:"omikuji",k:"shrine",ev:"place",test:emPl("omikuji"),t:()=>"вытяни омикудзи",w:"Вход → 📜 Омикудзи"},
 {id:"koi",k:"pond",ev:"place",test:emPl("koi"),t:()=>"покорми карпов в пруду",w:"Дворик → 🐟 Покормить карпов"},
 {id:"pebble",k:"pond",ev:"place",test:emPl("pebble"),t:()=>"брось в пруд камешек, пусть пойдут круги",w:"Дворик → 🪨 Бросить камешек"},
 {id:"medit",k:"pond",ev:"place",test:emPl("meditate"),t:()=>"посиди с Мусей в тишине у пруда",w:"Дворик → 🍃 Медитация"},
 {id:"act",k:"play",ev:"act",par:r=>emPick(r,Object.keys(EM_ACT)),t:p=>EM_ACT[p],w:"Веранда: игры с Мусей внизу",test:(d,p)=>d===p},
 {id:"guest",k:"guest",ev:"guest",ok:()=>!!S.guest&&S.guest.day===dayKey()&&(S.guest.state==="coming"||S.guest.state==="here"),t:()=>"угости гостя, что придёт к воротам",w:"Вход: гость-ёкай ждёт угощения"}];
const EM_TI={};for(const T of EM_T)EM_TI[T.id]=T;
const EM_RW=["ds_onigiri","ds_dango","ds_mochi","ds_tempura","ds_inari","ds_taiyaki","ds_yakiimo","ds_daifuku","ds_tamagoyaki","v_ichigo","v_kabocha","v_shiitake","v_obaketake","u_ayu","u_unagi"];

// ── state, seeded day rng ──
const emD=()=>S.ext.ema||(S.ext.ema={day:"",w:[],prev:[],bonus:0,streak:0,last:"",best:0,n:0});
function emRng(s){let h=1779033703;for(const c of s)h=Math.imul(h^c.charCodeAt(0),3432918353)>>>0;return()=>{h=h+0x6D2B79F5|0;let t=Math.imul(h^h>>>15,1|h);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
function emPick(r,a){return a[Math.floor(r()*a.length)%a.length];}
function emYest(){const d=today();d.setDate(d.getDate()-1);return dayKey(d);}
const emStreak=()=>{const E=emD();return E.last===dayKey()||E.last===emYest()?E.streak:0;};
const emReady=()=>{const E=emD();return E.day===dayKey()&&E.w.some(w=>w.done&&!w.got);};
const emCap=s=>s.charAt(0).toUpperCase()+s.slice(1);
const emWhere=(T,p)=>typeof T.w==="function"?T.w(p):T.w;
function emKnown(){const o=[];for(const g of GUESTS)if((S.friends[g.id]||{n:0}).n>0)o.push(g.id);
  for(const id in (S.ext.disc||{}).rareguest||{})o.push(id);const V=(S.ext.vis||{}).m||{};for(const id in V)if(V[id]&&V[id].met)o.push(id);
  return [...new Set(o)].filter(id=>EM_YK[id]);}
function emGen(){
  const E=emD(),day=dayKey();if(E.day===day&&E.w.length)return;
  for(const w of E.w)if(w.done&&!w.got)emGive(w,true);   // yesterday's fulfilled but forgotten: given quietly
  const r=emRng(day+"ema"),sh=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(r()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
  let ys=sh(emKnown()).slice(0,3);for(const id of sh(EM_BASIC))if(ys.length<3&&!ys.includes(id))ys.push(id);
  const av=EM_T.filter(T=>{try{return !T.ok||T.ok();}catch(e){return false;}}),prev=E.prev||[],used=new Set(),rw=EM_RW.filter(f=>FOOD[f]),ws=[];
  for(const y of ys){let c=av.filter(T=>!used.has(T.k)&&!prev.includes(T.id));if(!c.length)c=av.filter(T=>!used.has(T.k));if(!c.length)c=av;
    const fav=c.filter(T=>EM_YK[y].lk.includes(T.k)),T=fav.length&&r()<.65?emPick(r,fav):emPick(r,c);used.add(T.k);
    ws.push({t:T.id,p:T.par?T.par(r):null,y,n:0,need:T.n||1,done:0,got:0,r:emPick(r,rw),q:r()<.4?2:1});}
  Object.assign(E,{day,w:ws,prev:ws.map(w=>w.t),bonus:0});emNew=1;save();hubDot();tabDots();if(panelIs("em"))emOpen();
}

// ── fulfilling ──
function emEv(ev,d){
  const E=emD();if(E.day!==dayKey())return;let hit=null,moved=false;
  for(const w of E.w){if(w.done)continue;const T=EM_TI[w.t];if(!T||T.ev!==ev)continue;let ok=true;try{ok=!T.test||T.test(d,w.p);}catch(e){ok=false;}if(!ok)continue;
    w.n++;moved=true;if(w.n>=w.need){w.done=1;hit=w;}}
  if(!moved)return;save();
  if(hit){toast(`🎴 ${EM_YK[hit.y].n}: желание исполнено!`);chime([1318,1568,2093]);hubDot();tabDots();}
  if(panelIs("em"))emOpen();
}
let emNew=0,emMsg="",emSw=-9,emHit=null,emIM=null,emCv=null,emLd=0,emOn=0;
function emHeart(id){const gd=GUESTS.find(g=>g.id===id);if(!gd)return"";const f=S.friends[id]||(S.friends[id]={n:0});f.n++;
  const gift=gd.gifts[[1,3,5].indexOf(f.n)];let s=` · ♥ ${gd.n}`;if(gift&&IT[gift]&&!S.owned.has(gift)){S.owned.add(gift);s+=` и подарок «${IT[gift].n}»`;}
  if(GUESTS.every(g=>(S.friends[g.id]||{n:0}).n>=3))award("friends");return s;}
function emUnique(){const left=EM_ITEMS.filter(id=>!S.owned.has(id));if(!left.length)return null;const id=pick(left);S.owned.add(id);loadItem(id);disc("ema",id);return id;}
function emGive(w,quiet){
  w.got=1;const E=emD();E.n=(E.n||0)+1;give(w.r,w.q);S.needs.joy=clamp(S.needs.joy+5,0,100);
  let s=`${fThumb(w.r,26,20)} ${FOOD[w.r].n} ×${w.q}`+emHeart(w.y);
  if(!quiet&&Math.random()<.1){const u=emUnique();if(u)s+=` · 🎁 «${IT[u].n}»`;}
  return`<div>${EM_YK[w.y].n}: ${s}</div>`;}
function emCollect(){
  const E=emD();if(!emReady())return;let h="";for(const w of E.w)if(w.done&&!w.got)h+=emGive(w);award("em_first");
  if(E.w.length===3&&E.w.every(w=>w.got)&&!E.bonus){E.bonus=1;const st=E.last===emYest()?E.streak+1:E.last===dayKey()?E.streak:1;E.streak=st;E.last=dayKey();E.best=Math.max(E.best||0,st);
    if(st>=3)award("em_s3");if(st>=7)award("em_s7");S.needs.joy=clamp(S.needs.joy+12,0,100);
    const u=(E.best===1&&!EM_ITEMS.some(id=>S.owned.has(id)))||st===3||st===7||Math.random()<.6?emUnique():null;
    if(u)h+=`<div class="em-bt">${itemThumb(IT[u],44,40)}<span>Все три желания! Доска дарит: <b>«${IT[u].n}»</b> — ищи в 🧺 Вещи</span></div>`;
    else{const f=pick(EM_RW.filter(x=>FOOD[x]&&FOOD[x].k==="dish"));give(f,2);h+=`<div class="em-bt">${fThumb(f,40,32)}<span>Все три желания! Бонус: ${FOOD[f].n} ×2</span></div>`;}}
  emMsg=h;save();sfx("coin");chime([1046,1318,1568,2093]);hubDot();tabDots();ui();
  if(S.room==="entrance"&&emHit){for(let i=0;i<4;i++)floatFx.push({g:pick(["✨","🎴","🌸"]),x:emHit[0]+emHit[2]*(.25+.5*Math.random()),y:emHit[1]+emHit[3]*.7,t:now()+i*.12});}
  if(!petAway()){react("😻",2);burst(8);}
}

// ── the panel (wooden plaques) and the hub card ──
document.head.insertAdjacentHTML("beforeend",`<style>
.em-wr{margin:14px 0 4px}.em-wr.done{animation:emGl 1.8s ease-in-out infinite}
@keyframes emGl{0%,100%{filter:drop-shadow(0 0 6px rgba(255,196,110,.55))}50%{filter:drop-shadow(0 0 16px rgba(255,206,130,.95))}}
.em-cd{display:block;width:46px;height:12px;margin:0 auto -3px;border:2px solid #b3322a;border-bottom:none;border-radius:24px 24px 0 0}
.em-pl{position:relative;display:flex;gap:10px;align-items:center;padding:22px 12px 12px;color:#2a1a10;clip-path:polygon(0 18px,50% 0,100% 18px,100% 100%,0 100%);
 background:repeating-linear-gradient(90deg,rgba(80,52,24,.09) 0 2px,transparent 2px 11px),linear-gradient(180deg,#d2b07c,#b8945f 55%,#a07c4c)}
.em-wr.got .em-pl{filter:saturate(.6) brightness(.82)}
.em-pl>img{height:66px;width:58px;object-fit:contain;flex:none;filter:drop-shadow(0 2px 2px rgba(0,0,0,.4))}
.em-tx{flex:1;min-width:0}.em-tx small{display:block;font-size:12px;color:#5a3a20;letter-spacing:.02em}
.em-tx b{display:block;font-size:15px;line-height:1.3;font-weight:600;margin:1px 0 3px}
.em-wh{display:block;font-size:12px;color:#4a2e18}.em-bar{height:5px;background:rgba(60,30,10,.22);border-radius:3px;margin:6px 34px 5px 0;overflow:hidden}
.em-bar>i{display:block;height:100%;background:#8a2a1e;border-radius:3px}
.em-rw{display:flex;align-items:center;gap:5px;font-size:12px;color:#3a2412}
.em-sl{position:absolute;right:10px;bottom:10px;width:27px;height:27px;background:#b8322a;color:#f6e6cc;font-size:16px;display:flex;align-items:center;justify-content:center;border-radius:3px;transform:rotate(-8deg);box-shadow:0 1px 2px rgba(0,0,0,.4)}
.em-bn{margin:14px 0 8px;padding:10px 12px;border:1px dashed var(--line);border-radius:12px;font-size:13px;color:var(--muted)}.em-bn b{color:var(--paper)}
.em-got{margin:8px 0;padding:10px 12px;border-radius:12px;background:rgba(232,190,110,.12);border:1px solid rgba(232,190,110,.35);font-size:13px;line-height:1.6}
.em-got>div{margin:2px 0}.em-got .ath,.em-rw .ath{vertical-align:middle}.em-bt{display:flex;align-items:center;gap:8px;margin-top:6px}
.em-hb{display:block;font-size:13px;line-height:1.45;margin:2px 0}
.em-lk{filter:brightness(0) opacity(.45)}
</style>`);
function emCard(w){
  const T=EM_TI[w.t],Y=EM_YK[w.y];if(!T||!Y)return"";const st=w.got?"got":w.done?"done":"",pc=Math.round(100*Math.min(w.n,w.need)/w.need);
  return`<div class="em-wr ${st}"><i class="em-cd"></i><div class="em-pl"><img src="assets/mon/${Y.m}.webp" alt=""><div class="em-tx"><small>${Y.n} просит:</small>
   <b>«${emCap(T.t(w.p))}. ${Y.tl}»</b><span class="em-wh">${w.got?"✓ Исполнено, дар получен":w.done?"✓ Исполнено — забери дар":emWhere(T,w.p)+(w.need>1?` · ${w.n} из ${w.need}`:"")}</span>
   <div class="em-bar"><i style="width:${pc}%"></i></div><span class="em-rw">Дар: ${fThumb(w.r,26,20)} ${FOOD[w.r].n} ×${w.q}${GUESTS.some(g=>g.id===w.y)?" · ♥ дружба":""}</span></div>${w.done?'<span class="em-sl">叶</span>':""}</div></div>`;}
function emOpen(){
  emGen();const E=emD(),st=emStreak(),rd=emReady(),was=panelIs("em");
  const left=EM_ITEMS.filter(id=>!S.owned.has(id)).length;
  openPanel("Доска эма",`<p class="lead">Ёкаи, которых Муся уже знает, вешают у ворот деревянные таблички эма с маленькими желаниями. Каждый день — три новых. Исполни желание — и забери дар.</p>
   ${emMsg?`<div class="em-got">${emMsg}</div>`:""}${E.w.map(emCard).join("")}
   ${rd?`<div class="row" style="margin:12px 0"><button class="btn primary" data-x="em:take">🎴 Забрать дары</button></div>`:""}
   <div class="em-bn">${E.bonus?"<b>Все три желания исполнены</b> — доска уже сделала сегодня свой подарок ✓":`<b>Все три желания за день</b> — ещё дар от самой доски${left?`: может оказаться одна из вещей «${EM_C}» (осталось ${left} из ${EM_ITEMS.length})`:""}`}.<br>
   Серия: <b>${st}</b> ${st%10===1&&st%100!==11?"день":st%10>=2&&st%10<=4&&(st%100<12||st%100>14)?"дня":"дней"} подряд — штампы за 3 и 7 дней. Исполнено всего: ${E.n||0}.<br>Новые желания появятся завтра.</div>
   <h3 class="bh">${EM_C}</h3><div class="coll">${EM_ITEMS.map(emCi).join("")}</div>`,"em");
  if(!was)$("xpBody").scrollTop=0;emMsg="";}   // openPanel sets scrollTop while hidden → may keep the old panel's scroll
function emCi(id){const own=S.owned.has(id),I=IT[id];return`<div class="ci${own?" on":""}">${itemThumb(I,70,60,own?"":";filter:brightness(0) opacity(.45)")}<small>${own?I.n:"???"}</small></div>`;}
hook("hub",()=>{
  if(!emOn)return"";emGen();const E=emD(),rd=emReady(),dn=E.w.filter(w=>w.done).length;
  return`<div class="hubc"><h4>🎴 Доска эма <i>絵馬</i></h4><p>Желания ёкаев на сегодня — исполнено ${dn} из ${E.w.length}:</p>${E.w.map(w=>{const T=EM_TI[w.t],Y=EM_YK[w.y];
    return`<span class="em-hb">${w.got?"✓":w.done?"✨":"○"} <b>${Y.n}</b>: ${T.t(w.p)}${w.need>1&&!w.done?` (${w.n}/${w.need})`:""}</span>`;}).join("")}
   <div class="row">${rd?'<button class="btn primary" data-x="em:take">🎴 Забрать дары</button>':""}<button class="btn" data-x="em:open">Открыть доску</button></div></div>`;});
hook("click",key=>{if(!key.startsWith("em:"))return false;audioInit();const a=key.slice(3);
  if(a==="take"){emCollect();emOpen();}else if(a==="open")emOpen();return true;});
hook("hubDot",()=>emOn&&emReady());
hook("tabDot",r=>r==="entrance"&&emOn&&emReady());
hook("ev",(ev,d)=>{if(emOn&&ev!=="tick")emEv(ev,d);});
hook("boot",()=>{emOn=1;emGen();});
hook("away",()=>emNew?{i:"🎴",t:"На доске эма у ворот — три новых желания ёкаев"}:null);
hook("sec",()=>{if(!emOn)return;emGen();const E=emD(),T=S.ext.tree;if(T&&T.last===dayKey()&&E.w.some(w=>w.t==="sakura"&&!w.done))emEv("sakura");});
hook("album",el=>{const E=emD();el.insertAdjacentHTML("beforeend",`<h3 class="bh">Доска эма</h3><p class="lead">Исполнено желаний: ${E.n||0}. Лучшая серия: ${E.best||0}. Вещи «${EM_C}»: ${EM_ITEMS.filter(id=>S.owned.has(id)).length} из ${EM_ITEMS.length}.</p><div class="coll">${EM_ITEMS.map(emCi).join("")}</div>`);});

// ── the rack in the entrance: drawn behind Musya, dimmed to the night light; fulfilled plaques glow ──
function emPrep(im){const T=TINT.entrance||"rgba(8,12,14,.42)";emCv={};
  for(const [k,r,tint] of [["rack",EM_A.rack,1],["p0",EM_A.p0,1],["p1",EM_A.p1,1],["p1L",EM_A.p1,0]]){const c=document.createElement("canvas");c.width=r[2];c.height=r[3];const g=c.getContext("2d");
    g.drawImage(im,r[0],r[1],r[2],r[3],0,0,r[2],r[3]);if(tint){g.globalCompositeOperation="source-atop";g.fillStyle=T;g.fillRect(0,0,r[2],r[3]);}emCv[k]=c;}}
hook("draw",(t,front)=>{
  if(front)return;if(S.room!=="entrance"||scene.on||!emOn){emHit=null;return;}
  if(!emCv){if(!emLd){emLd=1;atlasImg("em",im=>{emIM=im;emPrep(im);});}return;}
  const E=emD(),ix=visX(EM_X,110),[sx,ya]=imgToStage(ix,EM_FY-EM_H,CAT_D),[,yb]=imgToStage(ix,EM_FY,CAT_D),h=yb-ya,k=h/400,w=250*k,x0=sx-w/2;
  ctx.save();
  if(X.tv){const qx0=visX(585,60),[qx,qa]=imgToStage(qx0,1050-175,CAT_D),[,qb]=imgToStage(qx0,1050,CAT_D),qh=qb-qa,qw=qh*84/170;   // the post box stands in front
    ctx.beginPath();ctx.rect(0,0,view.W,view.H);ctx.rect(qx-qw/2,qa,qw,qh);ctx.clip("evenodd");}
  ctx.drawImage(emCv.rack,x0,ya,w,h);
  const sw=t>emSw?Math.exp(-(t-emSw)*2.2):0;
  for(let i=0;i<3;i++){const wi=E.w[i];if(!wi)continue;const x=x0+EM_HK[i][0]*k,y=ya+EM_HK[i][1]*k,pw=66*k,ph=64*k,lit=wi.done&&!wi.got;
    if(lit){const pul=.6+.4*Math.sin(t*2.6+i*1.3),R=84*k,cy=y+ph*.55;ctx.save();ctx.globalCompositeOperation="lighter";const gr=ctx.createRadialGradient(x,cy,0,x,cy,R);
      gr.addColorStop(0,`rgba(255,200,120,${.62*pul})`);gr.addColorStop(.45,`rgba(255,170,80,${.22*pul})`);gr.addColorStop(1,"rgba(255,196,110,0)");ctx.fillStyle=gr;ctx.fillRect(x-R,cy-R,R*2,R*2);ctx.restore();
      if(Math.random()<.008)floatFx.push({g:"✨",x:x+(Math.random()-.5)*pw,y:y+ph*Math.random(),t:now()});}
    ctx.save();ctx.translate(x,y);ctx.rotate(Math.sin(t*1.2+i*2.1)*.035+sw*.3*Math.sin(t*11+i*1.7));
    ctx.drawImage(lit?emCv.p1L:wi.done?emCv.p1:emCv.p0,-pw/2,0,pw,ph);ctx.restore();}
  ctx.restore();emHit=[x0,ya,w,h*.78];
});
hook("hit",(x,y)=>{const r=emHit;if(S.room!=="entrance"||!r||scene.on)return false;
  if(x>r[0]&&x<r[0]+r[2]&&y>r[1]&&y<r[1]+r[3]){audioInit();emSw=now();tone(520,.06,"triangle",.05);setTimeout(()=>tone(700,.07,"triangle",.04),90);
    if(emReady())emCollect();emOpen();return true;}return false;});

X.em={D:emD,gen:emGen,ev:emEv,collect:emCollect,open:emOpen,T:EM_T,
  done(i){const w=emD().w[i];if(w){w.n=w.need-1;emEv(EM_TI[w.t].ev,null);if(!w.done){w.n=w.need;w.done=1;save();hubDot();tabDots();}}},
  tap(){const r=emHit;if(!r)return false;const b=cv.getBoundingClientRect();cv.dispatchEvent(new PointerEvent("pointerdown",{clientX:b.left+r[0]+r[2]/2,clientY:b.top+r[1]+r[3]*.6,pointerId:9,bubbles:true}));return true;},
  hit:()=>emHit};
}
