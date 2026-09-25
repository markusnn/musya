// ───────────────────────── Touchable, movable decor ─────────────────────────
const wob={},boost={},floatFx=[];let koiGust=-9,shishiOff=0;
function ipos(it){const d=S.dpos[it.id]||[0,0];return Object.assign({},it,{x:it.x+d[0],y:it.y+d[1]});}
function wobAng(id,t){const e=t-(wob[id]??-9);return e<1.4?.14*Math.sin(e*16)*Math.exp(-e*3.2):0;}
function spriteBox(it){const m=DMETA[it.id],x0=m[2]==="l"?it.x:it.x-m[0]/2,y0=m[2]==="t"?it.y:m[2]==="c"||m[2]==="l"?it.y-m[1]/2:it.y-m[1];return[x0,y0,m[0],m[1]];}
function decorHit(x,y){const room=DECOR[S.room];if(!room)return null;const sel=S.decor[S.room]||{};let hit=null;
  for(const slot of room){const it0=slot.items.find(i=>i.id===sel[slot.k]);if(!it0)continue;const it=ipos(it0),[x0,y0,w,h]=spriteBox(it);
    const [ax,ay]=imgToStage(x0+w*.1,y0+h*.06),[bx,by]=imgToStage(x0+w*(it.koi?3.4:.9),y0+h*(it.koi?.45:.97));
    if(x>=ax&&x<=bx&&y>=ay&&y<=by)hit={it0,it,slot};}
  return hit;}
