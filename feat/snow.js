{
// ───────────────────────── «Зимние забавы»: a snowman (yukidaruma — two balls) and a kamakura in the games yard ─────────────────────────
// S.ext.snow = {men:[{r1,r2,e,m,h,a,slot,ml,at}], km:{ml,at}|null, n:{<winter>:snowmen made}, kn:{<winter>:kamakuras}, wk:"<winter of the snow toast>", tot, melted}
// Available while snow lies (X.wx.snowLies(): winter, unless the real city is warm) or a festival with snow fx. Everything melts
// slowly when the real temperature is above +2° or the snow season is over: stages → a puddle with the bucket → gone.
// Art: assets/items/atlas_yk.webp (art/snow_art.py). Games: yk_man (roll two balls, lift, dress), yk_kama (pile, pack, dig, light).
const YK_R={"km":[0,0,480,330],"km_glow":[482,0,480,330],"dome":[964,0,480,330],"mound":[0,332,480,330],"ball":[482,332,208,208],"puddle":[344,664,300,90],"bucket":[1056,332,150,140],"cap":[1208,332,150,128],"scarf":[814,332,240,150],"scarf_i":[152,664,190,96],"lantern":[692,332,120,176],"brazier":[0,664,150,128],"twig":[646,664,200,84],"pine":[848,664,200,84],"coal":[1214,664,40,34],"pebble":[1256,664,40,34],"berry":[1298,664,40,34],"mikan":[1050,664,80,40],"leaf":[1132,664,80,40],"twigm":[1340,664,80,30]};
const YK_C="Зимние забавы",YK_SRC="⛄ зимние забавы";
addItems([
 {id:"yk_bucket",n:"Ведёрко-шляпа",c:YK_C,w:150,h:140,a:"b",p:0,at:["yk",1056,332],src:YK_SRC,hint:"⛄ Слепи первого снеговика, когда ляжет снег"},
 {id:"yk_scarf",n:"Вязаный шарф снеговика",c:YK_C,w:190,h:96,a:"b",p:0,at:["yk",152,664],src:YK_SRC,hint:"⛄ Слепи трёх снеговиков за одну зиму"},
 {id:"yk_lantern",n:"Фонарик из камакуры",c:YK_C,w:120,h:176,a:"b",p:0,at:["yk",692,332],src:YK_SRC,hint:"⛄ Построй камакуру — снежный домик",glow:[60,100]}],{yk:[1456,792]});
STAMPS.push(["yk_first","雪","Первый снеговик","Слепи снеговика-юкидаруму"],["yk_kama","灯","Камакура","Построй снежный домик и зажги в нём свечу"],["yk_three","三","Три снеговика","Слепи трёх снеговиков за одну зиму"]);

// where things stand in the games yard (image coords, floor depth): at the back of the yard, just in front of the torii line
// (lower down the foreground ferns of the near layer would cover them): the kamakura left of Musya, snowmen to the right
const YK_KM={x:560,y:1170,w:640},YK_MEN=[[1240,1174],[1640,1180],[1060,1150]],YK_MH=520;
const YK_EYE={coal:["coal","угольки"],pebble:["pebble","камешки"],berry:["berry","ягоды"]},YK_MOUTH={mikan:["mikan","мандарин"],leaf:["leaf","листик"],twigm:["twigm","веточка"]},
  YK_HEAD={bucket:["bucket","ведёрко"],cap:["cap","шапка"],scarf:["scarf","шарф"]},YK_ARM={twig:["twig","веточки"],pine:["pine","сосна"],none:[null,"без рук"]};
const YK_ROWS=[["e","Глаза",YK_EYE],["m","Рот",YK_MOUTH],["h","Наряд",YK_HEAD],["a","Руки",YK_ARM]];
const ykS=()=>{const s=S.ext.snow||(S.ext.snow={men:[],km:null,n:{},kn:{},wk:"",tot:0,melted:0,mt:Date.now()});if(!s.kn)s.kn={};return s;};
const ykWK=()=>{const T=today();return String(T.getMonth()<6?T.getFullYear()-1:T.getFullYear());};   // a winter = Dec + next Jan–Feb
const ykFest=()=>{const F=festNow();return !!F&&F.fx.includes("snow");};
const ykSnow=()=>!!(X.wx&&X.wx.snowLies&&X.wx.snowLies())||ykFest();
let YK_IM=null;const ykImg=()=>{if(!YK_IM&&!ykImg.q){ykImg.q=1;atlasImg("yk",im=>{YK_IM=im;});}return YK_IM;};
const YK_FF=()=>YK_FF.f||(YK_FF.f=getComputedStyle(document.body).fontFamily);
function ykTxt(g,t,x,y,sz,col="#f3ead8",w=700,al="center"){g.font=`${w} ${sz}px ${YK_FF()}`;g.textAlign=al;g.textBaseline="middle";g.fillStyle=col;g.fillText(t,x,y);}
// a sprite from the atlas, centred at (x,y), size w×h
function ykSp(g,k,x,y,w,h,rot=0,fx=1){const im=ykImg(),r=YK_R[k];if(!im||!r)return;g.save();g.translate(x,y);if(rot)g.rotate(rot);if(fx!==1)g.scale(fx,1);g.drawImage(im,r[0],r[1],r[2],r[3],-w/2,-h/2,w,h);g.restore();}

// ── melting: the real temperature above +2° (faster in rain) or the end of the snow season
function ykRate(){const w=X.wx&&X.wx.real&&X.wx.real();if(w&&w.temp>2)return clamp((w.temp-2)*.025,.03,.25)*(weather.on?1.5:1);return ykSnow()?0:.035;}   // per hour
function ykMelt(force){const s=ykS(),n=Date.now(),h=Math.min(72,(n-(s.mt||n))/3.6e6);if(!force&&h<.008)return;s.mt=n;const r=ykRate();if(!r||h<=0)return;
  for(const m of s.men){const was=m.ml;m.ml+=r*h;if(was<1&&m.ml>=1)s.melted=(s.melted||0)+1;}s.men=s.men.filter(m=>m.ml<1.7);
  if(s.km){s.km.ml+=r*h*.7;if(s.km.ml>=1){s.km=null;ykSitEnd();ykLantern(false);}}ykCache.clear();}
const ykStage=ml=>ml<.25?0:ml<.5?1:ml<.75?2:ml<1?3:4;
// the left stone lantern of the games yard steps aside while the kamakura stands in front of it (it would peek through the dome)
function ykLantern(on){const p=PROPS.find(p=>p.id==="p_gam_toro0");if(p)p.room=on?"-yk":"games";}

// ── a snowman: geometry shared by the game and the room. (x,y) = ground contact, H = height of a fresh one
function ykGeo(m,x,y,H,ml){const c=Math.min(ml,1),R1=H*.29,rr=clamp(m.r2/m.r1,.5,.8),w1=2*R1*(1+.18*c),h1=2*R1*(.94-.5*c*c),by=y-h1/2+R1*.05,top=y-h1+R1*.06,
  R2=R1*rr*(1-.4*c),h2=2*R2*(1-.16*c),hx=x+R1*.28*c,hy=top-R2*(.8-.5*c);return{R1,R2,w1,h1,by,top,h2,hx,hy,tilt:.38*c};}
function ykMan(g,m,x,y,H,ml,noHead){const im=ykImg();if(!im)return;const q=ykGeo(m,x,y,H,ml),{R1,R2}=q,c=Math.min(ml,1);
  if(ml>.3||ml>=1){g.save();g.globalAlpha=clamp((ml-.3)/.5,0,1)*.9;ykSp(g,"puddle",x+R1*.1,y-2,R1*2*(1+.6*c),R1*.5*(1+.4*c));g.restore();}
  if(ml>=1){// gone: the puddle and what the snowman wore
    if(m.a!=="none"){ykSp(g,m.a,x-R1*1.05,y-R1*.12,R1*1.2,R1*.5,.12,-1);ykSp(g,m.a,x+R1*1.1,y-R1*.05,R1*1.2,R1*.5,-.08);}
    ykSp(g,YK_EYE[m.e][0],x-R1*.3,y-R1*.08,R1*.2,R1*.17);ykSp(g,YK_EYE[m.e][0],x-R1*.05,y-R1*.02,R1*.2,R1*.17);ykSp(g,YK_MOUTH[m.m][0],x+R1*.25,y-R1*.12,R1*.4,R1*.18,.3);
    if(m.h==="bucket")ykSp(g,"bucket",x+R1*.55,y-R1*.42,R1*.95,R1*.9,1.75);else if(m.h==="cap")ykSp(g,"cap",x+R1*.5,y-R1*.25,R1*.9,R1*.62,.25);else ykSp(g,"scarf_i",x+R1*.45,y-R1*.18,R1*1.0,R1*.5,.08);
    return;}
  g.fillStyle="rgba(16,22,40,.32)";g.beginPath();g.ellipse(x,y,R1*1.05*(1+.2*c),R1*.17,0,0,Math.PI*2);g.fill();
  // twig / pine arms stuck into the body (behind it); they droop while melting and fall at the end
  if(m.a!=="none")for(const sd of [-1,1]){const L=R1*1.3;g.save();
    if(c>.82){g.translate(x+sd*R1*1.25,y-R1*.06);g.scale(sd,1);g.rotate(.05);}else{g.translate(x+sd*R1*.7*(1+.18*c),q.by-R1*.28*(1-c));g.scale(sd,1);g.rotate(-.22+c*1.2);}
    const r=YK_R[m.a];g.drawImage(im,r[0],r[1],r[2],r[3],-.03*L,-.71*L*r[3]/r[2],L,L*r[3]/r[2]);g.restore();}
  ykSp(g,"ball",x,q.by,q.w1,q.h1,c*.06);
  if(noHead)return q;
  g.save();g.translate(q.hx,q.hy);g.rotate(q.tilt);
  ykSp(g,"ball",0,0,R2*2,q.h2,.4);
  const es=R2*.24,ey=-R2*.1;ykSp(g,YK_EYE[m.e][0],-R2*.34,ey,es,es*.85);ykSp(g,YK_EYE[m.e][0],R2*.34,ey+Math.max(0,c-.6)*R2*.9,es,es*.85);
  if(c<.85){const mw=R2*.62;ykSp(g,YK_MOUTH[m.m][0],0,R2*.36,mw,m.m==="twigm"?mw*.37:mw*.5,c*.3);}
  if(m.h==="bucket"&&c<.9){const r=YK_R.bucket,w=R2*1.32,hh=w*110/150;g.save();g.translate(R2*.08,-R2*.62-hh*.32+c*R2*.3);g.rotate(-.2-c*.5);g.scale(1,-1);g.drawImage(im,r[0],r[1]+30,150,110,-w/2,-hh/2,w,hh);g.restore();}
  if(m.h==="cap"&&c<.9){const w=R2*1.5;ykSp(g,"cap",R2*.04,-R2*.62+c*R2*.25,w,w*128/150,-.12-c*.4);}
  g.restore();
  if(m.h==="scarf"){const w=R2*2.3;ykSp(g,"scarf",q.hx+w*.06,q.top+w*.12+c*R2*.2,w,w*150/240,q.tilt*.4);}
  return q;}
// cached tinted picture of each snowman for the room (rebuilt when its melt stage or size changes)
const ykCache=new Map();
function ykManCv(m,H){const st=Math.floor(Math.min(m.ml,1.2)*8),Hq=Math.max(24,Math.round(H/4)*4),key=[m.slot,m.e,m.m,m.h,m.a,st,Hq,S.room].join("|");
  let c=ykCache.get(key);if(c)return c;if(!ykImg())return null;
  c=document.createElement("canvas");const W=Math.ceil(Hq*1.5),HH=Math.ceil(Hq*1.2),d=Math.min(2,devicePixelRatio||1);c.width=W*d;c.height=HH*d;c.ww=W;c.hh=HH;
  const g=c.getContext("2d");g.scale(d,d);ykMan(g,m,W/2,HH-Hq*.08,Hq,st/8);g.globalCompositeOperation="source-atop";g.fillStyle=TINT[S.room]||"rgba(18,24,22,.24)";g.fillRect(0,0,W,HH);
  g.fillStyle="rgba(40,60,110,.12)";g.fillRect(0,0,W,HH);
  for(const k of ykCache.keys())if(k.startsWith(m.slot+"|"))ykCache.delete(k);ykCache.set(key,c);return c;}
function ykKmCv(w,ml){const sq=ml>.5?1-.45*(ml-.5)*2:1,key="km|"+Math.round(w/4)+"|"+Math.round(sq*20)+"|"+S.room;let c=ykCache.get(key);if(c)return c;if(!ykImg())return null;
  c=document.createElement("canvas");const W=Math.ceil(w),H=Math.ceil(w*330/480),d=Math.min(2,devicePixelRatio||1);c.width=W*d;c.height=H*d;c.ww=W;c.hh=H;
  const g=c.getContext("2d");g.scale(d,d);ykSp(g,"km",W/2,H-H*sq/2,W,H*sq);g.globalCompositeOperation="source-atop";g.fillStyle=TINT[S.room]||"rgba(18,24,22,.24)";g.fillRect(0,0,W,H);g.fillStyle="rgba(40,60,110,.12)";g.fillRect(0,0,W,H);
  for(const k of ykCache.keys())if(k.startsWith("km|"))ykCache.delete(k);ykCache.set(key,c);return c;}

// ── in the room: the kamakura (left) and up to 3 snowmen (right), drawn behind or in front of Musya by their floor line
const ykBox={km:null,men:[]};let ykSitS=null,ykGo=0;const ykCatCv=document.createElement("canvas");ykCatCv.width=384;ykCatCv.height=416;
const ykKd=(x,y)=>{const a=imgToStage(x-50,y,CAT_D),b=imgToStage(x+50,y,CAT_D);return Math.max(.05,(b[0]-a[0])/100);};
function ykDrawRoom(t,front){if(S.room!=="games"||scene.on||!ykImg())return;const s=ykS(),line=catLineY()+6;curRow=null;
  if(!front){ykBox.men=[];ykBox.km=null;}
  if(s.km&&(YK_KM.y>line)===front){const kd=ykKd(YK_KM.x,YK_KM.y),w=YK_KM.w*kd,[x,y]=imgToStage(YK_KM.x,YK_KM.y,CAT_D),c=ykKmCv(w,s.km.ml);
    if(c){const h=c.hh,sq=s.km.ml>.5?1-.45*(s.km.ml-.5)*2:1;ctx.drawImage(c,x-c.ww/2,y-h+h*.04,c.ww,h);ykBox.km=[x-w*.42,y-h*sq*.95,w*.84,h*sq*.95];
      const fl=.82+.1*Math.sin(t*7.3)+.06*Math.sin(t*12.1),gl=(sq<1?sq*sq:1)*fl,ks=w/480,hy=y-h+h*.04;
      ctx.save();ctx.globalAlpha=gl;ykSp(ctx,"km_glow",x,hy+h-h*sq/2,w,h*sq);ctx.restore();
      const ex=x+6*ks,ey=hy+h-(330-292)*ks*sq;
      if(ykSitS){ykCatDraw(t,ex,ey,ks*sq);}
      ctx.save();ctx.globalCompositeOperation="lighter";const R=150*ks,gr=ctx.createRadialGradient(ex,ey-30*ks,0,ex,ey-30*ks,R);gr.addColorStop(0,`rgba(255,170,80,${.32*gl})`);gr.addColorStop(1,"rgba(255,170,80,0)");
      ctx.fillStyle=gr;ctx.fillRect(ex-R,ey-30*ks-R,2*R,2*R);ctx.restore();}}
  for(const m of s.men){const p=YK_MEN[m.slot]||YK_MEN[0];if((p[1]>line)!==front)continue;const kd=ykKd(p[0],p[1]),H=YK_MH*kd*clamp(.85+(m.r1-90)/220,.8,1.1),[x,y]=imgToStage(p[0],p[1],CAT_D),c=ykManCv(m,H);
    if(!c)continue;ctx.drawImage(c,x-c.ww/2,y-(c.hh-H*.08),c.ww,c.hh);ykBox.men.push([x-H*.3,y-H*(m.ml>=1?.3:.95),H*.6,H*(m.ml>=1?.36:1),m]);}}
// Musya sitting in the kamakura entrance: her rest frames, warmed by the candle, clipped to the arch, a brazier with mochi in front
function ykCatDraw(t,ex,ey,ks){const g=ykCatCv.getContext("2d"),f=Math.floor(t*1.2)%8;g.setTransform(1,0,0,1,0,0);g.globalCompositeOperation="source-over";g.clearRect(0,0,384,416);
  frameImg("rest",f,g);try{drawWear(g,"rest",f,2);}catch(e){}g.globalCompositeOperation="source-atop";g.fillStyle="rgba(90,40,10,.3)";g.fillRect(0,0,384,416);g.fillStyle="rgba(255,170,90,.12)";g.fillRect(0,0,384,416);
  const sc=1.05*ks;ctx.drawImage(ykCatCv,ex-96*sc-14*ks,ey-195*sc+14*ks,192*sc,208*sc);
  ykSp(ctx,"brazier",ex+70*ks,ey+4*ks,84*ks,72*ks);
  const u=(t*.6)%1;ctx.save();ctx.globalAlpha=.4*Math.sin(Math.PI*u);ctx.fillStyle="#e8e2d8";ctx.beginPath();ctx.arc(ex+70*ks+Math.sin(t*2)*4*ks,ey-34*ks-u*60*ks,(5+u*7)*ks,0,Math.PI*2);ctx.fill();ctx.restore();}
function ykSitEnd(){if(!ykSitS)return;ykSitS=null;if(!petAway()&&S.room==="games")react("😸",1.4);}
function ykKmTap(){const s=ykS();if(ykSitS){ykSitEnd();return;}
  if(petAway()){toast("🏮 Муся в пути — камакура подождёт");return;}if(pet.action==="sleep"){toast("🏮 Муся спит — потом погреется");return;}
  ykGo=now();walkTo({x:YK_KM.x+20},"idle","❄️");}
function ykHit(x,y){if(S.room!=="games"||scene.on)return false;const inB=b=>b&&x>b[0]&&x<b[0]+b[2]&&y>b[1]&&y<b[1]+b[3];
  if(inB(ykBox.km)){ykKmTap();return true;}
  for(const b of ykBox.men)if(inB(b)){const m=b[4];sfx("pop");floatFx.push({g:m.ml>=1?"💧":"❄️",x:b[0]+b[2]/2,y:b[1]+10,t:now()});
    if(!petAway()&&pet.action!=="sleep"&&!ykSitS){const p=YK_MEN[m.slot];walkTo({x:p[0]-160},"peek",m.ml>=1?"🥺":m.ml>.5?"😿":"😺");}return true;}
  return false;}

// ── mini-game «Снеговик»: roll the big ball, roll the head, lift it, dress it
const YK_Y0=150,YK_Y1=1330,YK_CS=50,YK_GW=18,YK_GH=30;
const ykFit=G=>{const k=Math.min(G.W/900,G.H/1500);return{k,ox:(G.W-900*k)/2,oy:(G.H-1500*k)/2};};
const ykLoc=(G,x,y)=>{const f=ykFit(G);return[(x-f.ox)/f.k,(y-f.oy)/f.k];};
function ykYard(q){// dark ground (earth, dry grass, leaves) under a layer of snow, both at half resolution
  const mk=()=>{const c=document.createElement("canvas");c.width=450;c.height=750;return c;};
  const gd=mk(),g=gd.getContext("2d");g.fillStyle="#57534a";g.fillRect(0,0,450,750);
  for(let i=0;i<260;i++){const x=Math.random()*450,y=Math.random()*750;g.strokeStyle=`rgba(${110+Math.random()*50|0},${100+Math.random()*40|0},60,.5)`;g.lineWidth=1;g.beginPath();g.moveTo(x,y);g.lineTo(x+rand(-5,5),y-rand(4,10));g.stroke();}
  for(let i=0;i<60;i++){g.fillStyle=`rgba(${120+Math.random()*40|0},${70+Math.random()*30|0},34,.55)`;g.beginPath();g.ellipse(Math.random()*450,Math.random()*750,rand(2,4),rand(1,2),rand(0,3),0,Math.PI*2);g.fill();}
  for(let i=0;i<14;i++){g.fillStyle="rgba(150,150,140,.35)";g.beginPath();g.ellipse(Math.random()*450,Math.random()*750,rand(4,9),rand(3,6),0,0,Math.PI*2);g.fill();}
  const sn=mk(),h=sn.getContext("2d");h.fillStyle="#dfe6ef";h.fillRect(0,0,450,750);
  for(let i=0;i<500;i++){h.fillStyle=Math.random()<.5?"rgba(190,202,220,.14)":"rgba(250,252,255,.2)";h.beginPath();h.ellipse(Math.random()*450,Math.random()*750,rand(6,26),rand(4,14),rand(0,3),0,Math.PI*2);h.fill();}
  for(let i=0;i<120;i++){h.fillStyle="rgba(255,255,255,.9)";h.fillRect(Math.random()*450,Math.random()*750,1,1);}
  const vg=h.createLinearGradient(0,0,0,750);vg.addColorStop(0,"rgba(70,90,130,.25)");vg.addColorStop(1,"rgba(70,90,130,0)");h.fillStyle=vg;h.fillRect(0,0,450,750);
  q.gnd=gd;q.snow=sn;q.grid=new Float32Array(YK_GW*YK_GH).fill(1);}
function ykRoll(q,b,dt){const dx=q.tx-b.x,dy=q.ty-b.y,D=Math.hypot(dx,dy);if(D<1)return;const d=Math.min(D,1100*dt),ux=dx/D,uy=dy/D,ox=b.x,oy=b.y;
  b.x=clamp(b.x+ux*d,b.r,900-b.r);b.y=clamp(b.y+uy*d,YK_Y0+b.r*.6,YK_Y1-b.r*.6);
  for(const o of q.b)if(o!==b){const ex=b.x-o.x,ey=b.y-o.y,e=Math.hypot(ex,ey)||1,mn=o.r+b.r;if(e<mn){b.x=o.x+ex/e*mn;b.y=o.y+ey/e*mn;}}
  const mv=Math.hypot(b.x-ox,b.y-oy);if(mv<.1)return;b.rot+=mv/b.r;b.dir=Math.atan2(b.y-oy,b.x-ox);
  const fr=b.r*.75;let tk=0;const c0=Math.max(0,Math.floor((b.x-fr)/YK_CS)),c1=Math.min(YK_GW-1,Math.floor((b.x+fr)/YK_CS)),r0=Math.max(0,Math.floor((b.y-fr)/YK_CS)),r1=Math.min(YK_GH-1,Math.floor((b.y+fr)/YK_CS));
  for(let r=r0;r<=r1;r++)for(let c=c0;c<=c1;c++){const cx=(c+.5)*YK_CS,cy=(r+.5)*YK_CS;if(Math.hypot(cx-b.x,cy-b.y)>fr+YK_CS*.4)continue;const i=r*YK_GW+c,a=q.grid[i];if(a<=0)continue;const t=Math.min(a,a*mv/(YK_CS*.6));q.grid[i]=a-t;tk+=t;}
  const mx=q.ph==="big"?125:q.b[0].r*.8;b.r=Math.min(mx,Math.cbrt(b.r**3+tk*YK_CS*YK_CS*3));
  const h=q.snow.getContext("2d");h.globalCompositeOperation="destination-out";h.strokeStyle="rgba(0,0,0,.68)";h.lineCap="round";h.lineWidth=b.r*.72;h.beginPath();h.moveTo(ox/2,oy/2);h.lineTo(b.x/2,b.y/2);h.stroke();h.globalCompositeOperation="source-over";
  if(Math.random()<.3){tone(rand(70,110),.05,"triangle",.012);}
  if(b.r>=mx-.5&&!q.full){q.full=1;ykMsg(q,q.ph==="big"?"Ком такой тяжёлый, что больше не катится":"Голова готова — больше не надо");}}
function ykMsg(q,m){q.msg=m;q.msgT=q.clk;}
const ykCm=r=>Math.round(r*.8);
function ykManInit(G){const q=G.st;ykImg();Object.assign(q,{ph:"big",clk:0,b:[{x:450,y:1000,r:30,rot:0,dir:0}],drag:false,tx:450,ty:1000,sel:{e:"coal",m:"mikan",h:"bucket",a:"twig"},parts:[],full:0,btns:[]});
  ykYard(q);ykMsg(q,"Катай ком по снегу — он растёт");}
function ykNext(G){const q=G.st;if(q.ph==="big"){if(q.b[0].r<70){ykMsg(q,"Ком ещё маленький — покатай ещё");return;}
    q.ph="small";q.full=0;q.drag=false;let best=null,bv=-1;for(let i=0;i<24;i++){const x=rand(140,760),y=rand(300,1180);if(Math.hypot(x-q.b[0].x,y-q.b[0].y)<q.b[0].r+150)continue;let v=0;
      for(let r=0;r<YK_GH;r++)for(let c=0;c<YK_GW;c++)if(Math.hypot((c+.5)*YK_CS-x,(r+.5)*YK_CS-y)<180)v+=q.grid[r*YK_GW+c];if(v>bv){bv=v;best=[x,y];}}
    q.b.push({x:best?best[0]:450,y:best?best[1]:700,r:22,rot:0,dir:0});sfx("pop");ykMsg(q,"Теперь ком поменьше — для головы");return;}
  if(q.ph==="small"){const a=q.b[0].r,b=q.b[1].r;if(b<a*.45){ykMsg(q,"Голова пока слишком мала");return;}
    q.ph="lift";q.drag=false;q.man={r1:a,r2:b,e:"coal",m:"mikan",h:"bucket",a:"twig"};const g=ykGeo(q.man,450,990,600,0);q.L={hx:770,hy:990-g.R2*.95,R2:g.R2,tx:g.hx,ty:g.hy,drag:false,snap:-1,fall:0};
    ykMsg(q,"Юкидарума — два шара, как дарума: без ног");sfx("pop");}}
function ykManStep(G,dt){const q=G.st;q.clk+=dt;
  if((q.ph==="big"||q.ph==="small")&&q.drag)ykRoll(q,q.b[q.b.length-1],dt);
  if(q.ph==="lift"){const L=q.L;if(L.snap>=0){L.snap+=dt;const u=smooth(L.snap/.3);L.hx=mix(L.hx,L.tx,u);L.hy=mix(L.hy,L.ty,u);if(L.snap>.7){q.ph="deco";ykMsg(q,"Укрась снеговика");}}
    else if(!L.drag&&L.hy<990-L.R2*.95){L.fall+=dt*2600;L.hy=Math.min(990-L.R2*.95,L.hy+L.fall*dt);}}
  q.parts=q.parts.filter(p=>(p.t+=dt)<p.life);for(const p of q.parts){p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=1800*dt;}}
function ykPuff(q,x,y,n=14,sp=420){for(let i=0;i<n;i++){const a=rand(0,Math.PI*2),v=rand(.3,1)*sp;q.parts.push({x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v-sp*.6,t:0,life:rand(.4,.8),r:rand(5,12)});}}
function ykParts(g,q){for(const p of q.parts){g.globalAlpha=clamp(1-p.t/p.life,0,1);g.fillStyle="#eef3f8";g.beginPath();g.arc(p.x,p.y,p.r,0,Math.PI*2);g.fill();}g.globalAlpha=1;}
function ykBtn(g,q,x,y,w,h,label,key,on,ico){g.fillStyle=on?"rgba(232,196,120,.95)":"rgba(52,62,82,.88)";g.strokeStyle=on?"#fff1c8":"rgba(230,224,210,.35)";g.lineWidth=3;g.beginPath();g.roundRect(x,y,w,h,18);g.fill();g.stroke();
  if(ico){const r=YK_R[ico];const s=Math.min((h-16)/r[3],70/r[2]);ykSp(g,ico,x+46,y+h/2,r[2]*s,r[3]*s);ykTxt(g,label,x+92,y+h/2,28,on?"#2a1c10":"#f3ead8",700,"left");}
  else ykTxt(g,label,x+w/2,y+h/2,32,on?"#2a1c10":"#f3ead8",800);q.btns.push([x,y,w,h,key]);}
function ykSky(g,G){const f=ykFit(G);g.fillStyle="rgba(8,14,34,.42)";g.fillRect(-f.ox/f.k-10,-f.oy/f.k-10,G.W/f.k+20,G.H/f.k+20);   // a colder night over the temple yard
  const gr=g.createLinearGradient(0,900,0,1500);gr.addColorStop(0,"#9aa8bc");gr.addColorStop(1,"#4c566c");g.fillStyle=gr;g.fillRect(-f.ox/f.k-10,900,G.W/f.k+20,600+f.oy/f.k);
  g.fillStyle="rgba(255,255,255,.1)";for(let i=0;i<9;i++){g.beginPath();g.ellipse(((i*137)%1100)-100,915+(i*53)%70,160,22,0,0,Math.PI*2);g.fill();}}
function ykManDraw(G,g){const q=G.st,f=ykFit(G);q.btns=[];g.save();g.translate(f.ox,f.oy);g.scale(f.k,f.k);
  if(q.ph==="big"||q.ph==="small"){g.fillStyle="#2b2722";g.fillRect(-f.ox/f.k-10,-f.oy/f.k-10,G.W/f.k+20,G.H/f.k+20);g.drawImage(q.gnd,0,0,900,1500);g.drawImage(q.snow,0,0,900,1500);
    for(const b of q.b){g.fillStyle="rgba(20,26,44,.35)";g.beginPath();g.ellipse(b.x+b.r*.18,b.y+b.r*.55,b.r*.95,b.r*.45,0,0,Math.PI*2);g.fill();ykSp(g,"ball",b.x,b.y,b.r*2.04,b.r*2.04,b.rot);}
    const b=q.b[q.b.length-1];if(!q.drag&&q.clk%1.2<.8){g.strokeStyle="rgba(255,240,200,.6)";g.lineWidth=5;g.setLineDash([14,12]);g.beginPath();g.arc(b.x,b.y,b.r+26,0,Math.PI*2);g.stroke();g.setLineDash([]);}
    g.fillStyle="rgba(10,14,24,.72)";g.fillRect(-f.ox/f.k-10,0,G.W/f.k+20,140);
    const big=q.ph==="big";ykTxt(g,big?`Ком: ${ykCm(q.b[0].r)} см`:`Голова: ${ykCm(b.r)} см · туловище ${ykCm(q.b[0].r)} см`,450,46,40,"#f3ead8",800);
    const need=big?70:q.b[0].r*.45,mx=big?125:q.b[0].r*.8,u=clamp(b.r/mx,0,1);g.fillStyle="rgba(255,255,255,.15)";g.fillRect(150,92,600,16);g.fillStyle=b.r>=need?"#e8c478":"#9fb2cc";g.fillRect(150,92,600*u,16);
    g.fillStyle="#fff1c8";g.fillRect(150+600*need/mx-2,86,4,28);
    if(b.r>=need)ykBtn(g,q,230,1370,440,96,big?"Хватит — лепим голову ▶":"Поставить голову ▶","next",true);}
  else{ykSky(g,G);
    if(q.ph==="lift"){const L=q.L,m=q.man;ykMan(g,Object.assign({},m,{a:"none"}),450,990,600,0,true);
      g.fillStyle="rgba(16,22,40,.3)";g.beginPath();g.ellipse(L.hx,990,L.R2,L.R2*.16,0,0,Math.PI*2);g.fill();ykSp(g,"ball",L.hx,L.hy,L.R2*2,L.R2*1.9,.4);
      if(L.snap<0&&!L.drag){g.strokeStyle="rgba(255,240,200,.55)";g.lineWidth=5;g.setLineDash([14,12]);g.beginPath();g.arc(L.tx,L.ty,L.R2,0,Math.PI*2);g.stroke();g.setLineDash([]);}
      if(!petAway()&&IMG.gaze9)drawCatG(g,"gaze9",Math.floor(q.clk*.8)%8,110,1000,.95);
      ykTxt(g,"Перетащи голову на туловище",450,1110,36,"#1c2232",800);}
    else if(q.ph==="deco"||q.ph==="end"){const m=q.man;Object.assign(m,q.sel);ykMan(g,m,450,985,600,0);
      if(q.ph==="deco"){let y=1012;for(const [k,lab,opt] of YK_ROWS){ykTxt(g,lab,30,y+38,30,"#1c2232",800,"left");let x=170;
          for(const [id,v] of Object.entries(opt)){ykBtn(g,q,x,y,236,76,v[1],"sel:"+k+":"+id,q.sel[k]===id,v[0]);x+=246;}y+=86;}
        ykBtn(g,q,280,1360,340,92,"Готово ✓","fin",true);}}
    ykParts(g,q);}
  const e=q.clk-q.msgT;if(q.msg&&e<3.2){g.globalAlpha=clamp(Math.min(e/.2,(3.2-e)/.6),0,1);const y=q.ph==="big"||q.ph==="small"?200:120;g.fillStyle="rgba(10,14,24,.7)";g.beginPath();g.roundRect(60,y-36,780,72,30);g.fill();ykTxt(g,q.msg,450,y,32,"#fff3d8",700);g.globalAlpha=1;}
  g.restore();}
function ykManDown(G,x,y){const q=G.st,[sx,sy]=ykLoc(G,x,y);
  for(const b of q.btns)if(sx>b[0]&&sx<b[0]+b[2]&&sy>b[1]&&sy<b[1]+b[3]){ykBtnAct(G,b[4]);return;}
  if(q.ph==="big"||q.ph==="small"){const b=q.b[q.b.length-1];if(Math.hypot(sx-b.x,sy-b.y)<b.r+110){q.drag=true;q.tx=sx;q.ty=sy;}}
  if(q.ph==="lift"){const L=q.L;if(L.snap<0&&Math.hypot(sx-L.hx,sy-L.hy)<L.R2+80){L.drag=true;L.ox=L.hx-sx;L.oy=L.hy-sy;L.fall=0;}}}
function ykManMove(G,x,y,held){const q=G.st,[sx,sy]=ykLoc(G,x,y);if(!held)return;if(q.drag){q.tx=sx;q.ty=sy;}
  if(q.ph==="lift"&&q.L.drag){q.L.hx=clamp(sx+q.L.ox,0,900);q.L.hy=clamp(sy+q.L.oy,200,990-q.L.R2*.95);}}
function ykManUp(G){const q=G.st;q.drag=false;if(q.ph==="lift"&&q.L.drag){const L=q.L;L.drag=false;if(Math.hypot(L.hx-L.tx,L.hy-L.ty)<L.R2*.8+50){L.snap=0;sfx("pop");chime([784,988,1175]);ykPuff(q,L.tx,L.ty+L.R2*.8,16,380);}}}
function ykBtnAct(G,k){const q=G.st;if(k==="next"){ykNext(G);return;}
  if(k.startsWith("sel:")){const [,a,b]=k.split(":");q.sel[a]=b;sfx("pop");return;}
  if(k==="fin"&&q.ph==="deco"){q.ph="end";ykManFinish(G);}}
function ykManFinish(G){const q=G.st,s=ykS(),wk=ykWK();ykMelt(true);const m=Object.assign({},q.man,q.sel,{ml:0,at:Date.now()});
  // a free slot (a puddle counts as free), else the oldest snowman gives way
  const used=s.men.filter(x=>x.ml<1).map(x=>x.slot);let slot=[0,1,2].find(i=>!used.includes(i));
  if(slot==null){const o=s.men.filter(x=>x.ml<1).sort((a,b)=>b.ml-a.ml||a.at-b.at)[0];slot=o.slot;q.gave=1;}
  s.men=s.men.filter(x=>x.slot!==slot);m.slot=slot;s.men.push(m);s.n[wk]=(s.n[wk]||0)+1;s.tot=(s.tot||0)+1;q.res={first:!S.owned.has("yk_bucket"),three:s.n[wk]===3&&!S.owned.has("yk_scarf"),n:s.n[wk]};
  disc("snow","snowman_"+wk);if(!S.owned.has("yk_bucket"))S.owned.add("yk_bucket");award("yk_first");if(s.n[wk]>=3){if(!S.owned.has("yk_scarf"))S.owned.add("yk_scarf");award("yk_three");}
  S.needs.joy=clamp(S.needs.joy+8,0,100);ykCache.clear();save();chime([659,784,988,1319]);ykPuff(q,450,500,18,500);setTimeout(()=>{if(G.id==="yk_man"&&!G.over)gEnd();},900);}
function ykManCard(G){const q=G.st,r=q.res||{n:1},s=ykS();
  return`<div class="card"><p class="tag">雪だるま · юкидарума</p><h3>⛄ Снеговик готов</h3><p>Он встал у тории в «Играх». Пока на улице мороз — стоит, а когда станет теплее +2°, начнёт понемногу таять.</p>
   <p>Снеговиков этой зимой: ${r.n}${r.n<3&&!S.owned.has("yk_scarf")?" из 3 — за троих будет вязаный шарф":""}.${q.gave?" Самый старый снеговик уступил место новому.":""}</p>
   ${r.first?`<p>🎁 Новая вещь: <b>Ведёрко-шляпа</b> — в «🧺 Вещи».</p>`:""}${r.three?`<p>🎁 Новая вещь: <b>Вязаный шарф снеговика</b>.</p>`:""}
   <div class="row"><button class="btn" id="gHome">Посмотреть</button><button class="btn primary" id="gAgain">Ещё снеговика</button></div></div>`;}
const YK_GMAN={id:"yk_man",hidden:true,n:"Снеговик",tag:"雪だるま · юкидарума",icon:"⛄",bg:"temple",lives:null,time:null,
 lore:"В Японии снеговик — юкидарума: два снежных шара, как кукла-дарума без рук и ног.",how:"Катай ком пальцем — он растёт и собирает снег. Слепи голову, подними её и укрась.",
 init(G){ykManInit(G);},step(G,t,dt){ykManStep(G,dt);},draw(G,g){ykManDraw(G,g);},down(G,x,y){ykManDown(G,x,y);},move(G,x,y,h){ykManMove(G,x,y,h);},up(G){ykManUp(G);},
 stat:G=>{const q=G.st;return q.ph==="big"?"Катай большой ком":q.ph==="small"?"Катай голову":q.ph==="lift"?"Подними голову":"Укрась снеговика";},
 card(G){return ykManCard(G);},after(G){ykAfter(G);}};
GAMES.push(YK_GMAN);
function ykAfter(G){const h=$("gHome");if(h)h.onclick=()=>{closeGame();if(S.room!=="games")goRoom("games");};ui();hubDot();}

// ── mini-game «Камакура»: pile snow (taps), pack it (swipes), dig the entrance (taps), light the candle
const YK_KX=400,YK_KB=1090,YK_KW=700;
function ykKamaInit(G){ykImg();Object.assign(G.st,{ph:"pile",clk:0,p:0,pk:0,ho:0,lit:-1,parts:[],lx:null,ly:null,cat:-9,patD:0,btns:[]});ykMsg(G.st,"Насыпь сугроб: касайся экрана");}
function ykKamaStep(G,dt){const q=G.st;q.clk+=dt;q.parts=q.parts.filter(p=>(p.t+=dt)<p.life);for(const p of q.parts){p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=1800*dt;}
  if(q.lit>=0){q.lit+=dt;if(q.lit>2.2&&q.ph==="lit"){q.ph="end";ykKamaFinish(G);}}}
function ykKamaDraw(G,g){const q=G.st,f=ykFit(G);g.save();g.translate(f.ox,f.oy);g.scale(f.k,f.k);ykSky(g,G);
  const W=YK_KW,H=W*330/480,cy=YK_KB-H/2;
  if(q.ph==="pile"){const u=smooth(q.p);if(q.p>0){const w=W*(.3+.7*u),h=H*(.15+.85*u);ykSp(g,"mound",YK_KX,YK_KB-h/2,w,h);}}
  else{ykSp(g,"dome",YK_KX,cy,W,H);
    if(q.ph==="pack"){g.globalAlpha=1-q.pk;ykSp(g,"mound",YK_KX,cy,W,H);g.globalAlpha=1;}
    if(q.ph!=="pack"){const ks=W/480,ex=YK_KX+6*ks,ey=YK_KB-(330-226)*ks,o=q.ph==="hollow"?q.ho:1;
      if(o>0){g.save();g.beginPath();g.ellipse(ex,ey,130*ks*o,120*ks*o,0,0,Math.PI*2);g.clip();ykSp(g,"km",YK_KX,cy,W,H);g.restore();}
      if(q.lit>=0){const a=clamp(q.lit/1.2,0,1)*(.88+.08*Math.sin(q.clk*8));g.globalAlpha=a;ykSp(g,"km_glow",YK_KX,cy,W,H);g.globalAlpha=1;
        g.save();g.globalCompositeOperation="lighter";const R=300,gr=g.createRadialGradient(ex,ey+40,0,ex,ey+40,R);gr.addColorStop(0,`rgba(255,170,80,${.35*a})`);gr.addColorStop(1,"rgba(255,170,80,0)");g.fillStyle=gr;g.fillRect(ex-R,ey+40-R,2*R,2*R);g.restore();}}}
  ykParts(g,q);
  if(!petAway()&&IMG.play){const tap=q.clk-q.cat<.35;drawCatG(g,tap?"play":q.lit>=0?"purr":"gaze9",tap?(q.p*10|0)%2?2:5:Math.floor(q.clk*.8)%8,815,1110,.9);}
  const hint=q.ph==="pile"?`Сугроб: ${Math.round(q.p*100)}%`:q.ph==="pack"?`Утрамбовано: ${Math.round(q.pk*100)}%`:q.ph==="hollow"?`Вход: ${Math.round(q.ho*100)}%`:q.lit<0?"Коснись входа — зажги свечу":"";
  if(hint)ykTxt(g,hint,450,1240,40,"#1c2232",800);
  const e=q.clk-q.msgT;if(q.msg&&e<3.2){g.globalAlpha=clamp(Math.min(e/.2,(3.2-e)/.6),0,1);g.fillStyle="rgba(10,14,24,.7)";g.beginPath();g.roundRect(60,84,780,72,30);g.fill();ykTxt(g,q.msg,450,120,32,"#fff3d8",700);g.globalAlpha=1;}
  g.restore();}
function ykKamaDown(G,x,y){const q=G.st,[sx,sy]=ykLoc(G,x,y),ks=YK_KW/480,ex=YK_KX+6*ks,ey=YK_KB-(330-226)*ks;q.lx=sx;q.ly=sy;
  if(q.ph==="pile"){q.p=Math.min(1,Math.round(q.p*10+1)/10);q.cat=q.clk;const h=YK_KW*330/480*(.15+.85*q.p);for(let i=0;i<10;i++)q.parts.push({x:sx+rand(-30,30),y:1500,vx:(YK_KX-sx)*rand(.8,1.4)+rand(-200,200),vy:-rand(1500,1900),t:0,life:.9,r:rand(8,16)});
    tone(rand(160,220),.12,"triangle",.03);if(q.p>=1){q.ph="pack";ykMsg(q,"Утрамбуй: проводи пальцем по сугробу");sfx("pop");}return;}
  if(q.ph==="hollow"&&Math.abs(sx-YK_KX)<YK_KW*.5&&sy>YK_KB-YK_KW*.7&&sy<YK_KB+60){q.ho=Math.min(1,Math.round(q.ho*7+1)/7);q.cat=q.clk;ykPuff(q,ex+rand(-40,40),ey+60,10,520);tone(rand(120,160),.1,"square",.02);
    if(q.ho>=1){q.ph="light";ykMsg(q,"Вход готов. Зажги свечу внутри");chime([523,659,784]);}return;}
  if(q.ph==="light"&&Math.hypot(sx-ex,sy-ey)<240){q.ph="lit";q.lit=0;chime([784,988,1319,1568]);}}
function ykKamaMove(G,x,y,held){const q=G.st;if(!held||q.ph!=="pack")return;const [sx,sy]=ykLoc(G,x,y);if(q.lx==null){q.lx=sx;q.ly=sy;return;}
  const d=Math.hypot(sx-q.lx,sy-q.ly),H=YK_KW*330/480;q.lx=sx;q.ly=sy;if(Math.abs(sx-YK_KX)>YK_KW*.55||sy<YK_KB-H-60||sy>YK_KB+60)return;
  q.pk=Math.min(1,q.pk+d/4200);q.patD+=d;if(q.patD>90){q.patD=0;ykPuff(q,sx,sy,5,200);tone(rand(80,100),.06,"sine",.05);}
  if(q.pk>=1){q.ph="hollow";ykMsg(q,"Выкопай вход: касайся низа купола");sfx("pop");}}
function ykKamaFinish(G){const s=ykS(),wk=ykWK();ykMelt(true);G.st.first=!S.owned.has("yk_lantern");s.km={ml:0,at:Date.now()};s.kn[wk]=(s.kn[wk]||0)+1;ykLantern(true);
  disc("snow","kamakura_"+wk);S.owned.add("yk_lantern");award("yk_kama");S.needs.joy=clamp(S.needs.joy+8,0,100);ykCache.clear();save();gEnd();}
const YK_GKAMA={id:"yk_kama",hidden:true,n:"Камакура",tag:"かまくら · снежный домик",icon:"🏮",bg:"temple",lives:null,time:null,
 lore:"Камакура — снежный домик с севера Японии: внутри зажигают свечу, жарят моти и зовут гостей.",how:"Касайся — насыпай снег, води пальцем — утрамбуй, касайся купола — выкопай вход.",
 init(G){ykKamaInit(G);},step(G,t,dt){ykKamaStep(G,dt);},draw(G,g){ykKamaDraw(G,g);},down(G,x,y){ykKamaDown(G,x,y);},move(G,x,y,h){ykKamaMove(G,x,y,h);},up(G){G.st.lx=null;},
 stat:G=>{const q=G.st;return q.ph==="pile"?"Насыпь сугроб":q.ph==="pack"?"Утрамбуй":q.ph==="hollow"?"Выкопай вход":"Зажги свечу";},
 card(G){return`<div class="card"><p class="tag">かまくら · камакура</p><h3>🏮 Камакура готова</h3><p>Снежный домик стоит у тории в «Играх», а внутри горит свеча. Коснись его — и Муся заберётся греться у жаровни с моти.</p>
   ${G.st.first?`<p>🎁 Новая вещь: <b>Фонарик из камакуры</b> — в «🧺 Вещи».</p>`:""}<div class="row"><button class="btn" id="gHome">Посмотреть</button><button class="btn primary" id="gAgain" hidden>Ещё</button></div></div>`;},
 after(G){ykAfter(G);}};
GAMES.push(YK_GKAMA);

function ykOpen(k){if(G.id)return;const s=ykS();
  if(petAway()){toast("⛄ Муся в пути — снег подождёт");return;}
  if(!ykSnow()){toast("⛄ Снега пока нет — ждём зиму");return;}
  if(k==="kama"&&s.km&&s.km.ml<.5){closePanel();if(S.room!=="games")goRoom("games");toast("🏮 Камакура уже стоит у тории");return;}
  closePanel();ykImg();openPlace(k==="kama"?"yk_kama":"yk_man");}

// ── status line, hub card, tray, dots
const YK_MON=["январе","феврале","марте","апреле","мае","июне","июле","августе","сентябре","октябре","ноябре","декабре"];
function ykLine(){const s=ykS(),stand=s.men.filter(m=>m.ml<1),pud=s.men.length-stand.length,w=X.wx&&X.wx.real&&X.wx.real(),warm=ykRate()>0;
  const things=[stand.length?`${stand.length===1?"стоит снеговик":`стоят ${stand.length} снеговика`}`:"",s.km?"светится камакура":"",pud&&!stand.length?"от снеговика осталась лужа":""].filter(Boolean).join(", ");
  if(things)return`У тории ${things}${warm&&(stand.length||s.km)?` — ${w&&w.temp>2?`на улице +${Math.round(w.temp)}°, всё тает`:"весна, всё тает"}`:""}`;
  if(ykSnow())return"❄️ Лежит снег — можно слепить снеговика и построить камакуру";
  const mo=today().getMonth();return`Снега пока нет — зимой во дворике у тории можно будет слепить снеговика · ${mo===11||mo<2?"ждём снегопада":"снег ждём в декабре"}`;}
hook("hub",()=>{const s=ykS(),on=ykSnow(),wk=ykWK(),n=s.n[wk]||0;
  return`<div class="hubc"><h4>⛄ Зимние забавы <i>雪遊び</i></h4><p>${ykLine()}</p>
   <p class="yk-s">Юкидарума — японский снеговик из двух шаров. Скатай их сам, поставь голову и укрась: угольки, мандарин, ведёрко. Снеговики стоят, пока морозно, и тают выше +2°.${on?` Этой зимой: ${n} ${n===1?"снеговик":n>1&&n<5?"снеговика":"снеговиков"}.`:""}</p>
   <div class="row">${on?`<button class="btn primary" data-x="yk:man">⛄ Слепить снеговика</button><button class="btn" data-x="yk:kama">🏮 Камакура</button>`:""}${s.men.length||s.km?`<button class="btn" data-x="yk:go">Посмотреть</button>`:""}</div></div>`;});
hook("click",k=>{if(!k.startsWith("yk:"))return false;if(k==="yk:man")ykOpen("man");else if(k==="yk:kama")ykOpen("kama");else if(k==="yk:go"){closePanel();if(S.room!=="games")goRoom("games");}return true;});
hook("tray",(tray,room)=>{if(room!=="games"||(S.trayMode[room]||"play")!=="play"||!ykSnow())return;const el=tray.querySelector(".glist");if(!el||el.querySelector('[data-x="yk:man"]'))return;const s=ykS();
  el.insertAdjacentHTML("afterbegin",`<h4>Зимние забавы</h4><div class="games"><button class="gcard" data-x="yk:man"><b>⛄ Слепить снеговика</b><span>雪だるま · юкидарума</span><em>Этой зимой: ${s.n[ykWK()]||0}</em></button><button class="gcard" data-x="yk:kama"><b>🏮 Камакура</b><span>かまくら · снежный домик</span><em>${s.km?"Стоит у тории":"Построить"}</em></button></div>`);});
hook("hubDot",()=>ykSnow()&&!(ykS().n[ykWK()])&&!petAway());
hook("draw",(t,front)=>ykDrawRoom(t,front));
hook("hit",(x,y)=>ykHit(x,y));
hook("hideCat",()=>!!ykSitS&&S.room==="games"&&!scene.on);
hook("room",id=>{if(ykSitS)ykSitS=null;ykGo=0;if(id==="games")ykS().melted=0;});
hook("tick",()=>{if(ykGo&&pet.action!=="walkto"&&now()-ykGo>.3){ykGo=0;if(S.room==="games"&&ykS().km&&!petAway()&&pet.action!=="sleep"){ykSitS={t0:now(),until:now()+40};react("😌",2.4);S.needs.joy=clamp(S.needs.joy+5,0,100);chime([523,659]);}}
  if(ykSitS&&(now()>ykSitS.until||petAway()||scene.on||pet.action==="walkto"||pet.action==="sleep"))ykSitEnd();});
let ykSec=0;
hook("sec",()=>{ykSec++;if(ykSec%30===2)ykMelt(false);const s=ykS(),wk=ykWK();
  if(ykSec>8&&ykSnow()&&s.wk!==wk&&!scene.on&&!G.id&&!document.hidden&&!overlaysOpen()&&!$("toast").classList.contains("on")){s.wk=wk;toast("⛄ Выпал снег — можно слепить снеговика");save();}});
hook("boot",()=>{const s=ykS();ykMelt(true);ykLantern(!!s.km);if(ykSnow()||s.men.length||s.km)ykImg();});
hook("away",ms=>{const s=ykS();if(!s.melted)return null;const n=s.melted;s.melted=0;return{i:"💧",t:n>1?"Снеговики растаяли — у тории остались лужи":"Снеговик растаял — в луже осталось его ведёрко"};});
hook("album",el=>{const s=ykS();if(!s.tot&&!s.km)return;const k=Object.values(s.kn||{}).reduce((a,b)=>a+b,0);
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Зимние забавы</h3><p class="lead">Слеплено снеговиков: ${s.tot||0}, построено камакур: ${k}.</p>`);});
document.head.insertAdjacentHTML("beforeend","<style>:is(.story-body,.card,#panel) p.yk-s{font-size:13px;opacity:.8;margin:4px 0}</style>");

// test handles
X.snow={S:ykS,on:ykSnow,line:ykLine,melt(i,v){const s=ykS();if(i==="km"){if(s.km)s.km.ml=v;}else if(s.men[i])s.men[i].ml=v;ykCache.clear();},rate:ykRate,box:ykBox,
  sit(){ykKmTap();},sitNow(){ykSitS={t0:now(),until:now()+40};react("😌",2.4);},sitting:()=>!!ykSitS,open:ykOpen,
  ff(sec){for(let i=0;i<sec*60&&G.id&&!G.over;i++)G.def.step(G,now(),1/60);},
  // roll the current ball along a zigzag (u0..u1 = share of the yard height), synchronously
  roll(u0=0,u1=1,rows=5){if(!G.id||G.id!=="yk_man")return;const q=G.st,b=q.b[q.b.length-1];q.drag=true;
    for(let r=0;r<rows;r++){const y=YK_Y0+120+(YK_Y1-YK_Y0-240)*(u0+(u1-u0)*r/Math.max(1,rows-1));for(const x of r%2?[800,100]:[100,800]){q.tx=x;q.ty=y;for(let i=0;i<240&&Math.hypot(b.x-x,b.y-y)>4;i++)ykManStep(G,1/60);}}q.drag=false;return Math.round(b.r);},
  next(){if(G.id==="yk_man")ykNext(G);},lift(){if(G.id!=="yk_man")return;const L=G.st.L;L.hx=L.tx;L.hy=L.ty;L.drag=true;ykManUp(G);},
  dress(o){if(G.id==="yk_man")Object.assign(G.st.sel,o);},fin(){if(G.id==="yk_man")ykBtnAct(G,"fin");},
  tap(n,x=450,y=900){if(G.id!=="yk_kama")return;const f=ykFit(G);for(let i=0;i<n;i++){ykKamaDown(G,f.ox+x*f.k,f.oy+y*f.k);ykKamaStep(G,.05);}},
  pack(){if(G.id!=="yk_kama")return;const f=ykFit(G);G.st.lx=null;for(let i=0;i<80;i++){const x=YK_KX+Math.sin(i*.6)*300,y=YK_KB-180+Math.cos(i*.9)*90;ykKamaMove(G,f.ox+x*f.k,f.oy+y*f.k,true);}}};
}
