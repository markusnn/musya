{
// ───────────────────────── «Ночной парад ста демонов» (百鬼夜行): on the real new moon every yōkai Musya has met walks past the torii ─────────────────────────
// The parade walks on the three dark nights around the new moon (D−1, D, D+1; 20:00–04:00), once per lunation; it is announced 3 days before.
// S.ext.parade = {L: dayKey of the new-moon night D being tracked, prep:{lan,mask,off}, greet:[keys bowed to], pass:{t0,seq}|null, done, saw,
//   scroll:{m,g,p}|null (lies at the torii until picked up), got:{"YYYY-MM":{g,p}}, n: parades seen, ann: dayKey of the last toast, miss: L of a missed parade}
MON.m_pd_bearer=[320,520];MON.m_pd_biwa=[340,520];MON.m_pd_wanyudo=[460,460];
BESTIARY.push(["pd_bearer","m_pd_bearer","Тётин-кодзо","Мальчик с фонарём из преданий Сэндая, лицо красное, как спелый физалис. В тёмные ночи обгоняет путника и идёт впереди — догнать его нельзя."],
 ["pd_biwa","m_pd_biwa","Бива-бокубоку","Старая бива, сто лет певшая сказания о доме Тайра, стала слепым монахом. Нарисована Ториямой Сэкиэном в 1784 году."],
 ["pd_wanyudo","m_pd_wanyudo","Ванюдо","Горящее колесо бычьей повозки с головой сурового монаха. Катится ночью по улицам Киото, и выглядывать на него из окна нельзя. Нарисован Ториямой Сэкиэном."]);
const PD_MON=["январь","февраль","март","апрель","май","июнь","июль","август","сентябрь","октябрь","ноябрь","декабрь"];
const PD_AT={"pd_s01":[0,0],"pd_s02":[232,0],"pd_s03":[464,0],"pd_s04":[696,0],"pd_s05":[0,112],"pd_s06":[232,112],"pd_s07":[464,112],"pd_s08":[696,112],"pd_s09":[0,224],"pd_s10":[232,224],"pd_s11":[464,224],"pd_s12":[696,224]};
addItems([...PD_MON.map((m,i)=>{const id="pd_s"+String(i+1).padStart(2,"0");return{id,n:"Свиток парада · "+m,c:"Свитки парада",w:230,h:110,a:"t",p:90,at:["pd",...PD_AT[id]],src:"🏮 Ночной парад",hint:"Остаётся у тории, когда в новолуние ("+m+") пройдёт Ночной парад"};}),
 {id:"pd_chochin",n:"Фонарь с парада",c:"Дары парада",w:110,h:250,a:"t",p:80,at:["pd",0,336],glow:[55,133],src:"🏮 Ночной парад",hint:"Повесь у входа фонарь перед новолунием — парад оставит свой"},
 {id:"pd_kasa",n:"Зонтик каса-обакэ",c:"Дары парада",w:96,h:200,a:"b",p:80,at:["pd",112,336],src:"🏮 Ночной парад",hint:"Надень Мусе маску перед новолунием — парад оставит подарок"},
 {id:"pd_taiko",n:"Барабанчик парада",c:"Дары парада",w:170,h:160,a:"b",p:80,at:["pd",210,336],src:"🏮 Ночной парад",hint:"Оставь у тории подношение перед новолунием"},
 {id:"pd_bell",n:"Бубенцы парада",c:"Дары парада",w:96,h:200,a:"t",p:80,at:["pd",382,336],src:"🏮 Ночной парад",hint:"Поклонись на Ночном параде пятерым ёкаям"},
 {id:"pd_wheel",n:"Колёсико Ванюдо",c:"Дары парада",w:170,h:170,a:"b",p:120,at:["pd",480,336],glow:[85,86],src:"🏮 Ночной парад",hint:"Подготовься к параду целиком: фонарь, маска и подношение"}],{pd:[940,586]});
STAMPS.push(["pd_first","鬼","Ночной парад","Увидь Ночной парад в новолуние"],["pd_three","夜","Три новолуния","Встреть Ночной парад три раза"],["pd_bow","礼","Поклон каждому","Поклонись 10 ёкаям за одну ночь парада"]);
const pdS=()=>S.ext.parade||(S.ext.parade={prep:{},greet:[],got:{},n:0});
// ── the real moon: mean new moon + the main periodic terms (Meeus, ch. 49) → ms; error ~minutes
const PD_DAY=864e5;
function pdNM(k){const T=k/1236.85,E=1-.002516*T,r=Math.PI/180,M=(2.5534+29.1053567*k)*r,Mp=(201.5643+385.81693528*k)*r,F=(160.7108+390.67050284*k)*r,sin=Math.sin;
  const c=-.4072*sin(Mp)+.17241*E*sin(M)+.01608*sin(2*Mp)+.01039*sin(2*F)+.00739*E*sin(Mp-M)-.00514*E*sin(Mp+M)+.00208*E*E*sin(2*M)-.00111*sin(Mp-2*F)-.00057*sin(Mp+2*F)+.00056*E*sin(2*Mp+M)-.00042*sin(3*Mp);
  return(2451550.09766+29.530588861*k+.00015437*T*T+c-2440587.5)*PD_DAY-69e3;}
const pdDN=d=>Math.round(Date.UTC(d.getFullYear(),d.getMonth(),d.getDate())/PD_DAY);          // local calendar day number
const pdDate=n=>{const u=new Date(n*PD_DAY);return new Date(u.getUTCFullYear(),u.getUTCMonth(),u.getUTCDate());};
const pdD=k=>pdDN(new Date(pdNM(k)-PD_DAY/2));   // the date whose night (20:00–04:00) is centred nearest to the new-moon moment
const pdKey=n=>dayKey(pdDate(n)),pdFmt=n=>{const d=pdDate(n);return d.getDate()+" "+MON_G[d.getMonth()];};
// where we are: the lunation whose parade nights are not over yet (cur: tonight's day number, daytime = between two nights)
function pdNow(){const t=pdDN(today()),h=hourNow(),cur=h<4?t-1:h>=20?t:t-.5,night=h>=20?t:h<4?t-1:null;
  let k=Math.floor((t-10962)/29.530588861)-1,D=pdD(k);while(D+1<cur){k++;D=pdD(k);}
  return{t,h,k,D,night,active:night!==null&&Math.abs(night-D)<=1,days:D-t};}
// ── marchers
const PD_V=68,PD_GAP=270,PD_X0=1960,PD_Y=992,PD_D=.38;   // image px/s, spacing, start x (off the right edge), road line under the torii, torii depth
const PD_X=["pd_bearer","pd_biwa","pd_wanyudo"],PD_H={face:190,okubi:250,peek:170,rokuro:200,bettari:300,onryo:290,pd_bearer:250,pd_biwa:280,pd_wanyudo:250},
  PD_FL=new Set(["okubi","face","peek","rokuro","obake","pd_wanyudo","vs_yosuzume","vs_kamaitachi"]),PD_INFO={};
function pdInfo(k){if(PD_INFO[k])return PD_INFO[k];const b=BESTIARY.find(x=>x[0]===k);if(!b||!b[1]||!MON[b[1]])return null;
  return PD_INFO[k]={k,id:b[1],n:b[2],h:1.15*(PD_H[k]||clamp(MON[b[1]][1]*.5,180,290)),fl:PD_FL.has(k)};}
function pdRnd(s){let h=2166136261;for(const c of s)h=Math.imul(h^c.charCodeAt(0),16777619);return()=>((h=Math.imul(h^h>>>15,2246822507)^Math.imul(h^h>>>13,3266489909))>>>0)/4294967296;}
// lantern boys lead, the biwa monk walks third, the burning wheel rolls at two thirds, a lantern boy closes
function pdBuild(L){const rnd=pdRnd(L||"pd"),ys=BESTIARY.filter(b=>b[1]&&MON[b[1]]&&!b[0].startsWith("pd_")&&ST.seen.includes(b[0])).map(b=>b[0]);
  for(let i=ys.length-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[ys[i],ys[j]]=[ys[j],ys[i]];}
  const out=["pd_bearer"],n=ys.length,bi=Math.min(2,n),wa=Math.max(bi+1,Math.round(n*.66));
  for(let i=0;i<=n;i++){if(i===bi)out.push("pd_biwa");if(i===wa||i===n&&wa>n)out.push("pd_wanyudo");if(i<n){out.push(ys[i]);if(i%3===2&&i<n-1)out.push("pd_bearer");}}
  out.push("pd_bearer");return out;}
const pdDur=seq=>(PD_X0+(seq.length-1)*PD_GAP+320)/PD_V;
const pdEl=P=>(Date.now()-P.pass.t0)/1000;
const pdX=(i,el)=>PD_X0+i*PD_GAP-PD_V*el;
const pdMask=()=>!!(S.wear&&S.wear.mask);
function pdLanternHere(){return Object.entries(S.placed||{}).some(([id,q])=>q&&q.r==="entrance"&&IT[id]&&(IT[id].c==="Фонари"||IT[id].c==="Светильники"));}
function pdDishes(){return Object.keys(S.pantry||{}).filter(id=>FOOD[id]&&FOOD[id].k==="dish"&&S.pantry[id]>0);}
// ── keep the state in step with the moon
function pdSync(){const P=pdS(),M=pdNow(),L=pdKey(M.D);
  if(P.L!==L){if(P.L){if(P.pass)pdFinish(P,true);else if(!P.saw)P.miss=P.L;}
    Object.assign(P,{L,prep:{},greet:[],pass:null,done:false,saw:false});save();}
  pdPrep(M);return M;}
function pdPrep(M){const P=pdS();if(M.days>3||P.done)return;
  if(!P.prep.lan&&pdLanternHere()){P.prep.lan=1;save();toast("🏮 Фонарь у входа: парад увидит дорогу");}
  if(!P.prep.mask&&pdMask()){P.prep.mask=1;save();toast("🎭 Муся в маске — парад её не тронет");}}
function pdOffer(){const P=pdS(),ds=pdDishes();if(P.prep.off)return;
  if(!ds.length){toast("В кладовой нет готовых блюд — свари что-нибудь");return;}
  const id=["ds_onigiri","ds_inari","ds_dango","ds_mochi"].find(x=>ds.includes(x))||ds[0];take(id);P.prep.off=id;save();chime([784,988]);
  toast("🍙 "+FOOD[id].n+" — у тории, для парада");if(panelIs("hub"))openHub();}
function pdSeen(){let nw=0;for(const k of PD_X)if(!ST.seen.includes(k)){ST.seen.push(k);nw=1;}if(nw)setTimeout(()=>toast("Новая запись в бестиарии"),3200);}
function pdStart(){const P=pdS();P.pass={t0:Date.now(),seq:pdBuild(P.L)};P.saw=true;save();pdHello();}
function pdHello(){if(S.room==="engawa"){toast("🏮 За деревьями огни — это Ночной парад");return;}
  pdSeen();if(petAway())toast("🏮 По дороге идёт Ночной парад");else if(pdMask())toast("🎭 Парад! Муся в маске смотрит на него");else toast("🙈 Парад! Без маски Муся прячется");}
function pdFinish(P,late){P.pass=null;P.done=true;
  if(P.saw&&!P.scroll){P.scroll={m:P.L.slice(0,7),g:P.greet.length,p:Object.assign({},P.prep)};if(!late){toast("📜 Парад прошёл. У тории остался свиток");chime([523,659,784]);}}save();}
// the scroll at the torii: the month's scroll + a gift for each preparation (or dango when that gift is already home)
function pdCollect(){const P=pdS(),sc=P.scroll;if(!sc)return;P.scroll=null;const mo=+sc.m.slice(5,7),id="pd_s"+String(mo).padStart(2,"0"),got=[];let dg=0;
  S.owned.add(id);loadItem(id);const pr=sc.p||{},np=[pr.lan,pr.mask,pr.off].filter(Boolean).length;
  const gift=(c,g)=>{if(!c)return;if(S.owned.has(g))dg++;else{S.owned.add(g);loadItem(g);got.push(IT[g].n);}};
  gift(pr.lan,"pd_chochin");gift(pr.mask,"pd_kasa");gift(pr.off,"pd_taiko");gift(sc.g>=5,"pd_bell");gift(np===3,"pd_wheel");
  if(dg){give("ds_dango",dg);got.push("данго ×"+dg);}
  P.got[sc.m]={g:sc.g,p:np};P.n=(P.n||0)+1;disc("parade",sc.m);save();ui();sfx("chime");
  if(!petAway()){react("😸",2.2);burst(8);S.needs.joy=clamp(S.needs.joy+10,0,100);}
  toast("📜 "+IT[id].n+" — в 🧺 Вещах");got.forEach((n,i)=>setTimeout(()=>toast("🎁 От парада: "+n),1900*(i+1)));
  setTimeout(()=>{award("pd_first");if(P.n>=3)award("pd_three");if(sc.g>=10)award("pd_bow");},1900*(got.length+1));}
const PD_SAY=["Тёмной ночи и тебе","Мы ещё вернёмся","Добрая ночь для пути","Кошке — поклон","Фонарь у тебя тёплый","До следующей луны","Мы тебя помним","Береги свою кошку","Смотри, не догоняй"];
function pdBow(k,x,y){const P=pdS(),m=pdInfo(k);floatFx.push({g:"🙇",x,y,t:now()});
  if(!m||P.greet.includes(k)){tone(660,.15,"sine",.02);return;}
  P.greet.push(k);chime([660,880]);S.needs.joy=clamp(S.needs.joy+2,0,100);save();toast("🙇 "+m.n+": «"+pick(PD_SAY)+"»");
  if(P.greet.length===5)setTimeout(()=>toast("🔔 Пятеро ответили на поклон"),2000);}
// ── drawing
const pdGlow=(r,g,b)=>{const c=document.createElement("canvas");c.width=c.height=64;const x=c.getContext("2d"),gr=x.createRadialGradient(32,32,0,32,32,32);
  gr.addColorStop(0,`rgba(${r},${g},${b},1)`);gr.addColorStop(.3,`rgba(${r},${g},${b},.42)`);gr.addColorStop(1,`rgba(${r},${g},${b},0)`);x.fillStyle=gr;x.fillRect(0,0,64,64);return c;};
const PD_WARM=pdGlow(255,186,104),PD_BLUE=pdGlow(150,196,255),PD_FIRE=pdGlow(255,112,44);
const PD_FOG=(()=>{const c=document.createElement("canvas");c.width=256;c.height=64;const x=c.getContext("2d");x.scale(4,1);const gr=x.createRadialGradient(32,32,0,32,32,32);
  gr.addColorStop(0,"rgba(176,186,190,.5)");gr.addColorStop(1,"rgba(176,186,190,0)");x.fillStyle=gr;x.fillRect(0,0,64,64);return c;})();
let PD_IM=null,pdScrollBox=null,pdWatch=0,pdBeat=0;const PD_HIT=[];
function pdLight(c,x,y,r,a){if(a<=0)return;ctx.globalAlpha=a;ctx.drawImage(c,x-r,y-r,2*r,2*r);}
function pdParade(t){const P=pdS(),el=pdEl(P),seq=P.pass.seq||[],k=BGM.k;PD_HIT.length=0;
  // mist along the road behind the feet
  ctx.save();for(let i=0;i<7;i++){const fx=((i*290+t*14)%2100)-150,[x,y]=imgToStage(fx,PD_Y-14+(i%3)*8,PD_D);ctx.globalAlpha=.32;ctx.drawImage(PD_FOG,x-260*k,y-45*k,520*k,90*k);}ctx.restore();
  const L=[];
  for(let i=seq.length-1;i>=0;i--){const x=pdX(i,el);if(x<-320||x>2120)continue;const m=pdInfo(seq[i]);if(!m)continue;
    const ph=i*1.7,bob=m.fl?Math.sin(t*1.3+ph)*16:-Math.abs(Math.sin(t*2.4+ph))*7,y=PD_Y-(m.fl?70:0)+bob,rot=m.fl?Math.sin(t*.9+ph)*.06:Math.sin(t*2.4+ph)*.03;
    const al=clamp((x+300)/320,0,1)*clamp((2100-x)/320,0,1)*.94;drawMon(m.id,x,y,m.h,PD_D,al,"b",rot);
    const [sx,sy]=imgToStage(x,y,PD_D),w=MON[m.id][0]*m.h/MON[m.id][1]*k,h=m.h*k;PD_HIT.push({k:m.k,x:sx-w/2,y:sy-h,w,h});
    if(m.k==="pd_bearer")L.push([PD_WARM,sx-w/2+w*.144,sy-h+h*.377,70*k,.8*al]);
    else if(m.k==="pd_wanyudo")L.push([PD_FIRE,sx,sy-h/2,(150+18*Math.sin(t*11+ph))*k,.55*al]);
    else L.push([i%2?PD_BLUE:PD_WARM,sx-w*.42,sy-h*.92+Math.sin(t*2+ph)*8*k,24*k,.75*al]);}
  // mist in front of the feet, then the lights
  ctx.save();for(let i=0;i<6;i++){const fx=((i*350+700-t*9)%2100)-150,[x,y]=imgToStage(fx,PD_Y+4,PD_D);ctx.globalAlpha=.26;ctx.drawImage(PD_FOG,x-240*k,y-30*k,480*k,60*k);}
  ctx.globalCompositeOperation="lighter";for(const l of L)pdLight(...l);ctx.restore();}
// seen from the veranda: a string of small lights drifting between the far trees
function pdFar(t){const P=pdS(),el=pdEl(P),seq=P.pass.seq||[],k=BGM.k;ctx.save();ctx.globalCompositeOperation="lighter";
  for(let i=0;i<seq.length;i++){const x=pdX(i,el);if(x<-200||x>2000)continue;const u=(x+200)/2200,[sx,sy]=imgToStage(80+u*1290,930+Math.sin(t*1.4+i)*4,.2),b=seq[i]==="pd_bearer";
    const a=clamp(Math.min(x+200,2000-x)/200,0,1),c=seq[i]==="pd_wanyudo"?PD_FIRE:i%2&&!b?PD_BLUE:PD_WARM;
    pdLight(c,sx,sy,(b?28:18)*k*(1+.15*Math.sin(t*6+i)),a);if(b||c===PD_FIRE)pdLight(c,sx,sy,90*k,.16*a);}
  ctx.restore();}
function pdItems(t){const P=pdS(),k=BGM.k;pdScrollBox=null;
  if(P.prep.off&&!P.done&&FOOD[P.prep.off]){const [x,y]=imgToStage(1150,1006,.7);fDraw(ctx,P.prep.off,x,y-22*k,74*k);}
  if(P.scroll&&PD_IM){const id="pd_s"+P.scroll.m.slice(5,7),r=PD_AT[id],[x,y]=imgToStage(visX(1140,110),1080,.7),w=170*k,h=w*110/230,pul=.6+.4*Math.sin(t*2.6);
    ctx.save();ctx.globalCompositeOperation="lighter";pdLight(PD_WARM,x,y-h*.4,110*k,.35*pul);ctx.restore();
    ctx.save();ctx.translate(x,y);ctx.rotate(-.06);ctx.drawImage(PD_IM,r[0],r[1],230,110,-w/2,-h,w,h);ctx.restore();pdScrollBox=[x-w/2-10,y-h-14,w+20,h+24];}}
hook("draw",(t,front)=>{if(front||scene.on)return;const P=pdS();
  if(S.room==="entrance"){pdItems(t);if(P.pass)pdParade(t);}else if(S.room==="engawa"&&P.pass)pdFar(t);});
hook("hit",(x,y)=>{if(S.room!=="entrance")return;const P=pdS(),b=pdScrollBox;
  if(P.scroll&&b&&x>b[0]&&x<b[0]+b[2]&&y>b[1]&&y<b[1]+b[3]){pdCollect();return true;}
  if(!P.pass||scene.on)return;if(!petAway()&&Math.abs(x-pet.x)<70*view.s&&y>view.floor-190*view.s)return;
  for(let i=PD_HIT.length-1;i>=0;i--){const r=PD_HIT[i];if(x>r.x&&x<r.x+r.w&&y>r.y&&y<r.y+r.h){pdBow(r.k,x,y);return true;}}});
// ── every second: the moon, the start and end of the pass, drums and bells, Musya hides or watches in her mask
hook("sec",()=>{const P=pdS(),M=pdSync(),busy=scene.on||overlaysOpen();
  if(M.days<=3&&!P.done&&P.ann!==dayKey()&&!busy){P.ann=dayKey();save();
    toast(M.active?"🏮 Ночной парад идёт — скорее ко входу":M.days>=2?"🌑 Через "+M.days+" дня новолуние и Ночной парад":M.days===1?"🌑 Завтра новолуние: парад выйдет уже ночью":M.days===0?"🌑 Новолуние: ночью по дороге пойдёт парад":"🌑 Последняя тёмная ночь: парад ещё идёт");}
  if(M.active&&!P.done&&!P.pass&&(S.room==="entrance"||S.room==="engawa")&&!busy)pdStart();
  if(!P.pass)return;const el=pdEl(P);if(el>pdDur(P.pass.seq||[])){pdFinish(P);return;}
  if(busy)return;
  if(S.room==="entrance"){
    if(pdBeat++%3===0){tone(72,.32,"triangle",.14);setTimeout(()=>tone(64,.3,"triangle",.12),330);}
    if(Math.random()<.25)tone(pick([1568,1760,2093]),.7,"sine",.018);
    if((P.pass.seq||[]).some((k,i)=>k==="pd_biwa"&&Math.abs(pdX(i,el)-900)<500)&&Math.random()<.5){tone(196,.5,"sawtooth",.02);setTimeout(()=>tone(294,.6,"sawtooth",.016),180);}
    if(!petAway()&&el>3){if(pdMask()){if(pet.action==="hide")start("idle",true);if(now()-pdWatch>14){pdWatch=now();react(pick(["👀","😺","👀"]),2);}}
      else if(pet.action==="idle")start("hide",true);}}
  else if(S.room==="engawa"&&pdBeat++%3===0)tone(60,.3,"triangle",.05);});
hook("room",id=>{const P=pdS();if(id==="entrance"&&P.pass)pdHello();});
hook("ev",e=>{if(e==="put"||e==="wear")pdPrep(pdNow());});
hook("boot",()=>{atlasImg("pd",im=>{PD_IM=im;});pdSync();});
const pdWants=()=>{const P=pdS();return !!P.scroll||pdNow().active&&!P.done;};
hook("hubDot",pdWants);
hook("tabDot",r=>r==="entrance"&&pdWants());
hook("click",key=>{if(!key.startsWith("pd:"))return;const a=key.slice(3);
  if(a==="offer")pdOffer();else if(a==="go"){closePanel();goRoom("entrance");}else if(a==="take"){closePanel();goRoom("entrance");setTimeout(pdCollect,700);}
  return true;});
hook("hub",()=>{const P=pdS(),M=pdNow(),pr=P.prep||{};let h="",b="";
  if(P.scroll){h+=`<p>📜 Парад прошёл — у тории лежит свиток.</p>`;b+=`<button class="btn primary" data-x="pd:take">📜 Забрать свиток</button>`;}
  if(M.active&&!P.done){h+=`<p><b>Этой ночью по дороге за тории идёт Ночной парад.</b> Иди ко входу и поклонись ёкаям — нажми на каждого.${P.pass?` Поклонились: ${P.greet.length}.`:""}</p>`;b+=`<button class="btn primary" data-x="pd:go">⛩ Ко входу</button>`;}
  else if(M.days<=3&&!P.done)h+=`<p>${M.days>=2?`Через ${M.days} дня — новолуние: по дороге пойдёт Ночной парад.`:M.days===1?`Завтра новолуние: по дороге пойдёт Ночной парад. Он выйдет уже этой ночью, с 20:00 до 4:00.`:M.days===0?`Сегодня новолуние: ночью, с 20:00 до 4:00, по дороге пойдёт Ночной парад.`:`Последняя тёмная ночь: парад ещё пройдёт с 20:00 до 4:00.`}</p>`;
  else if(P.done)h+=`<p>Парад этого новолуния прошёл. Следующий — ${pdFmt(pdD(M.k+1))}.</p>`;
  else h+=P.miss&&P.miss===pdKey(pdD(M.k-1))?`<p>Парад прошёл мимо… Следующий — ${pdFmt(M.D)}.</p>`:`<p>В ночь новолуния по дороге за тории идёт Ночной парад ста демонов. Следующий — ${pdFmt(M.D)}.</p>`;
  if(M.days<=3&&!P.done){const li=(ok,t)=>`<li class="${ok?"ok":""}">${ok?"☑":"☐"} ${t}</li>`;
    h+=`<ul class="qtasks">${li(pr.lan,"Повесить у входа фонарь или светильник")}${li(pr.mask,"Надеть Мусе маску — в маске она не прячется")}${li(pr.off,pr.off&&FOOD[pr.off]?"Подношение у тории: "+FOOD[pr.off].n:"Оставить у тории подношение — блюдо из кладовой")}</ul><p class="lead">За каждое приготовление парад оставит подарок.</p>`;
    if(!pr.off)b+=`<button class="btn" data-x="pd:offer">🍙 Оставить подношение</button>`;}
  const n=PD_MON.filter((m,i)=>S.owned.has("pd_s"+String(i+1).padStart(2,"0"))).length;if(n)h+=`<p class="lead">Свитков парада: ${n} из 12.</p>`;
  return`<div class="hubc"><h4>🏮 Ночной парад <i>百鬼夜行</i></h4>${h}${b?`<div class="row">${b}</div>`:""}</div>`;});
hook("album",el=>{const P=pdS(),n=P.n||0;if(!n)return;const g=Object.values(P.got||{}).reduce((a,x)=>a+(x.g||0),0);
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Ночной парад</h3><p class="lead">Парадов увидено: ${n}. Поклонов ёкаям: ${g}. Свитки и дары парада — в разделах «Свитки парада» и «Дары парада».</p>`);});
hook("away",()=>pdS().scroll?{i:"📜",t:"У тории лежит свиток Ночного парада"}:null);
X.pd={now:pdNow,st:pdS,reset(){Object.assign(pdS(),{pass:null,done:false,saw:false,scroll:null});},build:pdBuild,start:pdStart,finish:()=>pdFinish(pdS()),collect:pdCollect,offer:pdOffer,
  jump(s){const P=pdS();if(P.pass)P.pass.t0=Date.now()-s*1000;},
  focus(k,x=900){const P=pdS(),i=P.pass?P.pass.seq.indexOf(k):-1;if(i>=0)P.pass.t0=Date.now()-(PD_X0+i*PD_GAP-x)/PD_V*1000;return i;},
  tap(i=0){const r=PD_HIT.filter(r=>r.x+r.w/2>40&&r.x+r.w/2<view.W-40)[i];if(!r)return null;const b=cv.getBoundingClientRect(),x=r.x+r.w/2,y=r.y+r.h*.4;
    cv.dispatchEvent(new PointerEvent("pointerdown",{clientX:b.left+x,clientY:b.top+y,bubbles:true,pointerId:1}));return r.k;}};
}