function fxAt(it,glyphs,n=3){const [x0,y0,w,h]=spriteBox(it),[sx,sy]=imgToStage(x0+w/2,y0+h*.35),t=now();for(let i=0;i<n;i++)floatFx.push({g:pick(glyphs),x:sx+rand(-24,24)*view.s,y:sy+rand(-10,10)*view.s,t:t+i*.1});}
function petalsAt(it,n=14){const [x0,y0,w,h]=spriteBox(it),[sx,sy]=imgToStage(x0+w/2,y0+h*.3);for(let i=0;i<n;i++)sakura.list.push({x:sx+rand(-40,40)*view.s,y:sy+rand(-20,20)*view.s,vx:rand(-40,40),vy:rand(-50,10),rot:rand(0,6),vr:rand(-3,3),size:rand(4,7)*view.s,ph:rand(0,6),life:rand(2.5,4)});}
function splashAt(it,n=30){const [x0,y0,w,h]=spriteBox(it),[sx,sy]=imgToStage(x0+w/2,y0+h*.3);for(let i=0;i<n;i++)pet.drops.push({x:sx+rand(-30,30)*view.s,y:sy,vx:rand(-60,60),vy:rand(-260,-80),a:1});sfx("splash");}
function walkTo(it,after,face){pet.walkTarget=clamp(imgToStage(it.x,0)[0],96*view.s,view.W-96*view.s);pet.walkAfter=after;start("walkto");if(face)react(face,1.6);}
function chime(notes){notes.forEach((f,i)=>setTimeout(()=>tone(f,1.1,"sine",.03),i*120));}
function decorTap(h){
  const it=h.it,id=it.id,t=now();wob[id]=t;boost[id]=t;audioInit();S.needs.joy=clamp(S.needs.joy+1,0,100);
  const P=id.replace(/^d_/,"");
  if(P.startsWith("furin")){chime(P==="furin_iron"?[1320,1760,1568]:[2093,2637,2349]);fxAt(it,["♪","♫"],3);react("😺",1.4);}
  else if(["andon","chochin","yukimi"].includes(P)){S.lightsOff[id]=!S.lightsOff[id];tone(S.lightsOff[id]?300:600,.08,"square",.04);react(S.lightsOff[id]?"🙀":"😸",1.2);save();}
  else if(["ikebana","sakura_tree","ume"].includes(P)){petalsAt(it,16);tone(900,.4,"sine",.03);react("😻",1.6);}
  else if(["bonsai","kokedama","bamboo","kiku"].includes(P)){fxAt(it,["🍃","🍂"],4);react("😼",1.2);}
  else if(P.startsWith("zab")){walkTo(it,"knead","😽");}
  else if(P.startsWith("futon")){walkTo(it,"sleep","😴");}
  else if(P==="koi_pole"){koiGust=t;tone(200,.6,"triangle",.03);react("😺",1.4);}
  else if(P==="tsukubai"||P==="okeya"){splashAt(it,24);react("😸",1.2);}
  else if(P==="towels"){S.needs.clean=clamp(S.needs.clean+3,0,100);walkTo(it,"purr","😽");}
  else if(P==="shishi_base"){shishiOff=t-5.55;}
  else if(P==="kaeru"){tone(190,.07,"square",.05);setTimeout(()=>tone(170,.1,"square",.05),110);fxAt(it,["♪"],2);react("😹",1.3);}
  else if(["yuzu","petals","sake"].includes(P)){splashAt(it,10);if(P==="sake")react("😹",1.4);}
  else if(P.startsWith("scroll")){fxAt(it,P==="scroll_neko"?["😺","💗"]:["✨"],2);}
  else if(P==="daruma"){wob[id]=t-.05;fxAt(it,["✨","🍀"],3);tone(160,.2,"triangle",.06);}
  else if(P==="kokeshi"){tone(880,.12,"triangle",.05);tone(660,.15,"triangle",.04);}
  else if(P==="maneki"){fxAt(it,["🪙","✨"],6);sfx("coin");S.needs.joy=clamp(S.needs.joy+3,0,100);react("😻",1.4);}
  else if(P==="cranes"){fxAt(it,["✨"],3);chime([1568,2093]);}
  else if(P==="teaset"){pet.food="🍵";walkTo(it,"treat","😌");}
  else if(P==="koro"){react("😌",1.6);}
  else if(P==="goban"){tone(1200,.05,"square",.05);setTimeout(()=>tone(1100,.05,"square",.05),160);if(pet.action==="idle")start("poke");}
  else if(P.startsWith("kimono")){fxAt(it,["✨","🌸"],4);react("😻",1.4);}
  else if(P==="kyodai"){walkTo(it,"groom","😼");}
  else if(P.startsWith("bowl")){if(S.needs.food>=95){start("refuse");return;}pet.food=P==="bowl_red"?"🐟":"🥛";S.needs.food=clamp(S.needs.food+14,0,100);award("food1");walkTo(it,"treat","😋");}
  else if(P==="masu"){walkTo(it,"box","😹");}
  else if(P==="tetsubin"||P==="donabe"){tone(2400,.5,"sine",.012);react("😺",1.2);}
  else if(P==="teru"){if(weather.on&&S.weather==="auto"){weather.until=t+4;toast("Тэру-тэру-бодзу прогоняет дождь");}else toast("Тэру-тэру-бодзу бережёт от дождя");react("😸",1.4);}
  else if(P==="hoshigaki"){react("😋",1.4);}
  else if(P==="kingyo"){walkTo(it,"poke","😼");}
  else sfx("pop");
}
function drawFloatFx(t){for(let i=floatFx.length-1;i>=0;i--){const f=floatFx[i],a=(t-f.t)/1.3;if(a>1){floatFx.splice(i,1);continue;}if(a<0)continue;
  if(f.g==="♪"||f.g==="♫"){ctx.save();ctx.globalAlpha=1-a;ctx.font=`800 ${18*view.s}px ${getComputedStyle(document.body).fontFamily}`;ctx.textAlign="center";ctx.fillStyle="#eea3bb";ctx.fillText(f.g,f.x+Math.sin(a*6)*6,f.y-a*50*view.s);ctx.restore();}
  else drawEmoji(ctx,f.g,f.x+Math.sin(a*5)*6,f.y-a*50*view.s,18*view.s,1-a);}}
