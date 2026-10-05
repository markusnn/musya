{
// ───────────────────────── New holidays: Cat Day, Japanese Halloween, Japanese Christmas, Omisoka ─────────────────────────
// Four festivals are spliced into FEST, so the calendar 暦, the chip, tasks, shop items, rewards and stamps all run on the
// core festival code. Year order after this block: Сэцубун · День кошки · Хинамацури … Цукими · Хэллоуин · Сити-го-сан ·
// Тодзи (now 19–23 Dec) · Рождество (24–25) · Омисока (30–31) · Сёгацу (moved last; still 28 Dec – 7 Jan, but on the
// 30th–31st festNow() finds Омисока first). S.ext.holidays = {n:{"<festKey>|pet":7,"<festKey>|bell":37}, carve:0..4}.
// Effects (F.fx keys): hl_paws paw prints + hearts · hl_kabo glowing kabocha (entrance, veranda garden) · hl_lights string
// lights over every room · hl_bell temple bell rings (108 strikes from the entrance tray, a far bell at night).
// Pictures: assets/items/atlas_hl.webp (art/holidays_art.py).
const HS=S.ext.holidays||(S.ext.holidays={n:{},carve:0});HS.n=HS.n||{};
const HLR={"hl_r_bell":[0,0,210,250],"hl_broom":[212,0,110,240],"hl_obakecos":[324,0,140,210],"hl_kab0":[466,0,250,200],"hl_poinsettia":[718,0,160,190],
 "hl_r_kabotan":[880,0,180,180],"hl_r_globe":[0,252,160,180],"hl_r_throne":[162,252,220,150],"hl_jack":[384,252,160,140],"hl_cake":[546,252,160,140],
 "hl_present":[708,252,140,140],"hl_nekocushion":[850,252,210,130],"hl_candy":[0,434,170,130],"hl_pawstamp":[172,434,170,120],"hl_nekoonigiri":[344,434,190,120],
 "hl_lights":[536,434,280,120],"hl_sobaset":[818,434,190,120],"hl_mikan":[0,566,170,110],"ds_hl_soba":[172,566,150,92]};
const hlIt=(id,n,a,p,fest,x={})=>({id,n,c:"Праздники",w:HLR[id][2],h:HLR[id][3],a,p,fest,at:["hl",HLR[id][0],HLR[id][1]],...x}),RW={reward:true};
addItems([
 hlIt("hl_pawstamp","Печать «Кошачья лапка»","b",20,"hl_neko"),hlIt("hl_nekocushion","Подушка-кошка","b",35,"hl_neko"),
 hlIt("hl_nekoonigiri","Онигири-котики","b",15,"hl_neko"),hlIt("hl_r_throne","Кошачий трон с кистями","b",0,"hl_neko",RW),
 hlIt("hl_kab0","Тыква кабоча для фонаря","b",30,"hl_halloween"),
 hlIt("hl_jack","Фонарь из кабочи","b",0,"hl_halloween",{glow:[80,92],src:"🎃 вырезать",hint:"Поставь тыкву кабоча и коснись её 5 раз"}),
 hlIt("hl_candy","Корзинка конфет для ряженых","b",25,"hl_halloween"),hlIt("hl_obakecos","Костюм-привидение обакэ","b",40,"hl_halloween"),
 hlIt("hl_r_kabotan","Кабоча-обакэ — одноглазая тыква","b",0,"hl_halloween",RW),
 hlIt("hl_lights","Гирлянда-иллюминация","t",30,"hl_xmas",{glow:[140,62]}),hlIt("hl_cake","Клубничный шорткейк","b",30,"hl_xmas"),
 hlIt("hl_poinsettia","Пуансеттия в горшке","b",30,"hl_xmas"),hlIt("hl_present","Коробка с бантом","b",25,"hl_xmas"),
 hlIt("hl_r_globe","Снежный шар с домиком","b",0,"hl_xmas",RW),
 hlIt("hl_sobaset","Тосикоси-соба на подносе","b",20,"hl_omisoka"),hlIt("hl_broom","Метла для осодзи","b",15,"hl_omisoka"),
 hlIt("hl_mikan","Мандарины микан","b",15,"hl_omisoka"),hlIt("hl_r_bell","Храмовый колокол бонсё","b",0,"hl_omisoka",RW)],{hl:[1100,676]});
FATL.hl={w:1100,h:676,r:{ds_hl_soba:HLR.ds_hl_soba}};
FOOD.ds_hl_soba={n:"Тосикоси-соба",k:"dish",food:34,joy:14};
RECIPES.push({id:"hl_soba",dish:"ds_hl_soba",n:"Тосикоси-соба",jp:"年越しそば",lore:"Гречневая лапша в горячем бульоне даси с зелёным луком. Её едят в последний вечер года: длинная лапша — к долгой жизни.",
 need:["i_noodles","i_katsuobushi","v_negi"],steps:[{k:"add",it:["i_katsuobushi"]},{k:"stir",n:2},{k:"add",it:["i_noodles"]},{k:"heat",n:2,lb:"Откинь лапшу"},{k:"chop",it:"v_negi",n:3},{k:"add",it:["v_negi"]}]});

// counters per festival year (festKey keeps the year, so next year starts from zero)
const hlFest=id=>FEST.find(f=>f.id===id);
const hlCnt=(id,k)=>HS.n[festKey(hlFest(id))+"|"+k]||0;
const hlInc=(id,k)=>{const q=festKey(hlFest(id))+"|"+k;return HS.n[q]=(HS.n[q]||0)+1;};
const hlPetAct=a=>a==="poke"||a==="purr"||a==="highfive";
const HL_F=[
 {id:"hl_neko",n:"День кошки",jp:"猫の日",sub:"«Ня-ня-ня»",from:[2,20],to:[2,22],icon:"🐾",fx:["hl_paws"],stamp:["hl_f_neko","猫"],reward:"hl_r_throne",
  lore:["По-японски кошка говорит не «мяу», а «ня». А «два» по-японски — «ни», так что 22.2 звучит почти как «ня-ня-ня». С 1987 года этот день — День кошки: его выбрали голосованием сами любители кошек.",
   "В эти дни пекут сладости с кошачьими мордочками, лепят онигири с ушками и ставят печати-лапки. А на станции Киси в Вакаяме когда-то служила начальницей кошка Тама: посмотреть на неё ехали со всей Японии, и маленькую дорогу так и не закрыли. Сегодня главная в доме — Муся."],
  tasks:[{get t(){const n=hlCnt("hl_neko","pet");return"Погладь Мусю 10 раз"+(n&&n<10?` · ${n}/10`:"");},ev:"act",test:a=>hlPetAct(a)&&hlInc("hl_neko","pet")>=10},
   {t:"Угости Мусю рыбкой",ev:"food",test:d=>d==="fish"||d==="sushi"||d==="ds_yakizakana"||!!(FOOD[d]&&FOOD[d].k==="fish")},
   {t:"Наряди Мусю: сегодня её праздник",ev:"wear"}]},
 {id:"hl_halloween",n:"Хэллоуин",jp:"ハロウィン",sub:"Ночь ряженых",from:[10,25],to:[10,31],icon:"🎃",fx:["hl_kabo"],stamp:["hl_f_hw","化"],reward:"hl_r_kabotan",
  lore:["Хэллоуин пришёл в Японию недавно, в конце девяностых, и прижился по-своему: здесь это не столько детский праздник, сколько ночь костюмов. Тысячи людей наряжаются и выходят на перекрёсток Сибуя — кто призраком, кто óни, кто рокурокуби с длинной шеей.",
   "Японцам это знакомо давно: в старину верили, что по ночным улицам идёт Хякки-яко, парад сотни ёкаев. Вот и выходит, что Хэллоуин здесь — ночь, когда люди наряжаются ёкаями. А тыкву зовут «кабоча»: её привезли португальцы из Камбоджи, и имя прижилось."],
  tasks:[{t:"Вырежи фонарь: поставь тыкву кабоча и коснись её",ev:"hl",test:d=>d==="carve"},
   {t:"Наряди Мусю ёкаем: надень маску",ev:"wear",test:d=>d.slot==="mask"},
   {t:"Угости гостя-ёкая у ворот",ev:"guest"}]},
 {id:"hl_xmas",n:"Рождество",jp:"クリスマス",sub:"Курисумасу по-японски",from:[12,24],to:[12,25],icon:"🎄",fx:["snow","hl_lights"],stamp:["hl_f_xmas","聖"],reward:"hl_r_globe",
  lore:["В Японии Рождество — не семейный праздник, а светлый и чуть-чуть влюблённый. Улицы и парки сияют иллюминацией, а сочельник проводят вдвоём, как День святого Валентина. Всей семьёй собираются через неделю — на Новый год.",
   "Главное угощение — клубничный шорткейк: белые сливки и красные ягоды, цвета праздника и удачи. Торт заказывают в кондитерской заранее, жареную курицу — чуть ли не за месяц, а дети ждут подарков от Санта-сан."],
  tasks:[{t:"Испеки на кухне торт с клубникой",ev:"cook",test:d=>d.id==="bd_cake"},
   {t:"Повесь гирлянду-иллюминацию",ev:"put",test:hasPut("hl_lights")},
   {t:"Подари Мусе подарок: поставь коробку с бантом и коснись её",ev:"hl",test:d=>d==="gift"}]},
 {id:"hl_omisoka",n:"Омисока",jp:"大晦日",sub:"Проводы старого года",from:[12,30],to:[12,31],icon:"🔔",fx:["snow","hl_bell"],stamp:["hl_f_omi","鐘"],reward:"hl_r_bell",
  lore:["Тридцать первое декабря — Омисока, последний вечер года. К нему заканчивают осодзи, большую уборку: выметают из дома пыль, а с ней и все неудачи старого года, чтобы божество нового года Тосигами вошло в чистый дом.",
   "Поздно вечером едят тосикоси-соба — «лапшу перехода через год»: длинную, как жизнь, и легко рвущуюся, как старые беды. А ближе к полуночи в храмах начинают бить в колокол — 108 раз, по удару на каждую людскую страсть. Последний удар звучит уже в новом году."],
  tasks:[{t:"Свари на кухне тосикоси-соба",ev:"cook",test:d=>d.id==="hl_soba"},
   {t:"Осодзи: искупай Мусю перед Новым годом",ev:"bath"},
   {get t(){const n=hlCnt("hl_omisoka","bell");return"Дзёя-но канэ: ударь в колокол у ворот 108 раз"+(n&&n<108?` · ${n}/108`:"");},ev:"hl",test:d=>d==="bell"}]}];
// splice into the year (block top-level, before boot); Тодзи ends on the 23rd now, Сёгацу goes after Омисока
if(!hlFest("hl_neko")){
  const at=(id,d=0)=>{const i=FEST.findIndex(f=>f.id===id);return i<0?FEST.length:i+d;},tj=hlFest("toji");if(tj)tj.to=[12,23];
  FEST.splice(at("setsubun",1),0,HL_F[0]);FEST.splice(at("tsukimi",1),0,HL_F[1]);
  const sg=FEST.findIndex(f=>f.id==="shogatsu"),SG=sg<0?null:FEST.splice(sg,1)[0];
  FEST.splice(at("toji",1),0,HL_F[2],HL_F[3],...(SG?[SG]:[]));
  STAMPS.push(...HL_F.map(F=>[F.stamp[0],F.stamp[1],F.n,"Выполни все задания праздника"]));
}

// ── pictures and cached glows
const hlCv=(w,h,f)=>{const c=document.createElement("canvas");c.width=w;c.height=h;f(c.getContext("2d"));return c;};
const HLGLOW=hlCv(128,128,g=>{const gr=g.createRadialGradient(64,64,0,64,64,64);gr.addColorStop(0,"rgba(255,176,80,.6)");gr.addColorStop(.42,"rgba(255,134,44,.24)");gr.addColorStop(1,"rgba(255,120,30,0)");g.fillStyle=gr;g.fillRect(0,0,128,128);});
const HLPAW=hlCv(48,48,g=>{g.fillStyle="#ffd6dc";g.shadowColor="rgba(255,150,180,.9)";g.shadowBlur=6;g.beginPath();g.ellipse(24,31,10,8,0,0,7);g.fill();
  for(const [x,y] of [[12,19],[19.5,12],[28.5,12],[36,19]]){g.beginPath();g.ellipse(x,y,4.4,5.3,0,0,7);g.fill();}});
const HLBULB=["#ff6a52","#ffd36a","#7ae08e","#86b8ff","#fff0d0"].map(c=>hlCv(32,32,g=>{const gr=g.createRadialGradient(16,16,0,16,16,16);gr.addColorStop(0,"#fffaf0");gr.addColorStop(.16,c);gr.addColorStop(.4,c+"66");gr.addColorStop(1,c+"00");g.fillStyle=gr;g.fillRect(0,0,32,32);}));
let HLIM=null;
hook("boot",()=>atlasImg("hl",im=>{HLIM=im;}));
const hlDark=()=>dayTint()[1]||hourNow()>=17||hourNow()<6;

// ── 猫の日: paw prints walk across the floor behind Musya, hearts when she is petted
function hlPaws(t){const P=16,ph=t%P,dir=Math.floor(t/P)%2?-1:1,l=visX(-1e5,60),r=visX(1e5,60),step=84,N=Math.floor((r-l)/step);if(N<2)return;
  const yb=catLineY()-8;
  for(let i=0;i<N;i++){const e=ph-i*.36;if(e<0)break;const a=clamp(Math.min(e/.25,(7-e)/2.5),0,1);if(a<=0)continue;
    const ix=dir>0?l+i*step:r-i*step,[x,y]=imgToStage(ix,yb+(i%2?-15:15),CAT_D),sz=54*BGM.k;
    ctx.save();ctx.translate(x,y);ctx.scale(1,.5);ctx.rotate(dir*Math.PI/2);ctx.globalAlpha=a*.6;ctx.drawImage(HLPAW,-sz/2,-sz/2,sz,sz);ctx.restore();}}
hook("ev",(ev,d)=>{if(ev!=="act"||!hlPetAct(d)||!festFxOn("hl_paws")||petAway())return;const t=now();
  for(let i=0;i<3;i++)floatFx.push({g:pick(["💕","💗","✨","🐾"]),x:pet.x+rand(-44,44)*view.s,y:view.floor-rand(100,170)*view.s,t:t+i*.14});});

// ── ハロウィン: carved kabocha glow by the torii and among the veranda garden bushes (dusk and night)
function hlKabo(t){let P=null;
  if(S.room==="entrance")P=[[762,1014,.7,92],[818,999,.7,64]];
  else if(S.room==="engawa"){const l=visX(-1e5,110),r=visX(1e5,110);P=[[l+(r-l)*.02,1094,.42,112],[l+(r-l)*.76,1090,.42,90],[l+(r-l)*.97,1094,.42,118]];}
  if(!P)return;const dark=hlDark(),r=HLR.hl_jack;
  P.forEach(([ix,iy,d,h],i)=>{const [x,y]=imgToStage(ix,iy,d),k=(imgToStage(ix+100,iy,d)[0]-x)/100,hh=h*k,w=hh*r[2]/r[3];
    if(dark){const fl=.78+.14*Math.sin(t*8.3+i*2)+.08*Math.sin(t*21+i),R=hh*1.6;ctx.save();ctx.globalCompositeOperation="lighter";ctx.globalAlpha=fl;ctx.drawImage(HLGLOW,x-R,y-hh*.45-R,R*2,R*2);ctx.restore();}
    ctx.drawImage(HLIM,r[0],r[1],r[2],r[3],x-w/2,y-hh,w,hh);});}
function hlCarved(){const q=S.placed.hl_kab0;if(!q)return;S.placed.hl_jack={...q};if(S.dpos.hl_kab0)S.dpos.hl_jack=S.dpos.hl_kab0;
  delete S.placed.hl_kab0;delete S.dpos.hl_kab0;delete vpos.hl_kab0;delete vpos.hl_jack;S.owned.delete("hl_kab0");S.owned.add("hl_jack");
  loadItem("hl_jack");wob.hl_jack=now();chime([784,988,1175,1568]);burst(6);if(!petAway())react("😸",1.6);qev("hl","carve");
  setTimeout(()=>toast("🎃 Фонарь из кабочи готов!"),1300);save();ui();}
hook("itemTap",it=>{
  if(it.id==="hl_kab0"){HS.carve=(HS.carve||0)+1;tone(300+HS.carve*60,.07,"triangle",.05);tone(150,.05,"square",.02);fxAt(it,["✨","🔸"],2);
    if(HS.carve===1){if(!petAway())react("😼",1.4);toast("🎃 Режем фонарь… коснись ещё");}
    if(HS.carve>=5){HS.carve=0;hlCarved();}return true;}
  if(it.id==="hl_present"){fxAt(it,["🎁","✨","💝"],4);chime([1318,1568,2093]);if(!petAway())walkTo(it,"box","😻");qev("hl","gift");return true;}
  return false;});

// ── クリスマス: string lights swagged over the top of every room
function hlGarland(t){const W=view.W,s=view.s,y0=view.H*.115,sag=view.H*.045,n=W>760?4:3,dark=dayTint()[1];
  ctx.save();ctx.lineWidth=1.5*s;ctx.strokeStyle="rgba(14,18,12,.92)";
  for(let j=0;j<n;j++){const xa=W*j/n,xb=W*(j+1)/n,Y=u=>y0+sag*4*u*(1-u);
    ctx.beginPath();for(let i=0;i<=20;i++){const u=i/20;i?ctx.lineTo(xa+(xb-xa)*u,Y(u)):ctx.moveTo(xa,Y(0));}ctx.stroke();
    ctx.globalCompositeOperation="lighter";
    for(let i=0;i<8;i++){const u=(i+.5)/8,x=xa+(xb-xa)*u,y=Y(u)+4*s,tw=.5+.5*Math.sin(t*2.3+i*1.7+j*2.9),R=(dark?14:10)*s;
      ctx.globalAlpha=(dark?.5:.32)+.5*tw;ctx.drawImage(HLBULB[(i+j*3)%5],x-R,y-R,R*2,R*2);}
    ctx.globalCompositeOperation="source-over";ctx.globalAlpha=1;}
  ctx.restore();}

// ── 大晦日: joya no kane — 108 strikes from the entrance tray; each strike is a deep tone and a ring of warm light
const HLB=[];let hlLast=-99,hlFar=0;
function hlBellSnd(v){tone(73.4,4.6,"sine",.12*v);tone(146.8,3.3,"sine",.05*v);tone(220.4,2.1,"triangle",.016*v);tone(311,1.3,"sine",.012*v);}
function hlRing(t,v){let x=view.W*.5,y=view.H*.22;if(S.room==="entrance")[x,y]=imgToStage(900,640,.38);HLB.push({t0:t,x,y,v});if(HLB.length>6)HLB.shift();}
function hlRings(t){ctx.save();ctx.globalCompositeOperation="lighter";
  for(let i=HLB.length-1;i>=0;i--){const b=HLB[i],e=(t-b.t0)/2.8;if(e>=1){HLB.splice(i,1);continue;}const a=(1-e)*(1-e)*b.v,r=(24+e*Math.max(view.W,view.H)*.5),R=110*view.s*(1+e*.6);
    ctx.globalAlpha=a*.85;ctx.drawImage(HLGLOW,b.x-R,b.y-R,R*2,R*2);ctx.globalAlpha=1;
    ctx.strokeStyle=`rgba(255,206,132,${.42*a})`;ctx.lineWidth=(7-5*e)*view.s;ctx.beginPath();ctx.arc(b.x,b.y,r,0,Math.PI*2);ctx.stroke();}
  ctx.restore();}
const hlBellLbl=()=>{const n=hlCnt("hl_omisoka","bell");return n>=108?"Колокол · 108 ✓":`Колокол · ${n}/108`;};
function hlStrike(btn){const t=now();if(t-hlLast<.18)return;hlLast=t;hlBellSnd(1);hlRing(t,1);
  let n=hlCnt("hl_omisoka","bell");if(n<108&&festOn("hl_omisoka")){n=hlInc("hl_omisoka","bell");if(n===108){qev("hl","bell");burst(10);save();}else if(n%27===0)toast(`🔔 Ударов: ${n} из 108`);}
  const nm=btn&&btn.querySelector(".nm");if(nm)nm.textContent=hlBellLbl();
  if(!petAway()&&n%12===1)react(pick(["🙀","😌","😸"]),1.3);}
hook("tray",(tray,room)=>{if(room!=="entrance"||!festOn("hl_omisoka")||(S.trayMode[room]||"play")!=="play")return;const el=tray.querySelector(".items");if(!el)return;
  el.insertAdjacentHTML("afterbegin",`<button class="item wide" data-x="hl:bell"><span class="ico">🔔</span><span class="nm">${hlBellLbl()}</span></button>`);});
hook("click",(k,btn)=>{if(k!=="hl:bell")return false;hlStrike(btn);return true;});
hook("tabDot",room=>room==="entrance"&&festOn("hl_omisoka")&&hlCnt("hl_omisoka","bell")<108);

// ── drawing: things in the room behind Musya, lights and rings over everything
hook("draw",(t,front)=>{if(front||scene.on)return;
  if(festFxOn("hl_paws"))hlPaws(t);
  if(HLIM&&festFxOn("hl_kabo"))hlKabo(t);
  if(festFxOn("hl_bell")&&S.room==="entrance"&&hlDark()){const [x,y]=imgToStage(900,640,.38),R=300*BGM.k;ctx.save();ctx.globalCompositeOperation="lighter";ctx.globalAlpha=.32+.08*Math.sin(t*.9);ctx.drawImage(HLGLOW,x-R,y-R,R*2,R*2);ctx.restore();}});
hook("overlay",t=>{if(scene.on)return;if(festFxOn("hl_lights"))hlGarland(t);if(HLB.length)hlRings(t);});
// discovery when a holiday's tasks are all done; a far temple bell every ~50 s on Omisoka night outdoors
hook("sec",()=>{const F=festNow();if(!F||!F.id.startsWith("hl_"))return;if(festProg(F).done)disc("holiday",F.id);
  if(F.id==="hl_omisoka"&&hlDark()&&OUTDOOR.includes(S.room)&&!overlaysOpen()&&!scene.on){const t=now();if(t-hlFar>50&&t-hlLast>20){hlFar=t;hlBellSnd(.35);hlRing(t,.45);}}});

X.holidays={HS,carve:()=>{for(let i=0;i<5;i++)hk("itemTap",{id:"hl_kab0",...S.placed.hl_kab0},IT.hl_kab0,now());},gift:()=>hk("itemTap",{id:"hl_present",...(S.placed.hl_present||{x:900,y:1100})},IT.hl_present,now()),
  strike:n=>{for(let i=0;i<n;i++){hlLast=-99;hlStrike(document.querySelector('[data-x="hl:bell"]'));}},cnt:hlCnt,
  prog:id=>{const F=hlFest(id);return{key:festKey(F),...festProg(F)};},order:()=>FEST.map(f=>f.id).join(",")};
}
