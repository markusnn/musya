{
// ───────────────────────── «Бонсай» 盆栽: a procedural tree in a pot on the veranda — grows every day; prune, wire and water it on the bench ─────────────────────────
// S.ext.bonsai = {sp:"momiji"|"matsu", pot:0..2, born:dayKey, sd:seed, n:next seg id, g:[[parent,relAngle,len,bornDay,id,wireDay+1]…] (parents first),
//   last:dayKey growth was counted, wat:dayKey watered, tend:dayKey tended, cutd:dayKey of the last cut, fresh:shoots since the last cut,
//   ft/fd:shoots that came on day fd, care:days tended, cuts, kod:dayKey the kodama last looked, named:[styles he named], flip:0|1}
// tree units (TU): the trunk foot is (0,0) on the soil, y grows downward; angle 0 = straight up, clockwise positive
const BN_SP={momiji:{n:"Клён момидзи",jp:"紅葉",d:"Весной красные листочки, осенью горит, зимой стоит голый"},matsu:{n:"Сосна мацу",jp:"松",d:"Зелёная круглый год, весной выпускает светлые «свечи»"}};
const BN_POT=[{n:"Селадон",w:196,b:172,h:34,c:["#b4d2c2","#6a988a","#2c4a44"],gl:1,sh:"oval"},{n:"Токонамэ",w:210,b:204,h:44,c:["#a8664a","#70402e","#381e14"],gl:0,sh:"rect"},
  {n:"Кобальт",w:150,b:104,h:62,c:["#8ea2dc","#34489a","#141c4a"],gl:1,sh:"round"}];
const BN_STY={chokkan:["Тёккан","直幹","прямой ствол, вершина ровно над корнем"],moyogi:["Моёги","模様木","ствол плавно изгибается, вершина над корнем"],
  shakan:["Сякан","斜幹","ствол наклонён, будто дерево всю жизнь росло на ветру"],kengai:["Кэнгай","懸崖","ветви свешиваются ниже края горшка, как сосна над обрывом"],
  bunjin:["Бундзин","文人","«стиль литератора»: голый тонкий ствол и крона только наверху"]};
const BN_KOD={chokkan:"Прямой, как кедр у моего святилища. Тёккан — строгий стиль.",moyogi:"Ствол петляет, как горная тропа. Это моёги.",
  shakan:"Клонится, будто всю жизнь стоял на ветру. Сякан.",kengai:"Свешивается, как сосна над обрывом. Кэнгай — смелое дерево.",bunjin:"Тонкий, одинокий, крона только наверху. Бундзин — дерево поэта."};
const BN_HI=["Можно взглянуть на дерево?.. …ерево… …ерево…","Каждое воскресенье прихожу. Ну-ка, как оно подросло?","Тихо… Я только посмотрю. Деревья любят, когда на них смотрят."];
const BN_BARK={momiji:["#17110e","#4a3d34","#9a8877"],matsu:["#150c07","#4a2b1f","#9a6e50"]};
const BN_X=1190,BN_Y=1296;   // where the tree stands on the veranda (image coords; visible on a phone, right of Musya)
STAMPS.push(["bn_cut","鋏","Первый срез","Срежь ветку бонсая ножницами"],["bn_30","盆","Месяц заботы","Ухаживай за бонсаем 30 разных дней"],["bn_named","幹","Имя стиля","Покажи бонсай кодаме — он приходит по воскресеньям"]);
addItems([{id:"bn_tree",n:"Мой бонсай",c:"Веранда",w:230,h:270,a:"b",p:0,src:"🌳 своё дерево",hint:"Посади бонсай: Веранда → «🌳 Бонсай»"}]);
// the veranda picture is a live render: DIMG gets a canvas, so the core never loads a file for it
const BN_CV=document.createElement("canvas");BN_CV.width=460;BN_CV.height=540;DIMG.bn_tree=BN_CV;loadItem.bn_tree=1;let bnUrl=null;

const bnS=()=>S.ext.bonsai||null;
const bnDN=k=>Math.round(Date.parse(k)/864e5),bnKey=n=>new Date(n*864e5).toISOString().slice(0,10);
const bnAge=T=>Math.max(0,bnDN(dayKey())-bnDN(T.born)),bnSun=()=>today().getDay()===0;
function bnWord(n,f){const a=n%10,b=n%100;return n+" "+(a===1&&b!==11?f[0]:a>=2&&a<=4&&(b<12||b>14)?f[1]:f[2]);}
const bnHex=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16));
function bnMix(a,b,t){const A=bnHex(a),B=bnHex(b);return"#"+A.map((v,i)=>Math.round(v+(B[i]-v)*clamp(t,0,1)).toString(16).padStart(2,"0")).join("");}
function bnSea(){const T=today(),doy=T.getMonth()*30.5+T.getDate();
  if(doy<70||doy>=340)return{k:"winter",p:0};if(doy<140)return{k:"spring",p:(doy-70)/70};if(doy<263)return{k:"summer",p:(doy-140)/123};return{k:"autumn",p:(doy-263)/77};}
// foliage colours [shadow, body, light] by species, season and freshness; null = bare (maple in winter)
function bnLeaf(sp,fresh,j=0){const S0=bnSea();let md;
  if(sp==="matsu")md=fresh&&S0.k==="spring"?"#a9bb72":S0.k==="winter"?"#2c4436":fresh?"#5d7e44":"#33502f";
  else{if(S0.k==="winter")return null;
    if(S0.k==="spring")md=fresh||S0.p<.25?"#a4503c":bnMix("#86a94a","#4f7232",S0.p);
    else if(S0.k==="summer")md=fresh?"#7f9e4a":"#43602e";
    else{const p=clamp(S0.p+j*.3,0,1);md=p<.3?bnMix("#4f6a30","#b07a2c",p/.3):p<.65?bnMix("#b07a2c","#a83e28",(p-.3)/.35):bnMix("#a83e28","#6e2620",(p-.65)/.35);}}
  if(j)md=bnMix(md,j>0?"#e8e0b0":"#0a0d08",Math.abs(j)*.22);return[bnMix(md,"#0a0d08",.6),md,bnMix(md,"#f2e2b0",.34)];}
const bnR=T=>T.sp==="matsu"?15:12;

// ── geometry: absolute angles, joints, pipe-model thickness (more tips above → thicker), older trees are thicker
function bnGeo(T,fl){const g=T.g,n=g.length,P=new Array(n),aF=1+Math.min(1.4,bnAge(T)/45),m=fl&&T.flip?-1:1;
  for(let i=0;i<n;i++){const s=g[i],p=s[0]>=0?P[s[0]]:null,A=(p?p.A:0)+s[1],x0=p?p.x1:0,y0=p?p.y1:0;P[i]={i,A,x0,y0,x1:x0+s[2]*Math.sin(A)*m,y1:y0-s[2]*Math.cos(A),kids:[],tips:0,dep:p?p.dep+1:0,s};if(p)p.kids.push(i);}
  for(let i=n-1;i>=0;i--){const q=P[i];if(!q.kids.length)q.tips=1;if(q.s[0]>=0)P[q.s[0]].tips+=q.tips;}
  for(let i=n-1;i>=0;i--){const q=P[i];q.w0=(1.5+2.1*Math.pow(q.tips,.6))*aF*(i===0?1.45:1);q.w1=q.kids.length?Math.max(...q.kids.map(k=>P[k].w0)):q.w0*.45;}
  return P;}
function bnBox(T,P){const pot=BN_POT[T.pot],R=bnR(T)*1.3;let a=-pot.w/2-8,b=-10,c=pot.w/2+8,d=pot.h+12;
  for(const q of P){const r=q.kids.length?q.w0:R;a=Math.min(a,q.x1-r);c=Math.max(c,q.x1+r);b=Math.min(b,q.y1-r);d=Math.max(d,q.y1+r);}return[a,b,c,d];}
