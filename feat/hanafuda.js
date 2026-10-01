{
// ───────────────────────── «Ханафуда с тануки»: real koi-koi against yōkai, Musya watches from the side ─────────────────────────
// S.ext.hanafuda = {w:{opp:wins}, l:{opp:losses}, y:{yakuKey:times scored}, len:3|6, opp:last chosen, n:matches}
// card i = month*4+k (atlas_hfc: 7 per row, 100×156 + 2 px gaps, back = 48); HF_T[i]: h bright · t animal · r ribbon · k plain
const HF_CW=100,HF_CH=156,HF_T="hrkktrkkhrkktrkktrkktrkktrkkhtkktrkktrkkhtrkhkkk";
const HF_YK={goko:["Гоко","все пять светил"],siko:["Сико","четыре светила без Дождя"],amesiko:["Амэ-сико","четыре светила с Дождём"],sanko:["Санко","три светила без Дождя"],
  isc:["Ино-сика-тё","кабан, олень и бабочки"],aka:["Акатан","три красные ленты со стихами"],ao:["Аотан","три синие ленты"],tsuki:["Цукими-дзакэ","луна и чаша сакэ"],hana:["Ханами-дзакэ","занавес сакуры и чаша сакэ"],
  tan:["Тан","пять лент и больше"],tane:["Танэ","пять животных и больше"],kasu:["Касу","десять простых и больше"]};
const HF_LIGHT=new Set(["goko","siko","amesiko","sanko"]),HF_YC={goko:[0,8,28,40,44],siko:[0,8,28,44],amesiko:[0,8,28,40,44],sanko:[0,8,28,44],isc:[20,24,36],aka:[1,5,9],ao:[21,33,37],tsuki:[28,32],hana:[8,32]};
const HF_OPP=[
 {id:"tanuki",m:"m_tanuki",n:"Тануки",gen:"Тануки",ins:"Тануки",style:"greedy",dish:"ds_yakiimo",item:"hf_deck",about:"весёлый и жадный",
  L:{hi:"Пом-пом! Сыграем на данго? Я, чур, уже проголодался.",koi:["Кои-кои! Живот подсказывает — будет ещё!","Ещё, ещё! Тануки так просто не останавливается."],stop:"Хватит, хватит, а то данго остынут.",
   win:"Хо-хо! Листик на голове принёс удачу.",lose:"Ой… Это была карта-оборотень, не считается!",pkoi:"Смелая лапа! Посмотрим, посмотрим…",draw:"Колода кончилась, а живот — нет.",
   mwin:"Данго мои! …Ладно, шучу. Возьму только запах.",mlose:"Эх! Держи данго. А листик не отдам."}},
 {id:"kitsune",m:"m_kitsune",n:"Кицунэ",gen:"Кицунэ",ins:"Кицунэ",style:"koi",dish:"ds_inari",item:"hf_box",about:"хитрая, любит «кои-кои»",
  L:{hi:"Тише… Карты любят, когда с ними говорят шёпотом.",koi:["Кои-кои. Мне ведь всегда везёт… правда?","Ещё круг. Лисы не уходят рано."],stop:"Довольно. Я видела, какую карту ты прячешь.",
   win:"Хвост знает, где лежит луна.",lose:"Ах. Ты почти так же хитра, как лиса.",pkoi:"Кои-кои? Как смело. Как глупо. Как мило.",draw:"Ничья — это когда обе лисы остались голодными.",
   mwin:"Данго оставь себе. Я играла ради твоего лица.",mlose:"Ты выиграла честно. Это даже обидно."}},
 {id:"nekomata",m:"m_nekomata",n:"Нэкомата",gen:"Нэкомату",ins:"Нэкоматой",style:"safe",dish:"ds_yakizakana",item:"hf_mat",about:"осторожная, не рискует",
  L:{hi:"Мур. Только без спешки: у меня девять жизней, а у карт нет.",koi:["Кои-кои… нет, всё-таки… ладно, кои-кои."],stop:"Стоп. Синица в лапах лучше журавля на сосне.",
   win:"Мяу. Осторожность тоже умеет кусаться.",lose:"Шшш… Хвосты распушились, но я спокойна.",pkoi:"Рискуешь, сестрёнка? Хвостами чую беду.",draw:"Никто не поймал мышь. Бывает.",
   mwin:"Мур-р. Данго не нужно — почеши за ухом, и квиты.",mlose:"Ты играешь, как кошка ловит рыбу: тихо и наверняка."}},
 {id:"kappa",m:"m_kappa",n:"Каппа",gen:"Каппу",ins:"Каппой",style:"master",dish:"ds_asazuke",item:"hf_fan",about:"старый мастер с реки",
  L:{hi:"Кап-кап. Я играл в эту игру с самураями у реки.",koi:["Кои-кои. Вода в блюдце не дрожит — значит, можно."],stop:"Стоп. Река не течёт обратно.",
   win:"Так играли в Эдо. Учись, маленькая.",lose:"Хо… Блюдце на макушке чуть не пролилось.",pkoi:"Кои-кои — красивое слово. Опасное слово.",draw:"Колода пуста, как моя река в засуху.",
   mwin:"Не грусти. Огурчик — и сыграем снова.",mlose:"Ты достойна играть у реки. Возьми угощение."}}];
addItems([
 {id:"hf_deck",n:"Колода с листиком тануки",c:"Ханафуда",w:170,h:120,a:"b",p:80,at:["hf",0,0],src:"🎴 ханафуда",hint:"Обыграй Тануки в ханафуду 🎴"},
 {id:"hf_box",n:"Лаковая шкатулка для карт",c:"Ханафуда",w:170,h:130,a:"b",p:120,at:["hf",172,0],src:"🎴 ханафуда",hint:"Обыграй Кицунэ в ханафуду 🎴"},
 {id:"hf_mat",n:"Красная подушка для ханафуды",c:"Ханафуда",w:300,h:120,a:"b",p:120,at:["hf",344,0],src:"🎴 ханафуда",hint:"Обыграй Нэкомату в ханафуду 🎴"},
 {id:"hf_fan",n:"Веер с картой Ивы",c:"Ханафуда",w:220,h:140,a:"t",p:100,at:["hf",646,0],src:"🎴 ханафуда",hint:"Обыграй Каппу в ханафуду 🎴"},
 {id:"hf_scroll",n:"Свиток «Пять светил»",c:"Ханафуда",w:130,h:330,a:"t",p:150,at:["hf",868,0],src:"🎴 ханафуда",hint:"Выиграй раунд ханафуды со светилами 🎴"}],{hf:[1000,330]});
STAMPS.push(["hf_first","札","Первая партия","Обыграй Тануки в ханафуду"],["hf_goko","光","Пять светил","Собери в ханафуде Гоко — все пять светил"],["hf_all","花","Мастер ханафуды","Обыграй в ханафуду всех четырёх ёкаев"]);
document.head.insertAdjacentHTML("beforeend",`<style>
.hf-card{width:min(370px,calc(100% - 20px))!important;gap:10px!important;padding:18px 16px 14px!important}
.hf-opps{display:grid;grid-template-columns:1fr 1fr;gap:7px}
.hf-op{display:flex;flex-direction:column;align-items:center;gap:1px;padding:7px 5px 8px;border-radius:12px;border:1px solid var(--line);background:rgba(255,255,255,.03)}
.hf-op img{height:58px;object-fit:contain}.hf-op b{font-size:14px;color:var(--paper)}.hf-op small{font-size:11px;color:var(--muted);line-height:1.25}
.hf-op.on{border-color:var(--sakura);background:rgba(238,163,187,.13)}.hf-op:disabled{cursor:default}.hf-op:disabled img{filter:brightness(0) opacity(.45)}
.hf-len{display:flex;gap:6px}.hf-len button{flex:1;padding:8px 6px;border-radius:10px;border:1px solid var(--line);font-size:12.5px;color:var(--muted)}
.hf-len button[aria-pressed=true]{border-color:var(--sakura);color:var(--paper);background:rgba(238,163,187,.12)}
.hf-rules{text-align:left;font-size:12.5px;color:var(--muted);line-height:1.45}.hf-rules summary{cursor:pointer;color:var(--paper);font-weight:600;font-size:13.5px}
.hf-rules ul{margin:6px 0 4px;padding-left:16px}.hf-rules li{margin:1px 0}.hf-rules b{color:var(--paper)}
.hf-res{display:flex;align-items:center;gap:10px;text-align:left}.hf-res img{height:74px}.hf-res p{font-style:italic}
.hf-got{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;align-items:flex-end}.hf-got span{display:flex;flex-direction:column;align-items:center;gap:2px;font-size:11px;color:var(--muted)}
.hf-alb{display:flex;flex-wrap:wrap;gap:6px}.hf-alb span{padding:4px 9px;border-radius:999px;border:1px solid var(--line);font-size:12.5px;color:var(--muted)}.hf-alb span.on{color:var(--paper);border-color:rgba(238,163,187,.5)}
</style>`);
let HF_IM=null;
function hfLoad(){if(!HF_IM&&!hfLoad.q){hfLoad.q=1;ldImg("assets/items/atlas_hfc.webp",im=>{HF_IM=im;});}}
function hfS(){const Z=S.ext.hanafuda||(S.ext.hanafuda={w:{},l:{},y:{},len:3,opp:"tanuki",n:0});return Z;}
const hfUnl=i=>i===0||(hfS().w[HF_OPP[i-1].id]||0)>0,hfM=c=>c>>2,hfWins=()=>Object.values(hfS().w).reduce((a,v)=>a+v,0);

// ── rules: yaku, points
function hfYaku(cap){const h=new Set(cap),n=cap.filter(c=>HF_T[c]==="h").length,rain=h.has(40),Y=[],has=a=>a.every(x=>h.has(x));
  if(n===5)Y.push(["goko",10]);else if(n===4)Y.push(rain?["amesiko",7]:["siko",8]);else if(n===3&&!rain)Y.push(["sanko",5]);
  if(has([20,24,36]))Y.push(["isc",5]);if(has([1,5,9]))Y.push(["aka",5]);if(has([21,33,37]))Y.push(["ao",5]);
  if(has([28,32]))Y.push(["tsuki",5]);if(has([8,32]))Y.push(["hana",5]);
  const k=t=>cap.filter(x=>HF_T[x]===t).length,tn=k("r"),ta=k("t"),ka=k("k")+(h.has(32)?1:0);   // the sake cup is an animal and a plain card at once
  if(tn>=5)Y.push(["tan",tn-4]);if(ta>=5)Y.push(["tane",ta-4]);if(ka>=10)Y.push(["kasu",ka-9]);return Y;}
const hfPts=cap=>hfYaku(cap).reduce((a,y)=>a+y[1],0);
function hfVal(c){if(c===32)return 16;if(c===40)return 13;const t=HF_T[c];let v=t==="h"?20:t==="t"?6:t==="r"?5:1;if(c===20||c===24||c===36)v+=4;if([1,5,9,21,33,37].includes(c))v+=3;return v;}
function hfNear(cap){const h=new Set(cap),n=a=>a.filter(x=>h.has(x)).length;let r=0;   // yaku that miss one card
  if(n([0,8,28,44])>=2)r++;if(n([20,24,36])===2)r++;if(n([1,5,9])===2)r++;if(n([21,33,37])===2)r++;if(h.has(32)&&!h.has(28)&&!h.has(8))r++;
  if(cap.filter(x=>HF_T[x]==="r").length===4)r++;if(cap.filter(x=>HF_T[x]==="t").length===4)r++;return r;}

// ── table state: slots (column-major, 2 rows), hands, captures, deck
function hfDeal(q){
  for(let tries=0;tries<50;tries++){const d=[...Array(48).keys()];for(let i=47;i>0;i--){const j=Math.random()*(i+1)|0;[d[i],d[j]]=[d[j],d[i]];}
    q.hand=[d.slice(0,8).sort((a,b)=>a-b),d.slice(8,16)];q.ts=[...d.slice(16,24),null,null,null,null];q.deck=d.slice(24);
    const tm=Array(12).fill(0);for(const c of q.ts)if(c!=null)tm[hfM(c)]++;
    const four=hd=>{const m=Array(12).fill(0);for(const c of hd)m[hfM(c)]++;return m.some(v=>v===4);};
    if(!tm.some(v=>v===4)&&!four(q.hand[0])&&!four(q.hand[1]))break;}   // four of a month on the table or in a hand → deal again
  q.cap=[[],[]];q.yk=[0,0];q.koi=[0,0];q.turn=q.dealer;q.sel=-1;q.pc=null;q.dc=null;q.via={};q.res=null;q.P={};q.jobs=[];q.ph="busy";}
const hfTable=q=>q.ts.filter(c=>c!=null),hfMatch=(q,c)=>hfTable(q).filter(x=>hfM(x)===hfM(c));
function hfPut(q,c){let i=q.ts.indexOf(null);if(i<0){i=q.ts.length;for(let k=0;k<(q.R||2);k++)q.ts.push(null);}q.ts[i]=c;}
function hfTake(q,p,c,tgt,t){const ms=hfMatch(q,c);   // card c lands on the table for player p → captured cards
  if(!ms.length){hfPut(q,c);return[];}
  const tk=ms.length===3?ms:[ms.length===1?ms[0]:(ms.includes(tgt)?tgt:ms[0])],sl=q.ts.indexOf(tk[0]),got=[c,...tk];
  for(const x of tk)q.ts[q.ts.indexOf(x)]=null;q.cap[p].push(...got);
  if(t!=null)for(const x of got)q.via[x]={sl,until:t+.5};return got;}
function hfPlay(q,p,c,tgt,t){const i=q.hand[p].indexOf(c);if(i<0)return null;q.hand[p].splice(i,1);return hfTake(q,p,c,tgt,t);}

// ── the opponents' minds
function hfRisk(q,p,c){const seen=new Set([...q.hand[p],...hfTable(q),...q.cap[0],...q.cap[1]]),un=[0,1,2,3].map(k=>hfM(c)*4+k).filter(x=>!seen.has(x));
  return un.length?hfVal(c)+.3*un.reduce((a,x)=>a+hfVal(x),0):0;}
function hfGain(q,p,got,st){const cap=q.cap[p],op=q.cap[1-p];let g=got.reduce((a,x)=>a+hfVal(x),0)+15*(hfPts(cap.concat(got))-hfPts(cap))+3*(hfNear(cap.concat(got))-hfNear(cap));
  if(st==="master"||st==="koi")g+=(st==="master"?.8:.4)*(10*(hfPts(op.concat(got.slice(1)))-hfPts(op))+3*(hfNear(op.concat(got.slice(1)))-hfNear(op)));   // deny what the other side needs
  return g;}
function hfBest(q,p,c,ms,st){let b=ms[0],bv=-1e9;for(const m of ms){const v=hfGain(q,p,[c,m],st);if(v>bv){bv=v;b=m;}}return b;}
function hfAiPick(q,p){const st=HF_OPP[q.oi].style;let best=null;
  for(const c of q.hand[p]){const ms=hfMatch(q,c);let v,tgt=null;
    if(!ms.length)v=-hfRisk(q,p,c)*(st==="safe"?1.6:st==="master"?1.1:.5);
    else if(ms.length===3)v=hfGain(q,p,[c,...ms],st)+4;
    else{tgt=hfBest(q,p,c,ms,st);v=hfGain(q,p,[c,tgt],st)+4;}
    if(st==="greedy")v+=Math.random()*5-2.5;else if(st==="koi")v+=Math.random()*2-1;
    if(!best||v>best.v)best={c,tgt,v};}
  return best;}
function hfAiKoi(q,p){const st=HF_OPP[q.oi].style,left=q.hand[p].length,pts=q.yk[p],op=q.cap[1-p];
  if(st==="safe")return false;if(st==="greedy")return left>=3&&pts<7&&Math.random()<.55;if(st==="koi")return left>=2&&pts<10&&Math.random()<.85;
  return left>=4&&pts<6&&hfPts(op)===0&&hfNear(op)<2;}
// AI vs AI, no timers: checks the rules engine (X.hf.sim)
function hfSimRound(q){let p=q.turn;
  for(let n=0;n<40;n++){const a=hfAiPick(q,p);hfPlay(q,p,a.c,a.tgt);const d=q.deck.pop(),ms=hfMatch(q,d);hfTake(q,p,d,ms.length===2?hfBest(q,p,d,ms,"greedy"):null);
    const pts=hfPts(q.cap[p]);if(pts>q.yk[p]){q.yk[p]=pts;if(!q.hand[p].length||!hfAiKoi(q,p))return p;q.koi[p]++;}
    if(!q.hand[0].length&&!q.hand[1].length)return-1;p=1-p;}return-2;}

// ── layout (portrait first; on wide screens a centred column)
function hfLayout(G){const q=G.st,W=G.W,H=G.H,wide=W>H*1.1,cw=Math.min(W,wide?780:560),x0=(W-cw)/2,pad=8,s=clamp(cw/480,.82,1.15),gap=Math.round(6*s),L={W,H,x0,cw,pad,s,gap};
  L.opY=6;L.opH=Math.round(56*s);L.cs=Math.round(29*s);L.chs=Math.round(L.cs*1.56);L.ow=Math.round(20*s);L.musW=Math.round(96*s);
  L.HC=wide?8:4;L.HR=wide?1:2;   // the hand: one row of 8 on wide screens, two rows of 4 on phones
  L.hw=Math.floor(Math.min(92*s,(cw-2*pad-(L.HC-1)*gap-L.musW)/L.HC));L.hh=Math.round(L.hw*1.56);
  const fixed=L.opY+L.opH+6+L.chs+32+14+L.chs+26+10+gap+L.HR*L.hh+(L.HR-1)*gap+20*s;   // everything but the table
  for(const R of H>W*1.5?[3,2]:[2]){const C=R===3?4:6,tw=Math.floor(Math.min((cw-2*pad-(C+1)*gap-gap)/(C+1),(H-fixed-(R-1)*gap)/R/1.56));
    L.R=R;L.C=C;L.tw=tw;if(R===2||tw>=54)break;}
  L.th=Math.round(L.tw*1.56);L.tH=L.R*L.th+(L.R-1)*gap;
  const e=Math.max(0,H-fixed-L.tH)/5;
  L.ocY=L.opY+L.opH+4;L.msgY=L.ocY+L.chs+15+e*.4;L.tbY=L.msgY+17+e*.6;L.pcY=L.tbY+L.tH+14+e*1.2;L.pyY=L.pcY+L.chs+13;
  L.hY=H-10-(L.HR*L.hh+(L.HR-1)*gap);L.dkx=x0+pad;L.dky=L.tbY+L.tH/2-L.th/2;
  L.mx=x0+cw-pad-L.musW/2+4;L.my=H-8;L.msc=L.musW/192*1.08;
  q.L=L;q.R=L.R;hfBg(G);}
function hfSlot(L,q,i){const R=L.R,cols=Math.max(L.C,Math.ceil(q.ts.length/R)),x1=L.x0+L.pad+L.tw+L.gap*2,w=Math.min(L.tw,(L.x0+L.cw-L.pad-x1-(cols-1)*L.gap)/cols);
  return{x:x1+Math.floor(i/R)*(w+L.gap),y:L.tbY+(i%R)*(w*1.56+L.gap),w};}
function hfHandR(L,i){return{x:L.x0+L.pad+(i%L.HC)*(L.hw+L.gap),y:L.hY+Math.floor(i/L.HC)*(L.hh+L.gap),w:L.hw};}
function hfCapR(L,q,p){   // captured cards in 4 groups: lights, animals, ribbons, plain
  const y=p?L.ocY:L.pcY,R={},span=L.cw-2*L.pad-(p?0:0),parts=[.19,.26,.25,.3];let x=L.x0+L.pad;
  "htrk".split("").forEach((t,gi)=>{const cs=q.cap[p].filter(c=>HF_T[c]===t),gw=span*parts[gi]-L.gap,st=cs.length>1?Math.min(L.cs*.62,(gw-L.cs)/(cs.length-1)):0;
    cs.forEach((c,i)=>{R[c]={x:x+i*st,y,w:L.cs};});R["g"+t]={x,y,w:gw,n:cs.length};x+=span*parts[gi];});return R;}
function hfBg(G){const q=G.st,L=q.L,d=Math.min(2,devicePixelRatio||1),c=document.createElement("canvas");c.width=G.W*d;c.height=G.H*d;const g=c.getContext("2d");g.setTransform(d,0,0,d,0,0);
  if(G.bgc)g.drawImage(G.bgc,0,0,G.W,G.H);g.fillStyle="rgba(8,6,5,.45)";g.fillRect(0,0,G.W,G.H);
  // a red play cushion under the table cards, a warm andon glow from above
  const x=L.x0+4,y=L.tbY-10,w=L.cw-8,h=L.tH+20,gr=g.createLinearGradient(0,y,0,y+h);gr.addColorStop(0,"#6e1c16");gr.addColorStop(1,"#4a110d");
  g.fillStyle="rgba(0,0,0,.45)";g.beginPath();g.roundRect(x+3,y+5,w,h,14);g.fill();g.fillStyle=gr;g.beginPath();g.roundRect(x,y,w,h,14);g.fill();
  const r=rng(31);for(let i=0;i<260;i++){g.fillStyle=`rgba(${r()<.5?0:255},${r()<.5?0:200},${r()<.5?0:180},.05)`;g.fillRect(x+r()*w,y+r()*h,1+r()*2,1);}
  g.strokeStyle="rgba(216,176,72,.35)";g.lineWidth=1.2;g.beginPath();g.roundRect(x+4,y+4,w-8,h-8,11);g.stroke();
  for(const [a,b] of [[x,y],[x+w,y],[x,y+h],[x+w,y+h]]){g.fillStyle="#c9a24a";g.beginPath();g.arc(a,b,3.5,0,Math.PI*2);g.fill();}
  const lg=g.createRadialGradient(G.W*.5,-40,10,G.W*.5,-40,G.H*.75);lg.addColorStop(0,"rgba(255,200,130,.16)");lg.addColorStop(1,"rgba(255,200,130,0)");g.fillStyle=lg;g.fillRect(0,0,G.W,G.H);
  q.bg=c;}

// ── drawing helpers
function hfCard(g,c,x,y,w,face,hl,t){const h=w*1.56,i=face?c:48;
  g.fillStyle="rgba(0,0,0,.38)";g.beginPath();g.roundRect(x+1.5,y+2.5,w,h,w*.07);g.fill();
  if(HF_IM)g.drawImage(HF_IM,(i%7)*(HF_CW+2),(i/7|0)*(HF_CH+2),HF_CW,HF_CH,x,y,w,h);else{g.fillStyle=face?"#e8dcc0":"#2a120e";g.beginPath();g.roundRect(x,y,w,h,w*.07);g.fill();}
  if(face&&w>=40){const r=w*.12,bx=x+w-r-w*.06,by=y+h-r-w*.06;g.fillStyle="rgba(18,12,10,.78)";g.beginPath();g.arc(bx,by,r,0,Math.PI*2);g.fill();textC(g,String(hfM(c)+1),bx,by+.5,r*1.25,"#f2e8d2",700);}
  if(hl){g.save();g.strokeStyle=hl===2?"#f2c86a":`rgba(238,163,187,${.75+.25*Math.sin(t*6)})`;g.lineWidth=hl===2?2:3;g.shadowColor=hl===2?"#f2c86a":"#eea3bb";g.shadowBlur=10;g.beginPath();g.roundRect(x-1.5,y-1.5,w+3,h+3,w*.08);g.stroke();g.restore();}}
function hfBox(g,x,y,w,h,a=.9){g.fillStyle=`rgba(14,11,10,${a})`;g.strokeStyle="rgba(216,210,195,.25)";g.lineWidth=1;g.beginPath();g.roundRect(x,y,w,h,14);g.fill();g.stroke();}
function hfTextL(g,txt,x,y,size,col,wt=600,al="left"){g.save();g.font=`${wt} ${size}px ${getComputedStyle(document.body).fontFamily}`;g.textAlign=al;g.textBaseline="middle";g.fillStyle=col;g.fillText(txt,x,y);g.restore();}
function hfWrap(g,txt,maxW,size){g.save();g.font=`600 ${size}px ${getComputedStyle(document.body).fontFamily}`;const out=[];let cur="";for(const w of txt.split(" ")){const n=cur?cur+" "+w:w;if(g.measureText(n).width>maxW&&cur){out.push(cur);cur=w;}else cur=n;}if(cur)out.push(cur);g.restore();return out;}
function hfOpp(q){return HF_OPP[q.oi];}
function hfSay(q,txt){q.say={txt,t:now()};}
function hfMus(q,e,st,dur=1.8){q.mb={e,t:now()};if(st)q.ma={st,until:now()+dur};}
const hfLater=(q,dt,fn)=>{q.jobs.push([now()+dt,fn]);q.jobs.sort((a,b)=>a[0]-b[0]);};
const hfSlap=()=>{tone(170,.07,"triangle",.09);tone(900,.03,"square",.012);},hfFlip=()=>{tone(520,.05,"triangle",.04);tone(260,.06,"sine",.03);};

// ── turn flow (timed): play → draw → check yaku → koi-koi/stop → next
function hfStartRound(G){const q=G.st;hfDeal(q);hfSlap();q.ph="busy";
  hfLater(q,1.1,()=>{if(q.turn===0){q.ph="play";}else hfLater(q,.6,()=>hfAiTurn(G));});}
function hfHuman(G,c,tgt){const q=G.st,ms=hfMatch(q,c);if(ms.length===2&&tgt==null){q.ph="pick";q.pc=c;q.sel=c;return;}
  const got=hfPlay(q,0,c,tgt,now());q.sel=-1;q.pc=null;q.ph="busy";got.length?sfx("pop"):hfSlap();
  if(got.some(x=>HF_T[x]==="h"))hfMus(q,"😻","purr");hfLater(q,.6,()=>hfDrawPhase(G,0));}
function hfAiTurn(G){const q=G.st;if(!q.hand[1].length){hfNext(G,1);return;}const a=hfAiPick(q,1),got=hfPlay(q,1,a.c,a.tgt,now());got.length?sfx("pop"):hfSlap();
  if(got.some(x=>HF_T[x]==="h"))hfMus(q,"🙀");hfLater(q,.65,()=>hfDrawPhase(G,1));}
function hfDrawPhase(G,p){const q=G.st;if(!q.deck.length){hfCheck(G,p);return;}q.dc=q.deck.pop();hfFlip();
  hfLater(q,.8,()=>{const ms=hfMatch(q,q.dc);if(ms.length===2&&p===0){q.ph="dpick";return;}
    hfDrawTake(G,p,ms.length===2?hfBest(q,1,q.dc,ms,hfOpp(q).style):null);});}
function hfDrawTake(G,p,tgt){const q=G.st,got=hfTake(q,p,q.dc,tgt,now());q.dc=null;q.ph="busy";got.length?sfx("pop"):hfSlap();
  if(p===0&&got.some(x=>HF_T[x]==="h"))hfMus(q,"😻","purr");hfLater(q,.6,()=>hfCheck(G,p));}
function hfCheck(G,p){const q=G.st,pts=hfPts(q.cap[p]);
  if(pts<=q.yk[p]){hfNext(G,p);return;}
  q.yk[p]=pts;q.ykT=now();chime([523,659,784,1047]);
  if(p===0){hfMus(q,"😸","highfive",1.6);if(!q.hand[0].length){q.ph="busy";hfLater(q,1.3,()=>hfEndRound(G,0));return;}q.ph="koi";return;}
  hfMus(q,"🙀",null);q.ph="busy";
  if(q.hand[1].length&&hfAiKoi(q,1)){q.koi[1]++;hfSay(q,pick(hfOpp(q).L.koi));q.flash={t:now(),who:1};hfLater(q,1.9,()=>hfNext(G,1));}
  else{hfSay(q,hfOpp(q).L.stop);hfLater(q,1.6,()=>hfEndRound(G,1));}}
function hfNext(G,p){const q=G.st;if(!q.hand[0].length&&!q.hand[1].length){hfEndRound(G,-1);return;}
  q.turn=1-p;if(q.turn===0)q.ph="play";else{q.ph="busy";hfLater(q,.85,()=>hfAiTurn(G));}}
function hfKoi(G,go){const q=G.st;if(q.ph!=="koi")return;
  if(go){q.koi[0]++;q.flash={t:now(),who:0};chime([784,988,1175]);hfMus(q,"😼","play",1.4);hfSay(q,hfOpp(q).L.pkoi);q.ph="busy";hfLater(q,1.1,()=>hfNext(G,0));}
  else hfEndRound(G,0);}
function hfEndRound(G,w){const q=G.st,o=hfOpp(q),Z=hfS();let pts=0,mult=1;
  if(w>=0){pts=q.yk[w];if(pts>=7)mult*=2;if(q.koi[1-w])mult*=2;q.tot[w]+=pts*mult;q.dealer=w;}
  q.res={w,yaku:w>=0?hfYaku(q.cap[w]):[],pts,mult,items:[]};
  if(w===0){for(const [k] of q.res.yaku){Z.y[k]=(Z.y[k]||0)+1;disc("hanafuda","y_"+k);}
    if(q.res.yaku.some(y=>y[0]==="goko"))award("hf_goko");
    if(q.res.yaku.some(y=>HF_LIGHT.has(y[0]))&&!S.owned.has("hf_scroll")){S.owned.add("hf_scroll");q.res.items.push("hf_scroll");q.got.push("hf_scroll");}
    hfSay(q,o.L.lose);hfMus(q,"😸","highfive",2);chime([659,784,988,1319]);}
  else if(w===1){hfSay(q,o.L.win);hfMus(q,"😿","sulk",2.2);tone(220,.4,"sine",.05);}
  else{hfSay(q,o.L.draw);hfMus(q,"😶",null);}
  q.ph="round";save();}
function hfNextRound(G){const q=G.st;if(q.ri+1>=q.rounds){hfFinish(G);return;}q.ri++;hfStartRound(G);}
function hfFinish(G){const q=G.st,o=hfOpp(q),Z=hfS(),r=Math.sign(q.tot[0]-q.tot[1]);Z.n=(Z.n||0)+1;q.out={r,unl:null,first:false};
  if(r>0){q.out.first=!Z.w[o.id];Z.w[o.id]=(Z.w[o.id]||0)+1;give("ds_dango",2);give(o.dish,1);
    if(q.out.first){disc("hanafuda",o.id);if(!S.owned.has(o.item)){S.owned.add(o.item);q.got.push(o.item);}const i=HF_OPP.indexOf(o);if(HF_OPP[i+1])q.out.unl=HF_OPP[i+1];}
    award("hf_first");if(HF_OPP.every(x=>Z.w[x.id]))award("hf_all");}
  else if(r<0)Z.l[o.id]=(Z.l[o.id]||0)+1;
  G.score=q.tot[0];save();gEnd();}

// ── the game
const HF={id:"hf_koikoi",fair:false,n:"Ханафуда",tag:"花札 · Кои-кои с ёкаями",bg:"tatami",lives:null,time:null,icon:"🎴",
 lore:"Ханафуда — «цветочные карты»: двенадцать месяцев, по четыре карты в каждом. В эпоху Эдо в них играли на деньги, а ёкаи до сих пор играют на угощение.",
 how:"Забирай со стола карты того же месяца и собирай комбинации.",
 init(G,t){hfLoad();const Z=hfS(),oi=Math.max(0,HF_OPP.findIndex(o=>o.id===Z.opp));
   Object.assign(G.st,{oi:hfUnl(oi)?oi:0,rounds:Z.len===6?6:3,ri:0,tot:[0,0],dealer:0,got:[],say:null,mb:null,ma:null,flash:null,btns:[],L:null});
   hfLayout(G);hfStartRound(G);hfSay(G.st,hfOpp(G.st).L.hi);},
 step(G,t,dt){const q=G.st;if(!q.L||q.L.W!==G.W||q.L.H!==G.H)hfLayout(G);
   let n=0;while(q.jobs.length&&q.jobs[0][0]<=t&&n++<4){const j=q.jobs.shift();j[1]();}
   const L=q.L,T={},k=1-Math.exp(-dt*13);
   q.ts.forEach((c,i)=>{if(c!=null){const r=hfSlot(L,q,i);T[c]={x:r.x,y:r.y,w:r.w,f:1,z:1};}});
   for(const p of [0,1]){const R=hfCapR(L,q,p);for(const c of q.cap[p]){const v=q.via[c];if(v&&v.until>t){const r=hfSlot(L,q,v.sl);T[c]={x:r.x+(HF_T[c]==="h"?0:4),y:r.y+5,w:r.w,f:1,z:5};}else T[c]={...R[c],f:1,z:2};}}
   q.hand[0].forEach((c,i)=>{const r=hfHandR(L,i);T[c]={x:r.x,y:r.y-(q.sel===c?Math.round(16*L.s):0),w:r.w,f:1,z:q.sel===c?4:3};});
   const oh=q.hand[1].length,ost=Math.min(L.ow*.7,(L.cw*.42)/Math.max(1,oh));q.hand[1].forEach((c,i)=>{T[c]={x:L.x0+L.cw-L.pad-L.ow-(oh-1-i)*ost,y:L.opY+6,w:L.ow,f:0,z:1};});
   if(q.dc!=null)T[q.dc]={x:L.dkx+L.tw*.45,y:L.dky-L.tw*.3,w:L.tw*1.3,f:1,z:6};
   for(const c in T){const a=T[c];let P=q.P[c];if(!P)P=q.P[c]={x:L.dkx,y:L.dky,w:L.tw};P.x+=(a.x-P.x)*k;P.y+=(a.y-P.y)*k;P.w+=(a.w-P.w)*k;P.f=a.f;P.z=a.z;P.on=1;P.mv=Math.abs(a.x-P.x)+Math.abs(a.y-P.y)>3;}
   for(const c in q.P)if(!T[c])delete q.P[c];
   q.T=T;},
 draw(G,g,t){const q=G.st,L=q.L;if(!L||!q.T)return;const o=hfOpp(q),W=G.W;
   g.drawImage(q.bg,0,0,W,G.H);
   // opponent: portrait, name, score, koi-koi marks
   const im=MIMG[o.m],m=MON[o.m];if(im&&m){const h=L.opH+6,w=h*m[0]/m[1],bob=q.turn===1&&q.ph==="busy"?Math.abs(Math.sin(t*5))*3:0;g.drawImage(im,L.x0+L.pad-4,L.opY-2-bob,w,h);}
   const nx=L.x0+L.pad+L.opH*.8+6;hfTextL(g,o.n,nx,L.opY+14*L.s,16*L.s,"#f2e8d2",700);
   hfTextL(g,`очки ${q.tot[1]}`+(q.yk[1]?` · яку ${q.yk[1]}`:"")+(q.koi[1]?` · こいこい×${q.koi[1]}`:""),nx,L.opY+34*L.s,12*L.s,q.koi[1]?"#eea3bb":"#b9b2a2",600);
   // deck
   if(q.deck.length){for(let i=Math.min(3,Math.ceil(q.deck.length/8));i>=0;i--)hfCard(g,48,L.dkx+i*1.2,L.dky-i*1.6,L.tw,false,0,t);textC(g,String(q.deck.length),L.dkx+L.tw/2,L.dky+L.th+11*L.s,11*L.s,"#b9b2a2",600);}
   // capture group labels (faint), then all cards by layer
   for(const p of [0,1]){const R=hfCapR(L,q,p);"htrk".split("").forEach((tt,i)=>{const r=R["g"+tt];if(!r.n){g.save();g.globalAlpha=.32;g.strokeStyle="#d8d2c3";g.setLineDash([3,3]);g.beginPath();g.roundRect(r.x,r.y,L.cs,L.chs,3);g.stroke();g.restore();textC(g,["✦","🦌","🎋","🍃"][i],r.x+L.cs/2,r.y+L.chs/2,11*L.s,"rgba(216,210,195,.5)");}});}
   const sel=q.ph==="pick"?q.pc:q.sel,mon=q.ph==="dpick"&&q.dc!=null?hfM(q.dc):sel>=0&&sel!=null&&(q.ph==="play"||q.ph==="pick")?hfM(sel):-1,canPlay=q.ph==="play"&&q.turn===0;
   const tm=new Set(hfTable(q).map(hfM)),ids=Object.keys(q.P).map(Number).sort((a,b)=>(q.P[a].z+(q.P[a].mv?10:0))-(q.P[b].z+(q.P[b].mv?10:0)));
   for(const c of ids){const P=q.P[c],inT=q.ts.includes(c),inH=q.hand[0].includes(c);
     const hl=(inT&&mon>=0&&hfM(c)===mon)||(inH&&c===sel)||(c===q.dc&&q.ph==="dpick")?1:canPlay&&sel<0&&inH&&tm.has(hfM(c))?2:0;
     hfCard(g,c,P.x,P.y,P.w,P.f,hl,t);}
   // counts on capture groups
   for(const p of [0,1]){const R=hfCapR(L,q,p);for(const tt of "htrk"){const r=R["g"+tt];if(r.n>1){const lx=Math.min(r.x+r.w,r.x+L.cs+(r.n-1)*Math.min(L.cs*.62,(r.w-L.cs)/(r.n-1)));g.fillStyle="rgba(14,11,10,.85)";g.beginPath();g.arc(lx-2,r.y+L.chs-4,8*L.s,0,Math.PI*2);g.fill();textC(g,String(r.n),lx-2,r.y+L.chs-3.5,10*L.s,"#f2e8d2",700);}}}
   // speech / status line
   const sy=L.msgY,fresh=q.say&&t-q.say.t<4.5;
   if(fresh){const a=clamp(Math.min((t-q.say.t)*4,(4.5-(t-q.say.t))*2),0,1),lines=hfWrap(g,"«"+q.say.txt+"»",L.cw-40,12.5*L.s),bh=lines.length*16*L.s+10;g.save();g.globalAlpha=a;hfBox(g,L.x0+L.pad,sy-bh/2,L.cw-2*L.pad,bh,.88);
     g.fillStyle="rgba(14,11,10,.88)";g.beginPath();g.moveTo(L.x0+L.pad+22,sy-bh/2);g.lineTo(L.x0+L.pad+30,sy-bh/2-8);g.lineTo(L.x0+L.pad+38,sy-bh/2);g.fill();
     lines.forEach((ln,i)=>textC(g,ln,W/2,sy-(lines.length-1)*8*L.s+i*16*L.s,12.5*L.s,"#f2e8d2",600));g.restore();}
   else textC(g,hfStatus(q),W/2,sy,12.5*L.s,"#cfc6b4",600);
   // the player's progress line
   const cp=q.cap[0],cn=tt=>cp.filter(x=>HF_T[x]===tt).length;
   hfTextL(g,`Ты: ${q.tot[0]} очк.`+(q.yk[0]?` · яку ${q.yk[0]}`:"")+(q.koi[0]?` · こいこい×${q.koi[0]}`:""),L.x0+L.pad,L.pyY,12*L.s,q.koi[0]?"#eea3bb":"#f2e8d2",700);
   hfTextL(g,`✦${cn("h")} · ленты ${cn("r")}/5 · звери ${cn("t")}/5 · простые ${cn("k")+(cp.includes(32)?1:0)}/10`,L.x0+L.cw-L.pad,L.pyY,11*L.s,"#b9b2a2",600,"right");
   // Musya at the side of the hand: watches the chosen card, reacts
   if(!petAway()){let st="rest",fi=Math.floor(t*2)%2;const fy=L.my;
     if(q.ma&&q.ma.until>t){st=q.ma.st;fi=Math.floor(t*9)%8;}
     else{const tc=q.dc!=null?q.dc:sel>=0&&sel!=null?sel:null,P=tc!=null&&q.P[tc];
       if(P){const gi=gazeIndex(P.x+P.w/2-L.mx,(fy-150*L.msc)-(P.y+P.w*.78));st=gi<8?"gaze9":"gaze10";fi=gi%8;}else if(Math.sin(t*.37)>.93){st="groom";fi=Math.floor(t*8)%8;}}
     drawCatG(g,st,fi,L.mx,fy,L.msc);
     if(q.mb){const e=t-q.mb.t;if(e<2.2)drawEmoji(g,q.mb.e,L.mx+30*L.s,fy-205*L.msc-e*8,22*L.s,clamp(Math.min(e*4,(2.2-e)*2),0,1));else q.mb=null;}}
   // big «こいこい!» flash
   if(q.flash){const e=t-q.flash.t;if(e<1.5){const a=clamp(Math.min(e*5,(1.5-e)*2.5),0,1),cy=L.tbY+L.tH/2,bg=g.createLinearGradient(0,cy-60*L.s,0,cy+70*L.s);bg.addColorStop(0,"rgba(8,6,5,0)");bg.addColorStop(.5,`rgba(8,6,5,${.7*a})`);bg.addColorStop(1,"rgba(8,6,5,0)");g.fillStyle=bg;g.fillRect(0,cy-60*L.s,W,130*L.s);g.save();g.globalAlpha=a;jpText(g,"こいこい！",W/2,L.tbY+L.tH/2,(46+e*8)*L.s,q.flash.who?"#eea3bb":"#f2c86a");g.restore();
     textC(g,q.flash.who?`${o.n}: «Кои-кои!»`:"Кои-кои! Играем дальше",W/2,L.tbY+L.tH/2+40*L.s,14*L.s,`rgba(242,232,210,${a})`,700);}else q.flash=null;}
   // the yaku/koi-koi panel and the round result
   q.btns=[];
   if(q.ph==="koi")hfPanel(G,g,t,"Комбинация!",hfYaku(q.cap[0]),q.yk[0],[["koi","Кои-кои!"],["stop",`Стоп: +${q.yk[0]*(q.yk[0]>=7?2:1)*(q.koi[1]?2:1)}`]],
     q.hand[0].length?"«Кои-кои» — играть дальше ради бóльшего. Но если соперник соберёт яку первым, его очки удвоятся.":"",false,q.cap[0]);
   if(q.ph==="round"){const r=q.res,nm=r.w===0?"Раунд твой!":r.w===1?`Раунд за ${o.ins}`:"Ничья",
     note=(r.w>=0?`${r.pts} очк.`+(r.mult>1?` × ${r.mult} (${[r.pts>=7?"7+ очков":"",q.koi[1-r.w]?"«кои-кои» соперника":""].filter(Boolean).join(", ")}) = ${r.pts*r.mult}`:""):"Карты кончились — никто не остановился.")+`  ·  Счёт ${q.tot[0]} : ${q.tot[1]}`+(r.items.length?`  ·  Новая вещь: ${IT[r.items[0]].n}`:"");
     hfPanel(G,g,t,nm,r.yaku,null,[["next",q.ri+1>=q.rounds?"Итоги партии":"Следующий раунд"]],note,r.w===1,r.w>=0?q.cap[r.w]:null);}},
 down(G,x,y,t){const q=G.st,L=q.L;if(!L)return;
   const b=q.btns.find(b=>x>=b.x&&x<=b.x+b.w&&y>=b.y&&y<=b.y+b.h);
   if(b){tone(420,.05,"triangle",.04);if(b.id==="koi")hfKoi(G,true);else if(b.id==="stop")hfKoi(G,false);else if(b.id==="next")hfNextRound(G);return;}
   if(q.ph==="koi"||q.ph==="round")return;
   if(!petAway()&&Math.abs(x-L.mx)<L.musW*.45&&y>L.my-200*L.msc&&y<L.my){hfMus(q,pick(["😺","😽","😸"]),"purr",1.2);tone(220,.3,"sine",.03);return;}
   const at=c=>{const P=q.P[c];return P&&x>=P.x&&x<=P.x+P.w&&y>=P.y&&y<=P.y+P.w*1.56;};
   if(q.ph==="dpick"){const ms=hfMatch(q,q.dc),c=ms.find(at);if(c!=null)hfDrawTake(G,0,c);return;}
   if(q.ph==="pick"){const ms=hfMatch(q,q.pc),c=ms.find(at);if(c!=null){hfHuman(G,q.pc,c);return;}const h=q.hand[0].find(at);if(h!=null&&h!==q.pc){q.ph="play";q.pc=null;q.sel=h;hfFlip();}return;}
   if(q.ph!=="play"||q.turn!==0)return;
   const h=[...q.hand[0]].reverse().find(at);
   if(h!=null){if(h===q.sel)hfHuman(G,h,null);else{q.sel=h;tone(600,.04,"triangle",.03);}return;}
   if(q.sel>=0){const ms=hfMatch(q,q.sel),c=ms.find(at);if(c!=null){hfHuman(G,q.sel,ms.length===2?c:null);return;}}
   q.sel=-1;},
 stat:G=>{const q=G.st;return q.tot?`Раунд ${q.ri+1}/${q.rounds} · ${q.tot[0]} : ${q.tot[1]}`:""},
 card(G){const q=G.st,o=hfOpp(q),r=q.out?q.out.r:0,Z=hfS();
   const got=q.got.map(id=>`<span>${itemThumb(IT[id],84,64)}${IT[id].n}</span>`).join("");
   return`<div class="card hf-card"><p class="tag">花札 · Кои-кои</p><h3>${r>0?"Победа!":r<0?`${o.n} выигрывает`:"Ничья"}</h3>
   <div class="hf-res"><img src="assets/mon/${o.m}.webp" alt=""><p>«${r>0?o.L.mlose:r<0?o.L.mwin:o.L.draw}»</p></div>
   <div class="big">${q.tot[0]} : ${q.tot[1]}</div>
   <p>${r>0?`На кону были данго — забирай: 🍡 данго ×2 и «${FOOD[o.dish].n}» уже в кладовой.`:r<0?`${o.n} делает вид, что съедает воображаемое данго. Твоя кладовая цела.`:"Данго остаются на своих местах. Муся довольна и так."}</p>
   ${got?`<p><b>Новые вещи</b> — в «🧺 Вещи», раздел «Ханафуда»:</p><div class="hf-got">${got}</div>`:""}
   ${q.out&&q.out.unl?`<p><b>Новый соперник:</b> ${q.out.unl.n} ждёт за столом.</p>`:""}
   <p style="font-size:12.5px">Побед над ёкаями: ${hfWins()} · соперников побеждено: ${HF_OPP.filter(x=>Z.w[x.id]).length} из 4</p>
   <div class="row"><button class="btn" id="gHome">Домой</button><button class="btn" id="hfOther">Соперники</button><button class="btn primary" id="gAgain">${r>0?"Ещё":"Реванш"}</button></div></div>`;},
 after(G){const q=G.st;const b=$("hfOther");if(b)b.onclick=hfIntro;if(!petAway()&&q.out)setTimeout(()=>{if(q.out.r>0)react("😸",2);else if(q.out.r<0)react("😿",1.6);},900);ui();}};
GAMES.push(HF);
function hfStatus(q){const o=hfOpp(q);
  if(q.ph==="pick"||q.ph==="dpick")return"Выбери одну из подсвеченных карт на столе";
  if(q.dc!=null)return q.turn===0?"Открываем карту из колоды…":`${o.n} открывает карту из колоды…`;
  if(q.ph==="play"&&q.turn===0){if(q.sel<0)return"Твой ход: выбери карту в руке";const n=hfMatch(q,q.sel).length;
    return n===0?"Пары нет — нажми ещё раз, и карта ляжет на стол":n===2?"Нажми на одну из двух подсвеченных карт":"Нажми ещё раз — и забери карту со стола";}
  return q.turn===1?`Ходит ${o.n}…`:"";}
function hfPanel(G,g,t,title,yaku,pts,btns,note,bad,cap){const q=G.st,L=q.L,W=G.W,w=Math.min(L.cw-24,380),lines=note?hfWrap(g,note,w-28,12*L.s):[];
  const kc=cap?[...new Set(yaku.flatMap(([k])=>(HF_YC[k]||[]).filter(c=>cap.includes(c))))].slice(0,8):[],cw2=Math.min(34*L.s,(w-30)/Math.max(1,kc.length)-4),ch2=kc.length?cw2*1.56+10:0;
  const h=(64+yaku.length*20+lines.length*16+58)*L.s+ch2,x=(W-w)/2,y=clamp(L.tbY+L.tH/2-h/2,8,G.H-h-8);
  g.fillStyle="rgba(5,4,4,.45)";g.fillRect(0,0,W,G.H);hfBox(g,x,y,w,h,.94);
  textC(g,title,W/2,y+26*L.s,22*L.s,bad?"#d8d2c3":"#f2c86a",700);let yy=y+52*L.s;
  if(kc.length){const x1=W/2-(kc.length*(cw2+4)-4)/2;kc.forEach((c,i)=>hfCard(g,c,x1+i*(cw2+4),y+44*L.s,cw2,true,0,t));yy+=ch2;}
  for(const [k,p] of yaku){hfTextL(g,HF_YK[k][0],x+18,yy,14*L.s,"#f2e8d2",700);hfTextL(g,HF_YK[k][1],x+18+108*L.s,yy,11.5*L.s,"#b9b2a2",500);hfTextL(g,`${p}`,x+w-18,yy,14*L.s,"#f2c86a",700,"right");yy+=20*L.s;}
  if(pts!=null){hfTextL(g,"Всего",x+18,yy,13*L.s,"#b9b2a2",600);hfTextL(g,`${pts}`,x+w-18,yy,15*L.s,"#f2c86a",700,"right");yy+=18*L.s;}
  lines.forEach(ln=>{textC(g,ln,W/2,yy+4,12*L.s,"#cfc6b4",500);yy+=16*L.s;});
  const bw=(w-24-(btns.length-1)*10)/btns.length,by=y+h-48*L.s;
  btns.forEach(([id,lb],i)=>{const bx=x+12+i*(bw+10);btnRect(g,bx,by,bw,38*L.s,lb,i===0);q.btns.push({id,x:bx,y:by,w:bw,h:38*L.s});});}

// ── the intro card: opponents, match length, stake, a short rules sheet
function hfIntro(){const Z=hfS(),res=$("gResult");if(G.id!=="hf_koikoi")return;res.hidden=false;
  if(!HF_OPP.some((o,i)=>o.id===Z.opp&&hfUnl(i)))Z.opp="tanuki";
  res.innerHTML=`<div class="card hf-card"><p class="tag">花札 · Ханафуда</p><h3>Кои-кои</h3><p class="lore">${HF.lore}</p>
   <div class="hf-opps">${HF_OPP.map((o,i)=>{const u=hfUnl(i);return`<button class="hf-op ${o.id===Z.opp?"on":""}" data-o="${o.id}" ${u?"":"disabled"}><img src="assets/mon/${o.m}.webp" alt=""><b>${u?o.n:"???"}</b><small>${u?(Z.w[o.id]?`побед: ${Z.w[o.id]} · ${o.about}`:o.about):`🔒 сначала обыграй ${HF_OPP[i-1].gen}`}</small></button>`;}).join("")}</div>
   <div class="hf-len"><button data-l="3" aria-pressed="${Z.len!==6}">3 раунда</button><button data-l="6" aria-pressed="${Z.len===6}">6 — как у мастеров</button></div>
   <p>На кону 🍡 данго. Победа — угощение в кладовую. Проигрыш — ничего страшного, только шутка соперника.</p>
   <details class="hf-rules"${Z.n?"":" open"}><summary>Правила коротко</summary>
   <p>48 карт: 12 месяцев по 4 (цифра в углу — месяц). У каждого 8 карт, 8 лежат на столе. Ход: выложи карту из руки — если на столе есть карта того же месяца, забери обе. Потом открой карту из колоды — с ней то же самое. Три карты месяца на столе забираются все сразу.</p>
   <ul><li><b>Гоко</b> — 5 светил: 10 · <b>Сико</b> — 4 без Дождя: 8 · <b>Амэ-сико</b> — 4 с Дождём (Ива): 7 · <b>Санко</b> — 3 без Дождя: 5</li>
   <li><b>Ино-сика-тё</b> — кабан, олень, бабочки: 5</li><li><b>Акатан</b> — 3 красные ленты со стихами: 5 · <b>Аотан</b> — 3 синие ленты: 5</li>
   <li><b>Цукими-дзакэ</b> — луна + чаша сакэ: 5 · <b>Ханами-дзакэ</b> — занавес + чаша: 5</li>
   <li><b>Тан</b> — 5 лент: 1 · <b>Танэ</b> — 5 животных: 1 · <b>Касу</b> — 10 простых: 1 (+1 за каждую следующую карту). Чаша сакэ — и животное, и простая.</li></ul>
   <p>Собрал комбинацию — реши: «Кои-кои!» (играть дальше) или «Стоп» (забрать очки). 7 очков и больше — ×2. Если соперник сказал «кои-кои», а раунд остановил ты — ещё ×2.</p></details>
   <div class="row"><button class="btn" id="gBack">Назад</button><button class="btn primary" id="gGo">Играть</button></div></div>`;
  res.querySelectorAll(".hf-op").forEach(b=>b.onclick=()=>{Z.opp=b.dataset.o;res.querySelectorAll(".hf-op").forEach(e=>e.classList.toggle("on",e===b));tone(500,.05,"triangle",.03);});
  res.querySelectorAll(".hf-len button").forEach(b=>b.onclick=()=>{Z.len=+b.dataset.l;res.querySelectorAll(".hf-len button").forEach(e=>e.setAttribute("aria-pressed",e===b));});
  $("gBack").onclick=closeGame;$("gGo").onclick=()=>{save();beginGame();};}
function hfOpen(){if(G.id&&G.id!=="hf_koikoi")return;closePanel();hfLoad();openGame("hf_koikoi");hfIntro();}

// ── entries: the games room card (opens our intro), the 家 hub card, the album
hook("tray",(tray,room)=>{if(room!=="games")return;const b=tray.querySelector('[data-game="hf_koikoi"]');if(!b)return;b.removeAttribute("data-game");b.dataset.x="hf:open";
  const em=b.querySelector("em"),n=hfWins();if(em)em.textContent=n?`Побед: ${n}`:"Тануки ждёт партию";});
hook("click",k=>{if(!k.startsWith("hf:"))return;if(k==="hf:open")hfOpen();return true;});
hook("hub",()=>{const Z=hfS(),b=HF_OPP.filter(o=>Z.w[o.id]),nx=HF_OPP.find((o,i)=>hfUnl(i)&&!Z.w[o.id]);
  return`<div class="hubc"><h4>🎴 Ханафуда <i>花札</i></h4><p>${!b.length?"Тануки зовёт сыграть в кои-кои на данго. Муся будет смотреть.":nx?`Побеждены: ${b.map(o=>o.n).join(", ")}. За столом ждёт ${nx.n}.`:"Все четыре ёкая побеждены. Реванш?"}</p><div class="row"><button class="btn" data-x="hf:open">Сыграть</button></div></div>`;});
hook("album",el=>{const Z=hfS(),n=Object.keys(HF_YK).filter(k=>Z.y[k]).length;if(!Z.n)return;
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Ханафуда</h3><p class="lead">Партий сыграно: ${Z.n}. Побеждены: ${HF_OPP.filter(o=>Z.w[o.id]).map(o=>o.n).join(", ")||"пока никто"}. Комбинаций собрано: ${n} из ${Object.keys(HF_YK).length}.</p>
   <div class="hf-alb">${Object.keys(HF_YK).map(k=>`<span class="${Z.y[k]?"on":""}">${Z.y[k]?"✓ "+HF_YK[k][0]+(Z.y[k]>1?` ×${Z.y[k]}`:""):"··· "+HF_YK[k][0]}</span>`).join("")}</div>`);});

// tests: open, start against someone, rig the player's captures, AI-vs-AI simulation of the rules engine
X.hf={open:hfOpen,intro:hfIntro,S:hfS,yaku:hfYaku,
  start(opp,len){const Z=hfS();if(opp)Z.opp=opp;if(len)Z.len=len;hfOpen();beginGame();},
  q:()=>G.st,
  auto(n=1){const q=G.st;for(let i=0;i<n;i++){if(q.ph!=="play"||q.turn!==0)return q.ph;const a=hfAiPick(q,0);hfHuman(G,a.c,a.tgt);}return q.ph;},
  rig(cards){const q=G.st;for(const c of cards){for(const A of [q.hand[0],q.hand[1],q.deck,q.cap[1]]){const i=A.indexOf(c);if(i>=0)A.splice(i,1);}const j=q.ts.indexOf(c);if(j>=0)q.ts[j]=null;if(!q.cap[0].includes(c))q.cap[0].push(c);}},
  check(){hfCheck(G,0);},
  sim(n=200){const R={w:[0,0,0],bad:0,pts:[0,0],errs:[]};for(const [oi] of HF_OPP.entries())for(let i=0;i<n/4;i++){const q={oi,dealer:i%2};hfDeal(q);
    const w=hfSimRound(q),all=[...q.hand[0],...q.hand[1],...hfTable(q),...q.deck,...q.cap[0],...q.cap[1]];
    if(all.length!==48||new Set(all).size!==48||w===-2){R.bad++;if(R.errs.length<3)R.errs.push({w,n:all.length});}
    R.w[w<0?2:w]++;if(w>=0)R.pts[w]+=q.yk[w];}return R;}};
}
