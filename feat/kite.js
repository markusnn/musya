{
// ───────────────────────── «Воздушный змей» (tako-age) on windy days ─────────────────────────
// Real wind from Open-Meteo for the city of the seasons add-on (S.ext.wx.city): a kite day when the wind is ≥ 12 km/h and
// it is not raining (sticky for the whole day once seen); no city / no network → ~2 pseudo-random windy days a week from
// dayKey(); New Year 1–7 January is always a kite day. On kite days «🪁 Змей» appears in the courtyard and games-room trays:
// a full-screen sky over the roofs, hold = pull the string, release = let it out, keep the tension green, dodge trees and
// a crow. 9 painted kites (atlas_ta): one new design per kite day flown, two for height records, one for beating the tengu
// in a kenka-dako duel (once a week). Every design is also a thing to hang on the wall («Воздушные змеи»).
// S.ext.kite = {got:[ids], sel:id, kd:{dayKey:1} sticky kite days, fl:dayKey of the last flight, days:kite days flown,
//   n:flights, best:m, w:{city,at,sp,dir,rain,day,f:[[date,max,prec]]}|null (cached fetch), try:ms, ts:dayKey toast shown,
//   tgw:week key of the last tengu duel, tgwin:duels won}
const TA_R={"ta_kaze":[0,0,150,200],"ta_koto":[152,0,150,200],"ta_koi":[304,0,150,200],"ta_yakko":[456,0,220,190],"ta_tsuru":[678,0,170,170],"ta_kitsune":[0,202,150,200],"ta_ryu":[152,202,150,200],"ta_musha":[304,202,170,190],"ta_tengu":[476,202,150,200]};   // assets/items/atlas_ta.webp 900×402 (art/kite_art.py)
const TA_TREES=[[560,150,95,490],[889,52,114,440],[1392,112,106,440]];   // assets/bg/ta_sky.webp 1600×600: crown [cx,top,halfW,bottom]
const TA_CITY={nn:[56.3269,44.0059],msk:[55.7558,37.6173],spb:[59.9343,30.3351],kzn:[55.7963,49.1088],ekb:[56.8389,60.6057],nsk:[55.0084,82.9357],
  sochi:[43.5855,39.7231],tokyo:[35.6762,139.6503],kyoto:[35.0116,135.7681]};   // same cities as feat/seasons.js (WX_CITY)
// designs: [id, name, kanji, how ("start"|"day"|"h"|"tengu"), value, hint, short hint, tail colours]
const TA_D=[["ta_kaze","Кадзэ — «Ветер»","風","start",0,"Первый змей Муси","Первый змей",["#c4302a","#efe6d2"]],
 ["ta_koto","Котобуки — «Долголетие»","寿","day",1,"Первый полёт змея","Первый полёт",["#c4302a","#d6a740"]],
 ["ta_koi","Карп, плывущий вверх","鯉","day",2,"Полёт во второй ветреный день","2-й ветреный день",["#d2452a","#a8c4dc"]],
 ["ta_yakko","Якко-дако, слуга самурая","奴","day",3,"Полёт в третий ветреный день","3-й ветреный день",["#2c3a66","#c4302a"]],
 ["ta_tsuru","Журавль из Сироне","鶴","day",4,"Полёт в четвёртый ветреный день","4-й ветреный день",["#efe6d2","#c83a2c"]],
 ["ta_kitsune","Маска лисы","狐","day",5,"Полёт в пятый ветреный день","5-й ветреный день",["#efe6d2","#c8322c"]],
 ["ta_ryu","Рю — «Дракон»","龍","h",100,"Подними змея на 100 метров","Высота 100 м",["#27355e","#c4302a"]],
 ["ta_musha","Воин муся-э","武","h",150,"Подними змея на 150 метров","Высота 150 м",["#c8562c","#d6a740"]],
 ["ta_tengu","Боевой змей тэнгу","天狗","tengu",1,"Победи тэнгу в бою змеев","Победи тэнгу",["#c23a2a","#1f2c24"]]];
const TA_ID={};for(const d of TA_D)TA_ID[d[0]]=d;
const TA_C="Воздушные змеи";
const TA_N={ta_kaze:"Змей «Ветер» 風",ta_koto:"Змей «Долголетие» 寿",ta_koi:"Змей-карп",ta_yakko:"Змей якко-дако",ta_tsuru:"Змей с журавлём",ta_kitsune:"Змей «Маска лисы»",ta_ryu:"Змей «Дракон» 龍",ta_musha:"Змей с воином",ta_tengu:"Боевой змей тэнгу"};
addItems(TA_D.map(d=>({id:d[0],n:TA_N[d[0]],c:TA_C,w:TA_R[d[0]][2],h:TA_R[d[0]][3],a:"t",p:0,at:["ta",TA_R[d[0]][0],TA_R[d[0]][1]],src:"🪁 змей",hint:"🪁 "+d[5]})),{ta:[900,402]});
STAMPS.push(["ta_first","凧","Первый змей","Запусти воздушного змея в ветреный день"],["ta_100","高","Сто метров","Подними змея на 100 метров"],["ta_all","揚","Все змеи","Собери все девять змеев"]);
document.head.insertAdjacentHTML("beforeend",`<style>.ta-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:10px;margin:10px 0}
.ta-grid .btn.ta-k{display:flex;flex-direction:column;align-items:center;gap:4px;padding:8px 4px;height:auto;min-height:0;white-space:normal;line-height:1.2;font-size:12px}
.ta-grid .btn.ta-k.on{outline:2px solid var(--sakura,#e6a2b4)}.ta-grid .ta-k .ath{filter:none}.ta-grid .ta-k.off .ath{filter:brightness(0) opacity(.45)}
:is(.hubc,.card) p.ta-s{font-size:13px;opacity:.85;margin:6px 0;line-height:1.45}</style>`);

const taS=()=>{const K=S.ext.kite||(S.ext.kite={});K.got=K.got||[];K.kd=K.kd||{};K.n=K.n||0;K.days=K.days||0;K.best=K.best||0;K.sel=K.sel||"ta_kaze";return K;};
const TA_WD=["воскресенье","понедельник","вторник","среду","четверг","пятницу","субботу"],TA_MO=["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"];
const taDK=d=>dayKey(d),taAdd=i=>{const T=today();return new Date(T.getFullYear(),T.getMonth(),T.getDate()+i,12);};
const taWeek=()=>{const T=today();return taDK(new Date(T.getFullYear(),T.getMonth(),T.getDate()-(T.getDay()+6)%7,12));};

// ── wind: real (current + 7-day forecast) or pseudo-random
let taBusy=0;
function taCity(){const c=(S.ext.wx||{}).city||"nn";return TA_CITY[c]?c:null;}
function taReal(){const K=taS(),w=K.w,c=taCity();return c&&w&&w.city===c&&Date.now()-w.at<3*3600e3?w:null;}
const TA_RAINC=c=>c>=51&&c<=67||c>=80&&c<=82||c>=95;
function taFetch(force){const K=taS(),c=taCity();if(!c||taBusy)return;const w=K.w;
  if(!force&&(w&&w.city===c&&Date.now()-w.at<30*60e3||Date.now()-(K.try||0)<30*60e3))return;
  K.try=Date.now();taBusy=1;const [la,lo]=TA_CITY[c];
  fetch(`https://api.open-meteo.com/v1/forecast?latitude=${la}&longitude=${lo}&current=wind_speed_10m,wind_direction_10m,precipitation,weather_code&daily=wind_speed_10m_max,precipitation_sum&timezone=auto&forecast_days=7`)
    .then(r=>r.ok?r.json():null).then(j=>{const n=j&&j.current,d=j&&j.daily;if(!n||typeof n.wind_speed_10m!=="number"||taCity()!==c)return;
      K.w={city:c,at:Date.now(),sp:Math.round(n.wind_speed_10m),dir:n.wind_direction_10m||270,rain:(n.precipitation||0)>0||TA_RAINC(n.weather_code||0),day:String(n.time||"").slice(0,10),
        f:d&&d.time?d.time.map((t,i)=>[t,Math.round(d.wind_speed_10m_max[i]||0),d.precipitation_sum[i]||0]):[]};
      taCheck();save();hubDot();if(panelIs("hub"))openHub();})
    .catch(()=>{}).finally(()=>{taBusy=0;});}
function taHash(s){let h=2166136261;for(const ch of s)h=Math.imul(h^ch.charCodeAt(0),16777619)>>>0;h^=h>>>13;h=Math.imul(h,0x5bd1e995)>>>0;return(h^h>>>15)>>>0;}
const taNY=dk=>dk.slice(5,7)==="01"&&+dk.slice(8)<=7;
// the wind of a day: {sp, dir (from), src:"now"|"fc"|"", rain}
function taWind(dk=dayKey()){const w=taReal();
  if(w&&w.day===dk)return{sp:w.sp,dir:w.dir,src:"now",rain:w.rain};
  const f=w&&w.f.find(r=>r[0]===dk);if(f)return{sp:f[1],dir:w.dir,src:"fc",rain:f[2]>=3};
  const h=taHash(dk);return{sp:h%7<2?13+(h>>>4)%15:3+(h>>>4)%7,dir:(h>>>9)%360,src:"",rain:false};}   // ~2 windy days a week
function taWindy(dk){const W=taWind(dk);return W.src==="fc"?W.sp>=18&&!W.rain:W.sp>=12&&!W.rain;}   // a daily max runs higher than «now»
function taIsDay(dk=dayKey()){const K=taS();return taNY(dk)||!!K.kd[dk]||taWindy(dk);}
function taCheck(){const K=taS(),dk=dayKey();if(!K.kd[dk]&&taWindy(dk)){K.kd[dk]=1;const ks=Object.keys(K.kd).sort();while(ks.length>20)delete K.kd[ks.shift()];}}
function taNext(){for(let i=1;i<=28;i++){const d=taAdd(i),dk=taDK(d);if(taNY(dk)||taWindy(dk))return[i,d,taWind(dk)];}return null;}
function taWhen(n){if(!n)return"пока не видно";const [i,d]=n;return i===1?"завтра":i===2?"послезавтра":`${d.getDay()===2?"во":"в"} ${TA_WD[d.getDay()]}, ${d.getDate()} ${TA_MO[d.getMonth()]}`;}
function taLine(){const dk=dayKey(),W=taWind(dk),day=taIsDay(dk),ny=taNY(dk),nw=W.src==="now";
  if(day&&weather.on)return"Ветер есть, но идёт дождь — змей подождёт";
  if(day)return ny?`Сёгацу — время такоагэ: змей полетит при любом ветре`:nw&&W.sp>=12?`Сегодня ветер ${W.sp} км/ч — можно запускать змея`:"Сегодня ветрено — можно запускать змея";
  const n=taNext();return`${nw&&W.rain&&W.sp>=12?"Идёт дождь":"Безветренно"}; ${n?"ветер обещают "+taWhen(n):"ветра пока не обещают"}`;}
// the second line of the card on calm days: the numbers behind the status
function taLine2(){const W=taWind(),n=taNext();if(taIsDay())return"";
  return(W.src==="now"?`Сейчас ${W.sp} км/ч, а змею нужно от 12. `:"")+(n&&n[2].src?`Тогда обещают до ${n[2].sp} км/ч. `:"");}

// ── designs
function taGive(id,quiet){const K=taS();if(K.got.includes(id))return false;K.got.push(id);S.owned.add(id);loadItem(id);disc("kite",id);
  if(K.got.length>=TA_D.length)award("ta_all");if(!quiet)chime([784,988,1175]);return true;}
let taIm=null;const taImg=()=>{if(!taIm)atlasImg("ta",im=>{taIm=im;});return taIm;};
let taSky=null;ldImg("assets/bg/ta_sky.webp",im=>{taSky=im;});

// ── the flight ────────────────────────────────────────────────────────────────
const TA_HMAX=200,TA_H0=45,TA_T=45;
// wind gusts: smooth wobble + events (gust +45 % / lull −38 %), each 1.5–2 s, every 3.5–6.5 s
function taGust(q,t){let g=1+.1*Math.sin(t*.9+q.ph0)+.06*Math.sin(t*2.3+1);for(const e of q.ev){const u=t-e.t;if(u<-.1||u>e.d+.9)continue;g+=e.a*clamp(Math.min((u+.1)/.5,(e.d+.9-u)/.9),0,1);}return g;}
// physics of one step: tension T toward a target (held pulls), angle θ climbs while T is green, the line runs out while released
function taPhys(q,dt,held,t){const g=taGust(q,t),wn=Math.min(1.7,q.wb*g);q.wn=wn;
  const Tt=held?.30+.50*wn:.02+.22*wn;q.T+=(Tt-q.T)*Math.min(1,dt*2.6);const T=q.T;
  if(T>.86)q.red+=dt;else q.red=Math.max(0,q.red-dt*2);
  const dA=T>=.36&&T<=.78?(held?9:5):T<.36?-(4+14*(.36-T)/.36):(held?2:0)-(T-.78)*30;
  q.th=clamp(q.th+dA*dt,8,76);q.L=clamp(q.L+(held?-2:(1.5+4*wn)*(T>.2?1:.5))*dt,12,200);q.h=q.L*Math.sin(q.th*Math.PI/180);
  if(q.red>1.1){q.red=0;q.th=Math.max(8,q.th-22);q.T=.45;q.spin=t;return"spin";}return null;}

function taLay(G){const W=G.W,H=G.H,s=G.s,sc=Math.max(W/1600,H*.36/600),x0=Math.max(W-1600*sc,-200*sc),top=H-600*sc,q=G.st,sg=q.sg;
  const fy=top+552*sc,mx=sg>0?Math.max(56*s,W*.14):Math.min(W-56*s,W*.86),yG=fy-34*s,yT=96*s+40;
  const X=ix=>sg>0?x0+ix*sc:W-(x0+ix*sc);
  return{W,H,s,sc,x0,top,fy,mx,yG,yT,X,roof:top+418*sc,span:sg>0?W-30*s-mx:mx-30*s,cs:.66*s};}
const taY=(L,h)=>L.yG-(L.yG-L.yT)*(h/(h+TA_H0))/(TA_HMAX/(TA_HMAX+TA_H0));
function taKpos(G,L,t){const q=G.st,c=Math.cos(q.th*Math.PI/180),wob=(q.wn-1)*8*L.s*Math.sin(t*1.7)+3*L.s*Math.sin(t*3.1);
  return[L.mx+q.sg*L.span*Math.pow(c,.9)+wob,taY(L,q.h)+(q.snag?0:2*L.s*Math.sin(t*2.3)),92*L.s*Math.pow(30/(30+q.L),.4)];}

function taMsg(q,txt,t){q.msg=txt;q.msgT=t;}
const TA_G={id:"ta_fly",hidden:true,n:"Воздушный змей",tag:"凧揚げ · такоагэ",icon:"🪁",bg:"forest",lives:null,time:null,
 lore:"В Японии змеев запускают на Новый год и в ветреные дни: большие расписные эдо-дако с иероглифами, якко-дако в виде слуги самурая, квадратные змеи из Сироне.",
 how:"Держи палец — тянешь нить, змей набирает высоту. Отпусти — нить уходит, змей улетает дальше. Держи натяжение в зелёной зоне, берегись сосен и вороны.",
 init(G,t){const K=taS(),W=taWind(),q=G.st;G.time=null;G.score=0;
   Object.assign(q,{ph:K.got.length>1?"pick":"fly",sel:K.got.includes(K.sel)?K.sel:K.got[0]||"ta_kaze",wb:clamp(.95+((W.sp||16)-12)/80,.92,1.15),sp:W.sp||16,sg:Math.sin((W.dir||270)*Math.PI/180)<0?1:-1,
     T:.5,th:52,L:24,h:0,max:0,red:0,wn:1,ph0:Math.random()*6,ev:[],nextE:t+3,crow:null,crowT:t+8,snag:0,snagN:0,spin:-9,msg:"",msgT:-9,crash:0,btns:[],
     streaks:[],clouds:[0,1,2].map(i=>({x:Math.random(),y:.1+.22*i+Math.random()*.08,k:.7+Math.random()*.6})),t0:t,clk:0,tg:null,
     tgOn:K.n>=1&&K.tgw!==taWeek(),pullT:0});
   if(q.ph==="fly")taLaunch(G,t);},
 step(G,t,dt){const q=G.st;q.clk+=dt;if(q.ph!=="fly")return;const L=taLay(G);
   // gust schedule (a streak warning 0.8 s before a gust)
   if(q.clk>q.nextE){const gust=Math.random()<.55;q.ev.push({t:q.clk+.8,d:rand(1.4,2.2),a:gust?rand(.38,.55):-rand(.3,.42)});q.nextE=q.clk+rand(3.5,6.5);q.ev=q.ev.filter(e=>q.clk-e.t<6);}
   if(q.snag){q.snag-=dt;if(q.snag<=0){q.snag=0;q.th=Math.min(78,q.th+18);q.L=Math.max(12,q.L-10);taMsg(q,"Вырвался! Тяни выше",q.clk);}}
   else if(q.crash){q.crash-=dt;if(q.crash<=0){q.crash=0;q.L=24;q.th=52;q.T=.5;taMsg(q,"Муся снова запускает змея",q.clk);}}
   else{const r=taPhys(q,dt,G.held,q.clk);if(r==="spin"){taMsg(q,"Перетянул! Змей кувыркнулся",q.clk);sfx("bad");}
     q.max=Math.max(q.max,q.h);G.score=Math.round(q.max);
     const [kx,ky,ks]=taKpos(G,L,q.clk);
     // snags: tree crowns (ellipses), the roofs
     for(const tr of TA_TREES){const cx=L.X(tr[0]),cy=L.top+(tr[1]+tr[3])/2*L.sc,rx=tr[2]*L.sc*.8,ry=(tr[3]-tr[1])/2*L.sc;
       if(((kx-cx)/rx)**2+((ky-cy)/ry)**2<1){q.snag=1.4;q.snagN++;q.T=.3;taMsg(q,"Змей зацепился за сосну!",q.clk);sfx("bad");if(!petAway())react("🙀",1.2);break;}}
     if(!q.snag&&ky+ks*.35>L.roof&&Math.abs(kx-L.mx)>40*L.s){q.crash=1.6;taMsg(q,"Змей упал на крышу…",q.clk);sfx("bad");}}
   // the crow: warned by a caw at the edge, flies across at the kite's height
   const [kx,ky,ks]=taKpos(G,L,q.clk);
   if(!q.crow&&q.clk>q.crowT){const dir=Math.random()<.5?1:-1;q.crow={x:dir>0?-60*L.s:L.W+60*L.s,y:clamp(ky+rand(-25,25)*L.s,L.yT+20,L.roof-60*L.s),v:dir*rand(120,150)*L.s,w:q.clk+1.2,hit:0};
     if(snd.on&&snd.ctx){tone(640,.32,"sawtooth",.02);setTimeout(()=>tone(600,.3,"sawtooth",.02),380);}}
   const c=q.crow;if(c){if(q.clk>c.w){c.x+=c.v*dt;c.y+=Math.sin(q.clk*2)*8*L.s*dt;
       if(!c.hit&&!q.snag&&!q.crash&&Math.hypot(c.x-kx,c.y-ky)<ks*.42+16*L.s){c.hit=1;q.th=Math.max(8,q.th-16);q.T=.25;q.spin=q.clk;taMsg(q,"Ворона клюнула змея!",q.clk);sfx("bad");c.v*=1.4;c.y-=30*L.s;}
       if(c.x<-120*L.s||c.x>L.W+120*L.s){q.crow=null;q.crowT=q.clk+rand(8,12);}}}
   // the tengu's kite: a kenka-dako duel (whoever stays higher 6 s cuts the other's line)
   if(q.tgOn&&!q.tg&&q.clk-q.t1>9){q.tg={h:12,me:0,him:0,res:0,t:q.clk};taMsg(q,"Тэнгу поднял боевого змея!",q.clk);chime([392,523,392]);}
   const d=q.tg;if(d&&!d.res){d.h+=clamp(Math.min(175,q.h+9)-d.h,-6*dt,6*dt);
     if(q.h>d.h+3)d.me+=dt;else if(d.h>q.h+3)d.him+=dt;
     if(d.me>=6){d.res=1;d.rt=q.clk;taS().tgw=taWeek();taS().tgwin=(taS().tgwin||0)+1;taMsg(q,"Нить тэнгу перерезана! Его змей — твой",q.clk);chime([659,784,1046,1318]);}
     else if(d.him>=6){d.res=-1;d.rt=q.clk;taS().tgw=taWeek();taMsg(q,"Тэнгу перерезал нить Муси…",q.clk);sfx("bad");setTimeout(()=>{if(G.id==="ta_fly"&&!G.over)gEnd();},2200);}}
   // wind streaks: denser before and during gusts
   const g=taGust(q,q.clk+.8);if(Math.random()<dt*(g>1.25?9:1.5))q.streaks.push({x:q.sg>0?-80:L.W+80,y:rand(L.yT,L.roof),v:rand(380,560)*L.s*q.sg,l:rand(40,110)*L.s});
   for(const s of q.streaks)s.x+=s.v*dt;q.streaks=q.streaks.filter(s=>s.x>-200&&s.x<L.W+200);
   for(const cl of q.clouds){cl.x+=q.sg*dt*.008*q.wn;if(cl.x>1.3)cl.x=-.3;if(cl.x<-.3)cl.x=1.3;}
   if(G.held&&!petAway()&&q.clk-q.pullT>.25){q.pullT=q.clk;}},
 draw(G,g,t){const q=G.st,L=taLay(G),W=L.W,H=L.H,s=L.s;
   g.drawImage(taSkyC(G,L),0,0,W,H);
   for(const cl of q.clouds)taCloud(g,cl.x*W,L.yT+cl.y*(L.roof-L.yT),110*s*cl.k);
   g.save();g.strokeStyle="rgba(235,240,250,.35)";g.lineWidth=1.2;g.lineCap="round";for(const st of q.streaks){g.beginPath();g.moveTo(st.x,st.y);g.lineTo(st.x-st.l*Math.sign(st.v),st.y+2);g.stroke();}g.restore();
   const sc=taStripC(G,L);if(sc)g.drawImage(sc,0,0,W,H);
   const im=taImg();
   // the tengu on a far roof with his kite
   if(q.tg){const d=q.tg,tx=q.sg>0?W-30*s:30*s,ty=L.roof+8*s,mi=MIMG.m_rm_tengu,th=74*s;
     if(mi){g.save();g.translate(tx,ty);if(q.sg<0)g.scale(-1,1);g.drawImage(mi,-th*440/580/2,-th,th*440/580,th);g.restore();}
     let gx=L.mx+q.sg*L.span*.8,gy=taY(L,d.h);if(d.res===1){const u=q.clk-d.rt;gx+=q.sg*u*60*s;gy+=u*u*30*s;}
     if(d.res!==1){g.strokeStyle="rgba(230,220,200,.55)";g.lineWidth=1;g.beginPath();g.moveTo(tx-q.sg*14*s,ty-th*.55);g.quadraticCurveTo((tx+gx)/2,(ty+gy)/2+30*s,gx,gy);g.stroke();}
     if(im&&gy<H)taKite(g,im,"ta_tengu",gx,gy,60*s,Math.sin(q.clk*2.1)*.12+(d.res===1?q.clk*3:0),q.clk,-q.sg,1);}
   // the crow
   const c=q.crow;if(c&&q.clk>c.w&&BI_IMC()){const ci=BI_IMC(),w=62*s,h=w*284/327,fl=.75+.3*Math.abs(Math.sin(q.clk*9));g.save();g.translate(c.x,c.y);if(c.v<0)g.scale(-1,1);g.scale(1,fl);g.drawImage(ci,0,0,327,284,-w/2,-h/2,w,h);g.restore();}
   else if(c){const ex=c.v>0?14*s:W-14*s;g.save();g.globalAlpha=.6+.4*Math.sin(q.clk*14);textC(g,"🐦‍⬛ кар!",ex+(c.v>0?28:-28)*s,c.y,15*s,"#f3e3c0",800);g.restore();}
   // string, kite, tail
   if(q.ph==="fly"){const [kx,ky,ks]=taKpos(G,L,q.clk),hp=taHand(G,L),cut=q.tg&&q.tg.res===-1;let X_=kx,Y_=ky,rot=Math.sin(q.clk*1.9)*.06*q.wn+(q.clk-q.spin<.9?(q.clk-q.spin)*7:0);
     if(cut){const u=q.clk-q.tg.rt;X_+=q.sg*u*50*s;Y_+=u*u*20*s;rot+=u*2;}
     if(q.crash){const u=1.6-q.crash;Y_=Math.min(L.roof,ky+u*u*200*s);rot=u*2;}
     if(!cut){const sag=(1-clamp(q.T,0,1))*.22*Math.hypot(X_-hp[0],Y_-hp[1]);g.strokeStyle="rgba(240,232,212,.8)";g.lineWidth=1.3;g.beginPath();g.moveTo(hp[0],hp[1]);g.quadraticCurveTo((hp[0]+X_)/2,(hp[1]+Y_)/2+sag,X_,Y_);g.stroke();}
     if(im)taKite(g,im,q.sel,X_,Y_,ks,rot,q.clk,q.sg,q.wn);}
   // Musya and the spool
   const fy=L.fy,mx=L.mx,cs=L.cs;g.save();g.translate(mx,0);if(q.sg<0)g.scale(-1,1);
   g.fillStyle="#5a3a22";g.beginPath();g.ellipse(46*cs,fy-10*cs,15*cs,10*cs,0,0,Math.PI*2);g.fill();g.fillStyle="#e8dcc0";g.beginPath();g.ellipse(46*cs,fy-10*cs,9*cs,6*cs,0,0,Math.PI*2);g.fill();
   if(!petAway()){const pull=G.held&&q.ph==="fly"&&!q.crash;drawCatG(g,pull?"play":"gaze9",pull?5:Math.floor(q.clk*.8)%2,0,fy,cs);}
   g.restore();
   // HUD: tension gauge, height scale, wind, messages, the duel
   if(q.ph==="fly"){const bx=W*.18,bw=W*.64,by=70*s+8,bh=10*s;g.fillStyle="rgba(10,12,20,.55)";g.beginPath();g.roundRect(bx-4,by-4,bw+8,bh+8,8);g.fill();
     g.fillStyle="rgba(200,80,60,.55)";g.fillRect(bx,by,bw,bh);g.fillStyle="rgba(110,170,100,.85)";g.fillRect(bx+bw*.36,by,bw*.42,bh);g.fillStyle="rgba(220,200,120,.55)";g.fillRect(bx,by,bw*.36,bh);
     const mk=bx+bw*clamp(q.T,0,1);g.fillStyle=q.red>.3&&Math.sin(q.clk*20)>0?"#ff5040":"#f6efe0";g.fillRect(mk-2,by-5,4,bh+10);
     textC(g,"натяжение",bx+bw/2,by+bh+12*s,11*s,"rgba(240,230,210,.75)",600);
     const sx=q.sg>0?W-20*s:20*s;g.strokeStyle="rgba(240,230,210,.35)";g.lineWidth=1;g.beginPath();g.moveTo(sx,taY(L,0));g.lineTo(sx,taY(L,TA_HMAX));g.stroke();
     for(const m of [10,25,50,100,150,200]){const y=taY(L,m);g.beginPath();g.moveTo(sx-5,y);g.lineTo(sx+5,y);g.stroke();g.save();g.font=`600 ${10*s}px sans-serif`;g.fillStyle="rgba(240,230,210,.6)";g.textAlign=q.sg>0?"right":"left";g.textBaseline="middle";g.fillText(m+" м",sx-q.sg*8*s,y);g.restore();}
     const K=taS();if(K.best>0){const y=taY(L,Math.min(K.best,TA_HMAX));g.strokeStyle="rgba(230,190,90,.8)";g.beginPath();g.moveTo(sx-9,y);g.lineTo(sx+9,y);g.stroke();}
     g.fillStyle="#f6e2b0";g.beginPath();g.arc(sx,taY(L,q.h),4*s,0,Math.PI*2);g.fill();
     textC(g,`${Math.round(q.h)} м`,W/2,by+bh+34*s,26*s,"#f6efe0",800);
     textC(g,`🍃 ${Math.round(q.sp*taGust(q,q.clk))} км/ч ${q.sg>0?"→":"←"}`,W/2,by+bh+58*s,13*s,"rgba(240,230,210,.8)",600);
     if(q.tg){const d=q.tg,w2=W*.22,y2=by+bh+84*s;g.fillStyle="rgba(10,12,20,.5)";g.fillRect(W/2-w2-6,y2-8*s,w2*2+12,16*s);
       g.fillStyle="#e6c060";g.fillRect(W/2-w2*Math.min(1,d.me/6),y2-4*s,w2*Math.min(1,d.me/6),8*s);g.fillStyle="#c23a2a";g.fillRect(W/2,y2-4*s,w2*Math.min(1,d.him/6),8*s);
       textC(g,"Муся выше",W/2-w2*.55,y2-14*s,11*s,"#f3e3c0",700);textC(g,"тэнгу выше",W/2+w2*.55,y2-14*s,11*s,"#f3c0b0",700);}
     const e=q.clk-q.msgT;if(q.msg&&e<2.6){g.save();g.globalAlpha=clamp(Math.min(e/.2,(2.6-e)/.5),0,1);textC(g,q.msg,W/2,H*.5,17*s,"#fff3d8",800);g.restore();}
     if(q.clk-q.t1<3.5){g.save();g.globalAlpha=clamp((3.5-(q.clk-q.t1))/.8,0,1);textC(g,"Держи — тянешь, отпусти — нить уходит",W/2,H*.56,14*s,"rgba(246,239,224,.9)",700);g.restore();}}
   if(q.ph==="pick")taPick(G,g,L,im);},
 down(G,x,y,t){const q=G.st;if(q.ph!=="pick")return;for(const b of q.btns)if(x>b[0]&&x<b[0]+b[2]&&y>b[1]&&y<b[1]+b[3]){q.sel=b[4];taS().sel=b[4];q.btns=[];sfx("pop");taLaunch(G,now());G.held=false;return;}},
 up(G){},
 stat:G=>{const q=G.st;return q.ph==="pick"?"Выбери змея":`↑ ${Math.round(q.h)} м · ${Math.ceil(Math.max(0,G.time||0))} с`;},
 card(G,rec){return taFinish(G);},
 after(){ui();hubDot();}};
GAMES.push(TA_G);
function taLaunch(G,t){const q=G.st;q.ph="fly";q.t1=q.clk;G.time=TA_T;q.L=24;q.th=52;q.T=.5;sfx("pop");}
const BI_IMC=()=>{if(BI_IMC.im)return BI_IMC.im;if(!BI_IMC.q){BI_IMC.q=1;atlasImg("bi",im=>{BI_IMC.im=im;});}return null;};
function taHand(G,L){const q=G.st,cs=L.cs,pull=G.held&&!q.crash;return pull?[L.mx+q.sg*80*cs,L.fy-99*cs]:[L.mx+q.sg*46*cs,L.fy-12*cs];}
// a kite with its bridle and two waving paper tails (they stream downwind)
function taKite(g,im,id,x,y,hh,rot,t,sg,wn){const r=TA_R[id],k=hh/r[3],w=r[2]*k,D=TA_ID[id];
  for(let j=0;j<2;j++){g.strokeStyle=D[7][j];g.lineWidth=Math.max(2,hh*.05);g.lineCap="round";g.beginPath();const ox=(j?.18:-.18)*w;let px_=x+ox,py_=y+hh*.45;g.moveTo(px_,py_);
    for(let i=1;i<=9;i++){const u=i/9;px_=x+ox+sg*u*hh*.9*Math.min(1.3,.5+wn*.6)+Math.sin(t*7-i*.9+j)*hh*.07*u;py_=y+hh*.45+u*hh*1.1/Math.max(.8,wn)+Math.cos(t*6-i*.8)*hh*.04;g.lineTo(px_,py_);}g.stroke();}
  g.save();g.translate(x,y);g.rotate(rot);g.drawImage(im,r[0],r[1],r[2],r[3],-w/2,-hh/2,w,hh);g.restore();}
let taCl=null;
function taCloud(g,x,y,r){if(!taCl){taCl=document.createElement("canvas");taCl.width=240;taCl.height=90;const c=taCl.getContext("2d");
    for(const [dx,dy,k] of [[-.55,.08,.42],[-.2,-.1,.55],[.2,-.04,.5],[.55,.1,.4],[0,.14,.6]]){const cx=120+dx*120,cy=48+dy*90,R=k*80,gr=c.createRadialGradient(cx,cy,0,cx,cy,R);gr.addColorStop(0,"rgba(240,244,248,.5)");gr.addColorStop(1,"rgba(240,244,248,0)");c.fillStyle=gr;c.fillRect(0,0,240,90);}}
  g.save();g.globalAlpha=dayTint()[1]?.28:.6;g.drawImage(taCl,x-r*1.2,y-r*.45,r*2.4,r*.9);g.restore();}
function taTod(){const h=hourNow();return dayTint()[1]?"n":h>=16.5&&h<19.5||h>=4.5&&h<7?"e":"d";}
let taSkyK="",taSkyCv=null,taStripK="",taStripCv=null;
function taSkyC(G,L){const k=[L.W,L.H,taTod(),G.st.sg].join("|");if(k===taSkyK)return taSkyCv;taSkyK=k;
  const c=document.createElement("canvas"),d=Math.min(2,devicePixelRatio||1);c.width=L.W*d;c.height=L.H*d;const g=c.getContext("2d");g.scale(d,d);const W=L.W,H=L.H,tod=taTod();
  g.fillStyle=vGrad(g,0,H,tod==="n"?[[0,"#0a1124"],[.6,"#1e2846"],[1,"#2e3650"]]:tod==="e"?[[0,"#2e3a66"],[.55,"#9a6878"],[1,"#d8946a"]]:[[0,"#6a88aa"],[.7,"#aebccb"],[1,"#d4d6d0"]]);g.fillRect(0,0,W,H);
  if(tod==="n"){const r=rng(7);for(let i=0;i<90;i++){g.fillStyle=`rgba(255,250,235,${.2+r()*.6})`;g.fillRect(r()*W,r()*H*.6,1.3,1.3);}
    const mx=G.st.sg>0?W*.78:W*.22,my=L.yT+60*L.s,gr=g.createRadialGradient(mx,my,0,mx,my,90*L.s);gr.addColorStop(0,"rgba(255,240,200,.35)");gr.addColorStop(1,"rgba(255,240,200,0)");g.fillStyle=gr;g.fillRect(mx-90*L.s,my-90*L.s,180*L.s,180*L.s);
    g.fillStyle="#f3ead0";g.beginPath();g.arc(mx,my,20*L.s,0,Math.PI*2);g.fill();}
  else{const sx=G.st.sg>0?W*.8:W*.2,sy=L.yT+(tod==="e"?L.roof*.55:40*L.s),gr=g.createRadialGradient(sx,sy,0,sx,sy,160*L.s);gr.addColorStop(0,tod==="e"?"rgba(255,200,140,.55)":"rgba(255,250,230,.45)");gr.addColorStop(1,"rgba(255,240,200,0)");g.fillStyle=gr;g.fillRect(0,0,W,H);}
  // film grain
  const r=rng(3);for(let i=0;i<W*H/90;i++){g.fillStyle=r()<.5?"rgba(255,255,255,.035)":"rgba(0,0,0,.05)";g.fillRect(r()*W,r()*H,1,1);}
  taSkyCv=c;return c;}
function taStripC(G,L){if(!taSky)return null;const k=[L.W,L.H,taTod(),G.st.sg].join("|");if(k===taStripK)return taStripCv;taStripK=k;
  const c=document.createElement("canvas"),d=Math.min(2,devicePixelRatio||1);c.width=L.W*d;c.height=L.H*d;const g=c.getContext("2d");g.scale(d,d);
  g.save();if(G.st.sg<0){g.translate(L.W,0);g.scale(-1,1);}g.drawImage(taSky,L.x0,L.top,1600*L.sc,600*L.sc);g.restore();
  const tod=taTod();g.globalCompositeOperation="source-atop";g.fillStyle=tod==="n"?"rgba(8,12,34,.55)":tod==="e"?"rgba(70,30,40,.3)":"rgba(40,50,70,.12)";g.fillRect(0,0,L.W,L.H);
  taStripCv=c;return c;}
// choosing the kite before the flight (locked ones as dark silhouettes, no ctx.filter for Safari)
const taSilC={};function taSil(im,id){if(taSilC[id])return taSilC[id];const r=TA_R[id],c=document.createElement("canvas");c.width=r[2];c.height=r[3];const x=c.getContext("2d");
  x.drawImage(im,r[0],r[1],r[2],r[3],0,0,r[2],r[3]);x.globalCompositeOperation="source-in";x.fillStyle="#0c0e16";x.fillRect(0,0,r[2],r[3]);return taSilC[id]=c;}
function taPick(G,g,L,im){const q=G.st,K=taS(),W=L.W,H=L.H,s=L.s;g.fillStyle="rgba(8,10,18,.62)";g.fillRect(0,0,W,H);
  textC(g,"Какого змея запустим?",W/2,96*s+20,20*s,"#f6efe0",800);
  const ids=TA_D.map(d=>d[0]),cols=W<640?3:5,cw=Math.min(130*s,(W-40)/cols-10),ch=cw*1.45,x0=(W-cols*(cw+10)+10)/2,y0=96*s+50;q.btns=[];
  ids.forEach((id,i)=>{const x=x0+(i%cols)*(cw+10),y=y0+Math.floor(i/cols)*(ch+10),got=K.got.includes(id),on=id===q.sel,D=TA_ID[id];
    g.fillStyle=on?"rgba(230,162,180,.25)":"rgba(255,255,255,.06)";g.strokeStyle=on?"rgba(230,162,180,.9)":"rgba(255,255,255,.18)";g.beginPath();g.roundRect(x,y,cw,ch,10);g.fill();g.stroke();
    if(im){const r=TA_R[id],k=Math.min((cw-16)/r[2],(ch-44*s)/r[3]);g.save();if(got)g.drawImage(im,r[0],r[1],r[2],r[3],x+cw/2-r[2]*k/2,y+8,r[2]*k,r[3]*k);else{g.globalAlpha=.4;g.drawImage(taSil(im,id),x+cw/2-r[2]*k/2,y+8,r[2]*k,r[3]*k);}g.restore();}
    textC(g,got?D[1].replace(/ — .*/,""):"???",x+cw/2,y+ch-26*s,11*s,got?"#f6efe0":"rgba(240,230,210,.5)",700);
    if(!got)textC(g,D[6],x+cw/2,y+ch-12*s,10*s,"rgba(240,230,210,.5)",500);else textC(g,D[2],x+cw/2,y+ch-12*s,11*s,"rgba(238,163,187,.85)",600);
    if(got)q.btns.push([x,y,cw,ch,id]);});}
// the end of a flight: records, a new design for the kite day, heights, the duel
function taFinish(G){const q=G.st,K=taS(),dk=dayKey(),h=Math.round(q.max),neu=[],line=[];
  if(!q.done){q.done=1;K.n++;award("ta_first");const rec=h>K.best;q.rec=rec&&K.best>0;if(rec)K.best=h;if(h>=100)award("ta_100");
    if(K.fl!==dk){K.fl=dk;K.days++;const nx=TA_D.find(d=>d[3]==="day"&&d[4]<=K.days&&!K.got.includes(d[0]));if(nx&&taGive(nx[0]))neu.push(nx[0]);}
    for(const d of TA_D)if(d[3]==="h"&&K.best>=d[4]&&taGive(d[0]))neu.push(d[0]);
    if(q.tg&&q.tg.res===1&&taGive("ta_tengu"))neu.push("ta_tengu");
    q.neu=neu;save();}
  if(q.tg)line.push(q.tg.res===1?"Муся перерезала нить тэнгу в бою змеев. «Хо! Крепкая лапа у котёнка», — гудит он с крыши.":q.tg.res===-1?"Тэнгу поднял змея выше и перерезал нить Муси. «Ветер любит смелых. Приходи через неделю», — смеётся он.":"Бой змеев с тэнгу не решился — он поднимет змея и в следующий полёт.");
  if(q.snagN)line.push(`Змей ${q.snagN===1?"один раз цеплялся":q.snagN+" раза цеплялся"} за сосны.`);
  const D=TA_ID[q.sel];
  return`<div class="card"><p class="tag">凧揚げ · ${D[2]}</p><h3>${q.rec?"Новый рекорд высоты!":"Змей опустился на траву"}</h3><div class="big">${h} м</div>
   <p>Рекорд: ${K.best} м · змеев ${K.got.length} из ${TA_D.length}.</p>${line.map(l=>`<p class="ta-s">${l}</p>`).join("")}
   ${(q.neu||[]).map(id=>`<div class="dish">${itemThumb(IT[id],110,120)}</div><p>Новый змей: <b>${TA_ID[id][1]}</b> ${TA_ID[id][2]} — он висит в «🧺 Вещи».</p>`).join("")}
   ${!(q.neu||[]).length&&K.got.length<TA_D.length?`<p class="ta-s">${K.fl===dk?"Новый змей — в следующий ветреный день":""}${K.best<100?" · на 100 м ждёт дракон 龍":K.best<150?" · на 150 м ждёт воин 武":""}</p>`:""}
   <div class="row"><button class="btn" id="gHome">Домой</button><button class="btn primary" id="gAgain">Ещё полёт</button></div></div>`;}

function taOpen(){if(G.id)return;const K=taS();
  if(petAway()){toast("Муся в пути — змей подождёт её");return;}
  if(!taIsDay()){toast("🍃 Безветренно — змей не взлетит");return;}
  if(weather.on){toast("🌧 Под дождём змей размокнет");return;}
  if(!K.got.includes("ta_kaze"))taGive("ta_kaze",true);closePanel();taImg();BI_IMC();openPlace("ta_fly");}

// ── hooks
hook("boot",()=>{taS();taCheck();taFetch(false);});
let taSec=0;
hook("sec",()=>{taSec++;if(taSec%20===3)taFetch(false);if(taSec%10===5)taCheck();
  const K=taS(),dk=dayKey();if(taSec>6&&K.ts!==dk&&taIsDay()&&K.fl!==dk&&!scene.on&&!G.id&&!document.hidden&&!overlaysOpen()&&!$("toast").classList.contains("on")){K.ts=dk;toast(taNY(dk)?"🪁 Сёгацу — время запускать змея":"🪁 Поднялся ветер — пора запускать змея");save();}});
hook("hubDot",()=>{const K=taS();return taIsDay()&&K.fl!==dayKey()&&!petAway();});
hook("tray",(tray,room)=>{if((S.trayMode[room]||"play")!=="play"||!taIsDay())return;const K=taS();
  if(room==="courtyard"){const el=tray.querySelector(".items");if(!el||el.querySelector('[data-x="ta:open"]'))return;
    el.insertAdjacentHTML("afterbegin",`<button class="item wide" data-x="ta:open"><span class="ico">🪁</span><span class="nm">Змей</span></button>`);}
  else if(room==="games"){const el=tray.querySelector(".glist");if(!el||el.querySelector('[data-x="ta:open"]'))return;const W=taWind();
    el.insertAdjacentHTML("afterbegin",`<h4>Ветреный день</h4><div class="games"><button class="gcard" data-x="ta:open"><b>🪁 Воздушный змей</b><span>${W.src==="now"?`Ветер ${W.sp} км/ч`:"凧揚げ · такоагэ"}</span><em>Рекорд: ${K.best} м</em></button></div>`);}});
hook("hub",()=>{const K=taS(),day=taIsDay(),wk=taWeek(),tg=K.n>=1&&K.tgw!==wk&&day,sel=TA_ID[K.got.includes(K.sel)?K.sel:"ta_kaze"];
  return`<div class="hubc"><h4>🪁 Воздушный змей <i>凧揚げ</i></h4><p>${taLine()}</p>
   <p class="ta-s">${taLine2()}${K.n?`Рекорд высоты: ${K.best} м · полётов: ${K.n} · змеев`:"Змеев"} ${Math.max(1,K.got.length)} из ${TA_D.length}. Новый змей — за каждый ветреный день с полётом и за высоту 100 и 150 м.</p>
   ${K.n>=1?`<p class="ta-s">${K.tgw===wk?"👺 Бой змеев с тэнгу на этой неделе уже был — следующий через неделю.":"👺 Тэнгу с дальней крыши ждёт боя змеев (кэнка-дако): он поднимет своего змея в следующий полёт."}</p>`:""}
   <div class="row">${day?`<button class="btn primary" data-x="ta:open">🪁 Запустить «${sel[1].replace(/ — .*/,"")}»</button>`:""}<button class="btn" data-x="ta:list">Змеи</button></div></div>`;});
function taList(){const K=taS();if(!K.got.includes("ta_kaze"))taGive("ta_kaze",true);
  openPanel("Воздушные змеи",`<p class="lead">Выбери змея для следующего полёта. Каждый полученный змей ещё и висит в «🧺 Вещи» — его можно повесить на стену.</p>
   <div class="ta-grid">${TA_D.map(d=>{const got=K.got.includes(d[0]);return`<button class="btn ta-k ${got?"":"off"} ${got&&K.sel===d[0]?"on":""}" data-x="ta:sel:${d[0]}">${itemThumb(IT[d[0]],80,90)}<b>${got?d[1]:"???"}</b><small>${got?d[2]:d[5]}</small></button>`;}).join("")}</div>
   <p class="ta-s">Рекорд высоты: ${K.best} м. Ветреные дни — по настоящему ветру в твоём городе (📍 в карточке погоды), а в Новый год змей летит всегда.</p>`,"ta_list");}
hook("click",k=>{if(!k.startsWith("ta:"))return false;
  if(k==="ta:open"){taOpen();return true;}if(k==="ta:list"){taList();return true;}
  if(k.startsWith("ta:sel:")){const id=k.slice(7),K=taS();if(K.got.includes(id)){K.sel=id;save();sfx("pop");}else toast("🪁 "+TA_ID[id][5]);taList();return true;}return true;});
hook("album",el=>{const K=taS();if(!K.got.length)return;
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Воздушные змеи</h3><p class="lead">Рекорд высоты ${K.best} м, полётов ${K.n}.</p><div class="coll">${TA_D.map(d=>`<div class="ci ${K.got.includes(d[0])?"on":""}">${itemThumb(IT[d[0]],60,70)}<small>${K.got.includes(d[0])?d[1]:"???"}</small></div>`).join("")}</div>`);});
hook("away",ms=>{const K=taS();if(ms<3*3600e3||!taIsDay()||K.fl===dayKey())return null;return{i:"🪁",t:"Поднялся ветер — можно запустить змея"};});

// on a kite day a neighbour's kite hangs in the courtyard sky (a tap opens the flight)
let taRK=null;
hook("overlay",t=>{taRK=null;if(S.room!=="courtyard"||scene.on||G.id||!taIsDay()||weather.on)return;const im=taImg();if(!im)return;
  const [x,y]=imgToStage(1180+Math.sin(t*.4)*14,400+Math.sin(t*.7)*8,.3),[x2]=imgToStage(1280,400,.3),k=Math.max(.25,(x2-x)/100),hh=36*k,sg=Math.sin((taWind().dir||270)*Math.PI/180)<0?1:-1;
  ctx.save();const gr=ctx.createLinearGradient(x,y,x-sg*120*k,y+220*k);gr.addColorStop(0,"rgba(240,232,212,.55)");gr.addColorStop(1,"rgba(240,232,212,0)");ctx.strokeStyle=gr;ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(x,y);ctx.quadraticCurveTo(x-sg*50*k,y+120*k,x-sg*120*k,y+220*k);ctx.stroke();ctx.globalAlpha=dayTint()[1]?.75:.9;
  const id=taS().got.includes(taS().sel)?taS().sel:"ta_kaze";taKite(ctx,im,id,x,y,hh,Math.sin(t*1.3)*.1,t,sg,1);ctx.restore();taRK=[x,y,Math.max(28,hh)];});
hook("hit",(x,y)=>{if(!taRK||S.room!=="courtyard"||Math.hypot(x-taRK[0],y-taRK[1])>taRK[2])return false;taOpen();return true;});

// test handles
X.kite={S:taS,day:taIsDay,wind:taWind,line:taLine,next:taNext,open:taOpen,list:taList,fetch:()=>taFetch(true),give:taGive,phys:taPhys,
  pick(i){if(G.id==="ta_fly"&&G.st.ph==="pick"){const b=G.st.btns[i||0];if(b)TA_G.down(G,b[0]+5,b[1]+5,now());}},
  ff(sec,hold){if(G.id!=="ta_fly")return;for(let i=0;i<sec*60&&!G.over;i++){G.held=typeof hold==="function"?hold(G.st):!!hold;G.time-=1/60;TA_G.step(G,now(),1/60);if(G.time<=0){G.time=0;gEnd();}}G.held=false;},
  bot:q=>q.T<.5,   // a simple player: pull while the tension is low
  crow(){if(G.id==="ta_fly"){G.st.crowT=G.st.clk;}},tengu(){if(G.id==="ta_fly"){G.st.tgOn=true;G.st.t1=G.st.clk-10;}},
  rk:()=>taRK,fake(sp,dir=270,rain=false){const K=taS();K.w={city:taCity()||"nn",at:Date.now(),sp,dir,rain,day:dayKey(),f:[]};K.try=Date.now();taCheck();}};
}
