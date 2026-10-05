{
// ───────────────────────── «Сачок и насекомые»: insects of Japan by real season, hour and room; a net, a card, a singing cricket cage ─────────────────────────
// S.ext.insects = {seen:{id:ms first recorded}, n:{id:times caught}, cage:"suzumushi"|"matsumushi"|null, net:0|1 (net mode), day, td:[ids caught today]}
const MU_R={"kabuto0":[472,0,84,128],"kuwagata0":[644,0,80,124],"minmin0":[874,264,80,104],"fuyu0":[294,390,96,84],"tento0":[396,496,60,60],"hotaru0":[778,390,52,66],"ageha0":[606,264,132,112],"monshiro0":[82,390,104,88],"akatombo0":[726,0,132,124],"shiokara0":[860,0,132,124],"suzumushi0":[832,390,112,66],"matsumushi0":[0,496,112,66],"batta0":[490,390,142,70],"kamakiri0":[350,264,126,120],"kabuto1":[558,0,84,128],"kuwagata1":[0,264,80,124],"minmin1":[0,390,80,104],"fuyu1":[392,390,96,84],"tento1":[458,496,60,60],"hotaru1":[114,496,52,66],"ageha1":[740,264,132,112],"monshiro1":[188,390,104,88],"akatombo1":[82,264,132,124],"shiokara1":[216,264,132,124],"suzumushi1":[168,496,112,66],"matsumushi1":[282,496,112,66],"batta1":[634,390,142,70],"kamakiri1":[478,264,126,120],"mu_ami":[0,0,112,262],"mu_kago":[114,0,150,172],"mu_hako":[266,0,204,160]};
const MU_A=[1024,562],MU_C="Насекомые",MU_OUT=["courtyard","engawa","entrance","games","hokora"];
// species: months, hours [from,to), kind (fly = flies a path / sit = sits on a perch), view (d = from above, head up / s = side, facing right),
// perches (T trunk or post, L leaf or bush, G ground or stone), weight, sprite scale (image px per sprite px), short name for the hub line
const MU_SP=[
 {id:"ageha",n:"Бабочка-парусник агэха",sn:"агэха",jp:"揚羽 · агэха",m:[4,5,6,7,8,9],h:[7,17.5],k:"fly",v:"d",at:["L"],w:2,s:1.3,
  line:"Большая жёлто-чёрная бабочка с «хвостиками» на задних крыльях. Летает по своим «бабочкиным тропам»: где пролетела вчера, там пролетит и сегодня. Её силуэт был гербом древнего рода Тайра.",hint:"весна и лето, днём"},
 {id:"monshiro",n:"Капустница",sn:"капустница",jp:"紋白蝶 · монсиро-тё",m:[3,4,5,6],h:[7,17],k:"fly",v:"d",at:["L","G"],w:3,s:1.25,
  line:"С неё в Японии начинается весна. Про неё малыши поют самую первую песенку: «Тётё, тётё, сядь на листок рапса».",hint:"весна, днём"},
 {id:"tento",n:"Божья коровка",sn:"божья коровка",jp:"七星天道 · нанахоси-тэнто",m:[3,4,5,6,10,11],h:[8,17],k:"sit",v:"d",at:["L","T","G"],w:2.5,s:1.5,
  line:"«Тэнто» — «небесная дорога», так зовут солнце. Она всегда ползёт на самый кончик травинки и оттуда взлетает прямо к солнцу.",hint:"весна и поздняя осень, днём"},
 {id:"kabuto",n:"Жук-носорог кабутомуси",sn:"кабутомуси",jp:"兜虫 · кабутомуси",m:[7,8],h:[19,4],k:"sit",v:"d",at:["T"],w:2.5,s:1.3,
  line:"«Жук в шлеме» — летний герой японских детей. Ночью они с фонариком идут к дубам за кабутомуси, а потом устраивают жучиное сумо: кто кого столкнёт с ветки.",hint:"лето, ночью · на стволах"},
 {id:"kuwagata",n:"Жук-олень кувагата",sn:"кувагата",jp:"鍬形 · кувагата",m:[6,7,8],h:[19,4],k:"sit",v:"d",at:["T"],w:1,s:1.3,rare:1,
  line:"Рога-клешни похожи на украшение старинного самурайского шлема «кувагата» — отсюда и имя. Найти его труднее, чем кабутомуси, и мальчишки ценят его дороже.",hint:"начало лета, ночью · редкий"},
 {id:"minmin",n:"Цикада минмин",sn:"цикада минмин",jp:"ミンミン蝉 · минмин-дзэми",m:[7,8,9],h:[8,17],k:"sit",v:"d",at:["T"],w:3,s:1.25,song:1,
  line:"Поёт «мин-мин-мин-миии…» — это и есть звук японского лета. Под землёй личинка живёт несколько лет, а на дереве цикада поёт всего пару недель.",hint:"лето, днём · на стволах"},
 {id:"hotaru",n:"Светлячок гэндзи",sn:"светлячки",jp:"源氏蛍 · гэндзи-ботару",m:[6,7],h:[19,23.5],k:"fly",v:"d",at:["L"],w:2,s:1.2,rare:1,glow:1,
  line:"Мигает зелёным медленно, будто дышит. Летними вечерами в старину ходили на «хотару-гари» — ловить светлячков веером, а потом сажали их в бумажный фонарик.",hint:"июнь и июль, вечером · редкий"},
 {id:"shiokara",n:"Стрекоза сиокара",sn:"сиокара",jp:"塩辛蜻蛉 · сиокара-тонбо",m:[5,6,7,8,9],h:[8,17.5],k:"fly",v:"d",at:["G","L"],w:2,s:1.2,dfly:1,
  line:"Самец голубовато-серый, будто присыпан солью, — отсюда имя «солёная». Любит садиться на один и тот же камень и охранять свой кусочек сада.",hint:"с мая по сентябрь, днём"},
 {id:"akatombo",n:"Красная стрекоза акатомбо",sn:"акатомбо",jp:"赤蜻蛉 · акатомбо",m:[9,10,11],h:[8,17.5],k:"fly",v:"d",at:["G","L"],w:3.5,s:1.2,dfly:1,
  line:"Лето она проводит в горах, а осенью спускается в деревни и краснеет. Песню «Акатомбо» про вечернюю зарю и красную стрекозу знает каждый японец.",hint:"осень, днём"},
 {id:"suzumushi",n:"Сверчок судзумуси",sn:"судзумуси",jp:"鈴虫 · судзумуси",m:[8,9,10],h:[17.5,3],k:"sit",v:"s",at:["G"],w:3,s:1.45,song:1,
  line:"Поёт «рии-ин», как крошечный колокольчик. Ещё при дворе Хэйан осенними вечерами «слушали насекомых» — муси-кики, а позже сверчков стали держать дома в бамбуковых клетках.",hint:"осень, вечером и ночью · в траве"},
 {id:"matsumushi",n:"Сверчок мацумуси",sn:"мацумуси",jp:"松虫 · мацумуси",m:[8,9,10],h:[17.5,3],k:"sit",v:"s",at:["G"],w:2.5,s:1.45,song:1,
  line:"Его песня — звонкое «чин-чирорин». Говорят, во времена «Повести о Гэндзи» его звали судзумуси, а судзумуси — мацумуси: с тех пор имена поменялись местами.",hint:"осень, вечером и ночью · в траве"},
 {id:"batta",n:"Кузнечик тоносама-батта",sn:"кузнечик",jp:"殿様飛蝗 · тоносама-батта",m:[7,8,9,10,11],h:[7,17.5],k:"sit",v:"s",at:["G"],w:2.5,s:1.35,jump:1,
  line:"«Кузнечик-князь» — самый крупный и важный на лугу. Подпускает совсем близко, а потом прыгает так далеко, что глазом не уследишь.",hint:"с лета до поздней осени, днём"},
 {id:"kamakiri",n:"Богомол",sn:"богомол",jp:"蟷螂 · камакири",m:[8,9,10,11],h:[7,18.5],k:"sit",v:"s",at:["G","L"],w:2,s:1.35,
  line:"Стоит, сложив лапки, будто молится, и поворачивает голову тебе вслед. Осенью богомолиха прячет пенный кокон с яйцами — по его высоте старики гадают, сколько выпадет снега.",hint:"конец лета и осень, днём"},
 {id:"fuyu",n:"Спящая бабочка рури-татэха",sn:"спящая бабочка",jp:"瑠璃立羽 · рури-татэха",m:[12,1,2],h:[0,24],k:"sit",v:"d",at:["T"],w:.6,s:1.15,rare:1,still:1,
  line:"Зимует взрослой: складывает крылья и становится похожа на кусочек коры. В тёплый полдень может на миг раскрыть их — и мелькнёт лазурная полоса.",hint:"зима · спит на коре, очень редко"}];
const MU_ID={};MU_SP.forEach(s=>MU_ID[s.id]=s);
// perches per room (image x, y, depth): T on trunks/posts, L on bushes, G on the ground; F = the air where flyers wander [x0,x1,y0,y1,d]
const MU_RM={
 courtyard:{T:[],L:[[1290,1150,.8]],G:[[1150,1228,.8],[1268,1262,.8],[1345,1200,.8]],F:[880,1360,640,1000,.8]},
 engawa:{T:[[652,820,.42],[1215,700,.42]],L:[[540,985,.42],[1060,990,.42],[790,1000,.42]],G:[[600,1190,.8],[1300,1250,.8]],F:[460,1340,700,1000,.8]},
 entrance:{T:[[1136,780,.38],[1136,620,.38]],L:[],G:[[1180,1110,.8],[1260,1190,.8],[1070,1250,.8]],F:[700,1320,520,940,.8]},
 games:{T:[[1176,820,.45],[636,860,.45]],L:[],G:[[1250,1235,.8],[560,1245,.8],[1110,1300,.8]],F:[640,1320,560,1000,.8]},
 hokora:{T:[[548,800,.22],[520,560,.22]],L:[],G:[[1240,1180,.8],[660,1250,.8],[1150,1290,.8]],F:[650,1300,440,940,.8]}};
addItems([
 {id:"mu_ami",n:"Сачок",c:MU_C,w:112,h:262,a:"b",p:60,at:["mu",0,0],src:"🥅 первый улов",hint:"Поймай сачком первое насекомое во дворе или в саду"},
 {id:"mu_kago",n:"Клетка для сверчка",c:MU_C,w:150,h:172,a:"b",p:140,at:["mu",114,0],src:"🥅 осенний улов",hint:"Поймай осенним вечером сверчка судзумуси или мацумуси"},
 {id:"mu_hako",n:"Ящик с коллекцией",c:MU_C,w:204,h:160,a:"b",p:180,at:["mu",266,0],src:"🥅 семь видов",hint:"Собери в альбом семь видов насекомых"}],{mu:MU_A});
STAMPS.push(["mu_first","虫","Первый улов","Поймать сачком первое насекомое"],["mu_seven","網","Юный энтомолог","Собрать в альбом семь видов насекомых"],["mu_all","蟲","Все насекомые сада","Собрать все 14 насекомых — в каждый сезон"]);
const muS=()=>S.ext.insects||(S.ext.insects={seen:{},n:{},cage:null,net:0,day:dayKey(),td:[]});
const muSeenN=()=>Object.keys(muS().seen).length;
const MU_MON=["январе","феврале","марте","апреле","мае","июне","июле","августе","сентябре","октябре","ноябре","декабре"];
function muInH(s,h=hourNow()){const [a,b]=s.h;return a<b?h>=a&&h<b:h>=a||h<b;}
function muNowSp(room){const m=today().getMonth()+1;return MU_SP.filter(s=>s.m.includes(m)&&muInH(s)&&(!room||s.at.some(k=>(MU_RM[room][k]||[]).length)));}
function muPart(h=hourNow()){return h>=5&&h<11?"утром":h>=11&&h<17?"днём":h>=17&&h<22?"вечером":"ночью";}
function muList(a){return a.length<2?a.join(""):a.slice(0,-1).join(", ")+" и "+a[a.length-1];}
function muStatus(){const L=muNowSp(null),w=`Сейчас, в ${MU_MON[today().getMonth()]} ${muPart()}`;
  if(!L.length)return`${w}, насекомые спят.`+(today().getMonth()+1<=2||today().getMonth()+1===12?" Разве что на коре найдётся спящая бабочка.":" Загляни в сад в другое время.");
  return`${w}: ${muList(L.map(s=>s.sn))}.`;}
function muRareNow(){return !weather.on&&muNowSp(null).some(s=>s.rare&&!muS().seen[s.id]);}

// ── sounds: songs of the singers, a whoosh of the net
function muNote(f0,f1,d,at=0,type="sine",vol=.03,am=0){if(!snd.on||!snd.ctx)return;const c=snd.ctx,t=c.currentTime+at,o=c.createOscillator(),g=c.createGain();o.type=type;
  o.frequency.setValueAtTime(f0,t);o.frequency.exponentialRampToValueAtTime(f1,t+d);g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(vol,t+Math.min(.02,d*.3));g.gain.exponentialRampToValueAtTime(.0001,t+d);
  if(am){const l=c.createOscillator(),lg=c.createGain(),m=c.createGain();l.frequency.value=am;lg.gain.value=.5;m.gain.value=.5;l.connect(lg);lg.connect(m.gain);o.connect(m);m.connect(g);l.start(t);l.stop(t+d+.05);}else o.connect(g);
  g.connect(c.destination);o.start(t);o.stop(t+d+.05);}
function muSong(id,v=1){audioInit();const q=.028*v;
  if(id==="suzumushi"){muNote(4300,4250,.55,0,"sine",q,38);muNote(4300,4250,.6,.8,"sine",q,38);}
  else if(id==="matsumushi"){muNote(3500,3450,.07,0,"sine",q);muNote(3300,3250,.05,.16,"sine",q);muNote(3600,3550,.05,.26,"sine",q);muNote(3700,3600,.42,.36,"sine",q,30);}
  else if(id==="minmin"){for(let i=0;i<4;i++)muNote(1500,2300,i<3?.2:.7,i*.26,"sawtooth",.012*v,46);}}
function muWhoosh(){audioInit();muNote(900,260,.18,0,"triangle",.02);muNote(500,180,.2,.03,"sine",.02);}

// ── sprites: the atlas tinted to the room light (one cached canvas per tint)
const MU_IM={a:null,t:{}};
function muLoad(){if(!MU_IM.a)atlasImg("mu",im=>{MU_IM.a=im;});}
function muAtlas(){const im=MU_IM.a;if(!im)return null;const tn=TINT[S.room]||DTINT[bgName()]||"";if(!tn)return im;let c=MU_IM.t[tn];
  if(!c){c=document.createElement("canvas");c.width=im.naturalWidth||im.width;c.height=im.naturalHeight||im.height;const g=c.getContext("2d");g.drawImage(im,0,0);g.globalCompositeOperation="source-atop";g.fillStyle=tn;g.fillRect(0,0,c.width,c.height);MU_IM.t[tn]=c;}
  return c;}
function muSpr(g,im,key,x,y,sc,rot=0,flip=false,a=1){const r=MU_R[key];if(!r||!im||a<=0)return;g.save();g.globalAlpha*=a;g.translate(x,y);if(rot)g.rotate(rot);g.scale(flip?-sc:sc,sc);g.drawImage(im,r[0],r[1],r[2],r[3],-r[2]/2,-r[3]/2,r[2],r[3]);g.restore();}
function muThumb(key,mw,mh,cls=""){const r=MU_R[key],k=Math.min(mw/r[2],mh/r[3]),f=v=>(v*k).toFixed(1);
  return`<span class="${cls}" style="display:inline-block;flex:none;width:${f(r[2])}px;height:${f(r[3])}px;background:url(assets/items/atlas_mu.webp) -${f(r[0])}px -${f(r[1])}px/${f(MU_A[0])}px ${f(MU_A[1])}px no-repeat"></span>`;}

// ── insects in the room (runtime only)
const muB=[];let muNext=0,muNet=null,muDbg=0,MU_K=.5;
const muPt=(x,y,d)=>{const oc=curRow;curRow=null;const p=imgToStage(x,y,d);curRow=oc;return p;};
function muFree(room,kinds){const R=MU_RM[room],out=[];for(const k of kinds)for(const p of R[k]||[])if(!muB.some(b=>b.pr===p))out.push([k,p]);return out;}
function muRndF(F){return[rand(F[0],F[1]),rand(F[2],F[3])];}
function muSpawn(id,room=S.room){const s=MU_ID[id],R=MU_RM[room];if(!s||!R)return null;const t=now();
  const b={id,s,st:"in",t0:t,a:0,x:0,y:0,d:.8,pr:null,pk:null,face:Math.random()<.5?1:-1,rot:0,ph:rand(0,6),fr:0,frT:0,until:t+rand(25,50),tx:0,ty:0,sp:0,hov:0,land:0,sx:-999,sy:-999,r:0};
  if(s.k==="fly"){const F=R.F,side=Math.random()<.5?-1:1;b.d=F[4];b.x=(side<0?F[0]-260:F[1]+260);b.y=rand(F[2],F[3]);[b.tx,b.ty]=muRndF(F);b.st="fly";b.a=1;b.sp=s.dfly?420:s.glow?60:150;}
  else{const fr=muFree(room,s.at);if(!fr.length)return null;const [k,p]=pick(fr);b.pr=p;b.pk=k;b.x=p[0];b.y=p[1];b.d=p[2];b.rot=k==="T"?rand(-.25,.25):k==="L"&&s.v==="d"?rand(-.7,.7):0;
    if(s.v==="d"&&k==="G")b.rot=rand(-1.4,1.4);b.y0=b.y;b.x0=b.x;if(k==="T")b.y=p[1]+40;else b.x=p[0]-b.face*30;}
  muB.push(b);return b;}
function muLeave(b,fast){if(b.st==="out"||b.st==="gone")return;const s=b.s,t=now();
  if(s.k==="fly"||s.id==="minmin"||s.id==="tento"&&fast){const F=MU_RM[S.room].F;b.st="fly";b.pr=null;b.d=F?F[4]:.8;b.tx=b.x+(Math.random()<.5?-1:1)*rand(900,1200);b.ty=b.y-rand(200,420);b.sp=(s.dfly?700:s.glow?120:320)*(fast?1.6:1);b.leaving=1;return;}
  if(s.jump){b.st="jump";b.t0=t;b.jx0=b.x;b.jy0=b.y;b.jx1=b.x+(Math.random()<.5?-1:1)*rand(500,700);b.jy1=b.y+rand(-20,30);b.leaving=1;return;}
  b.st="out";b.t0=t;}
function muDodge(b){const s=b.s,F=MU_RM[S.room].F;
  if(s.k==="fly"){b.st="fly";b.pr=null;b.hov=0;b.land=0;b.d=F[4];const [x,y]=muRndF(F);b.tx=clamp(b.x+(x>b.x?1:-1)*rand(260,420),F[0],F[1]);b.ty=clamp(y-rand(40,140),F[2]-80,F[3]);b.sp=(s.dfly?900:s.glow?200:420);return;}
  if(s.jump){const fr=muFree(S.room,s.at);if(fr.length&&Math.random()<.6){const [k,p]=pick(fr);b.st="jump";b.t0=now();b.jx0=b.x;b.jy0=b.y;b.jx1=p[0];b.jy1=p[1];b.pr=p;b.pk=k;return;}}
  muLeave(b,true);}
function muStep(t,dt){const R=MU_RM[S.room];if(!R)return;
  for(let i=muB.length-1;i>=0;i--){const b=muB[i],s=b.s;
    if(b.st==="gone"){muB.splice(i,1);continue;}
    if(b.st==="in"){const u=clamp((t-b.t0)/1.2,0,1);b.a=u;b.x=mix(b.x,b.x0,Math.min(1,dt*3));b.y=mix(b.y,b.y0,Math.min(1,dt*3));if(u>=1){b.st="sit";b.x=b.x0;b.y=b.y0;}continue;}
    if(b.st==="out"){b.a=1-clamp((t-b.t0)/.9,0,1);if(b.pk==="T")b.y+=dt*30;if(b.a<=0)muB.splice(i,1);continue;}
    if(b.st==="jump"){const u=clamp((t-b.t0)/.55,0,1);b.x=mix(b.jx0,b.jx1,u);b.y=mix(b.jy0,b.jy1,u)-Math.sin(u*Math.PI)*160;b.face=b.jx1>b.jx0?1:-1;
      if(u>=1){if(b.leaving){muB.splice(i,1);continue;}b.st="sit";b.x0=b.x;b.y0=b.y;}continue;}
    if(b.st==="sit"){if(t>b.until){muLeave(b);continue;}
      if(t>b.frT){b.fr=b.fr?0:1;b.frT=t+(b.fr?(s.song&&dayTint()[1]?rand(1.2,3):rand(.25,.6)):rand(1.2,4));if(s.still&&b.fr)b.frT=t+rand(.6,1.2);
        if(s.still&&b.fr&&Math.random()<.6){b.fr=0;b.frT=t+rand(3,8);}
        if(s.song&&b.fr&&(s.id==="minmin"?!dayTint()[1]:dayTint()[1])&&Math.random()<.5)muSong(s.id,.35);}
      if(s.id==="tento"&&b.pk!=="G"){b.y=b.y0-Math.sin((t-b.t0)*.4+b.ph)*6;}
      if(s.k==="fly"&&t>b.land){b.st="fly";b.pr=null;b.d=R.F[4];[b.tx,b.ty]=muRndF(R.F);b.sp=s.dfly?420:s.glow?60:150;}
      continue;}
    // flying: butterflies meander, dragonflies dart and hover, fireflies drift
    if(b.hov>t)continue;
    const dx=b.tx-b.x,dy=b.ty-b.y,dd=Math.hypot(dx,dy),stp=b.sp*dt;
    if(dd<=stp+2){b.x=b.tx;b.y=b.ty;
      if(b.leaving){muB.splice(i,1);continue;}
      if(b.landing){b.landing=0;b.st="sit";b.pr=b.lp;b.pk=b.lk;b.x0=b.x;b.y0=b.y;b.land=t+rand(4,9);b.rot=s.dfly?(b.face>0?1.5:-1.5):rand(-.4,.4);b.fr=0;continue;}
      if(t>b.until){muLeave(b);continue;}
      if(s.dfly)b.hov=t+rand(.5,1.6);
      const fr=s.at.length?muFree(S.room,s.at):[];
      if(fr.length&&Math.random()<(s.dfly?.3:.22)){const [k,p]=pick(fr);
        // land: switch to the perch's plane (image coords match from the home camera, only a little parallax jumps)
        b.d=p[2];b.tx=p[0];b.ty=p[1]-6;b.landing=1;b.lp=p;b.lk=k;}
      else[b.tx,b.ty]=muRndF(R.F);
      b.sp=s.dfly?rand(380,560):s.glow?rand(40,70):rand(110,170);continue;}
    let vx=dx/dd*stp,vy=dy/dd*stp;
    if(!s.dfly){const w=s.glow?.6:1.4;vy+=Math.sin(t*(s.glow?1.3:7)+b.ph)*w*stp*.6;vx+=Math.cos(t*(s.glow?.9:3.1)+b.ph)*w*stp*.3;}
    b.x+=vx;b.y+=vy;if(Math.abs(vx)>.05)b.face=vx>0?1:-1;
    if(s.dfly)b.rot=Math.atan2(vy,vx)+Math.PI/2;else b.rot=clamp(vx/Math.max(stp,.01)*.18,-.3,.3);}
}
function muPool(room){const out=[];for(const s of muNowSp(room)){let w=s.w;if(weather.on){if(s.k==="fly")continue;w*=.4;}if(muB.some(b=>b.id===s.id))continue;out.push([s.id,w]);}return out;}
function muTry(max){if(muB.filter(b=>b.st!=="out").length>=max)return null;const P=muPool(S.room);let tot=P.reduce((a,p)=>a+p[1],0),r=Math.random()*tot;for(const [id,w] of P){r-=w;if(r<=0)return muSpawn(id);}return null;}
hook("sec",()=>{const M=muS();if(M.day!==dayKey()){M.day=dayKey();M.td=[];}
  if(!MU_OUT.includes(S.room)||scene.on||overlaysOpen())return;
  muCage();if(now()<muNext)return;muNext=now()+rand(20,45);if(Math.random()<(M.net?.85:.6))muTry(Math.random()<.3?2:1);});
hook("tick",(t,dt)=>{if(muB.length&&MU_OUT.includes(S.room))muStep(t,Math.min(dt,.1));});
hook("room",id=>{muB.length=0;muNet=null;if(MU_OUT.includes(id)){muLoad();muNext=now()+rand(3,7);}});

// ── the singing cage: placed in the current room at night → a soft song now and then (respects the sound switch)
let muCageT=0;
function muCage(){const M=muS(),q=S.placed&&S.placed.mu_kago;if(!M.cage||!q||q.r!==S.room||!dayTint()[1]||!snd.on||!snd.ctx||document.hidden)return;
  const t=now();if(t<muCageT)return;muCageT=t+rand(6,12);muSong(M.cage,.45);
  const oc=curRow;curRow=q.y;const [x,y]=imgToStage(q.x,q.y-150,CAT_D);curRow=oc;floatFx.push({g:"♪",x,y,t:now()});}
hook("sec",()=>{if(!MU_OUT.includes(S.room)&&!scene.on&&!overlaysOpen())muCage();});
hook("itemTap",it=>{if(it.id==="mu_kago"){const M=muS();if(M.cage){muSong(M.cage,.8);toast(M.cage==="suzumushi"?"🎐 «Рии-ин…» — поёт судзумуси":"🎐 «Чин-чирорин…» — поёт мацумуси");}else toast("Клетка пока пустая");if(!petAway())react("😺",1.4);return true;}
  if(it.id==="mu_hako"){toast(`📦 В коллекции ${muSeenN()} из ${MU_SP.length} насекомых`);return true;}});

// ── drawing: the insects, a firefly glow, the net swing
hook("draw",(t,front)=>{if(!MU_OUT.includes(S.room)||scene.on)return;muLoad();const im=muAtlas();if(!im)return;const cl=catLineY()+6,night=dayTint()[1];
  if(!front)MU_K=Math.max(.05,(muPt(950,1100,.8)[0]-muPt(850,1100,.8)[0])/100);
  for(const b of muB){const s=b.s,isF=b.st==="fly"||b.st==="jump"||b.d>.79&&b.y>cl;if(isF!==front)continue;const [x,y]=muPt(b.x,b.y,b.d),kd=Math.max(.05,(muPt(b.x+50,b.y,b.d)[0]-muPt(b.x-50,b.y,b.d)[0])/100),sc=kd*s.s;b.sx=x;b.sy=y;
    const r=MU_R[s.id+"0"];b.r=Math.max(22,Math.max(r[2],r[3])*sc*.55);
    let fr=b.fr;if(b.st==="fly"||b.st==="jump"){fr=s.dfly?((t*16|0)%2):s.glow?1:((t*(s.id==="ageha"?9:12)+b.ph)|0)%2;if(b.hov>t&&s.dfly)fr=(t*20|0)%2;}
    if(s.glow){const p=.5+.5*Math.sin(t*2.4+b.ph),gr=(14+10*p)*kd*2.2;ctx.save();ctx.globalCompositeOperation="lighter";const g=ctx.createRadialGradient(x,y+r[3]*sc*.3,0,x,y+r[3]*sc*.3,gr);
      g.addColorStop(0,`rgba(200,255,150,${(.25+.5*p)*b.a})`);g.addColorStop(1,"rgba(200,255,150,0)");ctx.fillStyle=g;ctx.fillRect(x-gr,y-gr,gr*2,gr*2+r[3]*sc*.6);ctx.restore();}
    if(night&&!s.glow){const hr=b.r*1.2,g=ctx.createRadialGradient(x,y,0,x,y,hr);g.addColorStop(0,`rgba(215,225,200,${.15*b.a})`);g.addColorStop(1,"rgba(215,225,200,0)");ctx.fillStyle=g;ctx.fillRect(x-hr,y-hr,hr*2,hr*2);}
    if(b.st!=="fly"&&b.pk==="G"&&s.v==="s"){ctx.fillStyle=`rgba(6,8,8,${.28*b.a})`;ctx.beginPath();ctx.ellipse(x,y+r[3]*sc*.42,r[2]*sc*.36,5*kd,0,0,Math.PI*2);ctx.fill();}
    const flip=s.v==="s"?b.face<0:false,breathe=b.st==="sit"&&s.id==="kamakiri"?Math.sin(t*1.3+b.ph)*.06:0;
    muSpr(ctx,im,s.id+fr,x,y,sc,b.rot+breathe,flip,b.a);}
  if(muDbg&&!front){ctx.save();ctx.font="11px sans-serif";const R=MU_RM[S.room];for(const k of["T","L","G"])for(const p of R[k]){const [x,y]=muPt(p[0],p[1],p[2]);ctx.strokeStyle=k==="T"?"#f80":k==="L"?"#8f8":"#0ff";ctx.lineWidth=2;ctx.beginPath();ctx.arc(x,y,9,0,7);ctx.stroke();ctx.fillStyle="#fff";ctx.fillText(k+p[0],x+10,y);}
    const F=R.F,[a1,b1]=muPt(F[0],F[2],F[4]),[a2,b2]=muPt(F[1],F[3],F[4]);ctx.strokeStyle="#ff0";ctx.strokeRect(a1,b1,a2-a1,b2-b1);ctx.restore();}
});
hook("overlay",t=>{if(!muNet||!MU_OUT.includes(S.room))return;const e=t-muNet.t;if(e>1.1){muNet=null;return;}
  // the net: comes in from the upper right, scoops through the tap point, the bag swings shut
  const u=clamp(e/.42,0,1),eu=1-Math.pow(1-u,3),R=Math.max(24,64*MU_K),x=muNet.x+mix(110,-30,eu),y=muNet.y+mix(-120,26,eu)-Math.sin(eu*Math.PI)*24,fl=clamp(1-(e-.6)/.5,0,1);
  ctx.save();ctx.globalAlpha=fl;const px=x+R*6,py=y+R*7.5;
  ctx.strokeStyle="#b8955a";ctx.lineWidth=Math.max(3,R*.16);ctx.lineCap="round";ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(x+R*.7,y+R*.7);ctx.stroke();
  const sq=mix(1,.35,Math.sin(u*Math.PI)),ang=mix(-.5,.6,eu);ctx.translate(x,y);ctx.rotate(ang);
  const bagL=R*mix(1.4,2.1,eu);ctx.fillStyle="rgba(225,232,220,.4)";ctx.beginPath();ctx.moveTo(-R,0);ctx.quadraticCurveTo(-R*.6,bagL,0,bagL*1.05);ctx.quadraticCurveTo(R*.6,bagL,R,0);ctx.closePath();ctx.fill();
  ctx.strokeStyle="rgba(235,240,230,.5)";ctx.lineWidth=1;for(let i=-3;i<=3;i++){ctx.beginPath();ctx.moveTo(i*R/3.4,0);ctx.lineTo(i*R/9,bagL);ctx.stroke();}
  if(muNet.got&&e>.3){const im=muAtlas(),s=MU_ID[muNet.got];if(im)muSpr(ctx,im,s.id+"0",0,bagL*.62,MU_K*s.s*.7,0,false,clamp((e-.3)/.2,0,1));}
  ctx.strokeStyle="#c8a868";ctx.lineWidth=Math.max(2.5,R*.12);ctx.beginPath();ctx.ellipse(0,0,R,R*.42*sq,0,0,Math.PI*2);ctx.stroke();ctx.restore();});

// ── catching
function muNear(x,y,pad){let best=null,bd=1e9;for(const b of muB){if(b.st==="out"||b.st==="gone"||b.sx<-900)continue;const d=Math.hypot(x-b.sx,y-b.sy);if(d<b.r+pad&&d<bd){bd=d;best=b;}}return best;}
function muSwing(x,y,b){const M=muS();muWhoosh();muNet={x,y,t:now(),got:null};
  if(!b){for(const o of muB)if(o.st!=="out"&&Math.hypot(o.sx-x,o.sy-y)<140&&Math.random()<.5)muDodge(o);return false;}
  const s=b.s;let p=s.k==="fly"?(b.st==="sit"||b.hov>now()?.75:.5):s.jump?.6:s.id==="minmin"?.7:.88;if(M.net)p+=.12;if(s.rare)p-=.08;
  if(Math.random()>p){muDodge(b);setTimeout(()=>{if(!petAway()&&pet.action!=="sleep")react("🙀",1.2);toast(s.k==="fly"?"Увернулась! Лови снова 🍃":"Ускользнул… 🍃");},300);return false;}
  b.st="gone";muNet.got=b.id;setTimeout(()=>{chime([988,1318]);muCard(b.id,true);if(!petAway()&&pet.action!=="sleep")react("😻",1.6);},620);return true;}
function muCard(id,caught){const M=muS(),s=MU_ID[id],first=!M.seen[id];if(caught){M.n[id]=(M.n[id]||0)+1;if(!M.td.includes(id))M.td.push(id);award("mu_first");save();}
  if(s.song)setTimeout(()=>muSong(id,.9),500);
  const cnt=M.n[id]||0,tail=!caught?"":first?"\nНовое насекомое! Записать его в альбом и отпустить?":`\nУже в коллекции · поймано раз: ${cnt}.`;
  dlg({head:`${s.n} · ${s.jp}`,text:s.line+tail,img:muThumb(id+"0",110,90),
    ok:caught&&first?"📖 В коллекцию":"🍃 Выпустить",no:caught&&first?"🍃 Выпустить":"",
    onOk:()=>{if(caught&&first)muRecord(id);else if(caught)toast(`🍃 ${s.sn[0].toUpperCase()+s.sn.slice(1)} — снова на свободе`);},
    onNo:()=>{if(caught)toast("🍃 Отпустили — в коллекцию в другой раз");}});}
function muRecord(id){const M=muS(),s=MU_ID[id];if(M.seen[id])return;M.seen[id]=Date.now();disc("insect",id);save();tabDots();
  const n=muSeenN(),gifts=[];toast(`📖 ${s.sn[0].toUpperCase()+s.sn.slice(1)} — в альбоме и на свободе`);
  if(!S.owned.has("mu_ami")){S.owned.add("mu_ami");gifts.push("🎁 Сачок — в «Вещах»");}
  if((id==="suzumushi"||id==="matsumushi")&&!S.owned.has("mu_kago")){S.owned.add("mu_kago");M.cage=id;gifts.push("🎁 Клетка для сверчка — в «Вещах»");}
  if(n>=7&&!S.owned.has("mu_hako")){S.owned.add("mu_hako");award("mu_seven");gifts.push("🎁 Ящик с коллекцией — в «Вещах»");}
  if(n>=MU_SP.length)award("mu_all");save();ui();
  gifts.forEach((g,i)=>setTimeout(()=>toast(g),2600*(i+1)));}
hook("hit",(x,y)=>{if(!MU_OUT.includes(S.room)||scene.on)return;const M=muS(),b=muNear(x,y,M.net?26:4);
  if(b){audioInit();muSwing(x,y,b);return true;}
  if(M.net&&!hitCat(x,y)){audioInit();muSwing(x,y,null);return true;}});

// ── net mode: a tray button in the outdoor rooms
function muNetToggle(){const M=muS();M.net=M.net?0:1;save();ui();audioInit();
  if(M.net){tone(660,.08,"triangle",.03);const P=muPool(S.room);toast(muB.length?"🥅 Сачок в руках — лови!":P.length?"🥅 Сачок в руках — жди насекомых":"🥅 Здесь сейчас никого нет");if(!muB.length&&P.length)muNext=Math.min(muNext,now()+rand(2,4));}
  else toast("Сачок отложен");}
hook("tray",(tray,room)=>{if(!MU_OUT.includes(room)||(S.trayMode[room]||"play")!=="play")return;const el=tray.querySelector(".items");if(!el)return;const on=muS().net;
  const html=`<button class="item wide${on?" mu-on":""}" data-x="mu:net"><span class="ico">🥅</span><span class="nm">${on?"Сачок ✓":"Сачок"}</span></button>`,w=el.querySelectorAll(".item.wide");
  if(w.length)w[w.length-1].insertAdjacentHTML("afterend",html);else el.insertAdjacentHTML("afterbegin",html);});
hook("click",k=>{if(!k.startsWith("mu:"))return;
  if(k==="mu:net")muNetToggle();
  else if(k==="mu:album")muPanel();
  else if(k.startsWith("mu:card:"))muPanel(k.slice(8));
  else if(k==="mu:go"){closePanel();const P=MU_OUT.map(r=>[r,muNowSp(r).length]).sort((a,b)=>b[1]-a[1]);goRoom(P[0][1]?(S.room&&MU_OUT.includes(S.room)&&muNowSp(S.room).length?S.room:P[0][0]):"courtyard");setTimeout(()=>{if(!muS().net)muNetToggle();},700);}
  return true;});

// ── 家 card, album, panel
function muGrid(click){const M=muS();return`<div class="coll">${MU_SP.map(s=>{const on=!!M.seen[s.id];
  return`<div class="ci ${on?"on":""}" ${on&&click?`data-x="mu:card:${s.id}" style="cursor:pointer"`:""}>${muThumb(s.id+"0",64,52,"ath")}<small>${on?`${s.n}<br><i>${s.jp}</i>`:`???<br>${s.hint}`}</small></div>`;}).join("")}</div>`;}
function muLead(){const n=muSeenN();return`<p class="lead">В альбоме ${n} из ${MU_SP.length} насекомых. Каждое живёт в своё время года и суток: летом днём звенят цикады, ночью на стволы выползают жуки, осенними вечерами в траве поют сверчки. Лови сачком во дворике, в саду у веранды, у ворот, у святилища и на поляне игр — и отпускай.</p>`;}
function muPanel(id){const s=id&&MU_ID[id],M=muS();
  const det=s?`<div class="hubc mu-det">${muThumb(id+"0",120,96)}<div><h4>${s.n}</h4><p class="mu-n">${s.jp}</p><p>${s.line}</p><p class="mu-n">Поймано раз: ${M.n[id]||0} · ${s.hint}</p></div></div>`:"";
  openPanel("Насекомые",`${det}<p class="lead">${muStatus()}</p>${muLead()}${muGrid(1)}`,"mu");if(s){try{$("xpBody").scrollTop=0;}catch(e){}if(s.song)muSong(id,.8);}}
hook("hub",()=>{const n=muSeenN(),M=muS(),td=(M.day===dayKey()?M.td:[]);
  return`<div class="hubc"><h4>🥅 Сачок и насекомые <i>虫</i></h4><p>${muStatus()}</p><p>В альбоме ${n} из ${MU_SP.length}.${td.length?` Сегодня поймали: ${muList(td.map(i=>MU_ID[i].sn))}.`:""}${muRareNow()?" Сейчас можно встретить редкость!":""}</p>
  <div class="row"><button class="btn primary" data-x="mu:go">🥅 Ловить</button><button class="btn" data-x="mu:album">Альбом насекомых</button></div></div>`;});
hook("hubDot",()=>muRareNow());
hook("album",el=>{el.insertAdjacentHTML("beforeend",`<h3 class="bh">Насекомые</h3>${muLead()}${muGrid()}`);});
document.head.insertAdjacentHTML("beforeend","<style>#tray .item.wide.mu-on{box-shadow:inset 0 0 0 2px rgba(200,230,150,.55)}.mu-det{display:flex;gap:12px;align-items:flex-start}.mu-det>span{margin-top:6px}:is(.story-body,.card,#xpanel) .mu-det p.mu-n{font-size:12px;opacity:.75}</style>");
hook("boot",()=>{muS();if(MU_OUT.includes(S.room)){muLoad();muNext=now()+rand(3,7);}});
// test handles
X.insects={st:muS,list:muB,sp:MU_SP,spawn:muSpawn,card:muCard,record:muRecord,status:muStatus,nowSp:muNowSp,song:muSong,net:muNetToggle,panel:muPanel,
  dbg(v=1){muDbg=v;},reset(){muNext=now()+999;muB.length=0;},
  settle(){for(const b of muB){if(b.st==="in"){b.st="sit";b.a=1;b.x=b.x0;b.y=b.y0;}if(b.st==="fly"&&!b.leaving){const F=MU_RM[S.room].F;b.x=(F[0]+F[1])/2+rand(-120,120);b.y=(F[2]+F[3])/2;b.until=now()+999;}b.until=now()+999;}},
  pos(i=0){const b=muB[i];return b?[Math.round(b.sx),Math.round(b.sy),Math.round(b.r),b.id,b.st]:null;},
  tap(i=0){const b=muB[i];if(!b)return null;return hk("hit",b.sx,b.sy);},
  swing(i=0,ok=1){const b=muB[i];if(!b)return;const r=Math.random;if(ok)Math.random=()=>0;muSwing(b.sx,b.sy,b);Math.random=r;}};
}
