{
// ───────────────────────── «Кошки соседей»: 8 ordinary neighbour cats visit the garden wall, the onsen fence and the torii by schedule ─────────────────────────
// S.ext.cats = {c:{id:{met:ms first acquaintance, fr:0..5 friendship, fed:dayKey of the last fish, seen:dayKey greeted, down:dayKey came down to Musya}}}
// atlas nk: per cat sit / ear (ear flicked) / lie / w0,w1 (walk) / tail — [x,y,w,h,[[eye x,y,rx,ry]…],tail root?]; atlas nk2: the gifts
const NK_F={"daifuku_sit":[0,0,120,150,[[51.3,61.2,5.5,4.6],[68.7,61.2,5.5,4.6]]],"daifuku_ear":[122,0,120,150,[[51.3,61.2,5.5,4.6],[68.7,61.2,5.5,4.6]]],"daifuku_lie":[244,0,168,96,[[107.4,45.2,5.2,4.4],[124.1,45.2,5.2,4.4]],[22,89]],"daifuku_w0":[414,0,176,124,[[140.4,38.1,4.9,4.1],[156.2,38.1,4.9,4.1]]],"daifuku_w1":[592,0,176,124,[[140.4,38.1,4.9,4.1],[156.2,38.1,4.9,4.1]]],"daifuku_tail":[770,0,34,112,[]],"mike_sit":[0,152,120,150,[[52.0,68.6,5.0,4.2],[68.0,68.6,5.0,4.2]]],"mike_ear":[122,152,120,150,[[52.0,68.6,5.0,4.2],[68.0,68.6,5.0,4.2]]],"mike_lie":[244,152,168,96,[[99.7,58.6,4.8,4.0],[114.9,58.6,4.8,4.0]],[22,89]],"mike_w0":[414,152,176,124,[[131.4,54.4,4.5,3.8],[145.8,54.4,4.5,3.8]]],"mike_w1":[592,152,176,124,[[131.4,54.4,4.5,3.8],[145.8,54.4,4.5,3.8]]],"mike_tail":[770,152,34,112,[]],"sumimi_sit":[0,304,120,150,[[51.6,64.5,5.2,4.4],[68.4,64.5,5.2,4.4]]],"sumimi_ear":[122,304,120,150,[[51.6,64.5,5.2,4.4],[68.4,64.5,5.2,4.4]]],"sumimi_lie":[244,304,168,96,[[104.0,58.0,5.0,4.2],[120.0,58.0,5.0,4.2]],[22,89]],"sumimi_w0":[414,304,176,124,[[136.4,52.1,4.8,4.0],[151.6,52.1,4.8,4.0]]],"sumimi_w1":[592,304,176,124,[[136.4,52.1,4.8,4.0],[151.6,52.1,4.8,4.0]]],"sumimi_tail":[770,304,34,112,[]],"yuki_sit":[0,456,120,150,[[51.8,66.1,5.1,4.3],[68.2,66.1,5.1,4.3]]],"yuki_ear":[122,456,120,150,[[51.8,66.1,5.1,4.3],[68.2,66.1,5.1,4.3]]],"yuki_lie":[244,456,168,96,[[102.3,55.1,4.9,4.1],[118.0,55.1,4.9,4.1]],[22,89]],"yuki_w0":[414,456,176,124,[[134.4,50.0,4.7,3.9],[149.3,50.0,4.7,3.9]]],"yuki_w1":[592,456,176,124,[[134.4,50.0,4.7,3.9],[149.3,50.0,4.7,3.9]]],"yuki_tail":[770,456,34,112,[]],"tora_sit":[0,608,120,150,[[51.1,59.5,5.6,4.7],[68.9,59.5,5.6,4.7]]],"tora_ear":[122,608,120,150,[[51.1,59.5,5.6,4.7],[68.9,59.5,5.6,4.7]]],"tora_lie":[244,608,168,96,[[109.2,51.4,5.3,4.5],[126.1,51.4,5.3,4.5]],[22,89]],"tora_w0":[414,608,176,124,[[142.4,43.5,5.0,4.2],[158.5,43.5,5.0,4.2]]],"tora_w1":[592,608,176,124,[[142.4,43.5,5.0,4.2],[158.5,43.5,5.0,4.2]]],"tora_tail":[770,608,34,112,[]],"kinako_sit":[0,760,120,150,[[51.8,66.1,5.1,4.3],[68.2,66.1,5.1,4.3]]],"kinako_ear":[122,760,120,150,[[51.8,66.1,5.1,4.3],[68.2,66.1,5.1,4.3]]],"kinako_lie":[244,760,168,96,[[102.3,61.1,4.9,4.1],[118.0,61.1,4.9,4.1]],[22,89]],"kinako_w0":[414,760,176,124,[[134.4,55.9,4.7,3.9],[149.3,55.9,4.7,3.9]]],"kinako_w1":[592,760,176,124,[[134.4,55.9,4.7,3.9],[149.3,55.9,4.7,3.9]]],"kinako_tail":[770,760,34,112,[]],"pochi_sit":[0,912,120,150,[[51.8,66.1,5.1,4.3],[68.2,66.1,5.1,4.3]]],"pochi_ear":[122,912,120,150,[[51.8,66.1,5.1,4.3],[68.2,66.1,5.1,4.3]]],"pochi_lie":[244,912,168,96,[[102.3,57.5,4.9,4.1],[118.0,57.5,4.9,4.1]],[22,89]],"pochi_w0":[414,912,176,124,[[134.4,52.3,4.7,3.9],[149.3,52.3,4.7,3.9]]],"pochi_w1":[592,912,176,124,[[134.4,52.3,4.7,3.9],[149.3,52.3,4.7,3.9]]],"pochi_tail":[770,912,34,112,[]],"maru_sit":[0,1064,120,150,[[52.9,80.5,4.4,4.4],[67.1,80.5,4.4,4.4]]],"maru_ear":[122,1064,120,150,[[52.9,80.5,4.4,4.4],[67.1,80.5,4.4,4.4]]],"maru_lie":[244,1064,168,96,[[86.8,66.5,4.0,4.0],[99.6,66.5,4.0,4.0]],[22,89]],"maru_w0":[414,1064,176,124,[[116.3,67.3,3.8,3.8],[128.5,67.3,3.8,3.8]]],"maru_w1":[592,1064,176,124,[[116.3,67.3,3.8,3.8],[128.5,67.3,3.8,3.8]]],"maru_tail":[770,1064,34,112,[]]};
const NK_G={"nk_shell":[0,0,110,76],"nk_ribbon":[112,0,124,84],"nk_cap":[238,0,84,60],"nk_feather":[324,0,60,196],"nk_omamori":[386,0,76,120],"nk_bag":[464,0,104,130],"nk_leaf":[570,0,110,110],"nk_yarn":[682,0,100,92]};
const NK_A={nk:[806, 1216],nk2:[784, 196]},NK_C="Подарки соседских кошек";
// spots: room, depth, edge line (image y for x), the free strip, frame px → image px, where (for texts)
const NK_SP={
 wall:{room:"engawa",d:.2,y:()=>521,x0:965,x1:1180,f:.95,at:"на стене сада у веранды",go:"на стену сада у веранды"},
 fence:{room:"onsen",d:.28,y:()=>760,x0:430,x1:1370,f:.95,at:"на заборе у онсэна",go:"на забор у онсэна"},
 torii:{room:"entrance",d:.38,y:x=>357+3.33e-4*(x-900)**2,x0:540,x1:1260,f:.88,at:"на тории у входа",go:"на тории у входа"}};
const NK_DOW=["вс","пн","вт","ср","чт","пт","сб"],NK_DOWF=["в воскресенье","в понедельник","во вторник","в среду","в четверг","в пятницу","в субботу"];
// the cats: who owns them, schedule (days of week 0=Sun, hours [from,to)), spot, home x, idle pose, walker, gift, Musya's face, lines by friendship
const NK=[
 {id:"daifuku",n:"Дайфуку",jp:"大福",sex:1,who:"Кот булочника Окады из пекарни через дорогу",sp:"wall",x:1075,pose:"lie",d:[1,3,5],h:[11,13],dry:1,gift:"nk_bag",mf:"😺",
  hint:"пн, ср, пт с 11 до 13 — в обед пекарни; в дождь сидит дома",
  desc:"Рыжий толстяк, круглый, как пирожок, в честь которого его назвали. От него пахнет тёплым хлебом.",
  L:["Дайфуку лежит буханкой и даже не смотрит в вашу сторону. Ему лень.","Дайфуку приоткрывает один глаз и снова засыпает. Это почти приветствие.","Дайфуку зевает так широко, что видно все зубы, и сладко потягивается.","Дайфуку мурчит на всю улицу. Наверное, снится свежая выпечка.","Дайфуку перекатывается на спину и подставляет живот солнцу. Он вам доверяет."]},
 {id:"mike",n:"Микэ",jp:"三毛",sex:0,who:"Кошка храма на холме — её кормит старый каннуси",sp:"torii",x:930,pose:"sit",d:[0],h:[9,12],fest:[18,21],gift:"nk_omamori",mf:"😻",
  hint:"по воскресеньям с 9 до 12, а в праздники — вечером, с 18 до 21",
  desc:"Трёхцветная, с бубенчиком на красном шнурке. Говорят, трёхцветная кошка у ворот приносит удачу.",
  L:["Микэ сидит на тории ровно, как храмовая статуэтка, и смотрит поверх крыш.","Микэ медленно моргает вам — по-кошачьи это значит «здравствуй».","Микэ умывается, и бубенчик тихо звенит в такт.","Микэ вытягивает лапу к Мусе, будто благословляет.","Микэ щурится от удовольствия. Кажется, удача в доме теперь и правда своя."]},
 {id:"sumimi",n:"Сумими",jp:"墨",sex:1,who:"Кот старого каллиграфа с соседней улицы",sp:"fence",x:1040,pose:"sit",d:[0,1,2,3,4,5,6],h:[17,19],walk:1,gift:"nk_leaf",mf:"😺",
  hint:"каждый день в сумерки, с 17 до 19",
  desc:"Чёрный, как тушь, которой пишет его хозяин. Приходит только в сумерки и никогда не шумит.",
  L:["Сумими сидит неподвижно — в сумерках виден только жёлтый блеск глаз.","Сумими беззвучно переступает лапами и снова замирает.","Сумими долго смотрит на пар над онсэном, словно читает в нём иероглифы.","Сумими еле слышно мурлычет. Для него это целая речь.","Сумими сворачивается клубком — чёрной кляксой на заборе. Ему здесь спокойно."]},
 {id:"yuki",n:"Юки",jp:"雪",sex:0,who:"Кошка бабушки Ханы из дома с глицинией",sp:"wall",x:1100,pose:"lie",d:[2,4,6],h:[11,15],sun:1,gift:"nk_yarn",mf:"😺",
  hint:"вт, чт, сб с 11 до 15 — но только когда солнечно",
  desc:"Белая старушка с разными глазами: один голубой, другой золотой. Глуховата и больше всего на свете любит солнце.",
  L:["Юки греется на солнце и не слышит, как вы подходите.","Юки поворачивает ухо на звук — с опозданием, но вежливо.","Юки щурит разноцветные глаза и греет на стене старые косточки.","Юки дремлет, и во сне у неё подрагивают усы.","Юки медленно моргает обоими глазами — голубым и золотым. Теперь вы старые друзья."]},
 {id:"tora",n:"Тора",jp:"虎",sex:1,who:"Ничей. Живёт у рыбной лавки на углу, его подкармливает рыбник Гэн",sp:"fence",x:760,pose:"sit",d:[1,4,6],h:[6,9],walk:1,gift:"nk_feather",mf:"😾",crow:1,
  hint:"пн, чт, сб по утрам, с 6 до 9",
  desc:"Полосатый хулиган с рваным ухом. Каждое утро воюет с вороной за рыбьи головы — и не всегда побеждает.",
  L:["Тора смотрит на вас исподлобья: «чего надо?» — говорит весь его вид.","Тора дёргает рваным ухом и демонстративно отворачивается.","Тора следит за вороной на крыше и бьёт хвостом по забору.","Тора трётся щекой о столбик забора. Это он помечает вас как своих.","Тора громко урчит — хулиган, а мурчит, как котёнок."]},
 {id:"kinako",n:"Кинако",jp:"きなこ",sex:0,who:"Сиамская кошка хозяйки парикмахерской Мисаки-сан",sp:"fence",x:1180,pose:"sit",d:[0,3,5],h:[14,16],gift:"nk_ribbon",mf:"😺",
  hint:"ср, пт, вс с 14 до 16",
  desc:"Сиамская модница цвета соевой муки кинако: голубые глаза, тёмная мордочка и бант, который ей повязывают каждое утро.",
  L:["Кинако позирует на заборе и делает вид, что вас не замечает.","Кинако поправляет лапкой бант и смотрит, оценили ли вы.","Кинако разглядывает своё отражение в воде онсэна.","Кинако грациозно потягивается — совсем как балерина.","Кинако тянется к вам носиком. Это огромная честь."]},
 {id:"pochi",n:"Почи",jp:"ポチ",sex:1,who:"Дворовый кот — его кормит вся улица, а спит он у почты",sp:"torii",x:860,pose:"sit",d:[0,2,6],h:[20,23],walk:1,gift:"nk_cap",mf:"😺",
  hint:"вт, сб, вс вечером, с 20 до 23",
  desc:"Японский бобтейл: вместо хвоста — помпон. Обходит свои владения каждый вечер, как сторож.",
  L:["Почи обходит тории дозором и считает, всё ли на месте.","Почи вертит хвостом-помпоном — он в хорошем настроении.","Почи сидит на тории, как на сторожевой вышке.","Почи громко мяукает куда-то в темноту — кажется, рапортует.","Почи спрыгивает поближе и бодается лбом. Теперь вы его улица."]},
 {id:"maru",n:"Мару",jp:"丸",sex:1,who:"Котёнок-подросток из семьи почтальона Кэнты",sp:"wall",x:1010,pose:"sit",d:[0,3,6],h:[15,17],walk:1,gift:"nk_shell",mf:"😸",young:1,
  hint:"ср, сб, вс после обеда, с 15 до 17",
  desc:"Серый полосатый подросток с белыми носочками. Всё ему интересно, всего ему мало.",
  L:["Мару охотится на листок, который давно не шевелится.","Мару ловит собственный хвост и чуть не падает со стены.","Мару с любопытством разглядывает Мусю: кто это такой маленький?","Мару пытается мурчать басом, как взрослый. Выходит смешно.","Мару хочет играть с Мусей — и, кажется, Муся тоже."]}];
const NK_ID={};NK.forEach(c=>NK_ID[c.id]=c);
addItems([
 {id:"nk_bag",n:"Пакетик из пекарни",c:NK_C,w:104,h:130,a:"b",p:60,at:["nk2",464,0],src:"🐈 подарок кошки",hint:"Подарок рыжего Дайфуку — подружись с ним"},
 {id:"nk_omamori",n:"Амулет-омамори",c:NK_C,w:76,h:120,a:"b",p:120,at:["nk2",386,0],src:"🐈 подарок кошки",hint:"Подарок храмовой кошки Микэ — к удаче"},
 {id:"nk_leaf",n:"Кленовый лист",c:NK_C,w:110,h:110,a:"b",p:40,at:["nk2",570,0],src:"🐈 подарок кошки",hint:"Подарок чёрного Сумими — он приходит в сумерки"},
 {id:"nk_yarn",n:"Клубок бабушки Ханы",c:NK_C,w:100,h:92,a:"b",p:50,at:["nk2",682,0],src:"🐈 подарок кошки",hint:"Подарок белой Юки — она любит солнце"},
 {id:"nk_feather",n:"Перо вороны-соперницы",c:NK_C,w:60,h:196,a:"b",p:70,at:["nk2",324,0],src:"🐈 подарок кошки",hint:"Трофей полосатого Торы — подружись с хулиганом"},
 {id:"nk_ribbon",n:"Шёлковый бантик",c:NK_C,w:124,h:84,a:"b",p:80,at:["nk2",112,0],src:"🐈 подарок кошки",hint:"Подарок модницы Кинако"},
 {id:"nk_cap",n:"Крышечка от рамунэ",c:NK_C,w:84,h:60,a:"b",p:30,at:["nk2",238,0],src:"🐈 подарок кошки",hint:"Подарок дворового Почи"},
 {id:"nk_shell",n:"Шкурка цикады",c:NK_C,w:110,h:76,a:"b",p:40,at:["nk2",0,0],src:"🐈 подарок кошки",hint:"Подарок котёнка Мару — он охотится на всё подряд"}],{nk2:NK_A.nk2});
STAMPS.push(["nk_first","猫","Соседская кошка","Познакомиться с первой кошкой соседей"],["nk_all","隣","Вся улица","Познакомиться со всеми восемью кошками соседей"],["nk_best","友","Лучший друг","Подружиться с соседской кошкой до пяти сердечек"]);

const nkS=()=>S.ext.cats||(S.ext.cats={c:{}});
const nkC=id=>{const c=nkS().c;return c[id]||(c[id]={met:0,fr:0,fed:"",seen:"",down:""});};
const nkHash=s=>{let h=7;for(const ch of s)h=(h*31+ch.charCodeAt(0))>>>0;return h;};
const nkMetN=()=>NK.filter(c=>nkC(c.id).met).length;
const nkFish=()=>have("u_any");
let NK_IM=null,NK_IM2=null;const nkForce={};
function nkLoad(){if(!NK_IM)atlasImg("nk",im=>{NK_IM=im;nkLids();});if(!NK_IM2)atlasImg("nk2",im=>{NK_IM2=im;});}
// eyelid colours: sampled from the fur just above each eye (for blinking)
function nkLids(){try{const c=document.createElement("canvas");c.width=NK_A.nk[0];c.height=NK_A.nk[1];const g=c.getContext("2d",{willReadFrequently:true});g.drawImage(NK_IM,0,0);
  for(const k in NK_F){const r=NK_F[k];r.lid=r[4].map(([ex,ey,rx,ry])=>{const p=g.getImageData(Math.round(r[0]+ex),Math.round(r[1]+ey-ry*1.7),1,1).data;return p[3]>40?`rgb(${p[0]},${p[1]},${p[2]})`:"#777";});}}catch(e){}}
function nkSunny(){if(weather.on)return false;const w=X.wx&&X.wx.real&&X.wx.real();if(w)return w.code<=2;return nkHash(dayKey()+"sun")%3!==0;}
// is the cat visiting at hour h of weekday w (now: festival / weather apply)
function nkAt(c,w,h,live){if(nkForce[c.id])return true;const inH=r=>r&&h>=r[0]&&h<r[1];
  if(live&&c.fest&&festNow()&&inH(c.fest))return true;
  if(!c.d.includes(w)||!inH(c.h))return false;if(live&&c.dry&&weather.on)return false;if(live&&c.sun&&!nkSunny())return false;return true;}
const nkVis=c=>nkAt(c,today().getDay(),hourNow(),true);
const nkNowL=()=>NK.filter(nkVis);
// when does the cat come next (from now, up to a week ahead)
function nkNext(c){const d0=today(),h0=hourNow();for(let i=0;i<8;i++){const w=(d0.getDay()+i)%7;if(!c.d.includes(w))continue;const hs=c.h[0];if(i===0&&hs<=h0)continue;return{i,w,h:hs};}return null;}
function nkWhen(n){const hh=String(n.h).padStart(2,"0")+":00";return n.i===0?`сегодня в ${hh}`:n.i===1?`завтра в ${hh}`:`${NK_DOWF[n.w]} в ${hh}`;}
const nkName=c=>nkC(c.id).met?c.n:c.sex?"незнакомый кот":"незнакомая кошка";
const nkHearts=fr=>"♥".repeat(fr)+"♡".repeat(5-fr);
const nkGiftHere=c=>{const C=nkC(c.id);return C.fr>=3&&!S.owned.has(c.gift)&&nkHash(dayKey()+c.id)%3!==2;};

// ── runtime: cats present in the current room
const nkRT={};let nkReactAt=0,nkCrowT=0;
function nkSpawn(c,arrive){const sp=NK_SP[c.sp],t=now(),r={id:c.id,x:c.x,face:Math.random()<.5?1:-1,mode:c.pose,t0:t,nb:t+rand(2,5),ne:t+rand(3,8),na:t+rand(14,30),ph:rand(0,6),hop:0};
  if(arrive){const from=Math.random()<.5?sp.x0-80:sp.x1+80;r.x=from;r.tx=c.x;r.mode="walk";r.face=c.x>from?1:-1;}
  nkRT[c.id]=r;return r;}
function nkLeave(r){const sp=NK_SP[NK_ID[r.id].sp];r.leave=1;r.mode="walk";r.tx=r.x-sp.x0<sp.x1-r.x?sp.x0-90:sp.x1+90;r.face=r.tx>r.x?1:-1;}
function nkSync(arrive){const room=S.room;for(const c of NK){const vis=nkVis(c)&&NK_SP[c.sp].room===room,r=nkRT[c.id];
  if(vis&&!r)nkSpawn(c,arrive);else if(!vis&&r&&!r.leave&&r.mode!=="down"&&r.mode!=="jump")nkLeave(r);}}
function nkStep(t,dt){for(const id in nkRT){const r=nkRT[id],c=NK_ID[id];
  if(r.mode==="walk"){const v=(c.young?95:70)*dt;if(Math.abs(r.tx-r.x)<=v){r.x=r.tx;if(r.leave){delete nkRT[id];continue;}r.mode=c.pose;r.na=t+rand(14,30);}else r.x+=Math.sign(r.tx-r.x)*v;continue;}
  if(r.mode==="jump"){if(t-r.t0>=r.dur){r.mode=r.back?c.pose:"down";r.t0=t;if(!r.back){nkSeat(c);}}continue;}
  if(r.mode==="down"){if(t-r.t0>75||petAway()||pet.action==="sleep"){r.mode="jump";r.back=1;r.t0=t;r.dur=.9;}continue;}
  if(t>r.na){r.na=t+rand(16,34);const sp=NK_SP[c.sp];
    if(c.walk&&Math.random()<.55){r.tx=clamp(r.x+rand(-1,1)*320,sp.x0+30,sp.x1-30);if(Math.abs(r.tx-r.x)>40){r.mode="walk";r.face=r.tx>r.x?1:-1;}}
    else r.mode=r.mode==="sit"?"lie":"sit";}
  if(c.crow&&S.room==="onsen"&&t-nkCrowT>40&&Math.random()<.004){nkCrowT=t;nkCaw();r.hop=t;}}}
function nkCaw(){audioInit();for(const [a,b,d,at] of [[640,470,.32,0],[620,450,.34,.5]])setTimeout(()=>tone(a,d,"sawtooth",.02),at*1000);}

// ── geometry and drawing
const nkCv=document.createElement("canvas");nkCv.width=200;nkCv.height=160;const nkG=nkCv.getContext("2d");
function nkK(sp,x){const y=sp.y(x),a=imgToStage(x,y,sp.d),b=imgToStage(x+100,y,sp.d);return[a[0],a[1],(b[0]-a[0])/100];}
function nkTint(){const night=dayTint()[1];return[TINT[S.room]||"rgba(14,18,18,.28)",night?"rgba(10,14,30,.24)":null];}
// one frame (tinted, with a blink) → ctx at (x,y) = bottom anchor (ax,ay in frame px), size k = stage px per frame px
function nkSpr(key,x,y,k,flip,ax,ay,blink,al=1,rot=0){const r=NK_F[key];if(!NK_IM||!r)return null;const w=r[2],h=r[3];
  nkG.globalCompositeOperation="source-over";nkG.globalAlpha=1;nkG.clearRect(0,0,w+2,h+2);nkG.drawImage(NK_IM,r[0],r[1],w,h,0,0,w,h);
  if(blink&&r.lid)r[4].forEach(([ex,ey,rx,ry],i)=>{nkG.fillStyle=r.lid[i];nkG.beginPath();nkG.ellipse(ex,ey,rx*1.05,ry*1.1,0,0,7);nkG.fill();nkG.strokeStyle="rgba(30,22,20,.8)";nkG.lineWidth=.9;nkG.beginPath();nkG.ellipse(ex,ey+ry*.2,rx*.85,ry*.35,0,.15,Math.PI-.15);nkG.stroke();});
  nkG.globalCompositeOperation="source-atop";for(const f of nkTint())if(f){nkG.fillStyle=f;nkG.fillRect(0,0,w,h);}
  ctx.save();ctx.globalAlpha=al;ctx.translate(x,y);if(rot)ctx.rotate(rot);ctx.scale(flip?-k:k,k);ctx.drawImage(nkCv,0,0,w,h,-ax,-ay,w,h);ctx.restore();
  if(!blink&&!rot&&dayTint()[1]&&r[4].length){ctx.save();ctx.globalCompositeOperation="lighter";ctx.globalAlpha=al*.5;ctx.fillStyle="#d8e070";for(const [ex,ey,rx] of r[4]){ctx.beginPath();ctx.arc(x+(flip?-1:1)*(ex-ax)*k,y+(ey-ay)*k,Math.max(1,rx*k*.7),0,7);ctx.fill();}ctx.restore();}
  return[x-ax*k,y-ay*k,w*k,h*k];}
function nkTail(c,x,y,k,rot,al){const r=NK_F[c.id+"_tail"];if(!r)return;nkSpr(c.id+"_tail",x,y,k,false,r[2]/2,2,false,al,rot);}
function nkGiftDraw(c,x,y,k){const id=c.gift,r=NK_G[id];if(!NK_IM2||!r)return;const s=k*52/Math.max(r[2],r[3]);ctx.save();ctx.translate(x,y);if(r[3]>r[2]*1.5)ctx.rotate(-1.45);
  ctx.drawImage(NK_IM2,r[0],r[1],r[2],r[3],-r[2]*s/2,-r[3]*s,r[2]*s,r[3]*s);ctx.restore();if(Math.sin(now()*2.4+c.x)>.985&&Math.random()<.3)floatFx.push({g:"✨",x,y:y-14*k,t:now()});}
// next to Musya on the floor (best friends)
function nkFloor(c){const [ox,oy]=camOff(CAT_D),side=pet.x<view.W*.5?1:-1;return[pet.x+ox+side*120*view.s,view.floor+oy,175*view.s/150,side];}
function nkSeat(c){const C=nkC(c.id);C.down=dayKey();save();if(petAway()||pet.action==="sleep")return;setTimeout(()=>{if(!petAway())react(c.id==="tora"?"😼":"😻",2);},600);}
const nkBox={};
function nkDraw(t){for(const k in nkBox)delete nkBox[k];
  for(const id in nkRT){const r=nkRT[id],c=NK_ID[id],sp=NK_SP[c.sp];if(sp.room!==S.room)continue;
    const [sx,sy,ks]=nkK(sp,r.x),k=ks*sp.f,edge=Math.min(1,(r.x-sp.x0+60)/60,(sp.x1+60-r.x)/60),al=clamp(edge,0,1);if(al<=0)continue;
    const blink=t>r.nb&&t<r.nb+.16;if(t>r.nb+.16){r.nb=t+rand(2.5,6);}
    const ear=r.mode==="sit"&&t>r.ne&&t<r.ne+.28;if(t>r.ne+.28)r.ne=t+rand(4,9);
    const hop=r.hop&&t-r.hop<.5?Math.sin((t-r.hop)/.5*Math.PI)*10*k:0;
    if(r.mode==="down"||r.mode==="jump"){const [fx,fy,fk,side]=nkFloor(c);let x=fx,y=fy,kk=fk,u=1;
      if(r.mode==="jump"){u=clamp((t-r.t0)/r.dur,0,1);const e=r.back?1-u:u,ee=e*e*(3-2*e);x=mix(sx,fx,ee);y=mix(sy,fy,ee)-Math.sin(e*Math.PI)*90*view.s;kk=mix(k,fk,ee);
        nkBox[id]=nkSpr(c.id+"_w0",x,y,kk,r.back?sx<fx:fx<sx,88,121,false,1);continue;}
      ctx.save();ctx.globalAlpha=.3;ctx.fillStyle="#000";ctx.beginPath();ctx.ellipse(x,y+2*kk,46*kk,7*kk,0,0,7);ctx.fill();ctx.restore();
      nkTail(c,x+side*14*kk,y-6*kk,kk,-side*1.45+Math.sin(t*1.4+r.ph)*.1,1);
      nkBox[id]=nkSpr(c.id+"_sit",x,y,kk*(1+.01*Math.sin(t*2)),side<0,60,147,blink||(t+r.ph)%7<.6);continue;}
    if(r.mode==="walk"){const st=Math.floor(t*(c.young?6:4.5)+r.ph)%2,bob=Math.abs(Math.sin(t*4.5))*1.5*k;nkBox[id]=nkSpr(c.id+"_w"+st,sx,sy-bob-hop,k,r.face<0,88,121,false,al);continue;}
    const sw=Math.sin(t*1.25+r.ph)*.13+(c.crow&&hop?.4:0);
    if(r.mode==="lie"){const f=NK_F[c.id+"_lie"],fl=r.face<0,rx=(f[5][0]-84)*k*(fl?-1:1);nkTail(c,sx+rx,sy-4*k,k,sw*.8,al);
      nkBox[id]=nkSpr(c.id+"_lie",sx,sy-hop,k,fl,84,93,blink,al);}
    else{nkTail(c,sx+(r.face<0?-16:16)*k,sy-5*k,k,sw,al);nkBox[id]=nkSpr(c.id+(ear?"_ear":"_sit"),sx,sy-hop,k*(1+.008*Math.sin(t*2.1+r.ph)),r.face<0,60,147,blink,al);}
    if(nkGiftHere(c)&&r.mode!=="walk")nkGiftDraw(c,sx+(r.face<0?32:-34)*k,sy,k);}}
hook("draw",(t,front)=>{if(front||scene.on||!Object.keys(nkRT).length)return;nkLoad();nkDraw(t);});
hook("tick",(t,dt)=>{if(Object.keys(nkRT).length)nkStep(t,Math.min(dt,.1));});
hook("room",id=>{for(const k in nkRT)delete nkRT[k];if(Object.values(NK_SP).some(s=>s.room===id)){nkLoad();nkSync(false);if(Object.keys(nkRT).length)nkReactAt=now()+2.2;}});
hook("sec",()=>{if(scene.on)return;nkSync(true);
  if(nkReactAt&&now()>nkReactAt){nkReactAt=0;const r=Object.values(nkRT)[0];if(r)nkMusya(NK_ID[r.id],false);}
  for(const id in nkRT){const r=nkRT[id],c=NK_ID[id],C=nkC(id);if(C.fr>=5&&C.down!==dayKey()&&r.mode===c.pose&&!petAway()&&pet.action!=="sleep"&&!overlaysOpen()&&now()-r.t0>6&&pet.action==="idle"){r.mode="jump";r.back=0;r.t0=now();r.dur=.9;C.down=dayKey();save();break;}}});
// Musya looks at the cat: friendly ones get a slow blink, Tora a sulk, Mike delight
function nkMusya(c,fed){if(petAway()||pet.action==="sleep"||scene.on||S.room!==NK_SP[c.sp].room)return;const C=nkC(c.id),b=nkBox[c.id];
  if(b){pointer.x=b[0]+b[2]/2;pointer.y=b[1]+b[3]/2;pointer.known=true;pet.gazeUntil=now()+3;}
  const f=c.id==="tora"?"😾":c.id==="mike"?"😻":C.fr>=1||fed?(Math.random()<.5?"😌":"😺"):"😼";
  setTimeout(()=>{if(petAway())return;react(f,2);if(c.id==="tora"&&pet.action==="idle"&&Math.random()<.6)start("sulk");},400);}

// ── the card
function nkThumb(key,mw,mh,cls=""){const r=NK_F[key]||NK_G[key],A=NK_F[key]?NK_A.nk:NK_A.nk2,at=NK_F[key]?"nk":"nk2",k=Math.min(mw/r[2],mh/r[3]),f=v=>(v*k).toFixed(1);
  return`<span class="${cls}" style="display:inline-block;flex:none;width:${f(r[2])}px;height:${f(r[3])}px;background:url(assets/items/atlas_${at}.webp) -${f(r[0])}px -${f(r[1])}px/${f(A[0])}px ${f(A[1])}px no-repeat"></span>`;}
function nkCard(id){const c=NK_ID[id],C=nkC(id),dk=dayKey();audioInit();const first=!C.met;let pre="";
  if(first){C.met=Date.now();disc("cat",id);chime([880,1175,1568]);pre=`Познакомились! ${c.who}. ${c.desc} `;setTimeout(()=>{award("nk_first");if(nkMetN()>=NK.length)award("nk_all");},1800);}
  C.seen=dk;save();hubDot();tabDots();
  if(nkGiftHere(c)){S.owned.add(c.gift);save();setTimeout(()=>{chime([988,1318,1568]);toast(`🎁 ${IT[c.gift].n} — в «Вещах»`);},500);const gn=IT[c.gift].n;pre+=`${c.n} ${c.sex?"принёс":"принесла"} подарок: у ${c.sex?"его":"её"} лап лежит ${gn[0].toLowerCase()+gn.slice(1)}. `;}
  const line=c.L[Math.min(C.fr,c.L.length-1)],fish=nkFish(),fed=C.fed===dk,canFeed=fish>0&&!fed&&C.fr<5;
  const tail=C.fr>=5?"Лучшие друзья.":fed?`Сегодня ${c.n} уже угостили.`:fish?"":"Угостить нечем — рыбу можно наловить в пруду во дворике.";
  dlg({head:`${c.n} · ${c.jp}`,text:`${pre}${first?"":line+" "}Дружба: ${nkHearts(C.fr)}.${tail?" "+tail:""}`,img:nkThumb(id+"_sit",80,96),
    ok:canFeed?"🐟 Угостить рыбкой":"Хорошо",no:canFeed?"Пусть сидит":"",onOk:canFeed?()=>nkFeed(id):null});
  nkMusya(c,false);}
function nkFeed(id){const c=NK_ID[id],C=nkC(id);if(!take("u_any")){toast("🐟 Рыбы в кладовой нет");return;}C.fed=dayKey();C.fr=Math.min(5,C.fr+1);save();sfx("eat");
  const r=nkRT[id],b=nkBox[id];if(b)for(let i=0;i<3;i++)setTimeout(()=>floatFx.push({g:i?"♥":"🐟",x:b[0]+b[2]/2,y:b[1]+b[3]*.3,t:now()}),i*350);
  toast(C.fr>=5?`💞 ${c.n} теперь лучший друг Муси`:`🐟 ${c.n}: дружба ${C.fr} из 5`);nkMusya(c,true);
  if(C.fr===3)setTimeout(()=>toast(`🎁 ${c.n} будет приносить подарки`),2600);
  if(C.fr>=5){setTimeout(()=>award("nk_best"),2400);if(r&&r.mode===c.pose&&!petAway()){C.down=dayKey();save();setTimeout(()=>{if(nkRT[id]===r){r.mode="jump";r.back=0;r.t0=now();r.dur=.9;}},1200);}}}
function nkHit(x,y){let best=null,bd=1e9;for(const id in nkBox){const b=nkBox[id];if(!b)continue;const cx=b[0]+b[2]/2,cy=b[1]+b[3]*.55,hw=Math.max(30,b[2]*.4),hh=Math.max(30,b[3]*.5);
  if(Math.abs(x-cx)<hw&&Math.abs(y-cy)<hh){const d=Math.abs(x-cx)+Math.abs(y-cy);if(d<bd){bd=d;best=id;}}}return best;}
hook("hit",(x,y)=>{if(scene.on)return;const id=nkHit(x,y);if(!id)return;nkCard(id);return true;});

// ── hub, dots, album
function nkStatus(){const L=nkNowL();
  if(L.length)return L.map(c=>{const r=nkRT[c.id],sp=NK_SP[c.sp],nm=nkName(c);const m=r?r.mode:c.pose,v=m==="walk"?"гуляет":m==="lie"?"лежит":"сидит";
    return`${sp.at[0].toUpperCase()+sp.at.slice(1)} ${v} ${nm}`;}).join(". ")+".";
  let best=null;for(const c of NK){const n=nkNext(c);if(n&&(!best||n.i*24+n.h<best.n.i*24+best.n.h))best={c,n};}
  if(!best)return"Сегодня никто не придёт.";const c=best.c,met=nkC(c.id).met;
  return met?`${c.n} придёт ${nkWhen(best.n)} — ${NK_SP[c.sp].go}${c.sun?" (если будет солнце)":""}.`:`${nkWhen(best.n)[0].toUpperCase()+nkWhen(best.n).slice(1)} ${NK_SP[c.sp].go} заглянет ${c.sex?"незнакомый кот":"незнакомая кошка"}.`;}
hook("hub",()=>{const n=nkMetN(),L=nkNowL(),go=L[0]||null;
  return`<div class="hubc"><h4>🐈 Кошки соседей <i>近所の猫</i></h4><p>${nkStatus()}</p><p>Знакомых кошек: ${n} из ${NK.length}. Соседские кошки приходят по своему расписанию: на стену сада у веранды, на забор онсэна и на тории у входа. Нажми на кошку, чтобы познакомиться, а рыбкой из кладовой можно завоевать её дружбу.</p>
  ${n?`<div class="nk-row">${NK.filter(c=>nkC(c.id).met).map(c=>`<span>${nkThumb(c.id+"_sit",40,50)}<small>${c.n}<br>${nkHearts(nkC(c.id).fr)}</small></span>`).join("")}</div>`:""}
  <div class="row">${go?`<button class="btn primary" data-x="nk:go:${go.id}">Посмотреть</button>`:""}</div></div>`;});
hook("click",k=>{if(!k.startsWith("nk:"))return;const p=k.split(":");if(p[1]==="go"){const c=NK_ID[p[2]];closePanel();if(c&&S.room!==NK_SP[c.sp].room)goRoom(NK_SP[c.sp].room);}return true;});
hook("hubDot",()=>nkNowL().some(c=>nkC(c.id).seen!==dayKey()));
hook("tabDot",room=>nkNowL().some(c=>NK_SP[c.sp].room===room&&nkC(c.id).seen!==dayKey()));
hook("album",el=>{const n=nkMetN();
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Кошки соседей</h3><p class="lead">Знакомых кошек: ${n} из ${NK.length}. У каждой своё время: кто-то приходит по утрам, кто-то в сумерки, а кто-то только в солнечные дни.</p><div class="coll">${NK.map(c=>{const C=nkC(c.id),on=!!C.met;
    return`<div class="ci ${on?"on":""}">${nkThumb(c.id+"_sit",56,66,"ath")}<small>${on?`${c.n} · ${c.jp}<br>${nkHearts(C.fr)}<br>${c.hint}`:`???<br>${c.hint}<br>${NK_SP[c.sp].at}`}</small></div>`;}).join("")}</div>`);});
document.head.insertAdjacentHTML("beforeend","<style>.nk-row{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 4px}.nk-row>span{display:flex;flex-direction:column;align-items:center;gap:2px;width:62px}.nk-row small{font-size:10px;line-height:1.15;text-align:center;color:var(--muted)}</style>");
hook("boot",()=>{nkS();if(Object.values(NK_SP).some(s=>s.room===S.room)){nkLoad();nkSync(false);}});
// test handles
X.cats={st:nkS,rt:nkRT,box:nkBox,force(id,on=true,arr=false){if(on)nkForce[id]=1;else delete nkForce[id];nkSync(arr);},card:nkCard,feed:nkFeed,status:nkStatus,vis:nkVis,
  tap(id){const b=nkBox[id];if(!b)return"nobox";return hk("hit",b[0]+b[2]/2,b[1]+b[3]*.55)?"hit":"miss";},
  down(id){const r=nkRT[id];if(r){r.mode="jump";r.back=0;r.t0=now();r.dur=.9;}},sched:()=>NK.map(c=>c.id+":"+(nkNext(c)?nkWhen(nkNext(c)):"-")).join(" | ")};
}
