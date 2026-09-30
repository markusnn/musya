{
// ───────────────────────── «Доверие Муси»: care over time unlocks new habits ─────────────────────────
// Points come from petting, feeding, bathing, play, mini-games, time together and daily visits (daily caps, never decay).
// Every level adds a habit made of existing poses and wordless bubbles; she never talks.
const TS_LV=[["Осторожная",0],["Любопытная",30],["Доверчивая",100],["Ласковая",210],["Преданная",370],["Неразлучная",600],["Родная душа",900]];
const TS_DO=[
 ["Пока присматривается к тебе издалека.",""],
 ["Чаще смотрит на тебя и медленно моргает 💗 — по-кошачьи это значит «я тебе верю».","что-то про её взгляд…"],
 ["Выходит встречать, когда ты открываешь игру.","что-то случится, когда ты придёшь домой…"],
 ["Иногда приносит тебе свою игрушку.","Муся хочет чем-то с тобой поделиться…"],
 ["Засыпает, если долго-долго гладить её по голове.","если гладить её очень долго…"],
 ["Дольше ходит за пальцем и ластится, когда вы входите в комнату.","ей совсем не хочется отходить от тебя…"],
 ["Мурлычет от одного касания и засыпает с 💗.","самое тёплое — в самом конце."]];
const TS_CAP={visit:18,pet:16,food:12,bath:10,play:12,game:10,time:8,sleep:3,wear:3},TS_TOYS=["tm_red","tm_blue","ty_mouse","ty_yarn_r","ty_yarn_b","ty_suzu","ty_tsuru"];
const T=S.ext.trust||(S.ext.trust={p:0,lv:1,day:"",days:0,cd:"",c:{}});
document.head.insertAdjacentHTML("beforeend",`<style>
.ts-lv{font-size:15px!important}.ts-lv b{color:var(--sakura);font-family:var(--display);font-size:22px;font-weight:700;margin-right:6px}
.ts-bar{height:4px;border-radius:2px;background:rgba(216,210,195,.1);overflow:hidden;margin:6px 0 8px}.ts-bar i{display:block;height:100%;background:linear-gradient(90deg,#c9738f,#eea3bb)}
.ts-how{color:var(--muted);font-size:13px!important}.ts-list{list-style:none;margin:8px 0 0;padding:0;display:grid;gap:7px}
.ts-list li{font-size:13.5px;line-height:1.45;color:var(--paper);padding-left:22px;position:relative}.ts-list li::before{content:"💗";position:absolute;left:0;top:0;font-size:12px}
.ts-list li b{color:var(--sakura);font-weight:600;margin-right:5px}.ts-list li.next{color:var(--muted)}.ts-list li.next::before{content:"🔒";opacity:.7}.ts-list li.next b{color:var(--muted)}
</style>`);
const tsName=L=>TS_LV[clamp(L,1,7)-1][0];
function tsToday(){return T.cd===dayKey()?Object.values(T.c).reduce((a,b)=>a+b,0):0;}
function tsGain(k,v){const d=dayKey();if(T.cd!==d){T.cd=d;T.c={};}const used=T.c[k]||0,g=Math.min(v,(TS_CAP[k]||10)-used);if(g<=0)return;T.c[k]=used+g;T.p+=g;tsLevel(false);}
function tsLevel(quiet){let up=0;while(T.lv<7&&T.p>=TS_LV[T.lv][1]){T.lv++;up=T.lv;disc("trust","lv"+T.lv);}
  if(!up)return;save();if(quiet)return;setTimeout(()=>{toast("💗 Муся доверяет тебе больше: "+tsName(up));chime([784,988,1318]);if(!petAway())burst(10);},700);}
function tsVisit(first){const d=dayKey();if(T.day!==d){T.day=d;T.days++;tsGain("visit",12);}else if(first)tsGain("visit",3);}

// ── habits ──
const ts={blinkN:now()+6,toyN:now()+rand(100,200),purrT:0,heartAt:0,sleepSeen:-1,poke:0,greet:0,toy:null,roomT:-99,curS:-1,hidAt:0,dozeOK:0};
const tsFree=()=>!petAway()&&!scene.on&&!overlaysOpen()&&!drag.active;
function tsGreet(){if(T.lv<3||!tsFree()||pet.action!=="idle")return false;const s=view.s,side=Math.random()<.5?-1:1;
  pet.x=side<0?-80*s:view.W+80*s;pet.home=pet.x;pet.walkTarget=clamp(view.W/2+rand(-30,30)*s,96*s,view.W-96*s);pet.walkAfter="idle";start("walkto",true);pet.heading=-side;ts.greet=now();return true;}
function tsToy(){const id=pick(TS_TOYS);loadItem(id);start("gift",true);ts.toy={id,t0:now()};}
function tsTick(t){
  if(petAway()||scene.on)return;const a=pet.action,L=T.lv;
  if(ts.poke){if(a==="poke"){ts.poke=0;start("purr",true);react("💗",1.8);return;}if(t-ts.poke>.6)ts.poke=0;}
  if(ts.greet){if(a==="idle"&&t-ts.greet>.5){ts.greet=0;const g=L>=6?"knead":L>=5?"purr":"meow";start(g,true);if(g!=="meow")react("💗",2.2);const [x,y]=cellToStage(97,190);floatFx.push({g:"💗",x,y,t});}
    else if(a!=="walkto"&&a!=="idle"||t-ts.greet>12)ts.greet=0;return;}
  if(a==="sleep"&&pet.start!==ts.sleepSeen){ts.sleepSeen=pet.start;if(L>=7&&Math.random()<.6)ts.heartAt=t+3.4;}
  if(ts.heartAt&&t>ts.heartAt){ts.heartAt=0;if(pet.action==="sleep")react("💗",3.4);}
  // 5: a long stroke — when the hand lifts after ~15 s of purring, she dozes off
  if(L>=5&&a==="purr"&&!pet.auto){if(t-strokeT<1)ts.purrT=ts.purrT||t;if(ts.purrT&&t-ts.purrT>15&&t-strokeT>.7&&!drag.active){ts.purrT=0;start("sleep",true);pet.napUntil=t+rand(30,45);ts.heartAt=t+3.2;return;}}
  else ts.purrT=0;
  // 2: slow blinks at you
  if(L>=2&&a==="idle"&&pet.idle.kind==="none"&&t>ts.blinkN&&t-pet.start>2){ts.blinkN=t+rand(L>=6?6:8,L>=6?12:16);if(Math.random()<.8){pet.idle.kind="slow";pet.idle.start=t;pet.idle.next=t+idleLen.slow+2.4;}}
  // 4: brings a toy now and then, when nobody is fussing over her
  if(L>=4&&a==="idle"&&t>ts.toyN&&t-pet.start>5&&t-pet.lastInput>8&&tsFree()){ts.toyN=t+rand(240,420);tsToy();return;}
  // 6: follows the finger longer
  if(L>=6&&a==="cursor"&&!pet.auto&&ts.curS!==pet.start){pet.start+=8;ts.curS=pet.start;}
}
function tsDrawToy(t,front){const q=ts.toy;if(!front||!q||petAway())return;const e=t-q.t0;if(pet.action!=="gift"||e>9.6){ts.toy=null;return;}if(e<2.5)return;
  const al=clamp(Math.min((e-2.5)/.35,(9.6-e)/.6),0,1),im=DIMG[q.id],i=IT[q.id],s=view.s,[x,y]=cellToStage(pet.heading>=0?150:44,8),hh=42*s,ww=i?hh*i.w/i.h:hh;
  ctx.save();ctx.globalAlpha=al;ctx.fillStyle="rgba(0,0,0,.28)";ctx.beginPath();ctx.ellipse(x,y,ww*.42,5*s,0,0,7);ctx.fill();
  if(im)ctx.drawImage(im,x-ww/2,y-hh+2*s,ww,hh);else drawEmoji(ctx,"🧶",x,y-hh/2,hh);ctx.restore();}

// ── hooks ──
hook("boot",()=>{if(!T.init){T.init=1;T.p=Math.max(T.p,Math.min(100,ST.got.length*6+(QS.done?30:0)));tsLevel(true);}   // she already knows a player who has been here
  tsVisit(!saved.t||Date.now()-saved.t>36e5);setTimeout(tsGreet,1500);});
hook("sec",()=>{if(T.day!==dayKey())tsVisit(false);
  if(document.hidden){if(!ts.hidAt)ts.hidAt=Date.now();return;}if(ts.hidAt){const gone=Date.now()-ts.hidAt;ts.hidAt=0;if(gone>20*60e3)setTimeout(tsGreet,900);}
  if(!petAway()&&(T.sec=(T.sec||0)+1)>=180){T.sec=0;tsGain("time",1);}});
hook("ev",(ev,d)=>{
  if(ev==="act"){if(d==="purr")tsGain("pet",2);else if(PLAYS.includes(d)||d==="meow"||d==="knead")tsGain("play",1);if(d==="poke"&&T.lv>=7&&!petAway())ts.poke=now();}
  else if(ev==="food")tsGain("food",3);else if(ev==="bath")tsGain("bath",5);else if(ev==="towel")tsGain("bath",1);else if(ev==="game")tsGain("game",2);
  else if(ev==="lamp"&&d)tsGain("sleep",3);else if(ev==="wear")tsGain("wear",1);});
hook("tick",tsTick);
hook("draw",tsDrawToy);
hook("room",()=>{const t=now();if(T.lv<6||t-ts.roomT<90||Math.random()>.5)return;ts.roomT=t;setTimeout(()=>{if(tsFree()&&pet.action==="idle"){start("knead",true);react("💗",1.8);}},1100);});
hook("hub",()=>{const L=T.lv,lo=TS_LV[L-1][1],hi=L<7?TS_LV[L][1]:lo,pct=L<7?Math.round((T.p-lo)/(hi-lo)*100):100,td=tsToday();
  const list=TS_DO.map(([d,h],i)=>i<L?`<li><b>${TS_LV[i][0]}.</b>${d}</li>`:i===L?`<li class="next"><b>???</b>Подсказка: ${h}</li>`:"").join("");
  return`<div class="hubc"><h4>💗 Доверие Муси <i>信頼</i></h4><p class="ts-lv"><b>${tsName(L)}</b>${L<7?`уровень ${L} из 7`:"Муся доверяет тебе целиком"}</p>
   <div class="ts-bar"><i style="width:${clamp(pct,2,100)}%"></i></div>
   <p class="ts-how">Доверие растёт от заботы: гладь, корми, купай, играй — и заходи каждый день.${td?` Сегодня: +${td}.`:""}</p><ul class="ts-list">${list}</ul></div>`;});
X.ts={name:id=>tsName(+String(id).replace(/\D/g,"")||1),lv:()=>T.lv,st:T,greet:tsGreet,toy:tsToy,gain:tsGain,
  set(p){T.p=p;T.init=1;tsLevel(true);}};
}