function bnSub(P,i){const set=new Set([i]);for(let j=i+1;j<P.length;j++)if(set.has(P[j].s[0]))set.add(j);return set;}
// the trunk = the leader chain: the child that goes on straightest (a bigger branch wins a close call)
function bnTrunk(P){const out=[P[0]];let q=P[0];const sc=i=>Math.abs(P[i].s[1])-.12*Math.log(P[i].tips);while(q.kids.length){q=P[q.kids.reduce((a,b)=>sc(b)<sc(a)?b:a)];out.push(q);}return out;}
function bnStyle(T){const P=bnGeo(T,false);if(!P.length)return"chokkan";const tr=bnTrunk(P),ap=tr[tr.length-1],ax=ap.x1,H=Math.max(1,-ap.y1),L=Math.hypot(ax,ap.y1)||1;
  let low=-1e9;for(const p of P)low=Math.max(low,p.y1);if(low>14)return"kengai";
  const tips=P.filter(p=>!p.kids.length),inTr=new Set(tr.map(p=>p.i)),lowSide=tr.some(p=>p.y1>-.5*H&&p.kids.some(k=>!inTr.has(k)));
  if(!lowSide&&tips.length<=24&&tips.filter(p=>p.y1<-.55*H).length/tips.length>=.85&&H/P[0].w0>7)return"bunjin";
  if(Math.abs(Math.atan2(ax,H))>.3)return"shakan";
  let dev=0;for(const p of tr)dev=Math.max(dev,Math.abs(ax*p.y1-ap.y1*p.x1)/L);return dev/L>.035?"moyogi":"chokkan";}

// ── growth: a new shoot at a tip (higher tips are favoured) or a side bud on an older branch
function bnShoot(T,r,day){if(T.g.length>=170)return null;const P=bnGeo(T,false),tips=P.filter(q=>!q.kids.length&&q.dep>=1);if(!tips.length)return null;let par,a,l;
  if(r()<.72){const w=tips.map(q=>1+Math.max(0,-q.y1)/60),tot=w.reduce((x,y)=>x+y,0);let x=r()*tot,k=0;while(x>w[k]&&k<w.length-1){x-=w[k];k++;}
    par=tips[k];a=(r()-.5)*.8;l=clamp(par.s[2]*.82,9,24)*(.85+r()*.3);}
  else{const mids=P.filter(q=>q.kids.length===1&&q.dep>=1&&q.s[2]>10);if(!mids.length)return null;par=mids[Math.floor(r()*mids.length)];a=(r()<.5?-1:1)*(T.sp==="matsu"?.8+r()*.4:.55+r()*.5);l=10+r()*8;}
  const A=Math.atan2(Math.sin(par.A+a),Math.cos(par.A+a));if(Math.abs(A)>1.9)a=-a*.6;   // no growing into the soil
  T.g.push([par.i,+a.toFixed(3),+l.toFixed(1),day,T.n++,0]);return T.g.length-1;}
function bnGrow(){const T=bnS();if(!T)return 0;const dk=dayKey(),td=bnDN(dk),d0=T.last?bnDN(T.last):td;if(d0>=td){T.last=dk;return 0;}
  const r=rng(T.sd+td*131),b0=bnDN(T.born);let added=0;
  for(let d=Math.max(d0+1,td-10);d<=td;d++){const wet=T.wat&&bnDN(T.wat)===d-1,n=(r()<.5?1:2)+(wet?2:0);for(let i=0;i<n;i++)if(bnShoot(T,r,d-b0)!=null)added++;}
  T.last=dk;if(added){T.fresh=(T.fresh||0)+added;T.ft=added;T.fd=dk;}save();return added;}
function bnNew(sp,pot,sd){const r=rng(sd),T={sp,pot,born:dayKey(),sd,n:0,g:[],last:dayKey(),wat:null,tend:null,cutd:null,fresh:0,ft:0,fd:null,care:0,cuts:0,kod:null,named:[],flip:0};
  const add=(p,a,l)=>{T.g.push([p,+a.toFixed(3),+l.toFixed(1),0,T.n++,0]);return T.g.length-1;},sg=r()<.5?1:-1,pine=sp==="matsu";
  const t0=add(-1,sg*(.12+r()*.08),42),t1=add(t0,-sg*(.36+r()*.1),34),t2=add(t1,sg*(.42+r()*.1),28),t3=add(t2,-sg*.3,20),t4=add(t3,sg*.1,14);
  const br=(p,side,len,n)=>{let q=add(p,side*(pine?1.3:1.05)+(r()-.5)*.2,len),m=q;for(let i=1;i<n;i++){q=add(q,(pine?side*.12:-side*.22)+(r()-.5)*.3,len*.72);if(i===1)m=q;}
    add(q,.38,len*.45);add(q,-.38,len*.45);add(m,side*.6,len*.4);};
  br(t0,-sg,40,3);br(t1,sg,34,3);br(t2,-sg,26,2);br(t3,sg,18,2);add(t4,.32,10);add(t4,-.32,10);return T;}
function bnTend(){const T=bnS(),dk=dayKey();if(!T||T.tend===dk)return;T.tend=dk;T.care=(T.care||0)+1;if(T.care>=30)award("bn_30");S.needs.joy=clamp(S.needs.joy+4,0,100);}

// ── painting (tree units; the caller sets the transform). o.only = paint just these segments (a cut-off piece)
function bnQuad(g,x0,y0,x1,y1,w0,w1){const dx=x1-x0,dy=y1-y0,L=Math.hypot(dx,dy)||1,nx=-dy/L,ny=dx/L;
  g.moveTo(x0+nx*w0/2,y0+ny*w0/2);g.lineTo(x1+nx*w1/2,y1+ny*w1/2);g.lineTo(x1-nx*w1/2,y1-ny*w1/2);g.lineTo(x0-nx*w0/2,y0-ny*w0/2);g.closePath();
  g.moveTo(x1+w1/2,y1);g.arc(x1,y1,w1/2,0,Math.PI*2,true);}   // same winding as the quads, so one fill unites them
function bnPot(g,T,p,wet){const w=p.w,b=p.b,h=p.h,c=p.c,r=rng(T.sd+7),y0=3;
  g.fillStyle="rgba(0,0,0,.45)";g.beginPath();g.ellipse(0,y0+h+4,b*.62,6,0,0,Math.PI*2);g.fill();
  g.fillStyle=c[2];for(const s of [-1,1])g.fillRect(s*(b/2-20)-9,y0+h-2,18,7);
  g.beginPath();g.moveTo(-w/2,y0);g.lineTo(w/2,y0);
  if(p.sh==="rect"){g.lineTo(b/2,y0+h);g.lineTo(-b/2,y0+h);}
  else if(p.sh==="oval"){g.quadraticCurveTo(w/2,y0+h*.9,b/2-12,y0+h);g.lineTo(-b/2+12,y0+h);g.quadraticCurveTo(-w/2,y0+h*.9,-w/2,y0);}
  else{g.bezierCurveTo(w/2+14,y0+h*.45,b/2+12,y0+h,b/2,y0+h);g.lineTo(-b/2,y0+h);g.bezierCurveTo(-b/2-12,y0+h,-w/2-14,y0+h*.45,-w/2,y0);}
  g.closePath();let gr=g.createLinearGradient(-w/2,0,w/2,0);gr.addColorStop(0,c[0]);gr.addColorStop(.38,c[1]);gr.addColorStop(1,c[2]);g.fillStyle=gr;g.fill();
  gr=g.createLinearGradient(0,y0,0,y0+h);gr.addColorStop(0,"rgba(255,255,255,.06)");gr.addColorStop(1,"rgba(0,0,0,.4)");g.fillStyle=gr;g.fill();
  g.save();g.clip();
  if(p.gl){g.fillStyle="rgba(255,255,255,.2)";g.beginPath();g.ellipse(-w*.27,y0+h*.36,w*.06,h*.26,-.25,0,Math.PI*2);g.fill();g.fillStyle="rgba(255,255,255,.1)";g.beginPath();g.ellipse(-w*.17,y0+h*.3,w*.02,h*.2,-.25,0,Math.PI*2);g.fill();
    for(let i=0;i<10;i++){g.fillStyle=`rgba(0,0,0,${.07+r()*.1})`;g.beginPath();g.roundRect(-w/2+r()*w,y0+h*(.5+r()*.25),2+r()*3,h,2);g.fill();}}
  else{for(let i=0;i<70;i++){g.fillStyle=r()<.5?"rgba(0,0,0,.14)":"rgba(255,220,190,.08)";g.fillRect(-w/2+r()*w,y0+r()*h,1.6,1.6);}
    g.strokeStyle="rgba(0,0,0,.32)";g.lineWidth=1.2;g.strokeRect(-w*.16,y0+h*.3,w*.32,h*.42);}
  g.restore();
  g.fillStyle=wet?"#160f0a":"#2c2017";g.beginPath();g.ellipse(0,1,w/2-6,5.5,0,0,Math.PI*2);g.fill();
  const mc=wet?"#3a5426":"#46592e";g.fillStyle=bnMix(mc,"#0a0d08",.5);g.beginPath();g.ellipse(0,-.5,w/2-12,3.6,0,0,Math.PI*2);g.fill();
  for(const pass of [0,1,2]){g.fillStyle=pass===0?bnMix(mc,"#0a0d08",.45):pass===1?mc:bnMix(mc,"#e8e0a0",.32);g.beginPath();const r2=rng(T.sd+11);
    for(let i=0;i<46;i++){const x=(r2()*2-1)*(w/2-14),y=-.6-r2()*2.2,rr=1.8+r2()*2.6;if(pass===2&&r2()<.5)continue;const ox=pass===0?.6:pass===2?-.5:0,oy=pass===0?.9:pass===2?-.7:0,k=pass===2?.45:1;
      g.moveTo(x+ox+rr*k,y+oy);g.ellipse(x+ox,y+oy,rr*k,rr*k*.6,0,0,Math.PI*2);}g.fill();}}
