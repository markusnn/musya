{
// ───────────────────────── Third story «Шпилька Бэни»: one chapter per calendar day ─────────────────────────
// A book in the 物語 tab (BOOKS), opens after the first story. Beni (the zashiki-warashi) lost the kanzashi Haru gave her
// in 1924: the parade's wheel broke it in three; the pond, a cat that is long gone and an old kimono keep the parts, the
// kitchen lantern mends it with rice glue, and in the light of the torii lantern the girl Haru of 1924 pins it on her.
// Chapters touching the great-grandmother's chest (feat/chest.js) change their words with S.ext.chest.n, so nothing
// the chest has not told yet is spoiled. After the end Haru runs past the torii once a night while the lantern burns.
MON.m_s3_haru=[300,640];
STAMPS.push(["s3_end","簪","Шпилька Бэни","Пройди третью историю"]);
const S3C="Реликвии Бэни",S3L="📜 третья история",S3H="Эту вещь даст третья история — вкладка «Сюжет» 📜";
addItems([["s3_case","Пустой футляр для шпильки",0,180,110],["s3_fox","Фонарик с лисьим огнём",184,110,200,"t"],["s3_geta","Детская гэта Хару",298,150,100],
  ["s3_mouse","Тряпичная мышка",452,144,92],["s3_ame","Пакет леденцов титосэ-амэ",600,96,220],["s3_hashi","Детские палочки Хару",700,180,74],["s3_kaza","Вертушка Хару",884,112,204]]
  .map(([id,n,x,w,h,a])=>({id,n,c:S3C,w,h,a:a||"b",p:0,story:1,src:S3L,hint:S3H,at:["s3",x,0]})),{s3:[996,220]});
const S3LINE={s3_case:"На красном шёлке — отпечаток цветка сливы",s3_fox:"Лисий огонёк светит на то, что потеряно",s3_geta:"Сто лет пролежала у каппы под камнем",
  s3_mouse:"Игрушки оставляют только своим",s3_ame:"Леденцы «на тысячу лет» с праздника Сити-го-сан",s3_hashi:"Хару ела ими сто лет назад",s3_kaza:"Крутится, даже когда нет ветра"};
Object.assign(RELIC_LINE,S3LINE);

const st=S.ext.story3=Object.assign({ch:0,prog:[],started:false,done:false,seen:-1,ready:false},S.ext.story3||{});st.ready=!!st.ready;
const cn=()=>(S.ext.chest&&S.ext.chest.n)||0;   // pages of the chest already read: don't tell what it has not told
const vf=(f,m=120)=>()=>{const l=-BGM.dx/BGM.k,r=(view.W-BGM.dx)/BGM.k;return clamp(l+(r-l)*f,Math.max(m,l+m),Math.min(1800-m,r-m));};
const H3="m_s3_haru",KO="m_rm_kosode";
// my: characters drawn by this block (memory tint, faint, from/to paragraph); tora: the cat in Musya's dream
const CH=[
 {title:"Пролог. Чёлка без шпильки",room:"bedroom",reward:"s3_case",
  intro:{my:[{id:W_,x:vf(.8,150),y:1210,h:400,d:.8,a:.5,faint:1}],p:[
   "После Ста свечей девочка в красном осталась в доме. Она прячет клубки, топает босыми пятками по коридору и хихикает за сёдзи. Но этой ночью Муся проснулась от другого звука: кто-то медленно, щель за щелью, ощупывал татами.",
   "Это была она. Чёлка падала ей на глаза: в волосах не было шпильки — чёрной, лаковой, с серебряным цветком сливы и красной бусиной. Девочка носила её больше ста лет и ни разу не снимала.",
   "Дзасики-вараси не плачут. Они просто бледнеют — так выцветает дом, в котором перестали смеяться. Сквозь девочку уже просвечивали сёдзи. Шпильку нужно найти, пока её ещё видно."]},
  tasks:[{t:"Погладь Мусю: ей тоже не спится",ev:"act",test:a=>a==="purr"},{t:"Погаси андон в спальне — в темноте видно, где блестит",ev:"lamp",test:off=>!!off},
   {t:"Поиграй с Мусей 3 раза: от смеха вараси становятся ярче",ev:"act",n:3,test:a=>PLAYS.includes(a)}],
  outro:{sx:"shoji",my:[{id:W_,x:vf(.8,150),y:1210,h:400,d:.8,a:.62,faint:1}],p:[
   "Когда андон погас, девочка перестала искать. Она подошла к сёдзи и провела пальцем по бумаге. На белом проступили буквы — круглые, старинные, как в книгах, напечатанных сто лет назад: «Хару звала меня Бэни».",
   "Буквы появлялись медленно, будто писать было трудно: «Шпильку подарила Хару. Я потеряла её в ночь, когда мимо дома шёл парад. Без шпильки она меня не узнает».",
   "Кто — «она», Бэни не дописала. Утром у порога спальни лежал пустой лаковый футляр, выстланный красным шёлком. На шёлке остался отпечаток: тонкая палочка, цветок сливы и круглая вмятина от бусины."]}},
 {title:"Глава 1. Что видели лисы",room:"entrance",reward:"s3_fox",
  intro:{my:[{id:WB,x:vf(.24,110),y:1200,h:330,d:.7,a:.55,faint:1}],p:[
   "В ночь парада Бэни шла последней, спиной вперёд, и смотрела на Мусю. Значит, шпилька пропала там, на дороге за тории, среди фонарей с глазами, зонтов на одной ноге и колёс, которые катятся сами.",
   "Всё, что случается на ночных дорогах, знают лисы. Но даром они не рассказывают: им нужен запах жареного тофу, кошка в лисьей маске и поклон богине Инари, которой они служат.",
   "Бэни дошла с Мусей до ворот и остановилась. Дальше тории она не идёт — даже за шпилькой."]},
  tasks:[{t:"Приготовь инари-суси — лисье угощение (Кухня → 🍳 Готовить)",ev:"cook",test:d=>!!d&&d.id==="inari"},
   {t:"Надень Мусе маску кицунэ (Гардероб)",ev:"tick",test:()=>S.wear.head==="kitsune"||/mk_kitsune/.test(S.wear.mask||"")},{t:"Помолись у ворот — лисы служат Инари",ev:"place",test:a=>a==="pray"}],
  outro:{sx:"fox",my:[{id:"m_kitsune",x:vf(.78,200),y:1180,h:360,d:.7},{id:WB,x:vf(.24,110),y:1200,h:330,d:.7,a:.6,faint:1}],p:[
   "Белая лиса вышла из темноты, не потревожив ни одной травинки. Съела инари, облизнулась и только потом посмотрела на Мусю: «Котёнок в нашей маске. Как мило. Ты пришла узнать про шпильку».",
   "«Её никто не крал. Под утро парад торопился, и Ванюдо — горящее колесо с лицом — прокатился прямо по ней. Шпилька рассыпалась на три части, и каждая ушла туда, где её помнят».",
   "«Серебряный цветок утонул в пруду, у каппы. Лаковую палочку унесла в зубах кошка, которой давно нет на свете. А бусина… бусина покатилась домой». Лиса оставила у тории бумажный фонарик с голубым огоньком: «Им светят на то, что потеряно»."]}},
 {title:"Глава 2. Цветок на дне",room:"courtyard",reward:"s3_geta",
  intro:{sx:"pond",p:[
   "Каппа живёт в пруду дольше, чем стоит дом, и помнит всех детей, что бегали по этому двору. Если серебро упало в его воду, оно у него.",
   "Но каппа не выходит на шум. К нему стучат камешком по воде, сидят тихо, пока круги не улягутся, — и кланяются, когда он покажется.",
   "Муся поставила лисий фонарик у самой воды. В голубом свете на дне что-то блеснуло: маленькое, белое, похожее на цветок."]},
  tasks:[{t:"Брось в пруд камешек — так стучат к каппе",ev:"place",test:a=>a==="pebble"},{t:"Посиди у пруда: «Медитация»",ev:"place",test:a=>a==="meditate"},
   {t:"Поклонись каппе: выиграй «Поклон каппе» (Игры)",ev:"game",test:d=>!!d&&d.id==="kappa"&&d.score>=1}],
  outro:{my:[{id:"m_kappa",x:vf(.8,170),y:1150,h:360,d:.55},{id:H3,x:vf(.3,120),y:1150,h:330,d:.55,mem:1,p0:2,p1:3}],p:[
   "Каппа вынырнул, поклонился в ответ и придержал лапой блюдце на макушке — второй раз он воду не прольёт. На перепончатой ладони лежал серебряный цветок сливы, целый, только чуть потемневший.",
   "«Я знаю, чья это вещь, — проворчал каппа. — Девочки Хару. Сто лет назад она бросала мне огурцы и считала до ста, чтобы я успел спрятаться. Ни разу не подглядела. Вежливая была».",
   "Над водой на миг проступила девочка в лиловом кимоно со стрелами, с бумажной вертушкой в руке. Она зажмурилась и считала вслух: «…девяносто восемь, девяносто девять, сто!» Потом открыла глаза — и растаяла. Вода её помнит.",
   "Каппа отдал цветок Мусе, а из-под камня выкатил маленькую гэта с красным ремешком. «Это она тогда потеряла. Сто лет берёг. Отдай тому, кто будет её помнить»."]}},
 {title:"Глава 3. Кошка, которой нет",room:"engawa",reward:"s3_mouse",
  intro:{my:[{id:W_,x:vf(.2,130),y:1300,h:420,d:.8,a:.7,faint:1}],p:[
   "Лиса сказала: палочку унесла кошка, которой давно нет на свете. Муся не испугалась. Кошки знают: та, что любила свой дом, иногда возвращается посидеть на тёплом месте.",
   "Такую гостью не позовёшь по имени и не выманишь рыбой. Она приходит на смех, на игру и в сон. Лучше всего — в сон другой кошки.",
   "Бэни села на край веранды и болтала ногами. Она явно кого-то ждала — и, кажется, знала кого."]},
  tasks:[{t:"Поиграйте с Мусей на веранде 4 раза",ev:"act",n:4,test:a=>PLAYS.includes(a)&&S.room==="engawa"},
   {t:"Сыграй в «Кагомэ-кагомэ»: кто стоит у тебя за спиной? (Игры)",ev:"game",test:d=>!!d&&d.id==="kagome"&&d.score>=3},
   {t:"Уложи Мусю вздремнуть на веранде — кошки встречаются во сне",ev:"act",test:a=>a==="sleep"&&S.room==="engawa"}],
  outro:{tora:{x:vf(.8,140),p0:0,p1:3},my:[{id:W_,x:vf(.2,130),y:1300,h:420,d:.8,a:.8,faint:1}],get p(){return[
   "Муся задремала — и во сне на веранду вышла кошка. Полосатая, как Муся, с такими же полосками на лбу, с таким же кольцом на кончике хвоста. Только сквозь неё был виден сад.",
   cn()>=7?"Бэни беззвучно ахнула и протянула руки. Это была Тора — та самая кошка со старой фотографии из сундука прабабушки. Она прожила в этом доме долгую жизнь и, видно, так и не ушла из него насовсем."
    :"Бэни беззвучно ахнула и протянула к ней руки. Они были знакомы — давно, очень давно. Как зовут кошку, Бэни не написала: только улыбнулась и показала наверх, туда, где чердак. Когда-нибудь об этом расскажет сам дом.",
   "Кошка-тень положила к ногам Бэни лаковую палочку — чёрную, гладкую, с крошечными следами зубов. Потом потёрлась о Мусин нос, будто о свой, и растаяла вместе со сном.",
   "Когда Муся проснулась, у её лап лежала тряпичная мышка из старого шёлка, с надкушенным ухом. Свои игрушки кошки оставляют только своим."];}}},
 {title:"Глава 4. Руки из рукавов",room:"wardrobe",reward:"s3_ame",
  intro:{p:[
   "Осталась бусина. Лиса сказала: она покатилась домой. Но где дом у коралловой бусины? Бэни думала долго, а потом повела Мусю в гардероб — к сундукам с кимоно, которые носили задолго до Муси.",
   "У старой одежды есть память. Из рукавов кимоно, которое долго носила одна хозяйка, по ночам иногда тянутся руки. Торияма Сэкиэн называл их косодэ-но-тэ — «руки из рукавов». Обычно их боятся.",
   "Чтобы рукава раскрылись, к ним приходят нарядными, играют в детскую игру и оставляют подарок взамен того, что заберут."]},
  tasks:[{t:"Надень Мусе праздничное кимоно с хризантемами (Гардероб → Кимоно)",ev:"tick",test:()=>S.wear.body==="k_kiku"},
   {t:"Сыграй в «Дарума упал»: дойди до водящего 3 раза (Игры)",ev:"game",test:d=>!!d&&d.id==="daruma"&&d.score>=3},
   {t:"Поставь в Гардеробе вещь из «🧺 Вещи» — подарок рукаву",ev:"put",test:d=>!!d&&d.room==="wardrobe"}],
  outro:{fx:()=>seeBeast("rm_kosode"),my:[{id:KO,x:vf(.76,190),y:1160,h:420,d:.5},{id:H3,x:vf(.3,120),y:1180,h:340,d:.55,mem:1,p0:2,p1:3}],p:[
   "В глубине гардероба на старой вешалке висело праздничное кимоно — тёмно-сливовое, в белых цветах. Из рукава медленно показались руки — маленькие, детские, будто в рукаве, как в домике, кто-то спрятался. В ладонях лежала красная бусина.",
   "И гардероб вспомнил. Осень тысяча девятьсот двадцать четвёртого года, праздник Сити-го-сан. Это кимоно надела мама Хару, а семилетняя Хару весь день держалась за его рукав. В тот день ей подарили пару шпилек: одну — в причёску, вторую — про запас. Вечером вторую она оставила на татами для девочки, которую видела только она.",
   "Хару стояла у вешалки такой, какой была в тот вечер: с вертушкой, со шпилькой в волосах, румяная от сладостей. Она протянула бусину Бэни и что-то сказала, но слов не было слышно: воспоминания не говорят вслух.",
   "Руки спрятались в рукава. На полу остался бумажный пакет с журавлём и черепахой — в таких на Сити-го-сан дарят детям длинные леденцы «на тысячу лет». Все три части шпильки нашлись. Осталось её починить."]}},
 {title:"Глава 5. Рисовый клей",room:"kitchen",reward:"s3_hashi",
  intro:{p:[
   "Цветок, палочка и бусина лежат на столе. Но шпилька, по которой проехало колесо, сама не срастётся. В старину бумагу, дерево и лак чинили рисовым клеем: разминали горячий рис, пока он не станет тягучим и прозрачным.",
   "Лучше всех об этом знает старый бумажный фонарь под потолком кухни. Его сто лет подклеивали рисом, шов за швом. Говорят, однажды шов разошёлся — и оказался ртом.",
   "Фонарь проснётся, если на кухне запахнет рисом и домом. И если ему расскажут что-нибудь страшное: старые фонари это любят."]},
  tasks:[{t:"Слепи онигири (Кухня → 🍳 Готовить)",ev:"cook",test:d=>!!d&&d.id==="onigiri"},{t:"Свари мисо-суп — пусть кухня пахнет домом",ev:"cook",test:d=>!!d&&d.id==="miso"},
   {t:"Прочитай кайдан (Спальня → Кайдан)",ev:"kaidan"}],
  outro:{my:[{id:"m_obake",x:vf(.78,170),y:330,h:340,d:.5,anchor:"c"},{id:W_,x:vf(.22,130),y:1250,h:400,d:.8,a:.85}],p:[
   "Шов на фонаре разошёлся, моргнул огромный глаз, и длинный язык лизнул горячий рис. «Рисовый клей, — прошелестел тётин-обакэ. — Хороший. Как раньше».",
   "«Я помню эту шпильку, — сказал он, пока Бэни держала цветок, палочку и бусину. — Девочка Хару каждый вечер оставляла у очага горсть риса — для подружки, которую, кроме неё, никто не видел. А утром подружка прибегала сюда, в красном, со шпилькой в чёлке. Красиво блестело».",
   "Языком, тонко, как кисточкой, фонарь промазал клеем все трещины. Шпилька срослась. Шов на ней видно, только если знать, где искать.",
   "Бэни держала шпильку двумя руками, но не надевала. На запотевшем окне проступило: «Её должна надеть Хару». А под окном лежали детские палочки для еды, красные, лаковые. Хару ела ими сто лет назад."]}},
 {title:"Эпилог. Две шпильки",room:"entrance",reward:"s3_kaza",
  intro:{sx:"toro",my:[{id:W_,x:vf(.3,120),y:1200,h:380,d:.7}],p:[
   "Есть поверье: свет у ворот видят не только живые. Кто зажжёт фонарь для того, кого ждёт, — к тому он найдёт дорогу, даже если идти очень далеко. Даже из другого времени.",
   "Бэни стоит у тории со шпилькой в руках. Она ждёт так, как умеют ждать только дзасики-вараси: не шевелясь, не моргая, всем домом сразу.",
   "Осталось зажечь фонарь заново — для одного-единственного гостя — и сделать так, чтобы у ворот пахло домом."]},
  tasks:[{t:"Перезажги каменный фонарь у тории: погаси и зажги снова",ev:"lantern",test:on=>!!on},
   {t:"Поставь у входа футляр для шпильки (🧺 Вещи → Реликвии Бэни)",ev:"tick",test:()=>!!S.placed.s3_case&&S.placed.s3_case.r==="entrance"},{t:"Омой Мусе лапки у ворот",ev:"place",test:a=>a==="wash_paws"}],
  outro:{sx:"toro",fx:()=>{lanternOn=true;},my:[{id:W_,x:vf(.3,120),y:1200,h:380,d:.7,pin:1},{id:H3,x:vf(.72,130),y:1190,h:360,d:.7,mem:1,warm:1,p1:3}],get p(){return[
   "Фонарь разгорелся, и в его свете под тории вбежала девочка в лиловом кимоно — запыхавшаяся, с вертушкой в руке, с красной бусиной в волосах. Гэта стучали по камням так звонко, будто на дворе снова тысяча девятьсот двадцать четвёртый год.",
   "«Бэни! Вот ты где! — засмеялась Хару. — А я тебя везде ищу». Она взяла шпильку, привстала на цыпочки и воткнула её Бэни в чёлку. Потом потрогала свою: «Вот. Теперь у нас одинаковые. Теперь я тебя где угодно узнаю».",
   "Хару присела перед Мусей: «Какая полосатая! Как маленький тигр"+(cn()>=7?". Вырасту — заведу себе такую же и назову Тора":"")+"». Почесала её за ухом, вскочила и побежала обратно в свет фонаря. Оглянулась, помахала: «Бэни, завтра поиграем!» Стук гэта стал тише, тише — и пропал.",
   cn()>=11?"Бэни смотрела ей вслед и улыбалась. Она знала то, чего девочка Хару ещё не знала: что та проживёт в этом доме целую жизнь и каждый вечер будет зажигать для неё этот фонарь."
    :"Бэни смотрела ей вслед и улыбалась — впервые за много ночей. Шпилька в её чёлке горела красной искрой, а сама Бэни стала такой яркой, что от неё на камнях легла тень.",
   "Утром у подножия фонаря нашлась бумажная вертушка. Ветра не было, а она крутилась. Говорят, если в доме живёт дзасики-вараси, детей в нём всегда на одного больше, чем сосчитаешь. В эту ночь их было больше на двоих."];}}}
];
function seeBeast(k){if(BESTIARY.some(b=>b[0]===k)&&!ST.seen.includes(k))ST.seen.push(k);}
const plural=(n,a,b,c)=>{const x=n%10,y=n%100;return x===1&&y!==11?a:x>=2&&x<=4&&(y<12||y>14)?b:c;};
function gate(s){
  if(!QS.done)return"Откроется, когда закончится первая история";
  if(s.ch>0&&s.day&&dayKey()<=s.day){const d=today(),m=new Date(d);m.setHours(24,0,0,0);const h=Math.ceil((m-d)/36e5);
    return"Следующая глава откроется завтра"+(h>1?` — через ${h} ${plural(h,"час","часа","часов")}`:" — меньше чем через час");}
  return null;}
const B={id:"s3",title:"Шпилька Бэни",ch:CH,st,gate,
  lead:"Третья история: девочка в красном потеряла шпильку — подарок Хару, которая жила в этом доме сто лет назад. По главе в сутки: пройденная глава открывает следующую завтра.",
  fin:"История пройдена. Бэни снова носит шпильку. А ночью, пока горит фонарь у ворот, под тории иногда пробегает девочка с вертушкой.",
  after(k){disc("chapter3",k);st.day=dayKey();save();},
  end(){award("s3_end");st.endT=Date.now();vs.day="";}};
BOOKS.push(B);

// ── drawing the scene people: memory tint (warm, see-through), faint Beni, Tora from Musya's own frames ──
function glowAt(x,y,r,rgb,a){if(a<=0||r<=0)return;const g=ctx.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,`rgba(${rgb},${a})`);g.addColorStop(.35,`rgba(${rgb},${a*.45})`);g.addColorStop(1,`rgba(${rgb},0)`);ctx.fillStyle=g;ctx.fillRect(x-r,y-r,r*2,r*2);}
const TC={};function tinted(id,tint){const k=id+"|"+tint;if(TC[k])return TC[k];const im=MIMG[id],m=MON[id];if(!im||!m||!(im.naturalWidth||im.width))return null;
  const c=document.createElement("canvas");c.width=m[0];c.height=m[1];const g=c.getContext("2d");g.drawImage(im,0,0,m[0],m[1]);g.globalCompositeOperation="source-atop";g.fillStyle=tint;g.fillRect(0,0,m[0],m[1]);return TC[k]=c;}
