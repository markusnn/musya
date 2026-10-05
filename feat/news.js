{
// ───────────────────────── «Вестник ёкаев» (妖怪新聞): a weekly kawaraban about the player's week ─────────────────────────
// Every Monday after 6:00 (week of today()) a new issue comes out about the previous Mon–Sun; the very first one at once
// (about the last seven days). The roll lies at the foot of the travel post box (entrance) until read; hub dot, toast.
// An issue keeps only small data; the text is rebuilt from it and from the disc()/candle timestamps of its range.
// S.ext.news = {iss:[{n,k,a,b,r,f,g,act,c,cr,cd,wx,se}], w:{k,fd,gs,gv,act,c} this week's counters, pw: last week's, tq}
const SB=S.ext.news||(S.ext.news={iss:[],w:null,pw:null,tq:0});SB.iss=SB.iss||[];
STAMPS.push(["sb_1","報","Первый номер","Прочитай «Вестник ёкаев» (家 → Вестник ёкаев)"],["sb_4","読","Подписчик","Прочитай 4 номера «Вестника ёкаев»"],
 ["sb_10","刊","Подшивка","Собери и прочитай 10 номеров «Вестника ёкаев»"]);
const SB_MON=["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"];
const sbPl=(n,a,b,c)=>{const d=n%10,h=n%100;return d===1&&h!==11?a:d>=2&&d<=4&&(h<12||h>14)?b:c;};
const sbNow=()=>Date.now()+DATE_SHIFT;   // game-calendar ms (disc() stamps real ms → add DATE_SHIFT)
function sbMonD(d){const x=new Date(d);x.setHours(0,0,0,0);x.setDate(x.getDate()-((x.getDay()+6)%7));return x;}
const sbMonK=()=>dayKey(sbMonD(today()));
function sbHash(s){let h=2166136261;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619);}return h>>>0;}
function sbRnd(sd){let s=sd>>>0;return()=>{s=(s+0x6D2B79F5)>>>0;let t=s;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return((t^t>>>14)>>>0)/4294967296;};}
function sbPick(r,arr,n){const a=arr.slice(),o=[];while(a.length&&o.length<n)o.push(a.splice(Math.floor(r()*a.length),1)[0]);return o;}
// ── this week's counters (fed by game events) ──
function sbW(){const k=sbMonK();if(!SB.w||SB.w.k!==k){if(SB.w)SB.pw=SB.w;SB.w={k,fd:{},gs:{},gv:{},act:{},c:{}};}return SB.w;}
hook("ev",(ev,d)=>{const w=sbW(),inc=(o,k)=>{o[k]=(o[k]||0)+1;};
  if(ev==="food"&&d)inc(w.fd,d);else if(ev==="guest"&&d&&d.id)inc(w.gs,d.id);else if(ev==="act"&&d)inc(w.act,d);
  else if(["game","fish","cook","bath","harvest","kaidan"].includes(ev))inc(w.c,ev);});
const sbTop=o=>{let b=null;for(const k in o||{})if(!b||o[k]>b[1])b=[k,o[k]];return b;};
// ── names and pictures of what happened ──
function sbName(kind,id){try{const h=X[kind];if(h&&typeof h.name==="function"){const n=h.name(id);if(n)return n;}}catch(e){}
  if(kind==="q")return(STORY[+id]||{}).title||"";if(kind==="k")return(KAIDAN[+id]||{}).t||"";if(kind==="fe")return(FEST.find(F=>F.id===id)||{}).n||"";
  if(kind==="c")return(CROPS.find(c=>c.id===id)||{}).n||"";if(kind==="r")return(RECIPES.find(r=>r.id===id)||{}).n||"";
  if(kind==="friend"){const g=GUESTS.find(q=>q.id===id.split("_")[0]);if(g)return g.n;}
  const b=sbBest(id);return(IT[id]&&IT[id].n)||(FOOD[id]&&FOOD[id].n)||(b&&b[2])||(ROOMS.find(r=>r.id===id)||{}).ru||(GUESTS.find(g=>g.id===id)||{}).n||"";}
const sbBest=id=>BESTIARY.find(b=>b[0]===id||b[0]==="rg_"+id||b[0]==="vs_"+id);
function sbLabel(e){try{if(X.cd&&X.cd.label)return X.cd.label((e.d?"d:":"")+e.kind+":"+e.id);}catch(x){}return sbName(e.kind,e.id)||"Новая находка";}
const sbFoodN=id=>(FOOD[id]&&FOOD[id].n)||(FOODS.find(f=>f.id===id)||{}).n||(FAIRFOOD.find(f=>f.id===id)||{}).n||"угощение";
function sbFoodPic(id,s){const f=FOODS.find(q=>q.id===id)||FAIRFOOD.find(q=>q.id===id);if(f)return`<span class="sb-emo" style="font-size:${s*.7}px">${f.i}</span>`;try{return fThumb(id,s,s)||"";}catch(e){return"";}}
function sbPic(e,s){const {kind,id}=e;try{
  const gid=kind==="friend"?id.split("_")[0]:id,g=GUESTS.find(q=>q.id===gid);if(g&&(kind==="g"||kind==="friend"||kind==="rareguest"))return`<img src="assets/mon/${g.mon}.webp" alt="">`;
  const b=sbBest(id);if(b&&b[1]&&/^(b|rareguest|visitor|haunt|parade|rumor)$/.test(kind))return`<img src="assets/mon/${b[1].replace(/_open$/,"")}.webp" alt="">`;
  if(IT[id])return itemThumb(IT[id],s,s);
  if(kind==="r"){const R=RECIPES.find(r=>r.id===id);if(R&&R.dish)return fThumb(R.dish,s,s);}
  if(kind==="f"&&FOOD[id])return fThumb(id,s,s);if(kind==="c"&&FOOD["v_"+id])return fThumb("v_"+id,s,s);
  if(kind==="pet")return`<span class="sb-cat sm" style="background-image:url(assets/play@2x.webp)"></span>`;}catch(x){}
  return`<img src="${sbCut(SB_MOT[kind]||"moon")}" alt="">`;}
// what happened in [a,b): disc() stamps + the candle log (kaidan, bestiary, friends, crops, fish, recipes, festivals)
function sbEv(a,b){const o=[],D=S.ext.disc||{};
  for(const kind in D){if(kind==="news")continue;for(const id in D[kind]){const t0=D[kind][id];if(typeof t0!=="number")continue;const t=t0+DATE_SHIFT;if(t>=a&&t<b)o.push({kind,id,t,d:1});}}
  const L=(X.cd&&X.cd.st&&X.cd.st.log)||[];for(const [key,t0] of L){if(!t0||typeof key!=="string"||key.startsWith("d:"))continue;const t=t0+DATE_SHIFT,i=key.indexOf(":");if(t>=a&&t<b&&i>0)o.push({kind:key.slice(0,i),id:key.slice(i+1),t});}
  return o.sort((x,y)=>x.t-y.t);}
const SB_WT={room:10,q:9,chapter2:9,rareguest:9,pet:9,birthday:8,parade:8,fe:8,holiday:8,capsule:7,bloom:7,g:6,b:6,trust:6,haunt:6,visitor:6,rumor:6,friend:5,crane:5,
  dream:5,postcard:5,souvenir:5,star:5,season:5,daruma:4,ikebana:4,bonsai:4,tea:4,ryokan:4,koi:4,bird:4,shadow:4,paint:4,r:3,c:3,f:3,k:3,find:3};