function bnLip(g,p){const w=p.w;g.fillStyle=bnMix(p.c[1],"#000000",.1);g.beginPath();g.roundRect(-w/2-3,2,w+6,6,3);g.fill();g.fillStyle="rgba(255,255,255,.2)";g.fillRect(-w/2-1,2.2,w*.5,1.4);}
function bnPads(T,q){const r=rng(T.sd^Math.imul(q.s[4]+1,2654435761)),pine=T.sp==="matsu",R=bnR(T),out=[],sea=bnSea(),thin=T.sp==="momiji"&&sea.k==="autumn"&&sea.p>.8?1-(sea.p-.8)*3:1;
  const ctr=[[q.x1,q.y1,1]];if(q.s[2]>14)ctr.push([(q.x0+q.x1)/2,(q.y0+q.y1)/2,.7]);
  for(const [cx,cy,f] of ctr){const n=Math.round((pine?14:12)*f);for(let i=0;i<n;i++){const a=r()*Math.PI*2,d=Math.sqrt(r()),rb=((pine?3.2:3.4)+r()*2.6)*(f<1?.85:1),sp=[];if(r()>thin)continue;
    for(let k=0;k<4;k++){const b=r()*Math.PI*2;sp.push(Math.cos(b)*rb,Math.sin(b)*rb*.9,rb*(.3+r()*.15));}
    out.push([cx+Math.cos(a)*d*R*f*(pine?1.35:1.1),cy-R*f*(pine?.2:.15)+Math.sin(a)*d*R*f*(pine?.4:.6),rb,cx,cy-R*f*.2,R*f,sp]);}}return out;}
function bnPaint(g,T,P,o){const pot=BN_POT[T.pot],B=BN_BARK[T.sp],only=o.only,day=bnAge(T),L=only?P.filter(q=>only.has(q.i)):P;
  if(!only)bnPot(g,T,pot,T.wat===dayKey());
  // nebari: surface roots spreading over the moss
  if(!only&&P.length){const w=P[0].w0,r=rng(T.sd+3);g.beginPath();for(const s of [-1,1,-1,1]){const len=w*(1.1+r()*.9);bnQuad(g,0,-.5,s*len,1+r()*1.5,w*.5,.8);}g.fillStyle=B[0];g.fill();
    g.beginPath();for(const s of [-1,1])bnQuad(g,0,-1,s*w*1.4,.5,w*.38,.6);g.fillStyle=B[1];g.fill();}
  // wood: dark outline, bark, the edge lit from the upper left
  for(const pass of [0,1,2]){g.beginPath();
    for(const q of L){let {x0,y0,x1,y1,w0,w1}=q;
      if(pass===0){w0+=2.2;w1+=2.2;}
      if(pass===2){const dx=x1-x0,dy=y1-y0,Ln=Math.hypot(dx,dy)||1;let nx=-dy/Ln,ny=dx/Ln;if(nx+ny>0){nx=-nx;ny=-ny;}x0+=nx*w0*.24;y0+=ny*w0*.24;x1+=nx*w1*.24;y1+=ny*w1*.24;w0*=.34;w1*=.34;}
      bnQuad(g,x0,y0,x1,y1,w0,w1);if(q.i===0&&!only&&pass<2){const ry=-w0*.2,rr=w0*.42;g.moveTo(rr,ry);g.arc(0,ry,rr,0,Math.PI*2,true);}}
    g.fillStyle=B[pass];g.globalAlpha=pass===2?.45:1;g.fill();}
  g.beginPath();for(const q of L){let {x0,y0,x1,y1,w0,w1}=q;const dx=x1-x0,dy=y1-y0,Ln=Math.hypot(dx,dy)||1;let nx=-dy/Ln,ny=dx/Ln;if(nx+ny<0){nx=-nx;ny=-ny;}
    bnQuad(g,x0+nx*w0*.3,y0+ny*w0*.3,x1+nx*w1*.3,y1+ny*w1*.3,w0*.32,w1*.32);}g.fillStyle=B[0];g.globalAlpha=.4;g.fill();
  g.globalAlpha=1;
  // bark texture on thick wood, copper wire on fresh-wired branches
  g.lineCap="round";
  for(const q of L){const dx=q.x1-q.x0,dy=q.y1-q.y0,Ln=Math.hypot(dx,dy)||1,ux=dx/Ln,uy=dy/Ln,nx=-uy,ny=ux;
    if(q.w0>5.5){const r=rng(T.sd^(q.s[4]*977+5)),n=Math.floor(Ln/5);g.strokeStyle=T.sp==="matsu"?"rgba(14,8,5,.5)":"rgba(18,14,12,.4)";g.lineWidth=.8;g.beginPath();
      for(let i=0;i<n;i++){const u=r(),w=q.w0+(q.w1-q.w0)*u,o=(r()-.5)*w*.7,x=q.x0+dx*u+nx*o,y=q.y0+dy*u+ny*o,l=T.sp==="matsu"?2+r()*2:3+r()*4;g.moveTo(x,y);g.lineTo(x+ux*l+nx*(T.sp==="matsu"?l*.6:0),y+uy*l+ny*(T.sp==="matsu"?l*.6:0));}g.stroke();}
    const wr=q.s[5];if(wr&&day-(wr-1)<=21){g.lineWidth=1.3;g.strokeStyle="#a8622e";g.beginPath();
      for(let u=4;u<Ln-2;u+=4.5){const w=(q.w0+(q.w1-q.w0)*u/Ln)/2+.6,x=q.x0+ux*u,y=q.y0+uy*u;g.moveTo(x+nx*w-ux*1.6,y+ny*w-uy*1.6);g.lineTo(x-nx*w+ux*1.6,y-ny*w+uy*1.6);}g.stroke();
      g.strokeStyle="rgba(240,180,110,.55)";g.lineWidth=.5;g.stroke();}}
  if(!only)bnLip(g,pot);
  // foliage pads: all shadows, then bodies, then the lights (upper left) — the pads merge into soft clouds
  const tips=L.filter(q=>!q.kids.length&&q.dep>=1),fol=[];
  for(const q of tips){const pal=bnLeaf(T.sp,q.s[3]>0&&day-q.s[3]<=2,((q.s[4]*0.618)%1)-.5);
    if(!pal){g.strokeStyle=B[1];g.lineWidth=.7;g.beginPath();for(const da of [-.5,0,.5]){const l=6+Math.abs(da)*5,A=q.A+da,m=T.flip?-1:1;g.moveTo(q.x1,q.y1);g.lineTo(q.x1+Math.sin(A)*l*m,q.y1-Math.cos(A)*l);}g.stroke();continue;}
    for(const b of bnPads(T,q))fol.push([b,pal]);}
  for(const pass of [0,1,2]){const by=new Map();
    for(const [b,pal] of fol){if(pass===2&&(b[0]-b[3])+(b[1]-b[4])>b[5]*.15)continue;const c=pal[pass];if(!by.has(c))by.set(c,[]);by.get(c).push(b);}
    for(const [c,list] of by){g.fillStyle=c;g.globalAlpha=pass===2?.75:1;g.beginPath();
      for(const b of list){const x=pass===0?b[0]+1.4:pass===2?b[0]-1.1:b[0],y=pass===0?b[1]+2.4:pass===2?b[1]-1.4:b[1],rr=pass===0?b[2]*1.12:pass===2?b[2]*.5:b[2];g.moveTo(x+rr,y);g.arc(x,y,rr,0,Math.PI*2);
        if(pass<2)for(let k=0;k<b[6].length;k+=3){const sx=x+b[6][k]*(pass?1:1.1),sy=y+b[6][k+1]*(pass?1:1.1),sr=b[6][k+2];g.moveTo(sx+sr,sy);g.arc(sx,sy,sr,0,Math.PI*2);}}g.fill();}}
  g.fillStyle="rgba(8,6,4,.32)";g.beginPath();for(const [b] of fol){const x=b[0]+b[6][0]*.4,y=b[1]+b[6][1]*.4+.6;g.moveTo(x+.9,y);g.arc(x,y,.9,0,Math.PI*2);}g.fill();
  g.globalAlpha=1;}

