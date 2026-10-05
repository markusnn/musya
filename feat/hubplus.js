{
// «家 по-новому»: the hub gets «Ждёт сейчас» + folded groups, tab dots only for time-bound things, a calm start without a toast storm.
// Built LAST: wraps core openHub / tabDots / hubDot / toast (function declarations are mutable bindings).
const HP_G=[["daily","Каждый день","毎日"],["sched","По расписанию","予定"],["week","Раз в неделю","週"],["coll","Коллекции и занятия","集"],["home","Дом и Муся","家"],["misc","Прочее","他"]];
const HP_MAP={kamidana:"daily",ema:"daily",cranes:"daily",kanji:"daily",haunt:"daily",sakura:"daily",bonsai:"daily",ikebana:"daily",koi:"daily",birds:"daily",gacha:"daily",rice:"daily",forest:"daily",lanterns:"daily",
  serial:"sched",tea:"sched",shop:"sched",nurikabe:"sched",sumo:"sched",kite:"sched",ryokan:"sched",parade:"sched",stars:"sched",cats:"sched",visitors:"sched",rumors:"sched",kimodameshi:"sched",friends:"sched",holidays:"sched",
  news:"week",mystery:"week",chest:"week",haiku:"week",
  candles:"coll",dreams:"coll",hanafuda:"coll",shadow:"coll",paint:"coll",workshop:"coll",capsule:"coll",daruma:"coll",chronicle:"coll",hide:"coll",insects:"coll",snow:"coll",zen:"coll",
  rooms:"home",rooms2:"home",trust:"home",pet2:"home",music:"home",loom:"home",kimono3d:"home",birthday:"home",travel:"home",seasons:"home",story2:"home",return:"home"};
// tab dots only for what is time-bound or will be missed today; everything else («ещё не пробовал») waits in «Ждёт сейчас»
const HP_TAB=new Set(["lanterns","visitors","rumors","travel","parade","serial","ryokan","friends","tea","ikebana","holidays","cats","mystery","kamidana","rice","nurikabe"]);
const HP_TOP=4,HP_GAP=2500,HP_WIN=12000,HP_AWAY=10*60e3;
const hpLS=(k,v)=>{try{if(v===undefined)return JSON.parse(localStorage.getItem(k)||"{}");localStorage.setItem(k,JSON.stringify(v));}catch(e){return{};}};
const hpTxt=h=>String(h).replace(/<[^>]+>/g,"").replace(/\s+/g," ").trim();
const hpPl=(n,a,b,c)=>{const m=n%10,h=n%100;return m===1&&h!==11?a:m>=2&&m<=4&&(h<12||h>14)?b:c;};
const hpT={boot:0,t0:0,ph:1,col:[],q:[],tm:0,last:0,cur:"",log:[],hid:false,mute:false,bld:false,hidAt:0};
// which add-ons wait right now: blk → 2 (time-bound: an allow-listed tab dot is lit) | 1 (anything else: hubDot or a hidden tab dot)
function hpWaits(){const w={};if(hpT.mute)return w;
  for(const f of HK.tabDot||[]){if(w[f.blk]===2)continue;try{if(ROOMS.some(r=>f(r.id)))w[f.blk]=HP_TAB.has(f.blk)?2:1;}catch(e){}}
  for(const f of HK.hubDot||[]){if(w[f.blk])continue;try{if(f())w[f.blk]=1;}catch(e){}}
  return w;}
// next timed things for the quiet line: first <p> of schedule-like cards that speak about today
function hpSoon(cards){const h=hourNow(),out=[];
  for(const c of cards){if(c.w||c.g!=="sched"&&c.g!=="week")continue;const m=c.h.match(/<h4[^>]*>([\s\S]*?)<\/h4>\s*<p[^>]*>([\s\S]*?)<\/p>/);if(!m)continue;const t=hpTxt(m[2]);
    if(!/сегодня|вечером|ночью|откроется в|в \d{1,2}:\d\d|после \d{1,2}:\d\d/i.test(t)||/пропущ|уже |завтра|послезавтра|недел|пятниц|суббот|воскрес/i.test(t))continue;
    const tm=t.match(/(\d{1,2}):\d\d/),at=tm?+tm[1]:/ночью|после 2\d/i.test(t)?21:/вечером/i.test(t)?18:19;if(at<=h)continue;
    out.push({at,e:(hpTxt(m[1]).split(" ")[0]||"•"),t:t.length>90?t.slice(0,88)+"…":t});}
  return out.sort((a,b)=>a.at-b.at).slice(0,4);}
function hpCalm(cards){const h=hourNow(),S2=hpSoon(cards);
  if(S2.length)return`<p class="hp-calm">В доме тихо. ${h<17&&S2[0].at>=17?"Загляни вечером":"Позже сегодня"}:</p>`+S2.map(s=>`<p class="hp-soon">${/^[\p{L}\d«]/u.test(s.t)?s.e+" ":""}${s.t}</p>`).join("");
  return`<p class="hp-calm">${h>=23||h<5?"В доме тихо — все спят. Загляни утром.":h>=17?"В доме тихо. Можно просто посидеть с Мусей.":"В доме тихо. Загляни вечером: в сумерках к дому приходят гости."}</p>`;}
openHub=function(){
  const w=hpWaits(),cards=[];let i=0;
  for(const f of HK.hub||[]){let h="";try{h=f()||"";}catch(e){console.error("hook hub",e);}if(h)cards.push({b:f.blk,h,w:w[f.blk]||0,g:HP_MAP[f.blk]||"misc",i:i++});}
  const gr=Object.fromEntries(HP_G.map((g,k)=>[g[0],k])),rk=c=>c.w===2?-1:[2,1,0,3,4,5][gr[c.g]];
  const W=cards.filter(c=>c.w).sort((a,b)=>rk(a)-rk(b)||a.i-b.i),n2=W.filter(c=>c.w===2).length,top=new Set(W.slice(0,Math.max(n2,HP_TOP)));
  const go=hpLS("musya-hub-groups"),card=c=>`<div class="hp-c${top.has(c)?" hp-top":c.w?" hp-wt":""}" data-b="${c.b}">${c.h}</div>`;
  let html=`<p class="lead hp-lead">Сверху — что ждёт сейчас, ниже — всё остальное по разделам.</p><h3 class="hp-sh">Ждёт сейчас <i>今</i></h3>`+
    (top.size?[...top].map(card).join(""):hpCalm(cards));
  html+=`<div class="hp-gs">`;for(const [g,ru,jp] of HP_G){const L=cards.filter(c=>c.g===g&&!top.has(c));if(!L.length)continue;const d=L.some(c=>c.w);
    html+=`<div class="hp-g${go[g]?" open":""}" data-g="${g}"><button class="hp-gh" data-hpg="${g}" aria-expanded="${!!go[g]}"><span>${ru}</span><i>${jp}</i><small>${L.length}</small>${d?'<b class="hp-d" aria-label="ждёт"></b>':""}</button><div class="hp-gb">${L.map(card).join("")}</div></div>`;}html+=`</div>`;
  hpT.bld=true;openPanel("Дом Муси",html,"hub");hubFold();
  for(const c of $("xpBody").querySelectorAll(".hp-top>.hubc"))c.classList.add("open");
  hpMO.takeRecords();hpT.bld=false;X.hp.last={top:[...top].map(c=>c.b),wait:W.map(c=>c.b),n:cards.length};};
// a card opened by code (e.g. daruma's dmHome) inside a closed group → open the group too (not remembered)
const hpMO=new MutationObserver(R=>{if(hpT.bld)return;for(const r of R){const c=r.target;if(c.classList&&c.classList.contains("hubc")&&c.classList.contains("open")){const g=c.closest(".hp-g");if(g&&!g.classList.contains("open"))g.classList.add("open");}}});
hpMO.observe($("xpBody"),{subtree:true,attributes:true,attributeFilter:["class"]});
$("xpBody").addEventListener("click",ev=>{const b=ev.target.closest(".hp-gh");if(!b)return;const g=b.parentElement,o=hpLS("musya-hub-groups"),on=g.classList.toggle("open");b.setAttribute("aria-expanded",on);
  if(on)o[g.dataset.g]=1;else delete o[g.dataset.g];hpLS("musya-hub-groups",o);});
// tab dots: core guest + garden stay, add-ons only from the allow-list; the rest only lights 家
tabDots=function(){let hid=false;const F=hpT.mute?[]:HK.tabDot||[];
  for(const b of $("tabs").children){const r=b.dataset.room;if(!r){b.classList.toggle("dot",storyWants());continue;}
    let on=r==="entrance"&&!!S.guest&&S.guest.state==="here"||r==="courtyard"&&gardenRipe()>0;
    for(const f of F){if(on&&hid)break;const ok=HP_TAB.has(f.blk);if(ok?on:hid)continue;let v=false;try{v=f(r);}catch(e){console.error("hook tabDot",e);}if(v){if(ok)on=true;else hid=true;}}
    b.classList.toggle("dot",!!on);}
  hpT.hid=hid;};
hubDot=function(){$("homeBtn").classList.toggle("dot",!hpT.mute&&(!!hk("hubDot")||hpT.hid));};
// toasts: a calm start (collect ~12 s, show one + «ещё N»), then never closer than 2.5 s
const hpCore=toast;
function hpScore(m){if(/Погас\S*\s+(ещё\s+)?(\d+\s+)?свеч|^🕯\s*\d+\s*\/\s*100/i.test(m))return 0;
  if(/пришл|пришёл|прилетел|приплыл|заглянул|стучит|ждёт у|у ворот|у очага|на пороге|в гостях/i.test(m))return 4;
  if(/прид[её]т|придут|заглянет|в гости|на чай|гост|лиса|кицунэ|тануки|каппа|нурикабэ|нэкомата|ёкай/i.test(m))return 3;
  if(/Зажёгся фонарь|\d+\s*\/\s*\d+/i.test(m))return 1;return /«Сюжет|глав[аы] /i.test(m)?2.5:2;}
function hpShow(m){hpT.last=Date.now();hpT.cur=m;hpT.log.push(Math.round(now()*10)/10+"s "+m);if(hpT.log.length>40)hpT.log.shift();hpCore(m);}
function hpPump(){if(hpT.tm||!hpT.q.length)return;const it=hpT.q[0],w=hpT.last+(it.u?800:HP_GAP)-Date.now();
  if(w<=0){hpT.q.shift();hpShow(it.m);hpPump();}else hpT.tm=setTimeout(()=>{hpT.tm=0;hpPump();},w);}
function hpQ(m,u){if(hpT.q.some(x=>x.m===m)||m===hpT.cur&&Date.now()-hpT.last<6000)return;const it={m,u};if(u)hpT.q.unshift(it);else hpT.q.push(it);
  if(hpT.q.length>5){let k=hpT.q.length-1;for(let i=k;i>=0;i--)if(!hpT.q[i].u&&hpScore(hpT.q[i].m)<hpScore(hpT.q[k].m))k=i;hpT.q.splice(k,1);}hpPump();}
// a toast called synchronously from a tap/click/key handler answers the player: never collected, short gap
const hpUser=()=>{const e=window.event;return !!e&&/^(pointer|click|touch|key|mouse)/.test(e.type||"");};
toast=function(msg){const m=String(msg),u=hpUser();if(hpT.ph>0&&!u){if(hpT.col.length<60)hpT.col.push(m);return;}hpQ(m,u);};
function hpFlush(){const L=[...new Set(hpT.col)].filter(m=>hpScore(m)>0);hpT.col=[];
  if(hpT.ph===2){hpT.ph=0;const n=hpT.n+L.length;if(n>0)hpQ(`🔔 В доме ещё ${n} ${hpPl(n,"новость","новости","новостей")} — загляни в 家`);return;}
  if(!L.length){hpT.ph=0;return;}let b=L[0];for(const m of L)if(hpScore(m)>hpScore(b))b=m;
  hpQ(b);hpT.n=L.length-1;if(hpT.n>0){hpT.ph=2;hpT.t2=Date.now()+HP_GAP;}else hpT.ph=0;}
function hpStart(){hpT.t0=Date.now();hpT.ph=1;for(const it of hpT.q)hpT.col.push(it.m);hpT.q=[];clearTimeout(hpT.tm);hpT.tm=0;}
document.addEventListener("visibilitychange",()=>{if(document.hidden)hpT.hidAt=Date.now();else if(hpT.boot&&hpT.hidAt&&Date.now()-hpT.hidAt>HP_AWAY)hpStart();});
hook("boot",()=>{hpT.boot=1;hpT.t0=Date.now();});
hook("sec",()=>{if(!hpT.boot)return;if(hpT.ph===1&&Date.now()-hpT.t0>=HP_WIN)hpFlush();else if(hpT.ph===2&&Date.now()>=hpT.t2)hpFlush();});
document.head.insertAdjacentHTML("beforeend",`<style>
.story-body p.hp-lead{font-size:13px;margin:0 0 6px}
.story-body h3.hp-sh{font-size:22px;margin:4px 0 10px;display:flex;align-items:baseline;gap:8px}.hp-sh i{font-style:normal;font-family:var(--jp);font-size:14px;color:var(--sakura)}
.story-body p.hp-calm{font-size:15px;color:var(--paper);margin:0 0 6px;line-height:1.5}.story-body p.hp-soon{font-size:14px;color:#e6cf9c;margin:2px 0 4px 2px;line-height:1.45}
.hp-c>.hubc{margin-bottom:8px}.hp-top>.hubc{border-color:rgba(238,163,187,.35)}
.hp-gs{margin:16px 0 10px;border-bottom:1px solid var(--line)}.hp-g{border-top:1px solid var(--line);margin:0}
button.hp-gh{display:flex;align-items:center;gap:8px;width:100%;padding:13px 4px;text-align:left;font-family:var(--display);font-size:19px;color:var(--paper)}
.hp-gh i{font-style:normal;font-family:var(--jp);font-size:13px;color:var(--sakura)}
.hp-gh small{font-family:var(--ui);font-size:11.5px;color:var(--muted);background:rgba(216,210,195,.07);border-radius:99px;padding:1px 8px;line-height:1.6}
.hp-gh b.hp-d,.hp-wt>.hubc>h4::before{content:"";flex:none;width:7px;height:7px;border-radius:50%;background:var(--sakura);box-shadow:0 0 6px var(--sakura)}
.hp-gh::after{content:"▸";margin-left:auto;color:var(--muted);font-family:var(--ui);font-size:14px}.hp-g.open>.hp-gh::after{content:"▾"}
.hp-g:not(.open)>.hp-gb{display:none}.hp-gb{padding:0 0 6px}
</style>`);
X.hp={log:hpT.log,st:hpT,waits:hpWaits,score:hpScore,away:hpStart,get col(){return hpT.col.slice();},mute(v){hpT.mute=!!v;hubDot();tabDots();}};
}
