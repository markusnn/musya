{
// ───────────────────────── «Теневой театр» (kage-e 影絵) ─────────────────────────
// A full-screen hidden game: a paper shōji screen lit from behind by a flickering candle. The player takes black cut-paper
// figures on rods from the box below, drags them behind the paper (they bob and tilt like puppets), turns, flips and moves
// them nearer the candle (the shadow grows and softens) or back to the paper (sharp). Musya sits in front, follows the
// shadows with her eyes, flinches at scary ones (🙀), laughs at funny ones (😹), paws at fast shadows; tap her and she
// pounces at the screen. Four short plays with a narrator («Дальше»), Musya applauds at the end; free play.
// Entry: bedroom tray in the evening/night (19:00–5:00) + the 家 card (any time).
// S.ext.shadow = {plays:{playId:dayKey first performed}, n:performances finished}
const KG=S.ext.shadow||(S.ext.shadow={plays:{},n:0});KG.plays=KG.plays||{};KG.n=KG.n||0;
// assets/items/atlas_kg.webp (art/shadow_art.py): 240-px cells of figures; KGB = tight box of each figure inside its cell (0..1)
const KGR={"cat":[0,0],"fox":[242,0],"tanuki":[484,0],"crane":[726,0],"rabbit":[968,0],"oni":[1210,0],"yurei":[0,242],"kappa":[242,242],"pine":[484,242],"house":[726,242],"bridge":[968,242],"moon":[1210,242],"boat":[0,484],"samurai":[242,484],"princess":[484,484],"dragon":[726,484],"butterfly":[968,484],"lantern":[1210,484],"karakasa":[0,726],"musya":[242,726],"peach":[484,726],"oldman":[726,726],"kg_screen":[968,726,220,240],"kg_box":[1210,726,236,170]};
const KGB={"cat":[0.025,0.15,0.925,0.975],"fox":[0.029,0.1,0.879,0.971],"tanuki":[0.121,0.087,0.829,0.971],"crane":[0.1,0.058,0.879,0.963],"rabbit":[0.183,0.121,0.904,0.967],"oni":[0.179,0.008,0.892,0.971],"yurei":[0.258,0.058,0.925,0.963],"kappa":[0.217,0.129,0.879,0.963],"pine":[0.0,0.042,1.0,1.0],"house":[0.042,0.029,0.958,0.963],"bridge":[0.0,0.267,1.0,1.0],"moon":[0.004,0.029,1.0,0.933],"boat":[0.0,0.329,1.0,1.0],"samurai":[0.267,0.071,0.779,0.975],"princess":[0.237,0.033,0.979,0.992],"dragon":[0.033,0.062,1.0,0.817],"butterfly":[0.058,0.121,0.942,0.933],"lantern":[0.037,0.096,0.733,0.863],"karakasa":[0.154,0.0,0.846,0.954],"musya":[0.113,0.15,0.863,0.971],"peach":[0.0,0.083,1.0,1.0],"oldman":[0.217,0.146,0.8,0.979]};
// id → [name, mood (s scary, f funny, c cute), size × base, home (g on the ground, s in the sky, m middle)]
const KGF={cat:["кошка","c",.95,"g"],fox:["лиса","",1,"g"],tanuki:["тануки","f",.95,"g"],crane:["журавль","",1.05,"g"],rabbit:["заяц","c",.95,"g"],
  oni:["óни","s",1.15,"g"],yurei:["юрэй","s",1.1,"m"],kappa:["каппа","f",.95,"g"],pine:["сосна","",1.45,"g"],house:["домик","",1.3,"g"],
  bridge:["мост","",1.35,"g"],moon:["луна","",1.2,"s"],boat:["лодка","",1.2,"g"],samurai:["самурай","",1.1,"g"],princess:["принцесса","",1.1,"g"],
  dragon:["дракон","s",1.35,"s"],butterfly:["бабочка","c",.55,"s"],lantern:["фонарь","",.75,"s"],karakasa:["каракаса","f",.95,"g"],
  musya:["Муся","c",.8,"g"],peach:["персик","",.75,"g"],oldman:["старик","",1.05,"g"]};
const KG_ORD=Object.keys(KGF);
const KG_PLAYS=[
 {id:"momotaro",n:"Момотаро",s:"Момотаро",jp:"桃太郎",lead:"Мальчик из персика и остров óни",steps:[
  ["Давным-давно у горной реки жили старик со старухой. Их домик стоял под старой сосной.",["house","pine"]],
  ["Однажды старуха стирала бельё, и по реке приплыл огромный персик. Покачивается на волнах — плюх, плюх!",["peach"]],
  ["Персик раскрылся, а в нём — мальчик! Старики назвали его Момотаро, «персиковый мальчик».",["samurai","oldman"]],
  ["Момотаро вырос и отправился на остров óни. По пути к нему пристали пёс, обезьяна и фазан — у нас их сыграют кошка, тануки и журавль.",["cat","tanuki","crane"]],
  ["На острове жили óни: грабили деревни и прятали награбленное. Самый страшный вышел навстречу с железной палицей!",["oni","samurai"]],
  ["Друзья бились храбро, и óни сдались. Момотаро вернулся домой с сокровищами, и все зажили долго и счастливо.",["house","samurai","oldman"]]]},
 {id:"tsuru",n:"Журавлиная благодарность",s:"Журавль",jp:"鶴の恩返し",lead:"Цуру-но онгаэси",steps:[
  ["Зимой бедный старик шёл из леса с вязанкой хвороста и увидел журавля, попавшего в силок.",["oldman","pine","crane"]],
  ["Старик пожалел птицу и освободил её. Журавль сделал круг над его головой и улетел.",["crane"]],
  ["Той же ночью в дверь постучала девушка: «Я заблудилась в метель. Пустите переночевать».",["house","princess","lantern"]],
  ["Девушка осталась и стала ткать дивную ткань. Только попросила: «Никогда не смотри, как я работаю».",["princess","lantern"]],
  ["Старик не утерпел и заглянул за ширму. А там у станка — журавль: выдёргивает свои перья и вплетает их в ткань.",["crane","lantern"]],
  ["«Ты узнал мою тайну — мне пора». Журавль поклонился, поднялся в небо и улетел к луне.",["crane","moon"]]]},
 {id:"usagi",n:"Лунный заяц",s:"Лунный заяц",jp:"月の兎",lead:"Почему на луне виден заяц",steps:[
  ["В горном лесу дружили обезьяна, лиса и заяц. Обезьяну у нас сыграет тануки.",["pine","fox","rabbit"]],
  ["Однажды к ним вышел измождённый старик: «Я так голоден… Не найдётся ли у вас еды?»",["oldman","tanuki","fox"]],
  ["Обезьяна набрала плодов, лиса принесла рыбы. А заяц ничего не нашёл и сидел, опустив уши.",["rabbit","tanuki","fox"]],
  ["Тогда заяц попросил развести костёр: «У меня ничего нет — возьми меня самого». И прыгнул в огонь.",["rabbit","lantern"]],
  ["Но огонь его не обжёг: старик оказался богом. «Твою доброту будут помнить всегда», — сказал он и поднял зайца на луну.",["oldman","moon"]],
  ["С тех пор в полнолуние на луне виден заяц: он толчёт в ступке рисовые лепёшки моти.",["moon","rabbit"]]]},
 {id:"kitsune",n:"Кицунэ и луна",s:"Кицунэ",jp:"葛の葉",lead:"Белая лиса из леса Синода",steps:[
  ["В лесу Синода жила белая лиса. Однажды за ней погнались охотники, и юноша Ясуна спас её.",["fox","samurai","pine"]],
  ["В полнолуние лиса положила на голову листок, поклонилась луне — и обернулась красавицей.",["fox","moon"]],
  ["Красавицу звали Кудзуноха. Она пришла к Ясуне, они поженились, и у них родился сын.",["princess","samurai","house"]],
  ["Но однажды лунной ночью на сёдзи упала тень — не женская, а лисья…",["house","fox","moon"]],
  ["Кудзуноха оставила на сёдзи прощальные стихи: «Если любишь — приходи ко мне в лес Синода».",["princess","lantern"]],
  ["И белая лиса убежала в лес, к луне. А её сын вырос и стал великим мудрецом Абэ-но Сэймэем.",["fox","moon","pine"]]]}];
const KGC="Теневой театр",kgIt=(id,n,a,hint)=>({id,n,c:KGC,w:KGR[id][2],h:KGR[id][3],a,p:0,at:["kg",KGR[id][0],KGR[id][1]],src:"🕯 теневой театр",hint});
addItems([kgIt("kg_box","Коробка бумажных фигурок","b","Сыграй первый спектакль в теневом театре"),kgIt("kg_screen","Ширма для кагэ-э","b","Сыграй все четыре спектакля теневого театра")],{kg:[1450,966]});
STAMPS.push(["kg_first","影","Первый спектакль","Сыграй сказку в теневом театре"],["kg_all","幕","Все четыре сказки","Сыграй все спектакли теневого театра"]);
const kgN=()=>KG_PLAYS.filter(p=>KG.plays[p.id]).length,kgEve=()=>{const h=hourNow();return h>=19||h<5;};
const KG_INK="rgb(28,13,6)",KG_BL=[0,3,7,12,18],KG_CS=200,KG_PAD=26;
let kgFF="sans-serif";const kgC={},kgTmp=document.createElement("canvas");kgTmp.width=kgTmp.height=KG_CS+KG_PAD*2;
const kgAt=()=>IATL_IM.kg;
// a figure's shadow at blur level lv (cached; shadowBlur works everywhere, ctx.filter does not)
function kgBlur(id,lv){const key=id+lv;if(kgC[key])return kgC[key];const im=kgAt();if(!im)return null;const c=document.createElement("canvas");c.width=c.height=KG_CS+KG_PAD*2;
  const g=c.getContext("2d"),r=KGR[id],b=KG_BL[lv];
  if(!b){g.drawImage(im,r[0],r[1],240,240,KG_PAD,KG_PAD,KG_CS,KG_CS);g.globalCompositeOperation="source-in";g.fillStyle=KG_INK;g.fillRect(0,0,c.width,c.height);}
  else{g.shadowColor=KG_INK;g.shadowBlur=b;g.shadowOffsetX=4000;g.drawImage(im,r[0],r[1],240,240,KG_PAD-4000,KG_PAD,KG_CS,KG_CS);}
  return kgC[key]=c;}
const kgFl=t=>.86+.07*Math.sin(t*7.1)+.05*Math.sin(t*12.7+1.3)+.03*Math.sin(t*23.3+.4);
function kgClack(){tone(1600,.05,"square",.03);setTimeout(()=>tone(1760,.05,"square",.03),110);}
function kgWrap(g,txt,w){const key=g.font+w+txt;if(kgWrap[key])return kgWrap[key];const out=[];let ln="";
  for(const wd of txt.split(" ")){const t=ln?ln+" "+wd:wd;if(g.measureText(t).width>w&&ln){out.push(ln);ln=wd;}else ln=t;}if(ln)out.push(ln);return kgWrap[key]=out;}
function kgTxt(g,txt,x,y,size,color,weight=600,align="left"){g.save();g.font=`${weight} ${size}px ${kgFF}`;g.textAlign=align;g.textBaseline="middle";g.fillStyle=color;g.fillText(txt,x,y);g.restore();}

// ── layout (cached per field size) ──
function kgL(G){const W=G.W,H=G.H;if(kgL.c&&kgL.c.W===W&&kgL.c.H===H)return kgL.c;
  const k=Math.min(G.s,1.15),gap=8*k,stripH=84*k,narrH=148*k,toolH=46*k,bot=toolH+narrH+stripH+gap*3+10*k;
  const sh=Math.max(160,Math.min(H-bot-12*k,(W-20)*1.06)),sw=Math.min(W-20,sh*1.8),sx=(W-sw)/2,sy=Math.max(8,(H-bot-sh)*.4),fr=9*k;
  const P={x:sx+fr,y:sy+fr,w:sw-2*fr,h:sh-2*fr},cw=Math.min(W-24,640*k),cx=(W-cw)/2,cs=.5*k,mx=Math.max(sx+44*k,48*k),my=sy+sh+toolH+2*k;
  const ty=sy+sh+gap*.6,tx=Math.max(cx,mx+56*k),T={x:tx,y:ty,w:cx+cw-tx,h:toolH},N={x:cx,y:ty+toolH+gap,w:cw,h:narrH},R={x:cx,y:N.y+narrH+gap,w:cw,h:stripH};
  return kgL.c={W,H,k,sx,sy,sw,sh,fr,P,D0:P.h*.34,cs,mx,my,T,N,R};}

// ── cached pictures: the room, the paper, the frame with its lattice ──
function kgCv(w,h){const d=Math.min(2,devicePixelRatio||1),c=document.createElement("canvas");c.width=Math.max(1,w*d);c.height=Math.max(1,h*d);const g=c.getContext("2d");g.scale(d,d);return[c,g];}
function kgBg(L){if(kgBg.L===L)return kgBg.c;const {W,H,k}=L,[c,g]=kgCv(W,H),fy=L.sy+L.sh;
  g.fillStyle=vGrad(g,0,fy,[[0,"#140e0a"],[1,"#0d0a08"]]);g.fillRect(0,0,W,fy);
  g.fillStyle=vGrad(g,fy,H,[[0,"#262115"],[1,"#100e09"]]);g.fillRect(0,fy,W,H-fy);g.strokeStyle="rgba(0,0,0,.18)";g.lineWidth=1;
  for(let y=fy+3;y<H;y+=3.2*k){g.beginPath();g.moveTo(0,y);g.lineTo(W,y);g.stroke();}
  g.fillStyle="#0b0806";g.fillRect(0,fy-2*k,W,5*k);g.fillStyle="rgba(0,0,0,.35)";for(let x=-W;x<W*2;x+=W*.42)g.fillRect(x+L.sx*.3,fy,3*k,H);
  kgBg.L=L;return kgBg.c=c;}
function kgPaper(L){if(kgPaper.L===L)return kgPaper.c;const P=L.P,[c,g]=kgCv(P.w,P.h),r=rng(7);
  g.fillStyle=vGrad(g,0,P.h,[[0,"#ead2a0"],[1,"#f4ddab"]]);g.fillRect(0,0,P.w,P.h);
  for(let i=0;i<60;i++){const x=r()*P.w,y=r()*P.h,R=10+r()*40,rg=g.createRadialGradient(x,y,0,x,y,R);rg.addColorStop(0,`rgba(160,110,60,${.03+r()*.05})`);rg.addColorStop(1,"rgba(160,110,60,0)");g.fillStyle=rg;g.fillRect(x-R,y-R,R*2,R*2);}
  for(let i=0;i<Math.min(1600,P.w*P.h/120);i++){const x=r()*P.w,y=r()*P.h,l=4+r()*22,a=r()*Math.PI;g.strokeStyle=r()<.55?`rgba(255,250,235,${.06+r()*.14})`:`rgba(140,95,50,${.04+r()*.07})`;
    g.lineWidth=.4+r()*.8;g.beginPath();g.moveTo(x,y);g.quadraticCurveTo(x+Math.cos(a)*l*.5+r()*4,y+Math.sin(a)*l*.5+r()*4,x+Math.cos(a)*l,y+Math.sin(a)*l);g.stroke();}
  for(let j=1;j<4;j++){g.fillStyle="rgba(140,95,50,.07)";g.fillRect(0,P.h*j/4-1,P.w,2.2);}
  kgPaper.L=L;return kgPaper.c=c;}
function kgFrame(L){if(kgFrame.L===L)return kgFrame.c;const {sw,sh,fr,k}=L,[c,g]=kgCv(sw,sh),pw=sw-2*fr,ph=sh-2*fr;
  g.fillStyle=vGrad(g,0,sh,[[0,"#3e2717"],[1,"#22150c"]]);g.fillRect(0,0,sw,sh);g.strokeStyle="rgba(0,0,0,.25)";g.lineWidth=1;
  for(let y=2;y<sh;y+=5){g.beginPath();g.moveTo(0,y);g.lineTo(sw,y+Math.sin(y)*1.5);g.stroke();}
  g.fillStyle="rgba(255,200,140,.14)";g.fillRect(0,0,sw,1.5*k);g.clearRect(fr,fr,pw,ph);
  const bw=3*k,bar=(x,y,w,h)=>{g.fillStyle="rgba(255,190,110,.16)";g.fillRect(x-1.2*k,y-1.2*k,w+2.4*k,h+2.4*k);g.fillStyle="#2a1a10";g.fillRect(x,y,w,h);g.fillStyle="rgba(255,210,150,.12)";g.fillRect(x,y,w*.35,h);};
  for(const u of [1/3,2/3])bar(fr+pw*u-bw/2,fr,bw,ph);for(const v of [1/3,2/3])bar(fr,fr+ph*v-bw/2,pw,bw);
  g.strokeStyle="rgba(0,0,0,.6)";g.lineWidth=2*k;g.strokeRect(fr-k,fr-k,pw+2*k,ph+2*k);
  kgFrame.L=L;return kgFrame.c=c;}

// ── figures ──
function kgD(L,f){return L.D0*KGF[f.id][2]*(1+.85*f.z);}
function kgPos(L,f){return[L.P.x+f.u*L.P.w,L.P.y+f.v*L.P.h];}
function kgAdd(q,L,id,u,v,t,quiet){const live=q.figs.filter(f=>!f.gone);if(live.length>=10)live[0].gone=t;
  const F=KGF[id],B=KGB[id],D=L.D0*F[2]*1.13;
  if(u==null){const used=live.map(f=>f.u);u=[.5,.27,.73,.38,.62,.16,.84].map(c=>[c,Math.min(1,...used.map(w=>Math.abs(w-c)))]).sort((a,b)=>b[1]-a[1])[0][0];}
  if(v==null)v=F[3]==="s"?.27:F[3]==="m"?.45:1-.015-(B[3]-.5)*D/L.P.h;
  const f={id,u,v,z:.15,rot:0,flip:false,ft:-9,tilt:0,tv:0,bob:0,ph:0,vx:0,born:t,gone:0,seed:Math.random()*9,mv:t};q.figs.push(f);
  if(!quiet){q.sel=f;kgReact(q,id,t);tone(440,.07,"triangle",.03);tone(220,.05,"sawtooth",.01);}return f;}
function kgReact(q,id,t,force){const m=KGF[id][1];if(!m||petAway())return;const c=q.cat;if(!force&&t-c.et<1.4)return;c.emo=m==="s"?"🙀":m==="f"?"😹":"😻";c.et=t;if(m==="s")c.fl=t;}
function kgHit(q,L,x,y){for(let i=q.figs.length-1;i>=0;i--){const f=q.figs[i];if(f.gone)continue;const D=kgD(L,f),B=KGB[f.id],py=(B[3]-.5)*D,[fx,fy]=kgPos(L,f);
    const a=-(f.rot+f.tilt),dx=x-fx,dy=y-(fy+py);let lx=dx*Math.cos(a)-dy*Math.sin(a);const ly=dx*Math.sin(a)+dy*Math.cos(a);if(f.flip)lx=-lx;
    const ux=lx/D+.5,uy=(ly+py)/D+.5,m=Math.max(.03,14/D);if(ux>B[0]-m&&ux<B[2]+m&&uy>B[1]-m&&uy<B[3]+m)return f;}return null;}
function kgFig(g,L,f,t,q){const D=kgD(L,f),B=KGB[f.id],py=(B[3]-.5)*D,k=L.k;let [x,y]=kgPos(L,f);
  x+=Math.sin(t*5.3+f.seed)*1.4*k*f.z;y-=f.bob;const eb=clamp((t-f.born)/.3,0,1);y+=(1-eb)*30*k;if(f.gone)y+=(t-f.gone)*L.P.h*.7;
  let sx=f.flip?-1:1;if(t-f.ft<.3){const e=(t-f.ft)/.3;sx=e<.5?-sx*(1-2*e):sx*(2*e-1);}   // turning the paper over
  if(f.auto)sx*=.4+.6*Math.abs(Math.cos(t*8+f.seed));                                         // the butterfly flaps
  const lf=f.z*(KG_BL.length-1),l0=Math.floor(lf),l1=Math.min(KG_BL.length-1,l0+1),a=lf-l0,c0=kgBlur(f.id,l0);if(!c0)return;let c=c0;
  if(a>.02&&l1!==l0){const c1=kgBlur(f.id,l1),tg=kgTmp.getContext("2d");tg.globalCompositeOperation="copy";tg.globalAlpha=1-a;tg.drawImage(c0,0,0);tg.globalCompositeOperation="lighter";tg.globalAlpha=a;tg.drawImage(c1,0,0);tg.globalAlpha=1;tg.globalCompositeOperation="source-over";c=kgTmp;}
  const al=(.95-.42*f.z)*eb*(f.gone?clamp(1-(t-f.gone)/.45,0,1):1),full=D*(KG_CS+2*KG_PAD)/KG_CS;
  g.save();g.translate(x,y+py);g.rotate(f.rot+f.tilt);
  if(q.sel===f||q.drag&&q.drag.f===f){g.strokeStyle=`rgba(28,13,6,${al*.5})`;g.lineWidth=(2.2+3*f.z)*k;g.beginPath();g.moveTo(0,0);g.lineTo(0,L.P.h*1.3);g.stroke();}   // the rod
  g.scale(sx,1);g.globalAlpha=al;g.drawImage(c,-full/2,-py-full/2,full,full);g.restore();}
function kgSelMark(g,L,f,t){const D=kgD(L,f),B=KGB[f.id],py=(B[3]-.5)*D,[x,y]=kgPos(L,f),k=L.k;g.save();g.translate(x,y-f.bob+py);g.rotate(f.rot+f.tilt);if(f.flip)g.scale(-1,1);
  const x0=(B[0]-.5)*D-5*k,x1=(B[2]-.5)*D+5*k,y0=(B[1]-.5)*D-py-5*k,y1=(B[3]-.5)*D-py+5*k,c=9*k;g.strokeStyle=`rgba(255,236,200,${.45+.2*Math.sin(t*4)})`;g.lineWidth=1.6*k;g.beginPath();
  for(const [px,py_,dx,dy] of [[x0,y0,1,1],[x1,y0,-1,1],[x0,y1,1,-1],[x1,y1,-1,-1]]){g.moveTo(px+dx*c,py_);g.lineTo(px,py_);g.lineTo(px,py_+dy*c);}g.stroke();g.restore();}

// ── Musya ──
function kgLook(q,L,t){let best=null;for(const f of q.figs)if(!f.gone&&(!best||f.mv>best.mv))best=f;if(!best)return null;if(t-best.mv>4&&q.sel)best=q.sel;return kgPos(L,best);}
function kgPounce(q,L,t){if(petAway()||q.cat.a!=="sit")return;const live=q.figs.filter(f=>!f.gone),f=q.sel&&!q.sel.gone?q.sel:live.sort((a,b)=>b.mv-a.mv)[0];
  const P=L.P,fx=f?kgPos(L,f)[0]:P.x+P.w*rand(.3,.7);Object.assign(q.cat,{a:"leap",t0:t,hit:0,f,tx:clamp(fx,P.x+46*L.k,P.x+P.w-46*L.k),ty:P.y+P.h-6*L.k});tone(300,.08,"triangle",.03);}
function kgCat(g,L,q,t){if(petAway())return;const c=q.cat,cs=L.cs,k=L.k;let x=L.mx,y=L.my,st="rest",fr=[0,0,0,6,0,0,7,0][Math.floor(t*.7)%8],flip=false,sc=cs;
  if(q.fin&&t-q.fin<3.4){st="highfive";fr=[1,2,3,2][Math.floor(t*7)%4];}
  else if(c.a==="leap"){const e=t-c.t0;
    if(e<.5){const u=e/.5;x=mix(L.mx,c.tx,u);y=mix(L.my,c.ty,u)-Math.sin(Math.PI*u)*60*k;st="play";fr=4;sc=mix(cs,cs*.9,u);}
    else if(e<1.3){x=c.tx;y=c.ty;st="highfive";fr=Math.floor(e*8)%2?3:2;sc=cs*.9;}
    else{const u=clamp((e-1.3)/.5,0,1);x=mix(c.tx,L.mx,u);y=mix(c.ty,L.my,u)-Math.sin(Math.PI*u)*40*k;st="play";fr=4;flip=c.tx>L.mx;sc=mix(cs*.9,cs,u);}}
  else if(t-c.paw<.9){st="highfive";fr=Math.floor((t-c.paw)*5)%2?3:2;}
  else{const p=kgLook(q,L,t);if(p){const gi=gazeIndex(p[0]-x,(y-150*cs)-p[1]);st=gi<8?"gaze9":"gaze10";fr=gi%8;}}
  if(t-c.fl<.45)y-=Math.sin((t-c.fl)/.45*Math.PI)*12*k;
  const gl=g.createRadialGradient(x,y-60*sc,0,x,y-60*sc,120*sc);gl.addColorStop(0,"rgba(255,180,100,.13)");gl.addColorStop(1,"rgba(255,180,100,0)");g.fillStyle=gl;g.fillRect(x-120*sc,y-180*sc,240*sc,240*sc);
  if(flip){g.save();g.translate(x,0);g.scale(-1,1);drawCatG(g,st,fr,0,y,sc);g.restore();}else drawCatG(g,st,fr,x,y,sc);
  if(c.emo&&t-c.et<1.8)drawEmoji(g,c.emo,x+46*sc,y-200*sc,24*k,clamp(1.8-(t-c.et),0,1));
  c.box=[x-50*k,y-104*k,x+50*k,y+4*k];}

// ── plays ──
function kgGo(q,mode,t,i){for(const f of q.figs)if(!f.gone&&(mode==="play"||f.auto))f.gone=t;q.sel=null;q.mode=mode;q.fin=0;q.rew=null;q.so=0;
  if(mode==="play"){q.play=i;q.i=0;kgClack();}}
function kgNext(q,t){const p=KG_PLAYS[q.play];if(q.i>=p.steps.length-1){kgFinale(q,t);return;}const prev=p.steps[q.i][1];q.i++;const cur=p.steps[q.i][1];
  for(const f of q.figs)if(!f.gone&&prev.includes(f.id)&&!cur.includes(f.id))f.gone=t;q.sel=null;q.so=0;kgClack();}
function kgDone(p){const out=[];if(!KG.plays[p.id])KG.plays[p.id]=dayKey();KG.n++;disc("shadow",p.id);award("kg_first");
  if(!S.owned.has("kg_box")){S.owned.add("kg_box");loadItem("kg_box");out.push("kg_box");}
  if(kgN()>=KG_PLAYS.length){award("kg_all");if(!S.owned.has("kg_screen")){S.owned.add("kg_screen");loadItem("kg_screen");out.push("kg_screen");}}
  S.needs.joy=clamp(S.needs.joy+10,0,100);save();return out;}
function kgFinale(q,t){q.fin=t;q.sel=null;q.rew=kgDone(KG_PLAYS[q.play]);for(const f of q.figs)if(!f.gone)f.tv+=4;kgClack();setTimeout(()=>chime([523,659,784,1047]),300);}

// ── UI pieces drawn on the canvas ──
function kgBtn(g,q,x,y,w,h,label,key,hot){btnRect(g,x,y,w,h,label,hot);q.btns.push([x,y,w,h,key]);}
function kgThumb(g,id,x,y,s){const im=kgAt(),r=KGR[id];if(im)g.drawImage(im,r[0],r[1],240,240,x,y,s,s);}
function kgTools(g,L,q,t){const T=L.T,k=L.k,f=q.sel&&!q.sel.gone?q.sel:null,by=T.y+(T.h-34*k)/2,bh=34*k;
  if(q.mode==="menu"){kgTxt(g,"Выбери сказку",T.x+4*k,T.y+T.h*.38,17*k,"#f3e6cc",800);kgTxt(g,"или играй свободно",T.x+4*k,T.y+T.h*.38+19*k,12*k,"rgba(216,210,195,.7)",500);return;}
  if(q.fin){kgTxt(g,"Браво! Спектакль окончен",T.x+4*k,T.y+T.h/2,14*k,"#f3e6cc",700);return;}
  if(!f){kgTxt(g,"Нажми на тень — выберешь её",T.x+4*k,T.y+T.h/2,12.5*k,"rgba(216,210,195,.72)",500);
    const w=104*k;kgBtn(g,q,T.x+T.w-w,by,w,bh,q.mode==="free"?"📜 Сказки":"📜 Меню","menu");return;}
  let x=T.x;for(const [l,key] of [["↺","rl"],["↻","rr"],["⇄","fl"]]){kgBtn(g,q,x,by,bh,bh,l,key);x+=bh+5*k;}
  const dw=bh,sx0=x+8*k,sx1=T.x+T.w-dw-14*k,sy=T.y+T.h*.62;kgBtn(g,q,T.x+T.w-dw,by,dw,bh,"✕","del");
  kgTxt(g,"у бумаги",sx0,T.y+T.h*.2,10.5*k,"rgba(216,210,195,.7)",500);kgTxt(g,"у свечи 🕯",sx1,T.y+T.h*.2,10.5*k,"rgba(216,210,195,.7)",500,"right");
  g.save();g.lineCap="round";g.strokeStyle="rgba(216,210,195,.25)";g.lineWidth=5*k;g.beginPath();g.moveTo(sx0,sy);g.lineTo(sx1,sy);g.stroke();
  g.strokeStyle="rgba(240,190,120,.8)";g.beginPath();g.moveTo(sx0,sy);g.lineTo(mix(sx0,sx1,f.z),sy);g.stroke();
  g.fillStyle="#f3e6cc";g.shadowColor="rgba(255,190,110,.6)";g.shadowBlur=8*k;g.beginPath();g.arc(mix(sx0,sx1,f.z),sy,9*k,0,Math.PI*2);g.fill();g.restore();
  q.slider=[sx0,sx1,sy];}
function kgPanel(g,x,y,w,h,k){g.save();g.fillStyle="rgba(16,12,10,.86)";g.strokeStyle="rgba(240,190,120,.22)";g.lineWidth=1;g.beginPath();g.roundRect(x,y,w,h,12*k);g.fill();g.stroke();g.restore();}
function kgNarr(g,L,q,t){const N=L.N,k=L.k;
  if(q.mode==="menu"){const R=L.R,y0=N.y,h=(R.y+R.h-y0-30*k)/5;
    KG_PLAYS.forEach((p,i)=>{const y=y0+i*(h+6*k),done=!!KG.plays[p.id];kgPanel(g,N.x,y,N.w,h,k);q.btns.push([N.x,y,N.w,h,"p"+i]);
      jpText(g,p.jp,N.x+34*k,y+h/2,(p.jp.length>3?11:14)*k,"rgba(238,163,187,.9)");kgTxt(g,p.n,N.x+70*k,y+h*.36,15*k,"#f3e6cc",700);kgTxt(g,p.lead,N.x+70*k,y+h*.7,11.5*k,"rgba(216,210,195,.66)",500);
      kgTxt(g,done?"✓ сыграна":"▸",N.x+N.w-12*k,y+h/2,12.5*k,done?"rgba(160,210,150,.9)":"rgba(240,190,120,.9)",700,"right");});
    const y=y0+4*(h+6*k)+6*k;kgBtn(g,q,N.x,y,N.w,h,"🎭 Свободная игра","free");return;}
  kgPanel(g,N.x,N.y,N.w,N.h,k);const pad=14*k;g.save();g.font=`600 ${14.5*k}px ${kgFF}`;
  let text,btns=[];
  if(q.mode==="free"){text="Свободная игра. Бери фигурки из коробки внизу: нажми или потяни вверх. Двигай тени, крути их и переворачивай, а ползунок отодвигает фигурку к свече — тень растёт и мягчеет.";
    btns=[["🧹 Убрать всё","clear"],["📜 Сказки","menu"]];}
  else if(q.fin){const p=KG_PLAYS[q.play];text=`Конец сказки «${p.n}»! Муся хлопает лапками.`+(q.rew&&q.rew.length?" "+q.rew.map(id=>`🎁 ${IT[id].n} — в «🧺 Вещах».`).join(" "):kgN()<4?` Сыграно сказок: ${kgN()} из 4.`:" Все четыре сказки сыграны!");
    btns=[["🎭 Свободно","freego"],["📜 Ещё сказку","menu"]];}
  else{const p=KG_PLAYS[q.play];text=p.steps[q.i][0];}
  const lines=kgWrap(g,text,N.w-pad*2);g.restore();
  lines.slice(0,5).forEach((ln,i)=>kgTxt(g,ln,N.x+pad,N.y+pad+8*k+i*19*k,14.5*k,"#f0e4cc",600));
  const by=N.y+N.h-pad-32*k,bh=32*k;
  if(btns.length){let x=N.x+N.w-pad;for(const [l,key] of btns.slice().reverse()){const w=Math.max(96*k,l.length*8.4*k);x-=w;kgBtn(g,q,x,by,w,bh,l,key,key==="freego"||key==="menu"&&q.fin);x-=8*k;}return;}
  const p=KG_PLAYS[q.play],last=q.i===p.steps.length-1,nw=104*k;kgBtn(g,q,N.x+N.w-pad-nw,by,nw,bh,last?"Поклон 👏":"Дальше ▸","next",true);
  kgTxt(g,"Покажи:",N.x+pad,by+bh/2,12*k,"rgba(216,210,195,.66)",500);let x=N.x+pad+60*k;
  g.save();g.font=`700 ${12*k}px ${kgFF}`;
  for(const id of p.steps[q.i][1]){const on=q.figs.some(f=>!f.gone&&f.id===id),w=34*k+g.measureText(KGF[id][0]).width+8*k;if(x+w>N.x+N.w-pad-nw-6*k)break;
    g.fillStyle=on?"rgba(240,190,120,.85)":`rgba(240,190,120,${.16+.1*Math.sin(t*4)})`;g.beginPath();g.roundRect(x,by,w,bh,bh/2);g.fill();
    g.fillStyle="rgba(244,222,180,.95)";g.beginPath();g.arc(x+bh/2,by+bh/2,bh/2-3*k,0,Math.PI*2);g.fill();kgThumb(g,id,x+5*k,by+5*k,bh-10*k);
    kgTxt(g,KGF[id][0],x+32*k,by+bh/2,12*k,on?"#1a1008":"#f3e6cc",700);q.btns.push([x,by,w,bh,"chip:"+id]);x+=w+6*k;}g.restore();}
function kgStripOrd(q){if(q.mode!=="play"||q.fin)return KG_ORD;const s=KG_PLAYS[q.play].steps[q.i][1];return[...s,...KG_ORD.filter(id=>!s.includes(id))];}
function kgStrip(g,L,q,t){const R=L.R,k=L.k,cw=58*k,gp=6*k,pad=8*k,ord=kgStripOrd(q),sug=q.mode==="play"&&!q.fin?KG_PLAYS[q.play].steps[q.i][1]:[];
  q.soMax=Math.max(0,ord.length*(cw+gp)-gp+pad*2-R.w);q.so=clamp(q.so||0,0,q.soMax);
  g.save();g.fillStyle=vGrad(g,R.y,R.y+R.h,[[0,"#3a2616"],[1,"#24170e"]]);g.beginPath();g.roundRect(R.x,R.y,R.w,R.h,12*k);g.fill();g.strokeStyle="rgba(240,190,120,.25)";g.stroke();g.clip();
  ord.forEach((id,i)=>{const x=R.x+pad+i*(cw+gp)-q.so;if(x>R.x+R.w||x+cw<R.x)return;const s=cw-8*k,ty=R.y+7*k,on=q.figs.some(f=>!f.gone&&f.id===id);
    if(sug.includes(id)){g.fillStyle=`rgba(255,200,120,${.35+.25*Math.sin(t*4+i)})`;g.beginPath();g.roundRect(x-2*k,ty-2*k,cw+4*k,s+4*k,9*k);g.fill();}
    g.fillStyle="#ead3a2";g.beginPath();g.roundRect(x,ty,cw,s,8*k);g.fill();kgThumb(g,id,x+(cw-s)/2+2*k,ty+2*k,s-4*k);
    if(on){g.fillStyle="#c8322c";g.beginPath();g.arc(x+cw-6*k,ty+6*k,3.5*k,0,Math.PI*2);g.fill();}
    kgTxt(g,KGF[id][0],x+cw/2,ty+s+11*k,10.5*k,"rgba(243,230,204,.85)",600,"center");});
  for(const [x0,dir] of [[R.x,1],[R.x+R.w,-1]]){if(dir>0?q.so<2:q.so>q.soMax-2)continue;const gr=g.createLinearGradient(x0,0,x0+dir*28*k,0);gr.addColorStop(0,"rgba(20,12,8,.9)");gr.addColorStop(1,"rgba(20,12,8,0)");g.fillStyle=gr;g.fillRect(dir>0?x0:x0-28*k,R.y,28*k,R.h);}
  g.restore();q.ord=ord;q.cellW=cw+gp;q.pad=pad;}

// ── the game ──
const KG_GAME={id:"kg_theatre",hidden:true,scary:true,   /* scary: only hides the core sakura petals over the paper */n:"Теневой театр",tag:"影絵 · Кагэ-э",icon:"🕯",bg:"room",lives:null,time:null,lore:"",how:"",
 init(G,t){kgFF=getComputedStyle(document.body).fontFamily||kgFF;atlasImg("kg",()=>{});
   Object.assign(G.st,{mode:"menu",figs:[],sel:null,drag:null,so:0,play:0,i:0,fin:0,rew:null,btns:[],fx:[],shake:-9,cat:{a:"sit",t0:0,emo:null,et:-9,fl:-9,paw:-9,box:null}});
   const q=G.st,L=kgL(G);kgAdd(q,L,"moon",.72,.28,t,1).z=.25;kgAdd(q,L,"pine",.2,null,t,1);const b=kgAdd(q,L,"butterfly",.5,.4,t,1);b.auto=1;q.sel=null;tone(220,.4,"sine",.03);},
 step(G,t,dt){const q=G.st,L=kgL(G);
   for(const f of q.figs){const held=q.drag&&q.drag.f===f;
     if(f.auto&&!held){f.u=.5+.26*Math.sin(t*.45+f.seed);f.v=.38+.1*Math.sin(t*1.07+f.seed);f.tilt=.18*Math.sin(t*1.3);f.mv=t;continue;}
     if(!held)f.vx*=Math.exp(-dt*7);const sp=Math.abs(f.vx),tg=held?clamp(-f.vx/1500,-.32,.32):0;
     f.tv+=(-(f.tilt-tg)*70-f.tv*6.5)*dt;f.tilt+=f.tv*dt;
     if(held&&sp>40){f.ph+=dt*clamp(sp/45,4,16);f.bob=Math.abs(Math.sin(f.ph))*7*L.k*clamp(sp/300,.3,1);}else f.bob*=Math.exp(-dt*10);}
   q.figs=q.figs.filter(f=>!f.gone||t-f.gone<.5);if(q.sel&&q.sel.gone)q.sel=null;
   const c=q.cat;if(c.a==="leap"){const e=t-c.t0;if(!c.hit&&e>.5){c.hit=1;q.shake=t;sfx("pop");if(c.f&&!c.f.gone){c.f.tv+=(Math.random()<.5?-6:6);c.f.mv=t;}}if(e>1.8)c.a="sit";}
   if(c.a==="sit"&&q.drag&&q.drag.f&&Math.abs(q.drag.f.vx)>650&&t-c.paw>3.5&&Math.random()<dt*2.5)c.paw=t;
   if(q.fin&&t-q.fin<3.2&&!petAway()&&t>(q.clap||0)){q.clap=t+.3;q.fx.push({g:"👏",x:L.mx+rand(-30,40)*L.k,y:L.my-110*L.k,vx:rand(-20,20),vy:-rand(40,70)*L.k,t0:t,life:1.4});}
   for(const p of q.fx){p.x+=p.vx*dt;p.y+=p.vy*dt;}q.fx=q.fx.filter(p=>t-p.t0<p.life);},
 draw(G,g,t){const q=G.st,L=kgL(G),P=L.P,k=L.k,fl=kgFl(t);q.btns=[];q.slider=null;
   g.drawImage(kgBg(L),0,0,L.W,L.H);
   const wl=g.createRadialGradient(L.sx+L.sw/2,L.sy+L.sh*.75,0,L.sx+L.sw/2,L.sy+L.sh*.75,L.sw*.95);wl.addColorStop(0,`rgba(255,170,90,${.16*fl})`);wl.addColorStop(1,"rgba(255,170,90,0)");g.fillStyle=wl;g.fillRect(0,0,L.W,L.H);
   if(!kgAt()){textC(g,"…",L.W/2,L.H/2,20*k);return;}
   const e=t-q.shake,ox=e<.7?Math.sin(e*45)*3*k*Math.exp(-e*7):0;
   g.save();g.translate(ox,0);g.beginPath();g.rect(P.x,P.y,P.w,P.h);g.clip();g.drawImage(kgPaper(L),P.x,P.y,P.w,P.h);
   const lx=P.x+P.w*(.5+.015*Math.sin(t*1.3)),ly=P.y+P.h*.9,hs=g.createRadialGradient(lx,ly,0,lx,ly,P.h*.5);hs.addColorStop(0,`rgba(255,214,140,${.55*fl})`);hs.addColorStop(1,"rgba(255,214,140,0)");
   g.globalCompositeOperation="lighter";g.fillStyle=hs;g.fillRect(P.x,P.y,P.w,P.h);g.globalCompositeOperation="source-over";
   for(const f of q.figs)kgFig(g,L,f,t,q);
   if(q.fin&&q.mode==="play"){const a=clamp((t-q.fin)/.6,0,1);jpText(g,"終",P.x+P.w/2,P.y+P.h*.2,64*k,`rgba(28,13,6,${.85*a})`);}
   const R=Math.max(P.w,P.h)*1.05,vg=g.createRadialGradient(lx,ly-P.h*.25,R*.08,lx,ly-P.h*.25,R);vg.addColorStop(0,"rgba(60,30,10,0)");vg.addColorStop(.5,`rgba(50,24,8,${.16+.2*(1-fl)})`);vg.addColorStop(1,`rgba(18,8,3,${.7+.25*(1-fl)})`);g.fillStyle=vg;g.fillRect(P.x,P.y,P.w,P.h);
   if(q.sel&&!q.sel.gone)kgSelMark(g,L,q.sel,t);g.restore();
   g.drawImage(kgFrame(L),L.sx+ox,L.sy,L.sw,L.sh);
   kgCat(g,L,q,t);kgTools(g,L,q,t);kgNarr(g,L,q,t);if(q.mode!=="menu")kgStrip(g,L,q,t);
   for(const p of q.fx)drawEmoji(g,p.g,p.x,p.y,20*k,clamp(1-(t-p.t0)/p.life,0,1));},
 down(G,x,y,t){const q=G.st,L=kgL(G),k=L.k;q.drag=null;
   for(let i=q.btns.length-1;i>=0;i--){const [bx,by,bw,bh,key]=q.btns[i];if(x>=bx&&x<=bx+bw&&y>=by&&y<=by+bh){kgKey(q,L,key,t);return;}}
   if(q.slider&&q.sel&&Math.abs(y-q.slider[2])<18*k&&x>q.slider[0]-14*k&&x<q.slider[1]+14*k){q.drag={k:"z",f:q.sel};this.move(G,x,y,true);return;}
   const R=L.R;if(q.mode!=="menu"&&x>R.x&&x<R.x+R.w&&y>R.y&&y<R.y+R.h){const i=Math.floor((x-R.x-q.pad+q.so)/q.cellW);q.drag={k:"strip",x0:x,y0:y,so0:q.so,id:q.ord&&q.ord[i]};return;}
   const b=q.cat.box;if(b&&x>b[0]&&x<b[2]&&y>b[1]&&y<b[3]){kgPounce(q,L,t);return;}
   const f=kgHit(q,L,x,y);if(f){q.figs.splice(q.figs.indexOf(f),1);q.figs.push(f);q.sel=f;f.auto=0;const [fx,fy]=kgPos(L,f);q.drag={k:"fig",f,ox:fx-x,oy:fy-y,lx:x,lt:t};f.mv=t;tone(500,.04,"triangle",.02);return;}
   q.sel=null;},
 move(G,x,y,held){const q=G.st,d=q.drag;if(!d||!held)return;const L=kgL(G),P=L.P,t=now(),k=L.k;
   if(d.k==="z"){const s=q.slider;if(!s)return;const z=clamp((x-s[0])/(s[1]-s[0]),0,1);d.f.z=z;d.f.mv=t;if(z>.75&&!d.f.big){d.f.big=1;kgReact(q,d.f.id,t,true);}if(z<.5)d.f.big=0;return;}
   if(d.k==="strip"){const dx=x-d.x0,dy=y-d.y0;
     if(!d.m&&d.id&&dy<-14*k&&Math.abs(dy)>Math.abs(dx)){const f=kgAdd(q,L,d.id,clamp((x-P.x)/P.w,0,1),clamp((y-P.y)/P.h,0,1.05),t);q.drag={k:"fig",f,ox:0,oy:0,lx:x,lt:t};return;}
     if(!d.m&&Math.abs(dx)>8*k)d.m=1;if(d.m)q.so=clamp(d.so0-dx,0,q.soMax||0);return;}
   if(d.k==="fig"){const f=d.f,dt=Math.max(.008,t-d.lt);f.vx=mix(f.vx,(x-d.lx)/dt,.35);d.lx=x;d.lt=t;f.mv=t;
     f.u=clamp((x+d.ox-P.x)/P.w,-.05,1.05);f.v=clamp((y+d.oy-P.y)/P.h,0,1.15);}},
 up(G){const q=G.st,d=q.drag;q.drag=null;if(!d)return;const L=kgL(G),t=now();
   if(d.k==="strip"&&!d.m&&d.id)kgAdd(q,L,d.id,null,null,t);
   if(d.k==="fig"){const R=L.R,[fx,fy]=kgPos(L,d.f);if(q.mode!=="menu"&&fy>R.y&&fx>R.x&&fx<R.x+R.w){d.f.gone=t;q.sel=null;tone(260,.06,"triangle",.02);}}},
 stat:G=>{const q=G.st;if(q.mode==="play"){const p=KG_PLAYS[q.play];return`${p.s} · ${Math.min(q.i+1,p.steps.length)}/${p.steps.length}`;}return`Сыграно ${kgN()} из 4`;}};
function kgKey(q,L,key,t){const f=q.sel&&!q.sel.gone?q.sel:null;q.btns=[];
  if(key==="rl"||key==="rr"){if(f){f.rot+=key==="rl"?-.26:.26;f.mv=t;tone(600,.03,"triangle",.02);}return;}
  if(key==="fl"){if(f){f.flip=!f.flip;f.ft=t;f.mv=t;tone(700,.05,"triangle",.02);}return;}
  if(key==="del"){if(f){f.gone=t;q.sel=null;}return;}
  if(key==="menu"){kgGo(q,"menu",t);return;}
  if(key==="free"||key==="freego"){kgGo(q,"free",t);return;}
  if(key==="clear"){for(const g of q.figs)g.gone=t;q.sel=null;return;}
  if(key==="next"){kgNext(q,t);return;}
  if(key[0]==="p"&&key.length===2){kgGo(q,"play",t,+key[1]);return;}
  if(key.startsWith("chip:")){const id=key.slice(5),g=q.figs.find(f=>!f.gone&&f.id===id);if(g){q.sel=g;g.tv+=4;g.mv=t;kgReact(q,id,t);}else kgAdd(q,L,id,null,null,t);}}
GAMES.push(KG_GAME);
function kgOpen(){if(G.id)return;closePanel();openPlace("kg_theatre");}

// ── entry points ──
hook("tray",(tray,room)=>{if(room!=="bedroom"||(S.trayMode[room]||"play")!=="play"||!kgEve())return;const row=tray.querySelector(".items");if(!row||row.querySelector('[data-x="kg:open"]'))return;
  const b=`<button class="item wide" data-x="kg:open"><span class="ico">🕯</span><span class="nm">Теневой театр</span></button>`,kd=row.querySelector("[data-kaidan]");if(kd)kd.insertAdjacentHTML("afterend",b);else row.insertAdjacentHTML("beforeend",b);});
hook("click",k=>{if(k==="kg:open"){kgOpen();return true;}return false;});
hook("hub",()=>{const n=kgN();
  return`<div class="hubc"><h4>🕯 Теневой театр <i>影絵</i></h4><p>Сыграно спектаклей: ${n} из 4</p>
   <p>За бумажной ширмой горит свеча. Води чёрными фигурками на палочках — тени оживают, а Муся смотрит спектакль и ловит их лапой. Четыре японские сказки с рассказчиком и свободная игра. Вечером и ночью театр открыт и в спальне.</p>
   <div class="row"><button class="btn primary" data-x="kg:open">🕯 Открыть театр</button></div></div>`;});
hook("album",el=>{if(!KG.n)return;const its=["kg_box","kg_screen"];
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Теневой театр</h3><p class="lead">Сыграно сказок: ${kgN()} из 4 · спектаклей всего: ${KG.n}. ${KG_PLAYS.map(p=>`${KG.plays[p.id]?"✓":"·"} ${p.n}`).join(", ")}.</p>
   <div class="coll">${its.map(id=>`<div class="ci ${S.owned.has(id)?"on":""}">${itemThumb(IT[id],70,52)}<small>${S.owned.has(id)?IT[id].n:"???"}</small></div>`).join("")}</div>`);});
hook("boot",()=>{for(const id of ["kg_box","kg_screen"])if(S.owned.has(id))loadItem(id);});

// test handles
X.kg={K:KG,open:kgOpen,q:()=>G.st,L:()=>kgL(G),key:k=>kgKey(G.st,kgL(G),k,now()),pounce:()=>kgPounce(G.st,kgL(G),now()),
  add(id,u,v,z){const f=kgAdd(G.st,kgL(G),id,u,v,now());if(z!=null)f.z=z;return f.id;},
  drag(id,du,dv){const q=G.st,L=kgL(G),f=q.figs.find(f=>!f.gone&&f.id===id);if(!f)return false;const [x,y]=kgPos(L,f);G.held=true;KG_GAME.down(G,x,y,now());
    let i=0;const iv=setInterval(()=>{i++;KG_GAME.move(G,x+du*L.P.w*i/12,y+dv*L.P.h*i/12,true);if(i>=12)clearInterval(iv);},40);return true;},
  release(){G.held=false;KG_GAME.up(G);}};
}
