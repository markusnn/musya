{
// ───────────────────────── «Пруд с карпами»: breed koi in a wooden tub, raise the fry, release them into the big pond, Sunday koi show ─────────────────────────
// S.ext.koi = {f:[fish], n:next id, br:dayKey of the last spawning, fed:dayKey the fry were fed, sel:[ids picked for a pair], show:{d,f,pl,sc,rv}, wins:[1st,2nd,3rd,4th], shows}
// fish = {i, nm, g:{k,h,s,b,c,z,d,gin,og,tan} genes, p:[[u,v,r]] red patches, q:[[u,v,r]] sumi (white base) or white (black base), b:birth dayKey, fd:days fed (8 = adult), ad:dayKey adult, pond:1, par:"A × B", rv:1 variety revealed}
// genes: k black base, h red, s sumi, b asagi blue, c cha brown (0..1), z size, d doitsu (scaleless), gin / og (metallic) / tan (red crown) — rare mutations.
// Koi are painted on canvas from that data (head to the right, 300×110 like assets/koi/*.webp), so the pond can take them as KOI_IMG["ko_<id>"].
const KO_R={tub:[0,0,240,150],ko_cup:[242,0,150,210],ko_scroll:[394,0,120,270],ko_rib1:[516,0,110,190],ko_rib2:[628,0,110,190],ko_rib3:[740,0,110,190]};
addItems([["ko_rib1","Алая розетка · первое место","t","Займи первое место на воскресной выставке карпов"],["ko_rib2","Синяя розетка · второе место","t","Займи второе место на воскресной выставке карпов"],
  ["ko_rib3","Белая розетка · третье место","t","Займи третье место на воскресной выставке карпов"],["ko_scroll","Грамота выставки карпов","t","Выставь карпа на воскресную выставку у пруда"],
  ["ko_cup","Кубок Великого карпа","b","Трижды победи на выставке карпов"]].map(([id,n,a,hint])=>{const r=KO_R[id];return{id,n,c:"Выставка карпов",w:r[2],h:r[3],a,p:0,at:["ko",r[0],r[1]],src:"🏆 выставка карпов",hint};}),{ko:[852,270]});
STAMPS.push(["ko_fry","稚","Первые мальки","Разведи карпов в садке у пруда"],["ko_rare","銀","Редкий карп","Выведи огона, гинрина или тантё"],["ko_win","賞","Победа на выставке","Займи первое место на воскресной выставке карпов"]);
// variety: [name, kanji, rarity 1..5, description]
const KO_V={kohaku:["Кохаку","紅白",1,"Белый карп с алыми пятнами — самая любимая порода."],sanke:["Тайсё Сансёку","大正三色",2,"Белый, алый и чёрные пятнышки на спине; голова без чёрного."],
  showa:["Сёва","昭和三色",2,"Чёрный карп с алыми и белыми пятнами; чёрное заходит на голову."],shiro:["Сиро Уцури","白写り",2,"Чёрный с белым, как тушь на бумаге."],
  hiutsuri:["Хи Уцури","緋写り",3,"Чёрный с алым, как угли в очаге."],bekko:["Бэкко","鼈甲",2,"Белый, с чёрными пятнышками, как панцирь черепахи."],
  muji:["Сиромудзи","白無地",2,"Совсем белый, без единого пятнышка."],asagi:["Асаги","浅葱",2,"Голубая спина в сетке чешуи, алые щёки и бока."],
  goshiki:["Госики","五色",3,"Пять цветов: алые пятна поверх тёмной сетки чешуи."],shusui:["Сюсуй","秋翠",3,"Голубой, без чешуи, с рядом крупных чешуй вдоль спины."],
  kumonryu:["Кумонрю","九紋竜",4,"«Дракон девяти узоров»: чёрный с белыми разводами, без чешуи."],chagoi:["Тягои","茶鯉",2,"Бронзовый и спокойный, первым подплывает к руке."],
  tancho:["Тантё","丹頂",4,"Белоснежный, с одним алым кругом на голове — как журавль тантё."],ogon:["Огон","黄金",5,"Весь золотой, светится, как монета на дне."],
  platinum:["Пуратина","プラチナ",5,"Серебряный огон: светится, как луна в воде."],ginrin:["Гинрин","銀鱗",4,"Не порода, а чудо: чешуя искрится серебром."]};
const KO_VL=Object.keys(KO_V),KO_RARE=["ogon","platinum","tancho","ginrin"];
const KO_TPL={kohaku:{k:0,h:.55,s:0,b:0,c:0},sanke:{k:0,h:.5,s:.5,b:0,c:0},showa:{k:.7,h:.45,s:.3,b:0,c:0},shiro:{k:.7,h:0,s:0,b:0,c:0},bekko:{k:0,h:0,s:.55,b:0,c:0},
  asagi:{k:0,h:.3,s:0,b:.85,c:0},chagoi:{k:0,h:0,s:0,b:0,c:.85},hiutsuri:{k:.9,h:.5,s:0,b:0,c:0}};
const KO_NM=["Хана","Юки","Сора","Рин","Мио","Хару","Нацу","Фую","Аки","Момо","Анзу","Кури","Умэ","Кин","Гин","Таро","Дзиро","Котаро","Тама","Сумирэ","Ринго","Моти","Данго","Нисики",
  "Хотару","Сидзуку","Нами","Кири","Араси","Цубаки","Ёру","Акари","Хикари","Каэдэ","Мацу","Такэ","Кому","Ицуки","Сэн","Химэ","Ако","Тиё","Кохару","Минори","Томо","Кайто","Нанао","Усио"];
const KO_RVN=["Ёсино","Кагэ","Мангэцу","Дайкоку","Бэнтэн","Ханаби","Тацу","Коганэ","Сэйрю","Фудзи","Сакон","Укон"];
const KO_OWN=["Кицунэ из святилища","Дзасики-вараси","Нэкомата с крыши","Адзуки-арай с ручья","Каса-обакэ","Ёсудзумэ из леса"];
const KO_W=300,KO_H=110,KO_CY=55,KO_ADULT=8,KO_NURSE=12,KO_MAX=36,KO_PMAX=Math.max(0,12-KOI_NAMES.length);
const KO_TB={x:600,y:1192,w:250};      // the tub in the courtyard: foot point (image coords) and width
const KS=()=>S.ext.koi||null,koF=()=>KS()?KS().f:[],koById=i=>koF().find(f=>f.i===i);
const koSt=f=>f.fd>=KO_ADULT?2:f.fd>=3?1:0,koAdults=()=>koF().filter(f=>koSt(f)===2),koFry=()=>koF().filter(f=>koSt(f)<2);
const koDays=(a,b)=>Math.round((Date.parse(b)-Date.parse(a))/864e5);
function koW(n,w){const a=n%10,b=n%100;return n+" "+(a===1&&b!==11?w[0]:a>=2&&a<=4&&(b<12||b>14)?w[1]:w[2]);}
function koAge(f){const n=Math.max(0,koDays(f.b,dayKey()));return n<1?"родился сегодня":n<60?koW(n,["день","дня","дней"]):n<365?koW(Math.floor(n/30),["месяц","месяца","месяцев"]):koW(Math.floor(n/365),["год","года","лет"]);}
function koCm(f){if(f.cm)return f.cm;const z=f.g.z,a=z*(3+32*(1-Math.exp(-Math.min(f.fd,KO_ADULT)/4.5)));return Math.round(a+(f.ad?Math.min(24,Math.max(0,koDays(f.ad,dayKey()))*.6)*z:0));}
function koVar(g){if(g.og)return g.h>.3||g.c>.3?"ogon":"platinum";if(g.c>.55)return"chagoi";if(g.b>.55)return g.d?"shusui":"asagi";
  if(g.k>.55)return g.d?"kumonryu":g.h<.15?"shiro":g.k>.8?"hiutsuri":"showa";
  if(g.tan)return"tancho";if(g.b>.3&&g.h>.2)return"goshiki";if(g.s>.35)return g.h>.15?"sanke":"bekko";return g.h>.15?"kohaku":"muji";}
function koVName(f){const v=koVar(f.g);return(f.g.gin?"Гинрин ":"")+(f.g.d&&v!=="shusui"&&v!=="kumonryu"?"Дойцу ":"")+KO_V[v][0];}
const koRed=f=>`hsl(${6+(f.i*37)%10},${66+(f.i*7)%10}%,${43+(f.i*13)%6}%)`;

// ── genes and patterns
function koMix(a,b,R){const o=[];for(const s of [a||[],b||[]])for(const x of s)if(R()<.5)o.push([clamp(x[0]+(R()-.5)*.12,.15,.97),clamp(x[1]+(R()-.5)*.25,-.8,.8),clamp(x[2]*(.85+R()*.3),.1,.9)]);return o;}
function koFit(a,n,R,mk){while(a.length>n)a.splice(Math.floor(R()*a.length),1);while(a.length<n)a.push(mk());return a.map(b=>b.map(v=>Math.round(v*100)/100));}
function koBlobs(g,R,pa,pb){const black=g.k>.55,nP=g.h<.12?0:Math.round(1+g.h*5),nQ=black?2+Math.floor(R()*3):Math.round(g.s*9);
  const p=koFit(koMix(pa&&pa.p,pb&&pb.p,R),nP,R,()=>[mix(.22,.95,R()),(R()-.5)*1.1,mix(.38,.75,R())*(.7+g.h*.5)]);
  if(nP&&!pa&&R()<.85)p[0]=[+mix(.84,.93,R()).toFixed(2),+((R()-.5)*.3).toFixed(2),+mix(.45,.62,R()).toFixed(2)];   // a head mark on wild fish
  const q=koFit(koMix(pa&&pa.q,pb&&pb.q,R).map(b=>black?[b[0],b[1],Math.max(.45,b[2])]:[Math.min(.8,b[0]),b[1],Math.min(.26,b[2])]),nQ,R,
    ()=>black?[mix(.15,.95,R()),(R()-.5)*1.4,mix(.45,.8,R())]:[mix(.28,.78,R()),(R()-.5)*1.3,mix(.12,.24,R())]);
  return{p,q};}
function koGene(a,b,R){const m=(x,y)=>clamp(mix((x+y)/2,R()<.5?x:y,.55)+(R()+R()+R()-1.5)*.16,0,1);
  const g={k:m(a.k,b.k),h:m(a.h,b.h),s:m(a.s,b.s),b:m(a.b,b.b),c:m(a.c,b.c),z:clamp((a.z+b.z)/2+(R()-.5)*.22,.8,1.25)};
  if(R()<.06)g[["k","h","s","b"][Math.floor(R()*4)]]=R();
  const fl=(x,y,p0,p1,p2)=>R()<(x&&y?p2:x||y?p1:p0)?1:0;
  g.d=fl(a.d,b.d,.06,.5,.9);g.gin=fl(a.gin,b.gin,.05,.35,.7);g.og=fl(a.og,b.og,.03,.3,.7);g.tan=g.k<.55&&g.b<.55&&g.c<.55&&!g.og&&R()<.045?1:0;
  for(const k of "khsbcz")g[k]=Math.round(g[k]*100)/100;return g;}
function koName(){const used=new Set(koF().map(f=>f.nm)),fr=KO_NM.filter(n=>!used.has(n));return fr.length?pick(fr):pick(KO_NM)+" "+(koF().length+1);}
function koMake(g,pa,pb,nm){const K=KS(),f=Object.assign({i:K.n++,nm:nm||koName(),g,b:dayKey(),fd:0},koBlobs(g,Math.random,pa,pb));if(pa)f.par=pa.nm+" × "+pb.nm;return f;}

// ── painting a koi from its data (top view, head to the right)
function koHalf(x){const u=(x-70)/222;if(u<0||u>1)return 0;if(u<.62)return 4.5+29.5*Math.pow(u/.62,1.1);return 34*Math.pow(Math.max(0,1-Math.pow((u-.62)/.38,2.4)),.55);}
function koBody(g){g.beginPath();for(let x=70;x<=292;x+=2)g.lineTo(x,KO_CY-koHalf(x));for(let x=292;x>=70;x-=2)g.lineTo(x,KO_CY+koHalf(x));g.closePath();}
const koPt=(u,v)=>{const x=70+222*u;return[x,KO_CY+v*koHalf(x)];};
function koBlob(g,b,col){const [u,v,r]=b,[x,y]=koPt(u,v*.85),Rr=r*34,R=rng(Math.round(u*997+v*577+r*313)*31+7);g.fillStyle=col;g.beginPath();g.ellipse(x,y,Rr*.95,Rr*.7,0,0,Math.PI*2);
  for(let k=0;k<6;k++){const a=R()*6.283,d=R()*Rr*.6,rr=Rr*(.32+R()*.38),cx=x+Math.cos(a)*d,cy=y+Math.sin(a)*d*.75;g.moveTo(cx+rr,cy);g.ellipse(cx,cy,rr,rr*.85,0,0,Math.PI*2);}g.fill();}
function koFinPath(g,pts){g.beginPath();pts.forEach(([x,y],i)=>i?g.lineTo(x,y):g.moveTo(x,y));g.closePath();}
function koFins(g,fc,motoguro){g.save();g.globalAlpha=.45;g.fillStyle=fc;g.strokeStyle="rgba(0,0,0,.35)";g.lineWidth=.8;
  const tail=[[74,KO_CY]];for(let i=0;i<=24;i++){const a=-Math.PI/2+Math.PI*i/24;tail.push([22+18*Math.pow(Math.abs(Math.sin(a)),1.5),KO_CY+26*Math.sin(a)]);}
  koFinPath(g,tail);g.fill();g.beginPath();for(let i=0;i<13;i++){const a=-1.35+2.7*i/12;g.moveTo(74,KO_CY);g.lineTo(24+14*Math.pow(Math.abs(Math.sin(a)),1.5),KO_CY+25*Math.sin(a));}g.stroke();
  for(const s of [-1,1]){koFinPath(g,[[212,KO_CY+s*27],[196,KO_CY+s*46],[184,KO_CY+s*44],[196,KO_CY+s*30]]);g.fill();
    if(motoguro){g.save();g.globalAlpha=.8;g.fillStyle="#191514";koFinPath(g,[[212,KO_CY+s*27],[202,KO_CY+s*38],[196,KO_CY+s*36],[200,KO_CY+s*28]]);g.fill();g.restore();}
    koFinPath(g,[[132,KO_CY+s*22],[118,KO_CY+s*34],[112,KO_CY+s*31],[124,KO_CY+s*21]]);g.fill();}
  g.restore();}
function koNet(g,col,w){g.save();g.beginPath();g.rect(96,0,152,KO_H);g.clip();g.strokeStyle=col;g.lineWidth=w;g.beginPath();for(let d=-120;d<300;d+=7){g.moveTo(d,0);g.lineTo(d+110,110);g.moveTo(d+110,0);g.lineTo(d,110);}g.stroke();g.restore();}
function koPaint(f,st){
  const c=document.createElement("canvas");c.width=KO_W;c.height=KO_H;const g=c.getContext("2d"),G=f.g,v=koVar(G),R=rng(f.i*7919+13),red=koRed(f);
  const base={showa:"#1b1817",shiro:"#1b1817",hiutsuri:"#1b1817",kumonryu:"#1b1817",asagi:"#7d93a6",shusui:"#8ea6b8",chagoi:"#8a6640",ogon:"#d9a33a",platinum:"#dedbd2"}[v]||"#efe9dc";
  const blk=base==="#1b1817";
  koFins(g,blk?"#3a3330":v==="asagi"||v==="shusui"?"#c8704a":base,blk);
  g.save();koBody(g);g.clip();g.fillStyle=base;g.fillRect(0,0,KO_W,KO_H);
  if(v==="goshiki"){g.fillStyle="rgba(60,76,104,.28)";g.fillRect(0,0,KO_W,KO_H);}
  if(["kohaku","sanke","showa","hiutsuri","goshiki"].includes(v))for(const b of f.p)koBlob(g,b,red);
  if(v==="sanke"||v==="bekko")for(const b of f.q)koBlob(g,b,"#1b1817");
  if(v==="showa"||v==="shiro"||v==="kumonryu")for(const b of f.q)koBlob(g,b,"#ece6d8");
  if(v==="asagi"||v==="shusui"){const a=.35+G.h*.9;for(let x=78;x<292;x+=3){const h=koHalf(x+1.5);if(h<2)continue;const gr=g.createLinearGradient(0,KO_CY-h,0,KO_CY+h),cl=`rgba(205,92,50,${clamp(a,0,1)})`,z="rgba(205,92,50,0)";
    gr.addColorStop(0,cl);gr.addColorStop(.24,z);gr.addColorStop(.76,z);gr.addColorStop(1,cl);g.fillStyle=gr;g.fillRect(x,KO_CY-h,3.6,h*2);}
    const ch=g.createRadialGradient(262,KO_CY,4,262,KO_CY,30);ch.addColorStop(0,"rgba(205,92,50,0)");ch.addColorStop(1,`rgba(205,92,50,${clamp(a*.8,0,.9)})`);g.fillStyle=ch;g.fillRect(232,KO_CY-34,62,68);}
  if(v==="tancho"){g.fillStyle=red;g.beginPath();g.ellipse(249,KO_CY,13,11.5,0,0,Math.PI*2);g.fill();}
  if(!G.d){const nc={asagi:"rgba(232,238,244,.5)",goshiki:"rgba(24,28,44,.45)",chagoi:"rgba(240,214,160,.3)",ogon:"rgba(120,78,10,.35)",platinum:"rgba(110,110,110,.25)"}[v];koNet(g,nc||(blk?"rgba(255,255,255,.035)":"rgba(0,0,0,.04)"),nc?.9:.6);}
  else for(let i=0,x=112;x<240;x+=14,i++){const y=KO_CY+(i%2?2.5:-2.5);g.fillStyle=blk?"rgba(70,70,74,.7)":v==="shusui"?"rgba(40,64,96,.75)":"rgba(80,80,80,.35)";g.beginPath();g.ellipse(x,y,6,4.4,0,0,Math.PI*2);g.fill();
    g.fillStyle="rgba(255,255,255,.18)";g.beginPath();g.ellipse(x-1.5,y-1.2,2.2,1.3,0,0,Math.PI*2);g.fill();}
  for(let x=70;x<294;x+=4){const h=koHalf(x+2)+1;if(h<1.5)continue;const gr=g.createLinearGradient(0,KO_CY-h,0,KO_CY+h);
    gr.addColorStop(0,"rgba(0,0,0,.55)");gr.addColorStop(.2,"rgba(0,0,0,.14)");gr.addColorStop(.42,"rgba(255,255,255,.07)");gr.addColorStop(.58,"rgba(255,255,255,.07)");gr.addColorStop(.8,"rgba(0,0,0,.14)");gr.addColorStop(1,"rgba(0,0,0,.55)");
    g.fillStyle=gr;g.fillRect(x,KO_CY-h,4.6,h*2);}
  {const gr=g.createLinearGradient(70,0,292,0);gr.addColorStop(0,"rgba(0,0,0,.3)");gr.addColorStop(.25,"rgba(0,0,0,0)");gr.addColorStop(.9,"rgba(255,255,255,.05)");g.fillStyle=gr;g.fillRect(70,0,222,KO_H);}
  for(let i=0;i<160;i++){g.fillStyle=R()<.5?"rgba(0,0,0,.05)":"rgba(255,255,255,.05)";g.fillRect(75+R()*215,KO_CY-30+R()*60,1.5,1.5);}
  g.globalCompositeOperation="lighter";
  {const sp=g.createLinearGradient(0,KO_CY-4,0,KO_CY+4);sp.addColorStop(0,"rgba(255,255,255,0)");sp.addColorStop(.5,"rgba(255,255,255,.07)");sp.addColorStop(1,"rgba(255,255,255,0)");g.fillStyle=sp;g.beginPath();g.ellipse(176,KO_CY,74,4,0,0,Math.PI*2);g.fill();}
  if(G.og){const gr=g.createLinearGradient(0,KO_CY-30,0,KO_CY+30),hc=v==="ogon"?"255,226,150":"235,240,245";gr.addColorStop(0,`rgba(${hc},0)`);gr.addColorStop(.4,`rgba(${hc},.42)`);gr.addColorStop(.5,`rgba(${hc},.6)`);gr.addColorStop(.6,`rgba(${hc},.42)`);gr.addColorStop(1,`rgba(${hc},0)`);g.fillStyle=gr;g.fillRect(80,KO_CY-30,205,60);}
  if(G.gin)for(const [ri,vv] of [-.62,-.38,-.14,.1,.34,.58].entries())for(let x=104+(ri%2)*4;x<248;x+=8){if(R()>.72)continue;const y=KO_CY+vv*koHalf(x);g.fillStyle=`rgba(255,255,255,${.3+R()*.4})`;g.beginPath();g.ellipse(x,y,2.3,1.4,0,0,Math.PI*2);g.fill();}
  g.restore();
  for(const s of [-1,1]){const ex=262,ey=KO_CY+s*15;g.fillStyle="#120f0e";g.beginPath();g.ellipse(ex,ey,3.2,2.6,0,0,Math.PI*2);g.fill();g.fillStyle="rgba(230,230,230,.8)";g.beginPath();g.arc(ex-.4,ey-.9,.8,0,Math.PI*2);g.fill();
    g.fillStyle="rgba(0,0,0,.35)";g.beginPath();g.arc(284,KO_CY+s*6,1.2,0,Math.PI*2);g.fill();
    g.strokeStyle=blk?"#4a4240":base;g.globalAlpha=.8;g.lineWidth=1.1;g.beginPath();g.moveTo(286,KO_CY+s*5);g.lineTo(297,KO_CY+s*11);g.stroke();g.globalAlpha=1;}
  if(st<2){g.globalCompositeOperation="source-atop";g.fillStyle=st?"rgba(150,140,112,.3)":"rgba(66,64,46,.74)";g.fillRect(0,0,KO_W,KO_H);g.globalCompositeOperation="source-over";}
  return c;}
const KO_IMC={};
function koImg(f,st){const s=st==null?koSt(f):st,k=f.i+":"+s;if(!KO_IMC[k]){for(let j=0;j<s;j++)delete KO_IMC[f.i+":"+j];KO_IMC[k]=koPaint(f,s);}return KO_IMC[k];}

// ── the big pond: released adults swim with the others (≤ 12 fish in all)
function koPondAdd(f){const n="ko_"+f.i;KOI_IMG[n]=koImg(f,2);const sz=clamp(koCm(f)/44,.55,1.25),k=koiPond.find(q=>q.n===n);if(k){k.size=sz;return;}
  koiPond.push({n,x:rand(900,1440),z:rand(40,200),h:rand(0,6.28),v:30,ph:rand(0,6),d:rand(.3,.8),dT:.5,wx:0,wz:0,next:0,size:sz,on:true,fade:0,rip:0});}
function koPondDel(f){const i=koiPond.findIndex(k=>k.n==="ko_"+f.i);if(i>=0)koiPond.splice(i,1);}
const koInPond=()=>koF().filter(f=>f.pond).length;

// ── actions
let KO_MSG="",KO_VIEW=null,KO_ANIM=null,KO_TIM=null,koIm=null,koFeedT=-99;
function koLoad(){if(!koIm)atlasImg("ko",im=>{koIm=im;});}
function koStart(){if(KS())return;S.ext.koi={f:[],n:1,br:null,fed:null,sel:[],show:null,wins:[0,0,0,0],shows:0};const K=KS(),old=dayKey(new Date(today().getTime()-3*365*864e5));
  for(const [v,nm,z] of [["kohaku","Бэни",1.02],["showa","Сумиэ",.98],["asagi","Сора",.95],["chagoi","Кури",1.08]]){const g=Object.assign({z,d:0,gin:0,og:0,tan:0},KO_TPL[v]),f=koMake(g,null,null,nm);f.b=old;f.ad=old;f.fd=KO_ADULT;f.rv=1;K.f.push(f);}
  koLoad();save();KO_MSG="Каппа принёс деревянный садок и четырёх своих карпов: «Береги их. А мальков корми раз в день — вырастут за неделю».";tabDots();hubDot();}
function koSel(i){const K=KS(),s=K.sel||(K.sel=[]),j=s.indexOf(i);if(j>=0)s.splice(j,1);else{s.push(i);if(s.length>2)s.shift();}}
function koSpawn(){const K=KS(),[a,b]=(K.sel||[]).map(koById);if(!a||!b)return;
  if(K.br===dayKey()){KO_MSG="Сегодня нерест уже был — завтра можно снова.";return;}
  const n=3+Math.floor(Math.random()*3);if(koFry().length+n>KO_NURSE){KO_MSG="В садке тесно: пусть мальки сперва подрастут.";return;}
  if(koF().length+n>KO_MAX){KO_MSG="Карпов уже слишком много — отпусти кого-нибудь в реку.";return;}
  const kids=[];for(let i=0;i<n;i++){const f=koMake(koGene(a.g,b.g,Math.random),a,b);K.f.push(f);kids.push(f);}
  K.br=dayKey();K.sel=[];save();award("ko_fry");chime([659,784,988]);
  KO_MSG=`В садке ${koW(n,["малёк","малька","мальков"])} от пары ${a.nm} × ${b.nm}. Узор проявится, когда они подрастут.`;
  if(S.room==="courtyard"&&!petAway()){react("😻",2);S.needs.joy=clamp(S.needs.joy+4,0,100);}tabDots();hubDot();}
function koReveal(f){f.rv=1;const v=koVar(f.g),nw=[];if(disc("koi",v))nw.push(KO_V[v][0]);if(f.g.gin&&disc("koi","ginrin"))nw.push("Гинрин");
  if(f.g.og||f.g.gin||f.g.tan)award("ko_rare");return nw;}
function koFeed(){const K=KS(),fr=koFry();if(!fr.length){KO_MSG="В садке нет мальков — устрой нерест.";return;}if(K.fed===dayKey()){KO_MSG="Сегодня мальки уже сыты. Приходи завтра.";return;}
  K.fed=dayKey();const grown=[],nw=[];for(const f of fr){f.fd++;if(f.fd===3&&!f.rv)nw.push(...koReveal(f));if(f.fd===KO_ADULT){f.ad=dayKey();grown.push(f.nm);}}
  koFeedT=now();save();sfx("splash");S.needs.joy=clamp(S.needs.joy+3,0,100);if(S.room==="courtyard"&&!petAway())react("😺",1.6);
  KO_MSG=nw.length?`✨ У мальков проявился узор — новая порода: ${nw.join(", ")}!`:grown.length?`🐟 ${grown.join(", ")} ${grown.length>1?"выросли":"вырос"} — теперь это взрослые карпы.`:`🍚 Мальки поели (${fr.length}). Завтра снова.`;
  if(nw.length)chime([784,988,1175,1568]);tabDots();hubDot();}
function koPond(i){const f=koById(i);if(!f||koSt(f)<2)return;if(f.pond){f.pond=0;koPondDel(f);KO_MSG=`${f.nm} вернулся в садок.`;}
  else{if(koInPond()>=KO_PMAX){KO_MSG=`В большом пруду уже ${KO_PMAX} твоих карпов — больше там не поместится.`;return;}f.pond=1;koPondAdd(f);KO_MSG=`${f.nm} плывёт в большом пруду у водопада.`;sfx("splash");}save();}
function koFree(i){const K=KS(),f=koById(i);if(!f)return;if(koSt(f)===2&&koAdults().length<=2){KO_MSG="Для нереста нужны хотя бы два взрослых карпа.";return;}
  koPondDel(f);K.f.splice(K.f.indexOf(f),1);K.sel=(K.sel||[]).filter(x=>x!==i);KO_VIEW=null;KO_MSG=`${f.nm} уплыл вниз по ручью. Каппа помашет ему с камня.`;save();}

// ── the Sunday show: the player's koi and three rivals in blue bowls; the kappa and the old tanuki judge
const koSunday=()=>today().getDay()===0;
function koScore(f,R){const v=koVar(f.g),G=f.g;let pat;
  if(["kohaku","sanke","showa","hiutsuri","goshiki"].includes(v)&&f.p.length){const area=f.p.reduce((a,b)=>a+b[2]*b[2],0)*.33,cov=1-Math.min(1,Math.abs(area-.35)/.3),head=f.p.some(b=>b[0]>.8)?1:0,tail=f.p.some(b=>b[0]<.26)?0:1,
    sw=f.p.reduce((a,b)=>a+b[2],0),bal=1-Math.min(1,Math.abs(f.p.reduce((a,b)=>a+b[1]*b[2],0))/Math.max(.3,sw));pat=10*(cov*.42+head*.28+tail*.12+bal*.18);
    if(v==="sanke")pat=pat*.85+1.5*(f.q.length>=2&&f.q.length<=6?1:.4);}
  else if(v==="shiro"||v==="kumonryu"||v==="showa")pat=5+(f.q.length>=2&&f.q.length<=4?3.5:1.5);
  else if(v==="bekko")pat=4+(f.q.length>=3&&f.q.length<=7?4.5:2);
  else if(v==="tancho")pat=9.2;
  else if(v==="asagi"||v==="shusui")pat=5.5+3.5*(1-Math.min(1,Math.abs(G.h-.35)*2.5));
  else pat=7;
  const sc=[clamp(pat+(R()-.5)*1.2,1,10),clamp((koCm(f)-14)/46*10,0,10),clamp(KO_V[v][2]*1.8+(G.gin?1.6:0)+(G.d&&v!=="shusui"&&v!=="kumonryu"?.6:0),0,10)];
  return sc.map(x=>Math.round(x*10)/10);}
function koRivals(){const d=dayKey(),R=rng(Date.parse(d)/864e5|0),own=KO_OWN.slice();const L=[];
  for(let k=0;k<3;k++){const v=Object.keys(KO_TPL)[Math.floor(R()*8)],g=Object.assign({z:1,d:0,gin:R()<.12?1:0,og:0,tan:0},KO_TPL[v]);
    const f=Object.assign({i:900000+(Date.parse(d)/864e5|0)%1000*10+k,nm:KO_RVN[Math.floor(R()*KO_RVN.length)],g,b:d,fd:KO_ADULT,cm:Math.round(28+R()*26)},koBlobs(g,R));
    f.own=own.splice(Math.floor(R()*own.length),1)[0];L.push(f);}return L;}
function koEnter(i){const K=KS(),f=koById(i);if(!f||!koSunday()||K.show&&K.show.d===dayKey())return;const R=rng(Date.parse(dayKey())/864e5|0),rv=koRivals();
  const all=[f,...rv].map((x,j)=>({j,sc:koScore(x,R)})),tot=a=>a.sc[0]+a.sc[1]+a.sc[2];all.sort((a,b)=>tot(b)-tot(a)||a.j-b.j);
  const pl=all.findIndex(a=>a.j===0)+1,first=!K.shows;K.shows=(K.shows||0)+1;K.wins[pl-1]++;
  K.show={d:dayKey(),f:i,pl,sc:all.sort((a,b)=>a.j-b.j).map(a=>a.sc)};
  const got=[];if(pl<=3){const id="ko_rib"+pl;if(!S.owned.has(id))got.push(IT[id].n);S.owned.add(id);}if(first){S.owned.add("ko_scroll");got.push(IT.ko_scroll.n);}
  if(pl===1){award("ko_win");if(K.wins[0]>=3&&!S.owned.has("ko_cup")){S.owned.add("ko_cup");got.push(IT.ko_cup.n);}}
  K.show.got=got;save();KO_ANIM={t:Date.now()};hubDot();}
const KO_JL={pat:[[8,"Кромка узора — как по лезвию. Красиво."],[6,"Узор ровный, но кое-где расплылся."],[0,"Пятна разбежались кто куда. Подрастёт — выправится."]],
  size:[[8,"Вот это спина! Настоящий великан."],[5,"Крепкий карп, ещё подрастёт."],[0,"Маловат пока, но глаза живые."]],
  rar:[[8,"Такого я видел раз в сто лет."],[5,"Порода хорошая, не каждый день встретишь."],[0,"Простая порода — тем и мила."]]};
const koLine=(k,x)=>KO_JL[k].find(a=>x>=a[0])[1];

// ── panel «Пруд кои»
document.head.insertAdjacentHTML("beforeend","<style>.ko-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(136px,1fr));gap:8px;margin:6px 0 14px}"+
  ".ko-card{border:1px solid var(--line);border-radius:12px;background:radial-gradient(120% 90% at 50% 25%,#1f3a37,#0b1615);padding:6px 8px 8px;display:flex;flex-direction:column;gap:2px;min-width:0;text-align:left}"+
  ".ko-card.sel{box-shadow:inset 0 0 0 2px var(--sakura)}.ko-card canvas{width:100%;aspect-ratio:300/110;display:block;cursor:pointer}.ko-card b{font-family:var(--display);font-size:16px;color:var(--paper)}"+
  ".ko-card>span{font-size:11.5px;color:var(--muted);line-height:1.3}.ko-bt{display:flex;gap:4px;margin-top:4px}.ko-bt button{flex:1;padding:5px 0;border-radius:8px;border:1px solid var(--line);font-size:12.5px}"+
  ".ko-bt button.on{background:var(--paper);color:var(--ink)}.ko-bar{height:5px;border-radius:3px;background:#060908;overflow:hidden;margin:3px 0}.ko-bar i{display:block;height:100%;background:#d9a33a}"+
  ".ko-msg{border-left:3px solid var(--sakura);padding:4px 10px;margin:0 0 12px;color:var(--paper);font-size:14px;line-height:1.45}"+
  ".ko-chips{display:flex;flex-wrap:wrap;gap:5px;margin:6px 0 14px}.ko-chips span{font-size:12px;padding:3px 8px;border-radius:10px;border:1px solid var(--line);color:var(--paper)}.ko-chips span.off{color:var(--muted);opacity:.55}"+
  ".ko-big{width:100%;max-width:420px;aspect-ratio:300/110;display:block;margin:6px auto;border-radius:12px;background:radial-gradient(100% 120% at 50% 40%,#22403c,#0b1615)}"+
  ".ko-show{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:8px 0 12px}.ko-ent{text-align:center;font-size:12.5px;color:var(--muted);line-height:1.35}.ko-ent b{color:var(--paper);font-family:var(--display);font-size:15px}"+
  ".ko-ent.me b{color:var(--sakura)}.ko-ent .ko-pl{font-size:13px;color:var(--paper);min-height:1.3em}"+
  ".ko-bowl{position:relative;aspect-ratio:1;border-radius:50%;margin:0 auto 4px;width:min(100%,170px);background:radial-gradient(circle at 50% 42%,#3a72b8,#1b4682 62%,#0e2a52);box-shadow:inset 0 0 0 5px #6f97cc,inset 0 8px 22px rgba(0,0,0,.55),0 4px 10px rgba(0,0,0,.5);overflow:hidden}"+
  ".ko-bowl>div{position:absolute;inset:0;animation:koSw 17s linear infinite}.ko-bowl canvas{position:absolute;left:17%;top:19%;width:66%}.ko-ent:nth-child(2n) .ko-bowl>div{animation-duration:21s;animation-direction:reverse}.ko-ent:nth-child(2n) .ko-bowl canvas{transform:scaleX(-1)}.ko-sw [hidden]{display:none!important}"+
  "@keyframes koSw{to{transform:rotate(360deg)}}.ko-jd{display:flex;gap:10px;align-items:flex-end;margin:4px 0 10px}.ko-jd img{height:96px;flex:none}.ko-jd p{margin:0!important;font-size:14px!important;flex:1}"+
  ".ko-sc{display:grid;grid-template-columns:auto 1fr;gap:0 6px;font-size:12px;text-align:left;margin:2px auto 0;max-width:150px}.ko-sc i{font-style:normal;color:var(--paper);text-align:right}</style>");
function koCard(f){const K=KS(),st=koSt(f),sel=(K.sel||[]).includes(f.i),vn=st&&f.rv?koVName(f):"порода ещё не видна";
  const info=st===2?`${vn} · ${koCm(f)} см · ${koAge(f)}`:`${KO_STN[st]} · ${vn} · ${koCm(f)} см`;
  const bt=st===2?`<div class="ko-bt"><button class="${sel?"on":""}" data-x="ko:sel:${f.i}">♡ пара</button><button class="${f.pond?"on":""}" data-x="ko:pond:${f.i}">${f.pond?"🌊 в пруду":"🌊 в пруд"}</button></div>`
    :`<div class="ko-bar"><i style="width:${(f.fd/KO_ADULT*100).toFixed(0)}%"></i></div><span>${f.fd} из ${KO_ADULT} кормлений</span>`;
  return`<div class="ko-card${sel?" sel":""}"><canvas data-ko="${f.i}" data-x="ko:look:${f.i}" width="300" height="110"></canvas><b>${f.nm}</b><span>${info}</span>${bt}</div>`;}
const KO_STN=["Малёк","Подросток","Взрослый"];
function koHtml(){const K=KS(),dk=dayKey(),fr=koFry(),ad=koAdults(),msg=KO_MSG?`<p class="ko-msg">${KO_MSG}</p>`:"";KO_MSG="";
  if(KO_VIEW)return msg+koLookHtml(koById(KO_VIEW));
  const sel=(K.sel||[]).map(koById).filter(Boolean),fed=K.fed===dk,bred=K.br===dk;
  const sp=bred?`<p class="lead">Сегодня нерест уже был. Завтра можно выбрать новую пару.</p>`:sel.length===2?`<div class="row"><button class="btn primary" data-x="ko:spawn">🥚 Нерест: ${sel[0].nm} × ${sel[1].nm}</button></div>`
    :`<p class="lead">Отметь «♡ пара» у двух взрослых карпов — и устрой нерест. Раз в день в садке появляются 3–5 мальков.</p>`;
  const nd=(7-today().getDay())%7,sh=K.show&&K.show.d===dk;
  const show=`<h3 class="bh">Выставка карпов <span style="font-family:var(--jp);font-size:14px;color:var(--sakura)">品評会</span></h3><p class="lead">${koSunday()?(sh?`Сегодня ты уже выставлял карпа: ${K.show.pl} место.`:"Сегодня воскресенье — у пруда выставка! Судьи: каппа и старый тануки."):`Выставка — каждое воскресенье, через ${koW(nd,["день","дня","дней"])}.`}
    ${K.shows?` Выставок: ${K.shows}, побед: ${K.wins[0]}.`:""}</p><div class="row"><button class="btn${koSunday()&&!sh?" primary":""}" data-x="ko:show">🏆 ${koSunday()&&!sh?"На выставку":"Выставка"}</button></div>`;
  const dsc=(S.ext.disc||{}).koi||{};
  return msg+`<p class="lead">Деревянный садок у пруда. Мальков корми раз в день — за ${KO_ADULT} кормлений они вырастут. Взрослых карпов можно выпустить в большой пруд (до ${KO_PMAX}).</p>
    <h3 class="bh">Садок</h3>${fr.length?`<div class="row"><button class="btn${fed?"":" primary"}" data-x="ko:feed">${fed?"Мальки сегодня сыты ✓":"🍚 Покормить мальков"}</button></div><div class="ko-grid">${fr.map(koCard).join("")}</div>`:`<p class="lead">Мальков пока нет.</p>`}
    <h3 class="bh">Нерест</h3>${sp}
    <h3 class="bh">Взрослые карпы · ${ad.length}</h3><div class="ko-grid">${ad.map(koCard).join("")}</div>${show}
    <h3 class="bh">Породы · выведено ${KO_VL.filter(v=>dsc[v]).length} из ${KO_VL.length}</h3><div class="ko-chips">${KO_VL.map(v=>dsc[v]||koKnown(v)?`<span>${KO_V[v][0]} <i style="font-style:normal;color:var(--sakura)">${KO_V[v][1]}</i></span>`:`<span class="off">${KO_RARE.includes(v)?"✦ ???":"???"}</span>`).join("")}</div>`;}
function koLookHtml(f){if(!f){KO_VIEW=null;return koHtml();}const st=koSt(f),v=koVar(f.g),seen=st&&f.rv;
  return`<canvas class="ko-big" data-ko="${f.i}" width="300" height="110"></canvas><h3 style="margin-top:6px">${f.nm}</h3>
    <p class="lead">${seen?`${koVName(f)} <span style="font-family:var(--jp);color:var(--sakura)">${KO_V[v][1]}</span>`:"Порода проявится, когда малёк подрастёт"} · ${koCm(f)} см · ${koAge(f)}${st<2?` · ${KO_STN[st].toLowerCase()}`:""}</p>
    ${seen?`<p>${KO_V[v][3]}${f.g.gin&&v!=="ogon"&&v!=="platinum"?" А чешуя у него — гинрин: искрится серебром.":""}</p>`:""}${f.par?`<p class="lead">Родители: ${f.par}.</p>`:`<p class="lead">Из старых карпов каппы.</p>`}
    <div class="row"><button class="btn" data-x="ko:back">← Назад</button><button class="btn" data-x="ko:free:${f.i}">🍃 Отпустить в реку</button></div>`;}
function koPaintEls(){for(const c of $("xpBody").querySelectorAll("canvas[data-ko],canvas[data-kr]")){const g=c.getContext("2d");g.clearRect(0,0,c.width,c.height);
  const f=c.dataset.ko?koById(+c.dataset.ko):(KO_ANIM&&KO_ANIM.rv||koRivals())[+c.dataset.kr];if(f)g.drawImage(koImg(f,c.dataset.kr?2:null),0,0,c.width,c.height);}}
const KO_SG={kohaku:{h:.55},sanke:{h:.5,s:.5},showa:{k:.7,h:.45,s:.3},shiro:{k:.7},hiutsuri:{k:.9,h:.5},bekko:{s:.55},muji:{},asagi:{h:.3,b:.85},goshiki:{h:.5,b:.42},
  shusui:{h:.35,b:.85,d:1},kumonryu:{k:.8,d:1},chagoi:{c:.85},tancho:{tan:1},ogon:{og:1,h:.5},platinum:{og:1},ginrin:{h:.55,gin:1}},KO_SMP={};
function koSample(v){if(KO_SMP[v])return KO_SMP[v];let f=koF().find(f=>f.rv&&koSt(f)===2&&(v==="ginrin"?f.g.gin:koVar(f.g)===v&&!f.g.gin));
  if(!f){const g=Object.assign({k:0,h:0,s:0,b:0,c:0,z:1,d:0,gin:0,og:0,tan:0},KO_SG[v]);f=Object.assign({i:800000+KO_VL.indexOf(v),g,fd:KO_ADULT},koBlobs(g,rng(KO_VL.indexOf(v)+5)));}
  return KO_SMP[v]=koPaint(f,2).toDataURL("image/webp",.8);}
const koKnown=v=>koF().some(f=>f.rv&&(koVar(f.g)===v||v==="ginrin"&&f.g.gin));
function koOpen(){if(!KS())koStart();koLoad();const was=panelIs("ko");openPanel("Пруд кои",koHtml(),"ko");if(!was)$("xpBody").scrollTop=0;koPaintEls();}
function koShowHtml(){const K=KS(),dk=dayKey(),sh=K.show&&K.show.d===dk?K.show:null;
  if(!koSunday())return`<p class="lead">Выставка карпов бывает по воскресеньям, у большого пруда. Каппа приносит синие чаши, старый тануки — свои очки. Выбери лучшего карпа и приходи.</p>
    <p>Побед: ${K.wins[0]} · вторых мест: ${K.wins[1]} · третьих: ${K.wins[2]}.</p><div class="row"><button class="btn" data-x="ko:open">← К садку</button></div>`;
  if(!sh){const ad=koAdults();return`<p class="lead">Судьи смотрят на три вещи: узор (кромка пятен, алое на голове, чистый хвост), размер и редкость породы. Выбери одного карпа.</p>
    <div class="ko-grid">${ad.map(f=>`<div class="ko-card"><canvas data-ko="${f.i}" width="300" height="110"></canvas><b>${f.nm}</b><span>${koVName(f)} · ${koCm(f)} см</span><div class="ko-bt"><button data-x="ko:enter:${f.i}">🏆 Выставить</button></div></div>`).join("")}</div>`;}
  const rv=koRivals(),ents=[koById(sh.f)||{nm:"—"},...rv],me=sh.sc[0],H=(s,e)=>` data-s="${s}"${e!=null?` data-e="${e}"`:""}`;
  const tot=sc=>Math.round((sc[0]+sc[1]+sc[2])*10)/10,ord=sh.sc.map((s,j)=>[tot(s),j]).sort((a,b)=>b[0]-a[0]||a[1]-b[1]).map(a=>a[1]);
  const bowls=ents.map((f,j)=>{const sc=sh.sc[j],pl=ord.indexOf(j)+1;
    return`<div class="ko-ent${j?"":" me"}"><div class="ko-bowl"><div style="animation-delay:-${j*4.3}s"><canvas ${j?`data-kr="${j-1}"`:`data-ko="${f.i}"`} width="300" height="110"></canvas></div></div><b>${f.nm}</b><br>${f.g?koVName(f):""}<br>${j?f.own:"Муся и ты"}
      <div class="ko-sc"><span${H(1)}>Узор</span><i${H(1)}>${sc[0]}</i><span${H(2)}>Размер</span><i${H(2)}>${sc[1]}</i><span${H(3)}>Редкость</span><i${H(3)}>${sc[2]}</i></div>
      <div class="ko-pl"><span${H(4)}>${pl<=3?itemThumb(IT["ko_rib"+pl],22,36,";vertical-align:middle")+` ${pl} место`:"4 место"}</span></div></div>`;}).join("");
  const jd=[["m_kappa",`<span${H(0,1)}>«Каппа ставит синие чаши и долго смотрит в воду.»</span><span${H(1,3)}>«${koLine("pat",me[0])}»</span><span${H(3)}>«${koLine("rar",me[2])}»</span>`],
    ["m_tanuki",`<span${H(0,2)}>«Старый тануки протирает очки рукавом.»</span><span${H(2)}>«${koLine("size",me[1])}»</span>`]];
  const fin=`<div${H(4)}><p class="ko-msg">${sh.pl===1?"🏆 Первое место! Каппа хлопает в перепончатые ладоши.":sh.pl<4?`${sh.pl} место — достойно. В следующее воскресенье — снова.`:"Четвёртое место. Тануки шепчет: «Подрасти его — и приходи»."}${sh.got&&sh.got.length?" Награда: "+sh.got.join(", ")+" — в «🧺 Вещи».":""}</p><div class="row"><button class="btn" data-x="ko:open">← К садку</button></div></div>`;
  return`<div class="ko-sw"><div class="ko-show">${bowls}</div>${jd.map(([m,t])=>`<div class="ko-jd"><img src="assets/mon/${m}.webp" alt=""><p>${t}</p></div>`).join("")}${fin}</div>`;}
function koStep(stp){for(const el of $("xpBody").querySelectorAll("[data-s]")){const s=+el.dataset.s,e=el.dataset.e!=null?+el.dataset.e:99;el.hidden=!(stp>=s&&stp<e);}}
function koShow(){koLoad();clearInterval(KO_TIM);const was=panelIs("ko_show");openPanel("Выставка карпов",koShowHtml(),"ko_show");if(!was)$("xpBody").scrollTop=0;koPaintEls();
  const stp=()=>KO_ANIM?Math.floor((Date.now()-KO_ANIM.t)/1600):99;koStep(stp());
  if(KO_ANIM){let last=-1;KO_TIM=setInterval(()=>{if(!panelIs("ko_show")){clearInterval(KO_TIM);KO_ANIM=null;return;}const s=stp();
    if(s!==last){last=s;koStep(s);tone(660+s*110,.12,"sine",.04);if(s>=4){clearInterval(KO_TIM);KO_ANIM=null;if(KS().show.pl===1)chime([784,988,1175,1568]);}}},250);}}

// ── the tub in the courtyard (left of Musya, behind the zen patch), the fry circling in it
function koTubF(){const x=visX(KO_TB.x,KO_TB.w*.62),oc=curRow;curRow=KO_TB.y;const [bx,by]=imgToStage(x,KO_TB.y,CAT_D),[,ty]=imgToStage(x,KO_TB.y-100,CAT_D);curRow=oc;const k=(by-ty)/100;return{bx,by,k,s:k*KO_TB.w/240};}
const KO_FRY=[];   // per-fish swim phase in the tub
hook("draw",(t,front)=>{if(S.room!=="courtyard"||!KS()||!koIm||scene.on)return;if((KO_TB.y>catLineY()+6)!==front)return;
  const F=koTubF(),s=F.s,x0=F.bx-120*s,y0=F.by-140*s;ctx.drawImage(koIm,0,0,240,150,x0,y0,240*s,150*s);
  const cx=x0+120*s,cy=y0+58*s,rx=94*s,ry=22*s,fr=koFry().slice(0,KO_NURSE),hungry=fr.length&&KS().fed!==dayKey(),fe=t-koFeedT;
  ctx.save();ctx.beginPath();ctx.ellipse(cx,cy,rx,ry,0,0,Math.PI*2);ctx.clip();
  fr.forEach((f,i)=>{const q=KO_FRY[i]||(KO_FRY[i]={a:rand(0,6.28),w:rand(.25,.5)*(Math.random()<.5?-1:1),r:rand(.3,.85)});const w=q.w*(fe<6?2.2:1),a=q.a+t*w,px=cx+Math.cos(a)*rx*q.r,py=cy+Math.sin(a)*ry*q.r;
    const hd=Math.atan2(Math.cos(a)*ry*q.r*Math.sign(w),-Math.sin(a)*rx*q.r*Math.sign(w)),L=(koSt(f)?44:26)*s;
    ctx.save();ctx.translate(px,py);ctx.scale(1,.5);ctx.rotate(hd);ctx.globalAlpha=.92;ctx.drawImage(koImg(f),-L/2,-L*KO_H/KO_W/2,L,L*KO_H/KO_W);ctx.restore();});
  if(hungry||fe<4)for(let i=0;i<3;i++){const e=((t*.45+i/3)%1),bx=cx+Math.sin(i*2.1+Math.floor(t*.45+i/3)*1.7)*rx*.6,by=cy+Math.cos(i*1.3)*ry*.4;
    ctx.strokeStyle=`rgba(220,232,232,${.45*(1-e)})`;ctx.lineWidth=1;ctx.beginPath();ctx.ellipse(bx,by,(3+18*e)*s,(1+5*e)*s,0,0,Math.PI*2);ctx.stroke();}
  ctx.restore();});
hook("hit",(x,y)=>{if(S.room!=="courtyard"||!KS()||!koIm||scene.on)return;const F=koTubF();if(Math.abs(x-F.bx)>112*F.s||y<F.by-118*F.s||y>F.by+4*F.s)return;
  audioInit();sfx("splash");if(!petAway())react("😺",1.4);koOpen();return true;});

// ── hooks: tray button, clicks, hub card, dots, away line, album, boot
hook("tray",(tray,room)=>{if(room!=="courtyard"||(S.trayMode[room]||"play")!=="play")return;const el=tray.querySelector(".items");if(!el)return;
  const hg=KS()&&koFry().length&&KS().fed!==dayKey(),h=`<button class="item wide" data-x="ko:open"><span class="ico">🐟</span><span class="nm">Карпы${hg?" · 🍚":""}</span></button>`,c=el.querySelector('[data-place="koi"]');
  if(c)c.insertAdjacentHTML("beforebegin",h);else el.insertAdjacentHTML("beforeend",h);});
hook("click",(key)=>{if(!key.startsWith("ko:"))return;const [,a,v]=key.split(":"),i=+v;
  if(a==="open"){KO_VIEW=null;closePanel();koOpen();return true;}
  if(a==="show"){koShow();return true;}
  if(a==="enter"){koEnter(i);koShow();return true;}
  if(a==="look"){KO_VIEW=i;}else if(a==="back")KO_VIEW=null;else if(a==="sel")koSel(i);else if(a==="spawn")koSpawn();else if(a==="feed")koFeed();else if(a==="pond")koPond(i);
  else if(a==="free"){const b=document.querySelector(`[data-x="ko:free:${i}"]`);if(b&&!b.dataset.ok){b.dataset.ok=1;b.textContent="Точно отпустить?";return true;}koFree(i);}
  koOpen();ui();return true;});
hook("hub",()=>{const K=KS();
  if(!K)return`<div class="hubc"><h4>🐟 Пруд кои <i>錦鯉</i></h4><p>У пруда стоит пустой деревянный садок. Каппа предлагает разводить карпов: подбирать пары, растить мальков и показывать лучших на воскресной выставке.</p><div class="row"><button class="btn primary" data-x="ko:open">Взять садок</button></div></div>`;
  const fr=koFry(),hg=fr.length&&K.fed!==dayKey(),nd=(7-today().getDay())%7,sh=K.show&&K.show.d===dayKey(),dsc=(S.ext.disc||{}).koi||{};
  return`<div class="hubc"><h4>🐟 Пруд кои <i>錦鯉</i></h4><p>Карпов: ${koAdults().length}${fr.length?` · мальков в садке: ${fr.length} — ${hg?"ждут корма":"сыты ✓"}`:""}. Пород открыто: ${KO_VL.filter(v=>dsc[v]).length} из ${KO_VL.length}.</p>
    <p>${K.br===dayKey()?"Нерест сегодня уже был.":"Сегодня можно устроить нерест."} ${koSunday()?(sh?`Выставка: ${K.show.pl} место.`:"<b>Сегодня выставка карпов!</b>"):`Выставка через ${koW(nd,["день","дня","дней"])}.`}</p>
    <div class="row">${hg?`<button class="btn primary" data-x="ko:feed">🍚 Покормить мальков</button>`:""}<button class="btn" data-x="ko:open">Открыть садок</button>${koSunday()&&!sh?`<button class="btn primary" data-x="ko:show">🏆 Выставка</button>`:""}</div></div>`;});
const koHungry=()=>{const K=KS();return !!K&&koFry().length>0&&K.fed!==dayKey();};
hook("hubDot",()=>koHungry()||!!KS()&&koSunday()&&!(KS().show&&KS().show.d===dayKey())&&koAdults().length>0);
hook("tabDot",r=>r==="courtyard"&&koHungry());
hook("away",ms=>koHungry()&&ms>6*36e5?{i:"🐟",t:"Мальки в садке у пруда ждут корма"}:null);
hook("album",el=>{const K=KS();if(!K)return;const dsc=(S.ext.disc||{}).koi||{};
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Пруд кои</h3><p class="lead">Пород выведено: ${KO_VL.filter(v=>dsc[v]).length} из ${KO_VL.length}. Карпов: ${koF().length}. Побед на выставке: ${K.wins[0]}.</p><div class="coll">${KO_VL.map(v=>`<div class="ci${dsc[v]?" on":""}"${dsc[v]?"":' style="opacity:.45"'}>${dsc[v]?`<img src="${koSample(v)}" alt="" style="height:30px;margin:11px 0">`:'<span style="font-size:22px;line-height:52px">？</span>'}<span style="font-size:11px">${dsc[v]?KO_V[v][0]:"???"}</span></div>`).join("")}</div>`);});
hook("boot",()=>{const K=KS();if(!K)return;koLoad();for(const f of K.f)if(f.pond&&koSt(f)===2)koPondAdd(f);});
X.ko={open:koOpen,show:koShow,st:KS,start:koStart,img:koImg,rivals:koRivals,tub:koTubF,
  pair(a,b){KS().sel=[a,b];koSpawn();koOpen();},feed(){koFeed();koOpen();},
  grow(n){for(const f of koFry()){for(let k=0;k<n;k++){f.fd++;if(f.fd===3&&!f.rv)koReveal(f);if(f.fd===KO_ADULT)f.ad=dayKey();}}KS().fed=null;KS().br=null;save();},
  enter(i){koEnter(i);koShow();},pond(i){koPond(i);}};
}