const sbWt=e=>e.kind==="crane"?(e.id==="m100"||e.id==="m1000"?10:5):e.kind==="friend"&&/_5$/.test(e.id)?8:SB_WT[e.kind]||3;
const SB_MOT={room:"house",q:"scroll",chapter2:"scroll",k:"scroll",fe:"lantern",holiday:"lantern",parade:"lantern",birthday:"lantern",crane:"crane",bloom:"flower",
  season:"flower",star:"moon",koi:"wave",f:"wave",capsule:"house",trust:"moon",dream:"moon"};
// ── the headline: the most notable thing of the week ──
function sbHead(e,cr){const n=sbName(e.kind,e.id),L=sbLabel(e);
  switch(e.kind){
  case"room":return[`В доме открылась новая комната!`,`Двери, что так долго стояли запертыми, наконец поддались: теперь в доме есть ${n?`комната «${n}»`:"ещё одна комната"}. Первой внутрь, разумеется, вошла Муся — обнюхала все углы, посидела посередине и осталась довольна.`];
  case"rareguest":return[`Редкий гость: ${n||"кто-то из старых духов"}`,`Такие гости заходят раз в сто лет — а к Мусе вот заглянули. Очевидцы клянутся, что видели всё своими глазами, и требуют, чтобы редакция им поверила. Редакция верит.`];
  case"q":case"chapter2":return[`Новая глава${n?`: «${n}»`:" истории дома"}`,`История дома продолжается. Подробностей редакция не раскрывает, чтобы не портить удовольствие, но намекает: без Муси здесь не обошлось.`];
  case"pet":return[`В доме — пополнение!`,`Маленький котёнок обрёл дом и имя. Муся делает вид, что ей всё равно, но уже трижды проверила, как устроился новенький.`];
  case"crane":{const m=+String(e.id).slice(1)||cr;return m>=100?[`Сложен ${m}-й журавлик!`,`Нить бумажных птиц выросла до ${m}. Старики говорят: тысяча журавликов исполняет желание. Ёкаи уже спорят, о чём попросит Муся.`]:
    [`Журавликов уже ${m}`,`Бумажная стая растёт: на нитях висит ${m} ${sbPl(m,"журавлик","журавлика","журавликов")}. Сквозняк качает их по ночам, и кажется, что они вот-вот полетят.`];}
  case"fe":case"holiday":return[`Праздник${n?` «${n}»`:""} отгремел`,`Фонари, сладости и весёлая суматоха: дом гулял от ворот до кухни. Ёкаи вспоминают праздник до сих пор и уже ждут следующего.`];
  case"birthday":return[`День рождения в доме!`,`Свечи, подарки и торжественный вид Муси. Гости у ворот поздравляли наперебой, а самый маленький ёкай даже спел. Фальшиво, но от души.`];
  case"parade":return[`Ночной парад у ворот`,`Хякки яко — шествие ста духов — прошёл мимо дома. ${n?`Впереди, по словам свидетелей, шёл ${n}. `:""}Муся смотрела из-за сёдзи и не моргнула ни разу.`];
  case"friend":return/_5$/.test(e.id)?[`${n||"Друг"} пришёл в гости!`,`Долгая переписка закончилась встречей: ${n||"гость"} переступил порог дома. Угощение съедено, подарок вручён, Муся обнюхала гостя с ног до головы.`]:
    [`Письмо от ${n||"друга"}`,`Почтальон принёс конверт, пахнущий дорогой и дождём. Что в нём — личное дело Муси, но ёкаи у ворот уже строят догадки.`];
  case"g":return[`${n||"Гость"} — новый друг дома`,`У ворот подружились: гость получил угощение, а дом — первое сердечко дружбы. Редакция считает это началом долгой истории.`];
  case"b":case"haunt":case"visitor":case"rumor":return[`Замечен ёкай${n?`: ${n}`:""}`,`Свидетели описывают встречу по-разному, но сходятся в одном: было жутко интересно. Редакция напоминает: при встрече с ёкаем кланяйтесь вежливо и не показывайте пальцем.`];
  case"bloom":return[`Сакура зацвела!`,`Дерево, за которым ухаживали столько дней, покрылось розовыми цветами. Лепестки летят в чай, в миску и Мусе на нос.`];
  case"capsule":return[`Капсула времени открыта`,`Коробка на стене кура наконец открылась. Что внутри — знают только Муся и тот, кто её закладывал. Остальные гадают.`];
  case"season":{const sn=SB_SN[String(e.id).split("-")[0]];return[`Пришла ${sn||"новая пора года"}`,`Дом встретил новую пору: другие звуки во дворе, другой свет за сёдзи, другие гости у ворот. Муся обошла все комнаты и проверила, всё ли на месте.`];}
  case"trust":return[`Муся доверяет всё больше`,`Свидетели сообщают: Муся всё чаще подходит сама, щурится и подставляет лоб. У кошек это значит больше, чем любые слова.`];}
  return[`Новость недели: ${L.charAt(0).toLowerCase()+L.slice(1)}`,`Весть облетела все крыши ещё до рассвета. Ёкаи обсуждают её у ворот, а Муся делает вид, что ничего особенного не случилось.`];}
// ── short news («Происшествия») ──
function sbLine(e){const n=sbName(e.kind,e.id),L=sbLabel(e);
  switch(e.kind){
  case"find":return`Муся принесла в дом находку${n?` — «${n}»`:""}. Откуда — не признаётся.`;
  case"rareguest":return`К дому заглянул редкий гость${n?` — ${n}`:""}. Свидетели до сих пор не верят глазам.`;
  case"visitor":return`${n||"Ёкай"} пришёл на огонёк: его выманили вещи, расставленные в доме.`;
  case"rumor":return`Слух подтвердился${n?`: «${n}»`:""}. Редакция приносит извинения скептикам.`;
  case"room":return`Открыта новая комната${n?` — «${n}»`:""}. Муся первой обнюхала все углы.`;
  case"q":case"chapter2":return`Дописана глава${n?` «${n}»`:" истории"}. Продолжение следует.`;
  case"k":return`При свете андона прочитан кайдан${n?` «${n}»`:""}. Свидетели спали с огнём.`;
  case"b":return`Замечен ёкай${n?`: ${n}`:""}. Просим соблюдать вежливость при встрече.`;
  case"g":return`${n||"Гость"} теперь друг дома: первое сердечко дружбы получено у ворот.`;
  case"c":return`Огород порадовал: первый урожай${n?` — ${n.toLowerCase()}`:""}.`;
  case"f":return`Рыбалка удалась: в улове впервые ${n?n.toLowerCase():"новая рыба"}.`;
  case"r":return`На кухне впервые приготовлено блюдо${n?` «${n}»`:""}. Запах дошёл до соседних холмов.`;
  case"fe":case"holiday":return`Отгремел праздник${n?` «${n}»`:""}: фонари, сладости, суматоха.`;
  case"crane":{const m=+String(e.id).slice(1);return m?`Нить журавликов выросла: уже ${m} бумажных птиц.`:"Сложен новый журавлик.";}
  case"pet":return"В доме поселился котёнок. Муся присматривает за ним краем глаза.";
  case"friend":return/_5$/.test(e.id)?`${n||"Друг"} приходил в гости по приглашению.`:`Пришло письмо от ${n||"друга"}. Конверт пахнет дорогой.`;
  case"bloom":return"Сакура во дворике зацвела. Лепестки повсюду.";
  case"postcard":return`Из путешествия пришла открытка${n?` «${n}»`:""}.`;
  case"souvenir":return`Муся привезла из путешествия сувенир${n?` — «${n}»`:""}.`;
  case"trust":return`Муся доверяет всё больше${n?`: теперь она «${n.toLowerCase()}»`:""}.`;
  case"season":{const sn=SB_SN[String(e.id).split("-")[0]];return sn?`Пришла ${sn}. Дом переоделся по сезону.`:"Сменилась пора года.";}
  case"dream":return`Мусе приснился сон${n?` — «${n}»`:""}. Баку его не съел.`;}
  return L+".";}
