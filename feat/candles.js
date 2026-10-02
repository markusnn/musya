{
// ───────────────────────── «Сто свечей» (hyakumonogatari): every discovery in the game puts out one candle ─────────────────────────
// Sources: kaidan read, bestiary, fish, recipes, crops, guest friends, festivals, story chapters + every disc(kind,id) of the add-ons.
// The log keeps the order the candles went out; at 100 the last one burns blue and the player puts it out → Ao-andon comes.
const CD=S.ext.candles||(S.ext.candles={log:[],ms:0,fin:0});
const CD_ATL={cd_stand:[0,0,230,200],cd_rosoku:[234,0,150,200],cd_shokudai:[388,0,110,280],cd_hon:[502,0,200,150],cd_aoandon:[706,0,140,260]};
const CD_FL=[[44,127],[115,123],[186,127],[78,81],[152,81],[96,39],[134,39]];   // stand candles (sprite px), in the order they go out
const CD_CAT="Сто свечей",CD_SRC="🕯 сто свечей";
addItems([
 {id:"cd_rosoku",n:"Расписные свечи",c:CD_CAT,w:150,h:200,a:"b",p:0,glow:[94,40],at:["cd",234,0],src:CD_SRC,hint:"Погаси 25 из ста свечей (家 → Сто свечей)"},
 {id:"cd_shokudai",n:"Подсвечник сёкудай",c:CD_CAT,w:110,h:280,a:"b",p:0,glow:[69,36],at:["cd",388,0],src:CD_SRC,hint:"Погаси 50 из ста свечей (家 → Сто свечей)"},
 {id:"cd_hon",n:"Книги ста историй",c:CD_CAT,w:200,h:150,a:"b",p:0,at:["cd",502,0],src:CD_SRC,hint:"Погаси 75 из ста свечей (家 → Сто свечей)"},
 {id:"cd_aoandon",n:"Синий андон",c:CD_CAT,w:140,h:260,a:"b",p:0,at:["cd",706,0],src:CD_SRC,hint:"Погаси все сто свечей — и дождись духа"}
],{cd:[846,280]});
const CD_MS=[[25,"cd_rosoku"],[50,"cd_shokudai"],[75,"cd_hon"],[100,"cd_aoandon"]];
MON.m_cd_aoandon=[420,660];MON_BEAST.m_cd_aoandon="aoandon";
BESTIARY.push(["aoandon","m_cd_aoandon","Ао-андон","Дух синего фонаря. Приходит, когда в хякумоногатари гаснет сотая свеча: женщина в синем кимоно, с рожками и чернёными зубами. Нарисована Ториямой Сэкиэном в 1781 году."]);
STAMPS.push(["cd_half","燭","Полночь историй","Погаси 50 из ста свечей"],["cd_all","百","Сто историй","Погаси сотую свечу и встреть Ао-андон"]);
document.head.insertAdjacentHTML("beforeend",`<style>
.cd-cv{display:block;width:100%;aspect-ratio:4/3;border-radius:14px;background:#050607;margin:4px 0 10px;box-shadow:0 0 0 1px var(--line)}
.cd-count{display:flex;align-items:baseline;gap:4px 10px;flex-wrap:wrap;margin:0 0 10px}.cd-count b{font-family:var(--display);font-size:26px;color:var(--paper)}.cd-count span{font-size:13px;color:var(--muted);line-height:1.4}
.cd-go{width:100%;margin:0 0 12px}.cd-bar{height:4px;border-radius:2px;background:rgba(216,210,195,.1);overflow:hidden;margin:6px 0 4px}.cd-bar i{display:block;height:100%;background:linear-gradient(90deg,#e0a868,#8fb4ff)}
.cd-log{margin:0 0 16px;padding:0;list-style:none;display:grid;gap:5px}.cd-log li{font-size:13.5px;line-height:1.4;color:var(--paper);display:flex;gap:8px}.cd-log em{font-style:normal;color:#e0a868;min-width:2.1em;text-align:right;font-variant-numeric:tabular-nums}
.cd-src{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px}.cd-src span{font-size:12px;border:1px solid var(--line);border-radius:999px;padding:4px 9px;color:var(--paper);background:#0a0d0c}.cd-src em{font-style:normal;color:var(--muted);margin-left:4px}
</style>`);

// ── counting ──
const CD_KIND={find:"Находка Муси",rareguest:"Редкий гость",visitor:"Гость пришёл на вещи",rumor:"Слух подтвердился",chapter2:"Глава второй истории",dream:"Сон Муси",haunt:"Одержимая комната",postcard:"Открытка из путешествия",souvenir:"Сувенир из путешествия",room:"Открыта комната",figure:"Фигурка из гатяпона",bloom:"Цветение",trust:"Доверие Муси",
  ema:"Дар с доски эма",parade:"Ночной парад",forest:"Лес за тории",season:"Новое время года",birthday:"Праздник Муси",pet:"Котёнок подрос",
  star:"Звёздное небо",hanafuda:"Ханафуда",craft:"Поделка",crane:"Журавлики",bird:"Новая птица",koi:"Новый карп",serial:"Серия кайдана",ryokan:"Постоялец рёкана",kanji:"Иероглиф",
  friend:"Письмо друга",shop:"Лавка тануки",capsule:"Капсула времени",daruma:"Дарума исполнился",bonsai:"Бонсай",ikebana:"Икебана",tea:"Чайная церемония",shadow:"Теневой театр",paint:"Краски Муси"};
function cdAll(){const o=[];
  for(let k=0;k<Math.min(QS.ch,STORY.length);k++)o.push("q:"+k);
  for(const i of ST.stories)if(KAIDAN[i])o.push("k:"+i);
  for(const b of ST.seen)if(BESTIARY.some(x=>x[0]===b))o.push("b:"+b);
  for(const g of GUESTS)if((S.friends[g.id]||{}).n>0)o.push("g:"+g.id);
  for(const c of CROPS)if(S.crops[c.id])o.push("c:"+c.id);
  for(const f of FISHES)if(!f.junk&&S.catch[f.id])o.push("f:"+f.id);
  for(const r of RECIPES)if(S.cooked[r.id])o.push("r:"+r.id);
  const fd=new Set();for(const k in S.fest)if(S.fest[k]&&S.fest[k].done){const id=k.replace(/-\d+$/,"");if(FEST.some(F=>F.id===id))fd.add(id);}for(const id of fd)o.push("fe:"+id);
  const D=S.ext.disc||{},L=[];for(const kind in D)for(const id in D[kind])L.push([D[kind][id],"d:"+kind+":"+id]);L.sort((a,b)=>a[0]-b[0]);for(const x of L)o.push(x[1]);
  return o;}
function cdName(kind,id){if(kind==="trust"&&X.ts)return X.ts.name(id);const h=X[kind];if(h&&typeof h.name==="function"){try{const n=h.name(id);if(n)return n;}catch(e){}}
  return(IT[id]&&IT[id].n)||(FOOD[id]&&FOOD[id].n)||(BESTIARY.find(b=>b[0]===id)||[])[2]||(ROOMS.find(r=>r.id===id)||{}).ru||(GUESTS.find(g=>g.id===id)||{}).n||"";}
function cdLabel(key){const [s,a,b]=key.split(":");
  switch(s){case"q":return`Глава истории: «${(STORY[+a]||{}).title||"…"}»`;case"k":return`Прочитан кайдан «${(KAIDAN[+a]||{}).t||"…"}»`;
    case"b":return`Встречен ёкай: ${(BESTIARY.find(x=>x[0]===a)||[])[2]||a}`;case"g":return`Подружились с гостем: ${(GUESTS.find(x=>x.id===a)||{}).n||a}`;
    case"c":return`Первый урожай: ${(CROPS.find(x=>x.id===a)||{}).n||a}`;case"f":return`Поймана рыба: ${(FOOD[a]||{}).n||a}`;
    case"r":return`Приготовлено: ${(RECIPES.find(x=>x.id===a)||{}).n||a}`;case"fe":{const F=FEST.find(x=>x.id===a);return`Праздник: ${F?F.n:a}`;}
    case"d":{const n=cdName(a,b),k=CD_KIND[a]||"Новая находка";return n?`${k}: ${n}`:k;}}return key;}
const cdOut=()=>CD.fin?100:Math.min(99,CD.log.length),cdBlue=()=>CD.log.length>=100&&!CD.fin;
function cdPl(n,a,b,c){const d=n%10,h=n%100;return d===1&&h!==11?a:d>=2&&d<=4&&(h<12||h>14)?b:c;}
let cdPend=0,cdPendT=0,cdLastT=-9,cdGift=0,cdBooted=false;
function cdCheck(quiet){if(!cdBooted)return;const have=new Set(CD.log.map(e=>e[0]));let add=0;
  for(const k of cdAll()){if(CD.log.length>=100)break;if(have.has(k))continue;have.add(k);CD.log.push([k,quiet?0:Date.now()]);add++;}
  if(!add)return;if(!quiet){cdPend+=add;if(!cdPendT)cdPendT=now();}
  for(const [m,id] of CD_MS)if(m<100&&cdOut()>=m&&CD.ms<m){CD.ms=m;S.owned.add(id);if(m===50)award("cd_half");if(!quiet)cdGift=m;}
  save();if(panelIs("cd"))cdOpen(true);}
function cdToast(){const t=now();if(!cdPend||t-cdPendT<2.2||t-cdLastT<4||scene.on)return;cdLastT=t;
  const n=cdOut(),k=cdPend;cdPend=0;cdPendT=0;
  if(cdBlue()&&!CD.blueSaid){CD.blueSaid=1;toast("🕯 Сотая свеча вспыхнула синим…");chime([392,466,587]);return;}
  if(cdGift){toast(`🕯 ${n}/100 · подарок за ${cdGift} свечей → 🧺 Вещи`);cdGift=0;sfx("chime");return;}
  toast(k>1?`🕯 ${cdPl(k,"Погасла","Погасли","Погасли")} ещё ${k} ${cdPl(k,"свеча","свечи","свечей")}: ${n}/100`:`🕯 Погасла свеча: ${n}/100`);tone(880,.5,"sine",.03);}

// ── the stand in the bedroom corner: painted, the flames are live ──
const cdMk=(w,h,fn)=>{const c=document.createElement("canvas");c.width=w;c.height=h;fn(c.getContext("2d"));return c;};
function cdFlame(g,c){for(const [k,col] of [[1,c[0]],[.7,c[1]],[.4,c[2]]]){g.fillStyle=col;g.beginPath();g.moveTo(10,40-38*k);g.bezierCurveTo(10+9*k,40-20*k,10+7*k,38,10,39);g.bezierCurveTo(10-7*k,38,10-9*k,40-20*k,10,40-38*k);g.fill();}}
function cdGlow(g,r,gg,b){const q=g.createRadialGradient(32,32,0,32,32,32);q.addColorStop(0,`rgba(${r},${gg},${b},.85)`);q.addColorStop(.3,`rgba(${r},${gg},${b},.3)`);q.addColorStop(1,`rgba(${r},${gg},${b},0)`);g.fillStyle=q;g.fillRect(0,0,64,64);}
function cdBody(g,dark){const q=g.createLinearGradient(4,0,28,0),c=dark?["#37332d","#6a6356","#26231f"]:["#9a9080","#f4ecda","#7a7264"];q.addColorStop(0,c[0]);q.addColorStop(.4,c[1]);q.addColorStop(1,c[2]);
  g.fillStyle=dark?"#171210":"#2c2019";g.beginPath();g.ellipse(16,74,14,4.5,0,0,7);g.fill();
  g.fillStyle=q;g.beginPath();g.moveTo(4,9);g.lineTo(28,9);g.lineTo(25,73);g.lineTo(7,73);g.closePath();g.fill();
  g.fillStyle=dark?"#766f5f":"#fbf5e6";g.beginPath();g.ellipse(16,9,12,3.2,0,0,7);g.fill();
  g.fillStyle=dark?"rgba(118,111,95,.85)":"rgba(255,250,236,.9)";for(const [x,l] of [[9,14],[21,22],[14,8]])g.fillRect(x-1.5,9,3,l);
  g.strokeStyle="#1d130d";g.lineWidth=2;g.beginPath();g.moveTo(16,9);g.lineTo(16.5,3);g.stroke();}
const CDS={glow:cdMk(64,64,g=>cdGlow(g,255,170,90)),glowB:cdMk(64,64,g=>cdGlow(g,110,160,255)),flame:cdMk(20,40,g=>cdFlame(g,["#f0963c","#ffd678","#fffbe8"])),
  flameB:cdMk(20,40,g=>cdFlame(g,["#3f6dff","#9fc4ff","#eef6ff"])),body:cdMk(32,80,g=>cdBody(g,false)),bodyD:cdMk(32,80,g=>cdBody(g,true))};
atlasImg("cd",im=>{CDS.at=im;const r=CD_ATL.cd_stand;DIMG.cd_stand=cdMk(r[2],r[3],g=>g.drawImage(im,r[0],r[1],r[2],r[3],0,0,r[2],r[3]));DMETA.cd_stand=[r[2],r[3],"b"];});
ldImg("assets/bg/cd_tatami.webp",im=>{CDS.bg=im;});
const cdPos=()=>[visX(1548,135),1212];
function cdStandLit(){if(cdScene())return now()-scene.t0<1.3?[[6,1]]:[];if(CD.fin)return[];if(cdBlue())return[[6,1]];const k=Math.ceil((100-cdOut())/100*7);const o=[];for(let i=7-k;i<7;i++)o.push([i,0]);return o;}
function cdPt(g,im,x,y,w,h,a){g.globalAlpha=a;g.drawImage(im,x-w/2,y-h/2,w,h);g.globalAlpha=1;}
function cdDrawStand(t,front){
  if(S.room!=="bedroom"||!DIMG.cd_stand)return;const [x,y]=cdPos();if((y>catLineY()+6)!==front)return;
  const al=cdScene()?clamp(1-(now()-scene.t0-2.2)/1.2,0,1):1;if(al<=0)return;curD=CAT_D;curRow=y;drawSprite(ctx,"cd_stand",x,y,0,null,al);const k=BGM.k,dark=S.lampOff?1.5:1,lit=cdStandLit(),x0=x-115,y0=y-200;
  if(lit.length){const [cx,cy]=imgToStage(x,y-110),R=380*k,blue=lit[0][1],a=(blue?.16:.05+.1*lit.length/7)*dark,gr=ctx.createRadialGradient(cx,cy,0,cx,cy,R);
    gr.addColorStop(0,blue?`rgba(110,160,255,${a})`:`rgba(245,175,95,${a})`);gr.addColorStop(1,"rgba(0,0,0,0)");ctx.fillStyle=gr;ctx.fillRect(cx-R,cy-R,R*2,R*2);}
  ctx.save();ctx.globalCompositeOperation="lighter";
  for(const [i,blue] of lit){const [fx,fy]=imgToStage(x0+CD_FL[i][0],y0+CD_FL[i][1]),fl=1+.12*Math.sin(t*11+i*1.7)+.06*Math.sin(t*23+i),h=17*k*fl*(blue?1.2:1);
    cdPt(ctx,blue?CDS.glowB:CDS.glow,fx,fy-h*.4,90*k,90*k,.55*dark);ctx.drawImage(blue?CDS.flameB:CDS.flame,fx-h*.26+Math.sin(t*7+i)*.6,fy-h,h*.52,h*1.02);}
  ctx.restore();
  if(!lit.length&&(CD.fin||cdScene())){ctx.save();ctx.strokeStyle="rgba(190,196,210,.22)";ctx.lineWidth=1.2;for(let i=0;i<7;i+=3){const [fx,fy]=imgToStage(x0+CD_FL[i][0],y0+CD_FL[i][1]),u=(t*.2+i*.31)%1;ctx.globalAlpha=Math.sin(Math.PI*u);ctx.beginPath();ctx.moveTo(fx,fy);ctx.bezierCurveTo(fx+6*k*10*u,fy-20*k,fx-6*k*10*u,fy-40*k,fx+Math.sin(t+i)*8*k,fy-(30+50*u)*k);ctx.stroke();}ctx.restore();}
  curRow=null;}
function cdStandHit(x,y){if(S.room!=="bedroom"||!DIMG.cd_stand||hitCat(x,y))return false;const [ix,iy]=cdPos();curD=CAT_D;curRow=iy;const [ax,ay]=imgToStage(ix-120,iy-215),[bx,by]=imgToStage(ix+120,iy+10);curRow=null;return x>=ax&&x<=bx&&y>=ay&&y<=by;}
// the blue andon, once placed, lights its corner blue
function cdAndonGlow(t,front){const q=S.placed&&S.placed.cd_aoandon;if(!q||q.r!==S.room||!DMETA.cd_aoandon)return;const it=ipos({id:"cd_aoandon",x:q.x,y:q.y});if(isFront(it)!==front)return;
  curD=CAT_D;curRow=it.y;const [x0,y0,w,h]=spriteBox(it),[sx,sy]=imgToStage(x0+w/2,y0+h*.5),R=300*BGM.k,fl=.92+.06*Math.sin(t*3.1)+.03*Math.sin(t*9.7),gr=ctx.createRadialGradient(sx,sy,0,sx,sy,R);curRow=null;
  gr.addColorStop(0,`rgba(120,170,255,${.34*fl})`);gr.addColorStop(1,"rgba(120,170,255,0)");ctx.fillStyle=gr;ctx.fillRect(sx-R,sy-R,R*2,R*2);}

// ── the panel: a hundred candles in a spiral on a dark tatami around the blue andon ──
// projection shared with art/candles_art.py tatami(): x = 360 + X*560/Z, y = -300 + 560/Z (720×540 design units)
const CD_SP=(()=>{const L=[];let acc=0,p=null;for(let j=0;j<=3000;j++){const u=j/3000,r=1-.72*u,a=Math.PI/2+u*Math.PI*2*3.3,x=Math.cos(a)*r,y=Math.sin(a)*r;if(p)acc+=Math.hypot(x-p[0],y-p[1]);p=[x,y];L.push([acc,x,y]);}
  const out=[];let j=0;for(let i=0;i<100;i++){const want=acc*i/99;while(j<L.length-1&&L[j][0]<want)j++;const X=L[j][1]*.6,Z=.98+L[j][2]*.3;out.push({x:360+X*560/Z,y:-300+560/Z,s:.98/Z,Z});}return out;})();
const CD_ORDER=[...CD_SP.keys(),-1].sort((a,b)=>(b<0?.975:CD_SP[b].Z)-(a<0?.975:CD_SP[a].Z));
let cdRaf=0,cdAnim=null;
function cdFrame(){cdRaf=0;const cv=$("cdCv");if(!cv||!panelIs("cd"))return;cdRaf=requestAnimationFrame(cdFrame);
  const g=cv.getContext("2d"),t=now(),out=cdOut(),blue=cdBlue(),frac=out/100,sc=cv.width/720;g.setTransform(sc,0,0,sc,0,0);
  if(CDS.bg)g.drawImage(CDS.bg,0,0,720,540);else{g.fillStyle="#0b0a08";g.fillRect(0,0,720,540);}
  g.fillStyle=`rgba(3,4,10,${.06+.6*frac})`;g.fillRect(0,0,720,540);
  let lit=100-out;if(cdAnim)for(let i=cdAnim.from;i<cdAnim.to;i++)if(t<cdAnim.t0+(i-cdAnim.from)*.45)lit++;
  g.globalCompositeOperation="lighter";
  const pool=(x,y,r,col,a)=>{const q=g.createRadialGradient(x,y,0,x,y,r);q.addColorStop(0,`rgba(${col},${a})`);q.addColorStop(1,`rgba(${col},0)`);g.fillStyle=q;g.fillRect(x-r,y-r,r*2,r*2);};
  pool(360,310,420,"255,160,80",.3*lit/100*(1+.04*Math.sin(t*5)));pool(360,230,200+160*frac,"90,140,255",.05+.22*frac+(CD.fin?.1:0)+(blue?.08*Math.sin(t*2.2):0));
  g.globalCompositeOperation="source-over";
  for(const i of CD_ORDER){
    if(i<0){if(CDS.at){const r=CD_ATL.cd_aoandon,h=112,w=h*r[2]/r[3];g.drawImage(CDS.at,r[0],r[1],r[2],r[3],360-w/2,271-h,w,h);g.globalCompositeOperation="lighter";cdPt(g,CDS.glowB,360,215,170,170,.18+.5*frac);g.globalCompositeOperation="source-over";}continue;}
    const p=CD_SP[i],u=p.s,on=i>=out||(cdAnim&&i>=cdAnim.from&&i<cdAnim.to&&t<cdAnim.t0+(i-cdAnim.from)*.45),isB=i===99&&blue;
    g.drawImage(on?CDS.body:CDS.bodyD,p.x-7*u,p.y-35*u,14*u,35*u);const wx=p.x,wy=p.y-33.5*u;
    if(on){const fl=1+.13*Math.sin(t*(isB?6:11)+i*2.3)+.06*Math.sin(t*23+i),h=(isB?19:13)*u*fl;g.globalCompositeOperation="lighter";cdPt(g,isB?CDS.glowB:CDS.glow,wx,wy-h*.45,(isB?90:52)*u,(isB?90:52)*u,isB?.8:.55);g.globalCompositeOperation="source-over";
      g.drawImage(isB?CDS.flameB:CDS.flame,wx-h*.26+Math.sin(t*7+i)*.5*u,wy-h,h*.52,h*1.02);}
    else{const since=cdAnim&&i>=cdAnim.from&&i<cdAnim.to?t-(cdAnim.t0+(i-cdAnim.from)*.45):9,fresh=since<3,uu=fresh?since/3:(t*.16+i*.137)%1,al=fresh?.55*(1-uu):.13*Math.sin(Math.PI*uu);
      if(al>.01){g.strokeStyle=`rgba(200,204,214,${al})`;g.lineWidth=(fresh?1.6:1.1)*u;g.beginPath();g.moveTo(wx,wy);const hh=(fresh?40:28)*u*(.4+uu);g.bezierCurveTo(wx+6*u*Math.sin(t*1.3+i),wy-hh*.35,wx-6*u*Math.sin(t*1.1+i*2),wy-hh*.7,wx+3*u*Math.sin(t*.8+i),wy-hh);g.stroke();}}}
}
function cdHtml(){const out=cdOut(),blue=cdBlue(),fin=!!CD.fin,next=CD_MS.find(m=>m[0]>out);
  const st=fin?"Ао-андон приходила в эту спальню. Синий андон остался у тебя.":blue?"Сотая свеча горит синим. Погаси её — если не боишься.":next&&next[0]<100?`Осталось ${100-out}. До подарка — ${next[0]-out}.`:`Осталось ${100-out}.`;
  const log=CD.log.map((e,i)=>[e,i]).slice(0,fin?100:99).slice(-10).reverse();
  const n=(a,b)=>`<em>${a}${b!=null?"/"+b:""}</em>`,disc=Object.values(S.ext.disc||{}).reduce((a,k)=>a+Object.keys(k).length,0);
  const src=[["📜 Кайданы",ST.stories.length,KAIDAN.length],["👁 Ёкаи",ST.seen.filter(b=>BESTIARY.some(x=>x[0]===b)).length,BESTIARY.length],["🎣 Рыбы",FISHES.filter(f=>!f.junk&&S.catch[f.id]).length,FISHES.filter(f=>!f.junk).length],
    ["🍳 Рецепты",RECIPES.filter(r=>S.cooked[r.id]).length,RECIPES.length],["🌱 Урожай",CROPS.filter(c=>S.crops[c.id]).length,CROPS.length],["🦊 Гости",GUESTS.filter(g=>(S.friends[g.id]||{}).n>0).length,GUESTS.length],
    ["🎑 Праздники",cdAll().filter(k=>k.startsWith("fe:")).length,FEST.length],["📖 Главы истории",Math.min(QS.ch,STORY.length),STORY.length],["✨ Находки",disc,null]];
  return`<p class="lead">В эпоху Эдо рассказывали сто страшных историй и гасили по свече… Когда погаснет последняя, придёт настоящий дух.</p>
   <canvas class="cd-cv" id="cdCv"${blue?' data-x="cd:fin"':""}></canvas>
   <div class="cd-count"><b>Погашено ${out} из 100</b><span>${st}</span></div>
   ${blue?`<button class="btn primary cd-go" data-x="cd:fin">🕯 Погасить сотую свечу</button>`:""}
   <div class="coll">${CD_MS.map(([m,id])=>{const on=S.owned.has(id);return`<div class="ci ${on?"on":""}">${itemThumb(IT[id],64,52)}<small>${on?IT[id].n:"???"}<br>${m} свечей</small></div>`;}).join("")}</div>
   <h3 class="bh">Последние свечи</h3>${log.length?`<ol class="cd-log">${log.map(([e,i])=>`<li><em>${i+1}</em><span>${cdLabel(e[0])}</span></li>`).join("")}</ol>`:`<p class="lead">Пока ни одна свеча не погасла.</p>`}
   <h3 class="bh">Что гасит свечи</h3><p class="lead">Каждая новая находка — одна свеча.</p><div class="cd-src">${src.map(([a,b,c])=>`<span>${a}${n(b,c)}</span>`).join("")}</div>`;}
function cdOpen(keep){const was=CD.seen||0,out=cdOut();openPanel("Сто свечей",cdHtml(),"cd");
  if(!keep&&out>was&&out-was<=12)cdAnim={from:was,to:out,t0:now()+.8};else if(!keep)cdAnim=null;CD.seen=out;save();
  const cv=$("cdCv");if(cv){const w=cv.clientWidth||400,d=Math.min(2,devicePixelRatio||1);cv.width=Math.round(w*d);cv.height=Math.round(w*.75*d);}if(!cdRaf)cdRaf=requestAnimationFrame(cdFrame);}

// ── the finale: the hundredth candle, the blue lantern spirit ──
const CD_BOOK=[{title:"Сотая свеча",room:"bedroom",outro:{fx(){S.lampOff=true;pet.x=view.W*.27;pet.home=pet.x;paint();ui();setTimeout(()=>{if(scene.on&&scene.book===CD_BOOK&&snd.on&&snd.ctx){tone(98,3.5,"sine",.07);tone(147,3,"sine",.04);}},2600);setTimeout(()=>{if(scene.on&&scene.book===CD_BOOK)react("🙀",2.6);},3600);},
  chars:[{id:"m_cd_aoandon",x:()=>visX(1330,175),y:1228,h:450,d:.8,from:3}],p:[
  "Сотая свеча вспыхнула синим — и погасла. В спальне стало так темно, как бывает только в самой глубине ночи.",
  "В углу сам собой разгорелся бумажный андон. Свет у него был синий, как вода подо льдом.",
  "Рядом стояла женщина в синем кимоно. Длинные чёрные волосы, два маленьких рога — а когда она улыбнулась, зубы оказались чёрными, как у придворных дам старых времён.",
  "«Сто историй, — тихо сказала она. — Давно никто не досказывал до конца. Обычно убегают на девяносто девятой».",
  "Муся не убежала. Ао-андон наклонилась, коснулась её уха холодными пальцами — и растаяла вместе со светом. А синий андон остался. Он горит сам и совсем не греет."]}}];
const cdScene=()=>scene.on&&scene.book===CD_BOOK;
function cdFinale(){if(!cdBlue()||scene.on)return;closePanel();playScene(0,"outro",cdAfter,false,CD_BOOK);}
function cdAfter(){CD.fin=Date.now();CD.ms=100;S.owned.add("cd_aoandon");if(!ST.seen.includes("aoandon"))ST.seen.push("aoandon");
  if(!S.placed.cd_aoandon){S.placed.cd_aoandon={r:"bedroom",x:Math.round(visX(1330,175)-150),y:1236};loadItem("cd_aoandon");}
  award("cd_all");save();hubDot();setTimeout(()=>{toast("Синий андон остался в спальне · 🧺 Вещи");chime([587,698,880]);},2400);}
function cdOverlay(t){if(!cdScene())return;const e=t-scene.t0,a=clamp((e-3)/1.4,0,1),c=CD_BOOK[0].outro.chars[0],x=c.x(),[sx,sy]=imgToStage(x-94,c.y-90,.8),R=520*BGM.k,fl=.9+.07*Math.sin(t*3.3)+.03*Math.sin(t*11);
  ctx.fillStyle=`rgba(4,8,26,${.16-.06*a})`;ctx.fillRect(0,0,view.W,view.H);if(a<=0)return;ctx.save();ctx.globalCompositeOperation="lighter";const gr=ctx.createRadialGradient(sx,sy,0,sx,sy,R);
  gr.addColorStop(0,`rgba(110,160,255,${.5*a*fl})`);gr.addColorStop(.45,`rgba(70,110,220,${.2*a*fl})`);gr.addColorStop(1,"rgba(40,70,180,0)");ctx.fillStyle=gr;ctx.fillRect(sx-R,sy-R,R*2,R*2);ctx.restore();}

// ── hooks ──
hook("boot",()=>{cdBooted=true;setTimeout(()=>{cdCheck(true);if(CD.seen==null)CD.seen=cdOut();},0);});   // after every add-on's boot: what already exists goes in quietly
hook("sec",()=>{cdCheck(false);cdToast();});
hook("disc",()=>{setTimeout(()=>cdCheck(false),0);});
hook("draw",(t,front)=>{cdDrawStand(t,front);cdAndonGlow(t,front);});
hook("overlay",cdOverlay);
hook("hit",(x,y)=>{if(scene.on||!cdStandHit(x,y))return false;audioInit();sfx("pop");cdOpen();return true;});
hook("hubDot",()=>cdBlue());
hook("click",key=>{if(key==="cd:open"){cdOpen();return true;}if(key==="cd:fin"){cdFinale();return true;}});
hook("hub",()=>{const out=cdOut(),blue=cdBlue();
  return`<div class="hubc"><h4>🕯 Сто свечей <i>百物語</i></h4><p>${CD.fin?"Все сто свечей погасли. Ао-андон приходила — и оставила синий андон.":blue?"Девяносто девять свечей погасли. Сотая горит синим…":`Погашено ${out} из 100. Каждая новая находка гасит одну свечу — подставка стоит в углу спальни.`}</p>
   <div class="cd-bar"><i style="width:${out}%"></i></div><div class="row"><button class="btn${blue?" primary":""}" data-x="cd:open">${blue?"🕯 К сотой свече":"Посмотреть свечи"}</button></div></div>`;});
X.cd={n:()=>CD.log.length,out:cdOut,open:cdOpen,finale:cdFinale,check:cdCheck,st:CD,label:cdLabel,
  seed(n){const add=[()=>{for(let i=0;i<KAIDAN.length;i++)if(!ST.stories.includes(i)){ST.stories.push(i);return 1;}},()=>{for(const b of BESTIARY)if(b[0]!=="aoandon"&&!ST.seen.includes(b[0])){ST.seen.push(b[0]);return 1;}},
    ()=>{for(const f of FISHES)if(!f.junk&&!S.catch[f.id]){S.catch[f.id]=20;return 1;}},()=>{for(const r of RECIPES)if(!S.cooked[r.id]){S.cooked[r.id]=2;return 1;}},()=>{for(const c of CROPS)if(!S.crops[c.id]){S.crops[c.id]=2;return 1;}},
    ()=>{for(const g of GUESTS)if(!(S.friends[g.id]||{}).n){S.friends[g.id]={n:1};return 1;}},()=>{for(const F of FEST)if(!S.fest[F.id+"-2026"]){S.fest[F.id+"-2026"]={prog:[1,1,1],done:true};return 1;}},
    ()=>{for(const i of ITEMS)if(disc("find",i.id))return 1;}];let i=0,guard=0;while(cdAll().length<n&&guard++<600)add[i++%add.length]();cdCheck(false);}};
}
