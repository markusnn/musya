{
// ───────────────────────── «Свиток-летопись» (絵巻): the house's history as a hand scroll ─────────────────────────
// Milestones: disc() stamps (S.ext.disc), the day Musya came (S.ext.bd.start), the candle log (X.cd.st.log) and my own
// first-seen stamps for what the core keeps without a date (story chapters, festivals, friends, kaidans, bestiary, crops, fish, dishes).
// Firsts of each kind + round numbers; big events get a scene of their own, small ones of one day share a scene; ≤ 40 scenes
// (+10 for every full year). Read right → left: the title at the right end, the newest scene at the left end (fresh ink).
// S.ext.chronicle = {ts:{key:realMs|0 (0 = before the chronicle began)}, init:ms, seen:game ms of the newest event at the last
//   unrolling, od:dayKey of the last unrolling (the 家 dot at most once a day), n:unrollings}
const RK=S.ext.chronicle||(S.ext.chronicle={ts:{},init:0,seen:0,od:"",n:0});RK.ts=RK.ts||{};
STAMPS.push(["rk_open","巻","Летописец","Разверни свиток-летопись дома (家 → Свиток-летопись)"],["rk_25","絵","Двадцать пять сцен","Пусть на свитке дома наберётся 25 сцен"],
 ["rk_year","年","Целый год","Свиток помнит целый год жизни дома"]);
document.head.insertAdjacentHTML("beforeend",`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Kurale&display=swap"><style>
#xpBody .rk-wrap{margin:2px -16px 8px;position:relative}
.rk-cv{display:block;width:100%;height:520px;touch-action:pan-y;cursor:grab;background:#0b0907;user-select:none;-webkit-user-select:none}
#xpBody p.rk-cap{font-family:"Kurale",var(--display);font-size:16.5px;line-height:1.45;color:var(--paper);margin:2px 0 4px;min-height:4.3em}
#xpBody p.rk-cap b{color:#e8b77a;font-weight:400}#xpBody p.rk-n{font-size:12.5px;color:var(--muted);margin:0 0 10px}#xpBody p.rk-n i{font-style:normal;color:#e0574a}
.rk-row{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 6px}.rk-row .btn{flex:1 1 auto}
.rk-ci .rk-cat{display:block;width:52px;height:56px;background-size:416px 56px;background-repeat:no-repeat}.rk-ci small{font-size:11px;color:var(--muted);line-height:1.2}
.rk-ci.nw{border-color:#b8432f}</style>`);

// ── helpers ──
const RK_MON=["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"];
const rkPl=(n,a,b,c)=>{const d=n%10,h=n%100;return d===1&&h!==11?a:d>=2&&d<=4&&(h<12||h>14)?b:c;};
const rkLc=s=>s?s.charAt(0).toLowerCase()+s.slice(1):s;
function rkH(s){let h=2166136261;s=String(s);for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619);}return h>>>0;}
function rkR(sd){let s=sd>>>0;return()=>{s=(s+0x6D2B79F5)>>>0;let t=s;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return((t^t>>>14)>>>0)/4294967296;};}
const rkMk=(w,h)=>{const c=document.createElement("canvas");c.width=Math.max(1,Math.round(w));c.height=Math.max(1,Math.round(h));return c;};
const rkDate=g=>{const d=new Date(g);return d.getDate()+" "+RK_MON[d.getMonth()]+" "+d.getFullYear();};
const rkBest=id=>BESTIARY.find(b=>b[0]===id||b[0]==="rg_"+id||b[0]==="vs_"+id||b[1]===id);

// ── what the core keeps without a date: stamp it the first time I see it (from the candle log if it knows better) ──
function rkCore(){const o=[];
  for(let k=0;k<Math.min(QS.ch,STORY.length);k++)o.push("q:"+k);
  for(const k in S.fest)if(S.fest[k]&&S.fest[k].done&&/-\d{4}$/.test(k))o.push("fe:"+k);
  for(const g of GUESTS)if((S.friends[g.id]||{}).n>0)o.push("g:"+g.id);
  for(const i of ST.stories)if(KAIDAN[i])o.push("k:"+i);
  for(const b of ST.seen)o.push("b:"+b);
  for(const c of CROPS)if(S.crops[c.id])o.push("c:"+c.id);
  for(const f of FISHES)if(!f.junk&&S.catch[f.id])o.push("f:"+f.id);
  for(const r of RECIPES)if(S.cooked[r.id])o.push("r:"+r.id);
  return o;}
function rkTrack(){const quiet=!RK.init,L=(X.cd&&X.cd.st&&X.cd.st.log)||[],cdT={};let add=0;for(const [k,t] of L)if(t&&typeof k==="string")cdT[k]=t;
  for(const k of rkCore()){if(k in RK.ts)continue;let t=cdT[k.startsWith("fe:")?k.replace(/-\d{4}$/,""):k]||0;
    if(t&&k.startsWith("fe:")&&String(new Date(t+DATE_SHIFT).getFullYear())!==k.slice(-4))t=0;
    if(!t&&quiet&&k.startsWith("fe:")){const m=k.slice(3).match(/^(.*)-(\d{4})$/),F=m&&FEST.find(F=>F.id===m[1]);   // an old festival: its first day
      if(F&&F.from){const d=new Date(+m[2],F.from[0]-1,F.from[1],19).getTime();if(d<=Date.now()+DATE_SHIFT)t=d-DATE_SHIFT;}}
    RK.ts[k]=t||(quiet?0:Date.now());add++;}
  if(!RK.init){RK.init=Date.now();add++;}if(add)rkMemo=null;return add;}

// ── events → milestones → scenes ──
const RK_SKIP={chronicle:1,news:1};
// the second and third story books (their chapters: X.story2.CH, X.story3.CH)
const RK_BOOK={chapter2:["Кошачья гора",()=>(X.story2&&X.story2.CH)||[]],chapter3:["Шпилька Бэни",()=>(X.story3&&X.story3.CH)||[]]};
const RK_MAJ={room:10,q:9,chapter2:9,chapter3:9,fe:8,holiday:8,birthday:9,rareguest:8,capsule:7,bloom:7,trust:6,season:6,snow:7,parade:7};
const RK_FIRST1={haunt:6,postcard:6,dream:5,visitor:5,rumor:5,chest:6,kimo:5,forest:5,nurikabe:5,
  cat:6,insect:5,sumo:6,kite:5,rice:6,loom:6,haiku:5,mystery:6,music:4,hide:4,kamidana:5};
// every next one of these small collections still gets a line in its day's scene
const RK_EACH={cat:3,sumo:3,chest:3,mystery:3,music:2,kite:2,loom:2,rice:3};
// special milestones: a scene of their own
const rkSpec=e=>{const {kind,id,n}=e;return kind==="cat"&&n===8?7:kind==="sumo"&&id==="yokozuna"?8:kind==="chest"&&id==="w12"?8:kind==="chest"&&id==="w6"?6:
  kind==="kamidana"&&id==="d30"?7:kind==="kamidana"&&id==="d7"?5:kind==="music"&&n===7?6:kind==="mystery"&&n===8?7:kind==="kite"&&n===9?6:kind==="nurikabe"&&n===20?6:0;};
const RK_RND=[10,25,50,100,200,500],RK_TOT=[50,100,200,300,500,1000];
function rkStart(E){const B=S.ext.bd||{};let s=B.start&&/^\d{4}-\d\d-\d\d$/.test(B.start)?Date.parse(B.start+"T09:00:00"):0;
  if(!s)s=(RK.init||Date.now())+DATE_SHIFT;for(const e of E)if(e.g&&e.g<=s)s=e.g-60000;return s;}
function rkEvents(){const D=S.ext.disc||{},E=[],hol=D.holiday||{};
  for(const kind in D){if(RK_SKIP[kind])continue;for(const id in D[kind]){const t=D[kind][id];if(typeof t==="number"&&t>0)E.push({k:"d:"+kind+":"+id,kind,id,g:t+DATE_SHIFT});}}
  for(const k in RK.ts){const i=k.indexOf(":"),kind=k.slice(0,i),id=k.slice(i+1),t=RK.ts[k];
    if(kind==="fe"){const m=id.match(/^(.*)-(\d{4})$/);if(m&&hol[m[1]]&&String(new Date(hol[m[1]]+DATE_SHIFT).getFullYear())===m[2])continue;}
    E.push({k,kind,id,g:t?t+DATE_SHIFT:0});}
  const st=rkStart(E);let u=0;for(const e of E)if(!e.g){e.u=1;e.g=st+60000*(++u);}   // undated: right after the start, in their natural order
  E.sort((a,b)=>a.g-b.g);E.unshift({k:"start",kind:"start",id:"",g:st});
  const cnt={};let tot=0;for(const e of E){if(e.kind!=="start"){e.n=cnt[e.kind]=(cnt[e.kind]||0)+1;tot++;if(RK_TOT.includes(tot))e.tot=tot;}rkCls(e);}
  return E;}