const SB_SN={winter:"зима",spring:"весна",tsuyu:"пора дождей",summer:"лето",autumn:"осень"};
const SB_QUIET={winter:["Ночью выпал снег. На веранде нашли следы маленьких лап — подозревается Муся.","Сосулька над тории выросла на целый палец. Рост продолжается.","Снеговик у ворот стоит на посту третий день. Нарушений не обнаружено."],
  spring:["Во дворике распустились первые цветы. Пчела проверила каждый.","Ласточки вернулись под крышу ворот и заняли прошлогоднее гнездо.","Тёплый дождь вымыл камни во дворике. Камни довольны."],
  tsuyu:["Дождь шёл семь дней подряд. Каппа счастлив.","Улитка переползла веранду за одну ночь — новый рекорд.","Гортензии у ворот сменили цвет с голубого на лиловый."],
  summer:["Цикады пели с утра до вечера. Жалоб от соседей не поступало.","Над прудом летали светлячки. Муся пересчитала их — сбилась на седьмом.","Ветряной колокольчик звенел всю ночь, отгоняя жару."],
  autumn:["Ветер унёс со двора кленовый лист. Поиски продолжаются.","Сверчок под верандой пел до полуночи. Жалоб не поступало.","Луна вставала над тории каждую ночь, как и положено. Редакция проверила."]};
// ── gossip, ads, the cat of the week, the weather ──
const SB_GOS=[["Адзуки-арай","слышал у реки, что луна в этом месяце круглее обычного. Проверить не успел — мыл фасоль."],["Каракаса","клянётся, что видел, как Муся улыбалась во сне. Улыбалась хитро."],
 ["Бакэ-дзори","рассказывает всем, что его поносили по дому и забыли у ворот. Обиделся, но ненадолго."],["Лиса-невеста","намекает, что скоро снова пойдёт дождь при солнце. Значит, кто-то опять женится."],
 ["Ёсудзумэ","пела под окнами спальни и уверяет, что Муся подпевала. Мурлыканьем."],["Мокумокурэн","смотрел из сёдзи всеми глазами и докладывает: ночью кто-то таскал сушёную рыбку. Следы ведут к лежанке Муси."],
 ["Аканамэ","жалуется, что в онсэне стало слишком чисто: лизать совершенно нечего."],["Нуппэппо","всё ещё ищет свои брови. Нашедших просят обратиться в редакцию."],
 ["Камаитати","пронеслись по двору втроём и уверяют, что это был просто ветер."],["Тануки","пытался превратиться в чайник и почти успел: носик получился, ручка — нет."],
 ["Каппа","говорит, что видел в пруду лицо луны. Луна, по его словам, подмигнула."],["Дзасики-вараси","пряталась в шкафу целую ночь, но её так никто и не начал искать. Обижена."],
 ["Тётин-обакэ","уверяет, что у него открылся второй глаз. Редакция проверила — показалось."],["Нэкомата","шепчет, что полная луна — к танцам на крыше. Хвосты брать с собой."]];
const SB_ADS=[["Тануки","Меняю дубликаты на данго. Листья не предлагать — у самого полно."],["Каппа","Ищу огурцы. Дорого. Можно прямо с грядки."],["Каракаса","Сдаю себя в аренду на дождливые вечера. Прыгаю сам, ручка удобная."],
 ["Адзуки-арай","Мою фасоль у реки. Шумно, но качественно. Работаю по ночам."],["Тётин-обакэ","Освещу дорогу до дома. Оплата — маслом для фитиля."],["Нуппэппо","Ищу зеркало, в котором видно лицо. Любое. Своё."],
 ["Аканамэ","Вылижу баню до блеска. Ночью, без свидетелей."],["Бакэ-дзори","Старые сандалии ищут ноги. Не выбрасывайте обувь — она всё помнит."],["Мокумокурэн","Присмотрю за домом. Глаз много, все внимательные."],
 ["Лиса-невеста","Нужен дождь при солнце на субботу. Облака, откликнитесь!"],["Дзасики-вараси","Прячусь в домах, приношу удачу. Не ищите меня. Ну поищите немножко."],
 ["Камаитати","Стрижём траву и сквозняки. Быстро, втроём, без следов."],["Ёсудзумэ","Пою по ночам. Принимаю заказы на колыбельные."],["Нэкомата","Учу кошачьим танцам при полной луне. Хвосты свои."]];
const SB_CAT={sleep:["sleep","Спала много и со вкусом: клубком, на спине, с лапой на носу. Специалисты по сну из редакции снимают шляпы."],
 groom:["groom","Умывалась так старательно, что шёрстка блестит даже в темноте. За ушами — идеальный порядок."],
 play:["yarn","Носилась по дому, гоняла клубок и сражалась с невидимыми врагами. Невидимые враги отступили."],
 eat:["treat","Ела с удовольствием и всякий раз провожала миску долгим взглядом: вдруг там ещё что-то осталось."],
 purr:["purr","Мурлыкала, мяла лапками подушки и грела всех, кто садился рядом. Дом от этого заметно потеплел."],
 hide:["box","Пряталась в коробках и выглядывала из-за углов — каждый раз с таким видом, будто её тут нет."],
 stretch:["stretch","Потягивалась после каждого сна: от кончика носа до кончика хвоста, не пропуская ни сантиметра."],
 calm:["rest","Сидела у сёдзи, смотрела на луну и шевелила усами. Редакция считает это лучшим занятием недели."]};
const SB_ACT={sleep:"sleep",groom:"groom",yarn:"play",zoomies:"play",butterfly:"play",highfive:"play",firefly:"play",petals:"play",cursor:"play",poke:"play",
  treat:"eat",beg:"eat",purr:"purr",knead:"purr",box:"hide",hide:"hide",peek:"hide",house:"hide",stretch:"stretch"};
const SB_WXK=c=>c==null?"cloud":c<=1?"clear":c<=3?"cloud":c<=48?"fog":c<=57?"drizzle":c<=67||c>=80&&c<=82?"rain":c<=77||c===85||c===86?"snow":"thunder";
const SB_WXI={clear:["☀️","ясно"],cloud:["⛅","облачно"],fog:["🌫","туман"],drizzle:["🌦","морось"],rain:["🌧","дождь"],snow:["🌨","снег"],thunder:["⛈","гроза"]};
const SB_CITY={nn:"в Нижнем Новгороде",msk:"в Москве",spb:"в Санкт-Петербурге",kzn:"в Казани",ekb:"в Екатеринбурге",nsk:"в Новосибирске",sochi:"в Сочи",tokyo:"в Токио",kyoto:"в Киото"};
const SB_SEA={winter:[["snow","cloud","clear","snow","fog","cloud"],"Юки-онна обещает мороз по ночам и снег к выходным. Варежки держите поближе к андону."],
 spring:[["clear","cloud","drizzle","rain","clear","cloud"],"Ласточки летают высоко — значит, неделя будет тёплой. Зонтик-каракаса всё равно просится на прогулку."],
 tsuyu:[["rain","rain","drizzle","cloud","rain","fog"],"Сезон дождей: Амэ-онна никуда не торопится. Каппа просит не закрывать пруд крышкой."],
 summer:[["clear","clear","thunder","cloud","clear","clear"],"Жара днём, светлячки ночью, к середине недели — гроза. Райдзю уже бьёт в барабаны где-то за горами."],
 autumn:[["cloud","rain","clear","fog","drizzle","cloud","clear"],"Ёсудзумэ обещает туман по утрам, листопад и дождь, который Амэ-онна принесёт к середине недели."]};
