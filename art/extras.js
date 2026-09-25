// ───────────────────────── Room decor (Angela-style furnishing) ─────────────────────────
const DMETA=__DMETA__;
const DIMG={};
const DECOR={
  engawa:[
    {k:"plant",n:"Растение",items:[{id:"d_bonsai",n:"Бонсай",p:140,x:330,y:1262},{id:"d_ikebana",n:"Икебана",p:120,x:330,y:1262},{id:"d_kokedama",n:"Кокедама",p:90,x:330,y:1262},{id:"d_bamboo",n:"Бамбук",p:110,x:330,y:1262}]},
    {k:"seat",n:"Подушка",items:[{id:"d_zab_indigo",n:"Синяя волна",p:60,x:1290,y:1335},{id:"d_zab_red",n:"Алая асаноха",p:60,x:1290,y:1335},{id:"d_zab_moss",n:"Моховая",p:60,x:1290,y:1335}]},
    {k:"chime",n:"Фурин",items:[{id:"d_furin_glass",n:"Стеклянный",p:70,x:640,y:112,sway:1},{id:"d_furin_blue",n:"Синий",p:70,x:640,y:112,sway:1},{id:"d_furin_iron",n:"Чугунный",p:90,x:640,y:112,sway:1}]},
    {k:"light",n:"Фонарь",items:[{id:"d_andon",n:"Андон",p:130,x:1590,y:1282},{id:"d_chochin",n:"Красный тётин",p:100,x:1560,y:112,sway:.4}]}
  ],
  onsen:[
    {k:"bucket",n:"Ведро",items:[{id:"d_okeya",n:"Кэдровое окэ",p:50,x:320,y:1340}]},
    {k:"garden",n:"Сад",items:[{id:"d_shishi_base",n:"Сисиодоси",p:160,x:1500,y:1255,shishi:1},{id:"d_kaeru",n:"Каменная лягушка",p:70,x:1520,y:1262},{id:"d_yukimi",n:"Фонарь юкими",p:120,x:1520,y:1258}]},
    {k:"water",n:"В воде",items:[{id:"d_yuzu",n:"Юдзу",p:40,x:900,y:1075,bob:1},{id:"d_petals",n:"Лепестки",p:30,x:900,y:1075,bob:1}]}
  ],
  bedroom:[
    {k:"futon",n:"Футон",items:[{id:"d_futon_waves",n:"Сэйгайха",p:150,x:900,y:1382},{id:"d_futon_red",n:"Асаноха",p:150,x:900,y:1382},{id:"d_futon_bamboo",n:"Бамбук",p:150,x:900,y:1382},{id:"d_futon_moon",n:"Луны",p:170,x:900,y:1382}]},
    {k:"scroll",n:"Свиток",items:[{id:"d_scroll_moon",n:"Луна и сосна",p:120,x:270,y:206},{id:"d_scroll_koi",n:"Карпы",p:120,x:270,y:206},{id:"d_scroll_neko",n:"猫 «Кошка»",p:100,x:270,y:206},{id:"d_scroll_mount",n:"Горы в тумане",p:120,x:270,y:206}]},
    {k:"doll",n:"Кукла",items:[{id:"d_daruma",n:"Дарума",p:80,x:1500,y:1262},{id:"d_kokeshi",n:"Кокэси",p:70,x:1500,y:1262},{id:"d_maneki",n:"Манэки-нэко",p:110,x:1500,y:1262}]},
    {k:"mobile",n:"Над футоном",items:[{id:"d_cranes",n:"Журавлики",p:90,x:1460,y:70}]}
  ]
};
const DTINT={engawa:"rgba(18,26,22,.22)",onsen:"rgba(20,28,26,.26)",bedroom_on:"rgba(40,25,10,.2)",bedroom_off:"rgba(8,10,26,.62)"};
const tmpCv=document.createElement("canvas"),tmpCx=tmpCv.getContext("2d");
function drawSprite(g,id,x,y,rot=0,pivot=null,alpha=1){
  const im=DIMG[id],m=DMETA[id];if(!im||!m)return;const k=BGM.k,w=m[0]*k,h=m[1]*k;
  let x0=x-w/2,y0=m[2]==="t"?y:m[2]==="c"?y-h/2:y-h;const [sx,sy]=imgToStage(x0/k,y0/k);
  const tint=DTINT[bgName()];
  tmpCv.width=Math.ceil(w*view.dpr)+2;tmpCv.height=Math.ceil(h*view.dpr)+2;tmpCx.setTransform(view.dpr,0,0,view.dpr,0,0);
  tmpCx.drawImage(im,0,0,w,h);if(tint){tmpCx.globalCompositeOperation="source-atop";tmpCx.fillStyle=tint;tmpCx.fillRect(0,0,w,h);tmpCx.globalCompositeOperation="source-over";}
  g.save();g.globalAlpha=alpha;
  if(rot){const [px,py]=pivot?imgToStage(pivot[0],pivot[1]):[sx+w/2,sy];g.translate(px,py);g.rotate(rot);g.translate(-px,-py);}
  g.drawImage(tmpCv,0,0,tmpCv.width,tmpCv.height,sx,sy,tmpCv.width/view.dpr,tmpCv.height/view.dpr);g.restore();
}
let nextTinkle=now()+8,shishiClack=0;
function drawDecor(t){
  const room=DECOR[S.room];if(!room)return;const sel=S.decor[S.room]||{};
  for(const slot of room){const it=slot.items.find(i=>i.id===sel[slot.k]);if(!it)continue;
    if(it.sway){const wind=weather.on?1.8:1;const a=(.07*Math.sin(t*1.6+it.x)+.035*Math.sin(t*3.7))*wind*it.sway;drawSprite(ctx,it.id,it.x,it.y,a,[it.x,it.y]);
      if(it.id.startsWith("d_furin")&&t>nextTinkle){nextTinkle=t+rand(6,14)/wind;if(snd.on&&snd.ctx){tone(it.id==="d_furin_iron"?1320:2093,1.2,"sine",.025);setTimeout(()=>tone(it.id==="d_furin_iron"?1760:2637,1,"sine",.018),90);}}}
    else if(it.bob){drawSprite(ctx,it.id,it.x,it.y+Math.sin(t*1.3)*3);}
    else if(it.shishi){drawSprite(ctx,it.id,it.x,it.y);
      const cyc=(t%6)/6,ang=cyc<.93?mix(-.28,.34,Math.pow(cyc/.93,2.2)):mix(.34,-.28,(cyc-.93)/.07);
      if(cyc>.93&&t-shishiClack>1){shishiClack=t;if(snd.on&&snd.ctx){tone(420,.08,"square",.05);tone(210,.12,"triangle",.06);}}
      drawSprite(ctx,"d_shishi_tube",it.x+85,it.y-128,ang,[it.x+85,it.y-128]);}
    else drawSprite(ctx,it.id,it.x,it.y);}
}

