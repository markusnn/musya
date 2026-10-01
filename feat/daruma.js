{
// ───────────────────────── «Дарума желаний»: the player's real goals on daruma ─────────────────────────
// A goal → a daruma with the first eye painted by the player's own brush stroke; the goal comes true → the second eye.
// Each daruma is a thing (item dm_<n>) the player puts on any shelf; its picture is composed at runtime (body + strokes).
// Unfulfilled ones can be let go (burned at the shrine fire, no guilt); fulfilled ones can be taken to the shrine with thanks.
// S.ext.daruma = {seq, list:[{id,g,c,s,e1,e2,f}], done:[{id,g,c,s,f}], gone}
//   g goal (≤80), c colour key, s set (ms), e1/e2 strokes [[[u,v],…],…] in socket radii, f fulfilled (ms) | null
const DM_R={"big":{"red":[0,0,260,286],"white":[262,0,260,286],"gold":[524,0,260,286],"black":[786,0,260,286],"pink":[1048,0,260,286]},"sm":{"red0":[0,288,152,167],"red1":[0,457,152,167],"red2":[0,626,152,167],"white0":[154,288,152,167],"white1":[154,457,152,167],"white2":[154,626,152,167],"gold0":[308,288,152,167],"gold1":[308,457,152,167],"gold2":[308,626,152,167],"black0":[462,288,152,167],"black1":[462,457,152,167],"black2":[462,626,152,167],"pink0":[616,288,152,167],"pink1":[616,457,152,167],"pink2":[616,626,152,167]},"dab":[[780,288,64,64],[846,288,64,64],[912,288,64,64]],"eye":{"R":[157,99,19],"L":[103,99,19]},"bw":[260,286],"size":[1308,793]};
const DM_COL={red:["Красный","удача и здоровье","#b3302a"],white:["Белый","чистые помыслы","#e9e2d2"],gold:["Золотой","достаток","#cf9f3c"],black:["Чёрный","защита в делах","#2a262b"],pink:["Розовый","любовь","#df9aae"]};
const DM_MAX=12,DM_CAT="Дарума желаний",DM_BW=260,DM_BH=286;
const DM_LORE="Когда загадывают цель, дарума рисуют левый глаз (на картинке он справа), а когда цель сбывается — второй. В конце года старых дарума относят в храм и с благодарностью сжигают на костре — это называется дарума-куё.";
let dmAtl=null,dmD=null,dmJoy=0,dmB=0;
function dmS(){return S.ext.daruma||(S.ext.daruma={seq:0,list:[],done:[],gone:0});}
function dmGet(id){return dmS().list.find(d=>d.id===id);}
function dmPl(n,f){const a=n%10,b=n%100;return`${n} ${f[a===1&&b!==11?0:a>=2&&a<=4&&(b<12||b>14)?1:2]}`;}
function dmDays(ts){const a=new Date(ts),b=new Date(today());a.setHours(0,0,0,0);b.setHours(0,0,0,0);return Math.max(0,Math.round((b-a)/864e5));}
function dmAgo(ts){const n=dmDays(ts);return n===0?"сегодня":n===1?"вчера":dmPl(n,["день","дня","дней"])+" назад";}
function dmDate(ts){const d=new Date(ts);return`${String(d.getDate()).padStart(2,"0")}.${String(d.getMonth()+1).padStart(2,"0")}.${d.getFullYear()}`;}
function dmCut(s,n){return s.length>n?s.slice(0,n-1).trimEnd()+"…":s;}
function dmYearEnd(){const d=today(),m=d.getMonth(),x=d.getDate();return(m===11&&x>=20)||(m===0&&x<=15);}
function dmThumb(c,e,mw,mh){const r=DM_R.sm[c+e],a=DM_R.size,k=Math.min(mw/r[2],mh/r[3]),f=v=>(v*k).toFixed(1);
  return`<span class="dm-th" style="width:${f(r[2])}px;height:${f(r[3])}px;background:url(assets/items/atlas_dm.webp) -${f(r[0])}px -${f(r[1])}px/${f(a[0])}px ${f(a[1])}px no-repeat"></span>`;}

// ── items: one per daruma; the tray thumbnail follows the eyes, the room picture is composed from the strokes ──
function dmItem(d){const r=DM_R.sm[d.c+(d.f?2:1)];return{id:d.id,n:`Дарума «${esc(dmCut(d.g,14))}»`,c:DM_CAT,w:r[2],h:r[3],a:"b",p:0,at:["dm",r[0],r[1]],src:"🎯 дарума желаний",hint:"🎯 Загадай цель: «家» → «Дарума желаний»"};}
function dmReg(d){const I=dmItem(d);if(IT[d.id])Object.assign(IT[d.id],I);else addItems([I]);DMETA[d.id]=[I.w,I.h,"b"];/* shelf size: smaller than the core ×1.25 */loadItem[d.id]=1;dmPaint(d);}
function dmPaint(d){if(!dmAtl)return;const c=document.createElement("canvas");c.width=DM_BW;c.height=DM_BH;dmCompose(c,d);DIMG[d.id]=c;
  for(const k of [...SPRC.keys()])if(k.startsWith(d.id+"|"))SPRC.delete(k);}   // drop the tinted sprite cache
function dmUnreg(id){const i=ITEMS.findIndex(q=>q.id===id);if(i>=0)ITEMS.splice(i,1);delete IT[id];delete DIMG[id];delete DMETA[id];S.owned.delete(id);delete S.placed[id];delete S.dpos[id];
  for(const k of [...SPRC.keys()])if(k.startsWith(id+"|"))SPRC.delete(k);
  if(!ITEMS.some(q=>q.c===DM_CAT)){const k=ICATS.indexOf(DM_CAT);if(k>=0)ICATS.splice(k,1);}}
addItems([],{dm:DM_R.size});
for(const d of dmS().list){S.owned.add(d.id);addItems([dmItem(d)]);loadItem[d.id]=1;}

// ── painting: body from the atlas + ink dabs along the player's strokes, clipped to the socket ──
function dmDab(g,x,y,s,n){const d=DM_R.dab[n%3];g.save();g.translate(x,y);g.rotate((n*2.399)%6.283);g.drawImage(dmAtl,d[0],d[1],d[2],d[3],-s/2,-s/2,s,s);g.restore();}
function dmInk(g,st,side){if(!st||!st.length||!dmAtl)return;const [cx,cy,r]=DM_R.eye[side];let n=side==="L"?7:0;
  g.save();g.beginPath();g.arc(cx,cy,r-1.3,0,7);g.clip();
  for(const s of st){if(s.length===1){const [u,v]=s[0];for(let j=0;j<4;j++)dmDab(g,cx+u*r+Math.cos(j*1.9)*r*.18,cy+v*r+Math.sin(j*1.9)*r*.18,r*1.12,n++);continue;}
    for(let i=1;i<s.length;i++){const [u0,v0]=s[i-1],[u1,v1]=s[i],m=Math.max(1,Math.ceil(Math.hypot(u1-u0,v1-v0)/.12));
      for(let j=0;j<m;j++){const f=j/m;dmDab(g,cx+(u0+(u1-u0)*f)*r,cy+(v0+(v1-v0)*f)*r,r*.98,n++);}}
    const [u,v]=s[s.length-1];dmDab(g,cx+u*r,cy+v*r,r*1.02,n++);}
  g.restore();}
function dmGild(g){g.save();g.globalCompositeOperation="source-atop";const gr=g.createRadialGradient(92,64,8,130,150,200);gr.addColorStop(0,"rgba(255,228,150,.34)");gr.addColorStop(.6,"rgba(255,206,110,.1)");gr.addColorStop(1,"rgba(255,200,90,0)");
  g.fillStyle=gr;g.fillRect(0,0,DM_BW,DM_BH);g.restore();
  g.save();g.translate(198,232);g.rotate(-.14);g.shadowColor="rgba(0,0,0,.45)";g.shadowBlur=4;const lg=g.createLinearGradient(-17,-17,17,17);lg.addColorStop(0,"#f6dc8a");lg.addColorStop(.5,"#d4a842");lg.addColorStop(1,"#b8862a");
  g.fillStyle=lg;g.beginPath();g.moveTo(-15,-17);g.lineTo(16,-15);g.lineTo(17,16);g.lineTo(-16,17);g.closePath();g.fill();g.shadowBlur=0;
  g.strokeStyle="rgba(120,40,20,.75)";g.lineWidth=1.5;g.strokeRect(-12,-12,24,24);g.fillStyle="#7a1e14";g.font=`600 20px "Noto Serif JP","Hiragino Mincho ProN","Yu Mincho",serif`;g.textAlign="center";g.textBaseline="middle";g.fillText("叶",0,1);g.restore();}
function dmCompose(cv,d,o={}){const g=cv.getContext("2d"),k=cv.width/DM_BW;g.setTransform(k,0,0,k,0,0);g.clearRect(0,0,DM_BW,DM_BH);if(!dmAtl)return;
  const c=o.c||d.c,r=DM_R.big[c];g.drawImage(dmAtl,r[0],r[1],r[2],r[3],0,0,DM_BW,DM_BH);
  dmInk(g,o.e1||d.e1,"R");dmInk(g,o.e2||d.e2,"L");if(d.f)dmGild(g);
  if(o.aim){const [cx,cy,rr]=DM_R.eye[o.aim];g.save();g.setLineDash([3,4]);g.lineWidth=2;g.strokeStyle="rgba(238,163,187,.9)";g.beginPath();g.arc(cx,cy,rr+6,0,7);g.stroke();g.restore();}}

// ── the panels: a new daruma, the second eye, letting go ──
document.head.insertAdjacentHTML("beforeend",`<style>
:is(#xpBody,#albumBody) .dm-th{display:inline-block;flex:none}
#xpBody .dm-wrow{display:flex;gap:8px;margin:10px 0 8px}
#xpBody .dm-wrow input{flex:1 1 auto;min-width:0;background:#15120f;color:#efe3c8;border:1px solid var(--line);border-radius:9px;padding:9px 10px;font:inherit}
#xpBody .dm-cols{display:flex;gap:8px;flex-wrap:wrap;margin:4px 0}
#xpBody .dm-sw{width:38px;height:38px;border-radius:50%;border:2px solid var(--line);box-shadow:inset -5px -6px 10px rgba(0,0,0,.35),inset 4px 4px 8px rgba(255,255,255,.18)}
#xpBody .dm-sw[aria-pressed=true]{border-color:var(--sakura);transform:scale(1.08)}
#xpBody p.dm-mean{margin:6px 0 2px;font-size:14px;color:var(--paper)}
#xpBody .dm-face{display:flex;flex-direction:column;align-items:center;margin:6px 0 2px}
#xpBody .dm-face canvas{width:240px;height:264px;touch-action:none;cursor:crosshair}
#xpBody p.dm-goal{margin:4px 0 0;font-family:var(--display);font-size:20px;line-height:1.25;text-align:center;color:var(--paper);max-width:320px;overflow-wrap:anywhere}
#xpBody p.dm-msg{margin:6px 0 10px;text-align:center;font-size:14px;color:var(--sakura);min-height:20px}
:is(#xpBody,#albumBody) .dm-row{display:flex;gap:10px;align-items:flex-start;padding:8px 0;border-top:1px solid var(--line)}
:is(#xpBody,#albumBody) .dm-t{display:flex;flex-direction:column;gap:2px;min-width:0;flex:1}
:is(#xpBody,#albumBody) .dm-t b{font-weight:600;color:var(--paper);overflow-wrap:anywhere}
:is(#xpBody,#albumBody) .dm-t small{font-size:12px;color:var(--muted)}
#xpBody .dm-bt{display:flex;gap:6px;flex-wrap:wrap;margin-top:4px}
#xpBody .dm-bt .btn{flex:none;padding:6px 12px;font-size:13px}
:is(#xpBody,#albumBody) .dm-done b{color:#f0d27a}
</style>`);
function dmFaceHtml(goal,msg){return`<div class="dm-face"><canvas id="dmCv" width="480" height="528"></canvas><p class="dm-goal" id="dmGoalP">${goal}</p></div><p class="dm-msg" id="dmMsg">${msg}</p>`;}
function dmCv(){const c=$("dmCv");if(c){const k=Math.min(2,Math.max(1,devicePixelRatio||1));if(c.width!==Math.round(240*k)){c.width=Math.round(240*k);c.height=Math.round(264*k);}}return c;}
function dmRedraw(){const c=dmCv();if(!c||!dmD)return;
  if(dmD.mode==="new")dmCompose(c,{c:dmD.c,e1:dmD.st,e2:null,f:null},{aim:dmD.st.length?null:"R"});
  else{const d=dmGet(dmD.id);if(d)dmCompose(c,{c:d.c,e1:d.e1,e2:dmD.st,f:null},{aim:dmD.st.length?null:"L"});}}
function dmMsg(t){const m=$("dmMsg");if(m)m.textContent=t;}
function dmWire(){const c=dmCv();if(!c)return;let on=false;
  const at=ev=>{const r=c.getBoundingClientRect(),x=(ev.clientX-r.left)/r.width*DM_BW,y=(ev.clientY-r.top)/r.height*DM_BH,[cx,cy,rr]=DM_R.eye[dmD.mode==="new"?"R":"L"];return[+((x-cx)/rr).toFixed(2),+((y-cy)/rr).toFixed(2)];};
  c.addEventListener("pointerdown",ev=>{if(!dmD)return;const p=at(ev);if(Math.hypot(p[0],p[1])>1.9){dmMsg(dmD.mode==="new"?"Кисть — к глазу справа: это левый глаз дарума":"Второй глаз — слева на картинке");return;}
    if(dmPts()>=140)return;on=true;try{c.setPointerCapture(ev.pointerId);}catch(e){}dmD.st.push([p]);tone(220,.05,"sine",.02);dmRedraw();dmMsg("");});
  c.addEventListener("pointermove",ev=>{if(!on||!dmD)return;const p=at(ev),s=dmD.st[dmD.st.length-1],q=s[s.length-1];if(Math.hypot(p[0]-q[0],p[1]-q[1])<.07||dmPts()>=140)return;s.push(p);dmRedraw();});
  const up=()=>{if(!on)return;on=false;dmMsg(dmD.mode==="new"?"Глаз нарисован. Можно подправить кистью или стереть.":"Второй глаз нарисован!");};
  c.addEventListener("pointerup",up);c.addEventListener("pointercancel",up);}
function dmPts(){return dmD?dmD.st.reduce((a,s)=>a+s.length,0):0;}
function dmInked(){return !!dmD&&dmD.st.some(s=>s.some(([u,v])=>Math.hypot(u,v)<1.05));}
function dmNew(){const z=dmS();if(z.list.length>=DM_MAX){dmHome("Дома уже 12 дарума. Проводи исполнившиеся в храм — и место освободится.");return;}
  dmD={mode:"new",c:"red",g:"",st:[]};
  openPanel("Дарума желаний",`<p class="lead">${DM_LORE}</p>
    <div class="dm-wrow"><input id="dmGoal" maxlength="80" placeholder="Например: пробежать первые 10 км"></div>
    <div class="dm-cols">${Object.keys(DM_COL).map(k=>`<button class="dm-sw" data-x="dm:col:${k}" aria-pressed="${k===dmD.c}" aria-label="${DM_COL[k][0]}" style="background:${DM_COL[k][2]}"></button>`).join("")}</div>
    <p class="dm-mean" id="dmMean">${dmMean("red")}</p>
    ${dmFaceHtml("Напиши цель — она встанет под дарума","Нарисуй кистью левый глаз дарума — на картинке он справа")}
    <div class="row"><button class="btn" data-x="dm:clear">Стереть глаз</button><button class="btn primary" data-x="dm:make">Загадать</button></div>`,"dm_new");
  $("xpBody").scrollTop=0;dmWire();dmRedraw();
  $("dmGoal").addEventListener("input",ev=>{dmD.g=ev.target.value;const p=$("dmGoalP");if(p)p.textContent=dmD.g.trim()?`«${dmD.g.trim()}»`:"Напиши цель — она встанет под дарума";});}
function dmMean(k){return`<b>${DM_COL[k][0]}</b> — ${DM_COL[k][1]}`;}
function dmMake(){const z=dmS(),g=(dmD.g||"").replace(/\s+/g," ").trim().slice(0,80);
  if(!g){dmMsg("Сначала напиши цель — одной строкой");return;}if(!dmInked()){dmMsg("Нарисуй кистью первый глаз — справа");return;}if(z.list.length>=DM_MAX)return;
  const d={id:"dm_"+(++z.seq),g,c:dmD.c,s:Date.now(),e1:dmD.st,e2:null,f:null};z.list.push(d);S.owned.add(d.id);dmReg(d);award("dm_first");dmJoy=2;save();
  chime([784,988,1175]);dmD=null;
  openPanel("Дарума желаний",`<div class="dm-face"><canvas id="dmCv" width="480" height="528"></canvas><p class="dm-goal">«${esc(g)}»</p></div>
    <p class="dm-msg">Цель загадана. Дарума смотрит одним глазом и ждёт.</p>
    <p class="lead">Он лежит в «🧺 Вещи» → «${DM_CAT}». Поставь его на полку в любой комнате — пусть цель будет на виду.</p>
    <div class="row"><button class="btn" data-x="dm:home">← Дом</button><button class="btn primary" data-x="dm:put:${d.id}">Поставить в эту комнату</button></div>`,"dm_new");
  dmCompose(dmCv(),d);}
function dmEye(id){const d=dmGet(id);if(!d||d.f)return;dmD={mode:"eye",id,st:[]};
  openPanel("Дарума желаний",`<p class="lead">Цель исполнилась? Тогда нарисуй дарума второй глаз — теперь он увидит мир целиком.</p>
    ${dmFaceHtml(`«${esc(d.g)}»`,`Загадано ${dmAgo(d.s)}. Второй глаз — слева на картинке.`)}
    <div class="row"><button class="btn" data-x="dm:clear">Стереть</button><button class="btn primary" data-x="dm:done">Исполнилось!</button></div>`,"dm_eye");
  $("xpBody").scrollTop=0;dmWire();dmRedraw();}
function dmDone(){const d=dmGet(dmD&&dmD.id);if(!d||d.f)return;if(!dmInked()){dmMsg("Нарисуй кистью второй глаз — слева");return;}
  const z=dmS();d.e2=dmD.st;d.f=Date.now();z.done.push({id:d.id,g:d.g,c:d.c,s:d.s,f:d.f});dmReg(d);dmD=null;
  disc("daruma",d.id);award("dm_kanau");if(z.done.length>=5)award("dm_five");S.needs.joy=clamp(S.needs.joy+12,0,100);dmJoy=1;save();
  chime([1046,1318,1568,2093]);const n=dmDays(d.s);
  openPanel("Дарума желаний",`<div class="dm-face"><canvas id="dmCv" width="480" height="528"></canvas><p class="dm-goal">«${esc(d.g)}»</p></div>
    <p class="dm-msg">Исполнилось! ✨</p><p class="lead">${n?`От первого глаза до второго — ${dmPl(n,["день","дня","дней"])}.`:"Загадано и исполнено в один день!"} Теперь дарума смотрит обоими глазами, а на боку у него золотая метка 叶 — «сбылось». Цель записана в альбом.</p>
    <div class="row"><button class="btn primary" data-x="dm:home">← Дом</button></div>`,"dm_eye");
  dmCompose(dmCv(),d);}
function dmBurn(id){const d=dmGet(id);if(!d)return;
  openPanel("Дарума желаний",`${dmFaceHtml(`«${esc(d.g)}»`,"")}
    <p class="lead">${d.f?"Дарума отслужил своё. Его проводят в храм и сжигают на костре с благодарностью, а цель останется в альбоме.":"Цели меняются — это не поражение. Дарума сожгут на храмовом костре с благодарностью, и место на полке освободится."}</p>
    <div class="row"><button class="btn" data-x="dm:home">Оставить</button><button class="btn primary" data-x="dm:fire:${id}">${d.f?"Проводить в храм":"Отпустить"}</button></div>`,"dm_burn");
  $("xpBody").scrollTop=0;dmCompose(dmCv(),d);}
function dmFire(id){const d=dmGet(id);if(!d)return;const z=dmS(),c=dmCv(),thanks=!!d.f;
  z.list=z.list.filter(q=>q.id!==id);z.gone=(z.gone||0)+1;dmUnreg(id);save();ui();
  const row=$("xpBody").querySelector(".row");if(row)row.innerHTML=`<button class="btn" data-x="dm:home">← Дом</button>`;
  const lead=$("xpBody").querySelector("p.lead");if(lead)lead.textContent=thanks?"Дарума уходит вместе с дымом. Спасибо ему — он видел, как цель сбылась.":"Цель отпущена. Дым уносит её легко, без сожалений.";
  if(c)dmBurnAnim(c,d);tone(110,1.2,"sine",.05);setTimeout(()=>chime([523,659,784]),2600);}
function dmBurnAnim(cv,d){const g=cv.getContext("2d"),k=cv.width/DM_BW,t0=performance.now(),a=document.createElement("canvas"),b=document.createElement("canvas");a.width=b.width=DM_BW;a.height=b.height=DM_BH;dmCompose(a,d);
  const gb=b.getContext("2d"),sp=Array.from({length:46},(_,i)=>({x:130+((i*37)%90-45),d:(i*0.071)%3.2+.3,v:30+(i*13)%40,w:((i*7)%11-5)*3,s:.8+(i%4)*.5})),fl=[[-38,.7],[-20,1],[0,1.25],[20,.95],[38,.7],[-10,.8],[12,.85]];
  const step=()=>{if(!cv.isConnected)return;const e=(performance.now()-t0)/1000,F=Math.min(1,e/.7)*(1-smooth((e-3.4)/1.4));g.setTransform(k,0,0,k,0,0);g.clearRect(0,0,DM_BW,DM_BH);
    const bg=g.createRadialGradient(130,230,10,130,200,170);bg.addColorStop(0,`rgba(120,52,20,${.55*F+.12})`);bg.addColorStop(1,"rgba(20,12,10,0)");g.fillStyle=bg;g.fillRect(0,0,DM_BW,DM_BH);
    const sink=smooth((e-.9)/2.6),dark=smooth((e-.4)/2),fade=1-smooth((e-2.2)/1.4);
    if(fade>0){gb.globalCompositeOperation="source-over";gb.clearRect(0,0,DM_BW,DM_BH);gb.drawImage(a,0,0);gb.globalCompositeOperation="source-atop";gb.fillStyle=`rgba(30,12,6,${.75*dark})`;gb.fillRect(0,0,DM_BW,DM_BH);const wl=gb.createLinearGradient(0,DM_BH,0,DM_BH*.3);wl.addColorStop(0,`rgba(255,130,40,${.55*F})`);wl.addColorStop(1,"rgba(255,130,40,0)");gb.fillStyle=wl;gb.fillRect(0,0,DM_BW,DM_BH);
      g.save();g.beginPath();g.rect(0,0,DM_BW,250);g.clip();g.globalAlpha=fade;const s=.62*(1-.12*sink);g.drawImage(b,130-DM_BW*s/2,250-DM_BH*s+sink*70,DM_BW*s,DM_BH*s);g.restore();}
    g.fillStyle="#2a1810";g.save();g.translate(130,254);for(const r of [-.18,.18,0]){g.save();g.rotate(r);g.fillRect(-70,-5,140,10);g.restore();}g.restore();
    g.save();g.globalCompositeOperation="lighter";
    for(const [x,h] of fl){const fh=(95+45*Math.sin(e*7+x)+20*Math.sin(e*13+x*2))*h*F,fw=22*h*(.6+.4*F);if(fh<2)continue;const gr=g.createLinearGradient(0,252,0,252-fh);gr.addColorStop(0,"rgba(255,170,60,.85)");gr.addColorStop(.5,"rgba(240,90,30,.55)");gr.addColorStop(1,"rgba(200,40,20,0)");
      g.fillStyle=gr;g.beginPath();g.moveTo(130+x-fw,252);g.quadraticCurveTo(130+x-fw*.8,252-fh*.5,130+x+Math.sin(e*5+x)*6,252-fh);g.quadraticCurveTo(130+x+fw*.8,252-fh*.5,130+x+fw,252);g.fill();}
    for(const p of sp){const u=e-p.d;if(u<0||u>2.6||F<=0)continue;const y=250-u*p.v*1.6,x=p.x+p.w*u+Math.sin(u*4+p.x)*5;g.fillStyle=`rgba(255,${180+(p.s*20|0)},90,${(1-u/2.6)*.9*F})`;g.beginPath();g.arc(x,y,p.s,0,7);g.fill();}
    g.restore();
    if(e>1.6){const u=e-1.6,A=Math.min(1,u/.8);for(let i=0;i<9;i++){const v=(u*.42+i*.11)%1;const x=130+Math.sin(i*2.3+u*1.3)*(10+v*26),y=236-v*210,r=16+v*38,sg=g.createRadialGradient(x,y,0,x,y,r);sg.addColorStop(0,`rgba(176,166,156,${.13*A*(1-v)})`);sg.addColorStop(1,"rgba(176,166,156,0)");g.fillStyle=sg;g.fillRect(x-r,y-r,r*2,r*2);}}
    if(e<6.2)requestAnimationFrame(step);};
  requestAnimationFrame(step);}
function dmHome(note){openHub();const c=[...$("xpBody").querySelectorAll(".hubc")].find(x=>/^🎯/.test(x.firstElementChild?.textContent||""));
  if(c){c.classList.add("open");setTimeout(()=>c.scrollIntoView({block:"start"}),0);if(note)c.insertAdjacentHTML("beforeend",`<p class="lead">${note}</p>`);}}

// ── the hub card, the album, the stamps ──
function dmStatus(){const z=dmS(),w=z.list.filter(d=>!d.f).length,k=z.done.length;
  if(!w&&!k)return"Загадай цель — нарисуй первый глаз";
  if(!w)return`Все цели исполнились (${k}) — загадай новую`;
  return`${w===1?"1 дарума ждёт":`${w} дарума ждут`}, один глаз нарисован${k?` · исполнилось: ${k}`:""}`;}
function dmRows(){const z=dmS(),L=[...z.list].sort((a,b)=>(!!a.f-!!b.f)||a.s-b.s);
  return L.map(d=>{const pl=S.placed[d.id],rm=pl&&ROOMS.find(r=>r.id===pl.r);
    return`<div class="dm-row${d.f?" dm-done":""}">${dmThumb(d.c,d.f?2:1,40,44)}<div class="dm-t"><b>«${esc(d.g)}»</b><small>${d.f?`исполнилось ${dmAgo(d.f)}`:`загадано ${dmAgo(d.s)}`} · ${DM_COL[d.c][0].toLowerCase()}${rm?` · стоит: ${rm.ru}`:""}</small>
    <span class="dm-bt">${d.f?`<button class="btn" data-x="dm:burn:${d.id}">Проводить в храм</button>`:`<button class="btn primary" data-x="dm:eye:${d.id}">Исполнилось!</button><button class="btn" data-x="dm:burn:${d.id}">Отпустить</button>`}</span></div></div>`;}).join("");}
hook("hub",()=>{const z=dmS(),full=z.list.length>=DM_MAX;
  return`<div class="hubc"><h4>🎯 Дарума желаний <i>達磨</i></h4><p>${dmStatus()}</p><p>${DM_LORE}${dmYearEnd()&&z.list.some(d=>d.f)?" Год кончается — самое время проводить исполнившихся дарума в храм.":""}</p>
  ${dmRows()}<div class="row"><button class="btn${full?"":" primary"}" data-x="dm:new">${full?"Дома уже 12 дарума":"Загадать цель"}</button></div></div>`;});
hook("album",el=>{const z=dmS();if(!z.done.length)return;
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Дарума желаний</h3><p class="lead">Исполнилось целей: ${z.done.length}. Каждая — с двумя нарисованными глазами.</p>
  <div class="dm-alb">${[...z.done].reverse().map(d=>`<div class="dm-row dm-done">${dmThumb(d.c,2,40,44)}<div class="dm-t"><b>«${esc(d.g)}»</b><small>загадано ${dmDate(d.s)} · исполнилось ${dmDate(d.f)} · ${dmPl(Math.max(0,Math.round((new Date(d.f).setHours(0,0,0,0)-new Date(d.s).setHours(0,0,0,0))/864e5)),["день","дня","дней"])}</small></div></div>`).join("")}</div>`);});
STAMPS.push(["dm_first","達","Первый дарума","Загадай цель и нарисуй дарума первый глаз"],["dm_kanau","叶","Сбылось!","Нарисуй дарума второй глаз — цель исполнилась"],["dm_five","福","Пять сбывшихся целей","Пять дарума смотрят обоими глазами"]);
hook("click",(k,btn)=>{if(!k.startsWith("dm:"))return;const a=k.split(":");
  if(a[1]==="new")dmNew();
  else if(a[1]==="col"&&dmD&&DM_COL[a[2]]){dmD.c=a[2];for(const b of $("xpBody").querySelectorAll(".dm-sw"))b.setAttribute("aria-pressed",b.dataset.x===k);const m=$("dmMean");if(m)m.innerHTML=dmMean(a[2]);dmRedraw();tone(660,.06,"sine",.03);}
  else if(a[1]==="clear"&&dmD){dmD.st=[];dmRedraw();dmMsg(dmD.mode==="new"?"Нарисуй кистью левый глаз дарума — на картинке он справа":"Второй глаз — слева на картинке");}
  else if(a[1]==="make"&&dmD)dmMake();
  else if(a[1]==="eye")dmEye(a[2]);
  else if(a[1]==="done"&&dmD)dmDone();
  else if(a[1]==="burn")dmBurn(a[2]);
  else if(a[1]==="fire")dmFire(a[2]);
  else if(a[1]==="put"&&IT[a[2]]){closePanel();if(!(S.placed[a[2]]&&S.placed[a[2]].r===S.room))putItem(a[2]);}
  else if(a[1]==="home")dmHome();
  return true;});
hook("panelClose",id=>{if(/^dm_/.test(id||""))dmD=null;});

// ── in the room: a tap tells the goal; fulfilled daruma keep a soft golden glow ──
hook("itemTap",(it,I)=>{if(!/^dm_/.test(it.id))return;const d=dmGet(it.id);if(!d)return;
  toast(`«${dmCut(d.g,18)}» · ${d.f?`сбылось ${dmAgo(d.f)}`:`загадано ${dmAgo(d.s)}`}`);
  if(d.f){chime([1318,1568,2093]);fxAt(it,["✨","🌟"],4);}else{tone(160,.2,"triangle",.06);fxAt(it,["✨"],2);}
  if(!petAway())react(d.f?"😻":"😺",1.3);return true;});
hook("draw",(t,front)=>{if(scene.on)return;const z=dmS();
  for(const d of z.list){if(!d.f)continue;const q=S.placed[d.id];if(!q||q.r!==S.room||!DMETA[d.id])continue;
    const P=ipos({id:d.id,x:q.x,y:q.y});if(isFront(P)!==front)continue;const [x0,y0,w,h]=spriteBox(P),[cx,cy]=imgToStage(x0+w/2,y0+h*.5,CAT_D),R=w*BGM.k*.95,p=.75+.25*Math.sin(t*1.6+q.x);
    ctx.save();ctx.globalCompositeOperation="lighter";const gr=ctx.createRadialGradient(cx,cy,0,cx,cy,R);gr.addColorStop(0,"rgba(255,214,130,0)");gr.addColorStop(.5,"rgba(255,214,130,0)");gr.addColorStop(.62,`rgba(255,214,130,${.2*p})`);gr.addColorStop(1,"rgba(255,200,100,0)");ctx.fillStyle=gr;ctx.fillRect(cx-R,cy-R,R*2,R*2);
    for(let i=0;i<3;i++){const u=(t*.25+i/3+q.x*.001)%1,mx=cx+Math.sin(t+i*2.1)*w*BGM.k*.35,my=cy+h*BGM.k*.3-u*h*BGM.k*.9;ctx.fillStyle=`rgba(255,226,150,${.55*Math.sin(u*Math.PI)})`;ctx.beginPath();ctx.arc(mx,my,1.6*view.s+1,0,7);ctx.fill();}
    ctx.restore();}});
hook("sec",()=>{if(dmJoy&&!overlaysOpen()&&!scene.on){const j=dmJoy;dmJoy=0;if(!petAway()){if(j===1){react("😻",2.6);burst(18);sfx("chime");}else react("😺",1.8);}}});
hook("boot",()=>{dmB=1;atlasImg("dm",im=>{dmAtl=im;for(const d of dmS().list)dmReg(d);if(dmD)dmRedraw();});});

// test handles
X.dm={S:dmS,open:dmNew,eye:dmEye,burn:dmBurn,fire:dmFire,home:dmHome,draft:()=>dmD,
  stroke(pts){if(!dmD)return;dmD.st.push(pts);dmRedraw();return dmInked();},goal(g){const i=$("dmGoal");if(i){i.value=g;i.dispatchEvent(new Event("input"));}},
  col(c){hk("click","dm:col:"+c);},make(){dmMake();return dmS().list.length;},done:()=>dmDone(),
  place(id,room,x,y){S.placed[id]={r:room,x,y};loadItem(id);},
  tap(id){const q=S.placed[id];return hk("itemTap",{id,x:q.x,y:q.y,item:true},IT[id],now())?$("toast").textContent:null;}};
}