// the veranda picture (and the hub thumbnail): fixed scale while it fits, so the tree visibly grows in the room
function bnSync(){const T=bnS();if(!T)return;const g=BN_CV.getContext("2d");g.setTransform(1,0,0,1,0,0);g.clearRect(0,0,460,540);const P=bnGeo(T,true),B=bnBox(T,P),
  k=Math.min(1.6,450/(2*Math.max(-B[0],B[2])),534/(B[3]-B[1]));g.setTransform(k,0,0,k,230,538-B[3]*k);bnPaint(g,T,P,{});
  for(const key of [...SPRC.keys()])if(key.startsWith("bn_tree|"))SPRC.delete(key);bnUrl=null;}
function bnPng(){if(!bnUrl)try{bnUrl=BN_CV.toDataURL("image/png");}catch(e){bnUrl="";}return bnUrl;}
function bnStatus(T){const dk=dayKey(),cut=T.cutd===dk;
  if(T.fresh>0&&!cut)return T.fd===dk&&T.ft===T.fresh?`Сегодня ${T.ft%10===1&&T.ft%100!==11?"вырос":"выросли"} ${bnWord(T.ft,["побег","побега","побегов"])} — пора подрезать`:`Новых побегов: ${T.fresh} — пора подрезать`;
  if(T.wat===dk)return cut?"Подстрижено и полито сегодня":"Полито сегодня";return cut?"Подстрижено сегодня, но ещё не полито":"Сегодня бонсай ещё не полит";}
function bnPlant(T){S.ext.bonsai=T;T.born=dayKey();T.last=dayKey();S.owned.add("bn_tree");
  if(!S.placed.bn_tree)S.placed.bn_tree={r:"engawa",x:BN_X,y:BN_Y};
  const D=S.decor.engawa;if(D&&D.plant==="d_bonsai")D.plant=null;   // the living tree takes the old bonsai's place
  bnSync();save();}

// ── the bench: a full-screen hidden game
function bnLay(G){const q=G.st,T=q.T,s=G.s,W=G.W,H=G.H,pick=q.mode==="pick",TB=(pick?158:68)*s,floor=H-TB-6*s,stand=floor-38*s,top=(pick?92:66)*s,
  P=bnGeo(T,true),B=bnBox(T,P),pot=BN_POT[T.pot],k=Math.min(1.5*s,(W-24*s)/(2*Math.max(-B[0],B[2])),(stand-top)/(B[3]-B[1])),sw=Math.min(W-30*s,Math.max(pot.b*k+70*s,W*.56));
  return{s,W,H,TB,floor,stand,top,k,cx:W/2,cy:stand-(pot.h+9)*k,sx:W/2-sw/2,sw,cat:{x:W-42*s,y:floor+4*s,sc:.42*s},kx:34*s,pick};}
function bnBtns(G){const L=G.st.L,s=L.s,W=L.W,H=L.H,gap=7*s;
  if(L.pick){const h=40*s,y3=H-h-10*s,y2=y3-h-8*s,y1=y2-h-8*s,row=(arr,y)=>{const n=arr.length,bw=(W-gap*(n+1))/n;return arr.map((a,i)=>({id:a[0],n:a[1],x:gap+i*(bw+gap),y,w:bw,h}));};
    return[...row([["sp:momiji","🍁 Клён"],["sp:matsu","🌲 Сосна"]],y1),...row(BN_POT.map((p,i)=>["pot:"+i,p.n]),y2),...row([["plant","Посадить дерево"]],y3)];}
  const n=5,h=L.TB-14*s,bw=(W-gap*(n+1))/n,y=H-h-8*s;
  return[["cut","✂️","Ножницы"],["wire","➰","Проволока"],["water","💧","Полить"],["turn","🔄","Повернуть"],["done","✅","Готово"]].map((a,i)=>({id:a[0],ic:a[1],n:a[2],x:gap+i*(bw+gap),y,w:bw,h}));}
function bnBtn(g,b,hot,dim,s){g.save();g.globalAlpha=dim?.45:1;g.fillStyle=hot?"rgba(216,210,195,.95)":"rgba(16,21,19,.88)";g.strokeStyle="rgba(216,210,195,.35)";g.beginPath();g.roundRect(b.x,b.y,b.w,b.h,12);g.fill();g.stroke();
  if(b.ic){drawEmoji(g,b.ic,b.x+b.w/2,b.y+b.h*.37,19*s);textC(g,b.n,b.x+b.w/2,b.y+b.h*.77,11*s,hot?"#0d1210":"#d8d2c3",600);}
  else textC(g,b.n,b.x+b.w/2,b.y+b.h/2,Math.min(15*s,b.h*.38),hot?"#0d1210":"#d8d2c3",600);g.restore();}