const sbSea=d=>{const m=d.getMonth()+1;return m===12||m<=2?"winter":m<=5?"spring":m===6?"tsuyu":m<=8?"summer":"autumn";};
// ── publishing ──
const sbLast=()=>SB.iss[SB.iss.length-1];
const sbUnread=()=>{for(let i=SB.iss.length-1;i>=0;i--)if(!SB.iss[i].r)return SB.iss[i];return null;};
function sbDue(){const L=sbLast();if(!L)return true;if(L.k>=sbMonK())return false;const d=today();return d.getDay()!==1||hourNow()>=6;}
function sbPublish(){const w=sbW(),L=sbLast(),k=sbMonK(),mon=sbMonD(today()),pm=new Date(mon);pm.setDate(pm.getDate()-7);
  const first=!L,b=first?sbNow():mon.getTime(),a=first?(()=>{const x=new Date(sbNow());x.setHours(0,0,0,0);x.setDate(x.getDate()-6);return x.getTime();})():Math.max(pm.getTime(),L.b||0);
  const E0={fd:{},gs:{},gv:{},act:{},c:{}},C=first?sbMerge(SB.pw||E0,w):(SB.pw&&SB.pw.k===dayKey(pm)?SB.pw:E0);
  const gv={};for(const d in C.gv||{})gv[C.gv[d]]=(gv[C.gv[d]]||0)+1;if(!Object.keys(gv).length)Object.assign(gv,C.gs||{});   // days at the gate, else feedings
  const W=S.ext.wx&&S.ext.wx.w,sum=o=>Object.values(o||{}).reduce((s,v)=>s+v,0);
  const I={n:SB.iss.length+1,k,a,b,r:0,f:sbTop(C.fd)||0,g:sbTop(gv)||0,act:sbTop(C.act)||0,c:{m:sum(C.fd),gm:(C.c||{}).game||0,fi:(C.c||{}).fish||0,ck:(C.c||{}).cook||0,bt:(C.c||{}).bath||0},
    cr:(S.ext.cranes||{}).n||0,cd:X.cd&&X.cd.out?X.cd.out():0,wx:W?[W.code,Math.round(W.temp),S.ext.wx.city]:0,se:X.wx&&X.wx.season?X.wx.season():sbSea(today())};
  SB.iss.push(I);SB.tq=1;save();hubDot();tabDots();return I;}
function sbMerge(A,B){const o={};for(const f of ["fd","gs","act","c"]){o[f]={};for(const X_ of [A,B])for(const k in X_[f]||{})o[f][k]=(o[f][k]||0)+X_[f][k];}o.gv=Object.assign({},A.gv||{},B.gv||{});return o;}
let sbSecN=0;
function sbTick(){sbW();if(++sbSecN<4)return;if(S.guest&&S.guest.state==="here"&&S.guest.day)SB.w.gv[S.guest.day]=S.guest.id;if(sbDue())sbPublish();}
// ── the page ──
function sbRange(I){const A=new Date(I.a),B=new Date(Math.max(I.a,I.b-1));
  return A.getMonth()===B.getMonth()?`${A.getDate()}–${B.getDate()} ${SB_MON[B.getMonth()]}`:`${A.getDate()} ${SB_MON[A.getMonth()]} — ${B.getDate()} ${SB_MON[B.getMonth()]}`;}