function rkCls(e){const {kind,id,n}=e;let w=-1,m=0;
  if(kind==="start"){w=20;m=1;}
  else if(kind==="pet"){w=id==="pt1"?12:7;m=1;}
  else if(kind==="crane"){const v=+String(id).slice(1)||0;w=v>=1000?10:v>=100?9:v===1?5:4;m=v>=100?1:0;}
  else if(kind==="g"){w=n===1?9:5;m=n===1?1:0;}
  else if(kind==="friend"){if(/_5$/.test(id)){w=7;m=1;}else if(n===1)w=4;}
  else if(RK_MAJ[kind]){w=RK_MAJ[kind];m=1;}
  else if(RK_FIRST1[kind]&&n===1){w=RK_FIRST1[kind];m=1;}
  else if(rkSpec(e)){w=rkSpec(e);m=1;e.sp=1;}
  else if(n===1)w=4;
  else if(RK_EACH[kind])w=RK_EACH[kind];
  else if(RK_RND.includes(n)&&RK_RN[kind]){w=n>=50?4:3;e.r=1;}
  if(e.tot&&w<5)w=5;e.w=w;e.m=m;}
function rkBuild(){const E=rkEvents(),sc=[],day={},dk=e=>e.u?"u":dayKey(new Date(e.g)),D=k=>day[k]||(day[k]={maj:null,sm:null,more:0,last:null});
  const mk=e=>({ev:[e],main:e,w:e.w,g:e.g,gm:e.g,u:e.u,more:0});
  for(const e of E)if(e.w>=0&&e.m){const s=mk(e),d=D(dk(e));sc.push(s);if(!d.maj)d.maj=s;}
  for(const e of E){if(e.m&&e.w>=0)continue;const d=D(dk(e));if(e.w<0){d.more++;continue;}
    const s=d.maj||d.sm;if(s){s.ev.push(e);s.gm=Math.max(s.gm,e.g);if(!s.main.m&&e.w>s.main.w)s.main=e;s.w=Math.max(s.w,e.w)+.2;}
    else{const n=mk(e);sc.push(n);d.sm=n;}}
  sc.sort((a,b)=>a.g-b.g);for(const s of sc){const d=D(s.u?"u":dayKey(new Date(s.g)));d.last=s;}for(const k in day)if(day[k].last)day[k].last.more=day[k].more;
  const cap=rkCapN(E[0].g);let out=sc;if(sc.length>cap){const keep=new Set([sc[0],sc[sc.length-1]]);for(const s of [...sc].sort((a,b)=>b.w-a.w||b.g-a.g)){if(keep.size>=cap)break;keep.add(s);}out=sc.filter(s=>keep.has(s));}
  out.forEach((s,i)=>{s.i=i;s.key=s.main.k+"|"+s.ev.length+"|"+s.more;});return out;}
const rkCapN=st=>40+10*Math.max(0,Math.floor((Date.now()+DATE_SHIFT-st)/(365*864e5)));
let rkMemo=null,rkMemoT=0;
function rkScenes(){if(rkMemo&&performance.now()-rkMemoT<3000)return rkMemo;rkMemo=rkBuild();rkMemoT=performance.now();return rkMemo;}
const rkNewN=()=>rkScenes().filter(s=>s.gm>RK.seen).length;
const rkYear=()=>{const sc=rkScenes();return sc.length&&Date.now()+DATE_SHIFT-sc[0].g>=365*864e5;};

// ── words ──
const rkNK=(kind,id)=>{try{return X.sb&&X.sb.nk?X.sb.nk(kind,id):null;}catch(x){return null;}};
function rkName(kind,id){try{const q=rkNK(kind,id);if(q&&q.n)return q.n;
  if(kind==="q")return(STORY[+id]||{}).title||"";if(kind==="k")return(KAIDAN[+id]||{}).t||"";
  if(RK_BOOK[kind]){const C=RK_BOOK[kind][1]();const c=C&&C[+id];if(c&&c.title)return c.title;}
  if(kind==="fe"||kind==="holiday"){const f=kind==="fe"?String(id).replace(/-\d{4}$/,""):id;return(FEST.find(F=>F.id===f)||{}).n||"";}
  if(kind==="c")return(CROPS.find(c=>c.id===id)||{}).n||"";if(kind==="f")return(FOOD[id]||{}).n||"";if(kind==="r")return(RECIPES.find(r=>r.id===id)||{}).n||"";
  if(kind==="room")return(ROOMS.find(r=>r.id===id)||{}).ru||"";if(kind==="pet")return(S.ext.pet2||{}).name||"";
  if(kind==="trust"&&X.ts)return X.ts.name(id)||"";if(kind==="kanji")return id;
  const gs=GUESTS.find(q=>q.id===id||q.id===String(id).split("_")[0]);if(gs&&/^(g|friend|rareguest|ryokan|tea|serial)$/.test(kind))return gs.n;
  const b=rkBest(id);if(b)return b[2];const h=X[kind];if(h&&typeof h.name==="function"){const v=h.name(id);if(v)return v;}
  if(IT[id])return IT[id].n;if(FOOD[id])return FOOD[id].n;
  if(X.cd&&X.cd.label){const L=X.cd.label("d:"+kind+":"+id),i=L.indexOf(": ");if(i>0)return L.slice(i+2);}}catch(x){}return"";}
const RK_RN={find:N=>`Муся принесла в дом уже ${N}-ю находку`,k:N=>`у очага прочитан ${N}-й кайдан`,b:N=>`в бестиарии уже ${N} ${rkPl(N,"ёкай","ёкая","ёкаев")}`,
  bird:N=>`у кормушки побывало уже ${N} ${rkPl(N,"разная птица","разные птицы","разных птиц")}`,koi:N=>`в пруду уже ${N} ${rkPl(N,"карп","карпа","карпов")}`,
  insect:N=>`в коллекции насекомых уже ${N} ${rkPl(N,"находка","находки","находок")}`,figure:N=>`на полке уже ${N} ${rkPl(N,"фигурка","фигурки","фигурок")} из гатяпона`,
  kanji:N=>`выучено уже ${N} ${rkPl(N,"иероглиф","иероглифа","иероглифов")}`,c:N=>`на грядках выросло уже ${N} ${rkPl(N,"растение","растения","растений")}`,
  f:N=>`поймано уже ${N} ${rkPl(N,"вид","вида","видов")} рыбы`,r:N=>`освоено уже ${N} ${rkPl(N,"блюдо","блюда","блюд")}`,g:N=>`у дома уже ${N} ${rkPl(N,"друг","друга","друзей")}`,
  friend:N=>`от друзей пришло уже ${N} ${rkPl(N,"письмо","письма","писем")}`,visitor:N=>`на вещи в доме пришло уже ${N} ${rkPl(N,"ёкай","ёкая","ёкаев")}`,
  ema:N=>`доска эма принесла уже ${N} ${rkPl(N,"дар","дара","даров")}`,star:N=>`в небе над домом замечено уже ${N} ${rkPl(N,"звёздное чудо","звёздных чуда","звёздных чудес")}`};
const RK_F={find:n=>`Муся впервые принесла в дом находку${n?` — «${n}»`:""}`,k:n=>`у очага прочитан первый кайдан${n?` — «${n}»`:""}`,
  b:n=>`в бестиарий записан первый ёкай${n?` — ${n}`:""}`,c:n=>`собран первый урожай${n?` — ${rkLc(n)}`:""}`,f:n=>`поймана первая рыба${n?` — ${rkLc(n)}`:""}`,
  r:n=>`приготовлено первое блюдо${n?` — «${n}»`:""}`,bird:n=>`к кормушке прилетела первая птица${n?` — ${rkLc(n)}`:""}`,koi:n=>`в кадке поселился первый карп${n?` — ${n}`:""}`,
  insect:n=>`в сачок попалась первая добыча${n?` — ${rkLc(n)}`:""}`,figure:n=>`из гатяпона выпала первая фигурка${n?` — «${n}»`:""}`,
  visitor:n=>`на вещи в доме впервые пришёл ёкай${n?` — ${n}`:""}`,rumor:n=>`подтвердился первый слух${n?` — «${n}»`:""}`,dream:()=>`Мусе приснился первый вещий сон`,
  haunt:n=>`в доме поселился дух${n?` — ${n}`:""}`,postcard:n=>`Муся отправилась в путешествие и прислала открытку${n?` «${n}»`:""}`,
  souvenir:n=>`из путешествия привезён первый сувенир${n?` — «${n}»`:""}`,kanji:n=>`выучен первый иероглиф — ${n}`,ema:n=>`доска эма впервые принесла дар${n?` — «${n}»`:""}`,
  craft:n=>`в мастерской сделана первая поделка${n?` — «${n}»`:""}`,hanafuda:()=>`сыграна первая партия в ханафуда`,serial:()=>`лиса у очага начала рассказывать кайдан с продолжением`,
  ryokan:n=>`в рёкане остановился первый постоялец${n?` — ${n}`:""}`,shop:n=>`первая покупка в лавке тануки${n?` — «${n}»`:""}`,daruma:()=>`дарума впервые исполнил желание`,
  bonsai:()=>`бонсай на веранде обрёл первую форму`,ikebana:()=>`в токономе появилась первая икебана`,tea:()=>`в доме прошла первая чайная церемония`,
  shadow:n=>`теневой театр сыграл первый спектакль${n?` — «${n}»`:""}`,paint:()=>`Муся нарисовала первую картину`,cat:n=>`на заборе впервые показался соседский кот${n?` — ${n}`:""}`,
  mystery:()=>`раскрыта первая пропажа в доме`,music:()=>`в доме впервые зазвучала музыка`,hide:()=>`Муся впервые сыграла в прятки`,kimo:()=>`первая ночная прогулка смелости — кимодамэси`,
  sumo:()=>`прошёл первый поединок сумо`,kamidana:()=>`на домашнем алтаре впервые зажгли огонёк`,haiku:()=>`сложено первое хайку`,snow:()=>`выпал первый снег`,
  loom:()=>`на станке соткана первая ткань`,rice:()=>`собран первый рис`,kite:()=>`в небо поднялся первый воздушный змей`,chest:()=>`открыт сундук прабабушки`,
  nurikabe:()=>`ночью дорогу преградила нурикабэ`,forest:n=>`первая прогулка в лес за тории${n?` — ${rkLc(n)}`:""}`,star:()=>`над домом пролетела первая падающая звезда`};
