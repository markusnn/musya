{
// ───────────────────────── «Лес за тории» (add-on fo) ─────────────────────────
// An old hand-painted map of the forest behind the house, hidden in fog (a hidden full-screen GAME, opened from the 門 tray
// and the hub). Every night Musya has lantern oil for 2 steps (+1 with a lantern placed at the entrance, +1 in the rain):
// a step clears a fogged cell next to the cleared ones, Musya walks there with her lantern. 14 landmarks with painted
// vignettes and events (finds, mushrooms, known yōkai), the heart of the forest at the top once the map is clear.
// State: S.ext.forest. Art: art/forest_art.py → assets/items/atlas_fomap|fov1|fov2|foi.webp
const FON=56,FO0=52;   // 7×8 cells (100 px on the 700×1040 map, under a 130 px cloud strip); start = the torii, col 3 of the bottom row
const FOV={well:["fov1",0,0],bamboo:["fov1",420,0],temple:["fov1",0,285],jizo:["fov1",420,285],bridge:["fov1",0,570],hotaru:["fov1",420,570],cedar:["fov1",0,855],hermit:["fov1",420,855],
 mush:["fov2",0,0],fox:["fov2",420,0],lotus:["fov2",0,285],stairs:["fov2",420,285],tea:["fov2",0,570],neko:["fov2",420,570],heart:["fov2",0,855]};
const FOIR={fo_mirror:[0,0,120,150],fo_flute:[102,152,200,70],fo_mokugyo:[326,0,160,130],fo_jizo:[122,0,90,140],fo_hotaru:[214,0,110,140],fo_chawan:[630,0,120,90],fo_kasa:[752,0,160,80],fo_lotus:[488,0,140,110],fo_neko:[0,152,100,75],fo_sasabune:[304,152,140,60]};
const FOIN={fo_mirror:["Бронзовое зеркальце","у старого колодца"],fo_flute:["Бамбуковая флейта","в бамбуковой роще"],fo_mokugyo:["Деревянная рыба мокугё","в заброшенном храме"],
 fo_jizo:["Деревянный Дзидзо","у каменного Дзидзо"],fo_hotaru:["Клетка для светлячков","на поляне светлячков"],fo_chawan:["Чаван с золотым швом","в развалинах чайного домика"],
 fo_kasa:["Шляпа отшельника","в хижине отшельника"],fo_lotus:["Лотос в чаше","у пруда с лотосами"],fo_neko:["Камешек-кошка","у кошачьего камня"],fo_sasabune:["Лодочка из листа бамбука","у ручья под мостиком"]};
addItems(Object.keys(FOIR).map(id=>{const r=FOIR[id];return{id,n:FOIN[id][0],c:"Находки из леса",w:r[2],h:r[3],a:"b",p:0,at:["foi",r[0],r[1]],src:"🏮 находка в лесу",hint:"🏮 В лесу за тории, "+FOIN[id][1]};}),{foi:[1000,227]});
STAMPS.push(["fo_first","径","Первая тропа","Найди первое место в лесу за тории"],["fo_half","霧","Полкарты","Разгони туман над половиной лесной карты"],["fo_all","森","Сердце леса","Открой всю карту леса за тории"]);
// landmarks: cell (c,r), name, text; it = a find, food = pantry, mon/who/say = a known yōkai, beast = bestiary key
const FOL=[
 {id:"well",c:1,r:7,jp:"古井戸",n:"Старый колодец",it:"fo_mirror",t:"В колодце стоят звёзды. Из глубины кто-то тихо считает: «…семь, восемь, девять…» — и сбивается. На краю сруба лежит бронзовое зеркальце, тёплое, будто его только что держали в руках."},
 {id:"jizo",c:4,r:6,jp:"地蔵",n:"Каменный Дзидзо",it:"fo_jizo",t:"У тропы стоит Дзидзо в красном слюнявчике — хранитель детей и путников. Кто-то оставил ему рисовый колобок и вертушку. У подножия лежит маленький деревянный Дзидзо: такие дарят тем, кто идёт в туман."},
 {id:"fox",c:6,r:6,jp:"狐穴",n:"Лисья нора",mon:"m_kitsune",beast:"kitsune",who:"Лиса-невеста",food:[["ds_inari",2]],t:"В корнях старого дуба темнеет нора, а над ней пляшут синие лисьи огоньки. Из темноты выходит знакомая лиса.",say:"А, кошка из дома, где угощают. Держи, ещё тёплые. И не ходи за огоньками — заведут."},
 {id:"bamboo",c:0,r:5,jp:"竹林",n:"Бамбуковая роща",it:"fo_flute",t:"Бамбук шумит, как далёкое море. Один стебель светится изнутри — в старой сказке в таком нашли крошечную принцессу. Муся обнюхала его и решила: пусть светит. А у корней лежит забытая флейта."},
 {id:"bridge",c:2,r:5,jp:"小橋",n:"Ручей с мостиком",it:"fo_sasabune",mon:"m_kappa",beast:"kappa",who:"Каппа",t:"Через ручей перекинут горбатый мостик. Из-под него блеснули два глаза и мокрое блюдце на макушке.",say:"Не бойся, я тут лодочки пускаю. Возьми одну — пусть плывёт к твоему дому."},
 {id:"tea",c:3,r:4,jp:"茶室跡",n:"Развалины чайного домика",it:"fo_chawan",t:"От чайного домика остались очаг, столбы да низкая дверца, в которую входят только с поклоном. В золе — чаша, склеенная золотом. Её так берегли, что трещина стала красивее самой чаши."},
 {id:"mush",c:5,r:4,jp:"茸の原",n:"Грибная поляна",food:[["v_shiitake",3],["v_obaketake",1]],t:"Целая поляна грибов. Коричневые — сиитакэ, а маленькие бледные светятся в темноте: это призрачные грибы. Муся набрала полную корзинку и чихнула от грибного духа."},
 {id:"hotaru",c:1,r:3,jp:"蛍の原",n:"Поляна светлячков",it:"fo_hotaru",joy:16,t:"Над травой — сотни светлячков. Старики говорят, это души, которые вернулись посмотреть на лето ещё раз. Муся ловит их лапами и не ловит ни одного — и очень этому рада. В траве стоит пустая клетка: кто-то выпустил всех."},
 {id:"cedar",c:2,r:2,jp:"大杉",n:"Кедр-великан",mon:"m_rg_kodama",beast:"rg_kodama",who:"Кодама",joy:16,t:"Кедр опоясан соломенной верёвкой симэнава с белыми бумажными зигзагами: в таком дереве живёт дух. Муся мяукнула — и лес мяукнул ей в ответ.",say:"Это я, эхо. Триста лет отвечаю всем, кто зовёт. Приходи ещё — мне так редко мяукают."},
 {id:"lotus",c:5,r:2,jp:"蓮池",n:"Пруд с лотосами",it:"fo_lotus",t:"В пруду спят лотосы. Говорят, на рассвете они раскрываются с тихим хлопком, и Муся сидит у воды, ждёт хлопка. У берега в старой чаше плавает цветок — сорванный кем-то и забытый."},
 {id:"hermit",c:0,r:1,jp:"庵",n:"Хижина отшельника",it:"fo_kasa",t:"Хижина пустая, но угли в очаге ещё тлеют, а на крюке висит соломенная шляпа. Рядом записка: «Возьми, если идёшь дальше в туман». Читать Муся не умеет, но поняла всё правильно."},
 {id:"neko",c:6,r:1,jp:"猫石",n:"Кошачий камень",it:"fo_neko",mon:"m_nekomata",beast:"nekomata",who:"Нэкомата",t:"Камень похож на спящую кошку — даже уши есть. На нём сидит нэкомата и вылизывает оба своих хвоста.",say:"Сюда приходят все кошки округи — посидеть, помолчать. Держи камешек: теперь ты своя."},
 {id:"temple",c:1,r:0,jp:"廃寺",n:"Заброшенный храм",it:"fo_mokugyo",t:"Двери заброшенного храма открыты, на полу шуршат листья. В глубине сама по себе горит свеча — уже много лет. На подушке лежит деревянная рыба мокугё. Муся тронула её лапой — тук — и лес притих."},
 {id:"stairs",c:3,r:0,jp:"霧の石段",n:"Туманная лестница",mon:"m_rm_tengu",beast:"rm_tengu",who:"Тэнгу",joy:12,t:"Каменная лестница уходит вверх, в туман, и ступенек на ней больше, чем можно сосчитать. Сверху хлопают крылья: кто-то большой, с длинным носом, смотрит на Мусю.",say:"Наверху — сердце леса. Туда пускают тех, кто обошёл весь лес. Ступай, маленькая, свети."}
];
const FOH={id:"heart",jp:"森の心",n:"Сердце леса",joy:25,t:"На самом верху туман расступается. Над облаками стоят древние тории — старше дома и старше кедра-великана. Отсюда виден весь лес, а далеко внизу — тёплое окошко дома. Муся долго сидит и смотрит. Теперь это и её лес."};
const FOLI={};for(const l of FOL)FOLI[l.r*7+l.c]=l;
const FOAMB=["🍂 Только шорох листьев","🦉 Где-то ухает сова","👣 Чьи-то маленькие следы","🌫 Туман пахнет дождём","🔔 Вдали звякнул колокольчик","🍁 К лапе прилип кленовый лист","🕸 Паутинка вся в росе","🪨 Мох тёплый, как спина кошки"];
function foS(){const f=S.ext.forest||(S.ext.forest={d:"",u:0,rev:[FO0],at:FO0,n:0,fin:0});return f;}
function foLantern(){for(const id in S.placed){const p=S.placed[id],i=IT[id];if(p&&p.r==="entrance"&&i&&(i.c==="Фонари"||i.c==="Светильники"))return true;}return false;}
function foMax(){return 2+(foLantern()?1:0)+(weather.on?1:0);}
function foLeft(){const f=foS();return Math.max(0,foMax()-(f.d===dayKey()?f.u:0));}
function foGot(l){return foS().rev.includes(l.r*7+l.c);}
function foFound(){return FOL.filter(foGot).length;}
function foWaits(){const f=foS();return !petAway()&&f.rev.length<FON&&foLeft()>0;}
function foAdj(i){const c=i%7,r=(i/7)|0,o=[];if(c>0)o.push(i-1);if(c<6)o.push(i+1);if(r>0)o.push(i-7);if(r<7)o.push(i+7);return o;}
function foFront(){const R=new Set(foS().rev),o=[];for(let i=0;i<FON;i++)if(!R.has(i)&&foAdj(i).some(j=>R.has(j)))o.push(i);return o;}
const foIm={};let foFF="";
function foLoad(){if(foLoad.d)return;foLoad.d=1;for(const k of["fomap","fov1","fov2"])ldImg("assets/items/atlas_"+k+".webp",im=>{foIm[k]=im;});atlasImg("foi",im=>{foIm.foi=im;});}
function foFont(){return foFF||(foFF=getComputedStyle(document.body).fontFamily);}
// layout: the map fitted above a status strip
function foLay(G){const W=G.W,H=G.H,bot=Math.max(84,Math.min(112,H*.13)),k=Math.min((W-10)/700,(H-bot-6)/1040),w=700*k,h=1040*k;return{k,x:(W-w)/2,y:Math.max(3,(H-bot-h)/2),w,h};}
function foCell(L,i){const c=i%7,r=(i/7)|0,s=100*L.k;return{cx:L.x+(c+.5)*s,cy:L.y+(130+(r+.5)*100)*L.k,s};}
// fog: blurred cell mask filled with a cloudy texture (rebuilt only when the map changes)
let foTexC=null,foFogC=null;
function foTex(w,h){const c=document.createElement("canvas");c.width=w;c.height=h;const g=c.getContext("2d"),r=rng(77),u=Math.max(.6,w/520);
  g.fillStyle="#68727b";g.fillRect(0,0,w,h);
  const puff=(n,r0,r1,pl,al,ad)=>{for(let i=0;i<n;i++){const x=r()*w,y=r()*h,R=(r0+r()*(r1-r0))*u,l=r()<pl,col=l?"206,212,214":"34,42,54",gr=g.createRadialGradient(x,y,0,x,y,R);
    gr.addColorStop(0,`rgba(${col},${l?al+r()*.25:ad+r()*.2})`);gr.addColorStop(1,`rgba(${col},0)`);g.fillStyle=gr;g.fillRect(x-R,y-R,2*R,2*R);}};
  puff(Math.ceil(w*h/9000),60,150,.5,.18,.22);puff(Math.ceil(w*h/1400),14,50,.64,.2,.12);
  return c;}
function foFog(L,extra){const f=foS(),k=L.k,p=Math.ceil(40*k),w=Math.ceil(L.w)+2*p,h=Math.ceil(L.h)+2*p,c=document.createElement("canvas");c.width=w;c.height=h;const g=c.getContext("2d"),R=new Set(f.rev);
  g.filter=`blur(${Math.max(4,Math.round(15*k))}px)`;g.fillStyle="#fff";
  for(let i=0;i<FON;i++){if(R.has(i)&&i!==extra)continue;const col=i%7,row=(i/7)|0;let x0=p+(col*100-7)*k,y0=p+(130+row*100-7)*k,x1=x0+114*k,y1=y0+114*k;if(col===0)x0=0;if(col===6)x1=w;if(row===0)y0=p+80*k;g.fillRect(x0,y0,x1-x0,y1-y0);}
  if(!f.fin||extra===-2)g.fillRect(0,0,w,p+124*k);
  g.filter="none";g.globalCompositeOperation="source-in";if(!foTexC||foTexC.width!==w||foTexC.height!==h)foTexC=foTex(w,h);g.drawImage(foTexC,0,0);
  return{c,p,key:f.rev.length+"|"+f.fin+"|"+Math.round(L.w)+"|"+Math.round(L.h)};}
function foWrap(g,txt,mw){const out=[];let s="";for(const w of txt.split(" ")){const t=s?s+" "+w:w;if(g.measureText(t).width>mw&&s){out.push(s);s=w;}else s=t;}if(s)out.push(s);return out;}
function foReward(lm){const p=[];if(lm.it&&IT[lm.it])p.push("🎁 "+IT[lm.it].n+" → в «🧺 Вещи»");if(lm.food)p.push("🧺 "+lm.food.filter(([id])=>FOOD[id]).map(([id,n])=>FOOD[id].n+(n>1?" ×"+n:"")).join(", ")+" → в кладовую");
  if(!p.length)p.push(lm.id==="heart"?"⛩ Печать «Сердце леса»":"💗 Муся рада встрече");return p;}
function foGive(lm){disc("forest",lm.id);if(lm.it){S.owned.add(lm.it);disc("forest",lm.it);}
  if(lm.food)for(const [id,n] of lm.food)if(FOOD[id])give(id,n);
  if(lm.beast&&BESTIARY.some(b=>b[0]===lm.beast)&&!ST.seen.includes(lm.beast))ST.seen.push(lm.beast);
  S.needs.joy=clamp(S.needs.joy+(lm.joy||8),0,100);if(lm.id!=="heart")award("fo_first");}
function foSmall(){const r=Math.random();
  if(r<.2){give("v_shiitake");return"🍄 Сиитакэ → в кладовую";}if(r<.25&&FOOD.v_obaketake){give("v_obaketake");return"👻 Призрачный гриб → в кладовую";}
  return FOAMB[Math.floor(Math.random()*FOAMB.length)];}
function foCard(G,id,t){const lm=id==="heart"?FOH:FOL.find(l=>l.id===id);if(!lm)return;const g=G.ctx,cw=Math.min(G.W-20,440),mw=cw-32;
  g.save();g.font=`500 14px ${foFont()}`;const lines=foWrap(g,lm.t,mw);g.font=`italic 500 14px ${foFont()}`;const say=lm.say?foWrap(g,"«"+lm.say+"»",mw):[];g.restore();
  G.st.card={lm,t0:t,lines,say,cw};chime(id==="heart"?[523,659,784,1047,1319]:[784,988,1175]);}
function foStep(G,i,t){const f=foS(),q=G.st,L=foLay(G);if(f.d!==dayKey()){f.d=dayKey();f.u=0;}
  f.u++;f.n=(f.n||0)+1;const from=f.at;f.rev.push(i);f.at=i;
  q.walk={a:from,b:i,t0:t,dur:1};q.fade={t0:t+.5,dur:1.3,old:foFog(L,i)};tone(392,.18,"triangle",.04);setTimeout(()=>tone(523,.2,"sine",.03),180);
  const lm=FOLI[i];if(lm){foGive(lm);q.pend={id:lm.id,at:t+1.55};}else q.later={txt:foSmall(),at:t+1.1,i};
  S.needs.joy=clamp(S.needs.joy+3,0,100);
  if(f.rev.length>=FON/2)award("fo_half");
  if(f.rev.length>=FON&&!f.fin){f.fin=1;foGive(FOH);award("fo_all");q.after="heart";}
  save();hubDot();tabDots();}
function foFx(G,txt,x,y,t){G.st.fx.push({txt,x:clamp(x,110,G.W-110),y,t0:t});}
function foMusya(G,L,t){const f=foS(),q=G.st,w=q.walk;let a=foCell(L,f.at),dir=q.dir||1,mv=false;
  if(w&&t<w.t0+w.dur){const A=foCell(L,w.a),B=foCell(L,w.b),p=clamp((t-w.t0)/w.dur,0,1),e=p*p*(3-2*p);a={cx:A.cx+(B.cx-A.cx)*e,cy:A.cy+(B.cy-A.cy)*e};if(Math.abs(B.cx-A.cx)>1)dir=q.dir=Math.sign(B.cx-A.cx);mv=true;}
  return{x:a.cx,y:a.cy+24*L.k,dir,mv};}
const FO={id:"fo_forest",hidden:true,n:"Лес за тории",tag:"裏の森 · Ура-но мори",bg:"forest",lives:null,time:null,icon:"🏮",lore:"",how:"",
 init(G,t){G.st={fx:[],card:null,walk:null,fade:null,dir:1};foLoad();foFogC=null;},
 step(G,t,dt){const q=G.st;q.fx=q.fx.filter(f=>t-f.t0<2.4);
   if(q.later&&t>q.later.at){const C=foCell(foLay(G),q.later.i);foFx(G,q.later.txt,C.cx,C.cy-20,t);q.later=null;}
   if(q.pend&&t>q.pend.at&&!q.card){foCard(G,q.pend.id,t);q.pend=null;}
   if(q.after&&!q.pend&&!q.card&&(!q.fade||t>q.fade.t0+q.fade.dur)){foCard(G,q.after,t);q.after=null;}},
 draw(G,g,t){const q=G.st,f=foS(),L=foLay(G),k=L.k,W=G.W,H=G.H;
   g.fillStyle="rgba(5,7,9,.62)";g.fillRect(0,0,W,H);
   const M=foIm.fomap;if(!M){textC(g,"Разворачиваем карту…",W/2,H/2,15,"#d8d2c3",500);return;}
   g.save();g.shadowColor="rgba(0,0,0,.75)";g.shadowBlur=22;g.drawImage(M,L.x,L.y,L.w,L.h);g.restore();
   // fog (+ crossfade of the cell being cleared)
   const key=f.rev.length+"|"+f.fin+"|"+Math.round(L.w)+"|"+Math.round(L.h);if(!foFogC||foFogC.key!==key)foFogC=foFog(L,-1);
   const dx=Math.sin(t*.31)*2.5*k,dy=Math.cos(t*.23)*2*k,fd=q.fade,fp=fd?clamp((t-fd.t0)/fd.dur,0,1):1;
   g.save();g.beginPath();g.rect(L.x,L.y,L.w,L.h);g.clip();
   g.globalAlpha=.95;g.drawImage(foFogC.c,L.x-foFogC.p+dx,L.y-foFogC.p+dy);g.globalAlpha=1;
   if(fd&&fp<1){g.globalAlpha=1-fp;g.drawImage(fd.old.c,L.x-fd.old.p+dx,L.y-fd.old.p+dy);g.globalAlpha=1;
     const C=foCell(L,q.walk?q.walk.b:f.at);for(let j=0;j<6;j++){const a=j*1.05+fd.t0,r=(18+46*fp)*k;const x=C.cx+Math.cos(a)*r,y=C.cy+Math.sin(a)*r*.7,gr=g.createRadialGradient(x,y,0,x,y,30*k);
       gr.addColorStop(0,`rgba(220,224,222,${.45*(1-fp)})`);gr.addColorStop(1,"rgba(220,224,222,0)");g.fillStyle=gr;g.fillRect(x-30*k,y-30*k,60*k,60*k);}}
   else if(fd&&fp>=1)q.fade=null;
   for(let j=0;j<3;j++){const R=130*k,x=L.x-R+((t*7*k+j*260*k)%(L.w+2*R)),y=L.y+L.h*(.22+.24*j)+Math.sin(t*.2+j*2)*24*k;   // drifting mist
     g.save();g.translate(x,y);g.scale(1.9,1);const gr=g.createRadialGradient(0,0,0,0,0,R);gr.addColorStop(0,"rgba(196,204,210,.11)");gr.addColorStop(1,"rgba(196,204,210,0)");g.fillStyle=gr;g.fillRect(-R,-R,2*R,2*R);g.restore();}
   g.restore();
   // where Musya can step
   const busy=q.card||(q.walk&&t<q.walk.t0+q.walk.dur+1.4),can=!petAway()&&foLeft()>0&&!busy;
   if(can)for(const i of foFront()){const C=foCell(L,i),a=.5+.3*Math.sin(t*3+i);g.save();g.strokeStyle=`rgba(255,206,130,${a})`;g.lineWidth=2;g.setLineDash([5,5]);g.lineDashOffset=-t*8;g.beginPath();g.arc(C.cx,C.cy,30*k,0,Math.PI*2);g.stroke();g.restore();textC(g,"🐾",C.cx,C.cy,15*Math.max(.8,k*1.4),`rgba(255,226,180,${a})`,500);}
   // night around the lantern
   const P=foMusya(G,L,t),vg=g.createRadialGradient(P.x,P.y,70*k,P.x,P.y,Math.max(L.w,L.h)*.85);vg.addColorStop(0,"rgba(4,6,12,0)");vg.addColorStop(1,"rgba(4,6,12,.5)");g.fillStyle=vg;g.fillRect(L.x,L.y,L.w,L.h);
   if(!petAway()){const R=120*k,lx=P.x+P.dir*17*k,ly=P.y-13*k,fl=1+.06*Math.sin(t*9)+.03*Math.sin(t*23);
     g.save();g.globalCompositeOperation="lighter";const lg=g.createRadialGradient(lx,ly,0,lx,ly,R*fl);lg.addColorStop(0,"rgba(255,170,80,.28)");lg.addColorStop(1,"rgba(255,170,80,0)");g.fillStyle=lg;g.fillRect(lx-R*1.1,ly-R*1.1,R*2.2,R*2.2);g.restore();
     drawCatG(g,P.mv?(P.dir>0?"moveRight":"moveLeft"):"rest",P.mv?Math.floor(t*10)%8:Math.floor(t*2)%2,P.x,P.y,.3*k);
     g.save();g.strokeStyle="#2a1a10";g.lineWidth=1;g.beginPath();g.moveTo(lx,ly-7*k);g.lineTo(lx,ly-12*k);g.stroke();g.fillStyle="#f0a04a";g.beginPath();g.ellipse(lx,ly,5*k,6.5*k,0,0,Math.PI*2);g.fill();g.fillStyle="#1a120c";g.fillRect(lx-3.5*k,ly-7.5*k,7*k,2*k);g.fillRect(lx-3.5*k,ly+5.5*k,7*k,2*k);g.restore();}
   // status strip
   const sy=L.y+L.h+8,mx=foMax(),left=foLeft(),N=foFound();
   let s="";for(let i=0;i<mx;i++)s+=i<left?"🏮":"·";
   textC(g,`Масло на сегодня: ${s}   ·   найдено мест: ${N} из ${FOL.length}`,W/2,sy+12,13,"#e8dcc4",600);
   const hint=petAway()?"🎒 Муся в путешествии — лес подождёт её":f.fin?"Весь лес открыт · нажми на место, чтобы перечитать":left>0?"Выбери туман рядом с открытыми местами":"Масло кончилось — новое будет завтра ночью";
   textC(g,hint,W/2,sy+34,12,"rgba(216,210,195,.72)",500);
   if(!f.fin&&left>0&&!petAway())textC(g,`Фонарь у ворот — ещё шаг, в дождь — ещё один`,W/2,sy+54,11,"rgba(216,210,195,.45)",500);
   for(const x of q.fx){const a=clamp(2.4-(t-x.t0),0,1)*clamp((t-x.t0)*4,0,1),y=x.y-(t-x.t0)*14;g.save();g.globalAlpha=a;g.font=`600 13px ${foFont()}`;const w=g.measureText(x.txt).width+20;g.fillStyle="rgba(14,12,10,.82)";g.beginPath();g.roundRect(x.x-w/2,y-14,w,28,14);g.fill();g.restore();textC(g,x.txt,x.x,y,13,`rgba(245,232,205,${a})`,600);}
   if(q.card)foDrawCard(G,g,t);},
 down(G,x,y,t){const q=G.st,f=foS(),L=foLay(G);
   if(q.card){if(t-q.card.t0>.3)q.card=null;return;}
   if(q.walk&&t<q.walk.t0+q.walk.dur+1.5)return;
   if(x<L.x||x>L.x+L.w||y<L.y||y>L.y+L.h)return;
   const ly=(y-L.y)/L.k,c=Math.floor((x-L.x)/L.k/100),r=Math.floor((ly-130)/100);
   if(ly<130){if(f.fin)foCard(G,"heart",t);else foFx(G,"☁ Вершину скрывают облака",x,y,t);return;}
   if(r>7){foFx(G,"🏠 Дом. Отсюда Муся уходит в лес",x,y,t);return;}
   const i=r*7+c;
   if(f.rev.includes(i)){if(FOLI[i])foCard(G,FOLI[i].id,t);else if(i===FO0)foFx(G,"⛩ Тории за домом",x,y,t);return;}
   if(!foFront().includes(i)){foFx(G,"🌫 Туман густой — ищи место поближе",x,y,t);return;}
   if(petAway()){foFx(G,"🎒 Муся в путешествии",x,y,t);return;}
   if(foLeft()<=0){foFx(G,"🏮 Масло кончилось — до завтра",x,y,t);return;}
   foStep(G,i,t);},
 stat:G=>`🏮 ${foLeft()} · 🗺 ${foFound()}/${FOL.length}`};
GAMES.push(FO);
function foDrawCard(G,g,t){const c=G.st.card,lm=c.lm,a=clamp((t-c.t0)/.35,0,1),W=G.W,H=G.H,cw=c.cw,pad=16,vw=cw-pad*2,vh=vw*285/420,lh=19,rw=foReward(lm),FF=foFont();
  const tot=pad+52+vh+12+c.lines.length*lh+(c.say.length?26+c.say.length*lh:0)+8+rw.length*20+12+40+pad,x0=(W-cw)/2,y0=Math.max(6,(H-tot)/2)+(1-a)*16;
  g.save();g.globalAlpha=a;g.fillStyle="rgba(3,5,7,.8)";g.fillRect(0,0,W,H);
  g.fillStyle="rgba(24,21,18,.97)";g.strokeStyle="rgba(214,186,130,.42)";g.lineWidth=1.5;g.beginPath();g.roundRect(x0,y0,cw,tot,14);g.fill();g.stroke();
  let y=y0+pad+8;jpText(g,lm.jp,W/2,y,14,"#d9b77a");y+=22;textC(g,lm.n,W/2,y,18,"#f1e8d6",700);y+=22;
  const v=FOV[lm.id],im=v&&foIm[v[0]];if(im)g.drawImage(im,v[1],v[2],420,285,x0+pad,y,vw,vh);else{g.fillStyle="#101412";g.fillRect(x0+pad,y,vw,vh);}
  if(lm.mon&&MIMG[lm.mon]){const m=MIMG[lm.mon],mh=vh*.74,mw=mh*m.width/m.height,ap=clamp((t-c.t0-.35)/.8,0,1);g.save();g.globalAlpha=a*ap;g.beginPath();g.rect(x0+pad,y,vw,vh);g.clip();g.drawImage(m,x0+pad+vw-mw-vw*.03,y+vh-mh-vh*.03+(1-ap)*10,mw,mh);g.restore();}
  g.strokeStyle="rgba(214,186,130,.3)";g.lineWidth=1;g.strokeRect(x0+pad,y,vw,vh);y+=vh+12;
  g.textAlign="left";g.textBaseline="top";g.font=`500 14px ${FF}`;g.fillStyle="#ddd6c6";for(const l of c.lines){g.fillText(l,x0+pad,y);y+=lh;}
  if(c.say.length){y+=6;g.font=`700 13px ${FF}`;g.fillStyle="#e7b98a";g.fillText(lm.who,x0+pad,y);y+=20;g.font=`italic 500 14px ${FF}`;g.fillStyle="#efdcc0";for(const l of c.say){g.fillText(l,x0+pad,y);y+=lh;}}
  y+=8;g.font=`600 13px ${FF}`;g.fillStyle="#f3c98b";for(const l of rw){g.fillText(l,x0+pad,y);y+=20;}
  y+=12;btnRect(g,W/2-70,y,140,38,"Дальше",true);g.restore();}
function foOpen(){foLoad();closePanel();openPlace("fo_forest");}
// ───── hooks ─────
document.head.insertAdjacentHTML("beforeend","<style>.fo-mini{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 10px}.fo-mini>span{width:84px;height:57px;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,.5)}.fo-mini>span.off{background:rgba(255,255,255,.05)}</style>");
hook("boot",()=>{setTimeout(foLoad,9000);});
hook("tray",(tray,room)=>{if(room!=="entrance"||(S.trayMode[room]||"play")!=="play")return;const row=tray.querySelector(".items");if(!row)return;const n=foWaits()?foLeft():0;
  const h=`<button class="item wide" data-x="fo:open"><span class="ico">🏮</span><span class="nm">В лес за тории${n?" · "+n:""}</span></button>`,w=row.querySelectorAll('[data-x^="tv:"]');
  if(w.length)w[w.length-1].insertAdjacentHTML("afterend",h);else row.insertAdjacentHTML("afterbegin",h);});
hook("click",k=>{if(!k.startsWith("fo:"))return;if(k==="fo:open")foOpen();return true;});
hook("hub",()=>{const f=foS(),N=foFound(),n=foLeft(),mx=foMax();
  const st=petAway()?"Муся в путешествии — лес подождёт её.":f.fin?`Весь лес открыт, сердце леса найдено. Места на карте можно перечитать.`:`Старая карта леса за домом, почти вся в тумане. Каждую ночь Мусе хватает масла на пару шагов. Сегодня осталось: <b>${n} из ${mx}</b>.`;
  return`<div class="hubc"><h4>🏮 Лес за тории <i>裏の森</i></h4><p>${st}</p><p>Найдено мест: ${N} из ${FOL.length}${f.fin?" · ⛩ сердце леса":""}</p><div class="row"><button class="btn primary" data-x="fo:open">🏮 В лес</button></div></div>`;});
hook("hubDot",()=>foWaits());
hook("tabDot",r=>r==="entrance"&&foWaits());
hook("album",el=>{const got=FOL.filter(foGot);if(!got.length)return;const f=foS(),th=id=>{const v=FOV[id];return`<span style="background:url(assets/items/atlas_${v[0]}.webp) -${v[1]*.2}px -${v[2]*.2}px/168px 228px no-repeat"></span>`;};
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Лес за тории</h3><p class="lead">Мест на лесной карте: ${got.length} из ${FOL.length}${f.fin?" · сердце леса найдено":""}.</p><div class="fo-mini">${FOL.map(l=>foGot(l)?th(l.id):`<span class="off"></span>`).join("")}${f.fin?th("heart"):""}</div><button class="btn" data-x="fo:open" style="margin-bottom:10px">🏮 Открыть карту</button>`);});
X.forest={open:foOpen,state:foS,left:foLeft,
  tap(i){const L=foLay(G),C=i<0?{cx:L.x+L.w/2,cy:L.y+60*L.k}:foCell(L,i);FO.down(G,C.cx,C.cy,now());},
  reveal(list,at){const f=foS();for(const i of list)if(!f.rev.includes(i)){f.rev.push(i);const l=FOLI[i];if(l)foGive(l);}if(at!=null)f.at=at;save();}};
}
