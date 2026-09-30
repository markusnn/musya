{
// ───────────────────────── «Гатяпон на ярмарке»: one free capsule a day, 18 figurines in three series ─────────────────────────
// S.ext.gacha = {day: dayKey of the last free capsule, extra: capsules from swapped duplicates, got: {figurineId: copies}}
const GC_R={fg_kappa:[342,0,120,146],fg_kitsune:[464,0,120,146],fg_tanuki:[586,0,120,146],fg_nekomata:[708,0,120,146],fg_akaname:[830,0,120,146],fg_chochin:[952,0,120,146],
  fg_karakasa:[1074,0,120,146],fg_oni:[1196,0,130,146],fg_rokuro:[0,562,120,146],fg_bettari:[122,562,120,146],fg_okubi:[244,562,120,146],fg_warashi:[366,562,120,146],
  fg_maneki:[488,562,120,146],fg_samurai:[610,562,120,146],fg_kimono:[732,562,120,146],fg_basket:[854,562,120,146],fg_kuro:[976,562,120,146],fg_gold:[1098,562,120,146],
  machine:[0,0,340,560],crank:[1220,562,120,120]};
// [id, name, series, secret, a line about it]
const GC_F=[
 ["fg_kappa","Каппа",1,0,"Речной дух с блюдцем воды на макушке. Огурец — его любимое лакомство."],
 ["fg_kitsune","Лиса-невеста",1,0,"Когда солнце светит сквозь дождь, у лис свадьба. Невеста — во всём белом."],
 ["fg_tanuki","Тануки",1,0,"Весельчак-оборотень в соломенной шляпе, с бутылочкой сакэ на удачу."],
 ["fg_nekomata","Нэкомата",1,0,"Старая кошка, у которой раздвоился хвост. По ночам пляшет с полотенцем на голове."],
 ["fg_akaname","Аканамэ",1,0,"Вылизывает грязные купальни. Лучше мыться почаще."],
 ["fg_chochin","Тётин-обакэ",1,0,"Старый фонарь прорезал глаз и высунул язык."],
 ["fg_karakasa","Каракаса",2,0,"Зонтик, которому исполнилось сто лет, ожил и скачет на одной ноге."],
 ["fg_oni","Óни с барабаном",2,0,"Гром — это óни бьёт в барабан. В грозу прячь пупок!"],
 ["fg_rokuro","Рокурокуби",2,0,"Днём обычная женщина, а ночью её шея тянется до самого потолка."],
 ["fg_bettari","Бэттари",2,0,"Нарядная дама без глаз и носа — только улыбка с чернёными зубами."],
 ["fg_okubi","Оокуби",2,0,"Огромная голова, что всплывает в тумане над крышами."],
 ["fg_warashi","Дзасики-вараси",2,1,"Девочка — дух старого дома. Пока она здесь, дому везёт."],
 ["fg_maneki","Манэки-нэко",3,0,"Манит лапкой удачу и гостей. В лапах — золотая монета."],
 ["fg_samurai","Кот-самурай",3,0,"Бесстрашный воин в шлеме с золотыми рогами."],
 ["fg_kimono","Кошка в кимоно",3,0,"Нарядилась на праздник и обмахивается веером."],
 ["fg_basket","Котёнок в корзинке",3,0,"Уснул в корзинке для овощей, да так там и остался."],
 ["fg_kuro","Чёрный кот на заборе",3,0,"В Японии чёрный кот — к счастью. Особенно если сидит на заборе."],
 ["fg_gold","Золотой кот",3,1,"Редчайшая фигурка. Говорят, приносит удачу на сто лет вперёд."]];
const GC_SER=[null,{n:"Ёкаи дома",jp:"家の妖怪",st:"gc_s1",col:"#4aa06a"},{n:"Ночной парад",jp:"百鬼夜行",st:"gc_s2",col:"#7a5ad0"},{n:"Кошки Японии",jp:"日本の猫",st:"gc_s3",col:"#e08a3a"}];
addItems(GC_F.map(([id,n])=>({id,n,c:"Фигурки гатяпона",w:GC_R[id][2],h:GC_R[id][3],a:"b",p:40,at:["fg",GC_R[id][0],GC_R[id][1]],src:"🎰 гатяпон",hint:"Выпадает из гатяпона на ярмарке"})),{fg:[1400,708]});
STAMPS.push(["gc_s1","怪","Ёкаи дома в сборе","Собери в гатяпоне всю серию «Ёкаи дома»"],["gc_s2","行","Ночной парад в сборе","Собери в гатяпоне всю серию «Ночной парад»"],["gc_s3","猫","Кошки Японии в сборе","Собери в гатяпоне всю серию «Кошки Японии»"]);
const gcS=()=>S.ext.gacha||(S.ext.gacha={day:null,extra:0,got:{}});
const gcFree=()=>gcS().day!==dayKey(),gcLeft=()=>(gcFree()?1:0)+gcS().extra,gcGot=id=>gcS().got[id]||0;
function gcDupes(){let n=0;for(const k in gcS().got)n+=Math.max(0,gcS().got[k]-1);return n;}
function gcTake(){const st=gcS();if(gcFree())st.day=dayKey();else st.extra=Math.max(0,st.extra-1);save();tabDots();hubDot();}
function gcRoll(){if(X.gc.force)return X.gc.force;const sec=GC_F.filter(f=>f[3]),nor=GC_F.filter(f=>!f[3]);return pick(Math.random()<.04?sec:nor)[0];}
function gcGive(id){const st=gcS();st.got[id]=(st.got[id]||0)+1;S.owned.add(id);disc("figure",id);
  for(let s=1;s<=3;s++)if(GC_F.filter(f=>f[2]===s).every(f=>gcGot(f[0])))award(GC_SER[s].st);save();}
function gcSwap(){const st=gcS();if(gcDupes()<3)return;for(let i=0;i<3;i++){const id=Object.keys(st.got).sort((a,b)=>st.got[b]-st.got[a])[0];st.got[id]--;}
  st.extra++;save();sfx("coin");chime([988,1318]);toast("♻ Три дубликата → новая капсула!");tabDots();hubDot();}
let GC_IM=null;function gcLoad(){if(!GC_IM)atlasImg("fg",im=>{GC_IM=im;});}
function gcBlit(g,key,x,y,w,rot=0,alpha=1){const r=GC_R[key];if(!GC_IM||!r)return;const k=w/r[2];g.save();g.globalAlpha=alpha;g.translate(x,y);if(rot)g.rotate(rot);g.drawImage(GC_IM,r[0],r[1],r[2],r[3],-w/2,-r[3]*k/2,w,r[3]*k);g.restore();}
function gcOpen(){if(gcLeft()<1){toast(gcDupes()>=3?"Обменяй 3 дубликата на капсулу в «家»":"Сегодня капсула уже была — приходи завтра");return;}gcLoad();openPlace("gc_gacha");}

// ── the machine at the fair: in front of the toy stall, with a warm glow and a twinkle while a capsule waits
const GC_X=1275,GC_Y=1140,GC_H=400;
function gcFrame(){const x=visX(GC_X,150),oc=curRow;curRow=GC_Y;const [bx,by]=imgToStage(x,GC_Y,CAT_D),[,ty]=imgToStage(x,GC_Y-100,CAT_D);curRow=oc;const k=(by-ty)/100*GC_H/548;return{bx,by,k,w:340*k,h:560*k};}
hook("draw",(t,front)=>{if(S.room!=="matsuri"||(GC_Y>catLineY()+6)!==front)return;gcLoad();if(!GC_IM)return;const F=gcFrame(),x0=F.bx-F.w/2,y0=F.by-548*F.k;
  const fl=.85+.08*Math.sin(t*5.3)+.05*Math.sin(t*11.7),gx=F.bx,gy=y0+130*F.k,R=330*F.k;
  ctx.save();ctx.globalCompositeOperation="lighter";let gr=ctx.createRadialGradient(gx,gy,0,gx,gy,R);gr.addColorStop(0,`rgba(255,196,120,${.26*fl})`);gr.addColorStop(1,"rgba(255,196,120,0)");ctx.fillStyle=gr;ctx.fillRect(gx-R,gy-R,R*2,R*2);ctx.restore();
  ctx.fillStyle="rgba(0,0,0,.35)";ctx.beginPath();ctx.ellipse(F.bx,F.by,F.w*.46,10*F.k*3,0,0,Math.PI*2);ctx.fill();
  const r=GC_R.machine;ctx.drawImage(GC_IM,r[0],r[1],r[2],r[3],x0,y0,F.w,F.h);
  gcBlit(ctx,"crank",x0+214*F.k,y0+440*F.k,120*F.k,Math.sin(t*.4)*.08);
  ctx.save();ctx.globalCompositeOperation="lighter";gr=ctx.createRadialGradient(gx,gy,0,gx,gy,140*F.k);gr.addColorStop(0,`rgba(255,230,190,${.12*fl})`);gr.addColorStop(1,"rgba(255,230,190,0)");ctx.fillStyle=gr;ctx.fillRect(gx-R,gy-R,R*2,R*2);ctx.restore();
  if(gcLeft()>0){const a=.55+.45*Math.sin(t*3);drawEmoji(ctx,"✨",F.bx+120*F.k,y0+10*F.k+Math.sin(t*1.7)*6*F.k,Math.max(12,40*F.k),a);}});
hook("hit",(x,y)=>{if(S.room!=="matsuri"||!GC_IM||scene.on)return;const F=gcFrame(),y0=F.by-548*F.k;if(Math.abs(x-F.bx)>F.w*.46||y<y0||y>F.by+6)return;audioInit();tone(880,.06,"triangle",.04);gcOpen();return true;});
hook("tray",(tray,room)=>{if(room!=="matsuri"||(S.trayMode[room]||"play")!=="play")return;const el=tray.querySelector(".items"),n=gcLeft();
  if(el)el.insertAdjacentHTML("afterbegin",`<button class="item wide" data-x="gc:open"><span class="ico">🎰</span><span class="nm">Гатяпон${n?" · "+n:""}</span></button>`);});
hook("click",k=>{if(!k.startsWith("gc:"))return;
  if(k==="gc:open")gcOpen();else if(k==="gc:swap"){gcSwap();if(panelIs("hub"))openHub();}
  else if(k==="gc:go"){closePanel();goRoom("matsuri");if(gcLeft()>0)setTimeout(gcOpen,500);}
  return true;});
hook("hubDot",()=>gcFree());
hook("tabDot",r=>r==="matsuri"&&gcFree());
hook("away",ms=>gcFree()&&ms>6*3600e3?{i:"🎰",t:"На ярмарке ждёт капсула гатяпона"}:null);
document.head.insertAdjacentHTML("beforeend",`<style>.gc-h{font-family:var(--display);font-size:16px;margin:12px 0 2px;display:flex;align-items:baseline;gap:8px;color:var(--paper)}.gc-h i{font-style:normal;font-family:var(--jp);font-size:12px;color:var(--sakura,#eea3bb)}.gc-h em{margin-left:auto;font-style:normal;font-size:13px;color:var(--muted)}
.gc-bar{height:5px;border-radius:3px;background:#0a0d0c;overflow:hidden;margin:2px 0 8px}.gc-bar i{display:block;height:100%}.gc-fig{display:flex;justify-content:center;margin:6px 0}.gc-rar{font-weight:700;color:var(--muted)}.gc-rar.sec{color:#e8c060}</style>`);
function gcColl(){return GC_SER.slice(1).map((s,i)=>{const L=GC_F.filter(f=>f[2]===i+1),n=L.filter(f=>gcGot(f[0])).length;
  return`<h4 class="gc-h">${s.n} <i>${s.jp}</i><em>${n} из 6${n===6?" ✓":""}</em></h4><div class="gc-bar"><i style="width:${(n/6*100).toFixed(1)}%;background:${s.col}"></i></div><div class="coll">${L.map(f=>{const c=gcGot(f[0]);
    return`<div class="ci ${c?"on":""}">${itemThumb(IT[f[0]],62,74)}<small>${c?f[1]+(c>1?` ×${c}`:""):f[3]?"??? ★":"???"}</small></div>`;}).join("")}</div>`;}).join("");}
hook("hub",()=>{const n=gcLeft(),d=gcDupes(),tot=GC_F.filter(f=>gcGot(f[0])).length;
  return`<div class="hubc"><h4>🎰 Гатяпон <i>ガチャ</i></h4><p>${gcFree()?"На ярмарке ждёт бесплатная капсула на сегодня!":"Сегодняшняя капсула уже открыта — завтра будет новая."}${gcS().extra?` Ещё капсул за обмен: ${gcS().extra}.`:""}</p>
  <p>Собрано фигурок: ${tot} из 18. Дубликаты: ${d}${d>=3?" — можно обменять три на капсулу.":" (три дубликата = одна капсула)."}</p>${gcColl()}
  <div class="row">${n?`<button class="btn primary" data-x="gc:go">🎰 К автомату</button>`:""}${d>=3?`<button class="btn" data-x="gc:swap">♻ Обмен дубликатов</button>`:""}</div></div>`;});
hook("album",el=>el.insertAdjacentHTML("beforeend",`<h3 class="bh">Гатяпон</h3><p class="lead">Капсульные фигурки с ярмарки: ${GC_F.filter(f=>gcGot(f[0])).length} из 18. В каждой серии есть секретная ★.</p>${gcColl()}`));
hook("boot",()=>{gcLoad();});

// ── the capsule moment: turn the crank (drag round or tap three times), a capsule drops, tap it — it pops open
function gcCapsule(g,x,y,r,col,rot,sep=0,al=1){g.save();g.globalAlpha=al;g.translate(x,y);g.rotate(rot);
  g.save();g.translate(0,sep);const gr=g.createRadialGradient(-r*.35,r*.1,r*.1,0,0,r*1.05);gr.addColorStop(0,"#fff3e0");gr.addColorStop(.25,col);gr.addColorStop(1,"#1a1010");g.fillStyle=gr;g.beginPath();g.arc(0,0,r,0,Math.PI);g.closePath();g.fill();g.restore();
  g.save();g.translate(0,-sep);g.fillStyle="rgba(215,228,236,.32)";g.strokeStyle="rgba(255,255,255,.55)";g.lineWidth=1.5;g.beginPath();g.arc(0,0,r,Math.PI,Math.PI*2);g.closePath();g.fill();g.stroke();
  g.fillStyle="rgba(255,255,255,.75)";g.beginPath();g.ellipse(-r*.38,-r*.55,r*.24,r*.09,-.55,0,Math.PI*2);g.fill();g.restore();
  g.fillStyle="rgba(0,0,0,.25)";g.fillRect(-r,-1+sep*0,r*2,2);g.restore();}
function gcLay(G){const W=G.W,H=G.H,mh=Math.min(H*.6,W*.95/340*560),k=mh/560,mx=W/2-170*k,my=H*.04;return{k,mx,my,hx:mx+214*k,hy:my+440*k,ox:mx+170*k,oy:my+506*k,fy:H*.83};}
const gcCol=id=>{const f=GC_F.find(q=>q[0]===id);return f[3]?"#e0b040":GC_SER[f[2]].col;};
GAMES.push({id:"gc_gacha",hidden:true,n:"Гатяпон",tag:"ガチャガチャ · Капсулы",icon:"🎰",bg:"fair",lives:null,time:null,lore:"",how:"",
 init(G,t){const q=G.st;Object.assign(q,{ph:gcLeft()>0?"crank":"empty",ang:0,goal:0,tick:0,drag:false,a0:0,fx:[],pick:null,t1:0});G.score=0;gcLoad();},
 step(G,t,dt){const q=G.st,L=gcLay(G);
   if(q.ph==="crank"){q.ang+=(q.goal-q.ang)*Math.min(1,dt*9);const n=Math.floor(q.ang/(Math.PI/4));if(n>q.tick){q.tick=n;tone(260+n*20,.05,"square",.035);}
     if(q.ang>=Math.PI*2-.06){q.ph="drop";q.t1=t;gcTake();q.pick=gcRoll();[0,.08,.16,.3].forEach((d,i)=>setTimeout(()=>tone(700-i*90,.06,"triangle",.04),d*1000));}}
   else if(q.ph==="drop"&&t-q.t1>1.05){q.ph="ready";q.t1=t;sfx("pop");}
   for(const f of q.fx){f.x+=f.vx*dt;f.y+=f.vy*dt;f.vy+=f.gr*dt;f.life-=dt;}q.fx=q.fx.filter(f=>f.life>0);
   if(q.ph==="open"&&t-q.t1>1.9&&!q.ended){q.ended=1;gEnd();}},
 draw(G,g,t){const q=G.st,L=gcLay(G),W=G.W,H=G.H,s=G.s,k=L.k;if(!GC_IM){textC(g,"…",W/2,H/2,20*s);return;}
   const r=GC_R.machine;g.save();g.fillStyle="rgba(0,0,0,.4)";g.beginPath();g.ellipse(W/2,L.my+552*k,160*k,18*k,0,0,Math.PI*2);g.fill();
   const gx=W/2,gy=L.my+130*k,gr=g.createRadialGradient(gx,gy,0,gx,gy,300*k);gr.addColorStop(0,"rgba(255,196,120,.22)");gr.addColorStop(1,"rgba(255,196,120,0)");g.fillStyle=gr;g.fillRect(0,0,W,H);
   g.drawImage(GC_IM,r[0],r[1],r[2],r[3],L.mx,L.my,340*k,560*k);gcBlit(g,"crank",L.hx,L.hy,120*k,q.ang);g.restore();
   if(q.ph==="empty"){textC(g,"Сегодняшняя капсула уже открыта",W/2,L.fy-14*s,15*s,"#f3ead8",700);textC(g,"Новая — завтра. Три дубликата = капсула",W/2,L.fy+12*s,13*s,"rgba(216,210,195,.8)",500);return;}
   if(q.ph==="crank"){const a=.6+.4*Math.sin(t*4);g.save();g.strokeStyle=`rgba(238,163,187,${a})`;g.lineWidth=3*s;g.beginPath();g.arc(L.hx,L.hy,78*k,-Math.PI/2+q.ang,-Math.PI/2+q.ang+Math.PI*1.5);g.stroke();g.restore();
     textC(g,"Поверни ручку ↻",W/2,L.fy,17*s,"#f3ead8",700);textC(g,"веди пальцем по кругу или нажми три раза",W/2,L.fy+22*s,12*s,"rgba(216,210,195,.75)",500);return;}
   const col=gcCol(q.pick),cr=Math.min(W,H)*.075;
   if(q.ph==="drop"||q.ph==="ready"){let x,y,rot;if(q.ph==="drop"){const u=clamp((t-q.t1)/1.05,0,1),b=u<.55?Math.pow(u/.55,2):1-Math.abs(Math.sin((u-.55)/.45*Math.PI*1.5))*.28*(1-u);x=mix(L.ox,W/2,u);y=mix(L.oy,L.fy,b);rot=u*5;}
     else{x=W/2;y=L.fy;rot=5+Math.sin((t-q.t1)*5)*.12*Math.exp(-(t-q.t1)*.3)+Math.sin(t*2)*.05;const a=.55+.45*Math.sin(t*4);textC(g,"Нажми на капсулу!",W/2,L.fy+cr+26*s,15*s,`rgba(243,234,216,${a})`,700);}
     g.fillStyle="rgba(0,0,0,.35)";g.beginPath();g.ellipse(x,L.fy+cr*.95,cr*.9,cr*.2,0,0,Math.PI*2);g.fill();gcCapsule(g,x,y,cr,col,rot);q.cx=x;q.cy=y;return;}
   // open: halves fly apart, rays, the figurine rises
   const e=t-q.t1,f=GC_F.find(z=>z[0]===q.pick),sec=!!f[3];
   g.save();g.fillStyle=`rgba(6,5,8,${.55*clamp(e/.4,0,1)})`;g.fillRect(0,0,W,H);
   const cx=W/2,cy=L.fy-cr*.2,rays=clamp(e/.5,0,1);g.globalCompositeOperation="lighter";g.translate(cx,cy-H*.12);g.rotate(t*.25);
   for(let i=0;i<14;i++){g.rotate(Math.PI*2/14);g.fillStyle=sec?`rgba(255,215,120,${.14*rays})`:`rgba(255,200,215,${.11*rays})`;g.beginPath();g.moveTo(0,0);g.lineTo(-H*.05,-H*.6);g.lineTo(H*.05,-H*.6);g.fill();}g.restore();
   const sep=cr*2.4*smooth(clamp(e/.45,0,1)),ha=clamp(1-(e-.3)/.6,0,1);if(ha>0){gcCapsule(g,cx-sep*.3,cy,cr,col,-sep/cr*.3,0,ha);}
   const u=clamp(e/.75,0,1),sz=Math.min(H*.36,W*.55)*easeOutBack(u),fr=GC_R[q.pick];
   if(sz>1){const w=sz*fr[2]/fr[3];gcBlit(g,q.pick,cx,cy-H*.12-sz*.05-(1-u)*H*.05,w);}
   if(e>.8){const a=clamp((e-.8)/.4,0,1);textC(g,f[1],cx,L.my+40*s,24*s,`rgba(243,234,216,${a})`,800);textC(g,(sec?"★ Секретная · ":"")+GC_SER[f[2]].n,cx,L.my+68*s,14*s,sec?`rgba(232,192,96,${a})`:`rgba(216,210,195,${a*.85})`,600);}
   for(const p of q.fx){g.fillStyle=`rgba(255,${p.c},200,${clamp(p.life,0,1)})`;g.beginPath();g.arc(p.x,p.y,p.r,0,Math.PI*2);g.fill();}},
 down(G,x,y,t){const q=G.st,L=gcLay(G);
   if(q.ph==="crank"){const d=Math.hypot(x-L.hx,y-L.hy);q.drag=d<110*L.k;q.a0=Math.atan2(y-L.hy,x-L.hx);q.dn=[x,y,t];q.mv=0;return;}
   if(q.ph==="ready"&&Math.hypot(x-q.cx,y-q.cy)<Math.min(G.W,G.H)*.16){q.ph="open";q.t1=t;sfx("pop");chime(GC_F.find(f=>f[0]===q.pick)[3]?[784,988,1318,1568,2093]:[988,1318,1568]);
     const cx=G.W/2,cy=gcLay(G).fy;for(let i=0;i<46;i++){const a=rand(0,Math.PI*2),v=rand(80,340)*G.s;q.fx.push({x:cx,y:cy,vx:Math.cos(a)*v,vy:Math.sin(a)*v-160*G.s,gr:260*G.s,r:rand(1.5,3.5)*G.s,c:180+(Math.random()*60|0),life:rand(.8,1.6)});}
     q.isNew=gcGot(q.pick)===0;gcGive(q.pick);}},
 move(G,x,y,held){const q=G.st;if(q.ph!=="crank"||!held||!q.drag)return;const L=gcLay(G),a=Math.atan2(y-L.hy,x-L.hx);let d=a-q.a0;d=((d+Math.PI*3)%(Math.PI*2))-Math.PI;q.a0=a;if(d>0){q.mv+=d;q.goal=Math.min(Math.PI*2,q.goal+Math.min(d,.6));}},
 up(G){const q=G.st;if(q.ph!=="crank"){q.drag=false;return;}const t=now();if(q.dn&&t-q.dn[2]<.4&&!(q.mv>.25))q.goal=Math.min(Math.PI*2,(Math.floor(q.goal/(Math.PI*2/3)+.01)+1)*Math.PI*2/3);q.drag=false;},
 stat:G=>`🎰 капсул: ${gcLeft()} · фигурок ${GC_F.filter(f=>gcGot(f[0])).length}/18`,
 card(G){const q=G.st,f=GC_F.find(z=>z[0]===q.pick)||GC_F[0],n=gcGot(f[0]),left=gcLeft(),ser=GC_SER[f[2]],have=GC_F.filter(z=>z[2]===f[2]&&gcGot(z[0])).length;
   return`<div class="card"><p class="tag">${ser.n} · ${ser.jp}</p><h3>${f[1]}</h3><div class="gc-fig">${itemThumb(IT[f[0]],130,150)}</div>
   <p class="gc-rar ${f[3]?"sec":""}">${f[3]?"★ Секретная фигурка":"Фигурка серии"} · ${q.isNew?"новая!":"повтор, у тебя их "+n}</p><p class="lore">${f[4]}</p>
   <p>Серия: ${have} из 6.${gcDupes()>=3?" Три дубликата можно обменять на капсулу в «家».":""} Фигурка ждёт во вкладке «🧺 Вещи».</p>
   <div class="row"><button class="btn" id="gHome">Готово</button><button class="btn primary" id="gAgain" style="${left?"":"display:none"}">Ещё капсула · ${left}</button></div></div>`;},
 after(){ui();}
});
X.gc={open:gcOpen,give:gcGive,swap:gcSwap,st:gcS,left:gcLeft,frame:gcFrame,force:null,
  turn(){if(G.id==="gc_gacha")G.st.goal=Math.PI*2;},crankTap(){if(G.id!=="gc_gacha")return;const L=gcLay(G);G.def.down(G,L.hx,L.hy,now());G.def.up(G);},tap(){if(G.id==="gc_gacha"&&G.st.ph==="ready")G.def.down(G,G.st.cx,G.st.cy,now());}};
}