// ───────────────────────── Weather: rain and thunder ─────────────────────────
const weather={on:false,until:0,next:now()+rand(60,160),drops:[],splash:[],flash:-9,thunderAt:0,nextBolt:0,noise:null,gain:null};
const RAIN_REGION={engawa:[[64,112,1380,1118],"garden"],onsen:[[0,0,1800,1400],"out"],games:[[0,0,1800,1400],"out"],kitchen:[[240,180,820,640],"window"]};
function rainSound(on,loud){
  if(!snd.ctx)return;const c=snd.ctx;
  if(on&&snd.on){if(!weather.noise){const b=c.createBuffer(1,c.sampleRate*2,c.sampleRate),d=b.getChannelData(0);let last=0;for(let i=0;i<d.length;i++){last=(last+.02*(Math.random()*2-1))/1.02;d[i]=last*3+(Math.random()*2-1)*.25;}
      const s=c.createBufferSource();s.buffer=b;s.loop=true;const f=c.createBiquadFilter();f.type="lowpass";f.frequency.value=2400;const g=c.createGain();g.gain.value=0;s.connect(f);f.connect(g);g.connect(c.destination);s.start();weather.noise=s;weather.gain=g;}
    weather.gain.gain.setTargetAtTime(loud?.22:.1,c.currentTime,.8);}
  else if(weather.gain){weather.gain.gain.setTargetAtTime(0,c.currentTime,.6);}
}
function thunder(){if(!snd.on||!snd.ctx)return;const c=snd.ctx,t=c.currentTime,b=c.createBuffer(1,c.sampleRate*3,c.sampleRate),d=b.getChannelData(0);let last=0;for(let i=0;i<d.length;i++){last=(last+.03*(Math.random()*2-1))/1.03;d[i]=last*6*Math.pow(1-i/d.length,1.4)*(i<c.sampleRate*.15?i/(c.sampleRate*.15):1);}
  const s=c.createBufferSource();s.buffer=b;const f=c.createBiquadFilter();f.type="lowpass";f.frequency.value=260;const g=c.createGain();g.gain.value=.9;s.connect(f);f.connect(g);g.connect(c.destination);s.start(t);}
