{
// ───────────────────────── «Сундук прабабушки»: a kiri chest that gives one old thing a week ─────────────────────────
// An old paulownia nagamochi stands in the attic (in the kura while the attic is boarded up). Once per ISO week (the
// first one at once) it gives a thing wrapped in furoshiki + a page of the family story: great-grandmother Haru and
// her people through the 20th century, 12 weeks, 12 things — slowly explaining why the zashiki-warashi girl of the
// first story lives in the house. Pictures: art/chest_art.py → assets/items/atlas_ob.webp (chest ×3, furoshiki ×3, 12 things).
const OB=S.ext.chest||(S.ext.chest={n:0,wk:"",aw:""});   // n things given; wk = ISO week of the last one; aw = week already told on the postcard
const OB_AT={"closed":[700,289,320,160],"ajar":[536,0,320,215],"open":[0,0,320,287],"f0":[94,289,200,170],"f1":[296,289,200,170],"f2":[498,289,200,170],"ob_kanzashi":[182,621,200,120],"ob_koma":[232,469,130,140],"ob_notebook":[364,469,180,140],"ob_sakazuki":[0,621,180,130],"ob_letter":[546,469,190,140],"ob_fan":[0,469,230,150],"ob_photo":[858,0,150,196],"ob_kokeshi":[0,289,92,178],"ob_furin":[322,0,100,270],"ob_drawing":[738,469,180,140],"ob_chochin":[424,0,110,250],"ob_last":[920,469,170,140]};
const OB_CAT="Сундук прабабушки",OB_N=12;
// the twelve weeks: thing, year, brush kanji, Musya's face, the chapter and a short line for the tap in the room
const OB_W=[
 {id:"ob_kanzashi",n:"Детская шпилька кандзаси",y:"1924",jp:"簪",r:"😺",t:"Шпилька с красной бусиной",
  s:"Одна из пары шпилек, подаренных семилетней Хару. Вторую она оставила на татами для девочки в красном.",p:[
  "Осенью 1924 года семилетней Хару подарили на праздник Сити-го-сан пару шпилек кандзаси: чёрный лак, серебряный цветок сливы и бусина из красного коралла. Одну — в причёску, вторую — про запас.",
  "За праздничным столом Хару пересчитала детей: она, брат Сёта и три двоюродные сестры — пятеро. Пересчитала ещё раз — шестеро. Шестая сидела с краю, в красном кимоно, с ровной чёлкой, и смотрела на шпильку так, как смотрят на самое красивое на свете.",
  "Вечером Хару оставила вторую шпильку в дальней комнате, на татами. Утром шпильки не было, а за сёдзи кто-то тихонько смеялся. Своего имени девочка так и не сказала, и Хару стала звать её Бэни — «алая», по цвету кимоно."]},
 {id:"ob_koma",n:"Волчок Сёты",y:"1925",jp:"独楽",r:"😺",t:"Волчок, который не падал",
  s:"Волчок старшего брата Хару. По ночам он крутился сам — посреди пустой комнаты.",p:[
  "Сёта, старший брат Хару, лучше всех в деревне запускал волчки. Этот он выточил сам из вишнёвого корня и раскрасил тремя красками: красной, зелёной и жёлтой.",
  "Однажды ночью Хару проснулась от тихого жужжания. Посреди тёмной комнаты, на пустом татами, крутился волчок — ровно, не качаясь, будто его только что запустили. Рядом никого не было. Только на татами остались следы маленьких босых ног, и шли они почему-то задом наперёд.",
  "Сёта долго ворчал, что волчок берут без спроса. А потом стал сам оставлять его на ночь у сёдзи. «Пусть играет, — сказал он. — Ей, наверное, скучно одной»."]},
 {id:"ob_notebook",n:"Школьная тетрадь Хару",y:"1926",jp:"帳面",r:"😺",t:"Нас пятеро",
  s:"«Отец. Мать. Сёта. Я. Она». Под вопросом учителя кто-то ответил старинным детским почерком.",p:[
  "В третьем классе учитель велел написать, кто живёт в доме. Хару вывела аккуратно, столбиком: «Отец. Мать. Сёта. Я. Она».",
  "Учитель подчеркнул последнее слово красным карандашом и спросил на полях: «Кто — она?». Под его вопросом кто-то ответил очень мелко: «Я». Хару клялась, что это не она. Почерк и правда был чужой — круглый, старинный, как в книгах, напечатанных задолго до её рождения.",
  "Тетрадь Хару хранила всю жизнь. На последней странице — столбики палочек: каждый вечер, ложась спать, она пересчитывала детей в доме. И каждый вечер их выходило на одного больше."]},
 {id:"ob_sakazuki",n:"Свадебные чашечки",y:"1938",jp:"盃",r:"😺",t:"Лишняя чашечка",
  s:"Чашечки со свадьбы Хару и плотника Кэндзи. Утром на столе нашлась четвёртая — пустая и вымытая.",p:[
  "Весной 1938 года Хару вышла замуж за плотника Кэндзи из соседней долины. Сёта уехал учиться в город, и Кэндзи остался жить в её доме — так решили родители.",
  "На свадьбе жених и невеста трижды пьют сакэ из трёх красных чашечек. Когда гости разошлись, на столе нашлась четвёртая — маленькая, детская, полная до краёв. Её никто не ставил. Утром она была пуста и вымыта.",
  "Хару испугалась, что муж решит, будто в доме нечисто. Кэндзи повертел чашечку в пальцах и рассмеялся: «Значит, она тоже согласна». С тех пор на каждый праздник он ставил на стол лишнюю чашку и ни разу не спросил, для кого."]},
 {id:"ob_letter",n:"Письмо с фронта",y:"1944",jp:"便り",r:"🥺",t:"Зачёркнутая строчка",
  s:"Письмо Кэндзи с войны: «Оставляй ей рис». Сквозь тушь цензора проступает одно детское слово.",p:[
  "В 1943 году Кэндзи забрали на войну. Письма приходили редко и со штампом цензуры: всё, что казалось лишним, замазывали чёрной тушью.",
  "«Хару, ешь сама, даже если риса мало. Но горсть всё равно оставляй ей — в старой миске, как всегда. Пока она в доме, дом будет цел. А раз цел дом, мне есть куда вернуться». Дальше одна строчка замазана целиком.",
  "Если поднести письмо к лампе, сквозь тушь проступает круглый детский почерк — тот самый, из школьной тетради. Одно слово, написанное поверх цензуры: «Вернётся»."]},
 {id:"ob_fan",n:"Веер с золотыми швами",y:"1946",jp:"扇",r:"😺",t:"Починить золотом",
  s:"В ночь пожара сёдзи распахнулись сами. Дом устоял, а сломанный веер Кэндзи починил золотом.",p:[
  "Летом 1945 года горизонт по ночам был красным — горели города. Однажды ночью в доме сами собой распахнулись все сёдзи, и Хару с матерью выбежали в сад. Через минуту ветер принёс искры, и там, где они спали, затлел футон.",
  "Дом устоял. Сломался только старый веер над нишей: рёбра треснули, бумага разошлась на куски.",
  "Кэндзи вернулся осенью 1946 года, худой и молчаливый. Первым делом он починил веер: склеил лаком уруси и присыпал швы золотом, как чинят дорогую посуду. «Сломанное не выбрасывают, — сказал он. — Его чинят золотом, чтобы помнить, где болело»."]},
 {id:"ob_photo",n:"Фотография дома с кошкой",y:"1953",jp:"写真",r:"😺",t:"Тора на веранде",
  s:"Дом, веранда и полосатая кошка Тора. А за сёдзи, на уровне детского роста, светлое пятнышко.",p:[
  "Этот снимок сделал заезжий фотограф осенью 1953 года. Дом, веранда, белые сёдзи. На краю веранды сидит полосатая кошка Тора: она пришла из леса в ту зиму, когда вернулся Кэндзи, и осталась насовсем.",
  "Тора была странной кошкой. Она часами играла с пустотой, подставляла спину невидимой руке и мурлыкала. А спала только в дальней комнате, свернувшись у чьих-то колен, которых никто не видел.",
  "Посмотри внимательно: за сёдзи, на уровне детского роста, светлое пятнышко. Фотограф сказал, что это брак плёнки. Шестилетняя Юки, дочь Хару, сказала, что это Бэни. А Муся смотрит на снимок долго-долго: у Торы точно такие же полоски, как у неё."]},
 {id:"ob_kokeshi",n:"Кокэси Юки",y:"1955",jp:"こけし",r:"😺",t:"Кукла, которая улыбнулась",
  s:"Строгой кукле Юки однажды ночью нарисовали улыбку. Из коробочки Хару пропала капля помады бэни.",p:[
  "Эту кокэси Кэндзи привёз Юки с ярмарки на севере. Мастер нарисовал кукле строгое, почти сердитое лицо, и Юки её боялась: на ночь прятала в шкаф.",
  "Однажды утром кокэси стояла не в шкафу, а у Юкиной подушки. И улыбалась: тонкая красная улыбка, глаза-дуги — чей-то неумелый детский рисунок поверх мастерского. А из коробочки Хару пропала капля помады бэни.",
  "«Вот и выдала себя», — сказала Хару и никого не стала ругать. Юки с того дня спала с куклой в обнимку и подолгу шепталась с кем-то в темноте — со смешками, как с лучшей подругой."]},
 {id:"ob_furin",n:"Фурин с трещинкой",y:"1966",jp:"風鈴",r:"🥺",t:"Колокольчик без ветра",
  s:"Фурин звенел без ветра накануне каждого письма от Юки. А в ночь её болезни звенел так, что треснул.",p:[
  "В 1966 году Юки уехала учиться в Осаку. Дом опустел: детей в нём больше не было — по крайней мере, таких, которых видно.",
  "В ту осень стеклянный фурин на веранде начал звенеть без ветра. Сначала Хару пугалась, потом заметила: он звенит накануне каждого письма от дочери. Звенел — и назавтра приходил конверт. Ни разу не ошибся.",
  "А в ночь, когда Юки в Осаке тяжело заболела, фурин звенел до утра так отчаянно, что треснуло стекло. Хару уехала к дочери первым же поездом и успела вовремя. Треснувший фурин она так и не выбросила."]},
 {id:"ob_drawing",n:"Рисунок Мивы",y:"1989",jp:"絵",r:"😺",t:"Она ждёт кошку",
  s:"Внучка Хару нарисовала девочку в красном и полосатую кошку: «Бэни-тян ждёт кошку».",p:[
  "Каждое лето к бабушке Хару привозили внучку Миву. Взрослые в доме давно ничего не замечали, а Мива с первого же дня пропадала в дальних комнатах и возвращалась оттуда счастливой и пыльной.",
  "В шесть лет она нарисовала вот это: дом, луну, девочку в красном и полосатую кошку. «Это кто?» — спросила Хару. «Это Бэни-тян, она тут живёт, — ответила Мива. — А кошку она ждёт. Говорит, кошка обязательно придёт, только не сейчас».",
  "Хару долго молчала. Тора умерла задолго до рождения Мивы, а про Бэни Хару не рассказывала внучке никогда."]},
 {id:"ob_chochin",n:"Фонарик Хару",y:"2011",jp:"提灯",r:"🥺",t:"Ночь, когда погас фонарь",
  s:"Семьдесят лет Хару зажигала им каменный фонарь у тории: «Пока горит фонарь, я дома».",p:[
  "Семьдесят лет Хару каждый вечер выходила к воротам и зажигала каменный фонарь у тории — вот этим бумажным фонариком. Ещё девочкой она пообещала Бэни: «Пока горит фонарь, я дома».",
  "Когда Хару исполнилось девяносто четыре, Юки забрала её к себе в город. В последний вечер Хару, опираясь на палку, дошла до ворот, зажгла фонарь и сказала в темноту: «Жди. Я вернусь». Свой фонарик она задула и убрала в сундук.",
  "Хару не вернулась. А каменный фонарь горел ещё много лет — без масла, без фитиля, сам по себе: кто-то очень упрямо ждал. Он погас той осенью, когда в доме появилась Муся. Бэни поняла, что ждать больше некого, и ушла искать Хару в лес. Следы вели туда — и ни одного обратно."]},
 {id:"ob_last",n:"Письмо Хару",y:"2011",jp:"後の人へ",r:"🥺",t:"Тому, кто будет жить после",
  s:"Последнее письмо Хару — тем, кто будет жить в доме после неё: «Не бойтесь её».",p:[
  "На самом дне сундука лежит конверт. Почерк дрожит, но буквы ровные, как у школьницы: «Тому, кто будет жить в этом доме после меня».",
  "«Не бойтесь её. Она не призрак. Она — то, чем дом помнит детей, которые в нём смеялись. Я обещала ей, что фонарь у ворот будет гореть. Если он погас — значит, я не вернулась. Пожалуйста, зажгите его снова. Оставляйте ей рис. И заведите кошку: она любит их с тех пор, как у нас жила Тора. Хару».",
  "Всё это в доме уже есть. Фонарь у тории зажгли в самом начале, ещё не зная, для кого. Рис в миске для духа к утру исчезает. А кошка лежит на письме и мурлычет. На лестнице чердака кто-то сидит, болтает босыми ногами и улыбается. В волосах у неё — шпилька с красной бусиной. Точно такая же, как первая."]}];
addItems(OB_W.map(W=>{const a=OB_AT[W.id];return{id:W.id,n:W.n,c:OB_CAT,w:a[2],h:a[3],a:/furin|chochin/.test(W.id)?"t":"b",p:0,at:["ob",a[0],a[1]],
  src:"🧰 сундук прабабушки",hint:"🧰 Сундук прабабушки на чердаке отдаёт одну вещь в неделю"};}),{ob:[1100,751]});
STAMPS.push(["ob_first","簪","Сундук прабабушки","Получи первую вещь из сундука на чердаке"],["ob_six","扇","Полсундука","Шесть вещей из сундука прабабушки"],["ob_all","春","История Хару","Прочитай все 12 глав сундука прабабушки"]);

// ── the week rhythm: one thing per ISO week (Monday to Sunday), the first one at once ──
function obWeek(d=today()){const t=new Date(Date.UTC(d.getFullYear(),d.getMonth(),d.getDate())),wd=t.getUTCDay()||7;t.setUTCDate(t.getUTCDate()+4-wd);
  const y=t.getUTCFullYear();return y+"-W"+String(Math.ceil(((t-Date.UTC(y,0,1))/864e5+1)/7)).padStart(2,"0");}
const obOpenR=id=>!!ROOMX[id]&&!(X.ro&&X.ro.locked&&X.ro.locked(id));
function obRoom(){return obOpenR("attic")?"attic":obOpenR("kura")?"kura":null;}
function obWaits(){return OB.n<OB_N&&OB.wk!==obWeek();}
function obNew(){return obWaits()&&!!obRoom();}
const OB_KJ=["一","二","三","四","五","六","七","八","九","十","十一","十二"],obWk=k=>"第"+OB_KJ[k]+"週";
// the brush font (Yuji Syuku) under its own name, only the glyphs used here
const OB_CH="第週一二三四五六七八九十簪独楽帳面盃便り扇写真こけし風鈴絵提灯後の人へ桐長持春";
const OB_FONT='"ObBrush","Yuji Syuku","Noto Serif JP","Hiragino Mincho ProN","Yu Mincho",serif';
let obFontS=0;function obFontLoad(){if(obFontS)return;obFontS=1;try{fetch("https://fonts.googleapis.com/css2?family=Yuji+Syuku&display=swap&text="+encodeURIComponent(OB_CH)).then(r=>r.text()).then(css=>{const m=css.match(/url\(([^)]+)\)/);if(!m)return;
  return new FontFace("ObBrush",`url(${m[1]})`).load().then(f=>{document.fonts.add(f);obFontS=2;});}).catch(()=>{});}catch(e){}}