const RK_SEA={winter:"пришла зима: на веранде и тории лежит снег",spring:"пришла весна: на ветках набухли почки",summer:"пришло лето: в саду звенят цикады",autumn:"пришла осень: клёны у ворот покраснели"};
function rkBd(id){id=String(id);let m;if(/^w/.test(id))return"неделя вместе";if(id==="d100")return"сто дней вместе";if(id==="h")return"полгода вместе";
  if((m=id.match(/^m(\d+)$/)))return+m[1]===1?"месяц вместе":`${m[1]} ${rkPl(+m[1],"месяц","месяца","месяцев")} вместе`;if((m=id.match(/^y(\d+)$/)))return+m[1]===1?"год вместе — день рождения Муси":`${m[1]} ${rkPl(+m[1],"год","года","лет")} вместе — день рождения Муси`;return"праздник Муси";}
Object.assign(RK_RN,{nurikabe:N=>`у ворот разгадано уже ${N} ${rkPl(N,"загадка","загадки","загадок")} нурикабэ`,haiku:N=>`в тетради уже ${N} хайку`,
  hide:N=>`Мусю нашли уже в ${N} ${rkPl(N,"укромном месте","укромных местах","укромных местах")}`,kamidana:N=>`у камиданы получено уже ${N} ${rkPl(N,"благословение","благословения","благословений")}`});
// the newer add-ons: the first one, every next one and the special ones (names and grammar from the newspaper's table)
function rkSayNK(e){const {kind,id}=e,q=rkNK(kind,id),first=e.n===1;if(!q)return null;const n=q.n||"";
  switch(kind){
   case"cat":return e.sp?`теперь Муся знакома со всеми восемью соседскими кошками — последн${q.f?"ей":"им"} ${q.f?"пришла":"пришёл"} ${n}`:
     first?`Муся познакомилась с ${q.f?"первой соседкой":"первым соседом"} — ${n}, ${q.whoI}`:`новое знакомство на заборе: ${n}, ${q.who}`;
   case"insect":return first?`в сачок попалась первая добыча — ${rkLc(n)}`:null;
   case"sumo":return q.yk?`Муся одолела на басё самого ${q.acc} — кубок императора теперь стоит дома`:first?`первая победа на ночном басё у реки — над ${q.ins}`:`победа на басё над ${q.ins}`;
   case"nurikabe":return e.sp?"у ворот разгадано двадцать загадок нурикабэ — стена зовёт Мусю умной кошкой":first?`у ворот выросла стена-нурикабэ и загадала загадку: «${n}» Муся ответила верно, и стена ушла в землю`:null;
   case"kite":return e.sp?"в небе побывали все девять воздушных змеев":first?`в небо над крышами поднялся первый воздушный змей${n?` — ${n}`:""}`:`взлетел новый змей${n?` — ${n}`:""}`;
   case"rice":return first?"собран первый урожай риса с террас на холме: снопы сохнут на хасагакэ":`собран ${q.n}`;
   case"loom":return first?`на станке в куре соткан первый отрез — узор «${n}»${q.kim?", и из него сшито первое своё кимоно Муси":""}`:`соткан новый узор — «${n}»`;
   case"chest":return id==="w12"?"сундук прабабушки опустел: история Хару прочитана до последней строчки":first?`в сундуке прабабушки нашлась первая вещь — «${n}», ${q.y} год`:
     `сундук прабабушки отдал ещё одну вещь — «${n}», ${q.y} год`;
   case"haiku":return first?(q.x?`на веранде повешено первое хайку: «${q.x.join(" / ")}»`:"на веранде повешено первое хайку"):null;
   case"mystery":return e.sp?"раскрыты все восемь дел о пропажах в доме":first?`раскрыто первое дело о пропаже — «${n}»: вещь брал${q.f?"а":""} ${q.cul}`:`раскрыто «${n}»`;
   case"music":return e.sp?"в доме собраны все семь старинных мелодий":first?`в доме впервые зазвучала музыка — мелодия «${n}»`:`граммофон выучил мелодию «${n}»`;
   case"hide":return first?`Муся впервые сыграла в прятки и спряталась ${n||"где-то в доме"}`:null;
   case"kamidana":return id==="d30"?"месяц утренних подношений у камиданы подряд":id==="d7"?"неделя утренних подношений у камиданы подряд":
     first?`на кухонной камидане сделано первое утреннее подношение — ками послали «${n}»`:null;
   case"kimo":return first?`первая ночная прогулка смелости — кимодамэси; звание — «${n}»`:null;
   case"snow":return q.km?"во дворе игр построена камакура — снежный домик со свечой внутри":`во дворе игр слеплен ${first?"первый ":""}снеговик`;}
  return null;}
function rkSay(e){const {kind,id}=e,n=rkName(kind,id);let s;
  if(e.r)s=RK_RN[kind](e.n);
  else if((s=rkSayNK(e))){}
  else switch(kind){
   case"start":s="Муся пришла в дом. В пустых комнатах снова зажглись фонари";break;
   case"room":s=`открылась ${n?`комната «${n}»`:"новая комната"}. Муся первой обнюхала все углы`;break;
   case"q":{const t=String(n).match(/^(Глава \d+|Пролог|Эпилог)\.\s*(.+)$/),p=t?`${t[1].startsWith("Глава")?"пройдена":"пройден"} ${rkLc(t[1])} — «${t[2]}»`:`пройдена глава «${n}»`;
     s=+id===0?`началась история дома: ${p}`:+id===STORY.length-1?`история дома дописана: ${p}`:p;break;}
   case"chapter2":case"chapter3":{const B=RK_BOOK[kind],t=String(n).match(/^(Глава \d+|Пролог|Эпилог)\.\s*(.+)$/);
     s=t?`${t[1].startsWith("Глава")?"пройдена":"пройден"} ${rkLc(t[1])} истории «${B[0]}» — «${t[2]}»`:`новая глава истории «${B[0]}»${n?` — «${n}»`:""}`;break;}
   case"fe":case"holiday":s=`в доме праздновали ${n?`«${n}»`:"праздник"}: фонари, сладости и гости`;break;
   case"birthday":s=`праздник в доме: ${rkBd(id)}`;break;
   case"rareguest":s=`к дому заглянул редкий гость${n?` — ${n}`:""}`;break;
   case"capsule":s="открылась капсула времени — письмо из прошлого дошло";break;
   case"bloom":s="зацвела сакура во дворике";break;
   case"trust":s=`Муся стала доверять больше${n?`: «${n}»`:""}`;break;
   case"season":s=RK_SEA[Object.keys(RK_SEA).find(k=>String(id).startsWith(k))]||"пришла новая пора года";break;
   case"parade":s="мимо ворот прошёл ночной парад ста духов";break;
   case"pet":s=id==="pt1"?`в доме появился котёнок${n?` по имени ${n}`:""}`:id==="pt4"?`котёнок${n?` ${n}`:""} совсем вырос`:`котёнок${n?` ${n}`:""} подрос`;break;
   case"crane":{const v=+String(id).slice(1)||0;s=v===1?"сложен первый бумажный журавлик":v>=1000?"сложена тысяча журавликов — загадано желание":v===100?"на нити повис сотый журавлик":`журавликов уже ${v}`;break;}
   case"g":s=e.n===1?`у ворот появился первый друг — ${n}`:`подружились с гостем — ${n}`;break;
   case"friend":s=/_5$/.test(id)?`в гости после долгой переписки пришёл друг — ${n}`:`пришло первое письмо от друга — ${n}`;break;
   default:{const f=RK_F[kind];s=e.n===1&&f?f(n):e.tot?"":rkLc(n||"новая находка");}}
  if(e.tot)s=(s?s+". ":"")+`Это уже ${e.tot}-е открытие в доме`;return s;}
