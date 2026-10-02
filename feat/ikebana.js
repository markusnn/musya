{
// ───────────────────────── «Икебана» (add-on ik) ─────────────────────────
// Once a day Musya gathers 3 seasonal stems in the courtyard (+1 if the forest was explored today). The arranging game
// (hidden GAMES "ik_arr"): a vessel, stems go in by a tap or a drag, a drag on a stem tilts it around the kenzan, the scissors
// shorten it from below; a faint guide «небо — человек — земля» (син, соэ, хикаэ); score → 1–3 ★ with a comment.
// The finished arrangement stands in the bedroom tokonoma (rendered to a canvas, drawn on the alcove plane) and wilts over 3 days.
// Judges: on even day numbers from 18:00 a yōkai with taste (Лиса-невеста → Тётин-обакэ → Нэкомата) comes to the bedroom
// to look at a NEW arrangement; a tap → his opinion, a gift for ★★★. Art: art/ikebana_art.py → assets/items/atlas_ik.webp.
// S.ext.ikebana = {g:dayKey gathered, fx:dayKey forest extra, td:[today's ids], inv:[{f,d,l?}], v:last vessel,
//   cur:{v,st:[{f,a,l,x}],sc,w,d,h,j?}, last:{sc,d}, n, best, seas:{spring:1…}, jd:dayKey judged, ja:dayKey arrival toast, jn}
const IK_AT=[976,1022],IK_R={"sakura":[0,0,120,370],"ume":[122,0,120,365],"tsubaki":[244,0,120,328],"suisen":[366,0,120,307],"ayame":[488,0,120,344],"ajisai":[610,0,120,308],"hasu":[732,0,120,344],"asagao":[854,0,120,343],"kiku":[0,372,120,317],"susuki":[122,372,120,333],"momiji":[244,372,120,345],"hagi":[366,372,120,342],"matsu":[488,372,120,341],"nanten":[610,372,120,306],"take":[732,372,120,364],"v_suiban":[0,738,230,76],"v_heika":[232,738,124,214],"v_take":[358,738,92,236],"ik_kenzan":[452,738,124,62],"ik_suiban":[578,738,158,220],"ik_take":[738,738,91,284],"ik_kago":[831,738,140,248]};
// id, name, short (for toasts), seasons, kind (line = branch/linear, mass = flower), petal colour
const IK_FL=[["sakura","Сакура","сакура","spring","line","#efc3cf"],["ume","Слива умэ","умэ","spring","line","#f3e7ea"],["tsubaki","Камелия","камелия","spring","mass","#a3263a"],
 ["suisen","Нарцисс","нарцисс","spring,winter","mass","#f1ede0"],["ayame","Ирис","ирис","summer","line","#4d3f93"],["ajisai","Гортензия","гортензия","summer","mass","#7a8ac8"],
 ["hasu","Лотос","лотос","summer","mass","#e3a1b4"],["asagao","Вьюнок","вьюнок","summer","line","#3e5fb4"],["kiku","Хризантема","хризантема","autumn","mass","#e2b84a"],
 ["susuki","Мискант сусуки","сусуки","autumn","line","#d8c8a0"],["momiji","Клён","клён","autumn","line","#c0502a"],["hagi","Хаги","хаги","autumn","mass","#c45a98"],
 ["matsu","Сосна","сосна","winter","line","#2f5236"],["nanten","Нандина","нандина","winter","mass","#b8222a"],["take","Бамбук","бамбук","winter","line","#6e8a3a"]];
const IK_F={};for(const f of IK_FL)IK_F[f[0]]={id:f[0],n:f[1],sn:f[2],sea:f[3].split(","),k:f[4],pc:f[5]};
// vessels: picture, size, mouth (where stems leave it, from the top), M = the measure for «син ≈ 1.5 × vessel», kenzan x range
const IK_V={suiban:{n:"Суйбан",r:"v_suiban",w:230,h:76,mouth:18,M:230,x0:-38,xr:[-80,40]},heika:{n:"Высокая ваза",r:"v_heika",w:124,h:214,mouth:5,M:214,x0:0,xr:[-14,14]},
  take:{n:"Бамбуковая ваза",r:"v_take",w:92,h:236,mouth:7,M:236,x0:0,xr:[-18,18]}};
const IK_VO=["suiban","heika","take"];
// the three lines: angle (rad, 0 = up, − = left), share of син, kanji, word
const IK_G=[[-.26,1,"天","небо"],[-.79,.75,"人","человек"],[1.22,.5625,"地","земля"]];
const IK_SEA={spring:"весна",summer:"лето",autumn:"осень",winter:"зима"};
const IK_J=["kitsune","obake","nekomata"],IK_JF={kitsune:1,nekomata:1};   // judges by turn; feminine ones
const IK_POS={x:290,y:1066,k:.72};   // the vessel's spot in the alcove (right of the core prop, visible on a phone) and image px per unit;
// it stands at the left of the niche, so the arrangement is shown leaning right, toward the room (mirrored if needed)
// the core's painted «Икебана в нише» prop gives way to the player's arrangement (its room is switched off while one stands)
const IK_PROP=PROPS.find(p=>p.id==="p_bed_ikebana");
function ikProp(){if(IK_PROP)IK_PROP.room=ikS().cur?"-ik":"bedroom";}
addItems([["ik_kenzan","Кэндзан","Составь первую икебану"],["ik_suiban","Суйбан с ирисами","Получи ★★★ за икебану"],["ik_take","Бамбуковая ваза с камелией","Подарок ценителя за икебану на ★★★"],
  ["ik_kago","Корзинка ханакаго","Подарок ценителя за икебану на ★★★"]].map(([id,n,h])=>{const r=IK_R[id];return{id,n,c:"Икебана",w:r[2],h:r[3],a:"b",p:0,at:["ik",r[0],r[1]],src:"🌸 икебана",hint:"🌸 "+h};}),{ik:IK_AT});
STAMPS.push(["ik_first","花","Первая икебана","Составь композицию — она встанет в токонома"],["ik_3","華","Три звезды","Получи ★★★ за икебану"],["ik_sea","季","Четыре сезона","Составь икебану весной, летом, осенью и зимой"]);
document.head.insertAdjacentHTML("beforeend",`<style>.card p.ik-st,.hubc p.ik-st{color:#d8a24a;font-size:22px;letter-spacing:3px;margin:0;line-height:1.2}.card p.ik-gift{color:var(--sakura)}
.ik-fl{display:grid;grid-template-columns:repeat(auto-fill,minmax(64px,1fr));gap:6px;margin:8px 0 14px}.ik-fl>div{display:flex;flex-direction:column;align-items:center;gap:2px;padding:6px 2px;border-radius:10px;background:#0a0d0c;box-shadow:inset 0 0 0 1px var(--line)}
.ik-fl>div>small{font-size:10.5px;line-height:1.15;color:var(--muted);text-align:center}.ik-fl>div.off>span{filter:brightness(0);opacity:.55}</style>`);

let IK_IM=null,ikB=0,ikBox=null,ikJBox=null,ikJT=0,ikLeave=-9,ikCache=null;
const ikS=()=>S.ext.ikebana||(S.ext.ikebana={g:null,fx:null,td:[],inv:[],v:"suiban",cur:null,last:null,n:0,best:0,seas:{},jd:null,ja:null,jn:0});
const ikDay=dk=>Math.round(Date.parse(dk+"T12:00:00Z")/864e5);
const ikLen=f=>IK_R[f][3];
const ikStars=n=>"★".repeat(n)+"☆".repeat(3-n);
const ikDate=dk=>new Date(Date.parse(dk+"T12:00:00Z")).toLocaleDateString("ru-RU",{day:"numeric",month:"long"});
function ikSea(){const m=today().getMonth()+1;return m>=3&&m<=5?"spring":m>=6&&m<=8?"summer":m>=9&&m<=11?"autumn":"winter";}
function ikForest(){const f=S.ext.forest;return !!(f&&f.d===dayKey()&&(f.u||0)>0);}
function ikPrune(){const z=ikS(),n=ikDay(dayKey());z.inv=z.inv.filter(o=>n-ikDay(o.d)<=2);}   // stems older than 2 days have wilted
const ikCanGather=()=>{const z=ikS(),dk=dayKey();return z.g!==dk||(ikForest()&&z.fx!==dk);};
const ikToday=()=>{const z=ikS();return z.g===dayKey()&&z.td?z.td:[];};
const ikHasStems=()=>{const z=ikS();return z.inv.length>0||!!(z.cur&&z.cur.d===dayKey());};
function ikThumb(f,mw,mh){const r=IK_R[f],k=Math.min(mw/r[2],mh/r[3]),q=v=>(v*k).toFixed(1);
  return`<span style="display:inline-block;width:${q(r[2])}px;height:${q(r[3])}px;background:url(assets/items/atlas_ik.webp) -${q(r[0])}px -${q(r[1])}px/${q(IK_AT[0])}px ${q(IK_AT[1])}px no-repeat"></span>`;}
function ikOwn(id){if(S.owned.has(id))return false;S.owned.add(id);loadItem(id);return true;}

// ── gathering in the courtyard: one line material + one flower + one more (+1 from the forest path)
function ikGather(){const z=ikS(),dk=dayKey(),sea=ikSea(),pool=IK_FL.filter(f=>f[3].includes(sea)).map(f=>f[0]),ln=pool.filter(f=>IK_F[f].k==="line"),ms=pool.filter(f=>IK_F[f].k==="mass");
  ikPrune();let got=[];if(z.g!==dk){got=[pick(ln),pick(ms),pick(pool)];z.g=dk;z.td=[];}
  if(ikForest()&&z.fx!==dk){got.push(pick(pool));z.fx=dk;}
  if(!got.length){toast("🌸 Сегодня цветы уже собраны");return;}
  for(const f of got)z.inv.push({f,d:dk});z.td=(z.td||[]).concat(got);save();
  const t="🌸 Собраны: "+got.map(f=>IK_F[f].sn).join(", ");toast(t.length<=44?t:`🌸 Собрано стеблей: ${got.length}`);
  chime([784,988,1175]);if(!petAway()){react("🌸",1.8);burst(6);S.needs.joy=clamp(S.needs.joy+4,0,100);}
  setTimeout(()=>toast("Икебану составляют в «家» или в спальне"),2600);ui();}

// ── drawing a stem: the TOP l units of its picture (cut from below), base at (bx,by), tilted by a
function ikStem(g,f,bx,by,a,l,u){const r=IK_R[f];if(!IK_IM||!r)return;const h=Math.max(8,Math.min(l,r[3]));
  g.save();g.translate(bx,by);g.rotate(a);g.drawImage(IK_IM,r[0],r[1],r[2],h,-r[2]/2*u,-h*u,r[2]*u,h*u);g.restore();}
function ikVessel(g,v,cx,bot,u){const V=IK_V[v],r=IK_R[V.r];if(IK_IM)g.drawImage(IK_IM,r[0],r[1],r[2],r[3],cx-V.w/2*u,bot-V.h*u,V.w*u,V.h*u);}

// ── scoring: lengths against the rule (син ≈ 1.5 × vessel, соэ ¾ син, хикаэ ¾ соэ), angles/asymmetry, season, empty space
function ikScore(v,st){const V=IK_V[v],T1=1.5*V.M,s=[...st].sort((a,b)=>b.l-a.l),[A,B,C]=s,deg=x=>x*180/Math.PI;
  const f=(r,tol)=>clamp(1-Math.max(0,Math.abs(r-1)-tol)/.2,0,1),band=(x,lo,hi,sf)=>x<lo?clamp(1-(lo-x)/sf,0,1):x>hi?clamp(1-(x-hi)/sf,0,1):1;
  const P={},sd=Math.sign(A.a)||-1;
  P.shin=f(A.l/T1,.08);P.soe=f(B.l/(A.l*.75),.1);P.hikae=f(C.l/(B.l*.75),.12);
  P.tilt=band(Math.abs(deg(A.a)),5,30,20);P.soeA=band(deg(B.a)*sd,25,65,25);P.asym=band(-deg(C.a)*sd,40,95,30);
  const sea=ikSea(),inS=st.filter(o=>IK_F[o.f].sea.includes(sea)).length/st.length;P.season=clamp((inS-.5)*2,0,1);
  P.line=new Set(st.map(o=>IK_F[o.f].k)).size===2?1:.35;
  let sp=st.length<=5?1:st.length===6?.6:.25;for(const o of s.slice(3))if(o.l>C.l*.95)sp-=.25;
  for(let i=0;i<st.length;i++)for(let j=i+1;j<st.length;j++)if(Math.abs(st[i].a-st[j].a)<.12&&Math.abs(st[i].l-st[j].l)<60)sp-=.2;P.space=clamp(sp,0,1);
  const len=(P.shin+P.soe+P.hikae)/3,ang=(P.tilt+P.soeA+P.asym)/3,tot=.45*len+.25*ang+.14*(P.season*.6+P.line*.4)+.16*P.space;
  const k=Object.keys(P).sort((a,b)=>P[a]-P[b])[0],w=P[k]>=.85?"ok":k==="shin"?(A.l<T1?"shinS":"shinL"):k==="soe"?(B.l<A.l*.75?"soeS":"soeL"):k==="hikae"?(C.l<B.l*.75?"hikS":"hikL"):k;
  const mn=Math.min(...Object.values(P));return{st:tot>=.85&&mn>=.6?3:tot>=.6?2:1,tot,w,P};}
// what is wrong, as a phrase in the middle of a sentence
const IK_W={ok:"небо, человек и земля в равновесии",shinS:"небо коротковато — син должен быть в полтора раза выше сосуда",shinL:"небо слишком высокое — оно спорит с сосудом",
  soeS:"человек мал для такого неба — соэ должен быть на четверть короче сина",soeL:"человек почти вровень с небом — подрежь соэ на четверть",
  hikS:"земля совсем крошечная — хикаэ должен быть на четверть короче соэ",hikL:"земля великовата — хикаэ должен быть короче соэ",
  tilt:"небо стоит как столб — дай ему лёгкий наклон",soeA:"человек не склоняется к небу — наклони соэ сильнее, в ту же сторону",
  asym:"нет асимметрии — земля должна смотреть в другую сторону",season:"цветы не из одного времени года",line:"не хватает ветки или стебля-линии — одни цветы",space:"слишком тесно — пустоте тоже нужно место"};
const ikCap=s=>s[0].toUpperCase()+s.slice(1);

// ── the arranging game ──
function ikBase(q,o){const L=q.L,V=IK_V[q.v];return[L.cx+o.x*L.u,L.vb-(V.h-V.mouth)*L.u];}
function ikLay(G){const q=G.st,s=G.s,W=G.W,H=G.H,th=Math.min(118*s,H*.18),V=IK_V[q.v];
  const L={s,W,H,trY:H-th,trH:th,btY:H-th-48*s,btH:38*s,top:46*s};L.vb=L.btY-14*s;
  L.u=Math.min((L.vb-L.top-10*s)/(V.h+1.5*V.M*.98+24),(W-20*s)/430,1.3);L.cx=W*.5+(W>H?0:6*s);
  const n=4,gap=6*s,bw=(W-16*s-gap*(n-1))/n;L.btns=[["ves","🏺 Сосуд"],["cut","✂ Ножницы"],["out","↩ Вынуть"],["done","✓ Готово"]].map(([id,nm],i)=>({id,nm,x:8*s+i*(bw+gap),y:L.btY,w:bw,h:L.btH}));
  q.L=L;q.lw=W;q.lh=H;}
function ikTraySlots(q){const L=q.L,n=Math.max(1,q.tray.length),sw=Math.min(84*L.s,(L.W-16*L.s)/n),x0=(L.W-sw*n)/2;return q.tray.map((o,i)=>({x:x0+i*sw,y:L.trY,w:sw,h:L.trH,o,i}));}
function ikHitStem(q,x,y){const L=q.L;for(let i=q.st.length-1;i>=0;i--){const o=q.st[i],[bx,by]=ikBase(q,o),dx=Math.sin(o.a),dy=-Math.cos(o.a),px=x-bx,py=y-by,t=px*dx+py*dy,len=o.l*L.u;
    if(t<-6||t>len+8)continue;const d=Math.abs(px*dy-py*dx);if(d<(t>len*.55?28:16)*L.s)return{i,t};}return null;}
function ikInsert(q,k,x,y){const o=q.tray.splice(k,1)[0];if(!o)return;const V=IK_V[q.v],n=q.st.length,gd=IK_G[n],bx0=q.L.cx+V.x0*q.L.u,by=q.L.vb-(V.h-V.mouth)*q.L.u;
  let a=gd?gd[0]:(n%2?.55:-.5)+(Math.random()-.5)*.3;if(x!=null){const dx=x-bx0,dy=by-y;if(Math.hypot(dx,dy)>30*q.L.s)a=clamp(Math.atan2(dx,dy),-1.7,1.7);}
  const xo=clamp(V.x0+(n?((n*13)%(V.xr[1]-V.xr[0]))+V.xr[0]-V.x0:0)*.35,V.xr[0],V.xr[1]);
  q.st.push({f:o.f,d:o.d,a,l:o.l,x:xo});q.sel=q.st.length-1;tone(520+n*60,.08,"triangle",.04);}
function ikBtn(G,id,t){const q=G.st;tone(300,.05,"triangle",.05);
  if(id==="ves"){const i=IK_VO.indexOf(q.v);q.v=IK_VO[(i+1)%IK_VO.length];for(const o of q.st)o.x=clamp(o.x-IK_V[IK_VO[i]].x0+IK_V[q.v].x0,IK_V[q.v].xr[0],IK_V[q.v].xr[1]);ikLay(G);q.msg={t,s:IK_V[q.v].n};return;}
  if(id==="cut"){q.cut=!q.cut;q.msg={t,s:q.cut?"Коснись стебля там, где резать":"Ножницы убраны"};return;}
  if(id==="out"){const i=q.sel>=0&&q.sel<q.st.length?q.sel:q.st.length-1;if(i<0)return;const o=q.st.splice(i,1)[0];q.tray.push({f:o.f,d:o.d,l:o.l});q.sel=-1;return;}
  if(id==="done")ikFinish(G,t);}
function ikCut(G,i,tt,t){const q=G.st,o=q.st[i],cut=tt/q.L.u;if(cut<6)return;const nl=Math.max(70,o.l-cut);if(nl>=o.l-1){q.msg={t,s:"Короче нельзя — останется один цветок"};return;}
  const [bx,by]=ikBase(q,o);q.fx.push({x:bx+Math.sin(o.a)*tt,y:by-Math.cos(o.a)*tt,t,e:"✂"});o.l=nl;q.sel=i;tone(1500,.04,"square",.03);setTimeout(()=>tone(1100,.05,"square",.025),60);}
function ikFinish(G,t){const q=G.st,z=ikS();if(q.win)return;if(q.st.length<3){q.msg={t,s:"Нужно три стебля: небо, человек и земля"};tone(260,.2,"sine",.04);return;}
  const R=ikScore(q.v,q.st),dk=dayKey(),sea=ikSea();G.score=R.st;q.R=R;q.win=t;q.fin=t+2.8;q.cut=false;q.sel=-1;R.fresh=[];
  for(const o of q.st)if(disc("ikebana",o.f))R.fresh.push(o.f);
  z.cur={v:q.v,st:q.st.map(o=>({f:o.f,a:+o.a.toFixed(3),l:Math.round(o.l),x:Math.round(o.x)})),sc:R.st,w:R.w,d:dk,h:+hourNow().toFixed(2)};
  z.inv=q.tray.map(o=>o.l<ikLen(o.f)-1?{f:o.f,d:o.d,l:Math.round(o.l)}:{f:o.f,d:o.d});z.v=q.v;
  z.n=(z.n||0)+1;z.last={sc:R.st,d:dk};z.best=Math.max(z.best||0,R.st);(z.seas||(z.seas={}))[sea]=1;
  if(ikOwn("ik_kenzan"))R.gift="ik_kenzan";if(R.st===3&&ikOwn("ik_suiban"))R.gift="ik_suiban";
  award("ik_first");if(R.st===3)award("ik_3");if(Object.keys(z.seas).length>=4)award("ik_sea");
  S.needs.joy=clamp(S.needs.joy+4+R.st*2,0,100);ikCache=null;ikProp();save();
  setTimeout(()=>{tone(392,.3,"sine",.05);tone(523,.4,"sine",.04);},120);for(let i=0;i<R.st;i++)setTimeout(()=>tone(1046*[1,1.26,1.5][i],.5,"sine",.04),700+i*260);}
function ikBg(G){const q=G.st,W=G.W,H=G.H,c=document.createElement("canvas"),d=Math.min(2,devicePixelRatio||1);c.width=W*d;c.height=H*d;const g=c.getContext("2d");g.setTransform(d,0,0,d,0,0);
  let gr=g.createLinearGradient(0,0,0,H);gr.addColorStop(0,"#2f2a22");gr.addColorStop(.75,"#231f19");gr.addColorStop(1,"#14110d");g.fillStyle=gr;g.fillRect(0,0,W,H);
  const r=rng(77);for(let i=0;i<260;i++){g.fillStyle=`rgba(${r()<.5?"70,62,50":"20,17,13"},${.05+r()*.08})`;const s=4+r()*26;g.fillRect(r()*W,r()*H,s,s*(.5+r()));}   // plaster
  g.fillStyle="#1c140e";g.fillRect(0,q.L.vb-2,W,10*q.L.s);g.fillStyle="#3b2c20";g.fillRect(0,q.L.vb,W,q.L.btY-q.L.vb+4*q.L.s);   // the tokonoma board
  g.strokeStyle="rgba(20,14,10,.75)";g.lineWidth=10*q.L.s;g.strokeRect(5*q.L.s,5*q.L.s,W-10*q.L.s,q.L.vb-4*q.L.s);
  const vg=g.createRadialGradient(W/2,H*.42,Math.min(W,H)*.2,W/2,H*.42,Math.max(W,H)*.75);vg.addColorStop(0,"rgba(255,214,150,.07)");vg.addColorStop(1,"rgba(0,0,0,.5)");g.fillStyle=vg;g.fillRect(0,0,W,H);
  g.fillStyle="rgba(10,8,6,.72)";g.fillRect(0,q.L.trY,W,q.L.trH);g.fillStyle="rgba(216,210,195,.18)";g.fillRect(0,q.L.trY,W,1);return c;}
let IK_FF=null;const ikFF=()=>IK_FF||(IK_FF=getComputedStyle(document.body).fontFamily);
function ikTx(g,txt,x,y,size,col,w=600,al="center",font){g.font=`${w} ${size}px ${font||ikFF()}`;g.textAlign=al;g.textBaseline="middle";g.fillStyle=col;g.fillText(txt,x,y);}
const IKG={id:"ik_arr",hidden:true,n:"Икебана",tag:"生け花 · Икэбана",bg:"room",lives:null,time:null,icon:"🌸",lore:"",how:"",
 init(G,t){const z=ikS();ikPrune();const q=G.st,re=z.cur&&z.cur.d===dayKey();G.score=0;
   Object.assign(q,{v:re?z.cur.v:(z.v||"suiban"),st:re?z.cur.st.map(o=>({...o,d:z.cur.d})):[],tray:z.inv.map(o=>({f:o.f,d:o.d,l:o.l||ikLen(o.f)})),sel:-1,cut:false,drag:null,rot:null,msg:null,fx:[],win:0,fin:0,R:null,bub:null});
   ikLay(G);q.bg=ikBg(G);if(!IK_IM)atlasImg("ik",im=>{IK_IM=im;});},
 step(G,t){const q=G.st;if(q.lw!==G.W||q.lh!==G.H){ikLay(G);q.bg=ikBg(G);}if(q.fin&&t>q.fin){q.fin=0;gEnd();}},
 draw(G,g,t){const q=G.st,L=q.L,s=L.s,u=L.u,V=IK_V[q.v],T1=1.5*V.M;g.drawImage(q.bg,0,0,G.W,G.H);
   // the guide: three faint lines from the kenzan, markers glow when a stem tip is near
   const bx0=L.cx+V.x0*u,by0=L.vb-(V.h-V.mouth)*u,tips=q.st.map(o=>{const [bx,by]=ikBase(q,o);return[bx+Math.sin(o.a)*o.l*u,by-Math.cos(o.a)*o.l*u];});
   if(!q.win){g.save();g.setLineDash([5*s,7*s]);g.lineWidth=1.4*s;
     IK_G.forEach(([a,k,jp,ru])=>{const len=T1*k*u,ex=bx0+Math.sin(a)*len,ey=by0-Math.cos(a)*len,near=tips.some(([x,y])=>Math.hypot(x-ex,y-ey)<T1*.09*u);
       g.strokeStyle=near?"rgba(236,196,110,.55)":"rgba(230,220,190,.2)";g.beginPath();g.moveTo(bx0,by0);g.lineTo(ex,ey);g.stroke();
       g.setLineDash([]);g.fillStyle=near?"rgba(236,196,110,.85)":"rgba(230,220,190,.28)";g.beginPath();g.arc(ex,ey,(near?7:5.5)*s,0,7);g.fill();g.setLineDash([5*s,7*s]);
       const lf=a<0&&ex>70*s,lx=ex+(lf?-14:14)*s,ly=lf||a>0?ey:ey-22*s;ikTx(g,jp,lx,ly-8*s,17*s,near?"#ecc46e":"rgba(230,220,190,.5)",500,lf?"right":"left",'"Noto Serif JP","Hiragino Mincho ProN",serif');
       ikTx(g,ru,lx,ly+10*s,11*s,near?"#ecc46e":"rgba(230,220,190,.45)",600,lf?"right":"left");});g.restore();}
   // stems behind the vessel, the selected one with a soft halo
   q.st.forEach((o,i)=>{const [bx,by]=ikBase(q,o);if(i===q.sel&&!q.win){g.save();g.strokeStyle=q.cut?"rgba(240,150,140,.35)":"rgba(236,214,160,.28)";g.lineWidth=16*s;g.lineCap="round";g.beginPath();g.moveTo(bx,by);g.lineTo(bx+Math.sin(o.a)*o.l*u,by-Math.cos(o.a)*o.l*u);g.stroke();g.restore();}
     ikStem(g,o.f,bx,by,o.a,o.l,u);});
   g.save();g.fillStyle="rgba(0,0,0,.35)";g.beginPath();g.ellipse(L.cx,L.vb,V.w*.55*u,7*s,0,0,7);g.fill();g.restore();ikVessel(g,q.v,L.cx,L.vb,u);
   if(q.sel>=0&&q.st[q.sel]&&!q.win&&!q.cut){const [x,y]=tips[q.sel];g.fillStyle="rgba(236,214,160,.8)";g.beginPath();g.arc(x,y,5*s,0,7);g.fill();}
   for(const f of q.fx){const a=(t-f.t)/.8;if(a<1)drawEmoji(g,f.e,f.x+14*s,f.y-a*24*s,18*s,1-a);}q.fx=q.fx.filter(f=>t-f.t<.8);
   // Musya watches from the corner
   if(!petAway()){const mx=42*s,fl=L.vb+4*s,sc=.4*s;let st="rest",fi=Math.floor(t*1.5)%2;const p=q.drag||q.rot&&q.rot.p;
     if(q.win&&t-q.win<1.4){st="highfive";fi=Math.min(7,Math.floor((t-q.win)/1.4*8));}else if(p){const gi=gazeIndex(p[0]-mx,(fl-150*sc)-p[1]);st=gi<8?"gaze9":"gaze10";fi=gi%8;}
     drawCatG(g,st,fi,mx,fl,sc);if(q.bub){const e=t-q.bub.t;if(e<2)drawEmoji(g,q.bub.e,mx+30*s,fl-95*s-e*8*s,20*s,clamp(Math.min(e*4,(2-e)*2),0,1));else q.bub=null;}}
   // the tray of stems
   const sl=ikTraySlots(q);if(!sl.length)ikTx(g,q.st.length?"Все стебли в сосуде":"Стеблей нет — во дворике новые цветы",G.W/2,L.trY+L.trH/2,13*s,"rgba(216,210,195,.6)");
   for(const b of sl){if(q.drag&&q.drag.k===b.i&&q.drag.moved)continue;const r=IK_R[b.o.f],mh=b.h-30*s,k=Math.min(mh/r[3],(b.w-8*s)/r[2]),cx=b.x+b.w/2,bot=b.y+6*s+mh;
     if(IK_IM)g.drawImage(IK_IM,r[0],r[1],r[2],Math.min(r[3],b.o.l),cx-r[2]*k/2,bot-Math.min(r[3],b.o.l)*k,r[2]*k,Math.min(r[3],b.o.l)*k);
     ikTx(g,IK_F[b.o.f].sn,cx,b.y+b.h-12*s,11*s,"#d8d2c3",600);}
   if(q.drag&&q.drag.moved){const o=q.tray[q.drag.k];if(o){g.globalAlpha=.85;ikStem(g,o.f,q.drag.x,q.drag.y+20*s,0,o.l,u*.9);g.globalAlpha=1;}}
   for(const b of L.btns)btnRect(g,b.x,b.y,b.w,b.h,b.nm,(b.id==="cut"&&q.cut)||(b.id==="done"&&q.st.length>=3&&!q.win));
   // the hint line / the result
   if(q.win){for(let i=0;i<3;i++){const a=clamp((t-q.win-.6-i*.26)/.25,0,1);if(a<=0)continue;const on=i<q.R.st;ikTx(g,on?"★":"☆",G.W/2+(i-1)*36*s,26*s,(26+8*(1-a))*s,on?`rgba(216,162,74,${a})`:`rgba(200,190,170,${a*.5})`,400);}}
   else{const n=q.st.length,h=q.msg&&t-q.msg.t<2.6?q.msg.s:q.cut?"Коснись стебля там, где резать":!n?"Коснись стебля внизу — он встанет в сосуд":n<3?"Добавь ещё: небо, человек и земля":"Тяни стебель — наклон, ✂ — подрезать. Кончики к меткам";
     ikTx(g,h,G.W/2,24*s,Math.min(14*s,G.W/h.length*1.7),"rgba(236,228,210,.85)");}},
 down(G,x,y,t){const q=G.st,L=q.L;if(q.win)return;
   const b=L.btns.find(b=>x>=b.x&&x<=b.x+b.w&&y>=b.y&&y<=b.y+b.h);if(b){ikBtn(G,b.id,t);return;}
   if(y>=L.trY){const sl=ikTraySlots(q).find(b=>x>=b.x&&x<=b.x+b.w);if(sl)q.drag={k:sl.i,x,y,sx:x,sy:y,moved:false};return;}
   const h=ikHitStem(q,x,y);if(h){if(q.cut){ikCut(G,h.i,h.t,t);return;}const o=q.st[h.i],[bx,by]=ikBase(q,o);q.sel=h.i;q.rot={i:h.i,da:o.a-Math.atan2(x-bx,by-y),p:[x,y]};return;}
   if(!petAway()&&Math.abs(x-42*L.s)<40*L.s&&y>L.vb-90*L.s&&y<L.vb+6*L.s){q.bub={e:pick(["😺","😽","🐾"]),t};tone(520,.08,"sine",.03);return;}
   q.sel=-1;},
 move(G,x,y,held){const q=G.st;if(!held)return;
   if(q.drag){q.drag.x=x;q.drag.y=y;if(Math.hypot(x-q.drag.sx,y-q.drag.sy)>10)q.drag.moved=true;return;}
   if(q.rot){const o=q.st[q.rot.i];if(!o)return;const [bx,by]=ikBase(q,o);q.rot.p=[x,y];if(Math.hypot(x-bx,y-by)<22*q.L.s)return;o.a=clamp(Math.atan2(x-bx,by-y)+q.rot.da,-1.75,1.75);}},
 up(G){const q=G.st,d=q.drag;q.rot=null;if(!d)return;q.drag=null;if(!d.moved)ikInsert(q,d.k);else if(d.y<q.L.btY)ikInsert(q,d.k,d.x,d.y+20*q.L.s);},
 stat:G=>{const q=G.st;return q.v?`${IK_V[q.v].n} · ${q.st.length}`:"";},
 card(G){const q=G.st,R=q.R||{st:G.score,w:"ok",fresh:[]},z=ikS(),J=ikJudgeNext();
   return`<div class="card"><p class="tag">生け花 · Икэбана</p><h3>${["Ещё разок","Неплохо","Хорошо","Прекрасно"][R.st]}</h3><p class="ik-st">${ikStars(R.st)}</p>
   <p class="lore">${R.w==="ok"?"Небо, человек и земля в равновесии.":ikCap(IK_W[R.w])+"."}</p>
   ${R.fresh.length?`<p>Впервые в композиции: ${R.fresh.map(f=>IK_F[f].n.toLowerCase()).join(", ")}.</p>`:""}
   ${R.gift?`<p class="ik-gift">🎁 Новая вещь: «${IT[R.gift].n}». Её можно поставить в любой комнате.</p>`:""}
   <p>Композиция стоит в нише токонома в спальне.${J?" "+J:""}</p>
   <div class="row"><button class="btn" id="gHome">Домой</button><button class="btn primary" id="gAgain">Переставить</button></div></div>`;},
 after(){ui();}};
GAMES.push(IKG);
function ikOpen(){if(G.id)return;if(!ikHasStems()){toast("🌸 Сначала собери цветы во дворике");return;}closePanel();$("album").hidden=true;atlasImg("ik",im=>{IK_IM=im;openPlace("ik_arr");});}

// ── the tokonoma: the arrangement rendered once into a canvas (wilting: droop, browning, lost petals, petals on the board)
function ikWilt(){const c=ikS().cur;if(!c)return 0;const d=ikDay(dayKey())-ikDay(c.d)+(hourNow()-(c.h||12))/24;return clamp(Math.round(clamp((d-.4)/2.6,0,1)*6)/6,0,1);}
function ikRender(c,w){const V=IK_V[c.v],sc=.9,my=-(V.h-V.mouth),dr=o=>o.a+(o.a<0?-1:1)*w*.22;let x0=-V.w/2-30,x1=V.w/2+30,y0=-V.h,y1=10;
  for(const o of c.st){const a=dr(o),tx=o.x+Math.sin(a)*o.l,ty=my-Math.cos(a)*o.l;x0=Math.min(x0,tx-62);x1=Math.max(x1,tx+62);y0=Math.min(y0,ty-24);}
  const W=Math.ceil((x1-x0)*sc),H=Math.ceil((y1-y0)*sc),mk=()=>{const k=document.createElement("canvas");k.width=W;k.height=H;const g=k.getContext("2d");g.setTransform(sc,0,0,sc,-x0*sc,-y0*sc);return[k,g];};
  const [cv,g]=mk(),[sv,sg]=mk();for(const o of c.st)ikStem(sg,o.f,o.x,my,dr(o),o.l,1);
  if(w>0){sg.setTransform(1,0,0,1,0,0);sg.globalCompositeOperation="source-atop";sg.fillStyle=`rgba(88,66,40,${w*.5})`;sg.fillRect(0,0,W,H);
    sg.globalCompositeOperation="destination-out";sg.setTransform(sc,0,0,sc,-x0*sc,-y0*sc);const r=rng(c.st.length*97+(c.n||3));
    for(const o of c.st){const a=dr(o);for(let i=0;i<Math.round(w*18);i++){const t=o.l*(.55+.45*r()),p=(r()-.5)*44;sg.beginPath();sg.arc(o.x+Math.sin(a)*t+Math.cos(a)*p,my-Math.cos(a)*t+Math.sin(a)*p,3+r()*5,0,7);sg.fill();}}
    sg.globalCompositeOperation="source-over";}
  g.fillStyle="rgba(0,0,0,.4)";g.beginPath();g.ellipse(0,0,V.w*.56,8,0,0,7);g.fill();g.drawImage(sv,x0,y0,W/sc,H/sc);
  const r=IK_R[V.r];if(IK_IM)g.drawImage(IK_IM,r[0],r[1],r[2],r[3],-V.w/2,-V.h,V.w,V.h);
  if(w>0){const q=rng(11+c.st.length);for(let i=0;i<Math.round(w*22);i++){const o=c.st[i%c.st.length];g.fillStyle=IK_F[o.f].pc;g.globalAlpha=.75;g.beginPath();g.ellipse((q()-.5)*V.w*1.6,2+q()*6,3+q()*2.5,1.6,q()*3,0,7);g.fill();}g.globalAlpha=1;}
  return{c:cv,ox:-x0,oy:-y0,sc};}
function ikTinted(){const z=ikS(),c=z.cur;if(!c||!IK_IM)return null;const w=ikWilt(),tint=DTINT[bgName()]||"",key=[c.d,c.h,z.n,w,tint].join("|");if(ikCache&&ikCache.key===key)return ikCache;
  const R=ikRender(c,w);if(tint){const g=R.c.getContext("2d");g.setTransform(1,0,0,1,0,0);g.globalCompositeOperation="source-atop";g.fillStyle=tint;g.fillRect(0,0,R.c.width,R.c.height);}
  R.key=key;ikCache=R;return R;}
function ikFlip(){const c=ikS().cur;if(!c||!c.st.length)return false;return [...c.st].sort((a,b)=>b.l-a.l)[0].a<0;}
function ikDrawAlcove(){const R=ikTinted();ikBox=null;if(!R)return;const k=IK_POS.k,fl=ikFlip(),wl=R.ox/R.sc*k,wr=(R.c.width-R.ox)/R.sc*k,ix0=IK_POS.x-(fl?wr:wl),ix1=IK_POS.x+(fl?wl:wr),iy0=IK_POS.y-R.oy/R.sc*k,iy1=iy0+R.c.height/R.sc*k;
  const cr=curRow;curRow=null;const [x0,y0]=imgToStage(ix0,iy0,.5),[x1,y1]=imgToStage(ix1,iy1,.5);curRow=cr;if(x1<=x0||y1<=y0)return;
  if(fl){ctx.save();ctx.translate(x0+x1,0);ctx.scale(-1,1);ctx.drawImage(R.c,x0,y0,x1-x0,y1-y0);ctx.restore();}else ctx.drawImage(R.c,x0,y0,x1-x0,y1-y0);ikBox=[x0+(x1-x0)*.15,y0,x1-(x1-x0)*.15,y1];}

// ── the judges: even day numbers, from 18:00, only for a new arrangement; a tap → their opinion and (★★★) a gift
function ikJudgeOn(dk){const n=ikDay(dk);return n%2?null:GUESTS.find(g=>g.id===IK_J[((n/2)%3+3)%3]);}
function ikJHere(){const z=ikS(),J=ikJudgeOn(dayKey());return !!(J&&hourNow()>=18&&z.cur&&!z.cur.j&&z.jd!==dayKey());}
const ikCame=J=>IK_JF[J.id]?"пришла":"пришёл";
function ikJudgeNext(){const z=ikS(),dk=dayKey(),J=ikJudgeOn(dk);
  if(ikJHere())return`Сейчас в спальне ${J.n} — смотрит икебану.`;
  if(!z.cur)return"";if(z.cur.j)return"";
  if(J&&z.jd!==dk)return`Сегодня после 18:00 её оценит ${J.n}.`;
  const nx=ikJudgeOn(new Date(Date.parse(dk+"T12:00:00Z")+(J?2:1)*864e5).toISOString().slice(0,10));return nx?`${J?"Послезавтра":"Завтра"} вечером её оценит ${nx.n}.`:"";}
const IK_JL={kitsune:{3:"Небо, человек и земля — всё на своём месте, как на лисьей свадьбе. Возьми на память.",2:"Красиво… но %. Лисы замечают такие мелочи.",1:"Хм. %. Попробуй ещё — у тебя получится."},
  obake:{3:"Ох, даже фитиль затрепетал! Сто лет такой красоты не видел. Держи подарок.",2:"Глаз у меня один, но и он видит: %.",1:"Мигаю-мигаю, а гармонии не вижу. %."},
  nekomata:{3:"Мур-р… Оба хвоста дрожат от восторга. Это тебе, сестрёнка.",2:"Неплохо, сестрёнка. Только %.",1:"Фыр. %. Кошки любят порядок."}};
function ikJudgeTalk(){const z=ikS(),J=ikJudgeOn(dayKey()),c=z.cur;if(!J||!c||!ikJHere())return;audioInit();chime([523,659]);
  if(!petAway())react("😺",1.4);const tpl=IK_JL[J.id][c.sc],ph=c.w==="ok"?"всё почти безупречно":IK_W[c.w],txt=tpl.replace("%",tpl.indexOf("%")===0||/[.!?…] %/.test(tpl)?ikCap(ph):ph);
  dlg({head:`${J.n} · ${IK_JF[J.id]?"ценительница":"ценитель"} икебаны`,text:`«${txt}»`,img:`<img src="assets/mon/${J.mon}.webp" alt="" style="height:64px">`,ok:"Поклониться",onOk:()=>ikJudgeDone(J)});}
function ikJudgeDone(J){const z=ikS(),c=z.cur;if(!c)return;c.j={id:J.id,d:dayKey()};z.jd=dayKey();z.jn=(z.jn||0)+1;ikLeave=now();let g=null;
  if(c.sc===3){g=["ik_take","ik_kago"].find(id=>ikOwn(id));if(g)toast(`🎁 Подарок: ${IT[g].n.toLowerCase()}`);else{const f=pick(["ds_mochi","ds_dango","ds_daifuku"]);give(f,1);toast(`🎁 ${J.n}: подарок — ${FOOD[f].n.toLowerCase()}`);}}
  else toast(`${J.n} кланяется и уходит`);if(!petAway())S.needs.joy=clamp(S.needs.joy+3,0,100);save();hubDot();}
function ikJudgePos(){return[visX(500,80),catLineY()-34];}

// ── hooks ──
hook("boot",()=>{ikB=1;atlasImg("ik",im=>{IK_IM=im;});ikPrune();ikProp();});
hook("tray",(tray,room)=>{const mode=S.trayMode[room]||"play";if(mode!=="play")return;const el=tray.querySelector(".items");if(!el)return;let b=null;
  if(room==="courtyard"&&ikCanGather())b=["ik:gather","🌸",ikS().g===dayKey()?"Цветок с лесной тропы":"Собрать цветы"];
  else if(room==="bedroom"&&ikHasStems())b=["ik:open","🌸","Составить икебану"];if(!b)return;
  const html=`<button class="item wide" data-x="${b[0]}"><span class="ico">${b[1]}</span><span class="nm">${b[2]}</span></button>`;
  el.insertAdjacentHTML("afterbegin",html);});
hook("click",k=>{if(!k.startsWith("ik:"))return;const a=k.slice(3);
  if(a==="gather")ikGather();else if(a==="open")ikOpen();else if(a==="yard"){closePanel();goRoom("courtyard");}else if(a==="bed"){closePanel();goRoom("bedroom");}return true;});
hook("draw",(t,front)=>{if(front||S.room!=="bedroom"||scene.on)return;ikProp();ikDrawAlcove();ikJBox=null;
  const J=ikJudgeOn(dayKey()),here=ikJHere(),fade=clamp((now()-ikLeave)/1.2,0,1);if(!J||!(here||fade<1))return;if(here&&!ikJT)ikJT=now();
  const a=here?clamp((now()-ikJT)/1.5,0,1):1-fade,[ix,iy]=ikJudgePos(),h=J.h*.86;drawMon(J.mon,ix,iy+Math.sin(t*1.6)*3,h,CAT_D,a);
  curD=CAT_D;curRow=iy;const [x0,y0]=imgToStage(ix-h*.3,iy-h),[x1,y1]=imgToStage(ix+h*.3,iy);curRow=null;if(here)ikJBox=[x0,y0,x1,y1];
  if(here&&ikBox&&Math.sin(t*1.3)>.97)floatFx.push({g:"✨",x:(ikBox[0]+ikBox[2])/2+rand(-20,20),y:ikBox[1]+(ikBox[3]-ikBox[1])*rand(.2,.5),t:now()});});
hook("hit",(x,y)=>{if(S.room!=="bedroom"||scene.on)return false;
  if(ikJBox&&x>=ikJBox[0]&&x<=ikJBox[2]&&y>=ikJBox[1]&&y<=ikJBox[3]){ikJudgeTalk();return true;}
  if(ikBox&&x>=ikBox[0]&&x<=ikBox[2]&&y>=ikBox[1]&&y<=ikBox[3]){audioInit();const z=ikS(),c=z.cur;
    if(ikHasStems())ikOpen();else toast(c?`🌸 ${ikStars(c.sc)} · ${ikWilt()>=1?"увяла — пора собрать новые":"новые цветы — во дворике"}`:"🌸 Цветы — во дворике");return true;}
  return false;});
hook("sec",()=>{if(!ikB)return;const z=ikS();if(ikJHere()){if(z.ja!==dayKey()&&!scene.on&&!overlaysOpen()){z.ja=dayKey();const J=ikJudgeOn(dayKey());knock();
    setTimeout(()=>toast(`🌸 ${J.n} ${ikCame(J)} смотреть икебану`),600);save();}}else ikJT=0;});
hook("room",id=>{if(id==="bedroom"&&ikJHere())setTimeout(()=>{if(S.room==="bedroom"&&ikJHere())toast("Нажми на гостя — услышишь его мнение");},1500);});
hook("tabDot",r=>r==="bedroom"&&ikJHere());
hook("hubDot",()=>ikB&&(ikJHere()||(ikS().inv.length>=3&&!(ikS().cur&&ikS().cur.d===dayKey()))));
hook("hub",()=>{const z=ikS(),td=ikToday(),c=z.cur,w=ikWilt(),J=ikJudgeNext();
  const st=td.length?`Сегодня собраны: ${td.map(f=>IK_F[f].sn).join(", ")}`:"Цветы ждут — собери во дворике";
  const cur=c?`В нише — композиция на ${ikStars(c.sc)} от ${ikDate(c.d)}, ${w<=0?"свежая":w<1?"понемногу вянет":"увяла"}.`:"Ниша токонома в спальне пока пуста.";
  const jl=c&&c.j?` ${GUESTS.find(g=>g.id===c.j.id)?.n||"Ценитель"} уже ${IK_JF[c.j.id]?"оценила":"оценил"} её.`:"";
  return`<div class="hubc"><h4>🌸 Икебана <i>生け花</i></h4><p>${st}${z.inv.length?` · стеблей: ${z.inv.length}`:""}</p>
  <p>${cur}${jl} ${J||"Ценители-ёкаи приходят через вечер, после 18:00, — посмотреть на новую композицию."}</p>
  <p>Сезон: ${IK_SEA[ikSea()]}. Композиций: ${z.n||0}, лучшая — ${ikStars(z.best||0)}.</p>
  <div class="row">${ikHasStems()?`<button class="btn primary" data-x="ik:open">Составить икебану</button>`:""}${ikCanGather()?`<button class="btn${ikHasStems()?"":" primary"}" data-x="ik:yard">Во дворик за цветами</button>`:""}${c?`<button class="btn" data-x="ik:bed">В спальню</button>`:""}</div></div>`;});
hook("album",el=>{const z=ikS(),D=(S.ext.disc||{}).ikebana||{},n=Object.keys(D).length;if(!z.n&&!n)return;
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Икебана</h3><p class="lead">Цветы и ветки, побывавшие в композициях: ${n} из ${IK_FL.length}. Каждому сезону — свои.</p>
  <div class="ik-fl">${IK_FL.map(f=>`<div class="${D[f[0]]?"":"off"}">${ikThumb(f[0],40,70)}<small>${D[f[0]]?f[1]:IK_SEA[f[3].split(",")[0]]}</small></div>`).join("")}</div>`);});
X.ik={S:ikS,gather:ikGather,open:ikOpen,score:ikScore,wilt:ikWilt,here:ikJHere,talk:ikJudgeTalk,next:ikJudgeNext,
  // tests: act on the open game through its own handlers (synthetic pointer events break setPointerCapture)
  tray(k=0){const q=G.st;ikInsert(q,k);},
  rot(i,deg){const q=G.st,o=q.st[i];if(o)o.a=deg*Math.PI/180;},
  cut(i,len){const q=G.st,o=q.st[i];if(!o)return;const [bx,by]=ikBase(q,o),tt=(o.l-len)*q.L.u;q.cut=true;G.def.down(G,bx+Math.sin(o.a)*tt,by-Math.cos(o.a)*tt,now());},
  btn(id){const b=G.st.L.btns.find(b=>b.id===id);G.def.down(G,b.x+b.w/2,b.y+b.h/2,now());},
  dragTray(k,x,y){const q=G.st,b=ikTraySlots(q)[k];G.held=true;G.def.down(G,b.x+b.w/2,b.y+b.h/2,now());G.def.move(G,x,y,true);},drop(){G.held=false;G.def.up(G);},
  tapJudge(){if(!ikJBox)return"no judge box";hk("hit",(ikJBox[0]+ikJBox[2])/2,(ikJBox[1]+ikJBox[3])/2);return"ok";},
  tapAlcove(){return ikBox?hk("hit",(ikBox[0]+ikBox[2])/2,(ikBox[1]+ikBox[3])/2):"no box";},box:()=>[ikBox,ikJBox]};
}
