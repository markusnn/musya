{
// ───────────────────────── Night visitors: yōkai come to things + a treat left on the floor (like Neko Atsume) ─────────────────────────
// A room with the right things placed (S.placed) and a plate with a liked treat → 3–10 min later (real time, also while the game is
// closed) a visitor comes, eats and stays 1–3 h or until tapped. First meeting: a unique gift; later: a small present. S.ext.vis.
const VS=[
 {id:"karakasa",mon:"m_vs_karakasa",n:"Каракаса-обакэ",room:"engawa",h:330,anim:"hop",lure:{c:["Зонтики"],ids:["gf_kitsune_kasa","f_r_753","tk_kasa"],n:1},likes:["ds_tempura","ds_inari","ds_ramen"],gift:"vs_geta",small:["v_shiitake","v_obaketake"],gv:"оставил",
  hint:"Любит, когда на веранде стоят зонтики и есть тэмпура",short:"веранда · зонтик · тэмпура",
  first:"Кап-кап… Прыгал мимо — гляжу, на веранде стоят мои бумажные родичи. И тэмпура! Можно я у вас немножко посохну?",
  later:["Обещают дождь. Самое время прыгать!","Язык у меня длинный, а тэмпура кончилась быстро…","Сто лет простоял в углу. А теперь хожу в гости!"],
  desc:"Старый бумажный зонт, проживший сто лет, открывает глаз, высовывает язык и скачет на одной ноге в гэта. Самый озорной из цукумогами — ожившей утвари эпохи Эдо."},
 {id:"kamaitachi",mon:"m_vs_kamaitachi",n:"Кама-итати",room:"engawa",h:340,anim:"spin",lure:{c:["Фурины"],ids:["v2_furin3","v_suzu"],n:1},likes:["u_any","ds_yakizakana","ds_unadon"],gift:"vs_kusuri",small:["u_ayu","u_yamame"],gv:"оставили",
  hint:"Прилетают с ветром, когда на веранде звенит фурин, и любят рыбу",short:"веранда · фурин · рыба",
  first:"Ш-ш-ших! Фурин звенел так звонко, что мы прилетели на звук. Рыбу съели втроём — не сердись!",
  later:["Первый толкает, второй режет, третий лечит. А рыбу едим все вместе.","Вжух — и мы здесь. Вжух — и нас нет.","Твой фурин поёт, когда мы рядом. Слышишь?"],
  desc:"Три ласки верхом на вихре. Первая сбивает с ног, вторая режет лапами-серпами, третья тут же мажет рану целебной мазью — поэтому порез не болит и не кровит. Предание снежных краёв, особенно Этиго."},
 {id:"bakezori",mon:"m_vs_bakezori",n:"Бакэ-дзори",room:"entrance",h:230,anim:"hop",lure:{ids:["e2_getabako","v_geta","tk_zori","tk_geta","o_slippers","vs_geta"],n:1},likes:["ds_onigiri","ds_yakiimo","ds_edamame"],gift:"vs_waraji",small:["v_imo","v_edamame"],gv:"оставил",
  hint:"Прибегает к воротам, где стоит обувь, и любит онигири",short:"вход · обувь · онигири",
  first:"Карари-кори! У ворот стоит обувь — значит, тут любят ходить в гости. Спасибо за онигири: меня сплели из рисовой соломы, рис мне как родной.",
  later:["Карари-кори, кароринь-корорин!","Три глаза, два зуба — это не про меня, это про гэта.","Береги свою обувь — и она никогда не убежит."],
  desc:"Соломенная сандалия, которую не берегли, оживает и носится ночью по дому с песенкой «Карари-кори, три глаза, два зуба!». Старую обувь чинят и хранят — тогда она не обижается."},
 {id:"kozo",mon:"m_vs_kozo",n:"Хитоцумэ-кодзо",room:"games",h:330,anim:"sway",lure:{c:["Игрушки"],n:2},likes:["ds_dango","ds_takoyaki","ds_tamagoyaki"],gift:"vs_mekago",small:["v_ichigo","v_kabocha"],gv:"оставил",
  hint:"Заглядывает в «Игры», если там лежат две игрушки и есть данго",short:"игры · 2 игрушки · данго",
  first:"Ой! Я только посмотреть на игрушки… Можно одну данго? Честно-честно никому не скажу, как у вас весело.",
  later:["Я записываю в книжечку хорошие дома. Ваш — первый!","Не смотри так. У меня всего один глаз, мне неловко.","Тофу я несу бабушке. А данго — себе."],
  desc:"Одноглазый мальчик-монах. В Эдо верили, что в 8-й день 2-го и 12-го месяца он обходит дома и записывает, кто как живёт. От него вешали у дверей корзину мэкаго: у неё столько «глаз», что кодзо смущается и уходит."},
 {id:"azuki",mon:"m_vs_azuki",n:"Адзуки-арай",room:"courtyard",h:290,anim:"sway",lure:{c:["Посуда"],ids:["c2_well","c2_lotus"],n:1},likes:["ds_daifuku","ds_taiyaki","ds_mochi"],gift:"vs_zaru",small:["v_edamame","v_ichigo"],gv:"оставил",
  hint:"Шуршит у пруда, если там стоит чаша, и любит сладкое с бобами",short:"дворик · чаша · дайфуку",
  first:"Шоки-шоки, шоки-шоки… Чаша у пруда — как раз по мне. И сладкое с бобами! Мою адзуки триста лет, а попробовал впервые.",
  later:["Шоки-шоки… Бобы должны быть чистыми, как лунный свет.","Не говори никому, что я не страшный.","Вода у вас в пруду мягкая. Бобы довольны."],
  desc:"«Шоки-шоки…» — слышно ночью у реки: это Адзуки-арай моет красные бобы в решете. Видели его редко, чаще только слышали. Поёт: «Бобы помыть или человека поймать?» — но на деле очень застенчив."},
 {id:"nuppeppo",mon:"m_vs_nuppeppo",n:"Нуппэппо",room:"onsen",h:230,anim:"blob",lure:{c:["Онсэн"],n:2},likes:["ds_mochi","ds_nimono","ds_miso"],gift:"vs_plush",small:["v_daikon","v_kabocha"],gv:"оставил",
  hint:"Робко приходит в онсэн, где две банные вещи, и обожает моти",short:"онсэн · 2 банные вещи · моти",
  first:"…Здравствуй. Прости, что я такой… бесформенный. В тёплом пару не так стыдно. А моти похож на меня. Он был очень вкусный.",
  later:["…Можно я просто посижу? Я тихо.","…Мне говорили, что я некрасивый. А Муся не убежала.","…Тёплая вода — как объятия."],
  desc:"Бесформенный ком мягкой плоти с намёком на лицо. Бродит ночами у заброшенных храмов, никого не трогает. Торияма Сэкиэн нарисовал его в 1776 году. Этот — застенчивый и похож на моти."},
 {id:"yosuzume",mon:"m_vs_yosuzume",n:"Ёсудзумэ",room:"kitchen",h:118,anim:"birds",night:1,lure:{ids:["k_komedawara","k_hagama","k_onigiri","k_bento"],n:1},likes:["ds_onigiri","ds_edamame","ds_asazuke"],gift:"vs_tsuzura",small:["v_edamame","v_negi"],gv:"оставила",
  hint:"Ночью прилетает на кухню, где пахнет рисом, и клюёт онигири",short:"кухня · ночь · рис · онигири",
  first:"Ти-ти-ти! На кухне пахнет рисом — я и прилетела. Мы, воробьи, помним добро. Помнишь сказку про воробья с отрезанным язычком?",
  later:["Ти-ти-ти! Горные тропы сегодня тихие.","Рисинку тебе, рисинку мне.","Ночью я пою, чтобы путник не сбился с дороги."],
  desc:"Ночной воробей из преданий Эхимэ и Вакаямы. Его «ти-ти-ти» слышат в темноте на горных дорогах; говорят, он летит перед волком-провожатым окури-ōками. В доме это просто милая ночная птичка."},
 {id:"moku",mon:"m_vs_mokumokuren",n:"Мокумокурэн",room:"bedroom",h:400,anim:"blink",y:1196,lure:{c:["Свитки"],ids:["g2_go","v_shogi","b_books"],n:1},likes:["ds_ramen","ds_yakizakana","ds_tamagoyaki"],gift:"vs_goban",small:["v_nasu","v_obaketake"],gv:"оставили",
  hint:"Смотрит из сёдзи спальни, где висит свиток или лежит доска го",short:"спальня · свиток · рамэн",
  first:"Шёпот из-за бумаги: «Мы любим читать через плечо. Свиток у тебя красивый. А тарелка пустая — не спрашивай как».",
  later:["«Мы видели, как Муся спит. Очень сладко».","«Сыграем в го? Мы всегда знаем, куда ты посмотришь».","«Не заклеивай нас. Нам нравится смотреть»."],
  desc:"Глаза в сёдзи старого дома: из каждой клеточки бумаги кто-то смотрит. Торияма Сэкиэн (1781) шутит, что это игрок в го так долго глядел на доску, что глаза остались в клетках. Смотрит, но не трогает."}
];
const VSI={};for(const v of VS)VSI[v.id]=v;
const VS_EYES=[[92,88,22,15],[190,90,17,12],[286,96,24,16],[130,190,15,11],[256,200,26,18],[94,300,20,14],[190,296,14,10],[290,304,19,13],[178,396,23,16]];
const VS_RN={engawa:"Веранда",entrance:"Вход",games:"Игры",courtyard:"Дворик",onsen:"Онсэн",kitchen:"Кухня",bedroom:"Спальня"};
const VS_ROOMS=Object.keys(VS_RN);
Object.assign(MON,{m_vs_karakasa:[300,460],m_vs_bakezori:[280,370],m_vs_kozo:[300,500],m_vs_azuki:[380,400],m_vs_kamaitachi:[400,440],m_vs_nuppeppo:[340,340],m_vs_yosuzume:[270,270],m_vs_mokumokuren:[380,480]});
for(const v of VS)BESTIARY.push(["vs_"+v.id,v.mon,v.n,v.desc]);
STAMPS.push(["vs_first","客","Ночной гость","Встреть ёкая, пришедшего на угощение"],["vs_all","宴","Все ночные гости","Встреть всех восьмерых ночных гостей"]);
{const C="Подарки ночных гостей",A={vs_scroll:[0,0,150,440],vs_mekago:[152,0,180,170],vs_waraji:[334,0,170,150],vs_goban:[506,0,200,150],vs_tsuzura:[708,0,170,140],vs_plush:[0,442,150,130],vs_geta:[152,442,170,110],vs_zaru:[324,442,200,110],vs_kusuri:[526,442,150,100]},
  row=(id,n,a,hint)=>({id,n,c:C,w:A[id][2],h:A[id][3],a,p:0,at:["vs",A[id][0],A[id][1]],src:"👣 ночной гость",hint});
 addItems([row("vs_geta","Гэта на одном зубце","b","Подарок того, кто любит зонтики на веранде"),row("vs_kusuri","Ракушка с мазью кама-итати","b","Оставят те, кто прилетает на звон фурина"),
  row("vs_waraji","Оберег — крошечные варадзи","t","Подарок того, кто прибегает к обуви у ворот"),row("vs_mekago","Корзина мэкаго","b","Оставит одноглазый любитель игрушек"),
  row("vs_zaru","Решето с бобами адзуки","b","Подарок того, кто шуршит у пруда"),row("vs_plush","Плюшевый нуппэппо","b","Оставит застенчивый гость онсэна"),
  row("vs_tsuzura","Корзинка цудзура","b","Подарок ночной птички с кухни"),row("vs_goban","Доска го, что подмигивает","b","Оставят глаза из сёдзи спальни"),
  row("vs_scroll","Свиток «Ночные гости»","t","Награда за встречу со всеми восемью")],{vs:[1000,572]});}
document.head.insertAdjacentHTML("beforeend",`<style>.vs-g{display:grid;grid-template-columns:repeat(auto-fill,minmax(156px,1fr));gap:8px;margin:0 0 12px}.vs-c{display:flex;gap:8px;align-items:center;padding:8px;border-radius:12px;background:#0a0d0c;border:1px solid var(--line)}
.vs-c img{height:64px;width:54px;object-fit:contain;flex:none}.vs-c.no img{filter:brightness(0) opacity(.42)}.vs-c b{display:block;font-size:13px;line-height:1.25}.vs-c small{display:block;font-size:11px;line-height:1.3;color:var(--muted)}
.vs-pk{color:inherit;font:inherit;cursor:pointer}.vs-pk .vs-h{color:var(--sakura)}.story-body .vs-hn{font-size:13px;color:var(--muted);margin:2px 0}</style>`);

// ── state ──
const vsD=()=>{const D=S.ext.vis||(S.ext.vis={r:{},m:{}});D.r=D.r||{};D.m=D.m||{};return D;};
const vsM=id=>vsD().m[id]||(vsD().m[id]={n:0,met:0,miss:0});
const vsLikes=(v,f)=>v.likes.includes(f)||v.likes.includes("u_any")&&EATFISH.includes(f);
function vsLureThing(v){let n=0,first=null;for(const id in S.placed){const q=S.placed[id],i=IT[id];if(q.r!==v.room||!i)continue;if((v.lure.c||[]).includes(i.c)||(v.lure.ids||[]).includes(id)){n++;if(!first)first={id,x:q.x,y:q.y};}}return n>=v.lure.n?first:null;}
const vsHere=()=>Object.values(vsD().r).filter(R=>R.st==="here").length;
const vsMid=()=>(view.W/2-BGM.dx)/BGM.k;
function vsAnchor(room,v){const mid=vsMid(),th=(v?[v]:VS.filter(q=>q.room===room)).map(vsLureThing).find(Boolean);
  if(th)return Math.round(th.x+(th.x<mid?-1:1)*150);return Math.round(mid+(Math.random()<.5?-1:1)*300);}
function vsSmall(v,m){if(m.n%3===0)return null;return pick(v.small);}   // every third later visit brings joy instead of food
// one event at time T (ms): departures turn the plate into "left" (a small present waits); arrivals respect «max 2 in the house»
function vsArrive(room,R,T,live){const v=VSI[R.v];if(vsHere()>=2){const U=Math.min(...Object.values(vsD().r).filter(q=>q.st==="here").map(q=>q.until));R.at=U+rand(3,10)*60000;return;}
  R.st="here";R.until=R.at+rand(60,180)*60000;if(live)R.x=vsAnchor(room,v);else R.fresh=1;const m=vsM(v.id);m.n++;
  if(live){if(S.room===room){vsA[room]={in:now()};if(!petAway())react(m.met?"😺":"🙀",2);tone(660,.5,"sine",.03);setTimeout(()=>tone(990,.6,"sine",.02),160);}else toast(`👣 Кто-то пришёл: «${VS_RN[room]}»`);}}
function vsLeave(room,R,live){R.st="left";R.g=vsSmall(VSI[R.v],vsM(R.v));const m=vsM(R.v);if(!m.met)m.miss++;if(live&&S.room===room)vsGhost[room]={v:R.v,x:R.x,out:now()};}
function vsStep(T=Date.now(),live=true){
  const D=vsD();let ch=false;
  for(let guard=0;guard<24;guard++){   // process due events in time order (the boot catch-up can hold several)
    let best=null;for(const room in D.r){const R=D.r[room],e=R.st==="pend"?R.at:R.st==="here"?R.until:null;if(e!=null&&e<=T&&(!best||e<best[0]))best=[e,room];}
    if(!best)break;const R=D.r[best[1]];ch=true;
    if(R.st==="here")vsLeave(best[1],R,live);
    else if(scene.on&&S.room===best[1])R.at=T+60000;
    else vsArrive(best[1],R,best[0],live);}
  for(const room in D.r){const R=D.r[room];   // plates that can call someone now
    if(R.st==="pend"&&!vsLureThing(VSI[R.v])){R.st="wait";delete R.v;ch=true;}
    if(R.st!=="wait")continue;
    const c=VS.filter(v=>v.room===room&&vsLikes(v,R.f)&&(!v.night||dayTint()[1])&&vsLureThing(v));if(!c.length)continue;
    const v=c.find(q=>!vsM(q.id).met)||pick(c);Object.assign(R,{st:"pend",v:v.id,at:T+rand(3,10)*60000});ch=true;}
  if(ch){save();if(live&&VS_ROOMS.includes(S.room)&&(S.trayMode[S.room]||"play")==="play")ui();}
  return ch;}
// catch up on what happened while the game was closed (before any boot hook asks for the «away» postcard line)
let vsAway=null;{const D=vsD(),before=JSON.stringify(D.r);vsStep(Date.now(),false);
  const came=Object.entries(D.r).filter(([r,R])=>R.fresh&&(R.st==="here"||R.st==="left"));for(const R of Object.values(D.r))delete R.fresh;
  if(came.length&&before!==JSON.stringify(D.r)){const [r,R]=came[0];vsAway={i:"👣",t:`Пока тебя не было, в комнате «${VS_RN[r]}» кто-то съел ${FOOD[R.f]?FOOD[R.f].n.toLowerCase():"угощение"} 👣`};}}

// ── drawing ──
const vsA={},vsGhost={};
function vsPos(room,v,R){   // plate + visitor image coords: near the lure, off Musya, inside what a phone shows
  const mid=vsMid(),l=-BGM.dx/BGM.k,r=(view.W-BGM.dx)/BGM.k,m=MON[v?v.mon:"m_vs_kozo"],hw=(v?v.h:260)*m[0]/m[1]/2*(v&&v.anim==="birds"?2.4:1),cat=70*view.s/BGM.k;
  let side=(R.x??mid+1)<mid?-1:1;if(room==="entrance"&&S.guest&&S.guest.state==="here")side=-1;
  let x=R.x??mid+side*300;const need=cat+hw+10;if((x-mid)*side<need)x=mid+side*need;
  const lo=l+hw+14,hi=r-hw-14;if(lo<hi){x=clamp(x,lo,hi);if(Math.abs(x-mid)<need){const alt=mid-side*need;if(alt>=lo&&alt<=hi){x=alt;side=-side;}}}else x=(l+r)/2;
  const y=v&&v.y||vsFront(room,x,hw);return{x,y,px:clamp(x-side*hw*.55,l+60,r-60),py:Math.min(y+18,1322),side};}
// stand in front of floor things that would hide the visitor (cached for half a second)
const vsFC={};
function vsFront(room,x,hw){const key=room+"|"+Math.round(x),c=vsFC[key],t=now();if(c&&t-c.t<.5)return c.y;let y=1262;
  for(const id in S.placed){const q=S.placed[id],m=DMETA[id];if(q.r!==room||!m||m[2]!=="b")continue;const [qx,qy]=propAt(id,q.x,q.y);if(qx+m[0]/2>x-hw*.8&&qx-m[0]/2<x+hw*.8&&qy>=y-8)y=Math.max(y,qy+12);}
  y=Math.min(y,1330);vsFC[key]={t,y};return y;}
function vsPlate(x,y,f,eaten,t,left){
  const [sx,sy]=imgToStage(x,y,CAT_D),k=BGM.k*1.45;
  ctx.save();ctx.fillStyle="rgba(0,0,0,.3)";ctx.beginPath();ctx.ellipse(sx,sy+4*k,50*k,14*k,0,0,Math.PI*2);ctx.fill();
  ctx.fillStyle="#d8d0bf";ctx.beginPath();ctx.ellipse(sx,sy,46*k,15*k,0,0,Math.PI*2);ctx.fill();ctx.strokeStyle="#34507a";ctx.lineWidth=3*k;ctx.beginPath();ctx.ellipse(sx,sy,40*k,12*k,0,0,Math.PI*2);ctx.stroke();
  ctx.fillStyle="#ebe5d8";ctx.beginPath();ctx.ellipse(sx,sy-1*k,30*k,8*k,0,0,Math.PI*2);ctx.fill();ctx.restore();
  if(!eaten&&f)fDraw(ctx,f,sx,sy-12*k,54*k);
  else{ctx.fillStyle="rgba(170,130,80,.8)";for(let i=0;i<5;i++){ctx.beginPath();ctx.arc(sx+(i*13%29-14)*k,sy+((i*7)%9-4)*k*.6,1.6*k,0,Math.PI*2);ctx.fill();}}
  if(left)drawEmoji(ctx,"🎁",sx,sy-20*k+Math.sin(t*2.4)*3*k,22*view.s,.95);}
function vsBody(v,x,y,t,al){
  const k=BGM.k,[sx,sy]=imgToStage(x,y,CAT_D),w=v.h*MON[v.mon][0]/MON[v.mon][1]*k;
  ctx.save();ctx.globalAlpha=al*.9;ctx.fillStyle="rgba(0,0,0,.28)";ctx.beginPath();ctx.ellipse(sx,sy,w*(v.anim==="birds"?1.6:.42),w*.1,0,0,Math.PI*2);ctx.fill();ctx.restore();
  const a=v.anim;
  if(a==="hop")drawMon(v.mon,x,y-Math.abs(Math.sin(t*3.1))*16,v.h,CAT_D,al,"b",Math.sin(t*3.1)*.05);
  else if(a==="spin")drawMon(v.mon,x+Math.sin(t*5)*8,y-6-Math.sin(t*2)*6,v.h,CAT_D,al,"b",Math.sin(t*3.7)*.035);
  else if(a==="blob")drawMon(v.mon,x,y+Math.sin(t*1.6)*2,v.h*(1+.02*Math.sin(t*1.6)),CAT_D,al);
  else if(a==="birds"){for(const [dx,s,fl,ph] of [[-95,.8,false,1.3],[0,1,false,0],[92,.86,true,2.2]]){const pk=Math.max(0,Math.sin(t*2.3+ph*3))**8;drawMon(v.mon,x+dx,y+(s<1?-8:0),v.h*s,CAT_D,al,"b",(fl?-1:1)*-pk*.35,fl);}}
  else if(a==="blink"){drawMon(v.mon,x,y,v.h,CAT_D,al);const h=v.h*k,W=h*380/480,e=VS_EYES[Math.floor(t/1.7)%VS_EYES.length],u=t%1.7;
    if(u<.2){const ex=sx-W/2+e[0]/380*W,ey=sy-h+e[1]/480*h;ctx.save();ctx.globalAlpha=al;ctx.fillStyle="#cdbf9e";ctx.beginPath();ctx.ellipse(ex,ey,e[2]/380*W*1.12,e[3]/480*h*1.2*Math.sin(u/.2*Math.PI),0,0,Math.PI*2);ctx.fill();ctx.restore();}}
  else drawMon(v.mon,x,y+Math.sin(t*2)*3,v.h,CAT_D,al);}
hook("draw",(t,front)=>{
  if(scene.on)return;const room=S.room,R=vsD().r[room],line=catLineY()+6;
  if(R){const v=R.v&&VSI[R.v],P=vsPos(room,v,R);
    if((P.py>line)===front)vsPlate(P.px,P.py,R.f,R.st==="here"||R.st==="left",t,R.st==="left");
    if(R.st==="here"&&v&&(P.y>line)===front){const A=vsA[room]||(vsA[room]={in:t});vsBody(v,P.x,P.y,t,clamp((t-A.in)/1.4,0,1));}}
  const G=vsGhost[room];if(G){const v=VSI[G.v],al=1-(t-G.out)/1.6;if(al<=0)delete vsGhost[room];else{const P=vsPos(room,v,{x:G.x});if((P.y>line)===front)vsBody(v,P.x,P.y,t,al);}}
});
function vsBox(room,R){const v=VSI[R.v],P=vsPos(room,v,R),[sx,sy]=imgToStage(P.x,P.y,CAT_D),h=v.h*BGM.k*(v.anim==="hop"?1.1:1),w=h*MON[v.mon][0]/MON[v.mon][1]*(v.anim==="birds"?2.6:1);return{x0:sx-w/2,x1:sx+w/2,y0:sy-h,y1:sy+6,P};}
hook("hit",(x,y)=>{
  if(scene.on)return false;const room=S.room,R=vsD().r[room];if(!R)return false;
  if(R.st==="here"){const b=vsBox(room,R);if(x>b.x0&&x<b.x1&&y>b.y0&&y<b.y1){vsMeet(room);return true;}}
  const P=vsPos(room,R.v&&VSI[R.v],R),[px_,py_]=imgToStage(P.px,P.py,CAT_D),k=BGM.k*1.45;
  if(Math.abs(x-px_)<56*k&&y>py_-44*k&&y<py_+20*k){vsPlateTap(room);return true;}
  return false;});

// ── meeting: the dialog, the gift, discovery ──
function vsMeet(room){
  const D=vsD(),R=D.r[room],v=VSI[R.v],m=vsM(v.id);audioInit();let text,img;
  if(!m.met){m.met=Date.now();disc("visitor",v.id);if(!ST.seen.includes("vs_"+v.id))ST.seen.push("vs_"+v.id);S.owned.add(v.gift);loadItem(v.gift);
    text=`${v.first} В подарок ${v.gv}: «${IT[v.gift].n}» — ищи в 🧺 Вещи.`;img=itemThumb(IT[v.gift],72,60);award("vs_first");
    if(VS.every(q=>vsM(q.id).met)&&!S.owned.has("vs_scroll")){S.owned.add("vs_scroll");award("vs_all");text+=" Все восемь гостей встречены — в 🧺 Вещи ждёт свиток «Ночные гости».";}}
  else{const g=vsSmall(v,m);text=pick(v.later)+" ";
    if(g){give(g);text+=`В кладовой теперь: ${FOOD[g].n}.`;img=fThumb(g,60,44);}else{S.needs.joy=clamp(S.needs.joy+15,0,100);text+="От этой встречи на душе тепло: радость +15.";img=`<span style="font-size:34px">💗</span>`;}}
  vsGhost[room]={v:v.id,x:R.x,out:now()+99};delete D.r[room];
  chime([784,988,1318]);if(!petAway())react("😻",2);save();ui();hubDot();
  dlg({head:`${v.n} · ${m.n===1?"первая встреча":"визит "+m.n}`,text,img,ok:"До встречи",onOk:()=>{const G=vsGhost[room];if(G)G.out=now();}});}
function vsPlateTap(room){
  const D=vsD(),R=D.r[room];if(!R)return;audioInit();
  if(R.st==="left"){const v=VSI[R.v],g=R.g;delete D.r[room];
    if(g){give(g);toast(`Кто-то приходил и оставил: ${FOOD[g].n}`);}else{S.needs.joy=clamp(S.needs.joy+10,0,100);toast("Тарелка пустая. Кто-то приходил 👣");}
    sfx("chime");if(!petAway())react(vsM(v.id).met?"😺":"🙀",1.6);save();ui();hubDot();return;}
  if(R.st==="here"){toast("Нажми на гостя — он ждёт");return;}
  dlg({head:"Угощение на полу",text:`На тарелке — ${FOOD[R.f].n.toLowerCase()}. ${R.st==="pend"?"Кажется, кто-то уже почуял запах и спешит сюда…":"Пока никто не пришёл. Гости приходят на то, что любят, и только если в комнате стоят нужные им вещи."}`,
    img:fThumb(R.f,60,44),ok:"Пусть стоит",no:"Убрать",onNo:()=>{give(R.f);delete D.r[room];tone(300,.1,"triangle",.04);save();ui();}});}

// ── the tray button, the treat picker ──
hook("tray",(tray,room)=>{
  if(!VS_ROOMS.includes(room)||(S.trayMode[room]||"play")!=="play"||tray.querySelector('[data-x="vs:tray"]'))return;const R=vsD().r[room];
  const [ico,nm]=!R?["🍡","Оставить угощение"]:R.st==="here"?["👣","Гость пришёл!"]:R.st==="left"?["🎁","Пустая тарелка"]:["🍡","Угощение ждёт"];
  const b=`<button class="item wide" data-x="vs:tray"><span class="ico">${ico}</span><span class="nm">${nm}</span></button>`,row=tray.querySelector(".items");
  if(row)row.insertAdjacentHTML("afterbegin",b);else tray.querySelector(".glist")?.insertAdjacentHTML("beforebegin",`<div class="items">${b}</div>`);});
function vsPicker(){
  const room=S.room,eats=pantryEats(),here=VS.filter(v=>v.room===room);
  const love=f=>here.some(v=>vsM(v.id).met&&vsLikes(v,f));
  const tips=here.map(v=>vsM(v.id).met?`<p class="vs-hn">♥ ${v.n} любит: ${v.likes.map(f=>f==="u_any"?"любую рыбу":FOOD[f].n.toLowerCase()).join(", ")}.</p>`:`<p class="vs-hn">👣 ${v.hint}.</p>`).join("");
  openPanel("Угощение для ночных гостей",`<p class="lead">Тарелка встанет на пол в комнате «${VS_RN[room]}». Гость приходит минут через 3–10 — если любит это угощение и в комнате стоят нужные ему вещи. Можно даже закрыть игру.</p>${tips}
   ${eats.length?`<div class="coll">${eats.map(f=>`<button class="ci on vs-pk" data-x="vs:put:${f}">${fThumb(f,70,44)}<small>${FOOD[f].n}${love(f)?' <span class="vs-h">♥</span>':""}<br>×${S.pantry[f]}</small></button>`).join("")}</div>`
   :`<p class="lead">В кладовой нет готовых блюд и рыбы. Приготовь что-нибудь на кухне (🍳 Готовить) или налови рыбы в пруду во дворике.</p>`}`,"vs_pick");}
hook("click",(key,btn)=>{
  if(!key.startsWith("vs:"))return false;const [,a,arg]=key.split(":"),D=vsD();
  if(a==="tray"){const R=D.r[S.room];if(R)vsPlateTap(S.room);else vsPicker();return true;}
  if(a==="put"){const room=S.room;if(D.r[room]||!have(arg)){closePanel();return true;}take(arg);D.r[room]={f:arg,st:"wait",t:Date.now(),x:vsAnchor(room)};
    closePanel();sfx("pop");toast("Угощение ждёт на полу 🍡");if(!petAway())react("😋",1.4);vsStep();save();ui();return true;}
  if(a==="go"){closePanel();goRoom(arg);return true;}
  return false;});

// ── hooks: time, rooms, dots, hub, album, postcard ──
hook("sec",()=>{vsStep();});
hook("room",id=>{for(const k in vsGhost)delete vsGhost[k];const R=vsD().r[id];if(R&&R.st==="here"&&!scene.on){vsA[id]={in:now()};if(!petAway())setTimeout(()=>react(vsM(R.v).met?"😺":"🙀",2),700);}});
hook("hubDot",()=>Object.values(vsD().r).some(R=>R.st==="here"||R.st==="left"));
hook("tabDot",room=>{const R=vsD().r[room];return !!R&&(R.st==="here"||R.st==="left");});
hook("away",()=>vsAway);
hook("hub",()=>{
  const D=vsD(),met=VS.filter(v=>vsM(v.id).met).length,rs=Object.entries(D.r);
  const now_=rs.filter(([,R])=>R.st==="here").map(([r,R])=>`<b>${VSI[R.v].n}</b> — «${VS_RN[r]}»`),left=rs.filter(([,R])=>R.st==="left").map(([r])=>`«${VS_RN[r]}»`),wait=rs.filter(([,R])=>R.st==="wait"||R.st==="pend").map(([r,R])=>`«${VS_RN[r]}» (${FOOD[R.f].n.toLowerCase()})`);
  const go=[...new Set(rs.filter(([,R])=>R.st==="here"||R.st==="left").map(([r])=>r))];
  return`<div class="hubc"><h4>👣 Ночные гости <i>夜の客</i></h4><p>Ёкаи приходят сами, если в комнате стоят нужные вещи и на полу ждёт угощение (кнопка 🍡 в комнате). Встречено: ${met} из ${VS.length}.</p>
   ${now_.length?`<p>Сейчас в доме: ${now_.join(", ")}.</p>`:""}${left.length?`<p>Пустая тарелка с подарком: ${left.join(", ")}.</p>`:""}${wait.length?`<p>Угощение ждёт: ${wait.join(", ")}.</p>`:""}
   ${VS.filter(v=>!vsM(v.id).met).map(v=>`<p class="vs-hn">👣 ${v.short}</p>`).join("")}
   ${go.length?`<div class="row">${go.map(r=>`<button class="btn primary" data-x="vs:go:${r}">В «${VS_RN[r]}»</button>`).join("")}</div>`:""}</div>`;});
hook("album",el=>{
  const met=VS.filter(v=>vsM(v.id).met).length;
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Ночные гости</h3><p class="lead">Ёкаи, которые приходят на вещи и угощение. Встречено ${met} из ${VS.length}.</p><div class="vs-g">${VS.map(v=>{const m=vsM(v.id);
    return m.met?`<div class="vs-c"><img src="assets/mon/${v.mon}.webp" alt=""><div><b>${v.n}</b><small>«${VS_RN[v.room]}» · визитов: ${m.n}<br>♥ ${v.likes.map(f=>f==="u_any"?"рыба":FOOD[f].n.toLowerCase()).join(", ")}</small></div></div>`
     :`<div class="vs-c no"><img src="assets/mon/${v.mon}.webp" alt=""><div><b>???</b><small>${v.hint}.${m.miss?"<br>Уже приходил, пока тебя не было…":""}</small></div></div>`;}).join("")}</div>`);});

// test handle: X.vs.skip(ms) moves every timer back (time travel), X.vs.put(room,food) leaves a plate, X.vs.come(room) makes the pending guest arrive now
X.vs={VS,D:vsD,step:vsStep,meet:vsMeet,pos:r=>{const R=vsD().r[r];return R&&vsPos(r,R.v&&VSI[R.v],R);},
  skip(ms){for(const R of Object.values(vsD().r))for(const k of ["at","until","t"])if(R[k])R[k]-=ms;vsStep();},
  put(room,f){give(f);take(f);vsD().r[room]={f,st:"wait",t:Date.now(),x:vsAnchor(room)};vsStep();},
  come(room){const R=vsD().r[room];if(R&&R.st==="pend")R.at=Date.now()-1;vsStep();},
  tap(room){const b=vsBox(room,vsD().r[room]),r=cv.getBoundingClientRect();cv.dispatchEvent(new PointerEvent("pointerdown",{clientX:r.left+(b.x0+b.x1)/2,clientY:r.top+(b.y0+b.y1)/2,pointerId:9,bubbles:true}));}};
}
