{
// ───────────────────────── Рёкан для ёкаев: travelling yōkai ask to stay the night ─────────────────────────
// After 18:00 (hourNow) 1–2 known yōkai come to the gate; the lantern sign «宿» lights up, a dlg asks for a corner for the night
// (only when the player is at the gate). Hosting = a room (likes), a futon (3 kinds) and a dinner from the pantry. At night the
// guest sleeps in that room on the futon (dimmed, «z»). After 6:00 of the next day: a review 1–3 ★, a tip (pantry things, at the
// first 3★ a gift «Подарки постояльцев»), fame → ranks (stamps), the guest book. Tastes are shown after the first stay.
// State: S.ext.ryokan = {day, g:[{id,day,st:"ask"|"sleep"|"morn",room,fut,dish,side}], book:[{id,d,room,fut,dish,st,txt}], fame, met:{id:{n,best,g3}}}
const RY_A={fb_simple:[476,0,380,180],ff_simple:[0,292,380,180],fb_down:[382,292,380,180],ff_down:[764,292,380,180],fb_crane:[0,474,380,180],ff_crane:[382,474,380,180],sign:[0,0,130,290]};
const RY_C="Подарки постояльцев",RY_GIFTS=["ry_noren","ry_chochin","ry_yukata","ry_zen","ry_book","ry_hibachi"];
{const A={ry_noren:[764,474,210,180,"t"],ry_chochin:[354,0,120,200,"t"],ry_yukata:[132,0,220,230,"b"],ry_zen:[192,656,200,120,"b"],ry_book:[0,656,190,130,"b"],ry_hibachi:[976,474,160,170,"b"]},
  row=(id,n)=>({id,n,c:RY_C,w:A[id][2],h:A[id][3],a:A[id][4],p:0,at:["ry",A[id][0],A[id][1]],src:"🏮 рёкан",hint:"Подарок постояльца рёкана за ночлег на три звезды"});
 addItems([row("ry_noren","Норэн «宿»"),row("ry_chochin","Фонарь «御宿»"),row("ry_yukata","Юката постоялого двора"),row("ry_zen","Ужин на лаковом подносе"),
  row("ry_book","Книга постояльцев"),row("ry_hibachi","Хибати с чайником")],{ry:[1160,786]});}
const RY_RANK=[[0,"Ночлежка","宿","ry_r0"],[8,"Постоялый двор","旅","ry_r1"],[25,"Рёкан «Мусин дом»","館","ry_r2"],[50,"Знаменитый рёкан","名","ry_r3"],[90,"Рёкан, о котором шепчутся все ёкаи","噂","ry_r4"]];
STAMPS.push(["ry_r0","宿","Ночлежка","Прими первого постояльца-ёкая на ночь"],["ry_r1","旅","Постоялый двор","Набери 8 очков славы рёкана"],["ry_r2","館","Рёкан «Мусин дом»","Набери 25 очков славы рёкана"],
 ["ry_r3","名","Знаменитый рёкан","Набери 50 очков славы рёкана"],["ry_r4","噂","Рёкан, о котором шепчутся","Набери 90 очков славы рёкана"]);
const RY_FUT={simple:"простой футон",down:"пуховый футон",crane:"футон с журавлями"},RY_FUTN={simple:"Простой",down:"Пуховый",crane:"С журавлями"};
// guests: name, picture, standing height, bestiary key, rooms they like (best first), favourite futon, favourite food, tip, catchphrase, request, 3★ thanks
const RY_YK=[
 {id:"kappa",n:"Каппа",m:"m_kappa",h:330,k:"kappa",lk:["onsen","courtyard"],fut:"simple",ds:["v_kyuri","ds_asazuke","u_any","ds_onigiri"],tp:"v_kyuri",tl:"Кап-кап!",
  ask:"Кап-кап… Не найдётся ли угол на ночь? Мне бы поближе к воде — блюдце на макушке сохнет. Перин не надо, я речной.",
  r3:"Кап-кап! Тёплая вода, прохладный футон и хрустящие огурцы — будто дома, на дне реки. Кланяюсь до самой земли!"},
 {id:"kitsune",n:"Лиса-невеста",m:"m_kitsune",h:350,k:"kitsune",lk:["hokora","chashitsu","engawa"],fut:"crane",ds:["ds_inari","ds_tempura","ds_dango","ds_mochi"],tp:"ds_inari",tl:"Спасибо за кров, хозяюшка.",
  ask:"Свадебный поезд ушёл без меня, а до Инари ещё три перевала. Не найдётся ли угол на ночь? Поближе к богам — и постель понаряднее.",
  r3:"Я спала под журавлями, у самого порога богов, и во сне слышала бубенцы Инари. Такой ночлег не забывают даже лисы."},
 {id:"tanuki",n:"Тануки",m:"m_tanuki",h:340,k:"tanuki",lk:["kitchen","games"],fut:"down",ds:["ds_yakiimo","ds_dango","ds_takoyaki","v_kabocha","v_imo"],tp:"v_imo",tl:"Пом-пом!",
  ask:"Пом-пом! Странствую, ищу, где пахнет едой. Не найдётся ли угол на ночь? Где сытнее и мягче — там мне и спится.",
  r3:"Пом-пом-пом! Спал у самой плиты на пуховом облаке, живот полный — даже во сне превращался в чайник от счастья!"},
 {id:"nekomata",n:"Нэкомата",m:"m_nekomata",h:340,k:"nekomata",lk:["bedroom","engawa"],fut:"down",ds:["u_any","ds_yakizakana","ds_tamagoyaki","ds_unadon"],tp:"u_ayu",tl:"Мяу, спасибо, сестрёнка.",
  ask:"Мяу. Сестрёнка, пустишь старую кошку переночевать? Мне бы туда, где спят люди, — привычка двухсот лет. И чтобы мягко.",
  r3:"Мур-р… Спальня, пух и рыба — всё, как я люблю. Оба хвоста до сих пор мурлычут. Муся растёт настоящей хозяйкой."},
 {id:"akaname",n:"Аканамэ",m:"m_akaname",h:300,k:"akaname",lk:["onsen","kitchen"],fut:"simple",ds:["ds_miso","ds_dengaku","ds_edamame","ds_nimono"],tp:"v_edamame",tl:"Чтобы чисто-чисто!",
  ask:"Шлёп-шлёп… Не найдётся ли угол на ночь? Я люблю, где мокро и пахнет мылом. Перину не надо — сплю на простом, как в бане.",
  r3:"Чисто-чисто! Ночевал у самой купальни, к утру вылизал её до блеска, а суп был как в старой бане моего деда."},
 {id:"obake",n:"Тётин-обакэ",m:"m_obake",h:300,k:"obake",lk:["entrance","attic","engawa"],fut:"simple",ds:["ds_tempura","v_obaketake","ds_takoyaki","ds_ramen"],tp:"v_obaketake",tl:"Хи-хи, спасибо за ночлег.",
  ask:"Хи-хи… Я старый фонарь, меня гонят с порога на порог. Не найдётся ли угол на ночь? У ворот или под крышей — там, где светить привык.",
  r3:"Хи-хи-хи! Всю ночь светил у ворот, как в молодости, а тэмпура подлила масла — горю ярче прежнего!"},
 {id:"warashi",n:"Дзасики-вараси",m:"m_warashi",h:330,k:"warashi",lk:["games","bedroom","attic"],fut:"crane",ds:["ds_daifuku","ds_taiyaki","ds_mochi","ds_dango","v_ichigo"],tp:"v_ichigo",tl:"Хи-хи, спасибо!",
  ask:"Хи-хи! А можно я у вас переночую? Только там, где игрушки, — и чтобы одеяло было с картинками, с птицами!",
  r3:"Я спала среди игрушек под журавликами и ела сладкое. Знаешь, к какому дому приходит удача? К этому!"},
 {id:"yuki",n:"Юки-онна",m:"m_rg_yuki",h:420,k:"rg_yuki",lk:["kura","courtyard"],fut:"simple",ds:["ds_mochi","ds_daifuku","ds_edamame"],tp:"ds_mochi",tl:"Ш-ш-ш… спасибо за ночлег.",
  ask:"Ш-ш-ш… Метель позади, а до гор далеко. Не найдётся ли угол на ночь? Только похолоднее, в тепле я таю. И перину не надо.",
  r3:"В холодной куре, на тонком футоне, я спала, как в сугробе. На стенах остался иней — это мой подарок, не стирай его до вечера."},
 {id:"kodama",n:"Кодама",m:"m_rg_kodama",h:300,k:"rg_kodama",lk:["courtyard","hokora"],fut:"simple",ds:["v_shiitake","ds_nimono","ds_edamame"],tp:"v_shiitake",tl:"А-у… спасибо… спасибо…",
  ask:"А-у… а-у… Ветер унёс меня от моего дерева. Не найдётся ли угол на ночь? Чтобы сверху было небо, а рядом — что-то живое.",
  r3:"А-у! Спал под открытым небом среди деревьев, а грибы были как в моём лесу. Эхо до сих пор повторяет: «спасибо… спасибо…»"},
 {id:"amabie",n:"Амабиэ",m:"m_rg_amabie",h:340,k:"rg_amabie",lk:["onsen","courtyard"],fut:"crane",ds:["u_any","ds_yakizakana","ds_onigiri"],tp:"u_yamame",tl:"И пусть никто не хворает.",
  ask:"Я вышла из моря Хиго и иду предсказывать урожай. Не найдётся ли угол на ночь? Без воды мне тяжко, а журавли — к долгой жизни.",
  r3:"Вода, журавли и рыба — всё как надо. Предсказываю этому дому шесть добрых лет и ни одного больного котёнка."},
 {id:"usagi",n:"Цуки-но усаги",m:"m_rg_usagi",h:330,k:"rg_usagi",lk:["engawa","chashitsu"],fut:"down",ds:["ds_mochi","ds_dango","ds_daifuku"],tp:"ds_mochi",tl:"Пон-пон! Спасибо.",
  ask:"Пон-пон! Я спустился с луны и заблудился. Не найдётся ли угол на ночь? Чтобы луну было видно — и мягко, как на облаке.",
  r3:"Пон-пон! Всю ночь глядел на луну с мягкой перины, а моти — почти как мои. Скажу там, наверху: внизу есть дом, где ждут."},
 {id:"karakasa",n:"Каракаса-обакэ",m:"m_vs_karakasa",h:300,k:"vs_karakasa",lk:["engawa","entrance"],fut:"simple",ds:["ds_tempura","ds_inari","ds_ramen"],tp:"v_shiitake",tl:"Прыг-скок!",
  ask:"Прыг-скок! Сто лет простоял в углу, теперь путешествую. Не найдётся ли угол на ночь? Мне бы под навес, где слышно дождь.",
  r3:"Прыг-скок! Всю ночь слушал дождь с веранды, а тэмпура хрустела, как новая бумага. Снова чувствую себя молодым зонтом!"},
 {id:"kamaitachi",n:"Кама-итати",m:"m_vs_kamaitachi",h:320,k:"vs_kamaitachi",lk:["attic","engawa"],fut:"down",ds:["u_any","ds_yakizakana","ds_unadon"],tp:"u_iwana",tl:"Вжух — и готово.",
  ask:"Ш-ш-ших! Нас трое, мы устали лететь против ветра. Не найдётся ли угол на ночь? Повыше, где гуляет сквозняк, и помягче.",
  r3:"Вжух! Под самой крышей гулял ветер, а перина была такая, что все трое уснули разом. Рыбу, конечно, съели втроём."},
 {id:"bakezori",n:"Бакэ-дзори",m:"m_vs_bakezori",h:230,k:"vs_bakezori",lk:["entrance","wardrobe"],fut:"simple",ds:["ds_onigiri","ds_yakiimo","ds_edamame"],tp:"ds_onigiri",tl:"Карари-кори!",
  ask:"Карари-кори! Я сандалия-путешественница. Не найдётся ли угол на ночь? Мне бы у порога, рядом с обувью, — там спокойнее.",
  r3:"Карари-кори! Спал у самого порога, на простом футоне, а онигири — из настоящего риса, родного. Береги обувь — и она тебя не бросит!"},
 {id:"kozo",n:"Хитоцумэ-кодзо",m:"m_vs_kozo",h:300,k:"vs_kozo",lk:["games","attic"],fut:"down",ds:["ds_dango","ds_takoyaki","ds_tamagoyaki"],tp:"ds_dango",tl:"Спасибо, я всё записал.",
  ask:"Ой… Я записываю хорошие дома в книжечку. Не найдётся ли угол на ночь? Можно туда, где игрушки? И одеяло помягче.",
  r3:"Я записал ваш дом в книжечку первым! Игрушки, мягкая перина и данго — одним глазом я такого ещё не видел."},
 {id:"nuppeppo",n:"Нуппэппо",m:"m_vs_nuppeppo",h:260,k:"vs_nuppeppo",lk:["onsen","kura"],fut:"down",ds:["ds_nimono","ds_miso","ds_onigiri"],tp:"v_daikon",tl:"Шлёп-шлёп…",
  ask:"Шлёп-шлёп… Я брожу по заброшенным храмам. Не найдётся ли угол на ночь? Где тепло и сыро — и помягче, я весь из складочек.",
  r3:"Шлёп-шлёп! Тёплый пар и пуховое одеяло — я растёкся от счастья. А тыква была мягкая, как я сам."},
 {id:"yosuzume",n:"Ёсудзумэ",m:"m_vs_yosuzume",h:220,k:"vs_yosuzume",lk:["courtyard","engawa"],fut:"crane",ds:["v_edamame","ds_edamame","ds_onigiri"],tp:"v_edamame",tl:"Чи-чи-чи!",
  ask:"Чи-чи-чи! Нас, ночных воробьёв, застала темнота. Не найдётся ли угол на ночь? Под открытым небом — и чтобы на одеяле были птицы!",
  r3:"Чи-чи-чи! Спали во дворике под журавлями — будто в большой стае. Эдамамэ склевали до последнего бобика!"},
 {id:"moku",n:"Мокумокурэн",m:"m_vs_mokumokuren",h:320,k:"vs_mokumokuren",lk:["bedroom","attic"],fut:"crane",ds:["ds_tamagoyaki","ds_miso","ds_onigiri"],tp:"v_nasu",tl:"Все мои глаза благодарят.",
  ask:"Все мои глаза устали глядеть из дырявых сёдзи. Не найдётся ли угол на ночь? Где сёдзи целые — и одеяло, на которое приятно смотреть.",
  r3:"Целые сёдзи, журавли на одеяле — все мои глаза наконец закрылись разом. Впервые за сто лет."},
 {id:"tengu",n:"Тэнгу",m:"m_rm_tengu",h:380,k:"rm_tengu",lk:["hokora","attic"],fut:"simple",ds:["ds_onigiri","ds_ramen","v_shiitake"],tp:"v_shiitake",tl:"Хм. Благодарю.",
  ask:"Хм. Я с горы Курама, путь неблизкий. Не найдётся ли угол на ночь? Повыше от земли или у святыни. Перин не люблю — я ямабуси.",
  r3:"Хм! Святыня рядом, футон простой, как в горном храме, онигири — как у паломников. Достойный ночлег. Расскажу о нём на Кураме."},
 {id:"bunbuku",n:"Бунбуку-тягама",m:"m_rm_chagama",h:260,k:"rm_bunbuku",lk:["chashitsu","kitchen"],fut:"down",ds:["ds_dango","ds_yakiimo","ds_mochi"],tp:"ds_dango",tl:"Буль-буль!",
  ask:"Буль-буль… Я наполовину чайник, наполовину тануки. Не найдётся ли угол на ночь? Там, где заваривают чай, — и помягче, крышка ноет.",
  r3:"Буль-буль! Ночевал в чайной, как в родном храме, на пуховой перине. Даже крышка перестала дребезжать!"}];
const RYI={};for(const y of RY_YK)RYI[y.id]=y;
const RY_BASIC=["kappa","kitsune","tanuki","nekomata","akaname","obake"];
document.head.insertAdjacentHTML("beforeend",`<style>.ry-g{display:grid;grid-template-columns:repeat(auto-fill,minmax(98px,1fr));gap:6px;margin:4px 0 12px}
.ry-o{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;padding:6px 4px;min-height:62px;border-radius:12px;background:#0a0d0c;border:1px solid var(--line);color:inherit;font:inherit;cursor:pointer}
.ry-o.on{border-color:#e8b86a;background:#2a2014;box-shadow:0 0 0 1px #e8b86a inset}.ry-o.no{opacity:.38;pointer-events:none}
.ry-o b{font-family:var(--jp);font-size:17px;font-weight:400;color:var(--sakura)}.ry-o small{font-size:12px;line-height:1.2;text-align:center}.ry-o .ry-h{color:#f08a9a}
.ry-hd{display:flex;gap:12px;align-items:center;margin:0 0 8px}.ry-hd img{height:104px;width:84px;object-fit:contain;flex:none}.story-body .ry-hd p{margin:4px 0 0;font-size:14px;line-height:1.45;font-style:italic}
.story-body p.ry-tip{font-size:13px;color:#e8c8a0;margin:2px 0 8px}.ry-bar{display:inline-block;vertical-align:middle;width:110px;height:8px;border-radius:5px;background:#1a1612;border:1px solid var(--line);overflow:hidden;margin:0 4px}
.ry-bar i{display:block;height:100%;background:linear-gradient(90deg,#b8622a,#f2c878)}.ry-st{color:#f2c84a;letter-spacing:1px;white-space:nowrap}
.ry-bk{display:flex;gap:10px;padding:8px;border-radius:12px;background:#0a0d0c;border:1px solid var(--line);margin:0 0 8px}.ry-bk img{height:66px;width:56px;object-fit:contain;flex:none}
.story-body .ry-bk p{margin:2px 0;font-size:13px;line-height:1.4}.ry-bk small{color:var(--muted);font-size:11px}.ry-big{font-size:30px;color:#f2c84a;letter-spacing:4px;text-align:center;margin:4px 0}</style>`);

// ── state, time ──
const ryD=()=>{const R=S.ext.ryokan||(S.ext.ryokan={day:"",g:[],book:[],fame:0,met:{}});R.g=R.g||[];R.book=R.book||[];R.met=R.met||{};return R;};
const ryM=id=>ryD().met[id]||(ryD().met[id]={n:0,best:0,g3:0});
const ryRN=id=>(ROOMS.find(r=>r.id===id)||{ru:id}).ru;
function ryNext(day){const d=new Date(day+"T12:00:00");d.setDate(d.getDate()+1);return dayKey(d);}
function ryMorning(day){const n=ryNext(day),k=dayKey();return k>n||k===n&&hourNow()>=6;}
function ryRng(s){let h=2166136261;for(const c of s)h=Math.imul(h^c.charCodeAt(0),16777619)>>>0;return()=>{h=Math.imul(h^h>>>15,2246822507)+0x6D2B79F5>>>0;return(h>>>8)/16777216;};}
function ryKnown(){const D=(S.ext.disc||{}).rareguest||{},V=(S.ext.vis||{}).m||{};
  return RY_YK.filter(y=>ST.seen.includes(y.k)||(S.friends[y.id]||{}).n>0||D[y.id]||(V[y.id]||{}).met).map(y=>y.id);}
const ryLoves=(Y,f)=>!!f&&(Y.ds.includes(f)||Y.ds.includes("u_any")&&EATFISH.includes(f));
const ryFood=f=>f==="u_any"?"любая рыба":FOOD[f]?FOOD[f].n.toLowerCase():f;
function ryRank(f=ryD().fame){let i=0;for(let k=0;k<RY_RANK.length;k++)if(f>=RY_RANK[k][0])i=k;return i;}
const ryAsks=()=>ryD().g.filter(g=>g.st==="ask"),ryMorn=()=>ryD().g.filter(g=>g.st==="morn");
const ryOpenRooms=()=>ROOMS.filter(r=>r.id!=="matsuri"&&!hk("tabLock",r.id));
const ryBusy=room=>{const V=((S.ext.vis||{}).r||{})[room];return ryD().g.some(g=>g.st==="sleep"&&g.room===room)||!!V&&V.st==="here";};

// new requests after 18:00, sleepers wake after 6:00 of the next day, unanswered travellers leave
function ryStep(live=true){
  const R=ryD(),d=dayKey();let ch=false,woke=null;
  for(const g of R.g)if(g.st!=="morn"&&ryMorning(g.day)){if(g.st==="sleep"){g.st="morn";woke=woke||g;}else g.st="gone";ch=true;}
  if(ch)R.g=R.g.filter(g=>g.st!=="gone");
  if(hourNow()>=18&&R.day!==d){R.day=d;ch=true;
    const r=ryRng(d+"ryokan"),busy=R.g.map(g=>g.id),last=R.book.slice(-2).map(b=>b.id);let pool=ryKnown();
    if(pool.length<3)for(const id of RY_BASIC)if(!pool.includes(id))pool.push(id);
    pool=pool.filter(id=>!busy.includes(id));const fresh=pool.filter(id=>!last.includes(id));if(fresh.length)pool=fresh;
    const n=R.book.length&&pool.length>1&&r()<.4?2:1;
    for(let i=0;i<n&&pool.length;i++){const id=pool.splice(Math.floor(r()*pool.length),1)[0];R.g.push({id,day:d,st:"ask"});}
    if(live){ryArr=now();if(S.room==="entrance")setTimeout(()=>ryAskDlg(0,1),2600);else toast("🏮 У ворот путник просит ночлега");}}
  if(ch){save();if(live){hubDot();tabDots();}}
  return woke;}
let ryArr=0,ryRes=null,ryPick=null;
// catch up while the game was closed (before the «away» postcard is asked for)
let ryAway=null;{const w=ryStep(false);if(w)ryAway={i:"🏮",t:`Утро в рёкане: ${RYI[w.id].n} оставляет отзыв`};}

// ── pictures: the atlas, tinted copies (room light), dimmed sleepers ──
let RYIM=null,ryLd=0;const RYC={};
function ryCv(key,tint){if(!RYIM){if(!ryLd){ryLd=1;atlasImg("ry",im=>{RYIM=im;});}return null;}const ck=key+"|"+tint;if(RYC[ck])return RYC[ck];
  const r=RY_A[key],c=document.createElement("canvas");c.width=r[2];c.height=r[3];const g=c.getContext("2d");g.drawImage(RYIM,r[0],r[1],r[2],r[3],0,0,r[2],r[3]);
  if(tint){g.globalCompositeOperation="source-atop";g.fillStyle=tint;g.fillRect(0,0,r[2],r[3]);}return RYC[ck]=c;}
function ryMonCv(id,tint){const im=MIMG[id],m=MON[id];if(!im||!m)return null;const ck="m|"+id+"|"+tint;if(RYC[ck])return RYC[ck];
  const c=document.createElement("canvas");c.width=m[0];c.height=m[1];const g=c.getContext("2d");g.drawImage(im,0,0,m[0],m[1]);
  if(tint){g.globalCompositeOperation="source-atop";g.fillStyle=tint;g.fillRect(0,0,m[0],m[1]);}return RYC[ck]=c;}
function rySpr(key,ix,iy,wImg,tint,al=1){const c=ryCv(key,tint);if(!c)return null;const r=RY_A[key],w=wImg*BGM.k,h=w*r[3]/r[2],[x,y]=imgToStage(ix,iy,CAT_D);
  ctx.save();ctx.globalAlpha=al;ctx.drawImage(c,x-w/2,y-h,w,h);ctx.restore();return[x-w/2,y-h,w,h];}

// ── the gate: the lantern sign «宿» and the travellers ──
const RY_SIGN=[1300,1012,112];let ryHits=[];
function ryGate(t){
  const R=ryD(),h=hourNow(),asks=ryAsks();if(!(h>=17||h<7||R.g.length))return;
  const sx=visX(RY_SIGN[0],80),lit=asks.length>0,[gx,gy]=imgToStage(sx,RY_SIGN[1]-140,CAT_D),k=BGM.k;
  if(lit){const p=.82+.18*Math.sin(t*2.1),gr=ctx.createRadialGradient(gx,gy,0,gx,gy,230*k);gr.addColorStop(0,`rgba(255,196,110,${.42*p})`);gr.addColorStop(1,"rgba(255,196,110,0)");
    ctx.save();ctx.globalCompositeOperation="lighter";ctx.fillStyle=gr;ctx.fillRect(gx-230*k,gy-230*k,460*k,460*k);ctx.restore();}
  const b=rySpr("sign",sx,RY_SIGN[1],RY_SIGN[2],lit?"rgba(40,20,0,.08)":"rgba(6,8,14,.6)");if(b)ryHits.push(["sign",b]);
  asks.forEach((g,i)=>{const Y=RYI[g.id],a=clamp((t-ryArr)/1.6,0,1),x=i?sx-290:sx-150,y=i?RY_SIGN[1]-105:RY_SIGN[1]+30,hh=Y.h*(i?.55:.8);   // the second one waits up the path
    drawMon(Y.m,x,y+Math.sin(t*1.9+i)*3,hh,CAT_D,ryArr?a:1);const [px_,py_]=imgToStage(x,y,CAT_D),H_=hh*k,W_=H_*MON[Y.m][0]/MON[Y.m][1];ryHits.push(["ask:"+i,[px_-W_/2,py_-H_,W_,H_]]);});}

// ── a guest asleep in a room: futon back → dimmed guest (breathing) → comforter → «z» ──
function ryBedPos(g){const mid=(view.W/2-BGM.dx)/BGM.k,V=((S.ext.vis||{}).r||{})[g.room];let side=g.side||1;
  if(V&&X.vs&&X.vs.pos){const p=X.vs.pos(g.room);if(p)side=p.x<mid?1:-1;}
  return[visX(mid+side*250,225),catLineY()-26];}
function ryBed(g,t){
  const Y=RYI[g.id],m=MON[Y.m];if(!m)return;const [ix,iy]=ryBedPos(g),tint=TINT[S.room]||"rgba(20,22,20,.2)",sl=g.st==="sleep",FW=440,fs=FW/380,k=BGM.k;
  const fb=rySpr("fb_"+g.fut,ix,iy,FW,tint);if(!fb)return;
  const h=Y.h*.78*k*(1+(sl?.014*Math.sin(t*1.3):0)),w=h*m[0]/m[1],gx=fb[0]+fb[2]/2,gy=fb[1]+150*fs*k,c=ryMonCv(Y.m,sl?"rgba(10,14,36,.52)":tint);
  if(c)ctx.drawImage(c,gx-w/2,gy-h,w,h);
  rySpr("ff_"+g.fut,ix,iy,FW,tint);ryHits.push(["bed:"+ryD().g.indexOf(g),[Math.min(fb[0],gx-w/2),gy-h,Math.max(fb[2],w),fb[1]+fb[3]-(gy-h)]]);
  ctx.save();ctx.textAlign="center";ctx.textBaseline="middle";
  if(sl)for(let i=0;i<3;i++){const u=(t*.32+i/3)%1;ctx.globalAlpha=Math.sin(u*Math.PI)*.85;ctx.fillStyle="#dfe4ff";ctx.font=`italic 600 ${Math.round((11+u*12)*view.s)}px Georgia,serif`;
    ctx.fillText("z",gx+w*.22+u*34*k,gy-h*.82-u*90*k);}
  else{ctx.globalAlpha=.7+.3*Math.sin(t*3);drawEmoji(ctx,"✉️",gx+w*.36,gy-h*.9+Math.sin(t*2.4)*3*k,18*view.s);}
  ctx.restore();}

hook("draw",(t,front)=>{if(front||scene.on)return;ryHits=[];const R=ryD();
  if(S.room==="entrance")ryGate(t);
  for(const g of R.g)if((g.st==="sleep"||g.st==="morn")&&g.room===S.room)ryBed(g,t);});
hook("hit",(x,y)=>{if(scene.on)return false;
  for(const [k,b] of ryHits){if(x<b[0]||x>b[0]+b[2]||y<b[1]||y>b[1]+b[3])continue;const [a,i]=k.split(":");audioInit();
    if(a==="sign"){if(ryAsks().length)ryAskDlg();else toast(hourNow()>=18?"🏮 Сегодня путников больше не будет":"🏮 Путники приходят после шести вечера");return true;}
    if(a==="ask"){ryAskDlg(+i);return true;}
    if(a==="bed"){const g=ryD().g[+i];if(!g)return false;if(g.st==="morn")ryReview(+i);else{toast(`Тс-с… ${RYI[g.id].n} спит 💤`);tone(330,.4,"sine",.02);}return true;}}
  return false;});

// ── the request at the gate (the only dialog the add-on opens by itself) ──
function ryAskDlg(i=0,auto=0){
  const g=auto?ryAsks().find(q=>!q.dl):ryAsks()[i];if(!g||S.room!=="entrance"||scene.on||overlaysOpen()||!$("xdlg").hidden||!$("gdlg").hidden)return;const Y=RYI[g.id],M=ryM(g.id);g.dl=1;
  if(!petAway())react("😺",1.4);chime([660,880]);
  dlg({head:`${Y.n} · ${M.n?"снова в пути":"путник у ворот"}`,text:Y.ask,img:`<img src="assets/mon/${Y.m}.webp" alt="" style="height:64px">`,ok:"Принять",no:"Позже",
    onOk:()=>ryHost(ryD().g.indexOf(g))});}
hook("room",id=>{if(id==="entrance"&&ryAsks().some(g=>!g.dl))setTimeout(()=>ryAskDlg(0,1),1200);});

// ── hosting panel: room, futon, dinner ──
function ryHost(gi){
  const R=ryD(),g=R.g[gi];if(!g||g.st!=="ask"){closePanel();return;}const Y=RYI[g.id],M=ryM(g.id),kn=M.n>0;
  if(!ryPick||ryPick.gi!==gi)ryPick={gi,room:null,fut:null,dish:null};const P=ryPick;
  const rooms=ryOpenRooms().map(r=>{const b=ryBusy(r.id),hv=kn?(Y.lk[0]===r.id?"♥♥":Y.lk.includes(r.id)?"♥":""):"";
    return`<button class="ry-o ${P.room===r.id?"on":""} ${b?"no":""}" data-x="ry:room:${r.id}"><b>${r.jp}</b><small>${r.ru}${hv?` <span class="ry-h">${hv}</span>`:""}${b?"<br>занято":""}</small></button>`;}).join("");
  const futs=Object.keys(RY_FUT).map(f=>{const r=RY_A["ff_"+f];return`<button class="ry-o ${P.fut===f?"on":""}" data-x="ry:fut:${f}">${itemThumb({at:["ry",r[0],r[1]],w:r[2],h:r[3]},92,44)}<small>${RY_FUTN[f]}${kn&&Y.fut===f?' <span class="ry-h">♥</span>':""}</small></button>`;}).join("");
  const eats=[...pantryEats(),...Object.keys(S.pantry).filter(f=>S.pantry[f]>0&&FOOD[f]&&FOOD[f].k==="veg")];
  const dishes=`<button class="ry-o ${P.dish==="none"?"on":""}" data-x="ry:dish:none"><b>—</b><small>Без ужина</small></button>`+eats.map(f=>`<button class="ry-o ${P.dish===f?"on":""}" data-x="ry:dish:${f}">${fThumb(f,60,38)}<small>${FOOD[f].n}${kn&&ryLoves(Y,f)?' <span class="ry-h">♥</span>':""}<br>×${S.pantry[f]}</small></button>`).join("");
  const hint=kn?`<p class="ry-tip">♥ ${Y.n} любит: ${Y.lk.map(r=>"«"+ryRN(r)+"»").join(" и ")}, ${RY_FUT[Y.fut]}, на ужин — ${Y.ds.slice(0,3).map(ryFood).join(", ")}.</p>`
    :`<p class="ry-tip">Вкусы гостя узнаешь после первой ночи. А пока угадай по его словам.</p>`;
  openPanel("Ночлег для гостя",`<div class="ry-hd"><img src="assets/mon/${Y.m}.webp" alt=""><div><b>${Y.n}</b>${M.n?` <small>· ночей у нас: ${M.n}</small>`:""}<p>«${Y.ask}»</p></div></div>${hint}
   <div class="bh">Комната</div><div class="ry-g">${rooms}</div><div class="bh">Футон</div><div class="ry-g">${futs}</div>
   <div class="bh">Ужин из кладовой</div><div class="ry-g">${dishes}</div>${eats.length?"":`<p class="ry-tip">В кладовой пусто: приготовь что-нибудь на кухне или собери урожай.</p>`}
   <div class="row"><button class="btn primary" data-x="ry:ok">Проводить в комнату</button><button class="btn" data-x="ry:later">Позже</button></div>`,"ry_host");}
function ryOk(){
  const R=ryD(),P=ryPick;if(!P)return;const g=R.g[P.gi];if(!g||g.st!=="ask"){closePanel();return;}
  if(!P.room||!P.fut){toast(!P.room?"Выбери комнату для гостя":"Выбери футон");return;}
  if(ryBusy(P.room)){toast("Эта комната уже занята");return;}
  const dish=P.dish&&P.dish!=="none"&&have(P.dish)>0?take(P.dish):null,Y=RYI[g.id];
  Object.assign(g,{st:"sleep",room:P.room,fut:P.fut,dish,side:R.g.filter(q=>q.st==="sleep").length%2?-1:1,at:Date.now()});ryPick=null;
  disc("ryokan",g.id);sfx("chime");if(!petAway())react("😸",1.6);save();hubDot();tabDots();
  toast(`💤 ${Y.n} — «${ryRN(g.room)}»`);
  const nx=R.g.findIndex(q=>q.st==="ask");if(nx>=0)ryHost(nx);else closePanel();}

// ── morning: stars, review in the guest's voice, tip, fame ──
function ryScore(g){const Y=RYI[g.id],ri=Y.lk.indexOf(g.room);return(ri===0?2:ri>0?1:0)+(g.fut===Y.fut?1:0)+(g.dish?ryLoves(Y,g.dish)?2:1:0);}
function ryText(g,st){const Y=RYI[g.id],ri=Y.lk.indexOf(g.room);if(st===3)return Y.r3;
  return[Y.tl,ri===0?"Комната — лучше не придумать.":ri>0?"Комната хорошая.":`В комнате «${ryRN(g.room)}» мне было не по себе.`,
    g.fut===Y.fut?"Футон — в самый раз.":"Футон бы другой…",!g.dish?"Жаль, без ужина.":ryLoves(Y,g.dish)?"А ужин — моё любимое!":"Ужин сытный, спасибо."].join(" ");}
function ryReview(gi){
  const R=ryD(),g=R.g[gi];if(!g||g.st!=="morn")return;const Y=RYI[g.id],M=ryM(g.id),first=!M.n,sc=ryScore(g),st=sc>=4?3:sc>=2?2:1,txt=ryText(g,st);
  const tips=[],n=st;for(let i=0;i<n;i++){const f=i===0?Y.tp:pick(["v_shiitake","v_imo","v_kabocha","v_ichigo","v_edamame","v_daikon","u_ayu","ds_dango","ds_onigiri"]);if(FOOD[f]){give(f);tips.push(f);}}
  let gift=null;if(st===3&&!M.g3){M.g3=1;gift=RY_GIFTS.find(id=>!S.owned.has(id))||null;if(gift){S.owned.add(gift);loadItem(gift);}}
  const before=ryRank(),add=[0,1,3,5][st]+(first?2:0);R.fame+=add;M.n++;M.best=Math.max(M.best,st);
  R.book.push({id:g.id,d:g.day,room:g.room,fut:g.fut,dish:g.dish,st,txt});if(R.book.length>80)R.book.splice(0,R.book.length-80);
  R.g.splice(gi,1);S.needs.joy=clamp(S.needs.joy+6*st,0,100);
  for(const r of RY_RANK)if(R.fame>=r[0])award(r[3]);const up=ryRank()>before;
  chime(st===3?[784,988,1318,1568]:[784,988]);if(!petAway()){react(st===3?"😻":"😺",2);if(st===3)burst(10);}save();hubDot();tabDots();
  ryRes={Y,st,txt,tips,gift,add,up};
  openPanel("Утро в рёкане",`<div class="ry-hd"><img src="assets/mon/${Y.m}.webp" alt=""><div><b>${Y.n}</b> <small>· «${ryRN(g.room)}», ${RY_FUT[g.fut]}${g.dish?", "+FOOD[g.dish].n.toLowerCase():""}</small><p>«${txt}»</p></div></div>
   <div class="ry-big">${"★".repeat(st)}${"☆".repeat(3-st)}</div>
   <p class="lead">${tips.length?"На подушке оставлено: ":""}${tips.map(f=>`${fThumb(f,40,28)} ${FOOD[f].n}`).join(", ")}${tips.length?".":""} Слава рёкана +${add}.</p>
   ${gift?`<div class="ry-hd">${itemThumb(IT[gift],90,90)}<p>И ещё подарок: «${IT[gift].n}» — ищи в 🧺 Вещи → ${RY_C}.</p></div>`:""}
   ${up?`<p class="lead">🏮 Новое звание: <b>${RY_RANK[ryRank()][1]}</b>!</p>`:""}
   ${first?`<p class="ry-tip">Теперь ты знаешь, что любит ${Y.n}: это записано в книге постояльцев.</p>`:""}
   <div class="row"><button class="btn primary" data-x="${ryMorn().length?"ry:rev:"+R.g.indexOf(ryMorn()[0]):"ry:close"}">${ryMorn().length?"Следующий гость →":"До встречи!"}</button><button class="btn" data-x="ry:book">📖 Книга постояльцев</button></div>`,"ry_rev");$("xpBody").scrollTop=0;}

// ── the guest book ──
function ryBook(){
  const R=ryD(),rk=ryRank(),stars=s=>`<span class="ry-st">${"★".repeat(s)}${"☆".repeat(3-s)}</span>`;
  const rows=R.book.slice().reverse().map(b=>{const Y=RYI[b.id];if(!Y)return"";const [yy,mm,dd]=b.d.split("-");
    return`<div class="ry-bk"><img src="assets/mon/${Y.m}.webp" alt=""><div><b>${Y.n}</b> ${stars(b.st)} <small>${+dd}.${mm}.${yy} · «${ryRN(b.room)}», ${RY_FUT[b.fut]||""}${b.dish&&FOOD[b.dish]?", "+FOOD[b.dish].n.toLowerCase():""}</small><p>«${b.txt}»</p></div></div>`;}).join("");
  const tastes=RY_YK.filter(y=>(R.met[y.id]||{}).n>0).map(Y=>`<p class="ry-tip">♥ <b>${Y.n}</b>: ${Y.lk.map(r=>"«"+ryRN(r)+"»").join(", ")} · ${RY_FUT[Y.fut]} · ${Y.ds.slice(0,3).map(ryFood).join(", ")}</p>`).join("");
  openPanel("Книга постояльцев 宿帳",`<p class="lead">Звание: <b>${RY_RANK[rk][1]}</b> · слава ${R.fame}. Ночевали у нас: ${Object.values(R.met).filter(m=>m.n).length} из ${RY_YK.length} ёкаев.</p>
   ${rows||`<p class="lead">Книга пока пуста. Путники просятся на ночлег по вечерам, после шести.</p>`}${tastes?`<div class="bh">Что любят гости</div>${tastes}`:""}`,"ry_book");$("xpBody").scrollTop=0;}

hook("click",(key)=>{
  if(!key.startsWith("ry:"))return false;const [,a,v]=key.split(":");
  if(a==="room"||a==="fut"||a==="dish"){if(ryPick){ryPick[a]=v;sfx("pop");ryHost(ryPick.gi);}return true;}
  if(a==="ok")ryOk();else if(a==="later"||a==="close")closePanel();else if(a==="host")ryHost(+v);else if(a==="rev")ryReview(+v);else if(a==="book")ryBook();
  else if(a==="go"){closePanel();goRoom(v);}
  return true;});

// ── hooks: time, dots, hub, postcard ──
hook("sec",()=>{const w=ryStep();if(w&&S.room===w.room&&!petAway())react("😺",1.2);});
hook("hubDot",()=>ryAsks().length>0||ryMorn().length>0);
hook("tabDot",r=>r==="entrance"&&ryAsks().length>0);
hook("away",()=>ryAway);
hook("hub",()=>{
  const R=ryD(),rk=ryRank(),nx=RY_RANK[rk+1],lo=RY_RANK[rk][0],pct=nx?Math.round((R.fame-lo)/(nx[0]-lo)*100):100,h=hourNow();
  const lines=R.g.map((g,i)=>{const Y=RYI[g.id];
    if(g.st==="ask")return`<p>🏮 У ворот ждёт путник: <b>${Y.n}</b>. «Не найдётся ли угол на ночь?»</p><div class="row"><button class="btn primary" data-x="ry:host:${i}">Принять на ночлег</button></div>`;
    if(g.st==="sleep")return`<p>💤 <b>${Y.n}</b> спит: «${ryRN(g.room)}», ${RY_FUT[g.fut]}${g.dish?", на ужин — "+FOOD[g.dish].n.toLowerCase():""}. Отзыв — утром, после шести.</p>`;
    return`<p>☀️ Утро. <b>${Y.n}</b> («${ryRN(g.room)}») хочет попрощаться и оставить отзыв.</p><div class="row"><button class="btn primary" data-x="ry:rev:${i}">Прочитать отзыв</button></div>`;}).join("");
  const idle=R.g.length?"":`<p>${h>=18&&R.day===dayKey()?"Сегодня путников больше не будет.":"По вечерам, после шести, к воротам приходят странствующие ёкаи и просятся на ночлег."}</p>`;
  return`<div class="hubc"><h4>🏮 Рёкан <i>旅館</i></h4><p>«${RY_RANK[rk][1]}» · слава ${R.fame}<span class="ry-bar"><i style="width:${pct}%"></i></span>${nx?`<small>до «${nx[1]}» — ${nx[0]-R.fame}</small>`:""}</p>
   ${lines}${idle}<div class="row"><button class="btn" data-x="ry:book">📖 Книга постояльцев${R.book.length?" ("+R.book.length+")":""}</button></div></div>`;});

// test handle: X.ry.D() state, X.ry.step(), X.ry.host(i), X.ry.pick(room,fut,dish), X.ry.ok(), X.ry.review(i), X.ry.book(), X.ry.night(dayShift) moves sleepers back
X.ry={D:ryD,step:ryStep,host:ryHost,ok:ryOk,review:ryReview,book:ryBook,ask:ryAskDlg,known:ryKnown,hits:()=>ryHits,
  pick:(room,fut,dish)=>{if(ryPick)Object.assign(ryPick,{room,fut,dish});},
  night:()=>{const d=new Date(dayKey()+"T12:00:00");d.setDate(d.getDate()-1);for(const g of ryD().g)g.day=dayKey(d);},
  reset:()=>{const R=ryD();R.day="";R.g=[];ryArr=0;}};
}