function rkText(s){const m=s.main,ex=s.ev.filter(e=>e!==m).sort((a,b)=>b.w-a.w);let t=rkSay(m)+".";
  const xs=ex.slice(0,3).map(rkSay).filter(Boolean);if(xs.length)t+=` А ещё ${xs.join("; ")}.`;
  const k=s.more+Math.max(0,ex.length-3);if(k)t+=` И ещё ${k} ${rkPl(k,"событие","события","событий")} ${s.u?"в те дни":"за день"}.`;return t;}
const rkWhen=s=>s.u?"В первые дни в доме":rkDate(s.g);

// ── pictures: monsters, things, food, Musya's own frames, the kitten; plus a painted motif ──
// the newer add-ons: their picture (from the newspaper's table) + Musya's frame + a motif
const RK_NKP={cat:[["rest",2],"moon",.24],insect:[["gaze9",3],"sea",.13],mystery:[["gaze9",2],"moon"],sumo:[["highfive",3],"torii"],nurikabe:[null,"torii"],kite:[["gaze9",0],"moon"],
  rice:[["treat",1],"br_autumn"],loom:[["stretch",2],"house"],chest:[["gift",2],"house"],haiku:[["gaze10",1],"scroll"],kimo:[["hide",2],"lantern"],snow:[["stretch",2],"br_winter"],
  hide:[["box",3],"house"],music:[["purr",2],"moon"],kamidana:[["rest",2],"torii"]};
const rkSeaMot=g=>{const m=new Date(g).getMonth()+1;return"br_"+(m===12||m<3?"winter":m<6?"spring":m<9?"summer":"autumn");};
function rkPicNK(e){const P=RK_NKP[e.kind];if(!P)return null;const q=rkNK(e.kind,e.id);if(!q||!q.p)return null;const p=q.p,o={mot:P[1]==="sea"?rkSeaMot(e.g):P[1]};
  if(p.mon&&!P[0])o.mon=p.mon;else if(p.mon)o.mon2=p.mon;if(p.it&&IT[p.it])o.it=p.it;if(p.atl){o.atl=p.atl;o.ah=P[2]||.2;}if(p.cv)o.cv=p.cv;if(P[0])o.cat=P[0];else if(p.cat)o.cat=p.cat;return o;}
function rkPic(e){const {kind,id}=e,M=m=>m&&MIMG[m]?m:null;const nk=rkPicNK(e);if(nk)return nk;
  switch(kind){
   case"start":return{cat:["rest",2],mot:"house"};case"room":return{cat:["moveLeft",3],mot:"house"};
   case"q":{const C=STORY[+id]||{},ch=((C.intro||{}).chars||[])[0],m=ch&&typeof ch.id==="string"&&M(ch.id);return m?{mon:m,mot:"scroll"}:{cat:["gaze9",0],it:C.reward&&IT[C.reward]?C.reward:null,mot:"scroll"};}
   case"chapter2":case"chapter3":return{cat:["gaze10",0],mot:"scroll"};case"fe":case"holiday":return{cat:["highfive",3],mot:"lantern"};
   case"birthday":return{cat:["treat",2],mot:"lantern"};case"season":return{cat:["butterfly",2],mot:"br_"+String(id).split("-")[0]};
   case"snow":return{cat:["stretch",2],mot:"br_winter"};case"bloom":return{cat:["butterfly",4],mot:"br_spring"};
   case"pet":return{kit:1,cat:["rest",0],mot:"house"};case"crane":return{cat:["play",1],mot:"crane"};case"trust":return{cat:["purr",2],mot:"moon"};
   case"capsule":return{cat:["box",3],mot:"house"};case"c":return{food:FOOD["v_"+id]?"v_"+id:null,cat:["treat",1],mot:"br_summer"};
   case"f":return{food:id,cat:["treat",1],mot:"wave"};case"r":{const R=RECIPES.find(r=>r.id===id);return{food:R&&R.dish,cat:["treat",1],mot:"moon"};}
   case"koi":return{cat:["gaze10",2],mot:"wave"};case"bird":return{cat:["gaze9",3],mot:"br_autumn"};case"kanji":case"haiku":case"k":return{cat:["gaze10",1],mot:"scroll"};}
  const g=GUESTS.find(q=>q.id===id||q.id===String(id).split("_")[0]);if(g&&M(g.mon))return{mon:g.mon,mot:"moon"};
  const b=rkBest(id);if(b&&M(b[1]))return{mon:b[1],mot:kind==="parade"?"torii":"moon"};
  if(M(id))return{mon:id,mot:"torii"};if(IT[id])return{it:id,cat:["gift",2],mot:"moon"};if(FOOD[id])return{food:id,mot:"moon"};
  const h=rkH(e.k);return{cat:[["groom",1],["gaze9",4],["knead",2],["yarn",3]][h%4],mot:["moon","br_autumn","scroll"][h%3]};}
let rkPend=0;
function rkSrc(p,what){try{
  if(what==="mon"){const im=MIMG[p.mon];return im?{im,sx:0,sy:0,sw:im.width,sh:im.height}:null;}
  if(what==="it"){const c=DIMG[p.it];if(c&&c.width)return{im:c,sx:0,sy:0,sw:c.width,sh:c.height};loadItem(p.it);rkPend=1;return null;}
  if(what==="food"){const A=fAtlas(p.food);if(!A)return null;const im=FIMG[A[0]];if(!im){fLoad(A[0]);rkPend=1;return null;}const r=A[1].r[p.food];return{im,sx:r[0],sy:r[1],sw:r[2],sh:r[3]};}
  if(what==="cat"){const im=IMG[p.cat[0]];if(!im){rkPend=1;return null;}return{im,sx:p.cat[1]*384,sy:0,sw:384,sh:416};}
  if(what==="kit"){const im=MIMG.m_pt_atlas;return im?{im,sx:0,sy:0,sw:280,sh:250}:null;}
  if(what==="mon2"){const im=MIMG[p.mon2];return im&&im.width?{im,sx:0,sy:0,sw:im.width,sh:im.height}:null;}
  if(what==="atl"){const [k,r]=p.atl;let im=null;atlasImg(k,x=>{im=x;});if(!im){rkPend=1;return null;}return{im,sx:r[0],sy:r[1],sw:r[2],sh:r[3]};}
  if(what==="cv"){const c=p.cv;return c&&c.width?{im:c,sx:0,sy:0,sw:c.width,sh:c.height}:null;}}catch(x){}return null;}
function rkPicHtml(e){const p=rkPic(e);try{if(p.mon||p.mon2)return`<img src="assets/mon/${p.mon||p.mon2}.webp" alt="" style="max-height:56px;max-width:62px">`;
  if((p.atl||p.cv)&&X.sb&&X.sb.pic){const h=X.sb.pic(p.atl?{atl:p.atl}:{cv:p.cv},52);if(h)return h;}
  if(p.it&&IT[p.it])return itemThumb(IT[p.it],56,56);if(p.food){const h=fThumb(p.food,56,56);if(h)return h;}}catch(x){}
  const c=p.cat||["rest",0];return`<span class="rk-cat" style="background-image:url(assets/${c[0]}@2x.webp);background-position:-${c[1]*52}px 0"></span>`;}

// ── painting on the scroll ──
let rkPaper=null,rkGrain=null,rkSealC=null,rkSh=null,rkFont=false;
const RK_INK="#24170e",RK_FONT=`"Kurale","PT Serif",Georgia,serif`,RK_JP=`"Hiragino Mincho ProN","Yu Mincho","Noto Serif JP",serif`;
function rkTex(){if(rkPaper)return;const r=rkR(7),P=rkMk(256,256),g=P.getContext("2d"),im=g.createImageData(256,256),d=im.data;
  for(let i=0;i<d.length;i+=4){const n=(r()-.5)*15+(r()<.015?-16:0);d[i]=213+n;d[i+1]=194+n*.95;d[i+2]=154+n*.8;d[i+3]=255;}g.putImageData(im,0,0);
  for(let i=0;i<8;i++){const x=r()*256,y=r()*256,R=12+r()*42;for(const ox of [-256,0,256])for(const oy of [-256,0,256]){const q=g.createRadialGradient(x+ox,y+oy,0,x+ox,y+oy,R);
    q.addColorStop(0,"rgba(140,96,48,.10)");q.addColorStop(.7,"rgba(140,96,48,.035)");q.addColorStop(1,"rgba(140,96,48,0)");g.fillStyle=q;g.fillRect(x+ox-R,y+oy-R,2*R,2*R);}}
  g.lineCap="round";for(let i=0;i<150;i++){const x=r()*256,y=r()*256,a=r()*Math.PI,l=6+r()*22;g.strokeStyle=`rgba(${r()<.5?"110,84,52":"250,240,214"},${.05+r()*.08})`;g.lineWidth=.4+r()*.8;
    g.beginPath();g.moveTo(x,y);g.quadraticCurveTo(x+Math.cos(a)*l*.5+r()*4-2,y+Math.sin(a)*l*.5+r()*4-2,x+Math.cos(a)*l,y+Math.sin(a)*l);g.stroke();}
  rkPaper=P;const G=rkMk(128,128),gg=G.getContext("2d"),gi=gg.createImageData(128,128),gd=gi.data;for(let i=0;i<gd.length;i+=4){const v=60+r()*136;gd[i]=gd[i+1]=gd[i+2]=v;gd[i+3]=255;}gg.putImageData(gi,0,0);rkGrain=G;}