function sbHtml(I){const r=sbRnd(sbHash(I.k+"#"+I.n)),E=sbEv(I.a,I.b),y=new Date(I.b).getFullYear();
  const top=E.slice().sort((p,q)=>sbWt(q)-sbWt(p)||q.t-p.t)[0],[ht,hl]=top?sbHead(top,I.cr):["Тихая неделя: ёкаи отдыхают","Редакция обошла дом от ворот до онсэна и не нашла ни одного громкого происшествия. Муся спала, ела и смотрела на луну — а это, как известно, тоже большое дело."];
  const hp=top?sbPic(top,120):`<img src="${sbCut("moon")}" alt="">`;
  // short news: the rest of the week by weight, padded with quiet notes
  const rest=E.filter(e=>e!==top).sort((p,q)=>sbWt(q)-sbWt(p)||q.t-p.t),seenL=new Set(),nw=[];
  for(const e of rest){const l=sbLine(e);if(seenL.has(l))continue;seenL.add(l);nw.push([sbPic(e,44),l]);if(nw.length>=5)break;}
  if(nw.length<3)for(const l of sbPick(r,SB_QUIET[I.se]||SB_QUIET.autumn,3-nw.length))nw.push([`<img src="${sbCut(["moon","wave","flower"][Math.floor(r()*3)])}" alt="">`,l]);
  // gossip: facts of the week first, then the general chatter
  const g1=[];if(I.f)g1.push(["Тануки",`шепчет, что Муся за неделю ${I.f[1]} ${sbPl(I.f[1],"раз","раза","раз")} лакомилась блюдом «${sbFoodN(I.f[0])}». «Я считал, у меня лапки!»`]);
  if(I.g){const gn=(GUESTS.find(q=>q.id===I.g[0])||{}).n;if(gn)g1.push([I.g[0]==="nekomata"?"Каракаса":"Нэкомата",`уверяет, что ${gn} ходит к воротам не ради угощения, а чтобы поглазеть на Мусю.`]);}
  if(I.cr)g1.push(["Каппа",`ворчит: «Журавликов уже ${I.cr}. Ещё немного — и дом улетит на юг вместе с ними».`]);
  if(I.cd)g1.push(["Тётин-обакэ",`подсчитал, что погасло ${I.cd} ${sbPl(I.cd,"свеча","свечи","свечей")} из ста. «Что будет на сотой — не скажу», — моргает он.`]);
  if(E.length>=4)g1.push(["Дзасики-вараси",`хихикает: за неделю в доме случилось ${E.length} ${sbPl(E.length,"чудо","чуда","чудес")}, «и это только те, что я видела».`]);
  const g2=sbPick(r,g1,2),gos=[...g2,...sbPick(r,SB_GOS.filter(q=>!g2.some(p=>p[0]===q[0])),4)].slice(0,4);
  // ratings
  const tg=I.g?[(GUESTS.find(q=>q.id===I.g[0])||{}).n,`${I.g[1]} ${sbPl(I.g[1],"визит","визита","визитов")}`]:(()=>{const b=GUESTS.map(q=>[q.n,(S.friends[q.id]||{}).n||0]).sort((p,q)=>q[1]-p[1])[0];return b&&b[1]?[b[0],`♥${Math.min(5,b[1])} — по сердечкам дружбы`]:null;})();
  const rows=[["門","Самый частый гость у ворот",tg?`<b>${tg[0]}</b> · ${tg[1]}`:"ворота пустовали — гости ещё в пути"],
   ["食","Любимая еда Муси",I.f?`<b>${sbFoodN(I.f[0])}</b> · ${I.f[1]} ${sbPl(I.f[1],"раз","раза","раз")}`:"редакция не успела подсчитать: Муся ела слишком быстро"],
   ["鶴","Журавлики на нитях",I.cr?`<b>${I.cr}</b>`:"пока ни одного — бумага ждёт"],["燭","Погасшие свечи",`<b>${I.cd}</b> из 100`],
   ["新","Открытий за неделю",`<b>${E.length}</b>`]];
  if(I.c&&I.c.gm)rows.push(["遊","Сыграно игр",`<b>${I.c.gm}</b>`]);if(I.c&&I.c.fi)rows.push(["魚","Поймано рыбы",`<b>${I.c.fi}</b>`]);
  // weather for the coming week
  const P=SB_SEA[I.se]||SB_SEA.autumn,days=["Пн","Вт","Ср","Чт","Пт","Сб","Вс"].map((d,i)=>[d,i===0&&I.wx?SB_WXK(I.wx[0]):P[0][Math.floor(r()*P[0].length)]]);
  const now=I.wx?`Сейчас ${SB_CITY[I.wx[2]]||"за воротами"} ${I.wx[1]>0?"+":""}${I.wx[1]}°, ${SB_WXI[SB_WXK(I.wx[0])][1]}. `:"";
  const ads=sbPick(r,SB_ADS,3),[strip,ct]=SB_CAT[I.act?SB_ACT[I.act[0]]||"calm":"calm"];
  return`<div class="sb-pp" style="--sbn:url(${sbNoise()})">
  <div class="sb-top"><div class="sb-mast"><small>瓦版 · каварабан · ${I.n===1?"первый выпуск":"еженедельно по понедельникам"}</small><b>Вестник ёкаев</b>
   <span>№ ${I.n} · ${I.n===1?"последние семь дней":"неделя"}: ${sbRange(I)} ${y} г.</span><span>Цена — один жёлудь. Читать при свете андона.</span></div><div class="sb-ttl">妖怪新聞</div></div>
  <div class="sb-vig">${hp}</div><h3 class="sb-hl">${ht}</h3><p class="sb-lead">${hl}</p>
  <h5 class="sb-h"><i>事件</i>Происшествия</h5>${nw.map(([p,l])=>`<div class="sb-nw"><span class="sb-pic">${p}</span><p>${l}</p></div>`).join("")}
  <h5 class="sb-h"><i>噂</i>Слухи и сплетни</h5>${gos.map(([w,t])=>`<p class="sb-gs"><b>${w}</b> ${t}</p>`).join("")}
  <h5 class="sb-h"><i>番付</i>Рейтинги недели</h5><div class="sb-rk">${rows.map(([j,a,v])=>`<div><i>${j}</i><span>${a}</span><em>${v}</em></div>`).join("")}</div>
  <h5 class="sb-h"><i>天気</i>Погода на неделю</h5><div class="sb-wx">${days.map(([d,k])=>`<div><small>${d}</small><img src="${sbWxIco(k)}" alt=""><small>${SB_WXI[k][1]}</small></div>`).join("")}</div><p class="sb-sm">${now}${P[1]}</p>
  <h5 class="sb-h"><i>広告</i>Объявления</h5><div class="sb-ads">${ads.map(([w,t])=>`<div><p>${t}</p><small>— ${w}</small></div>`).join("")}</div>
  <h5 class="sb-h"><i>猫</i>Кот недели</h5><div class="sb-cw"><span class="sb-cat" style="background-image:url(assets/${strip}@2x.webp)"></span><div><p><b>Муся</b>, хозяйка дома. ${ct}</p>
   <p class="sb-sm">Приметы: полосатая, усатая, глаза — два фонарика. Не сказала за неделю ни слова, но всё поняла.</p></div></div>
  <p class="sb-foot">Печатано на рисовой бумаге в типографии Бакэ-дзори · тираж семь экземпляров</p></div>
  <div class="row">${I.n>1?`<button class="btn" data-x="sb:open:${I.n-1}">◀ №${I.n-1}</button>`:""}<button class="btn" data-x="sb:arch">🗞 Подшивка</button>${I.n<SB.iss.length?`<button class="btn" data-x="sb:open:${I.n+1}">№${I.n+1} ▶</button>`:""}</div>`;}
function sbOpen(n){const I=SB.iss[n-1];if(!I)return;const W=S.ext.wx&&S.ext.wx.w;if(!I.wx&&I===sbLast()&&W)I.wx=[W.code,Math.round(W.temp),S.ext.wx.city];if(!I.cd&&I===sbLast()&&X.cd&&X.cd.out)I.cd=X.cd.out();sbFont();let h;try{h=sbHtml(I);}catch(e){console.error("news",e);h=`<p class="lead">Номер промок под дождём — буквы расплылись.</p>`;}
  openPanel("Вестник ёкаев",h,"sb"+n);$("xpBody").scrollTop=0;
  if(!I.r){I.r=1;disc("news",I.k);const N=SB.iss.filter(q=>q.r).length;award("sb_1");if(N>=4)award("sb_4");if(N>=10)award("sb_10");save();hubDot();tabDots();
    S.needs.joy=clamp(S.needs.joy+3,0,100);chime([784,988]);}}
function sbArch(){sbFont();const L=SB.iss.slice().reverse().map(I=>{let t="";try{const E=sbEv(I.a,I.b),top=E.slice().sort((p,q)=>sbWt(q)-sbWt(p)||q.t-p.t)[0];t=top?sbHead(top,I.cr)[0]:"Тихая неделя: ёкаи отдыхают";}catch(e){}
    return`<button class="sb-ar ${I.r?"":"new"}" data-x="sb:open:${I.n}"><i>№${I.n}</i><span><b>${t}</b><small>${sbRange(I)} ${new Date(I.b).getFullYear()} г.${I.r?"":" · не прочитан"}</small></span></button>`;}).join("");
  openPanel("Подшивка «Вестника»",`<p class="lead">Все номера «Вестника ёкаев». Новый выходит каждый понедельник утром и ждёт у почтового ящика у ворот.</p>${L||`<p class="lead">Номеров пока нет.</p>`}`,"sbA");}
// ── paper texture + woodcut vignettes, painted once on canvas ──
let sbNz=null;const sbCuts={};
function sbNoise(){if(sbNz)return sbNz;const c=document.createElement("canvas");c.width=c.height=160;const g=c.getContext("2d"),r=sbRnd(7);
  for(let i=0;i<1400;i++){const v=r();g.fillStyle=v<.7?`rgba(110,74,32,${.05+r()*.09})`:`rgba(255,248,226,${.1+r()*.15})`;g.fillRect(r()*160,r()*160,1+r()*1.6,1+r()*1.6);}
  g.lineWidth=.7;for(let i=0;i<40;i++){g.strokeStyle=`rgba(120,86,40,${.05+r()*.08})`;const x=r()*160,y=r()*160,a=r()*6.3,l=6+r()*16;g.beginPath();g.moveTo(x,y);g.quadraticCurveTo(x+Math.cos(a+.5)*l*.6,y+Math.sin(a+.5)*l*.6,x+Math.cos(a)*l,y+Math.sin(a)*l);g.stroke();}
  return sbNz=c.toDataURL();}
