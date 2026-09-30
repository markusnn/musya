{
// ───────────────────────── «Путешествия Муси» (add-on tv, idea #9, like Tabikaeru) ─────────────────────────
// Pack a bento (+ omamori, lantern) → she walks out through the torii and is away 1–3 h (the first trip 30 min);
// 2–3 painted postcards arrive at random moments (also while the game is closed); she comes back to the gate with a souvenir.
// The only add-on that sets S.ext.away. State: S.ext.trip. Art: art/travel_art.py → assets/items/atlas_tvp1|tvp2|tvs.webp
const TVJ={cards:{fushimi:["tvp1",0,0],fuji:["tvp1",560,0],nara:["tvp1",0,380],arashiyama:["tvp1",560,380],itsukushima:["tvp1",0,760],nachi:["tvp1",560,760],jigokudani:["tvp1",0,1140],himeji:["tvp1",560,1140],kamakura:["tvp2",0,0],shirakawa:["tvp2",560,0],kinkakuji:["tvp2",0,380],shinkyo:["tvp2",560,380],sunset:["tvp2",0,760],foxnight:["tvp2",560,760],aoshima:["tvp2",0,1140]},
 atl:{tvp1:[1120,1520],tvp2:[1120,1520]},tvs:[1400,292],
 sp:{tv_s_torii:[514,0,130,130,"b"],tv_s_fuji:[758,0,200,120,"b"],tv_s_senbei:[1090,0,130,100,"b"],tv_s_bamboo:[960,0,80,120,"b"],tv_s_momiji:[1222,0,150,100,"b"],tv_s_crow:[646,0,110,130,"b"],tv_s_tenugui:[0,0,110,190,"t"],tv_s_castle:[198,0,130,150,"b"],tv_s_hato:[0,192,140,100,"b"],tv_s_sarubobo:[422,0,90,140,"b"],tv_s_yatsuhashi:[142,192,150,100,"b"],tv_s_monkeys:[294,192,170,100,"b"],tv_s_shell:[466,192,110,90,"b"],tv_s_foxbell:[330,0,90,150,"t"],tv_s_catstone:[578,192,110,80,"b"],tv_bundle:[690,192,90,70,"b"],tv_bell:[1042,0,46,110,"t"],tv_post:[112,0,84,170,"b"],tv_card:[782,192,44,30,"b"]}};
// places: id, name, region, «from …» for one-line messages, the narrator's caption (Musya never talks), souvenir, rare: om (needs an omamori) | lan (a night place, needs a lantern)
const TVP=[
 {id:"fushimi",n:"Фусими Инари",r:"Киото",f:"из Фусими Инари",s:"tv_s_torii",sn:"Маленькие тории из Фусими",c:"Тысяча тории — и Муся прошла под каждыми. Говорят, в самом конце тропы живут лисы-посланницы."},
 {id:"fuji",n:"Гора Фудзи",r:"озеро Кавагути",f:"с Фудзи",s:"tv_s_fuji",sn:"Веер с Фудзи",c:"Утро у озера Кавагути. Фудзи в снежной шапке смотрится в воду, а Муся смотрит на Фудзи и не шевелит даже ухом."},
 {id:"nara",n:"Олени Нары",r:"Нара",f:"из Нары",s:"tv_s_senbei",sn:"Печенье сика-сэмбэй",c:"В Наре олени кланяются тем, у кого есть печенье. Печенья у Муси не было, но ей всё равно поклонились."},
 {id:"arashiyama",n:"Бамбуковая роща",r:"Арасияма, Киото",f:"из Арасиямы",s:"tv_s_bamboo",sn:"Бамбуковый стаканчик",c:"Бамбук шумит над головой, как далёкое море. Муся долго сидела на тропинке и слушала."},
 {id:"itsukushima",n:"Плавучие тории",r:"остров Ицукусима",f:"с Ицукусимы",s:"tv_s_momiji",sn:"Момидзи-мандзю",c:"В прилив большие тории стоят прямо в море. Муся ждёт отлива, чтобы подойти к ним по мокрому песку."},
 {id:"nachi",n:"Водопад Нати",r:"Вакаяма",f:"с водопада Нати",s:"tv_s_crow",sn:"Ятагарасу из Нати",c:"Водопад Нати падает со ста тридцати трёх метров. Рядом алая пагода, а в тумане — маленькая Муся."},
 {id:"jigokudani",n:"Снежные обезьяны",r:"Дзигокудани, Нагано",f:"из Дзигокудани",s:"tv_s_tenugui",sn:"Тэнугуи с обезьянками",c:"Снежные обезьяны греются в горячем источнике. Мусю звали окунуться, но она кошка — смотрит с берега."},
 {id:"himeji",n:"Замок Химэдзи",r:"Хёго",f:"из Химэдзи",s:"tv_s_castle",sn:"Белый замок Химэдзи",c:"Замок Химэдзи зовут Белой цаплей: кажется, ещё немного — и расправит крылья. Муся на всякий случай сидит тихо."},
 {id:"kamakura",n:"Большой Будда",r:"Камакура",f:"из Камакуры",s:"tv_s_hato",sn:"Печенье хато-сабурэ",c:"Большой Будда сидит здесь почти восемьсот лет. Муся посидела рядом совсем чуть-чуть — и тоже очень спокойно."},
 {id:"shirakawa",n:"Сиракава-го",r:"Гифу",f:"из Сиракава-го",s:"tv_s_sarubobo",sn:"Кукла сарубобо",c:"Деревня под снегом. Крыши сложены, как ладони в молитве, в окнах тёплый свет. Муся греет лапы хотя бы взглядом."},
 {id:"kinkakuji",n:"Кинкаку-дзи",r:"Киото",f:"из Кинкаку-дзи",s:"tv_s_yatsuhashi",sn:"Сладости яцухаси",c:"Золотой павильон смотрится в пруд, как в зеркало. Муся тоже заглянула — и увидела там кошку."},
 {id:"shinkyo",n:"Мост Синкё",r:"Никко",f:"из Никко",s:"tv_s_monkeys",sn:"Три обезьяны из Никко",c:"Алый мост Синкё над рекой Дайя. Осень, клёны горят, а вода внизу шумит так, что Муся прижала уши."},
 {id:"sunset",n:"Тории у моря",r:"морской берег",f:"с морского берега",s:"tv_s_shell",sn:"Ракушка с морского берега",rare:"om",c:"Тории стоят на камне среди волн. Солнце садится прямо в ворота — Муся загадала желание и никому его не скажет."},
 {id:"foxnight",n:"Лисья тропа ночью",r:"Фусими Инари, Киото",f:"с ночной лисьей тропы",s:"tv_s_foxbell",sn:"Лисий бубенчик",rare:"lan",c:"Ночью на тропе Инари светятся только фонари и лисьи огоньки. Каменные лисы кивнули Мусе: своя."},
 {id:"aoshima",n:"Остров кошек",r:"Аосима, Эхимэ",f:"с острова Аосима",s:"tv_s_catstone",sn:"Кошачий камешек с Аосимы",rare:"om",c:"На острове Аосима кошек больше, чем людей. Муся нашла своих — и чуть не осталась."}];
const TVI={};for(const p of TVP)TVI[p.id]=p;
addItems(TVP.map(p=>{const r=TVJ.sp[p.s];return{id:p.s,n:p.sn,c:"Сувениры",w:r[2],h:r[3],a:r[4],p:0,at:["tvs",r[0],r[1]],src:"🎒 сувенир из путешествия",hint:`🎒 Привезёт из места «${p.n}»`};}),{tvs:TVJ.tvs});
STAMPS.push(["tv_trip","旅","Путешественница","Проводи Мусю в путешествие и встреть её"],["tv_rare","珍","Редкое место","Получи открытку из редкого места"],["tv_all","便","Все открытки","Собери все 15 открыток"]);

// state: n trips done · cur {t0,t1,food,om,lan,legs:[{p,at,got}],call,needs,st:"go"|"gate",gateAt} · pc {place:ms} · nw unseen postcards · last trip
const T=S.ext.trip||(S.ext.trip={n:0,cur:null,pc:{},nw:[],last:null});
if(T.cur){S.ext.away=true;if(T.cur.needs)Object.assign(S.needs,T.cur.needs);}   // her needs stood still while she was away
else if(S.ext.away)S.ext.away=false;
let TVIM=null;atlasImg("tvs",im=>{TVIM=im;});
const tvCv=document.createElement("canvas");tvCv.width=384;tvCv.height=416;const tvG=tvCv.getContext("2d");
const pk={food:null,om:null,lan:null};
let tvA=null,tvHit={},tvRoomAt=0,tvClosed=[],tvBackClosed=false,tvBoot=false;
document.head.insertAdjacentHTML("beforeend",`<style>
.tv-row{display:flex;gap:8px;overflow-x:auto;padding:4px 0 10px;scroll-snap-type:x mandatory}
.tv-chip{flex:none;width:92px;min-height:92px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;padding:8px 5px;border-radius:12px;background:var(--ink-2);border:1px solid var(--line);font-size:11.5px;line-height:1.2;color:var(--paper);text-align:center;scroll-snap-align:start}
.tv-chip.on{border-color:var(--sakura);box-shadow:inset 0 0 0 1px var(--sakura)}
.tv-chip small{color:var(--muted);font-size:11px}.tv-chip.on small{color:var(--sakura)}
.tv-chip .tv-none{font-size:24px;line-height:1;color:var(--muted)}
.story-body h3.tv-h{font-size:22px;margin:18px 0 2px}.tv-h small{font-family:var(--ui);font-size:12px;color:var(--muted);font-weight:400;margin-left:6px}
.tv-hero{display:flex;gap:14px;align-items:center;margin:4px 0 6px}.tv-hero p{margin:0!important}
.tv-go{width:100%;margin-top:18px;font-size:16px;padding:13px}
.tv-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:14px 12px;margin:10px 0 16px}
.tv-pc{display:flex;flex-direction:column;gap:3px;text-align:left;padding:0;color:var(--paper)}
.tv-img{display:block;width:100%;aspect-ratio:560/380;box-sizing:border-box;border-radius:5px;background-color:#0a0d0c;border:4px solid #e6dcc6;box-shadow:0 5px 16px rgba(0,0,0,.55);background-repeat:no-repeat}
.tv-pc.off .tv-img{border:2px dashed rgba(216,210,195,.18);box-shadow:none;display:grid;place-items:center;font-size:30px;color:var(--muted);font-family:var(--display)}
.tv-pc b{font-size:13px;font-weight:600;line-height:1.25}.tv-pc small{font-size:11px;color:var(--muted);line-height:1.3}
.tv-pc.new b{color:var(--sakura)}.tv-pc.new b::after{content:" · новая"}
.tv-big{margin:6px 0 14px}.tv-big .tv-img{border-width:8px;border-radius:6px;transform:rotate(-1.2deg);box-shadow:0 10px 30px rgba(0,0,0,.6)}
.story-body p.tv-cap{font-family:var(--display);font-size:21px;line-height:1.45;color:#ece5d4}
.story-body p.tv-sign{text-align:right;color:var(--sakura);font-size:15px;margin-top:-6px}
.tv-mini{display:grid;grid-template-columns:repeat(auto-fill,minmax(64px,1fr));gap:6px;margin:8px 0 10px}.tv-mini .tv-img{border-width:2px;box-shadow:none}.tv-mini .off{border:1px dashed rgba(216,210,195,.18);background:none}
</style>`);

// ───── helpers ─────
const tvDate=ms=>new Date(ms).toLocaleDateString("ru-RU",{day:"numeric",month:"long"});
function tvLeft(){const c=T.cur;if(!c)return"";const ms=(c.call||c.t1)-Date.now();if(ms<=60e3)return"вот-вот";const m=Math.round(ms/60e3),h=Math.floor(m/60),mm=m%60;return"примерно через "+(h?h+" ч"+(mm?" "+mm+" мин":""):mm+" мин");}
function tvBg(id){const [a,x,y]=TVJ.cards[id],[W,H]=TVJ.atl[a];return`background-image:url(assets/items/atlas_${a}.webp);background-size:${W/560*100}% ${H/380*100}%;background-position:${x/(W-560)*100}% ${y/(H-380)*100}%`;}
function tvSp(id,mw,mh){const r=TVJ.sp[id],k=Math.min(mw/r[2],mh/r[3]),f=v=>(v*k).toFixed(1);return`<span style="display:inline-block;flex:none;width:${f(r[2])}px;height:${f(r[3])}px;background:url(assets/items/atlas_tvs.webp) -${f(r[0])}px -${f(r[1])}px/${f(TVJ.tvs[0])}px ${f(TVJ.tvs[1])}px no-repeat"></span>`;}
const tvGot=()=>Object.keys(T.pc).length;
function tvOwned(cats){return ITEMS.filter(i=>cats.includes(i.c)&&S.owned.has(i.id));}

// ───── time: postcards arrive, the trip ends (works for time spent with the game closed too) ─────
function tvPost(p,silent,at){if(!T.pc[p])T.pc[p]=at||Date.now();if(!T.nw.includes(p))T.nw.push(p);disc("postcard",p);
  if(TVI[p].rare)award("tv_rare");if(tvGot()>=TVP.length)award("tv_all");
  if(silent)tvClosed.push(p);else{toast("🎴 Пришла открытка от Муси");chime([988,1319,1568]);ui();}save();}
function tvSync(silent){const c=T.cur;if(!c||c.st!=="go")return;const nw=Date.now(),end=c.call||c.t1;
  for(const L of c.legs)if(!L.got&&L.at<=Math.min(nw,end)){L.got=L.at;tvPost(L.p,silent,L.at);}
  if(nw>=end){c.legs=c.legs.filter(L=>L.got);c.st="gate";c.gateAt=nw;save();
    if(silent)tvBackClosed=true;else{knock();toast("🎒 Муся вернулась! Встречай у ворот ⛩");ui();}}}
// which places this trip visits: unseen ones first; an omamori opens the rare places, a lantern the night trail
function tvPlan(n,om,lan){const out=[],seen=p=>!!T.pc[p],free=a=>a.filter(p=>!out.includes(p)),pref=a=>{const u=a.filter(p=>!seen(p));return pick(u.length&&Math.random()<.85?u:a);};
  const rare=TVP.filter(p=>p.rare==="om").map(p=>p.id),com=TVP.filter(p=>!p.rare).map(p=>p.id),late=[];
  if(lan&&Math.random()<(seen("foxnight")?.25:.6))late.push("foxnight");
  if(om&&late.length<n-1&&Math.random()<(om==="om_road"?.15:0)+(rare.some(p=>!seen(p))?.55:.3))late.push(pref(rare));
  while(out.length+late.length<n)out.push(pref(free(com)));
  return out.concat(late);}
function tvLeave(){
  const f=pk.food;if(!f||!have(f)){toast("Сначала положи в узелок бэнто");return;}
  if(T.cur)return;take(f);const first=!T.n,t0=Date.now(),dur=first?30*60e3:Math.round(rand(60,180))*60e3,pl=tvPlan(first?2:(Math.random()<.5?2:3),pk.om,pk.lan);
  T.cur={t0,t1:t0+dur,food:f,om:pk.om,lan:pk.lan,needs:{...S.needs},st:"go",legs:pl.map((p,i)=>({p,at:Math.round(t0+dur*(.12+.8*(i+rand(.15,.85))/pl.length)),got:0}))};
  save();closePanel();if(S.room!=="entrance")goRoom("entrance");
  react("😸",1.6);const [hx,hy]=cellToStage(97,120);floatFx.push({g:"🎒",x:hx,y:hy,t:now()+.2});
  setTimeout(()=>{S.ext.away=true;tvA={k:"go",t0:now(),x0:pet.x};sfx("chime");save();ui();},1100);
}
// she is home: needs from before the trip + what the trip gave, a souvenir from a place she sent a postcard from
function tvHome(){const c=T.cur;if(!c)return null;const got=c.legs.filter(L=>L.got).map(L=>L.p),cand=got.map(p=>TVI[p].s).filter(s=>!S.owned.has(s)),sv=cand.length?cand[cand.length-1]:null;
  if(sv){S.owned.add(sv);disc("souvenir",sv);}
  const n=S.needs;if(c.needs)Object.assign(n,c.needs);const F=FOOD[c.food]||{};
  n.food=clamp(n.food+(F.food||20)*.6,0,100);n.joy=clamp(n.joy+(c.om?30:20),0,100);n.energy=clamp(n.energy-12,0,100);if(!c.om)n.clean=clamp(n.clean-15,0,100);
  T.last={pl:got,sv,t:Date.now(),om:c.om,called:!!c.call};T.n++;T.cur=null;S.ext.away=false;award("tv_trip");save();ui();return T.last;}
function tvWelcome(L){if(!L)return;const names=L.pl.map(p=>TVI[p].n).join(", "),sp=L.sv&&TVP.find(p=>p.s===L.sv);
  dlg({head:"Муся вернулась!",text:(names?`Она побывала: ${names}. `:"Далеко уйти она не успела. ")+(sp?`Привезла ${sp.f} сувенир — «${IT[L.sv].n}». Он уже в «🧺 Вещи» → «Сувениры».`:L.pl.length?"Сувениры оттуда у тебя уже есть — зато сколько впечатлений!":"")+(L.om?"":" С дороги она пыльная — загляни в онсэн."),
    img:L.sv?itemThumb(IT[L.sv],60,60):"",ok:"Ура!",no:L.pl.length?"Открытки":"",onNo:()=>tvCard(T.nw[0]||L.pl[0])});}
function tvArrive(){if(tvA)return;tvA={k:"back",t0:now()};sfx("chime");}
function tvArrived(){const L=tvHome();tvA=null;pet.x=view.W/2;pet.home=pet.x;start("idle",true);react("😻",2.6);burst(16);chime([784,988,1175,1568]);setTimeout(()=>tvWelcome(L),1300);}
function tvCall(){const c=T.cur;if(!c||c.st!=="go")return;if(c.call){toast("Муся уже идёт домой — "+tvLeft());return;}
  dlg({head:"Позвать Мусю домой?",text:"Позвонишь в колокольчик — и минуты через две она будет у ворот. Сувенир привезёт только оттуда, откуда уже прислала открытку.",ok:"Позвонить",no:"Пусть гуляет",
    onOk:()=>{c.call=Math.min(c.t1,Date.now()+120e3);chime([1568,1319,1568,1319]);toast("🔔 Муся услышала — уже идёт домой");save();ui();}});}

// ───── panels ─────
function tvPack(){
  if(T.cur){if(T.cur.st==="gate"){closePanel();goRoom("entrance");}else openHub();return;}
  const eats=pantryEats();if(!pk.food||!eats.includes(pk.food))pk.food=eats[0]||null;
  const oms=tvOwned(["Омамори"]),lans=tvOwned(["Фонари","Светильники"]);if(pk.om&&!S.owned.has(pk.om))pk.om=null;if(pk.lan&&!S.owned.has(pk.lan))pk.lan=null;
  const chip=(key,on,pic,name,sub)=>`<button class="tv-chip ${on?"on":""}" data-x="${key}">${pic}<span>${name}</span>${sub?`<small>${sub}</small>`:""}</button>`;
  const none=(k,on)=>chip(k,on,`<span class="tv-none">—</span>`,"Без него","");
  const food=eats.length?`<div class="tv-row">${eats.map(id=>chip("tv:food:"+id,pk.food===id,fThumb(id,64,40),FOOD[id].n,"×"+S.pantry[id])).join("")}</div>`
   :`<p class="lead">В кладовой нет готовой еды. Приготовь что-нибудь на кухне («Кухня» → 🍳 Готовить) или поймай рыбу в пруду во дворике.</p><div class="row" style="display:flex;gap:8px;flex-wrap:wrap"><button class="btn" data-x="tv:go:kitchen">🍳 На кухню</button><button class="btn" data-x="tv:go:pond">🎣 К пруду</button></div>`;
  const om=oms.length?`<div class="tv-row">${none("tv:om:",!pk.om)}${oms.map(i=>chip("tv:om:"+i.id,pk.om===i.id,itemThumb(i,40,50),i.n,"")).join("")}</div>`:`<p class="lead">Омамори продаются в «🧺 Вещи» → «Омамори». <button class="btn" data-x="tv:shop:Омамори" style="padding:5px 12px;margin-left:4px">Выбрать</button></p>`;
  const lan=lans.length?`<div class="tv-row">${none("tv:lan:",!pk.lan)}${lans.map(i=>chip("tv:lan:"+i.id,pk.lan===i.id,itemThumb(i,40,50),i.n,"")).join("")}</div>`:`<p class="lead">Фонари — в «🧺 Вещи» → «Фонари». <button class="btn" data-x="tv:shop:Фонари" style="padding:5px 12px;margin-left:4px">Выбрать</button></p>`;
  openPanel("Собрать узелок",`<div class="tv-hero">${tvSp("tv_bundle",86,66)}<p class="lead">Муся собирается посмотреть Японию. Собери ей узелок — и жди открыток. Вернётся она с сувениром.</p></div>
   <h3 class="tv-h">🍱 Бэнто<small>обязательно</small></h3><p class="lead">Одно блюдо или рыбка из кладовой — перекусить в дороге.</p>${food}
   <h3 class="tv-h">⛩ Омамори<small>по желанию</small></h3><p class="lead">С оберегом в пути спокойнее, и Муся чаще находит редкие места.</p>${om}
   <h3 class="tv-h">🏮 Фонарь<small>по желанию</small></h3><p class="lead">С фонарём Муся не боится ночных троп.</p>${lan}
   <button class="btn primary tv-go" data-x="tv:leave" ${pk.food?"":"disabled"}>Проводить</button>
   <p class="lead" style="margin-top:10px">${T.n?"Путешествие длится от часа до трёх.":"Первое путешествие — примерно полчаса."} Пока Муси нет, её сытость и радость не убывают.</p>`,"tv_pack");}
function tvAlbum(){
  const cards=TVP.map(p=>{const on=T.pc[p.id],nw=T.nw.includes(p.id);
    return on?`<button class="tv-pc ${nw?"new":""}" data-x="tv:card:${p.id}"><span class="tv-img" style="${tvBg(p.id)}"></span><b>${p.n}</b><small>${p.r} · ${tvDate(on)}</small></button>`
      :`<div class="tv-pc off"><span class="tv-img">?</span><b>???</b><small>${p.rare==="om"?"редкое место — нужен омамори":p.rare==="lan"?"ночная тропа — нужен фонарь":"ещё не была"}</small></div>`;}).join("");
  const sv=TVP.filter(p=>S.owned.has(p.s)).length;
  openPanel("Открытки Муси",`<p class="lead">Муся присылает их из путешествий. Открытки: ${tvGot()} из ${TVP.length} · сувениры: ${sv} из ${TVP.length}.</p>${T.cur&&T.cur.st==="go"?`<p class="lead">Сейчас Муся в пути и вернётся ${tvLeft()}.</p>`:""}<div class="tv-grid">${cards}</div>
   ${T.cur?"":`<button class="btn primary" data-x="tv:pack" style="width:100%">🎒 Собрать узелок</button>`}`,"tv_album");}
function tvCard(id){const p=TVI[id];if(!p||!T.pc[id]){tvAlbum();return;}
  T.nw=T.nw.filter(q=>q!==id);save();ui();hubDot();tabDots();
  const got=TVP.filter(q=>T.pc[q.id]),nx=T.nw[0]||(got[(got.findIndex(q=>q.id===id)+1)%got.length]||{}).id;
  openPanel(p.n,`<div class="tv-big"><span class="tv-img" style="${tvBg(id)}"></span></div><p class="src">${p.r} · открытка пришла ${tvDate(T.pc[id])}</p>
   <p class="tv-cap">${p.c}</p><p class="tv-sign">🐾</p>
   <div class="row" style="display:flex;gap:8px;margin-top:10px"><button class="btn" data-x="tv:album">← Все открытки</button>${nx&&nx!==id?`<button class="btn primary" data-x="tv:card:${nx}">${T.nw.length?"Новая →":"Следующая →"}</button>`:""}</div>`,"tv_card");}
function tvOpen(){if(T.nw.length)tvCard(T.nw[0]);else tvAlbum();}

// ───── hooks ─────
hook("boot",()=>{tvSync(true);tvBoot=true;
  if(tvBackClosed)setTimeout(()=>toast("🎒 Муся вернулась — встречай у ворот ⛩"),3500);
  else if(tvClosed.length)setTimeout(()=>toast("🎴 Пока тебя не было, пришла открытка"),3500);});
hook("away",()=>{tvSync(true);if(!tvClosed.length)return;const p=TVI[tvClosed[tvClosed.length-1]];return{i:"🎴",t:tvClosed.length>1?`Пришли открытки от Муси (${tvClosed.length})`:`Пришла открытка ${p.f}`};});
hook("away",()=>{tvSync(true);if(tvBackClosed)return{i:"🎒",t:"Муся вернулась из путешествия и ждёт у ворот"};});
hook("sec",()=>{if(!tvBoot)return;tvSync(false);const c=T.cur;if(!c||c.st!=="gate"||tvA)return;
  if(S.room==="entrance"&&now()-tvRoomAt>1.2&&!overlaysOpen()&&!scene.on){tvArrive();return;}
  if(Date.now()-c.gateAt>90e3&&!scene.on){const L=tvHome();start("idle",true);react("😻",2.6);burst(12);chime([784,988,1175]);toast(L&&L.sv?"🎒 Муся вернулась и принесла сувенир!":"🎒 Муся вернулась домой!");}});
hook("room",id=>{tvRoomAt=now();if(tvA&&tvA.k==="back")tvArrived();else if(tvA)tvA=null;});
hook("hubDot",()=>T.nw.length>0||!!(T.cur&&T.cur.st==="gate"));
hook("tabDot",r=>r==="entrance"&&(T.nw.length>0||!!(T.cur&&T.cur.st==="gate")));
hook("tray",(tray,room)=>{if((S.trayMode[room]||"play")!=="play"||room!=="entrance"&&room!=="engawa")return;const row=tray.querySelector(".items");if(!row)return;
  const c=T.cur,b=[];
  if(!c)b.push(["tv:pack","🎒","В путешествие"]);else if(c.st==="gate"){if(room!=="entrance")b.push(["tv:meet","⛩","Встретить у ворот"]);}
  else if(room==="entrance")b.push(["tv:call","🔔",c.call?"Муся идёт домой":"Позвать домой"]);else b.push(["tv:left","🎒","Муся в пути"]);
  if(tvGot()||c)b.push(["tv:open","🎴","Открытки"+(T.nw.length?" · "+T.nw.length:"")]);
  row.insertAdjacentHTML("afterbegin",b.map(([k,i,n])=>`<button class="item wide" data-x="${k}"><span class="ico">${i}</span><span class="nm">${n}</span></button>`).join(""));});
hook("click",(k)=>{if(!k.startsWith("tv:"))return;const [,a,b]=k.split(":");
  if(a==="pack")tvPack();else if(a==="food"){pk.food=b;tvPack();}else if(a==="om"){pk.om=b||null;tvPack();}else if(a==="lan"){pk.lan=b||null;tvPack();}
  else if(a==="leave")tvLeave();else if(a==="call")tvCall();else if(a==="meet"){closePanel();goRoom("entrance");}
  else if(a==="open")tvOpen();else if(a==="album")tvAlbum();else if(a==="card")tvCard(b);else if(a==="left")toast("Муся вернётся "+tvLeft());
  else if(a==="go"){closePanel();const r=b==="kitchen"?"kitchen":"courtyard";goRoom(r);if(r==="kitchen"){S.trayMode.kitchen="cook";ui();}}
  else if(a==="shop"){closePanel();S.trayMode[S.room]="items";S.icatBy[S.room]=b;ui();}
  return true;});
hook("hub",()=>{const c=T.cur,st=!c?`Муся дома. Собери ей узелок — и она отправится смотреть Японию.`:c.st==="gate"?`Муся вернулась и ждёт у ворот ⛩`:`Муся в пути: вернётся ${tvLeft()}.`;
  return`<div class="hubc"><h4>🎒 Путешествия <i>旅</i></h4><p>${st}</p><p>Открытки: ${tvGot()} из ${TVP.length}${T.nw.length?` · <b style="color:var(--sakura)">новых: ${T.nw.length}</b>`:""}</p>
   <div class="row">${!c?`<button class="btn primary" data-x="tv:pack">🎒 Собрать узелок</button>`:c.st==="gate"?`<button class="btn primary" data-x="tv:meet">⛩ Встретить</button>`:""}<button class="btn" data-x="tv:open">🎴 Открытки</button></div></div>`;});
hook("album",el=>{el.insertAdjacentHTML("beforeend",`<h3 class="bh">Открытки из путешествий</h3><p class="lead">Муся присылает их с дороги: ${tvGot()} из ${TVP.length}.</p>
  <div class="tv-mini">${TVP.map(p=>T.pc[p.id]?`<span class="tv-img" data-x="tv:card:${p.id}" style="${tvBg(p.id)};cursor:pointer"></span>`:`<span class="tv-img off"></span>`).join("")}</div>
  <button class="btn" data-x="tv:album" style="margin-bottom:10px">🎴 Альбом открыток</button>`);});
// the album is not the shared panel: route our buttons ourselves
hook("hit",(x,y)=>{
  if(S.room==="entrance"){const inR=r=>r&&x>r[0]&&x<r[0]+r[2]&&y>r[1]&&y<r[1]+r[3];
    if(inR(tvHit.bell)){tone(1568,.5,"sine",.05);tvCall();return true;}
    if(inR(tvHit.post)){sfx("pop");if(tvGot()||T.nw.length)tvOpen();else toast("Почтовый ящик пуст — Муся ещё не уезжала");return true;}}
  if(petAway()&&!tvA&&Math.abs(x-pet.x)<90*view.s&&y>view.floor-210*view.s&&y<view.floor+12*view.s){toast(T.cur&&T.cur.st==="gate"?"Муся ждёт у ворот ⛩":"Муся в путешествии");return true;}});
// the post box by the gate, the call bell on the torii, Musya walking out through the torii / back home
// a sprite from our atlas standing on (ix,iy) — or hanging from it when the sprite is anchored at the top
function tvSprite(id,ix,iy,hImg,d,al=1,rot=0){if(!TVIM)return null;const r=TVJ.sp[id],top=r[4]==="t",[x1,ya]=imgToStage(ix,top?iy:iy-hImg,d),[,yb]=imgToStage(ix,top?iy+hImg:iy,d),h=Math.max(4,yb-ya),w=h*r[2]/r[3];
  const g=tvG;g.globalCompositeOperation="source-over";g.globalAlpha=1;g.clearRect(0,0,r[2],r[3]);g.drawImage(TVIM,r[0],r[1],r[2],r[3],0,0,r[2],r[3]);   // dim it to the room's night light
  g.globalCompositeOperation="source-atop";g.fillStyle=TINT[S.room]||"rgba(8,12,14,.4)";g.fillRect(0,0,r[2],r[3]);g.globalCompositeOperation="source-over";
  ctx.save();ctx.globalAlpha=al;ctx.translate(x1,top?ya:yb);ctx.rotate(rot);ctx.drawImage(tvCv,0,0,r[2],r[3],-w/2,top?0:-h,w,h);ctx.restore();return[x1-w/2,ya,w,h];}
function tvCat(t,x,y,sc,al,right){const st=right?"moveRight":"moveLeft",im=IMG[st];if(!im||al<=0)return;const f=Math.floor(t*9)%8,g=tvG;
  g.globalCompositeOperation="source-over";g.globalAlpha=1;g.clearRect(0,0,384,416);g.drawImage(im,f*384,0,384,416,0,0,384,416);
  if(TVIM){const r=TVJ.sp.tv_bundle,bx=right?212:172;g.drawImage(TVIM,r[0],r[1],r[2],r[3],bx-48,118+Math.sin(t*18)*2,96,75);}
  g.globalCompositeOperation="source-atop";g.fillStyle=TINT.entrance;g.fillRect(0,0,384,416);g.globalCompositeOperation="source-over";
  ctx.save();ctx.globalAlpha=al*.35;ctx.fillStyle="#000";ctx.beginPath();ctx.ellipse(x,y+3*sc,55*sc,8*sc,0,0,Math.PI*2);ctx.fill();ctx.globalAlpha=al;ctx.drawImage(tvCv,x-96*sc,y-195*sc,192*sc,208*sc);ctx.restore();}
hook("draw",(t,front)=>{if(S.room!=="entrance"||front)return;
  const nw=T.nw.length>0;tvHit.post=tvSprite("tv_post",visX(585,60),1050,175,CAT_D);
  if(nw&&TVIM){const [px_,py_]=imgToStage(visX(585,60),1050-112,CAT_D),k=BGM.k,pul=.6+.4*Math.sin(t*3);
    ctx.save();const gr=ctx.createRadialGradient(px_,py_,0,px_,py_,90*k);gr.addColorStop(0,`rgba(255,200,120,${.35*pul})`);gr.addColorStop(1,"rgba(255,200,120,0)");ctx.fillStyle=gr;ctx.fillRect(px_-90*k,py_-90*k,180*k,180*k);ctx.restore();
    tvSprite("tv_card",visX(585,60)+6,950,40,CAT_D,1,-.18);}
  tvHit.bell=T.cur&&T.cur.st==="go"?tvSprite("tv_bell",1090,548,105,.38,1,Math.sin(t*1.7)*.06+(T.cur.call?Math.sin(t*14)*.12:0)):null;
  if(!tvA)return;const e=now()-tvA.t0,s=view.s,[gx,gy]=imgToStage(900,1002,.38),fy=view.floor+camOff(CAT_D)[1];
  if(tvA.k==="go"){const u=clamp(e/3.6,0,1),v=1-Math.pow(1-u,1.5),x0=tvA.x0,x=mix(x0,gx,v)+Math.sin(v*Math.PI)*46*s,y=mix(fy,gy,v),sc=s*mix(1,.24,v),al=u<.72?1:1-(u-.72)/.28;
    tvCat(t,x,y,sc,al,(gx-x0)+Math.cos(v*Math.PI)*Math.PI*46*s>0);
    if(u>.6){const k=Math.sin(clamp((u-.6)/.4,0,1)*Math.PI),r=120*BGM.k;ctx.save();const gr=ctx.createRadialGradient(gx,gy-40*BGM.k,0,gx,gy-40*BGM.k,r);gr.addColorStop(0,`rgba(255,214,150,${.45*k})`);gr.addColorStop(1,"rgba(255,214,150,0)");ctx.fillStyle=gr;ctx.fillRect(gx-r,gy-40*BGM.k-r,2*r,2*r);ctx.restore();}
    if(u>=1){tvA=null;toast("🎒 Муся ушла путешествовать");}}
  else{const u=clamp(e/3.0,0,1),v=Math.pow(u,1.3),x1=view.W/2,x=mix(gx,x1,v)-Math.sin(v*Math.PI)*46*s,y=mix(gy,fy,v),sc=s*mix(.24,1,v),al=clamp(u/.25,0,1);
    if(u<.35){const k=Math.sin(clamp(u/.35,0,1)*Math.PI),r=120*BGM.k;ctx.save();const gr=ctx.createRadialGradient(gx,gy-40*BGM.k,0,gx,gy-40*BGM.k,r);gr.addColorStop(0,`rgba(255,214,150,${.45*k})`);gr.addColorStop(1,"rgba(255,214,150,0)");ctx.fillStyle=gr;ctx.fillRect(gx-r,gy-40*BGM.k-r,2*r,2*r);ctx.restore();}
    tvCat(t,x,y,sc,al,(x1-gx)-Math.cos(v*Math.PI)*Math.PI*46*s>0);if(u>=1)tvArrived();}});
X.tv={T:()=>T,pk,pack:tvPack,leave:tvLeave,album:tvAlbum,card:tvCard,call:tvCall,sync:tvSync,
  skip(min){const c=T.cur,d=min*60e3;if(!c)return;for(const k of["t0","t1","call","gateAt"])if(c[k])c[k]-=d;for(const L of c.legs){L.at-=d;if(L.got)L.got-=d;}tvSync(false);}};
}
