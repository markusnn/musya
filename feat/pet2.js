{
// ───────────────────────── «Питомец Муси»: a little bakeneko kitten that lives with her ─────────────────────────
// It turns up in a wet box at the gate, gets a name, follows Musya from room to room, sits or sleeps beside her on her
// floor line, joins her games and grows over 21 days of care (fed + played with on the same day): малыш → подросток → юный бакэнэко.
// Art: art/pet2_art.py → assets/mon/m_pt_atlas.webp (frames 280×250, facing right, floor at y=238; [x,y,tail tips]) + assets/items/atlas_pt.webp
const PT_F={"sit0":[0,0,[[92,209],[102,206]]],"walk0":[280,0,[[107,155],[116,158]]],"sleep0":[560,0,[[120,211],[124,218]]],"pounce0":[840,0,[[81,170],[84,161]]],"look0":[0,250,[[92,209],[102,206]]],"sit1":[280,250,[[63,195],[83,187]]],"walk1":[560,250,[[92,117],[114,122]]],"sleep1":[840,250,[[125,201],[135,216]]],"pounce1":[0,500,[[47,154],[55,132]]],"look1":[280,500,[[63,195],[83,187]]],"sit2":[560,500,[[47,201],[54,178]]],"walk2":[840,500,[[75,100],[102,91]]],"sleep2":[0,750,[[123,183],[141,205]]],"pounce2":[280,750,[[21,157],[28,122]]],"look2":[560,750,[[47,201],[54,178]]],"box":[840,750,[[177,125],[187,129]]]};
MON.m_pt_atlas=[1120,1000];
addItems([
 {id:"pt_bowl",n:"Миска малыша",c:"Вещи малыша",w:130,h:84,a:"b",p:20,at:["pt",0,0],src:"🐾 подарок",hint:"Появится, когда у Муси заведётся питомец"},
 {id:"pt_basket",n:"Лежанка-корзинка",c:"Вещи малыша",w:230,h:140,a:"b",p:40,at:["pt",132,0],src:"🐾 подарок",hint:"Её подарят малышу, когда он подрастёт"},
 {id:"pt_ball",n:"Плетёный мячик с бубенцом",c:"Вещи малыша",w:92,h:100,a:"b",p:25,at:["pt",364,0]}],{pt:[458,140]});
STAMPS.push(["pt_home","猫","Новый жилец","Приюти котёнка из коробки у ворот"],["pt_tails","又","Второй хвост","Вырасти котёнка до юного бакэнэко"]);
const PT_NAMES=[["Кохаку","琥珀","«янтарь» — за медовые глаза"],["Моти","餅","«рисовый колобок» — мягкий и круглый"],["Кури","栗","«каштан» — осенний найдёныш"],
 ["Юдзу","柚子","«цитрус юдзу» — маленький и солнечный"],["Суми","墨","«тушь» — полоски как мазки кисти"],["Хотару","蛍","«светлячок» — за огонёк на хвосте"]];
const PT_CH={igr:["Игривый","охотится на всё, что шевелится"],zast:["Застенчивый","держится в тени Муси"],obzh:["Обжора","всегда готов перекусить"],sonya:["Соня","засыпает где придётся"]};
const PT_ST=["Малыш","Подросток","Юный бакэнэко"],PT_H=[132,148,164],PT_D=[104,112,120];
const PT=S.ext.pet2||(S.ext.pet2={first:dayKey(),box:"",name:"",kj:"",ch:"",born:"",care:0,cd:"",fed:"",played:"",st:0});
document.head.insertAdjacentHTML("beforeend",`<style>
.pt-card{display:flex;gap:12px;align-items:center}.pt-pic{flex:none;background-image:url(assets/mon/m_pt_atlas.webp);background-repeat:no-repeat}
.pt-card p{margin:2px 0!important}.pt-card b{color:var(--sakura)}.pt-how{color:var(--muted);font-size:12.5px!important}
.pt-bar{height:4px;border-radius:2px;background:rgba(216,210,195,.1);overflow:hidden;margin:5px 0}.pt-bar i{display:block;height:100%;background:linear-gradient(90deg,#6fa8d8,#bfe3ff)}
.pt-names{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}
.pt-nm{display:flex;flex-direction:column;align-items:flex-start;gap:2px;text-align:left;padding:10px 12px;border-radius:12px;border:1px solid rgba(216,210,195,.18);background:rgba(216,210,195,.05);color:var(--paper);font:inherit;cursor:pointer}
.pt-nm b{font-size:17px}.pt-nm i{font-style:normal;color:var(--sakura);font-family:var(--display);font-size:15px}.pt-nm span{font-size:12px;color:var(--muted);line-height:1.35}
.pt-row{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0 12px}.pt-row span{display:inline-block;border-radius:10px;background-color:rgba(216,210,195,.05)}.pt-row .off{filter:brightness(0) opacity(.35)}
</style>`);
const ptBg=(k,h)=>{const r=PT_F[k],q=h/250;return`width:${(280*q).toFixed(0)}px;height:${h}px;background-size:${(1120*q).toFixed(1)}px ${(1000*q).toFixed(1)}px;background-position:${(-r[0]*q).toFixed(1)}px ${(-r[1]*q).toFixed(1)}px`;};
const ptStage=()=>PT.care>=14?2:PT.care>=7?1:0;
const ptDays=(a,b)=>Math.round((new Date(b)-new Date(a))/864e5);
const ptHungry=()=>!!PT.name&&PT.fed!==dayKey();

// ── sprite: one frame of the atlas, dimmed to the room's light; the fox-fire at the tail is its own light ──
const ptCv=document.createElement("canvas");ptCv.width=280;ptCv.height=250;const ptG=ptCv.getContext("2d");
function ptSprite(key,x,y,h,flip,t,al=1,sq=1,rot=0){const im=MIMG.m_pt_atlas,r=PT_F[key];if(!im||!r||al<=0)return null;
  const g=ptG;g.globalCompositeOperation="source-over";g.globalAlpha=1;g.clearRect(0,0,280,250);g.drawImage(im,r[0],r[1],280,250,0,0,280,250);
  g.globalCompositeOperation="source-atop";g.fillStyle=S.room==="bedroom"&&S.lampOff?"rgba(8,10,20,.62)":TINT[S.room]||"rgba(14,18,18,.28)";g.fillRect(0,0,280,250);g.globalCompositeOperation="source-over";
  const k=h/250,f=flip?-1:1;ctx.save();ctx.globalAlpha=al*.3;ctx.fillStyle="#000";ctx.beginPath();ctx.ellipse(x,y+2*k,(key.startsWith("sleep")?92:62)*k,9*k,0,0,7);ctx.fill();
  ctx.globalAlpha=al;ctx.translate(x,y);if(rot)ctx.rotate(rot);ctx.scale(f,sq);ctx.drawImage(ptCv,-140*k,-238*k,280*k,h);ctx.restore();
  const night=dayTint()[1],lit=S.room==="bedroom"&&S.lampOff;ctx.save();ctx.globalCompositeOperation="lighter";
  r[2].forEach(([tx,ty],i)=>{const gx=x+f*(tx-140)*k,gy=y+(ty-238)*k*sq,R=(16+4*Math.sin(t*2.3+i*2))*k*(night||lit?1.25:.9),a=(.28+.14*Math.sin(t*3.1+i*1.7))*(night||lit?1:.6)*al;
    const gr=ctx.createRadialGradient(gx,gy,0,gx,gy,R);gr.addColorStop(0,`rgba(150,205,255,${a})`);gr.addColorStop(1,"rgba(150,205,255,0)");ctx.fillStyle=gr;ctx.fillRect(gx-R,gy-R,2*R,2*R);});
  ctx.restore();const w=280*k;return[x-w*.3,y-h*.72,x+w*.3,y+6*k];}

// ── the kitten's life: it follows Musya and mirrors what she does ──
const pk={x:null,side:1,mode:"sit",t0:0,next:0,hop:null,face:-1,eat:0,food:"",ph:0,box:null,boxHit:null,react:0,wander:0,wUntil:0,seen:0};
const ptOn=()=>!!PT.name&&!scene.on;
const ptFloor=()=>{const [ox,oy]=camOff(CAT_D);return[ox,view.floor+oy];};
function ptTarget(){const s=view.s,g=ptStage(),D=(PT_D[g]+(PT.ch==="zast"?16:0)-(pet.action==="sleep"?10:0))*s,lo=40*s,hi=view.W-40*s;
  let tx=pet.x+pk.side*D;if(tx<lo||tx>hi){pk.side=-pk.side;tx=pet.x+pk.side*D;}if(now()<pk.wUntil)tx+=pk.wander*s;return clamp(tx,lo,hi);}
function ptSet(m,t){if(pk.mode!==m){pk.mode=m;pk.t0=t;}}
function ptTick(t,dt){
  if(!ptOn()||petAway())return;const s=view.s,a=pet.action;if(pk.x==null)pk.x=pet.x+pk.side*PT_D[ptStage()]*s;
  const tx=ptTarget(),dx=tx-pk.x,far=Math.abs(dx),play=["yarn","butterfly","petals","firefly","zoomies","cursor"].includes(a);
  if(pk.hop&&t-pk.hop.t0>pk.hop.d)pk.hop=null;
  if(pk.eat>t){ptSet("eat",t);pk.face=pk.x<pet.x?1:-1;return;}
  if(pk.mode==="sleep"&&a!=="sleep"&&!play&&t-pk.t0<(PT.ch==="sonya"?40:20))return;   // a nap of its own: it does not get up just because she moved
  const walkSp=(play||a==="zoomies"?260:a==="walkto"?200:150)*s;
  if(far>(pk.mode==="walk"?4*s:play?60*s:a==="sleep"?16*s:46*s)){   // trot after her with little hops
    ptSet("walk",t);const st=Math.sign(dx)*Math.min(far,walkSp*dt);pk.x+=st;pk.ph+=Math.abs(st)/(22*s);pk.face=Math.sign(dx)||pk.face;return;}
  pk.face=pk.x<pet.x?1:-1;   // settled: look towards her
  if(a==="sleep"){ptSet("sleep",t);return;}
  if(play){if(pk.mode!=="play")ptSet("play",t);if(!pk.hop&&Math.random()<dt*.9)pk.hop={t0:t,d:.55,h:(18+Math.random()*16)*s};return;}
  if(pk.mode==="bfly"&&!pk.hop&&Math.random()<dt*.7)pk.hop={t0:t,d:.5,h:(14+Math.random()*14)*s};
  if(pk.mode==="walk"||pk.mode==="play"||pk.mode==="eat"||pk.mode==="sleep"&&a!=="sleep"&&t-pk.t0>(PT.ch==="sonya"?40:20)){ptSet("sit",t);pk.next=t+rand(4,9);}
  if((pk.mode==="look"||pk.mode==="bfly")&&t-pk.t0>(pk.mode==="bfly"?7:2.6)){ptSet("sit",t);pk.next=t+rand(5,10);}
  if(pk.mode==="sit"&&t>pk.next&&!drag.active){const C=PT.ch,r=Math.random(),w={igr:[.25,.5,.75],zast:[.45,.55,.72],obzh:[.5,.62,.78],sonya:[.3,.4,.5]}[C]||[.35,.5,.7];
    if(r<w[0])ptSet("look",t);else if(r<w[1]){ptSet("bfly",t);}else if(r<w[2]){pk.wander=(Math.random()<.5?-1:1)*rand(50,80);pk.wUntil=t+rand(5,9);}
    else if(r<.9&&Math.random()<(C==="sonya"?.9:S.placed&&S.placed.pt_basket&&S.placed.pt_basket.r===S.room?.7:.35)){ptSet("sleep",t);}else{pk.side=-pk.side;}   // or slips behind her to her other side
    pk.next=t+rand(6,14);}
  if(t>pk.react&&a==="idle"&&pk.mode!=="walk"&&!drag.active){pk.react=t+rand(45,100);if(pk.seen)react(pick(["😸","😽","💗"]),1.6);pk.seen=1;}
}
// Musya is travelling: the kitten waits at the gate, a little sad
function ptWaitDraw(t){if(S.room!=="entrance")return;const [x,y]=imgToStage(visX(1150,80),catLineY(),CAT_D),g=ptStage(),h=PT_H[g]*view.s;
  pk.box=ptSprite(Math.floor(t/9)%3===2?"look"+g:"sit"+g,x,y,h,true,t,1,.97+.01*Math.sin(t*1.4));
  const u=(t%6)/6;if(u<.5)drawEmoji(ctx,u<.25?"…":"💭",x-24*view.s,y-h*.8-u*30*view.s,13*view.s,Math.sin(u*2*Math.PI));}
// its own basket: when the kitten naps on its own and the basket stands in this room, it curls up there
const PT_BODY=[89,113,127];
function ptBasket(){const q=S.placed&&S.placed.pt_basket;if(!q||q.r!==S.room)return null;const it=roomThings().find(i=>i.id==="pt_basket");if(!it)return null;
  const p=ipos(it),sc=p.sc||1,m=DMETA.pt_basket;curD=CAT_D;curRow=p.y;const [x0]=imgToStage(p.x-m[0]*sc/2,p.y),[x1,y]=imgToStage(p.x+m[0]*sc/2,p.y-m[1]*.37*sc);curRow=null;
  return{x:(x0+x1)/2,y,bw:x1-x0,front:p.y>catLineY()+6};}
function ptBasketDraw(t,b){const g=ptStage(),h=150*b.bw/PT_BODY[g],e=t-pk.t0;pk.x=b.x-camOff(CAT_D)[0];
  pk.box=ptSprite("sleep"+g,b.x,b.y,h,pk.face<0,t,clamp(e/.8,0,1),1+.025*Math.sin(t*1.7));ptZ(t,b.x+pk.face*h*.08,b.y-h*.4,view.s*.9);}
function ptZ(t,x,y,s){for(let i=0;i<2;i++){const u=((t+i*.9)%1.8)/1.8;ctx.save();ctx.globalAlpha=Math.sin(u*Math.PI)*.85;ctx.font=`800 ${(8+5*u)*s}px ${getComputedStyle(document.body).fontFamily}`;ctx.fillStyle="#aeb8d8";ctx.textAlign="center";
    ctx.fillText("z",x+u*10*s,y-u*26*s);ctx.restore();}}
function ptDraw(t,front){
  if(!front)pk.box=null;
  if(!PT.name){if(front&&PT.box&&S.room==="entrance")ptBoxDraw(t);return;}
  if(scene.on)return;if(petAway()){if(!front)ptWaitDraw(t);return;}if(pk.x==null)return;
  const bk=pk.mode==="sleep"&&pet.action!=="sleep"?ptBasket():null;if(bk){if(front===bk.front)ptBasketDraw(t,bk);return;}if(front)return;
  const s=view.s,g=ptStage(),h=(PT_H[g]+(PT.care>=21?8:0))*s,[ox,fy]=ptFloor(),x=pk.x+ox,m=pk.mode,e=t-pk.t0;let k="sit"+g,y=fy,sq=1,rot=0;
  if(m==="walk"){k="walk"+g;y-=Math.abs(Math.sin(pk.ph*1.6))*7*s;rot=Math.sin(pk.ph*1.6)*.04;}
  else if(m==="sleep"){k="sleep"+g;sq=1+.025*Math.sin(t*1.7);}
  else if(m==="look")k="look"+g;
  else if(m==="eat"){k="pounce"+g;sq=1-.03*Math.abs(Math.sin(t*5));}
  else if(m==="play")k=pk.hop?"walk"+g:Math.floor(e*1.3)%3===2?"look"+g:"pounce"+g;
  else if(m==="bfly")k=e%2.4<1.4?"look"+g:"pounce"+g;
  else if(m==="sit")sq=1+.012*Math.sin(t*2.2);
  if(pk.hop){const u=clamp((t-pk.hop.t0)/pk.hop.d,0,1);y-=Math.sin(u*Math.PI)*pk.hop.h;if(m!=="play")k="walk"+g;}
  if(m==="eat")ptBowl(x+pk.face*58*h/250,fy,h/250,t);
  pk.box=ptSprite(k,x,y,h,pk.face<0,t,1,sq,rot*pk.face);
  if(m==="look"&&ptHungry()&&e>.6)drawEmoji(ctx,"🐟",x+pk.face*22*s,y-h*.78-4*s*Math.sin(t*2),12*s,clamp((e-.6)/.4,0,1)*.9);
  if(m==="sleep")ptZ(t,x+pk.face*20*s,fy-h*.4,s);
  if(m==="bfly"){const u=e,bx=x+pk.face*(30+16*Math.sin(u*1.3))*s,by=fy-h*.62-14*Math.sin(u*.9)*s,ww=3+3*(Math.sin(u*18)+1)/2,op=clamp(Math.min(u/.5,(7-u)/.6),0,1);
    ctx.save();ctx.globalAlpha=op;ctx.fillStyle="#cfe6f0";for(const sd of[-1,1]){ctx.beginPath();ctx.ellipse(bx+sd*ww*.6*s,by-2*s,ww*.7*s,4*s,sd*.4,0,7);ctx.fill();}ctx.restore();}
}
function ptBowl(x,y,k,t){ctx.save();ctx.fillStyle="rgba(0,0,0,.3)";ctx.beginPath();ctx.ellipse(x,y+2*k,40*k,7*k,0,0,7);ctx.fill();
  ctx.fillStyle="#2c4670";ctx.beginPath();ctx.ellipse(x,y-12*k,38*k,16*k,0,0,Math.PI);ctx.fill();ctx.fillRect(x-38*k,y-20*k,76*k,8*k);
  ctx.fillStyle=pk.food==="milk"?"#e8e4da":"#d9cdb8";ctx.beginPath();ctx.ellipse(x,y-20*k,34*k,8*k,0,0,7);ctx.fill();
  if(pk.food!=="milk"){ctx.fillStyle="#d98a5a";ctx.beginPath();ctx.ellipse(x-4*k,y-21*k,16*k,4.5*k,0,0,7);ctx.fill();ctx.beginPath();ctx.moveTo(x+12*k,y-21*k);ctx.lineTo(x+20*k,y-26*k);ctx.lineTo(x+20*k,y-16*k);ctx.fill();}
  ctx.restore();}
// the wet box at the gate, before the kitten has a name
function ptBoxDraw(t){const ix=visX(1240,110),[x,y]=imgToStage(ix,catLineY()+40,CAT_D),h=340*BGM.k,sh=Math.sin(t*38)*.012*(Math.sin(t*1.3)>.2?1:0);
  pk.boxHit=ptSprite("box",x,y,h,false,t,1,1,sh);}
function ptTap(){const t=now(),s=view.s,b=pk.box,cx=(b[0]+b[2])/2,cy=b[1]+12*s,d=dayKey();
  if(petAway()){pk.box&&floatFx.push({g:"💭",x:cx,y:cy,t});toast(`${PT.name} ждёт Мусю у ворот`);return;}
  if(pk.mode==="sleep"&&pet.action==="sleep"){floatFx.push({g:"💤",x:cx,y:cy,t});tone(220,.2,"sine",.03);return;}
  if(PT.ch==="zast"&&Math.random()<.35){pk.side=-pk.side;floatFx.push({g:"💦",x:cx,y:cy,t});}
  ptSet(pk.mode==="play"?"play":"sit",t);pk.hop={t0:t,d:.6,h:(26+ptStage()*4)*s};pk.next=t+rand(5,9);
  floatFx.push({g:"♪",x:cx-10*s,y:cy,t},{g:"💗",x:cx+12*s,y:cy-8*s,t:t+.25});chime([1046,1318,1568]);
  S.needs.joy=clamp(S.needs.joy+2,0,100);if(PT.played!==d){PT.played=d;ptCare();save();}
  if(Math.random()<.4&&pet.action==="idle"&&!petAway())setTimeout(()=>react("😸",1.6),500);}
function ptCare(){const d=dayKey();if(PT.fed!==d||PT.played!==d||PT.cd===d)return;PT.cd=d;PT.care++;save();hubDot();
  const g=ptStage();if(g>PT.st){PT.st=g;ptGrow(g);}else if(PT.care===21){disc("pet","pt4");toast(`🐾 ${PT.name} совсем вырос!`);chime([784,988,1318,1568]);}
  else toast(`🐾 День заботы: ${Math.min(PT.care,21)} из 21`);}
function ptGrow(g){disc("pet","pt"+(g+1));chime([660,880,1320]);if(!petAway())burst(8);
  if(g===1){S.owned.add("pt_basket");toast(`🐾 ${PT.name} подрос! Ему подарили корзинку`);}
  if(g===2){award("pt_tails");setTimeout(()=>toast(`🔥 У ${PT.name} раздвоился хвост!`),2600);}save();}
function ptFeed(){const d=dayKey();if(!PT.name)return;
  if(PT.fed===d){toast(PT.ch==="obzh"?`${PT.name} просит ещё, но хватит до завтра`:`${PT.name} уже сыт — до завтра`);return;}
  const fish=EATFISH.find(f=>S.pantry[f]>0);pk.food=fish?take(fish):"milk";pk.eat=now()+6.5;PT.fed=d;
  toast(fish?`🐟 ${PT.name} уплетает рыбку: ${FOOD[fish].n}`:`🥛 ${PT.name} лакает молоко`);setTimeout(()=>sfx("eat"),500);
  if(PT.ch==="obzh"&&!petAway())setTimeout(()=>react("😹",1.6),2200);ptCare();save();ui();hubDot();}
function ptFound(){dlg({head:"📦 Мокрая коробка у ворот",text:"В размокшей коробке дрожит крошечный котёнок. Хвостик короткий и раздвоен на кончике, а на нём теплится голубой огонёк. Возьмём его домой?",
  img:`<span style="display:inline-block;${ptBg("box",70)}" class="pt-pic"></span>`,ok:"Взять домой",no:"Позже",onOk:ptNames});}
function ptNames(){openPanel("Как назовём малыша?",`<div style="text-align:center"><span class="pt-pic" style="display:inline-block;${ptBg("look0",130)}"></span></div><p class="lead">Котёнок смотрит на тебя янтарными глазами и ждёт. Выбери ему имя:</p>
  <div class="pt-names">${PT_NAMES.map((n,i)=>`<button class="pt-nm" data-x="pt:name:${i}"><b>${n[0]}</b><i>${n[1]}</i><span>${n[2]}</span></button>`).join("")}</div>`,"pt_name");}
function ptAdopt(i){const n=PT_NAMES[i];if(!n||PT.name)return;PT.name=n[0];PT.kj=n[1];PT.ch=pick(Object.keys(PT_CH));PT.born=dayKey();PT.box="";PT.st=0;
  disc("pet","pt1");S.owned.add("pt_bowl");award("pt_home");save();closePanel();
  if(S.room==="entrance"&&pk.boxHit)pk.x=(pk.boxHit[0]+pk.boxHit[2])/2-camOff(CAT_D)[0];pk.side=1;ptSet("walk",now());
  toast(`🐾 ${n[0]} теперь живёт с Мусей`);chime([784,988,1175,1568]);if(!petAway())setTimeout(()=>{react("😻",2);burst(10);},700);ui();hubDot();buildTabs();}

// ── hooks ──
let ptBoot=0;
hook("boot",()=>{ptBoot=now();});
hook("sec",()=>{if(PT.name||PT.box||now()-ptBoot<40||scene.on||overlaysOpen())return;const h=hourNow(),old=(S.ext.trust&&S.ext.trust.days>=2)||ST.got.length>=8;
  if(old||ptDays(PT.first,dayKey())>=2||weather.on&&(h>=17||h<5)){PT.box=dayKey();save();toast("📦 У ворот кто-то тихо мяукает…");hubDot();}});
hook("tick",ptTick);
hook("draw",ptDraw);
hook("hit",(x,y)=>{const inB=b=>b&&x>b[0]&&x<b[2]&&y>b[1]&&y<b[3];
  if(!PT.name&&PT.box&&S.room==="entrance"&&inB(pk.boxHit)){sfx("pop");ptFound();return true;}
  if(PT.name&&!scene.on&&inB(pk.box)){if(!petAway()){const [cx,cy]=stageToCell(x,y);if(cx>50&&cx<142&&cy>10&&cy<200)return false;}ptTap();return true;}});
hook("room",()=>{if(!PT.name)return;const s=view.s;pk.x=pk.side<0?-50*s:view.W+50*s;pk.hop=null;pk.eat=0;ptSet("walk",now());});
hook("click",(k)=>{if(!k.startsWith("pt:"))return;const [,a,v]=k.split(":");
  if(a==="feed"){closePanel();ptFeed();}else if(a==="gate"){closePanel();goRoom("entrance");}else if(a==="name")ptAdopt(+v);return true;});
hook("tray",(tray,room)=>{if(!PT.name||(S.trayMode[room]||"play")!=="play"||room!=="kitchen"&&!ptHungry())return;const row=tray.querySelector(".items");if(!row)return;
  row.insertAdjacentHTML("afterbegin",`<button class="item wide" data-x="pt:feed"><span class="ico">🍼</span><span class="nm">${ptStage()?"Покормить: "+PT.name:"Покормить малыша"}</span></button>`);});
hook("itemTap",(it,I)=>{if(I&&I.id==="pt_ball"&&ptOn()&&!petAway()){const t=now();ptSet("bfly",t);pk.hop={t0:t,d:.6,h:30*view.s};fxAt(it,["🔔","♪"],3);tone(1760,.2,"sine",.04);
  const d=dayKey();if(PT.played!==d){PT.played=d;ptCare();save();}return true;}});
hook("hubDot",()=>!PT.name&&!!PT.box||ptHungry());
hook("tabDot",r=>r==="entrance"&&!PT.name&&!!PT.box);
hook("away",ms=>PT.name&&ms>8*36e5?{i:"🐾",t:`${PT.name} скучал и ждал тебя у ворот`}:null);
hook("hub",()=>{
  if(!PT.name)return PT.box?`<div class="hubc"><h4>📦 Коробка у ворот <i>門</i></h4><p>У ворот кто-то тихо мяукает…</p><div class="row"><button class="btn primary" data-x="pt:gate">⛩ Посмотреть</button></div></div>`:"";
  const g=ptStage(),d=dayKey(),fed=PT.fed===d,pl=PT.played===d,c=Math.min(PT.care,21),C=PT_CH[PT.ch]||PT_CH.igr;
  return`<div class="hubc"><h4>🐾 ${PT.name} <i>${PT.kj}</i></h4><div class="pt-card"><span class="pt-pic" style="${ptBg("sit"+g,96)}"></span><div>
   <p><b>${PT.care>=21?"Бакэнэко":PT_ST[g]}</b> · ${C[0]}: ${C[1]}</p><p>Растёт: ${c}/21 дней заботы</p><div class="pt-bar"><i style="width:${Math.max(3,c/21*100).toFixed(0)}%"></i></div>
   <p>Сегодня: ${fed?"🍼 накормлен ✓":"🍼 ещё не ел"} · ${pl?"🎾 поиграли ✓":"🎾 не играли"}</p></div></div>
   <p class="pt-how">День заботы — когда малыша покормили (🍼 в лотке) и с ним поиграли (нажми на него). ${g<2?`Через ${(g?14:7)-PT.care} дн. он ${g?"станет бакэнэко":"подрастёт"}.`:PT.care<21?"Второй хвост уже вырос!":"Вырос — и остался с Мусей."}</p>
   ${fed?"":`<div class="row"><button class="btn primary" data-x="pt:feed">🍼 Покормить</button></div>`}</div>`;});
hook("album",el=>{if(!PT.name)return;const g=ptStage();el.insertAdjacentHTML("beforeend",`<h3 class="bh">Питомец Муси</h3><p class="lead">${PT.name} растёт: ${Math.min(PT.care,21)} из 21 дня заботы.</p>
  <div class="pt-row">${[0,1,2].map(i=>`<span class="pt-pic${i>g?" off":""}" style="${ptBg("sit"+i,90)}" title="${PT_ST[i]}"></span>`).join("")}</div>`);});
X.pt={st:PT,pk,feed:ptFeed,adopt:ptAdopt,found:ptFound,tap:ptTap,
  box(){PT.box=dayKey();save();},arm(){ptBoot=-999;},care(n){PT.care=n;PT.st=ptStage();},
  nap(){ptSet("sleep",now());},boxXY(){const b=pk.boxHit;return b?[(b[0]+b[2])/2,(b[1]+b[3])/2]:null;},kitXY(){const b=pk.box;return b?[(b[0]+b[2])/2,(b[1]+b[3])/2]:null;}};
}