function rkSeal(dpr){const s=46,c=rkMk(s*dpr,s*dpr),g=c.getContext("2d"),r=rkR(55);g.scale(dpr,dpr);g.translate(s/2,s/2);g.rotate(-.1);
  g.fillStyle="rgba(186,44,32,.93)";g.beginPath();g.roundRect(-18,-18,36,36,5);g.fill();g.globalCompositeOperation="destination-out";
  g.font=`700 25px ${RK_JP}`;g.textAlign="center";g.textBaseline="middle";g.fillText("新",0,1.5);g.lineWidth=1.5;g.beginPath();g.roundRect(-14.5,-14.5,29,29,3);g.stroke();
  for(let i=0;i<90;i++){g.globalAlpha=.25+r()*.75;const z=.4+r()*1.4;g.fillRect((r()-.5)*38,(r()-.5)*38,z,z);}g.globalAlpha=1;g.globalCompositeOperation="source-over";return c;}
// suyari-gasumi: long gold bands overlapping into one cloud, a thin dark rim, gold-leaf flakes
function rkCaps(g,x,y,w,h){const q=h/2;g.moveTo(x+q,y);g.lineTo(x+w-q,y);g.arc(x+w-q,y+q,q,-Math.PI/2,Math.PI/2);g.lineTo(x+q,y+h);g.arc(x+q,y+q,q,Math.PI/2,Math.PI*1.5);g.closePath();}
function rkCloud(g,L,r){g.beginPath();for(const c of L)rkCaps(g,c[0],c[1],c[2],c[3]);g.strokeStyle="rgba(116,80,32,.55)";g.lineWidth=1.8;g.lineJoin="round";g.stroke();
  let y0=1e9,y1=-1e9;for(const c of L){y0=Math.min(y0,c[1]);y1=Math.max(y1,c[1]+c[3]);}const G=g.createLinearGradient(0,y0,0,y1);G.addColorStop(0,"rgba(236,206,136,.9)");G.addColorStop(1,"rgba(204,164,90,.9)");g.fillStyle=G;g.fill();
  for(const [x,y,w,h] of L){const n=w*h/240;for(let i=0;i<n;i++){const z=r()<.12?2.2+r()*1.6:.6+r()*1.1;g.fillStyle=r()<.55?"rgba(252,230,164,.75)":"rgba(170,126,56,.35)";g.fillRect(x+h*.4+r()*(w-h*.8),y+2+r()*(h-4),z,z);}}}
function rkCluster(r,cx,y,w){const L=[],n=2+(r()*2|0),h=14+r()*9;for(let k=0;k<n;k++){const ww=w*(1-k*.2)*(.85+r()*.3);L.push([cx-ww*(.3+r()*.4),y+k*h*.62,ww,h]);}return L;}
function rkWall(g,H,b,bx){const r=rkR(9137+b*7919);for(let y=-12-r()*24;y<H;){const L=rkCluster(r,bx+(r()-.5)*30,y,110+r()*110);rkCloud(g,L,r);y=Math.max(...L.map(c=>c[1]+c[3]))+30+r()*64;}}
function rkBands(g,W,H,r){rkCloud(g,rkCluster(r,W*(.3+r()*.3),-18,170+r()*110),r);const L=rkCluster(r,W*(.3+r()*.3),0,170+r()*110),dy=H+12-Math.max(...L.map(c=>c[1]+c[3]));for(const c of L)c[1]+=dy;rkCloud(g,L,r);}
// a picture on paper: an ink outline from its silhouette, then muted colours
function rkPaint(g,src,x,y,w,h,dpr,a=1){if(!src||w<2||h<2)return;const tw=Math.ceil((w+6)*dpr),th=Math.ceil((h+6)*dpr),T=rkMk(tw,th),t=T.getContext("2d",{willReadFrequently:true});
  t.drawImage(src.im,src.sx,src.sy,src.sw,src.sh,3*dpr,3*dpr,w*dpr,h*dpr);const D=t.getImageData(0,0,tw,th),d=D.data;   // ink silhouette: faint glows (alpha < 90) do not count
  for(let i=0;i<d.length;i+=4){const v=d[i+3];d[i]=36;d[i+1]=23;d[i+2]=14;d[i+3]=v<90?0:v>170?255:(v-90)*3.19;}t.putImageData(D,0,0);
  g.save();g.globalAlpha=.5*a;for(const [dx,dy] of [[-1.2,0],[1.2,0],[0,-1.2],[0,1.2]])g.drawImage(T,x-3+dx,y-3+dy,tw/dpr,th/dpr);
  g.globalAlpha=.94*a;g.filter="saturate(.5) sepia(.3) contrast(1.05) brightness(1.03)";g.drawImage(src.im,src.sx,src.sy,src.sw,src.sh,x,y,w,h);g.restore();}
function rkStroke(g,a,w){g.strokeStyle=`rgba(36,23,14,${a})`;g.lineWidth=w;g.lineCap="round";g.lineJoin="round";}
function rkMot(g,mot,x,y,k,r){g.save();g.translate(x,y);g.scale(k,k);const P=pts=>{g.beginPath();g.moveTo(pts[0],pts[1]);for(let i=2;i<pts.length;i+=2)g.lineTo(pts[i],pts[i+1]);g.closePath();};
  if(mot==="house"){g.fillStyle="rgba(150,108,62,.22)";P([-105,2,70,2,100,-24,-75,-24]);g.fill();rkStroke(g,.45,1.2);g.stroke();
    g.fillStyle="rgba(238,224,190,.38)";g.fillRect(-82,-128,140,104);rkStroke(g,.22,.8);for(let i=1;i<5;i++){g.beginPath();g.moveTo(-82+i*28,-128);g.lineTo(-82+i*28,-24);g.stroke();}for(let j=1;j<4;j++){g.beginPath();g.moveTo(-82,-128+j*26);g.lineTo(58,-128+j*26);g.stroke();}
    rkStroke(g,.6,2.2);for(const px of [-86,62]){g.beginPath();g.moveTo(px,-132);g.lineTo(px,-22);g.stroke();}
    g.fillStyle="rgba(46,38,34,.55)";P([-120,-128,90,-128,112,-146,-98,-146]);g.fill();rkStroke(g,.6,1.3);g.stroke();rkStroke(g,.35,.8);for(let i=0;i<14;i++){g.beginPath();g.moveTo(-114+i*15,-129);g.lineTo(-100+i*15,-145);g.stroke();}}
  else if(mot==="lantern"){rkStroke(g,.5,1);g.beginPath();g.moveTo(-120,-215);g.quadraticCurveTo(0,-180,110,-222);g.stroke();
    for(const [lx,ly] of [[-62,-190],[48,-196]]){const q=g.createRadialGradient(lx,ly,0,lx,ly,46);q.addColorStop(0,"rgba(255,196,110,.32)");q.addColorStop(1,"rgba(255,196,110,0)");g.fillStyle=q;g.fillRect(lx-46,ly-46,92,92);
      g.fillStyle="rgba(196,82,48,.78)";g.beginPath();g.ellipse(lx,ly,15,21,0,0,7);g.fill();rkStroke(g,.55,1);g.stroke();rkStroke(g,.3,.7);for(let i=-2;i<=2;i++){g.beginPath();g.ellipse(lx,ly+i*7,15*Math.sqrt(1-(i*7/21)**2),2,0,0,Math.PI);g.stroke();}
      g.fillStyle="rgba(30,22,16,.85)";g.fillRect(lx-8,ly-24,16,4);g.fillRect(lx-8,ly+20,16,4);}}
  else if(mot==="moon"){g.fillStyle="rgba(238,216,160,.85)";g.beginPath();g.arc(-62,-176,25,0,7);g.fill();rkStroke(g,.4,1);g.stroke();
    g.fillStyle="rgba(120,110,100,.18)";g.beginPath();g.ellipse(-40,-168,46,6,0,0,7);g.fill();}
  else if(mot==="scroll"){g.fillStyle="rgba(236,222,188,.85)";g.fillRect(-70,-6,140,13);rkStroke(g,.4,1);g.strokeRect(-70,-6,140,13);rkStroke(g,.35,.8);
    for(let i=0;i<9;i++){g.beginPath();g.moveTo(-60+i*14,-3);g.lineTo(-60+i*14+r()*4,4);g.stroke();}g.fillStyle="rgba(92,56,30,.8)";g.fillRect(-76,-9,7,19);g.fillRect(69,-9,7,19);}
  else if(mot==="torii"){g.fillStyle="rgba(176,62,40,.72)";g.fillRect(28,-168,9,168);g.fillRect(104,-168,9,168);P([10,-168,132,-168,138,-182,4,-182]);g.fill();g.fillRect(22,-150,98,7);rkStroke(g,.45,1);g.strokeRect(28,-168,9,168);g.strokeRect(104,-168,9,168);}
  else if(mot==="wave"){rkStroke(g,.32,1.1);for(let row=0;row<2;row++)for(let i=-4;i<=4;i++){const cx=i*26+(row?13:0),cy=8+row*9;for(const rr of [12,8,4]){g.beginPath();g.arc(cx,cy,rr,Math.PI,0);g.stroke();}}}
  else if(mot==="crane"){g.translate(56,-140);g.fillStyle="rgba(244,236,220,.92)";P([-26,0,0,-6,30,-22,8,4]);g.fill();rkStroke(g,.5,1);g.stroke();g.fillStyle="rgba(190,60,48,.85)";P([0,-6,-6,-30,8,4]);g.fill();g.stroke();P([-26,0,-40,-12,-30,2]);g.fillStyle="rgba(244,236,220,.92)";g.fill();g.stroke();}
  else if(mot.startsWith("br_")){const sea=mot.slice(3);g.translate(-140,-230);rkStroke(g,.75,4);g.beginPath();g.moveTo(0,0);g.bezierCurveTo(40,20,70,10,120,50);g.stroke();rkStroke(g,.7,2);
    g.beginPath();g.moveTo(60,22);g.quadraticCurveTo(80,0,104,-4);g.moveTo(90,34);g.quadraticCurveTo(100,60,96,80);g.stroke();
    const tips=[[120,50],[104,-4],[96,80],[70,16],[40,14],[110,36]];for(const [bx,by] of tips)for(let i=0;i<4;i++){const px=bx+(r()-.5)*22,py=by+(r()-.5)*18;
      if(sea==="spring"){g.fillStyle="rgba(236,170,182,.9)";for(let a=0;a<5;a++){g.beginPath();g.arc(px+Math.cos(a*1.26)*3,py+Math.sin(a*1.26)*3,2.6,0,7);g.fill();}}
      else if(sea==="autumn"){g.fillStyle=`rgba(${180+r()*40|0},${60+r()*40|0},40,.85)`;g.beginPath();for(let a=0;a<10;a++){const R=a%2?2.5:7;g.lineTo(px+Math.cos(a*Math.PI/5)*R,py+Math.sin(a*Math.PI/5)*R);}g.fill();}
      else if(sea==="winter"){g.fillStyle="rgba(250,250,246,.95)";g.beginPath();g.ellipse(px,py-2,7,3.5,0,0,7);g.fill();rkStroke(g,.35,.8);g.stroke();}
      else{g.fillStyle="rgba(104,136,74,.8)";g.beginPath();g.ellipse(px,py,7,3,r()*3,0,7);g.fill();}}}
  g.restore();}