function sbCut(m){if(sbCuts[m])return sbCuts[m];const W=300,H=170,c=document.createElement("canvas");c.width=W;c.height=H;const g=c.getContext("2d"),r=sbRnd(sbHash(m)),INK="#2a1d14",RED="#a3301f",PAP="#eadcb9";
  g.lineCap="round";g.lineJoin="round";
  // waves (seigaiha) along the bottom
  g.strokeStyle=INK;g.lineWidth=2;for(let row=0;row<2;row++)for(let x=-20+row*18;x<W+20;x+=36){for(const rr of [17,11,5]){g.beginPath();g.arc(x,H+4-row*12,rr,Math.PI,0);g.stroke();}}
  const moon=(x,y,R)=>{g.fillStyle=PAP;g.beginPath();g.arc(x,y,R,0,7);g.fill();g.lineWidth=2.5;g.stroke();g.lineWidth=1.2;for(let i=-R+6;i<R;i+=7){const h=Math.sqrt(R*R-i*i)*.5;g.beginPath();g.moveTo(x+i,y+h*.2);g.lineTo(x+i+3,y+h);g.stroke();}};
  const cloud=(x,y,s)=>{g.lineWidth=2;g.fillStyle=PAP;g.beginPath();g.moveTo(x-30*s,y);for(const [dx,rr] of [[-18,9],[-4,13],[12,10],[26,7]])g.arc(x+dx*s,y-2*s,rr*s,Math.PI,0);g.closePath();g.fill();g.stroke();};
  if(m==="house"){moon(240,40,22);g.fillStyle=INK;g.beginPath();g.moveTo(40,92);g.quadraticCurveTo(95,82,150,40);g.quadraticCurveTo(205,82,262,92);g.lineTo(240,100);g.lineTo(62,100);g.closePath();g.fill();
    g.fillStyle=PAP;g.fillRect(72,100,158,46);g.strokeStyle=INK;g.lineWidth=2.4;g.strokeRect(72,100,158,46);g.lineWidth=1.2;for(let x=92;x<230;x+=20){g.beginPath();g.moveTo(x,100);g.lineTo(x,146);g.stroke();}
    for(const yy of [115,131]){g.beginPath();g.moveTo(72,yy);g.lineTo(230,yy);g.stroke();}g.fillStyle="rgba(214,150,60,.55)";g.fillRect(133,101,38,44);}
  else if(m==="lantern"){g.strokeStyle=INK;g.lineWidth=1.6;g.beginPath();g.moveTo(0,26);g.quadraticCurveTo(150,58,300,26);g.stroke();
    for(let i=0;i<5;i++){const x=34+i*58,y=26+Math.sin(i/4*Math.PI)*30+4;g.beginPath();g.moveTo(x,y-10);g.lineTo(x,y);g.stroke();g.fillStyle=i%2?RED:"#c9642c";g.beginPath();g.ellipse(x,y+22,15,21,0,0,7);g.fill();
      g.lineWidth=1.3;g.stroke();for(const k of [-12,-4,4,12]){g.beginPath();g.ellipse(x,y+22+k,Math.sqrt(1-(k/21)**2)*15,2.2,0,0,Math.PI);g.stroke();}g.fillStyle=INK;g.fillRect(x-7,y,14,3);g.fillRect(x-7,y+41,14,3);g.lineWidth=1.6;}
    cloud(150,120,1.1);}
  else if(m==="crane"){moon(62,46,24);cloud(236,118,.8);g.strokeStyle=INK;g.lineWidth=2.4;const P=(pts,f)=>{g.fillStyle=f;g.beginPath();g.moveTo(pts[0],pts[1]);for(let i=2;i<pts.length;i+=2)g.lineTo(pts[i],pts[i+1]);g.closePath();g.fill();g.stroke();};
    P([150,24,128,100,170,100],"#d8c8a2");P([112,108,124,100,92,52,82,58,88,64],PAP);P([176,100,188,108,232,56],PAP);P([108,110,150,92,194,110,150,126],PAP);P([150,40,140,100,170,100],"#c9b68c");
    g.fillStyle=RED;g.beginPath();g.arc(150,108,4,0,7);g.fill();}
  else if(m==="scroll"){moon(236,44,22);g.fillStyle=PAP;g.strokeStyle=INK;g.lineWidth=2.4;g.fillRect(60,48,150,72);g.strokeRect(60,48,150,72);g.fillStyle=INK;g.fillRect(52,42,10,84);g.fillRect(208,42,10,84);
    g.lineWidth=2;for(let x=190;x>76;x-=16){const l=24+r()*30;g.beginPath();g.moveTo(x,58);g.lineTo(x,58+l);g.stroke();}}
  else if(m==="flower"){moon(70,46,22);g.strokeStyle=INK;g.lineWidth=4;g.beginPath();g.moveTo(300,30);g.quadraticCurveTo(200,40,150,96);g.moveTo(230,40);g.quadraticCurveTo(220,70,190,80);g.stroke();
    for(const [x,y] of [[160,88],[196,72],[226,52],[262,40],[186,96],[244,66]]){g.fillStyle="#d9a5a0";g.strokeStyle=INK;g.lineWidth=1.3;for(let k=0;k<5;k++){const a=k/5*6.283;g.beginPath();g.ellipse(x+Math.cos(a)*6,y+Math.sin(a)*6,5,3.6,a,0,7);g.fill();g.stroke();}g.fillStyle=RED;g.beginPath();g.arc(x,y,2,0,7);g.fill();}}
  else if(m==="wave"){moon(230,44,24);g.fillStyle=INK;g.beginPath();g.moveTo(0,150);g.quadraticCurveTo(40,70,120,62);g.quadraticCurveTo(150,62,160,84);g.quadraticCurveTo(130,74,118,96);g.quadraticCurveTo(110,130,170,150);g.closePath();g.fill();
    g.fillStyle=PAP;for(let i=0;i<7;i++){g.beginPath();g.arc(124+i*6,66+i*3.2,3,0,7);g.fill();}}
  else{moon(200,62,34);cloud(110,58,1.2);cloud(250,112,.9);g.fillStyle=INK;g.beginPath();g.moveTo(0,128);g.quadraticCurveTo(80,96,150,124);g.quadraticCurveTo(220,104,300,126);g.lineTo(300,150);g.lineTo(0,150);g.fill();}
  return sbCuts[m]=c.toDataURL();}
function sbWxIco(k){const m="wx_"+k;if(sbCuts[m])return sbCuts[m];const c=document.createElement("canvas");c.width=56;c.height=44;const g=c.getContext("2d"),INK="#2a1d14",PAP="#eadcb9";
  g.strokeStyle=INK;g.fillStyle=PAP;g.lineWidth=2;g.lineCap="round";g.lineJoin="round";
  const sun=(x,y,R)=>{for(let i=0;i<8;i++){const a=i/8*6.283;g.beginPath();g.moveTo(x+Math.cos(a)*(R+3),y+Math.sin(a)*(R+3));g.lineTo(x+Math.cos(a)*(R+7),y+Math.sin(a)*(R+7));g.stroke();}g.beginPath();g.arc(x,y,R,0,7);g.fill();g.stroke();};
  const cl=(x,y,s)=>{g.fillStyle=PAP;g.beginPath();g.moveTo(x-16*s,y+6*s);g.arc(x-9*s,y+1*s,6*s,Math.PI*.9,Math.PI*1.6);g.arc(x+1*s,y-3*s,8*s,Math.PI*1.1,Math.PI*1.95);g.arc(x+11*s,y+2*s,6*s,Math.PI*1.4,Math.PI*.4);g.lineTo(x-16*s,y+6*s);g.closePath();g.fill();g.stroke();};
  const ln=(x0,y0,x1,y1)=>{g.beginPath();g.moveTo(x0,y0);g.lineTo(x1,y1);g.stroke();};
  if(k==="clear")sun(28,22,9);else if(k==="cloud"){sun(36,16,6);cl(25,24,1.05);}
  else if(k==="rain"){cl(28,16,1);g.lineWidth=1.6;for(const x of [18,26,34,42])ln(x,27,x-4,38);}
  else if(k==="drizzle"){sun(38,14,5);cl(25,18,.95);g.lineWidth=1.5;for(const x of [20,29,38])ln(x,29,x-2,34);}
  else if(k==="snow"){cl(28,15,1);g.lineWidth=1.3;for(const [x,y] of [[18,32],[28,37],[38,31]])for(let i=0;i<3;i++){const a=i/3*Math.PI;ln(x-Math.cos(a)*3.5,y-Math.sin(a)*3.5,x+Math.cos(a)*3.5,y+Math.sin(a)*3.5);}}
  else if(k==="fog"){g.lineWidth=2.2;for(const y of [14,23,32]){g.beginPath();g.moveTo(8,y);for(let x=8;x<=48;x+=10)g.quadraticCurveTo(x+5,y-4,x+10,y);g.stroke();}}
  else{cl(28,15,1);g.strokeStyle="#a3301f";g.lineWidth=2.4;g.beginPath();g.moveTo(31,24);g.lineTo(24,32);g.lineTo(31,32);g.lineTo(25,41);g.stroke();}
  return sbCuts[m]=c.toDataURL();}
