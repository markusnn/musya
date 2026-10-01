{
// ───────────────────────── «Кормушка для птиц»: a feeder in the courtyard; birds of Japan come by season, hour and weather ─────────────────────────
// S.ext.birds = {full: ms the seeds were poured (they last 2 h), mk: ms a mandarin slice was put, seen:{id:ms first sighting}, day: dayKey, td:[ids seen today],
//   n: visits, fe:{s:species,dx}|null — a feather lying on the ground}
const BI_R={"suzume_sit":[546,594,105,78,60,76],"suzume_peck":[0,694,108,69,59,66],"suzume_fly":[657,472,116,103,63,78],"mejiro_sit":[110,694,89,67,48,64],"mejiro_peck":[755,694,90,56,47,53],"mejiro_fly":[350,594,97,87,50,67],"uguisu_sit":[865,594,108,74,65,72],"uguisu_peck":[311,694,109,66,63,64],"uguisu_fly":[231,594,117,96,66,75],"tsubame_sit":[531,694,125,61,77,58],"tsubame_peck":[975,594,127,73,77,70],"tsubame_fly":[512,472,143,107,93,85],"hiyodori_sit":[339,472,171,109,108,106],"hiyodori_peck":[775,472,175,100,108,97],"hiyodori_fly":[476,286,193,143,118,110],"shijukara_sit":[760,594,103,75,61,72],"shijukara_peck":[422,694,107,65,60,62],"shijukara_fly":[116,594,113,97,63,75],"kawasemi_sit":[449,594,95,80,40,76],"kawasemi_peck":[658,694,95,58,45,54],"kawasemi_fly":[0,594,114,98,47,75],"yamagara_sit":[653,594,105,77,60,74],"yamagara_peck":[201,694,108,67,59,64],"yamagara_fly":[952,472,115,99,62,76],"tsugumi_sit":[0,472,167,120,100,117],"tsugumi_peck":[169,472,168,111,97,108],"tsugumi_fly":[292,286,182,152,104,116],"kijibato_sit":[887,286,215,136,126,134],"kijibato_peck":[671,286,214,139,123,136],"kijibato_fly":[329,0,228,212,131,159],"karasu_sit":[559,0,299,210,155,208],"karasu_peck":[860,0,284,189,152,186],"karasu_fly":[0,0,327,284,162,214],"fukuro_sit":[128,286,80,154,40,150],"fukuro_peck":[210,286,80,154,40,150],"fukuro_fly":[0,286,126,184,86,112]};
const BI_T={"feeder":[0,0,300,640,150,640],"seeds":[0,642,214,34],"mikan":[694,0,56,40],"bi_f_kawa":[512,0,58,193],"bi_f_fuku":[377,0,65,223],"bi_f_kiji":[444,0,66,203],"bi_f_kara":[302,0,73,243],"bi_hatobue":[572,0,120,75]};
const BI_A={bi:[1180,763],bi2:[760,676]},BI_IM={},BI_C="Перья и птичьи вещи";
const BI_FS=.8,BI_BS=1.05,BI_X=520,BI_Y=1162,BI_FULL=2*3600e3;   // image px per sprite px (feeder, birds — a bit larger than life), feeder foot, seeds last 2 h
const BI_TRAY=(640-298)*BI_FS,BI_ROOF=(640-102)*BI_FS;          // heights of the tray floor and the roof ridge above the foot (image px)
const BI_SPOT={tray:[[-56,BI_TRAY],[-8,BI_TRAY],[44,BI_TRAY]],roof:[[0,BI_ROOF],[-62,BI_ROOF-34],[62,BI_ROOF-34]],ground:[[-58,-8],[-22,-20],[24,-12],[62,-24],[96,-6]]};
// species: months, hours, weight, where they perch, card text, album hint
const BI_SP=[
 {id:"suzume",n:"Воробей",jp:"雀 · судзумэ",m:[],h:[5,19],w:5,at:["tray","ground"],line:"Самый частый гость. Прилетает стайкой, ссорится за зёрнышки и чирикает без умолку.",hint:"круглый год, днём"},
 {id:"mejiro",n:"Белоглазка",jp:"目白 · мэдзиро",m:[11,12,1,2,3,4],h:[6,17],w:2.5,at:["tray"],line:"Зелёная крошка с белым колечком вокруг глаза. Сластёна: за дольку мандарина прилетит в любое время года.",hint:"зима и весна, днём · любит мандарин"},
 {id:"uguisu",n:"Японская камышовка",jp:"鶯 · угуису",m:[2,3,4,5],h:[5,11],w:3,at:["ground","tray"],line:"Её песню «хо-хокэкё» в Японии ждут как первую весть о весне. Сама скромная, оливковая.",hint:"весна, утром"},
 {id:"tsubame",n:"Ласточка",jp:"燕 · цубамэ",m:[4,5,6,7,8],h:[5,19],w:3,at:["roof"],line:"Каждую весну возвращается под те же стрехи. Ласточкино гнездо над дверью — к счастью в доме.",hint:"лето, днём · садится на крышу"},
 {id:"hiyodori",n:"Бюльбюль",jp:"鵯 · хиёдори",m:[9,10,11,12,1,2,3,4,5],h:[5,18],w:2.5,at:["tray","roof"],line:"Шумная серая птица с рыжими щёчками. Кричит «пии-ё!» и запросто отнимает еду у мелких.",hint:"с осени до весны, днём"},
 {id:"shijukara",n:"Большая синица",jp:"四十雀 · сидзюкара",m:[],h:[6,18],w:3,at:["tray"],line:"Чёрный «галстук» на белой грудке. Имя пишется «сорок воробьёв» — шумит она за всех сорок.",hint:"круглый год, днём"},
 {id:"kawasemi",n:"Зимородок",jp:"翡翠 · кавасэми",m:[],h:[6,17],w:.45,at:["roof"],line:"Летающий самоцвет. Ныряет в пруд за мальком и тут же возвращается. Увидеть его — к удаче.",hint:"редкий гость у пруда, днём"},
 {id:"yamagara",n:"Разноцветная синица",jp:"山雀 · ямагара",m:[9,10,11,12,1,2,3],h:[6,17],w:2.5,at:["tray"],line:"Рыжая грудка и кремовые щёчки. В старину её учили вытаскивать предсказания омикудзи у храмов.",hint:"осень и зима, днём"},
 {id:"tsugumi",n:"Бурый дрозд",jp:"鶫 · цугуми",m:[11,12,1,2,3],h:[6,17],w:2.5,at:["ground"],line:"Прилетает из Сибири на зиму. Скачет по земле, замирает и гордо выпячивает пёструю грудь.",hint:"зима, днём · кормится на земле"},
 {id:"kijibato",n:"Большая горлица",jp:"雉鳩 · кидзибато",m:[],h:[5,18],w:2,at:["ground"],line:"Чешуйчатые рыжие перья и полосатая шейка. По утрам глухо воркует: «дэ-дэ-поппо».",hint:"круглый год, днём · ходит по земле"},
 {id:"karasu",n:"Ворона",jp:"烏 · карасу",m:[],h:[5,19],w:0,at:["ground"],line:"Умная и наглая. Когда корма мало, разгоняет мелочь и ест сама. В легендах ворона Ятагарасу вела первого императора.",hint:"прилетает, когда корма осталось мало"},
 {id:"fukuro",n:"Неясыть",jp:"梟 · фукуро",m:[],h:[21,4],w:0,at:["roof"],line:"Ночная тень с круглым лицом стережёт кормушку: к зёрнышкам бегают мыши. «Фукуро» звучит как «без бед» — сова считается оберегом.",hint:"только глубокой ночью, очень редко"}];
const BI_ID={};BI_SP.forEach(s=>BI_ID[s.id]=s);
const BI_FE={kawasemi:"bi_f_kawa",fukuro:"bi_f_fuku",kijibato:"bi_f_kiji",karasu:"bi_f_kara"};
const BI_BIG={kijibato:1,karasu:1,fukuro:1,tsugumi:1,hiyodori:1};
addItems([
 {id:"bi_f_kawa",n:"Перо зимородка",c:BI_C,w:58,h:193,a:"b",p:80,at:["bi2",512,0],src:"🐦 у кормушки",hint:"Его роняет зимородок, который ныряет в пруд у кормушки"},
 {id:"bi_f_fuku",n:"Совиное перо",c:BI_C,w:65,h:223,a:"b",p:120,at:["bi2",377,0],src:"🐦 у кормушки",hint:"Ночью у кормушки бывает сова — иногда она оставляет перо"},
 {id:"bi_f_kiji",n:"Перо горлицы",c:BI_C,w:66,h:203,a:"b",p:60,at:["bi2",444,0],src:"🐦 у кормушки",hint:"Горлица у кормушки во дворике иногда теряет перо"},
 {id:"bi_f_kara",n:"Воронье перо",c:BI_C,w:73,h:243,a:"b",p:60,at:["bi2",302,0],src:"🐦 у кормушки",hint:"Ворона прилетает, когда корма мало, и может обронить перо"},
 {id:"bi_hatobue",n:"Свистулька-голубок",c:BI_C,w:120,h:75,a:"b",p:90,at:["bi2",572,0],src:"🐦 у кормушки",hint:"Подарок за шесть видов птиц у кормушки во дворике"}],{bi2:BI_A.bi2});
STAMPS.push(["bi_first","鳥","Первая птица","Увидеть первую птицу у кормушки во дворике"],["bi_six","羽","Птичий двор","Увидеть у кормушки шесть видов птиц"],["bi_all","梟","Все птицы двора","Увидеть все 12 видов, даже ночную сову"]);
const biS=()=>S.ext.birds||(S.ext.birds={full:0,mk:0,seen:{},day:dayKey(),td:[],n:0,fe:null});
const biLvl=()=>{const B=biS();return B.full?clamp(1-(Date.now()-B.full)/BI_FULL,0,1):0;};
const biFull=()=>biLvl()>0;
const biMk=()=>{const B=biS();return !!B.mk&&biFull()&&B.mk>=B.full;};
const biSeenN=()=>Object.keys(biS().seen).length;
function biDay(){const h=hourNow();return h>=6&&h<19;}
function biNight(){const h=hourNow();return h>=21||h<4;}
function biLoad(){for(const k of ["bi","bi2"])if(!BI_IM[k])atlasImg(k,im=>{BI_IM[k]=im;});}
function biInH(s){const h=hourNow(),[a,b]=s.h;return a<b?h>=a&&h<b:h>=a||h<b;}
function biMins(){const m=Math.ceil(biLvl()*BI_FULL/6e4);return m>=60?`${Math.floor(m/60)} ч ${m%60?m%60+" мин":""}`.trim():m+" мин";}

// ── sounds: tiny WebAudio synth for the calls, Musya's «ka-ka-ka» chatter, wing flutter
function biNote(f0,f1,d,at=0,type="sine",vol=.05,vib=0){if(!snd.on||!snd.ctx)return;const c=snd.ctx,t=c.currentTime+at,o=c.createOscillator(),g=c.createGain();o.type=type;
  o.frequency.setValueAtTime(f0,t);o.frequency.exponentialRampToValueAtTime(f1,t+d);
  if(vib){const l=c.createOscillator(),lg=c.createGain();l.frequency.value=vib;lg.gain.value=f0*.035;l.connect(lg);lg.connect(o.frequency);l.start(t);l.stop(t+d+.05);}
  g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(vol,t+Math.min(.03,d*.3));g.gain.exponentialRampToValueAtTime(.0001,t+d);o.connect(g);g.connect(c.destination);o.start(t);o.stop(t+d+.05);}
const BI_CALL={
 uguisu:[[1050,1180,.85,0,"sine",.05,5],[2000,2500,.1,1.05],[2900,2500,.1,1.2],[2800,1900,.42,1.34,"sine",.05,9]],
 mejiro:[0,1,2,3,4,5,6,7,8].map(i=>[3100+(i*733)%900,3500+(i*397)%800,.05,i*.07,"sine",.03]),
 suzume:[[3600,2800,.08,0],[3500,2900,.08,.16],[3700,2700,.09,.45]],
 tsubame:[0,1,2,3,4,5,6].map(i=>[4200-i*80,3200,.06,i*.085,"triangle",.025]),
 hiyodori:[[2400,3300,.22,0,"triangle",.04],[3200,2100,.32,.26,"triangle",.04]],
 shijukara:[0,1,2].flatMap(i=>[[4300,4100,.06,i*.3],[3000,2900,.1,i*.3+.08]]),
 kawasemi:[[4800,4100,.16,0,"sine",.04],[4800,4000,.18,.3,"sine",.04]],
 yamagara:[[2300,2250,.22,0,"triangle",.03,30],[2300,2200,.24,.32,"triangle",.03,30],[3100,3000,.08,.7]],
 tsugumi:[[1900,1500,.09,0,"triangle",.04],[1900,1450,.1,.18,"triangle",.04]],
 kijibato:[[430,400,.24,0,"sine",.09],[410,380,.24,.32,"sine",.09],[450,420,.16,.75,"sine",.09],[420,360,.36,.95,"sine",.09]],
 karasu:[[640,470,.32,0,"sawtooth",.022],[620,450,.34,.5,"sawtooth",.022]],
 fukuro:[[360,340,.35,0,"sine",.1],[340,320,.45,.5,"sine",.1],[350,330,.2,1.4,"sine",.08],[330,320,.2,1.65,"sine",.08],[345,320,.45,1.9,"sine",.08]]};
function biCall(id){audioInit();for(const n of BI_CALL[id]||[])biNote(...n);}
function biChatter(){for(let i=0;i<4;i++)biNote(1350+rand(-80,80),1250,.045,.05+i*.075,"triangle",.03);}
function biFlutter(n=6){for(let i=0;i<n;i++)biNote(rand(160,260),rand(120,180),.04,i*.03,"triangle",.025);}

// ── geometry: the feeder's foot on the floor; local coords (dx right, dy up, image px) → stage
function biFrame(){const x=visX(BI_X,128),oc=curRow;curRow=BI_Y;const [bx,by]=imgToStage(x,BI_Y,CAT_D),[,ty]=imgToStage(x,BI_Y-100,CAT_D);curRow=oc;return{bx,by,k:(by-ty)/100,x};}
const biAt=(F,dx,dy)=>[F.bx+dx*F.k,F.by-dy*F.k];
function biSpr(im,r,x,y,s,flip,a=1,sy=1){if(!im||a<=0)return;ctx.save();ctx.globalAlpha*=a;ctx.translate(x,y);ctx.scale(flip?-1:1,sy);ctx.drawImage(im,r[0],r[1],r[2],r[3],-r[4]*s,-r[5]*s,r[2]*s,r[3]*s);ctx.restore();}

// ── birds in the room (runtime only)
const biB=[];let biNext=0,biZoomT=-99,biPour=-9,biSplash=null;
function biFree(kind){const L=BI_SPOT[kind];const used=biB.filter(b=>b.kind===kind&&b.ph!=="out").map(b=>b.spot);const f=L.map((_,i)=>i).filter(i=>!used.includes(i));return f.length?pick(f):-1;}
function biPos(b){return BI_SPOT[b.kind][b.spot];}
function biSpawn(id){const s=BI_ID[id];if(!s)return null;let kind=null,spot=-1;
  for(const k of [...s.at].sort(()=>Math.random()-.5)){spot=biFree(k);if(spot>=0){kind=k;break;}}if(spot<0)return null;
  if(id==="fukuro"){kind="roof";spot=0;}
  const p1=BI_SPOT[kind][spot],side=Math.random()<.5?-1:1,t=now();
  const b={id,kind,spot,ph:"in",t0:t,dur:id==="fukuro"?2.6:rand(1.4,2),p0:[p1[0]+side*rand(520,760),p1[1]+rand(240,420)],p1:[...p1],x:0,y:0,face:-side,pose:"sit",nb:t+3,until:t+(id==="fukuro"?rand(45,80):rand(14,30)),ph0:rand(0,6),pk:0,dives:id==="kawasemi"?1+(Math.random()<.5):0};
  b.x=b.p0[0];b.y=b.p0[1];biB.push(b);if(id!=="fukuro")biFlutter(4);return b;}
function biLeave(b,fast){if(b.ph==="out")return;const t=now(),side=Math.random()<.5?-1:1;b.p0=[b.x,b.y];b.p1=[b.x+side*rand(560,800),b.y+rand(260,460)];b.t0=t;b.dur=fast?rand(.9,1.3):rand(1.5,2.1);b.ph="out";b.face=side;
  const B=biS(),fe=BI_FE[b.id];if(fe&&!S.owned.has(fe)&&!B.fe&&!fast&&Math.random()<(b.id==="fukuro"?.7:.4)){B.fe={s:b.id,dx:clamp(b.x+rand(-30,30),-80,90)};save();tabDots();}}
function biScare(){let n=0;for(const b of biB)if(b.ph!=="out"&&b.id!=="fukuro"){biLeave(b,true);n++;}if(n)biFlutter(10);return n;}
// a bird has landed: first sighting → album, Musya notices
function biLand(b){const B=biS(),s=BI_ID[b.id],t=now(),first=!B.seen[b.id];b.ph="sit";b.nb=t+rand(.4,1.2);B.n=(B.n||0)+1;
  if(B.day!==dayKey()){B.day=dayKey();B.td=[];}if(!B.td.includes(b.id))B.td.push(b.id);
  if(!B.seen[b.id]){B.seen[b.id]=Date.now();disc("bird",b.id);chime([1175,1568]);toast(`🐦 Новая птица: ${s.n.toLowerCase()}`);const n=biSeenN();
    setTimeout(()=>{award("bi_first");if(n>=6&&!S.owned.has("bi_hatobue")){S.owned.add("bi_hatobue");save();award("bi_six");setTimeout(()=>toast("🎁 Свистулька-голубок — в «Вещах»"),2600);}
      if(n>=BI_SP.length)award("bi_all");},2000);}
  save();if(Math.random()<.55||first)setTimeout(()=>{if(biB.includes(b)&&b.ph==="sit")biCall(b.id);},rand(400,1400));
  if(b.id==="karasu"){let n=0;for(const o of biB)if(o!==b&&o.ph!=="out"&&o.id!=="fukuro"){biLeave(o,true);n++;}if(n)biFlutter(8);}
  if(petAway()||pet.action==="sleep"||scene.on)return;
  if(pet.action==="idle"&&Math.random()<.75){const F=biFrame(),[x,y]=biAt(F,b.x,b.y+20);pointer.x=x;pointer.y=y;pointer.known=true;pet.gazeUntil=now()+3.5;
    setTimeout(()=>{if(S.room==="courtyard"&&!petAway()){react(b.id==="karasu"?"🙀":"😼",1.8);biChatter();}},500);
    if(b.id!=="fukuro"&&b.id!=="karasu"&&Math.random()<.17&&t-biZoomT>90){biZoomT=t;setTimeout(()=>{if(S.room==="courtyard"&&pet.action==="idle"&&!petAway()&&biB.some(o=>o.ph==="sit"))start("zoomies",true);},2600);}}}
function biStep(t,dt){
  if(pet.action==="zoomies"&&t-pet.start>.4&&biB.some(b=>b.ph!=="out"&&b.id!=="fukuro"))biScare();
  for(let i=biB.length-1;i>=0;i--){const b=biB[i],s=BI_ID[b.id];
    if(b.ph==="in"||b.ph==="out"||b.ph==="hop"||b.ph==="dive"||b.ph==="back"){const u=clamp((t-b.t0)/b.dur,0,1),e=b.ph==="out"?u*u:smooth(u),arc=b.ph==="hop"?28:b.ph==="dive"?-30:90;
      b.x=mix(b.p0[0],b.p1[0],e);b.y=mix(b.p0[1],b.p1[1],e)+Math.sin(u*Math.PI)*arc*(b.ph==="in"?.6:1);
      if(u>=1){if(b.ph==="out"){biB.splice(i,1);continue;}
        if(b.ph==="in")biLand(b);else if(b.ph==="dive"){biSplash={x:b.x,y:b.y,t};sfx("splash");b.ph="back";b.p0=[b.x,b.y];b.p1=[...biPos(b)];b.t0=t;b.dur=1.1;b.face=b.p1[0]>b.x?1:-1;}
        else{b.ph="sit";b.nb=t+rand(.5,1.4);}}
      continue;}
    // sitting: peck, look around, hop, dive, leave
    if(!biFull()&&b.id!=="fukuro"&&t>b.until-8)b.until=Math.min(b.until,t+rand(1,4));
    if(t>b.until){biLeave(b);continue;}
    if(b.pk>0){if(t>b.nb){b.pose=b.pose==="peck"?"sit":"peck";b.pk--;b.nb=t+(b.pose==="peck"?.14:rand(.12,.3));if(b.pose==="peck"&&Math.random()<.3)biNote(rand(2400,3200),2200,.02,0,"triangle",.008);}continue;}
    if(t<b.nb)continue;b.pose="sit";const r=Math.random();
    if(b.id==="fukuro"&&r<.35){b.pose="peck";b.nb=t+rand(1.2,2.6);continue;}   // the owl dozes: eyes closed
    if(b.dives&&r<.35){b.dives--;b.ph="dive";b.p0=[b.x,b.y];b.p1=[clamp(b.x+rand(120,200),80,260),70];b.t0=t;b.dur=.8;b.face=1;continue;}
    if(r<.5&&b.kind!=="roof")b.pk=2*Math.floor(rand(2,4));
    else if(r<.72)b.face*=-1;
    else if(r<.86&&b.kind!=="roof"){const j=biFree(b.kind);if(j>=0){b.spot=j;b.ph="hop";b.p0=[b.x,b.y];b.p1=[...biPos(b)];b.t0=t;b.dur=.35;b.face=b.p1[0]>b.x?1:-1;continue;}}
    b.nb=t+rand(.5,1.6)*(b.id==="fukuro"?3:1);}
}
function biPool(){const m=today().getMonth()+1,B=biS(),lv=biLvl(),out=[];
  for(const s of BI_SP){if(s.id==="fukuro")continue;let w=s.w;
    if(s.id==="karasu")w=lv<.4?2.6:.25;
    if(s.id==="mejiro"&&biMk())w=s.m.includes(m)?w*4:3;else if(s.m.length&&!s.m.includes(m))continue;
    if(!biInH(s))continue;if(weather.on)w*=.35;if(s.id==="kijibato"&&hourNow()<9)w*=2;if(biB.some(b=>b.id===s.id&&s.id!=="suzume"))continue;
    if(w>0)out.push([s.id,w]);}
  return out;}
function biTry(){if(biB.some(b=>b.id==="karasu"&&b.ph!=="out"))return null;
  if(biNight()){if(!biB.length&&Math.random()<.06)return biSpawn("fukuro");return null;}
  if(!biDay())return null;const max=biLvl()>.5?3:2;if(biB.filter(b=>b.ph!=="out").length>=max)return null;
  const P=biPool();let tot=P.reduce((a,p)=>a+p[1],0),r=Math.random()*tot;for(const [id,w] of P){r-=w;if(r<=0)return biSpawn(id);}return null;}
hook("sec",()=>{const B=biS();if(B.day!==dayKey()){B.day=dayKey();B.td=[];}
  if(S.room!=="courtyard"||scene.on||overlaysOpen()||!biFull())return;if(now()<biNext)return;biNext=now()+rand(7,15);biTry();});
hook("tick",(t,dt)=>{if(S.room==="courtyard"&&biB.length)biStep(t,dt);});
hook("room",id=>{biB.length=0;biSplash=null;if(id==="courtyard"){biLoad();biNext=now()+rand(3,6);}});

// ── drawing: the feeder (seeds, mandarin), the birds, a feather on the ground
hook("draw",(t,front)=>{if(S.room!=="courtyard"||scene.on)return;if((BI_Y>catLineY()+6)!==front)return;biLoad();const im=BI_IM.bi2,ib=BI_IM.bi;if(!im)return;
  const F=biFrame(),s=F.k*BI_FS,sb=F.k*BI_BS,lv=biLvl(),B=biS();
  // soft contact shadow, the feeder, seeds
  ctx.fillStyle="rgba(6,8,8,.35)";ctx.beginPath();ctx.ellipse(F.bx+6*F.k,F.by-2*F.k,76*F.k,11*F.k,0,0,Math.PI*2);ctx.fill();
  biSpr(im,BI_T.feeder,F.bx,F.by,s,false);
  if(lv>0){const r=BI_T.seeds,h=(.3+.7*lv);const [x,y]=biAt(F,0,BI_TRAY-6);ctx.save();ctx.translate(x,y);ctx.scale(1,h);ctx.drawImage(im,r[0],r[1],r[2],r[3],-r[2]*s/2,-r[3]*s,r[2]*s,r[3]*s);ctx.restore();}
  if(biMk()){const r=BI_T.mikan,[x,y]=biAt(F,12,BI_TRAY-52);ctx.drawImage(im,r[0],r[1],r[2],r[3],x-r[2]*s*.3,y-r[3]*s*.5,r[2]*s*.75,r[3]*s*.75);}
  if(t-biPour<1.4)for(let i=0;i<14;i++){const u=((t-biPour)*1.6+i/14)%1,[x,y]=biAt(F,rand(-50,50),BI_TRAY+60-u*60);ctx.fillStyle=`rgba(230,210,160,${.8*(1-u)})`;ctx.fillRect(x,y,2.2*F.k*2,2.2*F.k*2);}
  if(B.fe){const r=BI_T[BI_FE[B.fe.s]],[x,y]=biAt(F,B.fe.dx,-12);ctx.save();ctx.translate(x,y);ctx.rotate(-1.35);ctx.drawImage(im,r[0],r[1],r[2],r[3]-34,-r[2]*s*.4,-(r[3]-34)*s*.4,r[2]*s*.8,(r[3]-34)*s*.8);ctx.restore();
    if(Math.sin(t*2.2)>.97&&Math.random()<.2)floatFx.push({g:"✨",x,y:y-8*F.k,t:now()});}
  // kingfisher splash rings
  if(biSplash){const e=t-biSplash.t;if(e<1.4){const [x,y]=biAt(F,biSplash.x,biSplash.y);ctx.strokeStyle=`rgba(220,232,236,${.7*(1-e/1.4)})`;ctx.lineWidth=1.5;for(const k of[1,.6]){ctx.beginPath();ctx.ellipse(x,y,(8+60*e*k)*F.k,(2+14*e*k)*F.k,0,0,Math.PI*2);ctx.stroke();}}else biSplash=null;}
  if(!ib)return;
  for(const b of biB){const r0=BI_R[b.id+"_sit"],[x,y]=biAt(F,b.x,b.y),fl=b.face<0;
    if(b.ph==="sit"){if(b.kind!=="roof"){ctx.fillStyle="rgba(6,8,8,.3)";ctx.beginPath();ctx.ellipse(x,y,r0[2]*sb*.32,3*F.k,0,0,Math.PI*2);ctx.fill();}
      const breathe=1+.015*Math.sin(t*3+b.ph0);biSpr(ib,BI_R[b.id+"_"+b.pose],x,y,sb,fl,1,breathe);continue;}
    // in the air: small birds alternate flaps with folded-wing bounds, big ones flap
    const big=BI_BIG[b.id],fr=Math.sin(t*(big?9:26)+b.ph0),r=BI_R[b.id+"_fly"],cy=y-r0[5]*sb*.45;
    if(!big&&fr<-.55)biSpr(ib,r0,x,y,sb,fl);else biSpr(ib,r,x,cy,sb,fl,1,big?.8+.2*fr:1);}
});

// ── actions
function biFill(){const B=biS();audioInit();if(biFull()&&biLvl()>.85){toast("Кормушка и так полная");return;}
  B.full=Date.now();biPour=now();biNext=now()+rand(3,6);save();ui();tabDots();sfx("pop");for(let i=0;i<8;i++)setTimeout(()=>biNote(rand(2500,4200),rand(2000,3000),.02,0,"triangle",.012),i*70);
  if(!petAway()&&pet.action!=="sleep"){walkTo({x:biFrame().x+190},"idle");setTimeout(()=>react("😺",1.6),1200);}
  toast(biDay()||biNight()?"🌾 Корм насыпан — жди гостей":"🌾 Корм насыпан — птицы прилетят днём");}
function biMikan(){const B=biS();if(!biFull()){biFill();return;}if(biMk()){toast("Долька мандарина уже на гвоздике");return;}B.mk=Date.now();save();ui();sfx("pop");toast("🍊 Долька мандарина — для белоглазок");}
function biThumb(key,mw,mh,cls=""){const r=BI_R[key]||BI_T[key],A=BI_R[key]?BI_A.bi:BI_A.bi2,at=BI_R[key]?"bi":"bi2",k=Math.min(mw/r[2],mh/r[3]),f=v=>(v*k).toFixed(1);
  return`<span class="${cls}" style="display:inline-block;flex:none;width:${f(r[2])}px;height:${f(r[3])}px;background:url(assets/items/atlas_${at}.webp) -${f(r[0])}px -${f(r[1])}px/${f(A[0])}px ${f(A[1])}px no-repeat"></span>`;}
function biCard(id){const s=BI_ID[id];biCall(id);dlg({head:`${s.n} · ${s.jp}`,text:s.line,img:biThumb(id+"_sit",96,80),ok:"Красиво",no:"🔊 Голос",onNo:()=>biCard(id)});}
function biTap(x,y){const F=biFrame(),sb=F.k*BI_BS;let best=null,bd=1e9;
  for(const b of biB){const r=BI_R[b.id+"_sit"],[bx,by]=biAt(F,b.x,b.y),w=Math.max(30,r[2]*sb*.6),h=Math.max(30,r[3]*sb);
    if(Math.abs(x-bx)<w&&y<by+10&&y>by-h-10){const d=Math.abs(x-bx)+Math.abs(y-(by-h/2));if(d<bd){bd=d;best=b;}}}
  return best;}
hook("hit",(x,y)=>{if(S.room!=="courtyard"||scene.on)return;const F=biFrame(),B=biS();
  const b=biTap(x,y);if(b){audioInit();biCard(b.id);if(b.ph==="sit"&&Math.random()<.25)setTimeout(()=>biLeave(b),900);return true;}
  if(B.fe){const [fx,fy]=biAt(F,B.fe.dx,-12);if(Math.abs(x-fx)<40*F.k+14&&Math.abs(y-fy)<26*F.k+14){const id=BI_FE[B.fe.s];B.fe=null;S.owned.add(id);save();tabDots();audioInit();chime([988,1318,1568]);toast(`🪶 ${IT[id].n} — в «Вещах»`);return true;}}
  const s=F.k*BI_FS;if(Math.abs(x-F.bx)<100*s&&y<F.by-150*s&&y>F.by-560*s){audioInit();
    if(!biFull())biFill();else{const B2=biS(),nm=B2.td.map(i=>BI_ID[i].n.toLowerCase());tone(520,.08,"triangle",.04);toast(`🌾 Корма хватит на ${biMins()}`+(nm.length?` · ${nm.length} вид. сегодня`:""));}return true;}});
hook("tray",(tray,room)=>{if(room!=="courtyard"||(S.trayMode[room]||"play")!=="play")return;const el=tray.querySelector(".items");if(!el)return;
  const b=!biFull()?["bi:fill","🌾","Насыпать корм"]:!biMk()?["bi:mikan","🍊","Дольку мандарина"]:["bi:info","🐦",`Кормушка · ${Math.round(biLvl()*100)}%`];
  const html=`<button class="item wide" data-x="${b[0]}"><span class="ico">${b[1]}</span><span class="nm">${b[2]}</span></button>`,w=el.querySelectorAll(".item.wide");
  if(w.length)w[w.length-1].insertAdjacentHTML("afterend",html);else el.insertAdjacentHTML("afterbegin",html);});
hook("click",k=>{if(!k.startsWith("bi:"))return;
  if(k==="bi:fill")biFill();else if(k==="bi:mikan")biMikan();
  else if(k==="bi:info"){const nm=biS().td.map(i=>BI_ID[i].n.toLowerCase());toast(nm.length?`🐦 Сегодня: ${nm.slice(-3).join(", ")}`.slice(0,45):`🌾 Корма хватит на ${biMins()}`);}
  else if(k==="bi:go"||k==="bi:hubfill"){closePanel();goRoom("courtyard");if(k==="bi:hubfill")setTimeout(biFill,600);}
  return true;});
hook("hubDot",()=>!biFull()&&biDay());
hook("tabDot",r=>r==="courtyard"&&!!biS().fe);
hook("away",ms=>{const B=biS();if(B.full&&ms>3600e3&&saved&&saved.t&&saved.t-B.full<BI_FULL&&!biFull())return{i:"🌾",t:"Кормушка во дворике опустела — птицы ждут корма"};});
hook("hub",()=>{const B=biS(),n=biSeenN(),td=(B.day===dayKey()?B.td:[]).map(i=>BI_ID[i]);
  const st=biFull()?`Корм есть — хватит на ${biMins()}.${biMk()?" На гвоздике долька мандарина.":""}`:biDay()?"Кормушка пустая — птицы пролетают мимо.":"Кормушка пустая. Насыпь корм — утром прилетят птицы.";
  return`<div class="hubc"><h4>🐦 Кормушка <i>餌台</i></h4><p>${st}</p><p>Видели птиц: ${n} из ${BI_SP.length}.${td.length?" Сегодня прилетали:":""}</p>${td.length?`<div class="bi-row">${td.map(s=>`<span title="${s.n}">${biThumb(s.id+"_sit",54,40)}<small>${s.n}</small></span>`).join("")}</div>`:""}
  <div class="row">${biFull()?"":`<button class="btn primary" data-x="bi:hubfill">🌾 Насыпать корм</button>`}<button class="btn" data-x="bi:go">Во дворик</button></div></div>`;});
hook("album",el=>{const B=biS(),n=biSeenN();
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Птицы</h3><p class="lead">У кормушки во дворике побывало ${n} из ${BI_SP.length} видов. Птицы прилетают днём, когда в кормушке есть корм, и каждая — в своё время года.</p><div class="coll">${BI_SP.map(s=>{const on=!!B.seen[s.id];
    return`<div class="ci ${on?"on":""}">${biThumb(s.id+"_sit",64,52,"ath")}<small>${on?`${s.n}<br><i>${s.jp}</i>`:`???<br>${s.hint}`}</small></div>`;}).join("")}</div>`);});
document.head.insertAdjacentHTML("beforeend","<style>.bi-row{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 4px}.bi-row>span{display:flex;flex-direction:column;align-items:center;gap:2px;width:64px}.bi-row small{font-size:10px;line-height:1.15;text-align:center;color:var(--muted)}</style>");
hook("boot",()=>{biS();if(S.room==="courtyard"){biLoad();biNext=now()+rand(3,6);}});
// test handles
X.birds={st:biS,list:biB,spawn:biSpawn,fill:biFill,mikan:biMikan,card:biCard,call:biCall,scare:biScare,lvl:biLvl,frame:biFrame,
  tap(i=0){const b=biB[i];if(!b)return;const F=biFrame(),r=BI_R[b.id+"_sit"],[x,y]=biAt(F,b.x,b.y),rc=cv.getBoundingClientRect();
    cv.dispatchEvent(new PointerEvent("pointerdown",{clientX:rc.left+x,clientY:rc.top+y-r[3]*BI_BS*F.k*.45,bubbles:true,pointerId:1,isPrimary:true}));},
  tapFe(){const B=biS();if(!B.fe)return;const F=biFrame(),[x,y]=biAt(F,B.fe.dx,-12),rc=cv.getBoundingClientRect();cv.dispatchEvent(new PointerEvent("pointerdown",{clientX:rc.left+x,clientY:rc.top+y,bubbles:true,pointerId:1,isPrimary:true}));},
  land(){for(const b of biB)if(b.ph==="in"){b.t0=now()-b.dur;}},reset(){biNext=now()+999;}};
}
