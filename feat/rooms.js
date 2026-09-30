{
// ───────────────────────── «Дом открывается постепенно»: rooms that open one by one ─────────────────────────
// The kura (storehouse), the attic, the tea house and the shrine stand closed. The first one still closed is being
// cleared: three stages, each a task caught from game events, at most one stage ticked per calendar day. The kura
// also opens with the key from the first story. The tea house and the shrine are painted by the rooms2 add-on: they
// join the queue only when ROOMX has them. This block paints nothing itself: art/rooms_art.py made the pictures.
const RS=S.ext.rooms||(S.ext.rooms={});for(const k of ["open","prog","done","fresh","act"])RS[k]=RS[k]||{};
const RO_ORDER=["kura","attic","chashitsu","hokora"];
// pictures: art/rooms_art.py → assets/items/atlas_att|kra.webp (items), assets/layers/ro_boards.webp (boards, padlock, cobweb)
const RO_IT=[{"id":"at_nagamochi","n":"Сундук нагамоти","c":"Чердак","w":300,"h":190,"a":"b","p":160,"at":["att",758,382]},{"id":"at_tansu","n":"Пыльный комод тансу","c":"Чердак","w":220,"h":270,"a":"b","p":200,"at":["att",406,0]},{"id":"at_kiribako","n":"Стопка ящиков из павловнии","c":"Чердак","w":180,"h":210,"a":"b","p":90,"at":["att",242,382]},{"id":"at_hina_doll","n":"Забытая кукла итимацу","c":"Чердак","w":120,"h":150,"a":"b","p":120,"at":["att",516,604]},{"id":"at_hoshigaki","n":"Связка сушёной хурмы","c":"Чердак","w":110,"h":280,"a":"t","p":50,"at":["att",294,0]},{"id":"at_herbs","n":"Пучки сушёных трав","c":"Чердак","w":200,"h":190,"a":"t","p":40,"at":["att",1060,382]},{"id":"at_nawa","n":"Моток соломенной верёвки","c":"Чердак","w":180,"h":110,"a":"b","p":20,"at":["att",698,786]},{"id":"at_kumo","n":"Паутина в углу","c":"Чердак","w":200,"h":200,"a":"t","p":10,"at":["att",424,382]},{"id":"at_mino","n":"Соломенный плащ мино","c":"Чердак","w":170,"h":250,"a":"t","p":70,"at":["att",760,0]},{"id":"at_sugegasa","n":"Старая шляпа сугэгаса","c":"Чердак","w":220,"h":110,"a":"b","p":40,"at":["att",880,786]},{"id":"at_zaru","n":"Стопка бамбуковых сит","c":"Чердак","w":170,"h":150,"a":"b","p":30,"at":["att",638,604]},{"id":"at_kago","n":"Корзина со старыми клубками","c":"Чердак","w":160,"h":170,"a":"b","p":40,"at":["att",222,604]},{"id":"at_andon","n":"Пыльный андон","c":"Чердак","w":110,"h":220,"a":"b","p":90,"glow":[55,115],"at":["att",1206,0]},{"id":"at_itoguruma","n":"Прялка итогурума","c":"Чердак","w":240,"h":220,"a":"b","p":150,"at":["att",0,382]},{"id":"at_books","n":"Стопка старых книг","c":"Чердак","w":150,"h":120,"a":"b","p":40,"at":["att",152,786]},{"id":"at_wagasa","n":"Рваный зонтик вагаса","c":"Чердак","w":130,"h":260,"a":"b","p":30,"at":["att",628,0]},{"id":"at_kagami","n":"Мутное зеркало","c":"Чердак","w":130,"h":200,"a":"b","p":80,"at":["att",626,382]},{"id":"at_mokuba","n":"Деревянная лошадка","c":"Чердак","w":220,"h":180,"a":"b","p":120,"at":["att",0,604]},{"id":"at_daruma","n":"Выцветший дарума","c":"Чердак","w":120,"h":130,"a":"b","p":30,"at":["att",1124,604]},{"id":"at_tako","n":"Старый воздушный змей","c":"Чердак","w":180,"h":240,"a":"t","p":50,"at":["att",1024,0]},{"id":"at_chochin","n":"Сложенный фонарь тётин","c":"Чердак","w":90,"h":130,"a":"t","p":30,"at":["att",1246,604]},{"id":"at_furoshiki","n":"Узелок фуросики","c":"Чердак","w":150,"h":110,"a":"b","p":30,"at":["att",1102,786]},{"id":"at_geta","n":"Старые гэта","c":"Чердак","w":140,"h":70,"a":"b","p":20,"at":["att",304,918]},{"id":"at_hoki","n":"Веник хоки","c":"Чердак","w":90,"h":250,"a":"b","p":20,"at":["att",932,0]},{"id":"at_nezumitori","n":"Мышеловка без мышей","c":"Чердак","w":120,"h":70,"a":"b","p":15,"at":["att",446,918]},{"id":"at_hashigo","n":"Лестница хасиго","c":"Чердак","w":160,"h":380,"a":"b","p":60,"at":["att",0,0]},{"id":"at_tsuzura","n":"Плетёный короб цудзура","c":"Чердак","w":200,"h":150,"a":"b","p":90,"at":["att",810,604]},{"id":"at_futon","n":"Свёрнутый старый футон","c":"Чердак","w":240,"h":120,"a":"b","p":60,"at":["att",304,786]},{"id":"at_tokei","n":"Часы с маятником","c":"Чердак","w":130,"h":310,"a":"b","p":180,"at":["att",162,0]},{"id":"at_haribako","n":"Шкатулка для рукоделия","c":"Чердак","w":150,"h":130,"a":"b","p":50,"at":["att",0,786]},{"id":"at_f_letter","n":"Письмо без адреса","c":"Чердак","w":150,"h":100,"a":"b","p":60,"src":"🐾 находка на чердаке","hint":"Эта вещь найдётся в сундуке на чердаке — роется Муся раз в день","at":["att",0,918]},{"id":"at_f_buriki","n":"Жестяная рыбка","c":"Чердак","w":150,"h":100,"a":"b","p":80,"src":"🐾 находка на чердаке","hint":"Эта вещь найдётся в сундуке на чердаке — роется Муся раз в день","at":["att",152,918]},{"id":"at_f_ohajiki","n":"Мешочек стекляшек охадзики","c":"Чердак","w":130,"h":110,"a":"b","p":60,"src":"🐾 находка на чердаке","hint":"Эта вещь найдётся в сундуке на чердаке — роется Муся раз в день","at":["att",1254,786]},{"id":"at_f_photo","n":"Старая фотография","c":"Чердак","w":130,"h":160,"a":"b","p":80,"src":"🐾 находка на чердаке","hint":"Эта вещь найдётся в сундуке на чердаке — роется Муся раз в день","at":["att",384,604]},{"id":"at_f_neko","n":"Фарфоровая кошка без уха","c":"Чердак","w":110,"h":140,"a":"b","p":90,"src":"🐾 находка на чердаке","hint":"Эта вещь найдётся в сундуке на чердаке — роется Муся раз в день","at":["att",1012,604]},{"id":"at_f_musicbox","n":"Музыкальная шкатулка","c":"Чердак","w":150,"h":120,"a":"b","p":120,"src":"🐾 находка на чердаке","hint":"Эта вещь найдётся в сундуке на чердаке — роется Муся раз в день","at":["att",546,786]},{"id":"kr_tawara","n":"Рисовые мешки тавара","c":"Кура","w":250,"h":190,"a":"b","p":90,"at":["kra",284,292]},{"id":"kr_komodaru","n":"Бочка сакэ в соломе","c":"Кура","w":150,"h":170,"a":"b","p":120,"at":["kra",992,292]},{"id":"kr_misodaru","n":"Бочка мисо","c":"Кура","w":170,"h":160,"a":"b","p":100,"at":["kra",284,504]},{"id":"kr_kame","n":"Глиняный кувшин камэ","c":"Кура","w":150,"h":190,"a":"b","p":70,"at":["kra",536,292]},{"id":"kr_umeboshi","n":"Кувшин умэбоси","c":"Кура","w":120,"h":140,"a":"b","p":60,"at":["kra",1012,504]},{"id":"kr_kiribako","n":"Ящики из павловнии","c":"Кура","w":200,"h":180,"a":"b","p":90,"at":["kra",790,292]},{"id":"kr_tansu","n":"Лестничный комод кайдан-дансу","c":"Кура","w":220,"h":290,"a":"b","p":260,"at":["kra",0,0]},{"id":"kr_chest","n":"Окованный сундук","c":"Кура","w":240,"h":170,"a":"b","p":180,"at":["kra",1144,292]},{"id":"kr_senryobako","n":"Денежный сундук сэнрёбако","c":"Кура","w":200,"h":140,"a":"b","p":220,"at":["kra",1134,504]},{"id":"kr_chochin","n":"Фонарь хозяина кура","c":"Кура","w":100,"h":190,"a":"t","p":60,"glow":[50,104],"at":["kra",688,292]},{"id":"kr_shelf","n":"Полка с кувшинами","c":"Кура","w":260,"h":280,"a":"b","p":150,"at":["kra",222,0]},{"id":"kr_tokkuri","n":"Кувшинчики токкури","c":"Кура","w":150,"h":110,"a":"b","p":40,"at":["kra",304,676]},{"id":"kr_masu","n":"Мерки для риса масу","c":"Кура","w":160,"h":100,"a":"b","p":30,"at":["kra",608,676]},{"id":"kr_usu","n":"Ступа и молот для моти","c":"Кура","w":220,"h":250,"a":"b","p":140,"at":["kra",950,0]},{"id":"kr_hakari","n":"Весы-безмен","c":"Кура","w":170,"h":260,"a":"t","p":60,"at":["kra",778,0]},{"id":"kr_soroban","n":"Счёты соробан","c":"Кура","w":190,"h":80,"a":"b","p":40,"at":["kra",892,676]},{"id":"kr_daifukucho","n":"Торговая книга дайфукутё","c":"Кура","w":130,"h":210,"a":"t","p":50,"at":["kra",0,292]},{"id":"kr_yoroibitsu","n":"Доспехи предков в ящике","c":"Кура","w":200,"h":250,"a":"b","p":280,"at":["kra",1172,0]},{"id":"kr_zeni","n":"Связка монет мон","c":"Кура","w":140,"h":60,"a":"b","p":40,"at":["kra",1084,676]},{"id":"kr_nekoe","n":"Картина с кошкой от мышей","c":"Кура","w":150,"h":210,"a":"t","p":60,"at":["kra",132,292]},{"id":"kr_sumi","n":"Мешок древесного угля","c":"Кура","w":180,"h":150,"a":"b","p":30,"at":["kra",456,504]},{"id":"kr_oke","n":"Деревянная кадка","c":"Кура","w":170,"h":150,"a":"b","p":40,"at":["kra",638,504]},{"id":"kr_jo","n":"Старинный замок эбису-дзё","c":"Кура","w":140,"h":170,"a":"t","p":70,"at":["kra",0,504]},{"id":"kr_daikon","n":"Вяленый дайкон на верёвке","c":"Кура","w":170,"h":280,"a":"t","p":30,"at":["kra",484,0]},{"id":"kr_tebako","n":"Лаковая шкатулка тэбако","c":"Кура","w":150,"h":110,"a":"b","p":90,"at":["kra",456,676]},{"id":"kr_ishiusu","n":"Каменные жернова","c":"Кура","w":200,"h":150,"a":"b","p":110,"at":["kra",810,504]},{"id":"kr_hibachi","n":"Жаровня хибати","c":"Кура","w":160,"h":140,"a":"b","p":90,"at":["kra",0,676]},{"id":"kr_tetsubin","n":"Чугунный чайник тэцубин","c":"Кура","w":140,"h":140,"a":"b","p":60,"at":["kra",162,676]},{"id":"kr_shoyu","n":"Бочонок соевого соуса","c":"Кура","w":140,"h":170,"a":"b","p":70,"at":["kra",142,504]},{"id":"kr_komebukuro","n":"Мешочек риса","c":"Кура","w":120,"h":90,"a":"b","p":20,"at":["kra",770,676]},{"id":"kr_byobu","n":"Сложенная ширма","c":"Кура","w":120,"h":270,"a":"b","p":110,"at":["kra",656,0]}];
const RO_ATL={"att":[1400,1018],"kra":[1400,816]},RO_SPR={"b0":[0,4,1000,104],"b1":[0,120,1000,104],"b2":[0,236,1000,104],"lock":[0,360,164,196],"web":[168,360,200,200]};
addItems(RO_IT,RO_ATL);
const RO_L=[["wall",0.4],["floor",0.8],["near",1.4]],RO_L3={wall:{g:1140},floor:{g:1140},near:{ext:.22}};
addRoom({id:"kura",jp:"蔵",ru:"Кура",hint:"Старая кладовая: рис, сакэ и мисо, а на полках — ящики из павловнии. Внизу — чем заняться.",label:"Кладовая",
  layers:RO_L,l3:RO_L3,mote:[1,.86,.66],tint:"rgba(18,16,12,.32)",cat:"Кура",tray:()=>roTray("kura")});
addRoom({id:"attic",jp:"屋根裏",ru:"Чердак",hint:"Пыльный чердак: сундуки, хурма на верёвках и луна в круглом окошке. Сундук можно перерыть раз в день.",label:"Чердак",
  layers:RO_L,l3:RO_L3,mote:[1,.85,.62],tint:"rgba(20,14,8,.3)",cat:"Чердак",tray:()=>roTray("attic")});

// what is done at each stage (a) and what the player does for it (t, caught as qev(ev,d)); w = where to do it
const W_={harvest:"Дворик → 🌱 Огород",cook:"Кухня → 🍳 Готовить",guest:"Вход: гость-ёкай приходит раз в день",put:"Любая комната → 🧺 Вещи",
  fish:"Дворик → 🎣 Рыбалка",game:"Вкладка «Игры»",bath:"Онсэн: намыль Мусю и смой ковшом",pray:"Вход → 🙏 Помолиться",kaidan:"Спальня → Кайдан на ночь"};
const isFish=d=>!!d&&!!FOOD[d.id]&&FOOD[d.id].k==="fish",isGame=d=>{const g=GAMES.find(x=>x.id===(d&&d.id));return !g||!g.hidden;};
const RO={
 kura:{n:"Кура",t:"Запертая кладовая",ok:"Кура открыта",
  p:"Каменная кладовая за домом. Дверь толщиной в ладонь заперта с прошлого века, изнутри пахнет рисом и старым деревом. По ночам там кто-то шуршит. Наверное, мыши.",
  st:[{a:"Разобрать завал у двери",t:"Собери 3 урожая на огороде",ev:"harvest",n:3},{a:"Смазать ржавые петли",t:"Приготовь 2 блюда",ev:"cook",n:2},
      {a:"Отодвинуть засов",t:"Угости гостя у ворот",ev:"guest",n:1}]},
 attic:{n:"Чердак",t:"Заколоченный чердак",ok:"Чердак открыт",
  p:"Люк на чердак заколочен тремя досками. Сверху пахнет пылью и сушёной хурмой, а в щель видно круглое окошко с луной. Муся сидит под люком и не сводит с него глаз.",
  st:[{a:"Снять первую доску",t:"Поставь 5 вещей в комнатах",ev:"put",n:5},{a:"Снять вторую доску",t:"Поймай 2 рыбы",ev:"fish",n:2,test:isFish},
      {a:"Открыть люк",t:"Сыграй в мини-игру",ev:"game",n:1,test:isGame}]},
 chashitsu:{n:"Чайный домик",t:"Заросший чайный домик",ok:"Чайный домик открыт",
  p:"За бамбуком в глубине сада прячется чайный домик. Войти в него можно только склонившись — через низкую дверцу нидзиригути. Её затянуло плющом, а на пороге стоит чья-то забытая чашка.",
  st:[{a:"Срезать плющ с дверцы",t:"Искупай Мусю в онсэне",ev:"bath",n:1},{a:"Вымести сухие листья",t:"Приготовь 2 блюда",ev:"cook",n:2},
      {a:"Отворить нидзиригути",t:"Угости гостя у ворот",ev:"guest",n:1}]},
 hokora:{n:"Святилище",t:"Забытое святилище",ok:"Святилище открыто",
  p:"У старой тропы, за воротами, стоит крошечное святилище. Верёвка симэнава истлела, лисы у входа поросли мхом. Кто-то всё же оставляет там рисовые колобки — и никто не видел, кто.",
  st:[{a:"Расчистить тропинку",t:"Собери 3 урожая на огороде",ev:"harvest",n:3},{a:"Сплести новую симэнаву",t:"Помолись у храма у входа",ev:"place",n:1,test:a=>a==="pray",w:"pray"},
      {a:"Зажечь лампадку",t:"Прочитай кайдан на ночь",ev:"kaidan",n:1}]}
};
const roWhere=s=>W_[s.w||s.ev]||"";
function roKey(){return !!(QS.done||S.owned.has("r_key"));}
function roLocked(id){return RO_ORDER.includes(id)&&!!ROOMX[id]&&!RS.open[id];}
function roCur(){return RO_ORDER.find(roLocked)||null;}
function roReady(id){const s=RO[id].st[RS.done[id]||0];return !!s&&(RS.prog[id]||0)>=s.n;}
// the key from the first story opens the kura at once (quietly at boot, with a toast when the story has just ended)
function roSync(quiet){if(RS.open.kura||!ROOMX.kura||!roKey())return;RS.open.kura=Date.now();RS.fresh.kura=1;disc("room","kura");save();buildTabs();tabDots();hubDot();
  if(!quiet)setTimeout(()=>{toast("🗝 Ключ подошёл — кура открыта");chime([659,880,1046]);},1200);}

// ── the closed-room panel: a darkened look inside, boards on top, three stages ──
let roB=null,roPv=null;ldImg("assets/layers/ro_boards.webp",im=>{roB=im;if(panelIs("ro")&&roPv)roDraw(roPv);});
const RO_BP=[[360,128,-.16],[360,226,.11],[360,322,-.05]];
let roAn=null,roLoop=false;   // the board that is falling off right now: {id,i,t}
function roDraw(id){const cv=$("roPrev");if(!cv)return;const g=cv.getContext("2d"),W=cv.width,H=cv.height,t=now(),k=RS.done[id]||0,anim=roAn&&roAn.id===id&&t-roAn.t<1?roAn:null;
  g.fillStyle="#0a0806";g.fillRect(0,0,W,H);
  for(const [ln] of LAYERS[id]||[]){const im=LIMG[id+"_"+ln];if(im)g.drawImage(im,0,250,1800,1100,0,0,W,H);}
  g.fillStyle="rgba(8,6,4,.58)";g.fillRect(0,0,W,H);
  const vg=g.createRadialGradient(W/2,H*.55,H*.18,W/2,H*.55,W*.62);vg.addColorStop(0,"rgba(0,0,0,0)");vg.addColorStop(1,"rgba(0,0,0,.78)");g.fillStyle=vg;g.fillRect(0,0,W,H);
  if(roB){const w=RO_SPR.web;g.globalAlpha=.75;g.drawImage(roB,w[0],w[1],w[2],w[3],0,0,180,180);g.globalAlpha=1;
    for(let i=0;i<3;i++){const [x,y,a]=RO_BP[i],s=RO_SPR["b"+i];let dy=0,da=0,al=1;
      if(anim&&anim.i===i){const e=clamp((t-anim.t)/.9,0,1);if(e>=1)continue;dy=e*e*280;da=e*.55*(i%2?1:-1);al=1-e*e;}else if(i<k)continue;
      g.save();g.globalAlpha=al;g.translate(x,y+dy);g.rotate(a+da);g.shadowColor="rgba(0,0,0,.65)";g.shadowBlur=16;g.shadowOffsetY=7;g.drawImage(roB,s[0],s[1],s[2],s[3],-430,-45,860,90);g.restore();}
    if(id==="kura"&&!(anim&&k>=3)){const L=RO_SPR.lock;g.drawImage(roB,L[0],L[1],L[2],L[3],W/2-44,190,88,105);}}
  if(anim&&!roLoop){roLoop=true;requestAnimationFrame(function f(){if(panelIs("ro")&&roAn&&now()-roAn.t<1){roDraw(roPv);requestAnimationFrame(f);}else{roLoop=false;if(panelIs("ro"))roDraw(roPv);}});}}
function roPanel(id,anim){const I=RO[id],cur=roCur(),k=RS.done[id]||0,today_=RS.day===dayKey();
  const rows=I.st.map((s,i)=>{if(i<k)return`<li class="ok">${s.a}</li>`;if(id!==cur||i>k)return`<li class="ro-dim">${s.a}</li>`;
    if(today_)return`<li>${s.a}<small>Сегодня уже потрудились — этот этап завтра.</small></li>`;const p=Math.min(RS.prog[id]||0,s.n);
    return p>=s.n?`<li class="ro-go">${s.a}<small>${s.t} — готово! Можно браться за доски.</small></li>`:`<li>${s.a}: <em>${s.t}</em>${s.n>1?` · ${p}/${s.n}`:""}<small>${roWhere(s)}</small></li>`;}).join("");
  const btn=id===cur&&!today_&&roReady(id)?`<div class="row"><button class="btn primary" data-x="ro:tick:${id}">${k===2?"🔓":"🔨"} ${I.st[k].a}</button></div>`:"";
  openPanel(I.t,`<canvas id="roPrev" class="ro-prev" width="720" height="440"></canvas><p>${I.p}</p>${id!==cur&&cur?`<p class="lead">Сначала нужно расчистить «${RO[cur].n}».</p>`:""}<ol class="qtasks ro-st">${rows}</ol>${btn}`+
    `${id==="kura"?`<p class="lead">🗝 Или найди ключ — его отдаст история «Дом, где погас фонарь».</p>`:""}<p class="lead">Один этап в день: старые доски держатся крепко.</p>`,"ro");
  if(anim)roAn=Object.assign({id},anim);roPv=id;roDraw(id);}
function roTick(id){if(id!==roCur()||!roReady(id)||RS.day===dayKey())return;const k=RS.done[id]||0;
  RS.done[id]=k+1;RS.prog[id]=0;RS.day=dayKey();save();knock();tabDots();hubDot();
  if(k+1<3){roPanel(id,{i:k,t:now()});setTimeout(()=>toast("✓ "+RO[id].st[k].a),300);return;}
  RS.open[id]=Date.now();disc("room",id);save();roPanel(id,{i:2,t:now()});chime([784,1046,1318,1568]);
  setTimeout(()=>{closePanel();buildTabs();goRoom(id);tabDots();hubDot();toast("✨ "+RO[id].ok+"!");
    const b=document.querySelector(`#tabs [data-room="${id}"]`);if(b)b.scrollIntoView({inline:"center",block:"nearest"});
    setTimeout(()=>{if(!petAway()&&!scene.on){burst(14);react("😻",2);S.needs.joy=clamp(S.needs.joy+10,0,100);}},900);},1100);}

// ── tasks are caught from game events; only the room being cleared counts, and not on a day a stage was ticked ──
hook("ev",(ev,d)=>{const id=roCur();if(!id||RS.day===dayKey())return;const s=RO[id].st[RS.done[id]||0];if(!s||s.ev!==ev||s.test&&!s.test(d))return;
  const p=RS.prog[id]||0;if(p>=s.n)return;RS.prog[id]=p+1;save();
  if(p+1>=s.n){setTimeout(()=>{toast(`🔨 ${RO[id].n}: этап готов — загляни`);chime([784,1046]);},900);tabDots();hubDot();}});
hook("gate",id=>{if(!roLocked(id))return;audioInit();roPanel(id);return true;});
hook("tabLock",id=>roLocked(id)?"закрыто":"");
hook("tabDot",r=>!!RS.fresh[r]||r===roCur()&&roReady(r)&&RS.day!==dayKey());
hook("hubDot",()=>{const c=roCur();return c&&roReady(c)&&RS.day!==dayKey()||Object.keys(RS.fresh).some(r=>ROOMX[r]);});
hook("room",id=>{if(RS.fresh[id]){delete RS.fresh[id];save();tabDots();}});
hook("sec",()=>{if(!RS.open.kura&&!scene.on&&roKey())roSync(false);});
hook("boot",()=>{const ids=RO_ORDER.filter(id=>ROOMX[id]),mine=ids.map(id=>ROOMS.find(r=>r.id===id)).filter(Boolean),rest=ROOMS.filter(r=>!ids.includes(r.id));
  ROOMS.length=0;ROOMS.push(...rest,...mine);roSync(true);buildTabs();tabDots();});
hook("hub",()=>{const ids=RO_ORDER.filter(id=>ROOMX[id]);if(!ids.length)return"";const cur=roCur();
  const chips=ids.map(id=>`<span class="ro-chip${roLocked(id)?"":" on"}">${roLocked(id)?"🔒":"✓"} ${RO[id].n}</span>`).join("");let body;
  if(!cur)body=`<p>Все комнаты дома открыты. На чердаке сундук каждый день прячет что-нибудь новое.</p>`;
  else{const k=RS.done[cur]||0,s=RO[cur].st[k],p=Math.min(RS.prog[cur]||0,s.n);
    body=`<p><b>${RO[cur].t}</b> · этап ${k+1} из 3: ${s.a[0].toLowerCase()+s.a.slice(1)}.</p><p>${RS.day===dayKey()?"Сегодня уже потрудились — следующий этап завтра.":roReady(cur)?"Задание выполнено — можно браться за доски!":`<em>${s.t}</em>${s.n>1?` · ${p}/${s.n}`:""}. ${roWhere(s)}.`}</p>`;}
  return`<div class="hubc"><h4>🏚 Закрытые комнаты <i>開かずの間</i></h4><div class="ro-chips">${chips}</div>${body}${cur?`<div class="row"><button class="btn" data-x="ro:open:${cur}">Заглянуть</button></div>`:""}</div>`;});

// ── what Musya can do in the two rooms (the tray of ROOMX rooms) ──
function roTray(r){const d=RS.act,dk=dayKey(),b=(k,i,n,x)=>`<button class="item wide" data-x="ro:${k}"><span class="ico">${i}</span><span class="nm">${n}${x?" · ✓":""}</span></button>`;
  return r==="attic"?b("chest","🧰","Порыться в сундуке",d.chest===dk)+b("window",dayTint()[1]?"🌕":"🌤","Смотреть в окошко")+b("dust","💨","Сдуть пыль")
    :b("miso","🛢","Открыть бочку мисо",d.miso===dk)+b("rice","🌾","Пересчитать мешки риса")+b("mice","🐭","Послушать мышей");}
const RO_PANTRY=["v_shiitake","v_kabocha","v_imo","v_daikon","v_shiitake","v_imo"];
function roChest(){const finds=RO_IT.filter(i=>i.src&&!S.owned.has(i.id));RS.digs=(RS.digs||0)+1;
  if(finds.length&&(RS.digs===2||(RS.dry||0)>=3||Math.random()<.2)){const i=pick(finds);S.owned.add(i.id);disc("find",i.id);RS.dry=0;save();ui();
    toast(`✨ В сундуке: ${i.n}!`);chime([1046,1318,1568]);react("😻",2);return;}
  RS.dry=(RS.dry||0)+1;
  if(Math.random()<.62){const id=Math.random()<.08?"v_obaketake":pick(RO_PANTRY);give(id);save();toast(`🧺 В сундуке: ${FOOD[id].n} → в кладовую`);sfx("coin");react("😸",1.6);}
  else{S.needs.joy=clamp(S.needs.joy+10,0,100);save();toast("🧶 В сундуке — старый клубок");start("yarn");}}
function roAct(a){if(petAway()){toast("Муси нет дома");return;}if(scene.on)return;const d=RS.act,dk=dayKey(),at=(ix,iy)=>imgToStage(ix,iy,.4);
  if(a==="chest"){if(d.chest===dk){toast("Сундук уже перерыт — завтра ещё");react("😼",1.4);return;}d.chest=dk;save();ui();walkTo({x:470},"box","🧐");setTimeout(roChest,2600);return;}
  if(a==="window"){walkTo({x:1150},"peek",dayTint()[1]?"🌕":"☁️");const [x,y]=at(1190,560);setTimeout(()=>{for(let i=0;i<4;i++)floatFx.push({g:"✨",x:x+rand(-30,30),y:y+rand(-30,30),t:now()+i*.2});chime([1318,1568]);},1800);S.needs.joy=clamp(S.needs.joy+4,0,100);return;}
  if(a==="dust"){const t=now();for(let i=0;i<6;i++)floatFx.push({g:"💨",x:pet.x+rand(-60,60)*view.s,y:view.floor-rand(40,140)*view.s,t:t+i*.08});react("🤧",1.8);setTimeout(()=>{tone(700,.06,"square",.03);tone(420,.12,"triangle",.04);},500);S.needs.clean=clamp(S.needs.clean-2,0,100);return;}
  if(a==="miso"){if(d.miso===dk){toast("Бочку уже открывали — завтра ещё");react("😝",1.4);return;}d.miso=dk;give("ds_miso");save();ui();pet.food="🥣";walkTo({x:1150},"treat","😋");setTimeout(()=>toast("🥣 Из мисо сварили суп — он в кладовой"),1500);return;}
  if(a==="rice"){walkTo({x:656},"hide","🙈");const [x,y]=at(656,1000);["1","2","3","4","5","6"].forEach((g,i)=>setTimeout(()=>{floatFx.push({g,x:x+rand(-40,40),y:y-rand(0,60),t:now()});tone(520+i*60,.08,"triangle",.03);},1600+i*450));S.needs.joy=clamp(S.needs.joy+5,0,100);return;}
  if(a==="mice"){start("gift");[.3,.5,1.4].forEach(s=>setTimeout(()=>tone(3200+rand(-300,300),.04,"sine",.02),s*1000));react("👂",1.4);S.needs.joy=clamp(S.needs.joy+4,0,100);}}
hook("click",key=>{if(!key.startsWith("ro:"))return;const [,a,id]=key.split(":");
  if(a==="open"&&RO[id]){roPanel(id);return true;}if(a==="tick"){roTick(id);return true;}roAct(a);return true;});
hook("panelClose",id=>{if(id==="ro")roPv=null;});
// reactions for the attic and kura things — needs one core line in itemTap (see the report); harmless without it
hook("itemTap",(it,I,t)=>{const id=it.id;if(!/^(at|kr)_/.test(id))return;
  if(/tokei/.test(id)){[0,.5,1,1.5].forEach((s,i)=>setTimeout(()=>tone(i%2?1100:1400,.05,"square",.02),s*1000));react("😼",1.4);return true;}
  if(/hina_doll|f_neko|kagami/.test(id)){scareSound();react("🙀",1.6);fxAt(it,["👁"],1);return true;}
  if(/nezumitori|komebukuro|nekoe/.test(id)){[0,.15].forEach(s=>setTimeout(()=>tone(3000,.05,"sine",.02),s*1000));walkTo(it,"poke","😼");return true;}
  if(/nagamochi|tsuzura|kiribako|chest|senryobako|tebako|yoroibitsu/.test(id)){tone(140,.35,"sawtooth",.02);fxAt(it,["✨"],2);react("😺",1.2);return true;}
  if(/kumo/.test(id)){react("🤧",1.4);return true;}
  if(/kago|futon|tawara/.test(id)){walkTo(it,/futon/.test(id)?"sleep":"knead","😽");return true;}
  if(/mokuba|buriki|ohajiki|nawa|zaru/.test(id)){walkTo(it,"poke","😸");return true;}
  if(/f_letter|f_photo/.test(id)){chime([659,784]);toast(id==="at_f_letter"?"Письмо без адреса. Почерк — детский":"На фото — этот дом и кошка на крыльце");return true;}
  if(/hoshigaki|herbs|daikon|mino|chochin|hakari|daifukucho|tako/.test(id)){tone(700,.2,"sine",.02);return true;}});

document.head.insertAdjacentHTML("beforeend",`<style>.ro-prev{width:100%;height:auto;aspect-ratio:720/440;display:block;border-radius:12px;margin:4px 0 14px;background:#0a0806;box-shadow:0 0 0 1px var(--line)}
.ro-st{margin-bottom:14px}.ro-st li small{display:block;font-size:12px;color:var(--muted);margin-top:2px}.ro-st li.ro-dim{opacity:.45}.ro-st li.ro-go{color:var(--sakura)}
.ro-chips{display:flex;flex-wrap:wrap;gap:6px;margin:2px 0 6px}.ro-chip{font-size:12px;padding:3px 9px;border-radius:999px;border:1px solid var(--line);color:var(--muted)}.ro-chip.on{color:var(--paper);border-color:rgba(238,163,187,.45)}</style>`);
X.ro={RS,cur:roCur,panel:roPanel,tick:roTick,locked:roLocked,ready:roReady,act:roAct,newDay(){RS.day="";delete RS.act.chest;delete RS.act.miso;}};
}
