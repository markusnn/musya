// ───────────────────────── «Пропажа в доме» (prefix dt): a small weekly detective ─────────────────────────
// Once a week (Wednesday from 6:00, or the first visit on/after it) a thing vanishes from the house: one of the
// player's placed things, else a decor piece (the veranda furin…), else a core prop. Nothing is deleted for good:
// the original record lives in S.ext.mystery.c.thing and is ALWAYS put back — on solve, at the week's end, or at
// boot if anything looks wrong. Three clues lie in three rooms (fresh ones = the culprit, an old one = a red
// herring); three yōkai Musya knows give alibis in the notebook; the player names the culprit. A wrong name only
// offends the suspect and brings one more clue — the case can't be lost. Pictures: art/mystery_art.py → atlas_dt.
{
const DT_AT={wet:[568,0,150,70],cuke:[872,0,120,64],hair:[464,232,120,56],rice:[586,232,110,56],leaf:[0,232,96,64],paw:[720,0,150,70],sake:[98,232,110,64],
  thread:[698,232,116,52],bell:[210,232,76,64],fur2:[816,232,110,52],bone:[0,298,116,52],slick:[216,298,150,50],paper:[366,232,96,60],wax:[118,298,96,52],
  otedama:[288,232,76,62],bead:[368,298,90,46]};
const DT_CAT="Дела детектива",DT_IT=[
  {id:"dt_note",n:"Тетрадь сыщика",c:DT_CAT,w:170,h:110,a:"b",p:90,at:["dt",396,0]},
  {id:"dt_loupe",n:"Лупа на подставке",c:DT_CAT,w:140,h:180,a:"b",p:120,at:["dt",254,0]},
  {id:"dt_jitte",n:"Дзиттэ стражника",c:DT_CAT,w:110,h:230,a:"b",p:150,at:["dt",0,0]},
  {id:"dt_gando",n:"Фонарь гандо",c:DT_CAT,w:140,h:190,a:"b",p:160,at:["dt",112,0],glow:[70,112]}];
for(const i of DT_IT){i.src="🔍 дело недели";i.hint="🔍 Награда за раскрытое дело недели";}
addItems(DT_IT,{dt:[1024,350]});
STAMPS.push(["dt_first","探","Первое дело","Раскрой первое дело недели"],["dt_five","偵","Сыщик","Раскрой пять дел недели"],["dt_clean","明","Без единой ошибки","Раскрой дело, ни разу не обвинив невиновного"]);

// clues: name · what it is · fresh (the culprit, this night) · old (a red herring)
const DT_CL={
  wet:["Мокрые следы","Следы с перепонками между пальцами, пахнут тиной.","Вода ещё не высохла — их оставили этой ночью.","Края высохли и побелели — это след давнего визита."],
  cuke:["Огуречная кожура","Длинная спиралька кожуры — кто-то чистил огурец зубами.","Кожура сочная и пахнет свежестью.","Кожура высохла в бурую стружку — лежит не первый день."],
  hair:["Лисья шерсть","Клочок бело-золотой шерсти, мягкой, как пух.","Шерсть ещё тёплая и пахнет дождём при солнце.","Шерсть свалялась в пыли — её обронили давно."],
  rice:["Рис и абураагэ","Рассыпанный рис и кусочек жареного тофу — любимое подношение Инари.","Тофу ещё мягкое — кто-то перекусывал прямо здесь.","Рис засох и потемнел — это старое подношение."],
  leaf:["Листок на татами","Зелёный листок — тануки кладут такие на голову, чтобы превратиться.","Листок влажный, с пыльцой — сорван этой ночью.","Листок сухой и ломкий — пролежал тут с лета."],
  paw:["Круглые следы","Круглые грязные отпечатки лап — косолапые, вразвалочку.","Грязь ещё не засохла.","Грязь засохла коркой и крошится."],
  sake:["Опрокинутая чашечка","Чашечка для сакэ на боку и лужица — кто-то отмечал удачу.","Пахнет сакэ так, что щиплет нос.","Лужица давно высохла, остался липкий круг."],
  thread:["Красная нить","Тонкая красная шёлковая нить, длинная, как дорожка.","Нить блестит, на ней ни пылинки.","Нить вылиняла и пропылилась."],
  bell:["Бубенчик","Крошечный латунный бубенчик на красном шнурке — такие носят кошки.","Шнурок ещё пахнет шерстью.","Бубенчик потемнел и не звенит — потерян давно."],
  fur2:["Чёрно-белая шерсть","Шерстинки двух цветов, будто кто-то тёрся о порог двумя хвостами.","Шерстинки ещё тёплые.","Шерстинки серые от пыли."],
  bone:["Рыбий скелет","Скелетик рыбы, обглоданный до блеска.","Косточки влажные — ужинали этой ночью.","Косточки сухие, как бумага."],
  slick:["Блестящая полоса","Длинный блестящий след, будто доски вылизали языком.","Ещё липкая и блестит.","Потускнела — лизали давным-давно."],
  paper:["Клочок бумаги","Промасленный клочок фонарной бумаги с половинкой знака «灯».","Пахнет свежим маслом.","Масло выцвело, бумага пожелтела."],
  wax:["Капли воска","Застывшие капли воска и обгоревший фитилёк.","Воск ещё мягкий под лапой.","Воск твёрдый и пыльный."],
  otedama:["Мешочек отэдама","Маленький тряпичный мешочек с бобами для детской игры.","Он ещё тёплый, будто из чьей-то ладошки.","Ткань выцвела, по нему ползает паучок."],
  bead:["Стёклышки охадзики","Разноцветные стёклышки для детской игры.","Лежат кружком, будто игру бросили на середине.","Покрыты пылью — в них не играли много лет."]};
// the seven gate guests: their clues, gender (for «был/была»), innocent alibis, offended lines
const DT_YK={
  kitsune:{cl:["hair","rice","thread"],f:1,al:["Этой ночью я провожала паломников до святилища Инари. Спроси у каменных лис у ворот — они видели.","Лисы не берут чужого без спроса. Ну, почти никогда. В этот раз — точно нет."],
    off:"Меня? Лису-невесту? Фу. Я обиделась — до следующего дождя при солнце."},
  tanuki:{cl:["leaf","paw","sake"],al:["Я всю ночь играл в ханафуду и проиграл все листья. Свидетели — весь лес.","Пом-пом! Я был на рынке, менял каштаны на сладкий картофель. Могу показать кожуру."],
    off:"Пом… Обидно, вообще-то. Я думал, мы друзья. Пойду превращусь в обиженный чайник."},
  kappa:{cl:["wet","cuke"],al:["Я не выходил из реки: вода убывала, надо было беречь блюдце на макушке.","Каппа держит слово. Я дал слово не брать чужого — и блюдце моё полно воды."],
    off:"Кап… Даже блюдце на макушке задрожало от обиды. Ищите лучше."},
  nekomata:{cl:["bell","fur2","bone"],f:1,al:["Мяу. Я всю ночь танцевала на крыше храма с другими кошками. Нас видела луна.","Мне чужое ни к чему, сестрёнка. У меня два хвоста — что ещё нужно?"],
    off:"Ш-ш-ш! Два хвоста — ещё не повод подозревать. Обиделась."},
  akaname:{cl:["slick"],al:["Я до утра вылизывал вашу баню. Посмотри, как блестит!","Мне бы только грязь, а вещи мне ни к чему. Я их даже не лижу. Почти."],
    off:"Я вам баню вылизал, а вы… Эх. Пойду поплачу в кадушку."},
  obake:{cl:["paper","wax"],al:["Я светил у ворот всю ночь — спроси у мотыльков, они от меня не отходили.","Хи-хи, у меня один глаз, и он всю ночь смотрел на дорогу. Ничего не видел и ничего не брал."],
    off:"Хи… не хи-хи. Мне обидно. Даже глаз потускнел."},
  warashi:{cl:["otedama","bead","thread"],f:1,al:["Хи-хи. Я спала в кладовой на мешке с рисом. Спроси у мышей.","Если бы я что-то взяла, в доме стало бы холоднее. А разве холодно?"],
    off:"Не я! Не я! Вот уйду — и счастье из дома уйдёт… Ладно, не уйду. Но обиделась."}};
// eight cases: culprit, title, a shaky alibi, the reason told when the thing comes back ({n} = the thing)
const DT_TPL={
  kit_wed:{cul:"kitsune",t:"Дело о лисьей свадьбе",al:"Я? Всю ночь была дома. Ну… почти всю. А дождь при солнце — это просто погода, Муся. При чём тут свадьба?",
    why:"Это я, Муся. Этой ночью у нас была лисья свадьба: шёл дождь при солнце, и невеста шла через лес. По примете ей нужна вещь из доброго дома — тогда брак будет счастливым. Я взяла твою вещь — «{n}» — всего на одну ночь. Невеста кланяется тебе."},
  kit_moon:{cul:"kitsune",t:"Дело о луне на горе",al:"Я любовалась луной на горе. Одна. Совсем одна. Ничего с собой не брала, честное лисье.",
    why:"Да, я. Осенью луна так близко… Мне хотелось показать ей самое красивое, что есть в округе. Я отнесла твою вещь — «{n}» — на гору, и до рассвета мы вдвоём смотрели на луну. Возвращаю — с лунной пылью."},
  tan_form:{cul:"tanuki",t:"Дело о неудачном превращении",al:"Я всю ночь был… э-э… чайником. Стоял на полке, никого не трогал. Пом-пом.",
    why:"Пом… попался. Я учусь превращаться в вещи. Чайник у меня почти выходит, а вот твоя вещь — «{n}» — никак: без образца хвост торчит. Взял поучиться. Смотри — похоже? Ну, если не смотреть на хвост."},
  tan_drum:{cul:"tanuki",t:"Дело о барабане-животе",al:"Спал как убитый! Ну, барабанил немного. Во сне. Животом. А что, было слышно?",
    why:"Тануки-баяси! В полнолуние мы бьём в животы, как в барабаны, а сцена у нас была совсем голая. Я одолжил твою вещь — «{n}» — для красоты. Все хлопали! Животами."},
  kap_wind:{cul:"kappa",t:"Дело о ветре над рекой",al:"Я всю ночь сидел в реке. Под водой. Мокрый, как всегда. Огурцы? Какие огурцы?",
    why:"Кап… Над моим омутом так тихо. Хотелось, чтобы и у реки было как у вас — по-домашнему. Я унёс твою вещь — «{n}» — на одну ночь, слушать, как над водой гуляет ветер. Ни капли не пролил, честное каппье."},
  nek_warm:{cul:"nekomata",t:"Дело о тёплой ночи",al:"Мяу. Я гуляла по крышам, как все приличные кошки. Рыба? Не помню никакой рыбы.",
    why:"Мяу… Ночью было холодно и одиноко, а твоя вещь — «{n}» — пахнет домом и тобой, сестрёнка. Я проспала возле неё до рассвета, обвив двумя хвостами. Возвращаю — тёпленькой."},
  obk_talk:{cul:"obake",t:"Дело о ночном собеседнике",al:"Я светил у ворот, как обещал. Почти всю ночь. Масло капало? Это… от волнения.",
    why:"Хи-хи… У ворот ночью так скучно. Я забрал к себе твою вещь — «{n}» — поговорить. Чудесная собеседница: всё слушала и ни разу не перебила. Хи-хи."},
  war_hide:{cul:"warashi",t:"Дело о великих прятках",al:"Хи-хи. Я играла одна. В отэдаму. Нет, в охадзики. Нет… не скажу!",
    why:"Хи-хи! Это были прятки! Я спрятала твою вещь — «{n}» — и ждала, найдёшь ли. Ты так долго искала… значит, тебе не всё равно. Теперь водишь ты!"}};
const DT_IDS=Object.keys(DT_TPL),DT_REW=["dt_note","dt_loupe","dt_jitte","dt_gando"];
// rooms: on which side of Musya a clue may lie (on her floor line, a little behind it: the near 3D layers cover the
// strip in front of her; left sides of the courtyard/entrance and the kitchen hearth are busy), «из …» and «в …»
const DT_SPOT={entrance:[1],engawa:[1],courtyard:[1],kitchen:[-1],onsen:[-1,1],bedroom:[-1,1],wardrobe:[-1,1],games:[-1,1]};
const DT_FROM={entrance:"от ворот",engawa:"с веранды",courtyard:"из дворика",kitchen:"с кухни",onsen:"из онсэна",bedroom:"из спальни",wardrobe:"из гардероба",games:"из комнаты игр",kura:"из кладовой",attic:"с чердака"};
const DT_IN={entrance:"у ворот",engawa:"на веранде",courtyard:"во дворике",kitchen:"на кухне",onsen:"в онсэне",bedroom:"в спальне",wardrobe:"в гардеробе",games:"в комнате игр",kura:"в кладовой",attic:"на чердаке"};
// decor pieces that may vanish (bonsai, cranes, fish and moving things stay: other add-ons use them)
const DT_DEC={d_furin_glass:["стеклянный фурин","m"],d_furin_blue:["синий фурин","m"],d_furin_iron:["чугунный фурин","m"],d_chochin:["красный фонарь тётин","m"],d_andon:["андон","m"],
  d_ikebana:["икебана","f"],d_kokedama:["кокедама","f"],d_bamboo:["бамбук в горшке","m"],d_zab_indigo:["синяя подушка","f"],d_zab_red:["алая подушка","f"],d_zab_moss:["моховая подушка","f"],
  d_teru:["тэру-тэру-бодзу","m"],d_ume:["ветка сливы","f"],d_bowl_red:["миска Муси","f"],d_bowl_blue:["миска с рыбками","f"],d_masu:["коробочка масу","f"],d_tetsubin:["чайник тэцубин","m"],
  d_okeya:["кедровое окэ","n"],d_towels:["полотенца","p"],d_kaeru:["каменная лягушка","f"],d_kyodai:["зеркало кёдай","n"],d_kiku:["ваза с хризантемами","f"],
  d_scroll_moon:["свиток «Луна и сосна»","m"],d_scroll_koi:["свиток с карпами","m"],d_scroll_neko:["свиток «猫»","m"],d_scroll_mount:["свиток «Горы в тумане»","m"],
  d_daruma:["дарума","m"],d_kokeshi:["кукла кокэси","f"],d_maneki:["манэки-нэко","f"],d_teaset:["чайный набор","m"],d_koro:["курильница","f"],d_goban:["доска для го","f"]};
const DT_PROP=[["p_eng_toro","каменный фонарь","m"],["p_kit_noren","занавеска норэн","f"]];   // never the bedroom andon: it is the sleep switch
const DT_HOUSE=Object.keys(DT_SPOT),DT_SKIP=/^(mp_|dm_|bn_|dt_)/;
const rt={im:null,box:{},sc:null,lyK:"",ly:0};
const dt=()=>{const m=S.ext.mystery||(S.ext.mystery={});m.n=m.n||0;m.hist=m.hist||[];return m;};
const dtYmd=d=>d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");
// the «shifted week»: a case week runs Wednesday 6:00 → next Wednesday 6:00; its key is that Wednesday's date
// (the week of the newspaper stays Monday, the chest's is Thursday — one weekly event per day, no crowd on Monday)
const DT_WD=3,dtDay=()=>{const d=today(),h=hourNow()<6?1:0;return new Date(d.getFullYear(),d.getMonth(),d.getDate()-h);};
const dtWk=()=>{const d=dtDay();return dtYmd(new Date(d.getFullYear(),d.getMonth(),d.getDate()-(d.getDay()-DT_WD+7)%7));};
const dtDow=()=>(dtDay().getDay()-DT_WD+7)%7;   // 0 = Wednesday (from 6:00) … 6 = Tuesday
const dtAdd=(k,n)=>{const [y,m,d]=k.split("-").map(Number);return dtYmd(new Date(y,m-1,d+n));};
const DT_MON=["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"];
const dtEnd=c=>{const [y,m,d]=dtAdd(c.wk,7).split("-").map(Number);return`${d} ${DT_MON[m-1]}`;};   // the case closes by itself that Wednesday morning
// migration of saves from the Monday rhythm: a Monday key K → the Wednesday K+2 (the case opened on Monday 5 Oct 2026 lives
// on until Wednesday 14 Oct 6:00 and no second case opens on 7 Oct); keys only grow, so «<» compares weeks
function dtMig(){const m=dt();if(m.v===2)return;const f=k=>{if(typeof k!=="string"||!/^\d{4}-\d\d-\d\d$/.test(k))return k;const [y,mo,d]=k.split("-").map(Number);return new Date(y,mo-1,d).getDay()===1?dtAdd(k,2):k;};
  m.wk=f(m.wk);if(m.c)m.c.wk=f(m.c.wk);for(const h of m.hist)h.wk=f(h.wk);m.v=2;save();}
const dtShuf=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
const dtG=s=>{const w=s.toLowerCase().replace(/[«»"]/g,"").split(/[\s]+/)[0]||"";
  if(/(ый|ий|ой)$/.test(w))return"m";if(/(ая|яя)$/.test(w))return"f";if(/(ое|ее)$/.test(w))return"n";if(/(ые|ие)$/.test(w))return"p";
  if(/[ая]$/.test(w))return"f";if(/[оеёэу]$/.test(w))return"n";if(/(си|дзи|ти|ри|ми|ни)$/.test(w))return"n";if(/[ыи]$/.test(w))return"p";return"m";};
const dtVerb=g=>({m:"пропал",f:"пропала",n:"пропало",p:"пропали"})[g]||"пропал";
const dtLow=s=>s.charAt(0).toLowerCase()+s.slice(1),dtCap=s=>s.charAt(0).toUpperCase()+s.slice(1);
const dtGuest=id=>GUESTS.find(g=>g.id===id)||{n:id,mon:"m_obake",h:320};
const dtKnown=id=>{const g=dtGuest(id);return !!(S.friends[id]&&S.friends[id].n>0)||ST.seen.includes(g.beast);};
const dtRm=id=>(ROOMS.find(r=>r.id===id)||{}).ru||id;
const dtFound=c=>c.clues.filter(q=>q.f).length,dtNeed=c=>3+c.wrong.length;

// ── hiding and ALWAYS putting back
function dtPickThing(){
  const pl=Object.keys(S.placed||{}).filter(id=>{const q=S.placed[id];return q&&DT_FROM[q.r]&&IT[id]&&!DT_SKIP.test(id)&&DMETA[id];});
  const m=dt(),nx=a=>a.length>1?a.filter(x=>(x.id||x)!==m.lastThing):a;
  if(pl.length){const id=pick(nx(pl)),q=S.placed[id];return{k:"placed",id,room:q.r,n:IT[id].n,g:dtG(IT[id].n),x:q.x,y:q.y,rec:Object.assign({},q)};}
  const dec=[];for(const room in DECOR){const sel=S.decor[room]||{};for(const slot of DECOR[room]){const id=sel[slot.k],it=slot.items.find(i=>i.id===id);if(it&&DT_DEC[id]&&DT_FROM[room])dec.push({k:"decor",id,room,slot:slot.k,n:DT_DEC[id][0],g:DT_DEC[id][1],x:it.x,y:it.y});}}
  if(dec.length)return pick(nx(dec));
  for(const [id,n,g] of DT_PROP){const P=PROPS.find(p=>p.id===id);if(P&&P.room!=="-dt")return{k:"prop",id,room:P.room,n,g,x:P.x,y:P.y};}
  return null;}
function dtHide(th){
  if(th.k==="placed"){if(S.placed[th.id])delete S.placed[th.id];}
  else if(th.k==="decor"){const D=S.decor[th.room];if(D&&D[th.slot]===th.id)delete D[th.slot];}
  else{const P=PROPS.find(p=>p.id===th.id);if(P)P.room="-dt";}}
function dtRestore(c){const th=c&&c.thing;if(!th||th.back)return;
  if(th.k==="placed"){if(!S.placed[th.id]&&th.rec){S.placed[th.id]=Object.assign({},th.rec);if(IT[th.id])loadItem(th.id);}}
  else if(th.k==="decor"){const D=S.decor[th.room]||(S.decor[th.room]={});if(!D[th.slot])D[th.slot]=th.id;}
  else{const P=PROPS.find(p=>p.id===th.id);if(P&&P.room==="-dt")P.room=th.room;}
  th.back=1;save();try{ui();}catch(e){}}
// boot: re-hide a prop (runtime only) or notice the player has put the thing back by hand; anything odd → restore
function dtCheck(){const m=dt(),c=m.c;if(!c)return;
  const ok=c.thing&&c.thing.id&&DT_TPL[c.id]&&Array.isArray(c.clues)&&Array.isArray(c.sus)&&Array.isArray(c.wrong)&&c.wk&&c.wk<=dtAdd(dtWk(),7);
  if(!ok){dtRestore(c);m.c=null;save();return;}
  const th=c.thing;if(th.back)return;
  if(th.k==="placed"&&S.placed[th.id])th.back=1;
  else if(th.k==="decor"&&(S.decor[th.room]||{})[th.slot]===th.id)th.back=1;
  else if(th.k==="prop")dtHide(th);}

// ── the weekly rhythm
function dtOpen(tplId){const m=dt(),th=dtPickThing();if(!th)return false;
  const known=Object.keys(DT_YK).filter(dtKnown);
  let pool=DT_IDS.filter(id=>known.includes(DT_TPL[id].cul));if(!pool.length)pool=DT_IDS.filter(id=>["kitsune","tanuki","kappa"].includes(DT_TPL[id].cul));
  const got=(S.ext.disc||{}).mystery||{},nl=pool.filter(id=>id!==m.last),fresh=nl.filter(id=>!got[id]);
  const id=tplId&&DT_TPL[tplId]?tplId:pick(fresh.length?fresh:nl.length?nl:pool),cul=DT_TPL[id].cul;
  const okY=y=>y!==cul&&(y!=="warashi"||QS.done||dtKnown(y));
  let dec=dtShuf(known.filter(okY));if(dec.length<2)dec=dec.concat(dtShuf(Object.keys(DT_YK).filter(y=>okY(y)&&!dec.includes(y))));dec=dec.slice(0,2);
  const cc=dtShuf(DT_YK[cul].cl),her=dec.map(y=>DT_YK[y].cl.find(p=>!DT_YK[cul].cl.includes(p))).find(Boolean)||"slick";
  const rooms=dtShuf(DT_HOUSE.filter(r=>!hk("tabLock",r)));
  const clue=(p,cul1,room)=>({p,cul:cul1,room,dx:pick(DT_SPOT[room])*Math.round(190+Math.random()*90),f:0,seen:0});
  const clues=dtShuf([[cc[0],1],[cc[1%cc.length],1],[her,0]]).map(([p,k],i)=>clue(p,k,rooms[i%rooms.length]));
  dtHide(th);rt.box={};m.lastThing=th.id;m.cases=(m.cases||0)+1;m.c={id,no:m.cases,wk:dtWk(),t:Date.now(),thing:th,sus:dtShuf([cul,...dec]),clues,wrong:[],talk:{},seen:0,toast:0,solved:0,al:Math.floor(Math.random()*2)};
  m.wk=dtWk();m.last=id;m.say=null;save();try{ui();}catch(e){}return true;}
function dtExtra(c){const cul=DT_TPL[c.id].cul,used=c.clues.filter(q=>q.cul).map(q=>q.p),left=DT_YK[cul].cl.filter(p=>!used.includes(p)),p=left[0]||DT_YK[cul].cl[c.wrong.length%DT_YK[cul].cl.length];
  const busy=c.clues.filter(q=>!q.f).map(q=>q.room),rooms=dtShuf(DT_HOUSE.filter(r=>!busy.includes(r)&&r!==S.room&&!hk("tabLock",r))),room=rooms[0]||"bedroom";
  const q={p,cul:1,room,dx:pick(DT_SPOT[room])*Math.round(190+Math.random()*90),f:0,seen:0,again:left.length?0:1};c.clues.push(q);return q;}
// the week turned with the case still open: the thing comes back by itself, with a note from the culprit
function dtSelf(c){const m=dt(),Y=dtGuest(DT_TPL[c.id].cul);dtRestore(c);
  m.hist.unshift({id:c.id,no:c.no,n:c.thing.n,how:"self",wk:c.wk});m.hist.length=Math.min(m.hist.length,12);
  m.msg=`Прошлое дело закрылось само: пропажа вернулась на место с запиской «Простите, это был${DT_YK[Y.id]&&DT_YK[Y.id].f?"а":""} я». Подпись — ${Y.n}.`;m.c=null;save();}
function dtRoll(){const m=dt(),wk=dtWk();
  if(m.c&&m.c.wk<wk&&!m.c.solved)dtSelf(m.c);
  if(m.c&&m.c.solved&&m.c.wk<wk)m.c=null;
  if(!m.wk&&!m.cases&&dtDow()>=5){m.wk=wk;save();return;}   // a brand-new detective on Monday/Tuesday waits for Wednesday
  if(!(m.wk>=wk)){m.wk=wk;if(!dtOpen())save();}}

// ── in the room: small painted tells on the floor, softly glinting; tap one to take it into the notebook
const dtOn=()=>{const c=dt().c;return c&&!c.solved;};
// Musya's floor line, taken once the camera has settled in the room (so clues don't slide with the parallax)
function dtLine(){const k=S.room+"|"+view.W+"x"+view.H,L=catLineY();if(rt.lyK!==k){if(now()-cam.trans<1.3)return L;rt.lyK=k;rt.ly=L;}return rt.ly;}
function dtPos(q,i){const mx=(view.W/2-BGM.dx)/BGM.k;return[visX(mx+(q.dx||220),80),dtLine()-12-(i%2)*12];}
function dtDrawClue(q,i,t){const r=DT_AT[q.p];if(!r||!rt.im)return;const [x,y]=dtPos(q,i),s=1.15,w=r[2]*s,h=r[3]*s;
  curRow=y;let [ax,ay]=imgToStage(x-w/2,y-h,CAT_D),[bx,by]=imgToStage(x+w/2,y,CAT_D);curRow=null;const W=bx-ax,H=by-ay,lo=by-(view.H-8);if(lo>0){ay-=lo;by-=lo;}
  const cx=(ax+bx)/2,cy=by-H*.4,br=.5+.5*Math.sin(t*2.2+i*1.7),R=W*.75;
  ctx.save();const g=ctx.createRadialGradient(cx,cy,0,cx,cy,R);g.addColorStop(0,`rgba(255,228,165,${.16+.16*br})`);g.addColorStop(1,"rgba(255,230,170,0)");
  ctx.fillStyle=g;ctx.beginPath();ctx.ellipse(cx,cy,R,R*.42,0,0,Math.PI*2);ctx.fill();
  ctx.drawImage(rt.im,r[0],r[1],r[2],r[3],ax,ay,W,H);ctx.globalCompositeOperation="lighter";ctx.globalAlpha=.2+.18*br;ctx.drawImage(rt.im,r[0],r[1],r[2],r[3],ax,ay,W,H);ctx.globalCompositeOperation="source-over";ctx.globalAlpha=1;
  const ph=(t*.45+i*.37)%1;if(ph<.22){const a=Math.sin(ph/.22*Math.PI),sx=ax+W*(.25+.5*((i*.61)%1)),sy=ay+H*.3,L=7*a*Math.max(.7,view.s||1);
    ctx.strokeStyle=`rgba(255,246,215,${.85*a})`;ctx.lineWidth=1.3;ctx.beginPath();ctx.moveTo(sx-L,sy);ctx.lineTo(sx+L,sy);ctx.moveTo(sx,sy-L);ctx.lineTo(sx,sy+L);ctx.stroke();}
  ctx.restore();const pad=16;rt.box[i]=[ax-pad,ay-pad-6,W+pad*2,H+pad*2+6];}
function dtDrawCul(t,front){const sc=rt.sc;if(!sc||S.room!==sc.room)return;const fy=sc.y>catLineY()+6;if(fy!==front)return;
  const a=Math.min(1,(t-sc.t0)/.7)*(sc.t1?Math.max(0,1-(t-sc.t1)/.9):1);if(sc.t1&&a<=0){rt.sc=null;return;}if(!sc.t1&&t-sc.t0>45)sc.t1=t;
  const bob=Math.sin(t*1.8)*4;curRow=sc.y;
  const [gx,gy]=imgToStage(sc.x,sc.y,CAT_D);ctx.save();ctx.globalAlpha=.35*a;ctx.fillStyle="#000";ctx.beginPath();ctx.ellipse(gx,gy,70*BGM.k,14*BGM.k,0,0,Math.PI*2);ctx.fill();ctx.restore();
  drawMon(sc.mon,sc.x,sc.y+bob*.2,sc.h,CAT_D,a,"b",0,sc.flip);curRow=null;}
hook("draw",(t,front)=>{if(scene.on)return;dtDrawCul(t,front);if(!dtOn())return;const c=dt().c,cl=catLineY()+6;
  c.clues.forEach((q,i)=>{if(q.f||q.room!==S.room)return;if((dtPos(q,i)[1]>cl)!==front)return;delete rt.box[i];dtDrawClue(q,i,t);});});
hook("hit",(x,y)=>{if(!dtOn()||scene.on)return false;const c=dt().c;
  for(let i=0;i<c.clues.length;i++){const q=c.clues[i],b=rt.box[i];if(q.f||q.room!==S.room||!b)continue;if(x>=b[0]&&x<=b[0]+b[2]&&y>=b[1]&&y<=b[1]+b[3]){dtFind(i,x,y);return true;}}return false;});
function dtFind(i,x,y){const c=dt().c,q=c.clues[i];if(!q||q.f)return;q.f=1;q.seen=0;delete rt.box[i];const t=now();
  if(x!=null)floatFx.push({g:"🔍",x,y:y-10,t});sfx("pop");setTimeout(()=>chime([660,880]),180);
  if(!petAway()){react("🧐",1.8);S.needs.joy=clamp(S.needs.joy+3,0,100);}
  const f=dtFound(c),n=dtNeed(c);toast(f>=n?"🔍 Улики собраны — открой тетрадь в «家»":`🔍 Улика: ${dtLow(DT_CL[q.p][0])} (${f} из ${n})`);save();}
hook("room",id=>{rt.lyK="";if(!dtOn()||petAway())return;const c=dt().c;if(c.clues.some(q=>!q.f&&q.room===id))setTimeout(()=>{if(S.room===id&&pet.action!=="sleep")react("🧐",1.6);},1400);});

// ── the detective's notebook
document.head.insertAdjacentHTML("beforeend",`<style>
#xpBody .dt-c,#xpBody .dt-s{display:flex;gap:10px;align-items:center;margin:8px 0;padding:8px 10px;border-radius:12px;background:rgba(255,238,205,.05);border:1px solid rgba(255,228,190,.13)}
#xpBody .dt-c.off{opacity:.62;border-style:dashed}
#xpBody .dt-th{flex:0 0 78px;height:52px;display:flex;align-items:center;justify-content:center;filter:brightness(1.35)}
#xpBody .dt-q{font-size:26px;opacity:.55}
#xpBody .dt-c p.dt-t,#xpBody .dt-s p.dt-t,#xpBody .dt-say p.dt-t{margin:2px 0;font-size:13px;line-height:1.38}
#xpBody .dt-c p.dt-t i{opacity:.85}
#xpBody .dt-s img{flex:0 0 64px;height:86px;width:64px;object-fit:contain}
#xpBody .dt-s.no{opacity:.5}
#xpBody .dt-s .row{margin-top:6px}
#xpBody .dt-say{display:flex;gap:10px;align-items:center;padding:8px 10px;border-radius:12px;background:rgba(160,40,30,.16);border:1px solid rgba(230,120,90,.3);margin:8px 0}
#xpBody .dt-say img{height:64px;width:48px;object-fit:contain}
#xpBody .dt-tip{font-size:12.5px;opacity:.75;margin:4px 0 10px}
</style>`);
function dtThumb(p,mw,mh){const r=DT_AT[p];if(!r)return"";const f=Math.min(mw/r[2],mh/r[3],1),q=v=>Math.round(v*f);
  return`<span style="display:inline-block;width:${q(r[2])}px;height:${q(r[3])}px;background:url(assets/items/atlas_dt.webp) -${q(r[0])}px -${q(r[1])}px/${q(1024)}px ${q(350)}px no-repeat"></span>`;}
const dtMonImg=(id,h)=>`<img src="assets/mon/${dtGuest(id).mon}.webp" alt="" style="height:${h}px">`;
function dtNb(){const m=dt(),c=m.c;if(!c){openPanel("Тетрадь сыщика",`<p class="lead">${m.msg||"Тихая неделя: в доме всё на месте."} Новое дело — в среду.</p>`+dtCases(),"dt");return;}
  c.seen=1;c.clues.forEach(q=>{if(q.f)q.seen=1;});save();hubDot();tabDots();
  const T=DT_TPL[c.id],th=c.thing,f=dtFound(c),n=dtNeed(c),can=!c.solved&&f>=n,thumb=th.k==="placed"&&IT[th.id]?`<div style="float:right;margin:0 0 6px 8px">${itemThumb(IT[th.id],64,56)}</div>`:"";
  let h=`<p class="lead">${thumb}Дело № ${c.no}. ${dtCap(DT_IN[th.room]||"")} ${dtVerb(th.g)} ${dtLow(th.n)}. Найди улики, расспроси подозреваемых и назови виновного.</p>`+
    `<p class="dt-tip">Свежие улики виновный оставил этой ночью. Старые — давний след кого-то другого. Если не раскрыть дело до утра среды, ${dtEnd(c)}, пропажа вернётся сама.</p>`;
  if(m.say&&!c.solved)h+=`<div class="dt-say">${dtMonImg(m.say.id,64)}<div><b>${dtGuest(m.say.id).n}</b><p class="dt-t">«${m.say.t}»</p><p class="dt-t" style="opacity:.8">Улика: появилась ещё одна — ${DT_IN[m.say.room]||""}.</p></div></div>`;
  h+=`<h4 class="bh">Улики · ${f} из ${n}</h4>`+c.clues.map(q=>q.f?`<div class="dt-c"><div class="dt-th">${dtThumb(q.p,76,50)}</div><div><b>${DT_CL[q.p][0]}</b> <span style="opacity:.65">· ${dtRm(q.room)}</span><p class="dt-t">${q.again?"Ещё одна такая же. ":""}${DT_CL[q.p][1]} <i>${DT_CL[q.p][q.cul?2:3]}</i></p></div></div>`
    :`<div class="dt-c off"><div class="dt-th"><span class="dt-q">?</span></div><div><b>Улика ещё не найдена</b><p class="dt-t">Ищи ${DT_IN[q.room]} — Муся чует её носом.</p><div class="row"><button class="btn" data-x="dt:go:${q.room}">Пойти туда</button></div></div></div>`).join("");
  h+=`<h4 class="bh">Подозреваемые</h4>`+c.sus.map(id=>{const Y=dtGuest(id),no=c.wrong.includes(id),said=c.talk[id],al=id===T.cul?T.al:DT_YK[id].al[(c.al+c.sus.indexOf(id))%2];
    return`<div class="dt-s${no?" no":""}">${dtMonImg(id,86)}<div style="flex:1"><b>${Y.n}</b>${no?` <span style="opacity:.8">· обиделся${DT_YK[id].f?"а":""}</span>`:""}<p class="dt-t">${said?"«"+al+"»":"Пока не расспрошен"+(DT_YK[id].f?"а":"")+"."}</p>`+
      (c.solved||no?"":`<div class="row">${said?"":`<button class="btn" data-x="dt:talk:${id}">Расспросить</button>`}<button class="btn${can?" primary":""}" data-x="dt:acc:${id}"${can?"":" disabled"}>Обвинить</button></div>`)+`</div></div>`;}).join("");
  if(!can&&!c.solved)h+=`<p class="dt-tip">Назвать виновного можно, когда найдены все улики (${f} из ${n}).</p>`;
  openPanel("Тетрадь сыщика · "+T.t.replace("Дело ","дело "),h+dtCases(),"dt");}
function dtCases(){const m=dt(),got=(S.ext.disc||{}).mystery||{};if(!m.hist.length)return"";
  return`<h4 class="bh">Раскрытые дела · ${Object.keys(got).length} из ${DT_IDS.length}</h4>`+m.hist.slice(0,8).map(e=>`<p class="dt-t" style="margin:3px 0">№ ${e.no} · ${DT_TPL[e.id]?DT_TPL[e.id].t:""} — ${e.how==="self"?"вещь вернулась сама":"раскрыто"+(e.clean?" без ошибок":"")} <span style="opacity:.6">(${dtLow(e.n)})</span></p>`).join("");}
function dtAccuse(id){const m=dt(),c=m.c;if(!c||c.solved||c.wrong.includes(id)||dtFound(c)<dtNeed(c))return;
  if(id===DT_TPL[c.id].cul){dtSolve();return;}
  c.wrong.push(id);const q=dtExtra(c);m.say={id,t:DT_YK[id].off,room:q.room};sfx("bad");save();dtNb();$("xpBody").scrollTop=0;}
function dtSolve(){const m=dt(),c=m.c,T=DT_TPL[c.id],Y=dtGuest(T.cul),th=c.thing;c.solved=1;m.n++;m.say=null;
  const clean=!c.wrong.length;if(clean)m.clean=(m.clean||0)+1;
  m.hist.unshift({id:c.id,no:c.no,n:th.n,how:"solved",clean,wk:c.wk});m.hist.length=Math.min(m.hist.length,12);
  const rew=DT_REW.find(i=>!S.owned.has(i));if(rew)S.owned.add(rew);m.msg="";
  disc("mystery",c.id);save();closePanel();
  const go=()=>{dtRestore(c);const mx=(view.W/2-BGM.dx)/BGM.k,sd=(DT_SPOT[th.room]||[1])[0],fx=visX(mx+sd*380,120),fy=catLineY()-4;
    rt.sc={room:th.room,mon:Y.mon,x:fx,y:fy,h:Y.h||330,t0:now(),t1:0,flip:sd>0};
    const [px,py]=imgToStage(fx,fy-(Y.h||330)*.55,CAT_D);floatFx.push({g:"✨",x:px,y:py,t:now()+.5},{g:"🔍",x:px+18,y:py+20,t:now()+.8});
    if(!petAway()){pointer.x=px;pointer.y=py;pointer.known=true;pet.gazeUntil=now()+8;react("🙀",1.4);}
    setTimeout(()=>{chime([523,659,784]);dlg({head:Y.n+" · "+T.t,text:"«"+T.why.replace("{n}",dtCap(th.n))+"»",img:dtMonImg(T.cul,64),ok:"Дело закрыто 🔍",onOk:()=>{
      if(rt.sc)rt.sc.t1=now();if(!petAway()){react("😻",2.2);burst(8);S.needs.joy=clamp(S.needs.joy+10,0,100);}
      toast(rew?`🔍 Награда: ${IT[rew].n} — в 🧺 Вещах`:"🔍 Дело раскрыто! Муся гордится собой");
      setTimeout(()=>{award("dt_first");if(clean)award("dt_clean");if(m.n>=5)award("dt_five");},1800);save();}});},900);};
  if(S.room!==th.room&&DT_FROM[th.room]){goRoom(th.room);setTimeout(go,400);}else go();}

// ── hub, dots, tray, clicks, album, «while you were away»
hook("hub",()=>{dtRoll();const m=dt(),c=m.c;let st,more;
  if(c&&!c.solved){const f=dtFound(c),n=dtNeed(c),th=c.thing;
    st=`🔍 ${dtCap(dtVerb(th.g))} ${dtLow(th.n)} ${DT_FROM[th.room]||""} · ${f>=n?"пора назвать виновного":"улики "+f+" из "+n}`;   // the folded card shows ~50 chars
    more=`Дело недели. Подозреваемые: ${c.sus.map(id=>dtGuest(id).n).join(", ")}. Не раскроешь до утра среды, ${dtEnd(c)}, — пропажа вернётся сама.`;}
  else{const w=today().getDay()===DT_WD&&hourNow()<6;st=w?"Тихо… Утром в доме что-то пропадёт":c&&c.solved?"Дело недели раскрыто — новое в среду":"Тихо… Новое дело — в среду";
    more=(m.msg?m.msg+" ":"")+`Раскрыто дел: ${m.n}. Награды — в «🧺 Вещи» → ${DT_CAT}.`;}
  return`<div class="hubc"><h4>🔍 Пропажа в доме <i>探偵</i></h4><p>${st}</p><p style="opacity:.75;margin:6px 0 0">${more}</p><div class="row"><button class="btn${c&&!c.solved?" primary":""}" data-x="dt:nb">Тетрадь сыщика</button></div></div>`;});
hook("hubDot",()=>{const c=dt().c;return !!c&&!c.solved&&(!c.seen||c.clues.some(q=>q.f&&!q.seen));});
hook("tabDot",r=>{const c=dt().c;return !!c&&!c.solved&&c.clues.some(q=>!q.f&&q.room===r);});
hook("tray",(el)=>{const c=dt().c;if(!c||c.solved||c.thing.k!=="placed"||c.thing.back)return;const b=el.querySelector(`[data-item="${c.thing.id}"]`);if(!b)return;
  b.removeAttribute("data-item");b.dataset.x="dt:gone";b.classList.remove("on");const pr=b.querySelector(".pr");if(pr)pr.textContent="пропажа 🔍";});
hook("click",k=>{if(!k.startsWith("dt:"))return false;const a=k.split(":");
  if(a[1]==="nb")dtNb();
  else if(a[1]==="gone")toast("🔍 Её кто-то унёс — тетрадь сыщика в «家»");
  else if(a[1]==="go"){closePanel();goRoom(a[2]);}
  else if(a[1]==="talk"){const c=dt().c;if(c){c.talk[a[2]]=1;tone(520,.08,"sine",.03);save();dtNb();}}
  else if(a[1]==="acc")dtAccuse(a[2]);return true;});
hook("sec",()=>{dtRoll();const c=dt().c;if(!c||c.toast||c.solved||scene.on||overlaysOpen()||document.hidden||now()<6)return;if($("toast").classList.contains("on"))return;
  const th=c.thing,s=`🔍 ${dtCap(DT_FROM[th.room]||"")} ${dtVerb(th.g)} ${dtLow(th.n)}!`;toast(s.length<=46?s:`🔍 Пропажа ${DT_IN[th.room]||"в доме"}!`);c.toast=1;save();});
hook("away",()=>{const c=dt().c;if(!c||c.solved||!saved.t||c.t<saved.t)return null;return{i:"🔍",t:`${dtCap(DT_FROM[c.thing.room]||"")} ${dtVerb(c.thing.g)} ${dtLow(c.thing.n)}. Кто-то оставил следы…`};});
hook("album",el=>{const got=(S.ext.disc||{}).mystery||{};el.insertAdjacentHTML("beforeend",`<h3 class="bh">🔍 Дела сыщика · ${Object.keys(got).length} из ${DT_IDS.length}</h3><p class="lead">${DT_IDS.map(id=>got[id]?DT_TPL[id].t:"Дело ???").join(" · ")}</p>`);});
hook("boot",()=>{atlasImg("dt",im=>rt.im=im);dtMig();dtCheck();dtRoll();});

// test handles
X.mystery={st:dt,rt,wk:dtWk,tpl:DT_TPL,yk:DT_YK,name:id=>(DT_TPL[id]||{}).t||"",mig:dtMig,dow:dtDow,roll:dtRoll,nb:dtNb,accuse:dtAccuse,restore:()=>dtRestore(dt().c),
  force(id){const m=dt();if(m.c&&!m.c.solved)dtRestore(m.c);m.c=null;m.wk="";m.last="";return dtOpen(id);},
  find(i){dtFind(i);},
  here(){const c=dt().c;if(!c)return;const q=c.clues.find(q=>!q.f);if(q)goRoom(q.room);return q&&q.room;},
  tap(){const c=dt().c;for(let i=0;i<c.clues.length;i++){const q=c.clues[i],b=rt.box[i];if(!q.f&&q.room===S.room&&b)return hk("hit",b[0]+b[2]/2,b[1]+b[3]/2);}return"no box";}};
}