// one scene → a cached canvas (picture, caption; the newest keeps its ink separately for the wet shimmer)
function rkWrap(g,txt,max){const out=[];let line="";for(const w of txt.split(/\s+/)){const t=line?line+" "+w:w;if(g.measureText(t).width>max&&line){out.push(line);line=w;}else line=t;}if(line)out.push(line);return out;}
function rkRender(s,newest){const {SW:W,PH:H,dpr}=rkV,c=rkMk(W*dpr,H*dpr),g=c.getContext("2d"),r=rkR(rkH(s.main.k));g.scale(dpr,dpr);rkPend=0;
  rkBands(g,W,H,r);rkWall(g,H,s.i,W);rkWall(g,H,s.i+1,0);
  // caption: vertical columns, right to left; the first one is the date in vermilion
  const colLen=H*.62,y0=H*.16;let F=15,lh=21,lines;g.font=`${F}px ${RK_FONT}`;lines=rkWrap(g,rkText(s),colLen);
  if(lines.length>5){F=13.5;lh=18.5;g.font=`${F}px ${RK_FONT}`;lines=rkWrap(g,rkText(s),colLen);}if(lines.length>6){lines=lines.slice(0,6);lines[5]=lines[5].replace(/[\s,.;—-]*\S*$/,"")+"…";}
  const ink=newest?rkMk(W*dpr,H*dpr):null,ig=ink?ink.getContext("2d"):g;if(ink){ig.scale(dpr,dpr);}
  const xr=W-56,col=(txt,j,font,color)=>{ig.save();ig.translate(xr-j*lh,y0);ig.rotate(Math.PI/2);ig.font=font;ig.fillStyle=color;ig.textBaseline="middle";ig.fillText(txt,0,0);ig.restore();};
  col(rkWhen(s)+" —",0,`${F-.5}px ${RK_FONT}`,"rgba(150,40,24,.92)");lines.forEach((l,j)=>col(l,j+1,`${F}px ${RK_FONT}`,"rgba(36,23,14,.9)"));
  const capL=xr-lines.length*lh-lh*.6,ax=26,aw=Math.max(90,capL-ax-8),cx=ax+aw/2,yF=H*.775,p=rkPic(s.main);
  // ground wash and a painted motif behind
  const q=g.createRadialGradient(cx,yF+2,4,cx,yF+2,aw*.55);q.addColorStop(0,"rgba(70,48,26,.2)");q.addColorStop(1,"rgba(70,48,26,0)");g.save();g.translate(0,yF+2);g.scale(1,.16);g.translate(0,-(yF+2));g.fillStyle=q;g.fillRect(cx-aw,yF-aw,aw*2,aw*2);g.restore();
  rkStroke(g,.35,1);for(let i=0;i<7;i++){const gx=cx+(r()-.5)*aw*.9;g.beginPath();g.moveTo(gx,yF+3);g.quadraticCurveTo(gx+2,yF-4,gx+4+r()*3,yF-8-r()*6);g.stroke();}
  rkMot(g,p.mot||"moon",cx,yF,Math.min(1,aw/230),r);
  const put=(src,hh,x,y,maxw,a)=>{if(!src)return 0;let w=src.sw*hh/src.sh;if(maxw&&w>maxw){hh*=maxw/w;w=maxw;}rkPaint(g,src,x-w/2,y-hh,w,hh,dpr,a);return w;};
  if(p.mon)put(rkSrc(p,"mon"),H*.4,cx,yF+6,aw*.98);
  else{const two=(p.it||p.food||p.kit||p.atl||p.cv||p.mon2)&&p.cat,cw=two?aw*.55:aw*.95;
    if(p.cat)put(rkSrc(p,"cat"),H*(two?.27:.34),two?cx+aw*.2:cx,yF+H*.035,cw);
    if(p.kit)put(rkSrc(p,"kit"),H*.2,cx-aw*.26,yF+8,aw*.5);
    if(p.it)put(rkSrc(p,"it"),Math.min(H*.2,DIMG[p.it]&&DIMG[p.it].height||H*.2),cx-aw*.22,yF+4,aw*.48);
    if(p.food)put(rkSrc(p,"food"),H*.11,cx-aw*.22,yF+6,aw*.4);
    if(p.mon2)put(rkSrc(p,"mon2"),H*.3,cx-aw*.24,yF+6,aw*.52);if(p.atl)put(rkSrc(p,"atl"),H*(p.ah||.2),cx-aw*.22,yF+(p.ah<.15?-H*.06:4),aw*.46);
    if(p.cv)put(rkSrc(p,"cv"),H*.22,cx-aw*.22,yF+4,aw*.48);}
  // the other events of that day: small pictures in front
  let j=0;for(const e of s.ev){if(e===s.main||j>=3)continue;const q2=rkPic(e),sz=H*.1;let src=null;
    if(q2.mon)src=rkSrc(q2,"mon");else if(q2.mon2)src=rkSrc(q2,"mon2");else if(q2.atl)src=rkSrc(q2,"atl");else if(q2.it)src=rkSrc(q2,"it");else if(q2.food)src=rkSrc(q2,"food");if(!src)continue;
    put(src,q2.mon||q2.mon2?sz*1.35:sz,ax+16+j*(aw-30)/2.4,yF+H*.12,sz*1.3,.95);j++;}
  if(ink)g.drawImage(ink,0,0,W,H);return{c,ink,pend:rkPend,at:performance.now()};}
function rkEndR(){const {TW:W,PH:H,dpr}=rkV,c=rkMk(W*dpr,H*dpr),g=c.getContext("2d");g.scale(dpr,dpr);rkWall(g,H,0,0);
  const bx=32;g.fillStyle="#1e2a3e";g.fillRect(bx,0,W-bx,H);g.fillStyle="rgba(212,176,96,.5)";for(let y=8,k=0;y<H;y+=17,k++)for(let x=bx+10+(k%2)*8.5;x<W;x+=17){g.beginPath();g.moveTo(x,y-4);g.lineTo(x+4,y);g.lineTo(x,y+4);g.lineTo(x-4,y);g.fill();}
  const sh=g.createLinearGradient(bx,0,W,0);sh.addColorStop(0,"rgba(0,0,0,0)");sh.addColorStop(1,"rgba(0,0,0,.45)");g.fillStyle=sh;g.fillRect(bx,0,W-bx,H);
  g.fillStyle="rgba(214,178,98,.85)";g.fillRect(bx,0,2.5,H);
  const sx=bx+24,sy=H*.09,sw=40,sl=H*.6;g.fillStyle="#e9ddc2";g.fillRect(sx,sy,sw,sl);g.fillStyle="rgba(200,160,80,.5)";const r=rkR(3);for(let i=0;i<60;i++)g.fillRect(sx+r()*sw,sy+r()*sl,1.2,1.2);
  g.strokeStyle="rgba(110,80,36,.7)";g.lineWidth=1;g.strokeRect(sx+.5,sy+.5,sw-1,sl-1);
  g.save();g.translate(sx+sw/2,sy+18);g.rotate(Math.PI/2);g.font=`21px ${RK_FONT}`;g.fillStyle="#2a1b10";g.textBaseline="middle";g.fillText("Летопись дома Муси",0,0);g.restore();
  g.fillStyle="rgba(186,44,32,.9)";g.fillRect(sx+9,sy+sl-32,22,22);g.font=`700 15px ${RK_JP}`;g.fillStyle="#efe2c6";g.textAlign="center";g.textBaseline="middle";g.fillText("家",sx+20,sy+sl-20.5);
  return{c,ink:null,pend:0,at:performance.now()};}
