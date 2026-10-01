{
// ───────────────────────── «Слово дня»: one kanji a day, traced with a brush on washi; the notebook «Тетрадь» ─────────────────────────
// S.ext.kanji = {d:{"猫":[bestStars,firstDayKey]}, last: dayKey of the last day whose word was traced, streak, best (longest streak),
//   sc:{k,st,im} the best trace as a small png (written on the «scroll» thing)}
// word: [kanji, kana, reading (Polivanov), meaning, strokes, example, example reading, translation]
const KJ_W=[
 ["猫","ねこ","нэко","кошка",11,"猫が寝ている。","нэко га нэтэ иру","Кошка спит."],
 ["家","いえ","иэ","дом",10,"家に帰る。","иэ ни каэру","Вернуться домой."],
 ["月","つき","цуки","луна",4,"月が出た。","цуки га дэта","Взошла луна."],
 ["桜","さくら","сакура","сакура",10,"桜が咲いた。","сакура га сайта","Сакура зацвела."],
 ["雨","あめ","амэ","дождь",8,"雨が降っている。","амэ га футтэ иру","Идёт дождь."],
 ["雪","ゆき","юки","снег",11,"雪が降る。","юки га фуру","Падает снег."],
 ["火","ひ","хи","огонь",4,"火が燃える。","хи га моэру","Горит огонь."],
 ["水","みず","мидзу","вода",4,"猫が水を飲む。","нэко га мидзу о ному","Кошка пьёт воду."],
 ["山","やま","яма","гора",3,"山の上の月。","яма но уэ но цуки","Луна над горой."],
 ["川","かわ","кава","река",3,"川で魚を釣る。","кава дэ сакана о цуру","Ловить рыбу в реке."],
 ["花","はな","хана","цветок",7,"花が咲いている。","хана га сайтэ иру","Цветут цветы."],
 ["鬼","おに","они","о́ни, демон",10,"鬼は外、福は内！","они ва сото, фуку ва ути","О́ни — прочь, счастье — в дом!"],
 ["狐","きつね","кицунэ","лиса",9,"狐の嫁入り。","кицунэ но ёмэири","Лисья свадьба — дождь при солнце."],
 ["夢","ゆめ","юмэ","сон, мечта",13,"猫が夢を見る。","нэко га юмэ о миру","Кошке снится сон."],
 ["星","ほし","хоси","звезда",9,"星を数える。","хоси о кадзоэру","Считать звёзды."],
 ["鈴","すず","судзу","колокольчик",13,"鈴が鳴る。","судзу га нару","Звенит колокольчик."],
 ["茶","ちゃ","тя","чай",9,"お茶を飲む。","о-тя о ному","Пить чай."],
 ["魚","さかな","сакана","рыба",11,"猫は魚が好き。","нэко ва сакана га суки","Кошка любит рыбу."],
 ["鳥","とり","тори","птица",11,"鳥が飛ぶ。","тори га тобу","Летит птица."],
 ["春","はる","хару","весна",9,"春が来た。","хару га кита","Пришла весна."],
 ["夏","なつ","нацу","лето",10,"夏の夜。","нацу но ёру","Летняя ночь."],
 ["秋","あき","аки","осень",9,"秋の月。","аки но цуки","Осенняя луна."],
 ["冬","ふゆ","фую","зима",5,"冬は寒い。","фую ва самуи","Зимой холодно."],
 ["友","とも","томо","друг",4,"友と遊ぶ。","томо то асобу","Играть с другом."],
 ["愛","あい","ай","любовь",13,"愛をこめて。","ай о комэтэ","С любовью."],
 ["光","ひかり","хикари","свет",6,"月の光。","цуки но хикари","Лунный свет."],
 ["影","かげ","кагэ","тень",15,"猫の影。","нэко но кагэ","Кошачья тень."],
 ["風","かぜ","кадзэ","ветер",9,"風が吹く。","кадзэ га фуку","Дует ветер."],
 ["空","そら","сора","небо",8,"空を見る。","сора о миру","Смотреть в небо."],
 ["雲","くも","кумо","облако",12,"月が雲に隠れる。","цуки га кумо ни какурэру","Луна прячется за облако."],
 ["森","もり","мори","лес",12,"森の奥。","мори но оку","В глубине леса."],
 ["木","き","ки","дерево",4,"木の下で眠る。","ки но сита дэ нэмуру","Спать под деревом."],
 ["竹","たけ","такэ","бамбук",6,"竹の林。","такэ но хаяси","Бамбуковая роща."],
 ["石","いし","иси","камень",5,"庭の石。","нива но иси","Камни в саду."],
 ["庭","にわ","нива","сад, двор",10,"庭で遊ぶ。","нива дэ асобу","Играть во дворе."],
 ["道","みち","мити","дорога",12,"森の道。","мори но мити","Лесная тропа."],
 ["門","もん","мон","ворота",8,"門を開ける。","мон о акэру","Открыть ворота."],
 ["窓","まど","мадо","окно",11,"窓から月が見える。","мадо кара цуки га миэру","Из окна видна луна."],
 ["本","ほん","хон","книга",5,"本を読む。","хон о ёму","Читать книгу."],
 ["紙","かみ","ками","бумага",10,"紙に字を書く。","ками ни дзи о каку","Писать иероглиф на бумаге."],
 ["筆","ふで","фудэ","кисть",12,"筆で書く。","фудэ дэ каку","Писать кистью."],
 ["字","じ","дзи","иероглиф, буква",6,"字を習う。","дзи о нарау","Учить иероглифы."],
 ["心","こころ","кокоро","сердце, душа",4,"心が温かい。","кокоро га ататакаи","Тёплое сердце."],
 ["夜","よる","ёру","ночь",8,"夜は静か。","ёру ва сидзука","Ночью тихо."],
 ["朝","あさ","аса","утро",12,"朝ご飯を食べる。","асагохан о табэру","Завтракать."],
 ["日","ひ","хи","солнце, день",4,"日が昇る。","хи га нобору","Восходит солнце."],
 ["雷","かみなり","каминари","гром",13,"雷が鳴る。","каминари га нару","Гремит гром."],
 ["虹","にじ","нидзи","радуга",9,"空に虹が出た。","сора ни нидзи га дэта","В небе радуга."],
 ["海","うみ","уми","море",9,"海で泳ぐ。","уми дэ оёгу","Плавать в море."],
 ["犬","いぬ","ину","собака",4,"犬と猫。","ину то нэко","Собака и кошка."],
 ["狸","たぬき","тануки","тануки",10,"狸が化ける。","тануки га бакэру","Тануки превращается."],
 ["蛍","ほたる","хотару","светлячок",11,"蛍が光る。","хотару га хикару","Светятся светлячки."],
 ["蛙","かえる","каэру","лягушка",12,"蛙が鳴く。","каэру га наку","Квакают лягушки."],
 ["亀","かめ","камэ","черепаха",11,"亀は万年。","камэ ва маннэн","Черепаха живёт десять тысяч лет."],
 ["鶴","つる","цуру","журавль",21,"鶴は千年。","цуру ва сэннэн","Журавль живёт тысячу лет."],
 ["松","まつ","мацу","сосна",8,"松に鶴。","мацу ни цуру","Сосна и журавль — карта ханафуда."],
 ["梅","うめ","умэ","слива умэ",10,"梅の花。","умэ но хана","Цветы сливы."],
 ["菊","きく","кику","хризантема",11,"菊の香り。","кику но каори","Аромат хризантем."],
 ["葉","は","ха","лист",12,"葉が落ちる。","ха га отиру","Падают листья."],
 ["草","くさ","куса","трава",9,"草の上で眠る。","куса но уэ дэ нэмуру","Спать на траве."],
 ["米","こめ","комэ","рис",6,"米を炊く。","комэ о таку","Варить рис."],
 ["酒","さけ","сакэ","сакэ",10,"お酒を一杯。","о-сакэ о иппай","Чашечку сакэ."],
 ["湯","ゆ","ю","горячая вода",12,"お湯に入る。","о-ю ни хаиру","Забраться в горячую воду."],
 ["傘","かさ","каса","зонтик",12,"傘をさす。","каса о сасу","Раскрыть зонтик."],
 ["祭","まつり","мацури","праздник",11,"夏祭りに行く。","нацумацури ни ику","Пойти на летний праздник."],
 ["神","かみ","ками","бог, дух",9,"山の神。","яма но ками","Дух горы."],
 ["寺","てら","тэра","буддийский храм",6,"山の寺。","яма но тэра","Храм в горах."],
 ["面","めん","мэн","маска",9,"狐の面。","кицунэ но мэн","Лисья маска."],
 ["玉","たま","тама","шарик",5,"猫が玉で遊ぶ。","нэко га тама дэ асобу","Кошка играет с мячиком."],
 ["糸","いと","ито","нить",6,"赤い糸。","акаи ито","Красная нить судьбы."],
 ["箱","はこ","хако","коробка",15,"猫は箱が好き。","нэко ва хако га суки","Кошки любят коробки."],
 ["手","て","тэ","рука, лапа",4,"猫の手も借りたい。","нэко но тэ мо каритаи","Дел столько, что рад и кошачьей лапке."],
 ["目","め","мэ","глаз",5,"猫の目が光る。","нэко но мэ га хикару","Светятся кошачьи глаза."],
 ["耳","みみ","мими","ухо",6,"壁に耳あり。","кабэ ни мими ари","И у стен есть уши."],
 ["声","こえ","коэ","голос",7,"鳥の声。","тори но коэ","Пение птиц."],
 ["音","おと","ото","звук",9,"雨の音。","амэ но ото","Шум дождя."],
 ["色","いろ","иро","цвет",6,"秋の色。","аки но иро","Краски осени."],
 ["赤","あか","ака","красный",7,"赤い鳥居。","акаи тории","Красные тории."],
 ["白","しろ","сиро","белый",5,"白い雪。","сирои юки","Белый снег."],
 ["黒","くろ","куро","чёрный",11,"黒猫。","куронэко","Чёрная кошка."],
 ["金","きん","кин","золото",8,"金の鈴。","кин но судзу","Золотой колокольчик."],
 ["鏡","かがみ","кагами","зеркало",19,"鏡を見る。","кагами о миру","Смотреться в зеркало."],
 ["兎","うさぎ","усаги","заяц",7,"月の兎。","цуки но усаги","Лунный заяц."],
 ["栗","くり","кури","каштан",10,"栗を焼く。","кури о яку","Жарить каштаны."],
 ["柿","かき","каки","хурма",9,"柿が赤くなった。","каки га акаку натта","Хурма покраснела."],
 ["舟","ふね","фунэ","лодка",6,"舟に乗る。","фунэ ни нору","Сесть в лодку."],
 ["橋","はし","хаси","мост",16,"赤い橋。","акаи хаси","Красный мостик."],
 ["宿","やど","ядо","гостиница",11,"山の宿。","яма но ядо","Гостиница в горах."],
 ["旅","たび","таби","путешествие",10,"旅に出る。","таби ни дэру","Отправиться в путь."],
 ["歌","うた","ута","песня",14,"歌を歌う。","ута о утау","Петь песню."],
 ["絵","え","э","картина",12,"絵を描く。","э о каку","Рисовать картину."],
 ["福","ふく","фуку","счастье",13,"福が来る。","фуку га куру","Приходит счастье."],
 ["墨","すみ","суми","тушь",14,"墨をする。","суми о суру","Растирать тушь."],
 ["硯","すずり","судзури","тушечница",12,"硯と筆。","судзури то фудэ","Тушечница и кисть."],
 ["霧","きり","кири","туман",19,"霧の森。","кири но мори","Лес в тумане."],
 ["波","なみ","нами","волна",8,"波の音。","нами но ото","Шум волн."],
 ["池","いけ","икэ","пруд",6,"池に月が映る。","икэ ни цуки га уцуру","В пруду отражается луна."],
 ["鼠","ねずみ","нэдзуми","мышь",13,"猫と鼠。","нэко то нэдзуми","Кошка и мышь."],
 ["子","こ","ко","ребёнок, детёныш",3,"子猫が遊ぶ。","конэко га асобу","Котёнок играет."],
 ["豆","まめ","мамэ","боб",7,"豆をまく。","мамэ о маку","Разбрасывать бобы на Сэцубун."],
 ["枕","まくら","макура","подушка",8,"猫は枕で寝る。","нэко ва макура дэ нэру","Кошка спит на подушке."],
 ["笛","ふえ","фуэ","флейта",11,"笛を吹く。","фуэ о фуку","Играть на флейте."],
 ["凧","たこ","тако","воздушный змей",5,"凧をあげる。","тако о агэру","Запускать воздушного змея."],
 ["虫","むし","муси","насекомое",6,"秋の虫。","аки но муси","Осенние сверчки."],
 ["鍋","なべ","набэ","котелок",17,"鍋で煮る。","набэ дэ ниру","Варить в котелке."],
 ["箸","はし","хаси","палочки для еды",15,"箸で食べる。","хаси дэ табэру","Есть палочками."],
 ["灯","ひ","хи","огонёк",6,"灯がともる。","хи га томору","Зажёгся огонёк."]];
const KJ_CH=KJ_W.map(w=>w[0]).join("")+"済今日字";
const KJ_ORD=(()=>{const r=rng(5021),a=KJ_W.map((w,i)=>i);for(let i=a.length-1;i>0;i--){const j=Math.floor(r()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;})();
const KJ_FONT='"Yuji Syuku","Noto Serif JP","Hiragino Mincho ProN","Yu Mincho",serif';
const KJ_INK="#1b1512",KJ_RED="#a8382a",TAU=Math.PI*2;
// the four calligraphy things (one atlas, art/kanji_art.py); the scroll's paper is blank: the game writes the best kanji on it
const KJ_R={kj_scroll:[0,0,120,330],kj_rack:[122,0,170,210],kj_box:[294,0,220,140],kj_desk:[516,0,260,160]};
const KJ_IT=[["kj_scroll","Свиток с твоим иероглифом","t",10],["kj_rack","Подставка с кистями","b",20],["kj_box","Шкатулка для туши","b",30],["kj_desk","Столик для каллиграфии","b",40]];
addItems(KJ_IT.map(([id,n,a,th])=>{const r=KJ_R[id];return{id,n,c:"Каллиграфия",w:r[2],h:r[3],a,p:0,at:["kj",r[0],r[1]],src:"✍️ слово дня",hint:`✍️ Выучи ${th} слов в «Слове дня»`};}),{kj:[778,330]});
STAMPS.push(["kj_first","字","Первый иероглиф","Обведи кистью слово дня"],["kj_s3","筆","Три дня с кистью","Обводи слово дня три дня подряд"],
  ["kj_s7","墨","Неделя каллиграфии","Обводи слово дня семь дней подряд"],["kj_s30","書","Месяц каллиграфии","Обводи слово дня тридцать дней подряд"]);
document.head.insertAdjacentHTML("beforeend",`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Yuji+Syuku&display=swap&text=${encodeURIComponent(KJ_CH)}"><style>
.kj-day,.kj-res{display:flex;gap:14px;align-items:center;margin:4px 0 8px;text-align:left}
.kj-big{flex:none;font-family:"Yuji Syuku",var(--jp);font-weight:400;font-style:normal;font-size:60px;line-height:1;color:#241a14;background:#e4d9c0;border-radius:10px;padding:10px 12px;box-shadow:inset 0 0 0 2px rgba(168,56,42,.4)}
:is(.story-body .kj-day,.kj-res,.card) p.kj-m{font-size:20px;font-weight:600;margin:0;line-height:1.25;color:var(--paper)}:is(.story-body .kj-day,.kj-res,.card) p.kj-r{margin:3px 0 0;line-height:1.35;color:var(--muted);font-size:14px}:is(.story-body .kj-day,.kj-res) p.kj-st{color:#d8a24a;font-size:18px;line-height:1.2;letter-spacing:2px;margin:0 0 2px}
.kj-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(72px,1fr));gap:6px;margin:8px 0 14px}
.kj-t{display:flex;flex-direction:column;align-items:center;gap:1px;padding:6px 2px 5px;border-radius:10px;background:#e4d9c0;color:#241a14;border:0;font:inherit;cursor:pointer}
.kj-t b{font-family:"Yuji Syuku",var(--jp);font-weight:400;font-size:32px;line-height:1.15}.kj-t small{font-size:10.5px;line-height:1.15;color:#4e3c2e;max-width:100%;overflow-wrap:anywhere}.kj-t i{font-style:normal;font-size:10px;color:#a8382a;letter-spacing:1px}
.kj-t.q{background:#0a0d0c;color:var(--muted);box-shadow:inset 0 0 0 1px var(--line)}.kj-t.q small{color:var(--muted)}
.kj-ex{background:#0a0d0c;border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:10px 0}#xpBody .kj-ex p{margin:2px 0;font-size:15px;line-height:1.45}#xpBody .kj-ex p.jp{font-family:var(--jp);font-size:20px}.kj-ex i{color:var(--muted)}
.card p.kj-gift{color:var(--sakura)}</style>`);

let kjCur=null,kjForce=null,kjB=0,kjScV=1,kjScD=0;
function kjS(){return S.ext.kanji||(S.ext.kanji={d:{},last:null,streak:0,best:0,sc:null});}
const kjDay=dk=>Math.round(Date.parse(dk+"T12:00:00Z")/864e5);
function kjToday(){return kjForce&&KJ_W.find(w=>w[0]===kjForce)||KJ_W[KJ_ORD[((kjDay(dayKey())%KJ_W.length)+KJ_W.length)%KJ_W.length]];}
function kjYest(){return new Date(Date.parse(dayKey()+"T12:00:00Z")-864e5).toISOString().slice(0,10);}
const kjDone=()=>kjS().last===dayKey();
const kjStreak=()=>{const z=kjS();return z.last===dayKey()||z.last===kjYest()?z.streak||0:0;};
const kjN=()=>Object.keys(kjS().d).length;
function kjPl(n,f){const a=n%10,b=n%100;return n+" "+(a===1&&b!==11?f[0]:a>=2&&a<=4&&(b<12||b>14)?f[1]:f[2]);}
const kjStars=n=>"★".repeat(n)+"☆".repeat(3-n);
const kjDate=dk=>new Date(Date.parse(dk+"T12:00:00Z")).toLocaleDateString("ru-RU",{day:"numeric",month:"long"});
function kjFont(){try{document.fonts&&document.fonts.load('80px "Yuji Syuku"',KJ_CH).catch(()=>{});}catch(e){}}

// ── the sheet: washi (fibres, mottling, lantern light), the red practice grid; the layout for a phone (column) or a wide screen (side)
function kjLay(G){const s=G.s,W=G.W,H=G.H,side=W>H*1.05,bh=44*s;let L;
  if(!side){const y=100*s,sq=Math.min(W-28*s,H-y-232*s),by=H-bh-12*s,bw=Math.min(128*s,(W-40*s)/3);
    L={sq,x:(W-sq)/2,y,cx:W/2,ty:14*s,ey:y+sq+30*s,by,bx:14*s,mx:W-66*s,mf:H-14*s,ms:.5*s,ix:14*s,iy:by-16*s,ia:"left",
      btns:[{id:"clear",n:"Стереть",x:14*s,y:by,w:bw,h:bh},{id:"done",n:"Готово",x:24*s+bw,y:by,w:bw,h:bh}]};}
  else{const sq=Math.min(H-40*s,W*.52),x=Math.max(20*s,W*.55/2-sq/2),y=(H-sq)/2,px=x+sq+28*s,cx=(px+W)/2,bw=Math.min(140*s,(W-px-30*s)/2),by=H-bh-18*s;
    L={sq,x,y,cx,ty:y,ey:y+sq*.36,by,mx:W-70*s,mf:by-10*s,ms:.52*s,ix:cx,iy:y+sq*.62,ia:"center",
      btns:[{id:"clear",n:"Стереть",x:cx-bw-5*s,y:by,w:bw,h:bh},{id:"done",n:"Готово",x:cx+5*s,y:by,w:bw,h:bh}]};
    if(L.mx-60*s<cx+bw)L.mf=by-14*s;}
  L.s=s;L.side=side;L.fs=L.sq*.8;L.fo=L.sq*.02;return L;}
function kjBuild(G){const q=G.st,L=kjLay(G),d=Math.min(2,devicePixelRatio||1),W=G.W,H=G.H,s=L.s;q.L=L;q.lw=W;q.lh=H;
  const c=document.createElement("canvas");c.width=Math.round(W*d);c.height=Math.round(H*d);const g=c.getContext("2d"),cw=c.width,ch=c.height,r=rng(17);
  // paper tone: soft cloudy mottling (bilinear value noise) + fine tooth
  const gs=24,gx=Math.ceil(cw/gs)+2,gy=Math.ceil(ch/gs)+2,N=new Float32Array(gx*gy);for(let i=0;i<N.length;i++)N[i]=r()-.5;
  const im=g.createImageData(cw,ch),D=im.data;
  for(let y=0;y<ch;y++){const fy=y/gs,iy=fy|0,ty=fy-iy;for(let x=0;x<cw;x++){const fx=x/gs,ix=fx|0,tx=fx-ix,o=iy*gx+ix,
      n=(N[o]*(1-tx)+N[o+1]*tx)*(1-ty)+(N[o+gx]*(1-tx)+N[o+gx+1]*tx)*ty,l=226+n*16+(r()-.5)*9,i=(y*cw+x)*4;
      D[i]=l;D[i+1]=l*.955;D[i+2]=l*.86;D[i+3]=255;}}
  g.putImageData(im,0,0);g.setTransform(d,0,0,d,0,0);
  // kozo fibres: short curly light/dark threads and a few long ones
  for(let i=0;i<(W*H)/260;i++){const x=r()*W,y=r()*H,a=r()*TAU,L0=4+r()*16*(r()<.1?4:1),k=(r()-.5)*.6;
    g.strokeStyle=r()<.6?`rgba(255,250,236,${.25+r()*.3})`:`rgba(120,96,64,${.08+r()*.12})`;g.lineWidth=.4+r()*.7;
    g.beginPath();g.moveTo(x,y);g.quadraticCurveTo(x+Math.cos(a+k)*L0*.6,y+Math.sin(a+k)*L0*.6,x+Math.cos(a)*L0,y+Math.sin(a)*L0);g.stroke();}
  for(let i=0;i<14;i++){g.fillStyle=`rgba(140,110,70,${.03+r()*.04})`;g.beginPath();g.ellipse(r()*W,r()*H,10+r()*40,6+r()*26,r()*3,0,TAU);g.fill();}   // faint stains
  // light: a warm lantern from the top left at night, soft daylight otherwise; darker deckled edges
  const night=dayTint()[1],gr=g.createRadialGradient(W*.28,H*.12,0,W*.4,H*.35,Math.max(W,H)*.95);
  gr.addColorStop(0,night?"#fff0d6":"#fffaf0");gr.addColorStop(.55,night?"#d6c2a0":"#efe6d6");gr.addColorStop(1,night?"#6e5a44":"#b9ab92");
  g.save();g.globalCompositeOperation="multiply";g.fillStyle=gr;g.fillRect(0,0,W,H);g.restore();
  const e=14*s;for(const [x0,y0,x1,y1,w,h] of [[0,0,0,e,W,e],[0,H,0,H-e,W,-e],[0,0,e,0,e,H],[W,0,W-e,0,-e,H]]){const lg=g.createLinearGradient(x0,y0,x1,y1);lg.addColorStop(0,"rgba(60,40,24,.35)");lg.addColorStop(1,"rgba(60,40,24,0)");g.fillStyle=lg;g.fillRect(x0,y0,w,h);}
  // the practice square: a red frame and a dashed cross (like school paper)
  g.strokeStyle="rgba(168,56,42,.6)";g.lineWidth=1.8;g.strokeRect(L.x,L.y,L.sq,L.sq);g.strokeStyle="rgba(168,56,42,.25)";g.lineWidth=.9;g.strokeRect(L.x+4*s,L.y+4*s,L.sq-8*s,L.sq-8*s);
  g.setLineDash([7*s,6*s]);g.strokeStyle="rgba(168,56,42,.3)";g.lineWidth=1;g.beginPath();g.moveTo(L.x+L.sq/2,L.y+4*s);g.lineTo(L.x+L.sq/2,L.y+L.sq-4*s);g.moveTo(L.x+4*s,L.y+L.sq/2);g.lineTo(L.x+L.sq-4*s,L.y+L.sq/2);g.stroke();g.setLineDash([]);
  q.bg=c;
  // the ink layer (kept on resize)
  const ik=document.createElement("canvas");ik.width=ik.height=Math.round(L.sq*d);const ig=ik.getContext("2d");if(q.ink)ig.drawImage(q.ink,0,0,ik.width,ik.height);
  ig.setTransform(d,0,0,d,0,0);ig.fillStyle=KJ_INK;q.ink=ik;q.ig=ig;q.d=d;
  // the hanko 済: vermilion seal, the character cut out, worn speckles
  const hs=Math.round(60*s*d),hk=document.createElement("canvas");hk.width=hk.height=hs;const hg=hk.getContext("2d");hg.fillStyle="#b3301f";hg.beginPath();hg.roundRect(hs*.04,hs*.04,hs*.92,hs*.92,hs*.12);hg.fill();
  hg.globalCompositeOperation="destination-out";hg.lineWidth=hs*.035;hg.strokeRect(hs*.13,hs*.13,hs*.74,hs*.74);hg.font=`${hs*.62}px ${KJ_FONT}`;hg.textAlign="center";hg.textBaseline="middle";hg.fillText("済",hs/2,hs*.52);
  for(let i=0;i<70;i++){hg.globalAlpha=.3+r()*.7;hg.beginPath();hg.arc(r()*hs,r()*hs,r()*hs*.018+.5,0,TAU);hg.fill();}q.hk=hk;}

// ── the brush: dabs along the path; width follows speed (slow = pressed), a held brush spreads a blot, the ink runs dry into kasure streaks
function kjDab(q,x,y,w,a){const g=q.ig,l=q.live,r=w/2,wet=l?l.ink:1,ba=a*clamp((wet-.15)/.55,0,1);
  if(ba>0){g.globalAlpha=ba;g.beginPath();g.arc(x,y,r*(.88+Math.random()*.09),0,TAU);g.fill();}   // the wet body of the stroke
  if(l){g.globalAlpha=a*.9;for(const b of l.br){if(b.dry>wet*1.4+.15)continue;g.beginPath();g.arc(x+l.nx*b.o*r,y+l.ny*b.o*r,r*.15,0,TAU);g.fill();}   // bristle tracks: streaks, dry-brush gaps
    if(wet>.5&&Math.random()<.2){g.globalAlpha=.03;g.beginPath();g.arc(x+(Math.random()-.5)*2,y+(Math.random()-.5)*2,r*1.3,0,TAU);g.fill();}}   // a little bleed into the paper
  else{g.globalAlpha=a*2;g.beginPath();g.arc(x,y,r,0,TAU);g.fill();}
  g.globalAlpha=1;}
function kjSeg(q,x0,y0,w0,x1,y1,w1){const L=Math.hypot(x1-x0,y1-y0),n=Math.max(1,Math.ceil(L/Math.max(.9,Math.min(w0,w1)*.13)));
  for(let i=1;i<=n;i++){const u=i/n;kjDab(q,x0+(x1-x0)*u,y0+(y1-y0)*u,w0+(w1-w0)*u,.3);}}
function kjDown(q,u,v,t){const bw=q.L.sq*.064;q.live={x:u,y:v,su:u,sv:v,w:bw*.62,bw,ink:1,mt:t,sp:0,nx:0,ny:1,len:0,
    br:Array.from({length:12},(_,i)=>({o:-.92+i*1.84/11+(Math.random()-.5)*.08,dry:Math.random()}))};kjDab(q,u,v,bw*.62,.3);kjDab(q,u+bw*.06,v+bw*.06,bw*.7,.3);
  q.miss=null;q.msg=null;tone(150+Math.random()*30,.06,"sine",.025);}
function kjMove(q,u,v,t){const l=q.live;l.su+=(u-l.su)*.6;l.sv+=(v-l.sv)*.6;const dx=l.su-l.x,dy=l.sv-l.y,dd=Math.hypot(dx,dy);if(dd<1.4)return;
  const sp=dd/Math.max(.008,t-l.mt);l.mt=t;l.sp=l.sp*.55+sp*.45;const w1=l.w+(l.bw*clamp(1.28-l.sp/1500,.42,1.25)-l.w)*.3;
  l.nx=-dy/dd;l.ny=dx/dd;kjSeg(q,l.x,l.y,l.w,l.su,l.sv,w1);l.x=l.su;l.y=l.sv;l.w=w1;l.len+=dd;l.ink=Math.max(0,l.ink-dd*(1+l.sp/900)/(l.bw*48));}
function kjUp(q){const l=q.live;if(!l)return;q.live=null;q.n++;
  if(l.sp>420&&l.len>12){const n=Math.round(clamp(l.sp*.03,8,36)),dx=l.ny,dy=-l.nx;let x=l.x,y=l.y;   // a flick: the brush lifts off in a thin tail (harai)
    for(let i=1;i<=n;i++){const k=1-i/n,w=l.w*(.08+.8*k*k);x+=dx*1.7;y+=dy*1.7;l.ink=Math.max(0,l.ink-.012);kjDab(q,x,y,w,.3);}}}

// ── checking: the glyph rendered to a small mask (core + a tolerance band) against the ink → coverage, spill → 0–3 ★
function kjMask(q){const L=q.L,N=120,k=N/L.sq,c=document.createElement("canvas");c.width=c.height=N;const g=c.getContext("2d");
  g.font=`${L.fs*k}px ${KJ_FONT}`;g.textAlign="center";g.textBaseline="middle";g.fillText(q.w[0],N/2,N/2+L.fo*k);const a=g.getImageData(0,0,N,N).data;
  g.lineWidth=L.sq*.09*k;g.lineJoin="round";g.strokeText(q.w[0],N/2,N/2+L.fo*k);const b=g.getImageData(0,0,N,N).data,core=new Uint8Array(N*N),tol=new Uint8Array(N*N);let nc=0;
  for(let i=0;i<N*N;i++){if(a[i*4+3]>110){core[i]=1;nc++;}if(b[i*4+3]>20)tol[i]=1;}return{N,core,tol,nc};}
function kjScore(q){const m=kjMask(q),N=m.N,c=document.createElement("canvas");c.width=c.height=N;const g=c.getContext("2d");g.drawImage(q.ink,0,0,N,N);const a=g.getImageData(0,0,N,N).data;
  let hit=0,ink=0,out=0;for(let i=0;i<N*N;i++){if(a[i*4+3]>70){ink++;if(m.core[i])hit++;if(!m.tol[i])out++;}}
  const cov=hit/Math.max(1,m.nc),sp=out/Math.max(1,ink),st=cov>=.76&&sp<=.22?3:cov>=.62&&sp<=.32?2:cov>=.48&&sp<=.42?1:0;return{cov,sp,st};}
function kjMiss(q){const L=q.L,c=document.createElement("canvas");c.width=c.height=q.ink.width;const g=c.getContext("2d"),k=c.width/L.sq;
  g.font=`${L.fs*k}px ${KJ_FONT}`;g.textAlign="center";g.textBaseline="middle";g.fillStyle="rgba(200,60,40,.85)";g.fillText(q.w[0],c.width/2,c.width/2+L.fo*k);
  g.globalCompositeOperation="destination-out";g.drawImage(q.ink,0,0);return c;}
function kjPng(q){const c=document.createElement("canvas");c.width=c.height=128;c.getContext("2d").drawImage(q.ink,0,0,128,128);try{return c.toDataURL("image/png");}catch(e){return null;}}

// ── result: the notebook, the streak, stamps, things every 10 words
function kjSave(q){const z=kjS(),w=q.w,ch=w[0],dk=dayKey(),st=q.res.st,prev=z.d[ch],R={st,fresh:!prev,day:false,gift:null};
  if(q.mode==="day"&&z.last!==dk){R.day=true;z.streak=(z.last===kjYest()?z.streak||0:0)+1;z.last=dk;z.best=Math.max(z.best||0,z.streak);}
  if(!prev){z.d[ch]=[st,dk];disc("kanji",ch);}else if(st>prev[0])prev[0]=st;
  if(!z.sc||st>=z.sc.st){const im=kjPng(q);if(im){z.sc={k:ch,st,im};kjScV++;}}
  const n=kjN();for(const [id,,,th] of KJ_IT)if(n>=th&&!S.owned.has(id)){S.owned.add(id);loadItem(id);R.gift=id;}
  award("kj_first");const sk=kjStreak();if(sk>=3)award("kj_s3");if(sk>=7)award("kj_s7");if(sk>=30)award("kj_s30");
  S.needs.joy=clamp(S.needs.joy+(R.day?6:2),0,100);save();q.R=R;}
function kjBtn(G,id,t){const q=G.st;tone(260,.05,"triangle",.05);
  if(id==="clear"){q.ig.save();q.ig.setTransform(1,0,0,1,0,0);q.ig.clearRect(0,0,q.ink.width,q.ink.height);q.ig.restore();q.n=0;q.miss=null;q.msg=null;return;}
  if(id!=="done")return;if(!q.n){q.msg={t,s:"Сначала обведи иероглиф кистью"};return;}
  const res=kjScore(q);q.res=res;
  if(!res.st){q.miss=kjMiss(q);q.missT=t;q.msg={t,s:res.cov<.5?"Дорисуй места, что светятся красным":"Много туши мимо — сотри и попробуй ещё"};tone(330,.18,"sine",.04);setTimeout(()=>tone(262,.25,"sine",.035),160);return;}
  G.score=res.st;q.win=t;q.pat=t+.55;q.fin=t+2.9;kjSave(q);
  setTimeout(()=>{tone(105,.16,"sine",.22);tone(210,.07,"triangle",.07);},140);
  for(let i=0;i<res.st;i++)setTimeout(()=>tone(1046*[1,1.26,1.5][i],.5,"sine",.04),700+i*260);}

// ── drawing helpers
function kjTx(g,txt,x,y,font,col,al="center"){g.font=font;g.textAlign=al;g.textBaseline="middle";g.fillStyle=col;g.fillText(txt,x,y);}
function kjFit(g,txt,font,size,maxW){g.font=font.replace("#",size);const w=g.measureText(txt).width;return w>maxW?size*maxW/w:size;}
function kjPaw(g,x,y,s,a){g.save();g.translate(x,y);g.rotate(-.35);g.globalAlpha=a;g.fillStyle="rgba(27,21,18,.82)";
  g.beginPath();g.ellipse(0,4*s,8.5*s,7*s,0,0,TAU);g.fill();for(const [tx,ty] of [[-9,-6],[-3.3,-11],[3.3,-11],[9,-6]]){g.beginPath();g.ellipse(tx*s,ty*s,3.1*s,3.8*s,0,0,TAU);g.fill();}g.restore();}

const KJG={id:"kj_trace",hidden:true,n:"Слово дня",tag:"筆 · Фудэ",bg:"room",lives:null,time:null,icon:"✍️",lore:"",how:"",
 init(G,t){G.score=0;const c=kjCur||{w:kjToday(),mode:"day"};Object.assign(G.st,{w:c.w,mode:c.mode,live:null,n:0,win:0,fin:0,pat:0,miss:null,missT:-9,msg:null,bub:null,res:null,R:null,ink:null});kjBuild(G);kjFont();},
 step(G,t,dt){const q=G.st;if(q.lw!==G.W||q.lh!==G.H)kjBuild(G);
   const l=q.live;if(l&&G.held&&now()-l.mt>.12&&l.w<l.bw*1.5){l.w=Math.min(l.bw*1.5,l.w+dt*l.bw*1.1);kjDab(q,l.x,l.y,l.w,.15);}   // a held brush spreads
   if(q.fin&&t>q.fin){q.fin=0;gEnd();}},
 draw(G,g,t){const q=G.st,L=q.L;if(!L)return;const s=L.s,w=q.w,UI=getComputedStyle(document.body).fontFamily,DSP='"Cormorant Garamond",Georgia,serif',JP='"Noto Serif JP","Hiragino Mincho ProN","Yu Mincho",serif';
   g.drawImage(q.bg,0,0,G.W,G.H);
   g.save();g.font=`${L.fs}px ${KJ_FONT}`;g.textAlign="center";g.textBaseline="middle";g.fillStyle=q.win?"rgba(70,52,40,.08)":"rgba(70,52,40,.17)";g.fillText(w[0],L.x+L.sq/2,L.y+L.sq/2+L.fo);g.restore();
   if(q.miss){const u=t-q.missT;if(u<3.4){g.globalAlpha=clamp(Math.min(u*4,(3.4-u)*1.4),0,1)*(.6+.3*Math.sin(t*6));g.drawImage(q.miss,L.x,L.y,L.sq,L.sq);g.globalAlpha=1;}else q.miss=null;}
   g.drawImage(q.ink,L.x,L.y,L.sq,L.sq);
   // title: meaning, reading, strokes
   const tw=L.side?G.W-L.x-L.sq-40*s:G.W-28*s,ty=L.side?L.ty+20*s:L.ty;
   const fm=kjFit(g,w[3],`700 #px ${DSP}`,30*s,tw);kjTx(g,w[3],L.cx,ty+20*s,`700 ${fm}px ${DSP}`,"#2a1d15");
   kjTx(g,`${w[1]} · ${w[2]}`,L.cx,ty+52*s,`500 ${16*s}px ${UI}`,"#6a4c38");
   kjTx(g,`черт: ${w[4]}`,L.x+L.sq-2*s,L.y-11*s,`600 ${12*s}px ${UI}`,KJ_RED,"right");
   kjTx(g,q.mode==="day"?"слово дня":"повторение",L.x+2*s,L.y-11*s,`600 ${12*s}px ${UI}`,"rgba(90,64,48,.8)","left");
   // the example
   const ew=L.side?tw:G.W-28*s,ex=L.side?L.cx:G.W/2;
   kjTx(g,w[5],ex,L.ey,`500 ${kjFit(g,w[5],`500 #px ${JP}`,19*s,ew)}px ${JP}`,"#241a14");
   kjTx(g,w[6],ex,L.ey+26*s,`italic 500 ${kjFit(g,w[6],`italic 500 #px ${UI}`,14.5*s,ew)}px ${UI}`,"#6a4c38");
   kjTx(g,w[7],ex,L.ey+48*s,`500 ${kjFit(g,w[7],`500 #px ${UI}`,14.5*s,ew)}px ${UI}`,"#3a2a1e");
   const sk=kjStreak();kjTx(g,`В тетради: ${kjN()}`+(sk?` · серия: ${kjPl(sk,["день","дня","дней"])}`:""),L.ix,L.iy,`500 ${12.5*s}px ${UI}`,"rgba(80,58,42,.85)",L.ia);
   // win: the seal thumps down, stars, Musya pats the paper and leaves a paw print
   if(q.win){const u=(t-q.win)/.24,k=u<1?1.8-.8*smooth(u):1,hs=60*s*k,hx=L.x+L.sq-42*s,hy=L.y+L.sq-42*s;
     g.save();g.globalAlpha=clamp(u*1.5,0,1)*.92;g.translate(hx,hy);g.rotate(-.12);g.drawImage(q.hk,-hs/2,-hs/2,hs,hs);g.restore();
     for(let i=0;i<3;i++){const a=clamp((t-q.win-.7-i*.26)/.25,0,1);if(a<=0)continue;const on=i<q.res.st,sz=(26+8*(1-a))*s;
       kjTx(g,on?"★":"☆",L.x+L.sq/2+(i-1)*34*s,L.y+30*s,`${sz}px ${UI}`,on?`rgba(200,140,40,${a})`:`rgba(120,96,70,${a*.6})`);}
     if(t>q.pat+.6&&!petAway())kjPaw(g,L.mx-58*L.ms/(.5*s),L.mf-96*L.ms/(.5*s),s,clamp((t-q.pat-.6)*4,0,1));}
   for(const b of L.btns)btnRect(g,b.x,b.y,b.w,b.h,b.n,b.id==="done"&&q.n>0&&!q.win);
   if(!petAway()){let st="rest",fi=Math.floor(t*1.5)%2;const fl=L.mf,sc=L.ms;
     if(q.win&&t>q.pat&&t<q.pat+1.4){st="highfive";fi=Math.min(7,Math.floor((t-q.pat)/1.4*8));}
     else if(q.live){const gi=gazeIndex(L.x+q.live.x-L.mx,(fl-150*sc)-(L.y+q.live.y));st=gi<8?"gaze9":"gaze10";fi=gi%8;}
     drawCatG(g,st,fi,L.mx,fl,sc);
     if(q.bub){const e=t-q.bub.t;if(e<2)drawEmoji(g,q.bub.e,L.mx+40*sc*2,fl-200*sc-e*8*s,22*s,clamp(Math.min(e*4,(2-e)*2),0,1));else q.bub=null;}
     if(q.win&&t>q.pat+1.4&&t<q.pat+3.4){const e=t-q.pat-1.4;drawEmoji(g,"😸",L.mx+40*sc*2,fl-200*sc-e*8*s,22*s,clamp(Math.min(e*4,(2-e)*2),0,1));}}
   const hint=q.msg&&t-q.msg.t<3.6?q.msg.s:!q.n&&!q.live&&!q.win?"Веди пальцем по бледному иероглифу":"";
   if(hint){g.save();g.font=`600 ${13*s}px ${UI}`;const hw=g.measureText(hint).width+26*s,hy=L.y+L.sq-24*s;g.fillStyle="rgba(24,18,14,.72)";g.beginPath();g.roundRect(L.x+L.sq/2-hw/2,hy-14*s,hw,28*s,14*s);g.fill();g.restore();
     kjTx(g,hint,L.x+L.sq/2,hy,`600 ${13*s}px ${UI}`,"#efe6d4");}},
 down(G,x,y,t){const q=G.st,L=q.L;if(!L||q.win)return;
   const b=L.btns.find(b=>x>=b.x&&x<=b.x+b.w&&y>=b.y&&y<=b.y+b.h);if(b){kjBtn(G,b.id,t);return;}
   const u=x-L.x,v=y-L.y;if(u>-14&&v>-14&&u<L.sq+14&&v<L.sq+14){kjDown(q,u,v,t);return;}
   if(!petAway()&&Math.abs(x-L.mx)<60*L.ms*2&&y<L.mf&&y>L.mf-200*L.ms){q.bub={e:pick(["😺","😽","🐾"]),t};tone(520,.08,"sine",.03);}},
 move(G,x,y,held,tt){const q=G.st;if(!q.live||!held)return;kjMove(q,x-q.L.x,y-q.L.y,tt??now());},
 up(G){kjUp(G.st);},
 stat:G=>`✍️ черт: ${G.st.w?G.st.w[4]:""}`,
 card(G){const q=G.st,w=q.w,R=q.R||{st:G.score},z=kjS(),n=kjN(),sk=kjStreak(),nx=KJ_IT.find(a=>!S.owned.has(a[0])),left=nx?nx[3]-n:0;
   return`<div class="card"><p class="tag">筆 · Фудэ</p><h3>${["Ещё разок","Получилось","Хорошо","Прекрасно"][R.st]}</h3>
   <div class="kj-res"><b class="kj-big">${w[0]}</b><div><p class="kj-st">${kjStars(R.st)}</p><p class="kj-m">${w[3]}</p><p class="kj-r">${w[1]} · ${w[2]}</p></div></div>
   <p class="lore">${R.fresh?"Слово записано в «Тетрадь».":`Лучшая оценка: ${kjStars(z.d[w[0]]?z.d[w[0]][0]:R.st)}.`}${R.day?` Серия: ${kjPl(sk,["день","дня","дней"])}.`:""} В тетради: ${kjPl(n,["слово","слова","слов"])}.${R.day?" Новое слово — завтра.":""}</p>
   ${R.gift?`<p class="kj-gift">🎁 Новая вещь: «${IT[R.gift].n}». Её можно поставить в любой комнате.</p>`:nx&&left>0?`<p class="kj-r">До новой вещи — ${kjPl(left,["слово","слова","слов"])}.</p>`:""}
   <div class="row"><button class="btn" id="gHome">Домой</button><button class="btn primary" id="gAgain">Ещё раз</button></div></div>`;},
 after(){ui();}};
GAMES.push(KJG);
function kjOpen(w,mode){if(G.id)return;if(w===kjToday()&&!kjDone())mode="day";closePanel();$("album").hidden=true;kjCur={w,mode};kjFont();openPlace("kj_trace");}

// ── the notebook «Тетрадь»: learned words (newest first) → a card; the calligraphy things
function kjTiles(){const z=kjS(),tw=kjToday(),list=KJ_W.map((w,i)=>[w,i]).filter(([w])=>z.d[w[0]]).sort((a,b)=>z.d[b[0][0]][1].localeCompare(z.d[a[0][0]][1]));
  return(kjDone()?"":`<button class="kj-t q" data-x="kj:go"><b>？</b><small>сегодня</small><i>обвести</i></button>`)+
    list.map(([w,i])=>`<button class="kj-t" data-x="kj:c:${i}"><b>${w[0]}</b><small>${w[2]}<br>${w[3].split(",")[0]}</small><i>${kjStars(z.d[w[0]][0])}</i></button>`).join("");}
function kjThings(){return`<div class="coll">${KJ_IT.map(([id,n,,th])=>{const on=S.owned.has(id);return`<div class="ci${on?" on":""}">${itemThumb(IT[id],60,60)}<small>${on?n:`${th} слов`}</small></div>`;}).join("")}</div>`;}
function kjLead(){const z=kjS();return`Каждый день — новое слово. В тетради ${kjN()} из ${KJ_W.length}. Серия: ${kjPl(kjStreak(),["день","дня","дней"])}, лучшая — ${z.best||0}.`;}
function kjBook(){openPanel("Тетрадь",`<p class="lead">${kjLead()}</p><div class="kj-grid">${kjTiles()}</div><h3 class="bh">Каллиграфия</h3><p class="lead">Каждые десять слов — новая вещь.</p>${kjThings()}`,"kj_book");}
function kjCard(i){const w=KJ_W[i],r=kjS().d[w[0]];if(!w)return;
  openPanel("Тетрадь",`<div class="kj-day"><b class="kj-big">${w[0]}</b><div><p class="kj-m">${w[3]}</p><p class="kj-r">${w[1]} · ${w[2]}</p><p class="kj-r">черт: ${w[4]}${r?` · ${kjStars(r[0])} · ${kjDate(r[1])}`:""}</p></div></div>
    <div class="kj-ex"><p class="jp">${w[5]}</p><p><i>${w[6]}</i></p><p>${w[7]}</p></div>
    <div class="row"><button class="btn" data-x="kj:book">← Тетрадь</button><button class="btn primary" data-x="kj:rep:${i}">Обвести ещё раз</button></div>`,"kj_card");}

hook("click",k=>{if(!k.startsWith("kj:"))return;const a=k.split(":");
  if(a[1]==="go")kjOpen(kjToday(),"day");else if(a[1]==="book")kjBook();else if(a[1]==="c")kjCard(+a[2]);else if(a[1]==="rep"&&KJ_W[+a[2]])kjOpen(KJ_W[+a[2]],"rep");return true;});
hook("hub",()=>{const w=kjToday(),d=kjDone(),r=kjS().d[w[0]],sk=kjStreak();
  return`<div class="hubc"><h4>✍️ Слово дня <i>今日の字</i></h4><div class="kj-day"><b class="kj-big">${w[0]}</b><div><p class="kj-m">${w[3]}</p><p class="kj-r">${w[1]} · ${w[2]} · черт: ${w[4]}</p>${d&&r?`<p class="kj-st">${kjStars(r[0])}</p>`:""}</div></div>
  <p>${d?"Сегодня уже обведено. Новое слово появится завтра.":"Обведи иероглиф кистью — слово попадёт в «Тетрадь»."} В тетради: ${kjN()}${sk?`, серия: ${kjPl(sk,["день","дня","дней"])}`:""}.</p>
  <div class="row"><button class="btn${d?"":" primary"}" data-x="kj:go">${d?"Обвести ещё раз":"Обвести кистью"}</button><button class="btn" data-x="kj:book">Тетрадь</button></div></div>`;});
hook("hubDot",()=>kjB&&!kjDone());
hook("album",el=>{if(!kjN())return;el.insertAdjacentHTML("beforeend",`<h3 class="bh">Тетрадь иероглифов</h3><p class="lead">${kjLead()}</p><div class="kj-grid">${kjTiles()}</div>${kjThings()}`);});
hook("boot",()=>{kjB=1;kjFont();});
// the scroll thing shows the player's best trace (its paper in the atlas is blank)
function kjScroll(){if(kjScD===kjScV||!DIMG.kj_scroll)return;kjScD=kjScV;const z=kjS();
  atlasImg("kj",im=>{const r=KJ_R.kj_scroll,c=document.createElement("canvas");c.width=r[2];c.height=r[3];const g=c.getContext("2d");g.drawImage(im,r[0],r[1],r[2],r[3],0,0,r[2],r[3]);
    const seal=()=>{g.fillStyle="rgba(178,48,31,.9)";g.fillRect(74,214,13,13);g.fillStyle="rgba(230,219,194,.8)";g.fillRect(77,217,7,2);g.fillRect(79.5,217,2,7);DIMG.kj_scroll=c;for(const k of [...SPRC.keys()])if(k.startsWith("kj_scroll|"))SPRC.delete(k);};   // drop the tinted sprite cache
    if(z.sc&&z.sc.im){const i=new Image();i.onload=()=>{g.globalAlpha=.94;g.drawImage(i,17,88,86,86);g.globalAlpha=1;seal();};i.src=z.sc.im;}
    else{g.font=`64px ${KJ_FONT}`;g.textAlign="center";g.textBaseline="middle";g.fillStyle=KJ_INK;g.fillText(kjToday()[0],60,132);seal();}});}
hook("sec",kjScroll);
X.kj={S:kjS,today:kjToday,open:()=>kjOpen(kjToday(),"day"),book:kjBook,card:kjCard,force(ch){kjForce=ch;},
  // tests: a real brush stroke through points in square units (0..1) taking `dur` seconds; press a button; the score
  stroke(pts,dur=.45){const q=G.st,L=q.L,P=pts.map(([u,v])=>[u*L.sq,v*L.sq]);let t=now(),tot=0;for(let i=1;i<P.length;i++)tot+=Math.hypot(P[i][0]-P[i-1][0],P[i][1]-P[i-1][1]);
    G.held=true;G.def.down(G,L.x+P[0][0],L.y+P[0][1],t);
    let done=0;for(let i=1;i<P.length;i++){const [x0,y0]=P[i-1],[x1,y1]=P[i],n=Math.ceil(Math.hypot(x1-x0,y1-y0)/5),sl=Math.hypot(x1-x0,y1-y0)/n;
      for(let j=1;j<=n;j++){done+=sl;t+=dur*sl/Math.max(1,tot)*1.6/(.45+Math.sin(Math.PI*clamp(done/tot,0,1)));G.def.move(G,L.x+x0+(x1-x0)*j/n,L.y+y0+(y1-y0)*j/n,true,t);}}
    G.held=false;G.def.up(G);},
  btn(id){const b=G.st.L.btns.find(b=>b.id===id);G.def.down(G,b.x+b.w/2,b.y+b.h/2,now());},score:()=>kjScore(G.st),scrollRedo(){kjScD=0;}};
}