function bnBg(G){const q=G.st,L=q.L,s=L.s,W=L.W,H=L.H,d=Math.min(2,devicePixelRatio||1),c=document.createElement("canvas");c.width=W*d;c.height=H*d;const g=c.getContext("2d");g.setTransform(d,0,0,d,0,0);
  const r=rng(41),night=dayTint()[1],fy=L.stand-50*s;
  let gr=g.createLinearGradient(0,0,0,fy);gr.addColorStop(0,"#191512");gr.addColorStop(1,"#0f0c0a");g.fillStyle=gr;g.fillRect(0,0,W,fy);
  shoji(g,W*.04,H*.07,W*.44,fy-H*.1,s,night?.12:.3);
  // a round window with the sky and the moon
  const mx=W*.76,my=H*.2,mr=Math.min(W*.19,120*s);g.save();g.beginPath();g.arc(mx,my,mr,0,Math.PI*2);g.clip();gr=g.createLinearGradient(0,my-mr,0,my+mr);
  gr.addColorStop(0,night?"#16233a":"#8fa6b8");gr.addColorStop(1,night?"#28334a":"#c9cdbf");g.fillStyle=gr;g.fillRect(mx-mr,my-mr,mr*2,mr*2);
  if(night){g.fillStyle="#efe6c8";g.beginPath();g.arc(mx+mr*.35,my-mr*.3,mr*.2,0,Math.PI*2);g.fill();const mg=g.createRadialGradient(mx+mr*.35,my-mr*.3,0,mx+mr*.35,my-mr*.3,mr*.9);mg.addColorStop(0,"rgba(240,230,200,.25)");mg.addColorStop(1,"rgba(240,230,200,0)");g.fillStyle=mg;g.fillRect(mx-mr,my-mr,mr*2,mr*2);}
  g.strokeStyle="#0c0a08";g.lineCap="round";g.lineWidth=5*s;g.beginPath();g.moveTo(mx-mr,my+mr*.5);g.quadraticCurveTo(mx-mr*.2,my+mr*.2,mx+mr*.3,my+mr*.35);g.stroke();g.lineWidth=2*s;
  for(let i=0;i<5;i++){const x=mx-mr*.8+i*mr*.3;g.beginPath();g.moveTo(x,my+mr*.42);g.lineTo(x+mr*.15,my+mr*.15-r()*mr*.2);g.stroke();}g.restore();
  g.strokeStyle="#3a2a1c";g.lineWidth=7*s;g.beginPath();g.arc(mx,my,mr+3*s,0,Math.PI*2);g.stroke();g.strokeStyle="rgba(210,170,120,.25)";g.lineWidth=1.2*s;g.beginPath();g.arc(mx,my,mr+6*s,Math.PI*.9,Math.PI*1.6);g.stroke();
  // a beam, then the floor planks
  g.fillStyle="#24190f";g.fillRect(0,fy-8*s,W,8*s);
  for(let y=fy,j=0;y<H;y+=26*s,j++){g.fillStyle=`rgb(${38+r()*10|0},${28+r()*7|0},${20+r()*5|0})`;g.fillRect(0,y,W,26*s-1.5);for(let i=0;i<14;i++){g.fillStyle=`rgba(${r()<.5?0:90},${r()<.5?0:70},${r()<.5?0:50},.12)`;g.fillRect(r()*W,y+r()*26*s,40+r()*140,1);}
    g.fillStyle="rgba(0,0,0,.5)";g.fillRect(0,y+26*s-1.5,W,1.5);}
  gr=g.createLinearGradient(0,fy,0,H);gr.addColorStop(0,"rgba(0,0,0,.35)");gr.addColorStop(1,"rgba(0,0,0,0)");g.fillStyle=gr;g.fillRect(0,fy,W,60*s);
  // the stand: a low wooden table
  const x0=L.sx,w=L.sw,ty=L.stand;g.fillStyle="rgba(0,0,0,.5)";g.beginPath();g.ellipse(W/2,L.floor+2*s,w*.55,9*s,0,0,Math.PI*2);g.fill();
  for(const lx of [x0+14*s,x0+w-34*s]){gr=g.createLinearGradient(lx,0,lx+20*s,0);gr.addColorStop(0,"#6a4a30");gr.addColorStop(1,"#2e1e12");g.fillStyle=gr;g.fillRect(lx,ty+12*s,20*s,L.floor-ty-12*s);}
  gr=g.createLinearGradient(0,ty,0,ty+16*s);gr.addColorStop(0,"#9a7050");gr.addColorStop(.25,"#74523a");gr.addColorStop(1,"#3a2616");g.fillStyle=gr;g.beginPath();g.roundRect(x0,ty,w,16*s,3*s);g.fill();
  g.fillStyle="rgba(240,200,150,.28)";g.fillRect(x0+4*s,ty+1,w*.6,1.5);for(let i=0;i<8;i++){g.fillStyle=`rgba(20,12,6,${.15+r()*.2})`;g.fillRect(x0+r()*w,ty+3*s+r()*9*s,30+r()*60,1);}
  // the andon's warm light from the upper left
  gr=g.createRadialGradient(W*.05,H*.38,0,W*.05,H*.38,Math.max(W,H)*.75);gr.addColorStop(0,night?"rgba(255,190,110,.16)":"rgba(255,230,190,.1)");gr.addColorStop(1,"rgba(255,190,110,0)");g.fillStyle=gr;g.fillRect(0,0,W,H);
  const vg=g.createRadialGradient(W/2,H*.45,Math.min(W,H)*.3,W/2,H/2,Math.max(W,H)*.8);vg.addColorStop(0,"rgba(0,0,0,0)");vg.addColorStop(1,"rgba(0,0,0,.5)");g.fillStyle=vg;g.fillRect(0,0,W,H);
  g.fillStyle="rgba(8,10,9,.82)";g.fillRect(0,H-L.TB-2*s,W,L.TB+2*s);return c;}
function bnBake(G){const q=G.st,L=q.L,d=Math.min(2,devicePixelRatio||1),W=Math.round(G.W*d),H=Math.round(G.H*d);if(!q.tc){q.tc=document.createElement("canvas");}
  if(q.tc.width!==W||q.tc.height!==H){q.tc.width=W;q.tc.height=H;}const g=q.tc.getContext("2d");g.setTransform(1,0,0,1,0,0);g.clearRect(0,0,W,H);
  q.P=bnGeo(q.T,true);g.setTransform(d*L.k,0,0,d*L.k,d*L.cx,d*L.cy);bnPaint(g,q.T,q.P,{});q.dirty=0;}
function bnBuild(G){const q=G.st;q.L=bnLay(G);q.bg=bnBg(G);q.lw=G.W;q.lh=G.H;bnBake(G);}
const bnSc=(L,x,y)=>[L.cx+x*L.k,L.cy+y*L.k];
function bnNear(G,x,y){const q=G.st,L=q.L,P=q.P,R=bnR(q.T)*L.k;let best=-1,bd=1e9;
  for(const p of P){const [ax,ay]=bnSc(L,p.x0,p.y0),[bx,by]=bnSc(L,p.x1,p.y1),dx=bx-ax,dy=by-ay,l2=dx*dx+dy*dy||1,u=clamp(((x-ax)*dx+(y-ay)*dy)/l2,0,1);
    let dd=Math.hypot(x-ax-u*dx,y-ay-u*dy)-p.w0*L.k/2;if(!p.kids.length&&p.dep>=1)dd=Math.min(dd,Math.hypot(x-bx,y-by+R*.2)-R*.9);if(dd<bd){bd=dd;best=p.i;}}
  return bd<16*L.s?best:-1;}
function bnSnip(){tone(2600,.03,"square",.03);setTimeout(()=>{tone(1900,.05,"triangle",.05);tone(5200,.02,"square",.012);},45);}
function bnRattle(){[0,110,220].forEach(d=>setTimeout(()=>tone(rand(650,900),.05,"triangle",.035),d));}
function bnSay(q,tx,t,who){q.say={tx,t0:t,who:who||""};}
function bnPiece(G,set,i,t){const q=G.st,L=q.L,P=q.P,R=bnR(q.T)*1.5,d=Math.min(2,devicePixelRatio||1);let a=1e9,b=1e9,c=-1e9,e=-1e9;
  for(const j of set){const p=P[j];for(const [x,y] of [[p.x0,p.y0],[p.x1,p.y1]]){a=Math.min(a,x-R);b=Math.min(b,y-R);c=Math.max(c,x+R);e=Math.max(e,y+R);}}
  const cv=document.createElement("canvas"),w=(c-a)*L.k,h=(e-b)*L.k;cv.width=Math.max(2,Math.ceil(w*d));cv.height=Math.max(2,Math.ceil(h*d));const g=cv.getContext("2d");
  g.setTransform(d*L.k,0,0,d*L.k,-a*L.k*d,-b*L.k*d);bnPaint(g,q.T,P,{only:set});const [px,py]=bnSc(L,P[i].x0,P[i].y0),[x,y]=bnSc(L,a,b);
  return{cv,x,y,w,h,px,py,vx:rand(-40,40)*L.s,vy:-60*L.s,vr:rand(-2.5,2.5),t0:t,dx:0,dy:0,rot:0};}
function bnCut(G,i,t){const q=G.st,T=q.T;if(i<=0){bnSay(q,"Ствол не режут — только ветки",t);tone(220,.12,"triangle",.04);return;}
  const set=bnSub(q.P,i);q.fall.push(bnPiece(G,set,i,t));const [lx,ly]=bnSc(q.L,q.P[i].x0,q.P[i].y0);q.look={x:lx,y:ly,t};
  const keep=[],map={};T.g.forEach((s,j)=>{if(set.has(j))return;map[j]=keep.length;keep.push(s);});for(const s of keep)if(s[0]>=0)s[0]=map[s[0]];T.g=keep;
  T.cuts=(T.cuts||0)+1;T.cutd=dayKey();T.fresh=0;q.cuts++;G.score++;bnTend();award("bn_cut");bnSnip();q.dirty=1;q.last=t;
  if(Math.random()<.5)q.bub={e:pick(["😼","😮","😺"]),t};save();bnSync();}
