{
// ───────── «Чайная церемония» 茶道: every third day (from the add-on's first day) a yōkai sends word that they will come
// for tea in the evening (from 17:00). The guest waits in the tea house (or on the veranda with a travel tea box while the
// tea house is still closed) until served. The ceremony is a hidden mini-game over a painted tatami seen from above:
// 9 steps with gestures; order slips and sloppy gestures soften the score (1–3 ★). ★★★ with a guest → a tea thing.
// Other days: practise alone, Musya is the guest. State: S.ext.tea {d0,n,best,served:{id:day},done,told,arr,g:{d,id},gifts}
// Art: art/tea_art.py → assets/bg/te_mat.webp, assets/items/atlas_te.webp
const TE_ATL=[1400,700],TE_SPR={"g_bowl":[454,0,260,260],"g_natsume":[242,432,150,150],"g_kama":[132,0,320,320],"g_kensui":[1030,0,180,180],"g_mizusashi":[716,0,190,190],"g_chasen":[394,432,130,130],"g_hishaku":[0,604,420,96],"g_chashaku":[594,604,300,44],"g_fukusa":[1214,432,150,104],"g_wagashi":[1072,432,140,112],"g_chabako":[0,432,240,170]};
const TE_SRC="🍵 подарок гостя",TE_HINT="Гость дарит её за чайную церемонию на ★★★";
addItems([{"id":"te_raku","n":"Чаван раку с золотым швом","c":"Чайная церемония","w":180,"h":130,"a":"b","p":120,"at":["te",526,432]},{"id":"te_natsume","n":"Нацумэ под красным лаком","c":"Чайная церемония","w":130,"h":124,"a":"b","p":110,"at":["te",708,432]},{"id":"te_chasen","n":"Бамбуковый тясэн на подставке","c":"Чайная церемония","w":120,"h":190,"a":"b","p":50,"at":["te",908,0]},{"id":"te_fukusa","n":"Шёлковая фукуса","c":"Чайная церемония","w":170,"h":96,"a":"b","p":60,"at":["te",422,604]},{"id":"te_kashi","n":"Осенние вагаси на лаковом подносе","c":"Чайная церемония","w":230,"h":120,"a":"b","p":80,"at":["te",840,432]},{"id":"te_jiku","n":"Свиток «Итиго итиэ» с кругом энсо","c":"Чайная церемония","w":130,"h":430,"a":"b","p":140,"at":["te",0,0]}].map(i=>Object.assign(i,{src:TE_SRC,hint:TE_HINT})),{te:TE_ATL});
const TE_GIFTS=["te_raku","te_fukusa","te_natsume","te_kashi","te_chasen","te_jiku"];
STAMPS.push(["te_first","茶","Первая церемония","Проведи чайную церемонию"],["te_star3","雅","Три звезды","Проведи чайную церемонию на ★★★"],["te_guests7","客","Семь гостей за чаем","Угости чаем семь разных ёкаев"]);
// guests: f = feminine (for verbs), h = height in the room, th = height in the ceremony view; hi/ty = what they say
const TE_G=[
 {id:"nekomata",mon:"m_nekomata",n:"Нэкомата",f:1,h:340,th:300,hi:"Мяу… Сто лет не сидела на татами. Заваривай, сестрёнка, я не тороплюсь.",ty:"Вот это чай. Как в старом замке, при свечах. Мур-р."},
 {id:"kitsune",mon:"m_kitsune",n:"Лиса-невеста",f:1,h:350,th:300,hi:"В святилище Инари тоже пьют маття. Посмотрим, чей вкуснее.",ty:"Даже у Инари так не взбивают. Я расскажу о тебе лисам."},
 {id:"chagama",mon:"m_rm_chagama",n:"Бунбуку-тягама",h:300,th:250,hi:"Я сам когда-то был чайником, так что не обессудь — придирчив!",ty:"Сам бы лучше не заварил. А я ведь чайник! Буль-буль."},
 {id:"usagi",mon:"m_rg_usagi",n:"Цуки-но усаги",h:330,th:290,hi:"Всю ночь толок моти на луне. Чашечка чая — как раз то, что нужно.",ty:"Пена белая, как лунный свет. В следующий раз принесу тебе моти."},
 {id:"tanuki",mon:"m_tanuki",n:"Тануки",h:340,th:300,hi:"Пом-пом! Чай я люблю почти так же, как поесть.",ty:"Ух! Так хорошо, что даже превращаться ни во что не хочется."},
 {id:"kappa",mon:"m_kappa",n:"Каппа",h:330,th:300,hi:"Говорят, здесь заваривают чай по всем правилам. Я только блюдце на макушке поправлю.",ty:"Безупречно. Я расскажу о вас всей реке."},
 {id:"warashi",mon:"m_warashi",n:"Дзасики-вараси",f:1,h:360,th:320,hi:"Только чтобы не горько! И чтобы с пенкой!",ty:"Пенка! Самая настоящая! Я теперь у вас поселюсь, хи-хи."},
 {id:"tengu",mon:"m_rm_tengu",n:"Тэнгу",h:400,th:330,hi:"Я учил фехтованию воинов. Посмотрим, как ты владеешь венчиком.",ty:"Ни одного лишнего движения. Достойно горы Курама."},
 {id:"akaname",mon:"m_akaname",n:"Аканамэ",h:300,th:270,hi:"Я тут всё вылизал, чистота! Теперь бы чайку.",ty:"Чашу даже мыть не придётся — вылизал до блеска! Вот это церемония."},
 {id:"obake",mon:"m_obake",n:"Тётин-обакэ",h:300,th:290,hi:"Во мне сто лет горела свеча. А чаю я не пил… ни разу.",ty:"Так вот он какой, чай… Теперь я буду светить вашему чайному домику."}];
const TE_TY2=["Хороший чай. Спасибо, что пригласили.","Тёплая чашка в холодный вечер — что ещё нужно?"],TE_TY1=["Чай есть чай. Спасибо за вечер.","Ничего, путь чая долгий. Я приду ещё."];
const TE_SLIP=["Тише, не спеши…","Кажется, сейчас черёд другого…","Хм… порядок чуть сбился."];
const TE={im:null,mat:null,mode:null,back:null,bw:0,bh:0,ff:null,sh:null,t0:now()};
const teS=()=>S.ext.tea||(S.ext.tea={d0:dayKey(),n:0,best:0,served:{},done:"",told:"",arr:"",g:null,gifts:[]});
const teV=(g,m,f)=>g&&g.f?f:m;
const tePool=()=>TE_G.filter(g=>MON[g.mon]);
function teIdx(){const T=teS(),d=Math.round((Date.parse(dayKey()+"T12:00:00Z")-Date.parse(T.d0+"T12:00:00Z"))/864e5);return((d%3)+3)%3;}
const teDay=()=>teIdx()===0;
function teGuest(){if(!teDay())return null;const T=teS(),dk=dayKey();
  if(!T.g||T.g.d!==dk){const P=tePool();if(!P.length)return null;const un=P.filter(g=>!T.served[g.id]),L=un.length?un:P,v=Math.round((Date.parse(dk)-Date.parse(T.d0))/864e5/3);T.g={d:dk,id:L[((v%L.length)+L.length)%L.length].id};}
  return TE_G.find(g=>g.id===T.g.id)||null;}
const teEve=()=>hourNow()>=17;
const teHere=()=>teEve()&&teS().done!==dayKey()&&!!teGuest();
const teHouse=()=>ROOMS.some(r=>r.id==="chashitsu")&&!hk("tabLock","chashitsu");
const teRoom=()=>teHouse()?"chashitsu":"engawa";
function teMsg(g){const a=`🍵 Сегодня вечером на чай придёт ${g.n}`;return a.length<=45?a:`🍵 Вечером на чай придёт ${g.n}`;}
const teArr=g=>`🍵 ${g.n} ${teV(g,"пришёл","пришла")} на чай`;

// ── the ceremony view: stage 900×1500 (the painted tatami), contained in the game field
const TE_P={guest:[615,402],musya:[250,420],kama:[690,640],hish:[500,560],mizu:[180,560],nat:[300,900],shak:[270,1010],bowl:[590,1010],chasen:[790,875],kensui:[160,1250],fuku:[470,1300],gbowl:[560,505]};
const TE_HA=-.64,TE_HLEN=330;   // the ladle rests with its handle to the lower left
const TE_STEPS=[
 {k:"pn",n:"Фукуса и нацумэ",hint:"Протри нацумэ фукусой: веди пальцем по крышке",ok:["nat","fuku"]},
 {k:"pc",n:"Фукуса и тясяку",hint:"Протри тясяку: проведи вдоль ложечки",ok:["shak","fuku"]},
 {k:"wb",n:"Тёплая чаша",hint:"Согрей чашу: нажми на черпак",ok:["hish","kama","bowl"]},
 {k:"em",n:"Вода в кэнсуй",hint:"Вылей воду в кэнсуй: перетащи туда чашу",ok:["bowl"],soft:["kensui"]},
 {k:"mt",n:"Две ложечки маття",hint:"Две ложечки маття: нажми на нацумэ дважды",ok:["nat","shak"]},
 {k:"wt",n:"Кипяток",hint:"Держи палец на черпаке — и не перелей",ok:["hish","kama"],soft:["bowl"]},
 {k:"wh",n:"Венчик",hint:"Взбей чай: быстро води венчиком зигзагом",ok:["bowl","chasen"]},
 {k:"tn",n:"Поворот чаши",hint:"Поверни чашу дважды по часовой стрелке",ok:["bowl"]},
 {k:"sv",n:"Подача",hint:"Подай чашу гостю: подвинь её вверх",ok:["bowl"]}];
const TE_NOTE={pn:"Фукуса скользила торопливо — утварь любит неспешность.",pc:"Фукуса скользила торопливо — утварь любит неспешность.",wb:"Чашу грели суетливо.",em:"Вода плеснула мимо кэнсуя.",
 mt:"Маття многовато — чай вышел терпким.",wtH:"Воды многовато — чай жидковат.",wtL:"Воды маловато — чай густой, почти как кой-тя.",wh:"Пена не поднялась как следует — венчику не хватило задора.",
 tn:"Чашу повернули не в ту сторону.",sv:"Чашу подали не с первого раза.",slip:"Порядок сбился — гость вежливо сделал вид, что не заметил."};
const TE_SUM=["","Чай выпит, и это главное. Путь чая долог — в следующий раз выйдет лучше.","Хорошая чашка. До мастера — пара вечеров.","Безупречно: тишина, пар над котлом и пена, лёгкая, как облако."];
const teD=(a,b,c,d)=>Math.hypot(a-c,b-d);
function teSeg(u,v,ax,ay,bx,by){const dx=bx-ax,dy=by-ay,l=dx*dx+dy*dy,s=clamp(((u-ax)*dx+(v-ay)*dy)/l,0,1);return teD(u,v,ax+s*dx,ay+s*dy);}
const teHishEnd=()=>[TE_P.hish[0]-Math.cos(TE_HA)*TE_HLEN,TE_P.hish[1]-Math.sin(TE_HA)*TE_HLEN];
function teObj(u,v,q){const B=q.B,P=TE_P;
  if(teD(u,v,...P.hish)<58||teSeg(u,v,...P.hish,...teHishEnd())<26)return"hish";
  if(teD(u,v,B.x,B.y)<138)return"bowl";
  if(teD(u,v,...P.nat)<80)return"nat";if(teSeg(u,v,P.shak[0]-140,P.shak[1],P.shak[0]+140,P.shak[1])<30)return"shak";
  if(teD(u,v,...P.kensui)<95)return"kensui";if(teD(u,v,...P.chasen)<66)return"chasen";if(teD(u,v,...P.kama)<150)return"kama";
  if(teD(u,v,...P.fuku)<80)return"fuku";if(teD(u,v,...P.mizu)<95)return"mizu";return null;}
function teSay(q,txt,t,dur=3.2){q.say={txt,t,dur};}
function teSlip(q,st,t){st.qual=Math.max(.3,st.qual-.15);q.slips++;q.shake=t;tone(196,.18,"triangle",.035);if(q.gd)teSay(q,pick(TE_SLIP),t,2.2);}
function teLay(G){const k=Math.min(G.W/900,G.H/1500);return{k,ox:(G.W-900*k)/2,oy:(G.H-1500*k)/2};}
function teNext(G,t){const q=G.st;if(q.st)q.q.push({k:q.st.k,v:q.st.qual,lv:q.st.lv});q.i++;const d=TE_STEPS[q.i];
  if(!d){q.st=null;q.phase="fin";q.fin=t;teFinish(G,t);return;}
  q.st={k:d.k,t0:t,done:false,qual:1,ph:0,n:0,len:0,a:0,c:0,strokes:0,anim:null,drag:null};tone(660,.08,"sine",.03);}
const teDone=(st,t)=>{if(!st.done){st.done=true;st.doneT=t;chime([784,988]);}};
function teAnim(st,k,t,d){st.anim={k,t0:t,d};}
const teAu=(st,t)=>st.anim?clamp((t-st.anim.t0)/st.anim.d,0,1):1;
const ease=u=>u<.5?2*u*u:1-2*(1-u)*(1-u);
function teStars(q){const v=q.q.map(x=>x.v),avg=v.reduce((a,b)=>a+b,0)/Math.max(1,v.length)-Math.max(0,q.slips-2)*.03;return avg>=.85?3:avg>=.62?2:1;}
function teNote(q){let w=null;for(const x of q.q)if(x.v<.95&&(!w||x.v<w.v))w=x;if(q.slips>=2&&(!w||w.v>.7))return TE_NOTE.slip;if(!w)return"";return w.k==="wt"?(w.lv>.7?TE_NOTE.wtH:TE_NOTE.wtL):TE_NOTE[w.k];}
function teFinish(G,t){const q=G.st,T=teS(),gd=q.gd,stars=teStars(q);q.stars=stars;q.note=teNote(q);G.score=stars;T.n=(T.n||0)+1;q.rec=stars>(T.best||0);T.best=Math.max(T.best||0,stars);
  if(gd){T.done=dayKey();T.served[gd.id]=dayKey();q.first=disc("tea",gd.id);const b=BESTIARY.find(e=>e[1]===gd.mon);if(b&&!ST.seen.includes(b[0]))ST.seen.push(b[0]);
    teSay(q,stars===3?gd.ty:pick(stars===2?TE_TY2:TE_TY1),t+.9,3.6);
    if(stars===3){const id=TE_GIFTS.find(i=>!S.owned.has(i));if(id){S.owned.add(id);T.gifts.push(id);q.gift=id;}}}
  award("te_first");if(stars===3)award("te_star3");if(Object.keys(T.served).length>=7)award("te_guests7");
  if(!petAway()){S.needs.joy=clamp(S.needs.joy+6,0,100);S.needs.food=clamp(S.needs.food+4,0,100);}
  chime(stars===3?[1046,1318,1568,2093]:[784,1046,1318]);save();hubDot();tabDots();}

// ── drawing helpers (stage coords)
function teSpr(g,k,x,y,w,rot=0,al=1,ax=.5,ay=.5){const r=TE_SPR[k],im=TE.im;if(!im||!r||al<=0)return;const s=w/r[2],h=r[3]*s;g.save();g.globalAlpha=al;g.translate(x,y);if(rot)g.rotate(rot);g.drawImage(im,r[0],r[1],r[2],r[3],-w*ax,-h*ay,w,h);g.restore();}
function teShadow(g,x,y,rx,ry,a=.5){if(!TE.sh){const c=document.createElement("canvas");c.width=c.height=64;const h=c.getContext("2d"),gr=h.createRadialGradient(32,32,0,32,32,32);gr.addColorStop(0,"rgba(0,0,0,.75)");gr.addColorStop(.6,"rgba(0,0,0,.4)");gr.addColorStop(1,"rgba(0,0,0,0)");h.fillStyle=gr;h.fillRect(0,0,64,64);TE.sh=c;}
  g.save();g.globalAlpha=a;g.drawImage(TE.sh,x-rx,y-ry,rx*2,ry*2);g.restore();}
function teGlow(g,x,y,r,rgb,a){if(a<=.003)return;const gr=g.createRadialGradient(x,y,0,x,y,r);gr.addColorStop(0,`rgba(${rgb},${a})`);gr.addColorStop(1,`rgba(${rgb},0)`);g.fillStyle=gr;g.fillRect(x-r,y-r,r*2,r*2);}
function teFont(px,w=600){return`${w} ${px}px ${TE.ff||(TE.ff=getComputedStyle(document.body).fontFamily)}`;}
function teWrap(g,txt,maxW){const out=[];let line="";for(const w of txt.split(" ")){const t=line?line+" "+w:w;if(g.measureText(t).width>maxW&&line){out.push(line);line=w;}else line=t;}if(line)out.push(line);return out;}
function teBubble(g,txt,x,y,w,al,tailX){g.save();g.globalAlpha=al;g.font=teFont(29,600);const L=teWrap(g,txt,w-44),h=L.length*38+30;
  g.fillStyle="rgba(240,234,220,.95)";g.beginPath();g.roundRect(x,y,w,h,22);g.fill();g.beginPath();g.moveTo(tailX-14,y+h-2);g.lineTo(tailX+18,y+h-2);g.lineTo(tailX+20,y+h+26);g.fill();
  g.fillStyle="#2a2018";g.textAlign="left";g.textBaseline="top";L.forEach((s,i)=>g.fillText(s,x+22,y+17+i*38));g.restore();}
function teBowl(g,q,t,x,y,al=1){const B=q.B;teShadow(g,x+10,y+14,150,140,.55*al);teSpr(g,"g_bowl",x,y,260,B.rot,al);
  const Ri=104;g.save();g.globalAlpha=al;
  if(B.powder>0&&B.lv<.05){g.fillStyle="#5d7a2a";for(let i=0;i<B.powder;i++){const a=i*2.4,r=i?16:0;g.beginPath();g.ellipse(x+Math.cos(a)*r,y+Math.sin(a)*r,15,12,0,0,Math.PI*2);g.fill();}g.fillStyle="rgba(170,200,110,.5)";g.beginPath();g.arc(x-4,y-5,6,0,Math.PI*2);g.fill();}
  if(B.lv>.01){const r=Ri*(.5+.46*Math.sqrt(Math.min(1,B.lv))),f=B.foam;let col;
    if(B.kind==="hot")col="rgba(190,205,200,.32)";else{const c0=[46,72,24],c1=[156,186,96],m=f*f;col=`rgb(${c0.map((v,i)=>Math.round(v+(c1[i]-v)*m)).join(",")})`;}
    g.fillStyle=col;g.beginPath();g.arc(x,y,r,0,Math.PI*2);g.fill();
    if(B.kind==="tea"&&f>.05){const R=rng(7);g.fillStyle=`rgba(225,240,200,${.35*f})`;for(let i=0;i<Math.floor(70*f);i++){const a=R()*6.283,d=Math.sqrt(R())*r*.92,s=1.5+R()*3.2*f;g.beginPath();g.arc(x+Math.cos(a)*d,y+Math.sin(a)*d,s,0,Math.PI*2);g.fill();}}
    if(B.ripple&&t-B.ripple<1.2){const u=(t-B.ripple)/1.2;g.strokeStyle=`rgba(230,240,230,${.4*(1-u)})`;g.lineWidth=3;g.beginPath();g.arc(x,y,r*(.2+.75*u),0,Math.PI*2);g.stroke();}
    g.fillStyle="rgba(255,255,250,.16)";g.beginPath();g.ellipse(x-r*.35,y-r*.4,r*.32,r*.14,-.6,0,Math.PI*2);g.fill();}
  g.restore();teGlow(g,x-70,y-80,60,"255,240,220",.08*al);}
// the ladle: where its cup is now (rest / over the kama / over the bowl)
function teLadle(q,t){const st=q.st,P=TE_P,B=q.B,rest=P.hish,kama=P.kama,over=[B.x+70,B.y-130];let p=rest,full=false,pour=false;if(!st)return{p,full,pour};const u=teAu(st,t);
  const L=(a,b,w)=>[mix(a[0],b[0],w),mix(a[1],b[1],w)];
  if(st.k==="wb"){if(st.ph===1||st.ph===1.5){const w=st.ph===1.5?1:ease(u);p=w<.5?L(rest,kama,w*2):L(kama,over,w*2-1);full=w>.5;}else if(st.ph===2){p=over;full=u<.9;pour=u<.9;}else if(st.ph===3)p=L(over,rest,ease(u));}
  else if(st.k==="wt"){if(st.ph===1){p=L(rest,over,ease(clamp((t-st.ht)/.35,0,1)));full=true;pour=t-st.ht>.35;}else if(st.ph===2)p=L(over,rest,ease(u));}
  return{p,full,pour};}
function teCam(G,g,t){const q=G.st,L=q.L,W=G.W,H=G.H;
  if(!TE.back||TE.bw!==W||TE.bh!==H){const c=document.createElement("canvas");c.width=Math.max(1,W);c.height=Math.max(1,H);const h=c.getContext("2d");h.fillStyle="#120e0a";h.fillRect(0,0,W,H);
    if(TE.mat){const k=Math.max(W/900,H/1500);h.globalAlpha=.5;h.drawImage(TE.mat,(W-900*k)/2,(H-1500*k)/2,900*k,1500*k);h.globalAlpha=1;h.fillStyle="rgba(8,6,10,.5)";h.fillRect(0,0,W,H);}
    TE.back=c;TE.bw=W;TE.bh=H;}
  g.drawImage(TE.back,0,0,W,H);}

const TE_GAME={id:"te_cha",hidden:true,n:"Чайная церемония",tag:"茶道 · Путь чая",icon:"🍵",bg:"room",lives:null,time:null,lore:"",how:"",
 init(G,t){const q=G.st,gd=TE.mode;Object.assign(q,{gd,i:-1,q:[],slips:0,shake:-9,phase:"play",fin:0,say:null,fx:[],bow:-9,
   B:{x:TE_P.bowl[0],y:TE_P.bowl[1],rot:0,lv:0,kind:"",powder:0,foam:0,ripple:0}});G.score=0;q.L=teLay(G);
   if(gd)teSay(q,gd.hi,t+.4,4.2);teNext(G,t);},
 step(G,t,dt){const q=G.st,st=q.st,B=q.B;q.L=teLay(G);
   if(q.phase==="fin"){if(t-q.fin>5.2&&!q.ended){q.ended=1;gEnd();}return;}
   if(!st)return;const u=teAu(st,t),P=TE_P;
   if(st.k==="wb"){if(st.ph===1&&u>=1){st.ph=1.5;}else if(st.ph===2){B.lv=Math.max(B.lv,.45*u);B.kind="hot";if(u>=1){st.ph=3;teAnim(st,"back",t,.6);}}else if(st.ph===3&&u>=1)teDone(st,t);}
   if(st.k==="em"&&st.ph===2){B.x=mix(B.x,P.kensui[0]+90,.2);B.y=mix(B.y,P.kensui[1]-60,.2);if(u>.4)B.lv=Math.max(0,.45*(1-(u-.4)/.5));if(u>=1){st.ph=3;teAnim(st,"home",t,.5);st.from=[B.x,B.y];sfx("splash");}}
   if(st.k==="em"&&st.ph===3){B.x=mix(st.from[0],P.bowl[0],ease(u));B.y=mix(st.from[1],P.bowl[1],ease(u));B.lv=0;B.kind="";if(u>=1)teDone(st,t);}
   if((st.k==="em"||st.k==="sv")&&st.ph===-1){B.x=mix(st.from[0],P.bowl[0],ease(u));B.y=mix(st.from[1],P.bowl[1],ease(u));if(u>=1)st.ph=0;}
   if(st.k==="mt"&&st.anim&&u>=1){st.anim=null;B.powder=Math.min(4,B.powder+1);tone(330,.12,"triangle",.03);if(st.n>=2&&!st.queue)teDone(st,t);if(st.queue){st.queue=0;teAnim(st,"scoop",t,.75);}}
   if(st.k==="wt"){if(st.ph===1&&t-st.ht>.35){B.lv=Math.min(1.02,B.lv+.3*dt);B.kind="tea";B.ripple=B.ripple&&t-B.ripple<.5?B.ripple:t;if(Math.random()<dt*14)tone(1400+Math.random()*700,.03,"sine",.01);if(B.lv>=1){st.lv=B.lv;st.qual=.3;st.ph=2;teAnim(st,"back",t,.5);teSay(q,"Ох, через край!",t,1.8);}}
     else if(st.ph===2&&u>=1)teDone(st,t);}
   if(st.k==="wh"&&!st.drag&&B.foam<1)B.foam=Math.max(0,B.foam-.03*dt);
   if(st.k==="sv"&&st.ph===2){B.x=mix(st.from[0],P.gbowl[0],ease(u));B.y=mix(st.from[1],P.gbowl[1],ease(u));if(u>=1)st.ph=3;}
   if(st.k==="sv"&&st.ph===4&&u>=1)teDone(st,t);
   if(st.done&&t-st.doneT>.7)teNext(G,t);},
 draw(G,g,t){const q=G.st,L=q.L||teLay(G),P=TE_P,st=q.st,B=q.B,night=dayTint()[1],gd=q.gd;teCam(G,g,t);
   g.save();const sh=clamp(1-(t-q.shake)/.3,0,1)*5;g.translate(L.ox+(Math.random()-.5)*sh,L.oy);g.scale(L.k,L.k);
   g.save();g.beginPath();g.rect(0,0,900,1500);g.clip();
   if(TE.mat)g.drawImage(TE.mat,0,0,900,1500);else{g.fillStyle="#3a3624";g.fillRect(0,0,900,1500);}
   if(night){g.fillStyle="rgba(10,8,22,.28)";g.fillRect(0,0,900,1500);}
   // the guest and Musya across the mat
   const fin=q.phase==="fin"?t-q.fin:-1,away=petAway();
   if(gd&&MIMG[gd.mon]){const im=MIMG[gd.mon],m=MON[gd.mon],h=gd.th,w=m[0]*h/m[1],bob=Math.sin(t*1.6)*3,bw=fin>0&&fin<1.6?Math.sin(fin/1.6*Math.PI)*10:0;
     teShadow(g,P.guest[0],P.guest[1]-6,w*.42,26,.5);g.drawImage(im,P.guest[0]-w/2,P.guest[1]-h+bob+bw,w,h);}
   if(!away){const mx=gd?P.musya[0]:P.guest[0],my=gd?P.musya[1]:P.guest[1]-6,eat=fin>1.8&&fin<4.6;
     const strip=eat?"treat":fin>0&&fin<1.8&&!gd?"purr":"rest",fr=Math.floor(t*(eat?9:2))%8;teShadow(g,mx,my-6,80,20,.45);drawCatG(g,strip,strip==="rest"?fr%2:fr,mx,my,.95);
     if(fin>1.6){const a=clamp((fin-1.6)/.4,0,1)*clamp((4.8-fin)/.4,0,1);teSpr(g,"g_wagashi",mx+(gd?78:-92),my+8-30*(1-clamp((fin-1.6)/.4,0,1)),104,0,a);}
     if(fin>2.2&&fin<4.8)drawEmoji(g,fin<3.4?"😋":"😻",mx+60,my-215-(fin-2.2)*10,44,clamp((4.8-fin)/.5,0,1));}
   // utensils (from the back of the mat to the front)
   teShadow(g,P.mizu[0]+8,P.mizu[1]+12,100,95);teSpr(g,"g_mizusashi",P.mizu[0],P.mizu[1],190);
   const kx=P.kama[0],ky=P.kama[1];g.save();g.globalCompositeOperation="lighter";teGlow(g,kx,ky,190,"255,110,40",.16+.05*Math.sin(t*2.3)+.03*Math.sin(t*7.1));g.restore();
   teShadow(g,kx+10,ky+14,150,145,.6);teSpr(g,"g_kama",kx,ky,320);
   for(let i=0;i<5;i++){const ph=(t*.22+i/5)%1;teGlow(g,kx+Math.sin(t*.9+i*2.1)*30*ph-10,ky-20-ph*170,30+60*ph,"236,234,226",.11*Math.sin(Math.PI*ph));}
   teShadow(g,P.kensui[0]+8,P.kensui[1]+12,95,90);teSpr(g,"g_kensui",P.kensui[0],P.kensui[1],180);
   if(q.kSplash&&t-q.kSplash>=0&&t-q.kSplash<1){const u=t-q.kSplash;g.strokeStyle=`rgba(220,230,225,${.5*(1-u)})`;g.lineWidth=3;g.beginPath();g.arc(P.kensui[0],P.kensui[1],20+60*u,0,Math.PI*2);g.stroke();}
   const natU=st&&st.k==="pn"?clamp(st.len/420,0,1):0;teShadow(g,P.nat[0]+6,P.nat[1]+10,80,76);teSpr(g,"g_natsume",P.nat[0],P.nat[1],150);
   if(natU>0){g.strokeStyle="rgba(255,236,190,.55)";g.lineWidth=5;g.beginPath();g.arc(P.nat[0],P.nat[1],86,-Math.PI/2,-Math.PI/2+natU*6.283);g.stroke();}
   // the scoop: resting, or flying natsume → bowl with a green heap
   let sp=[P.shak[0],P.shak[1]],sa=0,heap=false;
   if(st&&st.k==="mt"&&st.anim){const u=teAu(st,t),tipOff=136;
     if(u<.3){const w=ease(u/.3);sp=[mix(P.shak[0],P.nat[0]-tipOff*.8,w),mix(P.shak[1],P.nat[1]-tipOff*.5,w)];sa=mix(0,.55,w);}
     else if(u<.7){const w=ease((u-.3)/.4);sp=[mix(P.nat[0]-tipOff*.8,B.x-tipOff*.8,w),mix(P.nat[1]-tipOff*.5,B.y-tipOff*.5,w)];sa=.55;heap=true;}
     else{const w=ease((u-.7)/.3);sp=[mix(B.x-tipOff*.8,P.shak[0],w),mix(B.y-tipOff*.5,P.shak[1],w)];sa=mix(.55,0,w);}}
   if(st&&st.k==="pc"){const u=clamp(st.a/500,0,1);if(u>0){g.strokeStyle="rgba(255,236,190,.5)";g.lineWidth=4;g.beginPath();g.moveTo(P.shak[0]-140,P.shak[1]+34);g.lineTo(P.shak[0]-140+280*u,P.shak[1]+34);g.stroke();}}
   teShadow(g,sp[0]+6,sp[1]+10,150,22,.45);teSpr(g,"g_chashaku",sp[0],sp[1],300,sa);
   if(heap){g.fillStyle="#6a8a30";g.beginPath();g.arc(sp[0]+Math.cos(sa)*136,sp[1]+Math.sin(sa)*136,9,0,Math.PI*2);g.fill();}
   // the bowl
   const served=q.phase==="fin";if(!served||fin<1.4)teBowl(g,q,t,B.x,B.y-(served?Math.min(1,fin/1.2)*40:0),served?clamp(1-(fin-.6)/.8,0,1):1);
   if(st&&st.k==="wt"){const gx=B.x+170,y0=B.y+110,hh=220;g.fillStyle="rgba(10,8,6,.55)";g.beginPath();g.roundRect(gx-12,y0-hh-6,24,hh+12,12);g.fill();
     g.fillStyle="rgba(143,208,184,.35)";g.fillRect(gx-10,y0-hh*.74,20,hh*.16);g.fillStyle="#a8c8d8";g.fillRect(gx-7,y0-hh*Math.min(1,B.lv),14,hh*Math.min(1,B.lv));}
   if(st&&st.k==="wh"){g.strokeStyle="rgba(10,8,6,.5)";g.lineWidth=12;g.beginPath();g.arc(B.x,B.y,150,Math.PI*.75,Math.PI*2.25);g.stroke();g.strokeStyle="#c8e09a";g.lineWidth=7;g.beginPath();g.arc(B.x,B.y,150,Math.PI*.75,Math.PI*(.75+1.5*clamp(B.foam,0,1)));g.stroke();}
   // the whisk, the ladle, the cloth
   const wp=st&&st.k==="wh"&&st.drag?st.wp:null;if(wp){teSpr(g,"g_chasen",wp[0],wp[1],120,t*3);}else{teShadow(g,P.chasen[0]+6,P.chasen[1]+8,66,62,.5);teSpr(g,"g_chasen",P.chasen[0],P.chasen[1],130);}
   const La=teLadle(q,t);teShadow(g,La.p[0]-110,La.p[1]+90,190,40,.35);teSpr(g,"g_hishaku",La.p[0],La.p[1],420,TE_HA,1,372/420,.5);
   if(La.full){g.fillStyle="rgba(200,215,210,.55)";g.beginPath();g.arc(La.p[0],La.p[1],26,0,Math.PI*2);g.fill();}
   if(La.pour){g.strokeStyle="rgba(215,230,230,.6)";g.lineWidth=7;g.setLineDash([14,8]);g.lineDashOffset=-t*120;g.beginPath();g.moveTo(La.p[0]-16,La.p[1]+30);g.lineTo(B.x+12,B.y-20);g.stroke();g.setLineDash([]);}
   const fp=st&&(st.k==="pn"||st.k==="pc")&&st.drag?st.fp:P.fuku;teShadow(g,fp[0]+6,fp[1]+10,80,56,.45);teSpr(g,"g_fukusa",fp[0],fp[1],150,st&&st.drag&&(st.k==="pn"||st.k==="pc")?-.2:0);
   // a soft ring around what this step is about (a gentle lesson, not a full tutorial)
   if(st&&!st.done&&q.phase==="play"){const ring=(x,y,r)=>{g.strokeStyle=`rgba(238,163,187,${.28+.18*Math.sin(t*3.5)})`;g.lineWidth=4;g.setLineDash([12,10]);g.beginPath();g.arc(x,y,r,0,Math.PI*2);g.stroke();g.setLineDash([]);};
     const k=st.k;if(k==="pn"||k==="mt")ring(...P.nat,92);else if(k==="pc")ring(P.shak[0],P.shak[1],150);else if((k==="wb"&&st.ph===0)||(k==="wt"&&st.ph===0))ring(...P.hish,62);else if(k==="wb"&&st.ph===1.5)ring(B.x,B.y,142);
     else if(k==="em"&&st.ph===0)ring(...P.kensui,104);else if(k==="sv"&&st.ph===0){g.fillStyle=`rgba(238,163,187,${.25+.15*Math.sin(t*3.5)})`;g.beginPath();g.moveTo(B.x-24,B.y-170);g.lineTo(B.x+24,B.y-170);g.lineTo(B.x,B.y-215);g.fill();}}
   // the bow: the button, then the whole view dips for a moment
   if(st&&st.k==="sv"&&st.ph===3){g.fillStyle="rgba(16,12,10,.85)";g.beginPath();g.roundRect(290,1150,320,96,48);g.fill();g.strokeStyle="rgba(238,163,187,.7)";g.lineWidth=3;g.stroke();g.fillStyle="#f3ead8";g.font=teFont(36,700);g.textAlign="center";g.textBaseline="middle";g.fillText("🙇 Поклониться",450,1199);}
   const bw=t-q.bow;if(bw<1.1){g.fillStyle=`rgba(0,0,0,${.45*Math.sin(Math.PI*clamp(bw/1.1,0,1))})`;g.fillRect(0,0,900,1500);}
   for(const f of q.fx){const e=t-f.t;if(e<1.2)drawEmoji(g,f.g,f.x,f.y-e*40,40,clamp(1.2-e,0,1));}q.fx=q.fx.filter(f=>t-f.t<1.2);
   // what the guest says
   if(q.say&&t>=q.say.t&&t-q.say.t<q.say.dur){const e=t-q.say.t,a=clamp(Math.min(e/.3,(q.say.dur-e)/.4),0,1);teBubble(g,q.say.txt,40,36,560,a,P.guest[0]-40);}
   // the hint strip with the step dots
   if(q.phase==="play"&&st){const txt=st.k==="wb"&&st.ph>=1.5?"Вылей горячую воду в чашу — нажми на неё":st.k==="sv"&&st.ph>=3?(gd?"Поклонись гостю":"Поклонись Мусе"):st.k==="sv"&&!gd?"Подай чашу Мусе: подвинь её вверх":TE_STEPS[q.i].hint;
     g.fillStyle="rgba(10,8,6,.72)";g.beginPath();g.roundRect(30,1388,840,100,24);g.fill();g.font=teFont(29,700);g.fillStyle="#f3ead8";g.textAlign="center";g.textBaseline="middle";g.fillText(txt,450,1450,800);
     TE_STEPS.forEach((s,i)=>{g.fillStyle=i<q.i?"#8fd0b8":i===q.i?"#eea3bb":"rgba(255,255,255,.22)";g.beginPath();g.arc(450+(i-4)*30,1408,7,0,Math.PI*2);g.fill();});}
   g.restore();g.restore();},
 down(G,x,y,t){const q=G.st,st=q.st;if(!st||st.done||q.phase!=="play")return;const L=q.L,u=(x-L.ox)/L.k,v=(y-L.oy)/L.k,B=q.B,P=TE_P,o=teObj(u,v,q),D=TE_STEPS[q.i];
   if(st.k==="sv"&&st.ph===3){if(u>280&&u<620&&v>1140&&v<1256){st.ph=4;q.bow=t;teAnim(st,"bow",t,1.1);tone(150,.3,"sine",.04);}return;}
   if(st.anim&&teAu(st,t)<1&&st.k!=="mt")return;
   const okd=o&&D.ok.includes(o),soft=o&&(D.soft||[]).includes(o);
   if(st.k==="pn"||st.k==="pc"){const near=st.k==="pn"?teD(u,v,...P.nat)<170:teSeg(u,v,P.shak[0]-140,P.shak[1],P.shak[0]+140,P.shak[1])<80;
     if(near||o==="fuku"){st.drag={l:[u,v],lt:t};st.fp=[u,v];st.strokes++;}else if(o&&o!=="mizu")teSlip(q,st,t);return;}
   if((st.k==="wh"&&teD(u,v,B.x,B.y)<175)||(st.k==="tn"&&teD(u,v,B.x,B.y)<180)){}
   else if(o&&!okd&&!soft&&o!=="mizu"){teSlip(q,st,t);return;}
   if(o==="mizu"){tone(523,.2,"sine",.03);return;}
   if(soft){q.shake=t;tone(262,.1,"triangle",.03);return;}
   if(st.k==="wb"){if(st.ph===0&&(o==="hish"||o==="kama")){st.ph=1;teAnim(st,"dip",t,1.1);tone(220,.4,"sine",.03);}else if(st.ph===0&&o==="bowl")teSlip(q,st,t);else if(st.ph===1.5&&(o==="bowl"||o==="hish")){st.ph=2;teAnim(st,"pour",t,1);sfx("splash");}return;}
   if(st.k==="em"||st.k==="sv"){if(st.ph===0&&o==="bowl"){st.drag={dx:B.x-u,dy:B.y-v};tone(300,.06,"triangle",.03);}return;}
   if(st.k==="mt"){if(!okd)return;if(st.anim&&teAu(st,t)<1){if(st.n>=2&&!st.over){st.over=1;st.qual=Math.max(.3,st.qual-.3);B.powder=4;teSay(q,"Ох, крепковато будет…",t,1.8);}else if(st.n<2){st.n++;st.queue=1;}return;}st.n++;teAnim(st,"scoop",t,.75);return;}
   if(st.k==="wt"){if(st.ph===0&&okd){st.ph=1;st.ht=t;}return;}
   if(st.k==="wh"){if(teD(u,v,B.x,B.y)>175&&o!=="chasen")return;if(!st.t1)st.t1=t;st.drag={lx:u,dir:0,seg:0,segT:t};st.wp=teWP(B,u,v);return;}
   if(st.k==="tn"){if(teD(u,v,B.x,B.y)>180)return;st.drag={a0:Math.atan2(v-B.y,u-B.x),acc:0,base:B.rot};}},
 move(G,x,y,held){const q=G.st,st=q.st;if(!st||st.done||!st.drag||!G.held)return;const L=q.L,u=(x-L.ox)/L.k,v=(y-L.oy)/L.k,B=q.B,P=TE_P,t=now();
   if(st.k==="pn"||st.k==="pc"){const [lu,lv]=st.drag.l,d=teD(u,v,lu,lv),dt=Math.max(.016,t-st.drag.lt);st.fp=[u,v];if(d<2)return;
     if(st.k==="pn"){if(teD(u,v,...P.nat)<88){st.len+=d;if(d/dt>4200)st.c+=d;if(Math.random()<.3)tone(2400+Math.random()*600,.03,"sine",.008);}if(st.len>=420){st.qual=clamp(1-Math.min(.4,st.c/st.len*.7)-Math.max(0,st.strokes-4)*.08,.3,1);teDone(st,t);st.drag=null;}}
     else{if(teSeg(u,v,P.shak[0]-140,P.shak[1],P.shak[0]+140,P.shak[1])<50){st.a+=Math.abs(u-lu);st.c+=Math.abs(v-lv);}if(st.a>=500){st.qual=clamp(1.12-st.c/st.a*1.6-Math.max(0,st.strokes-4)*.08,.35,1);teDone(st,t);st.drag=null;}}
     if(st.drag){st.drag.l=[u,v];st.drag.lt=t;}return;}
   if(st.k==="em"||st.k==="sv"){B.x=u+st.drag.dx;B.y=v+st.drag.dy;return;}
   if(st.k==="wh"){const w=teWP(B,u,v),dx=u-st.drag.lx;st.wp=w;if(Math.abs(dx)<1.5)return;const dir=Math.sign(dx);
     if(st.drag.dir&&dir!==st.drag.dir&&st.drag.seg>=24){const sp=st.drag.seg/Math.max(.03,t-st.drag.segT);B.foam=Math.min(1,B.foam+.05*clamp(sp/1300,.25,1.2));st.drag.seg=0;st.drag.segT=t;B.ripple=t;tone(1900+Math.random()*900,.03,"triangle",.012);
       if(B.foam>=1){const e=t-st.t1;st.qual=e<=5?1:e<=9?.85:e<=14?.7:.55;teDone(st,t);st.drag=null;return;}}
     if(dir!==st.drag.dir){st.drag.dir=dir;}st.drag.seg+=Math.abs(dx);st.drag.lx=u;return;}
   if(st.k==="tn"){const a=Math.atan2(v-B.y,u-B.x);let da=a-st.drag.a0;da=Math.atan2(Math.sin(da),Math.cos(da));st.drag.a0=a;st.drag.acc+=da;B.rot=st.drag.base+clamp(st.drag.acc,-.5,1.6);
     if(st.drag.acc>=1.2){st.n++;st.drag.base+=Math.PI/2;st.drag.acc=0;B.rot=st.drag.base;chime([659,880]);if(st.n>=2){teDone(st,t);st.drag=null;}}
     else if(st.drag.acc<=-.55){st.qual=Math.max(.3,st.qual-.25);B.rot=st.drag.base;st.drag=null;q.shake=t;tone(196,.18,"triangle",.035);teSay(q,q.gd?"Не в ту сторону…":"",t,q.gd?1.8:0);q.fx.push({g:"↻",x:B.x,y:B.y-160,t});}}},
 up(G){const q=G.st,st=q.st;if(!st||st.done||!st.drag){if(st&&st.k==="wt"&&st.ph===1)teWtUp(q,st);return;}const B=q.B,P=TE_P,t=now();
   if(st.k==="em"){st.drag=null;if(teD(B.x,B.y,...P.kensui)<170){st.ph=2;teAnim(st,"pour",t,.9);q.kSplash=t+.45;}else{st.qual=Math.max(.3,st.qual-.15);st.ph=-1;st.from=[B.x,B.y];teAnim(st,"home",t,.45);q.shake=t;}return;}
   if(st.k==="sv"){st.drag=null;if(B.y<760){st.ph=2;st.from=[B.x,B.y];teAnim(st,"slide",t,.6);tone(392,.2,"sine",.03);}else{st.qual=Math.max(.4,st.qual-.15);st.ph=-1;st.from=[B.x,B.y];teAnim(st,"home",t,.45);}return;}
   if(st.k==="tn"){B.rot=st.drag.base;}
   st.drag=null;},
 stat:G=>{const q=G.st;return q.phase==="fin"?(q.gd?`${q.gd.n} пьёт чай`:"Муся пробует чай"):`Шаг ${q.i+1} из ${TE_STEPS.length}${q.gd?" · гость: "+q.gd.n:" · тренировка"}`;},
 card(G){const q=G.st,gd=q.gd,s=q.stars||1,T=teS(),gi=q.gift&&IT[q.gift];
   return`<div class="card"><p class="tag">茶道 · Путь чая</p><h3>${gd?`Чай для гостя: ${gd.n}`:"Чай для Муси"}</h3><div class="stars">${"★".repeat(s)}${"☆".repeat(3-s)}</div>
   <p>${TE_SUM[s]}${q.note&&s<3?" "+q.note:""}</p>${gd?`<p class="lore">«${q.say?q.say.txt:gd.ty}»</p>`:petAway()?"":`<p class="lore">Муся сидела смирно, понюхала пенку и получила вагаси.</p>`}
   ${gi?`<div class="dish">${itemThumb(gi,170,120)}</div><p>Подарок гостя: <b>${gi.n}</b>. Найдёшь в «🧺 Вещи».</p>`:""}
   <p style="opacity:.75">Лучшая церемония: ${"★".repeat(T.best||s)}${"☆".repeat(3-(T.best||s))} · гостей за чаем: ${Object.keys(T.served).length} из ${tePool().length}</p>
   <div class="row"><button class="btn" id="gHome">Домой</button><button class="btn primary" id="gAgain">Ещё раз</button></div></div>`;},
 after(G){$("gAgain").onclick=()=>{TE.mode=teHere()?teGuest():null;beginGame();};ui();}};
GAMES.push(TE_GAME);
function teWP(B,u,v){const d=teD(u,v,B.x,B.y),r=Math.min(d,92),a=Math.atan2(v-B.y,u-B.x);return[B.x+Math.cos(a)*r,B.y+Math.sin(a)*r];}
function teWtUp(q,st){if(st.ph!==1)return;const B=q.B,t=now();if(B.lv<.15){st.ph=0;return;}st.lv=B.lv;const e=Math.abs(B.lv-.66);st.qual=clamp(1-Math.max(0,e-.08)*3.2,.3,1);st.ph=2;teAnim(st,"back",t,.5);}
function teOpen(){if(G.id)return;closePanel();TE.mode=teHere()?teGuest():null;if(!TE.im)atlasImg("te",im=>TE.im=im);openPlace("te_cha");}

// ── in the rooms: the guest waits on a cushion in the tea house, or on the veranda beside a travel tea box
const TE_RP={chashitsu:[600,1236],engawa:[560,1250]};   // veranda: left of Musya — the bonsai stands on the right
function tePos(){const r=TE_RP[S.room];if(!r)return null;return[visX(r[0],S.room==="engawa"?150:120),r[1]];}
function teDrawRoom(t,front){if(!teHere()||S.room!==teRoom()||scene.on)return;const g=teGuest(),p=tePos();if(!g||!p)return;const [ix,iy]=p;if((iy>catLineY()+6)!==front)return;
  const a=clamp((now()-TE.t0)/1.2,0,1),k=BGM.k,[sx,sy]=imgToStage(ix,iy,CAT_D);
  ctx.save();ctx.globalAlpha=a*.85;ctx.fillStyle=S.room==="chashitsu"?"#3a2230":"#2a2a3a";ctx.beginPath();ctx.ellipse(sx,sy-4*k,110*k,26*k,0,0,Math.PI*2);ctx.fill();ctx.restore();
  drawMon(g.mon,ix,iy+Math.sin(t*1.6)*3,g.h*.82,CAT_D,a);
  if(S.room==="engawa"&&TE.im){const r=TE_SPR.g_chabako,w=180*k,h=r[3]*w/r[2],[bx,by]=imgToStage(ix+110,iy+46,CAT_D);ctx.save();ctx.globalAlpha=a;ctx.drawImage(TE.im,r[0],r[1],r[2],r[3],bx-w/2,by-h,w,h);ctx.restore();}
  const side=imgToStage(ix,iy,CAT_D)[0]>view.W*.6?-1:1,[hx,hy]=imgToStage(ix+side*g.h*.3,iy-g.h*.86,CAT_D),r=26*view.s,pu=1+.06*Math.sin(t*3);ctx.save();ctx.globalAlpha=a*.95;ctx.fillStyle="rgba(238,233,220,.93)";ctx.beginPath();ctx.arc(hx,hy,r*pu,0,Math.PI*2);ctx.fill();ctx.restore();drawEmoji(ctx,"🍵",hx,hy,r*1.15,a);}
function teHit(x,y){if(!teHere()||S.room!==teRoom()||scene.on)return false;const g=teGuest(),p=tePos();if(!g||!p)return false;const [sx,sy]=imgToStage(p[0],p[1],CAT_D),h=g.h*.9*BGM.k,w=h*.7;
  let hit=x>sx-w/2&&x<sx+w/2&&y>sy-h&&y<sy+10;if(!hit&&S.room==="engawa"){const [bx,by]=imgToStage(p[0]+110,p[1]+46,CAT_D);hit=Math.abs(x-bx)<100*BGM.k&&y>by-140*BGM.k&&y<by+20;}
  if(!hit)return false;audioInit();tone(523,.15,"sine",.03);teOpen();return true;}
hook("draw",teDrawRoom);
hook("hit",teHit);
hook("room",()=>{TE.t0=now();});
hook("tray",(tray,room)=>{if((S.trayMode[room]||"play")!=="play")return;const row=tray.querySelector(".items");if(!row||row.querySelector('[data-x="te:open"]'))return;
  const here=teHere();if(room!=="chashitsu"&&!(room==="engawa"&&here&&!teHouse()))return;
  const b=`<button class="item wide" data-x="te:open"><span class="ico">🍵</span><span class="nm">${here?"Чай для гостя":"Чайная церемония"}</span></button>`,sc=row.querySelector('[data-x="ro2:scroll"]');
  if(sc&&!here)sc.insertAdjacentHTML("afterend",b);else row.insertAdjacentHTML("afterbegin",b);});
hook("click",k=>{if(!k.startsWith("te:"))return;if(k==="te:open")teOpen();else if(k==="te:go"){closePanel();goRoom(teRoom());}return true;});
hook("hubDot",()=>teHere());
hook("tabDot",r=>teHere()&&r===teRoom());
hook("sec",()=>{if(now()<4||scene.on||overlaysOpen()||$("toast").classList.contains("on"))return;   // wait for a free toast line
  const T=teS(),dk=dayKey();if(!teDay()||T.done===dk)return;const g=teGuest();if(!g)return;
  if(T.told!==dk){T.told=dk;if(teEve())T.arr=dk;save();toast(teEve()?teArr(g):teMsg(g));hubDot();tabDots();return;}
  if(teEve()&&T.arr!==dk){T.arr=dk;save();toast(teArr(g));hubDot();tabDots();ui();}});
hook("hub",()=>{const T=teS(),g=teGuest(),dk=dayKey(),idx=teIdx(),best=T.best||0,nS=Object.keys(T.served).length;
  let st;if(g&&T.done===dk)st="Сегодняшний гость напоён чаем. Следующий — через три дня";else if(g&&teEve())st=`${g.n} ждёт чая ${teHouse()?"в чайном домике":"на веранде"}`;else if(g)st=`Сегодня вечером на чай придёт ${g.n}`;else st=idx===2?"Следующий гость — завтра вечером":"Следующий гость — послезавтра";
  const here=teHere();
  return`<div class="hubc"><h4>🍵 Чайная церемония <i>茶道</i></h4><p>${st}.</p><p>Лучшая церемония: ${best?"★".repeat(best)+"☆".repeat(3-best):"ещё не было"} · гостей за чаем: ${nS} из ${tePool().length}. Раз в три дня вечером, после пяти, приходит ёкай; в другие дни можно потренироваться — гостьей будет Муся.</p>
  <div class="row">${here?`<button class="btn primary" data-x="te:open">Заварить чай гостю</button><button class="btn" data-x="te:go">К гостю</button>`:`<button class="btn" data-x="te:open">Потренироваться</button>`}</div></div>`;});
hook("album",el=>{const T=teS(),P=tePool();el.insertAdjacentHTML("beforeend",`<h3 class="bh">Чайная церемония</h3><p class="lead">Гостей за чаем: ${Object.keys(T.served).length} из ${P.length}. Церемоний: ${T.n||0}.</p><div class="coll">${P.map(g=>{const on=!!T.served[g.id];
  return`<div class="ci${on?" on":""}"${on?"":' style="opacity:.45"'}>${on?`<img src="assets/mon/${g.mon}.webp" alt="" style="height:44px;margin:4px 0">`:'<span style="font-size:22px;line-height:52px">？</span>'}<span style="font-size:11px">${on?g.n:"???"}</span></div>`;}).join("")}</div>`);});
hook("boot",()=>{teS();atlasImg("te",im=>TE.im=im);ldImg("assets/bg/te_mat.webp",im=>{TE.mat=im;TE.back=null;});});
X.tea={open:teOpen,st:teS,guest:teGuest,here:teHere,room:teRoom,G:TE_GAME,P:TE_P,
  // tests: stage point → screen point; skip the current step with a quality; drive gestures in stage coords
  scr(u,v){const L=G.st.L;return[L.ox+u*L.k,L.oy+v*L.k];},
  skip(qv=1){const st=G.st.st;if(!st)return;st.qual=qv;const B=G.st.B,k=st.k;if(k==="wb"){B.lv=.45;B.kind="hot";}if(k==="em"){B.lv=0;B.kind="";}if(k==="mt")B.powder=2;if(k==="wt"){B.lv=.66;B.kind="tea";st.lv=.66;}if(k==="wh")B.foam=1;if(k==="tn")B.rot+=Math.PI;
    if(k==="sv"){B.x=TE_P.gbowl[0];B.y=TE_P.gbowl[1];}st.done=true;st.doneT=now()-1;},
  drag(pts){const s=p=>X.tea.scr(p[0],p[1]);G.held=true;G.def.down(G,...s(pts[0]),now());
    for(let i=1;i<pts.length;i++){const a=pts[i-1],b=pts[i],n=Math.max(1,Math.ceil(teD(...a,...b)/20));for(let j=1;j<=n;j++)G.def.move(G,...s([mix(a[0],b[0],j/n),mix(a[1],b[1],j/n)]),true);}},
  lift(){G.held=false;G.def.up(G);},
  tap(u,v){X.tea.drag([[u,v]]);X.tea.lift();}};
}