// ── giving a thing: the state is saved at once, the scene only shows it ──
function obGive(){if(!obWaits())return -1;const k=OB.n,W=OB_W[k];OB.n=k+1;OB.wk=obWeek();S.owned.add(W.id);disc("chest","w"+OB.n);
  award("ob_first");if(OB.n>=6)award("ob_six");if(OB.n>=OB_N)award("ob_all");S.needs.joy=clamp(S.needs.joy+8,0,100);save();ui();hubDot();tabDots();return k;}

// ── the chest in the room: on the floor left of Musya (attic) or right of her by the casks (kura) ──
let OBI=null;const OB_POS={attic:[600,1192],kura:[1230,1200]},OB_BW=250,OB_TC={};
function obSpot(){const r=obRoom();if(!r||S.room!==r||!OBI)return null;const p=OB_POS[r];return{x:visX(p[0],OB_BW/2+14),y:p[1]};}
function obQuad(b,key){const a=OB_AT[key],[x0,y0]=imgToStage(b.x-OB_BW/2,b.y,CAT_D),[x1]=imgToStage(b.x+OB_BW/2,b.y,CAT_D),w=x1-x0,k=w/320,h=a[3]*k;return{x:x0,y:y0+10*k-h,w,h,k};}
function obTinted(key){const tn=TINT[S.room]||"rgba(20,14,8,.3)",ck=key+"|"+tn;if(OB_TC[ck])return OB_TC[ck];const a=OB_AT[key],c=document.createElement("canvas");c.width=a[2];c.height=a[3];
  const g=c.getContext("2d");g.drawImage(OBI,a[0],a[1],a[2],a[3],0,0,a[2],a[3]);g.globalCompositeOperation="source-atop";g.fillStyle=tn;g.fillRect(0,0,a[2],a[3]);return OB_TC[ck]=c;}
