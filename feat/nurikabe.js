{
// «Нурикабэ у ворот» — the wall yōkai with a riddle. On every other evening (odd day numbers since 1970 — 5 Oct 2026 is one;
// 18:00–01:00, the hour after midnight still belongs to that evening) an old whitewashed wall with sleepy eyes grows across
// the path in the torii gate (soft rumble + toast once). Tap it → one riddle per visit (3 options); wrong → it yawns, gives a
// hint and 2 options; right → «Проходи, умная кошка», Musya taps its bottom with a paw (the legend: a stick to the bottom
// makes a nurikabe vanish), it sinks into the ground and leaves pantry food. Tap its bottom before that → it giggles (😼).
// 3/10/20 riddles → things. S.ext.nurikabe = {sol:[riddle ids], n: solved total, row: first-try streak, best, miss,
//  done: evening key answered, wait: evening key whose wall still waits to sink, cur:{k,id,w: wrong option or -1},
//  toast/rose: evening keys already announced / risen, last: last missed id, gift, prize}
const NU_C="Нурикабэ",NU_JP="塗壁",NU_MW=640,NU_MH=478,NU_IW=548,NU_BASE=[900,968,.38];
const NU_AT={nu_staff:[0,0,112,280],yawn:[114,0,250,174],nu_chip:[0,282,160,128],nu_tile:[162,282,176,124],blink:[0,412,248,68]};
const NU_PATCH={blink:[196,160,248,68],yawn:[196,158,250,174]};   // where the patches sit in the wall picture
MON.m_nu_wall=[NU_MW,NU_MH];
addItems([
 {id:"nu_tile",n:"Черепица с крыши нурикабэ",c:NU_C,w:176,h:124,a:"b",p:80,at:["nu",162,282],src:"🧱 загадки",hint:"Отгадай 3 загадки нурикабэ у ворот"},
 {id:"nu_chip",n:"Кусочек штукатурки с глазком",c:NU_C,w:160,h:128,a:"b",p:90,at:["nu",0,282],src:"🧱 загадки",hint:"Отгадай 10 загадок нурикабэ у ворот"},
 {id:"nu_staff",n:"Посох путника",c:NU_C,w:112,h:280,a:"b",p:120,at:["nu",0,0],src:"🧱 загадки",hint:"Отгадай 20 загадок нурикабэ у ворот"}],{nu:[520,480]});
const NU_PRIZE=[[3,"nu_tile"],[10,"nu_chip"],[20,"nu_staff"]];
STAMPS.push(["nu_first","壁","Загадка у ворот","Отгадай первую загадку нурикабэ"],["nu_ten","謎","Десять загадок","Отгадай 10 загадок нурикабэ"],
  ["nu_five","賢","Умная кошка","Отгадай 5 загадок нурикабэ подряд с первого раза"]);
BESTIARY.push(["nu_wall","m_nu_wall","Нурикабэ","Невидимая стена из преданий Кюсю: ночью вдруг встаёт поперёк дороги — ни пройти, ни обойти. Стукни палкой по её низу — и стены как не бывало, а по верху бить бесполезно. Наша, у ворот, старая, белёная и сонная — и загадывает загадки."]);
const NU_FOOD=["ds_dango","ds_onigiri","ds_mochi","ds_yakiimo","ds_taiyaki","ds_daifuku","ds_inari","v_kabocha","v_imo","v_shiitake"];
// [id, riddle, [right, wrong, wrong], hint after a wrong answer, explanation]
const NU_R=[
 [1,"Что значит японское слово «нэко»?",["Кошка","Собака","Лиса"],"Посмотри в лужу — оттуда на тебя глядит ответ.","猫 нэко — кошка. А кто не может есть горячее, у японцев «нэкодзита» — с кошачьим языком."],
 [2,"Как по-японски сказать «спасибо»?",["Аригато","Сайонара","Итадакимас"],"Это говорят, когда тебе что-то дали, — не перед едой и не на прощание.","Аригато — «спасибо». «Итадакимас» говорят перед едой, «сайонара» — при долгом прощании."],
 [3,"Кого в синто называют словом «ками»?",["Божеств и духов","Странствующих монахов","Самураев"],"Им молятся у тории — вот у этих самых ворот.","Ками — божества синто. Они живут в горах, деревьях, камнях и даже в старых вещах."],
 [4,"Как называется любование цветущей сакурой?",["Ханами","Цукими","Момидзигари"],"В этом слове прячется «хана» — цветок.","Ханами — «смотреть на цветы». Цукими — любование луной, момидзигари — красными клёнами."],
 [5,"Кого японцы видят в пятнах на Луне?",["Зайца, что толчёт моти","Лягушку под зонтиком","Спящего кота"],"Он длинноухий и очень трудолюбивый.","На Луне живёт заяц со ступкой и толчёт рисовые лепёшки моти. А люди на цукими угощаются данго."],
 [6,"Что такое фурин?",["Летний колокольчик на ветру","Банный халат","Бумажный фонарь"],"Его слышно, а не видно: «фу» — ветер, «рин» — звон.","Фурин — стеклянный или железный колокольчик. Говорят, от его звона в жару становится прохладнее."],
 [8,"Что такое котацу?",["Столик с одеялом и грелкой","Соломенная шляпа","Деревянные сандалии"],"Зимой из-под него торчат кошачьи хвосты.","Котацу — низкий столик, укрытый стёганым одеялом, с грелкой внизу. Кошки занимают его первыми."],
 [10,"Как зовут кошку, что машет лапкой у входа в лавку?",["Манэки-нэко","Бакэнэко","Нэкомата"],"Она совсем не страшная — только зазывает гостей и удачу.","Манэки-нэко — «зазывающая кошка». Правая лапа зовёт деньги, левая — гостей."],
 [11,"Как прогнать нурикабэ, если она встала на дороге?",["Стукнуть палкой по низу","Стукнуть палкой по верху","Обойти её стороной"],"Хи-хи… Верх у меня крепкий, а вот снизу щекотно.","Так говорят на Кюсю: стукни палкой по низу стены — и она исчезнет. По верху стучать бесполезно, а обойти её нельзя."],
 [12,"Что у каппы на макушке?",["Блюдце с водой","Соломенная шляпа","Пара рожек"],"Поклонись каппе — он поклонится в ответ, и всё прольётся.","В макушке у каппы блюдце с водой. Пока оно полное, каппа силён; прольётся — ослабеет."],
 [13,"Во что превращается зонтик, прослуживший сто лет?",["В одноглазого прыгуна","В журавля","В горного духа"],"Он скачет на одной ноге и показывает язык.","Каракаса-обакэ — старый зонтик с одним глазом, длинным языком и одной ногой. Так вещь, прослужившая век, обретает душу."],
 [14,"Сколько хвостов у нэкоматы?",["Два","Девять","Ни одного"],"Хвост у неё раздвоился, как тропинка у старой сосны.","Нэкомата — старая кошка-оборотень с раздвоенным хвостом. Девять хвостов бывает у лис."],
 [15,"Сколько хвостов может вырасти у очень старой лисы-кицунэ?",["Девять","Три","Двенадцать"],"Столько же, сколько жизней у кошки по пословице.","С годами у кицунэ прибавляются хвосты. Девятихвостая лиса мудра и могущественна."],
 [16,"Кто такой тэнгу?",["Горный дух с длинным носом","Речной дух с панцирем","Дух старого фонаря"],"Живёт в горах, машет веером из перьев и очень гордится своим носом.","Тэнгу — горный дух-воитель. У одних длинный красный нос, у других — птичий клюв."],
 [17,"Что делает аканамэ, когда ночью приходит в баню?",["Вылизывает грязь","Поёт колыбельные","Ворует мыло"],"Его имя так и значит — «лизун грязи».","Аканамэ навещает неубранные бани и слизывает грязь длинным языком. Лучшее средство от него — почаще мыть онсэн."],
 [18,"Что слышно у ручья, где живёт адзуки-арай?",["Шорох промываемых бобов","Звон монет","Плач младенца"],"Шурх-шурх… Всё дело в красных бобах.","Адзуки-арай невидим: у воды слышен только шорох бобов адзуки, которые он моет, а порой и его песенка."],
 [19,"Что творится ночью с шеей рокурокуби?",["Она тянется без конца","Она исчезает","На ней растут грибы"],"Смотри выше. Ещё выше. Ещё…","Днём рокурокуби — обычная женщина, а ночью её шея вытягивается, и голова бродит по дому."],
 [20,"Кто такие цукумогами?",["Старые вещи, обретшие душу","Лисы-оборотни","Горные отшельники"],"Твои зонтик, фонарь и сандалии тоже однажды могут проснуться.","Цукумогами — вещи, прослужившие сто лет: зонтики, фонари, гэта. Говорят, они обижаются, если их выбросить."],
 [21,"Чем питается баку?",["Дурными снами","Рисовой кашей","Лунным светом"],"Перед сном его просят: «Баку, съешь мой сон».","Баку — химера с хоботом слона. Если приснился кошмар, говорят: «Баку, съешь мой сон», — и он съест."],
 [22,"Чем знаменит тануки в японских сказках?",["Превращается во что угодно","Летает на облаке","Живёт в колодце"],"Положит листок на голову — и вот он уже чайник.","Тануки — енотовидная собака-оборотень. В сказке «Бумбуку тягама» он обернулся чайником."],
 [23,"Сколько часов в сутки спит кошка?",["Двенадцать — шестнадцать","Четыре","Ровно восемь, как люди"],"Посмотри на Мусю после обеда.","Кошки спят полдня и больше — копят силы для охоты. Или для клубка."],
 [24,"Зачем кошка мнёт лапками одеяло?",["Так она делала котёнком у мамы","Ищет спрятанную рыбу","Проверяет, не стена ли это"],"Это у неё с молочного детства.","Котята мнут маму лапками, когда пьют молоко. Взрослая кошка мнёт одеяло, когда ей тепло и спокойно."],
 [25,"Зачем кошке усы?",["Чтобы чуять проходы в темноте","Только для красоты","Чтобы ловить ими мух"],"В узкой щели ночью они важнее глаз.","Усы-вибриссы ловят малейшее движение воздуха. По ним кошка понимает, пролезет ли она в щель."],
 [27,"Как мяукают японские кошки?",["«Нян»","«Ван»","«Кэро»"],"Скажи «мяу» в нос — и поймёшь.","Японские кошки говорят «нян», собаки — «ван-ван», а лягушки — «кэро-кэро»."],
 [28,"Из чего делают татами?",["Из рисовой соломы и тростника","Из бамбуковых досок","Из овечьей шерсти"],"Они пахнут летним полем.","Татами — маты из рисовой соломы, обтянутые тростником игуса. Комнаты в Японии до сих пор меряют в татами."],
 [29,"Что такое токонома?",["Ниша для свитка и цветов","Кладовая для риса","Бочка с горячей водой"],"В спальне Муси в ней стоит икебана.","Токонома — почётная ниша в комнате: там вешают свиток и ставят цветы по сезону."],
 [32,"Что будет с домом, пока в нём живёт дзасики-вараси?",["Дому будет везти","Скиснет всё молоко","Пропадут все ложки"],"Этот ребёнок-дух любит играть в дальних комнатах.","Дзасики-вараси — дух-ребёнок. Пока он в доме, дом процветает; уйдёт — жди беды."],
 [33,"Какую птицу в Японии считают символом долголетия?",["Журавля","Ворону","Воробья"],"Сложишь тысячу бумажных таких — и желание сбудется.","Говорят, журавль живёт тысячу лет. Отсюда обычай складывать тысячу журавликов — сэмбадзуру."],
 [34,"Что ищут осенью на момидзигари?",["Красные листья клёна","Опавшие сосновые иглы","Цветущий лотос"],"Листья похожи на детские ладошки, только красные.","Момидзи — японский клён. Осенью ходят смотреть, как он краснеет: это и есть момидзигари."],
 [35,"Когда в Японии идёт цую — «сливовый дождь»?",["В начале лета","Зимой","В середине осени"],"Как раз когда зреют сливы.","Цую — затяжные дожди в июне и начале июля. Пишется 梅雨, «сливовый дождь»: в это время зреют сливы."],
 [36,"Как по-японски «светлячок»?",["Хотару","Хоси","Хотокэ"],"Он светится летними ночами над рисовыми полями.","Хотару — светлячок. «Хоси» — звезда, «хотокэ» — Будда. Смотреть на светлячков ходят к рекам в начале лета."],
 [38,"Как называется бумажка с предсказанием, которую тянут в храме?",["Омикудзи","Офуда","Оригами"],"У этих ворот её тянет и Муся — загляни в лоток.","Омикудзи — гадание на бумажке. Дурное предсказание завязывают на ветке у храма: пусть беда останется там."],
 [39,"Что пишут на деревянной дощечке эма?",["Желание","Свой адрес","Рецепт моти"],"Её вешают у храма, чтобы ками прочли.","Эма — дощечка, на которой пишут желание и вешают у храма для ками."],
 [40,"Что отмечают ворота тории?",["Вход в священное место","Границу рисового поля","Место для сушки белья"],"Ты стоишь прямо у них. За ними — уже не совсем наш мир.","Тории отделяют обычный мир от священного. Проходя под ними, кланяются и держатся края дорожки: середина — для ками."],
 [41,"Что празднуют на Танабату, 7 июля?",["Встречу двух звёзд-влюблённых","День рождения кошки","Первый снег"],"Раз в год они встречаются через Небесную реку.","Ткачиха и Пастух — звёзды Вега и Альтаир — встречаются раз в год. Желания пишут на полосках бумаги и вешают на бамбук."],
 [42,"Какую лапшу едят в канун Нового года?",["Гречневую собу","Рамэн","Удон с тыквой"],"Она длинная — к долгой жизни, и легко рвётся — как старые беды.","Тосикоси-соба — «лапша проводов года». Длинная — к долголетию, легко рвётся — чтобы оборвать невзгоды."],
 [43,"Кого встречают в дни Обона?",["Души предков","Первый снег","Перелётных журавлей"],"Летом для них зажигают фонари и танцуют.","В Обон души предков навещают родной дом: им зажигают фонари, а потом провожают огоньками по воде."],
 [44,"Без ног, а ходит; без рта, а гудит; в сёдзи стучит, в фурин звонит. Что это?",["Ветер","Мышь","Призрак"],"Он и мне в бока дует, а я стою.","Ветер — по-японски кадзэ. Летом ему рады: звенит фурин, и жара отступает."],
 [45,"Чем больше из неё берёшь, тем больше она становится. Что это?",["Яма","Миска риса","Стена"],"Возьми лопату — и увидишь. Со мной так не выйдет.","Яма: чем больше земли вынешь, тем она больше. А стена от этого только тоньше."],
 [46,"Что можно нарушить, даже не прикоснувшись?",["Обещание","Палочки для еды","Глиняную чашку"],"Его дают словами — и словами же нарушают.","Обещание. Японские дети скрепляют его мизинцами — юбикири — и поют, что лгунишка проглотит тысячу иголок."],
 [47,"Японская пословица: «У стен есть уши, а у сёдзи — …»",["глаза","хвост","зубы"],"Посмотри на меня внимательно. Что у меня под бровями?","«У стен есть уши, у сёдзи — глаза»: говори тише, тебя слышат. Я, между прочим, всё слышу."],
 [48,"Что значит пословица «И обезьяна падает с дерева»?",["Ошибаются и мастера","Не лезь куда не просят","Обезьяны плохо лазают"],"Даже лучшая древолазка иногда… бум!","Даже обезьяна падает с дерева — ошибиться может и знаток. Так что не горюй, если промахнёшься."],
 [49,"Что значит «кошке — золотую монету»?",["Дарить ценное тому, кто не оценит","Кошки приносят богатство","Кошку покупают на вес золота"],"Кошке нужна рыбка, а не золото.","Нэко ни кобан — «кошке золотой кобан». Как наше «метать бисер перед свиньями»."],
 [51,"Как молятся у храма синто?",["Два поклона, два хлопка, поклон","Один хлопок и прыжок","Три поклона спиной к храму"],"Число «два» здесь встречается дважды.","Обычай такой: два поклона, два хлопка, загадать желание — и ещё один поклон."],
 [52,"Почему палочки нельзя втыкать в рис стоймя?",["Так рис ставят для ушедших","Палочки от этого тупеют","Рис обидится и убежит"],"Так делают у поминального алтаря.","Миску риса с воткнутыми палочками ставят на поминальный алтарь. За обычным столом это дурная примета."]];
const NU_RI=Object.fromEntries(NU_R.map(r=>[r[0],r]));
const NU_ORD=(()=>{const a=NU_R.map(r=>r[0]);let h=4242;for(let i=a.length-1;i>0;i--){h=h*16807%2147483647;const j=h%(i+1);[a[i],a[j]]=[a[j],a[i]];}
  a.splice(a.indexOf(11),1);a.unshift(11);return a;})();   // the first riddle is about the nurikabe itself
// ── schedule ──
const nuDay=k=>Math.round(Date.parse(k)/864e5),nuOn=k=>nuDay(k)%2===1;
function nuEve(){return hourNow()<1?dayKey(new Date(today().getTime()-864e5)):dayKey();}   // 00:00–01:00 belongs to the evening before
function nuS(){const s=S.ext.nurikabe||(S.ext.nurikabe={});if(!s.sol)Object.assign(s,{sol:[],n:0,row:0,best:0,miss:0});return s;}
function nuHere(){const h=hourNow();return(h>=18||h<1)&&nuOn(nuEve());}
function nuWaits(){return nuHere()&&nuS().done!==nuEve();}                                   // the riddle is still unanswered tonight
function nuStands(){const s=nuS(),k=nuEve();return nuHere()&&(s.done!==k||s.wait===k);}
function nuNext(){const s=nuS(),T=today();for(let i=0;i<4;i++){const k=dayKey(new Date(T.getTime()+i*864e5));if(nuOn(k)&&s.done!==k)return i;}return 2;}
function nuStatus(){if(nuWaits())return"Сегодня вечером у ворот стоит нурикабэ";const d=nuNext(),w=d===0?"сегодня":d===1?"завтра":"послезавтра";
  if(nuHere())return`Стена ушла в землю — вернётся ${w} вечером`;return d===0?"Сегодня вечером у ворот встанет нурикабэ":`Стена придёт ${w} вечером`;}
function nuHideGame(){const k=X.kb&&X.kb.st&&X.kb.st();return!!(k&&k.room==="entrance");}
function nuPick(){const s=nuS();return NU_ORD.find(id=>!s.sol.includes(id)&&id!==s.last)??NU_ORD[(s.n+nuDay(nuEve()))%NU_ORD.length];}
function nuOrder(id){const r=id%3,a=[r,(r+1)%3,(r+2)%3];return id%2?a.reverse():a;}
function nuGift(k){const P=NU_FOOD.filter(id=>FOOD[id]);return P[(nuDay(k)>>1)%P.length];}
// ── sounds ──
function nuRumble(){tone(42,1.6,"sawtooth",.022);tone(55,1.3,"triangle",.07);setTimeout(()=>tone(47,1.2,"triangle",.05),380);}
function nuYawnSnd(){[392,330,262,220].forEach((f,i)=>setTimeout(()=>tone(f,.5,"sine",.035),i*210));}
function nuGiggle(){[880,988,880,1046].forEach((f,i)=>setTimeout(()=>tone(f,.09,"triangle",.03),i*90));}
// ── the riddle dialog ──
let nuA=null,nuBox=null,nuCv=null,nuAt=null,nuPuff=null,nuW=null,nuTk=0;
function nuDlg(head,html,ok,onOk){dlg({head,text:"",ok,onOk,img:`<img src="assets/mon/m_nu_wall.webp" alt="" style="height:40px">`});$("xdText").innerHTML=html;}
function nuShow(){const s=nuS(),c=s.cur,R=NU_RI[c.id],o=nuOrder(c.id).filter(i=>i!==c.w),btn=`<div class="nu-o">${o.map(i=>`<button class="btn" data-nu="${i}">${R[2][i]}</button>`).join("")}</div>`;
  if(c.w<0)nuDlg("🧱 Нурикабэ: «Отгадай — пропущу»",`<p class="nu-q">${R[1]}</p>${btn}`,"Потом");
  else nuDlg("🧱 Хо-о-ам… Не то",`<p class="nu-h">${R[3]}</p><p class="nu-q">${R[1]}</p>${btn}`,"Потом");}
function nuAsk(){const s=nuS(),k=nuEve();if(s.done===k)return;if(!s.cur||s.cur.k!==k){s.cur={k,id:nuPick(),w:-1};save();}nuShow();}
function nuAns(i){const s=nuS(),c=s.cur,k=nuEve();if(!c||c.k!==k||s.done===k)return dlgClose();const R=NU_RI[c.id];
  if(i===0){const first=c.w<0;s.n++;if(!s.sol.includes(c.id))s.sol.push(c.id);disc("nurikabe","r"+c.id);s.row=first?s.row+1:0;s.best=Math.max(s.best,s.row);
    s.done=s.wait=k;s.cur=null;s.gift=nuGift(k);give(s.gift,1);const pr=NU_PRIZE.find(([n,id])=>s.n>=n&&!S.owned.has(id));s.prize=pr?pr[1]:null;if(pr){S.owned.add(pr[1]);loadItem(pr[1]);}
    award("nu_first");if(s.n>=10)award("nu_ten");if(s.row>=5)award("nu_five");save();chime([660,880,990]);nuA={k:"smile",t0:now()};
    nuDlg("🧱 «Проходи, умная кошка»",`<p class="nu-r">Верно — «${R[2][0]}».</p><p class="nu-e">${R[4]}</p>`,"Пройти 🐾",nuPass);}
  else if(c.w<0){c.w=i;s.row=0;save();nuA={k:"yawn",t0:now()};nuYawnSnd();nuShow();}
  else{s.done=s.wait=k;s.cur=null;s.row=0;s.miss++;s.last=c.id;s.gift=s.prize=null;save();nuA={k:"yawn",t0:now()};nuYawnSnd();
    nuDlg("🧱 Эх, не угадала",`<p class="nu-r">Правильно — «${R[2][0]}».</p><p class="nu-e">${R[4]}</p><p class="nu-e">Ничего, приходи через вечер — будет новая.</p>`,"Ладно",nuPass);}
  hubDot();tabDots();}
// Musya taps the wall's bottom with her paw — and the wall sinks into the ground (gift and the new thing were given on the answer)
function nuPass(){const s=nuS();if(s.wait!==nuEve())return;s.wait=null;save();dlgClose();
  if(!petAway()&&pet.action!=="sleep"){start("poke");react("😼",1.6);}sfx("pop");nuA={k:"sink",t0:now()+.5};setTimeout(nuRumble,500);
  setTimeout(()=>{const g=s.gift,p=s.prize;s.gift=s.prize=null;save();
    if(g&&FOOD[g]){toast("🎁 Стена оставила: "+FOOD[g].n);if(S.room==="entrance"&&nuBox0)for(let i=0;i<4;i++)floatFx.push({g:pick(["🎁","✨"]),x:nuBox0.bx+rand(-40,40)*view.s,y:nuBox0.gY-rand(10,40)*view.s,t:now()+i*.12});}
    else toast("🧱 Стена сладко зевнула и ушла в землю");
    if(p&&IT[p])setTimeout(()=>toast("🧱 Новая вещь: "+IT[p].n),2100);ui();},3200);}
function nuTickle(){nuA={k:"tick",t0:now()};nuGiggle();if(!petAway()&&pet.action!=="sleep"){start("poke");react("😼",1.6);}
  toast(["🧱 Хи-хи, щекотно! Лапкой не считается","🧱 «Палкой бы по низу… Но сперва загадка»","🧱 «Ой-ой, не щекочи старую стену»"][nuTk++%3]);}
function nuTap(low){const s=nuS(),k=nuEve();if(s.wait===k)return nuPass();if(low&&s.done!==k)return nuTickle();nuAsk();}
function nuList(){const s=nuS(),sv=NU_R.filter(r=>s.sol.includes(r[0]));
  openPanel("Загадки нурикабэ",`<p class="lead">Стена загадывает по одной загадке за вечер. Отгаданные остаются здесь — с ответом и пояснением.</p>`+
    (sv.length?sv.map(r=>`<div class="hubc"><p><b>${r[1]}</b></p><p>— ${r[2][0]}. ${r[4]}</p></div>`).join(""):`<p class="lead">Пока ни одной. Загляни к воротам вечером.</p>`)+
    `<p class="lead">Ещё не отгадано: ${NU_R.length-sv.length}. Лучшая серия без ошибок: ${s.best}.</p>`,"nu_list");}
// ── drawing: the wall stands on the torii plane, across the path; things nearer than it are drawn again on top ──
function nuPrep(){if(nuCv||!MIMG.m_nu_wall||!nuAt)return;const T=TINT.entrance||"rgba(8,12,14,.42)";
  const mk=(w,h,f)=>{const c=document.createElement("canvas");c.width=w;c.height=h;const g=c.getContext("2d");f(g);g.globalCompositeOperation="source-atop";g.fillStyle=T;g.fillRect(0,0,w,h);return c;};
  nuCv={wall:mk(NU_MW,NU_MH,g=>g.drawImage(MIMG.m_nu_wall,0,0))};for(const k of["blink","yawn"]){const r=NU_AT[k];nuCv[k]=mk(r[2],r[3],g=>g.drawImage(nuAt,r[0],r[1],r[2],r[3],0,0,r[2],r[3]));}
  nuPuff=document.createElement("canvas");nuPuff.width=nuPuff.height=64;const g=nuPuff.getContext("2d"),gr=g.createRadialGradient(32,32,0,32,32,32);gr.addColorStop(0,"rgba(120,112,98,.55)");gr.addColorStop(1,"rgba(120,112,98,0)");g.fillStyle=gr;g.fillRect(0,0,64,64);}
let nuBox0=null;
function nuGeo(){curRow=null;const [bx,by]=imgToStage(NU_BASE[0],NU_BASE[1],NU_BASE[2]),[cx]=imgToStage(NU_BASE[0]+100,NU_BASE[1],NU_BASE[2]),k=(cx-bx)/100,w=NU_IW*k,h=w*NU_MH/NU_MW;
  return{bx,by,k,w,h,x0:bx-w/2,y0:by-h,gY:by-h*(1-466/NU_MH)};}
function nuOver(t,G){const d0=curD;for(const it of roomThings().map(ipos)){if(isFront(it))continue;const iid=it.imgId||it.id,m=DMETA[iid];if(!m)continue;const d=it.prop?it.d:(DECOR_D[it.id]??CAT_D);if(d<.45)continue;
    curD=d;curRow=it.y;const [x0,y0,w,h]=spriteBox(it),[sx,sy]=imgToStage(x0,y0);if(sx<G.x0+G.w&&sx+w*BGM.k>G.x0&&sy<G.gY&&sy+h*BGM.k>G.y0)drawSprite(ctx,iid,it.x,it.y,0,[it.x,it.y],1,it.sc,!!it.prop);}
  curD=d0;curRow=null;const q=S.guest;if(q&&(q.state==="here"||q.state==="fed"))drawGuest(t,false);}
const nuDraw=(t,front)=>{if(front)return;nuBox=null;if(S.room!=="entrance"||scene.on||nuHideGame())return;const a=nuA,sink=a&&a.k==="sink";
  if(!nuStands()&&!sink)return;nuPrep();if(!nuCv)return;if(!ST.seen.includes("nu_wall"))ST.seen.push("nu_wall");
  const G=nuGeo(),e=a?t-a.t0:99,s=view.s;nuBox0=G;let dy=0,rot=0,al=1,sh=0,face=(t*.19)%1<.03?"blink":null,dust=0;
  if(a&&a.k==="rise"){const u=clamp(e/1.8,0,1);dy=Math.pow(1-u,3)*G.h;al=clamp(u*3,0,1);if(u<1){sh=Math.sin(t*55)*1.6*s;dust=1-u;}else nuA=null;}
  else if(sink){const u=clamp(e/2.6,0,1);dy=u*u*G.h;face="blink";if(e>0&&u<1){sh=Math.sin(t*50)*1.6*s;dust=Math.min(1,u*3);}if(u>=1){nuA=null;return;}}
  else if(a&&a.k==="tick"){const u=clamp(e/1.3,0,1);rot=Math.sin(e*19)*.03*(1-u);face=u<1?"blink":face;if(u>=1)nuA=null;}
  else if(a&&a.k==="yawn"){if(e<2.8)face="yawn";else nuA=null;}
  else if(a&&a.k==="smile"){if(e<1.8)face="blink";else nuA=null;}
  const sy=1+.006*Math.sin(t*1.2);
  ctx.save();ctx.beginPath();ctx.rect(0,0,view.W,G.gY+1);ctx.clip();ctx.translate(G.bx+sh,G.by+dy);if(rot)ctx.rotate(rot);ctx.scale(1,sy);ctx.globalAlpha=al*.97;
  ctx.drawImage(nuCv.wall,-G.w/2,-G.h,G.w,G.h);if(face){const p=NU_PATCH[face],q=G.w/NU_MW;ctx.drawImage(nuCv[face],-G.w/2+p[0]*q,-G.h+p[1]*q,p[2]*q,p[3]*q);}ctx.restore();
  if(dust>0){ctx.save();for(let i=0;i<9;i++){const x=G.x0+G.w*(i+.5)/9+Math.sin(t*2.3+i)*8*s,r=(26+12*Math.sin(t*3.1+i*1.7))*G.k*2.2;ctx.globalAlpha=dust*(.55+.3*Math.sin(t*4+i));ctx.drawImage(nuPuff,x-r,G.gY-r*.9,r*2,r*1.4);}ctx.restore();}
  nuOver(t,G);if(!sink&&!(a&&a.k==="rise"))nuBox=G;};
hook("draw",nuDraw);
hook("hit",(x,y)=>{const b=nuBox;if(!b||S.room!=="entrance"||scene.on)return false;
  if(x<b.x0+b.w*.03||x>b.x0+b.w*.97||y<b.y0+b.h*.12||y>b.gY||hitCat(x,y)||decorHit(x,y))return false;audioInit();nuTap(y>b.y0+b.h*.74);return true;});
function nuRise(){const s=nuS(),k=nuEve();if(s.rose===k)return;s.rose=k;nuA={k:"rise",t0:now()+.5};setTimeout(nuRumble,450);
  if(s.toast!==k&&s.done!==k){s.toast=k;setTimeout(()=>toast("🧱 У ворот выросла стена…"),500);}save();
  if(s.done!==k)setTimeout(()=>{if(S.room==="entrance"&&nuWaits()&&$("xdlg").hidden)toast("🧱 «Не пущу! Отгадай загадку — пропущу»");},2600);}
hook("room",id=>{if(id==="entrance"&&nuStands()&&!scene.on)nuRise();});
hook("sec",()=>{const s=nuS(),k=nuEve(),w=nuWaits();if(w!==nuW){nuW=w;hubDot();tabDots();}
  if(S.room==="entrance"&&nuStands()&&s.rose!==k&&!scene.on&&!overlaysOpen())nuRise();
  if(w&&s.toast!==k&&now()>6&&!scene.on&&!$("toast").classList.contains("on")){s.toast=k;save();if(S.room!=="entrance"){toast("🧱 У ворот выросла стена…");nuRumble();}}});
hook("click",(key)=>{if(!key.startsWith("nu:"))return;const a=key.slice(3);if(a==="go"){closePanel();goRoom("entrance");}else if(a==="list")nuList();return true;});
hook("hub",()=>{const s=nuS(),p=NU_PRIZE.find(([n])=>s.n<n);
  return`<div class="hubc"><h4>🧱 Нурикабэ у ворот <i>${NU_JP}</i></h4><p>${nuStatus()}</p><p>Через вечер, с 18:00 до часу ночи, в тории у входа вырастает старая белёная стена с сонными глазами. Нажми на неё — она загадает загадку. Отгадаешь — пропустит и оставит гостинец.</p><p>Отгадано загадок: <b>${s.sol.length} из ${NU_R.length}</b>${s.row>1?` · подряд без ошибки: ${s.row}`:""}${p&&IT[p[1]]?` · до вещи «${IT[p[1]].n}» — ещё ${p[0]-s.n}`:""}</p><div class="row">${nuWaits()?`<button class="btn primary" data-x="nu:go">⛩ К воротам</button>`:""}<button class="btn" data-x="nu:list">📜 Загадки</button></div></div>`;});
hook("hubDot",()=>nuWaits());
hook("tabDot",r=>r==="entrance"&&nuWaits());
hook("away",ms=>{if(nuWaits()&&ms>3*3600e3)return{i:"🧱",t:"У ворот стоит сонная стена с загадкой"};});
hook("boot",()=>{atlasImg("nu",im=>{nuAt=im;});const h=HK.draw,i=h.indexOf(nuDraw);if(i>0)h.unshift(h.splice(i,1)[0]);   // the wall stands behind every other add-on's figure
  $("xdText").addEventListener("click",ev=>{const b=ev.target.closest("[data-nu]");if(!b)return;ev.stopPropagation();audioInit();nuAns(+b.dataset.nu);});nuW=nuWaits();});
document.head.insertAdjacentHTML("beforeend",`<style>#xdlg .nu-q{margin:0 0 2px}#xdlg .nu-o{display:flex;flex-direction:column;gap:7px;margin:10px 0 0}
#xdlg .nu-o .btn{text-align:left;justify-content:flex-start;font-size:16px;padding:9px 14px;width:100%;line-height:1.25}
#xdlg p.nu-h{font-size:15px;color:#d9c9a8;font-style:italic;margin:0 0 6px}#xdlg p.nu-r{margin:0 0 6px;color:#f0dcae}#xdlg p.nu-e{font-size:15px;line-height:1.45;color:#cfc8b8;margin:0 0 4px}</style>`);
X.nu={st:nuS,R:NU_R,ord:NU_ORD,eve:nuEve,here:nuHere,waits:nuWaits,stands:nuStands,next:nuNext,status:nuStatus,ask:nuAsk,ans:nuAns,pass:nuPass,box:()=>nuBox,
  anim(k){nuA={k,t0:now()};},reset(){S.ext.nurikabe=null;nuS();save();},
  tap(low){const b=nuBox;if(!b)return"nobox";return hk("hit",b.x0+b.w*(low?.12:.5),b.y0+b.h*(low?.86:.3))?"hit":"miss";},
  geo(){const G=nuGeo();return[G.x0,G.y0,G.w,G.h,G.gY].map(v=>Math.round(v));}};
}
