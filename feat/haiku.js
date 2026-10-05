{
// «Хайку недели» (prefix hi, S.ext.haiku). Every ISO week a new set of 26 word tiles: kigo of the season, pauses, small words and words about
// the house, Musya, the night and yōkai. The player lays them into three lines (5-7-5, ±1 allowed with a softer rating) or types the lines,
// needs one kigo of the current season, and hangs the poem on the veranda (a paper strip on the right pillar). The week's first haiku counts:
// the next day one of the known yōkai answers with its own haiku and a line about the player's poem. Art: art/haiku_art.py → atlas_hi.webp.
// S.ext.haiku={l:[{id,w,d,x:[3 lines],s:[3 counts],k:kigo,sea,st:★,own,c:counted,r:{y:yokai,d:reply day,c:comment,got,tst,read}}],
//   dr:{w,l:[[tile idx]×3],a:active line,sel:[line,pos],m:"t"|"w",tx:[3 typed lines]},sea:{aut:1},hang:id on the veranda}
const HI_SEA={aut:["осень","осени"],win:["зима","зимы"],spr:["весна","весны"],sum:["лето","лета"]};
// kigo: "shown text|stems for typed text" (stems match at a word start, ё = е)
const HI_K={
 aut:["луна|лун","полная луна|лун","лунный свет|лун","красные клёны|клён,клен","крик журавлей|журавл","осенний ветер|осен","осенний дождь|осен","осенний вечер|осен",
  "первый холод|холод","сверчок|сверч","хурма|хурм","долгая ночь|долгая ночь,долгие ноч,долгой ноч","туман|туман","листопад|листопад,опавш","роса|роса,росы,росу,росой,росинк",
  "хризантемы|хризантем","Млечный Путь|млечн","гуси летят|гуси,гусей,гусин","каштаны|каштан","жёлтые листья|жёлт,желт"],
 win:["первый снег|снег,снеж","снегопад|снег","иней|иней,инее","мороз|мороз","метель|метел","зимняя луна|зим","котацу|котацу","сосульки|сосульк","голые ветви|голые ветв,голых ветв",
  "зимнее солнце|зим","тонкий лёд|лёд,лед,льдин,ледян","угли в жаровне|жаровн,угли,углей","зимняя ночь|зим","следы на снегу|снег","нарциссы|нарцисс","дикие утки|утки,уток,утка",
  "юдзу в купальне|юдзу","сухие листья|сухие лист,сухих лист","стужа|стуж","вьюга|вьюг"],
 spr:["сакура|сакур","цветы сливы|слив","весенний дождь|весен,весн","весенний ветер|весен,весн","весенняя ночь|весен,весн","соловей|солов","лягушка|лягуш,лягушат","бабочка|бабоч",
  "тающий снег|тающ,талый,талая,талые","дымка|дымк","ласточки|ласточ","лепестки|лепест","первые травы|первые трав,молодая трав","ива|ива,ивы,иву,ивой","жаворонок|жаворон",
  "одуванчик|одуванч","долгий день|долгий ден,долгие дн","бутоны|бутон","тёплый ветер|тёплый ветер,теплый ветер","первые листья|первые листь,юные листь"],
 sum:["светлячки|светляч","цикады|цикад","летний дождь|летн","жара|жара,жары,жару,жарк,зно","прохлада|прохлад","лотос|лотос","ирисы|ирис","короткая ночь|короткая ночь,короткой ноч",
  "кукушка|кукуш","веер|веер","фурин|фурин","гроза|гроз","башни облаков|облак","юная листва|листв","сезон дождей|сезон дождей,цую","улитка|улитк","летний вечер|летн",
  "знойный полдень|зно,полдн","прохлада ночи|прохлад","вьюнок|вьюн"]};
// words about the house, Musya, the night and yōkai; small words and pauses (kireji) come every week
const HI_W={dom:["старый дом","на веранде","у порога","сёдзи","татами","бумажный фонарь","пустая чашка","чайник","в очаге","тень на стене","скрипит ступенька","дым над крышей",
  "под крышей","над прудом","колокольчик","открытая дверь"],
 cat:["Муся","котёнок","спит котёнок","Муся не спит","мягкие лапы","тихо мурлычет","хвост","ловит","жмурится","зевает","клубок","усы","смотрит"],
 nig:["ночь","тишина","темнота","звёзды","полночь","до рассвета","гаснет фонарь","тёмный сад","тихо","шорох","вдруг","снова","где-то","спят","ветер"],
 yo:["каппа","лисий огонь","тануки","кто-то смеётся","чьи-то шаги","глаз в темноте","тень за сёдзи","два хвоста","старый фонарь","ёкай","кто там?"]};
const HI_SM=["и","лишь","опять","как"],HI_P=["—","…","ах!"],HI_T=[5,7,5];
// the yōkai who answer: their own haiku for each season and a line about the player's poem (exact 5-7-5 / free)
const HI_Y={
 kappa:{n:"Каппа",f:0,mon:"m_kappa",aut:"Осенний ручей —/в блюдечке на макушке/плавает луна.",win:"Тонкий лёд реки —/я стучу в него снизу,/как в чужую дверь.",
  spr:"Талая вода —/в старом русле вновь слышу/голос лягушат.",sum:"Летняя река./Огурец плывёт ко мне —/прямо в лапы сам.",
  ex:k=>`Пять, семь, пять — ровно, как камни через ручей. «${k}» — будто из моей реки. Кап!`,lo:k=>`Слогов то больше, то меньше — река тоже не считает берега. А слово «${k}» хорошее. Кап!`},
 kitsune:{n:"Лиса-невеста",f:1,mon:"m_kitsune",aut:"Лисьи огоньки/кружат над сжатым полем —/свадьба без гостей.",win:"Белый капюшон/растворился в метели —/только след хвоста.",
  spr:"Дождь сквозь лепестки —/к Инари под зонтиком/невеста идёт.",sum:"Короткая ночь./Не успела я сменить/девичье лицо.",
  ex:k=>`Пять-семь-пять — след в след, как лиса ступает по снегу. Слово «${k}» я унесу на свадьбу.`,lo:k=>`Строчки разной длины — как следы, когда спешишь домой. Слово «${k}» мне по душе.`},
 tanuki:{n:"Тануки",f:0,mon:"m_tanuki",aut:"Полная луна —/бью в живот, а в ответ мне/ухает сова.",win:"Холод до костей —/прыгну в очаг чайником,/буду закипать.",
  spr:"Новый лист на лбу —/кем же стать этой весной?/Может, лягушкой.",sum:"Хор цикад в саду./Я стучу по животу —/сбились с ритма все.",
  ex:k=>`Пом-пом! Отстучал твои строки на животе — пять, семь, пять, до слога. А «${k}» — вкусно сказано.`,lo:k=>`Пом-пом! Отстучал на животе — где-то сбился, ну и ладно. Слово «${k}» звенит хорошо.`},
 nekomata:{n:"Нэкомата",f:1,mon:"m_nekomata",aut:"Ветер в камышах./Два хвоста мои шуршат/громче, чем листва.",win:"Сплю на котацу —/снится: я ещё совсем/слепой котёнок.",
  spr:"Весенняя ночь./На крыше кошки поют —/и я среди них.",sum:"Светлячок в траве —/лапой бью, а он уже/над моей спиной.",
  ex:k=>`Мяу. Ровно пять-семь-пять — мягко, как кошачий шаг. Слово «${k}» я промурлыкала вслух.`,lo:k=>`Мяу. Не по счёту, зато по сердцу. Слово «${k}» пахнет ночью — я проверила.`},
 akaname:{n:"Аканамэ",f:0,mon:"m_akaname",aut:"Осенний туман./Даже языком своим/не слизать луну.",win:"Зимний вечер. Пар/над остывшей купелью —/запах юдзу в нём.",
  spr:"Капли с потолка —/весенний дождь моет пол/лучше, чем язык.",sum:"Летний ливень стих —/в каждой лужице двора/звёзды… Лизнуть бы.",
  ex:k=>`Чисто-чисто, ни одного лишнего слога! Я бы так вылизал купальню. «${k}» — так и блестит.`,lo:k=>`Пара слогов торчит, как мочалка из кадки, но слово «${k}» блестит.`},
 obake:{n:"Тётин-обакэ",f:0,mon:"m_obake",aut:"Осенний вечер./Мотылёк стучится в бок —/тоже одинок.",win:"Первый снег. Мой глаз/щурится на белый двор —/слишком он светел.",
  spr:"Весенний ветер/рвёт мою бумагу — пусть:/сквозь неё — луна.",sum:"Комары звенят —/даже у бумажного/просят хоть глоток.",
  ex:k=>`Хи-хи. Пять-семь-пять — я посветил на каждую строку, и тени легли ровно. Слово «${k}» тёплое.`,lo:k=>`Хи-хи. Одна строка длинновата, как мой язык. Но слово «${k}» светит не хуже меня.`},
 warashi:{n:"Дзасики-вараси",f:1,mon:"m_warashi",aut:"Листья во дворе —/прячусь в самую кучу:/найди меня, ну!",win:"Иней на окне —/пальцем рисую кошку/с двумя хвостами.",
  spr:"Ласточки в гнезде —/значит, дом этот живой,/и я — никуда.",sum:"Фурин зазвенел —/это я дунула в щель/из-за сёдзи. Хи!",
  ex:k=>`Пять, семь, пять — я считала на пальцах, и всё сошлось! Слово «${k}» я спрятала в рукав.`,lo:k=>`Я считала на пальцах и сбилась — значит, весело написано! Слово «${k}» теперь моё любимое.`},
 kodama:{n:"Кодама",f:0,mon:"m_rg_kodama",aut:"Красные клёны./Кто-то крикнул в лес «ау»./Эхо — это я.",win:"Голые ветви./Сплю в старом стволе и жду/звона капели.",
  spr:"Первые листья./Каждый, как ладошка, мне/машет: «Ну, проснись!»",sum:"Ливень на листве —/тысячей ладоней я/пью и не напьюсь.",
  ex:k=>`Лес повторил твои строки эхом: пять, семь, пять — ни слога мимо. «${k}» звучит до сих пор.`,lo:k=>`Эхо вернуло строки чуть иначе — в горах так и бывает. Слово «${k}» лес запомнил.`}};
const HI_ORD=["первую","вторую","третью"],HI_ORDP=["первой","второй","третьей"];

// the two things (art/haiku_art.py → atlas_hi.webp 274×330)
addItems([{id:"hi_kake",n:"Танзаку-какэ с хайку",c:"Хайку",w:96,h:330,a:"t",p:0,at:["hi",0,0],src:"🖌 хайку недели",hint:"🖌 Повесь на веранде своё первое хайку"},
  {id:"hi_shikishi",n:"Сикиси с хайку на подставке",c:"Хайку",w:176,h:214,a:"b",p:0,at:["hi",98,0],src:"🖌 хайку недели",hint:"🖌 Сложи хайку ровно в 5-7-5 слогов"}],{hi:[274,330]});
STAMPS.push(["hi_first","句","Первое хайку","Повесь на веранде своё первое хайку"],["hi_575","韻","Пять-семь-пять","Сложи хайку ровно в 5-7-5 слогов"],
  ["hi_four","季","Четыре сезона","Напиши хайку осенью, зимой, весной и летом"]);
document.head.insertAdjacentHTML("beforeend",`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Marck+Script&display=swap"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Yuji+Syuku&display=swap&text=${encodeURIComponent("句俳")}"><style>
.hi-seg{display:flex;gap:6px;margin:4px 0 10px}.hi-seg button{flex:1;padding:8px 6px;border-radius:10px;border:1px solid var(--line);background:#0e1311;color:var(--muted);font-size:14px}.hi-seg button[aria-pressed=true]{background:var(--paper);color:var(--ink);font-weight:600}
.hi-lines{display:flex;flex-direction:column;gap:6px;margin:0 0 8px}
.hi-ln{display:flex;flex-wrap:wrap;align-items:center;gap:4px;min-height:46px;padding:5px 50px 5px 7px;position:relative;border-radius:10px;background:#1a1611;border:1px dashed rgba(216,210,195,.2);cursor:pointer}
.hi-ln.on{border:1px solid #c9a35a;background:#221c14}.hi-ln.w{padding-left:10px}
.hi-ph{color:var(--muted);font-size:13px;font-style:italic}
.hi-c{position:absolute;right:8px;top:50%;transform:translateY(-50%);font-size:13px;color:#d0705e;font-weight:700}.hi-c.ok{color:#8fcf7a}.hi-c.nr{color:#d8b25a}
.hi-t{touch-action:none;user-select:none;-webkit-user-select:none;display:inline-flex;align-items:flex-start;gap:2px;padding:6px 8px;border-radius:8px;background:#e9dfc8;color:#231a13;font-size:15px;line-height:1.1;box-shadow:0 1px 0 rgba(0,0,0,.45)}
.hi-t sup{font-size:9px;color:#8a6a4a;line-height:1}.hi-t.k{background:#f2dcc4;box-shadow:inset 0 0 0 1.5px #b8402a}.hi-t.k sup::after{content:" 季";color:#b8402a;font-family:var(--jp)}
.hi-t.p{background:#3a302a;color:#f0e4cc;font-weight:700}.hi-t.sel{outline:2px solid var(--sakura);outline-offset:1px}.hi-t.hi-gone{opacity:.25}
.hi-ghost{position:fixed;left:0;top:0;pointer-events:none;z-index:9999;transform:translate(-50%,-70%) scale(1.1);opacity:.95;box-shadow:0 6px 14px rgba(0,0,0,.6)}
.hi-pool{display:flex;flex-wrap:wrap;gap:5px;padding:8px;border-radius:10px;background:#0b0f0d;border:1px solid var(--line)}
.hi-tool{display:flex;gap:5px;margin:0 0 8px}.hi-tool button{flex:1;padding:7px 4px;border-radius:9px;border:1px solid var(--line);background:#1a1611;font-size:14px}
.hi-inp{flex:1;min-width:0;background:transparent;border:0;color:#efe3c8;font:inherit;font-size:16px;outline:none;padding:6px 0}
#xpBody p.hi-msg{font-size:14px;color:#d8b25a;margin:8px 0;line-height:1.4}#xpBody p.hi-msg.ok{color:#8fcf7a}#xpBody p.hi-kg{font-size:13px;color:var(--muted);margin:4px 0;line-height:1.45}
.hi-sk{position:relative;max-width:300px;margin:12px auto;padding:6px;border-radius:3px;background:linear-gradient(135deg,#a8782e,#e6c676 28%,#9c6e28 52%,#dcb868 78%,#8e6224);box-shadow:0 8px 20px rgba(0,0,0,.55)}
.hi-pp{position:relative;overflow:hidden;aspect-ratio:9/10;display:flex;flex-direction:column;justify-content:center;padding:26px 14px 46px 18px;background:#eee3ca;background-size:128px}
.hi-dc{position:absolute;inset:0;width:100%;height:100%}
:is(#xpBody,#albumBody) .hi-pp p.hi-l{position:relative;font-family:"Marck Script","Segoe Script",cursive;font-size:24px;line-height:1.45;margin:0;text-wrap:balance;color:#1e1612;text-shadow:0 0 1px rgba(30,22,18,.35)}
:is(#xpBody,#albumBody) .hi-pp p.hi-l1{padding-left:.8em}:is(#xpBody,#albumBody) .hi-pp p.hi-l2{padding-left:1.6em}
.hi-sk.sm{max-width:330px}.hi-sk.sm .hi-pp{aspect-ratio:auto;min-height:150px;padding:18px 12px 34px 16px}:is(#xpBody,#albumBody) .hi-sk.sm .hi-pp p.hi-l{font-size:19px;line-height:1.35}
.hi-seal{position:absolute;right:12px;bottom:10px;width:24px;height:24px;display:grid;place-items:center;background:#a8302a;color:#f4e2c4;font-style:normal;font-family:"Yuji Syuku",var(--jp);font-size:16px;border-radius:2px;box-shadow:inset 0 0 0 1.5px rgba(244,226,196,.5)}
.hi-sig{position:absolute;left:16px;bottom:10px;font-size:11px;color:#6e5a44;letter-spacing:.3px}
.hi-rp{display:flex;gap:10px;align-items:flex-start;max-width:360px;margin:6px auto 16px;padding:10px 12px;border-radius:12px;background:linear-gradient(160deg,#262b48,#171a2c);border:1px solid rgba(206,168,92,.35)}
.hi-rp img{width:62px;flex:none;filter:drop-shadow(0 3px 5px #000)}.hi-rp>div{flex:1;min-width:0}.hi-rp b{display:block;font-size:13px;color:#d8c08a;margin-bottom:4px}
:is(#xpBody,#albumBody) .hi-rp p.hi-rl{font-family:"Marck Script","Segoe Script",cursive;font-size:19px;line-height:1.3;color:#efdcae;margin:0}:is(#xpBody,#albumBody) .hi-rp p.hi-rl1{padding-left:.9em}:is(#xpBody,#albumBody) .hi-rp p.hi-rl2{padding-left:1.8em}
:is(#xpBody,#albumBody) .hi-rp p.hi-cm{font-size:13.5px;line-height:1.45;color:#b9c0d8;margin:8px 0 0;font-style:italic}
:is(#xpBody,#albumBody) p.hi-wait{text-align:center;font-size:13.5px;color:var(--muted);margin:0 0 16px}
.hi-row{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}.hi-row .btn{flex:1}</style>`);

let hiB=0,hiTC=null,hiCv=null,hiBox=null,hiFont=0,hiDrag=null,hiNoClk=0,hiPap=null;
function hiS(){const z=S.ext.haiku||(S.ext.haiku={l:[],dr:null,sea:{},hang:null});z.l=z.l||[];z.sea=z.sea||{};return z;}
const hiSea=()=>{const m=today().getMonth()+1;return m===12||m<3?"win":m<6?"spr":m<9?"sum":"aut";};
const hiSyl=s=>(String(s).toLowerCase().match(/[аеёиоуыэюя]/g)||[]).length;
const hiNorm=s=>String(s).toLowerCase().replace(/ё/g,"е");
function hiPl(n,f){const a=n%10,b=n%100;return n+" "+(a===1&&b!==11?f[0]:a>=2&&a<=4&&(b<12||b>14)?f[1]:f[2]);}
function hiWeek(){const d=new Date(Date.parse(dayKey()+"T12:00:00Z")),wd=(d.getUTCDay()+6)%7;d.setUTCDate(d.getUTCDate()-wd+3);
  const y=d.getUTCFullYear(),j=new Date(Date.UTC(y,0,4,12));return[y,1+Math.round(((d-j)/864e5-3+(j.getUTCDay()+6)%7)/7)];}
const hiWk=()=>{const [y,w]=hiWeek();return y+"-W"+String(w).padStart(2,"0");};
const hiNext=()=>new Date(Date.parse(dayKey()+"T12:00:00Z")+864e5).toISOString().slice(0,10);
const hiDate=dk=>new Date(Date.parse(dk+"T12:00:00Z")).toLocaleDateString("ru-RU",{day:"numeric",month:"long"});
const hiYN=y=>(HI_Y[y]||HI_Y.kappa).n,hiVerb=y=>(HI_Y[y]||HI_Y.kappa).f?"ответила":"ответил";
// this week's tiles: 7 kigo + 3 words of each theme (shuffled together), then small words and pauses
function hiTiles(){const wk=hiWk();if(hiTC&&hiTC.wk===wk)return hiTC.t;const [y,w]=hiWeek(),r=rng(y*977+w*7919),sea=hiSea();
  const mix=(a,n)=>{const b=a.slice();for(let i=b.length-1;i>0;i--){const j=Math.floor(r()*(i+1));[b[i],b[j]]=[b[j],b[i]];}return b.slice(0,n);};
  const main=mix([...mix(HI_K[sea],7).map(s=>({t:s.split("|")[0],k:1})),...["dom","cat","nig","yo"].flatMap(c=>mix(HI_W[c],3).map(t=>({t})))],99);
  const t=[...main,...HI_SM.map(t=>({t})),...HI_P.map(t=>({t,p:1}))].map(o=>Object.assign(o,{s:hiSyl(o.t)}));hiTC={wk,t};return t;}
function hiDr(){const z=hiS(),wk=hiWk();let d=z.dr;if(!d||d.w!==wk)d=z.dr={w:wk,l:[[],[],[]],a:0,sel:null,m:d&&d.m||"t",tx:d&&d.tx||["","",""]};return d;}
function hiJoin(ids){const T=hiTiles();let s="";for(const i of ids){const w=T[i]&&T[i].t;if(!w)continue;s+=w==="…"?"…":(s?" ":"")+w;}return s;}
function hiFind(text,sea){const tx=" "+hiNorm(text).replace(/[^а-я0-9 ]+/g," ").replace(/\s+/g," ")+" ";
  const E=HI_K[sea].map(e=>e.split("|"));for(const [disp] of E.slice().sort((a,b)=>b[0].length-a[0].length))if(tx.includes(" "+hiNorm(disp)+" "))return disp;   // the whole kigo first, then any stem
  for(const [disp,st] of E)if(st.split(",").some(s=>tx.includes(" "+hiNorm(s))))return disp;return null;}
function hiCheck(L){const s=L.map(hiSyl),sea=hiSea(),all=L.join(" "),k=hiFind(all,sea);let msg="",ok=false;
  const emp=L.findIndex(x=>!x.trim()),bad=s.findIndex((n,i)=>Math.abs(n-HI_T[i])>1);
  if(emp>=0)msg=`Заполни ${HI_ORD[emp]} строку.`;
  else if(bad>=0)msg=`В ${HI_ORDP[bad]} строке ${hiPl(s[bad],["слог","слога","слогов"])} — нужно ${HI_T[bad]}.`;
  else if(!k){const o=Object.keys(HI_SEA).filter(q=>q!==sea).map(q=>[hiFind(all,q),q]).find(q=>q[0]),ex=hiTiles().filter(t=>t.k).slice(0,2).map(t=>`«${t.t}»`).join(" или ");
    msg=o?`«${o[0]}» — слово ${HI_SEA[o[1]][1]}, а сейчас ${HI_SEA[sea][0]}. Добавь, например, ${ex}.`:`Нужно слово сезона — сейчас ${HI_SEA[sea][0]}. Например, ${ex}.`;}
  else ok=true;
  const ex=ok&&s.every((n,i)=>n===HI_T[i]),dev=s.reduce((a,n,i)=>a+Math.abs(n-HI_T[i]),0),st=!ok?0:ex?3:dev<=1?2:1;
  if(ok)msg=ex?`Ровно 5-7-5, слово сезона — «${k}». Можно вешать!`:`Почти 5-7-5 — свободная форма тоже хороша. Слово сезона — «${k}».`;
  return{s,ok,ex,st,k,msg};}
const hiCc=(n,i)=>n===HI_T[i]?"ok":Math.abs(n-HI_T[i])===1?"nr":"";
const hiTile=(t,i,x,sel)=>`<button class="hi-t${t.k?" k":""}${t.p?" p":""}${sel?" sel":""}" data-ti="${i}"${x}>${esc(t.t)}${t.s?`<sup>${t.s}</sup>`:""}</button>`;

// ── the composer panel ──
function hiComp(){const d=hiDr(),T=hiTiles(),sea=hiSea(),[,w]=hiWeek(),used=new Set(d.l.flat()),L=d.m==="w"?d.tx:d.l.map(hiJoin),c=hiCheck(L);
  let h=`<p class="lead">${w}-я неделя, ${HI_SEA[sea][0]}. Три строки — 5, 7 и 5 слогов, и хотя бы одно слово сезона (метка 季). Новые слова — каждый понедельник.</p>
  <div class="hi-seg"><button data-x="hi:m:t" aria-pressed="${d.m!=="w"}">Из слов</button><button data-x="hi:m:w" aria-pressed="${d.m==="w"}">Написать самой</button></div><div class="hi-lines">`;
  if(d.m==="w")h+=[0,1,2].map(i=>`<div class="hi-ln w"><input class="hi-inp" data-i="${i}" maxlength="60" autocomplete="off" value="${esc(d.tx[i])}" placeholder="${["пять","семь","пять"][i]} слогов"><b class="hi-c ${hiCc(c.s[i],i)}" id="hiC${i}">${c.s[i]}/${HI_T[i]}</b></div>`).join("");
  else h+=[0,1,2].map(i=>`<div class="hi-ln${d.a===i?" on":""}" data-x="hi:ln:${i}" data-ln="${i}">${d.l[i].map((ti,p)=>hiTile(T[ti],ti,` data-x="hi:pt:${i}:${p}" data-ln="${i}" data-p="${p}"`,d.sel&&d.sel[0]===i&&d.sel[1]===p)).join("")||`<span class="hi-ph">${["пять","семь","пять"][i]} слогов — нажми на слово внизу</span>`}<b class="hi-c ${hiCc(c.s[i],i)}">${c.s[i]}/${HI_T[i]}</b></div>`).join("");
  h+=`</div>`;
  if(d.m!=="w"){if(d.sel)h+=`<div class="hi-tool"><button data-x="hi:mv:l">◀</button><button data-x="hi:mv:r">▶</button><button data-x="hi:mv:up">↑ строка</button><button data-x="hi:mv:dn">↓ строка</button><button data-x="hi:mv:rm">✕</button></div>`;
    h+=`<div class="hi-pool">${T.map((t,i)=>used.has(i)?"":hiTile(t,i,` data-x="hi:t:${i}"`,false)).join("")}</div><p class="hi-kg">Нажми на слово — оно встанет в выделенную строку. Слова можно перетаскивать; нажми на слово в строке, чтобы сдвинуть или убрать его.</p>`;}
  else h+=`<p class="hi-kg">Слова сезона: ${HI_K[sea].map(s=>s.split("|")[0]).join(", ")}.</p>`;
  h+=`<p class="hi-msg${c.ok?" ok":""}" id="hiMsg">${c.msg}</p><div class="hi-row"><button class="btn" data-x="hi:clr">Стереть</button><button class="btn primary" id="hiHang" data-x="hi:hang"${c.ok?"":" disabled"}>Повесить на веранде</button></div>`;
  openPanel("Хайку недели",h,"hi_comp");}
function hiLive(){const d=hiDr(),c=hiCheck(d.tx);for(let i=0;i<3;i++){const e=$("hiC"+i);if(e){e.textContent=c.s[i]+"/"+HI_T[i];e.className="hi-c "+hiCc(c.s[i],i);}}
  const m=$("hiMsg");if(m){m.textContent=c.msg;m.className="hi-msg"+(c.ok?" ok":"");}const b=$("hiHang");if(b)b.disabled=!c.ok;}
function hiMove(op){const d=hiDr();if(!d.sel)return;const [ln,p]=d.sel,a=d.l[ln];if(p>=a.length){d.sel=null;return;}
  if(op==="l"||op==="r"){const q=p+(op==="l"?-1:1);if(q<0||q>=a.length)return;[a[p],a[q]]=[a[q],a[p]];d.sel=[ln,q];}
  else if(op==="up"||op==="dn"){const nl=ln+(op==="up"?-1:1);if(nl<0||nl>2)return;const [ti]=a.splice(p,1);d.l[nl].push(ti);d.sel=[nl,d.l[nl].length-1];d.a=nl;}
  else if(op==="rm"){a.splice(p,1);d.sel=null;}}
// drag a tile (pool or line) into a line; dropped outside the lines it goes back to the pool
function hiDrop(b,x,y){const d=hiDr(),ti=+b.dataset.ti,from=b.dataset.ln!=null?[+b.dataset.ln,+b.dataset.p]:null,el=document.elementFromPoint(x,y),ln=el&&el.closest&&el.closest(".hi-ln[data-ln]");
  if(!ln){if(from){d.l[from[0]].splice(from[1],1);d.sel=null;}hiComp();return;}
  const li=+ln.dataset.ln,kids=[...ln.querySelectorAll(".hi-t")].filter(e=>e!==b);let at=kids.length;
  for(let i=0;i<kids.length;i++){const r=kids[i].getBoundingClientRect();if(y<r.top||(y<=r.bottom&&x<r.left+r.width/2)){at=i;break;}}
  if(from)d.l[from[0]].splice(from[1],1);else if(d.l.flat().includes(ti)){hiComp();return;}
  d.l[li].splice(Math.min(at,d.l[li].length),0,ti);d.a=li;d.sel=null;tone(620,.08,"sine",.03);hiComp();}
$("xpBody").addEventListener("pointerdown",ev=>{const b=ev.target.closest&&ev.target.closest(".hi-t");if(!b||!panelIs("hi_comp"))return;hiDrag={b,x:ev.clientX,y:ev.clientY,id:ev.pointerId,on:false,g:null};});
window.addEventListener("pointermove",ev=>{const g=hiDrag;if(!g||ev.pointerId!==g.id)return;
  if(!g.on){if(Math.hypot(ev.clientX-g.x,ev.clientY-g.y)<8)return;g.on=true;g.g=g.b.cloneNode(true);g.g.classList.add("hi-ghost");document.body.appendChild(g.g);g.b.classList.add("hi-gone");}
  g.g.style.left=ev.clientX+"px";g.g.style.top=ev.clientY+"px";ev.preventDefault();},{passive:false});
window.addEventListener("pointerup",ev=>{const g=hiDrag;hiDrag=null;if(!g||!g.on)return;g.g.remove();hiNoClk=Date.now();hiDrop(g.b,ev.clientX,ev.clientY);});
window.addEventListener("pointercancel",()=>{const g=hiDrag;hiDrag=null;if(g&&g.g){g.g.remove();hiComp();}});
$("xpBody").addEventListener("input",ev=>{const t=ev.target;if(!t.classList||!t.classList.contains("hi-inp"))return;hiDr().tx[+t.dataset.i]=t.value.slice(0,60);hiLive();});

// ── hanging the poem; the yōkai who will answer ──
function hiWho(){const z=hiS(),met=(S.ext.lan&&S.ext.lan.met)||{},D=(S.ext.disc||{}).rareguest||{};
  let p=GUESTS.filter(g=>HI_Y[g.id]&&(S.friends[g.id]||{n:0}).n>0).map(g=>g.id);if(met.kodama||D.kodama)p.push("kodama");
  if(!p.length)p=["kappa","tanuki","obake","kitsune"];
  const last=(z.l.filter(h=>h.r).slice(-1)[0]||{r:{}}).r.y,[y,w]=hiWeek();let i=(y*31+w)%p.length;if(p.length>1&&p[i]===last)i=(i+1)%p.length;return p[i];}
function hiHang(){const d=hiDr(),L0=(d.m==="w"?d.tx:d.l.map(hiJoin)).map(s=>s.replace(/\s+/g," ").trim()),c=hiCheck(L0);if(!c.ok)return;
  const L=L0.slice();L[0]=L[0].charAt(0).toUpperCase()+L[0].slice(1);
  const z=hiS(),wk=hiWk(),sea=hiSea(),first=!z.l.length,cnt=!z.l.some(h=>h.w===wk&&h.c),got=[];
  const h={id:Date.now().toString(36)+Math.floor(Math.random()*1296).toString(36),w:wk,d:dayKey(),x:L,s:c.s,k:c.k,sea,st:c.st,own:d.m==="w"?1:0};
  if(cnt){const y=hiWho();h.c=1;h.r={y,d:hiNext(),c:HI_Y[y][c.ex?"ex":"lo"](c.k)};disc("haiku",wk);S.needs.joy=clamp(S.needs.joy+8,0,100);}
  z.l.push(h);z.hang=h.id;z.sea[sea]=1;
  if(first)award("hi_first");
  if(cnt&&!S.owned.has("hi_kake")){S.owned.add("hi_kake");got.push("hi_kake");}
  if(c.ex){award("hi_575");if(!S.owned.has("hi_shikishi")){S.owned.add("hi_shikishi");got.push("hi_shikishi");}}
  if(Object.keys(z.sea).length>=4)award("hi_four");
  d.l=[[],[],[]];d.tx=["","",""];d.a=0;d.sel=null;save();chime([523,659,784]);hubDot();hiShow(h.id,got);}

// ── the shikishi card: washi texture (made once), gold flecks and a seasonal motif in SVG, the poem in a brush hand ──
function hiPaper(){if(hiPap)return hiPap;const c=document.createElement("canvas");c.width=c.height=128;const g=c.getContext("2d"),r=rng(808);g.fillStyle="#eee3ca";g.fillRect(0,0,128,128);
  const im=g.getImageData(0,0,128,128),a=im.data;for(let i=0;i<a.length;i+=4){const n=(r()-.5)*14;a[i]+=n;a[i+1]+=n;a[i+2]+=n*.8;}g.putImageData(im,0,0);
  for(let i=0;i<26;i++){g.strokeStyle=i%3?"rgba(255,252,240,.5)":"rgba(140,110,70,.16)";g.lineWidth=.6+r()*.6;const x=r()*128,y=r()*128;g.beginPath();g.moveTo(x,y);g.quadraticCurveTo(x+r()*30-15,y+r()*30-15,x+r()*40-20,y+r()*40-20);g.stroke();}
  try{hiPap=c.toDataURL("image/jpeg",.82);}catch(e){hiPap="";}return hiPap;}
function hiLeaf(x,y,s,rot,col){const T=[[-200,.62],[-142,.85],[-90,1],[-38,.85],[20,.62]],P=[];
  T.forEach(([a,l],i)=>{P.push([a,l]);if(i<T.length-1)P.push([(a+T[i+1][0])/2,.34]);});
  const pt=([a,l])=>{const t=(a+rot)*Math.PI/180;return(x+Math.cos(t)*l*s).toFixed(1)+","+(y+Math.sin(t)*l*s).toFixed(1);};
  const st=(90+rot)*Math.PI/180;return`<path d="M${pt([-200,.25])} L${P.map(pt).join(" L")} L${pt([20,.25])} Z" fill="${col}"/><path d="M${x},${y} L${(x+Math.cos(st)*s*.55).toFixed(1)},${(y+Math.sin(st)*s*.55).toFixed(1)}" stroke="${col}" stroke-width="1.2"/>`;}
function hiDeco(sea,r,sm){let s="";const W=300,H=sm?230:333;
  if(sea==="sum"){const gr=`<linearGradient id="hiDusk" x1="0" y1="0" x2="0" y2="1"><stop offset=".55" stop-color="#5a6aa0" stop-opacity="0"/><stop offset="1" stop-color="#5a6aa0" stop-opacity=".28"/></linearGradient>`;s+=`<defs>${gr}</defs><rect width="${W}" height="${H}" fill="url(#hiDusk)"/>`;}
  else s+=`<circle cx="${W-54}" cy="48" r="${sea==="spr"?27:22}" fill="${sea==="win"?"#c9d2dc":"#d8bf84"}" opacity="${sea==="spr"?.28:.42}"/>`;
  for(let i=0;i<46;i++){const z=1+r()*3.2;s+=`<rect x="${(r()*W).toFixed(1)}" y="${(r()*H).toFixed(1)}" width="${z.toFixed(1)}" height="${(z*(.6+r()*.6)).toFixed(1)}" fill="#c49a48" opacity="${(.3+r()*.55).toFixed(2)}"/>`;}
  if(sea==="aut")for(let i=0;i<5;i++)s+=hiLeaf(18+i*15+r()*10,H-30-r()*34,8+r()*5,r()*80-40,i%2?"#b8402a":"#c8642c");
  if(sea==="win")for(let i=0;i<34;i++)s+=`<circle cx="${(r()*W).toFixed(1)}" cy="${(r()*H).toFixed(1)}" r="${(.8+r()*1.8).toFixed(1)}" fill="#ffffff" opacity="${(.5+r()*.4).toFixed(2)}"/>`;
  if(sea==="spr")for(let i=0;i<14;i++){const x=W-r()*150,y=r()*H*.8;s+=`<ellipse cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" rx="${(3.5+r()*2).toFixed(1)}" ry="2.3" transform="rotate(${(r()*180)|0} ${x.toFixed(1)} ${y.toFixed(1)})" fill="#e89ab4" opacity="${(.55+r()*.35).toFixed(2)}"/>`;}
  if(sea==="sum")for(let i=0;i<9;i++){const x=(20+r()*(W-40)).toFixed(1),y=(H*.45+r()*H*.5).toFixed(1);s+=`<circle cx="${x}" cy="${y}" r="7" fill="#e8f070" opacity=".14"/><circle cx="${x}" cy="${y}" r="1.8" fill="#f4ff9a" opacity=".95"/>`;}
  return`<svg class="hi-dc" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true">${s}</svg>`;}
function hiCard(h,sm){const sea=h.sea||"aut",r=rng(parseInt(h.id,36)%2147483647);
  return`<div class="hi-sk${sm?" sm":""}"><div class="hi-pp" style="background-image:url(${hiPaper()})">${hiDeco(sea,r,sm)}${h.x.map((l,i,a)=>{const mx=Math.max(...a.map(q=>q.length)),fs=sm?Math.min(19,Math.floor(255/(mx*.48))):Math.min(24,Math.floor(228/(mx*.48)));return`<p class="hi-l hi-l${i}" style="font-size:${fs}px;white-space:nowrap">${hiNb(l)}</p>`;}).join("")}<i class="hi-seal">句</i><small class="hi-sig">${HI_SEA[sea][0]} · ${hiDate(h.d)}${h.st?" · "+"★".repeat(h.st):""}</small></div></div>`;}
function hiReply(h){const r=h.r;if(!r)return"";if(!r.got)return`<p class="hi-wait">Ответ придёт ${r.d<=hiNext()?"завтра":hiDate(r.d)} — его напишет кто-то из гостей.</p>`;
  const Y=HI_Y[r.y]||HI_Y.kappa;if(!r.read){r.read=1;save();}
  return`<div class="hi-rp"><img src="assets/mon/${Y.mon}.webp" alt=""><div><b>${Y.n} ${hiVerb(r.y)}:</b>${Y[h.sea||"aut"].split("/").map((l,i)=>`<p class="hi-rl hi-rl${i}">${hiNb(l)}</p>`).join("")}<p class="hi-cm">${esc(r.c)}</p></div></div>`;}
function hiShow(id,got){const z=hiS(),h=z.l.find(q=>q.id===id);if(!h)return;let msg="";
  if(got){msg=h.c?"Хайку висит на веранде, на правом столбе. Завтра кто-нибудь из гостей ответит своим.":"Хайку этой недели уже висит, а это легло в тетрадь и тоже повешено на веранде. Гости отвечают на одно хайку в неделю.";
    if(got.length)msg+=` Новая вещь: ${got.map(i=>IT[i].n).join(", ")} — в «🧺 Вещи».`;}
  openPanel("Хайку",`${msg?`<p class="lead">${msg}</p>`:""}${hiCard(h)}${hiReply(h)}<div class="hi-row"><button class="btn" data-x="hi:book">Тетрадь хайку</button><button class="btn primary" data-x="hi:go">Сложить ещё</button></div>`,"hi_card");
  $("xpBody").scrollTop=0;hubDot();}
function hiLead(){const z=hiS(),ex=z.l.filter(h=>h.st===3).length,se=["aut","win","spr","sum"].filter(q=>z.sea[q]).map(q=>HI_SEA[q][0]);
  return`Хайку в тетради: ${z.l.length}, ровно 5-7-5: ${ex}. Времена года: ${se.join(", ")||"—"} (${se.length} из 4). Гости отвечают на одно хайку в неделю.`;}
function hiBook(){const z=hiS();openPanel("Тетрадь хайку",`<p class="lead">${hiLead()}</p>${z.l.slice().reverse().map(h=>hiCard(h,1)+hiReply(h)).join("")||`<p class="lead">Пока пусто.</p>`}<div class="hi-row"><button class="btn primary" data-x="hi:go">Сложить хайку</button></div>`,"hi_book");$("xpBody").scrollTop=0;hubDot();}
const hiNb=l=>esc(l).replace(/ —/g,"\u00a0—");
const hiUnread=()=>hiS().l.slice().reverse().find(h=>h.r&&h.r.got&&!h.r.read);
const hiHung=()=>{const z=hiS();return z.l.find(h=>h.id===z.hang)||null;};

hook("click",(k,b)=>{if(!k.startsWith("hi:"))return;const a=k.split(":"),d=hiDr();
  if(Date.now()-hiNoClk<400&&(a[1]==="t"||a[1]==="pt"||a[1]==="ln"))return true;   // the click that ends a drag
  if(a[1]==="go")hiComp();else if(a[1]==="book")hiBook();else if(a[1]==="show")hiShow(a[2]);else if(a[1]==="hang")hiHang();
  else if(a[1]==="m"){d.m=a[2]==="w"?"w":"t";d.sel=null;hiComp();}
  else if(a[1]==="ln"){d.a=+a[2];d.sel=null;hiComp();}
  else if(a[1]==="t"){const ti=+a[2];if(!d.l.flat().includes(ti))d.l[d.a].push(ti);d.sel=null;tone(560+hiTiles()[ti].s*40,.07,"sine",.03);hiComp();}
  else if(a[1]==="pt"){const ln=+a[2],p=+a[3];d.sel=d.sel&&d.sel[0]===ln&&d.sel[1]===p?null:[ln,p];d.a=ln;hiComp();}
  else if(a[1]==="mv"){hiMove(a[2]);hiComp();}
  else if(a[1]==="clr"){if(d.m==="w")d.tx=["","",""];else{d.l=[[],[],[]];d.a=0;}d.sel=null;hiComp();}
  return true;});
hook("hub",()=>{const z=hiS(),wk=hiWk(),cur=z.l.find(h=>h.w===wk&&h.c),u=hiUnread(),K=hiTiles().filter(t=>t.k).slice(0,3).map(t=>t.t);let p;
  if(u)p=`${hiYN(u.r.y)} ${hiVerb(u.r.y)} на твоё хайку`;else if(!cur)p=`Хайку этой недели ещё не написано — слова: ${K.join(", ")}…`;
  else if(!cur.r.got)p="Хайку недели висит на веранде. Ответ придёт завтра.";else p="Хайку этой недели написано. Новые слова — в понедельник.";
  return`<div class="hubc"><h4>🖌 Хайку недели <i>俳句</i></h4><p>${p}</p>${cur?hiCard(cur,1):""}<div class="row">${u?`<button class="btn primary" data-x="hi:show:${u.id}">Читать ответ</button>`:""}<button class="btn${!cur&&!u?" primary":""}" data-x="hi:go">${cur?"Сложить ещё":"Сложить хайку"}</button>${z.l.length?`<button class="btn" data-x="hi:book">Тетрадь</button>`:""}</div></div>`;});
hook("hubDot",()=>hiB&&!!hiUnread());
hook("album",el=>{const z=hiS();if(!z.l.length)return;const L=z.l.slice().reverse();
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Тетрадь хайку</h3><p class="lead">${hiLead()}</p>${L.slice(0,3).map(h=>hiCard(h,1)+hiReply(h)).join("")}${L.length>3?`<div class="hi-row"><button class="btn" data-x="hi:book">Вся тетрадь (${L.length})</button></div>`:""}`);});
// the reply comes the next day: a toast once the line is free, a dot on 家 until it is read
hook("sec",()=>{if(!hiB)return;const z=hiS(),dk=dayKey();let ch=0;for(const h of z.l)if(h.r&&!h.r.got&&dk>=h.r.d){h.r.got=1;ch=1;}if(ch)save();
  const p=z.l.find(h=>h.r&&h.r.got&&!h.r.read&&!h.r.tst);if(!p||scene.on||overlaysOpen()||$("toast").classList.contains("on"))return;
  p.r.tst=1;save();toast(`🖌 ${hiYN(p.r.y)} ${hiVerb(p.r.y)} на твоё хайку`);chime([784,988]);});
hook("away",()=>{const z=hiS(),p=z.l.find(h=>h.r&&!h.r.tst&&!h.r.read&&dayKey()>=h.r.d);if(!p)return null;p.r.got=1;p.r.tst=1;save();
  return{i:"🖌",t:`${hiYN(p.r.y)} ${hiVerb(p.r.y)} на твоё хайку своим — ответ ждёт в «家».`};});
hook("boot",()=>{hiB=1;try{document.fonts&&document.fonts.load('20px "Marck Script"',"Хайку луна").then(()=>{hiFont=1;hiCv=null;}).catch(()=>{});}catch(e){}});

// ── the strip on the veranda's right pillar (behind Musya, hangs from a nail and sways a little) ──
function hiStrip(h){if(hiCv&&hiCv.id===h.id&&hiCv.f===hiFont)return hiCv;const W=72,H=400;
  const mk=night=>{const c=document.createElement("canvas");c.width=W;c.height=H;const g=c.getContext("2d"),r=rng(parseInt(h.id,36)%2147483647);
    g.fillStyle="#ece0c4";g.fillRect(0,0,W,H);let gr=g.createLinearGradient(0,0,0,96);gr.addColorStop(0,"rgba(110,140,190,.55)");gr.addColorStop(1,"rgba(110,140,190,0)");g.fillStyle=gr;g.fillRect(0,0,W,96);
    gr=g.createLinearGradient(0,H-90,0,H);gr.addColorStop(0,"rgba(150,110,170,0)");gr.addColorStop(1,"rgba(150,110,170,.5)");g.fillStyle=gr;g.fillRect(0,H-90,W,90);
    for(let i=0;i<80;i++){g.fillStyle=`rgba(200,160,84,${(.3+r()*.6).toFixed(2)})`;const s=1+r()*3;g.fillRect(r()*W,r()*H,s,s*(.6+r()*.6));}
    g.fillStyle="#1e1612";g.textBaseline="middle";
    h.x.forEach((l,i)=>{const y0=20+i*30,len=H-y0-44;let fs=20;g.font=`${fs}px "Marck Script",cursive`;const m=g.measureText(l).width;if(m>len){fs*=len/m;g.font=`${fs}px "Marck Script",cursive`;}
      g.save();g.translate(W-15-i*21,y0);g.rotate(Math.PI/2);g.fillText(l,0,0);g.restore();});
    g.fillStyle="#b02e26";g.fillRect(9,H-32,14,14);g.strokeStyle="rgba(90,66,40,.55)";g.lineWidth=2;g.strokeRect(1,1,W-2,H-2);
    if(night){g.globalCompositeOperation="source-atop";g.fillStyle="rgba(10,14,28,.3)";g.fillRect(0,0,W,H);}return c;};
  hiCv={id:h.id,f:hiFont,d:mk(0),n:mk(1)};return hiCv;}
hook("draw",(t,front)=>{if(front||S.room!=="engawa")return;hiBox=null;if(scene.on)return;const h=hiHung();if(!h)return;const c=hiStrip(h);
  const x=Math.min(1350,visR()-32),[nx,ny]=imgToStage(x,610,.92),k=(imgToStage(x+100,610,.92)[0]-nx)/100,w=40*k,hh=222*k,cd=18*k;
  const a=(.03*Math.sin(t*.9)+.012*Math.sin(t*2.3+1))*(weather.on?2.2:1);
  ctx.save();ctx.translate(nx,ny);ctx.rotate(a);ctx.strokeStyle="rgba(206,170,104,.9)";ctx.lineWidth=Math.max(1,1.4*k);ctx.beginPath();ctx.moveTo(-w*.38,cd);ctx.lineTo(0,0);ctx.lineTo(w*.38,cd);ctx.stroke();
  ctx.fillStyle="rgba(0,0,0,.25)";ctx.fillRect(-w/2+2*k,cd+3*k,w,hh);ctx.drawImage(dayTint()[1]?c.n:c.d,-w/2,cd,w,hh);ctx.restore();
  ctx.fillStyle="#2a1e14";ctx.beginPath();ctx.arc(nx,ny,Math.max(1.5,2.6*k),0,Math.PI*2);ctx.fill();
  hiBox=[nx-w*.9,ny-4,nx+w*.9,ny+cd+hh+6];});
hook("hit",(x,y)=>{const b=hiBox;if(S.room!=="engawa"||!b||scene.on||x<b[0]||x>b[2]||y<b[1]||y>b[3])return false;const h=hiHung();if(!h)return false;
  hiShow(h.id);if(!petAway()&&pet.action!=="sleep")react("😺",1.4);return true;});

X.hi={S:hiS,tiles:hiTiles,week:hiWk,comp:hiComp,book:hiBook,show:hiShow,check:hiCheck,find:hiFind,box:()=>hiBox,Y:HI_Y,K:HI_K,syl:hiSyl,
  // tests: lay tiles by their texts into the three lines; type lines; hang; make the reply arrive now; tap the strip
  lay(L){const d=hiDr(),T=hiTiles();d.m="t";d.l=L.map(line=>line.map(w=>T.findIndex(t=>t.t===w)).filter(i=>i>=0));hiComp();return d.l.map(hiJoin);},
  type(L){const d=hiDr();d.m="w";d.tx=L.slice();hiComp();return hiCheck(L);},hang:hiHang,
  arrive(){for(const h of hiS().l)if(h.r)h.r.d=dayKey();},
  drag(sel,tsel){const b=document.querySelector(sel),t=document.querySelector(tsel);if(!b||!t)return"no";const r=b.getBoundingClientRect(),q=t.getBoundingClientRect(),x0=r.left+r.width/2,y0=r.top+r.height/2,x1=q.right-6,y1=q.top+q.height/2,P=(e,x,y,el)=>(el||window).dispatchEvent(new PointerEvent(e,{bubbles:true,clientX:x,clientY:y,pointerId:7}));
    P("pointerdown",x0,y0,b);P("pointermove",x0+20,y0+12);P("pointermove",x1,y1);P("pointerup",x1,y1);return hiDr().l.map(hiJoin);},tap(){const b=hiBox;return b?!!hk("hit",(b[0]+b[2])/2,(b[1]+b[3])/2):false;}};
}
