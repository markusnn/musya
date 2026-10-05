{
// ───────────────────────── «Муся замечает новое»: small, rare reactions of Musya to the new things around her ─────────────────────────
// She glances at neighbour cats, follows a flying insect with her eyes (sometimes a quick swipe — never a catch), naps by the
// cricket cage once a night, sways to a melody, looks up at the sky kite, sniffs a waiting chest / a fresh haiku strip / a snowman,
// sits in the kamakura at night, pats the nurikabe's bottom. Read-only use of X.cats, X.insects, X.og, X.kite, X.ob, X.hi, X.snow, X.nu.
// Rhythm: at most one reaction every 40–90 s (one-off things — a new chest, a new strip, a tune, the cage — after 40 s), only while she is
// idle ≥3 s, 10 s after the player's last touch, 4 s after a room change; never away / hidden / in a scene, overlay or dialog.
// S.ext.notice = {cg: night of the cage nap, km: night of the kamakura sit, sm: dayKey of the snowman sniff, ob: ISO week of the chest sniff, hi: haiku id sniffed}
const NT=S.ext.notice||(S.ext.notice={});
const NT_GAP=[40,90],NT_CD={cat:150,bug:60,kite:240,nuri:200,kama:90,melody:600,cage:120,chest:120,haiku:120,snowman:120};
let ntTap=-99,ntLast=now()-15,ntNext=now()+rand(25,45),ntRoomT=now(),ntThen=null,ntFol=null,ntSeq=0,ntAmb=-1e9,ntTu={id:null,t:0,done:0};
const ntCd={},ntLog=[],ntNu={};
document.addEventListener("pointerdown",()=>{ntTap=now();},true);   // any touch of the player (room, tray, buttons) pauses her own life
document.addEventListener("keydown",()=>{ntTap=now();},true);
const ntNight=()=>dayKey(new Date(today().getTime()-(hourNow()<12?864e5:0)));   // the evening a night belongs to
const ntDays=dk=>Math.round((Date.parse(dayKey())-Date.parse(dk))/864e5);
const ntTry=f=>{try{return f();}catch(e){return null;}};
function ntWhy(t=now()){return petAway()?"away":pet.action!=="idle"?"busy:"+pet.action:hk("hideCat")?"hidden":scene.on?"scene":overlaysOpen()?"overlay":
  !$("xdlg").hidden||!$("gdlg").hidden?"dialog":drag.active?"drag":t-ntTap<10?"tap":t-pet.start<3?"fresh":t-ntRoomT<4?"room":ntThen||ntFol?"mine":"";}

// ── small moves: look at a stage point, walk beside a thing (auto: no player events), a delayed step that dies on a touch or a room change
function ntLook(x,y,sec){pointer.x=x;pointer.y=y;pointer.known=true;pet.gazeUntil=now()+sec;}
function ntWalk(x,fn,face){const s=view.s;pet.walkTarget=clamp(x,96*s,view.W-96*s);pet.walkAfter="idle";start("walkto",true);if(face)react(face,1.4);ntThen={fn,room:S.room,t0:now(),until:now()+12};}
const ntBeside=(x,off)=>x+(x>view.W/2?-1:1)*off;   // stand on the side facing the middle of the screen
function ntLater(ms,fn){const r=S.room,t0=now(),q=ntSeq;setTimeout(()=>{if(S.room!==r||ntTap>t0||q!==ntSeq||petAway()||scene.on)return;fn();},ms);}
function ntSniff(x,y,after){ntLook(x,y,2.8);react("👃",1.3);ntLater(1400,()=>{if(pet.action==="idle")react(after,1.6);});}
function ntChirp(){for(let i=0;i<4;i++)setTimeout(()=>tone(rand(820,1020),.07,"triangle",.012),i*120);}   // soft chattering at a cat

// ── the things she notices (each returns a function to run, or null)
function ntCat(){const R=X.cats&&X.cats.rt,B=X.cats&&X.cats.box;if(!R||!B)return null;const ids=Object.keys(R).filter(id=>B[id]&&!R[id].leave&&R[id].mode!=="jump");if(!ids.length)return null;
  return()=>{const id=pick(ids),b=B[id];if(!b)return;ntLook(b[0]+b[2]/2,b[1]+b[3]*.4,3.4);const fr=((X.cats.st().c||{})[id]||{}).fr||0;
    ntLater(500,()=>{if(pet.action!=="idle")return;if(id==="tora"){react("😾",2);return;}react(fr>=1?"😺":"😼",1.8);
      if(Math.random()<.35)ntLater(2700,()=>{if(pet.action==="idle"){start("meow",true);ntChirp();}});});};}
function ntBugNear(){const L=X.insects&&X.insects.list;if(!L)return null;let best=null,bd=1e9;
  for(const b of L){if(b.st!=="fly"||b.leaving||!(b.a>.5)||!(b.sx>0&&b.sx<view.W))continue;const [cx,cy]=stageToCell(b.sx,b.sy),d=Math.hypot(cx-97,(cy-140)*.8);if(cy>-20&&cy<340&&d<230&&d<bd){bd=d;best=b;}}
  return best;}
function ntBug(){const b=ntBugNear();if(!b)return null;return()=>{ntFol={b,t0:now(),until:now()+rand(3,4.5),room:S.room};ntLater(600,()=>{if(ntFol)react("😼",1.4);});};}
function ntFolStep(){const f=ntFol,b=f.b,t=now(),L=(X.insects&&X.insects.list)||[];
  if(S.room!==f.room||ntTap>f.t0||pet.action!=="idle"||!L.includes(b)||b.st==="out"){ntFol=null;return;}
  if(t>f.until){ntFol=null;const [cx,cy]=stageToCell(b.sx,b.sy);if(X.nt.swipe||Math.hypot(cx-97,cy-120)<200&&Math.random()<.45){start("poke",true);react("😼",1.6);}return;}   // a swipe at the air: the player catches, not she
  pointer.x=b.sx;pointer.y=b.sy;pointer.known=true;pet.gazeUntil=t+.35;}
function ntCagePos(){const q=S.placed&&S.placed.mu_kago;if(!q||q.r!==S.room||!DMETA.mu_kago)return null;const it=ipos({id:"mu_kago",x:q.x,y:q.y,item:true});
  curD=DECOR_D.mu_kago??CAT_D;curRow=it.y;const [x0,y0,w,h]=spriteBox(it),p=imgToStage(x0+w/2,y0+h);curD=CAT_D;curRow=null;return p;}
function ntCage(){if(!dayTint()[1]||NT.cg===ntNight())return null;const h=hourNow();if(!(S.needs.energy<85||h>=22||h<5))return null;const p=ntCagePos();if(!p)return null;
  return()=>{ntWalk(ntBeside(p[0],105*view.s),()=>{NT.cg=ntNight();save();const M=X.insects&&X.insects.st(),p2=ntCagePos()||p;ntLook(p2[0],p2[1]-30*view.s,1.4);react("😌",1.4);
    ntLater(1400,()=>{if(pet.action!=="idle")return;start("sleep",true);pet.napUntil=now()+rand(70,120);if(M&&M.cage&&snd.on&&snd.ctx)ntTry(()=>X.insects.song(M.cage,.5));});},"🥱");};}
// music: a tune (gramophone or the hub) once per play; the house's own phrases at most every 10 minutes
function ntTuneTrack(){const st=X.og&&ntTry(()=>X.og.st());if(!st)return null;if(st.tune!==ntTu.id)ntTu={id:st.tune,t:now(),done:0};return st;}
function ntMusic(t,st){if(!st||!(st.L>0)||st.state!=="running")return null;
  if(st.tune){if(ntTu.done||t-ntTu.t<3||st.tune==="takeda"&&S.room==="bedroom"&&dayTint()[1])return null;   // that lullaby puts her to sleep itself (music.js)
    return{k:"tune",e:1,f:()=>{ntTu.done=1;start("music",true);react(st.tune==="takeda"?"😌":"😸",2);}};}
  if(st.q>0&&t-ntAmb>600&&(st.mood==="lullaby"||Math.random()<.3))return{k:"melody",e:0,w:1,f:()=>{ntAmb=now();start("music",true);}};
  return null;}
function ntKite(){if(S.room!=="courtyard"||!X.kite||weather.on||!X.kite.day())return null;const k=X.kite.rk();if(!k)return null;
  return()=>{const k2=X.kite.rk()||k;ntLook(k2[0],k2[1],4.2);ntLater(700,()=>{if(pet.action==="idle")react("😸",1.8);});};}
function ntChest(){const O=X.ob;if(!O||S.room!=="attic"||O.room()!=="attic"||!O.waits()||NT.ob===O.week())return null;const z=O.hit();if(!z)return null;
  return()=>{ntWalk(ntBeside(z.x+z.w/2,z.w/2+60*view.s),()=>{NT.ob=O.week();save();const z2=O.hit()||z;ntSniff(z2.x+z2.w/2,z2.y+z2.h*.3,"😺");});};}
function ntHaiku(){const H=X.hi;if(!H||S.room!=="engawa")return null;const z=H.S(),h=z.l.find(q=>q.id===z.hang);if(!h||NT.hi===h.id||ntDays(h.d)>2)return null;const b=H.box();if(!b)return null;
  return()=>{ntWalk(ntBeside((b[0]+b[2])/2,75*view.s),()=>{NT.hi=h.id;save();const b2=H.box()||b;ntSniff((b2[0]+b2[2])/2,b2[3],"😺");});};}
function ntSnowman(){const Y=X.snow;if(!Y||S.room!=="games"||NT.sm===dayKey())return null;const men=((Y.box&&Y.box.men)||[]).filter(b=>b[4]&&b[4].ml<1);if(!men.length)return null;
  return()=>{const b=pick(men),cx=b[0]+b[2]/2;ntWalk(ntBeside(cx,b[2]/2+50*view.s),()=>{NT.sm=dayKey();save();ntSniff(cx,b[1]+b[3]*.8,"😺");});};}
function ntKama(){const Y=X.snow;if(!Y||S.room!=="games"||!dayTint()[1]||NT.km===ntNight())return null;const s=Y.S();if(!s.km||s.km.ml>=1||Y.sitting())return null;
  return()=>{NT.km=ntNight();save();Y.sit();};}   // snow.js: she walks into the kamakura and sits by the candle (40 s, a tap ends it)
function ntNuri(){const N=X.nu;if(!N||S.room!=="entrance"||!N.waits())return null;const e=N.eve();if(N.st().wait===e||(ntNu[e]||0)>=2)return null;const b=N.box();if(!b)return null;
  return()=>{ntNu[e]=(ntNu[e]||0)+1;ntLook(b.x0+b.w*.3,b.gY-b.h*.06,2.4);react("😼",1.4);
    ntLater(1600,()=>{if(pet.action!=="idle"||!N.waits()||N.st().wait===N.eve()||!$("xdlg").hidden)return;
      if(N.tickle)N.tickle();else{N.anim("tick");start("poke",true);react("😼",1.7);toast("🧱 «Хи-хи… Кто там щекочется?»");}});};}

// ── choosing: one-off things first (after 40 s), otherwise a weighted pick once the 40–90 s pause is over
function ntCands(t,all,st){const out=[],add=(k,e,w,f)=>{if(f&&(all||!(ntCd[k]>t)))out.push({k,e,w,f});};
  const m=ntTry(()=>ntMusic(t,st===undefined?ntTuneTrack():st));if(m)add(m.k,m.e,m.w||1,m.f);
  for(const [k,e,w,fn] of [["cage",1,1,ntCage],["chest",1,1,ntChest],["haiku",1,1,ntHaiku],["snowman",1,1,ntSnowman],["cat",0,2,ntCat],["bug",0,3,ntBug],["kite",0,2,ntKite],["kama",0,2,ntKama],["nuri",0,2,ntNuri]])
    add(k,e,w,ntTry(fn));
  return out;}
function ntPick(L){let r=Math.random()*L.reduce((a,c)=>a+c.w,0);for(const c of L){r-=c.w;if(r<=0)return c;}return L[L.length-1];}
function ntRun(c,t){ntLast=t;ntNext=t+rand(NT_GAP[0],NT_GAP[1]);ntCd[c.k]=t+(NT_CD[c.k]||0);nextAuto=Math.max(nextAuto,t+12);ntLog.push([Math.round(t),c.k,S.room]);if(ntLog.length>40)ntLog.shift();c.f();}

hook("sec",()=>{const t=now(),st=ntTuneTrack();if(ntWhy(t)||t-ntLast<NT_GAP[0])return;
  const C=ntCands(t,false,st);let c=C.find(c=>c.e);if(!c&&t>=ntNext){const L=C.filter(c=>!c.e);if(L.length)c=ntPick(L);}if(c)ntRun(c,t);});
hook("tick",()=>{if(ntThen){const q=ntThen;if(S.room!==q.room||ntTap>q.t0||now()>q.until||pet.action!=="walkto"&&pet.action!=="idle")ntThen=null;else if(pet.action==="idle"){ntThen=null;q.fn();}}
  if(ntFol)ntFolStep();});
hook("room",()=>{const t=now();ntRoomT=t;ntSeq++;ntFol=null;ntCd.cat=Math.max(ntCd.cat||0,t+60);   // cats.js already greets the cats on arrival
  if(ntThen){ntThen=null;if(pet.action==="walkto")start("idle",true);}});

// test handles: go(kind) runs one reaction now (its own conditions still apply), open() lets the rhythm fire on the next second
X.nt={N:NT,log:ntLog,why:()=>ntWhy(),swipe:0,
  go(k){const c=ntCands(now(),true).find(c=>c.k===k);if(!c)return"no:"+k;ntRun(c,now());return"ok:"+k;},
  cands:()=>ntCands(now(),true).map(c=>c.k),open(){ntTap=-99;ntLast=-99;ntNext=now();ntRoomT=-99;},
  st:()=>({next:+(ntNext-now()).toFixed(1),last:+(now()-ntLast).toFixed(1),act:pet.action,face:pet.face&&pet.face.face,gaze:+(pet.gazeUntil-now()).toFixed(1),fol:!!ntFol,then:!!ntThen,why:ntWhy()})};
}