function updateWeather(t,dt){
  const mode=S.weather;
  if(mode==="rain")weather.on=true;else if(mode==="clear")weather.on=false;
  else{if(!weather.on&&t>weather.next){weather.on=true;weather.until=t+rand(80,200);}if(weather.on&&t>weather.until){weather.on=false;weather.next=t+rand(120,300);}}
  const reg=RAIN_REGION[S.room];rainSound(weather.on,!!reg&&reg[1]!=="window");
  if(weather.on){if(!weather.nextBolt)weather.nextBolt=t+rand(8,20);if(t>weather.nextBolt){weather.flash=t;weather.thunderAt=t+rand(.5,1.6);weather.nextBolt=t+rand(14,40);if(pet.action!=="sleep"){react("🙀",1.6);if(pet.action==="idle")start("hide",true);}}}
  else weather.nextBolt=0;
  if(weather.thunderAt&&t>weather.thunderAt){weather.thunderAt=0;thunder();}
  const want=weather.on&&reg?(reg[1]==="window"?60:170):0;
  while(weather.drops.length<want)weather.drops.push({u:Math.random(),v:Math.random(),sp:rand(.9,1.4),len:rand(.7,1.3)});
  if(weather.drops.length>want)weather.drops.length=want;
  for(const d of weather.drops){d.v+=dt*d.sp*(reg&&reg[1]==="window"?1.1:.8);if(d.v>1){d.v-=1+Math.random()*.2;d.u=Math.random();if(reg&&reg[1]!=="window"&&Math.random()<.5)weather.splash.push({u:d.u,t});}}
  weather.splash=weather.splash.filter(s=>t-s.t<.35);
}
function drawRain(t,front){
  const reg=RAIN_REGION[S.room];
  if(weather.on&&!front){ctx.fillStyle="rgba(10,16,22,.16)";ctx.fillRect(0,0,view.W,view.H);}
  if(!weather.on||!reg)return;const isFront=reg[1]==="out";if(front!==isFront)return;
  const [x0,y0,x1,y1]=reg[0],[sx0,sy0]=imgToStage(x0,y0),[sx1,sy1]=imgToStage(x1,y1),w=sx1-sx0,h=sy1-sy0,s=view.s;
  ctx.save();ctx.beginPath();ctx.rect(sx0,sy0,w,h);ctx.clip();ctx.strokeStyle="rgba(196,206,212,.32)";ctx.lineWidth=1.1;ctx.beginPath();
  for(const d of weather.drops){const x=sx0+d.u*w+d.v*18*s,y=sy0+d.v*h,L=(reg[1]==="window"?10:22)*s*d.len;ctx.moveTo(x,y);ctx.lineTo(x-4*s,y-L);}ctx.stroke();
  ctx.strokeStyle="rgba(200,210,215,.35)";for(const p of weather.splash){const a=(t-p.t)/.35,x=sx0+p.u*w,y=sy1-6*s-(p.u*37%1)*(reg[1]==="garden"?10:60)*s;ctx.beginPath();ctx.ellipse(x,y,(2+10*a)*s,(1+3*a)*s,0,0,Math.PI*2);ctx.globalAlpha=1-a;ctx.stroke();}
  ctx.restore();
}
function drawFlash(t){const a=t-weather.flash;if(a<0||a>.5)return;const k=a<.08?1:a<.14?.25:a<.22?.8:1-(a-.22)/.28;ctx.fillStyle=`rgba(220,228,240,${.55*Math.max(0,k)})`;ctx.fillRect(0,0,view.W,view.H);}

