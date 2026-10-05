// ───────────────────────── Сумо с каппой (sm): a weekly basho Fri–Sun on the night dohyō ─────────────────────────
// Kappa love sumo and challenge passers-by; bow to one and he bows back, spilling the water of his head plate — and his strength.
// Basho = Friday, Saturday, Sunday: one official bout a day against the next opponent of the ladder; other days only training.
{
const SM_R={"sm_dohyo":[0,0,230,130],"sm_kesho":[232,0,150,210],"sm_gunbai":[384,0,110,215],"sm_cup":[496,0,180,240],"sm_doll":[678,0,120,170],"ds_sm_chanko":[800,0,176,132],"sm_fan":[978,0,92,192]};
const SM_IT=[["sm_doll","Кукла-рикиси","Победи Каппу на басё","b"],["sm_kesho","Кэсё-маваси","Победи Тануки на басё","t"],["sm_gunbai","Веер гёдзи гумбай","Победи Нэкомату на басё","b"],
 ["sm_dohyo","Маленький дохё","Победи Тэнгу на басё","b"],["sm_cup","Кубок императора","Победи старого каппу-ёкодзуну","b"]];
addItems(SM_IT.map(([id,n,hint,a])=>{const r=SM_R[id];return{id,n,c:"Сумо",w:r[2],h:r[3],a,p:120,at:["sm",r[0],r[1]],src:"🥋 басё",hint:"🥋 "+hint};}),{sm:[1072,240]});
FATL.sm={w:1072,h:240,r:{ds_sm_chanko:SM_R.ds_sm_chanko}};
FOOD.ds_sm_chanko={n:"Тянко-набэ",k:"dish",food:36,joy:16};
STAMPS.push(["sm_win","勝","Первая победа","Выиграй бой на басё"],["sm_rei","礼","Вежливый поклон","Поклонись каппе так низко, чтобы он пролил почти всю воду"],["sm_yoko","綱","Ёкодзуна","Победи старого каппу-ёкодзуну"]);
BESTIARY.push(["sm_oldkappa","m_kappa","Старый каппа-ёкодзуна","Самый сильный борец реки: сорок лет никто не выталкивал его из круга. На поясе — белый канат ёкодзуны. Вежлив, как все каппы."]);
// opponents: belt = [top,bottom,left,right] as parts of the sprite; F = steady push (ring per s), surge = [period s, extra]
const SM_OPP=[
 {id:"kappa",mon:"m_kappa",n:"Каппа",sn:"Каппа",ins:"Каппой",acc:"Каппу",dat:"Каппе",h:300,belt:[.7,.8,.08,.92],col:"#24443e",F:.15,surge:[3.2,.3],ch:0,water:1,gift:["v_kyuri",3],item:"sm_doll",
  hi:"Эй, малышка! Поборемся? Каппы любят сумо больше огурцов.",bowG:"Ой… поклон за поклон. Вода… льётся…",bowM:"Кивнула? Тогда и я кивну.",lose:"Уф! Держи огурцы — честно заработала.",win:"Ха! Вода при мне — и сила при мне. Приходи ещё."},
 {id:"tanuki",mon:"m_tanuki",n:"Тануки",sn:"Тануки",ins:"Тануки",acc:"Тануки",dat:"Тануки",h:300,belt:[.8,.885,.24,.84],col:"#5e3418",F:.16,surge:[2.6,.28],ch:1,gift:["v_imo",2],item:"sm_kesho",
  hi:"Пон-пон! Мой живот — лучший барабан и лучший щит.",bowG:"Тануки кланяется и хихикает в рукав.",bowM:"Тануки кланяется и хихикает в рукав.",lose:"Перехитрила старого тануки! Держи батат.",win:"Пон! Живот не подвёл."},
 {id:"nekomata",mon:"m_nekomata",n:"Нэкомата",sn:"Нэкомата",ins:"Нэкоматой",acc:"Нэкомату",dat:"Нэкомате",h:300,belt:[.78,.86,.16,.66],col:"#46285a",F:.17,surge:[2.2,.28],feint:1,ch:1,gift:["u_ayu",1],item:"sm_gunbai",
  hi:"Кошка против кошки? Два хвоста против одного, мур-р.",bowG:"Нэкомата щурится: поклон принят.",bowM:"Нэкомата щурится: поклон принят.",lose:"Ловкая… Ладно, вот тебе рыбка. Не жалко. Почти.",win:"Мр-р. Хвосты решают."},
 {id:"tengu",mon:"m_rm_tengu",n:"Тэнгу",sn:"Тэнгу",ins:"Тэнгу",acc:"Тэнгу",dat:"Тэнгу",h:345,belt:[.655,.725,.25,.78],col:"#17171b",F:.19,surge:[3,.38],ch:2,gift:["v_kabocha",1],item:"sm_dohyo",
  hi:"С горы Курама я видел многих борцов. Покажи, что умеешь.",bowG:"Тэнгу чуть кивает длинным носом.",bowM:"Тэнгу чуть кивает длинным носом.",lose:"Хо! Мал котёнок, да дух велик. Признаю.",win:"Крылья ветра не подводят."},
 {id:"yokozuna",mon:"m_kappa",n:"Старый каппа-ёкодзуна",sn:"Ёкодзуна",ins:"старым каппой-ёкодзуной",acc:"старого каппу-ёкодзуну",dat:"старому каппе-ёкодзуне",h:390,belt:[.7,.8,.06,.94],col:"#3a2252",tsuna:1,old:1,F:.24,surge:[2.4,.45],ch:2,water:1,gift:["v_kyuri",5],item:"sm_cup",
  hi:"Сорок лет никто не выталкивал меня из круга. Ну-ну.",bowG:"Вежливость — моя слабость… ох, вода…",bowM:"Старика не проведёшь — кланяйся ниже.",lose:"Вот и выросла новая ёкодзуна. Канат теперь твой.",win:"Рано тебе, рано. Но глаза у тебя хорошие."}];
const SM_RANK=["Дзёнокути","Дзёнидан","Сандамэ","Макусита","Дзюрё","Макуути","Ёкодзуна"],SM_TH=[0,1,2,4,6,8];
const SM={bg:null,at:null,oc:{},mode:null,bgc:null,bgKey:""};
function smS(){const T=S.ext.sumo||(S.ext.sumo={w:0,l:0,lad:0,beat:{},days:{},wk:"",bw:0,bl:0,tr:0});return T;}
function smDow(){return today().getDay();}
function smBasho(){const d=smDow();return d===5||d===6||d===0;}
function smWk(){const d=smDow(),back=d===5?0:d===6?1:d===0?2:-1;return back<0?"":dayKey(new Date(today().getTime()-back*864e5));}
function smDone(){return smS().days[dayKey()]||"";}
function smOpp(){const T=smS();if(!T.beat.yokozuna)return SM_OPP[Math.min(4,T.lad)];const d=today();return SM_OPP[Math.floor(d.getTime()/864e5)%5];}
function smRank(){const T=smS();let r=0;SM_TH.forEach((v,i)=>{if(T.w>=v)r=i;});return T.beat.yokozuna?6:r;}
function smPl(n,a,b,c){const m=n%10,h=n%100;return m===1&&h!==11?a:m>=2&&m<=4&&(h<12||h>14)?b:c;}
function smNext(){const n=(5-smDow()+7)%7;return n===1?"Следующее басё — в пятницу, уже завтра":`Следующее басё — в пятницу, через ${n} ${smPl(n,"день","дня","дней")}`;}
function smC(o){return(o.id==="yokozuna"?"со ":"с ")+o.ins;}
function smSync(){const T=smS(),wk=smWk();if(wk&&T.wk!==wk){T.wk=wk;T.bw=0;T.bl=0;}}

// ── the bout ──
const smE=u=>u<0?0:u>1?1:u*u*(3-2*u);
function smSay(q,txt,dur=2.6){q.say={txt,t0:q.clk,dur};}
function smMsg(q,txt,dur=1.2,sz=1){q.msg={txt,t0:q.clk,dur,sz};}
function smPhase(q,ph){q.ph=ph;q.pt=q.clk;
  if(ph==="bow"){q.bowRes=null;q.bowT=0;smMsg(q,"Поклон",1.2);}
  if(ph==="tachi"){q.sig=q.clk+1.6+Math.random()*1.6;q.sigOn=0;q.fs=0;smSay(q,"Хаккэёй…",9);q.who="g";}}
function smSalt(q,who){const x=who?q.ox-30:q.mx+20,y=who?968-q.o.h*.7:880;for(let i=0;i<34;i++)q.fx.push({k:"s",x,y,vx:(who?-1:1)*(60+Math.random()*260),vy:-260-Math.random()*240,t0:q.clk,life:1.4+Math.random()*.5,r:2+Math.random()*3.5});
  tone(who?1700:2100,.25,"triangle",.012);}
function smSpill(q){const amt=q.bowRes==="perfect"?.75:.4;q.water=Math.max(0,q.water-amt);const x=q.ox,y=968-q.o.h*.85;
  for(let i=0;i<26;i++)q.fx.push({k:"w",x:x+(Math.random()-.5)*40,y,vx:-40-Math.random()*150,vy:-60-Math.random()*120,t0:q.clk+Math.random()*.3,life:1.3,r:2.5+Math.random()*3});
  sfx("splash");}
function smClash(q,r,auto){const o=q.o,c=q.clk;q.started=1;q.ph="push";q.t0=c;q.clashT=c;q.say=null;
  if(auto){q.p=-.18;smMsg(q,"Соперник успел первым!",1.2);}
  else if(r<.4){q.p=.12;q.stun=c+.6;smMsg(q,"Отличный старт!",1.2);}
  else if(r<.9){q.p=.03;smMsg(q,"Старт!",1);}
  else{q.p=-.1;smMsg(q,"Поздновато…",1.1);}
  q.p+=q.spirit||0;q.vp=0;q.nextS=c+o.surge[0];q.nextC=c+5+Math.random()*2;q.chN=0;tone(90,.25,"sine",.12);tone(140,.12,"square",.03);}
function smEnd(q,res,byTime){if(q.ph==="end")return;q.ph="end";q.res=res;q.endT=q.clk;q.say=null;G.score=res==="w"?5:1;
  if(res==="w"){q.kim=byTime?"Решение судей":q.kimT&&q.clk-q.kimT<2.5?"Уватэнагэ":"Ёрикири";chime([523,659,784,1047]);smMsg(q,q.kim+"!",2.4,1.3);}
  else{q.kim=byTime?"Решение судей":"Оситаси";sfx("bad");smMsg(q,byTime?"Судьи решили: не в этот раз":"Муся за кругом…",2.4,1.1);}
  smResult(q);}
function smResult(q){const T=smS(),o=q.o,res=q.res;q.got=[];
  if(!q.off){T.tr=(T.tr||0)+1;save();return;}
  smSync();T.days[dayKey()]=res;T.last={id:o.id,res};const ks=Object.keys(T.days).sort();while(ks.length>14)delete T.days[ks.shift()];
  if(res==="w"){T.w++;T.bw++;const first=!T.beat[o.id];T.beat[o.id]=(T.beat[o.id]||0)+1;
    if(!T.beat.yokozuna&&SM_OPP[T.lad]===o)T.lad=Math.min(4,T.lad+1);
    give(o.gift[0],o.gift[1]);give("ds_sm_chanko",1);q.got.push(o.gift,["ds_sm_chanko",1]);
    if(first){S.owned.add(o.item);q.item=o.item;disc("sumo",o.id);}
    award("sm_win");if(o.id==="yokozuna")award("sm_yoko");}
  else{T.l++;T.bl++;}
  save();}
function smInit(G,t){const q=G.st,M=SM.mode||{off:false,o:smOpp()},o=M.o;
  Object.assign(q,{o,off:M.off,clk:0,ph:"salt",pt:0,p:0,vp:0,pp:0,fx:[],water:o.water?1:null,last:-1,step:0,saltT:0,oSalt:0,bowT:0,oBow:0,taps:[0,0],spirit:0,
   mx:330,ox:690,sg:null,ch:null,chN:0,stun:0,hitT:-9,msg:null,say:null,kim:"",res:"",down:null});
  smSay(q,o.hi,3.4);if(o.old&&!ST.seen.includes("sm_oldkappa"))ST.seen.push("sm_oldkappa");}
function smStep(G,t,dt){const q=G.st;dt=Math.min(dt,.05);q.clk+=dt;const c=q.clk,o=q.o;
  for(const f of q.fx)if(c>=f.t0){f.vy+=700*dt;f.x+=f.vx*dt;f.y+=f.vy*dt;if(f.y>975&&f.k!=="d"){f.vy*=-.15;f.vx*=.4;f.y=975;}}
  q.fx=q.fx.filter(f=>c-f.t0<f.life);
  if(q.ph==="salt"){if(q.saltT&&!q.oSalt&&c-q.saltT>.6){q.oSalt=c;smSalt(q,1);}if(q.oSalt&&c-q.oSalt>1.3)smPhase(q,"bow");}
  else if(q.ph==="bow"){const B=q.bowT;if(B&&!q.oBow&&c-B>.4){q.oBow=c;if(q.water!=null&&q.bowRes!=="miss")smSpill(q);smSay(q,q.bowRes==="miss"?o.bowM:o.bowG,2.2);}
    if(B&&c-B>2.9)smPhase(q,"tachi");}
  else if(q.ph==="tachi"){if(!q.sigOn&&c>=q.sig){q.sigOn=c;q.say=null;smMsg(q,"Нокотта!",1,1.3);tone(988,.1,"square",.03);tone(1320,.14,"triangle",.03);}
    if(q.sigOn&&!q.started&&c-q.sigOn>1.15)smClash(q,9,true);}
  else if(q.ph==="push"){const wf=q.water!=null?.5+.5*q.water:1;let f=o.F*wf;
    if(!q.sg&&!q.ch&&c>=q.nextS)q.sg={t0:c,fe:o.feint&&Math.random()<.4};
    if(q.sg){const u=c-q.sg.t0;if(u>.55&&u<1.15&&!q.sg.fe)f+=o.surge[1]/.6*wf;if(u>=1.15){q.sg=null;q.nextS=c+o.surge[0]*(.8+Math.random()*.4);}}
    if(q.stun>c)f=0;
    if(!q.ch&&q.chN<o.ch&&c>=q.nextC&&!q.sg){q.ch={t0:c,dodge:0,done:0};q.pp=0;smMsg(q,"Смахни — увернись!",1.25,1.1);tone(220,.3,"sawtooth",.03);}
    if(q.ch){const ch=q.ch,u=c-ch.t0;f=0;
      if(ch.dodge){if(!ch.done&&c-ch.dodge>.45){ch.done=1;q.p+=.45;q.stun=c+1;q.kimT=c;smMsg(q,"Бросок!",1);tone(160,.2,"sine",.1);}
        if(c-ch.dodge>1){q.ch=null;q.chN++;q.nextC=c+6+Math.random()*3;}}
      else if(u>1.3){q.p-=.36;q.hitT=c;q.ch=null;q.chN++;q.nextC=c+6+Math.random()*3;smMsg(q,"Таран!",.9);tone(70,.3,"sine",.14);}}
    const take=q.pp*(1-Math.exp(-dt*7));q.pp-=take;if(!q.ch)q.p+=take-f*dt;
    if(q.p>=1)smEnd(q,"w");else if(q.p<=-1)smEnd(q,"l");else if(c-q.t0>34)smEnd(q,q.p>0?"w":"l",1);}
  else if(q.ph==="end"){if(c-q.endT>2.6&&!q.ended){q.ended=1;gEnd();}}
  q.vp+=(q.p-q.vp)*Math.min(1,dt*9);}
function smDown(G,x,y){const q=G.st,c=q.clk;q.down={x,y,sw:0};
  if(q.ph==="salt"){if(!q.saltT){q.saltT=c;smSalt(q,0);}return;}
  if(q.ph==="bow"){if(q.bowT)return;const u=smBowU(q),e=Math.abs(u-.5);q.bowRes=e<.07?"perfect":e<.18?"good":"miss";q.bowT=c;
    if(q.water==null&&q.bowRes!=="miss")q.spirit=q.bowRes==="perfect"?.08:.04;
    if(q.water!=null&&q.bowRes==="perfect")award("sm_rei");
    smMsg(q,q.bowRes==="perfect"?"Идеальный поклон!":q.bowRes==="good"?"Хороший поклон":"Только кивок…",1.4);tone(q.bowRes==="miss"?330:660,.2,"sine",.04);return;}
  if(q.ph==="tachi"){if(q.started)return;if(!q.sigOn){q.fs++;smMsg(q,"Матта! Рано",1.1);tone(200,.15,"square",.03);q.sig=c+1.4+Math.random()*1.4;if(q.fs>=3)smClash(q,9,true);return;}
    smClash(q,c-q.sigOn,false);return;}
  if(q.ph==="push"){if(q.ch)return;const side=x<G.W/2?0:1,good=side!==q.last;q.last=side;q.taps[side]=c;q.pp+=good?.052:.016;if(good)q.step++;tone(good?180+Math.random()*30:120,.06,"sine",.05);}}
function smMove(G,x,y,held){const q=G.st,d=q.down;if(!d||!held||d.sw)return;if(Math.hypot(x-d.x,y-d.y)>36*G.s){d.sw=1;smSwipe(q);}}
function smSwipe(q){const ch=q.ch;if(q.ph!=="push"||!ch||ch.dodge)return;const u=q.clk-ch.t0;if(u<.2)return;ch.dodge=q.clk;tone(520,.12,"triangle",.04);}
function smBowU(q){const u=((q.clk-q.pt)/1.3)%2;return u<1?u:2-u;}

// ── drawing ──
function smOppCv(o){let c=SM.oc[o.id];if(c)return c;const im=MIMG[o.mon];if(!im||!im.width)return null;const [w,h]=MON[o.mon];
  c=document.createElement("canvas");c.width=w;c.height=h;const g=c.getContext("2d");g.drawImage(im,0,0,w,h);g.globalCompositeOperation="source-atop";
  if(o.old){g.fillStyle="rgba(150,160,168,.24)";g.fillRect(0,0,w,h);g.globalCompositeOperation="source-over";smBrows(g,w,h);g.globalCompositeOperation="source-atop";}   // the old master's white brows
  const [y0,y1,x0,x1]=o.belt,sag=h*.025,mid=w*(x0+x1)/2,band=()=>{g.beginPath();g.moveTo(x0*w,y0*h);g.quadraticCurveTo(mid,y0*h+sag*2,x1*w,y0*h);g.lineTo(x1*w,y1*h);g.quadraticCurveTo(mid,y1*h+sag*2,x0*w,y1*h);g.closePath();};
  band();const gr=g.createLinearGradient(0,y0*h,0,y1*h+sag);gr.addColorStop(0,o.col);gr.addColorStop(.45,smTint(o.col,.25));gr.addColorStop(1,smTint(o.col,-.4));g.fillStyle=gr;g.fill();
  const hg=g.createLinearGradient(x0*w,0,x1*w,0);hg.addColorStop(0,"rgba(0,0,0,.5)");hg.addColorStop(.38,"rgba(255,240,220,.08)");hg.addColorStop(1,"rgba(0,0,0,.55)");g.fillStyle=hg;band();g.fill();
  g.strokeStyle="rgba(0,0,0,.28)";g.lineWidth=2;for(let k=1;k<4;k++){const yy=(y0+(y1-y0)*k/4)*h;g.beginPath();g.moveTo(x0*w,yy);g.quadraticCurveTo(mid,yy+sag*2,x1*w,yy);g.stroke();}
  g.fillStyle=smTint(o.col,-.15);g.fillRect(mid-w*.055,y1*h+sag-2,w*.11,h*.07);                     // front panel between the legs
  g.globalCompositeOperation="source-over";g.lineCap="round";
  for(let i=0;i<9;i++){const x=mid-w*.11+i*w*.0275,yy=y1*h+sag*1.5;g.strokeStyle=smTint(o.col,i%2?-.25:.05);g.lineWidth=Math.max(2,w*.012);g.beginPath();g.moveTo(x,yy);g.lineTo(x+(i-4)*.6,yy+h*.075);g.stroke();}   // sagari cords
  if(o.tsuna){const ty=y0*h-h*.01;g.lineWidth=h*.034;g.strokeStyle="#e9e4d6";g.beginPath();g.moveTo(x0*w-4,ty);g.quadraticCurveTo(mid,ty+sag*2.2,x1*w+4,ty);g.stroke();
    g.lineWidth=2;g.strokeStyle="rgba(120,110,95,.6)";for(let x=x0*w;x<x1*w;x+=h*.022){const u=(x-x0*w)/((x1-x0)*w),yy=ty+sag*2.2*4*u*(1-u)*.5*2;g.beginPath();g.moveTo(x,yy-h*.016);g.lineTo(x+h*.014,yy+h*.016);g.stroke();}
    g.fillStyle="#f4f1e8";g.strokeStyle="rgba(90,80,70,.5)";g.lineWidth=1;
    for(const dx of[-.16,0,.16]){const x=mid+dx*w,yy=ty+sag*2*(1-(dx*2)**2)+h*.012;g.beginPath();g.moveTo(x-w*.02,yy);g.lineTo(x+w*.02,yy);g.lineTo(x+w*.03,yy+h*.03);g.lineTo(x,yy+h*.03);g.lineTo(x+w*.012,yy+h*.06);g.lineTo(x-w*.015,yy+h*.06);g.lineTo(x-w*.022,yy+h*.03);g.closePath();g.fill();g.stroke();}}
  SM.oc[o.id]=c;return c;}
// long bushy white brows of the old yokozuna: tufts from above each eye sweeping out and drooping past the cheeks (m_kappa 340×480: eyes at x .40/.60, y .254)
function smBrows(g,w,h){g.save();g.lineCap="round";const u=w/340;
  for(const pass of[0,1])for(const s of[-1,1]){const ex=w*(.5+s*.103),ey=h*.254-u*24;
    for(let i=0;i<9;i++){const f=i/8,x0=ex-s*u*(14-f*6),y0=ey+u*(f*5-2),x1=ex+s*u*(30+f*16),y1=ey+u*(-6+f*12),x2=ex+s*u*(44+f*12),y2=ey+u*(10+f*16);
      g.strokeStyle=pass?`rgba(${246-i*3},${243-i*3},${232-i*4},.97)`:"rgba(16,22,16,.55)";g.lineWidth=u*(pass?3.4-f*.9:6.5);
      g.beginPath();g.moveTo(x0,y0);g.quadraticCurveTo(x1,y1,x2,y2);g.stroke();}}
  g.restore();}
function smTint(hex,k){const n=parseInt(hex.slice(1),16),f=v=>Math.round(k>0?v+(255-v)*k:v*(1+k));return`rgb(${f(n>>16&255)},${f(n>>8&255)},${f(n&255)})`;}
function smLay(G){const W=G.W,H=G.H,k=Math.min(W/740,H/1180);return{k,ox:W/2-500*k,oy:H-1310*k};}
function smBg(G){const W=G.W,H=G.H,c=document.createElement("canvas"),d=Math.min(2,devicePixelRatio||1);c.width=W*d;c.height=H*d;const g=c.getContext("2d");g.setTransform(d,0,0,d,0,0);
  g.fillStyle="#08090c";g.fillRect(0,0,W,H);const im=SM.bg,L=smLay(G);if(!im)return c;
  const k2=Math.max(W/1000,H/1400);g.globalAlpha=.3;g.drawImage(im,W/2-500*k2,H-1400*k2,1000*k2,1400*k2);g.globalAlpha=1;
  g.fillStyle="rgba(6,7,10,.55)";g.fillRect(0,0,W,H);g.drawImage(im,L.ox,L.oy,1000*L.k,1400*L.k);
  if(L.ox>2)for(const s of[0,1]){const x0=s?L.ox+1000*L.k:L.ox,gr=g.createLinearGradient(x0,0,x0+(s?-60:60),0);gr.addColorStop(0,"rgba(8,9,12,.9)");gr.addColorStop(1,"rgba(8,9,12,0)");g.fillStyle=gr;g.fillRect(s?x0-60:x0,0,60,H);}
  return c;}
function smFF(){return SM.ff||(SM.ff=getComputedStyle(document.body).fontFamily);}
function smTxt(g,txt,x,y,size,col="#efe6d2",w=700){g.save();g.font=`${w} ${size}px ${smFF()}`;g.textAlign="center";g.textBaseline="middle";
  g.lineJoin="round";g.lineWidth=Math.max(3,size*.22);g.strokeStyle="rgba(10,8,6,.85)";g.strokeText(txt,x,y);g.fillStyle=col;g.fillText(txt,x,y);g.restore();}
function smBubble(g,txt,x,y,s,dn=1){g.save();const fs=Math.round(13.5*s);g.font=`600 ${fs}px ${smFF()}`;
  const mw=Math.min(230*s,G.W-24),words=txt.split(" "),lines=[];let cur="";for(const w of words){const t=cur?cur+" "+w:w;if(g.measureText(t).width>mw-18*s&&cur){lines.push(cur);cur=w;}else cur=t;}lines.push(cur);
  const bw=Math.max(...lines.map(l=>g.measureText(l).width))+20*s,bh=lines.length*fs*1.3+12*s,bx=clamp(x-bw/2,8,G.W-bw-8),by=y-bh-10*s;
  g.fillStyle="rgba(238,230,212,.95)";g.beginPath();g.roundRect(bx,by,bw,bh,10*s);g.fill();g.beginPath();g.moveTo(clamp(x,bx+12,bx+bw-12)-7*s,by+bh-1);g.lineTo(clamp(x,bx+12,bx+bw-12)+7*s,by+bh-1);g.lineTo(clamp(x,bx+14,bx+bw-14),by+bh+9*s*dn);g.fill();
  g.fillStyle="#2a2018";g.textAlign="center";g.textBaseline="top";lines.forEach((l,i)=>g.fillText(l,bx+bw/2,by+6*s+i*fs*1.3));g.restore();}
function smDraw(G,g,t){const q=G.st,o=q.o,c=q.clk,L=smLay(G),k=L.k,X=ix=>L.ox+ix*k,Y=iy=>L.oy+iy*k,key=G.W+"x"+G.H+(SM.bg?1:0);
  if(SM.bgKey!==key||!SM.bgc){SM.bgc=smBg(G);SM.bgKey=key;}G.bgc=SM.bgc;g.drawImage(SM.bgc,0,0,G.W,G.H);
  // positions in image coords
  const ph=q.ph,cx=500+clamp(q.vp,-1,1)*240,oc=smOppCv(o),[mw,mh]=MON[o.mon];let mx,ox;
  if(ph==="salt"||ph==="bow"){mx=330;ox=690;}else if(ph==="tachi"){mx=392;ox=650;}
  else{const u=smE((c-q.clashT)/.22);mx=392+(cx-58-392)*u;ox=650+(cx+o.h*mw/mh*.3-650)*u;}
  let my=0,orot=0,osx=1,osy=1,odx=0;
  if(q.ch&&ph==="push"){const ch=q.ch,u=c-ch.t0;if(ch.dodge){const v=(c-ch.dodge)/.45;my=-Math.sin(Math.PI*Math.min(1,v))*70;mx-=30*Math.sin(Math.PI*Math.min(1,v));odx=v<1?-60*smE(v):-60+60*smE((v-1)/.6);orot=v<1?-.15*v:-.15+.5*Math.sin(Math.PI*Math.min(1,(v-1)/1.2));}
    else odx=u<.6?45*smE(u/.6):45-105*smE((u-.6)/.7);}
  if(ph==="push"&&!q.ch){const sg=q.sg;orot=-.05-(sg&&!sg.fe&&c-sg.t0>.55?.1:0);if(sg&&c-sg.t0<.55){osx=osy=1+.04*Math.sin(Math.PI*(c-sg.t0)/.55);}}
  if(ph==="bow"&&q.oBow){const v=c-q.oBow,b=Math.sin(Math.PI*Math.min(1,v/1.2));osy=1-.1*b;orot=-.12*b;}
  if(ph==="tachi")osy=.94;
  if(ph==="end"){const v=smE((c-q.endT)/1.2);if(q.res==="w"){odx=30*v;orot=.5*v;}else mx-=50*v;}
  q.mx=mx;q.ox=ox+odx;
  // gyōji fox with the gunbai
  const fox=MIMG.m_kitsune;if(fox&&fox.width){const fh=205*k,fw=fh*400/450;g.drawImage(fox,X(478)-fw/2,Y(905)-fh,fw,fh);}
  if(SM.at){const r=SM_R.sm_fan,fh=168*k,fw=fh*r[2]/r[3],sg=ph==="tachi"&&q.sigOn?smE((c-q.sigOn)/.12):0,py=836-96*sg;let a=-.1+.06*Math.sin(t*1.3);
    if(ph==="tachi")a=q.sigOn?-.08-.22*sg:-.08+.035*Math.sin(t*9);   // trembles before tachi-ai, jerks up on «Нокотта!» (the gyōji's bubble is gone then)
    g.save();g.translate(X(558),Y(py));g.rotate(a);g.drawImage(SM.at,r[0],r[1],r[2],r[3],-fw/2,-fh*150/192,fw,fh);g.restore();
    if(q.sigOn&&c-q.sigOn<.5){const d=fh*94/192,fx=X(558)+Math.sin(a)*d,fy=Y(py)-Math.cos(a)*d;g.save();g.globalAlpha=1-(c-q.sigOn)/.5;g.strokeStyle="#fff2c8";g.lineWidth=4;g.beginPath();g.arc(fx,fy,(20+140*(c-q.sigOn))*k,0,7);g.stroke();g.restore();}}
  // opponent
  if(oc){const sc=o.h/mh*k,w=mw*sc,h=mh*sc,shake=q.hitT>0&&c-q.hitT<.3?(Math.random()-.5)*6:0;
    g.save();g.fillStyle="rgba(0,0,0,.35)";g.beginPath();g.ellipse(X(q.ox),Y(970),w*.42,h*.05,0,0,7);g.fill();
    g.translate(X(q.ox),Y(970));g.rotate(orot);g.scale(osx,osy);g.drawImage(oc,-w/2,-h,w,h);
    if(q.water!=null){g.fillStyle=`rgba(98,112,92,${(1-q.water)*.9})`;g.beginPath();g.ellipse(0,-h*(1-.153),w*.15,h*.022,0,0,7);g.fill();}
    if(ph==="push"&&q.sg&&c-q.sg.t0<.6)smTxt(g,"!",w*.3,-h*1.02,26*G.s,"#ffcf70");
    g.restore();
    if(q.ch&&!q.ch.dodge&&ph==="push")smTxt(g,"‼",X(q.ox),Y(970-o.h)-16,34*G.s,"#ff8a6a");}
  // Musya
  let st="rest",fr=0;if(ph==="salt"&&q.saltT&&c-q.saltT<.7){st="highfive";fr=5;}else if(ph==="bow"&&q.bowT&&c-q.bowT<1.5||ph==="tachi"){st="stretch";fr=2;}
  else if(ph==="push"){if(q.ch&&q.ch.dodge&&c-q.ch.dodge<.6){st="play";fr=2;}else{st="moveRight";fr=q.step%8;}}
  else if(ph==="end"){if(q.res==="w"){st="play";fr=Math.floor(c*3)%2?2:5;}else{st="sulk";fr=2;}}
  const shake=q.hitT>0&&c-q.hitT<.35?(Math.random()-.5)*8:0;
  g.save();g.fillStyle="rgba(0,0,0,.35)";g.beginPath();g.ellipse(X(mx),Y(972),46*k,8*k,0,0,7);g.fill();g.restore();
  drawCatG(g,st,fr,X(mx)+shake,Y(978+my),1.12*k);
  // particles
  g.save();for(const f of q.fx){if(c<f.t0)continue;const a=1-Math.max(0,(c-f.t0)/f.life-.6)/.4;g.globalAlpha=Math.max(0,a);g.fillStyle=f.k==="w"?"#bfe4ec":"#f4f1ea";g.beginPath();g.arc(X(f.x),Y(f.y),f.r*k*1.4,0,7);g.fill();}g.restore();
  // speech, prompts
  const s=G.s;
  if(q.say&&c-q.say.t0<q.say.dur){if(q.who==="g"&&ph==="tachi")smBubble(g,q.say.txt,X(500),Y(690),s);else smBubble(g,q.say.txt,X(Math.min(q.ox,760)),Y(960-o.h)-6,s);}
  const P=(txt,sz=15)=>smTxt(g,txt,G.W/2,Y(1078),sz*s,"#efe6d2",600);
  if(ph==="salt"&&!q.saltT)P("Коснись — Муся бросит соль");
  if(ph==="bow"&&!q.bowT){const bw=Math.min(280*s,G.W-60),bx=G.W/2-bw/2,by=Y(1125),u=smBowU(q);
    g.save();g.fillStyle="rgba(12,10,8,.75)";g.beginPath();g.roundRect(bx-6,by-6,bw+12,30,10);g.fill();g.fillStyle="rgba(120,150,110,.65)";g.fillRect(bx+bw*.32,by,bw*.36,18);g.fillStyle="#d8b048";g.fillRect(bx+bw*.43,by,bw*.14,18);
    g.fillStyle="#fff";g.beginPath();g.moveTo(bx+bw*u,by+20);g.lineTo(bx+bw*u-8,by+32);g.lineTo(bx+bw*u+8,by+32);g.fill();g.fillRect(bx+bw*u-1.5,by-4,3,26);g.restore();
    P(q.water!=null?"Поклонись, когда метка в золоте: каппа прольёт воду":"Поклонись, когда метка в золотой зоне",13.5);}
  if(ph==="tachi"&&!q.sigOn)P("Жди сигнала веера — и сразу касайся!",14);
  if(ph==="push"){const pw=Math.min(300*s,G.W-60),px0=G.W/2-pw/2,py=14;g.save();g.fillStyle="rgba(12,10,8,.7)";g.beginPath();g.roundRect(px0-6,py-5,pw+12,18,8);g.fill();
      const gr=g.createLinearGradient(px0,0,px0+pw,0);gr.addColorStop(0,"#b8322a");gr.addColorStop(.18,"#5a4636");gr.addColorStop(.82,"#5a4636");gr.addColorStop(1,"#3f8a5a");g.fillStyle=gr;g.fillRect(px0,py,pw,8);
      const mxp=px0+pw*(q.vp+1)/2;g.fillStyle="#f4ead2";g.beginPath();g.arc(mxp,py+4,7,0,7);g.fill();g.restore();
      if(c-q.t0<3.2&&!q.ch)P("Касайся по очереди: слева — справа!",14);
      if(q.ch&&!q.ch.dodge){const u=c-q.ch.t0,a=.5+.5*Math.sin(u*18);smTxt(g,"⇠  смахни  ⇢",G.W/2,Y(1078),18*s,`rgba(255,214,150,${a})`);}
      const ex=q.last===0?1:0;for(const sd of[0,1]){const x=sd?G.W*.8:G.W*.2,y=G.H-56*s,hot=c-q.taps[sd]<.12;
        g.save();g.globalAlpha=q.ch?.35:1;g.fillStyle=hot?"rgba(244,234,210,.85)":"rgba(16,13,11,.62)";g.strokeStyle=sd===ex||q.last<0?"rgba(255,214,150,.9)":"rgba(216,210,195,.3)";g.lineWidth=sd===ex?3:1.5;
        g.beginPath();g.arc(x,y,34*s,0,7);g.fill();g.stroke();g.font=`${26*s}px sans-serif`;g.textAlign="center";g.textBaseline="middle";g.fillText("🐾",x,y+1);g.restore();}}
  if(q.msg&&c-q.msg.t0<q.msg.dur){const u=(c-q.msg.t0)/q.msg.dur,a=u<.8?1:(1-u)/.2;g.save();g.globalAlpha=a;smTxt(g,q.msg.txt,G.W/2,Y(1150)-12*smE(u*4),24*s*q.msg.sz,"#ffe2a8",800);g.restore();}
  if(q.water!=null&&ph!=="end"){const x=G.W-14,y=44;g.save();g.fillStyle="rgba(12,10,8,.65)";g.beginPath();g.roundRect(x-74,y-12,72,24,8);g.fill();g.fillStyle="#7fc6d6";g.fillRect(x-48,y-4,44*q.water,8);g.strokeStyle="rgba(216,210,195,.4)";g.strokeRect(x-48,y-4,44,8);
    g.font=`${13}px sans-serif`;g.textAlign="left";g.textBaseline="middle";g.fillText("💧",x-70,y);g.restore();}
}
const SM_GAME={id:"sm_bout",hidden:true,n:"Сумо с каппой",tag:"相撲 · Басё",icon:"🥋",bg:"temple",lives:null,time:null,lore:"",how:"",
 init:smInit,step:smStep,draw:smDraw,down:smDown,move:smMove,up(G){G.st.down=null;},
 stat:G=>{const q=G.st;return`${q.off?"Басё":"Тренировка"}${q.ph==="push"?" · "+Math.max(0,Math.ceil(34-(q.clk-q.t0)))+" с":""}`;},
 card(G){const q=G.st,o=q.o,T=smS(),w=q.res==="w",r=smRank(),it=q.item&&IT[q.item];
  const got=(q.got||[]).map(([id,n])=>`${fThumb(id,44,34)} ${FOOD[id]?FOOD[id].n:id}${n>1?" ×"+n:""}`).join(" · ");
  const nx=!q.off?"Тренировка: ранг не меняется.":smDow()===0?`Басё окончено: ${T.bw} ${smPl(T.bw,"победа","победы","побед")}, ${T.bl} ${smPl(T.bl,"поражение","поражения","поражений")}. Следующее — в пятницу.`:`Завтра на дохё — бой ${smC(smOpp())}.`;
  return`<div class="card"><p class="tag">${q.off?"相撲 · Басё":"稽古 · Тренировка"}</p><h3>${w?"Победа! "+q.kim:"Поражение"}</h3>
   <p class="lore">«${w?o.lose:o.win}» — ${o.n}</p>${got?`<p>В кладовой: ${got}</p>`:""}
   ${it?`<div class="dish">${itemThumb(it,170,120)}</div><p>Новая вещь: <b>${it.n}</b>. Найдёшь в «🧺 Вещи».</p>`:""}
   <p>Ранг Муси: <b>${SM_RANK[r]}</b> · побед на басё: ${T.w}</p><p style="opacity:.75">${nx}</p>
   <div class="row"><button class="btn" id="gHome">Домой</button><button class="btn primary" id="gAgain">Тренировка</button></div></div>`;},
 after(G){$("gAgain").onclick=()=>{SM.mode={off:false,o:smOpp()};beginGame();};ui();}};
GAMES.push(SM_GAME);
function smOpen(off){if(petAway()){toast("🥋 Муся в пути — бой подождёт");return;}const o=smOpp();if(off&&(!smBasho()||smDone()))off=false;
  SM.mode={off,o};SM_GAME.tag=off?"相撲 · Басё":"稽古 · Тренировка";SM_GAME.n=off?`Басё: ${o.sn}`:`Тренировка: ${o.sn}`;
  SM_GAME.lore="Каппы обожают сумо и зовут на бой каждого, кто идёт мимо реки. Но они очень вежливы: поклонишься — каппа поклонится в ответ, вода из блюдца на макушке прольётся, а с ней уйдёт и сила."+(off?"":" Тренировка ранг не меняет.");
  SM_GAME.how="Коснись — брось соль. Поклонись, когда метка в золоте. На «Нокотта!» гёдзи коснись сразу. Потом касайся по очереди слева и справа — Муся толкает. Если соперник разбегается для тарана, смахни в сторону. Вытолкни его за соломенный круг!";
  closePanel();openGame("sm_bout");}

// ── hub, dots, album ──
document.head.insertAdjacentHTML("beforeend","<style>.story-body .hubc p.sm-lad,.hubc p.sm-lad{font-size:12.5px;opacity:.85;line-height:1.6}.sm-lad b{color:#e8c77a;font-weight:600}.sm-lad s{opacity:.5;text-decoration:none}</style>");
let smBooted=false;
hook("boot",()=>{smBooted=true;smS();smSync();ldImg("assets/bg/sm_dohyo.webp",im=>{SM.bg=im;SM.bgc=null;});atlasImg("sm",im=>SM.at=im);});
hook("hubDot",()=>smBooted&&smBasho()&&!smDone()&&!petAway());
hook("hub",()=>{const T=smS();smSync();const o=smOpp(),done=smDone(),d=smDow(),r=smRank();
  let st;if(smBasho()){if(!done)st=`Басё идёт: сегодня бой ${smC(o)}`;else{const lo=SM_OPP.find(x=>x.id===(T.last&&T.last.id))||o;
    st=d===0?`Басё окончено: ${T.bw} ${smPl(T.bw,"победа","победы","побед")} и ${T.bl} ${smPl(T.bl,"поражение","поражения","поражений")}. Следующее — в пятницу`:done==="w"?`Басё идёт: сегодня Муся победила ${lo.acc}! Завтра — бой ${smC(o)}`:`Басё идёт: сегодня Муся уступила ${lo.dat}. Завтра — снова бой ${smC(o)}`;}}
  else st=smNext();
  const lad=SM_OPP.map((x,i)=>T.beat[x.id]?`<b>✓ ${x.n.replace("Старый каппа-ёкодзуна","Ёкодзуна")}</b>`:x===o&&!T.beat.yokozuna?`▶ ${x.n.replace("Старый каппа-ёкодзуна","Ёкодзуна")}`:`<s>${x.n.replace("Старый каппа-ёкодзуна","Ёкодзуна")}</s>`).join(" · ");
  const can=smBasho()&&!done;
  return`<div class="hubc"><h4>🥋 Сумо с каппой <i>相撲</i></h4><p>${st}</p>
   <p>Басё каждую неделю: пятница, суббота и воскресенье — по одному бою в день, соперник за соперником. В остальные дни — тренировка, ранг не меняется.</p>
   <p>Ранг Муси: <b>${SM_RANK[r]}</b> · побед на басё: ${T.w}${T.bw||T.bl?` · ${smBasho()?"это":"прошлое"} басё: ${T.bw}–${T.bl}`:""}</p><p class="sm-lad">${lad}</p>
   <div class="row">${can?`<button class="btn primary" data-x="sm:bout">🥋 На дохё: бой ${smC(o)}</button>`:""}<button class="btn ${can?"":"primary"}" data-x="sm:train">Тренировка</button></div></div>`;});
hook("click",k=>{if(k==="sm:bout"){smOpen(true);return true;}if(k==="sm:train"){smOpen(false);return true;}return false;});
hook("album",el=>{const T=smS();if(!T.w&&!T.l&&!T.tr)return;
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Сумо с каппой</h3><p class="lead">Ранг Муси: ${SM_RANK[smRank()]}. Побед на басё: ${T.w}, поражений: ${T.l}, тренировок: ${T.tr||0}.</p>`);});

// test handles
X.sumo={S:smS,opp:smOpp,open:smOpen,rank:smRank,
  tap(side){if(G.id!=="sm_bout")return;smDown(G,side?G.W*.8:G.W*.2,G.H*.6);G.st.down=null;},
  swipe(){if(G.id==="sm_bout")smSwipe(G.st);},
  bowNow(){if(G.id!=="sm_bout")return;const q=G.st;q.pt=q.clk-.65;X.sumo.tap(0);},sig(){if(G.id==="sm_bout")G.st.sig=G.st.clk+.02;},charge(){if(G.id==="sm_bout")G.st.nextC=G.st.clk;},
  ff(sec,tapHz){if(G.id!=="sm_bout")return;const q=G.st;let n=Math.round(sec*60),j=0;for(let i=0;i<n&&!G.over;i++){if(tapHz&&q.ph==="push"&&i%Math.max(1,Math.round(60/tapHz))===0)X.sumo.tap(j++%2);G.def.step(G,now(),1/60);}},
  st:()=>{const q=G.st;return q&&q.o?{ph:q.ph,p:+q.p.toFixed(2),water:q.water,res:q.res,clk:+q.clk.toFixed(1),ch:!!q.ch,bow:q.bowRes}:null;}};
}