function rkEndL(){const {LW:W,PH:H,dpr}=rkV,c=rkMk(W*dpr,H*dpr),g=c.getContext("2d");g.scale(dpr,dpr);rkWall(g,H,rkV.sc.length,W);
  g.save();g.translate(W*.3,H*.2);g.rotate(Math.PI/2);g.font=`15px ${RK_FONT}`;g.fillStyle="rgba(36,23,14,.34)";g.textBaseline="middle";g.fillText("Свиток ждёт новых историй…",0,0);g.restore();
  return{c,ink:null,pend:0,at:performance.now()};}

// ── the unrolling view ──
const rkV={off:0,vel:0,drag:null,tgt:null,raf:0,sc:[],nw:new Set(),stamp:{},ci:null,cw:0};
const rkT=new Map();
const rkClamp=o=>clamp(o,rkV.mn,rkV.mx),rkLeft=i=>rkV.L-rkV.TW-(i+1)*rkV.SW,rkAt=i=>clamp(rkLeft(i)+rkV.SW/2-rkV.W/2,rkV.mn,rkV.mx);
function rkGeom(cv){const V=rkV,W=cv.clientWidth||440,H=Math.round(clamp(innerHeight*.6,340,560)),dpr=Math.min(2,devicePixelRatio||1);cv.style.height=H+"px";cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);
  const SW=Math.round(clamp(W*.74,280,380)),TW=150,LW=Math.round(clamp(W*.45,170,260)),L=LW+V.sc.length*SW+TW;
  Object.assign(V,{cw:W,W,H,dpr,T0:16,PH:H-32,SW,TW,LW,L,mn:L<W?-(W-L)/2:0,mx:L<W?-(W-L)/2:L-W,pat:null});V.off=rkClamp(V.off);rkT.clear();rkSealC=rkSeal(dpr);}
function rkTile(k,fn){let o=rkT.get(k);if(o){rkT.delete(k);if(o.pend&&performance.now()-o.at>700)o=null;else rkT.set(k,o);}if(!o){o=fn();rkT.set(k,o);
  if(rkT.size>12)for(const kk of rkT.keys()){if(kk!==k){rkT.delete(kk);if(rkT.size<=9)break;}}}return o;}
function rkDraw(){const cv=$("rkCv");if(!cv)return;const V=rkV;if(cv.clientWidth&&cv.clientWidth!==V.cw)rkGeom(cv);rkTex();
  const g=cv.getContext("2d"),{W,H,T0,PH,SW,L,dpr}=V,off=V.off,n=V.sc.length,tn=performance.now()/1000;g.setTransform(dpr,0,0,dpr,0,0);
  const bg=g.createLinearGradient(0,0,0,H);bg.addColorStop(0,"#0d0b09");bg.addColorStop(.5,"#16110c");bg.addColorStop(1,"#0a0807");g.fillStyle=bg;g.fillRect(0,0,W,H);
  const a=Math.max(0,-off),b=Math.min(W,L-off);if(b<=a)return;
  g.fillStyle="rgba(0,0,0,.55)";g.fillRect(a+2,T0+4,b-a,PH+3);
  if(!V.pat){V.pat=g.createPattern(rkPaper,"repeat");}V.pat.setTransform(new DOMMatrix().translateSelf(-off,T0));g.fillStyle=V.pat;g.fillRect(a,T0,b-a,PH);
  // tiles: blank end (left), scenes, the title (right)
  if(-off+V.LW>0)g.drawImage(rkTile("L|"+n,rkEndL).c,-off,T0,V.LW,PH);
  for(let i=0;i<n;i++){const x=rkLeft(i)-off;if(x>W||x+SW<0)continue;const s=V.sc[i],nwst=i===n-1,o=rkTile(i+"|"+s.key+(nwst?"|n":""),()=>rkRender(s,nwst));g.drawImage(o.c,x,T0,SW,PH);
    if(nwst&&o.ink)rkWet(g,o.ink,x,T0,SW,PH,tn);
    if(V.nw.has(i)&&rkSealC){const vis=x+SW*.8<W&&x+SW*.4>0;if(vis&&!V.stamp[i]){V.stamp[i]=tn;tone(196,.12,"sine",.05);}const e=V.stamp[i]?clamp((tn-V.stamp[i])/.32,0,1):0;
      if(e>0){const k=1+(1-e)*.7,z=40*k;g.globalAlpha=e;g.drawImage(rkSealC,x+SW-74-z/2+20,T0+PH*.84-z/2,z,z);g.globalAlpha=1;}}}
  if(L-off-V.TW<W)g.drawImage(rkTile("R",rkEndR).c,L-off-V.TW,T0,V.TW,PH);
  // aged edges of the paper
  if(!V.age){const q=g.createLinearGradient(0,T0,0,T0+PH);q.addColorStop(0,"rgba(96,62,28,.42)");q.addColorStop(.06,"rgba(96,62,28,0)");q.addColorStop(.94,"rgba(96,62,28,0)");q.addColorStop(1,"rgba(96,62,28,.46)");V.age=q;}
  g.fillStyle=V.age;g.fillRect(a,T0,b-a,PH);g.fillStyle="rgba(80,52,24,.55)";g.fillRect(a,T0,b-a,1);g.fillRect(a,T0+PH-1,b-a,1);
  // the roller at the left end and the cord at the right end
  const jx=-off;if(jx>-20&&jx<W){const q=g.createLinearGradient(jx-9,0,jx+9,0);q.addColorStop(0,"#2a170b");q.addColorStop(.45,"#8c5a32");q.addColorStop(1,"#26140a");g.fillStyle=q;g.fillRect(jx-9,T0-9,18,PH+18);
    g.fillStyle="#e2d4b2";for(const y of [T0-15,T0+PH+9]){g.beginPath();g.roundRect(jx-7,y,14,7,3);g.fill();}}
  const cx=L-off;if(cx>-10&&cx<W+40){g.strokeStyle="#6e3b5c";g.lineWidth=3;g.lineCap="round";g.beginPath();g.moveTo(cx-3,T0+PH*.5);g.bezierCurveTo(cx+30,T0+PH*.42,cx+26,T0+PH*.66,cx+8,T0+PH*.6);g.stroke();
    g.strokeStyle="rgba(230,190,220,.35)";g.lineWidth=1;g.stroke();}
  // more paper beyond the view: a curl shadow at the edges
  for(const [on,x0,x1] of [[off>V.mn+2,0,26],[off<V.mx-2,W,W-26]])if(on){const q=g.createLinearGradient(x0,0,x1,0);q.addColorStop(0,"rgba(20,12,6,.5)");q.addColorStop(1,"rgba(20,12,6,0)");g.fillStyle=q;g.fillRect(Math.min(x0,x1),T0,26,PH);}
  // film grain
  g.save();g.globalCompositeOperation="overlay";g.globalAlpha=.13;if(!V.gp)V.gp=g.createPattern(rkGrain,"repeat");V.gp.setTransform(new DOMMatrix().translateSelf((tn*997)%128|0,(tn*613)%128|0));g.fillStyle=V.gp;g.fillRect(0,0,W,H);g.restore();
  rkCapUpd();}
// fresh ink: a slow glint running down the newest caption
function rkWet(g,ink,x,y,w,h,tn){const T=rkSh||(rkSh=rkMk(ink.width,ink.height));if(T.width!==ink.width||T.height!==ink.height){T.width=ink.width;T.height=ink.height;}
  const t=T.getContext("2d"),u=(tn*.22)%1.5-.25,H2=T.height;t.globalCompositeOperation="source-over";t.clearRect(0,0,T.width,H2);t.drawImage(ink,0,0);t.globalCompositeOperation="source-in";
  const q=t.createLinearGradient(0,H2*(u-.12),0,H2*(u+.12));q.addColorStop(0,"rgba(255,246,222,0)");q.addColorStop(.5,"rgba(255,246,222,1)");q.addColorStop(1,"rgba(255,246,222,0)");t.fillStyle=q;t.fillRect(0,0,T.width,H2);
  g.globalAlpha=.35;g.drawImage(ink,x,y,w,h);g.globalAlpha=.6;g.drawImage(T,x,y,w,h);g.globalAlpha=1;}