function bnWater(G,t){const q=G.st,T=q.T;if(T.wat===dayKey()){bnSay(q,"Сегодня уже полито — земля ещё влажная",t);return;}
  T.wat=dayKey();q.wa=t;q.waDone=0;G.score++;bnTend();save();setTimeout(()=>sfx("splash"),500);setTimeout(()=>sfx("splash"),1200);q.bub={e:"😺",t:t+.6};}
function bnDone(G){const q=G.st,T=q.T,st=bnStyle(T),dk=dayKey();q.style=st;q.newSty=disc("bonsai",st);q.kodSaid=null;
  if(q.kod&&T.kod!==dk){T.kod=dk;T.named=T.named||[];if(!T.named.includes(st))T.named.push(st);award("bn_named");q.kodSaid=BN_KOD[st];}
  else if(q.kod)q.kodSaid=BN_KOD[st];
  chime([1318,1568,2093]);gEnd();S.needs.joy=clamp(S.needs.joy+4,0,100);save();bnSync();}
function bnTool(G,b,t){const q=G.st;tone(1100,.04,"triangle",.05);
  if(b.id==="cut"||b.id==="wire"){q.tool=b.id;bnSay(q,b.id==="cut"?"Нажми на ветку — ножницы срежут её":"Тяни ветку пальцем — проволока согнёт её",t);}
  else if(b.id==="water")bnWater(G,t);else if(b.id==="turn"){if(!q.rot)q.rot={t0:t,sw:0};}else if(b.id==="done")bnDone(G);
  else if(b.id.startsWith("sp:")||b.id.startsWith("pot:")){if(b.id.startsWith("sp:"))q.sp=b.id.slice(3);else q.pot=+b.id.slice(4);q.T=bnNew(q.sp,q.pot,q.sd);bnBuild(G);}
  else if(b.id==="plant"){bnPlant(q.T);q.T=bnS();q.mode="play";bnBuild(G);chime([988,1318,1568]);bnSay(q,"Дерево посажено. Новые побеги появятся завтра",t);q.bub={e:"😻",t};}}
