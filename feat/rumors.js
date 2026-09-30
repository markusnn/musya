{
// ───────────────────────── «Слухи и час быка»: guests whisper rumours; at the right hour, in the right room, a quiet sign appears ─────────────────────────
MON.m_rm_tengu=[440,580];MON.m_rm_okiku=[300,620];MON.m_rm_kosode=[520,540];MON.m_rm_chagama=[360,380];
const RMC="Тайны дома";
addItems([
 {id:"rm_chasen",n:"Чайный венчик Бунбуку",c:RMC,w:150,h:150,a:"b",p:0,at:["rm",0,0],src:"👂 слух",hint:"Слух про котелок на кухне — проверь ночью"},
 {id:"rm_kagami",n:"Зеркальце нэкоматы",c:RMC,w:140,h:180,a:"b",p:0,at:["rm",154,0],src:"👂 слух",hint:"Слух про отражение в онсэне — в сумерки"},
 {id:"rm_hauchiwa",n:"Веер из перьев тэнгу",c:RMC,w:140,h:210,a:"b",p:0,at:["rm",298,0],src:"👂 слух",hint:"Слух про сосну на веранде — в час быка"},
 {id:"rm_azuki",n:"Ситечко с фасолью адзуки",c:RMC,w:180,h:110,a:"b",p:0,at:["rm",0,214],src:"👂 слух",hint:"Слух про пруд во дворике — под дождём"},
 {id:"rm_key",n:"Ключ от амбара Инари",c:RMC,w:110,h:210,a:"t",p:0,at:["rm",184,214],src:"👂 слух",hint:"Слух про лисьи следы у тории — на рассвете"},
 {id:"rm_moku",n:"Сёдзи с глазами",c:RMC,w:150,h:210,a:"b",p:0,at:["rm",298,214],src:"👂 слух",hint:"Слух про кухонное окно — днём"},
 {id:"rm_sara",n:"Десятая тарелка",c:RMC,w:160,h:150,a:"b",p:0,at:["rm",0,428],src:"👂 слух",hint:"Слух про сёдзи в спальне — в полночь"},
 {id:"rm_tsuzumi",n:"Лунный барабанчик",c:RMC,w:160,h:160,a:"b",p:0,at:["rm",164,428],src:"👂 слух",hint:"Слух про барабан во дворике — в полнолуние"},
 {id:"rm_kosode",n:"Косодэ на вешалке",c:RMC,w:200,h:200,a:"b",p:0,at:["rm",0,592],src:"👂 слух",hint:"Слух про гардероб — в час быка"}
],{rm:[520,792]});
STAMPS.push(["rm_first","噂","Слухи не врут","Проверь первый слух"],["rm_ushi","丑","Час быка","Раскрой тайну в час быка, с часу до трёх ночи"],["rm_all","秘","Хранительница тайн","Раскрой все слухи о доме"]);
BESTIARY.push(
 ["rm_tengu","m_rm_tengu","Тэнгу","Горный дух с длинным красным носом, в одежде отшельника-ямабуси, с крыльями и веером из перьев. Самый знаменитый — Содзёбо с горы Курама: он учил фехтованию юного Минамото-но Ёсицунэ."],
 ["rm_okiku","m_rm_okiku","Окику","Служанка из легенды «Банчо Сараясики». Её обвинили в пропаже одной из десяти тарелок, и с тех пор по ночам она считает их до девяти. Затихает, если кто-нибудь скажет: «Десять»."],
 ["rm_kosode","m_rm_kosode","Косодэ-но-тэ","«Руки из рукавов»: из кимоно, купленного у старьёвщика, по ночам тянутся руки прежней хозяйки. Нарисован Ториямой Сэкиэном в 1779 году."],
 ["rm_bunbuku","m_rm_chagama","Бунбуку-тягама","Тануки, который превратился в чайный котёл и не сумел превратиться обратно. Этот котёл до сих пор хранят в храме Моринзи в Татэбаяси."],
 ["rm_moku","","Мокумокурэн","«Множество глаз» в решётках и рваных сёдзи старого дома. Нарисован Ториямой Сэкиэном в 1781 году."],
 ["rm_azuki","","Адзуки-арай","Тот, кто по ночам моет красную фасоль у воды и поёт. Его почти никто не видел — только слышал: шорх-шорх."]);

// ── time and conditions
function rmIn(w,h){return w[0]<w[1]?h>=w[0]&&h<w[1]:h>=w[0]||h<w[1];}
function moonAge(){const S0=Date.UTC(2000,0,6,18,14),P=29.530588853;return(((today().getTime()-S0)/864e5)%P+P)%P;}
function moonFull(){return Math.abs(moonAge()-14.77)<1.6||festOn("tsukimi");}
function rmPt(ix,iy,d,row){curRow=row??null;const p=imgToStage(ix,iy,d);curRow=null;return p;}
function rmMon(id,ix,iy,h,d,row,a,rot=0,flip=false){curRow=row??null;drawMon(id,ix,iy,h,d,a,"b",rot,flip);curRow=null;}
const SIL={};
function sil(id,col,blur){const k=id+col;if(SIL[k])return SIL[k];const im=MIMG[id];if(!im||!im.width)return null;const c=document.createElement("canvas");c.width=im.width;c.height=im.height;const g=c.getContext("2d");if(blur)g.filter=`blur(${blur}px)`;g.drawImage(im,0,0);g.filter="none";g.globalCompositeOperation="source-in";g.fillStyle=col;g.fillRect(0,0,c.width,c.height);return SIL[k]=c;}
function drawSil(c,id,ix,iy,h,d,row,a,rot=0){if(!c||a<=0)return;const m=MON[id],sc=h/m[1]*BGM.k,w=m[0]*sc,hh=m[1]*sc,[x,y]=rmPt(ix,iy,d,row);ctx.save();ctx.globalAlpha=a;ctx.translate(x,y);if(rot)ctx.rotate(rot);ctx.drawImage(c,-w/2,-hh,w,hh);ctx.restore();}
function monS(id,x,y,hp,a,rot=0){const im=MIMG[id],m=MON[id];if(!im||!m||a<=0)return;const w=m[0]*hp/m[1];ctx.save();ctx.globalAlpha=Math.min(1,a);ctx.translate(x,y);if(rot)ctx.rotate(rot);ctx.drawImage(im,-w/2,-hp,w,hp);ctx.restore();}
function glow(x,y,r,col,a){if(a<=0)return;const gr=ctx.createRadialGradient(x,y,0,x,y,r);gr.addColorStop(0,col.replace("A",a));gr.addColorStop(1,col.replace("A",0));ctx.fillStyle=gr;ctx.fillRect(x-r,y-r,r*2,r*2);}
function eyeAt(x,y,w,open,col="#e8dcc0",iris="#1a120c"){if(open<=.02)return;ctx.save();ctx.translate(x,y);ctx.scale(1,open);ctx.beginPath();ctx.ellipse(0,0,w,w*.55,0,0,Math.PI*2);ctx.fillStyle=col;ctx.fill();ctx.beginPath();ctx.arc(0,0,w*.42,0,Math.PI*2);ctx.fillStyle=iris;ctx.fill();ctx.restore();}
// sounds (all quiet; nothing plays unless the sound is on)
let nzBuf=null;
function noise(dur,freq,vol){if(!snd.on||!snd.ctx)return;const c=snd.ctx;if(!nzBuf){nzBuf=c.createBuffer(1,c.sampleRate,c.sampleRate);const d=nzBuf.getChannelData(0);for(let i=0;i<d.length;i++)d[i]=Math.random()*2-1;}
  const s=c.createBufferSource();s.buffer=nzBuf;const f=c.createBiquadFilter();f.type="bandpass";f.frequency.value=freq;f.Q.value=1.4;const g=c.createGain(),t=c.currentTime;g.gain.setValueAtTime(vol,t);g.gain.exponentialRampToValueAtTime(.0001,t+dur);s.connect(f);f.connect(g);g.connect(c.destination);s.start(t,Math.random()*.5,dur+.05);}
function pon(){tone(118,.28,"sine",.13);tone(74,.34,"sine",.1);}
function clink(){tone(2350,.35,"sine",.02);tone(3140,.25,"sine",.012);}

// ── the rumours: who says what, when, where; the sign; the reveal
const PINE=[600,330],WIN=[[486,262],[628,318],[766,246],[548,470],[706,540],[790,420]];
const kam=()=>propAt("p_kit_pot0",1030,705),rock=()=>propAt("p_crt_rock0",1130,985);
const RUM=[
 {id:"kama",t:"Котелок на кухне",room:"kitchen",w:[21,5],when:"ночью, с девяти вечера до пяти утра",where:"кухня, котелок на полке",
  say:"По ночам на кухне котелок на полке сам стучит крышкой — тук-тук, будто кто-то просится наружу. А ведь он пустой…",short:"котелок на полке сам стучит крышкой, а ведь он пустой",
  pt:()=>{const [x,y]=kam();return[x,y-40,.5];},hr:120,it:"rm_chasen",beast:"rm_bunbuku",who:"Бунбуку-тягама",cute:1,
  words:"Пом! Ой… Не бойся, я Бунбуку. Когда-то я превратился в чайный котёл, да так и не смог стать обратно тануки. А у тёплой печки ночью так уютно… Можно я посплю тут до утра? Вот, возьми мой венчик — с ним чай выходит пенный-пенный."},
 {id:"neko",t:"Отражение в онсэне",room:"onsen",w:[17,19],when:"в сумерки, с пяти до семи вечера",where:"онсэн, вода в купальне",
  say:"В сумерки, когда вода в онсэне темнеет, в ней отражается кошка. Посмотришь — а у отражения два хвоста.",short:"в тёмной воде отражается кошка с двумя хвостами",
  pt:()=>[visX(780,160),1050,.55],hr:150,it:"rm_kagami",beast:"nekomata",who:"Нэкомата",cute:1,
  words:"Мяу. Не пугайся, сестрёнка. Кошка, что проживёт долго-долго, однажды увидит в воде свой второй хвост. Я пришла посмотреть, каким будет твой. Пушистым — я так и знала. Возьми зеркальце: в нём иногда видно, кем ты станешь."},
 {id:"tengu",t:"Тэнгу на сосне",room:"engawa",w:[2,3],when:"в час быка, с двух до трёх ночи",where:"веранда, верхушка старой сосны",
  say:"В саду у веранды растёт старая сосна. В час быка, с двух до трёх ночи, на её верхушке кто-то сидит — большой, с крыльями. И глаза горят, как угольки.",short:"на верхушке сосны сидит кто-то с крыльями",
  pt:()=>[PINE[0],PINE[1]+60,.42],hr:150,it:"rm_hauchiwa",beast:"rm_tengu",who:"Тэнгу",
  words:"Кар!.. То есть доброй ночи. Я тэнгу с горы Курама. Когда-то я учил там фехтованию мальчика Усиваку — потом он стал великим Ёсицунэ. Теперь я стар и люблю тихие сосны: в час быка слышно, как растут иголки. Возьми мой веер — взмахнёшь, и поднимется добрый ветер."},
 {id:"azuki",t:"Кто-то моет фасоль",room:"courtyard",w:[0,24],cond:()=>weather.on,when:"когда идёт дождь, в любое время",where:"дворик, пруд у водопада",
  say:"Когда идёт дождь, у пруда во дворике кто-то моет фасоль: шорх-шорх, шорх-шорх. Подойдёшь — никого, только круги на воде.",short:"в дождь у пруда кто-то моет фасоль: шорх-шорх",
  pt:()=>[visX(1250,130),1045,.55],hr:150,it:"rm_azuki",beast:"rm_azuki",who:"Адзуки-арай",
  words:"Шорх-шорх… Из тумана над прудом кто-то тихонько поёт: «Помыть ли фасоль… или поймать кого-нибудь да съесть?» — и смеётся. Но у воды никого. Только на камне лежит мокрое ситечко с красной фасолью. Адзуки-арая никто не видел — его можно только услышать.",
  soft:"Шорх-шорх… Из тумана над прудом кто-то тихонько поёт: «Помыть ли фасоль… помыть ли…» Но у воды никого. Только на камне лежит мокрое ситечко с красной фасолью. Адзуки-арая никто не видел — его можно только услышать."},
 {id:"fox",t:"Лисьи следы у тории",room:"games",w:[5,7],when:"на рассвете, с пяти до семи утра",where:"лесное святилище, тории",
  say:"На рассвете, пока все спят, у тории в лесном святилище появляются лисьи следы. К воротам ведут — а обратно не ведут.",short:"у тории лисьи следы, и ведут они только туда",
  pt:()=>[1150,1150,.8],hr:210,it:"rm_key",beast:"kitsune",who:"Кицунэ",cute:1,
  words:"Ты встала раньше солнца? Тогда вот тебе лисий секрет: следы на рассвете ведут не туда, откуда пришла лиса, а туда, куда она ещё только пойдёт. Возьми ключик — им в святилищах Инари запирают рисовые амбары. Пусть в этом доме всегда будет рис."},
 {id:"moku",t:"Глаза в кухонном окне",room:"kitchen",w:[12,15],when:"днём, с полудня до трёх",where:"кухня, окно с решёткой",
  say:"Днём, когда в доме тихо, в кухонное окно кто-то подглядывает. Не один — много. Сквозь решётку смотрят глаза и моргают по очереди.",short:"сквозь решётку окна смотрят глаза и моргают",
  pt:()=>[640,400,.5],hr:200,it:"rm_moku",beast:"rm_moku",who:"Мокумокурэн",
  words:"Мы — Мокумокурэн, «множество глаз». Мы живём в старых решётках и сёдзи и смотрим, всё ли в доме хорошо. Раз ты нас заметила — значит, всё хорошо. Возьми на память уголок сёдзи: мы будем приглядывать за Мусей и оттуда."},
 {id:"okiku",t:"Кто-то считает тарелки",room:"bedroom",w:[0,1],cond:()=>S.lampOff,when:"в полночь, с двенадцати до часу, андон погашен",where:"спальня, большое сёдзи",
  say:"Если в полночь погасить андон в спальне, за сёдзи кто-то тихо считает: «Одна… две… три…» — до девяти. И вздыхает.",short:"за сёдзи кто-то считает до девяти и вздыхает",
  pt:()=>[1100,760,.4],hr:260,it:"rm_sara",beast:"rm_okiku",who:"Окику",
  words:"…восемь… девять… Ах, ты не спишь? Я Окику. Мне доверили десять тарелок, одна пропала — и с тех пор я всё считаю. …Муся тихо мяукнула, будто сказала «десять». Окику улыбнулась: «Десять… Спасибо. Сегодня я усну. А эту оставь себе — пусть будет десятой»."},
 {id:"pon",t:"Барабан в полнолуние",room:"courtyard",w:[20,4],cond:moonFull,when:"в полнолуние (и в дни Цукими), с восьми вечера до четырёх утра",where:"дворик, большой камень в пруду",
  say:"В полнолуние во дворике кто-то бьёт в барабан: пон-пон-покон! Звук идёт от большого камня в пруду. Говорят, так веселятся тануки.",short:"в полнолуние от камня в пруду: пон-пон-покон!",
  pt:()=>{const [x,y]=rock();return[x,y-160,.55,y];},hr:170,it:"rm_tsuzumi",beast:"tanuki",who:"Тануки-барабанщик",cute:1,
  words:"Пон-пон-покон! Ой, заметили… Я тануки из храма Сёдзёдзи. Там мы каждое полнолуние устраиваем оркестр: кто в барабан, кто в живот. Настоятель сперва сердился, а потом сам начал подпевать! Держи барабанчик — стучи, когда луна круглая."},
 {id:"kosode",t:"Рукава в гардеробе",room:"wardrobe",w:[1,3],when:"в час быка, с часу до трёх ночи",where:"гардероб, у ширмы",
  say:"В час быка в гардеробе шевелятся кимоно. Висят себе на вешалке, а рукава тихонько колышутся — хотя окна закрыты.",short:"рукава кимоно колышутся, хотя окна закрыты",
  pt:()=>[visX(1180,220),960,.5],hr:220,it:"rm_kosode",beast:"rm_kosode",who:"Косодэ-но-тэ",
  words:"Из рукавов тянутся бледные руки — тонкие, как у той, кто носила это кимоно давным-давно. Они ничего не хватают: разглаживают складки, поправляют воротник, а одна легонько гладит Мусю по голове — и прячется. На вешалке остаётся маленькое кимоно, как раз по росту Муси."}
];
const RI=Object.fromEntries(RUM.map(r=>[r.id,r]));
function st(){return S.ext.rum||(S.ext.rum={k:["kama"],s:{},who:{kama:"Дзасики-вараси"},nw:1});}
function known(r){return st().k.includes(r.id);}
function solved(r){return !!st().s[r.id];}
function openNow(r){return rmIn(r.w,hourNow())&&(!r.cond||r.cond());}
function live(r){return known(r)&&!solved(r)&&openNow(r);}
function here(){return scene.on||overlaysOpen()?null:RUM.find(r=>r.room===S.room&&live(r))||null;}
let roomT=0,rv=null,nextSnd=0,toastNew=0,FFc="";
const FF=()=>FFc||(FFc=getComputedStyle(document.body).fontFamily);
function roomName(id){const r=ROOMS.find(q=>q.id===id);return r?r.ru:id;}

// ── the signs (quiet things inside the painting)
function sign(r,t,a){
  if(r.id==="kama"){const [x0,y0]=kam(),[x,y]=rmPt(x0,y0-66,.5),k=BGM.k,jig=(t%1.6)<.22?Math.abs(Math.sin(t*60))*4*k:0;
    glow(x,y+20*k,90*k,"rgba(255,190,120,A)",.14*a);ctx.save();ctx.globalAlpha=a;ctx.fillStyle="#4a4038";ctx.beginPath();ctx.ellipse(x,y-jig,44*k,8*k,0,0,Math.PI*2);ctx.fill();ctx.strokeStyle="rgba(230,200,150,.5)";ctx.lineWidth=1;ctx.stroke();ctx.fillStyle="#6a5a48";ctx.beginPath();ctx.ellipse(x,y-jig-5*k,8*k,5*k,0,0,Math.PI*2);ctx.fill();
    for(let i=0;i<3;i++){const u=((t*.35+i/3)%1),sx=x+Math.sin(t+i*2)*10*k+(i-1)*18*k,sy=y-10*k-u*110*k;glow(sx,sy,(14+u*26)*k,"rgba(225,220,210,A)",.34*(1-u)*a);}ctx.restore();}
  else if(r.id==="neko"){const [ix,iy,d]=r.pt(),w=Math.sin(t*1.7)*6;ctx.save();ctx.globalAlpha=1;rmMon("m_nekomata",ix+w,iy-30,150,d,null,.22*a*(.8+.2*Math.sin(t*2.3)),Math.PI,true);ctx.restore();
    const [x,y]=rmPt(ix,iy+10,d),k=BGM.k;ctx.save();ctx.strokeStyle=`rgba(200,215,220,${.18*a})`;ctx.lineWidth=1.5;for(let i=0;i<2;i++){const u=(t*.4+i*.5)%1;ctx.beginPath();ctx.ellipse(x,y,(30+u*120)*k,(8+u*30)*k,0,0,Math.PI*2);ctx.globalAlpha=1-u;ctx.stroke();}ctx.restore();}
  else if(r.id==="tengu"){const [x,y]=rmPt(PINE[0],PINE[1]+70,.42),k=BGM.k,bl=(t%5)<.18?.1:1;glow(x,y,70*k,"rgba(255,150,60,A)",.18*a);eyeAt(x-14*k,y,7*k,bl*a,"#ffb44a","#3a1400");eyeAt(x+16*k,y,7*k,bl*a,"#ffb44a","#3a1400");
    const u=(t*.12)%1,[fx,fy]=rmPt(PINE[0]+40+Math.sin(t*1.3)*40,PINE[1]+90+u*700,.42);ctx.save();ctx.globalAlpha=a*(1-u)*.8;ctx.translate(fx,fy);ctx.rotate(Math.sin(t*2)*.8);ctx.fillStyle="#2e2620";ctx.beginPath();ctx.ellipse(0,0,4*k*2,16*k*2,0,0,Math.PI*2);ctx.fill();ctx.restore();}
  else if(r.id==="azuki"){const [ix,iy,d]=r.pt(),k=BGM.k;for(let i=0;i<3;i++){const u=(t*.5+i/3)%1,[x,y]=rmPt(ix+(i-1)*60,iy+(i%2)*14,d);ctx.save();ctx.globalAlpha=a*(1-u)*.5;ctx.strokeStyle="#cfd8d4";ctx.lineWidth=1.4;ctx.beginPath();ctx.ellipse(x,y,(10+u*70)*k,(3+u*18)*k,0,0,Math.PI*2);ctx.stroke();ctx.restore();}
    for(let i=0;i<5;i++){const [x,y]=rmPt(ix-60+i*28+Math.sin(t+i)*8,iy+6+Math.sin(t*1.3+i*2)*6,d);ctx.save();ctx.globalAlpha=a*.7;ctx.fillStyle="#8a2020";ctx.beginPath();ctx.ellipse(x,y,5*k,3.5*k,0,0,Math.PI*2);ctx.fill();ctx.restore();}}
  else if(r.id==="fox"){const n=3+Math.floor(t*1.6)%11,k=BGM.k;for(let i=0;i<Math.min(n,10);i++){const u=i/9,ix=1330-u*250+(i%2?14:-14),iy=1215-u*95,[x,y]=rmPt(ix,iy,.8),s=(1.1-u*.4)*k;
      ctx.save();ctx.globalAlpha=a*.75*(n>11?.5:1)*(1-.5*u);ctx.fillStyle="#dbe8ff";ctx.shadowColor="#9fc0ff";ctx.shadowBlur=10;ctx.beginPath();ctx.ellipse(x,y,9*s,6*s,0,0,Math.PI*2);ctx.fill();for(let j=0;j<4;j++){ctx.beginPath();ctx.arc(x+(j-1.5)*6*s,y-9*s-(j%3?2*s:0),2.8*s,0,Math.PI*2);ctx.fill();}ctx.restore();}
    const [gx,gy]=rmPt(1070,980,.45);glow(gx+Math.sin(t*.7)*30*k,gy+Math.sin(t*1.1)*20*k,40*k,"rgba(160,200,255,A)",.25*a);}
  else if(r.id==="moku"){const k=BGM.k;WIN.forEach(([ix,iy],i)=>{const ph=(t*.23+i*.37)%1,o=ph<.2?Math.sin(ph/.2*Math.PI):0;if(o<=0)return;const [x,y]=rmPt(ix,iy,.5);ctx.save();ctx.globalAlpha=a*.9;eyeAt(x,y,16*k*2,o);ctx.restore();});}
  else if(r.id==="okiku"){const c=sil("m_rm_okiku","#b4c4dc",6),sw=Math.sin(t*.8)*.02;drawSil(c,"m_rm_okiku",1100,1000,560,.4,null,a*(.3+.06*Math.sin(t*1.9)),sw);
    const ph=t%16,n=Math.floor(ph/1.4);if(n<9){const u=(ph%1.4)/1.4,[x,y]=rmPt(1260,560,.4);ctx.save();ctx.globalAlpha=a*.55*Math.sin(u*Math.PI);ctx.font=`italic ${15*view.s}px ${FF()}`;ctx.textAlign="center";ctx.fillStyle="#c8d4e8";
      ctx.fillText(["одна…","две…","три…","четыре…","пять…","шесть…","семь…","восемь…","девять…"][n],x,y-u*18);ctx.restore();}}
  else if(r.id==="pon"){const [ix,iy,d,row]=r.pt(),k=BGM.k,ph=t%2.4,b=ph<.9?Math.abs(Math.sin(ph*Math.PI/.3))*6:0;drawSil(sil("m_tanuki","#0c0c0a",2),"m_tanuki",ix,iy+70,230,d,row,a*.32,0);
    for(const o of [0,.3,.6])if(ph>o&&ph<o+.8){const u=(ph-o)/.8,[x,y]=rmPt(ix,iy-10,d,row);ctx.save();ctx.globalAlpha=a*(1-u)*.5;ctx.strokeStyle="#efe2b8";ctx.lineWidth=2;ctx.beginPath();ctx.arc(x,y-b,(20+u*80)*k,0,Math.PI*2);ctx.stroke();ctx.restore();}}
  else if(r.id==="kosode"){const [ix,iy,d]=r.pt();drawSil(sil("m_rm_kosode","#120c08",5),"m_rm_kosode",ix+30,iy+170,470,d,null,a*.5,Math.sin(t*.9)*.03);}
}
function signSound(r,t){if(t<nextSnd)return;const k={kama:1.6,neko:3.4,tengu:6,azuki:1.3,fox:4.5,moku:5,okiku:1.4,pon:2.4,kosode:4.2}[r.id]||3;nextSnd=t+k;
  if(r.id==="kama"){tone(640,.05,"square",.02);setTimeout(()=>tone(700,.05,"square",.02),90);}
  else if(r.id==="neko")tone(1760,.18,"sine",.02);
  else if(r.id==="tengu"){noise(.35,380,.05);setTimeout(()=>noise(.3,420,.04),260);}
  else if(r.id==="azuki"){noise(.14,2600,.07);setTimeout(()=>noise(.14,2300,.06),330);}
  else if(r.id==="fox")tone(2093,.7,"sine",.014);
  else if(r.id==="moku")tone(90,.4,"sine",.02);
  else if(r.id==="okiku"){if(t%16/1.4<9)clink();}
  else if(r.id==="pon"){pon();setTimeout(pon,300);setTimeout(()=>{tone(150,.22,"sine",.12);tone(90,.3,"sine",.08);},600);}
  else if(r.id==="kosode")noise(.6,5200,.025);}

// ── the reveal: the yōkai shows itself, speaks, leaves a keepsake
function pose(r,t,a){const [ix,iy,d,row]=r.pt(),e=t-rv.t0;
  const k=BGM.k;
  if(r.id==="kama"){const [x0,y0]=kam(),u=smooth(clamp((e-.8)/.8,0,1)),p0=rmPt(x0,y0-10,.5),p1=rmPt(visX(x0+140,110),1245,.8),rise=clamp(e/.6,0,1);
    monS("m_rm_chagama",mix(p0[0],p1[0],u),mix(p0[1],p1[1],u)-Math.sin(u*Math.PI)*90*k-(1-u)*rise*30*k,mix(140,210,u)*k,a);}
  else if(r.id==="neko")rmMon("m_nekomata",ix,1150,280,d,null,a);
  else if(r.id==="tengu"){const u=smooth(clamp((e-.5)/1.3,0,1)),p0=rmPt(PINE[0],PINE[1]+34,.42),p1=rmPt(720,1110,.42);
    monS("m_rm_tengu",mix(p0[0],p1[0],u),mix(p0[1],p1[1],u)-Math.sin(u*Math.PI)*40*k+Math.sin(e*1.6)*3,mix(260,320,u)*k,a);}
  else if(r.id==="azuki"){const im=DIMG.rm_azuki;if(im){const [x,y]=rmPt(ix,iy-4,d),k=BGM.k*1.1;ctx.save();ctx.globalAlpha=a;ctx.drawImage(im,x-90*k,y-100*k,180*k,110*k);ctx.restore();}
    for(let i=0;i<3;i++){const u=(e*.5+i/3)%1,[x,y]=rmPt(ix+(i-1)*50,iy+10,d);ctx.save();ctx.globalAlpha=a*(1-u)*.5;ctx.strokeStyle="#cfd8d4";ctx.beginPath();ctx.ellipse(x,y,(10+u*90)*BGM.k,(3+u*22)*BGM.k,0,0,Math.PI*2);ctx.stroke();ctx.restore();}}
  else if(r.id==="fox")rmMon("m_kitsune",1070,1108,280,.45,null,a);
  else if(r.id==="moku"){const k=BGM.k;WIN.forEach(([x0,y0],i)=>{const [x,y]=rmPt(x0,y0,.5),bl=((e+i*.7)%3.2)<.15?.1:1;eyeAt(x,y,18*k*2,Math.min(1,e*2)*bl*a);});}
  else if(r.id==="okiku")rmMon("m_rm_okiku",visX(1100,150),1262,500,.8,null,a*.92,Math.sin(e*.8)*.01);
  else if(r.id==="pon"){const b=Math.abs(Math.sin(e*Math.PI/.4))*10;rmMon("m_tanuki",ix,iy+70-b,240,d,row,a);if(e>(rv.nn||0)){rv.nn=e+.8;const [x,y]=rmPt(ix,iy-60,d,row);floatFx.push({g:pick(["♪","♫"]),x,y,t});}}
  else if(r.id==="kosode")rmMon("m_rm_kosode",ix,iy+180,440,d,null,a,Math.sin(e*.9)*.015);
}
function reveal(r){
  const R=st(),t=now();rv={r,t0:t,out:0};R.s[r.id]=Date.now();S.owned.add(r.it);loadItem(r.it);disc("rumor",r.id);
  if(!ST.seen.includes(r.beast))ST.seen.push(r.beast);
  award("rm_first");const h=hourNow();if(h>=1&&h<3)award("rm_ushi");if(RUM.every(solved))award("rm_all");save();
  if(r.cute)chime([784,988,1318]);else if(S.scary){tone(70,1.6,"sawtooth",.025);tone(104,1.4,"sine",.03);setTimeout(()=>chime([523,622,784]),900);}else chime([659,784,1046]);
  if(!petAway()){if(!r.cute&&S.scary&&pet.action!=="sleep")start("hide");react(r.cute?"😸":S.scary?"🙀":"😳",2.4);}
  const [x,y]=rmPt(...r.pt());for(let i=0;i<4;i++)floatFx.push({g:"✨",x:x+rand(-30,30),y:y+rand(-20,20),t:t+i*.15});
  setTimeout(()=>dlg({head:r.who,text:!S.scary&&r.soft?r.soft:r.words,img:itemThumb(IT[r.it],70,60),ok:"Спасибо",onOk:()=>{if(rv)rv.out=now();toast(`🗝 Тайна дома: «${IT[r.it].n}»`);sfx("chime");}}),r.id==="moku"?2400:r.id==="kama"||r.id==="tengu"?1900:1400);
  tabDots();hubDot();
}

// ── hooks
hook("boot",()=>{st();roomT=now();for(const r of RUM)if(solved(r))loadItem(r.it);});
hook("room",()=>{roomT=now();if(rv&&rv.r.room!==S.room)rv=null;});
hook("draw",(t,front)=>{if(front||scene.on)return;
  if(rv&&rv.r.room===S.room){const a=clamp((t-rv.t0)/1.2,0,1)*(rv.out?1-clamp((t-rv.out)/1.4,0,1):1);if(rv.out&&a<=0){rv=null;return;}
    const sa=1-clamp((t-rv.t0)/1,0,1);if(sa>0)sign(rv.r,t,sa);pose(rv.r,t,a);return;}
  const r=here();if(!r)return;const a=clamp((t-roomT-2.5)/3,0,1);if(a<=0)return;sign(r,t,a);if(a>.6)signSound(r,t);});
hook("hit",(x,y)=>{if(rv||scene.on)return false;const r=here();if(!r||now()-roomT<3)return false;const [sx,sy]=rmPt(...r.pt()),R=Math.max(44,r.hr*BGM.k);
  if(Math.hypot(x-sx,y-sy)>R)return false;audioInit();reveal(r);return true;});
hook("ev",(ev,d)=>{if(ev!=="guest")return;const R=st(),r=RUM.find(q=>!R.k.includes(q.id));if(!r)return;const gd=GUESTS.find(g=>g.id===d.id);
  R.k.push(r.id);R.who[r.id]=gd?gd.n:"Гость";R.nw=1;toastNew=1;save();const el=$("gdText");if(el)el.textContent+=` А на прощание шепчет: «${r.say}»`;hubDot();});
hook("sec",()=>{if(toastNew&&$("gdlg").hidden&&!scene.on){toastNew=0;setTimeout(()=>toast("👂 Новый слух — загляни в 家"),400);}});
hook("hubDot",()=>{const R=st();return R.nw||RUM.some(live);});
hook("tabDot",room=>RUM.some(r=>r.room===room&&live(r)));
hook("click",key=>{if(!key.startsWith("rm:"))return false;const id=key.slice(3);if(ROOMS.some(q=>q.id===id)){closePanel();goRoom(id);return true;}return false;});
hook("hub",()=>{const R=st();R.nw=0;hubDot();const K=RUM.filter(known),N=RUM.filter(live),left=RUM.length-K.length;
  const now_=N.length?`<p class="rm-now">🕯 Самое время: ${N.map(r=>`«${r.t}» — ${r.where}`).join("; ")}.</p><div class="row">${[...new Set(N.map(r=>r.room))].map(id=>`<button class="btn primary" data-x="rm:${id}">Пойти: ${roomName(id)}</button>`).join("")}</div>`:"";
  return`<div class="hubc"><h4>👂 Слухи <i>噂</i></h4><p>Гости у ворот шепчут о доме. Приди в нужный час в нужное место — там появится тихий знак. Коснись его.</p>${now_}
   <div class="rm-list">${K.map(r=>`<div class="rm-r${solved(r)?" on":""}"><b>${solved(r)?"✓":"・"} ${r.t}</b><span>${r.when[0].toUpperCase()+r.when.slice(1)} · ${r.where}</span><small>«${r.short[0].toUpperCase()+r.short.slice(1)}» — ${R.who[r.id]||"гость"}</small></div>`).join("")}</div>
   <p class="rm-more">${left?`Ещё не рассказано слухов: ${left}. Угощай гостей у ворот.`:`Все слухи рассказаны. Раскрыто ${RUM.filter(solved).length} из ${RUM.length}.`}</p></div>`;});
hook("album",el=>{const n=RUM.filter(solved).length;el.insertAdjacentHTML("beforeend",`<h3 class="bh">Тайны дома</h3><p class="lead">Слухи, которые оказались правдой: ${n} из ${RUM.length}.</p><div class="coll">${RUM.map(r=>{const on=solved(r),b=BESTIARY.find(q=>q[0]===r.beast),img=b&&b[1]?`<img src="assets/mon/${b[1]}.webp" alt="">`:itemThumb(IT[r.it],60,52);
  return`<div class="ci ${on?"on":""}">${img}<small>${on?r.t:"???"}</small></div>`;}).join("")}</div>`);});
document.head.insertAdjacentHTML("beforeend",`<style>.rm-list{display:flex;flex-direction:column;gap:6px;margin-top:8px}.rm-r{padding:7px 10px;border-radius:10px;background:#0a0d0c;border:1px solid var(--line)}.rm-r b{display:block;font-size:14px;color:var(--paper)}
.rm-r span{display:block;font-size:12px;color:var(--sakura);margin-top:2px}.rm-r small{display:block;font-size:12px;line-height:1.35;color:var(--muted);margin-top:3px;font-style:italic}.rm-r.on{opacity:.62}.rm-r.on b{color:#b9c9a4}
.story-body .hubc p.rm-now{color:#f0d9a0}.story-body .hubc p.rm-more{font-size:12px;color:var(--muted)}</style>`);
X.rm={RUM,st,live,here,moonAge,unlockAll(){const R=st();for(const r of RUM)if(!R.k.includes(r.id)){R.k.push(r.id);R.who[r.id]="Каппа";}save();},
  spot(id){const r=RI[id];return rmPt(...r.pt());},tap(id){const b=cv.getBoundingClientRect(),[x,y]=this.spot(id);cv.dispatchEvent(new PointerEvent("pointerdown",{clientX:b.left+x,clientY:b.top+y,bubbles:true,pointerId:1,isPrimary:true}));},reveal(id){reveal(RI[id]);},wake(){roomT=now()-10;}};
}