hook("draw",(t,front)=>{if(scene.on)return;const b=obSpot();if(!b||front!==(b.y>catLineY()+6))return;const w8=obWaits(),key=w8?"ajar":"closed",q=obQuad(b,key);
  ctx.drawImage(obTinted(key),q.x,q.y,q.w,q.h);if(!w8)return;
  const gx=q.x+160*q.k,gy=q.y+(key==="ajar"?103:60)*q.k,p=.65+.35*Math.sin(t*2.3),R=150*q.k;   // warm light from the gap, breathing
  ctx.save();ctx.globalCompositeOperation="lighter";const gr=ctx.createRadialGradient(gx,gy,0,gx,gy,R);gr.addColorStop(0,`rgba(255,196,110,${.55*p})`);gr.addColorStop(.35,`rgba(255,170,80,${.16*p})`);gr.addColorStop(1,"rgba(255,150,60,0)");
  ctx.fillStyle=gr;ctx.fillRect(gx-R,gy-R,R*2,R*2);ctx.restore();
  drawEmoji(ctx,"✨",gx+60*q.k*Math.sin(t*.9),gy-40*q.k-10*Math.sin(t*1.7),16*view.s,.35+.35*Math.sin(t*2.6));});
function obHitBox(){const b=obSpot();if(!b)return null;const q=obQuad(b,"ajar");return{x:q.x+8*q.k,y:q.y+60*q.k,w:q.w-16*q.k,h:q.h-60*q.k};}
hook("hit",(x,y)=>{if(scene.on)return;const z=obHitBox();if(!z||x<z.x||x>z.x+z.w||y<z.y||y>z.y+z.h)return;audioInit();obTap();return true;});
function obTap(){const b=obSpot();if(!obWaits()){tone(150,.25,"sawtooth",.02);toast(OB.n>=OB_N?"Сундук пуст: история Хару прочитана":"🔒 Сундук закрыт до понедельника");
    if(!petAway()&&b)walkTo({x:b.x+150},"peek","😼");return;}
  tone(140,.35,"sawtooth",.025);if(!petAway()&&b)walkTo({x:b.x+170},"peek","🧐");const k=obGive();if(k>=0)setTimeout(()=>obScene(k),650);}