const BN_GAME={id:"bn_bench",hidden:true,n:"Бонсай",tag:"盆栽 · Бонсай",bg:"room",lives:null,time:null,icon:"🌳",lore:"",how:"",
 init(G,t){const T=bnS();bnGrow();const sd=(Math.random()*1e9)|0;
   Object.assign(G.st,{mode:T?"play":"pick",sp:"momiji",pot:0,sd,T:T||bnNew("momiji",0,sd),tool:"cut",fall:[],lv:[],spk:[],cuts:0,wires:0,sel:null,wire:null,say:null,bub:null,
     last:t,sleep:0,groom:0,nextGroom:t+rand(9,15),kod:T&&bnSun()?{t0:t+1.4,said:0}:null,rot:null,wa:0,look:null});
   G.score=0;bnBuild(G);if(T)bnSay(G.st,T.fresh>0&&T.cutd!==dayKey()?bnStatus(T):"Нажми на ветку — ножницы срежут её",t);},
 step(G,t,dt){const q=G.st,T=q.T,L=q.L;if(q.lw!==G.W||q.lh!==G.H)bnBuild(G);
   if(q.dirty)bnBake(G);
   if(q.kod&&!q.kod.said&&t>q.kod.t0+.8){q.kod.said=1;bnRattle();bnSay(q,T.kod===dayKey()?"Я ещё посижу тут. Хорошее дерево.":pick(BN_HI),t,"Кодама");q.bub={e:"😳",t};}
   if(q.wa&&!q.waDone&&t-q.wa>1.4){q.waDone=1;const i=bnShoot(T,rng((Math.random()*1e9)|0),bnAge(T));
     if(i!=null){const dk=dayKey();T.fresh=(T.fresh||0)+1;if(T.fd===dk)T.ft=(T.ft||0)+1;else{T.ft=1;T.fd=dk;}bnBake(G);const p=q.P[i],[x,y]=bnSc(L,p.x1,p.y1);q.spk.push({x,y,t});bnSay(q,"Полито — сразу проклюнулся новый побег",t);}
     else bnSay(q,"Полито. Завтра побегов будет больше",t);q.dirty=1;save();bnSync();}
   if(q.rot&&!q.rot.sw&&t-q.rot.t0>.25){q.rot.sw=1;T.flip=T.flip?0:1;bnBuild(G);save();bnSync();}
   if(q.rot&&t-q.rot.t0>.5)q.rot=null;
   for(const f of q.fall){f.vy+=900*L.s*dt;f.dy+=f.vy*dt;f.dx+=f.vx*dt;f.rot+=f.vr*dt;}q.fall=q.fall.filter(f=>t-f.t0<1.7);
   // autumn maple: a leaf drifts down now and then
   if(T.sp==="momiji"&&bnSea().k==="autumn"&&q.mode==="play"&&Math.random()<dt*.5&&q.P.length){const tp=q.P.filter(p=>!p.kids.length);const p=tp[Math.floor(Math.random()*tp.length)];if(p){const [x,y]=bnSc(L,p.x1,p.y1);q.lv.push({x,y,vx:rand(-10,20)*L.s,vy:rand(20,34)*L.s,r:rand(0,6),vr:rand(-2,2),c:bnLeaf("momiji",0)[1],life:5});}}
   for(const l of q.lv){l.x+=(l.vx+Math.sin(l.life*2.3)*12*L.s)*dt;l.y+=l.vy*dt;l.r+=l.vr*dt;l.life-=dt;if(l.y>L.stand)l.vy=0,l.vx=0;}q.lv=q.lv.filter(l=>l.life>0);
   // Musya: watches, grooms now and then, naps after a quiet spell
   if(!q.sleep&&t-q.last>24)q.sleep=t;if(!q.sleep&&t>q.nextGroom){q.groom=t+3;q.nextGroom=t+rand(14,24);}},
 draw(G,g,t){const q=G.st,T=q.T,L=q.L;if(!L)return;const s=L.s;g.drawImage(q.bg,0,0,G.W,G.H);
   // Sunday: the old kodama by the stand
   if(q.kod){const im=MIMG.m_rg_kodama,e=t-q.kod.t0;if(e>0){const a=clamp(e/1.2,0,1),h=112*s,x=L.kx,y=L.floor+6*s;
     const gl=g.createRadialGradient(x,y-h*.6,0,x,y-h*.6,h*.8);gl.addColorStop(0,`rgba(190,230,190,${.14*a})`);gl.addColorStop(1,"rgba(190,230,190,0)");g.fillStyle=gl;g.fillRect(x-h,y-h*1.4,h*2,h*1.6);
     if(im){const w=h*im.width/im.height;g.save();g.globalAlpha=a*.95;g.translate(x,y);g.rotate(e<4?Math.sin(t*14)*.025*clamp(4-e,0,1):0);g.drawImage(im,-w/2,-h,w,h);g.restore();}}}
   // the tree (turning: squeeze it to the middle and open it mirrored)
   const ro=q.rot?Math.abs(Math.cos(clamp((t-q.rot.t0)/.5,0,1)*Math.PI)):1;g.save();if(ro<1){g.translate(L.cx,0);g.scale(Math.max(.02,ro),1);g.translate(-L.cx,0);}g.drawImage(q.tc,0,0,G.W,G.H);g.restore();
   // the soil darkens when watered; the can pours
   if(q.wa){const e=t-q.wa;if(e<2.4){const [px,py]=bnSc(L,BN_POT[T.pot].w*.22,-30),u=smooth(clamp(e/.4,0,1))*(1-smooth(clamp((e-2)/.4,0,1)));g.save();g.globalAlpha=u;g.translate(px+40*s,py-40*s);g.rotate(-.5*u);fDraw(g,"g_can",0,0,64*s);g.restore();
     if(e>.4&&e<2)for(let i=0;i<10;i++){const dd=(e*2.2+i/10)%1,dx=px+12*s+Math.sin(i*2.3)*10*s,dy=py-30*s+dd*44*s;g.fillStyle=`rgba(170,205,225,${.85*(1-dd)})`;g.beginPath();g.ellipse(dx,dy,2*s,4.5*s,0,0,Math.PI*2);g.fill();}}}
   // selection under the scissors / the branch being wired
   const hl=q.sel?q.sel.set:q.wire&&q.wire.mv?new Set([q.wire.i]):null;
   if(hl){g.save();g.lineCap="round";g.strokeStyle=q.sel?`rgba(238,163,187,${.55+.25*Math.sin(t*10)})`:"rgba(232,170,96,.7)";for(const i of hl){const p=q.P[i];if(!p)continue;const [ax,ay]=bnSc(L,p.x0,p.y0),[bx,by]=bnSc(L,p.x1,p.y1);g.lineWidth=Math.max(3,p.w0*L.k*.5);g.beginPath();g.moveTo(ax,ay);g.lineTo(bx,by);g.stroke();}g.restore();}
   for(const f of q.fall){g.save();g.globalAlpha=clamp((1.7-(t-f.t0))/.5,0,1);g.translate(f.px+f.dx,f.py+f.dy);g.rotate(f.rot);g.drawImage(f.cv,f.x-f.px,f.y-f.py,f.w,f.h);g.restore();}
   for(const l of q.lv){g.save();g.translate(l.x,l.y);g.rotate(l.r);g.globalAlpha=Math.min(1,l.life);g.fillStyle=l.c;g.beginPath();g.ellipse(0,0,3.6*s,2*s,0,0,Math.PI*2);g.fill();g.restore();}
   for(const p of q.spk){const e=t-p.t;if(e<1.6)drawEmoji(g,"✨",p.x,p.y-e*14*s,18*s,clamp(Math.min(e*5,(1.6-e)*2),0,1));}
   // Musya on the floor beside the stand
   if(!petAway()){const M=L.cat;let st="rest",fi=Math.floor(t*2)%2,tg=null;
     if(q.wire&&q.wire.p)tg=q.wire.p;else if(q.look&&t-q.look.t<1.8)tg=[q.look.x,q.look.y];else if(q.wa&&t-q.wa<2.2)tg=bnSc(L,0,0);
     if(q.sleep&&!tg){st="sleep";fi=Math.floor(t*1.2)%8;}
     else if(tg){const gi=gazeIndex(tg[0]-M.x,(M.y-150*M.sc)-tg[1]);st=gi<8?"gaze9":"gaze10";fi=gi%8;}
     else if(q.groom>t){st="groom";fi=Math.floor(t*8)%8;}
     drawCatG(g,st,fi,M.x,M.y,M.sc);
     if(st==="sleep"&&Math.floor(t/3)%2===0)drawEmoji(g,"💤",M.x+30*M.sc,M.y-170*M.sc-(t%3)*6*s,16*s,.8);
     if(q.bub){const e=t-q.bub.t;if(e>=0&&e<2.2)drawEmoji(g,q.bub.e,M.x+40*M.sc,M.y-205*M.sc-e*8*s,22*s,clamp(Math.min(e*4,(2.2-e)*2),0,1));else if(e>=2.2)q.bub=null;}}
   // top lines: status and the current hint / what the kodama says
   if(q.mode==="play"){const st=bnStyle(T),a=bnAge(T);g.save();g.font=`600 ${12*s}px ${getComputedStyle(document.body).fontFamily}`;g.fillStyle="rgba(216,210,195,.75)";g.textBaseline="middle";
     g.fillText(`${BN_SP[T.sp].n} · ${a?bnWord(a,["день","дня","дней"]):"посажен сегодня"} · стиль ${BN_STY[st][0].toLowerCase()}`,12*s,16*s);g.restore();}
   else{textC(g,BN_SP[q.sp].d,G.W/2,58*s,11.5*s,"rgba(216,210,195,.8)",500);}
   const say=q.say&&t-q.say.t0<(q.say.who?8:4.5)?q.say:null,hint=say?(say.who?`${say.who}: «${say.tx}»`:say.tx):q.mode==="pick"?"Выбери дерево и горшок":"";
   if(hint){g.save();const fs=12.5*s;g.font=`600 ${fs}px ${getComputedStyle(document.body).fontFamily}`;const words=hint.split(" "),lines=[];let ln="";
     for(const w of words){const tt=ln?ln+" "+w:w;if(g.measureText(tt).width>G.W-56*s&&ln){lines.push(ln);ln=w;}else ln=tt;}lines.push(ln);
     const tw=Math.max(...lines.map(l=>g.measureText(l).width))+26*s,hh=lines.length*fs*1.35+12*s,hy=(q.mode==="pick"?22:30)*s,al=say?clamp(Math.min((t-say.t0)*4,((say.who?8:4.5)-(t-say.t0))*2),0,1):1;
     g.globalAlpha=al;g.fillStyle=say&&say.who?"rgba(16,30,20,.8)":"rgba(10,12,14,.66)";g.beginPath();g.roundRect(G.W/2-tw/2,hy,tw,hh,13*s);g.fill();g.restore();
     lines.forEach((l,i)=>textC(g,l,G.W/2,hy+6*s+fs*.68+i*fs*1.35,fs,say&&say.who?`rgba(214,236,208,${al})`:`rgba(232,226,212,${al})`,600));}
   const dk=dayKey();for(const b of bnBtns(G))bnBtn(g,b,b.id===q.tool||b.id==="sp:"+q.sp||b.id==="pot:"+q.pot||b.id==="plant",b.id==="water"&&T.wat===dk&&q.mode==="play",s);},
 down(G,x,y,t){const q=G.st,L=q.L;if(!L)return;q.last=t;
   const b=bnBtns(G).find(b=>x>=b.x&&x<=b.x+b.w&&y>=b.y&&y<=b.y+b.h);if(b){bnTool(G,b,t);return;}
   const M=L.cat;if(!petAway()&&Math.abs(x-M.x)<70*M.sc&&y<M.y&&y>M.y-190*M.sc){q.bub={e:q.sleep?"😪":pick(["😽","😺","💕"]),t};q.sleep=0;tone(220,.3,"sine",.03);return;}
   if(q.mode!=="play"||q.rot)return;q.sleep=0;
   const i=bnNear(G,x,y);
   if(i<0){const pot=BN_POT[q.T.pot],[px,py]=bnSc(L,0,0);if(Math.abs(x-px)<pot.w/2*L.k&&y>py&&y<py+(pot.h+8)*L.k){q.T.pot=(q.T.pot+1)%3;q.dirty=1;tone(520,.08,"triangle",.05);bnSay(q,`Горшок: ${BN_POT[q.T.pot].n}`,t);save();bnSync();}return;}
   if(q.tool==="cut"){q.sel={i,set:bnSub(q.P,i),x,y};return;}
   const p=q.P[i],[px,py]=bnSc(L,p.x0,p.y0);q.wire={i,a0:q.T.g[i][1],px,py,th0:Math.atan2(y-py,x-px),mv:0,p:[x,y]};tone(140,.12,"sawtooth",.02);},
 move(G,x,y,held){const q=G.st;if(!held)return;
   if(q.sel&&Math.hypot(x-q.sel.x,y-q.sel.y)>36*G.s)q.sel=null;
   if(q.wire){const w=q.wire;if(Math.hypot(x-w.px,y-w.py)<8*G.s)return;let d=Math.atan2(y-w.py,x-w.px)-w.th0;d=Math.atan2(Math.sin(d),Math.cos(d));if(q.T.flip)d=-d;
     const lim=w.i===0?1.2:2.6;q.T.g[w.i][1]=+clamp(w.a0+clamp(d,-.55,.55),-lim,lim).toFixed(3);w.mv=1;w.p=[x,y];q.dirty=1;}},
 up(G){const q=G.st,t=now();
   if(q.sel){const i=q.sel.i;q.sel=null;bnCut(G,i,t);return;}
   if(q.wire){const w=q.wire;q.wire=null;if(!w.mv)return;const T=q.T;T.g[w.i][5]=bnAge(T)+1;q.wires++;G.score++;bnTend();tone(260,.08,"triangle",.04);q.dirty=1;save();bnSync();}},
 stat:G=>{const q=G.st;return q.mode==="play"?`🌳 ${BN_STY[bnStyle(q.T)][0]}`:"🌱 новое дерево";},
 card(G){const q=G.st,T=q.T,st=q.style||bnStyle(T),S0=BN_STY[st],dk=dayKey(),acts=[q.cuts?`срезано веток: ${q.cuts}`:"",q.wires?`согнуто проволокой: ${q.wires}`:"",T.wat===dk?"полито ✓":"ещё не полито"].filter(Boolean).join(" · ");
   return`<div class="card"><p class="tag">盆栽 · Бонсай</p><h3>Стиль: ${S0[0].toLowerCase()} <span style="opacity:.6">${S0[1]}</span></h3><p class="lore">${S0[2][0].toUpperCase()+S0[2].slice(1)}.</p>
   ${q.kodSaid?`<p class="lore">Кодама: «${q.kodSaid}»</p>`:`<p>${bnSun()?"Кодама сегодня у дерева.":`Кодама придёт полюбоваться в воскресенье — через ${bnWord((7-today().getDay())%7,["день","дня","дней"])}.`}</p>`}
   ${q.newSty?`<p><b>Новый стиль в коллекции!</b></p>`:""}<p>${acts[0].toUpperCase()+acts.slice(1)}. Дереву ${bnWord(bnAge(T),["день","дня","дней"])}, дней заботы: ${T.care||0}.</p>
   <div class="row"><button class="btn" id="gHome">Домой</button><button class="btn primary" id="gAgain">К дереву</button></div></div>`;},
 after(){ui();}};
