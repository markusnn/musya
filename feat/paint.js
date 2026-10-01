{
// ───────────────────────── «Картины Муси»: Musya walks over washi with inky paws; a finished painting gets a title, a hanko and a frame ─────────────────────────
// S.ext.paint = {n: paintings finished, fr: paintings ever framed, u:[ink ids used in finished paintings],
//   f:[{id:"mp_3" (its item slot), t:"Название", fr:"black"|"bamboo"|"gold", im: jpeg dataURL 192×256 (ink on white), d:dayKey, c:[ink ids]}] (≤ 12)}
// The twelve slots mp_1…mp_12 are room things («Картины Муси»); their pictures are painted at runtime into DIMG (mpSync).
const MP_INK=[["sumi","Суми","#1d1a18",0],["shu","Киноварь","#b5311d",0],["ai","Индиго","#264479",0],["kin","Золото","#c4922c",1],["sakura","Сакура","#e2849c",3],["koke","Мох","#5c7c36",5]];
const MP_FR=[["black","Чёрная"],["bamboo","Бамбук"],["gold","Золото"]],MP_FRN={black:"тонкая чёрная",bamboo:"бамбуковая",gold:"золотая"},MP_FB={black:12,bamboo:22,gold:26};
const MP_MAX=12,MP_PW=600,MP_PH=800,MP_CAT="Картины Муси",MP_TAU=Math.PI*2,MP_JP='"Hiragino Mincho ProN","Yu Mincho","Noto Serif JP",serif',MP_DSP='"Cormorant Garamond",Georgia,serif';
const MP_T={
 sumi:["Следы на первом снегу","Тушь и тишина","Ночная прогулка по рисовой бумаге","Чёрная кошка в безлунную ночь","Куда ушла Муся","Дорога к миске","Тень, которая убежала","Четыре лапки и одна тайна"],
 shu:["Красная луна над тремя лапками","Клён в октябре","Киноварь на рассвете","Фонари у ворот","Красные следы лисьей свадьбы","Печать на сердце"],
 ai:["Индиговая река","Дождь над черепичной крышей","Синяя ночь на веранде","Следы у пруда с карпами","Волна, которая мурлычет"],
 kin:["Золотая пыль светлячков","Тропа к храму на закате","Лунный свет на татами","Монетка для тануки"],
 sakura:["Лепестки сакуры на ветру","Весна пришла на мягких лапах","Ханами для одной кошки"],
 koke:["Мох у каменного фонаря","Сад после дождя","Бамбуковая роща шепчет"],
 many:["Праздник в Мусином доме","Фейерверк над рекой","Осенний сад, вид с подоконника","Все краски одной ночи","Мацури на кончиках лап"],
 roll:["Кувырок в облаках","Буря в чернильнице","Здесь кто-то кувыркался"],
 sit:["Привал на полпути","Здесь кто-то отдыхал","Луна, на которой посидели"],
 any:["Прогулка без цели","Здесь была Муся","Танец перед ужином","Мысли о рыбке","Лапки помнят дорогу","Утро, которого ещё нет"]};
addItems(Array.from({length:MP_MAX},(_,i)=>({id:"mp_"+(i+1),n:"Картина Муси",c:MP_CAT,w:150,h:208,a:"t",p:0,at:["mp",0,0],src:"🎨 картина",hint:"🎨 Нарисуйте с Мусей картину в комнате «Игры»"})),{mp:[150,208]});
for(let i=1;i<=MP_MAX;i++)loadItem["mp_"+i]=1;   // never cut from the atlas (that picture is only the fallback): mpSync paints them
STAMPS.push(["mp_first","画","Первая картина","Нарисуйте с Мусей картину лапками"],["mp_five","額","Пять картин в рамах","Вставьте в рамы пять картин Муси"],["mp_all","彩","Все краски","Используйте в картинах все шесть красок"]);
document.head.insertAdjacentHTML("beforeend",`<style>
.mp-gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:12px 8px;margin:8px 0 14px}
.mp-p{display:flex;flex-direction:column;align-items:center;gap:3px;background:none;border:0;padding:0;color:inherit;font:inherit;cursor:pointer;text-align:center}
.mp-p img{width:84px;height:auto;filter:drop-shadow(0 3px 4px rgba(0,0,0,.5))}
:is(#xpBody,#albumBody) .mp-p small{font-size:12px;line-height:1.25;color:var(--paper)}:is(#xpBody,#albumBody) .mp-p i{font-style:normal;font-size:10.5px;color:var(--muted)}
.mp-one{display:flex;flex-direction:column;align-items:center;gap:2px;margin:4px 0 6px;text-align:center}.mp-one img{width:min(200px,56vw);filter:drop-shadow(0 6px 10px rgba(0,0,0,.55))}
.card .mp-card img{display:block;margin:4px auto 2px;width:128px;filter:drop-shadow(0 5px 8px rgba(0,0,0,.5))}.card p.mp-new{color:var(--sakura)}</style>`);

function mpS(){const z=S.ext.paint||(S.ext.paint={n:0,fr:0,u:[],f:[]});z.f=z.f||[];z.u=z.u||[];return z;}
function mpPl(n,f){const a=n%10,b=n%100;return n+" "+(a===1&&b!==11?f[0]:a>=2&&a<=4&&(b<12||b>14)?f[1]:f[2]);}
const mpDate=dk=>new Date(Date.parse(dk+"T12:00:00Z")).toLocaleDateString("ru-RU",{day:"numeric",month:"long"});
const mpAd=(a,b)=>{let d=a-b;while(d>Math.PI)d-=MP_TAU;while(d<-Math.PI)d+=MP_TAU;return d;};
const mpUnl=n=>MP_INK.map((x,i)=>i).filter(i=>MP_INK[i][3]<=n);
function mpLead(){const z=mpS();return`Нарисовано картин: ${z.n}. В рамах: ${z.f.length} из ${MP_MAX}. Картину в раме можно повесить в любой комнате: «🧺 Вещи» → «${MP_CAT}».`;}
function mpUrl(c){try{return c.toDataURL("image/webp",.86);}catch(e){return c.toDataURL();}}

// ── washi (shared by the sheet and the framed things): cloudy mottling, kozo fibres, faint stains, darker deckled edges
let mpPap=null;
function mpPaper(){if(mpPap)return mpPap;const W=MP_PW,H=MP_PH,c=document.createElement("canvas");c.width=W;c.height=H;const g=c.getContext("2d"),r=rng(2203),gs=26,gx=Math.ceil(W/gs)+2,gy=Math.ceil(H/gs)+2,N=new Float32Array(gx*gy);
  for(let i=0;i<N.length;i++)N[i]=r()-.5;const im=g.createImageData(W,H),D=im.data;
  for(let y=0;y<H;y++){const fy=y/gs,iy=fy|0,ty=fy-iy;for(let x=0;x<W;x++){const fx=x/gs,ix=fx|0,tx=fx-ix,o=iy*gx+ix,
      n=(N[o]*(1-tx)+N[o+1]*tx)*(1-ty)+(N[o+gx]*(1-tx)+N[o+gx+1]*tx)*ty,l=233+n*15+(r()-.5)*8,i=(y*W+x)*4;D[i]=l;D[i+1]=l*.958;D[i+2]=l*.872;D[i+3]=255;}}
  g.putImageData(im,0,0);
  for(let i=0;i<1600;i++){const x=r()*W,y=r()*H,a=r()*MP_TAU,L=5+r()*18*(r()<.1?3:1),k=(r()-.5)*.7;g.strokeStyle=r()<.6?`rgba(255,251,238,${.3+r()*.3})`:`rgba(120,96,64,${.08+r()*.1})`;g.lineWidth=.5+r()*.8;
    g.beginPath();g.moveTo(x,y);g.quadraticCurveTo(x+Math.cos(a+k)*L*.6,y+Math.sin(a+k)*L*.6,x+Math.cos(a)*L,y+Math.sin(a)*L);g.stroke();}
  for(let i=0;i<12;i++){g.fillStyle=`rgba(150,118,72,${.03+r()*.035})`;g.beginPath();g.ellipse(r()*W,r()*H,12+r()*50,8+r()*30,r()*3,0,MP_TAU);g.fill();}
  const e=16;for(const [x0,y0,x1,y1,w,h] of [[0,0,0,e,W,e],[0,H,0,H-e,W,-e],[0,0,e,0,e,H],[W,0,W-e,0,-e,H]]){const lg=g.createLinearGradient(x0,y0,x1,y1);lg.addColorStop(0,"rgba(110,84,50,.32)");lg.addColorStop(1,"rgba(110,84,50,0)");g.fillStyle=lg;g.fillRect(x0,y0,w,h);}
  mpPap=c;return c;}

// ── the hanko «ムシャ»: vermilion seal, the kana cut out (read top to bottom), worn speckles
let mpHk=null;
function mpHanko(){if(mpHk)return mpHk;const w=64,h=96,c=document.createElement("canvas");c.width=w;c.height=h;const g=c.getContext("2d"),r=rng(88);
  g.fillStyle="#b3301f";g.beginPath();g.roundRect(2,2,w-4,h-4,8);g.fill();g.globalCompositeOperation="destination-out";g.lineWidth=2.6;g.strokeRect(7,7,w-14,h-14);
  g.textAlign="center";g.textBaseline="middle";g.font=`700 27px ${MP_JP}`;g.fillText("ム",w/2,25);g.fillText("シ",w/2,52);g.font=`700 19px ${MP_JP}`;g.fillText("ャ",w/2+4,74);
  for(let i=0;i<70;i++){g.globalAlpha=.3+r()*.7;g.beginPath();g.arc(r()*w,r()*h,r()*1.4+.3,0,MP_TAU);g.fill();}mpHk=c;return c;}

// ── frames, drawn around the outer rect (x,y,w,h) with thickness b
function mpTrap(g,pts,f){g.fillStyle=f;g.beginPath();pts.forEach(([a,c],i)=>i?g.lineTo(a,c):g.moveTo(a,c));g.closePath();g.fill();}
function mpFrame(g,x,y,w,h,b,kind){g.save();const T=[[x,y],[x+w,y],[x+w-b,y+b],[x+b,y+b]],B=[[x,y+h],[x+w,y+h],[x+w-b,y+h-b],[x+b,y+h-b]],Lf=[[x,y],[x+b,y+b],[x+b,y+h-b],[x,y+h]],R=[[x+w,y],[x+w-b,y+b],[x+w-b,y+h-b],[x+w,y+h]];
  if(kind==="black"){const gr=g.createLinearGradient(x,y,x+w,y+h);gr.addColorStop(0,"#2c2723");gr.addColorStop(.5,"#0f0d0c");gr.addColorStop(1,"#1e1a17");
    for(const p of [T,B,Lf,R])mpTrap(g,p,gr);mpTrap(g,T,"rgba(255,238,215,.13)");mpTrap(g,Lf,"rgba(255,238,215,.07)");mpTrap(g,B,"rgba(0,0,0,.35)");mpTrap(g,R,"rgba(0,0,0,.25)");
    g.strokeStyle="rgba(255,240,220,.22)";g.lineWidth=Math.max(.8,b*.07);g.strokeRect(x+b*.3,y+b*.3,w-b*.6,h-b*.6);
    g.strokeStyle="rgba(205,166,96,.85)";g.lineWidth=Math.max(.8,b*.11);g.strokeRect(x+b-g.lineWidth/2,y+b-g.lineWidth/2,w-2*b+g.lineWidth,h-2*b+g.lineWidth);}
  else if(kind==="gold"){const st=[[0,"#5a3b10"],[.18,"#c9952f"],[.36,"#f6dc86"],[.56,"#ad7a22"],[.76,"#ecc967"],[1,"#684512"]];
    const grad=(x0,y0,x1,y1)=>{const gr=g.createLinearGradient(x0,y0,x1,y1);for(const [o,c] of st)gr.addColorStop(o,c);return gr;};
    mpTrap(g,T,grad(0,y,0,y+b));mpTrap(g,B,grad(0,y+h,0,y+h-b));mpTrap(g,Lf,grad(x,0,x+b,0));mpTrap(g,R,grad(x+w,0,x+w-b,0));
    mpTrap(g,B,"rgba(50,24,0,.26)");mpTrap(g,R,"rgba(50,24,0,.18)");mpTrap(g,T,"rgba(255,246,210,.08)");
    const ins=b*.74,step=b*.42,dot=(px,py)=>{g.fillStyle="rgba(70,40,6,.6)";g.beginPath();g.arc(px+b*.025,py+b*.03,b*.075,0,MP_TAU);g.fill();g.fillStyle="#f8e39a";g.beginPath();g.arc(px,py,b*.065,0,MP_TAU);g.fill();};
    for(let p=x+ins;p<=x+w-ins+.1;p+=(w-2*ins)/Math.round((w-2*ins)/step)){dot(p,y+ins);dot(p,y+h-ins);}
    for(let p=y+ins;p<=y+h-ins+.1;p+=(h-2*ins)/Math.round((h-2*ins)/step)){dot(x+ins,p);dot(x+w-ins,p);}
    for(const [cx,cy] of [[x+b/2,y+b/2],[x+w-b/2,y+b/2],[x+b/2,y+h-b/2],[x+w-b/2,y+h-b/2]]){const rg=g.createRadialGradient(cx-b*.08,cy-b*.08,1,cx,cy,b*.3);rg.addColorStop(0,"#fff1b8");rg.addColorStop(.6,"#c8942e");rg.addColorStop(1,"#5e3e0e");g.fillStyle=rg;g.beginPath();g.arc(cx,cy,b*.3,0,MP_TAU);g.fill();}
    g.strokeStyle="rgba(60,34,4,.85)";g.lineWidth=Math.max(1,b*.06);g.strokeRect(x+b,y+b,w-2*b,h-2*b);g.strokeStyle="rgba(255,236,170,.5)";g.lineWidth=Math.max(.6,b*.04);g.strokeRect(x+.5,y+.5,w-1,h-1);}
  else{const o=b*.45,k=b/22,st=[[0,"#4b3b16"],[.2,"#a68d48"],[.45,"#e3d290"],[.7,"#b29852"],[1,"#463613"]],r=rng(Math.round(w+h));
    const pole=(x0,y0,len,hz)=>{const gr=hz?g.createLinearGradient(0,y0,0,y0+b):g.createLinearGradient(x0,0,x0+b,0);for(const [q,c] of st)gr.addColorStop(q,c);g.fillStyle=gr;g.beginPath();g.roundRect(x0,y0,hz?len:b,hz?b:len,b*.42);g.fill();
      const n=Math.max(2,Math.round(len/(b*3.3)));for(let i=1;i<n;i++){const p=(hz?x0:y0)+len*(i+(r()-.5)*.35)/n;
        g.fillStyle="rgba(58,42,12,.6)";if(hz)g.fillRect(p-1.4*k,y0+1,2.8*k,b-2);else g.fillRect(x0+1,p-1.4*k,b-2,2.8*k);
        g.fillStyle="rgba(255,246,205,.4)";if(hz)g.fillRect(p+1.4*k,y0+2*k,1.4*k,b-4*k);else g.fillRect(x0+2*k,p+1.4*k,b-4*k,1.4*k);}};
    pole(x,y-o,h+2*o,false);pole(x+w-b,y-o,h+2*o,false);pole(x-o,y,w+2*o,true);pole(x-o,y+h-b,w+2*o,true);
    g.strokeStyle="#3a2816";g.lineWidth=Math.max(1,b*.1);g.lineCap="round";
    for(const [cx,cy] of [[x+b/2,y+b/2],[x+w-b/2,y+b/2],[x+b/2,y+h-b/2],[x+w-b/2,y+h-b/2]]){g.beginPath();for(let i=-1;i<=1;i++){g.moveTo(cx-b*.42+i*b*.16,cy-b*.42);g.lineTo(cx+b*.42+i*b*.16,cy+b*.42);g.moveTo(cx+b*.42+i*b*.16,cy-b*.42);g.lineTo(cx-b*.42+i*b*.16,cy+b*.42);}g.stroke();}}
  g.restore();}
// the framed painting as a room thing: 300×416 (the item is 150×208): a cord on a brass nail, a shadow, washi × the ink, the frame
function mpFramed(src,kind){const c=document.createElement("canvas");c.width=300;c.height=416;const g=c.getContext("2d"),fx=10,fy=56,fw=280,fh=360,b=kind?MP_FB[kind]:0;
  if(kind){g.strokeStyle="#3a2c20";g.lineWidth=2.4;g.beginPath();g.moveTo(fx+fw*.2,fy+b*.5);g.lineTo(150,13);g.lineTo(fx+fw*.8,fy+b*.5);g.stroke();
    const ng=g.createRadialGradient(148,9,1,150,11,7);ng.addColorStop(0,"#f2d894");ng.addColorStop(1,"#6a4a1a");g.fillStyle=ng;g.beginPath();g.arc(150,11,6,0,MP_TAU);g.fill();}
  g.save();g.shadowColor="rgba(0,0,0,.5)";g.shadowBlur=12;g.shadowOffsetY=6;g.fillStyle="#2a2420";g.fillRect(fx+2,fy+2,fw-4,fh-4);g.restore();
  const ix=fx+b,iy=fy+b,iw=fw-2*b,ih=fh-2*b;g.drawImage(mpPaper(),ix,iy,iw,ih);g.save();g.globalCompositeOperation="multiply";g.drawImage(src,ix,iy,iw,ih);g.restore();
  if(kind){g.strokeStyle="rgba(0,0,0,.22)";g.lineWidth=3;g.strokeRect(ix+1.5,iy+1.5,iw-3,ih-3);mpFrame(g,fx,fy,fw,fh,b,kind);}
  return c;}

// ── framed paintings → DIMG (room things) + thumbnails; repainted when a painting or its frame changes
const MPC={};let mpOneId=null;
function mpDropC(id){for(const k of [...SPRC.keys()])if(k.startsWith(id+"|"))SPRC.delete(k);}
function mpSync(){const z=mpS();
  for(const p of z.f){const key=p.fr+"|"+p.im.length+"|"+p.t,e=MPC[p.id];IT[p.id].n=`«${p.t}»`;
    if(e&&e.k===key){if(e.c&&DIMG[p.id]!==e.c){DIMG[p.id]=e.c;mpDropC(p.id);}continue;}
    if(e&&e.busy===key)continue;MPC[p.id]=Object.assign({},e,{busy:key});
    const im=new Image();im.onload=()=>{if(MPC[p.id].busy!==key)return;const c=mpFramed(im,p.fr);MPC[p.id]={k:key,c,u:mpUrl(c)};DIMG[p.id]=c;mpDropC(p.id);
      if(panelIs("mp_gal"))mpGal();else if(panelIs("mp_one")&&mpOneId===p.id)mpOne(p.id);if(document.querySelector('#tray [data-item^="mp_"]'))ui();};im.src=p.im;}
  for(let i=1;i<=MP_MAX;i++){const id="mp_"+i;if(!z.f.some(p=>p.id===id)){if(MPC[id]){delete MPC[id];delete DIMG[id];mpDropC(id);}IT[id].n="Картина Муси";}}}
const mpImg=p=>MPC[p.id]&&MPC[p.id].u||p.im;

// ── the sheet: layout (phone column / wide side), the tatami floor, the paper
function mpLay(G){const s=G.s,W=G.W,H=G.H,side=W>H*1.05,bh=44*s;let L;
  if(!side){const by=H-bh-12*s,top=34*s,mh=by-124*s-top,pw=Math.min(W-28*s,mh*.75),ph=pw/.75,py=top,bw=Math.min(150*s,(W-40*s)/2);
    L={px:(W-pw)/2,py,pw,ph,sy:py+ph+(by-py-ph)/2-8*s,sx0:14*s,sx1:W-14*s,by,ty:top/2,tx:W/2,
      btns:[{id:"clear",n:"Стереть",x:14*s,y:by,w:bw,h:bh},{id:"done",n:"Готово",x:W-14*s-bw,y:by,w:bw,h:bh}]};}
  else{const top=34*s,ph=H-top-16*s,pw=ph*.75,px=Math.max(16*s,(W*.58-pw)/2),cx0=px+pw+26*s,cx1=W-20*s,by=H-bh-18*s,bw=Math.min(150*s,(cx1-cx0-10*s)/2),cx=(cx0+cx1)/2;
    L={px,py:top,pw,ph,sy:H*.46,sx0:cx0,sx1:cx1,by,ty:top/2,tx:px+pw/2,
      btns:[{id:"clear",n:"Стереть",x:cx-bw-5*s,y:by,w:bw,h:bh},{id:"done",n:"Готово",x:cx+5*s,y:by,w:bw,h:bh}]};}
  L.s=s;L.side=side;L.k=L.pw/MP_PW;L.sc=L.pw*.00122;L.sr=Math.min(25*s,(L.sx1-L.sx0)/12-5*s);
  L.fw=L.pw*.78;L.fh=L.ph*.78;L.fx=L.px+(L.pw-L.fw)/2;L.fy=L.py+(L.ph-L.fh)/2+10*s;   // the framing view
  const fb=(L.sx1-L.sx0-16*s)/3;L.fb=MP_FR.map(([id,n],i)=>({id,n,x:L.sx0+i*(fb+8*s),y:L.sy-20*s,w:fb,h:40*s}));
  L.kb=[{id:"bare",n:"Без рамы",x:L.btns[0].x,y:L.by,w:L.btns[0].w,h:bh},{id:"keep",n:"В раму",x:L.btns[1].x,y:L.by,w:L.btns[1].w,h:bh}];return L;}
function mpBuild(G){const q=G.st,L=mpLay(G),d=Math.min(2,devicePixelRatio||1),W=G.W,H=G.H,s=L.s,r=rng(61),night=dayTint()[1];q.L=L;q.lw=W;q.lh=H;
  const mk=()=>{const c=document.createElement("canvas");c.width=Math.round(W*d);c.height=Math.round(H*d);const g=c.getContext("2d");g.setTransform(d,0,0,d,0,0);return[c,g];};
  const [fc,f]=mk();f.fillStyle="#4c4730";f.fillRect(0,0,W,H);
  for(let y=0;y<H;y+=2.6*s){f.fillStyle=r()<.5?`rgba(255,238,180,${.03+r()*.05})`:`rgba(0,0,0,${.05+r()*.07})`;f.fillRect(0,y,W,1.3*s);}   // the straw weave
  for(let i=0;i<W*H/900;i++){f.fillStyle=`rgba(${r()<.5?"255,240,190":"20,16,8"},${.04+r()*.05})`;f.fillRect(r()*W,r()*H,(3+r()*14)*s,1*s);}
  const band=(x,y,w,h)=>{f.fillStyle="#1c1f26";f.fillRect(x,y,w,h);f.strokeStyle="rgba(170,160,130,.18)";f.lineWidth=1;f.strokeRect(x+1.5,y+1.5,w-3,h-3);};   // heri, the cloth borders of the mats
  band(W*.5-4.5*s,0,9*s,H);band(0,H*.52-4.5*s,W*.5,9*s);band(W*.5,H*.86-4.5*s,W*.5,9*s);
  const lg=f.createRadialGradient(W*.2,H*.05,0,W*.4,H*.35,Math.max(W,H)*1.05);lg.addColorStop(0,night?"#ffe2b0":"#fff8ea");lg.addColorStop(.5,night?"#a8865c":"#d8ccb4");lg.addColorStop(1,night?"#2c2014":"#7a6c56");
  f.save();f.globalCompositeOperation="multiply";f.fillStyle=lg;f.fillRect(0,0,W,H);f.restore();q.floor=fc;
  const [bc,b]=mk();b.drawImage(fc,0,0,W,H);b.save();b.shadowColor="rgba(0,0,0,.55)";b.shadowBlur=18*s;b.shadowOffsetY=7*s;b.fillStyle="#cfc3aa";b.fillRect(L.px,L.py,L.pw,L.ph);b.restore();
  b.drawImage(mpPaper(),L.px,L.py,L.pw,L.ph);const pg=b.createRadialGradient(W*.2,H*.05,0,W*.4,H*.35,Math.max(W,H)*1.1);pg.addColorStop(0,"#fff6e6");pg.addColorStop(.6,night?"#e2cba4":"#f3ece0");pg.addColorStop(1,night?"#a88c66":"#d6cbb6");
  b.save();b.globalCompositeOperation="multiply";b.fillStyle=pg;b.fillRect(L.px,L.py,L.pw,L.ph);b.restore();q.bg=bc;}

// ── the paws: a print = main pad (three lobes) + four toes; pressure (alpha, size), a darker core, the ink bleeding into washi, a dry paw leaves speckles
const mpA=q=>q.col<0?0:q.load>.28?clamp(.62+q.load*.4,0,1):clamp(q.load*2.4,0,.7);
function mpPaw(q,u,v,ang,sz,a){const g=q.ig,dry=q.load<.28;g.save();g.translate(u,v);g.rotate(ang+Math.PI/2);g.fillStyle=q.cc;g.globalCompositeOperation="multiply";
  if(!dry){g.globalAlpha=a*.07;g.beginPath();g.ellipse(0,-1*sz,16*sz,16*sz,0,0,MP_TAU);g.fill();}
  const part=(x,y,rx,ry,al,rot)=>{if(dry){const n=Math.round(rx*ry*1.3);g.globalAlpha=a*.9;for(let i=0;i<n;i++){const t=Math.random()*MP_TAU,m=Math.sqrt(Math.random());g.beginPath();g.arc((x+Math.cos(t)*rx*m)*sz,(y+Math.sin(t)*ry*m)*sz,(.5+Math.random()*.7)*sz,0,MP_TAU);g.fill();}return;}
    g.globalAlpha=a*al;g.beginPath();g.ellipse(x*sz,y*sz,rx*sz,ry*sz,rot,0,MP_TAU);g.fill();g.globalAlpha=a*al*.35;g.beginPath();g.ellipse(x*sz,(y+.7)*sz,rx*sz*.6,ry*sz*.58,rot,0,MP_TAU);g.fill();};
  part(0,3.6,7.2,5.6,rand(.78,.95),0);part(-3.7,6.5,3.4,2.7,.75,0);part(3.7,6.5,3.4,2.7,.75,0);
  for(const [tx,ty,tr] of [[-7.6,-5.2,-.35],[-2.7,-9.9,-.1],[2.7,-9.9,.1],[7.6,-5.2,.35]])part(tx+rand(-.4,.4),ty+rand(-.4,.4),2.7,3.4,rand(.62,1),tr);
  g.restore();}
function mpPrint(q,u,v,h){if(q.col<0||q.load<=0)return;const a=mpA(q),sz=rand(.9,1.1);mpPaw(q,u,v,h+rand(-.14,.14),sz,a*rand(.78,1));
  if(Math.random()<.1)for(const k of [3,6])mpPaw(q,u-Math.cos(h)*k,v-Math.sin(h)*k,h,sz,a*.26);   // a smudged, dragged print
  q.wet.push({u,v,h,sz,t:q.clk});if(q.wet.length>40)q.wet.shift();q.load=Math.max(0,q.load-.024);q.nPr++;const id=MP_INK[q.col][0];q.cnt[id]=(q.cnt[id]||0)+1;
  tone(170+Math.random()*50,.03,"sine",.012);}
// a tail swipe on a sharp turn: one curved brush stroke behind her, thick to thin, with bristle streaks
function mpTail(q,u,v,h0,h1){const a=mpA(q);if(a<=0)return;const g=q.ig,dir=Math.sign(mpAd(h1,h0))||1,a0=h0+Math.PI,a1=a0-dir*2.3,n=30;g.save();g.globalCompositeOperation="multiply";g.fillStyle=g.strokeStyle=q.cc;
  for(let i=0;i<=n;i++){const k=i/n,an=a0+(a1-a0)*k,rr=36+13*Math.sin(k*Math.PI),x=u+Math.cos(an)*rr,y=v-10+Math.sin(an)*rr*.75,w=(1-k)*9.5+1.2;g.globalAlpha=a*.36*(1-k*.45);g.beginPath();g.ellipse(x,y,w,w*.85,an,0,MP_TAU);g.fill();}
  g.lineWidth=1;for(const o of [-5,-2,1.5,4.5]){g.globalAlpha=a*.22;g.beginPath();for(let i=0;i<=n;i++){const k=i/n,an=a0+(a1-a0)*k,rr=36+o*(1-k)+13*Math.sin(k*Math.PI),x=u+Math.cos(an)*rr,y=v-10+Math.sin(an)*rr*.75;i?g.lineTo(x,y):g.moveTo(x,y);}g.stroke();}
  g.restore();q.load=Math.max(0,q.load-.04);q.tails++;}
// she sits: a round soft smudge of her bottom (with fur at the edge) and both front paws side by side
function mpSitMark(q){const a=mpA(q),c=q.cat;if(a<=0)return;const g=q.ig,x=c.u-c.face*4,y=c.v-8;g.save();g.globalCompositeOperation="multiply";g.fillStyle=g.strokeStyle=q.cc;
  for(let i=0;i<12;i++){g.globalAlpha=a*.1;g.beginPath();g.ellipse(x+rand(-2,2),y+rand(-2,2),27-i*1.6,20-i*1.2,0,0,MP_TAU);g.fill();}
  g.lineWidth=1.1;for(let i=0;i<34;i++){const t=Math.random()*MP_TAU,r0=.85+Math.random()*.2,L=3+Math.random()*5;g.globalAlpha=a*.3;g.beginPath();g.moveTo(x+Math.cos(t)*27*r0,y+Math.sin(t)*20*r0);g.lineTo(x+Math.cos(t)*(27*r0+L),y+Math.sin(t)*(20*r0+L));g.stroke();}
  g.restore();const h=c.face>0?0:Math.PI;mpPaw(q,c.u+c.face*20,c.v-1,h,.95,a*.9);mpPaw(q,c.u+c.face*22,c.v+13,h,.95,a*.85);q.load=Math.max(0,q.load-.1);q.sat++;}
// she rolls over: a big smear along the way with fur streaks
function mpSmear(q,x0,x1,v){const a=mpA(q);if(a<=0)return;const g=q.ig,n=Math.max(1,Math.ceil(Math.abs(x1-x0)/3));g.save();g.globalCompositeOperation="multiply";g.fillStyle=g.strokeStyle=q.cc;
  for(let i=1;i<=n;i++){const x=x0+(x1-x0)*i/n;g.globalAlpha=a*.07;g.beginPath();g.ellipse(x,v-22+rand(-2,2),18,27,0,0,MP_TAU);g.fill();
    if(Math.random()<.8){g.globalAlpha=a*.22;g.lineWidth=.8+Math.random();const yy=v-22+rand(-26,26),L=rand(8,22);g.beginPath();g.moveTo(x,yy);g.lineTo(x-Math.sign(x1-x0)*L,yy+rand(-1.5,1.5));g.stroke();}}
  g.restore();}

// ── Musya on the sheet: follows the finger, prints every stride, swipes her tail on sharp turns; sits, rolls, wanders off, licks her paws clean
function mpPush(q,u,v){const c=q.cat;u=clamp(u,36,MP_PW-36);v=clamp(v,62,MP_PH-24);const l=q.path[q.path.length-1]||[c.u,c.v];if(Math.hypot(u-l[0],v-l[1])<5)return;q.path.push([u,v]);q.mvT=q.clk;q.held1=0;
  if(c.act==="sit"||c.act==="groom"){c.act="rest";c.at=q.clk;}}
function mpAdv(q,mx,my,m){const c=q.cat;c.u+=mx;c.v+=my;c.wd+=m;if(Math.abs(mx)>m*.3)c.face=mx>0?1:-1;
  if(Math.hypot(c.u-c.au,c.v-c.av)>=12){const h=Math.atan2(c.v-c.av,c.u-c.au);if(c.h!=null&&Math.abs(mpAd(h,c.h))>1.75&&q.clk-c.tt>.4){mpTail(q,c.u,c.v,c.h,h);c.tt=q.clk;}c.h=h;c.au=c.u;c.av=c.v;}
  c.sd+=m;if(c.sd>=30){c.sd-=30;c.side=-c.side;const h=c.h??(c.face>0?0:Math.PI);mpPrint(q,c.u+Math.cos(h+Math.PI/2)*c.side*7,c.v+Math.sin(h+Math.PI/2)*c.side*7,h);}}
function mpWalk(q,dt){const c=q.cat;let back=0,pu=c.u,pv=c.v;for(const p of q.path){back+=Math.hypot(p[0]-pu,p[1]-pv);pu=p[0];pv=p[1];}
  let rem=(q.auto?160:clamp(260+back*3,260,1100))*dt;
  while(rem>0&&q.path.length){const [tu,tv]=q.path[0],dx=tu-c.u,dy=tv-c.v,d=Math.hypot(dx,dy);if(d<.01){q.path.shift();continue;}const m=Math.min(d,rem);mpAdv(q,dx/d*m,dy/d*m,m);rem-=m;if(m>=d)q.path.shift();}}
function mpSit(q){const c=q.cat;c.act="sit";c.at=q.clk;mpSitMark(q);tone(220,.12,"sine",.03);}
function mpRoll(q){const c=q.cat;let r1=clamp(c.u+c.face*120,50,MP_PW-50);if(Math.abs(r1-c.u)<70){c.face=-c.face;r1=clamp(c.u+c.face*120,50,MP_PW-50);}
  c.act="roll";c.at=q.clk;c.r0=c.pu=c.u;c.r1=r1;q.rolled++;[0,.15,.3].forEach((d,i)=>setTimeout(()=>tone(300+i*120,.12,"triangle",.03),d*1000));}
function mpAuto(q){const c=q.cat;let h=c.h??(c.face>0?0:Math.PI),u=c.u,v=c.v;const n=4+Math.floor(Math.random()*5);
  for(let i=0;i<n;i++){h+=rand(-.6,.6);let nu=u+Math.cos(h)*30,nv=v+Math.sin(h)*30;if(nu<50||nu>MP_PW-50||nv<80||nv>MP_PH-40){h+=Math.PI*.8;nu=u+Math.cos(h)*30;nv=v+Math.sin(h)*30;}
    u=clamp(nu,50,MP_PW-50);v=clamp(nv,80,MP_PH-40);q.path.push([u,v]);}q.auto=true;}
function mpArrive(q){const r=Math.random();if(q.load>.3&&r<.13)mpRoll(q);else if(q.load>.15&&r<.38)mpSit(q);else if(q.load>.3&&r<.72)mpAuto(q);}
function mpDip(q,i){const c=MP_INK[i];if(!c||c[3]>mpS().n)return;q.col=i;q.cc=c[2];q.load=1;q.dipT=q.clk;q.dipI=i;q.bub={e:pick(["😺","😼","🐾"]),t:q.clk};sfx("splash");tone(520+i*40,.08,"sine",.03);}
function mpSaucers(q){const n=mpS().n,on=mpUnl(n),nx=MP_INK.findIndex(x=>x[3]>n),list=nx>=0?[...on,nx]:on,L=q.L,w=(L.sx1-L.sx0)/list.length;
  return list.map((i,j)=>({i,x:L.sx0+w*(j+.5),y:L.sy,r:L.sr,lock:MP_INK[i][3]>n}));}
function mpTitle(q){const z=mpS(),cols=Object.keys(q.cnt).sort((a,b)=>q.cnt[b]-q.cnt[a]),taken=new Set(z.f.map(p=>p.t));let pool;
  if(cols.length>=3&&Math.random()<.5)pool=MP_T.many;else if(q.rolled&&Math.random()<.4)pool=MP_T.roll;else if(q.sat&&Math.random()<.3)pool=MP_T.sit;else if(Math.random()<.72)pool=MP_T[cols[0]]||MP_T.any;else pool=MP_T.any;
  const free=pool.filter(t=>!taken.has(t)),all=Object.values(MP_T).flat().filter(t=>!taken.has(t));return pick(free.length?free:all.length?all:pool);}
function mpComp(q){const c=document.createElement("canvas");c.width=192;c.height=256;const g=c.getContext("2d");g.fillStyle="#fff";g.fillRect(0,0,192,256);g.drawImage(q.ink,0,0,192,256);return c;}
function mpFree(){const used=new Set(mpS().f.map(p=>p.id));for(let i=1;i<=MP_MAX;i++)if(!used.has("mp_"+i))return"mp_"+i;return null;}
function mpFinish(q,fr){const z=mpS();z.n++;const used=Object.keys(q.cnt);for(const k of used)if(!z.u.includes(k))z.u.push(k);
  const unl=[];MP_INK.forEach(([id,,,th],i)=>{if(th<=z.n&&disc("paint","c_"+id)&&th>0)unl.push(i);});
  const comp=mpComp(q),R={unl,framed:null,full:false};
  if(fr){const id=mpFree();if(!id)R.full=true;else{let qq=.84,im=comp.toDataURL("image/jpeg",qq);const tot=()=>z.f.reduce((a,p)=>a+p.im.length,0)+im.length;while(tot()>400000&&qq>.35){qq-=.12;im=comp.toDataURL("image/jpeg",qq);}
    z.f.push({id,t:q.title,fr,im,d:dayKey(),c:used});z.fr=(z.fr||0)+1;S.owned.add(id);R.framed=fr;R.id=id;if(z.fr>=5)award("mp_five");}}
  R.url=mpUrl(mpFramed(comp,R.framed));award("mp_first");if(MP_INK.every(([id])=>z.u.includes(id)))award("mp_all");
  S.needs.joy=clamp(S.needs.joy+8,0,100);S.needs.clean=clamp(S.needs.clean-10,0,100);save();mpSync();q.R=R;}

function mpTx(g,txt,x,y,font,col,al="center"){g.font=font;g.textAlign=al;g.textBaseline="middle";g.fillStyle=col;g.fillText(txt,x,y);}
function mpFit(g,txt,font,size,maxW){g.font=font.replace("#",size);const w=g.measureText(txt).width;return w>maxW?size*maxW/w:size;}
function mpSaucerDraw(g,o,q,t,s){const {x,y,r}=o,ink=MP_INK[o.i],sel=q.col===o.i&&q.ph==="paint";
  g.fillStyle="rgba(10,8,4,.35)";g.beginPath();g.ellipse(x+2*s,y+r*.32,r*1.04,r*.5,0,0,MP_TAU);g.fill();
  const dg=g.createLinearGradient(x,y-r*.6,x,y+r*.6);dg.addColorStop(0,"#f1eadb");dg.addColorStop(1,"#958a78");g.fillStyle=dg;g.beginPath();g.ellipse(x,y,r,r*.6,0,0,MP_TAU);g.fill();
  g.fillStyle="#b9ae9a";g.beginPath();g.ellipse(x,y+r*.04,r*.78,r*.44,0,0,MP_TAU);g.fill();
  if(!o.lock){const rip=q.dipI===o.i?clamp(1-(q.clk-q.dipT)/.6,0,1):0;g.fillStyle=ink[2];g.beginPath();g.ellipse(x,y+r*.06,r*.7,r*.38,0,0,MP_TAU);g.fill();
    g.fillStyle="rgba(255,255,255,.35)";g.beginPath();g.ellipse(x-r*.25,y-r*.06,r*.22,r*.07,-.15,0,MP_TAU);g.fill();
    if(rip>0){g.strokeStyle=`rgba(255,255,255,${.5*rip})`;g.lineWidth=1.2;g.beginPath();g.ellipse(x,y+r*.06,r*.7*(1-rip*.7),r*.38*(1-rip*.7),0,0,MP_TAU);g.stroke();}}
  else{g.globalAlpha=.85;drawEmoji(g,"🔒",x,y+r*.02,r*.62);g.globalAlpha=1;}
  if(sel){g.strokeStyle=`rgba(255,228,160,${.7+.25*Math.sin(t*4)})`;g.lineWidth=2.4*s;g.beginPath();g.ellipse(x,y,r+4*s,r*.6+4*s,0,0,MP_TAU);g.stroke();}
  const n=mpS().n;mpTx(g,o.lock?`через ${mpPl(ink[3]-n,["картину","картины","картин"])}`:ink[1],x,y+r*.6+11*s,`600 ${(o.lock?10.5:12)*s}px ${q.UI}`,o.lock?"rgba(216,210,195,.6)":sel?"#ffe6b0":"#e8dfca");}
function mpCat(g,q,x,y,sc,st,fr,rot){if(petAway())return;g.fillStyle="rgba(40,28,16,.22)";g.beginPath();g.ellipse(x,y-2*sc,56*sc,13*sc,0,0,MP_TAU);g.fill();
  if(rot){g.save();g.translate(x,y-52*sc);g.rotate(rot);drawCatG(g,st,fr,0,52*sc,sc);g.restore();}else drawCatG(g,st,fr,x,y,sc);
  if(q.bub){const e=q.clk-q.bub.t;if(e<1.8)drawEmoji(g,q.bub.e,x+30*sc*2,y-190*sc-e*8,22*q.L.s,clamp(Math.min(e*4,(1.8-e)*2),0,1));else q.bub=null;}}

const MPG={id:"mp_paint",hidden:true,n:"Муся рисует",tag:"墨 · Суми-э лапками",bg:"room",lives:null,time:null,icon:"🎨",lore:"",how:"",
 init(G){G.score=0;const ik=document.createElement("canvas");ik.width=MP_PW;ik.height=MP_PH;
   Object.assign(G.st,{ink:ik,ig:ik.getContext("2d"),col:-1,cc:"#000",load:0,dipT:-9,dipI:-1,path:[],drag:false,pend:0,auto:false,held1:0,mvT:0,clk:0,wet:[],nPr:0,cnt:{},sat:0,rolled:0,tails:0,
     ph:"paint",fr:"black",title:"",msg:null,bub:null,R:null,UI:getComputedStyle(document.body).fontFamily,
     cat:{u:MP_PW*.62,v:MP_PH*.74,face:-1,act:"rest",at:0,wd:0,sd:0,side:1,h:null,au:MP_PW*.62,av:MP_PH*.74,tt:-9}});mpBuild(G);},
 step(G,t,dt){const q=G.st;if(q.lw!==G.W||q.lh!==G.H)mpBuild(G);q.clk+=dt;const c=q.cat,k=q.clk;
   if(q.ph==="stamp"){if(!q.stamped&&k-q.stT>.32){q.stamped=1;const g=q.ig;g.save();g.globalAlpha=.93;g.translate(MP_PW-62,MP_PH-84);g.rotate(-.05);g.drawImage(mpHanko(),-26,-39,52,78);g.restore();}
     if(k-q.stT>1.1)q.ph="frame";return;}
   if(q.ph==="done"){if(k-q.doneT>1.6&&!G.over)gEnd();return;}if(q.ph!=="paint")return;
   if(c.act==="roll"){const e=(k-c.at)/.9;if(e>=1){c.act="rest";c.at=k;q.bub={e:"😹",t:k};q.load=Math.max(0,q.load-.2);}else{const u=c.r0+(c.r1-c.r0)*smooth(e);mpSmear(q,c.pu,u,c.v);c.pu=c.u=u;}}
   else if(c.act==="sit"||c.act==="groom"){if(k-c.at>(c.act==="sit"?1.4:2.4)){if(c.act==="groom"){q.load=0;q.bub={e:"😽",t:k};}c.act="rest";c.at=k;}}
   if(c.act==="rest"||c.act==="walk"){
     if(q.path.length){mpWalk(q,dt);c.act="walk";}
     else{if(c.act==="walk"){c.act="rest";c.at=k;}
       if(q.drag){if(k-q.mvT>1.1&&!q.held1&&q.load>.1){q.held1=1;mpSit(q);}}   // the finger rests → she sits down for a moment
       else if(q.pend){q.pend=0;mpArrive(q);}
       else if(q.auto){q.auto=false;if(Math.random()<.4)mpSit(q);}
       else if(q.load>.2&&k-c.at>7){c.act="groom";c.at=k;}}}   // bored: licks the ink off her paws
   q.wet=q.wet.filter(w=>k-w.t<3.2);},
 draw(G,g,t){const q=G.st,L=q.L;if(!L)return;const s=L.s,c=q.cat,k=q.clk,z=mpS();
   if(q.ph==="frame"||q.ph==="done"){g.drawImage(q.floor,0,0,G.W,G.H);
     const fb=MP_FB[q.fr],b=fb/(280-2*fb)*L.fw,ox=L.fx-b,oy=L.fy-b,ow=L.fw+2*b,oh=L.fh+2*b;
     g.save();g.shadowColor="rgba(0,0,0,.6)";g.shadowBlur=20*s;g.shadowOffsetY=8*s;g.fillStyle="#1a1612";g.fillRect(ox,oy,ow,oh);g.restore();
     g.drawImage(mpPaper(),L.fx,L.fy,L.fw,L.fh);g.save();g.globalCompositeOperation="multiply";g.drawImage(q.ink,L.fx,L.fy,L.fw,L.fh);g.restore();mpFrame(g,ox,oy,ow,oh,b,q.fr);
     const tt=`«${q.title}»`;mpTx(g,tt,L.tx,L.ty+2*s,`italic 700 ${mpFit(g,tt,`italic 700 #px ${MP_DSP}`,22*s,(L.side?L.pw:G.W)-24*s)}px ${MP_DSP}`,"#f1e6cf");
     const full=!mpFree();
     if(q.ph==="frame"){for(const o of L.fb)btnRect(g,o.x,o.y,o.w,o.h,o.n,o.id===q.fr);
       if(full){mpTx(g,"Все 12 рам заняты — снимите картину в «家»",(L.sx0+L.sx1)/2,L.sy+34*s,`600 ${12*s}px ${q.UI}`,"#e8c9a0");btnRect(g,L.kb[0].x,L.kb[0].y,L.kb[0].w,L.kb[0].h,L.kb[0].n,true);}
       else for(const o of L.kb)btnRect(g,o.x,o.y,o.w,o.h,o.n,o.id==="keep");}
     const sc=L.sc*.85,cx=L.fx+L.fw*.1,cy=oy+oh+14*s,dn=q.ph==="done";mpCat(g,q,cx,cy,sc,dn?"highfive":"rest",dn?Math.min(7,Math.floor((k-q.doneT)/1.2*8)):Math.floor(k*1.2)%8,0);
     if(dn)for(let i=0;i<5;i++){const e=(k-q.doneT)*1.2-i*.15;if(e>0&&e<1)drawEmoji(g,"✨",ox+ow*(.15+.18*i),oy+oh*.2+i%2*30*s-e*30*s,16*s,1-e);}
     return;}
   g.drawImage(q.bg,0,0,G.W,G.H);g.save();g.globalCompositeOperation="multiply";g.drawImage(q.ink,L.px,L.py,L.pw,L.ph);g.restore();
   for(const w of q.wet){const al=1-(k-w.t)/3.2;if(al<=0)continue;const x=L.px+w.u*L.k,y=L.py+w.v*L.k,m=L.k*w.sz;   // wet ink glistens, then dries matte
     g.save();g.translate(x,y);g.rotate(w.h+Math.PI/2);g.fillStyle=`rgba(255,255,255,${.4*al})`;g.beginPath();g.ellipse(-2*m,1.6*m,2.6*m,1.1*m,-.4,0,MP_TAU);g.fill();
     for(const [tx,ty] of [[-7.6,-5.2],[-2.7,-9.9],[2.7,-9.9],[7.6,-5.2]]){g.beginPath();g.ellipse((tx-.7)*m,(ty-1)*m,.9*m,.6*m,0,0,MP_TAU);g.fill();}g.restore();}
   if(q.ph==="stamp"&&!q.stamped){const u=clamp((k-q.stT)/.32,0,1),sz=1.9-.9*smooth(u),x=L.px+(MP_PW-62)*L.k,y=L.py+(MP_PH-84)*L.k;
     g.save();g.globalAlpha=u;g.translate(x,y);g.rotate(-.05);g.drawImage(mpHanko(),-26*L.k*sz,-39*L.k*sz,52*L.k*sz,78*L.k*sz);g.restore();}
   const x=L.px+c.u*L.k,y=L.py+c.v*L.k;
   if(c.act==="roll"){const e=clamp((k-c.at)/.9,0,1);mpCat(g,q,x,y,L.sc,"play",Math.floor(e*16)%8,c.face*smooth(e)*MP_TAU);}
   else if(c.act==="walk")mpCat(g,q,x,y,L.sc,c.face>0?"moveRight":"moveLeft",Math.floor(c.wd/7.5)%8,0);
   else if(c.act==="groom")mpCat(g,q,x,y,L.sc,"groom",Math.min(7,Math.floor((k-c.at)/2.4*8)),0);
   else mpCat(g,q,x,y,L.sc,"rest",Math.floor(k*1.2)%8,0);
   for(const o of mpSaucers(q))mpSaucerDraw(g,o,q,t,s);
   for(const b of L.btns)btnRect(g,b.x,b.y,b.w,b.h,b.n,b.id==="done"&&q.nPr>0&&q.ph==="paint");
   mpTx(g,`Картин в рамках: ${z.f.length} из ${MP_MAX}`,L.tx,L.ty,`600 ${12.5*s}px ${q.UI}`,"rgba(232,223,202,.75)");
   const hint=q.msg&&k-q.msg.t<3.2?q.msg.s:!q.nPr&&!q.path.length&&q.ph==="paint"?(q.col<0?"Нажмите на блюдце с краской":"Ведите пальцем по бумаге — Муся пойдёт следом"):"";
   if(hint){g.save();g.font=`600 ${13*s}px ${q.UI}`;const hw=g.measureText(hint).width+26*s,hy=L.py+L.ph-26*s;g.fillStyle="rgba(24,18,14,.74)";g.beginPath();g.roundRect(L.px+L.pw/2-hw/2,hy-14*s,hw,28*s,14*s);g.fill();g.restore();
     mpTx(g,hint,L.px+L.pw/2,hy,`600 ${13*s}px ${q.UI}`,"#efe6d4");}},
 down(G,x,y,t){const q=G.st,L=q.L;if(!L)return;const s=L.s,hitB=b=>x>=b.x&&x<=b.x+b.w&&y>=b.y&&y<=b.y+b.h;
   if(q.ph==="frame"){const f=L.fb.find(hitB);if(f){q.fr=f.id;tone(660,.06,"triangle",.04);return;}const b=L.kb.find(hitB);if(!b)return;
     const fr=b.id==="keep"&&mpFree()?q.fr:null;if(b.id==="keep"&&!fr)return;mpFinish(q,fr);q.ph="done";q.doneT=q.clk;G.score=1;chime(fr?[1046,1318,1568]:[784,988]);return;}
   if(q.ph!=="paint")return;const b=L.btns.find(hitB);
   if(b){tone(260,.05,"triangle",.05);if(b.id==="clear"){q.ig.clearRect(0,0,MP_PW,MP_PH);Object.assign(q,{nPr:0,cnt:{},wet:[],sat:0,rolled:0,tails:0});tone(500,.12,"triangle",.02);return;}
     if(!q.nPr){q.msg={t:q.clk,s:"Сначала окуните лапку и пройдитесь по бумаге"};return;}
     q.title=mpTitle(q);q.ph="stamp";q.stT=q.clk;q.stamped=0;q.path=[];q.drag=false;setTimeout(()=>{tone(105,.16,"sine",.22);tone(210,.07,"triangle",.07);},300);return;}
   const o=mpSaucers(q).find(o=>Math.hypot(x-o.x,(y-o.y)/.75)<o.r+10*s);
   if(o){if(o.lock){q.msg={t:q.clk,s:`«${MP_INK[o.i][1]}» откроется через ${mpPl(MP_INK[o.i][3]-mpS().n,["картину","картины","картин"])}`};tone(300,.1,"sine",.03);}else mpDip(q,o.i);return;}
   const u=(x-L.px)/L.k,v=(y-L.py)/L.k;
   if(u>-20&&v>-20&&u<MP_PW+20&&v<MP_PH+20&&!petAway()){q.drag=true;q.pend=0;if(q.auto){q.auto=false;q.path=[];}mpPush(q,u,v);if(q.col<0)q.msg={t:q.clk,s:"Лапки чистые — сначала окуните их в краску"};}},
 move(G,x,y,held){const q=G.st,L=q.L;if(!q.drag||!held||!L)return;mpPush(q,(x-L.px)/L.k,(y-L.py)/L.k);},
 up(G){const q=G.st;if(q.drag){q.drag=false;q.pend=1;}},
 stat:G=>{const q=G.st;return q.ph!=="paint"?"🖼 рама":q.col<0?"🐾 лапки чистые":q.load<=0?"🐾 краска кончилась":`🐾 ${MP_INK[q.col][1].toLowerCase()} · ${Math.round(q.load*100)}%`;},
 card(G){const q=G.st,R=q.R||{unl:[]},z=mpS();
   return`<div class="card"><p class="tag">墨 · Картины Муси</p><h3>«${q.title}»</h3>${R.url?`<div class="mp-card"><img src="${R.url}" alt=""></div>`:""}
   <p class="lore">${R.framed?`Рама ${MP_FRN[R.framed]}. Картина ждёт в «🧺 Вещи» → «${MP_CAT}» — её можно повесить в любой комнате.`:R.full?"Все двенадцать рам заняты — снимите одну из картин в «家» → «Картины Муси».":"Эту картину оставили без рамы."} В рамах: ${z.f.length} из ${MP_MAX}.</p>
   ${R.unl.length?`<p class="mp-new">🎨 Новая краска: ${R.unl.map(i=>MP_INK[i][1].toLowerCase()).join(", ")}!</p>`:""}<p class="lore">Лапки у Муси в краске — после рисования ей не помешает онсэн.</p>
   <div class="row"><button class="btn" id="gHome">Домой</button><button class="btn primary" id="gAgain">Ещё картину</button></div></div>`;},
 after(){ui();}};
GAMES.push(MPG);
function mpOpen(){if(G.id)return;if(petAway()){toast("Муся в пути — порисуете, когда вернётся");return;}closePanel();$("album").hidden=true;openPlace("mp_paint");}

// ── the gallery (家 → «Галерея»): framed paintings → one painting: change the frame or take it down
function mpGal(){const z=mpS();mpOneId=null;
  openPanel(MP_CAT,`<p class="lead">${mpLead()}</p>${z.f.length?`<div class="mp-gal">${z.f.map(p=>`<button class="mp-p" data-x="mp:p:${p.id}"><img src="${mpImg(p)}" alt=""><small>«${p.t}»</small><i>${mpDate(p.d)}</i></button>`).join("")}</div>`:`<p class="lead">Пока ни одной картины в раме.</p>`}
   <div class="row"><button class="btn primary" data-x="mp:go">Рисовать</button></div>`,"mp_gal");}
function mpOne(id,ask){const z=mpS(),p=z.f.find(p=>p.id===id);if(!p)return mpGal();mpOneId=id;const pl=S.placed[id],rm=pl&&ROOMS.find(r=>r.id===pl.r);
  openPanel(MP_CAT,`<div class="mp-one"><img src="${mpImg(p)}" alt=""><h3 class="bh">«${p.t}»</h3><p class="lead">${mpDate(p.d)} · рама ${MP_FRN[p.fr]} · ${p.c.map(c=>(MP_INK.find(i=>i[0]===c)||[,c])[1].toLowerCase()).join(", ")}${rm?` · висит: ${rm.ru}`:""}</p></div>
   ${ask?`<p class="lead">Картина исчезнет из рамы и из комнаты, а рама освободится для новой.</p><div class="row"><button class="btn primary" data-x="mp:del:${id}">Да, снять</button><button class="btn" data-x="mp:p:${id}">Оставить</button></div>`
   :`<div class="row">${MP_FR.map(([k,n])=>`<button class="btn${p.fr===k?" primary":""}" data-x="mp:fr:${id}:${k}">${n}</button>`).join("")}</div><div class="row"><button class="btn" data-x="mp:gal">← Все картины</button><button class="btn" data-x="mp:ask:${id}">Снять картину</button></div>`}`,"mp_one");}
function mpDel(id){const z=mpS(),i=z.f.findIndex(p=>p.id===id);if(i<0)return;z.f.splice(i,1);S.owned.delete(id);delete S.placed[id];if(S.dpos)delete S.dpos[id];save();mpSync();ui();mpGal();}

hook("click",k=>{if(!k.startsWith("mp:"))return;const a=k.split(":");
  if(a[1]==="go")mpOpen();else if(a[1]==="gal")mpGal();else if(a[1]==="p")mpOne(a[2]);else if(a[1]==="ask")mpOne(a[2],1);else if(a[1]==="del")mpDel(a[2]);
  else if(a[1]==="fr"){const p=mpS().f.find(p=>p.id===a[2]);if(p&&MP_FRN[a[3]]){p.fr=a[3];save();mpSync();mpOne(p.id);}}return true;});
hook("hub",()=>{const z=mpS(),nx=MP_INK.find(x=>x[3]>z.n);
  return`<div class="hubc"><h4>🎨 Картины Муси <i>猫の絵</i></h4><p>Картин в рамках: ${z.f.length} из ${MP_MAX}</p>
  <p>${z.n?`Нарисовано картин: ${z.n}.`:"Муся окунает лапку в тушь и гуляет по бумаге — получается картина."}${nx?` Краска «${nx[1]}» откроется через ${mpPl(nx[3]-z.n,["картину","картины","картин"])}.`:" Открыты все шесть красок."}</p>
  <div class="row"><button class="btn primary" data-x="mp:go">Рисовать</button>${z.f.length?`<button class="btn" data-x="mp:gal">Галерея</button>`:""}</div></div>`;});
hook("tray",(tray,room)=>{
  if(room==="games"&&(S.trayMode[room]||"play")==="play"&&!tray.querySelector('[data-x="mp:go"]')){const b=`<button class="item wide" data-x="mp:go"><span class="ico">🎨</span><span class="nm">Муся рисует</span></button>`,row=tray.querySelector(".items");
    if(row)row.insertAdjacentHTML("afterbegin",b);else tray.querySelector(".glist")?.insertAdjacentHTML("beforebegin",`<div class="items">${b}</div>`);}
  const bs=tray.querySelectorAll('[data-item^="mp_"]');if(!bs.length)return;   // «🧺 Вещи» → «Картины Муси»: only framed paintings, each with its own picture
  for(const b of bs){const id=b.dataset.item,e=MPC[id];if(!S.owned.has(id)){b.remove();continue;}const sp=b.querySelector(".ath");if(sp&&e&&e.u)Object.assign(sp.style,{backgroundImage:`url(${e.u})`,backgroundPosition:"center",backgroundSize:"100% 100%"});}
  if(!tray.querySelector('[data-item^="mp_"]'))tray.querySelector(".items")?.insertAdjacentHTML("afterbegin",`<button class="item wide" data-x="mp:go"><span class="ico">🎨</span><span class="nm">Нарисовать картину</span></button>`);});
hook("album",el=>{const z=mpS();
  for(const h of [...el.querySelectorAll("h4.ch")])if(h.textContent===MP_CAT){const n=h.nextElementSibling;if(n&&n.classList.contains("coll"))n.remove();h.remove();}   // not twelve empty frames in «Коллекция вещей»
  if(!z.n)return;el.insertAdjacentHTML("beforeend",`<h3 class="bh">${MP_CAT}</h3><p class="lead">${mpLead()}</p>${z.f.length?`<div class="mp-gal">${z.f.map(p=>`<div class="mp-p"><img src="${mpImg(p)}" alt=""><small>«${p.t}»</small><i>${mpDate(p.d)}</i></div>`).join("")}</div>`:""}`);});
hook("itemTap",(it)=>{if(!/^mp_/.test(it.id))return;const p=mpS().f.find(p=>p.id===it.id);if(!p)return;toast(`🖼 «${p.t}»`);chime([784,988]);if(!petAway())react(pick(["😸","😻","😼"]),1.6);return true;});
hook("boot",mpSync);hook("sec",mpSync);
X.mp={S:mpS,open:mpOpen,gal:mpGal,one:mpOne,sync:mpSync,
  // tests: dip a saucer, walk a finger path (paper share 0..1; hold = the finger stays down), run the sheet's own clock (headless frames are rare)
  dip(i){mpDip(G.st,i);},drag(pts,hold){const q=G.st;q.drag=true;q.pend=0;q.auto=false;for(const [u,v] of pts)mpPush(q,u*MP_PW,v*MP_PH);if(!hold){q.drag=false;q.pend=1;}},
  ff(sec){for(let i=0;i<sec*60;i++)G.def.step(G,now(),1/60);},sit(){mpSit(G.st);},roll(){mpRoll(G.st);},auto(){mpAuto(G.st);},
  btn(id){const L=G.st.L,b=[...L.btns,...L.fb,...L.kb].find(b=>b.id===id);G.def.down(G,b.x+b.w/2,b.y+b.h/2,now());},q:()=>G.st};
}