let sbFontOn=0;function sbFont(){if(sbFontOn)return;sbFontOn=1;
  document.head.insertAdjacentHTML("beforeend",`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Antique&display=swap&text=${encodeURIComponent("妖怪新聞瓦版事件噂番付天気広告猫門食鶴燭遊魚")}"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Kurale&display=swap">`);}
document.head.insertAdjacentHTML("beforeend",`<style>
#xpBody .sb-pp{position:relative;color:#2a1d14;background:var(--sbn),radial-gradient(ellipse at 14% 8%,rgba(150,96,36,.22),transparent 38%),radial-gradient(ellipse at 88% 72%,rgba(140,90,30,.18),transparent 34%),#e6d6b0;
 border-radius:3px;padding:16px 14px 14px;margin:4px 0 14px;box-shadow:inset 0 0 42px rgba(112,70,24,.55),inset 0 0 6px rgba(80,50,20,.6),0 8px 22px rgba(0,0,0,.55);font-family:Kurale,var(--display),serif}
#xpBody .sb-pp::before{content:"";position:absolute;inset:7px;border:2.5px solid rgba(42,29,20,.85);box-shadow:inset 0 0 0 3px rgba(230,214,176,.0),inset 0 0 0 4px rgba(42,29,20,.55);pointer-events:none}
#xpBody .sb-pp p{color:#2a1d14;font-size:14.5px;line-height:1.42;margin:0 0 6px}
#xpBody .sb-top{display:flex;gap:10px;align-items:stretch;border-bottom:3px double #2a1d14;padding:2px 2px 8px;margin-bottom:8px}
#xpBody .sb-mast{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
#xpBody .sb-mast small{font-size:11px;letter-spacing:.5px;color:#7a2a1c}#xpBody .sb-mast b{font-size:31px;line-height:1.05;font-weight:400;letter-spacing:.5px}
#xpBody .sb-mast span{font-size:12.5px;line-height:1.3;color:#4a3826}
#xpBody .sb-ttl{flex:none;writing-mode:vertical-rl;background:#a3301f;color:#f1e3c2;font-family:"Zen Antique",var(--jp),serif;font-size:27px;line-height:1;letter-spacing:5px;padding:9px 6px;border:2px solid #2a1d14;box-shadow:3px 3px 0 #2a1d14;margin:2px 4px 4px 0}
#xpBody .sb-vig{height:150px;display:flex;justify-content:center;align-items:flex-end;border:2px solid #2a1d14;overflow:hidden;margin:4px 2px 0;background:repeating-linear-gradient(-32deg,rgba(42,29,20,.16) 0 1.2px,transparent 1.2px 6px)}
#xpBody .sb-vig>*,#xpBody .sb-pic>*{filter:grayscale(1) sepia(.55) contrast(1.55) brightness(.92);mix-blend-mode:multiply}
#xpBody .sb-vig img{max-height:146px;max-width:100%}
#xpBody .sb-hl{font-family:Kurale,var(--display),serif;font-weight:400;font-size:25px;line-height:1.12;text-align:center;margin:10px 4px 6px;color:#1f150e}
#xpBody .sb-pp p.sb-lead{font-size:15px;text-indent:1.2em;margin:0 2px 4px}
#xpBody .sb-h{display:flex;align-items:center;gap:8px;font-family:Kurale,var(--display),serif;font-size:18px;font-weight:400;margin:14px 2px 7px;padding-top:7px;border-top:1.5px solid #2a1d14;color:#1f150e}
#xpBody .sb-h i{font-style:normal;font-family:"Zen Antique",var(--jp),serif;background:#2a1d14;color:#eadcb9;font-size:13px;padding:2px 5px;border-radius:2px}
#xpBody .sb-nw{display:flex;gap:9px;align-items:center;margin:0 2px 6px}#xpBody .sb-nw p{margin:0}
#xpBody .sb-pic{flex:none;width:46px;height:46px;display:flex;align-items:center;justify-content:center;border:1.5px solid rgba(42,29,20,.7);overflow:hidden}
#xpBody .sb-pic img{max-width:44px;max-height:44px}#xpBody .sb-emo{line-height:1}
#xpBody .sb-pp p.sb-gs{margin:0 2px 6px}#xpBody .sb-gs b{color:#7a2a1c;font-weight:600}
#xpBody .sb-rk>div{display:flex;align-items:baseline;gap:7px;margin:0 2px 5px;font-size:14.5px;border-bottom:1px dotted rgba(42,29,20,.45);padding-bottom:4px}
#xpBody .sb-rk i{font-style:normal;font-family:"Zen Antique",var(--jp),serif;color:#a3301f;font-size:15px}#xpBody .sb-rk span{flex:1}#xpBody .sb-rk em{font-style:normal;text-align:right;max-width:55%}
#xpBody .sb-wx{display:flex;justify-content:space-between;margin:0 2px 6px}#xpBody .sb-wx>div{flex:1;text-align:center;border:1px solid rgba(42,29,20,.6);margin:0 1.5px;padding:3px 0 2px}
#xpBody .sb-wx small{display:block;font-size:11px;line-height:1.1;white-space:nowrap;overflow:hidden}#xpBody .sb-wx img{display:block;width:100%;max-width:44px;margin:1px auto}#xpBody .sb-wx>div{min-width:0}
#xpBody .sb-pp p.sb-sm{font-size:13.5px;color:#3e2e1f}
#xpBody .sb-ads{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:0 2px}#xpBody .sb-ads>div{border:1.5px solid #2a1d14;padding:6px 7px 5px;background:rgba(255,246,222,.25)}
#xpBody .sb-ads>div:first-child{grid-column:1/-1}#xpBody .sb-ads p{font-size:13.5px;margin:0 0 3px}#xpBody .sb-ads small{font-size:12px;color:#7a2a1c}
#xpBody .sb-cw{display:flex;gap:10px;align-items:center;margin:0 2px}#xpBody .sb-cw p{margin:0 0 5px}
#xpBody .sb-cat{flex:none;width:96px;height:104px;background-size:800% 100%;background-position:0 0;background-repeat:no-repeat;border:2px solid #2a1d14;border-radius:50%;filter:grayscale(.8) sepia(.6) contrast(1.3);background-color:rgba(255,246,222,.3)}
#xpBody .sb-cat.sm{width:42px;height:45px;border:0;border-radius:0}
#xpBody .sb-pp p.sb-foot{text-align:center;font-size:11.5px;color:#5a4430;margin:12px 0 0;border-top:3px double #2a1d14;padding-top:6px}
#xpBody .sb-ar{display:flex;gap:10px;align-items:center;width:100%;text-align:left;background:#e6d6b0;color:#2a1d14;border:2px solid #2a1d14;border-radius:4px;padding:8px 10px;margin:0 0 8px;font:inherit;cursor:pointer;box-shadow:inset 0 0 18px rgba(112,70,24,.4)}
#xpBody .sb-ar i{font-style:normal;font-family:Kurale,var(--display),serif;font-size:20px;color:#a3301f;min-width:42px}#xpBody .sb-ar span{display:flex;flex-direction:column}
#xpBody .sb-ar b{font-family:Kurale,var(--display),serif;font-weight:400;font-size:16px;line-height:1.2}#xpBody .sb-ar small{font-size:12px;color:#5a4430}
#xpBody .sb-ar.new{border-color:#a3301f;box-shadow:inset 0 0 18px rgba(112,70,24,.4),0 0 0 2px rgba(163,48,31,.4)}
</style>`);
// ── the rolled newspaper at the foot of the post box (entrance) ──
let sbBox=null;
hook("draw",(t,front)=>{if(front)return;sbBox=null;if(S.room!=="entrance"||scene.on||!sbUnread())return;
  const ix=visX(585,60)+2,[x,y]=imgToStage(ix,1064,CAT_D),k=BGM.k,L=74*k,D=17*k,pul=.55+.45*Math.sin(t*2.4),night=dayTint()[1];
  ctx.save();ctx.globalCompositeOperation="lighter";const gr=ctx.createRadialGradient(x,y-D*.5,0,x,y-D*.5,70*k);gr.addColorStop(0,`rgba(255,214,150,${.32*pul})`);gr.addColorStop(1,"rgba(255,200,120,0)");
  ctx.fillStyle=gr;ctx.fillRect(x-70*k,y-D*.5-70*k,140*k,140*k);ctx.restore();
  ctx.save();ctx.fillStyle="rgba(0,0,0,.4)";ctx.beginPath();ctx.ellipse(x,y+1,L*.56,D*.3+1,0,0,Math.PI*2);ctx.fill();
  ctx.translate(x,y-D*.5);ctx.rotate(-.07);
  const body=()=>{ctx.beginPath();ctx.moveTo(-L/2,-D/2);ctx.lineTo(L/2-D*.2,-D/2);ctx.ellipse(L/2-D*.2,0,D*.26,D/2,0,-Math.PI/2,Math.PI/2);ctx.lineTo(-L/2,D/2);ctx.ellipse(-L/2,0,D*.26,D/2,0,Math.PI/2,Math.PI*1.5);ctx.closePath();};
  const g=ctx.createLinearGradient(0,-D/2,0,D/2);g.addColorStop(0,"#e8d9b4");g.addColorStop(.42,"#cfbb90");g.addColorStop(1,"#7a6644");ctx.fillStyle=g;body();ctx.fill();
  ctx.save();body();ctx.clip();ctx.fillStyle="#9d2c1d";ctx.fillRect(L*.1,-D/2,L*.11,D);ctx.strokeStyle="rgba(42,29,20,.45)";ctx.lineWidth=Math.max(.6,1.1*k);
  for(let i=0;i<6;i++){const xx=-L*.42+i*L*.075;ctx.beginPath();ctx.moveTo(xx,-D*.34);ctx.lineTo(xx,D*.28);ctx.stroke();}
  ctx.fillStyle="#7a2418";ctx.fillRect(-L*.1,-D/2,Math.max(1.5,3.2*k),D);ctx.restore();
  ctx.fillStyle="#efe3c4";ctx.beginPath();ctx.ellipse(L/2-D*.2,0,D*.26,D/2,0,0,Math.PI*2);ctx.fill();ctx.strokeStyle="rgba(96,70,42,.85)";ctx.lineWidth=Math.max(.7,1.1*k);
  ctx.beginPath();ctx.ellipse(L/2-D*.2,0,D*.15,D*.3,0,0,Math.PI*2);ctx.stroke();ctx.beginPath();ctx.ellipse(L/2-D*.2,0,D*.06,D*.12,0,0,Math.PI*2);ctx.stroke();
  if(night){ctx.fillStyle="rgba(12,16,24,.38)";body();ctx.fill();}ctx.restore();
  const pad=14*view.s;sbBox=[x-L*.6-pad,y-D-pad,L*1.2+pad*2,D+pad*2];});