// ───────────────────────── Scary happenings in the rooms ─────────────────────────
const spook={ev:null,next:now()+rand(40,90)};
const SPOOKS={engawa:["eyes","shadow","kitsunebi","knock"],kitchen:["obake","eyes_win","flicker"],onsen:["hair","eyes","kitsunebi"],bedroom:["hands","shadow_bed","knock","flicker"],wardrobe:["screen_eyes","flicker"],games:["eyes","kitsunebi"]};
function knock(){if(!snd.on||!snd.ctx)return;[0,.28,.56].forEach(d=>setTimeout(()=>{tone(90,.18,"triangle",.14);tone(60,.22,"sine",.12);},d*1000));}
function updateSpook(t){
  if(spook.ev&&t-spook.ev.t>spook.ev.dur)spook.ev=null;
  if(!S.scary||spook.ev||t<spook.next||!document.getElementById("game").hidden||!document.getElementById("story").hidden)return;
  spook.next=t+rand(55,140)*(weather.on?.6:1);
  const kind=pick(SPOOKS[S.room]||["flicker"]),r=Math.random;
  spook.ev={kind,t,dur:kind==="knock"?2:kind==="flicker"?1.2:4.2,x:r(),y:r(),seed:r()*100};
  if(kind==="knock")knock();else tone(55,1.4,"sawtooth",.05);
  setTimeout(()=>{if(pet.action!=="sleep"){react("🙀",2);if(["idle","beg","music","knead","groom"].includes(pet.action))start("hide",true);}},kind==="knock"?300:900);
}
function silhouette(drawFn,w,h,alpha){tmpCv.width=Math.ceil(w);tmpCv.height=Math.ceil(h);tmpCx.setTransform(1,0,0,1,0,0);tmpCx.clearRect(0,0,w,h);drawFn(tmpCx);tmpCx.globalCompositeOperation="source-in";tmpCx.fillStyle="#050606";tmpCx.fillRect(0,0,w,h);tmpCx.globalCompositeOperation="source-over";return tmpCv;}
function drawSpook(t){
  const ev=spook.ev;if(!ev)return;const e=t-ev.t,k=BGM.k,s=view.s,fade=clamp(Math.min(e/.6,(ev.dur-e)/.8),0,1);
  const eyes=(x,y,r,col="230,40,30")=>{const bl=Math.sin(e*3)>.93?.1:1;for(const d of[-1,1]){const gx=x+d*r*1.6,gr=ctx.createRadialGradient(gx,y,0,gx,y,r*2.4);gr.addColorStop(0,`rgba(${col},${.9*fade})`);gr.addColorStop(1,`rgba(${col},0)`);ctx.fillStyle=gr;ctx.fillRect(gx-r*2.4,y-r*2.4,r*4.8,r*4.8);ctx.fillStyle=`rgba(255,220,200,${fade})`;ctx.beginPath();ctx.ellipse(gx,y,r*.7,r*.45*bl,0,0,Math.PI*2);ctx.fill();}};
  switch(ev.kind){
    case"eyes":{const [x,y]=imgToStage(200+ev.x*1100,S.room==="engawa"?1000+ev.y*70:700+ev.y*300);eyes(x,y,4*s);break;}
    case"eyes_win":{const [x,y]=imgToStage(300+ev.x*460,300+ev.y*250);eyes(x,y,3.5*s,"200,220,255");break;}
    case"screen_eyes":{for(let i=0;i<3;i++){const [x,y]=imgToStage(260+((ev.x*1300+i*430)%1300),320+((ev.y*400+i*130)%420));eyes(x,y,5*s,"230,190,90");}break;}
    case"shadow":case"shadow_bed":{const box=ev.kind==="shadow"?[1400,124,1792,1100]:[640,150,1560,1000],[bx0,by0]=imgToStage(box[0],box[1]),[bx1,by1]=imgToStage(box[2],box[3]);
      const u=ev.kind==="shadow"?e/ev.dur:.5+Math.sin(e*.7)*.08,hh=(by1-by0)*.95,ww=hh*.5;
      const c=silhouette(g=>drawYurei(g,ww/2,0,hh,1,false,false),ww,hh);ctx.save();ctx.beginPath();ctx.rect(bx0,by0,bx1-bx0,by1-by0);ctx.clip();ctx.globalAlpha=.55*fade;ctx.filter="blur(2px)";ctx.drawImage(c,mix(bx0-ww,bx1,u),by1-hh);ctx.restore();break;}
    case"hands":{const [bx0,by0]=imgToStage(640,150),[bx1,by1]=imgToStage(1560,1000),n=Math.min(7,Math.floor(e*2.2));const rr=rng(ev.seed|0);
      ctx.save();ctx.globalAlpha=.6*fade;ctx.fillStyle="#1a0e0c";for(let i=0;i<n;i++){const x=mix(bx0,bx1,.1+rr()*.8),y=mix(by0,by1,.15+rr()*.7),r=13*s,a=rr()*.6-.3;ctx.save();ctx.translate(x,y);ctx.rotate(a);ctx.beginPath();ctx.ellipse(0,0,r,r*1.15,0,0,Math.PI*2);ctx.fill();
        for(let f=0;f<5;f++){const fa=-Math.PI/2+(f-2)*.32+(f===0?-.5:0),fl=r*(f===0?1.1:f===2?1.9:1.6);ctx.beginPath();ctx.ellipse(Math.cos(fa)*fl*.9,Math.sin(fa)*fl*.9,r*.24,fl*.5,fa+Math.PI/2,0,Math.PI*2);ctx.fill();}ctx.restore();}ctx.restore();break;}
    case"kitsunebi":{for(let i=0;i<3;i++){const [x,y]=imgToStage(mix(-100,1900,(e/ev.dur+i*.12)%1),860+Math.sin(e*2+i)*40+i*30);const gr=ctx.createRadialGradient(x,y,0,x,y,26*s);gr.addColorStop(0,`rgba(140,200,255,${.8*fade})`);gr.addColorStop(1,"rgba(80,140,220,0)");ctx.fillStyle=gr;ctx.fillRect(x-26*s,y-26*s,52*s,52*s);}break;}
    case"hair":{const [x,y]=imgToStage(700+ev.x*400,1060);ctx.save();ctx.globalAlpha=.8*fade;ctx.strokeStyle="#060606";ctx.lineWidth=1.4;for(let i=0;i<40;i++){ctx.beginPath();ctx.moveTo(x,y);for(let j=1;j<8;j++)ctx.lineTo(x+Math.cos(i*.16)*j*12*s+Math.sin(e*2+j+i)*4*s,y+Math.sin(i*.16)*j*3*s);ctx.stroke();}ctx.restore();break;}
    case"obake":{const [x,y]=imgToStage(1560,300),r=62*BGM.k;ctx.save();ctx.globalAlpha=fade;ctx.fillStyle="#f4efe2";ctx.beginPath();ctx.ellipse(x+r*.1,y-r*.35,r*.42,r*.3*Math.min(1,e*2),0,0,Math.PI*2);ctx.fill();ctx.fillStyle="#140a08";ctx.beginPath();ctx.arc(x+r*.1+Math.sin(e*1.5)*r*.15,y-r*.35,r*.14,0,Math.PI*2);ctx.fill();
      ctx.fillStyle="#1a0806";ctx.beginPath();ctx.ellipse(x,y+r*.45,r*.5,r*.14,0,0,Math.PI*2);ctx.fill();ctx.fillStyle="#c23a3a";ctx.beginPath();ctx.moveTo(x-r*.12,y+r*.5);ctx.quadraticCurveTo(x+r*.1,y+r*(1.4+.3*Math.sin(e*4)),x+r*.25,y+r*.5);ctx.fill();ctx.restore();break;}
    case"flicker":{const on=[.05,.15,.3,.42,.62,.7].some((v,i)=>e>v&&e<v+.07+(i%2)*.05);if(on){ctx.fillStyle="rgba(2,3,5,.78)";ctx.fillRect(0,0,view.W,view.H);}break;}
  }
}