GAMES.push(BN_GAME);
function bnOpen(){if(G.id)return;closePanel();audioInit();bnGrow();openPlace("bn_bench");}

// ── the house: tray button on the veranda, the tree itself (a placed thing), the 家 card, album, postcard
hook("tray",(tray,room)=>{if(room!=="engawa"||(S.trayMode[room]||"play")!=="play")return;const el=tray.querySelector(".items");if(!el)return;const T=bnS(),dk=dayKey();
  const h=`<button class="item wide" data-x="bn:open"><span class="ico">🌳</span><span class="nm">${!T?"Посадить бонсай":T.fresh>0&&T.cutd!==dk?"Бонсай: новые побеги":"Бонсай"}</span></button>`,tv=[...el.querySelectorAll('[data-x^="tv:"]')].pop();
  if(tv)tv.insertAdjacentHTML("afterend",h);else el.insertAdjacentHTML("afterbegin",h);});
hook("click",k=>{if(!k.startsWith("bn:"))return;if(k==="bn:open")bnOpen();else if(k==="bn:go"){closePanel();goRoom("engawa");}return true;});
hook("itemTap",it=>{if(it.id!=="bn_tree")return;if(!petAway())react("😺",1.4);bnOpen();return true;});
hook("hubDot",()=>{const T=bnS();if(!T)return false;const dk=dayKey();return T.fresh>0&&T.tend!==dk||bnSun()&&T.kod!==dk;});
document.head.insertAdjacentHTML("beforeend","<style>.bn-row{display:flex;gap:12px;align-items:flex-end}.bn-row>img{width:84px;height:101px;flex:none;object-fit:contain}.bn-row>div{flex:1;min-width:0}</style>");
hook("hub",()=>{const T=bnS(),dk=dayKey();
  if(!T)return`<div class="hubc"><h4>🌳 Бонсай <i>盆栽</i></h4><p>На веранде ждёт пустой горшок — посади своё дерево</p><p>Клён или сосна в глазурованном горшке. Дерево растёт каждый день: подрезай побеги ножницами, гни ветви проволокой, поливай. По воскресеньям полюбоваться им приходит старый кодама.</p><div class="row"><button class="btn primary" data-x="bn:open">Посадить</button></div></div>`;
  const st=bnStyle(T),a=bnAge(T),nx=(7-today().getDay())%7;
  return`<div class="hubc"><h4>🌳 Бонсай <i>盆栽</i></h4><p>${bnStatus(T)}</p><div class="bn-row"><img src="${bnPng()}" alt=""><div><p>${BN_SP[T.sp].n} · ${a?bnWord(a,["день","дня","дней"]):"посажен сегодня"} · дней заботы: ${T.care||0}</p>
    <p>Стиль: <b>${BN_STY[st][0]}</b> ${BN_STY[st][1]} — ${BN_STY[st][2]}</p><p>${bnSun()?(T.kod===dk?"Кодама сегодня уже полюбовался деревом":"Сегодня воскресенье — у дерева ждёт кодама"):`Кодама приходит по воскресеньям — через ${bnWord(nx,["день","дня","дней"])}`}</p></div></div>
    <div class="row"><button class="btn primary" data-x="bn:open">К дереву</button><button class="btn" data-x="bn:go">На веранду</button></div></div>`;});
hook("album",el=>{const T=bnS();if(!T)return;const D=(S.ext.disc||{}).bonsai||{},ks=Object.keys(BN_STY);
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Бонсай</h3><p class="lead">Стилей: ${ks.filter(k=>D[k]).length} из ${ks.length}. Дереву ${bnWord(bnAge(T),["день","дня","дней"])}, срезано веток: ${T.cuts||0}.</p><div class="coll">${ks.map(k=>`<div class="ci${D[k]?" on":""}"${D[k]?"":' style="opacity:.45"'}><span style="font-size:17px;line-height:52px">${D[k]?BN_STY[k][1]:"？"}</span><span style="font-size:11px">${D[k]?BN_STY[k][0]:"???"}</span></div>`).join("")}</div>`);});
hook("away",ms=>{const T=bnS();if(!T||ms<6*3600e3)return;bnGrow();if(T.fresh>=2&&T.cutd!==dayKey())return{i:"🌳",t:"У бонсая на веранде выросли новые побеги"};});
hook("sec",()=>{const T=bnS();if(T&&T.last!==dayKey()){bnGrow();bnSync();}});
hook("boot",()=>{if(bnS()){bnGrow();bnSync();}});
try{bnSync();}catch(e){}
X.bn={open:bnOpen,st:bnS,style:()=>bnS()&&bnStyle(bnS()),png:bnPng,thumb(){const c=document.createElement("canvas");c.width=230;c.height=270;c.getContext("2d").drawImage(BN_CV,0,0,230,270);return c.toDataURL("image/webp",.88);},sync:bnSync,grow:bnGrow,status:()=>bnS()&&bnStatus(bnS()),
  plant(sp="momiji",pot=0){bnPlant(bnNew(sp,pot,12345));},
  // tests: age the tree by n days (growing as if watered every other day)
  age(n){const T=bnS();if(!T)return;const r=rng(99),b=bnDN(T.born)-n;T.born=bnKey(b);for(let d=1;d<=n;d++){const k=(r()<.5?1:2)+(d%2?2:0);for(let i=0;i<k;i++)bnShoot(T,r,d);}T.last=dayKey();T.care=Math.floor(n*.6);bnSync();save();},
  btn(id){const b=bnBtns(G).find(b=>b.id===id);if(b)G.def.down(G,b.x+b.w/2,b.y+b.h/2,now());},
  tapSeg(i){const q=G.st,p=q.P[i],[x,y]=bnSc(q.L,(p.x0+p.x1)/2,(p.y0+p.y1)/2);G.held=true;G.def.down(G,x,y,now());G.held=false;G.def.up(G);return[x,y];},
  bend(i,da){const q=G.st,p=q.P[i],[px,py]=bnSc(q.L,p.x0,p.y0),[x,y]=bnSc(q.L,p.x1,p.y1),r=Math.hypot(x-px,y-py),a=Math.atan2(y-py,x-px);G.held=true;G.def.down(G,x,y,now());
    for(let k=1;k<=4;k++){const b=a+da*k/4;G.def.move(G,px+Math.cos(b)*r,py+Math.sin(b)*r,true);}G.held=false;G.def.up(G);},
  near:(x,y)=>bnNear(G,x,y),q:()=>G.st,
  pos(){const q=S.placed.bn_tree;if(!q)return null;curRow=q.y;const a=imgToStage(q.x,q.y,CAT_D);curRow=null;return{stage:a,vis:[visX(-1e5),visX(1e5)],cat:catLineY()};}};
}