function monWith(id,img,...a){const o=MIMG[id];MIMG[id]=img;try{drawMon(id,...a);}finally{MIMG[id]=o;}}
function chAlpha(c,k,t){const T=scene.s3||(scene.s3={});if(scene.i<(c.p0||0))return 0;const on=T[k]||(T[k]=t);let a=clamp((t-on)/1.2,0,1);
  if(c.p1!=null&&scene.i>=c.p1){const off=T[k+"x"]||(T[k+"x"]=t);a*=clamp(1-(t-off)/1.6,0,1);}return a;}
let toraC=null;
function drawTora(t,ix,a){if(!IMG.rest||a<=0)return;if(!toraC){toraC=document.createElement("canvas");toraC.width=384;toraC.height=416;}
  const g=toraC.getContext("2d");g.globalCompositeOperation="source-over";g.clearRect(0,0,384,416);frameImg("rest",Math.floor(t*2.2)%8,g);
  g.globalCompositeOperation="source-atop";g.fillStyle="rgba(150,178,226,.4)";g.fillRect(0,0,384,416);g.globalCompositeOperation="source-over";
  const s=view.s,[x,y]=imgToStage(ix,catLineY(),CAT_D);glowAt(x,y-90*s,160*s,"170,200,255",.22*a);
  ctx.save();ctx.globalAlpha=a*(.5+.08*Math.sin(t*2.1));ctx.translate(x,y);ctx.scale(-1,1);ctx.drawImage(toraC,-96*s,-195*s,192*s,208*s);ctx.restore();}