// ── the opening scene: the lid lifts, the furoshiki is untied in three taps, the thing and its page appear ──
let obQ=null,obLp=false;
function obPage(k){const W=OB_W[k];return`<div class="ob-paper"><div class="ob-hd"><span class="ob-jp">${obWk(k)}</span><span class="ob-th">${itemThumb(IT[W.id],96,80)}</span><span class="ob-jp ob-jp2">${W.jp}</span></div>
  <h3 class="ob-t">${W.t}</h3><p class="ob-y">${W.n} · ${W.y}</p>${W.p.map(p=>`<p class="ob-pp">${p}</p>`).join("")}<p class="ob-sig">${k===OB_N-1?"春":"桐の長持"}</p></div>`;}
function obBtns(k){const id=OB_W[k].id,pl=S.placed[id];return`<div class="row ob-row">${pl?"":`<button class="btn primary" data-x="ob:put:${k}">Поставить в комнату</button>`}<button class="btn" data-x="ob:book">Все главы</button></div>`;}
function obScene(k){obFontLoad();obQ={k,t0:now(),st:0,taps:0,tt:-9,ft:0};
  openPanel(OB_CAT,`<canvas id="obCv" class="ob-cv" width="720" height="720"></canvas><p class="lead ob-hint" id="obHint">Крышка поддаётся со скрипом…</p><div id="obPg" class="ob-pg" hidden>${obPage(k)}${obBtns(k)}</div>`,"ob");$("xpBody").scrollTop=0;
  $("obCv").addEventListener("pointerdown",obDown);if(!obLp){obLp=true;requestAnimationFrame(function f(){if(obQ&&panelIs("ob")){obDraw();requestAnimationFrame(f);}else obLp=false;});}}