function rkCenter(){const V=rkV,c=V.off+V.W/2;if(c>V.L-V.TW)return"t";if(c<V.LW)return"e";return clamp(Math.floor((V.L-V.TW-c)/V.SW),0,V.sc.length-1);}
function rkCapUpd(){const ci=rkCenter();if(ci===rkV.ci)return;rkV.ci=ci;const P=$("rkCap"),N=$("rkN");if(!P)return;const n=rkV.sc.length;
  if(ci==="t"){P.innerHTML=`<b>Летопись дома Муси</b> — свиток читают справа налево, как старинные эмаки. Веди пальцем вправо, чтобы развернуть его дальше.`;N.innerHTML=`${n} ${rkPl(n,"сцена","сцены","сцен")} · начало свитка`;return;}
  if(ci==="e"){P.innerHTML=`<b>Конец свитка</b> — здесь кисть остановилась. Дом сам допишет новые сцены, когда в нём что-то случится.`;N.innerHTML=`${n} ${rkPl(n,"сцена","сцены","сцен")} · свежий край`;return;}
  const s=rkV.sc[ci];P.innerHTML=`<b>${esc(rkWhen(s))}</b> — ${esc(rkText(s))}`;N.innerHTML=`Сцена ${ci+1} из ${n}${rkV.nw.has(ci)?` · <i>新 новая</i>`:""}${ci===n-1?" · тушь ещё не высохла":""}`;}
function rkStep(dt){const V=rkV;if(V.tgt!=null){V.off+=(V.tgt-V.off)*(1-Math.exp(-dt*3.4));if(Math.abs(V.tgt-V.off)<.6){V.off=V.tgt;V.tgt=null;}}
  else if(!V.drag&&V.vel){const o=V.off;V.off=rkClamp(V.off+V.vel*dt);V.vel*=Math.exp(-dt*3.5);if(Math.abs(V.vel)<8||V.off===o)V.vel=0;}}
function rkLoop(){if(rkV.raf)return;let lt=performance.now();const f=()=>{rkV.raf=0;if(!panelIs("rk")||!$("rkCv"))return;const t=performance.now();rkStep(Math.min(.05,(t-lt)/1000));lt=t;
  try{rkDraw();}catch(e){console.error("chronicle",e);return;}rkV.raf=requestAnimationFrame(f);};rkV.raf=requestAnimationFrame(f);}
function rkBind(cv){const V=rkV;
  cv.addEventListener("pointerdown",e=>{V.drag={x:e.clientX,o:V.off,lx:e.clientX,lt:performance.now()};V.vel=0;V.tgt=null;cv.style.cursor="grabbing";try{cv.setPointerCapture(e.pointerId);}catch(x){}});
  cv.addEventListener("pointermove",e=>{const d=V.drag;if(!d)return;const t=performance.now(),dt=Math.max(1,t-d.lt);V.off=rkClamp(d.o-(e.clientX-d.x));V.vel=clamp(V.vel*.5-(e.clientX-d.lx)/dt*500,-4000,4000);d.lx=e.clientX;d.lt=t;});
  const up=()=>{if(!V.drag)return;if(performance.now()-V.drag.lt>90)V.vel=0;V.drag=null;cv.style.cursor="";};
  for(const k of ["pointerup","pointercancel","lostpointercapture"])cv.addEventListener(k,up);
  cv.addEventListener("wheel",e=>{const h=Math.abs(e.deltaX)>Math.abs(e.deltaY);V.off=rkClamp(V.off+(h?e.deltaX:-e.deltaY));V.tgt=null;V.vel=0;e.preventDefault();},{passive:false});}
function rkOpen(){rkTrack();rkMemo=null;const sc=rkScenes(),V=rkV,first=!RK.n;V.sc=sc;V.nw=new Set(sc.filter(s=>s.gm>RK.seen).map(s=>s.i));V.stamp={};V.ci=null;V.tgt=null;V.vel=0;V.drag=null;V.age=null;V.gp=null;
  openPanel("Свиток-летопись",`<div class="rk-wrap"><canvas class="rk-cv" id="rkCv"></canvas></div><p class="rk-cap" id="rkCap"></p><p class="rk-n" id="rkN"></p>
   <div class="rk-row"><button class="btn" data-x="rk:start">⏮ К началу</button><button class="btn" data-x="rk:end">К свежей сцене ⏭</button></div>
   <p class="lead">Свиток читают справа налево, как старинные эмаки: справа — начало, слева — самые свежие сцены. Дом сам дописывает его: первые встречи, главы истории, праздники и круглые числа. Мелкие события одного дня собираются в одну сцену, новые помечены красной печатью 新.</p>`,"rk");
  $("xpBody").scrollTop=0;const cv=$("rkCv");rkGeom(cv);rkBind(cv);
  const nw=[...V.nw].sort((a,b)=>a-b);V.off=first?V.mx:rkAt(nw.length?nw[0]:sc.length-1);
  RK.n++;RK.od=dayKey();RK.seen=Math.max(RK.seen,...sc.map(s=>s.gm));award("rk_open");if(rkYear())award("rk_year");save();hubDot();
  if(!rkFont&&document.fonts&&document.fonts.load)document.fonts.load(`15px Kurale`,"Аа").then(f=>{if(f&&f.length){rkFont=true;rkT.clear();}}).catch(()=>{});
  rkLoop();}
hook("panelClose",id=>{if(id==="rk"){rkT.clear();rkSh=null;}});

// ── 家 card, album, dots ──
function rkStatus(){const n=rkScenes().length,k=rkNewN();return`На свитке ${n} ${rkPl(n,"сцена","сцены","сцен")}${k?` — ${k} ${rkPl(k,"новая","новые","новых")}`:""}`;}
hook("hub",()=>`<div class="hubc"><h4>📜 Свиток-летопись <i>絵巻</i></h4><p>${rkStatus()}</p><p>Длинный свиток-эмаки, на котором дом сам записывает свою историю: день, когда пришла Муся, первые гости, главы, праздники, круглые числа. Его читают справа налево, новые сцены помечены красной печатью.</p>
  <div class="row"><button class="btn${rkNewN()?" primary":""}" data-x="rk:open">📜 Развернуть свиток</button></div></div>`);
hook("hubDot",()=>RK.od!==dayKey()&&rkNewN()>0);
hook("album",el=>{const sc=rkScenes(),n=sc.length,last=sc.slice(-8).reverse();if(!n)return;
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Свиток-летопись</h3><p class="lead">На свитке ${n} ${rkPl(n,"сцена","сцены","сцен")}: от «${esc(rkWhen(sc[0]))}» до «${esc(rkWhen(sc[n-1]))}». Последние сцены:</p>
   <div class="coll">${last.map(s=>`<div class="ci on rk-ci${s.gm>RK.seen?" nw":""}">${rkPicHtml(s.main)}<small>${esc(s.u?"первые дни":rkDate(s.g).replace(/ \d{4}$/,""))}</small></div>`).join("")}</div>
   <div class="row"><button class="btn" data-x="rk:open">📜 Развернуть свиток</button></div>`);});
hook("click",key=>{if(!key.startsWith("rk:"))return;audioInit();const a=key.slice(3),V=rkV;
  if(a==="open")rkOpen();else if(a==="start"){V.tgt=V.mx;V.vel=0;}else if(a==="end"){V.tgt=V.sc.length?rkAt(V.sc.length-1):V.mn;V.vel=0;}return true;});
hook("disc",kind=>{if(kind!=="chronicle")rkMemo=null;});
hook("boot",()=>{rkTrack();if(!RK.seen){const E=rkEvents();RK.seen=E.length?E[E.length-1].g:0;}save();});
let rkTk=0;
hook("sec",()=>{if(++rkTk%5)return;rkTrack();const n=rkScenes().length;for(const m of [10,25,50])if(n>=m)disc("chronicle","len"+m);if(n>=25)award("rk_25");if(RK.n&&rkYear())award("rk_year");});
X.rk={st:RK,scenes:rkScenes,events:rkEvents,text:rkText,say:rkSay,when:rkWhen,open:rkOpen,V:rkV,track:rkTrack,status:rkStatus,
  reset(){rkMemo=null;},go(i){rkV.tgt=null;rkV.vel=0;rkV.off=i==="start"?rkV.mx:i==="end"?rkAt(rkV.sc.length-1):i==="edge"?rkV.mn:rkAt(i);},
  // test: drag the paper by dx px through the real pointer handlers
  drag(dx){const cv=$("rkCv");if(!cv)return;const r=cv.getBoundingClientRect(),y=r.top+r.height/2,x=r.left+r.width/2;
    cv.dispatchEvent(new PointerEvent("pointerdown",{clientX:x,clientY:y,pointerId:7,bubbles:true}));for(let k=1;k<=10;k++)cv.dispatchEvent(new PointerEvent("pointermove",{clientX:x+dx*k/10,clientY:y,pointerId:7,bubbles:true}));
    cv.dispatchEvent(new PointerEvent("pointerup",{clientX:x+dx,clientY:y,pointerId:7,bubbles:true}));return rkV.off;}};
}