function drawPeople(t,front){
  if(!scene.on||scene.book!==CH)return;const sc=CH[scene.ch][scene.kind];if(!sc)return;const cl=catLineY()+6;
  (sc.my||[]).forEach((c,k)=>{if((c.y>cl)!==front)return;let a=chAlpha(c,"m"+k,t)*(c.a||1);if(a<=0)return;const x=c.x();
    if(c.faint)a*=.82+.18*Math.sin(t*1.7+k);
    if(c.mem){const [sx,sy]=imgToStage(x,c.y,c.d),hh=c.h*BGM.k;ctx.save();ctx.globalCompositeOperation="lighter";glowAt(sx,sy-hh*.5,hh*.62,c.warm?"255,196,120":"255,214,160",.28*a);ctx.restore();
      const im=tinted(c.id,"rgba(255,206,140,.26)");if(im)monWith(c.id,im,x,c.y,c.h,c.d,a*.8,c.anchor||"b");return;}
    drawMon(c.id,x,c.y,c.h,c.d,a,c.anchor||"b");
    if(c.pin&&scene.i>=1){const [sx,sy]=imgToStage(x,c.y,c.d),hh=c.h*BGM.k;glowAt(sx+hh*.09,sy-hh*.79,hh*.07,"255,90,70",.6+.25*Math.sin(t*3));}});
  if(sc.tora&&!front){const a=scene.i>=(sc.tora.p0||0)?chAlpha(sc.tora,"tora",t):0;drawTora(t,sc.tora.x(),a);}}