const LIGHT_PT={d_andon:[85,160],d_chochin:[90,175],d_yukimi:[120,80]};
function lightGlow(it,t){const p=LIGHT_PT[it.id];if(!p||S.lightsOff[it.id])return;const [x0,y0]=spriteBox(it),[sx,sy]=imgToStage(x0+p[0],y0+p[1]),fl=.9+.08*Math.sin(t*6.3+it.x)+.04*Math.sin(t*13),R=260*BGM.k;
  const gr=ctx.createRadialGradient(sx,sy,0,sx,sy,R);gr.addColorStop(0,`rgba(245,185,105,${.3*fl})`);gr.addColorStop(1,"rgba(245,185,105,0)");ctx.fillStyle=gr;ctx.fillRect(sx-R,sy-R,R*2,R*2);}

// ───────────────────────── Courtyard waterfall and shrine entrance ─────────────────────────
const FALLS=[[110,340,105],[290,580,115],[540,780,130]];
const fallLines=Array.from({length:70},()=>({f:Math.floor(Math.random()*3),u:Math.random(),v:Math.random(),sp:rand(.7,1.2),len:rand(.08,.2)}));
const koiFish=Array.from({length:5},(_,i)=>({ph:i*1.3,r:rand(.6,1),c:["#e2522e","#f2efe6","#e8a13a","#e2522e","#f2efe6"][i]}));
let koiUntil=0,pebble=null,lanternOn=true;
function drawPlaces(t,dt){
  if(S.room==="courtyard"){
    ctx.save();ctx.lineCap="round";
    for(const l of fallLines){l.v+=dt*.55*l.sp;if(l.v>1.1){l.v=-.1;l.u=Math.random();}const [a,b,top]=FALLS[l.f],x=mix(a+20,b-20,l.u),y=mix(top,930,l.v),[sx,sy]=imgToStage(x,y),[,ey]=imgToStage(x,y+l.len*820);
      ctx.strokeStyle=`rgba(235,240,242,${.18+.2*Math.sin(l.u*20)})`;ctx.lineWidth=(2+l.sp*2)*BGM.k*2;ctx.beginPath();ctx.moveTo(sx,sy);ctx.lineTo(sx,ey);ctx.stroke();}
    for(let i=0;i<7;i++){const ph=(t*.08+i/7)%1,[bx,by]=imgToStage(160+i*95+Math.sin(t*.3+i)*30,920-ph*220),r=(120+120*ph)*BGM.k;const gr=ctx.createRadialGradient(bx,by,0,bx,by,r);gr.addColorStop(0,`rgba(236,240,238,${.28*Math.sin(Math.PI*ph)})`);gr.addColorStop(1,"rgba(236,240,238,0)");ctx.fillStyle=gr;ctx.fillRect(bx-r,by-r,r*2,r*2);}
    if(t<koiUntil){const al=clamp(Math.min(koiUntil-t,1.2-(koiUntil-8-t))*1.2,0,1);for(const f of koiFish){const a=t*.6*f.r+f.ph,[x,y]=imgToStage(1150+Math.cos(a)*300*f.r,1030+Math.sin(a*1.4)*40),dir=-Math.sin(a)>0?1:-1,k=BGM.k*2.2;
      ctx.save();ctx.globalAlpha=al*.9;ctx.translate(x,y);ctx.scale(dir,1);ctx.fillStyle=f.c;ctx.beginPath();ctx.ellipse(0,0,18*k,7*k,0,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.moveTo(-16*k,0);ctx.lineTo(-30*k,-9*k+Math.sin(t*8+f.ph)*3);ctx.lineTo(-30*k,9*k);ctx.fill();ctx.restore();}}
    if(pebble){const e=t-pebble.t;if(e<.7){const u=e/.7,[x,y]=imgToStage(mix(900,pebble.x,u),mix(1150,1040,u)-Math.sin(u*Math.PI)*220);ctx.fillStyle="#8a8d86";ctx.beginPath();ctx.arc(x,y,5*view.s,0,Math.PI*2);ctx.fill();}
      else if(e<2.2){const u=(e-.7)/1.5,[x,y]=imgToStage(pebble.x,1040);ctx.strokeStyle=`rgba(220,230,232,${.7*(1-u)})`;ctx.lineWidth=1.5;for(const k of[1,.6]){ctx.beginPath();ctx.ellipse(x,y,(10+120*u*k)*BGM.k*2,(3+30*u*k)*BGM.k*2,0,0,Math.PI*2);ctx.stroke();}}
      else pebble=null;}
    ctx.restore();
  }
  if(S.room==="entrance"){const fl=.88+.08*Math.sin(t*5.7)+.05*Math.sin(t*12.3);
    for(const [ix,iy,R,on] of [[330,880,380,lanternOn],[882,870,160,true]]){if(!on)continue;const [x,y]=imgToStage(ix,iy),r=R*BGM.k;const gr=ctx.createRadialGradient(x,y,0,x,y,r);gr.addColorStop(0,`rgba(245,190,110,${.32*fl})`);gr.addColorStop(1,"rgba(245,190,110,0)");ctx.fillStyle=gr;ctx.fillRect(x-r,y-r,r*2,r*2);}
    if(!lanternOn){const [x,y]=imgToStage(330,885);ctx.fillStyle="rgba(8,8,8,.85)";ctx.fillRect(x-20*BGM.k,y-26*BGM.k,40*BGM.k,52*BGM.k);}
    ctx.save();ctx.globalAlpha=.45;const fw=900*view.s*1.3,fh=260*view.s*1.3,off=(t*6*view.s)%fw;for(let x=-off;x<view.W;x+=fw)ctx.drawImage(fogTex,x,view.H*.45,fw,fh);ctx.restore();
  }
}
const FORTUNES=[
 ["大吉","Большая удача","Всё, что задумано, сбудется. Даже огурцы сегодня не страшны."],
 ["吉","Удача","Хороший день для новых дел и долгого мурчания."],
 ["中吉","Средняя удача","Удача придёт, если не торопиться. Сначала вкусняшка — потом подвиги."],
 ["小吉","Малая удача","Маленькие радости: солнечное пятно, мягкая подушка, новый клубок."],
 ["末吉","Удача придёт позже","Терпение. Под дождём тоже растут цветы сакуры."],
 ["凶","Неудача","Будь осторожна у колодцев и фонарей. Бумажку привяжем к верёвке — пусть беда останется здесь."],
 ["大凶","Большая неудача","Сегодня лучше не открывать двери после заката. Привяжи бумажку к верёвке у храма."]
];
function omikuji(){const i=Math.random()<.12?0:Math.floor(rand(0,FORTUNES.length)),[k,t1,t2]=FORTUNES[i],bad=i>=5;
  const st=$("story");$("storyTitle").textContent="Омикудзи";st.hidden=false;
  $("storyBody").innerHTML=`<div class="fortune ${bad?"bad":""}"><div class="fk">${k}</div><h3>${t1}</h3><p>${t2}</p><p class="src">${bad?"По обычаю плохое предсказание привязывают к верёвке у храма — и беда остаётся там.":"Хорошее предсказание забирают с собой."}</p><button class="btn primary" id="fortuneOk">${bad?"Привязать к верёвке":"Забрать с собой"}</button></div>`;
  $("fortuneOk").onclick=()=>{st.hidden=true;react(bad?"😾":"😻",2);if(!bad)burst(10);};
  tone(bad?110:880,.5,"sine",.05);if(bad)react("🙀",1.5);}
function placeAction(a){
  const t=now();
  if(a==="pray"){start("hide");setTimeout(()=>{tone(174,2.4,"sine",.06);tone(349,2,"sine",.03);},200);S.needs.joy=clamp(S.needs.joy+8,0,100);react("🙏",2.4);}
  else if(a==="wash_paws"){S.needs.clean=clamp(S.needs.clean+15,0,100);sfx("splash");start("groom");react("😌",1.6);}
  else if(a==="omikuji"){omikuji();}
  else if(a==="lantern"){lanternOn=!lanternOn;tone(lanternOn?600:300,.08,"square",.04);react(lanternOn?"😸":"🙀",1.4);}
  else if(a==="koi"){koiUntil=t+9;sfx("splash");react("😼",2);start("firefly");}
  else if(a==="pebble"){pebble={t,x:rand(1000,1500)};setTimeout(()=>sfx("splash"),700);start("poke");}
  else if(a==="meditate"){start("music");S.needs.energy=clamp(S.needs.energy+10,0,100);react("😌",2.5);}
}
