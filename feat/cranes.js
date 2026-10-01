{
// ───────────────────────── «Тысяча журавликов» (senbazuru) ─────────────────────────
// The player folds paper cranes in a short swipe mini-game (up to 10 a day: the first counts ×3, the 2nd–3rd ×2), every
// befriended yōkai folds one a day by itself. The cranes hang in the bedroom as strings (one per 50, up to 20) that grow
// visibly. 100/250/500 → a thing; 1000 → a one-chapter scene (the strings glow, the cranes fly around Musya) and a wish.
// S.ext.cranes = {n:total, day:dayKey of k, k:folded by the player that day, fd:dayKey friends last folded, fr:[[id,name]] who
//   folded on fd, away:cranes friends folded since the postcard, ms:{100:1,…} milestones given, ready:1 → the wish waits,
//   wish:{t,d}|null, pat:last paper}
const CR=S.ext.cranes||(S.ext.cranes={n:0,day:"",k:0,fd:"",fr:[],away:0,ms:{},ready:0,wish:null,pat:0});CR.ms=CR.ms||{};CR.fr=CR.fr||[];
const CRR={k0:[0,0,72,46],k1:[76,0,72,46],k2:[152,0,72,46],k3:[228,0,72,46],k4:[304,0,72,46],k5:[380,0,72,46],k6:[456,0,72,46],k7:[532,0,72,46],k8:[608,0,72,46],k9:[684,0,72,46],
 p0:[760,0,160,160],p1:[0,164,160,160],p2:[164,164,160,160],p3:[328,164,160,160],p4:[492,164,160,160],p5:[656,164,160,160],
 cr_box:[0,328,190,140],cr_garland:[194,328,130,330],cr_furin:[328,328,110,250],cr_gold:[442,328,230,200]};   // assets/items/atlas_cr.webp (art/cranes_art.py)
const CR_PAPER=[["Асаноха","麻の葉","#2c3a66"],["Сэйгайха","青海波","#2e7a82"],["Сакура","桜","#d98aa0"],["Итимацу","市松","#b8322a"],["Киккō","亀甲","#7a4a8a"],["Кинпаку","金箔","#3c6a4a"]];
const CRC="Тысяча журавликов",crIt=(id,n,a,hint)=>({id,n,c:CRC,w:CRR[id][2],h:CRR[id][3],a,p:0,at:["cr",CRR[id][0],CRR[id][1]],src:"🕊 журавлики",hint});
addItems([crIt("cr_box","Шкатулка для бумаги","b","100 журавликов на гирлянде"),crIt("cr_garland","Гирлянда «Сто журавликов»","t","250 журавликов на гирлянде"),
 crIt("cr_furin","Фурин с журавлём","t","500 журавликов на гирлянде"),crIt("cr_gold","Золотой журавль","b","Тысяча журавликов и желание")],{cr:[1000,658]});
STAMPS.push(["cr_first","鶴","Первый журавлик","Сложи бумажного журавлика"],["cr_100","百","Сто журавликов","Набери сто журавликов на гирлянде"],["cr_1000","千","Тысяча журавликов","Набери тысячу журавликов и загадай желание"]);
const CR_MS=[[100,"cr_box"],[250,"cr_garland"],[500,"cr_furin"]];
document.head.insertAdjacentHTML("beforeend",`<style>.cr-big{font-size:17px;margin:2px 0 6px}.cr-big b{color:var(--sakura);font-size:22px}
.cr-bar{height:7px;border-radius:5px;background:rgba(255,255,255,.08);overflow:hidden;margin:0 0 8px}.cr-bar span{display:block;height:100%;background:linear-gradient(90deg,#c8322c,#e2b040,#6a9a58,#3d5f9e,#7a4a8a)}
.hubc p.cr-fr{font-size:13px;opacity:.85;margin:6px 0;line-height:1.5}.hubc p.cr-wish,.cr-wish{font-family:var(--display);font-size:18px;line-height:1.35;color:#f3d9a0;margin:6px 0}
.cr-wrow{display:flex;gap:8px;margin:10px 0}.cr-wrow .btn{flex:0 0 auto}.cr-wrow input{flex:1 1 auto;min-width:0;background:#15120f;color:#efe3c8;border:1px solid var(--line);border-radius:9px;padding:9px 10px;font:inherit}</style>`);

// ── counting ──
const crPl=(n,a,b,c)=>{const m=n%10,h=n%100;return m===1&&h!==11?a:m>=2&&m<=4&&(h<12||h>14)?b:c;};
const crW=n=>crPl(n,"журавлик","журавлика","журавликов");
const crList=a=>a.length<2?a.join(""):a.slice(0,-1).join(", ")+" и "+a[a.length-1];
function crDay(){if(CR.day!==dayKey()){CR.day=dayKey();CR.k=0;}}
const crLeft=()=>{crDay();return Math.max(0,10-CR.k);};
const crVal=k=>k===0?3:k<3?2:1;   // the first crane of the day counts ×3, the 2nd and 3rd ×2
const crStrN=()=>Math.min(20,Math.ceil(Math.min(CR.n,1000)/50));
let crQ=[],crDirty=true,crBooted=false;
function crAdd(v){const b=CR.n;CR.n+=v;crDirty=true;
  for(const [m,id] of CR_MS)if(b<m&&CR.n>=m&&!CR.ms[m]){CR.ms[m]=1;S.owned.add(id);loadItem(id);disc("crane","m"+m);if(m===100)award("cr_100");crQ.push(`🎁 ${IT[id].n} — в 🧺 Вещах`);}
  if(b<1000&&CR.n>=1000&&!CR.wish){CR.ready=1;crQ.push("🕊 Тысяча журавликов! Загадай желание в 家");}
  save();}
// friends: gate guests the player has fed, rare lantern guests, visitors the player has met
const CR_FEM={kitsune:1,nekomata:1,warashi:1,yuki:1,amabie:1,yosuzume:1},CR_PLU={kamaitachi:1};
const CR_RG={yuki:["m_rg_yuki","Юки-онна",500],kodama:["m_rg_kodama","Кодама",340],amabie:["m_rg_amabie","Амабиэ",410],usagi:["m_rg_usagi","Лунный кролик",390]};
function crFriends(){const o=[];for(const g of GUESTS){const f=S.friends[g.id];if(f&&f.n>0)o.push({id:g.id,n:g.n,mon:g.mon,h:g.h});}
  const L=S.ext.lan&&S.ext.lan.met;if(L)for(const k in CR_RG)if(L[k])o.push({id:k,n:CR_RG[k][1],mon:CR_RG[k][0],h:CR_RG[k][2]});
  const V=S.ext.vis&&S.ext.vis.m,VS=X.vs&&X.vs.VS;if(V&&VS)for(const v of VS)if(V[v.id]&&V[v.id].met)o.push({id:v.id,n:v.n,mon:v.mon,h:v.h});
  return o;}
const crVerb=id=>CR_PLU[id]?"сложили":CR_FEM[id]?"сложила":"сложил";
const crDays=(a,b)=>Math.round((Date.parse(b)-Date.parse(a))/864e5);
// once a day every friend folds a crane (missed days too, up to a week); a new friend joins in on the same day
function crFriendsTick(loud){const F=crFriends(),dk=dayKey();
  if(CR.fd!==dk){const d=CR.fd?clamp(crDays(CR.fd,dk),1,7):1;CR.fd=dk;CR.fr=F.map(f=>[f.id,f.n]);if(F.length){CR.away+=d*F.length;crAdd(d*F.length);}else save();return;}
  const nw=F.filter(f=>!CR.fr.some(r=>r[0]===f.id));if(!nw.length)return;
  for(const f of nw)CR.fr.push([f.id,f.n]);crAdd(nw.length);if(loud)crQ.push(`🕊 ${nw[0].n} ${crVerb(nw[0].id)} журавлика`);}
function crFoldDone(){crDay();const v=crVal(CR.k);CR.k++;const first=!ST.got.includes("cr_first");award("cr_first");if(first)disc("crane","m1");
  S.needs.joy=clamp(S.needs.joy+(CR.k===1?12:4),0,100);crAdd(v);return v;}

// ── the folding game ──
// a face = [x0,y0,x1,y1,x2,y2,x3,y3, shade, side(0 pattern, 1 back), alpha]; faces: tl, tr, bl, br, head, body; z = draw order
const F_=(a,s,sd,al=1)=>a.concat([s,sd,al]),HID=(x,y)=>[x,y,x,y,x,y,x,y,0,0,0];
const CR_ST=[
 {f:[F_([0,-1,0,0,-1,0,-1,0],.05,0),F_([0,-1,1,0,0,0,0,0],-.03,0),F_([-1,0,0,0,0,1,0,1],.02,0),F_([1,0,0,0,0,1,0,1],-.06,0),HID(0,.7),HID(0,.1)],z:[2,3,0,1,4,5]},
 {f:[F_([0,.5,0,-.5,-1,-.5,-1,-.5],.1,1),F_([0,.5,1,-.5,0,-.5,0,-.5],-.04,1),F_([-1,-.5,0,-.5,0,.5,0,.5],-.15,0),F_([1,-.5,0,-.5,0,.5,0,.5],-.2,0),HID(0,.5),HID(0,0)],z:[2,3,0,1,4,5]},
 {f:[F_([0,-.72,0,.72,-.52,0,-.52,0],.1,0),F_([0,-.72,.52,0,0,.72,0,.72],-.14,0),F_([-.5,.02,0,.05,-.02,.72,-.02,.72],-.22,0),F_([.5,.02,0,.05,.02,.72,.02,.72],-.26,0),HID(0,.72),HID(0,.1)],z:[2,3,0,1,4,5]},
 {f:[F_([0,-1.1,0,.3,-.38,.08,-.38,.08],.12,0),F_([0,-1.1,.38,.08,0,.3,0,.3],-.14,0),F_([-.38,.08,0,.3,-.03,.95,-.03,.95],-.04,0),F_([.38,.08,0,.3,.03,.95,.03,.95],-.18,0),HID(-.03,.95),HID(0,.2)],z:[2,3,0,1,4,5]},
 {f:[F_([0,-.95,0,.32,-.2,.12,-.2,.12],.12,0),F_([0,-.95,.2,.12,0,.32,0,.32],-.14,0),F_([-.16,.16,0,.32,-.78,-.54,-.8,-.56],.04,0),F_([.16,.16,0,.32,.86,-.62,.84,-.64],-.1,0),F_([-.8,-.56,-.74,-.5,-.92,-.76,-.92,-.76],.02,0),HID(0,.2)],z:[2,3,4,1,0,5]},
 {f:[F_([0,-.95,0,.32,-.2,.12,-.2,.12],.12,0),F_([0,-.95,.2,.12,0,.32,0,.32],-.14,0),F_([-.16,.16,0,.32,-.78,-.54,-.8,-.56],.04,0),F_([.16,.16,0,.32,.86,-.62,.84,-.64],-.1,0),F_([-.8,-.56,-.74,-.5,-.98,-.38,-.98,-.38],-.02,0),HID(0,.2)],z:[2,3,4,1,0,5]},
 {f:[F_([-.3,.04,.3,.04,-.4,.6,-.4,.6],.18,0),F_([0,-.06,.9,-.6,.53,0,.53,0],-.3,0),F_([-.4,.04,-.23,-.04,-.9,-.7,-.96,-.66],.06,0),F_([.26,-.04,.43,0,1.03,-.73,.96,-.73],-.08,0),F_([-.96,-.7,-.83,-.64,-1.1,-.43,-1.1,-.43],-.04,0),F_([-.47,0,0,-.23,.53,0,0,.26],0,0)],z:[1,3,5,2,4,0]}];
const CR_STEP=[["По диагонали","Сложи лист пополам — верхний угол к нижнему",[0,1],"↓"],["Базовый квадрат","Сложи ещё раз и расплющи в квадрат",[-1,0],"←"],
 ["Лепестковая складка","Подогни края к середине и подними лепесток",[1,0],"→"],["Шея и хвост","Выверни нижние углы вверх",[0,-1],"↑"],
 ["Голова","Загни кончик шеи вниз",[-.707,.707],"↙"],["Крылья","Опусти крылья и чуть подуй внутрь",[0,1],"↓"]];
const CR_REF=CR_ST[0].f.map((f,i)=>i<4?f:CR_ST[6].f[i]);   // pattern anchor: where each face lies on the flat sheet
let crIm=null;const crPats={};
function crImg(){if(crIm)return crIm;atlasImg("cr",im=>{crIm=im;});return null;}
function crPat(g,i){if(crPats[i])return crPats[i];const im=crImg();if(!im)return null;const r=CRR["p"+i],c=document.createElement("canvas");c.width=r[2];c.height=r[3];
  c.getContext("2d").drawImage(im,r[0],r[1],r[2],r[3],0,0,r[2],r[3]);return crPats[i]=g.createPattern(c,"repeat");}
const crEase=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
function crGeo(q){const a=CR_ST[Math.min(q.i,6)],b=CR_ST[Math.min(q.i+1,6)],p=q.i>=6?0:crEase(clamp(q.p,0,1));
  return{p,z:p<.5?a.z:b.z,f:a.f.map((fa,k)=>{const fb=b.f[k],o=[];for(let j=0;j<8;j++)o.push(fa[j]+(fb[j]-fa[j])*p);
    const flip=fa[9]!==fb[9];if(flip){const bm=1+.14*(1-Math.abs(2*p-1));for(let j=0;j<8;j+=2)o[j]*=bm;}o.push(fa[8]+(fb[8]-fa[8])*p-(flip?.35*(1-Math.abs(2*p-1)):0),p<.5?fa[9]:fb[9],fa[10]+(fb[10]-fa[10])*p);return o;})};}
// affine that carries a face's place on the flat sheet to where it is now (so the pattern folds with the paper)
function crAff(r,c){const a=r[2]-r[0],b=r[3]-r[1],cc=r[4]-r[0],d=r[5]-r[1],det=a*d-b*cc;if(Math.abs(det)<1e-6)return null;
  const ia=d/det,ib=-b/det,ic=-cc/det,id=a/det,ux=c[2]-c[0],uy=c[3]-c[1],vx=c[4]-c[0],vy=c[5]-c[1];
  const A=ux*ia+vx*ib,B=uy*ia+vy*ib,C=ux*ic+vx*id,D=uy*ic+vy*id;return[A,B,C,D,c[0]-A*r[0]-C*r[1],c[1]-B*r[0]-D*r[1]];}
function crPaper(g,q,cx,cy,R,rot,t){const G_=crGeo(q),pat=crPat(g,q.pat),col=CR_PAPER[q.pat][2],P=(x,y)=>[cx+(x*Math.cos(rot)-y*Math.sin(rot))*R,cy+(x*Math.sin(rot)+y*Math.cos(rot))*R];
  const path=f=>{g.beginPath();for(let j=0;j<4;j++){const [x,y]=P(f[j*2],f[j*2+1]);j?g.lineTo(x,y):g.moveTo(x,y);}g.closePath();};
  g.save();g.shadowColor="rgba(0,0,0,.5)";g.shadowBlur=16*G.s;g.shadowOffsetY=9*G.s;g.fillStyle="#2a2018";
  for(const f of G_.f)if(f[10]>.5){path(f);g.fill();}g.restore();
  const lg=g.createLinearGradient(cx-R,cy-R,cx+R,cy+R);lg.addColorStop(0,"rgba(255,240,210,.16)");lg.addColorStop(1,"rgba(0,0,0,.18)");
  for(const k of G_.z){const f=G_.f[k];if(f[10]<.02)continue;g.save();g.globalAlpha=f[10];path(f);
    if(f[9]===0&&pat){const sc=[],rf=CR_REF[k];for(let j=0;j<3;j++){const [x,y]=P(f[j*2],f[j*2+1]);sc.push(x,y);}
      const m=crAff(rf,sc);if(m){const s=1/110,M=new DOMMatrix([m[0],m[1],m[2],m[3],m[4],m[5]]).multiply(new DOMMatrix([s*.707,s*.707,-s*.707,s*.707,0,0]));pat.setTransform(M);g.fillStyle=pat;}else g.fillStyle=col;}
    else g.fillStyle=f[9]===0?col:"#ece3d0";
    g.fill();const sh=f[8];g.fillStyle=sh>0?`rgba(255,246,226,${sh})`:`rgba(10,6,4,${-sh})`;g.fill();g.fillStyle=lg;g.fill();
    g.strokeStyle="rgba(30,20,14,.42)";g.lineWidth=1;g.lineJoin="round";g.stroke();g.restore();}}
function crArrow(g,cx,cy,R,d,t,a){const L=R*.62,x0=cx-d[0]*L,y0=cy-d[1]*L,x1=cx+d[0]*L,y1=cy+d[1]*L,u=(t*.8)%1;g.save();g.globalAlpha=a;
  g.strokeStyle="rgba(243,222,170,.85)";g.lineWidth=4*G.s;g.lineCap="round";g.setLineDash([2*G.s,10*G.s]);g.beginPath();g.moveTo(x0,y0);g.lineTo(x1,y1);g.stroke();g.setLineDash([]);
  const hx=x1,hy=y1,an=Math.atan2(d[1],d[0]);g.fillStyle="rgba(243,222,170,.95)";g.beginPath();g.moveTo(hx+Math.cos(an)*14*G.s,hy+Math.sin(an)*14*G.s);
  g.lineTo(hx+Math.cos(an+2.4)*14*G.s,hy+Math.sin(an+2.4)*14*G.s);g.lineTo(hx+Math.cos(an-2.4)*14*G.s,hy+Math.sin(an-2.4)*14*G.s);g.fill();
  const fx=mix(x0,x1,u),fy=mix(y0,y1,u),gr=g.createRadialGradient(fx,fy,0,fx,fy,22*G.s);gr.addColorStop(0,"rgba(255,236,190,.9)");gr.addColorStop(1,"rgba(255,236,190,0)");
  g.fillStyle=gr;g.fillRect(fx-22*G.s,fy-22*G.s,44*G.s,44*G.s);g.restore();}
const crLay=G=>{const W=G.W,H=G.H,R=Math.min(W*.33,H*.22),cy=H*.42;return{W,H,R,cx:W/2,cy,mx:W*.2,my:Math.min(H-4*G.s,cy+R*1.95),top:H*.075};};
function crPaw(q,t){q.paw=t;q.wob=t+.25;}
const CR_GAME={id:"cr_fold",hidden:true,n:"Журавлик",tag:"折り鶴 · Оригами",icon:"🕊",bg:"room",lives:null,time:null,lore:"",how:"",
 init(G,t){const q=G.st;const o=[0,1,2,3,4,5].sort(()=>Math.random()-.5).slice(0,3);Object.assign(q,{ph:"pick",opts:o,pat:o[0],i:0,p:0,drag:null,anim:null,paw:-9,wob:-9,idle:t,t1:0,fx:[],v:0,no:0,bad:-9});G.score=0;crImg();},
 step(G,t,dt){const q=G.st;
   if(q.anim){const u=(t-q.anim.t0)/.42;q.p=mix(q.anim.from,1,u);if(u>=1){q.anim=null;q.i++;q.p=0;q.idle=t;tone(520+q.i*70,.14,"triangle",.05);tone(180,.06,"sawtooth",.015);
       if(Math.random()<.5)crPaw(q,t+.1);
       if(q.i>=6){q.ph="done";q.t1=t;q.v=crFoldDone();q.no=CR.n;G.score=q.v;chime([988,1318,1568,2093]);
         const L=crLay(G);for(let k=0;k<36;k++){const a=rand(0,Math.PI*2),v=rand(60,260)*G.s;q.fx.push({x:L.cx,y:L.cy,vx:Math.cos(a)*v,vy:Math.sin(a)*v-90*G.s,life:rand(.7,1.4)});}}}}
   else if(!q.drag&&q.p>0){q.p=Math.max(0,q.p-dt*3);}
   if(q.ph==="fold"&&!q.drag&&!q.anim&&t-q.idle>6){q.idle=t;crPaw(q,t);}
   for(const f of q.fx){f.x+=f.vx*dt;f.y+=f.vy*dt;f.vy+=200*G.s*dt;f.life-=dt;}q.fx=q.fx.filter(f=>f.life>0);
   if(q.ph==="done"&&t-q.t1>2.7&&!q.ended){q.ended=1;gEnd();}},
 draw(G,g,t){const q=G.st,L=crLay(G),s=G.s,{W,H,R,cx,cy}=L;
   // low lacquer table and the lantern light
   g.save();const tg=g.createLinearGradient(0,cy-R*1.5,0,cy+R*1.7);tg.addColorStop(0,"#3a2418");tg.addColorStop(1,"#1c110c");g.fillStyle=tg;g.beginPath();g.roundRect(W*.04,cy-R*1.45,W*.92,R*3.05,22*s);g.fill();
   g.strokeStyle="rgba(210,160,90,.25)";g.lineWidth=2;g.stroke();g.strokeStyle="rgba(0,0,0,.14)";g.lineWidth=1;for(let k=1;k<9;k++){const y=cy-R*1.45+k*R*.34;g.beginPath();g.moveTo(W*.06,y);g.bezierCurveTo(W*.4,y+4*s,W*.6,y-4*s,W*.94,y+2*s);g.stroke();}const lg=g.createRadialGradient(W*.3,cy-R,0,W*.3,cy-R,R*3);lg.addColorStop(0,"rgba(255,200,130,.2)");lg.addColorStop(1,"rgba(255,200,130,0)");g.fillStyle=lg;g.fillRect(0,0,W,H);g.restore();
   if(!crImg()){textC(g,"…",cx,cy,20*s);return;}
   const pawing=t-q.paw<.9&&t>=q.paw;
   if(q.ph==="pick"){textC(g,"Выбери бумагу",cx,L.top,20*s,"#f3ead8",800);textC(g,"квадрат васи — японской бумаги",cx,L.top+24*s,13*s,"rgba(216,210,195,.75)",500);
     const sz=Math.min(W*.27,H*.17);q.boxes=q.opts.map((o,k)=>{const x=W*(.2+k*.3),y=cy-R*.2+Math.sin(t*1.6+k)*3*s;
       g.save();g.translate(x,y);g.rotate(.06*Math.sin(t*.9+k*2));g.shadowColor="rgba(0,0,0,.5)";g.shadowBlur=12*s;g.shadowOffsetY=6*s;const pt=crPat(g,o);g.fillStyle=CR_PAPER[o][2];g.fillRect(-sz/2,-sz/2,sz,sz);
       if(pt){pt.setTransform(new DOMMatrix([sz/160,0,0,sz/160,-sz/2,-sz/2]));g.shadowColor="transparent";g.fillStyle=pt;g.fillRect(-sz/2,-sz/2,sz,sz);}g.restore();
       textC(g,CR_PAPER[o][0],x,y+sz*.5+18*s,14*s,"#efe3c8",700);jpText(g,CR_PAPER[o][1],x,y+sz*.5+38*s,13*s,"rgba(238,163,187,.85)");return[x,y,sz];});}
   else{const wob=t>q.wob?.07*Math.sin((t-q.wob)*17)*Math.exp(-(t-q.wob)*4):0;let px_=cx,py_=cy,RR=R,al=1;
     if(q.ph==="done"){const e=t-q.t1;RR=R*(1+.08*Math.sin(Math.min(e,1.2)*Math.PI/1.2));py_=cy+Math.sin(t*3)*4*s;if(e>1.5){const u=(e-1.5)/1.1;py_-=u*u*H*.7;px_+=u*W*.25;RR*=1-u*.6;al=clamp(1-u*1.1,0,1);}
       const gr=g.createRadialGradient(cx,cy,0,cx,cy,R*1.6);gr.addColorStop(0,`rgba(255,220,150,${.28*al})`);gr.addColorStop(1,"rgba(255,220,150,0)");g.fillStyle=gr;g.fillRect(0,0,W,H);}
     g.save();g.globalAlpha=al;crPaper(g,q,px_,py_,RR,wob,t);g.restore();
     if(q.ph==="fold"){const S_=CR_STEP[q.i];textC(g,`Шаг ${q.i+1} из 6 · ${S_[0]}`,cx,L.top,19*s,"#f3ead8",800);textC(g,S_[1],cx,L.top+24*s,13*s,"rgba(216,210,195,.8)",500);
       if(!q.anim&&q.p<.15)crArrow(g,cx,cy,R,S_[2],t,t-q.bad<.8?.4+.6*Math.abs(Math.sin(t*14)):.9);
       for(let k=0;k<6;k++){g.fillStyle=k<q.i?"#e6a2b4":k===q.i?"rgba(243,234,216,.9)":"rgba(243,234,216,.25)";g.beginPath();g.arc(cx+(k-2.5)*18*s,cy+R*1.32,(k===q.i?5:4)*s,0,Math.PI*2);g.fill();}
       if(t-q.bad<1.2)textC(g,`Проведи пальцем ${S_[3]}`,cx,cy+R*1.62,15*s,"rgba(243,222,170,.95)",700);}
     else{const e=t-q.t1;if(e>.5){const a=clamp((e-.5)/.4,0,1);textC(g,`Журавлик №${q.no}`,cx,L.top,22*s,`rgba(243,234,216,${a})`,800);
       textC(g,q.v>1?`+${q.v} — ${q.v===3?"первый журавлик дня к удаче":"утренние журавлики считаются вдвойне"}`:"+1 на гирлянду",cx,L.top+26*s,14*s,`rgba(238,163,187,${a})`,600);}}}
   for(const p of q.fx){g.fillStyle=`rgba(255,${200+(p.x*7%50)|0},180,${clamp(p.life,0,1)})`;g.beginPath();g.arc(p.x,p.y,2.4*s,0,Math.PI*2);g.fill();}
   // Musya watches the paper and paws at it now and then
   if(pawing)drawCatG(g,"highfive",Math.floor((t-q.paw)*5)%2?3:2,L.mx,L.my,.82*s);
   else drawCatG(g,"rest",[0,0,0,6,0,0,7,0][Math.floor(t*.7)%8],L.mx,L.my,.82*s);},
 down(G,x,y,t){const q=G.st;
   if(q.ph==="pick"){for(let k=0;k<(q.boxes||[]).length;k++){const [bx,by,sz]=q.boxes[k];if(Math.abs(x-bx)<sz*.6&&Math.abs(y-by)<sz*.6){q.pat=q.opts[k];CR.pat=q.pat;q.ph="fold";q.idle=t;sfx("pop");tone(330,.1,"sawtooth",.02);return;}}return;}
   if(q.ph==="fold"&&!q.anim)q.drag={x0:x,y0:y,t0:t,mx:0};},
 move(G,x,y,held){const q=G.st;if(!q.drag||!held||q.ph!=="fold")return;const d=CR_STEP[q.i][2],dx=x-q.drag.x0,dy=y-q.drag.y0,along=dx*d[0]+dy*d[1];
   q.drag.mx=Math.max(q.drag.mx,Math.hypot(dx,dy));q.drag.al=along;q.p=clamp(along/(crLay(G).R*1.1),0,.85);if(q.p>.02)q.idle=now();},
 up(G){const q=G.st;if(!q.drag)return;const D=q.drag,t=now();q.drag=null;if(q.ph!=="fold")return;
   if(q.p>.3||(D.al||0)>24*G.s&&t-D.t0<.3){q.anim={from:q.p,t0:t};tone(240,.05,"sawtooth",.015);}
   else if(D.mx>24*G.s){q.bad=t;crPaw(q,t);sfx("bad");}else q.bad=t;},
 stat:G=>`🕊 ${CR.n} / 1000 · сегодня ${CR.k}/10`,
 card(G){const q=G.st,left=crLeft(),m=CR_MS.find(z=>CR.ms[z[0]]&&q.no-q.v<z[0]&&q.no>=z[0]);
   return`<div class="card"><p class="tag">折り鶴 · ${CR_PAPER[q.pat][0]}</p><h3>Журавлик №${q.no}</h3><div class="big">${Math.min(CR.n,1000)} / 1000</div>
   <p>${q.v===3?"Первый журавлик дня — к удаче: он засчитан за три.":q.v===2?"Утренние журавлики считаются вдвойне.":"Ещё один журавлик на нитке."} Сегодня сложено ${CR.k} из 10.</p>
   ${m?`<div class="dish">${itemThumb(IT[m[1]],120,110)}</div><p>${m[0]} журавликов! ${IT[m[1]].n} — в «🧺 Вещи».</p>`:CR.ready?`<p>🕊 Тысяча! Загадай желание в «家».</p>`:`<p>Гирлянда висит в спальне: ${crStrN()} ${crPl(crStrN(),"нитка","нитки","ниток")}.</p>`}
   <div class="row"><button class="btn" id="gHome">Готово</button><button class="btn primary" id="gAgain" style="${left?"":"display:none"}">Ещё журавлик · ${left}</button></div></div>`;},
 after(){ui();hubDot();}};
GAMES.push(CR_GAME);
function crOpen(){if(G.id)return;if(!crLeft()){toast("🕊 На сегодня хватит — 10 из 10. Завтра ещё");return;}closePanel();openPlace("cr_fold");}

// ── the strings in the bedroom ──
// slot k → image x; strings fill from the middle outwards; each hangs from a bamboo rod at y=88 and is 700 px long
const CR_D=.62,CR_Y=88,CR_L=700,CR_SLOT=Array.from({length:20},(_,i)=>560+i*42),CR_ORD=Array.from({length:20},(_,i)=>i).sort((a,b)=>Math.abs(a-9.5)-Math.abs(b-9.5)||a-b);
const crStr={};let crHit=null,crGust=-9,crGlow=-99;
function crBuild(i,cnt,dark){const im=crImg();if(!im)return null;const c=document.createElement("canvas");c.width=64;c.height=CR_L;const g=c.getContext("2d"),r=rng(i*97+5);
  g.strokeStyle="rgba(232,216,180,.55)";g.lineWidth=1.2;g.beginPath();g.moveTo(32,0);g.lineTo(32,24+cnt*13);g.stroke();
  for(let j=0;j<cnt;j++){const ci=(Math.floor(j/5)+i)%10,rc=CRR["k"+ci],y=14+j*13,sc=.62+r()*.06;g.save();g.translate(32+(r()-.5)*3,y);g.rotate((r()-.5)*.12);
    g.drawImage(im,rc[0],rc[1],rc[2],rc[3],-36*sc,-23*sc,72*sc,46*sc);g.restore();}
  if(cnt>=50){const y=24+cnt*13;g.fillStyle="#b8322a";g.beginPath();g.arc(32,y,4,0,Math.PI*2);g.fill();g.strokeStyle="#a02a24";g.lineWidth=1.4;for(let k=-2;k<=2;k++){g.beginPath();g.moveTo(32,y+3);g.lineTo(32+k*1.6,y+24);g.stroke();}}
  g.globalCompositeOperation="source-atop";g.fillStyle=dark?"rgba(8,10,26,.62)":"rgba(40,25,10,.2)";g.fillRect(0,0,64,CR_L);return c;}
function crStrings(){const N=Math.min(CR.n,1000),o=[];for(let k=0;k<20;k++){const c=Math.max(0,Math.min(50,N-k*50));if(c>0)o.push([CR_ORD[k],c]);}return o;}
function crDraw(t){const L=crStrings();if(!L.length)return;if(crDirty){for(const k in crStr)delete crStr[k];crDirty=false;}
  const dark=!!S.lampOff,xs=L.map(z=>CR_SLOT[z[0]]),x0=Math.min(...xs)-30,x1=Math.max(...xs)+30;
  const [ax,ay]=imgToStage(x0,CR_Y,CR_D),[bx,by]=imgToStage(x1,CR_Y,CR_D),k=Math.hypot(bx-ax,by-ay)/(x1-x0);
  // cords to the beam, the rod
  const [cx0,cy0]=imgToStage(x0+8,60,CR_D),[cx1,cy1]=imgToStage(x1-8,60,CR_D);ctx.save();ctx.strokeStyle=dark?"rgba(70,62,52,.8)":"rgba(150,120,80,.85)";ctx.lineWidth=Math.max(1,1.4*k);
  ctx.beginPath();ctx.moveTo(cx0,cy0);ctx.lineTo(ax+8*k,ay);ctx.moveTo(cx1,cy1);ctx.lineTo(bx-8*k,by);ctx.stroke();
  ctx.strokeStyle=dark?"#3a3424":"#8a7444";ctx.lineWidth=Math.max(2,7*k);ctx.lineCap="round";ctx.beginPath();ctx.moveTo(ax,ay);ctx.lineTo(bx,by);ctx.stroke();
  ctx.strokeStyle=dark?"rgba(120,110,80,.4)":"rgba(230,210,150,.55)";ctx.lineWidth=Math.max(1,2*k);ctx.beginPath();ctx.moveTo(ax,ay-2*k);ctx.lineTo(bx,by-2*k);ctx.stroke();ctx.restore();
  const glow=CR.wish||CR.ready||scene.on&&scene.book===CR_BOOK,gu=t-crGust,ga=gu<4?Math.exp(-gu*.9)*.09:0;let ymax=ay;
  for(const [sl,cnt] of L){const key=sl+(dark?"d":"l");let c=crStr[key];if(!c||c.n!==cnt){c=crBuild(sl,cnt,dark);if(!c)return;c.n=cnt;crStr[key]=c;}
    const [tx,ty]=imgToStage(CR_SLOT[sl],CR_Y,CR_D),[,by2]=imgToStage(CR_SLOT[sl],CR_Y+CR_L,CR_D),kk=(by2-ty)/CR_L,a=.018*Math.sin(t*.7+sl*.9)+.008*Math.sin(t*1.9+sl)+ga*Math.sin(gu*5+sl*.6);
    if(glow&&(dark||dayTint()[1])){const e=scene.on&&scene.book===CR_BOOK?1:.45+.15*Math.sin(t*1.3+sl),R=60*kk,h=(24+cnt*13)*kk;ctx.save();ctx.globalCompositeOperation="lighter";
      const gr=ctx.createLinearGradient(tx-R,0,tx+R,0);gr.addColorStop(0,"rgba(255,200,120,0)");gr.addColorStop(.5,`rgba(255,200,120,${.16*e})`);gr.addColorStop(1,"rgba(255,200,120,0)");ctx.fillStyle=gr;ctx.fillRect(tx-R,ty,R*2,h);ctx.restore();}
    ctx.save();ctx.translate(tx,ty);ctx.rotate(a);ctx.drawImage(c,-32*kk,0,64*kk,CR_L*kk);ctx.restore();ymax=Math.max(ymax,ty+(30+cnt*13)*kk);}
  crHit=[Math.min(ax,bx)-10,Math.min(ay,by,cy0)-10,Math.max(ax,bx)+10,ymax];}
hook("draw",(t,front)=>{if(front)return;if(S.room!=="bedroom"){crHit=null;return;}crDraw(t);});
hook("hit",(x,y)=>{if(S.room!=="bedroom"||!crHit||scene.on)return false;const b=crHit;if(x<b[0]||x>b[2]||y<b[1]||y>b[3])return false;crGust=now();
  const n=CR.n;toast(n>=1000?(CR.wish?"🕊 Тысяча журавликов. Желание бережётся":"🕊 Тысяча! Загадай желание в 家"):`🕊 Журавликов: ${n} из 1000`);
  if(snd.on&&snd.ctx){tone(1568,.5,"sine",.02);setTimeout(()=>tone(2093,.6,"sine",.015),120);}return true;});

// ── 1000: the wish ──
const CR_BOOK=[{title:"Тысяча журавликов",room:"bedroom",intro:{p:[],chars:[]}}];
const CR_SLOTS=[[-330,1236],[330,1236],[-470,1180],[470,1180]];
function crWishStart(){if(!CR.ready||scene.on||G.id)return;closePanel();
  const F=crFriends().filter(f=>MON[f.mon]).slice(0,4),names=F.map(f=>f.n);
  const chars=F.map((f,i)=>({id:f.mon,x:()=>visX(900+CR_SLOTS[i][0],120),y:CR_SLOTS[i][1],h:Math.round(Math.min(f.h||340,420)*.7),d:.8,from:1+i*.5})).sort((a,b)=>a.y-b.y);
  CR_BOOK[0].intro={chars,p:["Тысячный журавлик лёг на нитку — и вся гирлянда тихо засветилась, будто в каждой бумажной птице зажгли по крошечному фонарику.",
    "Старики говорят: журавль живёт тысячу лет. Кто сложит тысячу бумажных журавлей, тому исполнится одно желание — каждая птица отдаёт ему свой год.",
    `Нитки качнулись, и журавлики снялись с них. Тысяча бумажных крыльев шуршит над Мусей, как дождь по сёдзи.${names.length?` ${crList(names)} смотрят, затаив дыхание.`:""}`,
    "Муся смотрит вверх и не мигает. Загадай желание — журавлики унесут его туда, где желания слышат."]};
  crGlow=now();playScene(0,"intro",crWishPanel,false,CR_BOOK);}
function crWishPanel(){if(CR.wish)return;openPanel("Желание тысячи журавликов",`<p class="lead">Напиши своё желание. Журавлики сберегут его, а в альбоме оно останется навсегда.</p>
  <div class="cr-wrow"><input id="crWishIn" maxlength="80" placeholder="Чтобы Муся всегда была рядом…"><button class="btn primary" data-x="cr:wish">Загадать</button></div>`,"cr_wish");$("xpBody").scrollTop=0;}
function crWish(v){CR.wish={t:v.slice(0,80),d:dayKey()};CR.ready=0;S.owned.add("cr_gold");loadItem("cr_gold");award("cr_1000");disc("crane","m1000");crGlow=now();save();
  closePanel();chime([1046,1318,1568,2093]);if(!petAway()){burst(16);setTimeout(()=>react("😻",2.4),400);}setTimeout(()=>toast("✨ Желание загадано · 🧺 Золотой журавль"),700);hubDot();}
// the cranes take off and circle around Musya while the scene plays (and settle back afterwards)
const CR_FLY=Array.from({length:42},(_,i)=>({c:i%10,ph:i*2.39,r:.55+(i*37%42)/42*.6,h:(i*53%42)/42,sp:.5+(i*29%42)/42*.5,sl:i%20}));
hook("overlay",t=>{if(S.room!=="bedroom"||petAway())return;const on=scene.on&&scene.book===CR_BOOK,e=t-crGlow;if(!on&&e>3.5)return;
  const im=crImg();if(!im)return;const fly=on?clamp(scene.i-1.6+Math.min(1,(t-scene.t0)*.05),0,1):clamp(1-e/3,0,1);if(fly<=0)return;
  const [mx,my]=cellToStage(97,120),s=view.s;
  for(const q of CR_FLY){const sl=CR_SLOT[q.sl],[hx,hy]=imgToStage(sl,CR_Y+120+q.h*400,CR_D),a=t*q.sp+q.ph,ox=mx+Math.cos(a)*q.r*230*s,oy=my-60*s-q.h*170*s+Math.sin(a)*q.r*50*s-Math.sin(t*.7+q.ph)*14*s;
    const u=smooth(clamp(fly*1.6-q.h*.6,0,1)),x=mix(hx,ox,u),y=mix(hy,oy,u),rc=CRR["k"+q.c],sz=(30+q.r*14)*s*(0.75+.25*Math.sin(a)),fl=.6+.4*Math.abs(Math.sin(t*7+q.ph));
    ctx.save();ctx.globalAlpha=.4+.6*u;ctx.translate(x,y);if(Math.cos(a)>0)ctx.scale(-1,1);ctx.scale(1,fl);ctx.drawImage(im,rc[0],rc[1],rc[2],rc[3],-sz/2,-sz*.32,sz,sz*.64);ctx.restore();
    if(u>.3){ctx.save();ctx.globalCompositeOperation="lighter";ctx.globalAlpha=.25*u;const gr=ctx.createRadialGradient(x,y,0,x,y,sz*.7);gr.addColorStop(0,"rgba(255,215,140,.8)");gr.addColorStop(1,"rgba(255,215,140,0)");ctx.fillStyle=gr;ctx.fillRect(x-sz,y-sz,sz*2,sz*2);ctx.restore();}}});
hook("tick",()=>{if(!scene.on||scene.book!==CR_BOOK)return;if(scene.i===CR_BOOK[0].intro.p.length-1)$("scNext").textContent="Загадать ✨";});

// ── boot, the day, the hub card, the dot, the postcard, the album ──
hook("boot",()=>{crBooted=true;crImg();crDay();crFriendsTick(false);for(const id of ["cr_box","cr_garland","cr_furin","cr_gold"])if(S.owned.has(id))loadItem(id);});
let crSec=0;
hook("sec",()=>{if(!crBooted)return;if(++crSec%10===0)crFriendsTick(true);if(crQ.length&&!overlaysOpen()&&!scene.on)toast(crQ.shift());});
hook("hubDot",()=>crBooted&&(!!CR.ready||(crDay(),CR.k===0)));
hook("away",()=>{crFriendsTick(false);const n=CR.away;if(!n)return null;CR.away=0;save();const nm=CR.fr.map(r=>r[1]);
  return{i:"🕊",t:`Пока тебя не было, друзья сложили ${n} ${crW(n)}: ${crList(nm.slice(0,3))}${nm.length>3?" и другие":""}. На гирлянде ${Math.min(CR.n,1000)} из 1000.`};});
hook("hub",()=>{crDay();const n=CR.n,sn=crStrN(),left=crLeft(),F=CR.fd===dayKey()?CR.fr:[];
  const fr=F.length?`<p class="cr-fr">${F.slice(0,4).map(r=>`🕊 ${r[1]} ${crVerb(r[0])} журавлика`).join("<br>")}${F.length>4?`<br>…и ещё ${F.length-4}: каждый по журавлику`:""}</p>`
    :`<p class="cr-fr">Друзья-ёкаи помогают: каждый, кого ты угостишь у ворот или встретишь, складывает по журавлику в день.</p>`;
  return`<div class="hubc"><h4>🕊 Тысяча журавликов <i>千羽鶴</i></h4>
   <p class="cr-big"><b>${Math.min(n,1000)}</b> / 1000${sn?` · ${sn} ${crPl(sn,"нитка","нитки","ниток")} в спальне`:""}</p><div class="cr-bar"><span style="width:${Math.min(100,n/10)}%"></span></div>
   ${CR.wish?`<p class="cr-wish">«${esc(CR.wish.t)}»</p><p>Тысяча журавликов сберегают твоё желание.</p>`:CR.ready?`<p class="cr-wish">Тысяча журавликов готова. Пора загадать желание!</p>`:
     `<p>Легенда говорит: сложи тысячу журавликов — и исполнится желание. ${CR.k?`Сегодня сложено ${CR.k} из 10.`:"Сегодня ещё ни одного: первый журавлик дня засчитывается за три."}</p>`}
   ${fr}<div class="row">${CR.ready?`<button class="btn primary" data-x="cr:wishgo">✨ Загадать желание</button>`:""}<button class="btn ${CR.ready?"":"primary"}" data-x="cr:fold" ${left?"":"disabled"}>🕊 ${left?"Сложить журавлика":"На сегодня 10 из 10"}</button><button class="btn" data-x="cr:see">Гирлянда</button></div></div>`;});
hook("click",k=>{if(k==="cr:fold"){crOpen();return true;}if(k==="cr:see"){closePanel();goRoom("bedroom");return true;}if(k==="cr:wishgo"){crWishStart();return true;}
  if(k==="cr:wish"){const el=$("crWishIn"),v=el&&el.value.trim();if(!v){el&&el.focus();return true;}crWish(v);return true;}return false;});
hook("panelClose",id=>{if(id==="cr_wish"&&CR.ready)setTimeout(()=>toast("🕊 Желание подождёт — кнопка в 家"),300);});
hook("album",el=>{if(!CR.n)return;const its=["cr_box","cr_garland","cr_furin","cr_gold"];
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Тысяча журавликов</h3><p class="lead">На гирлянде ${Math.min(CR.n,1000)} из 1000.${CR.wish?` Желание (${CR.wish.d.slice(8)}.${CR.wish.d.slice(5,7)}.${CR.wish.d.slice(0,4)}): «${esc(CR.wish.t)}»`:""}</p>
   <div class="coll">${its.map(id=>`<div class="ci ${S.owned.has(id)?"on":""}">${itemThumb(IT[id],70,52)}<small>${S.owned.has(id)?IT[id].n:"???"}</small></div>`).join("")}</div>`);});

// test handles
X.cr={C:CR,add:crAdd,open:crOpen,friends:crFriends,tick:crFriendsTick,wish:crWishStart,setWish:crWish,hit:()=>crHit,
  swipe(p){if(G.id!=="cr_fold")return;const q=G.st;if(q.ph==="pick"){q.pat=q.opts[0];q.ph="fold";return;}if(p==null){q.anim={from:0,t0:now()};}else{q.p=p;q.drag={x0:0,y0:0,t0:now(),mx:0};}},
  pick(i){if(G.id==="cr_fold"){const q=G.st;q.pat=q.opts[i||0];q.ph="fold";}},
  tap(){if(!crHit)return false;const x=(crHit[0]+crHit[2])/2,y=(crHit[1]+crHit[3])/2;return hk("hit",x,y);}};
}