// scene light: the fox-fire by the pond, the shoji glow, the torii lantern breathing
function drawFx(t){
  if(!scene.on||scene.book!==CH)return;const sc=CH[scene.ch][scene.kind];if(!sc||!sc.sx)return;
  ctx.save();ctx.globalCompositeOperation="lighter";
  if(sc.sx==="toro"){const [x,y]=imgToStage(...propAt("p_ent_toro",330,885),.85),p=.8+.2*Math.sin(t*2.4);glowAt(x,y,170*BGM.k*p+40*view.s,"255,180,90",.35*p);}
  if(sc.sx==="fox"&&scene.i>=2){const [x,y]=imgToStage(vf(.6,120)(),1150,.7),p=.75+.25*Math.sin(t*3.1);glowAt(x,y,90*view.s,"110,190,255",.4*p);}
  if(sc.sx==="pond"){const [x,y]=imgToStage(vf(.62,140)(),1120,.55),p=.7+.3*Math.sin(t*2.7);glowAt(x,y,110*view.s,"110,190,255",.32*p);if(scene.i>=2)glowAt(x-20*view.s,y+18*view.s,26*view.s,"235,245,255",.6*p);}
  if(sc.sx==="shoji"){const [x,y]=imgToStage(vf(.66,150)(),900,.6),p=.6+.2*Math.sin(t*1.3);glowAt(x,y,150*view.s,"255,226,190",.18*p*(scene.i>=0?1:0));}
  ctx.restore();}