function obDown(){const q=obQ;if(!q||q.st!==1)return;q.taps++;q.tt=now();audioInit();tone(320+q.taps*90,.09,"triangle",.04);
  if(q.taps>=3){q.st=2;q.ft=now();chime([784,988,1175,1568]);const W=OB_W[q.k];if(!petAway())react(W.r,2.4);
    setTimeout(()=>{const P=$("obPg"),h=$("obHint");if(!P||!obQ)return;if(h)h.hidden=true;P.hidden=false;const cv=$("obCv");try{$("xpBody").scrollTo({top:cv.offsetHeight*.62,behavior:"smooth"});}catch(e){}},1100);}
  else{const h=$("obHint");if(h)h.textContent=q.taps===1?"Узел тугой, старый… ещё!":"Ещё один узел — и всё!";}}
const obEase=e=>e<.5?2*e*e:1-Math.pow(-2*e+2,2)/2,obSeg=(e,a,b)=>clamp((e-a)/(b-a),0,1);
let obBg=null;
function obBack(W,H){if(obBg)return obBg;const c=document.createElement("canvas");c.width=W;c.height=H;const g=c.getContext("2d");
  let gr=g.createLinearGradient(0,0,0,H);gr.addColorStop(0,"#1a120c");gr.addColorStop(.56,"#2a1d13");gr.addColorStop(.57,"#1c140d");gr.addColorStop(1,"#120c08");g.fillStyle=gr;g.fillRect(0,0,W,H);
  g.strokeStyle="rgba(0,0,0,.35)";g.lineWidth=2;for(let i=-8;i<=8;i++){g.beginPath();g.moveTo(W/2+i*40,H*.57);g.lineTo(W/2+i*150,H);g.stroke();}
  gr=g.createRadialGradient(W*.45,H*.5,40,W*.45,H*.5,W*.7);gr.addColorStop(0,"rgba(0,0,0,0)");gr.addColorStop(1,"rgba(0,0,0,.7)");g.fillStyle=gr;g.fillRect(0,0,W,H);
  for(let i=0;i<70;i++){g.fillStyle=`rgba(232,220,190,${Math.random()*.25})`;g.fillRect(Math.random()*W,Math.random()*H*.6,1.5,1.5);}return obBg=c;}
