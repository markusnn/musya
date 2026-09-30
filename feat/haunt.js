{
// ───────────────────────── Одержимая комната (idea #13): once a day a yōkai hides in one room ─────────────────────────
// S.ext.haunt = {day,room,yk,spot,found,wrong,told,n (catches in total),got:[yōkai ids found]}
const HN_ROOMS=["engawa","kitchen","onsen","bedroom","wardrobe","games","entrance","courtyard"];
// Hiding spots in image coords. k: up = rises from behind a horizontal edge at (x,y) · down = hangs head-down below an edge ·
// sl/sr = peeks left/right from behind a vertical edge x, standing on y · water = rises from water · out = seeps out of a painting/steam/dark.
// prop: follows a movable prop (its offset), row: that prop's floor row (same 3D plane as the prop). n: «где» for texts.
const HN_SPOTS={
  engawa:[{x:1398,y:1100,d:.92,k:"sl",n:"за сёдзи"},{x:1246,y:1088,d:.42,k:"sr",s:.6,prop:"p_eng_toro",n:"за каменным фонарём"},
    {x:640,y:330,d:.42,k:"down",n:"в кроне сосны"},{x:560,y:985,d:.42,k:"up",n:"в кустах у веранды"}],
  kitchen:[{x:1265,y:852,d:.8,k:"up",prop:"p_kit_kamado",row:1155,n:"за печкой-камадо"},{x:520,y:636,d:.5,k:"up",n:"за окном"},
    {x:1250,y:432,d:.5,k:"up",s:.8,n:"среди пиал на полке"},{x:1440,y:40,d:.5,k:"down",n:"под потолком у фонаря"}],
  onsen:[{x:1250,y:1070,d:.55,k:"water",n:"в воде онсэна"},{x:600,y:765,d:.28,k:"up",n:"за изгородью"},
    {x:1560,y:915,d:.55,k:"up",n:"в кустах у купальни"},{x:520,y:1020,d:.55,k:"out",n:"в пару над водой"}],
  bedroom:[{x:1250,y:1236,d:.8,k:"up",n:"за футоном"},{x:1100,y:560,d:.4,k:"out",n:"за сёдзи"},
    {x:470,y:1070,d:.5,k:"sr",n:"в нише токонома"},{x:1350,y:62,d:.4,k:"down",n:"под потолком"},{x:405,y:1300,d:.8,k:"sr",prop:"p_bed_andon",row:1305,n:"за андоном"}],
  wardrobe:[{x:1180,y:140,d:.5,k:"up",n:"за ширмой"},{x:640,y:1070,d:.5,k:"sr",n:"за створкой ширмы"},
    {x:700,y:380,d:.5,k:"out",n:"в нарисованной сакуре"},{x:1682,y:1070,d:.5,k:"sr",n:"за краем ширмы"}],
  games:[{x:1200,y:1100,d:.45,k:"sr",n:"за столбом тории"},{x:470,y:490,d:.45,k:"down",n:"на перекладине тории"},
    {x:440,y:1250,d:.8,k:"sr",s:.8,prop:"p_gam_toro0",row:1255,n:"за каменным фонарём"}],
  entrance:[{x:690,y:955,d:.38,k:"sr",n:"за столбом тории"},{x:1060,y:545,d:.38,k:"down",n:"на воротах тории"},
    {x:491,y:1260,d:.85,k:"sr",prop:"p_ent_toro",row:1264,n:"за каменным фонарём"},{x:1500,y:1030,d:.85,k:"up",n:"за чашей для омовения"}],
  courtyard:[{x:1320,y:925,d:.55,k:"up",prop:"p_crt_rock1",n:"за валуном в заводи"},{x:560,y:1060,d:.55,k:"water",n:"в пруду"},
    {x:520,y:520,d:.3,k:"out",n:"за струями водопада"},{x:1250,y:45,d:.95,k:"down",n:"под стрехой"}]
};
const HN_YK={
  warashi:{mon:"m_warashi",n:"Дзасики-вараси",it:"hn_koma",eye:"250,240,232",sign:"sleeve",
    say:["Нашли… Теперь вы водите. Завтра я спрячусь лучше.","Хи-хи. Я только чуть-чуть подвинула вещи. Дому так веселее."]},
  tanuki:{mon:"m_tanuki",n:"Тануки",it:"hn_tokkuri",eye:"255,190,80",sign:"tail",tail:["#9a7248","#3e2a1a"],
    say:["Эх, а я почти превратился в чайник. Ладно, держите на память.","Меня выдал хвост? Опять этот хвост…"]},
  kitsune:{mon:"m_kitsune",n:"Кицунэ",it:"hn_fur",eye:"255,210,90",sign:"tail",tail:["#efe8dc","#e0b070"],
    say:["Зоркая у вас кошка. Лисы таких уважают.","Я просто проходила мимо. С хвостом. Сквозь стену."]},
  kappa:{mon:"m_kappa",n:"Каппа",it:"hn_scale",eye:"230,230,90",sign:"ripple",
    say:["Ой, не трясите — блюдце расплещется! Ваша взяла.","Я искал огурцы. Огурцов нет. Зато нашли меня."]},
  nekomata:{mon:"m_nekomata",n:"Нэкомата",it:"hn_fluff",eye:"190,255,120",sign:"tail2",tail:["#d88a3a","#f2ece2"],
    say:["Мяу. Это я переставила вещи: кошкам виднее, где им стоять.","Два хвоста спрятать труднее, чем один. Ваша взяла."]},
  akaname:{mon:"m_akaname",n:"Аканамэ",it:"hn_claw",eye:"255,220,60",sign:"tongue",
    say:["Я только облизал тут немножко… Зато теперь всё чисто!","Не смотрите так. Грязь сама себя не слижет."]},
  obake:{mon:"m_obake",n:"Тётин-обакэ",it:"hn_wick",eye:"255,245,220",sign:"glow",one:1,
    say:["Тсс… я просто фонарь. Обычный старый фонарь. …Ладно, нашли.","Сто лет висел без дела — вот и ожил. Поиграем ещё?"]},
  rokuro:{mon:"m_rokuro",n:"Рокурокуби",it:"hn_hair",eye:"240,240,255",sign:"hair",scary:1,
    say:["Шея затекла — всё утро выглядывала. Спасибо, что нашли.","Голова тут, а тело спит в соседней комнате. Не будите его."]}
};
const HN_IDS=Object.keys(HN_YK);
// trophies: one small painted thing per yōkai, all in assets/items/atlas_hn.webp (art/haunt_art.py)
const HN_CAT="Трофеи охоты на ёкаев",HN_AT=[["hn_tokkuri","Бутылочка сакэ тануки",110,170,"b",112,0,"tanuki"],["hn_fur","Клочок лисьего меха",150,110,"b",448,0,"kitsune"],
  ["hn_scale","Чешуйка каппы",120,110,"b",600,0,"kappa"],["hn_wick","Фитилёк тётин-обакэ",100,150,"b",224,0,"obake",[50,55]],["hn_hair","Прядь рокурокуби",110,200,"t",0,0,"rokuro"],
  ["hn_fluff","Клубочек шерсти нэкоматы",130,110,"b",722,0,"nekomata"],["hn_koma","Волчок дзасики-вараси",120,130,"b",326,0,"warashi"],["hn_claw","Коготок аканамэ",120,90,"b",854,0,"akaname"]];
addItems(HN_AT.map(([id,n,w,h,a,x,y,yk,glow])=>Object.assign({id,n,c:HN_CAT,w,h,a,p:0,at:["hn",x,y],src:"👻 одержимая комната",hint:hnHint(yk)},glow?{glow}:{})),{hn:[1024,200]});
function hnHint(yk){return({tanuki:"Найди тануки в одержимой комнате",kitsune:"Найди кицунэ в одержимой комнате",kappa:"Найди каппу в одержимой комнате",
  obake:"Найди тётин-обакэ в одержимой комнате",rokuro:"Найди рокурокуби в одержимой комнате",nekomata:"Найди нэкомату в одержимой комнате",
  warashi:"Найди вараси в одержимой комнате",akaname:"Найди аканамэ в одержимой комнате"})[yk];}
STAMPS.push(["hn_first","憑","Охотница на ёкаев","Найди ёкая в одержимой комнате"],["hn_seven","七","Семь проказников","Найди 7 разных ёкаев в одержимых комнатах"],
  ["hn_thirty","狩","Гроза проказников","Найди спрятавшихся ёкаев 30 раз"]);

const hnHash=s=>{let h=2166136261;for(let i=0;i<s.length;i++)h=Math.imul(h^s.charCodeAt(i),16777619);return h>>>0;};
const hnRng=seed=>()=>{seed=(seed+0x6D2B79F5)|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};
const hnRC={};
// room of a day: a fixed walk from 2025-01-01 that never repeats yesterday's room (same on every reload)
function hnRoomFor(dk){if(hnRC[dk])return hnRC[dk];const [y,m,d]=dk.split("-").map(Number),n=Math.round((Date.UTC(y,m-1,d)-Date.UTC(2025,0,1))/864e5);
  let r=hnHash("hn0")%8;if(n<0)r=hnHash(dk)%8;else for(let i=1;i<=n;i++)r=(r+1+hnHash("hn"+i)%7)%8;return hnRC[dk]=HN_ROOMS[r];}
function hnH(){return S.ext.haunt||(S.ext.haunt={day:"",n:0,got:[]});}
function hnRoll(){const h=hnH(),dk=dayKey();if(h.day===dk)return;const R=hnRng(hnHash("hn:"+dk));let room=hnRoomFor(dk);
  if(!ROOMS.some(r=>r.id===room)||hk("tabLock",room))room=HN_ROOMS.find(r=>ROOMS.some(q=>q.id===r)&&!hk("tabLock",r))||"engawa";
  const pool=HN_IDS.filter(y=>S.scary||!HN_YK[y].scary),fresh=pool.filter(y=>!h.got.includes(y)),from=fresh.length?fresh:pool;
  Object.assign(h,{day:dk,room,yk:from[Math.floor(R()*from.length)],spot:Math.floor(R()*HN_SPOTS[room].length),found:0,wrong:0,told:0});save();}
const hnOn=()=>{const h=hnH();return h.day===dayKey()&&S.room===h.room&&!scene.on;};
const rt={inT:0,tellAt:-9,tellKind:0,nextTell:0,nextWob:0,nextFx:0,nextGaze:0,flick:-9,shove:null,rev:null,off:0,debug:false};

// projection of a spot: edge point on stage + stage px per image px at that depth
function hnP(sp){let x=sp.x,y=sp.y,row=sp.row??null;if(sp.prop){const o=vpos[sp.prop]||S.dpos[sp.prop]||[0,0];x+=o[0];y+=o[1];if(row!=null)row+=o[1];}
  curRow=row;const a=imgToStage(x,y,sp.d),b=imgToStage(x+100,y,sp.d);curRow=null;const ks=Math.hypot(b[0]-a[0],b[1]-a[1])/100;
  const hS=300*ks*(sp.s||1),o={up:[0,-.12],down:[0,.12],sl:[-.12,-.72],sr:[.12,-.72],water:[0,-.06],out:[0,0]}[sp.k];
  return{ex:a[0],ey:a[1],ks,hS,tx:a[0]+o[0]*hS,ty:a[1]+o[1]*hS,y};}
function hnVisible(sp){const p=hnP(sp);return p.tx>24&&p.tx<view.W-24&&p.ty>30&&p.ty<view.H-30;}
function hnSpot(){const h=hnH();return HN_SPOTS[h.room][h.spot]||HN_SPOTS[h.room][0];}
function hnMove(avoid){const h=hnH(),L=HN_SPOTS[h.room],c=L.map((s,i)=>i).filter(i=>i!==avoid&&hnVisible(L[i]));if(!c.length)return false;h.spot=pick(c);h.wrong=0;save();return true;}
const hnFront=(sp,p)=>sp.d>CAT_D+.01||(Math.abs(sp.d-CAT_D)<.01&&p.y>catLineY()+6);

// ── sounds (only when scary happenings are on)
const hnSnd=()=>S.scary&&snd.on&&snd.ctx;
function hnKnock(){if(!hnSnd())return;[0,.32].forEach(d=>setTimeout(()=>{tone(92,.14,"triangle",.09);tone(62,.18,"sine",.07);},d*1000));}
function hnGiggle(){if(!hnSnd())return;[1250,1480,1320,1560,1400].forEach((f,i)=>setTimeout(()=>tone(f*(.97+Math.random()*.06),.09,"triangle",.014),i*85));}
function hnCreak(){if(!hnSnd())return;const c=snd.ctx,t=c.currentTime,o=c.createOscillator(),g=c.createGain(),f=c.createBiquadFilter();o.type="sawtooth";
  o.frequency.setValueAtTime(150,t);o.frequency.linearRampToValueAtTime(92,t+.7);f.type="bandpass";f.frequency.value=620;f.Q.value=6;
  g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(.05,t+.08);g.gain.exponentialRampToValueAtTime(.0001,t+.78);o.connect(f);f.connect(g);g.connect(c.destination);o.start(t);o.stop(t+.8);}

// ── every second: time in the room, the day's roll, the house acting up
hook("boot",()=>{hnRoll();});
hook("room",()=>{rt.inT=0;rt.off=0;rt.nextTell=now()+2;rt.nextWob=now()+1.5;rt.nextFx=now()+rand(6,10);rt.nextGaze=0;const h=hnH();
  if(h.day===dayKey()&&S.room===h.room&&!h.found&&!h.told){h.told=1;save();setTimeout(()=>{if(S.room===h.room)toast("Здесь кто-то есть… Вещи сдвинуты");},1600);}});
hook("sec",()=>{hnRoll();const h=hnH();if(!hnOn()||h.found||overlaysOpen()||document.hidden)return;const t=now();rt.inT++;
  if(rt.inT>=5&&!hnVisible(hnSpot())){if(++rt.off>=6){hnMove(-1);rt.off=0;}}else rt.off=0;
  if(t>rt.nextWob){rt.nextWob=t+rand(4,9);const L=roomThings().filter(it=>it.id!==dragId);if(L.length){const it=pick(L);wob[it.id]=t;
    if(Math.random()<.4)rt.shove={id:it.id,t0:t,dx:rand(-16,16),dy:rand(-4,4)};if(hnSnd()&&Math.random()<.3)tone(rand(180,240),.08,"triangle",.03);}}
  if(t>rt.nextFx){rt.nextFx=t+rand(10,20);if(S.scary){rt.flick=t;const r=Math.random();if(r<.3)hnKnock();else if(r<.6)hnGiggle();else if(r<.85)hnCreak();}}
  if(rt.inT>=20&&t>rt.nextGaze&&!petAway()&&pet.action==="idle"&&!rt.rev){rt.nextGaze=t+rand(12,20);const p=hnP(hnSpot());
    pointer.x=p.tx;pointer.y=p.ty;pointer.known=true;pet.gazeUntil=t+4;if(Math.random()<.45)react(S.scary?"🙀":"😼",1.6);rt.tellAt=t+.3;}
  if(t>rt.nextTell&&t-rt.tellAt>1.8){rt.tellAt=t;rt.tellKind++;rt.nextTell=t+rand(3,6);}});
hook("tick",(t,dt)=>{const sv=rt.shove;if(!sv)return;const e=t-sv.t0;if(e>2||!hnOn()){rt.shove=null;return;}const vp=vpos[sv.id];if(!vp||dragId===sv.id)return;
  const env=e<.2?e/.2:Math.max(0,1-(e-.2)/1.6),k=Math.min(.9,dt*11),tg=S.dpos[sv.id]||[0,0];vp[0]=tg[0]+sv.dx*env/(1-k);vp[1]=tg[1]+sv.dy*env/(1-k);});

// ── drawing: tells, the reveal, the flicker
function hnEyes(x,y,r,col,one,al,t){const bl=Math.sin(t*5.3)>.9?.12:1;for(const d of one?[0]:[-1,1]){const gx=x+d*r*1.7,rr=one?r*1.6:r,gr=ctx.createRadialGradient(gx,y,0,gx,y,rr*2.6);
  gr.addColorStop(0,`rgba(${col},${.55*al})`);gr.addColorStop(1,`rgba(${col},0)`);ctx.fillStyle=gr;ctx.fillRect(gx-rr*2.6,y-rr*2.6,rr*5.2,rr*5.2);
  ctx.fillStyle=`rgba(${col},${al})`;ctx.beginPath();ctx.ellipse(gx,y,rr*.75,rr*.5*bl,0,0,Math.PI*2);ctx.fill();ctx.fillStyle=`rgba(10,8,6,${al})`;ctx.beginPath();ctx.ellipse(gx,y,rr*.22,rr*.42*bl,0,0,Math.PI*2);ctx.fill();}}
function hnTail(x,y,dx,dy,L,w,cols,al,t,ph=0){const nx=-dy,ny=dx,wav=Math.sin(t*4+ph)*L*.35,mx=x+dx*L*.5+nx*wav*.5,my=y+dy*L*.5+ny*wav*.5,ex=x+dx*L+nx*wav,ey=y+dy*L+ny*wav;
  ctx.save();ctx.globalAlpha=al;ctx.lineCap="round";ctx.strokeStyle="rgba(255,226,180,.22)";ctx.lineWidth=w*1.8;ctx.beginPath();ctx.moveTo(x,y);ctx.quadraticCurveTo(mx,my,ex,ey);ctx.stroke();ctx.strokeStyle=cols[0];ctx.lineWidth=w;ctx.beginPath();ctx.moveTo(x,y);ctx.quadraticCurveTo(mx,my,ex,ey);ctx.stroke();
  ctx.strokeStyle=cols[1];ctx.lineWidth=w*.95;ctx.beginPath();ctx.moveTo(mix(mx,ex,.45),mix(my,ey,.45));ctx.lineTo(ex,ey);ctx.stroke();ctx.restore();}
function hnTell(sp,p,t){const h=hnH(),Y=HN_YK[h.yk],e=t-rt.tellAt;if(e<0||e>1.6)return;const al=Math.min(1,e/.25,(1.6-e)/.4),r=Math.max(2.6,.03*p.hS);
  const dir={up:[0,-1],down:[0,1],sl:[-1,0],sr:[1,0],water:[0,-1],out:[0,-1]}[sp.k],sign=rt.tellKind%2&&sp.k!=="out"?Y.sign:"eyes";
  if(sign==="eyes"||sign==="glow"){if(sign==="glow"){const g=ctx.createRadialGradient(p.tx,p.ty,0,p.tx,p.ty,p.hS*.35);g.addColorStop(0,`rgba(255,170,90,${.35*al})`);g.addColorStop(1,"rgba(255,170,90,0)");ctx.fillStyle=g;ctx.fillRect(p.tx-p.hS*.35,p.ty-p.hS*.35,p.hS*.7,p.hS*.7);}
    hnEyes(p.tx,p.ty,r,Y.eye,Y.one,al,t);return;}
  const bx=sp.k==="sl"||sp.k==="sr"?p.ex:p.ex+p.hS*.06,by=sp.k==="sl"||sp.k==="sr"?p.ey-p.hS*.18:p.ey;
  if(sign==="tail")hnTail(bx,by,dir[0],dir[1],p.hS*.22,p.hS*.07,Y.tail,al,t);
  else if(sign==="tail2"){hnTail(bx,by,dir[0],dir[1],p.hS*.2,p.hS*.055,Y.tail,al,t);hnTail(bx+p.hS*.05,by,dir[0],dir[1],p.hS*.18,p.hS*.055,[Y.tail[1],Y.tail[0]],al,t,1.7);}
  else if(sign==="ripple"){ctx.save();ctx.strokeStyle=`rgba(200,230,225,${.6*al})`;ctx.lineWidth=1.4;for(let i=0;i<3;i++){const u=((e*.8+i/3)%1);ctx.globalAlpha=1-u;ctx.beginPath();ctx.ellipse(p.tx,p.ty+r*2,p.hS*.05+u*p.hS*.3,(p.hS*.05+u*p.hS*.3)*.28,0,0,Math.PI*2);ctx.stroke();}ctx.restore();hnEyes(p.tx,p.ty,r,Y.eye,0,al*.8,t);}
  else if(sign==="tongue"){const u=Math.max(0,Math.sin(e*7));ctx.save();ctx.globalAlpha=al;ctx.fillStyle="#c9424a";ctx.beginPath();ctx.ellipse(p.tx+dir[0]*p.hS*.08*u,p.ty+dir[1]*p.hS*.08*u+r*2,p.hS*.03,p.hS*.07*u+1,dir[0]?Math.PI/2:0,0,Math.PI*2);ctx.fill();ctx.restore();hnEyes(p.tx,p.ty-r,r,Y.eye,0,al,t);}
  else if(sign==="sleeve"){ctx.save();ctx.globalAlpha=al;const sx=p.tx+dir[0]*p.hS*.02,sy=p.ty+p.hS*.05,w=p.hS*.12,sw=Math.sin(e*3)*w*.15;ctx.fillStyle="#a8262a";ctx.beginPath();ctx.ellipse(sx+sw,sy,w*.6,w,dir[0]*.4,0,Math.PI*2);ctx.fill();
    ctx.fillStyle="rgba(250,230,230,.8)";for(let i=0;i<4;i++){ctx.beginPath();ctx.arc(sx+sw+Math.cos(i*1.7)*w*.35,sy+Math.sin(i*2.3)*w*.6,w*.09,0,Math.PI*2);ctx.fill();}ctx.restore();}
  else if(sign==="hair"){ctx.save();ctx.globalAlpha=al*.9;ctx.strokeStyle="#0a0a0c";ctx.lineWidth=1.2;for(let i=0;i<14;i++){const x0=p.tx+(i-7)*r*.5;ctx.beginPath();ctx.moveTo(x0,p.ty-r*2);ctx.quadraticCurveTo(x0+Math.sin(e*2+i)*r,p.ty+p.hS*.08,x0+Math.sin(i)*r,p.ty+p.hS*.16);ctx.stroke();}ctx.restore();hnEyes(p.tx,p.ty,r*.8,Y.eye,0,al,t);}}
function hnMon(id,x,y,hS,al,rot,anchor){const im=MIMG[id],m=MON[id];if(!im||!m||al<=0)return;const w=m[0]*hS/m[1];ctx.save();ctx.globalAlpha=Math.min(1,al);ctx.translate(x,y);if(rot)ctx.rotate(rot);ctx.drawImage(im,-w/2,anchor==="c"?-hS/2:-hS,w,hS);ctx.restore();}
function hnReveal(sp,p,t){const v=rt.rev,e=t-v.t,Y=HN_YK[v.yk],m=MON[Y.mon];if(!m)return;const u=smooth(clamp(e/1.1,0,1)),tilt=Math.sin(Math.max(0,e-1.1)*2.4)*.07*Math.min(1,Math.max(0,e-1.1)),
    al=e>v.end?Math.max(0,1-(e-v.end)/.6):1,hS=p.hS*(Y.mon==="m_rokuro"?.62:1),w=m[0]*hS/m[1],show=sp.k==="sl"||sp.k==="sr"?.45:.62;
  ctx.save();ctx.beginPath();
  if(sp.k==="up"||sp.k==="water"){ctx.rect(0,0,view.W,p.ey);ctx.clip();hnMon(Y.mon,p.ex,p.ey+hS-show*hS*u,hS,al,tilt,"b");}
  else if(sp.k==="down"){ctx.rect(0,p.ey,view.W,view.H);ctx.clip();hnMon(Y.mon,p.ex,p.ey-hS+show*hS*u,hS,al,Math.PI+tilt,"b");}
  else if(sp.k==="sl"){ctx.rect(0,0,p.ex,view.H);ctx.clip();hnMon(Y.mon,p.ex+w/2-show*w*u,p.ey,hS,al,-.2*u+tilt,"b");}
  else if(sp.k==="sr"){ctx.rect(p.ex,0,view.W,view.H);ctx.clip();hnMon(Y.mon,p.ex-w/2+show*w*u,p.ey,hS,al,.2*u+tilt,"b");}
  else{const sc=.6+.4*u;ctx.rect(0,0,view.W,view.H);ctx.clip();hnMon(Y.mon,p.ex,p.ey,hS*sc,al*u,tilt,"c");}
  ctx.restore();
  if(sp.k==="water"){ctx.save();ctx.strokeStyle=`rgba(200,230,225,${.5*al})`;ctx.lineWidth=1.5;for(let i=0;i<3;i++){const q=((e*.6+i/3)%1);ctx.globalAlpha=(1-q)*al;ctx.beginPath();ctx.ellipse(p.ex,p.ey,w*.35+q*w*.6,(w*.35+q*w*.6)*.22,0,0,Math.PI*2);ctx.stroke();}ctx.restore();}
  if(e<.9||(e>v.end&&e<v.end+.6)){const q=e<.9?e/.9:(e-v.end)/.6;ctx.save();for(let i=0;i<6;i++){const a=i*1.05,R=p.hS*(.12+q*.3),x=p.tx+Math.cos(a)*R,y=p.ty+Math.sin(a)*R*.6,g=ctx.createRadialGradient(x,y,0,x,y,p.hS*.14);
    g.addColorStop(0,`rgba(225,228,222,${.35*(1-q)})`);g.addColorStop(1,"rgba(225,228,222,0)");ctx.fillStyle=g;ctx.fillRect(x-p.hS*.14,y-p.hS*.14,p.hS*.28,p.hS*.28);}ctx.restore();}
  if(e>v.end+.7)rt.rev=null;}
hook("draw",(t,front)=>{const h=hnH();if(!hnOn())return;const L=HN_SPOTS[h.room];
  if(rt.debug&&front)L.forEach((sp,i)=>{const p=hnP(sp);ctx.save();ctx.strokeStyle=i===h.spot?"#ff4":"#4ff";ctx.lineWidth=2;ctx.beginPath();ctx.arc(p.tx,p.ty,Math.max(28,.38*p.hS),0,Math.PI*2);ctx.stroke();
    ctx.fillStyle="#f44";ctx.fillRect(p.ex-3,p.ey-3,6,6);ctx.fillStyle="#fff";ctx.font="bold 12px sans-serif";ctx.fillText(i+" "+sp.k,p.tx+4,p.ty-4);ctx.restore();});
  if(rt.rev){const sp=L[rt.rev.spot],p=hnP(sp);if(hnFront(sp,p)===front)hnReveal(sp,p,t);return;}
  if(h.found)return;const sp=hnSpot(),p=hnP(sp);if(hnFront(sp,p)===front)hnTell(sp,p,t);});
hook("overlay",t=>{if(!S.scary||!hnOn()||hnH().found)return;const e=t-rt.flick;if(e<0||e>.8)return;
  if([.02,.14,.3,.46].some((v,i)=>e>v&&e<v+.05+(i%2)*.05)){ctx.fillStyle="rgba(3,4,8,.42)";ctx.fillRect(0,0,view.W,view.H);}});

// ── taps: the right spot reveals the yōkai, a wrong one only makes it giggle (three wrong taps and it runs to another spot)
hook("hit",(x,y)=>{const h=hnH();if(!hnOn()||h.found||rt.rev)return false;const L=HN_SPOTS[h.room];let best=-1,bd=1e9;
  L.forEach((sp,i)=>{const p=hnP(sp),d=Math.hypot(x-p.tx,y-p.ty);if(d<Math.max(28,.38*p.hS)&&d<bd){bd=d;best=i;}});if(best<0)return false;
  if(best===h.spot){hnFound();return true;}
  const t=now();floatFx.push({g:"💨",x,y,t});if(snd.on&&snd.ctx)tone(300,.1,"triangle",.035);hnGiggle();h.wrong=(h.wrong||0)+1;
  if(h.wrong>=3){if(hnMove(h.spot)){toast("Хи-хи! Ёкай перебежал в другое место");hnCreak();}}else rt.nextTell=Math.min(rt.nextTell,t+1.2);save();return true;});
function hnFound(){const h=hnH(),Y=HN_YK[h.yk],t=now();h.found=1;h.n=(h.n||0)+1;if(!h.got.includes(h.yk))h.got.push(h.yk);
  rt.rev={t,spot:h.spot,yk:h.yk,end:9};sfx("pop");if(!petAway()){react("🙀",1.2);setTimeout(()=>react("😸",2),1500);}
  const p=hnP(hnSpot());pointer.x=p.tx;pointer.y=p.ty;pointer.known=true;pet.gazeUntil=t+6;
  S.needs.joy=clamp(S.needs.joy+12,0,100);disc("haunt",h.yk);if(!ST.seen.includes(h.yk)&&BESTIARY.some(b=>b[0]===h.yk))ST.seen.push(h.yk);
  const got=IT[Y.it]&&!S.owned.has(Y.it)?Y.it:null;if(got)S.owned.add(got);save();
  setTimeout(()=>{chime([784,988,1175]);dlg({head:"Нашёлся: "+Y.n,text:"«"+Y.say[(h.n-1)%Y.say.length]+"»"+(got?" Трофей: "+IT[got].n+".":" Муся довольна — теперь в доме тихо."),
    img:got?`<div style="display:flex;align-items:center;gap:10px">${itemThumb(IT[got],64,64)}<span style="opacity:.8">«🧺 Вещи» → ${HN_CAT}</span></div>`:"",ok:"Ура!"});
    award("hn_first");if(h.got.length>=7)award("hn_seven");if(h.n>=30)award("hn_thirty");},2600);}

// ── where the player sees it: a card in «家 Дом», a dot on 家 and on the room tab — no pop-ups
const hnRoomRu=id=>(ROOMS.find(r=>r.id===id)||{}).ru||id;
hook("hub",()=>{hnRoll();const h=hnH(),Y=HN_YK[h.yk]||{},total=HN_IDS.filter(y=>S.scary||!HN_YK[y].scary||h.got.includes(y)).length;
  const hint=h.found?`Нашёлся ${Y.n}. Завтра спрячется кто-то ещё.`:h.told?"Следи за мелочами: глаза, хвост, шорох. Муся подскажет.":"Ёкай переставил вещи и где-то спрятался.";
  return`<div class="hubc"><h4>👻 Одержимая комната <i>憑き部屋</i></h4><p>${h.found?"Было неспокойно":"Сегодня неспокойно"}: <b>${hnRoomRu(h.room)}</b>. ${hint}</p>`+
    `<p style="opacity:.75;margin:6px 0 0">Найдено ёкаев: ${h.got.length} из ${total} · всего поймано: ${h.n||0}</p>`+
    (h.found?"":`<div class="row"><button class="btn" data-x="hn:go">Пойти туда</button></div>`)+`</div>`;});
hook("click",k=>{if(k!=="hn:go")return false;closePanel();goRoom(hnH().room);return true;});
hook("hubDot",()=>{const h=hnH();return h.day===dayKey()&&!h.found;});
hook("tabDot",r=>{const h=hnH();return h.day===dayKey()&&!h.found&&r===h.room;});

// test handles
X.hn={H:hnH,rt,spots:HN_SPOTS,yk:HN_YK,roomFor:hnRoomFor,
  force(room,yk,spot=0){const h=hnH();Object.assign(h,{day:dayKey(),room,yk:yk||h.yk||"tanuki",spot,found:0,wrong:0,told:0});rt.rev=null;save();},
  pt(i){const h=hnH(),p=hnP(HN_SPOTS[h.room][i??h.spot]),r=cv.getBoundingClientRect();return[Math.round(r.left+p.tx),Math.round(r.top+p.ty)];},
  tap(i){const [x,y]=X.hn.pt(i);cv.dispatchEvent(new PointerEvent("pointerdown",{clientX:x,clientY:y,pointerId:7,bubbles:true}));},
  tell(k){rt.tellAt=now();if(k!=null)rt.tellKind=k;},flick(){rt.flick=now();}};
}