hook("draw",(t,front)=>{drawPeople(t,front);drawVis(t,front);});
hook("overlay",t=>drawFx(t));

// ── after the end: once a night, while the torii lantern burns, Haru runs past the gate ──
const vs={on:false,t0:0,day:"",x0:0,x1:0};const vsX=t=>vs.x0+(vs.x1-vs.x0)*clamp((t-vs.t0)/12,0,1);   // she runs across the path, right to left
function visTick(t){
  if(!st.done)return;
  if(vs.on){if(t-vs.t0>12||S.room!=="entrance"||scene.on){vs.on=false;}return;}
  if(S.room!=="entrance"||!dayTint()[1]||!lanternOn||scene.on||overlaysOpen()||vs.day===dayKey()||t-roomT<6)return;
  vs.on=true;vs.t0=t;vs.day=dayKey();vs.x0=vf(.78,130)();vs.x1=vf(.34,130)();
  if(!petAway())setTimeout(()=>{if(vs.on&&pet.action!=="sleep")react("😸",2);},1500);}
let roomT=0;hook("room",()=>{roomT=now();});
function visA(t){const e=t-vs.t0;return clamp(Math.min(e/1.4,(12-e)/1.6),0,1);}
function drawVis(t,front){if(!vs.on||S.room!=="entrance"||(1190>catLineY()+6)!==front)return;const a=visA(t);if(a<=0)return;
  const x=vsX(t),[sx,sy]=imgToStage(x,1190,.7),hh=330*BGM.k;ctx.save();ctx.globalCompositeOperation="lighter";glowAt(sx,sy-hh*.5,hh*.6,"255,196,120",.22*a);ctx.restore();
  const im=tinted(H3,"rgba(255,206,140,.26)");if(im)monWith(H3,im,x,1190,330,.7,a*.75,"b",0,true);}