function obSpr(g,key,cx,by,s,al=1,rot=0){const a=OB_AT[key];if(!a||!OBI)return;g.save();g.globalAlpha=al;g.translate(cx,by);if(rot)g.rotate(rot);g.drawImage(OBI,a[0],a[1],a[2],a[3],-a[2]*s/2,-a[3]*s,a[2]*s,a[3]*s);g.restore();}
function obDraw(){const cv=$("obCv"),q=obQ;if(!cv||!q)return;const g=cv.getContext("2d"),W=cv.width,H=cv.height,t=now(),e=t-q.t0,CX=280,CB=420,s=1.12;
  g.drawImage(obBack(W,H),0,0);
  // the chest: closed (a small shake) → ajar → open, light from inside
  const ea=obSeg(e,.45,.8),eo=obSeg(e,.95,1.45),sh=e<.45?Math.sin(e*70)*2.2*(1-e/.45):0;
  if(eo<1)obSpr(g,ea<1?"closed":"ajar",CX+sh,CB,s,1-eo);if(ea>0&&ea<1)obSpr(g,"ajar",CX,CB,s,ea*(1-eo));if(eo>0)obSpr(g,"open",CX,CB,s,eo);
  const lg=Math.max(ea*.5,eo)*(.8+.2*Math.sin(t*2.4)),gy=CB-114*s;
  if(lg>0){g.save();g.globalCompositeOperation="lighter";const gr=g.createRadialGradient(CX,gy,0,CX,gy,260);gr.addColorStop(0,`rgba(255,200,120,${.55*lg})`);gr.addColorStop(.4,`rgba(255,170,80,${.2*lg})`);gr.addColorStop(1,"rgba(255,150,60,0)");g.fillStyle=gr;g.fillRect(CX-260,gy-260,520,520);g.restore();}
  if(q.st===0&&e>1.5){q.st=1;const h=$("obHint");if(h)h.textContent="Коснись узелка: фуросики завязан на три узла";}
  // the bundle rises out of the chest and lands in front
  const BX=260,BB=690,bs=1.3;
  if(q.st>=1){const u=obEase(obSeg(e,1.5,2.2)),x=CX+(BX-CX)*u,y=gy+40+(BB-gy-40)*u-150*Math.sin(Math.PI*u),sc=.45+(bs-.45)*u;
    const w=q.st===1?Math.max(0,1-(t-q.tt)/.45):0,rot=Math.sin((t-q.tt)*34)*.09*w,key=q.st===2?"f2":q.taps>=2?"f1":"f0";
    if(q.st===2){const u2=obSeg(t-q.ft,0,.9),ue=obEase(u2);obSpr(g,"f2",BX,BB,bs);
      const I=OB_W[q.k].id,a=OB_AT[I],k2=Math.min(230/a[2],230/a[3],1.4),iy=BB-52-36*ue;
      g.save();g.globalCompositeOperation="lighter";const gr=g.createRadialGradient(BX,iy-a[3]*k2*.5,0,BX,iy-a[3]*k2*.5,170);gr.addColorStop(0,`rgba(255,214,140,${.35*ue})`);gr.addColorStop(1,"rgba(255,180,90,0)");g.fillStyle=gr;g.fillRect(BX-170,iy-a[3]*k2*.5-170,340,340);g.restore();
      obSpr(g,I,BX,iy,k2,ue);}
    else obSpr(g,key,x,y+(q.taps===1&&w>0?0:0),sc*(1+.04*w),1,rot);}
  // Musya beside the chest, sniffing; a wordless bubble once the thing is out
  const st=q.st===2?"purr":"rest",f=q.st===2?3+Math.floor(t*2.5)%2:Math.floor(t*4)%8;if(IMG[st]){g.save();g.translate(600,0);g.scale(-1,1);drawCatG(g,st,f,0,BB-6,1.4);g.restore();}
  if(q.st===2&&t-q.ft>.6){const al=Math.min(1,(t-q.ft-.6)/.3);g.save();g.globalAlpha=al*.92;g.fillStyle="#efe6d2";g.beginPath();g.ellipse(560,360,40,34,0,0,Math.PI*2);g.fill();g.beginPath();g.moveTo(548,390);g.lineTo(572,390);g.lineTo(576,414);g.fill();g.restore();drawEmoji(g,OB_W[q.k].r,560,360,42,al);}
  // the week in brush kanji, the hint for the knot
  g.save();g.font=`48px ${OB_FONT}`;g.textAlign="left";g.textBaseline="top";g.fillStyle="rgba(236,224,196,.85)";g.fillText(obWk(q.k),28,22);g.restore();
  if(q.st===1&&e>2.2&&t-q.tt>1.2)drawEmoji(g,"👆",BX+84,BB-170+8*Math.sin(t*4),44,.85);}
X.ob={OB,week:obWeek,room:obRoom,waits:obWaits,give:obGive,scene:obScene,tap:obDown,hit:obHitBox,
  at(e){if(obQ)obQ.t0=now()-e;},atf(e){if(obQ){obQ.ft=now()-e;obQ.tt=now()-9;}},q:()=>obQ,font:()=>obFontS+" "+document.fonts.check("40px ObBrush","第"),
  tapRoom(){const z=obHitBox();return z?hk("hit",z.x+z.w/2,z.y+z.h/2):"no box";},reset(){OB.n=0;OB.wk="";OB.aw="";obQ=null;}};

