{
// ───────────────────────── Musya's birthday and «months together» ─────────────────────────
// S.ext.bd = {start:"YYYY-MM-DD" (the day Musya came; guessed from the save on first boot, the player can correct it),
//   auto:1 while guessed, done:{milestoneId:dayKey} parties held, toast:dayKey of the last «today is…» toast, log:[[id,dayKey,guests]]}
// Milestones: 7 days, every month (6 = half a year, 12 = birthday), 100 days. On the day the engawa is decorated; the strawberry
// cake fed to Musya starts a one-chapter party scene with the yōkai the player knows; rewards: a thing, a stamp, disc("birthday",id).
const B=S.ext.bd||(S.ext.bd={start:null,auto:1,done:{},toast:null,log:[]});B.done=B.done||{};B.log=B.log||[];
const BDA={gar:[0,0,440,120],ban:[444,0,560,132],bon:[1008,0,100,230]};   // decor rects in assets/items/atlas_bd.webp (art/birthday_art.py)
FATL.bd={w:1180,h:638,r:{ds_bd_cake:[0,498,180,140],ds_bd_sekihan:[184,498,170,130]}};
FOOD.ds_bd_cake={n:"Торт с клубникой",k:"dish",food:30,joy:30};FOOD.ds_bd_sekihan={n:"Сэкихан",k:"dish",food:32,joy:16};
RECIPES.push(
 {id:"bd_cake",dish:"ds_bd_cake",n:"Торт с клубникой",jp:"いちごのケーキ",lore:"В Японии на день рождения пекут «шорткейк»: нежный бисквит, взбитые сливки и целые клубничины сверху. Его режут на всех, кто пришёл поздравить.",
  need:["i_egg","i_sugar","i_flour","v_ichigo"],steps:[{k:"add",it:["i_egg","i_sugar","i_flour"]},{k:"stir",n:3},{k:"heat",n:2,lb:"Вынь бисквит"},{k:"chop",it:"v_ichigo",n:3},{k:"add",it:["v_ichigo"]}]},
 {id:"bd_sekihan",dish:"ds_bd_sekihan",n:"Сэкихан",jp:"赤飯",lore:"Клейкий рис, сваренный с красными бобами адзуки. Его готовят на праздники — дни рождения, свадьбы, первый шаг малыша: красный цвет отгоняет беду.",
  need:["i_mochigome","i_azuki"],steps:[{k:"add",it:["i_azuki"]},{k:"heat",n:2,lb:"Отвари бобы"},{k:"add",it:["i_mochigome"]},{k:"stir",n:2},{k:"shape",n:2,pic:"ds_bd_sekihan"}]});
const BDC="Праздники Муси",bdIt=(id,n,r,a,hint)=>({id,n,c:BDC,w:r[2],h:r[3],a,p:0,at:["bd",r[0],r[1]],src:"🎂 праздник",hint});
addItems([
 bdIt("bd_frame","Рамка «Неделя вместе»",[0,234,170,190],"b","Неделя с Мусей: угости её тортом в тот день"),
 bdIt("bd_ribbon","Лента «Месяц вместе»",[174,234,160,170],"b","Месяц с Мусей: угости её тортом в тот день"),
 bdIt("bd_bonbori","Бонбори «Месяцы вместе»",BDA.bon,"b","2 месяца с Мусей: торт в день праздника"),
 bdIt("bd_fan","Веер «100 дней»",[338,234,220,170],"b","100 дней с Мусей: торт в день праздника"),
 bdIt("bd_kusudama","Кусудама «Полгода»",[562,234,150,260],"t","Полгода с Мусей: торт в день праздника"),
 bdIt("bd_cakefig","Торт «Год вместе»",[716,234,220,230],"b","День рождения Муси: торт и гости"),
 bdIt("bd_maneki","Манэки-нэко «Ещё год»",[940,234,160,210],"b","Второй день рождения Муси: торт и гости")],{bd:[1180,638]});
STAMPS.push(["bd_week","週","Неделя вместе","Отпразднуй с Мусей первую неделю"],["bd_month","月","Месяц вместе","Отпразднуй с Мусей первый месяц"],
 ["bd_100","百","Сто дней","Отпразднуй сто дней вместе"],["bd_year","誕","День рождения","Отпразднуй день рождения Муси"]);
document.head.insertAdjacentHTML("beforeend",`<style>.bd-big{font-size:17px;margin:2px 0 8px}.bd-big b{color:var(--sakura)}.bd-now{color:#f3d9a0}
.bd-l{display:flex;flex-direction:column;gap:5px;margin:12px 0 2px;font-size:13px;opacity:.9}.bd-l input{max-width:210px;background:#15120f;color:#efe3c8;border:1px solid var(--line);border-radius:9px;padding:7px 9px;font:inherit;color-scheme:dark}
.bd-log{font-size:12.5px;opacity:.75;margin:8px 0 0}</style>`);

// ── dates ──
const pl=(n,a,b,c)=>{const m=n%10,h=n%100;return m===1&&h!==11?a:m>=2&&m<=4&&(h<12||h>14)?b:c;};
const dOf=k=>{const [y,m,d]=k.split("-").map(Number);return new Date(y,m-1,d);};
const d0=d=>new Date(d.getFullYear(),d.getMonth(),d.getDate());
const bdStart=()=>dOf(B.start||dayKey()),bdDiff=(s,d)=>Math.round((d0(d)-d0(s))/864e5);
const fmt=d=>d.toLocaleDateString("ru-RU",d.getFullYear()===today().getFullYear()?{day:"numeric",month:"long"}:{day:"numeric",month:"long",year:"numeric"});
// the earliest trace of the player in the save: discoveries, candles, visitors, festivals, the sakura
function bdGuess(){let m=Date.now();const lo=v=>{if(v>1e12&&v<m)m=v;};
  const D=S.ext.disc||{};for(const k in D)for(const i in D[k])lo(D[k][i]);
  for(const e of (S.ext.candles&&S.ext.candles.log)||[])lo(e[1]);
  const V=S.ext.vis&&S.ext.vis.m;if(V)for(const i in V)lo(V[i].met);
  for(const k in S.fest||{}){const i=k.lastIndexOf("-"),F=FEST.find(f=>f.id===k.slice(0,i)),y=+k.slice(i+1);if(!F||!y)continue;
    lo(new Date(y+(F.to[0]*100+F.to[1]<F.from[0]*100+F.from[1]?1:0),F.to[0]-1,F.to[1]).getTime());}
  const tr=S.ext.tree;if(tr&&/^\d{4}-\d\d-\d\d$/.test(tr.pl||""))lo(dOf(tr.pl).getTime());
  const d=new Date(m);return dayKey(d>today()?today():d);}
// the milestone on day d (or null)
function bdMs(d=today()){if(!B.start)return null;const s=bdStart(),n=bdDiff(s,d);if(n<=0)return null;
  const mo=(d.getFullYear()-s.getFullYear())*12+d.getMonth()-s.getMonth(),dim=new Date(d.getFullYear(),d.getMonth()+1,0).getDate();
  if(mo>=1&&d.getDate()===Math.min(s.getDate(),dim)){
    if(mo%12===0){const y=mo/12;return{id:"y"+y,k:"y",n:y,title:"С днём рождения, Муся!",ban:"С днём рождения, Муся!",sub:y===1?"год вместе":`${y} ${pl(y,"год","года","лет")} вместе`};}
    if(mo===6)return{id:"h",k:"h",n:6,title:"Полгода вместе",ban:"Полгода вместе!"};
    const t=mo===1?"Месяц вместе":`${mo} ${pl(mo,"месяц","месяца","месяцев")} вместе`;return{id:"m"+mo,k:"m",n:mo,title:t,ban:t+"!"};}
  if(n===100)return{id:"d100",k:"d",n:100,title:"100 дней вместе",ban:"100 дней вместе!"};
  if(n===7)return{id:"w1",k:"w",n:7,title:"Неделя вместе",ban:"Неделя вместе!"};return null;}
function bdNext(){const t=today();for(let i=1;i<400;i++){const d=new Date(t.getFullYear(),t.getMonth(),t.getDate()+i),M=bdMs(d);if(M)return{d,M,i};}return null;}
const bdOpen=()=>{const M=bdMs();return M&&!B.done[M.id]?M:null;};

// ── who comes: befriended gate guests, rare lantern guests, Kumo, visitors the player has met ──
const BD_GG={kappa:"принёс огурец, завёрнутый в лист лопуха",kitsune:"подарила рисовый колосок — на сытый год",tanuki:"бил в живот, как в барабан: пом-пом-пом!",
 nekomata:"учила Мусю кошачьему танцу на задних лапах",akaname:"вылизал все тарелки до блеска",obake:"светил ярче всех фонарей сразу",warashi:"хлопала в ладоши и пела «Тоорянсэ»"};
const BD_RG={yuki:["m_rg_yuki","Юки-онна",500,"принесла снежинку, которая не тает до утра"],kodama:["m_rg_kodama","Кодама",340,"повторял эхом: «С праздником! …ником… …ником…»"],
 amabie:["m_rg_amabie","Амабиэ",410,"пожелала Мусе здоровья на сто лет вперёд"],usagi:["m_rg_usagi","Лунный кролик",390,"принёс моти, натолчённые прямо на луне"]};
const BD_VS={karakasa:["m_vs_karakasa","Каракаса-обакэ",330,"прыгал на одной ноге вокруг торта"],kamaitachi:["m_vs_kamaitachi","Кама-итати",340,"закружили над верандой вихрь конфетти"],
 bakezori:["m_vs_bakezori","Бакэ-дзори",230,"отбивал такт подошвой: карари-кори!"],kozo:["m_vs_kozo","Хитоцумэ-кодзо",330,"записал Мусю в книжечку хороших домов"],
 azuki:["m_vs_azuki","Адзуки-арай",290,"принёс горсть бобов для сэкихана"],nuppeppo:["m_vs_nuppeppo","Нуппэппо",230,"просто сидел рядом и улыбался"],
 yosuzume:["m_vs_yosuzume","Ёсудзумэ",118,"пела до самого рассвета"],moku:["m_vs_mokumokuren","Мокумокурэн",400,"смотрел из сёдзи сотней глаз — и все улыбались"]};
function bdFriends(){const o=[],add=(mon,n,h,gift,w)=>{if(MON[mon])o.push({mon,n,h,gift,w});};
  for(const g of GUESTS){const f=S.friends[g.id]||{n:0};if(f.n>0||g.id==="warashi"&&QS.done)add(g.mon,g.n,g.h,BD_GG[g.id],2+f.n);}
  const L=S.ext.lan&&S.ext.lan.met;if(L)for(const k in BD_RG)if(L[k])add(...BD_RG[k],5);
  if(S.ext.story2&&S.ext.story2.done)add("m_s2_king","Кумо, король Кошачьей горы",420,"мурлыкнул так, что задрожали сёдзи",6);
  const V=S.ext.vis&&S.ext.vis.m;if(V)for(const k in BD_VS)if(V[k]&&V[k].met)add(...BD_VS[k],3+Math.min(3,V[k].n||0));
  return o.sort((a,b)=>b.w-a.w);}

// ── the party: a one-chapter book played in the engawa ──
const BDB=[{title:"",room:"engawa",intro:{p:[],chars:[]}}];
const SLOT=[[-250,1236],[250,1236],[-400,1180],[400,1180],[-180,1146],[180,1146]];
const BD_RW={w:["bd_frame"],d:["bd_fan"],h:["bd_kusudama","bd_ribbon","bd_bonbori"],m:["bd_ribbon","bd_bonbori"],y:["bd_cakefig","bd_maneki"]};
const bdReward=M=>BD_RW[M.k].find(r=>!S.owned.has(r))||null;
const BD_ST={w:"bd_week",d:"bd_100",y:"bd_year"};
function bdIntro(M){const n=M.n;return M.k==="w"?"Ровно неделю назад Муся впервые переступила порог этого дома. Тогда она пряталась под столом, а теперь спит посреди веранды, раскинув лапы."
  :M.k==="d"?"Сто дней! В Японии сотый день малыша празднуют особо: ему впервые дают попробовать «взрослую» еду. Муся пробует торт с клубникой и ужасно этим горда."
  :M.k==="h"?"Полгода вместе. Полгода назад этот дом был тихим и тёмным, а теперь в нём пахнет рисом, тёплой шерстью и счастьем."
  :M.k==="y"?(n===1?"Ровно год назад в доме впервые зазвенел колокольчик Муси. Сегодня её день рождения — и все, кто знает дорогу к этому дому, пришли поздравить."
    :`Муся живёт здесь уже ${n} ${pl(n,"год","года","лет")}. И снова её день рождения: на веранде шуршат бумажные гирлянды, в бонбори теплятся огоньки.`)
  :n===1?"Сегодня ровно месяц, как Муся живёт в этом доме. На веранде шуршат бумажные гирлянды, в бонбори теплятся огоньки, а посередине — торт с клубникой."
  :`Ещё один месяц позади — уже ${n}. Муся знает здесь каждую скрипучую доску и каждый тёплый угол, а гирлянды на веранде снова шуршат на ветру.`;}
let bdRun=null,bdLinger=null;
function bdParty(M){if(!M||scene.on||petAway())return;
  const F=bdFriends(),show=F.slice(0,SLOT.length),R=bdReward(M);
  const chars=show.map((f,i)=>({id:f.mon,x:()=>visX(900+SLOT[i][0],125),y:SLOT[i][1],h:Math.round(Math.min(f.h,420)*.74),d:.8,from:.5+i*.45})).sort((a,b)=>a.y-b.y);
  const names=show.map(f=>f.n),more=F.length-show.length,list=names.length>1?names.slice(0,-1).join(", ")+" и "+names[names.length-1]:names[0];
  const p=[bdIntro(M),
    show.length?`На свет фонариков собрались гости. Сегодня у Муси в гостях ${list}.${more>0?` И ещё ${more} — всех не уместить на веранде!`:""}`
      :"Гостей пока нет: ёкаи ещё не знают дорогу к этому дому. Но фонарики светят для двоих — для Муси и для тебя. Угощай гостей у ворот, и в следующий праздник они придут.",
    ...(show.length?[show.slice(0,3).map(f=>`${f.n} ${f.gift}.`).join(" ")]:[]),
    `Муся задула свечку на торте и замурлыкала на всю веранду. Под утро гости разошлись, ${R?`а у порога остался подарок — ${IT[R].n}.`:"а в кладовой остались гостинцы: данго и итиго-дайфуку."}`];
  BDB[0]={title:M.title,room:"engawa",intro:{p,chars}};bdRun={M,R,last:-1};
  playScene(0,"intro",()=>bdDone(M,R,chars),false,BDB);}
function bdDone(M,R,chars){bdRun=null;B.done[M.id]=dayKey();B.log.push([M.id,dayKey(),chars.length]);if(B.log.length>40)B.log.shift();
  if(R){S.owned.add(R);if(typeof loadItem==="function")loadItem(R);}else{give("ds_dango");give("ds_daifuku");}
  if(M.k!=="w"&&M.k!=="d")award("bd_month");if(BD_ST[M.k])award(BD_ST[M.k]);
  disc("birthday",M.id);S.needs.joy=100;bdLinger={t:now(),chars};bdConf=now();
  if(!petAway()){burst(16);setTimeout(()=>react("😻",2.4),500);}chime([1046,1318,1568,2093]);
  setTimeout(()=>toast(R?`🎁 ${IT[R].n} — в 🧺 Вещах`:"🎁 Гостинцы от гостей — в кладовой"),900);save();ui();hubDot();}
// cake fed on a milestone day → the party
hook("ev",(ev,d)=>{if(ev!=="eat"||d!=="ds_bd_cake")return;const M=bdOpen();
  if(M)setTimeout(()=>{if(!scene.on&&!overlaysOpen())bdParty(M);},2600);
  else{const N=bdNext();if(N)setTimeout(()=>toast(`🎂 Следующий праздник — ${fmt(N.d)}`),1800);}});
// «there is always room for cake»: a full Musya still eats it (capture phase runs before the tray's own handler)
$("tray").addEventListener("click",e=>{if(e.target.closest('[data-pfood="ds_bd_cake"]')&&S.needs.food>=95)S.needs.food=90;},true);
// the scene's last button and the reward picture
hook("tick",()=>{if(!bdRun||!scene.on||scene.book!==BDB||scene.i===bdRun.last)return;bdRun.last=scene.i;const last=scene.i>=BDB[0].intro.p.length-1;
  $("scNext").textContent=last?"Ура! 🎉":"Дальше ›";const im=$("scImg");if(last&&bdRun.R){im.innerHTML=itemThumb(IT[bdRun.R],90,56);im.hidden=false;}});

// ── decorations in the engawa ──
let bdIm=null,glowC=null,bdFont=null,bdBan=null,bdConf=-99;
const bdImg=()=>bdIm||(FIMG.bd?(bdIm=FIMG.bd):(fLoad("bd"),null));
function bdGlow(){if(glowC)return glowC;const c=document.createElement("canvas");c.width=c.height=128;const g=c.getContext("2d"),gr=g.createRadialGradient(64,64,0,64,64,64);
  gr.addColorStop(0,"rgba(255,190,110,.85)");gr.addColorStop(.4,"rgba(255,150,70,.3)");gr.addColorStop(1,"rgba(255,140,60,0)");g.fillStyle=gr;g.fillRect(0,0,128,128);return glowC=c;}
// a sprite hung between image x0..x1 at image y (its own row ty is the hanging line), projected at depth d
function hang(im,r,x0,x1,y,d,ty){const [ax,ay]=imgToStage(x0,y,d),[bx,by]=imgToStage(x1,y,d),L=Math.hypot(bx-ax,by-ay),k=L/r[2];
  ctx.save();ctx.translate(ax,ay);ctx.rotate(Math.atan2(by-ay,bx-ax));ctx.drawImage(im,r[0],r[1],r[2],r[3],0,-ty*k,L,r[3]*k);return k;}
function bdDecor(t,front){const M=bdMs(),im=bdImg();if(!M||!im)return;const night=dayTint()[1];
  if(!front){for(const x of [470,1330]){const [sx,sy]=imgToStage(x,1132,.8),k=BGM.k*1.1,r=BDA.bon,w=r[2]*k,h=r[3]*k;
      ctx.drawImage(im,r[0],r[1],r[2],r[3],sx-w/2,sy-h,w,h);
      const fl=.88+.08*Math.sin(t*6.1+x)+.04*Math.sin(t*13+x),R=(night?230:110)*BGM.k;ctx.save();ctx.globalCompositeOperation="lighter";ctx.globalAlpha=(night?.5:.2)*fl;
      ctx.drawImage(bdGlow(),sx-R,sy-h*.72-R,R*2,R*2);ctx.restore();}
    return;}
  // garland swags along the eaves, then the banner on two cords
  const xs=[86,407,728,1049,1370];for(let i=0;i<xs.length-1;i++){hang(im,BDA.gar,xs[i],xs[i+1],104,.92,10);ctx.restore();}
  const bx0=visX(900,0)-330,bx1=bx0+660,[c0x,c0y]=imgToStage(bx0+12,104,.92),[c1x,c1y]=imgToStage(bx1-12,104,.92),[l0x,l0y]=imgToStage(bx0+14,452,.92),[l1x,l1y]=imgToStage(bx1-14,452,.92);
  ctx.strokeStyle="rgba(150,44,36,.9)";ctx.lineWidth=Math.max(1,2.2*BGM.k);ctx.beginPath();ctx.moveTo(c0x,c0y);ctx.lineTo(l0x,l0y);ctx.moveTo(c1x,c1y);ctx.lineTo(l1x,l1y);ctx.stroke();
  const sway=Math.sin(t*.9)*1.5*BGM.k,k=hang(im,BDA.ban,bx0,bx1,452+sway/BGM.k,.92,0),W=560,ty=64;
  bdFont=bdFont||getComputedStyle(document.body).fontFamily;ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillStyle="#3a1a12";
  let fs=(M.sub?38:46)*k;ctx.font=`700 ${fs}px ${bdFont}`;const mw=ctx.measureText(M.ban).width;if(mw>W*.88*k){fs*=W*.88*k/mw;ctx.font=`700 ${fs}px ${bdFont}`;}
  ctx.fillText(M.ban,W/2*k,(M.sub?ty-10:ty+1)*k);if(M.sub){ctx.fillStyle="#9a2a20";ctx.font=`600 ${20*k}px ${bdFont}`;ctx.fillText(M.sub,W/2*k,(ty+20)*k);}
  ctx.restore();bdBan=[Math.min(l0x,l1x),Math.min(l0y,l1y),Math.max(l0x,l1x),Math.max(l0y,l1y)+132*k];}
// friends stay a little after the party
function bdStay(t,front){const L=bdLinger;if(!L||scene.on)return;const e=t-L.t;if(e>34){bdLinger=null;return;}const a=clamp(Math.min(e/1.2,(34-e)/4),0,1);
  for(const c of L.chars){if((c.y>catLineY()+6)!==front)continue;drawMon(c.id,c.x(),c.y+Math.sin(t*3+c.y)*4,c.h,c.d,a);}}
hook("draw",(t,front)=>{if(S.room!=="engawa")return;bdDecor(t,front);bdStay(t,front);});
// paper confetti around Musya: for a while after entering the decorated engawa and after the party
const CF=Array.from({length:24},(_,i)=>({p:i/24*1.7%1,o:((i*37)%24)/12-1,c:["#c8382e","#efe3c8","#d8b048","#e6a2b4","#4a6aa8"][i%5],r:i*.7}));
hook("overlay",t=>{if(S.room!=="engawa"||petAway()||!bdMs()||t-bdConf>14)return;const [hx,hy]=cellToStage(97,160),s=view.s,fade=clamp((14-(t-bdConf))/3,0,1);
  for(const q of CF){const u=(t*.32+q.p)%1,x=hx+(q.o+.18*Math.sin(t*1.4+q.r))*120*s,y=hy-170*s+u*260*s;ctx.save();ctx.globalAlpha=fade*Math.sin(Math.PI*u)*.9;
    ctx.translate(x,y);ctx.rotate(t*2.2+q.r);ctx.scale(1,Math.cos(t*3+q.r));ctx.fillStyle=q.c;ctx.fillRect(-7*s,-4*s,14*s,8*s);ctx.restore();}});
hook("room",id=>{if(id!=="engawa"||!bdMs())return;bdConf=now();if(!petAway()&&!scene.on)setTimeout(()=>{if(S.room==="engawa"&&!scene.on&&pet.action!=="sleep")react("🥳",2);},1600);});
hook("hit",(x,y)=>{if(S.room!=="engawa"||!bdBan||!bdMs()||scene.on)return false;const b=bdBan;if(x<b[0]||x>b[2]||y<b[1]||y>b[3])return false;
  const n=bdDiff(bdStart(),today());toast(`🎉 Муся с тобой ${n} ${pl(n,"день","дня","дней")}`);chime([1046,1318,1568]);bdConf=now();return true;});

// ── hub card, dot, the one toast of the day, the postcard line ──
let bdBooted=false;
hook("boot",()=>{if(!B.start||!/^\d{4}-\d\d-\d\d$/.test(B.start)){B.start=bdGuess();B.auto=1;save();}bdBooted=true;fLoad("bd");});
hook("sec",()=>{if(!bdBooted)return;const M=bdOpen();if(!M||B.toast===dayKey()||scene.on||overlaysOpen()||now()<9)return;B.toast=dayKey();save();
  toast(M.k==="y"?"🎂 Сегодня день рождения Муси! Загляни в 家":`🎉 Сегодня «${M.title}» — загляни в 家`);chime([1318,1568]);});
hook("hubDot",()=>bdBooted&&!!bdOpen());
hook("away",()=>{const M=bdOpen();return M?{i:"🎂",t:`Сегодня особенный день — «${M.title}». Испеки торт с клубникой и угости Мусю: на веранде соберутся гости.`}:null;});
hook("hub",()=>{const s=bdStart(),n=bdDiff(s,today()),M=bdMs(),N=bdNext(),ich=have("v_ichigo"),cake=have("ds_bd_cake");
  const now_=M?(B.done[M.id]?`<p>🎉 Сегодня «${M.title}». Праздник удался — гости разошлись только под утро.</p>`
    :`<p class="bd-now">🎉 Сегодня «${M.title}»! Испеки «Торт с клубникой» и угости Мусю — на веранде соберутся друзья.</p>`):"";
  return`<div class="hubc"><h4>🎂 Муся с тобой <i>誕生日</i></h4>
   <p class="bd-big">${n>0?`Муся живёт в доме <b>${n} ${pl(n,"день","дня","дней")}</b> — с ${fmt(s)}.`:"Муся появилась в доме сегодня."}</p>${now_}
   ${N?`<p>Следующий праздник: «${N.M.title}» — ${fmt(N.d)} (через ${N.i} ${pl(N.i,"день","дня","дней")}).</p>`:""}
   <p>🍰 Торт: клубника с огорода, мука, яйца и сахар. ${ich?`Клубники в кладовой: ${ich}.`:"Клубники нет — посади её: «Дворик» → 🌱 Огород."} В праздник варят и сэкихан — рис с бобами адзуки.</p>
   <div class="row">${cake?`<button class="btn primary" data-x="bd:feed">🎂 Угостить Мусю тортом</button>`:""}<button class="btn ${!cake&&bdOpen()?"primary":""}" data-x="bd:cook">🍳 Испечь торт</button></div>
   <label class="bd-l">День, когда Муся появилась в доме${B.auto?" (мы угадали по сохранению — поправь, если не так)":""}<input type="date" class="bd-date" value="${B.start}" max="${dayKey()}"></label>
   ${B.log.length?`<p class="bd-log">Праздники: ${B.log.slice(-4).map(e=>`${e[1].slice(8)}.${e[1].slice(5,7)} — ${e[2]} ${pl(e[2],"гость","гостя","гостей")}`).join(" · ")}</p>`:""}</div>`;});
hook("click",k=>{if(k==="bd:cook"){closePanel();S.trayMode.kitchen="cook";goRoom("kitchen");ui();toast("🍳 Внизу — «Торт с клубникой»");return true;}
  if(k==="bd:feed"){if(!have("ds_bd_cake"))return true;closePanel();if(S.room!=="kitchen")goRoom("kitchen");S.trayMode.kitchen="play";ui();
    setTimeout(()=>{if(S.needs.food>=95)S.needs.food=90;eatPantry("ds_bd_cake");},1100);return true;}return false;});
document.addEventListener("change",e=>{const el=e.target;if(!el.classList||!el.classList.contains("bd-date"))return;const v=el.value;
  if(!/^\d{4}-\d\d-\d\d$/.test(v)||dOf(v)>today())return;B.start=v;B.auto=0;save();toast(`📅 Запомнили: Муся с тобой с ${fmt(dOf(v))}`);if(panelIs("hub"))openHub();hubDot();});

// test handles: X.bd.party() plays today's party, X.bd.set("2025-10-01") moves the start day
X.bd={B,ms:bdMs,next:bdNext,guess:bdGuess,friends:bdFriends,party:()=>bdParty(bdMs()),set:k=>{B.start=k;B.auto=0;save();},ban:()=>bdBan};
}