hook("hit",(x,y)=>{const r=sbBox;if(S.room!=="entrance"||!r||scene.on)return false;if(x>r[0]&&x<r[0]+r[2]&&y>r[1]&&y<r[1]+r[3]){audioInit();sfx("pop");const u=sbUnread();if(u){if(!petAway())react("😺",1.4);sbOpen(u.n);}return true;}return false;});
// ── hub, dots, buttons ──
function sbStatus(){const u=sbUnread();if(u)return`Свежий номер №${u.n} — не прочитан`;const d=today();
  return d.getDay()===1&&hourNow()<6&&sbLast()&&sbLast().k<sbMonK()?"Свежий номер выйдет сегодня в 6 утра":"Следующий номер — в понедельник";}
hook("hub",()=>{const u=sbUnread(),L=sbLast();
  return`<div class="hubc"><h4>📰 Вестник ёкаев <i>妖怪新聞</i></h4><p>${sbStatus()}</p><p>Газета ёкаев о том, как прошла неделя в доме Муси: главная новость, слухи, рейтинги, погода и объявления. Выходит по понедельникам утром; свежий номер ждёт у почтового ящика у ворот.</p>
   <div class="row">${L?`<button class="btn ${u?"primary":""}" data-x="sb:open:${(u||L).n}">📰 ${u?`Читать №${u.n}`:"Последний номер"}</button>`:""}<button class="btn" data-x="sb:arch">🗞 Подшивка (${SB.iss.length})</button></div></div>`;});
hook("hubDot",()=>!!sbUnread());
hook("tabDot",r=>r==="entrance"&&!!sbUnread());
hook("away",()=>{const u=sbUnread();if(u)return{i:"📰",t:`У ворот ждёт свежий «Вестник ёкаев», №${u.n}`};});
hook("click",key=>{if(!key.startsWith("sb:"))return;const a=key.split(":");audioInit();
  if(a[1]==="open")sbOpen(+a[2]);else if(a[1]==="arch")sbArch();return true;});
hook("boot",()=>{sbTick();});
hook("sec",()=>{sbTick();if(SB.tq&&!overlaysOpen()&&!scene.on&&!$("toast").classList.contains("on")){SB.tq=0;save();toast("📰 Вышел свежий «Вестник ёкаев»");chime([659,880]);}});
X.sb={S:SB,pub:sbPublish,open:sbOpen,arch:sbArch,tick:sbTick,ev:sbEv,html:sbHtml,box:()=>sbBox,status:sbStatus,
  reset(){SB.iss=[];SB.w=null;SB.pw=null;SB.tq=0;},
  // test: tap the roll through the hit hook
  tap(){const r=sbBox;return r?hk("hit",r[0]+r[2]/2,r[1]+r[3]/2):false;}};
}