// ───────────────────────── Kaidan reader ─────────────────────────
const KAIDAN=[
 {t:"Безликая у рва",src:"«Мудзина», Лафкадио Хирн, «Кайдан», 1904",p:["В Токио есть склон Кии-но-куни-дзака. С одной его стороны — старый глубокий ров, с другой — высокие стены княжеской усадьбы. В те времена, когда ещё не было уличных фонарей, после заката здесь старались не ходить.","Однажды поздно вечером по склону торопился купец и увидел у рва девушку. Она сидела одна и горько плакала, закрыв лицо рукавом. Купец испугался, что она задумала броситься в воду, и заговорил с ней ласково: «Не плачьте, расскажите, что случилось». Девушка всхлипывала и не отвечала. Он тронул её за плечо.","Тогда она опустила рукав и медленно повернулась. У неё не было лица: ни глаз, ни носа, ни рта — только гладкая кожа, как яичная скорлупа.","Купец с криком бросился бежать и бежал, пока не увидел огонёк. Это был фонарь ночного продавца лапши. «Там… у рва… девушка… у неё лицо…» — задыхался купец. «Вот такое?» — спросил продавец и провёл ладонью по своему лицу. Оно стало гладким, как яйцо. И фонарь погас."]},
 {t:"Хоити Безухий",src:"«Мими-наси Хоити», Лафкадио Хирн, «Кайдан», 1904",p:["Слепой монах Хоити лучше всех пел под бива «Повесть о доме Тайра» — о морской битве при Дан-но-ура, где погиб весь род Тайра вместе с малолетним императором. Жил он в храме Амидадзи у самого моря.","Однажды ночью за ним пришёл самурай: «Мой господин желает тебя послушать». Он вёл Хоити через ворота, по камням, в зал, полный шелеста шёлка и шёпота. Хоити пел — и слышал, как невидимые слушатели рыдают. Так было каждую ночь, и Хоити слабел.","Слуги храма проследили за ним и нашли его одного под дождём, на кладбище Тайра: он пел среди могил, а вокруг горели блуждающие огни. Настоятель понял, что мёртвые не отпустят певца. Он исписал всё тело Хоити священной сутрой и велел сидеть неподвижно и молчать.","Ночью самурай звал его, но видел пустоту. Только в темноте висели два уха — их забыли покрыть письменами. «Отнесу господину хоть это», — сказал голос, и уши оторвали. Хоити выжил. С тех пор его зовут Хоити Безухий."]},
 {t:"Снежная женщина",src:"«Юки-онна», Лафкадио Хирн, «Кайдан», 1904",p:["Старый дровосек Мосаку и юный Минокити возвращались из леса, когда началась метель. Лодочник уже ушёл, и они укрылись в его хижине у реки. Ночью Минокити проснулся от снега на лице: дверь была открыта, а над Мосаку склонилась женщина в белом. Она дохнула на старика — и его дыхание стало белым дымом.","Потом она наклонилась к Минокити. Лицо её было прекрасным, а глаза — страшными. «Ты молод, я тебя пощажу, — сказала она. — Но если расскажешь кому-нибудь о том, что видел, я узнаю. И тогда убью тебя». Утром Мосаку нашли замёрзшим.","Через год Минокити встретил на дороге девушку О-Юки. Они поженились, у них родилось десять детей, а О-Юки совсем не старела. Однажды вечером, глядя на неё при свете лампы, Минокити сказал: «Ты напоминаешь мне одну женщину…» — и рассказал о той ночи.","О-Юки поднялась: «Это была я! Я обещала убить тебя, если скажешь хоть слово. Только ради детей ты жив». Её голос стал тонким, как вой ветра, и она растаяла белым туманом. Больше её никто не видел."]},
 {t:"Тарелки Окику",src:"«Банчо Сараясики», легенда эпохи Эдо",p:["В доме самурая Аоямы служила девушка Окику. Ей доверили беречь десять драгоценных тарелок фамильного сервиза. Однажды одна тарелка исчезла — по одной версии, её спрятал сам хозяин, по другой — завистливый слуга.","Сколько бы Окику ни пересчитывала, тарелок было девять. Её обвинили в пропаже и бросили в старый колодец в саду.","С тех пор каждую ночь из колодца доносится тихий голос: «Одна… две… три… четыре…» — и так до девяти. А после девятой тарелки раздаётся крик, от которого слышавшие его заболевали.","Говорят, Окику затихла, лишь когда смельчак крикнул в колодец: «Десять!». Колодец Окику до сих пор показывают в замке Химэдзи."]},
 {t:"Лицо в фонаре",src:"«Ёцуя-кайдан», пьеса кабуки Цуруи Намбоку IV, 1825",p:["Ронин Тамия Иэмон был женат на кроткой О-Иве, но захотел жениться на богатой соседке. Её семья прислала О-Иве «лекарство» — на самом деле яд. Волосы О-Ивы стали выпадать клоками, один глаз опух и закрылся. Увидев себя в зеркале, она поняла, что её предали, и умерла, проклиная мужа.","Иэмон женился на богатой невесте. Но в первую же ночь он поднял покрывало — и увидел изуродованное лицо О-Ивы. Он выхватил меч и ударил — а на полу лежала его невеста.","С тех пор лицо О-Ивы смотрело на Иэмона из бумажных фонарей, выплывало из дыма, шептало из воды. Он потерял рассудок.","Эту историю считают самым страшным японским кайданом. Актёры до сих пор перед постановкой приходят к святилищу О-Ивы в Ёцуе просить прощения — говорят, иначе беды не миновать."]},
 {t:"Летающие головы",src:"«Рокурокуби», Лафкадио Хирн, «Кайдан», 1904",p:["Монах Кайрё, в прошлом храбрый самурай, странствовал по горам провинции Каи. Лесоруб пригласил его переночевать в хижине, где жили ещё четверо. Все были очень учтивы.","Ночью Кайрё вышел попить воды и увидел в комнате пять тел — без голов. Ран на шеях не было: головы просто отделились. Монах понял, что это рокурокуби — существа, чьи головы по ночам улетают охотиться. А если спрятать тело, голова не сможет вернуться.","Он вытащил тело хозяина наружу. Из леса донеслись голоса: головы летали среди деревьев, ловили насекомых и спорили, как бы съесть толстого монаха. Когда они нашли Кайрё, началась битва. Монах отбивался молодым деревцем, пока головы не пали. Лишь голова хозяина вцепилась зубами в его рукав и так и умерла.","Кайрё продолжил путь с головой, висящей на рукаве. В соседней деревне его чуть не схватили как убийцу, пока судья не разглядел на шее головы красные знаки — метки рокурокуби."]},
 {t:"Кошка из Набэсимы",src:"Легенда эпохи Эдо о княжеском роде Набэсима",p:["Князь Набэсима из Хидзэна любил красавицу О-Тоё. Однажды ночью в её покои пробралась огромная кошка-оборотень. Она погубила девушку и приняла её облик.","С тех пор князь начал чахнуть. Каждую ночь его мучили кошмары, и никакие лекари не помогали. Сотня стражников дежурила у его постели, но к полуночи всех их одолевал непреодолимый сон.","Молодой воин Ито Сода вызвался сторожить. Когда накатила сонливость, он вонзил нож себе в бедро, чтобы боль не давала уснуть. В полночь дверь бесшумно открылась, и вошла «О-Тоё». Увидев неспящего Ито, она отступила. Так было несколько ночей, и князь начал поправляться.","Тогда Ито пришёл к «О-Тоё» с копьём. Она прыгнула на крышу и обернулась огромной кошкой. Её загнали в горы, и князь выздоровел. Муся уверяет, что эта история не про неё."]},
 {t:"Женщина в маске",src:"Городская легенда, паника 1979 года",p:["Весной 1979 года по японским школам поползли слухи: в сумерках к одиноким прохожим подходит высокая женщина в длинном плаще и марлевой маске. Она спрашивает: «Я красивая?»","Если ответить «нет» — беда. Если сказать «да», она медленно снимет маску: её рот разрезан от уха до уха. «А теперь?» — спросит она. Бежать бесполезно: она всегда оказывается впереди.","Говорили, что спастись можно, ответив «так себе», бросив ей леденцы бэккоамэ или трижды сказав слово «помада». Слухи были такими сильными, что в некоторых городах учителя провожали детей домой группами.","Похожие рассказы находят ещё в эпоху Эдо: там это была лиса-оборотень, прикидывающаяся красавицей."]}
];
function openStory(i){
  const st=$("story"),body=$("storyBody");st.hidden=false;
  if(i==null){body.innerHTML=`<p class="lead">Страшные истории Японии в пересказе. Муся слушает из-под одеяла.</p><div class="slist">${KAIDAN.map((k,j)=>`<button class="scard" data-story-i="${j}"><b>${k.t}</b><span>${k.src}</span></button>`).join("")}</div>`;}
  else{const k=KAIDAN[i];body.innerHTML=`<button class="back" data-story-i="-1">← Все истории</button><h3>${k.t}</h3><p class="src">${k.src}</p>${k.p.map(x=>`<p>${x}</p>`).join("")}<button class="btn primary next" data-story-i="${(i+1)%KAIDAN.length}">Следующая история</button>`;body.scrollTop=0;tone(70,1.2,"sawtooth",.04);}
  if(pet.action!=="sleep")start("hide");
}
$("story").addEventListener("click",ev=>{const b=ev.target.closest("[data-story-i]");if(b){const i=+b.dataset.storyI;openStory(i<0?null:i);}if(ev.target.closest("#storyClose")){$("story").hidden=true;start("purr");}});