// ── reading: the whole book, one page, the album ──
function obBook(){obFontLoad();const rows=OB_W.map((W,k)=>k<OB.n?`<button class="ob-ch" data-x="ob:read:${k}"><span class="ob-th">${itemThumb(IT[W.id],60,50)}</span><span class="ob-tx"><b>Неделя ${k+1}. ${W.t}</b><small>${W.n} · ${W.y}</small></span></button>`
  :`<div class="ob-ch off"><span class="ob-th ob-q">?</span><span class="ob-tx"><b>Неделя ${k+1}</b><small>${k===OB.n&&obWaits()?"ждёт в сундуке":"откроется позже"}</small></span></div>`).join("");
  openPanel(OB_CAT,`<p class="lead">История семьи, которая жила в доме до вас: прабабушка Хару и её родные. Раз в неделю — одна вещь и одна глава. Прочитано ${OB.n} из ${OB_N}.</p><div class="ob-list">${rows}</div>`,"obb");$("xpBody").scrollTop=0;}
function obRead(k){if(k<0||k>=OB.n)return;obFontLoad();openPanel(OB_CAT,`<div class="ob-pg">${obPage(k)}${obBtns(k)}</div>`,"obr");$("xpBody").scrollTop=0;}
hook("click",(key)=>{if(!key.startsWith("ob:"))return;const [,a,v]=key.split(":"),k=+v;
  if(a==="book")obBook();else if(a==="read")obRead(k);
  else if(a==="put"&&OB_W[k]&&S.owned.has(OB_W[k].id)){closePanel();if(!(S.placed[OB_W[k].id]&&S.placed[OB_W[k].id].r===S.room))putItem(OB_W[k].id);}
  else if(a==="go"){const r=obRoom();closePanel();if(!r)return true;if(S.room!==r)goRoom(r);setTimeout(()=>{if(S.room!==r)return;toast(obWaits()?"🧰 Сундук ждёт — коснись его":"🧰 Сундук стоит здесь");const b=obSpot();if(b&&!petAway()&&!scene.on)walkTo({x:b.x+170},"peek","🧐");},900);}
  else if(a==="open"&&obWaits())obTap();
  return true;});
hook("panelClose",id=>{if(id==="ob")obQ=null;});
hook("itemTap",(it)=>{const k=OB_W.findIndex(W=>W.id===it.id);if(k<0)return;const W=OB_W[k];chime([659,784]);fxAt(it,["✨"],2);
  if(!petAway()&&pet.action!=="sleep")walkTo(it,"peek",W.r);
  dlg({head:`${W.n} · ${W.y}`,text:W.s,img:itemThumb(IT[W.id],90,72),ok:"Читать главу",no:"Закрыть",onOk:()=>obRead(k)});return true;});
