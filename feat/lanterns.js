{
// ───────────────────────── «Фонарики дней»: seven paper lanterns under the veranda eaves ─────────────────────────
// Every calendar day the player opens the game one more lantern lights (up to 7); every missed day puts one out.
// On the day the seventh lights, a rare seasonal guest comes to the veranda with a gift; then a new circle begins.
const LAN=S.ext.lan||(S.ext.lan={n:0,day:null,cyc:0,met:{},rg:null,done:null});LAN.met=LAN.met||{};
const LSPR={"0on":[588,0],"0off":[674,0],"1on":[760,0],"1off":[846,0],"2on":[932,0],"2off":[0,182],"3on":[86,182],"3off":[172,182],"4on":[258,182],"4off":[344,182],"5on":[430,182],"5off":[516,182],"6on":[602,182],"6off":[688,182]},LW=84,LH=132,RGA=[1024,436];
const ORD=["первый","второй","третий","четвёртый","пятый","шестой","седьмой"],ORDG=["первого","второго","третьего","четвёртого","пятого","шестого","седьмого"];
const NOTE=[523,587,659,784,880,1047,1175];
function lPl(n,a,b,c){n=Math.abs(n)%100;const m=n%10;return n>10&&n<20?c:m===1?a:m>=2&&m<=4?b:c;}

// ── the four rare guests, one per season ──
const RG=[
 {id:"yuki",mon:"m_rg_yuki",n:"Юки-онна",h:500,mo:[12,1,2],when:"Зимой",fx:"snow",gifts:["rg_yuki_usagi","rg_yuki_comb"],
  hi:"Ш-ш-ш… я пришла вместе с метелью. Семь огоньков на вашей веранде горели так ровно, что я не смогла пройти мимо. Не бойся, маленькая, сегодня я ничего не заморожу.",
  bye:"Юки-онна улыбается одними губами. «Только никому не рассказывай, откуда это», — и тает в снежной пыли."},
 {id:"kodama",mon:"m_rg_kodama",n:"Кодама",h:340,mo:[3,4,5],when:"Весной",fx:"leaf",gifts:["rg_kodama_sprout","rg_kodama_rope"],
  hi:"А-у… а-у… Это я отвечаю вам эхом из леса. Я живу в старом дереве за садом уже триста вёсен, и ваши фонарики видно из самой чащи.",
  bye:"Кодама кивает, и где-то в горах эхо повторяет: «Берегите старые деревья… деревья…»"},
 {id:"amabie",mon:"m_rg_amabie",n:"Амабиэ",h:410,mo:[6,7,8],when:"Летом",fx:"sea",gifts:["rg_amabie_print","rg_amabie_float"],
  hi:"Я вышла из моря Хиго, где светилась по ночам. Людям я сказала: будут шесть урожайных лет, а если придёт мор — покажите всем мой портрет.",
  bye:"Амабиэ ныряет в темноту сада, будто в море. Пахнет солью, и на досках веранды блестят капли."},
 {id:"usagi",mon:"m_rg_usagi",n:"Цуки-но усаги",h:390,mo:[9,10,11],when:"Осенью",fx:"moon",gifts:["rg_usagi_usu","rg_usagi_dango"],
  hi:"Пон-пон! Я спустился с луны по лунной дорожке — ваши фонарики видно даже оттуда. Там, наверху, я толку моти с тех пор, как отдал всё, что имел, голодному путнику.",
  bye:"Заяц подпрыгивает — и вот его уже нет. Только луна над садом кажется чуть ярче."}
];
for(const g of RG)MON[g.mon]={m_rg_yuki:[340,620],m_rg_kodama:[300,420],m_rg_amabie:[360,480],m_rg_usagi:[360,480]}[g.mon];
BESTIARY.push(
 ["rg_yuki","m_rg_yuki","Юки-онна","Снежная женщина: бледная, в белом кимоно, приходит в метель, и дыхание её замораживает. В «Кайдане» Лафкадио Хирна (1904) она пощадила юного дровосека, взяв с него слово молчать."],
 ["rg_kodama","m_rg_kodama","Кодама","Дух старого дерева. Горное эхо — это кодама отвечает путнику. Срубить такое дерево — к беде, поэтому его опоясывают верёвкой симэнава. Нарисован Ториямой Сэкиэном в 1776 году."],
 ["rg_amabie","m_rg_amabie","Амабиэ","Морской дух с птичьим клювом, длинными волосами и чешуёй на трёх ногах. В 1846 году вышел из моря в провинции Хиго, предсказал шесть урожайных лет и велел показывать людям свой портрет, если придёт мор."],
 ["rg_usagi","m_rg_usagi","Цуки-но усаги","Лунный заяц. По древней притче, заяц бросился в костёр, чтобы накормить голодного старика, и тот — а это был бог Тайсякутэн — поселил его на луне. В Японии в пятнах луны видят зайца, что толчёт в ступке моти."]);
STAMPS.push(["lan_seven","灯","Семь фонариков","Зажечь все семь фонариков на веранде"]);
const GI=[["rg_yuki_usagi","Снежный зайчик, который не тает",150,104,"b",232,316],["rg_yuki_comb","Ледяной гребень Юки-онны",150,84,"b",384,316,[75,30]],
 ["rg_kodama_sprout","Росток векового дерева",130,160,"b",142,0],["rg_kodama_rope","Верёвка симэнава со священного дерева",230,120,"t",0,316],
 ["rg_amabie_print","Листок с портретом Амабиэ",140,180,"t",0,0],["rg_amabie_float","Стеклянный поплавок из моря Хиго",124,124,"b",774,182],
 ["rg_usagi_usu","Лунная ступка с пестиком",170,160,"b",274,0],["rg_usagi_dango","Цукими-данго с луны",140,150,"b",446,0,[70,60]]];
addItems(GI.map(([id,n,w,h,a,x,y,glow])=>Object.assign({id,n,c:"Дары редких гостей",w,h,a,p:0,at:["rg",x,y],src:"🏮 дар редкого гостя",
  hint:"Зажги все 7 фонариков на веранде"},glow?{glow}:{})),{rg:RGA});

document.head.insertAdjacentHTML("beforeend",`<style>
.lan-row{display:flex;gap:4px;align-items:flex-start;margin:4px 0 8px;padding:8px 6px 4px;border-top:2px solid #2a2018;border-radius:2px}
.lan-row span{width:30px;height:47px;background:url(assets/items/atlas_rg.webp) no-repeat;flex:none}
.lan-row span.on{filter:drop-shadow(0 0 7px rgba(255,170,80,.75))}
.lan-row span:nth-child(even){margin-top:7px}
.lan-g{display:flex;gap:10px;align-items:center}.lan-g img{height:64px;flex:none;filter:drop-shadow(0 0 10px rgba(255,220,160,.25))}
</style>`);

function dnum(k){const [y,m,d]=k.split("-").map(Number);return Math.round(Date.UTC(y,m-1,d)/864e5);}
function seasonG(){const m=today().getMonth()+1;return RG.find(g=>g.mo.includes(m));}
function rgDef(){return LAN.rg&&RG.find(g=>g.id===LAN.rg.id);}
// a new calendar day: light one, put out one per missed day (never while a guest waits), start a new circle after a visit
let EV=null;
function lanDay(){
  const k=dayKey();if(LAN.day===k)return null;
  const gap=LAN.day?dnum(k)-dnum(LAN.day):1;if(gap<=0){LAN.day=k;save();return null;}
  const ev={out:0,cyc:false,first:!LAN.day};
  if(LAN.done||(LAN.n>=7&&!LAN.rg)){LAN.n=0;LAN.done=null;LAN.cyc++;ev.cyc=true;}
  else if(!LAN.rg){ev.out=Math.min(LAN.n,gap-1);LAN.n-=ev.out;}
  LAN.n=Math.min(7,LAN.n+1);ev.n=LAN.n;LAN.day=k;
  if(LAN.n===7&&!LAN.rg){const g=seasonG();LAN.rg={id:g.id,day:k,st:"coming",at:Date.now()+rand(5,10)*1000};ev.guest=g.id;award("lan_seven");}
  save();return ev;
}
function lanLine(ev){
  if(ev.guest){const g=RG.find(x=>x.id===ev.guest);return`Зажёгся седьмой фонарик! На его свет уже спешит редкий гость — ${g.n}.`;}
  if(ev.first)return"На веранде зажёгся первый фонарик. Приходи каждый день — их семь.";
  if(ev.cyc)return"Начался новый круг: на веранде зажёгся первый фонарик.";
  if(ev.out)return`Пока тебя не было, ${ev.out===1?"погас один фонарик":`погасли ${ev.out} ${lPl(ev.out,"фонарик","фонарика","фонариков")}`}, но сегодня зажёгся новый — горит ${ev.n} из 7.`;
  return`На веранде зажёгся ${ORD[ev.n-1]} фонарик — горит ${ev.n} из 7.`;
}
function lanToast(ev){toast(ev.guest?"🏮 Горят все семь фонариков!":ev.out?`🏮 Фонарики: горит ${ev.n} из 7`:`🏮 Зажёгся фонарь ${ORDG[ev.n-1]} дня`);chime([NOTE[ev.n-1],NOTE[ev.n-1]*1.5]);}
hook("away",()=>{if(!EV||EV.told)return null;EV.told=1;return{i:"🏮",t:lanLine(EV)};});

// ── where the lanterns hang: spread over the visible part of the eaves, making room for a hanging wind chime ──
const SLOT={key:"",xs:[]},TOPS=[196,222,204,230,200,226,210],EAVE=96,LD=.92,LSC=.95;
function slots(){
  const sel=S.decor.engawa||{},obs=[];
  for(const sp of DECOR.engawa||[]){const it=sp.items.find(i=>i.id===sel[sp.k]);if(it&&DMETA[it.id]&&DMETA[it.id][2]==="t"){const x=it.x+(S.dpos[it.id]||[0])[0],w=DMETA[it.id][0]/2+34;obs.push([x-w,x+w]);}}
  const key=view.W+"x"+view.H+"|"+BGM.k.toFixed(4)+"|"+obs.map(o=>o[0]|0).join(",");if(SLOT.key===key)return SLOT.xs;
  const a=Math.max(150,visX(-1e5,60)),b=Math.min(1330,visX(1e5,60));let segs=[[a,b]];
  for(const [o0,o1] of obs)segs=segs.flatMap(([s0,s1])=>o1<=s0||o0>=s1?[[s0,s1]]:[[s0,o0],[o1,s1]].filter(([u,v])=>v-u>4));
  let L=segs.reduce((s,[u,v])=>s+v-u,0);if(L<6*70){segs=[[a,b]];L=b-a;}
  const xs=[];for(let i=0;i<7;i++){let s=L*i/6;for(const [u,v] of segs){if(s<=v-u+1e-6){xs.push(u+s);break;}s-=v-u;}}
  SLOT.key=key;SLOT.xs=xs;return xs;
}
const WOB=[0,0,0,0,0,0,0].map(()=>-9);let lanIm=null,glowCv=null;
function glow(){if(glowCv)return glowCv;const c=document.createElement("canvas");c.width=c.height=128;const g=c.getContext("2d"),gr=g.createRadialGradient(64,64,0,64,64,64);
  gr.addColorStop(0,"rgba(255,196,110,.9)");gr.addColorStop(.35,"rgba(255,150,60,.35)");gr.addColorStop(1,"rgba(255,140,50,0)");g.fillStyle=gr;g.fillRect(0,0,128,128);return glowCv=c;}
function lanGeo(i,t){const x=slots()[i],top=TOPS[i],k=BGM.k,[px,py]=imgToStage(x,EAVE,LD),[,ly]=imgToStage(x,top,LD),wind=weather.on?2:1,w=t-WOB[i];
  const a=(.035*Math.sin(t*1.1+i*1.9)+.015*Math.sin(t*2.7+i))*wind+(w<3?.22*Math.exp(-w*1.6)*Math.sin(w*9):0);return{px,py,off:ly-py,w:LW*LSC*k,h:LH*LSC*k,a};}
function drawLanterns(t){
  if(!lanIm)return;const night=dayTint()[1],lit=LAN.n;
  for(let i=0;i<7;i++){const on=i<lit,G=lanGeo(i,t),fl=.86+.09*Math.sin(t*7.3+i*2.1)+.05*Math.sin(t*13.7+i);
    ctx.save();ctx.translate(G.px,G.py);ctx.rotate(G.a);
    ctx.strokeStyle="rgba(24,18,14,.85)";ctx.lineWidth=Math.max(1,1.4*BGM.k*2);ctx.beginPath();ctx.moveTo(0,-40);ctx.lineTo(0,G.off+2);ctx.stroke();
    if(on){const R=(night?300:150)*BGM.k;ctx.globalCompositeOperation="lighter";ctx.globalAlpha=(night?.55:.22)*fl;ctx.drawImage(glow(),-R,G.off+G.h*.52-R,R*2,R*2);ctx.globalCompositeOperation="source-over";ctx.globalAlpha=1;}
    const s=LSPR[i+(on?"on":"off")];ctx.drawImage(lanIm,s[0],s[1],LW,LH,-G.w/2,G.off,G.w,G.h);
    if(on){ctx.globalCompositeOperation="lighter";ctx.globalAlpha=.3*fl*(night?1:.6);const r=G.w*.55;ctx.drawImage(glow(),-r,G.off+G.h*.52-r,r*2,r*2);ctx.globalCompositeOperation="source-over";ctx.globalAlpha=1;}
    ctx.restore();}
}
function lanHit(x,y){const t=now();for(let i=0;i<7;i++){const G=lanGeo(i,t),cx=G.px-Math.sin(G.a)*(G.off+G.h/2),cy=G.py+G.off+G.h/2;
  if(Math.abs(x-cx)<G.w*.62&&Math.abs(y-cy)<G.h*.58)return i;}return -1;}
function tapLantern(i){
  WOB[i]=now();const on=i<LAN.n,d=i-LAN.n+1;
  if(on){chime([NOTE[i],NOTE[i]*1.5]);toast(`🏮 Фонарь ${ORDG[i]} дня`);}
  else{tone(NOTE[i]/2,.5,"triangle",.035);toast(LAN.rg||LAN.done?`Фонарь ${ORDG[i]} дня ждёт нового круга`:d===1?`Фонарь ${ORDG[i]} дня зажжётся завтра`:`Фонарь ${ORDG[i]} дня — через ${d} ${lPl(d,"день","дня","дней")}`);}
}

// ── the rare guest on the veranda ──
const GV={side:0,t0:0,leave:0,gone:null};const GY=1222;
function guestX(){if(!GV.side){const l=visX(-1e5,0),r=visX(1e5,0),pi=(pet.x-BGM.dx)/BGM.k;GV.side=pi<(l+r)/2?1:-1;}
  const l=visX(-1e5,0),r=visX(1e5,0);return clamp(GV.side>0?r-170:l+170,300,1340);}
function guestHere(){return LAN.rg&&LAN.rg.st==="here";}
function drawRG(t,front){
  const g=GV.gone||(guestHere()?rgDef():null);if(!g||scene.on||(GY>catLineY()+6)!==front)return;
  if(!GV.t0)GV.t0=t;let a=clamp((t-GV.t0)/1.6,0,1);if(GV.gone){a=1-clamp((t-GV.leave)/2,0,1);if(a<=0){GV.gone=null;return;}}
  const x=guestX(),bob=g.fx==="moon"?-Math.abs(Math.sin(t*2.2))*10:Math.sin(t*1.4)*6,k=BGM.k,[sx,sy]=imgToStage(x,GY,CAT_D);
  ctx.save();ctx.globalCompositeOperation="lighter";ctx.globalAlpha=a*(.35+.08*Math.sin(t*2));const R=g.h*.75*k;
  const c=g.fx==="snow"?"200,220,255":g.fx==="leaf"?"170,230,140":g.fx==="sea"?"120,230,210":"255,230,160",gr=ctx.createRadialGradient(sx,sy-R*.7,0,sx,sy-R*.7,R);
  gr.addColorStop(0,`rgba(${c},.45)`);gr.addColorStop(1,`rgba(${c},0)`);ctx.fillStyle=gr;ctx.fillRect(sx-R,sy-R*1.7,R*2,R*2);ctx.restore();
  ctx.fillStyle=`rgba(0,0,0,${.28*a})`;ctx.beginPath();ctx.ellipse(sx,sy+2,g.h*.28*k,g.h*.05*k,0,0,Math.PI*2);ctx.fill();
  drawMon(g.mon,x,GY+bob,g.h,CAT_D,a);
  for(let i=0;i<9;i++){const u=((t*(g.fx==="snow"?.12:.16)+i/9)%1),px=sx+Math.sin(i*2.4+t*.7)*g.h*.4*k,py=g.fx==="snow"?sy-g.h*k*(1.1-u*1.1):sy-g.h*k*u*1.1;
    ctx.globalAlpha=a*Math.sin(Math.PI*u)*.8;ctx.fillStyle=g.fx==="snow"?"#f4f8ff":g.fx==="leaf"?"#b6e08a":g.fx==="sea"?"#9ff0e0":"#fff0c0";ctx.beginPath();ctx.arc(px,py,(g.fx==="snow"?2.2:1.6)*Math.max(1,k*2),0,Math.PI*2);ctx.fill();}
  ctx.globalAlpha=1;
  if(!GV.gone&&a>.6){const [bx,by]=imgToStage(x+g.h*.3,GY-g.h*1.02+bob,CAT_D),r=16*view.s;ctx.save();ctx.globalAlpha=a*.95;ctx.fillStyle="rgba(238,233,220,.93)";
    ctx.beginPath();ctx.arc(bx,by,r,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.arc(bx-r*.95,by+r*1.05,r*.2,0,Math.PI*2);ctx.fill();drawEmoji(ctx,"🏮",bx,by+1,r*1.15);ctx.restore();}
}
function rgHit(x,y){const g=guestHere()&&rgDef();if(!g||S.room!=="engawa"||scene.on)return false;const [sx,sy]=imgToStage(guestX(),GY,CAT_D),h=g.h*BGM.k*1.1,w=h*.62;
  if(x>sx-w/2&&x<sx+w/2+h*.25&&y>sy-h&&y<sy+10){openRG();return true;}return false;}
function openRG(){
  const g=rgDef();if(!g)return;const gift=g.gifts.find(id=>!S.owned.has(id));if(!petAway())react("😺",1.6);
  if(!ST.seen.includes("rg_"+g.id)){ST.seen.push("rg_"+g.id);setTimeout(()=>toast("Новая запись в бестиарии"),600);}
  dlg({head:g.n,text:g.hi,img:`<img src="assets/mon/${g.mon}.webp" alt="" style="height:64px">`,ok:gift?"Принять дар":"Поклониться",no:"Позже",onOk:()=>meetRG(g,gift)});
}
function meetRG(g,gift){
  if(gift)S.owned.add(gift);LAN.met[g.id]=(LAN.met[g.id]||0)+1;disc("rareguest",g.id);
  S.needs.joy=clamp(S.needs.joy+15,0,100);chime([1046,1318,1568,2093]);if(!petAway()){burst(10);react("😻",2.4);}
  dlg({head:g.n,text:g.bye+(gift?` Остался дар: «${IT[gift].n}» — ищи в 🧺 Вещи → Дары редких гостей.`:" Все дары этого гостя уже у тебя — он приходил просто повидаться."),img:gift?itemThumb(IT[gift],70,56):"",ok:"До встречи"});
  GV.gone=g;GV.leave=now();LAN.rg=null;LAN.done=dayKey();save();tabDots();hubDot();
}

// ── hooks ──
hook("boot",()=>{atlasImg("rg",im=>{lanIm=im;});EV=lanDay();GV.bootT=now();});
hook("sec",()=>{
  if(LAN.day!==dayKey()){const ev=lanDay();if(ev){EV=ev;ev.told=1;lanToast(ev);}}
  if(EV&&!EV.told&&now()-(GV.bootT||0)>(EV.first?9.5:5)&&!(X.ret&&X.ret.R.pending)&&!scene.on&&!overlaysOpen()){EV.told=1;lanToast(EV);}
  const q=LAN.rg;if(q&&q.st==="coming"&&Date.now()>q.at&&!scene.on&&!overlaysOpen()&&(!EV||EV.told)){q.st="here";GV.t0=0;GV.side=0;save();chime([659,784,1047]);
    toast(S.room==="engawa"?"🏮 На свет фонариков кто-то пришёл":"🏮 На веранду пришёл редкий гость");tabDots();}
});
hook("draw",(t,front)=>{if(S.room!=="engawa")return;if(front)drawLanterns(t);drawRG(t,front);});
hook("hit",(x,y)=>{if(S.room!=="engawa")return false;if(rgHit(x,y))return true;const i=lanHit(x,y);if(i>=0){tapLantern(i);return true;}return false;});
hook("room",id=>{if(id==="engawa"){GV.t0=0;GV.side=0;}});
hook("hubDot",()=>guestHere());
hook("tabDot",r=>r==="engawa"&&guestHere());
hook("hub",()=>{
  const g=rgDef()||seasonG(),n=LAN.n,f=v=>(v*.36).toFixed(1);
  const row=[0,1,2,3,4,5,6].map(i=>{const s=LSPR[i+(i<n?"on":"off")];return`<span class="${i<n?"on":""}" style="background-position:-${f(s[0])}px -${f(s[1])}px;background-size:${f(RGA[0])}px ${f(RGA[1])}px"></span>`;}).join("");
  const q=LAN.rg,left=7-n;
  const st=q?`${g.n} уже в пути к веранде…`:LAN.done===dayKey()?"Гость уже побывал у вас. Завтра начнётся новый круг.":
    `Ещё ${left} ${lPl(left,"день","дня","дней")} подряд — и ${g.n} придёт.`;
  return`<div class="hubc"><h4>🏮 Фонарики дней <i>灯</i></h4><div class="lan-row">${row}</div>
  <p>Каждый день, когда ты заходишь, на веранде зажигается ещё один фонарик, а пропущенный день гасит один. Горит ${n} из 7.</p>
  <div class="lan-g"><img src="assets/mon/${g.mon}.webp" alt=""><p>${q&&q.st==="here"?`<b>${g.n} ждёт на веранде!</b> Гость пришёл на свет семи фонариков — нажми на него, чтобы получить дар.`:`${g.when} на свет семи фонариков приходит <b>${g.n}</b>. ${st}`}</p></div>
  <div class="row"><button class="btn" data-x="lan:go">На веранду</button></div></div>`;
});
hook("click",k=>{if(k==="lan:go"){closePanel();goRoom("engawa");return true;}});
// test handles: X.lan.set({n,day}) then X.lan.day() simulates coming back on another day
X.lan={S:LAN,day:()=>{const ev=lanDay();if(ev){EV=ev;}return ev;},arrive:()=>{if(LAN.rg){LAN.rg.at=0;}},slots,open:openRG,
  pt:i=>{const G=lanGeo(i,now());return[G.px,G.py+G.off+G.h/2];},gx:()=>{const g=rgDef();const [x,y]=imgToStage(guestX(),GY,CAT_D);return[x,y-(g?g.h:300)*BGM.k*.5];},
  set:o=>Object.assign(LAN,o),back:n=>{const d=today();d.setDate(d.getDate()-n);LAN.day=dayKey(d);}};
}
