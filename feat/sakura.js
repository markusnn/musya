{
// ───────────────────────── «Дерево, которое растёт месяц»: a sakura stone in the courtyard grows by watered days ─────────────────────────
// S.ext.tree = {pl: dayKey planted, days: watered days, last: dayKey of the last watering, bd: dayKey the tree first bloomed}
const SK_TH=[0,2,5,10,16,23,30],SK_N=["Косточка в земле","Росток","Саженец","Молодое деревце","Деревце","Молодое дерево","Цветущая сакура"];
const SK_R={s0:["sk",394,742,170,130],s1:["sk",232,742,160,180],s2:["sk",0,742,230,330],s3:["sk",1044,0,330,450],s4:["sk",592,0,450,590],s5:["sk",0,0,590,740],
  s6:["sk1",0,0,800,900],summer:["sk1",802,0,800,900],autumn:["sk2",0,0,800,900],winter:["sk2",802,0,800,900]};
const SK_A={sk:[1400,1072],sk1:[1604,900],sk2:[1604,900]},SK_IM={},SK_SC={s0:1.7,s1:1.6,s2:1.3,s3:1.1};   // young stages are drawn a bit larger so they read on a phone
const SK_LOOK={s6:"цветёт",summer:"летняя листва",autumn:"осенний наряд",winter:"зимний сон"};
const SK_X=1430,SK_Y=1222;   // image coords of the tree's foot; visX pulls it in on narrow phones
STAMPS.push(["sk_bloom","樹","Своя сакура","Вырасти сакуру из косточки: 30 дней полива"]);
const skS=()=>S.ext.tree||null;
function skStage(d){let i=0;SK_TH.forEach((v,k)=>{if(d>=v)i=k;});return i;}
function skDays(a,b){return Math.round((Date.parse(b)-Date.parse(a))/864e5);}
function skWord(n,f){const a=n%10,b=n%100;return n+" "+(a===1&&b!==11?f[0]:a>=2&&a<=4&&(b<12||b>14)?f[1]:f[2]);}
function skSpring(){const T=today(),m=T.getMonth()+1,d=T.getDate();return m===3&&d>=25||m===4&&d<=15;}
// the grown tree blooms for a week after it first bloomed and every real spring; otherwise it wears the season
function skLook(){const tr=skS();if(!tr)return null;const st=skStage(tr.days);if(st<6)return"s"+st;
  if(tr.bd&&skDays(tr.bd,dayKey())<7||skSpring())return"s6";const T=today(),m=T.getMonth()+1,d=T.getDate();
  if(m===12||m<=3)return"winter";if(m===10||m===11||m===9&&d>=20)return"autumn";return"summer";}
function skLoad(){for(const k of Object.keys(SK_A))if(!SK_IM[k])atlasImg(k,im=>{SK_IM[k]=im;});}
function skPos(){return{x:visX(SK_X,230),y:SK_Y};}
function skDue(){const tr=skS();return !!tr&&tr.days<30&&tr.last!==dayKey();}
// screen frame of the tree picture: foot point and scale (image px → stage px) at the depth of the foot
function skFrame(){const P=skPos(),oc=curRow;curRow=P.y;const [bx,by]=imgToStage(P.x,P.y,CAT_D),[,ty]=imgToStage(P.x,P.y-100,CAT_D);curRow=oc;return{bx,by,k:(by-ty)/100,P};}
let skAnim=null,skWet=null,skAcc=0;const skLeaves=[];
function skPic(key,alpha,sc,t){
  const r=SK_R[key];if(!r)return;const im=SK_IM[r[0]];if(!im||alpha<=0)return;const [,sx,sy,w,h]=r,F=skFrame(),k=F.k*sc*(SK_SC[key]||1),W=w*k,H=h*k,N=key==="s0"||key==="s1"?1:14;
  const wind=(weather.on?2.8:1)*(1+.5*Math.max(0,Math.sin(t*.21))),amp=Math.min(14,h*.012)*wind*F.k;
  ctx.save();ctx.globalAlpha=alpha;
  for(let i=0;i<N;i++){const u=i/N,hu=1-(i+.5)/N,off=(Math.sin(t*1.05)+.35*Math.sin(t*2.7+i*.4))*amp*Math.pow(hu,1.7);
    ctx.drawImage(im,sx,sy+h*u,w,h/N+.5,F.bx-W/2+off,F.by-H+H*u,W,H/N+1);}
  if(key==="s6"){const gx=F.bx,gy=F.by-H*.66,R=W*.5,gr=ctx.createRadialGradient(gx,gy,0,gx,gy,R);gr.addColorStop(0,`rgba(240,168,196,${dayTint()[1]?.13:.07})`);gr.addColorStop(1,"rgba(240,168,196,0)");ctx.globalCompositeOperation="lighter";ctx.fillStyle=gr;ctx.fillRect(gx-R,gy-R,R*2,R*2);}
  ctx.restore();
}
hook("draw",(t,front)=>{
  const tr=skS();if(S.room!=="courtyard"||!tr)return;if((SK_Y>catLineY()+6)!==front)return;skLoad();
  const key=skLook(),e=skAnim?(t-skAnim.t0)/1.6:1;
  if(skAnim&&e<1&&skAnim.from!==key){const a=smooth(clamp(e,0,1));skPic(skAnim.from,1-a,1,t);skPic(key,a,.86+.14*a,t);}else{if(e>=1)skAnim=null;skPic(key,1,1,t);}
  const F=skFrame();
  // the damp patch after watering, and the can pouring
  if(skWet){const e2=(Date.now()-skWet)/1000,a=clamp(1-e2/40,0,1);if(a>0){ctx.fillStyle=`rgba(8,10,14,${.35*a})`;ctx.beginPath();ctx.ellipse(F.bx,F.by-6*F.k,70*F.k,13*F.k,0,0,Math.PI*2);ctx.fill();}}
  if(skAnim&&skAnim.can){const c=t-skAnim.t0+2.2;if(c<2.6){const u=smooth(clamp(c/.5,0,1))*(1-smooth(clamp((c-2.1)/.5,0,1))),x=F.bx-60*F.k,y=F.by-150*F.k;
    ctx.save();ctx.globalAlpha=u;ctx.translate(x,y);ctx.rotate(.55*u);fDraw(ctx,"g_can",0,0,120*F.k);ctx.restore();
    if(c>.4&&c<2.2)for(let i=0;i<10;i++){const d=((c*2.4+i/10)%1),dx=x+40*F.k+Math.sin(i*2.3)*18*F.k,dy=y+18*F.k+d*120*F.k;ctx.fillStyle=`rgba(170,205,225,${.85*(1-d)})`;ctx.beginPath();ctx.ellipse(dx,dy,2.2*F.k*1.4,5*F.k*1.4,0,0,Math.PI*2);ctx.fill();}}}
  // autumn: a leaf now and then
  for(const L of skLeaves){ctx.save();ctx.translate(L.x,L.y);ctx.rotate(L.r);ctx.globalAlpha=Math.min(1,L.life);ctx.fillStyle=L.c;ctx.beginPath();ctx.ellipse(0,0,L.s,L.s*.55,0,0,Math.PI*2);ctx.fill();ctx.restore();}
});
function skCrownPt(){const F=skFrame(),r=SK_R.s6;return[F.bx+rand(-.38,.38)*r[3]*F.k,F.by-rand(.5,.9)*r[4]*F.k];}
function skPetals(n){for(let i=0;i<n;i++){const [x,y]=skCrownPt();sakura.list.push({x,y,vx:rand(5,45),vy:rand(10,40),rot:rand(0,6),vr:rand(-2.5,2.5),size:rand(4,7.5)*Math.max(.8,view.s),ph:rand(0,6),life:rand(4,8),sk:1});}}
hook("tick",(t,dt)=>{
  if(S.room!=="courtyard"||!skS()||overlaysOpen())return;const key=skLook();
  if(key==="s6"){skAcc+=dt*(weather.on?5:2.4);while(skAcc>1){skAcc--;skPetals(1);}}
  else if(key==="autumn"&&Math.random()<dt*.7){const [x,y]=skCrownPt();skLeaves.push({x,y,vx:rand(8,30),vy:rand(22,40),r:rand(0,6),vr:rand(-2,2),s:rand(3,5)*Math.max(.8,view.s),c:pick(["#b8542a","#d0782e","#9a3a1e","#d89a3a"]),life:7});}
  for(const L of skLeaves){L.x+=(L.vx+Math.sin(L.life*2)*14)*dt;L.y+=L.vy*dt;L.r+=L.vr*dt;L.life-=dt;}
  for(let i=skLeaves.length-1;i>=0;i--)if(skLeaves[i].life<=0||skLeaves[i].y>view.H)skLeaves.splice(i,1);
});
hook("room",()=>{sakura.list=sakura.list.filter(q=>!q.sk);skLeaves.length=0;});
// Musya walks to the tree and watches
function skVisit(face,after="idle"){if(petAway())return;const P=skPos();walkTo({x:P.x-190},after);setTimeout(()=>{if(S.room!=="courtyard")return;const F=skFrame();pointer.x=F.bx;pointer.y=F.by-200*F.k;pointer.known=true;pet.gazeUntil=now()+6;if(face)react(face,2);},1500);}
function skPlant(){if(skS())return;S.ext.tree={pl:dayKey(),days:0,last:null};skLoad();skAnim={from:"-",t0:now()+.9};save();ui();tabDots();
  if(!petAway()){skVisit("😺","knead");}setTimeout(()=>{sfx("pop");tone(420,.12,"triangle",.05);tone(630,.14,"sine",.03);toast("🌸 Косточка посажена — поливай каждый день");},900);}
function skWater(){const tr=skS();if(!tr){skPlant();return;}if(tr.days>=30){skHanami();return;}
  if(tr.last===dayKey()){toast("Сегодня уже полито — приходи завтра");return;}
  const was=skLook(),st0=skStage(tr.days);tr.days++;tr.last=dayKey();const st=skStage(tr.days),t=now();
  skAnim={from:was,t0:t+2.2,can:1};skWet=Date.now()+2000;save();ui();tabDots();skVisit(null);
  setTimeout(()=>sfx("splash"),700);setTimeout(()=>sfx("splash"),1500);
  setTimeout(()=>{if(!petAway())react(st>st0?"😻":"😺",2);S.needs.joy=clamp(S.needs.joy+4,0,100);
    if(st===6){tr.bd=dayKey();save();skPetals(90);chime([784,988,1175,1568]);award("sk_bloom");disc("bloom","tree");toast("🌸 Твоя сакура зацвела!");}
    else if(st>st0){chime([988,1318]);const F=skFrame();for(let i=0;i<5;i++)floatFx.push({g:pick(["✨","🌱"]),x:F.bx+rand(-40,40)*view.s,y:F.by-rand(40,120)*view.s,t:now()+i*.12});toast(`🌱 Сакура подросла: ${SK_N[st].toLowerCase()}`);}
    else{tone(660,.1,"sine",.04);toast(`💧 Полито: ${tr.days} из 30 дней`);}},2300);}
function skHanami(){if(!petAway())skVisit("😌","music");S.needs.joy=clamp(S.needs.joy+6,0,100);const k=skLook();
  if(k==="s6")setTimeout(()=>skPetals(40),1400);toast(k==="s6"?"Ханами: Муся любуется сакурой":k==="winter"?"Сакура спит под снегом до весны":k==="autumn"?"Сакура в осеннем наряде":"Сакура шелестит листвой");}
hook("tray",(tray,room)=>{if(room!=="courtyard"||(S.trayMode[room]||"play")!=="play")return;const tr=skS(),el=tray.querySelector(".items");if(!el)return;
  const b=!tr?["sk:plant","🌸","Посадить косточку сакуры"]:tr.days<30?["sk:water","💧",tr.last===dayKey()?`Сакура полита · ${tr.days}/30`:"Полить сакуру"]:["sk:hanami","🌸","Ханами под сакурой"];
  el.insertAdjacentHTML("afterbegin",`<button class="item wide" data-x="${b[0]}"><span class="ico">${b[1]}</span><span class="nm">${b[2]}</span></button>`);});
hook("click",(k)=>{if(!k.startsWith("sk:"))return;
  if(k==="sk:plant")skPlant();else if(k==="sk:water")skWater();else if(k==="sk:hanami")skHanami();
  else if(k==="sk:go"||k==="sk:hubwater"){closePanel();goRoom("courtyard");if(k==="sk:hubwater")setTimeout(skWater,500);}
  return true;});
// tap on the young tree (or the trunk of the grown one): water it if it is thirsty, otherwise a small greeting
hook("hit",(x,y)=>{if(S.room!=="courtyard"||!skS()||scene.on)return;const key=skLook(),r=SK_R[key],F=skFrame(),big=key.length>2||key==="s6";
  const z=SK_SC[key]||1,hw=(big?70:r[3]*.4*z)*F.k,top=(big?420:r[4]*.95*z)*F.k;if(Math.abs(x-F.bx)>hw||y>F.by+10*F.k||y<F.by-top)return;
  if(skDue()){skWater();return true;}audioInit();chime([1318,1760]);if(key==="s6")skPetals(12);toast(`🌸 ${SK_N[skStage(skS().days)]} · ${Math.min(30,skS().days)}/30`);return true;});
hook("tabDot",r=>r==="courtyard"&&skDue());
hook("away",ms=>{const tr=skS();if(tr&&skDue()&&tr.last&&ms>3*3600e3)return{i:"💧",t:"Сакура во дворике ждёт полива"};if(tr&&tr.days>=30&&skSpring())return{i:"🌸",t:"Во дворике цветёт твоя сакура"};});
function skThumb(key,mw,mh){const r=SK_R[key],A=SK_A[r[0]],k=Math.min(mw/r[3],mh/r[4]),f=v=>(v*k).toFixed(1);
  return`<span style="display:inline-block;flex:none;width:${f(r[3])}px;height:${f(r[4])}px;background:url(assets/items/atlas_${r[0]}.webp) -${f(r[1])}px -${f(r[2])}px/${f(A[0])}px ${f(A[1])}px no-repeat"></span>`;}
document.head.insertAdjacentHTML("beforeend","<style>.sk-row{display:flex;gap:12px;align-items:flex-end}.sk-row>div{flex:1;min-width:0}.sk-bar{height:6px;border-radius:3px;background:#0a0d0c;overflow:hidden;margin:6px 0 2px}.sk-bar i{display:block;height:100%;background:var(--sakura,#eea3bb)}</style>");
hook("hub",()=>{const tr=skS();
  if(!tr)return`<div class="hubc"><h4>🌸 Сакура <i>桜</i></h4><p>Во дворике есть местечко для дерева. Посади косточку сакуры и поливай её каждый день — за месяц вырастет настоящее дерево и зацветёт.</p><div class="row"><button class="btn primary" data-x="sk:go">Во дворик</button></div></div>`;
  const st=skStage(tr.days),key=skLook(),done=tr.last===dayKey();
  const info=st<6?`<p><b>${SK_N[st]}</b></p><div class="sk-bar"><i style="width:${(tr.days/30*100).toFixed(1)}%"></i></div><p>Полито дней: ${tr.days} из 30</p><p>Следующая стадия через ${skWord(SK_TH[st+1]-tr.days,["полив","полива","поливов"])}</p><p>${done?"Сегодня уже полито ✓":"Сегодня сакура ещё не полита"}</p>`
    :`<p><b>Сакура выросла</b> — сейчас ${SK_LOOK[key]}.</p><p>Цветёт каждую весну, с 25 марта по 15 апреля.</p>`;
  return`<div class="hubc"><h4>🌸 Сакура <i>桜</i></h4><div class="sk-row">${skThumb(key,96,110)}<div>${info}</div></div><div class="row">${st<6&&!done?`<button class="btn primary" data-x="sk:hubwater">💧 Полить</button>`:""}<button class="btn" data-x="sk:go">Во дворик</button></div></div>`;});
hook("boot",()=>{if(skS())skLoad();});
X.sk={plant:skPlant,water:skWater,look:skLook,pos:skPos,frame:skFrame,st:skS,
  set(n){if(!skS())S.ext.tree={pl:dayKey(),days:0,last:null};const tr=S.ext.tree;tr.days=n;tr.last=null;if(n<30)delete tr.bd;skLoad();ui();tabDots();}};
}