hook("album",el=>{for(const h of [...el.querySelectorAll("h4.ch")])if(h.textContent===OB_CAT){const n=h.nextElementSibling;if(n&&n.classList.contains("coll"))n.remove();h.remove();}
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">${OB_CAT}</h3><p class="lead">${OB.n?`Прочитано глав: ${OB.n} из ${OB_N}. Нажми на вещь, чтобы перечитать её историю.`:"Старый сундук на чердаке: раз в неделю — одна вещь и одна глава истории дома."}</p>
  <div class="coll">${OB_W.map((W,k)=>k<OB.n?`<button class="ci on ob-ci" data-x="ob:read:${k}">${itemThumb(IT[W.id],70,52)}<small>${W.n}<br><i>${W.y}</i></small></button>`:`<div class="ci">${itemThumb(IT[W.id],70,52)}<small>???<br><i>неделя ${k+1}</i></small></div>`).join("")}</div>`);});

// ── the hub card, dots, the tray, the postcard ──
hook("hub",()=>{const r=obRoom(),w8=obWaits();
  const st=!r?"Сундук стоит на чердаке — сначала открой чердак":OB.n>=OB_N?`Вся история прочитана: ${OB_N} вещей из ${OB_N}`:w8?`В сундуке новая вещь — неделя ${OB.n+1} из ${OB_N}`:"Следующая вещь — в понедельник";
  const where=r==="kura"?"Пока чердак заколочен, сундук ждёт в куре, у бочек.":"Он стоит на чердаке, у старого нагамоти.";
  const body=`Старый сундук из павловнии с железными уголками. ${r?where+" ":""}Раз в неделю он отдаёт одну вещь, завёрнутую в фуросики, и страницу истории семьи, что жила в доме до вас.`;
  const b=[r&&(w8||OB.n<OB_N)?`<button class="btn${w8?" primary":""}" data-x="ob:go">${w8?"Открыть сундук":"К сундуку"}</button>`:"",OB.n?`<button class="btn" data-x="ob:book">Читать историю</button>`:""].join("");
  return`<div class="hubc"><h4>🧰 ${OB_CAT} <i>桐の長持</i></h4><p>${st}</p><p class="ob-s">${body}${OB.n?` Прочитано глав: ${OB.n} из ${OB_N}.`:""}</p>${b?`<div class="row">${b}</div>`:""}</div>`;});
hook("hubDot",obNew);
hook("tabDot",r=>r===obRoom()&&obNew());
hook("tray",(tray,room)=>{if(room!==obRoom()||!obWaits()||(S.trayMode[room]||"play")!=="play"||tray.querySelector('[data-x="ob:open"]'))return;
  const b=`<button class="item wide" data-x="ob:open"><span class="ico">🎁</span><span class="nm">Новая вещь в сундуке</span></button>`,row=tray.querySelector(".items");
  if(row)row.insertAdjacentHTML("afterbegin",b);else tray.querySelector(".glist")?.insertAdjacentHTML("beforebegin",`<div class="items">${b}</div>`);});
hook("away",()=>{if(!obNew()||OB.aw===obWeek()||!OB.n)return;OB.aw=obWeek();return{i:"🧰",t:`В сундуке прабабушки новая вещь — неделя ${OB.n+1} из ${OB_N}`};});
let obLast=null;hook("sec",()=>{const v=obNew();if(v!==obLast){obLast=v;hubDot();tabDots();if(S.room===obRoom())ui();}});
hook("boot",()=>{atlasImg("ob",im=>{OBI=im;});obFontLoad();});

document.head.insertAdjacentHTML("beforeend",`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Kurale&display=swap"><style>
.ob-cv{width:100%;height:auto;aspect-ratio:1;display:block;border-radius:12px;margin:2px 0 8px;background:#120c08;box-shadow:0 0 0 1px var(--line);touch-action:manipulation;cursor:pointer}
:is(.story-body,.card) p.ob-hint{text-align:center;margin:0 0 10px}
.ob-paper{position:relative;margin:6px 0 12px;padding:16px 16px 12px;border-radius:4px;color:#2b2119;
 background:radial-gradient(circle at 18% 12%,rgba(150,110,60,.18),transparent 32%),radial-gradient(circle at 86% 78%,rgba(140,100,50,.2),transparent 36%),repeating-linear-gradient(90deg,rgba(120,90,50,.05) 0 1px,transparent 1px 7px),linear-gradient(#ebe0c6,#e1d3b3);
 box-shadow:inset 0 0 38px rgba(110,80,40,.38),0 8px 22px rgba(0,0,0,.45)}
.ob-hd{display:flex;align-items:center;justify-content:space-between;gap:8px;border-bottom:1px solid rgba(80,50,30,.25);padding-bottom:8px;margin-bottom:8px}
.ob-jp{font-family:${OB_FONT};font-size:26px;line-height:1;color:#3a2418;writing-mode:vertical-rl;letter-spacing:2px}.ob-jp2{color:#9a2a22}
.ob-hd .ob-th{flex:1;display:flex;justify-content:center}
:is(.story-body,.card) h3.ob-t{font-family:var(--display);font-size:22px;font-weight:600;color:#2b1d14;margin:2px 0 2px;text-align:center}
:is(.story-body,.card) p.ob-y{text-align:center;font-size:12px;color:#7a5e44;margin:0 0 10px;letter-spacing:.5px}
:is(.story-body,.card) p.ob-pp{font-family:Kurale,var(--display),serif;font-size:15px;line-height:1.6;color:#2b2119;margin:0 0 9px;text-indent:1.2em}
:is(.story-body,.card) p.ob-sig{text-align:right;font-family:${OB_FONT};font-size:22px;color:#9a2a22;margin:4px 2px 0}
:is(.story-body,.card) p.ob-s{color:var(--muted);font-size:12.5px}
.ob-row{margin-bottom:10px}
.ob-list{display:flex;flex-direction:column;gap:6px;margin-bottom:12px}
.ob-ch{display:flex;align-items:center;gap:10px;width:100%;text-align:left;padding:6px 8px;border-radius:10px;background:#0a0d0c;border:1px solid var(--line);color:var(--paper);font:inherit;cursor:pointer}
.ob-ch.off{opacity:.5;cursor:default}.ob-ch .ob-th{flex:none;width:62px;display:flex;justify-content:center}.ob-ch .ob-q{font-size:22px;color:var(--muted)}
.ob-tx{display:flex;flex-direction:column;gap:2px;min-width:0}.ob-tx b{font-weight:600;font-size:14px}.ob-tx small{font-size:12px;color:var(--muted)}
button.ci.ob-ci{font:inherit;color:inherit;cursor:pointer}.ci small i{font-style:normal;color:var(--muted);font-size:11px}
</style>`);
}
