{ // «Рисовое поле» (add-on rice): three terraced paddies on the hill behind the house, one cycle ≈ 3 weeks of real days.
// Steps: flood the paddies → plant seedlings along the rows → pull weeds (every 2–3 days; skipping only slows growth)
// → rice grows by real days → reap with a sickle → 2 days on the hasa-gake rack → thresh → own rice → mochitsuki with a yōkai.
// Art: art/rice_art.py → assets/bg/ri_field.webp (900×1500, transparent sky), assets/items/atlas_ri.webp
const RI_A=[1000,638];
const RI_R={"nae":[378,538,46,58],"g1":[642,322,72,106],"g2":[388,322,96,152],"gold":[282,322,104,160],"stub":[426,538,56,32],"weed":[318,538,58,66],"sheaf":[574,322,66,126],"hang":[486,322,86,132],"rack":[114,0,400,300],"kakashi":[516,0,176,280],"kasa":[0,538,184,100],"kakeho":[694,0,132,236],"usu":[0,322,280,214],"kine":[0,0,112,320],"kama":[716,322,122,104],"tawara":[186,538,130,100]};
addItems([{id:"ri_kasa",n:"Соломенная шляпа",c:"Рисовое поле",w:184,h:100,a:"b",p:0,at:["ri",0,538],src:"🌾 рисовое поле",hint:"Шляпу дают за первую посадку риса: Дворик → 🌾 Рисовое поле"},
 {id:"ri_kakeho",n:"Сноп риса какэхо",c:"Рисовое поле",w:132,h:236,a:"t",p:0,at:["ri",694,0],src:"🌾 рисовое поле",hint:"Первые колосья вешают в дом после жатвы: сожни рис на рисовом поле"},
 {id:"ri_kakashi",n:"Пугало какаси",c:"Рисовое поле",w:176,h:280,a:"b",p:0,at:["ri",516,0],src:"🌾 рисовое поле",hint:"Пугало переедет в дом, когда натолчёшь моти из своего риса"}],{ri:RI_A});
FATL.ri={w:RI_A[0],h:RI_A[1],r:{v_ri_kome:[186,538,130,100]}};
FOOD.v_ri_kome={n:"Свой рис",k:"veg"};
STAMPS.push(["ri_plant","苗","Первая посадка","Посади рассаду на рисовом поле"],["ri_harvest","稲","Первая жатва","Сожни свой рис серпом"],["ri_mochi","餅","Свои моти","Натолки моти из своего риса"]);
const RI_PAD=[[585,700,290,330,26,30],[770,935,360,400,34,40],[1015,1225,425,470,44,50]];   // top y, bottom y, half-widths, contour bow, wall (= art/rice_art.py)
const RI_GROW=16,RI_LEN=21,RI_DRY=2,RI_SLOTS=12;
const RI_E=(p,u,b)=>{const P=RI_PAD[p];return[450+u*P[b?3:2],P[b?1:0]+P[4]*(1-u*u)];};
const RI_POLY=RI_PAD.map((P,p)=>{const a=[];for(let i=0;i<=24;i++)a.push(RI_E(p,-1+i/12,0));for(let i=24;i>=0;i--)a.push(RI_E(p,-1+i/12,1));return a;});
const RI_H=[];[[2,6],[3,7],[3,8]].forEach(([nr,nc],p)=>{for(let j=0;j<nr;j++){const v=nr===2?[.42,.86][j]:[.3,.6,.9][j];
  for(let i=0;i<nc;i++){const u=-.82+1.64*(i+.5+(j%2?.22:-.22))/nc,[ax,ay]=RI_E(p,u,0),[bx,by]=RI_E(p,u,1),x=mix(ax,bx,v),y=mix(ay,by,v);RI_H.push({p,x,y,f:.5+.5*(y-585)/685});}}});
const RI_N=RI_H.length;
const RI_SL=[0,1].flatMap(r=>[590,625,660,720,755,790].map(x=>[x,r?1346:1280]));   // sheaf slots on the two rack poles
const RI_SC={x:84,y:1022,h:232};    // the scarecrow on the ridge between the middle and the lower paddy
const RI_BI={sit:[546,594,105,78,60,76],peck:[0,694,108,69,59,66],fly:[657,472,116,103,63,78]};   // sparrows from the feeder atlas (bi)
const RI={im:null,bg:null,bi:null,cache:{},sky:{}};
const riS=()=>S.ext.rice||(S.ext.rice={st:"fallow",c:0,fl:[0,0,0],pl:[],cut:[],th:[],d0:0,g:0,gl:0,wn:0,wd:[],dy:0,sc:0,lz:0,h:0,mo:0});
const riDN=()=>Math.round(Date.parse(dayKey()+"T00:00:00Z")/864e5);
const riDay=()=>riDN()-riS().d0+1;
const riKome=()=>S.pantry.v_ri_kome||0;
const riCnt=a=>a.filter(Boolean).length;
const riDryLeft=()=>riS().dy+RI_DRY-riDN();
function riWeeds(R,seed){const r=rng(seed*31+R.c*7+3),n=Math.min(6-R.wd.length,3+Math.floor(r()*3));for(let k=0;k<n;k++){const p=r()<.2?0:r()<.45?1:2;R.wd.push([p,+(-.78+1.56*r()).toFixed(3),+(.18+.78*r()).toFixed(3)]);}}
function riTick(){const R=riS(),dn=riDN();let ch=0;if(R.st==="grow"&&dn-R.gl>60)R.gl=dn-60;
  while(R.st==="grow"&&R.gl<dn){R.gl++;ch=1;if(R.wd.length){R.g+=.5;R.lz++;}else R.g+=1;
    if(R.g>=RI_GROW){R.st="ripe";R.wd=[];R.cut=[];R.news="ripe";break;}
    if(R.gl>=R.wn){const w0=R.wd.length;riWeeds(R,R.gl);R.wn=R.gl+2+(R.gl%2);if(R.wd.length>w0)R.news=R.news||"weeds";}}
  if(ch)save();return R;}
function riDue(){const R=riTick();return R.st==="flood"||R.st==="plant"||R.st==="grow"&&R.wd.length>0||R.st==="ripe"||R.st==="dry"&&riDryLeft()<=0;}
function riGrowWord(g){return g<3?"рассада приживается":g<8?"рис кустится":g<12?"появляются колоски":"колосья наливаются";}
function riLine(){const R=riTick(),d=riDay(),dd=`день ${d}${d<=RI_LEN?" из "+RI_LEN:""}`;
  switch(R.st){
    case"flood":return`Залито ${riCnt(R.fl)} из 3 чеков — долей остальные`;
    case"plant":return`Посажено ${riCnt(R.pl)} из ${RI_N} кустиков — досади рассаду`;
    case"grow":return`Рис растёт: ${dd} — `+(R.wd.length?"пора прополоть":riGrowWord(R.g));
    case"ripe":return`Рис созрел: ${dd} — пора жать`;
    case"dry":{const l=riDryLeft();return l>1?"Урожай сохнет на хасагакэ — обмолот через 2 дня":l===1?"Урожай сохнет на хасагакэ — завтра обмолот":"Снопы высохли — пора молотить";}
    default:return R.c?(riKome()>=3?`Свой рис в кладовой: ${riKome()} — пора толочь моти`:"Поле отдыхает — можно снова залить чеки"):"Террасы за домом ждут воды и рассады";}}
function riOpen(mochi){if(G.id)return;closePanel();$("album").hidden=true;audioInit();RI.go=mochi?"mochi":null;openPlace("ri_field");}

// ── drawing helpers (scene = 900×1500 picture coords)
function riSp(g,k,x,y,h,rot=0,al=1,anchor="b",flip=false){const r=RI_R[k];if(!RI.im||!r)return;const w=r[2]*h/r[3];g.save();g.globalAlpha*=al;g.translate(x,y);if(rot)g.rotate(rot);if(flip)g.scale(-1,1);g.drawImage(RI.im,r[0],r[1],r[2],r[3],-w/2,anchor==="c"?-h/2:-h,w,h);g.restore();}
function riBird(g,k,x,y,s,flip){const r=RI_BI[k];if(!RI.bi)return;g.save();g.translate(x,y);if(flip)g.scale(-1,1);g.drawImage(RI.bi,r[0],r[1],r[2],r[3],-r[4]*s,-r[5]*s,r[2]*s,r[3]*s);g.restore();}
function riNight(){return!!dayTint()[1];}
function riBgC(){const n=riNight(),k=n?"n":"d";if(RI.cache[k])return RI.cache[k];if(!RI.bg)return null;
  const c=document.createElement("canvas");c.width=900;c.height=1500;const g=c.getContext("2d");g.drawImage(RI.bg,0,0);
  g.globalCompositeOperation="source-atop";g.fillStyle=n?"rgba(10,16,38,.56)":"rgba(40,46,40,.08)";g.fillRect(0,0,900,1500);return RI.cache[k]=c;}
function riSkyC(){const n=riNight(),k=n?"n":"d";if(RI.sky[k])return RI.sky[k];const c=document.createElement("canvas");c.width=450;c.height=320;const g=c.getContext("2d");g.scale(.5,.5);
  const gr=g.createLinearGradient(0,0,0,640);if(n){gr.addColorStop(0,"#070b16");gr.addColorStop(1,"#1b2434");}else{gr.addColorStop(0,"#7e8d97");gr.addColorStop(1,"#c3cac4");}g.fillStyle=gr;g.fillRect(0,0,900,640);
  if(n){const r=rng(5);for(let i=0;i<120;i++){g.fillStyle=`rgba(220,226,240,${.2+r()*.6})`;g.fillRect(r()*900,r()*460,r()<.1?2.4:1.4,r()<.1?2.4:1.4);}
    const m=g.createRadialGradient(690,150,0,690,150,170);m.addColorStop(0,"rgba(220,226,236,.45)");m.addColorStop(1,"rgba(220,226,236,0)");g.fillStyle=m;g.fillRect(500,0,400,340);g.fillStyle="#e4e6e0";g.beginPath();g.arc(690,150,34,0,7);g.fill();}
  else{const m=g.createRadialGradient(640,170,0,640,170,260);m.addColorStop(0,"rgba(255,246,222,.5)");m.addColorStop(1,"rgba(255,246,222,0)");g.fillStyle=m;g.fillRect(300,0,600,460);}
  return RI.sky[k]=c;}
function riPath(g,p){const P=RI_POLY[p];g.beginPath();P.forEach(([x,y],i)=>i?g.lineTo(x,y):g.moveTo(x,y));g.closePath();}
function riIn(p,x,y){const P=RI_POLY[p];let c=false;for(let i=0,j=P.length-1;i<P.length;j=i++){const [xi,yi]=P[i],[xj,yj]=P[j];if((yi>y)!==(yj>y)&&x<(xj-xi)*(y-yi)/(yj-yi)+xi)c=!c;}return c;}
function riWet(R,p){return R.st==="flood"&&R.fl[p]||R.st==="plant"||R.st==="grow";}
function riWater(g,p,t,q,R){if(!riWet(R,p))return;const a=q.fl[p]?clamp((t-q.fl[p])/1.3,0,1):1,n=riNight(),P=RI_PAD[p];
  g.save();riPath(g,p);g.clip();g.globalAlpha=a;const gr=g.createLinearGradient(0,P[0],0,P[1]+P[4]);
  if(n){gr.addColorStop(0,"rgba(30,40,62,.9)");gr.addColorStop(1,"rgba(14,20,34,.86)");}else{gr.addColorStop(0,"rgba(176,186,186,.88)");gr.addColorStop(1,"rgba(120,134,136,.84)");}
  g.fillStyle=gr;g.fillRect(0,P[0]-4,900,P[1]-P[0]+P[4]+8);
  const mx=n?690:640,mr=g.createRadialGradient(mx,P[1]-10,0,mx,P[1]-10,110);mr.addColorStop(0,n?"rgba(226,230,236,.24)":"rgba(255,248,226,.22)");mr.addColorStop(1,"rgba(226,230,236,0)");
  g.save();g.translate(mx,P[1]-10);g.scale(.3+.03*Math.sin(t*1.7+p),1);g.translate(-mx,-(P[1]-10));g.fillStyle=mr;g.fillRect(mx-110,P[0],220,P[1]-P[0]+P[4]);g.restore();
  g.strokeStyle=n?"rgba(0,0,8,.35)":"rgba(40,50,40,.22)";g.lineWidth=26;g.beginPath();for(let i=0;i<=24;i++){const [x,y]=RI_E(p,-1+i/12,0);i?g.lineTo(x,y):g.moveTo(x,y);}g.stroke();
  g.globalCompositeOperation="lighter";for(let i=0;i<9;i++){const x=(i*113+t*9*(1+p*.3))%900,y=mix(P[0]+P[4],P[1],((i*37)%100)/100);g.fillStyle=`rgba(200,214,220,${(.05+.05*Math.sin(t*2+i))*a})`;g.fillRect(x,y,26+i%3*12,1.4);}
  for(const r of q.rip){const e=(t-r.t)/1.2;if(e>1||r.p!==p)continue;g.strokeStyle=`rgba(220,230,236,${.5*(1-e)})`;g.lineWidth=1.6;g.beginPath();g.ellipse(r.x,r.y,8+40*e,(8+40*e)*.3,0,0,7);g.stroke();}
  g.restore();}
function riStage(R,i){const st=R.st,h=RI_H[i];
  if(st==="plant")return R.pl[i]?["nae",46]:null;
  if(st==="grow"){const g=R.g;return g<3?["nae",46*(1+g*.12)]:g<8?["g1",96*(.8+.2*(g-3)/5)]:["g2",140*(.86+.14*Math.min(1,(g-8)/6))];}
  if(st==="ripe")return R.cut[i]?["stub",26]:["gold",150];
  if(R.c&&(st==="dry"||st==="fallow"||st==="flood"&&!R.fl[h.p]))return["stub",26];
  return null;}
function riPlants(g,p,t,q,R){
  const dryW=(R.st==="fallow"||R.st==="flood")&&!R.fl[p]&&!q.fl[p];
  for(let i=0;i<RI_N;i++){const h=RI_H[i];if(h.p!==p)continue;const s=riStage(R,i);
    if(!s){if(R.st==="plant")continue;if(dryW&&i%4===1)riSp(g,"weed",h.x,h.y,40*h.f,Math.sin(t+i)*.05);continue;}
    const pop=q.pop[i]?easeOutBack((t-q.pop[i])/.35):1,big=s[0]!=="nae"&&s[0]!=="stub";
    riSp(g,s[0],h.x,h.y,s[1]*h.f*pop,big?Math.sin(t*1.1+i*.7+h.x*.01)*.035:0,1,"b",i%3===0);}
  if(R.st==="plant"){g.fillStyle=`rgba(226,236,206,${.28+.14*Math.sin(t*3)})`;for(let i=0;i<RI_N;i++){const h=RI_H[i];if(h.p===p&&!R.pl[i]){g.beginPath();g.ellipse(h.x,h.y-3,7*h.f,3*h.f,0,0,7);g.fill();}}}
  if(R.st==="grow")for(const w of R.wd)if(w[0]===p){const [ax,ay]=RI_E(p,w[1],0),[bx,by]=RI_E(p,w[1],1),y=mix(ay,by,w[2]),f=.5+.5*(y-585)/685;const wx=mix(ax,bx,w[2]),rt=Math.sin(t*1.4+w[1]*9)*.06;riSp(g,"weed",wx,y,56*f,rt);if(riNight()){g.save();g.globalCompositeOperation="lighter";riSp(g,"weed",wx,y,56*f,rt,.45);g.restore();}}}
function riScare(g,t,q){const e=t-q.shake,sh=e<1?Math.sin(e*28)*.12*(1-e):Math.sin(t*.9)*.015;riSp(g,"kakashi",RI_SC.x,RI_SC.y,RI_SC.h,sh);
  if(e<1)for(let k=0;k<2;k++)jpText(g,"カラ",RI_SC.x+60+k*26,RI_SC.y-110-e*40-k*16,22,`rgba(240,230,200,${1-e})`);}
function riRack(g,t,q,R){riSp(g,"rack",690,1462,232);
  const n=R.st==="ripe"?q.hung:R.st==="dry"?RI_SLOTS:0;
  if(R.st==="dry"&&riDryLeft()<=0){g.fillStyle="rgba(150,122,70,.85)";g.beginPath();g.moveTo(560,1446);g.lineTo(830,1446);g.lineTo(850,1484);g.lineTo(545,1484);g.closePath();g.fill();
    g.fillStyle="rgba(232,214,160,.9)";for(let k=0;k<riCnt(R.th)*6;k++){const r=rng(k*7+1);g.fillRect(565+r()*270,1450+r()*30,3,2);}}
  for(let k=0;k<n;k++){if(R.th[k])continue;const [x,y]=RI_SL[k];riSp(g,"hang",x,y-6+80,80,Math.sin(t*1.3+k)*.02,1,"b",k%2===1);}}
function riCat(g,t,q){if(petAway())return;const m=q.mode==="mochi",x=m?820:330,fl=m?1474:1446,cs=m?.62:.78;let st="rest",fi=Math.floor(t*2)%2;
  const tg=q.look&&t-q.look.t<3?q.look:q.sp.find(b=>b.st!=="out");
  if(tg&&!m){const gi=gazeIndex(tg.x-x,(fl-150*cs)-tg.y);st=gi<8?"gaze9":"gaze10";fi=gi%8;}
  if(q.joy&&t-q.joy<1.2){st="play";fi=4;}
  g.save();g.globalAlpha=.4;g.fillStyle="#000";g.beginPath();g.ellipse(x,fl,70*cs,12*cs,0,0,7);g.fill();g.restore();
  drawCatG(g,st,fi,x,fl,cs);}
function riFx(g,t,q){for(const f of q.fx){const e=(t-f.t)/f.d;if(e<0||e>1)continue;
  if(f.k==="fly"){const x=mix(f.x,f.tx,e),y=mix(f.y,f.ty,e)-Math.sin(e*Math.PI)*120;riSp(g,f.s,x,y,f.h,e*6,1,"c");}
  else if(f.k==="up"){riSp(g,f.s,f.x+e*f.vx,f.y-e*80+e*e*90,f.h,e*3,1-e,"c");}
  else if(f.k==="grain"){g.fillStyle=`rgba(236,216,150,${1-e})`;for(let i=0;i<14;i++){const a=i*2.4;g.fillRect(f.x+Math.cos(a)*30*e,f.y+Math.sin(a)*12*e+e*e*140,3,2);}}
  else if(f.k==="txt")jpText(g,f.s,f.x,f.y-e*50,f.sz||30,`rgba(250,240,214,${1-e*e})`);}
  q.fx=q.fx.filter(f=>t-f.t<f.d);}
function riBirds(g,t,q){for(const b of q.sp){const e=t-b.t0;let x=b.x,y=b.y,k="sit";
  if(b.st==="in"){const u=clamp(e/1.4,0,1);x=mix(b.fx,b.x,u);y=mix(b.fy,b.y,u)-Math.sin(u*Math.PI)*60;k=Math.floor(t*14)%2?"fly":"sit";if(u>=1){b.st="sit";b.t0=t;}}
  else if(b.st==="sit")k=Math.sin(t*3+b.ph)>.3?"peck":"sit";
  else{x=b.x+e*260*b.dir;y=b.y-e*320;k=Math.floor(t*14)%2?"fly":"sit";}
  b.cx=x;b.cy=y;riBird(g,k,x,y,.42,b.dir<0);}
  q.sp=q.sp.filter(b=>b.st!=="out"||t-b.t0<2.5);}

// ── mochitsuki: you swing the kine, the yōkai turns the dough between strikes
const RI_US={x:450,y:1404,h:212},RI_DO={x:450,y:1252},RI_PV={x:300,y:1580};
function riMochiStart(G,t){const q=G.st,R=riS();if(riKome()<3){riMsg(q,"Нужно 3 мешочка своего риса",t);return;}
  for(let i=0;i<3;i++)take("v_ri_kome");save();const kp=R.mo%2===0;
  q.mode="mochi";q.m={t0:t,n:0,good:0,P:1.15,next:t+2.4,turn:-9,kine:-9,ouch:-9,end:0,dough:0,hit:false,id:kp?"m_kappa":"m_tanuki",
    lumps:Array.from({length:9},(_,i)=>[Math.cos(i*2.4)*rand(20,70),Math.sin(i*2.4)*rand(6,16)-6,rand(14,24)])};
  q.m.say={t,s:kp?"Каппа: «Ты бьёшь — я переворачиваю. Только по лапе не попади!»":"Тануки: «По очереди: ты пестом, я лапой. Ёй-сё!»"};}
function riMochiStep(G,t){const q=G.st,m=q.m;if(m.end)return;
  if(t>m.next+.3){if(!m.hit){m.miss=t;}m.n++;m.turn=m.next+m.P/2;m.next+=m.P;m.hit=false;m.P=Math.max(.8,m.P-.025);
    if(m.n>=14){m.end=t+1;riMochiEnd(G,t);}}}
function riMochiTap(G,t){const q=G.st,m=q.m;if(m.end)return;
  if(Math.abs(t-m.next)<.27&&!m.hit){m.hit=true;m.good++;m.kine=t;m.dough=Math.min(1,m.good/12);tone(86,.22,"sine",.16);tone(150,.08,"triangle",.05);
    q.fx.push({k:"txt",s:pick(["ぺったん","よいしょ"]),x:RI_DO.x-120,y:RI_DO.y-120,t,d:.9,sz:28});if(navigator.vibrate)try{navigator.vibrate(18);}catch(e){}return;}
  if(Math.abs(t-m.turn)<.3){m.ouch=t;tone(520,.12,"square",.03);q.fx.push({k:"txt",s:"Ай!",x:RI_DO.x+150,y:RI_DO.y-170,t,d:1,sz:30});return;}
  m.kine=t;tone(120,.12,"sine",.05);}
function riMochiEnd(G,t){const q=G.st,m=q.m,R=riS(),n=2+Math.floor(m.good/4);give("ds_mochi",n);R.mo++;
  S.needs.joy=clamp(S.needs.joy+10,0,100);award("ri_mochi");let gift="";if(!S.owned.has("ri_kakashi")){S.owned.add("ri_kakashi");gift="ri_kakashi";}
  m.res={n,gift};save();chime([784,988,1175]);q.joy=t;}
function riMochiDraw(g,t,q){const m=q.m;g.fillStyle="rgba(6,8,12,.5)";g.fillRect(0,0,900,1500);
  const lg=g.createRadialGradient(450,1300,0,450,1300,420);lg.addColorStop(0,"rgba(255,214,150,.22)");lg.addColorStop(1,"rgba(255,214,150,0)");g.fillStyle=lg;g.fillRect(0,880,900,620);
  // helper turns the dough half a beat after each strike
  const tu=t-m.turn,lean=tu>-.2&&tu<.35?-.16*Math.sin(clamp((tu+.2)/.55,0,1)*Math.PI):0,ow=t-m.ouch<.5?.12*Math.sin((t-m.ouch)*30):0,im=MIMG[m.id];
  if(im){const h=300,w=im.width*h/im.height;g.save();g.translate(660,1452);g.rotate(lean+ow);g.drawImage(im,-w/2,-h,w,h);g.restore();}
  riSp(g,"usu",RI_US.x,RI_US.y,RI_US.h);
  const sq=Math.max(0,1-(t-m.kine)/.18),dn=m.dough,rx=96*(1+.1*sq),ry=34*(1-.3*sq);
  const dg=g.createRadialGradient(RI_DO.x-30,RI_DO.y-20,6,RI_DO.x,RI_DO.y,rx);dg.addColorStop(0,"#fbf8f0");dg.addColorStop(1,dn>.6?"#e6dfd0":"#d8cfbc");g.fillStyle=dg;g.beginPath();g.ellipse(RI_DO.x,RI_DO.y,rx,ry,0,Math.PI,0);g.ellipse(RI_DO.x,RI_DO.y,rx,ry*.35,0,0,Math.PI);g.fill();
  for(const [dx,dy,r] of m.lumps){g.fillStyle=`rgba(236,230,214,${(1-dn)*.95})`;g.beginPath();g.arc(RI_DO.x+dx,RI_DO.y+dy-ry*.3,r*(1-dn*.6),0,7);g.fill();g.fillStyle=`rgba(255,255,250,${(1-dn)*.6})`;for(let k=0;k<3;k++)g.fillRect(RI_DO.x+dx+k*5-6,RI_DO.y+dy-ry*.4-k*3,3,2);}
  if(tu>-.15&&tu<.3){const u=clamp((tu+.15)/.45,0,1),hx=mix(590,RI_DO.x+40,Math.sin(u*Math.PI)),hy=mix(1180,RI_DO.y-10,Math.sin(u*Math.PI));g.fillStyle=m.id==="m_kappa"?"#5f8a4a":"#6a4a32";g.beginPath();g.ellipse(hx,hy,24,14,-.4,0,7);g.fill();
    if(u>.3&&u<.7)jpText(g,"はい!",660,1110,30,"rgba(250,240,214,.95)");}
  if(!m.end){const a=clamp((m.next-t)/m.P,0,1),rr=rx+260*a;g.strokeStyle=`rgba(255,236,200,${.25+.6*(1-a)})`;g.lineWidth=4;g.beginPath();g.ellipse(RI_DO.x,RI_DO.y,rr,rr*.36,0,0,7);g.stroke();
    g.strokeStyle="rgba(255,236,200,.35)";g.lineWidth=2;g.beginPath();g.ellipse(RI_DO.x,RI_DO.y,rx+4,(rx+4)*.36,0,0,7);g.stroke();}
  // the kine: raised, comes down on a strike
  const ad=Math.atan2(RI_DO.x-RI_PV.x,-(RI_DO.y-RI_PV.y)),k=t-m.kine,sw=k<.1?1-k/.1:k<.2?0:k<.55?(k-.2)/.35:1,ang=ad-1.05*sw,L=Math.hypot(RI_DO.x-RI_PV.x,RI_DO.y-RI_PV.y),s=L/276;
  if(RI.im){const r=RI_R.kine;g.save();g.translate(RI_PV.x,RI_PV.y);g.rotate(ang);g.drawImage(RI.im,r[0],r[1],r[2],r[3],-56*s,-318*s,112*s,320*s);g.restore();}
  if(m.say&&t-m.say.t<4.5){const al=clamp(4.5-(t-m.say.t),0,1);g.save();g.globalAlpha=al;g.fillStyle="rgba(10,12,14,.8)";g.beginPath();g.roundRect(70,960,760,90,18);g.fill();
    g.font=`500 25px ${getComputedStyle(document.body).fontFamily}`;g.fillStyle="#efe6d2";g.textAlign="center";const w=m.say.s.split("«");g.fillText(w[0]+(w[1]?"":""),450,992);if(w[1])g.fillText("«"+w[1],450,1026);g.restore();}}

// ── the place
function riMsg(q,txt,t){q.msg={txt,t};}
function riL(G){const q=G.st;q.lw=G.W;q.lh=G.H;q.k=Math.min(G.W/840,G.H/1500);q.ox=(G.W-900*q.k)/2;q.oy=G.H-1500*q.k;q.top=Math.min(0,-q.oy/q.k)-2;}
function riHint(R,q){if(q.mode==="mochi")return q.m.end?"":"Бей пестом, когда круг сожмётся на моти";
  switch(R.st){case"fallow":return R.c&&riKome()>=3?"Поле отдыхает. Можно толочь моти или снова залить чеки":"Нажми на чек — прополем его и зальём водой";
    case"flood":return"Нажимай на сухие чеки — залей все три";
    case"plant":return`Веди пальцем вдоль рядов — сажаем рассаду · ${riCnt(R.pl)}/${RI_N}`;
    case"grow":return R.wd.length?`Сорняки! Выдёргивай — они мешают рису · ${R.wd.length}`:`Рис растёт: день ${riDay()}${riDay()<=RI_LEN?" из "+RI_LEN:""} — ${riGrowWord(R.g)}`;
    case"ripe":return q.sp.some(b=>b.st!=="out")?"Воробьи клюют колосья — нажми на пугало!":"Проведи серпом по золотым колосьям";
    case"dry":{const l=riDryLeft();return l>0?(l===1?"Снопы сохнут на хасагакэ — обмолот завтра":`Снопы сохнут на хасагакэ — обмолот через ${l} дня`):"Снопы высохли — нажимай на них, чтобы обмолотить";}}return"";}
function riFlood(q,p,t){const R=riS();if(R.st==="fallow"){R.st="flood";R.fl=[0,0,0];}if(R.fl[p])return;R.fl[p]=1;q.fl[p]=t;sfx("splash");
  for(let i=0;i<RI_N;i++){const h=RI_H[i];if(h.p===p&&i%4===1)q.fx.push({k:"up",s:"weed",x:h.x,y:h.y-20,vx:rand(-40,40),h:40*h.f,t,d:.9});}
  const P=RI_PAD[p];q.rip.push({p,x:450,y:(P[0]+P[1])/2,t});
  if(riCnt(R.fl)===3){R.st="plant";R.d0=riDN();R.pl=Array(RI_N).fill(0);riMsg(q,"Чеки залиты — сажаем рассаду рядами",t);}save();}
function riPlant(q,i,t){const R=riS(),h=RI_H[i];R.pl[i]=1;q.pop[i]=t;q.look={x:h.x,y:h.y,t};q.rip.push({p:h.p,x:h.x,y:h.y,t});tone(rand(480,560),.07,"sine",.04);
  if(riCnt(R.pl)>=RI_N){R.st="grow";R.g=0;R.gl=riDN();R.wn=R.gl+2;R.wd=[];R.cut=[];R.th=[];R.sc=0;R.lz=0;q.joy=t;chime([659,784,988]);
    award("ri_plant");let s="Посадка окончена! Рис растёт сам — заглядывай через день-два";if(!S.owned.has("ri_kasa")){S.owned.add("ri_kasa");s="🎁 Соломенная шляпа — в «🧺 Вещи». Рис растёт сам!";}riMsg(q,s,t);}
  save();}
function riPull(q,k,t){const R=riS(),w=R.wd[k],[ax,ay]=RI_E(w[0],w[1],0),[bx,by]=RI_E(w[0],w[1],1),x=mix(ax,bx,w[2]),y=mix(ay,by,w[2]);R.wd.splice(k,1);
  q.fx.push({k:"up",s:"weed",x,y:y-25,vx:rand(-60,60),h:56*(.5+.5*(y-585)/685),t,d:1});q.look={x,y,t};sfx("pop");if(!R.wd.length){riMsg(q,"Чисто! Рис снова растёт быстрее",t);q.joy=t;}save();}
function riCut(q,i,t){const R=riS(),h=RI_H[i];R.cut[i]=1;const n=riCnt(R.cut),sl=Math.min(RI_SLOTS,Math.floor(n*RI_SLOTS/RI_N));tone(rand(1500,1800),.04,"triangle",.03);tone(700,.06,"sine",.02);
  if(sl>q.hung){const [sx,sy]=RI_SL[sl-1];q.fx.push({k:"fly",s:"sheaf",x:h.x,y:h.y-40,tx:sx,ty:sy+40,h:70,t,d:.7});setTimeout(()=>{q.hung=Math.max(q.hung,sl);},700);}
  if(n>=RI_N){R.st="dry";R.dy=riDN();R.th=[];R.h=(R.h||0)+1;q.hung=RI_SLOTS;disc("rice","harvest_"+Math.min(5,R.h));award("ri_harvest");q.sp.forEach(b=>{b.st="out";b.t0=t;});q.joy=t;chime([523,659,784,1046]);
    let s="Жатва окончена! Снопы сохнут 2 дня на хасагакэ";if(!S.owned.has("ri_kakeho")){S.owned.add("ri_kakeho");s="🎁 Сноп какэхо — в «🧺 Вещи». Сушим 2 дня";}riMsg(q,s,t);}
  save();}
function riThresh(q,k,t){const R=riS(),[x,y]=RI_SL[k];R.th[k]=1;q.fx.push({k:"grain",x,y:y+60,t,d:1});tone(rand(900,1200),.05,"triangle",.03);q.look={x,y,t};
  if(riCnt(R.th)>=RI_SLOTS){const n=5+Math.min(2,R.sc)+(R.lz?0:1);give("v_ri_kome",n);give("i_rice",n);R.st="fallow";R.c++;R.fl=[0,0,0];q.joy=t;sfx("coin");chime([784,988,1318]);
    S.needs.joy=clamp(S.needs.joy+8,0,100);riMsg(q,X.ws?`Свой рис: +${n} в кладовую, солома — в мастерскую`:`Свой рис: +${n} мешочков в кладовую!`,t);}save();}
function riTouch(G,x,y,t,drag){const q=G.st,R=riS(),sx=(x-q.ox)/q.k,sy=(y-q.oy)/q.k;
  if(q.mode==="mochi"){if(!drag)riMochiTap(G,t);return;}
  if(R.st==="fallow"||R.st==="flood"){if(drag)return;for(let p=2;p>=0;p--)if(riIn(p,sx,sy)){riFlood(q,p,t);return;}return;}
  if(R.st==="plant"){let b=-1,bd=46;for(let i=0;i<RI_N;i++){if(R.pl[i])continue;const h=RI_H[i],d=Math.hypot(h.x-sx,(h.y-sy)*1.3)/h.f;if(d<bd){bd=d;b=i;}}if(b>=0)riPlant(q,b,t);return;}
  if(R.st==="grow"){for(let k=0;k<R.wd.length;k++){const w=R.wd[k],[ax,ay]=RI_E(w[0],w[1],0),[bx,by]=RI_E(w[0],w[1],1),wx=mix(ax,bx,w[2]),wy=mix(ay,by,w[2])-18;if(Math.hypot(wx-sx,wy-sy)<48){riPull(q,k,t);return;}}
    if(!drag){q.look={x:sx,y:sy,t};}return;}
  if(R.st==="ripe"){q.cur={x:sx,y:sy,t};
    if(!drag){if(Math.abs(sx-RI_SC.x)<70&&sy<RI_SC.y+10&&sy>RI_SC.y-RI_SC.h){q.shake=t;tone(330,.06,"square",.03);setTimeout(()=>tone(280,.06,"square",.03),90);const on=q.sp.filter(b=>b.st!=="out");if(on.length){R.sc++;q.joy=t;save();}on.forEach(b=>{b.st="out";b.t0=t;});return;}
      const b=q.sp.find(b=>b.st!=="out"&&Math.hypot(b.cx-sx,b.cy-sy)<50);if(b){b.st="out";b.t0=t;return;}}
    for(let i=0;i<RI_N;i++){if(R.cut[i])continue;const h=RI_H[i];if(Math.hypot(h.x-sx,(h.y-60*h.f)-sy)<62*h.f+10)riCut(q,i,t);}return;}
  if(R.st==="dry"&&riDryLeft()<=0&&!drag){for(let k=0;k<RI_SLOTS;k++){if(R.th[k])continue;const [hx,hy]=RI_SL[k];if(Math.abs(hx-sx)<30&&sy>hy-10&&sy<hy+90){riThresh(q,k,t);return;}}}
  if(R.st==="dry"&&riDryLeft()>0&&!drag)riMsg(q,riDryLeft()===1?"Ещё сыроваты — обмолот завтра":"Снопы ещё сырые — сушим 2 дня",t);}
function riUI(G,g,t){const q=G.st,R=riS(),W=G.W,H=G.H,hint=riHint(R,q);q.btns=[];
  if(hint){g.save();g.font=`600 ${Math.min(14,W/34)}px ${getComputedStyle(document.body).fontFamily}`;const tw=Math.min(W-20,g.measureText(hint).width+32);g.fillStyle="rgba(8,10,9,.74)";g.beginPath();g.roundRect(W/2-tw/2,8,tw,32,16);g.fill();g.restore();textC(g,hint,W/2,24,Math.min(14,W/34),"#e6dfcd",600);}
  if(q.msg&&t-q.msg.t<4){const a=clamp(4-(t-q.msg.t),0,1);g.save();g.globalAlpha=a;g.font=`600 13px ${getComputedStyle(document.body).fontFamily}`;const tw=Math.min(W-20,g.measureText(q.msg.txt).width+30);g.fillStyle="rgba(60,44,20,.85)";g.beginPath();g.roundRect(W/2-tw/2,46,tw,28,14);g.fill();g.restore();textC(g,q.msg.txt,W/2,60,13,`rgba(255,240,206,${a})`,600);}
  const bt=(k,label,w=230)=>{const b={x:W/2-w/2,y:H-60,w,h:42,k};q.btns.push(b);btnRect(g,b.x,b.y,b.w,b.h,label,k==="ri:m");};
  if(q.mode==="mochi"&&q.m.end&&t>q.m.end){const m=q.m,cw=Math.min(W-40,340),cx=W/2-cw/2,cy=H*.3;g.fillStyle="rgba(12,14,13,.9)";g.beginPath();g.roundRect(cx,cy,cw,170,18);g.fill();
    textC(g,`Моти готовы: ×${m.res.n}`,W/2,cy+34,20,"#f3e8d0",700);textC(g,`Точных ударов: ${m.good} из 14 · в кладовой`,W/2,cy+66,13,"#cfc6b2",500);
    if(m.res.gift)textC(g,"🎁 Пугало какаси — в «🧺 Вещи»",W/2,cy+92,13,"#eec98a",600);fDraw(g,"ds_mochi",W/2,cy+128,40);bt("ri:back","К полю",180);}
  else if(q.mode!=="mochi"&&riKome()>=3&&(R.st==="fallow"||R.st==="grow"&&!R.wd.length||R.st==="dry"&&riDryLeft()>0))bt("ri:m",`Толочь моти · свой рис ×${riKome()}`);}
const RI_GAME={id:"ri_field",hidden:true,n:"Рисовое поле",tag:"棚田 · Танада",bg:"field",lives:null,time:null,icon:"🌾",lore:"",how:"",
 init(G,t){riTick();Object.assign(G.st,{mode:"field",fx:[],fl:{},pop:{},rip:[],sp:[],spT:t+rand(2,4),shake:-9,msg:null,look:null,cur:null,btns:[],hung:0,joy:0,chk:t});riL(G);
   const R=riS();R.news=null;if(R.st==="ripe")G.st.hung=Math.min(RI_SLOTS,Math.floor(riCnt(R.cut)*RI_SLOTS/RI_N));if(RI.go==="mochi"){RI.go=null;riMochiStart(G,t);}},
 step(G,t,dt){const q=G.st,R=riS();if(t-q.chk>2){q.chk=t;const st=R.st;riTick();if(R.st!==st)riMsg(q,R.st==="ripe"?"Рис созрел — пора жать!":"Взошли сорняки",t);}
   if(q.mode==="mochi")riMochiStep(G,t);
   else if(R.st==="ripe"&&t>q.spT&&!riNight()){q.spT=t+rand(6,10);const n=q.sp.filter(b=>b.st!=="out").length;
     for(let k=0;k<Math.min(3,4-n);k++){const c=RI_H.map((h,i)=>i).filter(i=>!R.cut[i]);if(!c.length)break;const h=RI_H[pick(c)],dir=Math.random()<.5?1:-1;
       q.sp.push({st:"in",t0:t+k*.3,x:h.x+rand(-10,10),y:h.y-120*h.f,fx:dir>0?-60:960,fy:rand(380,560),dir,ph:rand(0,6),cx:-99,cy:-99});}}
   q.rip=q.rip.filter(r=>t-r.t<1.3);},
 draw(G,g,t){const q=G.st,R=riS();if(q.lw!==G.W||q.lh!==G.H)riL(G);
   const bg=riBgC();if(q.ox>4){const n=riNight(),gr=g.createLinearGradient(0,0,0,G.H),w=900*q.k;gr.addColorStop(0,n?"#0a0f1c":"#7f8c94");gr.addColorStop(.42,n?"#131a1c":"#59634c");gr.addColorStop(1,n?"#0b0d0b":"#2b2a20");g.fillStyle=gr;g.fillRect(0,0,G.W,G.H);
     if(bg){g.save();g.globalAlpha=.5;for(const sd of[-1,1]){g.save();g.translate(sd<0?q.ox:q.ox+w,0);g.scale(-1,1);g.drawImage(bg,sd<0?0:-w,q.oy,w,1500*q.k);g.restore();}g.restore();}
     g.fillStyle="rgba(0,0,0,.42)";g.fillRect(0,0,q.ox,G.H);g.fillRect(q.ox+w,0,G.W-q.ox-w,G.H);}
   g.save();g.translate(q.ox,q.oy);g.scale(q.k,q.k);g.beginPath();g.rect(0,q.top,900,1500-q.top);g.clip();
   g.drawImage(riSkyC(),0,q.top,900,640-q.top);if(bg)g.drawImage(bg,0,0);
   for(let p=0;p<3;p++){riWater(g,p,t,q,R);riPlants(g,p,t,q,R);if(p===1)riScare(g,t,q);}
   riRack(g,t,q,R);if(q.mode!=="mochi")riCat(g,t,q);riBirds(g,t,q);
   if(R.st==="ripe"&&q.cur&&G.held&&t-q.cur.t<.4)riSp(g,"kama",q.cur.x+34,q.cur.y-14,100,-.3+Math.sin(t*20)*.1,1,"c");
   if(riNight()){g.fillStyle="rgba(8,12,30,.18)";g.fillRect(0,0,900,1500);}
   if(q.mode==="mochi"){riMochiDraw(g,t,q);riCat(g,t,q);}
   riFx(g,t,q);g.restore();riUI(G,g,t);},
 down(G,x,y,t){const q=G.st,b=q.btns.find(b=>x>b.x&&x<b.x+b.w&&y>b.y&&y<b.y+b.h);
   if(b){q.btns=[];if(b.k==="ri:m")riMochiStart(G,t);else if(b.k==="ri:back"){q.mode="field";q.m=null;}return;}riTouch(G,x,y,t,false);},
 move(G,x,y,held){if(held)riTouch(G,x,y,now(),true);},
 up(G){G.st.cur=null;},
 stat:G=>{const R=riS();return R.st==="grow"||R.st==="ripe"?`🌾 день ${riDay()}${riDay()<=RI_LEN?" из "+RI_LEN:""}`:`🌾 свой рис ×${riKome()}`;},
 after(){ui();}};
GAMES.push(RI_GAME);

// ── own rice in the kitchen: three recipes that need «Свой рис» (more joy than the usual dishes).
// Pictures: onigiri and sekihan reuse the core/birthday dish pictures (aliased rects), chazuke → art/links_art.py → atlas_ri2.webp
FATL.ri2={w:140,h:98,r:{ds_ri_chazuke:[0,2,140,96]}};
const RI_ALIAS=[["ds_ri_onigiri","ds_onigiri"],["ds_ri_sekihan","ds_bd_sekihan","ds_onigiri"]];
function riAlias(){for(const [id,...src] of RI_ALIAS){if(fAtlas(id))continue;for(const s of src){const A=fAtlas(s);if(A){A[1].r[id]=A[1].r[s];break;}}}}
riAlias();
Object.assign(FOOD,{ds_ri_onigiri:{n:"Онигири из своего риса",k:"dish",food:32,joy:22},ds_ri_chazuke:{n:"Тядзукэ из своего риса",k:"dish",food:26,joy:18},
  ds_ri_sekihan:{n:"Сэкихан из своего риса",k:"dish",food:34,joy:26}});
const RI_RC=[
 {id:"ri_onigiri",dish:"ds_ri_onigiri",n:"Онигири из своего риса",jp:"新米のおにぎり",after:"onigiri",
  lore:"Рис нового урожая с собственных террас — Муся видела, как он рос. Такие онигири пахнут полем и солнцем, и радости от них почти втрое больше, чем от обычных.",
  need:["v_ri_kome","i_nori"],steps:[{k:"add",it:["v_ri_kome"]},{k:"shape",n:3,pic:"ds_ri_onigiri"},{k:"add",it:["i_nori"]}]},
 {id:"ri_chazuke",dish:"ds_ri_chazuke",n:"Тядзукэ из своего риса",jp:"お茶漬け",after:"ri_onigiri",
  lore:"Миску своего риса заливают горячим зелёным чаем, сверху — полоски нори и кислая слива умэбоси. Так ужинают поздним вечером, когда хочется тепла.",
  need:["v_ri_kome","i_nori"],steps:[{k:"add",it:["v_ri_kome"]},{k:"add",it:["i_nori"]},{k:"stir",n:2}]},
 {id:"ri_sekihan",dish:"ds_ri_sekihan",n:"Сэкихан из своего риса",jp:"赤飯",after:"bd_sekihan",
  lore:"Свой рис, сваренный с бобами адзуки, к празднику становится розово-красным. Сэкихан из риса нового урожая варят, чтобы поблагодарить поле.",
  need:["v_ri_kome","i_azuki"],steps:[{k:"add",it:["i_azuki"]},{k:"heat",n:2,lb:"Отвари бобы"},{k:"add",it:["v_ri_kome"]},{k:"stir",n:2},{k:"shape",n:2,pic:"ds_ri_sekihan"}]}];
for(const r of RI_RC){if(RECIPES.some(x=>x.id===r.id))continue;const i=RECIPES.findIndex(x=>x.id===r.after);RECIPES.splice(i<0?RECIPES.length:i+1,0,r);}
const RI_WHERE="Свой рис растят на террасах за домом: «Дворик» → 🌾 Рисовое поле. После обмолота мешочки риса появятся в кладовой.";
// the recipe card names the missing ingredient's source; the core text says «grows in the garden» for every veg → fix it for own rice
function riCookFix(){const R=cook.R,el=$("gResult");if(G.id!=="cook"||!R||!el||el.hidden||!R.need.includes("v_ri_kome")||!el.querySelector("#gGo"))return;
  const m=el.querySelector("p.miss");if(m&&!have("v_ri_kome"))m.textContent=RI_WHERE;
  const tg=el.querySelector("p.tag");if(tg&&!tg.dataset.ri){tg.dataset.ri=1;tg.textContent=`${R.jp} · 🌾 свой рис`;}}
hook("boot",()=>{riAlias();const el=$("gResult");if(el)new MutationObserver(riCookFix).observe(el,{childList:true});});
hook("ev",(e,d)=>{if(e==="eat"&&/^ds_ri_/.test(d)&&!petAway())setTimeout(()=>{burst(6);react("😻",1.8);},1500);});

// ── courtyard tray, hub card, dots, postcard
hook("tray",(tray,room)=>{if(room!=="courtyard"||(S.trayMode[room]||"play")!=="play")return;const el=tray.querySelector(".items");if(!el)return;
  const h=`<button class="item wide" data-x="ri:open"><span class="ico">🌾</span><span class="nm">Рисовое поле</span></button>`,zn=el.querySelector('[data-x="zn:open"]');
  if(zn)zn.insertAdjacentHTML("afterend",h);else el.insertAdjacentHTML("beforeend",h);});
hook("click",k=>{if(!k.startsWith("ri:"))return;if(k==="ri:open")riOpen();else if(k==="ri:mochi")riOpen(1);return true;});
hook("hub",()=>{const R=riTick(),k=riKome();
  const more=R.st==="grow"?`Сорняки лезут каждые два-три дня: если не выполоть, рис растёт вдвое медленнее, но не гибнет.`:R.st==="ripe"?"К спелым колосьям слетаются воробьи — пугало их прогонит.":R.st==="dry"?"Снопы висят колосьями вниз — так зерно дозревает и сохнет.":"Залей три чека, посади рассаду и жди: рис растёт по настоящим дням, около трёх недель.";
  return`<div class="hubc"><h4>🌾 Рисовое поле <i>棚田</i></h4><p>${riLine()}</p><p>${more}${R.h?` Урожаев: ${R.h}.`:""}${R.c?" Из своего риса на кухне готовят онигири, тядзукэ и сэкихан.":""}${R.mo?` Моти толкли ${R.mo} ${R.mo%10===1&&R.mo%100!==11?"раз":R.mo%10>=2&&R.mo%10<=4&&(R.mo%100<12||R.mo%100>14)?"раза":"раз"}.`:""}</p><div class="row"><button class="btn${riDue()?" primary":""}" data-x="ri:open">На поле</button>${k>=3?`<button class="btn" data-x="ri:mochi">Толочь моти · ×${k}</button>`:""}</div></div>`;});
hook("hubDot",()=>riDue());
hook("tabDot",r=>{if(r!=="courtyard")return false;const R=riTick();return R.st==="grow"&&R.wd.length>0||R.st==="ripe"||R.st==="dry"&&riDryLeft()<=0;});
hook("away",()=>{const R=riTick(),n=R.news;if(!n)return null;R.news=null;return{i:"🌾",t:n==="ripe"?"На террасах за домом созрел рис — пора жать":"На рисовом поле взошли сорняки"};});
hook("boot",()=>{riS();atlasImg("ri",im=>{RI.im=im;});atlasImg("bi",im=>{RI.bi=im;});ldImg("assets/bg/ri_field.webp",im=>{RI.bg=im;RI.cache={};});});
X.ri={st:riS,tick:riTick,open:riOpen,line:riLine,due:riDue,
  age(n){const R=riS();R.d0-=n;R.gl-=n;R.wn-=n;R.dy-=n;riTick();},
  tap(sx,sy){if(G.id!=="ri_field")return;const q=G.st;riTouch(G,q.ox+sx*q.k,q.oy+sy*q.k,now(),false);},
  drag(pts){if(G.id!=="ri_field")return;const q=G.st;G.held=true;for(let i=1;i<pts.length;i++){const [a,b]=pts[i-1],[c,d]=pts[i],n=Math.ceil(Math.hypot(c-a,d-b)/18);for(let k=0;k<=n;k++)riTouch(G,q.ox+mix(a,c,k/n)*q.k,q.oy+mix(b,d,k/n)*q.k,now(),true);}G.held=false;},
  floodAll(){for(let p=0;p<3;p++)X.ri.tap(450,(RI_PAD[p][0]+RI_PAD[p][1])/2);},
  plantAll(a=0,b=RI_N){for(let i=a;i<b;i++){const h=RI_H[i];X.ri.tap(h.x,h.y);}},
  pullAll(){const R=riS();while(R.wd.length&&G.id==="ri_field"){const w=R.wd[0],[ax,ay]=RI_E(w[0],w[1],0),[bx,by]=RI_E(w[0],w[1],1);X.ri.tap(mix(ax,bx,w[2]),mix(ay,by,w[2])-18);}},
  scare(){X.ri.tap(RI_SC.x,RI_SC.y-100);},
  cutAll(a=0,b=RI_N){for(let i=a;i<b;i++)if(!riS().cut[i]){const h=RI_H[i];X.ri.drag([[h.x-8,h.y-50*h.f],[h.x+8,h.y-50*h.f]]);}},
  thresh(n=RI_SLOTS){for(let k=0;k<n;k++){const [x,y]=RI_SL[k];X.ri.tap(x,y+40);}},
  mochi(){if(G.id==="ri_field")riMochiStart(G,now());},
  hit(){const q=G.st;if(q.m){q.m.next=now();riMochiTap(G,now());}},
  turn(){const q=G.st;if(q.m){q.m.turn=now()-.05;}},
  birds(){if(G.id!=="ri_field")return;G.st.spT=0;}};
}