hook("hit",(x,y)=>{if(!vs.on||visA(now())<.3)return false;const [sx,sy]=imgToStage(vsX(now()),1190,.7),h=330*BGM.k,w=h*.5;
  if(x>sx-w/2&&x<sx+w/2&&y>sy-h&&y<sy){vs.t0=now()-10.4;S.needs.joy=clamp(S.needs.joy+8,0,100);toast("Хару машет рукой и убегает в свет фонаря");chime([1046,1318,1568]);return true;}return false;});
hook("tick",t=>visTick(t));
// relics: a line and a little chime when tapped in a room
hook("itemTap",it=>{if(!S3LINE[it.id])return;chime([1046,1318,1568]);fxAt(it,["✨"],4);toast(S3LINE[it.id]);if(!petAway()&&pet.action!=="sleep")react("😺",1.4);return true;});
// a quiet note when a new chapter unlocks (at start or at midnight while playing) — nothing opens by itself
let last=null;
function note(){const k=bkState(B);if(k==="intro"&&(last==="gate"||last===null)&&st.note!==st.ch+"@"+dayKey()&&!scene.on){st.note=st.ch+"@"+dayKey();
  setTimeout(()=>{if(!scene.on)toast(st.ch?"📜 Шпилька Бэни: новая глава в «Сюжете»":"📜 В «Сюжете» — история про шпильку Бэни");},last===null?11000:300);}last=k;}
hook("boot",note);hook("sec",()=>{if(last!==null)note();});
// test handles
X.story3={B,st,CH,gate:()=>gate(st),state:()=>bkState(B),vs,cn,
  intro(){bkIntro(B);},outro(){bkOutro(B);},
  fin(){CH[st.ch].tasks.forEach((tk,i)=>st.prog[i]=tk.n||1);st.ready=true;tabDots();},
  jump(k,kind,i){st.ch=k;st.seen=k;st.prog=[];st.ready=kind==="outro";st.done=false;playScene(k,kind,()=>{},true,CH);scene.i=i||0;showPara();},
  vis(){st.done=true;vs.day="";vs.on=false;roomT=-99;}};
}
