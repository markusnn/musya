{
// ───────────────────────── «Лавка тануки» (prefix tn): a night barter cart at the fair ─────────────────────────
// Open 17:00–03:00: the tanuki stands behind the counter; by day the cart is shut («Закрыто — тануки спит до вечера»).
// Stock: every night (key = the evening's dayKey) 4–6 offers — rare painted things «Лавка тануки», sometimes rare pantry food,
// and the weekly rarity. No coins: the tanuki takes only what the player has in excess — gachapon duplicates (one of each stays),
// workshop materials, pantry surplus (more than 2 of a kind), Musya's repeat finds. Prices are fitted to what the player has.
// State: S.ext.shop = {day, stock:[{k:"it"|"fd",id,n,w,p:[[kind,arg,n]…]}], sold:[i], n, seen, line, wk:{k,id,p}, used:{findId:n}}
// Art: art/shop_art.py → assets/items/tn_stall.webp (cart: back / open front / closed front) + assets/items/atlas_tn.webp (12 things).
const TN_ST={back:[0,0,440,470],open:[442,0,440,470],closed:[884,0,440,470]};
const TN_R={tn_shigaraki:[304,0,160,210,"b"],tn_bunbuku:[466,0,200,210,"b"],tn_kabocha:[212,232,150,140,"b"],tn_happa:[0,232,210,150,"t"],tn_suzu:[668,0,110,210,"t"],tn_tsuki:[0,0,180,230,"t"],
  tn_koban:[364,232,180,140,"b"],tn_hyotan:[780,0,110,200,"b"],tn_uchiwa:[892,0,140,200,"b"],tn_kaki:[182,0,120,230,"t"],tn_netsuke:[546,232,130,110,"b"],tn_chou:[1034,0,160,160,"b"]};
// [id, name, short name for status lines, a line about it, weekly rarity]
const TN_I=[
 ["tn_shigaraki","Тануки из Сигараки","тануки из Сигараки","Глиняный тануки в шляпе, с бутылочкой сакэ и долговой книжкой. Такие стоят у входа в лавки и зазывают удачу.",0],
 ["tn_bunbuku","Бумбуку-канатоходец","бумбуку-канатоходец","Из сказки о храме Мориндзи: чайник-тануки ходил по канату с веером, и на него сбегался смотреть весь город.",1],
 ["tn_kabocha","Фонарь из тыквы","фонарь из тыквы","Тануки уверяет, что вырезал его сам. Светит изнутри тёплым рыжим светом.",0],
 ["tn_happa","Листья-превращалки","листья-превращалки","Тануки кладёт лист на голову — и превращается во что пожелает. Эти пока отдыхают на нитке.",0],
 ["tn_suzu","Колокольчик удачи","колокольчик удачи","Звякнет — и беда пройдёт стороной. Так говорит тануки, а он врать не станет. Почти.",0],
 ["tn_tsuki","Луна Сёдзёдзи","луна Сёдзёдзи","В саду храма Сёдзёдзи тануки в полнолуние били в животы, как в барабаны, и пели до утра.",1],
 ["tn_koban","Монетки из листьев","монетки из листьев","Золотые кобаны тануки. К утру они снова станут листьями — зато как блестят!",1],
 ["tn_hyotan","Тыква-горлянка","горлянка","Для сакэ, для воды и для удачи: старая горлянка с красным шнуром.",0],
 ["tn_uchiwa","Веер-утива с тануки","веер","Круглый веер: тануки под луной бьёт в барабан-живот.",0],
 ["tn_kaki","Связка сушёной хурмы","сушёная хурма","Хосигаки всю осень сушат под стрехой. Тануки отрывал от сердца — и от живота.",0],
 ["tn_netsuke","Нэцкэ «Спящий тануки»","нэцкэ","Резная фигурка-противовес для пояса. Тануки спит, обернувшись хвостом.",0],
 ["tn_chou","Долговая книжка тануки","долговая книжка","Каёйтё: сюда тануки записывает, кто ему должен. Тебя там нет. Пока.",0]];
const TN_IT={};for(const r of TN_I)TN_IT[r[0]]=r;
const TN_CAT="Лавка тануки",TN_RARE=TN_I.filter(r=>r[4]).map(r=>r[0]),TN_COMMON=TN_I.filter(r=>!r[4]).map(r=>r[0]);
addItems(TN_I.map(([id,n])=>{const a=TN_R[id],it={id,n,c:TN_CAT,w:a[2],h:a[3],a:a[4],p:90,at:["tn",a[0],a[1]],src:"🍃 лавка тануки",hint:"Это меняет тануки в своей лавке на ярмарке — по вечерам, с 17:00"};
  if(id==="tn_kabocha")it.glow=[75,88];if(id==="tn_tsuki")it.glow=[90,124];return it;}),{tn:[1220,382]});
STAMPS.push(["tn_first","狸","Первая сделка","Обменяйся с тануки в его лавке на ярмарке"],["tn_ten","商","Завсегдатай лавки","Сделай десять обменов в лавке тануки"],["tn_rare","珍","Редкость недели","Выменяй у тануки редкость недели"]);

// rare pantry things he sometimes brings: [id, how many]
const TN_P=[["v_obaketake",2],["u_unagi",1],["u_obakeuo",1],["u_namazu",1],["v_ichigo",3]];
// what he takes: workshop materials (same keys as feat/workshop.js) and his favourite food
const TN_MAT={wara:["Солома","🌾"],ha:["Листья","🍁"],uroko:["Чешуя","🐟"],kai:["Ракушки","🐚"],eda:["Веточки","🌿"],koke:["Мох","🌱"],donguri:["Жёлуди","🌰"],hane:["Перья","🪶"],tsuchi:["Глина","🟤"],nuno:["Ткань","🧵"]};
const TN_FAV=["ds_yakiimo","ds_dango","ds_takoyaki","v_kabocha","v_imo"];
const TN_LINES=["Пом-пом! Тебе обновка, мне — лишнее. Честная сделка… почти.","Ох, какие славные лишние вещички! Тануки знает, куда их пристроить.",
 "Бери, бери. А я это превращу во что-нибудь полезное. Или съем.","Сделка! Только никому не говори, за сколько я отдал. Разоришь старика!",
 "Хо-хо, глаз у тебя намётанный. Эту вещицу я берёг для особого покупателя.","По рукам! То есть по лапам. Завтра вечером притащу ещё диковинок.",
 "Мне — добро, тебе — диво. Тануки всегда в выигрыше, хе-хе.","Смотри, чтобы к утру обратно в лист не превратилась! Шучу. Наверное.",
 "Хорошо торгуешься. Почти как лиса. Но лисе я бы ни за что не уступил!","Пом! Живот доволен, лавка довольна. Заходи ещё вечерком."];
const TN_HI=["Заходи, заходи! Монеты мне ни к чему — у тебя ведь наверняка завалялось что-нибудь лишнее?",
 "Хо! Покупатель! Меняю диковинки на повторы, обрезки и лишнюю еду. Монеты не беру — от них живот не растёт.",
 "Не стесняйся. Всё по-честному: ты мне лишнее, я тебе редкое. Ну, почти по-честному."];

const tnS=()=>{const s=S.ext.shop||(S.ext.shop={day:"",stock:[],sold:[],n:0,seen:"",line:"",wk:null,used:{}});s.used=s.used||{};s.sold=s.sold||[];return s;};
const tnH=()=>hourNow(),tnOpen=()=>{const h=tnH();return h>=17||h<3;};
const tnDay=()=>tnH()<3?dayKey(new Date(today().getTime()-864e5)):dayKey();                      // one night = one stock (17:00 → 03:00)
const tnWeek=()=>{const [y,m,d]=tnDay().split("-").map(Number);return Math.floor((Date.UTC(y,m-1,d)-Date.UTC(2024,0,1))/864e5/7);};   // 2024-01-01 is a Monday
function tnRng(seed){let a=2166136261;for(const c of String(seed))a=Math.imul(a^c.charCodeAt(0),16777619);   // FNV-1a seed → mulberry32
  return()=>{a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}

// ── what the player has in excess (never the only copy of anything, never a placed thing) ──
const tnGot=()=>(S.ext.gacha&&S.ext.gacha.got)||{};
const tnSur=k=>Object.keys(FOOD).filter(id=>FOOD[id].k===k&&id!=="u_any"&&(k!=="fish"||EATFISH.includes(id))).reduce((a,id)=>a+Math.max(0,(S.pantry[id]||0)-2),0);
const tnFinds=()=>{const c=(S.ext.ret&&S.ext.ret.cnt)||{},u=tnS().used,o={};for(const id in c){const n=Math.max(0,(c[id]||0)-1-(u[id]||0));if(n)o[id]=n;}return o;};
function tnHave([k,a]){
  if(k==="dup"){let n=0;const g=tnGot();for(const id in g)n+=Math.max(0,g[id]-1);return n;}
  if(k==="mat")return Math.max(0,(S.ext.craft&&S.ext.craft.mat&&S.ext.craft.mat[a])||0);
  if(k==="dish"||k==="fish"||k==="veg")return tnSur(k);
  if(k==="food")return Math.max(0,(S.pantry[a]||0)-2);
  if(k==="find")return Object.values(tnFinds()).reduce((x,y)=>x+y,0);return 0;}
function tnLabel([k,a,n]){const L={dup:"🎎 Повторные фигурки гатяпона",dish:"🍱 Лишние блюда",fish:"🐟 Лишняя рыба",veg:"🥕 Лишние овощи",find:"🐾 Повторные находки Муси"};
  return(k==="mat"?TN_MAT[a][1]+" "+TN_MAT[a][0]:k==="food"?"😋 "+FOOD[a].n:L[k])+" ×"+n;}
function tnTake([k,a,n]){
  const most=(ids,cnt,min)=>ids.filter(id=>cnt(id)>min).sort((x,y)=>cnt(y)-cnt(x))[0];
  for(let i=0;i<n;i++){
    if(k==="dup"){const g=tnGot(),id=most(Object.keys(g),id=>g[id],1);if(id)g[id]--;}
    else if(k==="mat")S.ext.craft.mat[a]=Math.max(0,(S.ext.craft.mat[a]||0)-1);
    else if(k==="dish"||k==="fish"||k==="veg"){const id=most(Object.keys(S.pantry).filter(id=>FOOD[id]&&FOOD[id].k===k&&(k!=="fish"||EATFISH.includes(id))),id=>S.pantry[id]||0,2);if(id)take(id);}
    else if(k==="food"){if((S.pantry[a]||0)>2)take(a);}
    else if(k==="find"){const f=tnFinds(),id=Object.keys(f).sort((x,y)=>f[y]-f[x])[0];if(id){const u=tnS().used;u[id]=(u[id]||0)+1;}}}}

// ── the price: 1–2 things he wants, leaning toward what the player actually has (fixed for the whole night) ──
function tnPrice(r,tier){const big=tier===2,cand=[];
  const add=(k,a,n,w)=>{const h=tnHave([k,a]);cand.push({c:[k,a,n],w:w*(h>=n?5:h>0?2:1)});};
  add("dup",null,big?2+(r()*2|0):1+(r()*2|0),3);
  for(const m in TN_MAT)add("mat",m,big?5+(r()*3|0):tier?3+(r()*3|0):2+(r()*2|0),1);
  add("dish",null,big?2:1,2);add("fish",null,big?2+(r()*2|0):1+(r()<.4?1:0),2);add("veg",null,big?3+(r()*2|0):2+(r()<.5?1:0),2);
  for(const f of TN_FAV)add("food",f,1,.5);
  if(S.ext.ret)add("find",null,big?2:1,1.6);
  const out=[],nc=big?2:tier&&r()<.35?2:1;
  for(let j=0;j<nc;j++){const pool=cand.filter(c=>!out.some(o=>o[0]===c.c[0])),tot=pool.reduce((a,c)=>a+c.w,0);let x=r()*tot;
    for(const c of pool){x-=c.w;if(x<=0){out.push(c.c);break;}}}
  return out;}
function tnWeekly(){const s=tnS(),w=tnWeek();if(!s.wk||s.wk.k!==w){const r=tnRng("tnw"+w),i0=w%TN_RARE.length;let id=null;
    for(let j=0;j<TN_RARE.length;j++){const c=TN_RARE[(i0+j)%TN_RARE.length];if(!S.owned.has(c)){id=c;break;}}
    s.wk={k:w,id,p:id?tnPrice(r,2):[],got:0};}
  return s.wk;}
function tnStock(){const s=tnS(),day=tnDay();if(s.day===day&&s.stock.length)return s.stock;
  const r=tnRng("tn"+day),wk=tnWeekly(),st=[];
  if(wk.id&&!wk.got&&!S.owned.has(wk.id))st.push({k:"it",id:wk.id,n:1,w:1,p:wk.p});
  const total=4+(r()*3|0),np=1+(r()<.4?1:0),pool=TN_COMMON.filter(id=>!S.owned.has(id)).sort(()=>r()-.5);
  while(st.length<total-np&&pool.length){const id=pool.pop();st.push({k:"it",id,n:1,w:0,p:tnPrice(r,1)});}
  const pp=TN_P.slice().sort(()=>r()-.5);while(st.length<total&&pp.length){const [id,n]=pp.pop();st.push({k:"fd",id,n,w:0,p:tnPrice(r,0)});}
  Object.assign(s,{day,stock:st,sold:[],line:""});save();return st;}
const tnName=o=>o.k==="it"?IT[o.id].n:FOOD[o.id].n+(o.n>1?" ×"+o.n:"");
const tnShort=o=>o.k==="it"?TN_IT[o.id][2]:FOOD[o.id].n.toLowerCase();
const tnCan=o=>o.p.every(c=>tnHave(c)>=c[2]);
const tnLeft=()=>tnStock().filter((o,i)=>!tnS().sold.includes(i));
const tnRareWaits=()=>tnOpen()&&tnLeft().some(o=>o.w)&&tnS().seen!==tnDay();
const tnAnd=a=>a.length<2?a.join(""):a.slice(0,-1).join(", ")+" и "+a[a.length-1];

function tnBuy(i){const s=tnS(),st=tnStock(),o=st[i];if(!o||s.sold.includes(i)||!tnOpen())return false;
  if(!tnCan(o)){s.line="Э-э, нет, так не пойдёт. Принеси сначала, что прошу, — тогда и поговорим.";tnPanel();return false;}
  for(const c of o.p)tnTake(c);
  if(o.k==="it"){S.owned.add(o.id);disc("shop",o.id);if(o.w){tnWeekly().got=1;award("tn_rare");}}else give(o.id,o.n);
  s.sold.push(i);s.n=(s.n||0)+1;
  s.line=o.w?"Редкость недели уходит к тебе! Береги её — второй такой нет на всём тракте Токайдо.":s.n===1?"Первая сделка! Запишу тебя в долговую книжку… на страницу «Друзья».":pick(TN_LINES);
  award("tn_first");if(s.n>=10)award("tn_ten");
  save();sfx("coin");chime(o.w?[784,988,1318,1568]:[988,1318]);hubDot();tnPanel();return true;}

// ── the shop panel ──
document.head.insertAdjacentHTML("beforeend",`<style>.tn-say{display:flex;gap:10px;align-items:flex-end;margin:2px 0 10px}.tn-say img{width:64px;height:auto;flex:none;filter:drop-shadow(0 2px 6px #000a)}
.tn-say p{margin:0;padding:9px 12px;border-radius:12px 12px 12px 2px;background:#1d1812;border:1px solid #4a3a26;color:var(--paper);font-size:14px;line-height:1.35}.tn-say b{color:#e0b060}
.tn-of{display:grid;grid-template-columns:78px 1fr;gap:10px;padding:10px;margin:8px 0;border-radius:12px;background:#11100d;border:1px solid var(--line,#2a2a26)}
.tn-of.rare{border-color:#a8843a;background:linear-gradient(160deg,#221a0e,#11100d 60%)}.tn-of.sold{opacity:.55}
.tn-pic{display:flex;align-items:center;justify-content:center;align-self:start;height:88px;border-radius:10px;background:radial-gradient(circle at 50% 60%,#3a2c1a,#14110c 70%)}
.tn-bd b{font-size:15px;color:var(--paper)}.tn-bd i{display:inline-block;margin-left:6px;font-style:normal;font-size:11px;color:#e8c060;border:1px solid #a8843a;border-radius:8px;padding:0 6px}
.tn-bd small{display:block;color:var(--muted);font-size:12px;line-height:1.3;margin:3px 0 5px}
.tn-pr{list-style:none;margin:0 0 7px;padding:0;font-size:13px;color:var(--paper)}.tn-pr li{margin:2px 0}.tn-pr em{display:block;font-style:normal;font-size:12px;color:#c87a6a}.tn-pr li.ok em{color:#8fc07a}
.tn-done{font-size:13px;color:#8fc07a;font-weight:700}.tn-note{font-size:12px;color:var(--muted);margin-top:10px}
.tn-hl{display:grid;gap:4px;margin:4px 0 8px}.tn-hl div{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--paper)}.tn-hl div>span:first-child{flex:none;width:34px;display:flex;justify-content:center}.tn-hl em{font-style:normal;color:var(--muted);font-size:12px}</style>`);
function tnCard(o,i){const s=tnS(),sold=s.sold.includes(i),can=tnCan(o),th=o.k==="it"?itemThumb(IT[o.id],70,74):fThumb(o.id,70,70);
  const pr=o.p.map(c=>{const h=tnHave(c),ok=h>=c[2];return`<li class="${ok?"ok":""}">${tnLabel(c)}<em>у тебя есть: ${h}${ok?" ✓":""}</em></li>`;}).join("");
  return`<div class="tn-of${o.w?" rare":""}${sold?" sold":""}"><div class="tn-pic">${th}</div><div class="tn-bd"><b>${tnName(o)}</b>${o.w?"<i>редкость недели</i>":""}
    <small>${o.k==="it"?TN_IT[o.id][3]:"Из кладовой тануки — такое на огороде и на рыбалке попадается нечасто."}</small>
    ${sold?`<span class="tn-done">Обменяно ✓</span>`:`<ul class="tn-pr">${pr}</ul><button class="btn${can?" primary":""}" data-x="tn:buy:${i}"${can?"":" disabled"}>${can?"Обменять":"Не хватает"}</button>`}</div></div>`;}
function tnPanel(){if(!tnOpen()){toast("Закрыто — тануки спит до вечера");return;}const s=tnS(),st=tnStock(),first=!panelIs("tn");
  if(s.seen!==tnDay()){s.seen=tnDay();save();hubDot();}
  if(first&&!s.line)s.line=pick(TN_HI);
  const left=st.filter((o,i)=>!s.sold.includes(i)),line=left.length?s.line:"Всё распродал! Приходи завтра вечером — лапы уже чешутся поторговаться.";
  const rare=st.map((o,i)=>o.w?tnCard(o,i):"").join(""),rest=st.map((o,i)=>o.w?"":tnCard(o,i)).join("");
  openPanel("Лавка тануки",`<div class="tn-say"><img src="assets/mon/m_tanuki.webp" alt=""><p><b>Тануки:</b> «${line}»</p></div>
    <p class="lead">Монеты тануки не берёт — только то, чего у тебя в избытке. Лавка открыта до 3 ночи, новый товар — каждый вечер.</p>
    ${rare?`<h3 class="bh">✦ Редкость недели</h3>${rare}`:""}<h3 class="bh">Сегодня на прилавке</h3>${rest||`<p class="lead">Пусто — всё уже у тебя.</p>`}
    <p class="tn-note">Последнее тануки не забирает: одна фигурка каждого вида, вещи в комнатах и по два каждого блюда, рыбы и овоща остаются у тебя. Обрезки для мастерской, повторы фигурок и находок Муси — пожалуйста.</p>`,"tn");
  if(first)$("xpBody").scrollTop=0;}

// ── the cart at the fair: left of Musya, in front of the goldfish stall (gachapon is on the right at x≈1275) ──
const TN_X=440,TN_Y=1215,TN_H=400;let TN_IM=null,tnSeen=false;ldImg("assets/items/tn_stall.webp",im=>{TN_IM=im;});
function tnFrame(){const x=visX(TN_X,190),oc=curRow;curRow=TN_Y;const [bx,by]=imgToStage(x,TN_Y,CAT_D),[,ty]=imgToStage(x,TN_Y-100,CAT_D);curRow=oc;const k=(by-ty)/100*TN_H/470;
  return{bx,by,k,x0:bx-220*k,y0:by-462*k};}
const tnBlit=(F,key)=>{const r=TN_ST[key];ctx.drawImage(TN_IM,r[0],r[1],r[2],r[3],F.x0,F.y0,r[2]*F.k,r[3]*F.k);};
function tnGlow(x,y,R,col,a){const g=ctx.createRadialGradient(x,y,0,x,y,R);g.addColorStop(0,`rgba(${col},${a})`);g.addColorStop(1,`rgba(${col},0)`);ctx.fillStyle=g;ctx.fillRect(x-R,y-R,R*2,R*2);}
hook("draw",(t,front)=>{if(S.room!=="matsuri"||!TN_IM||(TN_Y>catLineY()+6)!==front)return;const F=tnFrame(),k=F.k,open=tnOpen();
  ctx.fillStyle="rgba(0,0,0,.35)";ctx.beginPath();ctx.ellipse(F.bx,F.by,200*k,22*k,0,0,Math.PI*2);ctx.fill();
  tnBlit(F,"back");
  const im=MIMG.m_tanuki;
  if(open&&im&&!scene.on){const ph=t%9,look=Math.floor(t/6.5)%2,bob=Math.sin(t*2.1)*3*k+(ph<.5?-Math.abs(Math.sin(ph*Math.PI/.25))*10*k:0),h=340*k,w=h*340/470,cx=F.x0+220*k,top=F.y0+80*k+bob;   // face shows between the noren and the counter
    ctx.save();ctx.beginPath();ctx.rect(F.x0,F.y0+116*k,440*k,177*k);ctx.clip();ctx.translate(cx,top);if(look)ctx.scale(-1,1);ctx.drawImage(im,-w/2,0,w,h);ctx.restore();
    if(!tnSeen){tnSeen=true;if(!ST.seen.includes("tanuki"))ST.seen.push("tanuki");}}
  tnBlit(F,open?"open":"closed");
  if(open){const fl=.8+.12*Math.sin(t*5.1)+.08*Math.sin(t*12.3);ctx.save();ctx.globalCompositeOperation="lighter";
    for(const lx of [28,412])tnGlow(F.x0+lx*k,F.y0+150*k,80*k,"255,170,90",.32*fl);tnGlow(F.x0+220*k,F.y0+230*k,230*k,"255,190,120",.13*fl);ctx.restore();}
  else{const px=F.x0+220*k,py=F.y0+224*k;ctx.save();ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillStyle="#2a1a0e";
    const fit=(txt,wt,sz,y)=>{ctx.font=`${wt} ${sz}px sans-serif`;const m=ctx.measureText(txt).width,mw=200*k;if(m>mw)ctx.font=`${wt} ${sz*mw/m}px sans-serif`;ctx.fillText(txt,px,y);};
    fit("ЗАКРЫТО",800,Math.max(8,28*k),py-14*k);fit("тануки спит до вечера",600,Math.max(6,16*k),py+16*k);ctx.restore();
    drawEmoji(ctx,"💤",F.x0+330*k,F.y0+20*k-((t*.4)%1)*30*k,Math.max(12,46*k),.85-((t*.4)%1)*.6);}});
hook("hit",(x,y)=>{if(S.room!=="matsuri"||!TN_IM||scene.on)return;const F=tnFrame(),k=F.k;if(x<F.x0+10*k||x>F.x0+430*k||y<F.y0+40*k||y>F.by)return;
  audioInit();tone(660,.06,"triangle",.04);if(tnOpen())tnPanel();else{toast("Закрыто — тануки спит до вечера");tone(220,.25,"sine",.03);}return true;});
hook("tray",(tray,room)=>{if(room!=="matsuri"||(S.trayMode[room]||"play")!=="play")return;const el=tray.querySelector(".items");if(!el)return;
  const b=`<button class="item wide" data-x="tn:open"><span class="ico">🍃</span><span class="nm">Лавка тануки${tnOpen()?"":" · с 17:00"}</span></button>`,g=el.querySelector('[data-x="gc:open"]');
  if(g)g.insertAdjacentHTML("afterend",b);else el.insertAdjacentHTML("afterbegin",b);});
hook("click",k=>{if(!k.startsWith("tn:"))return;
  if(k==="tn:open")tnPanel();else if(k.startsWith("tn:buy:"))tnBuy(+k.slice(7));
  else if(k==="tn:go"){closePanel();goRoom("matsuri");if(tnOpen())setTimeout(tnPanel,600);}
  return true;});
hook("hubDot",()=>tnRareWaits());
hook("hub",()=>{const st=tnStock(),s=tnS(),open=tnOpen(),left=st.filter((o,i)=>!s.sold.includes(i)),names=tnAnd(left.slice(0,2).map(tnShort)),wk=left.find(o=>o.w);
  const status=open?(left.length?`Лавка открыта до 3 ночи: сегодня ${names}${wk&&left.indexOf(wk)>1?" и редкость недели":""}`:"Лавка открыта до 3 ночи, но тануки уже всё распродал — новый товар завтра вечером")
    :`Лавка откроется в 17:00${left.length?`, на прилавке: ${names}`:""}`;
  const rows=st.map((o,i)=>{const sold=s.sold.includes(i);return`<div><span>${o.k==="it"?itemThumb(IT[o.id],30,32):fThumb(o.id,30,30)}</span><span>${tnName(o)}${o.w?" ✦":""} <em>${sold?"· обменяно ✓":"· просит: "+o.p.map(c=>(t=>t[0].toLowerCase()+t.slice(1))(tnLabel(c).replace(/^\S+ /,""))).join(", ")}</em></span></div>`;}).join("");
  return`<div class="hubc"><h4>🍃 Лавка тануки <i>たぬき屋</i></h4><p>${status}.</p><div class="tn-hl">${rows}</div>
    <p class="lead">Тануки торгует с 17:00 до 3 ночи и меняет диковинки только на лишнее: повторы фигурок, материалы мастерской, излишки кладовой. Собрано: ${TN_I.filter(r=>S.owned.has(r[0])).length} из ${TN_I.length}.</p>
    <div class="row"><button class="btn primary" data-x="tn:go">🏮 ${open?"К лавке":"На ярмарку"}</button></div></div>`;});
hook("itemTap",(it,I)=>{const id=it.id;if(!/^tn_/.test(id))return;
  if(id==="tn_suzu"){chime([1568,2093,2637]);fxAt(it,["🔔","✨"],3);}else if(id==="tn_tsuki"||id==="tn_uchiwa"){[0,.25,.4,.8].forEach(d=>setTimeout(()=>tone(90,.2,"sine",.06),d*1000));fxAt(it,["♪","♫","🌕"],3);}
  else if(id==="tn_koban"){sfx("coin");fxAt(it,["🍃","✨"],3);}else{tone(330,.12,"triangle",.04);fxAt(it,["🍃"],2);}
  if(!petAway()&&pet.action!=="sleep")react("😸",1.2);return true;});
let tnSec=null;   // open/closed flips at 17:00 and 03:00 → refresh the 家 dot and the fair tray
hook("sec",()=>{const o=tnOpen();if(tnSec!==o){const was=tnSec;tnSec=o;if(was!==null){hubDot();if(S.room==="matsuri"&&!overlaysOpen())ui();}}});
X.tn={st:tnS,stock:tnStock,buy:tnBuy,open:tnPanel,frame:tnFrame,can:i=>tnCan(tnStock()[i]),have:tnHave,
  regen(){const s=tnS();s.day="";s.wk=null;return tnStock();},tap(){const F=tnFrame();return !!hk("hit",F.x0+220*F.k,F.y0+250*F.k);}};
}
