{
// ───── «Звездопад и телескоп» (st): shooting stars on clear nights, real meteor showers by date, a telescope with Japanese constellations
// Shooting stars live in the 3D sky (two additive meshes right after the sky layer, so roofs and trees cover them); 2D fallback + the attic's round window.
const stS=()=>{const s=S.ext.stars||(S.ext.stars={});s.sh=s.sh||{};s.c=s.c||{};return s;};
const ST_MON=["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"];
// meteor showers: peak day, ± nights, flight angle in the painting (deg, 0 = right, 90 = down)
const ST_SH=[
 {id:"qua",n:"Квадрантиды",g:"Квадрантид",m:1,d:3,w:1,a:150},{id:"lyr",n:"Лириды",g:"Лирид",m:4,d:22,w:1,a:35},
 {id:"eta",n:"Эта-Аквариды",g:"Эта-Акварид",m:5,d:6,w:1,a:55},{id:"per",n:"Персеиды",g:"Персеид",m:8,d:12,w:2,a:140},
 {id:"dra",n:"Дракониды",g:"Драконид",m:10,d:8,w:1,a:120},{id:"ori",n:"Ориониды",g:"Орионид",m:10,d:21,w:1,a:40},
 {id:"leo",n:"Леониды",g:"Леонид",m:11,d:17,w:1,a:25},{id:"gem",n:"Геминиды",g:"Геминид",m:12,d:14,w:1,a:155}];
// one painted thing per shower (art/stars_art.py → assets/items/atlas_st.webp)
const ST_IT={per:["Звёздная пыль Персеид",130,160,"b",878,0,[65,122]],lyr:["Звёздная пыль Лирид",116,176,"b",760,0,[58,138]],leo:["Звёздная пыль Леонид",130,160,"b",0,402,[65,122]],
 eta:["Звёздная вода Эта-Акварид",130,180,"b",628,0,[65,140]],qua:["Звёздный фонарь Квадрантид",150,280,"b",152,0,[75,150]],dra:["Звёздная карта Драконид",150,400,"t",0,0],
 ori:["Латунный телескоп Орионид",220,240,"b",406,0],gem:["Звёздный фурин Геминид",100,260,"t",304,0]};
addItems(ST_SH.map(s=>{const [n,w,h,a,x,y,glow]=ST_IT[s.id];return Object.assign({id:"st_"+s.id,n,c:"Звёздное небо",w,h,a,p:0,at:["st",x,y],src:"🌠 звездопад",
  hint:`🌠 5 звёзд в ночь ${s.g} · ~${s.d} ${ST_MON[s.m-1]}`},glow?{glow}:{});}),{st:[1024,562]});
STAMPS.push(["st_wish","願","Желание на звезду","Нажми на падающую звезду, пока она летит, и загадай желание"],["st_shower","流","Звездопад","Поймай пять звёзд в ночь метеорного потока"],
  ["st_sky","星","Всё небо","Найди в телескоп все семь созвездий"]);
const ST_WISH=["Загадано: чтобы миска не пустела","Загадано: тёплый бок у котацу","Загадано: чтобы фонарь не гас","Загадано: рыбку побольше в пруду",
 "Загадано: чтобы гости заглядывали","Загадано: длинную-длинную дрёму","Загадано: чтобы Муся была рядом","Загадано: лунный моти на двоих",
 "Загадано: тихий дождь по крыше","Загадано: клубок без конца","Загадано: снег к Новому году","Загадано: чтобы лисы не шалили","Загадано: солнечное пятно на татами"];

// ── dates: a night belongs to the evening it started
function stNight(){const d=today();if(hourNow()<12)d.setDate(d.getDate()-1);d.setHours(12,0,0,0);return d;}
const stNK=()=>dayKey(stNight());
function stShAt(d){const y=d.getFullYear();for(const s of ST_SH)for(const yy of[y-1,y,y+1]){const df=Math.round((d-new Date(yy,s.m-1,s.d,12))/864e5);if(Math.abs(df)<=s.w)return s;}return null;}
const stShowerNow=()=>stShAt(stNight());
function stNextSh(){const d0=today(),cur=stShowerNow();d0.setHours(12,0,0,0);let b=null;
  for(const s of ST_SH){if(s===cur)continue;for(const yy of[d0.getFullYear(),d0.getFullYear()+1]){const df=Math.round((new Date(yy,s.m-1,s.d,12)-d0)/864e5);if(df>=0&&(!b||df<b.df))b={s,df};}}return b;}
const stPl=(n,f)=>f[n%10===1&&n%100!==11?0:n%10>=2&&n%10<=4&&(n%100<10||n%100>=20)?1:2];

// ── shooting stars in the room
const ST_ROOMS={engawa:[450,1150,140,330],courtyard:[920,1380,150,560],games:[650,1350,50,320],entrance:[430,1150,70,340],matsuri:[430,1370,70,250],hokora:[700,1060,110,520]};
const ST_UNDER={engawa:"mid"};   // the veranda's sky is a sliver behind the eaves: there stars cross the misty far hills, under the pine
const ST_ATT=[1190,558,82];    // the attic's round window (wall layer): centre and inner radius
let stFly=[],stNext=0,stRoomT=-9,stPool=null,stWasN=null;
function stOn(){return dayTint()[1]&&!weather.on&&!scene.on&&!overlaysOpen()&&(!!ST_ROOMS[S.room]||S.room==="attic");}
function stZ(room){const L=LAYERS[room][0];return layerZ(room,L[0],L[1])*.97;}
function stScr(s,ix,iy){if(!s.att&&G3.on)return proj3(ix,iy,stZ(s.room));const oc=curRow;curRow=null;const p=imgToStage(ix,iy,s.att?.4:LAYERS[s.room][0][1]);curRow=oc;return p;}
function stSpawn(o={}){const room=S.room,sh=stShowerNow(),t=now();let s;
  if(room==="attic"){const [cx,cy,r]=ST_ATT,dir=Math.random()<.5?1:-1,a=rand(.3,.6);
    s={room,att:1,x0:cx-dir*r*.95,y0:cy-r*rand(.3,.65),dx:dir*Math.cos(a),dy:Math.sin(a),L:r*1.9,tail:r*.85,t0:t,dur:o.dur||rand(1.5,1.9),sh};}
  else{const B=ST_ROOMS[room];if(!B)return null;let [x0,x1,y0,y1]=B;
    const vt=-BGM.dy/BGM.k+30,vl=-BGM.dx/BGM.k+30,vr=(view.W-BGM.dx)/BGM.k-30;   // keep to what the screen shows
    x0=Math.max(x0,vl);x1=Math.min(x1,vr);if(x1-x0<220){const c=(x0+x1)/2;x0=c-110;x1=c+110;}y0=Math.max(y0,vt);if(y1-y0<150)y1=y0+150;
    let a=sh?sh.a+rand(-7,7):(Math.random()<.5?rand(14,42):rand(138,166));
    if(y1-y0<260)a=Math.cos(a*Math.PI/180)>0?Math.min(a,rand(12,24)):Math.max(a,180-rand(12,24));   // a low strip of sky: fly flatter
    a*=Math.PI/180;const dx=Math.cos(a),dy=Math.sin(a),sx=dx>0?rand(x0,x0+(x1-x0)*.45):rand(x1-(x1-x0)*.45,x1),sy=rand(y0,y0+(y1-y0)*.35);
    let L=rand(330,470);if(dy>0)L=Math.min(L,(y1+40-sy)/dy);L=Math.min(L,dx>0?(x1+60-sx)/dx:(sx-x0+60)/-dx);L=Math.max(L,200);
    s={room,x0:sx,y0:sy,dx,dy,L,tail:rand(150,230),t0:t,dur:o.dur||rand(1.6,2.2)*L/380,sh};}
  if(o.e0)s.t0=t-o.e0*s.dur-.2;stFly.push(s);if(!petAway()&&pet.action==="idle"&&Math.random()<(sh?.12:.45))react("😮",1.4);return s;}
const stHead=(s,e)=>{const p=Math.min(1,e)*s.L;return[s.x0+s.dx*p,s.y0+s.dy*p,Math.max(4,Math.min(p,s.tail))];};
function stAlpha(s,e){if(s.hit)return clamp(1-(now()-s.hit)/.7,0,1);return clamp((now()-s.t0)/.15,0,1)*clamp((1-e)/.35,0,1);}
// textures: a tapered tail (head at the right end) and a soft head
function stTailCv(){if(stTailCv.c)return stTailCv.c;const c=document.createElement("canvas");c.width=256;c.height=16;const g=c.getContext("2d");
  const gr=g.createLinearGradient(0,0,256,0);gr.addColorStop(0,"rgba(150,180,255,0)");gr.addColorStop(.5,"rgba(190,210,255,.3)");gr.addColorStop(.88,"rgba(236,242,255,.85)");gr.addColorStop(1,"rgba(255,255,255,1)");
  g.fillStyle=gr;const w=()=>{g.beginPath();g.moveTo(0,8);g.lineTo(256,3.6);g.lineTo(256,12.4);g.closePath();g.fill();};g.filter="blur(2px)";w();g.filter="none";w();return stTailCv.c=c;}
function stHeadCv(){if(stHeadCv.c)return stHeadCv.c;const c=document.createElement("canvas");c.width=c.height=64;const g=c.getContext("2d"),gr=g.createRadialGradient(32,32,0,32,32,32);
  gr.addColorStop(0,"rgba(255,255,255,1)");gr.addColorStop(.16,"rgba(246,250,255,.95)");gr.addColorStop(.36,"rgba(190,210,255,.36)");gr.addColorStop(1,"rgba(170,195,255,0)");g.fillStyle=gr;g.fillRect(0,0,64,64);
  g.fillStyle="rgba(235,242,255,.5)";g.fillRect(4,31,56,2);g.fillRect(31,8,2,48);return stHeadCv.c=c;}
function stMk(){const T=G3.T,geo=new T.PlaneGeometry(1,1),mat=c=>{const x=new T.CanvasTexture(c);x.premultiplyAlpha=true;
    return new T.MeshBasicMaterial({map:x,transparent:true,premultipliedAlpha:true,depthTest:false,depthWrite:false,blending:T.AdditiveBlending});};
  return [0,1,2].map(()=>{const P={tail:new T.Mesh(geo,mat(stTailCv())),head:new T.Mesh(geo,mat(stHeadCv()))};for(const m of[P.tail,P.head]){m.renderOrder=.6;m.frustumCulled=false;m.visible=false;}return P;});}
function stMesh(){if(!G3.on||!G3.T)return;const R=G3.rooms&&G3.rooms[bgName()],fly=stFly.filter(s=>!s.att&&s.room===S.room);
  if(!stPool){if(!fly.length)return;stPool=stMk();}const t=now();stPool.vis=fly.length>0;
  stPool.forEach((P,i)=>{const s=fly[i];if(!s||!R){P.tail.visible=P.head.visible=false;return;}
    if(P.tail.parent!==R.back){R.back.add(P.tail);R.back.add(P.head);   // just before the first painted layer after the sky (over the far fog, under trees and roofs)
      if(R.stRO==null){let ro=99;const un=ST_UNDER[S.room],im=un&&LIMG[bgName()+"_"+un];for(const m of R.back.children){const u=m.material&&m.material.uniforms;if(u&&u.map&&u.map.value!==G3.fogT&&m.renderOrder>0&&m.renderOrder<ro&&(!im||u.map.value.image===im))ro=m.renderOrder;}R.stRO=ro===99?.6:ro-.4;}
      P.tail.renderOrder=P.head.renderOrder=R.stRO;}
    const e=(t-s.t0)/s.dur,a=stAlpha(s,e),Z=stZ(s.room),u=Z*TANV/700,[hx,hy,T]=stHead(s,e),W=(ix,iy)=>[(ix/900-1)*Z*TANV*ASP3,(1-iy/700)*Z*TANV];
    const [X,Y]=W(hx-s.dx*T/2,hy-s.dy*T/2);P.tail.position.set(X,Y,-Z);P.tail.rotation.z=Math.atan2(-s.dy,s.dx);P.tail.scale.set(T*u,22*u,1);
    const [hX,hY]=W(hx,hy),hs=(s.hit?64:54)*(.92+.08*Math.sin(t*31))*u;P.head.position.set(hX,hY,-Z+.01);P.head.scale.set(hs,hs,1);
    for(const m of[P.tail,P.head]){m.visible=a>.01;m.material.opacity=a;if(s.hit)m.material.color.setRGB(1,.84,.56);else m.material.color.setRGB(1,1,1);}});}
function stDraw2D(s){const e=(now()-s.t0)/s.dur,a=stAlpha(s,e);if(a<.01)return;const [hx,hy,T]=stHead(s,e),[ax,ay]=stScr(s,hx,hy),[bx,by]=stScr(s,hx-s.dx*T,hy-s.dy*T),k=BGM.k;
  ctx.save();if(s.att){const [cx,cy]=stScr(s,ST_ATT[0],ST_ATT[1]),[ex]=stScr(s,ST_ATT[0]+ST_ATT[2],ST_ATT[1]);ctx.beginPath();ctx.arc(cx,cy,Math.abs(ex-cx),0,Math.PI*2);ctx.clip();}
  ctx.globalCompositeOperation="lighter";ctx.globalAlpha=a;const len=Math.hypot(ax-bx,ay-by),th=(s.att?12:18)*k;
  ctx.save();ctx.translate(bx,by);ctx.rotate(Math.atan2(ay-by,ax-bx));if(s.hit)ctx.filter="sepia(.8)";ctx.drawImage(stTailCv(),0,-th/2,len,th);ctx.restore();
  const hs=(s.hit?44:s.att?30:46)*k;ctx.drawImage(stHeadCv(),ax-hs/2,ay-hs/2,hs,hs);ctx.restore();}
const stSeg=(x,y,ax,ay,bx,by)=>{const vx=bx-ax,vy=by-ay,l=vx*vx+vy*vy||1,u=clamp(((x-ax)*vx+(y-ay)*vy)/l,0,1);return Math.hypot(x-ax-u*vx,y-ay-u*vy);};

// ── a wish
function stWish(s,x,y){const st=stS(),nk=stNK(),t=now();s.hit=t;if(st.nk!==nk){st.nk=nk;st.n=0;}st.n++;st.w=(st.w||0)+1;
  for(let i=0;i<7;i++)floatFx.push({g:i?"✨":"🌠",x:x+rand(-28,28),y:y+rand(-24,20),t:t+i*.06});
  chime([1568,2093,2637]);S.needs.joy=clamp(S.needs.joy+6,0,100);if(!petAway()&&pet.action!=="sleep")react("😻",1.8);
  toast("🌠 Загадай желание!");setTimeout(()=>toast("✨ "+pick(ST_WISH)),1600);award("st_wish");
  const sh=s.sh;if(sh&&stShowerNow()===sh&&st.n>=5&&!st.sh[sh.id]){st.sh[sh.id]=nk;const id="st_"+sh.id;S.owned.add(id);disc("star",sh.id);
    setTimeout(()=>{award("st_shower");toast(`🌠 ${IT[id].n} — в «Вещах»`);chime([784,1047,1319,1568]);},3400);}
  save();}

hook("sec",()=>{const t=now(),st=stS(),sh=stShowerNow(),h=hourNow(),nk=stNK();
  stFly=stFly.filter(s=>s.room===S.room&&(s.hit?t-s.hit<.8:t-s.t0<s.dur+.2));
  if(sh&&(h>=18.5||h<4.5)&&st.tell!==nk&&!overlaysOpen()&&!scene.on){st.tell=nk;save();toast(`🌠 Этой ночью звездопад — ${sh.n}!`);}
  const night=dayTint()[1];if(night!==stWasN){const was=stWasN;stWasN=night;if(was!==null&&S.room==="engawa")ui();}
  if(!stOn())return;if(!stNext)stNext=t+rand(15,40);   // the first star comes soon after dark
  if(t<stNext||t-stRoomT<3||stFly.length>=3)return;
  stSpawn();if(sh&&Math.random()<.3)setTimeout(()=>{if(stOn())stSpawn();},rand(500,1400));
  stNext=t+(sh?rand(10,30):rand(60,180));});
hook("room",()=>{stRoomT=now();stFly=[];});
hook("tick",()=>{if(stFly.length||stPool&&stPool.vis)stMesh();});
hook("draw",(t,front)=>{if(front||!stFly.length)return;for(const s of stFly)if(s.room===S.room&&(s.att||!G3.on))stDraw2D(s);});
hook("hit",(x,y)=>{if(!stFly.length||scene.on)return false;const t=now();let best=null,bd=1e9;
  for(const s of stFly){if(s.room!==S.room||s.hit)continue;const e=(t-s.t0)/s.dur;if(e<0||e>1.03)continue;
    const [hx,hy,T]=stHead(s,e),[ax,ay]=stScr(s,hx,hy),[bx,by]=stScr(s,hx-s.dx*T,hy-s.dy*T),d=Math.min(Math.hypot(x-ax,y-ay)*.8,stSeg(x,y,bx,by,ax,ay)+14);if(d<bd){bd=d;best=s;}}
  if(!best||bd>54)return false;audioInit();stWish(best,x,y);return true;});
// the Milky Way over the house on shower nights
hook("fx",k=>k==="stars"&&!!stShowerNow()&&(dayTint()[1]||hourNow()>=19));

// ── the telescope: a star field with seven Japanese constellations to connect
// stars: [x, y, magnitude, colour] in degrees on the sky (east to the left), edges by index; field 1600×1000
const ST_C=[
 {id:"ikari",jp:"Икари-боси",kj:"錨星",ru:"Кассиопея",cx:250,cy:210,sc:20,hint:"пять звёзд буквой W",
  s:[[6.51,.85,2.3],[2.69,3.47,2.2],[.4,-.72,2.2],[-3.2,-.23,2.7],[-6.09,-3.67,3.4]],e:[[0,1],[1,2],[2,3],[3,4]],
  leg:"Пять звёзд буквой W рыбаки звали Икари-боси — «звёзды-якорь»: будто кто-то бросил якорь в Небесную реку. А в горных деревнях видели в них зубцы хребта и звали Ямагата-боси."},
 {id:"nenohoshi",jp:"Нэ-но хоси",kj:"子の星",ru:"Полярная звезда",cx:640,cy:160,sc:13,mo:-.8,hint:"маленький ковш, на конце ручки — неподвижная звезда",
  s:[[-.45,.58,2.0],[3.39,-.41,4.4],[7.55,-2.53,4.2],[10.11,-6.82,4.3],[12.85,-6.16,5.0],[10.75,-11.65,2.1,"y"],[13.96,-11.63,3.0]],e:[[0,1],[1,2],[2,3],[3,5],[5,6],[6,4],[4,3]],
  leg:"«Звезда Мыши»: она стоит на севере, в стороне Мыши по старому компасу, и никогда не сдвигается с места. По ней правили лодки, а в храмах Мёкэн ей молились как бодхисаттве Полярной звезды."},
 {id:"hokuto",jp:"Хокуто ситисэй",kj:"北斗七星",ru:"Большой Ковш",cx:1040,cy:220,sc:14,hint:"семь ярких звёзд ковшом",
  s:[[11.52,-6.25,1.8,"y"],[11.79,-.88,2.4],[4.33,1.8,2.4],[1.23,-1.53,3.3],[-4.31,-.47,1.8],[-8.6,.57,2.2],[-11.98,6.18,1.9]],d:[[-9.05,.02,4.0]],e:[[0,1],[1,2],[2,3],[3,0],[3,4],[4,5],[5,6]],
  leg:"Семь звёзд Северного Ковша. Возле средней звезды ручки еле видна крошечная соседка. В старину её звали «звездой жизни»: кто перестал её различать, тому, говорят, оставалось недолго."},
 {id:"subaru",jp:"Субару",kj:"昴",ru:"Плеяды",cx:1440,cy:330,sc:190,mo:-1.5,hint:"тесная кучка голубых звёздочек",
  s:[[0,0,2.9,"b"],[-.381,.05,3.6,"b"],[.265,.15,4.2,"b"],[.596,0,3.7,"b"],[.377,-.267,3.9,"b"],[.521,-.367,4.3,"b"]],d:[[-.42,-.08,5.1],[.66,-.2,5.4],[.33,-.47,5.8]],
  e:[[1,0],[0,2],[2,3],[3,4],[4,0],[4,5]],
  leg:"«Субару» — значит «собранные вместе»: звёздочки нанизаны на одну нить, как бусины. Тысячу лет назад Сэй-Сёнагон начала с них свой список в «Записках у изголовья»: «Звёзды — это Субару»."},
 {id:"tanabata",jp:"Орихимэ и Хикобоси",kj:"織姫・彦星",ru:"Вега и Альтаир",cx:620,cy:640,sc:11,hint:"три яркие звезды треугольником у Небесной реки",
  s:[[12.29,-11.78,0,"b"],[-10.81,-18.28,1.25],[-2.67,18.13,.77],[-1.53,16.38,2.7,"y"],[-3.81,20.6,3.7]],e:[[0,1],[1,2],[2,0],[3,2],[2,4]],
  leg:"Небесная ткачиха Орихимэ и пастух Хикобоси так полюбили друг друга, что забросили работу, и Небесный владыка развёл их по берегам Небесной реки. Видятся они раз в год, в седьмой день седьмой луны, — если нет дождя."},
 {id:"sasori",jp:"Уоцури-боси",kj:"魚釣り星",ru:"Скорпион",cx:985,cy:815,sc:11.5,hint:"длинный изогнутый хвост с красной звездой",
  s:[[10.01,-12.2,2.6],[11,-9.38,2.3],[11.04,-5.88,2.9],[6.04,-6.4,2.9],[4.16,-5.57,1,"r"],[2.67,-3.78,2.8],[-.45,2.3,2.3],[-.76,6.05,3],[-1.22,10.37,3.6],[-4.4,11.24,3.3],[-9.01,11,1.9],[-10.57,7.03,2.4],[-9.09,5.1,1.6]],
  e:[[0,1],[1,2],[1,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[10,11],[11,12]],
  leg:"Изогнутый хвост Скорпиона на Внутреннем море звали Уоцури-боси — «рыболовный крючок»: будто кто-то удит рыбу в Небесной реке. А красную звезду в его сердце звали Акабоси — «красная звезда»."},
 {id:"tsuzumi",jp:"Цудзуми-боси",kj:"鼓星",ru:"Орион",cx:1380,cy:700,sc:19,hint:"барабан: красная звезда вверху, белая внизу, три в поясе",
  s:[[-4.75,-8.4,.5,"r"],[2.7,-7.35,1.6],[1,-.7,2.2],[-.05,.2,1.7],[-1.19,.95,1.8],[-2.9,8.67,2.1],[5.32,7.2,.1,"b"]],e:[[0,1],[1,2],[0,4],[2,3],[3,4],[4,5],[2,6],[6,5]],
  leg:"Орион, перетянутый посередине, похож на ручной барабан цудзуми. Красная звезда наверху — Хэйкэ-боси, под алым знаменем рода Тайра, белая внизу — Гэндзи-боси, под белым знаменем Минамото. Так и стоят друг против друга."}];
const ST_CH=["Икари-боси","Нэ-но хоси","Хокуто","Субару","Орихимэ","Уоцури","Цудзуми"];
for(const c of ST_C){const all=c.s.concat(c.d||[]),xs=all.map(p=>p[0]),ys=all.map(p=>p[1]),mx=(Math.min(...xs)+Math.max(...xs))/2,my=(Math.min(...ys)+Math.max(...ys))/2,f=p=>[c.cx+(p[0]-mx)*c.sc,c.cy+(p[1]-my)*c.sc];
  c.P=c.s.map(f);c.D=(c.d||[]).map(f);const px=c.P.map(p=>p[0]),py=c.P.map(p=>p[1]);c.bb=[Math.min(...px),Math.min(...py),Math.max(...px),Math.max(...py)];}
const ST_MW=[[90,-120],[250,210],[493,426],[665,728],[874,952],[990,1160]];   // the Milky Way: Cassiopeia → Deneb → between Vega and Altair → Scorpius
const stGot=id=>!!stS().c[id],stFound=()=>ST_C.filter(c=>stGot(c.id)).length,stEk=(a,b)=>a<b?a+"-"+b:b+"-"+a;
const ST_COL={w:["255,250,240","#fffaf0"],y:["255,226,170","#fff0d0"],r:["255,150,110","#ffd0b8"],b:["185,210,255","#eef4ff"]};
function stSpr(k){const C=stSpr.c||(stSpr.c={});if(C[k])return C[k];const c=document.createElement("canvas");c.width=c.height=64;const g=c.getContext("2d"),gr=g.createRadialGradient(32,32,0,32,32,32),col=ST_COL[k][0];
  gr.addColorStop(0,`rgba(${col},1)`);gr.addColorStop(.18,`rgba(${col},.55)`);gr.addColorStop(.45,`rgba(${col},.14)`);gr.addColorStop(1,`rgba(${col},0)`);g.fillStyle=gr;g.fillRect(0,0,64,64);return C[k]=c;}
function stStar(g,x,y,r,k,al){const R=r*3.6;g.globalAlpha=al*.9;g.drawImage(stSpr(k||"w"),x-R,y-R,R*2,R*2);g.globalAlpha=al;g.fillStyle=ST_COL[k||"w"][1];g.beginPath();g.arc(x,y,Math.max(.8,r*.55),0,Math.PI*2);g.fill();g.globalAlpha=1;}
function stLay(G){const q=G.st,s=G.s,gap=6*s,rh=Math.max(30,31*s);q.lw=G.W;q.lh=G.H;q.top=8*s;
  q.chips=ST_C.map((c,i)=>{const row=i<4?0:1,n=row?3:4,k=row?i-4:i,cw=(G.W-gap*(n+1))/n;return{x:gap+k*(cw+gap),y:G.H-gap-rh-(row?0:rh+gap),w:cw,h:rh,i};});
  const fs=q.fs=(G.H-2*(rh+gap)-gap-q.top)/1000,vw=G.W/fs;q.pmax=Math.max(0,1600-vw);q.px0=(1600-vw)/2;q.pan=q.pan==null?q.pmax*.5:clamp(q.pan,0,q.pmax);
  const bx0=Math.min(0,q.px0)-20,bx1=Math.max(1600,q.px0+vw)+20,by0=-q.top/fs-4,by1=(G.H-q.top)/fs+4;q.bx0=bx0;q.by0=by0;
  const c=document.createElement("canvas");c.width=Math.ceil((bx1-bx0)*fs);c.height=Math.ceil((by1-by0)*fs);const g=c.getContext("2d"),r=Math.random,X=fx=>(fx-bx0)*fs,Y=fy=>(fy-by0)*fs;
  const gr=g.createLinearGradient(0,0,0,c.height);gr.addColorStop(0,"#060a16");gr.addColorStop(.7,"#0d1428");gr.addColorStop(1,"#18203a");g.fillStyle=gr;g.fillRect(0,0,c.width,c.height);
  const band=[];for(let i=0;i<ST_MW.length-1;i++){const [ax,ay]=ST_MW[i],[bx,by]=ST_MW[i+1],n=Math.ceil(Math.hypot(bx-ax,by-ay)/14);for(let j=0;j<n;j++)band.push([mix(ax,bx,j/n),mix(ay,by,j/n),Math.atan2(by-ay,bx-ax)]);}
  for(const [x,y] of band){const ox=(r()-.5)*60,oy=(r()-.5)*60,R=(70+r()*90)*fs,h=g.createRadialGradient(X(x+ox),Y(y+oy),0,X(x+ox),Y(y+oy),R);h.addColorStop(0,`rgba(176,186,226,${.03+r()*.035})`);h.addColorStop(1,"rgba(176,186,226,0)");g.fillStyle=h;g.fillRect(X(x+ox)-R,Y(y+oy)-R,R*2,R*2);}
  for(const [x,y,a] of band)if(r()<.35){const o=(r()-.5)*50,R=(14+r()*26)*fs,cx=X(x-Math.sin(a)*o),cy=Y(y+Math.cos(a)*o),h=g.createRadialGradient(cx,cy,0,cx,cy,R);h.addColorStop(0,"rgba(4,6,14,.22)");h.addColorStop(1,"rgba(4,6,14,0)");g.fillStyle=h;g.fillRect(cx-R,cy-R,R*2,R*2);}
  const dot=(x,y,sz,al,tone)=>{g.fillStyle=`rgba(${tone},${al})`;g.beginPath();g.arc(x,y,sz,0,Math.PI*2);g.fill();};
  for(let i=0;i<1600;i++){const [x,y,a]=band[(r()*band.length)|0],o=(r()+r()+r()-1.5)*70,j=(r()-.5)*16;dot(X(x-Math.sin(a)*o+Math.cos(a)*j),Y(y+Math.cos(a)*o+Math.sin(a)*j),.35+r()*.6,.25+r()*.5,"215,222,255");}
  const N=Math.round(c.width*c.height/850);for(let i=0;i<N;i++){const b=r()<.04;dot(r()*c.width,r()*c.height,b?.7+r()*.3:.3+r()*.45,b?.45+r()*.25:.15+r()*.45,r()<.15?"255,226,196":r()<.3?"200,215,255":"238,240,250");}
  q.bg=c;const v=document.createElement("canvas");v.width=Math.ceil(G.W);v.height=Math.ceil(G.H);const vg=v.getContext("2d"),vr=vg.createRadialGradient(G.W/2,G.H*.42,Math.min(G.W,G.H)*.32,G.W/2,G.H*.42,Math.max(G.W,G.H)*.78);
  vr.addColorStop(0,"rgba(0,0,0,0)");vr.addColorStop(1,"rgba(0,0,0,.6)");vg.fillStyle=vr;vg.fillRect(0,0,G.W,G.H);q.vig=v;}
function stHitStar(G,x,y){const q=G.st,px=q.pmax>0?q.pan:q.px0,R=Math.max(22,24*G.s);let b=null,bd=R;
  ST_C.forEach((c,ci)=>c.P.forEach(([fx,fy],i)=>{const d=Math.hypot((fx-px)*q.fs-x,q.top+fy*q.fs-y);if(d<bd){bd=d;b={c:ci,i};}}));return b;}
function stWrap(g,txt,w){const out=[];let ln="";for(const wd of txt.split(" ")){const t=ln?ln+" "+wd:wd;if(g.measureText(t).width>w&&ln){out.push(ln);ln=wd;}else ln=t;}if(ln)out.push(ln);return out;}
function stTap(G,h){const q=G.st,c=ST_C[h.c],t=now();
  if(stGot(c.id)){q.sel=null;q.card={c,t};tone(880,.08,"sine",.03);return;}
  if(q.sel&&q.sel.c===h.c&&q.sel.i!==h.i){const k=stEk(h.i,q.sel.i),E=q.ed[c.id]||(q.ed[c.id]=new Set());
    if(c.e.some(([a,b])=>stEk(a,b)===k)){if(!E.has(k)){E.add(k);q.lines++;tone(560+E.size*55,.3,"sine",.05);if(E.size===c.e.length){stFoundC(G,c);return;}}}
    else tone(190,.14,"triangle",.04);}
  else tone(990,.07,"sine",.03);
  q.sel=h;}
function stFoundC(G,c){const q=G.st,st=stS(),t=now();q.sel=null;st.c[c.id]=1;disc("star","c_"+c.id);S.needs.joy=clamp(S.needs.joy+4,0,100);
  chime([784,988,1175,1568]);for(const [x,y] of c.P)q.fx.push({x,y,t:t+Math.random()*.4});q.card={c,t:t+.9};if(stFound()===ST_C.length)award("st_sky");save();}
const STG={id:"st_scope",hidden:true,n:"Телескоп",tag:"星空 · Звёздное небо",icon:"🔭",bg:"forest",lives:null,time:null,lore:"",how:"",
 init(G,t){Object.assign(G.st,{pan:null,sel:null,dn:null,rub:null,card:null,hint:null,fx:[],lines:0,ed:{}});stLay(G);},
 step(G){const q=G.st;if(q.lw!==G.W||q.lh!==G.H)stLay(G);if(q.panTo!=null){q.pan+=(q.panTo-q.pan)*.12;if(Math.abs(q.panTo-q.pan)<1){q.pan=q.panTo;q.panTo=null;}}},
 draw(G,g,t){const q=G.st,s=G.s,fs=q.fs;if(!q.bg)return;const px=q.pmax>0?q.pan:q.px0,X=fx=>(fx-px)*fs,Y=fy=>q.top+fy*fs;
  g.fillStyle="#070b17";g.fillRect(0,0,G.W,G.H);g.drawImage(q.bg,(q.bx0-px)*fs,q.top+q.by0*fs);
  g.save();g.lineCap="round";
  for(const c of ST_C){const got=stGot(c.id),E=q.ed[c.id];if(!got&&!(E&&E.size))continue;
    for(const [a,b] of c.e){if(!got&&!E.has(stEk(a,b)))continue;g.beginPath();g.moveTo(X(c.P[a][0]),Y(c.P[a][1]));g.lineTo(X(c.P[b][0]),Y(c.P[b][1]));
      g.strokeStyle="rgba(236,206,140,.16)";g.lineWidth=5*s;g.stroke();g.strokeStyle=got?"rgba(240,214,150,.78)":"rgba(240,214,150,.6)";g.lineWidth=1.4*s;g.stroke();}}
  if(q.hint){const e=t-q.hint.t,c=q.hint.c;if(e>4.5||stGot(c.id))q.hint=null;else{g.setLineDash([5*s,6*s]);g.strokeStyle=`rgba(200,214,255,${Math.min(1,e*3,(4.5-e)/.8)*(.4+.15*Math.sin(t*5))})`;g.lineWidth=1.2*s;
    for(const [a,b] of c.e){g.beginPath();g.moveTo(X(c.P[a][0]),Y(c.P[a][1]));g.lineTo(X(c.P[b][0]),Y(c.P[b][1]));g.stroke();}g.setLineDash([]);}}
  if(q.rub&&q.dn&&q.dn.star){const h=q.dn.star,p=ST_C[h.c].P[h.i];g.setLineDash([4*s,5*s]);g.strokeStyle="rgba(240,214,150,.55)";g.lineWidth=1.3*s;g.beginPath();g.moveTo(X(p[0]),Y(p[1]));g.lineTo(q.rub[0],q.rub[1]);g.stroke();g.setLineDash([]);}
  g.restore();
  ST_C.forEach((c,ci)=>{const mo=c.mo||0,rad=m=>clamp(1.5+(3.4-m-mo)*.75,1.4,4.8)*s;
    c.D.forEach(([fx,fy],i)=>stStar(g,X(fx),Y(fy),rad(c.d[i][2])*.8,"w",.75));
    c.P.forEach(([fx,fy],i)=>{const x=X(fx),y=Y(fy);if(x<-30||x>G.W+30)return;const p=c.s[i];stStar(g,x,y,rad(p[2])*(.88+.12*Math.sin(t*2.3+i*1.7+ci*2.1)),p[3],1);
      if(q.sel&&q.sel.c===ci&&q.sel.i===i){g.strokeStyle=`rgba(240,214,150,${.6+.3*Math.sin(t*6)})`;g.lineWidth=1.5*s;g.beginPath();g.arc(x,y,11*s,0,Math.PI*2);g.stroke();}});
    if(stGot(c.id)){const x=X((c.bb[0]+c.bb[2])/2),y=Y(c.bb[3])+16*s;if(x>-80&&x<G.W+80)textC(g,`${c.kj} ${c.jp}`,x,y,11.5*s,"rgba(236,214,160,.82)",600);}});
  for(let i=q.fx.length-1;i>=0;i--){const f=q.fx[i],e=(t-f.t)/1.4;if(e>1){q.fx.splice(i,1);continue;}if(e<0)continue;const x=X(f.x),y=Y(f.y),r=(4+16*Math.sin(Math.PI*e))*s;
    g.save();g.globalCompositeOperation="lighter";g.strokeStyle=`rgba(255,236,190,${1-e})`;g.lineWidth=1.4*s;g.beginPath();g.moveTo(x-r,y);g.lineTo(x+r,y);g.moveTo(x,y-r);g.lineTo(x,y+r);g.stroke();g.restore();}
  g.drawImage(q.vig,0,0,G.W,G.H);
  // the top line: a hint, or the legend card of a constellation
  const fam=getComputedStyle(document.body).fontFamily;
  if(q.card&&t>=q.card.t){const c=q.card.c,pad=14*s,w=Math.min(G.W-24*s,520*s),x0=(G.W-w)/2,y0=12*s;g.save();g.font=`500 ${13.2*s}px ${fam}`;const L=stWrap(g,c.leg,w-pad*2),all=stFound()===ST_C.length,h=pad*2+28*s+L.length*18.5*s+(all?22*s:0)+16*s;
    g.globalAlpha=clamp((t-q.card.t)*4,0,1);g.fillStyle="rgba(12,16,28,.93)";g.strokeStyle="rgba(232,200,120,.45)";g.lineWidth=1.2;g.beginPath();g.roundRect(x0,y0,w,h,14*s);g.fill();g.stroke();
    g.textAlign="left";g.textBaseline="top";g.fillStyle="#ecd49a";g.font=`700 ${16*s}px ${fam}`;g.fillText(`${c.jp} — ${c.ru}`,x0+pad,y0+pad);
    g.textAlign="right";g.font=`600 ${15*s}px ${fam}`;g.fillStyle="rgba(236,212,154,.7)";g.fillText(c.kj,x0+w-pad,y0+pad+1*s);
    g.textAlign="left";g.font=`500 ${13.2*s}px ${fam}`;g.fillStyle="#e4ded0";L.forEach((l,i)=>g.fillText(l,x0+pad,y0+pad+28*s+i*18.5*s));
    if(all){g.fillStyle="#ecd49a";g.font=`700 ${13*s}px ${fam}`;g.fillText("✦ Всё небо найдено!",x0+pad,y0+pad+28*s+L.length*18.5*s+4*s);}
    g.fillStyle="rgba(228,222,208,.45)";g.font=`500 ${10.5*s}px ${fam}`;g.textAlign="right";g.fillText("нажми, чтобы закрыть",x0+w-pad,y0+h-pad-6*s);g.restore();}
  else{const hc=q.hint&&q.hint.c,txt=hc?`${ST_CH[ST_C.indexOf(hc)]}: ${hc.hint}`:!q.lines&&!stFound()?"Соединяй яркие звёзды пальцем · небо двигается":"";
    if(txt){g.save();g.font=`600 ${12.5*s}px ${fam}`;const tw=Math.min(G.W-16*s,g.measureText(txt).width+26*s),hy=q.top+18*s;g.fillStyle="rgba(10,12,20,.66)";g.beginPath();g.roundRect(G.W/2-tw/2,hy-13*s,tw,26*s,13*s);g.fill();g.restore();textC(g,txt,G.W/2,hy,12.5*s,"#e8e2d4",600);}}
  for(const b of q.chips){const c=ST_C[b.i],got=stGot(c.id),hot=q.hint&&q.hint.c===c;g.save();g.fillStyle=got?"rgba(54,44,22,.9)":hot?"rgba(40,48,76,.92)":"rgba(14,18,30,.86)";g.strokeStyle=got?"rgba(236,206,140,.6)":"rgba(200,210,235,.25)";
    g.beginPath();g.roundRect(b.x,b.y,b.w,b.h,10*s);g.fill();g.stroke();g.restore();textC(g,(got?"✓ ":"")+ST_CH[b.i],b.x+b.w/2,b.y+b.h/2,Math.min(12.5*s,b.h*.4),got?"#ecd49a":"#c9cfdc",600);}},
 down(G,x,y,t){const q=G.st;if(q.card&&t>=q.card.t){q.card=null;return;}
  const ch=q.chips.find(b=>x>=b.x&&x<=b.x+b.w&&y>=b.y&&y<=b.y+b.h);
  if(ch){const c=ST_C[ch.i];tone(700,.06,"sine",.03);if(stGot(c.id))q.card={c,t};else{q.hint={c,t};q.sel=null;if(q.pmax>0)q.panTo=clamp((c.bb[0]+c.bb[2])/2-G.W/q.fs/2,0,q.pmax);}return;}
  q.dn={x,y,pan:q.pan,star:stHitStar(G,x,y),mv:0};q.mx=x;q.my=y;},
 move(G,x,y){const q=G.st,d=q.dn;if(!d)return;q.mx=x;q.my=y;if(Math.hypot(x-d.x,y-d.y)>8)d.mv=1;if(!d.mv)return;
  if(d.star)q.rub=[x,y];else if(q.pmax>0){q.panTo=null;q.pan=clamp(d.pan-(x-d.x)/q.fs,0,q.pmax);}},
 up(G){const q=G.st,d=q.dn;q.dn=null;q.rub=null;if(!d)return;
  if(!d.mv){if(d.star)stTap(G,d.star);else q.sel=null;return;}
  if(d.star){const h=stHitStar(G,q.mx,q.my);if(h&&h.c===d.star.c&&h.i!==d.star.i){q.sel=d.star;stTap(G,h);}}},
 stat:()=>`✦ Созвездий: ${stFound()} из ${ST_C.length}`};
GAMES.push(STG);
function stScope(){if(G.id)return;if(!dayTint()[1]){toast("🔭 Звёзды видно только ночью");return;}if(weather.on){toast("☁️ Небо в тучах — звёзд не видно");return;}closePanel();openPlace("st_scope");}

// ── tray, hub, album, away
document.head.insertAdjacentHTML("beforeend","<style>.st-kj{display:flex;align-items:center;justify-content:center;height:60px;font-size:24px;color:#e8d49a;font-family:serif;letter-spacing:-1px}</style>");
hook("tray",(tray,room)=>{if(room!=="engawa"||(S.trayMode[room]||"play")!=="play"||!dayTint()[1])return;const row=tray.querySelector(".items");if(!row)return;
  row.insertAdjacentHTML("afterbegin",`<button class="item wide" data-x="st:scope"><span class="ico">🔭</span><span class="nm">Телескоп</span></button>`);});
hook("click",k=>{if(!k.startsWith("st:"))return;if(k==="st:scope")stScope();return true;});
hook("hub",()=>{const st=stS(),sh=stShowerNow(),nx=stNextSh(),night=dayTint()[1],tn=st.nk===stNK()?st.n||0:0,caught=Object.keys(st.sh).length;
  const md=s=>`${s.d} ${ST_MON[s.m-1]}`,when=nx?(nx.df===0?"Сегодня ночью":nx.df===1?"Завтра ночью":`Через ${nx.df} ${stPl(nx.df,["день","дня","дней"])}`)+` — ${nx.s.n} (${md(nx.s)})`:"";
  const top=sh?`<b>Этой ночью звездопад — ${sh.n}!</b> ${st.sh[sh.id]?"Звёздный подарок уже у тебя.":`Звёзды падают часто: поймай пять — и останется «${IT["st_"+sh.id].n}».`}`
    :"Ясными ночами над домом пролетают падающие звёзды. Нажми на звезду, пока она летит, и загадай желание.";
  return`<div class="hubc"><h4>🌠 Звёздное небо <i>星空</i></h4><p>${top}</p>${when?`<p>${when}.</p>`:""}<p>Желаний: ${st.w||0}${tn?` (этой ночью ${tn}${sh&&!st.sh[sh.id]?" из 5":""})`:""} · звездопадов: ${caught} из ${ST_SH.length} · созвездий: ${stFound()} из ${ST_C.length}</p>
    <div class="row"><button class="btn${night?" primary":""}" data-x="st:scope">🔭 ${night?"Телескоп":"Телескоп — ночью"}</button></div></div>`;});
hook("hubDot",()=>{const sh=stShowerNow();return !!sh&&dayTint()[1]&&!stS().sh[sh.id];});
hook("away",()=>{const sh=stShowerNow();if(!sh||stS().sh[sh.id])return null;return{i:"🌠",t:`Этой ночью звездопад — ${sh.n}. Смотри в небо!`};});
hook("album",el=>{const st=stS(),N=stFound(),caught=Object.keys(st.sh).length;if(!st.w&&!N&&!caught)return;
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Звёздное небо</h3><p class="lead">Загадано желаний: ${st.w||0}. Созвездий в телескоп: ${N} из ${ST_C.length}. Звездопадов поймано: ${caught} из ${ST_SH.length}.</p>
   <div class="coll">${ST_C.map(c=>stGot(c.id)?`<div class="ci on"><span class="st-kj" style="font-size:${c.kj.length<3?26:c.kj.length<4?20:14}px">${c.kj}</span><small>${c.jp}<br>${c.ru}</small></div>`:`<div class="ci"><span class="q">?</span><small>???</small></div>`).join("")}</div>
   <div class="coll">${ST_SH.map(s=>{const it=IT["st_"+s.id],on=S.owned.has(it.id);return`<div class="ci ${on?"on":""}">${on?itemThumb(it,64,60):`<span class="q">?</span>`}<small>${s.n}<br>${s.d} ${ST_MON[s.m-1]}</small></div>`;}).join("")}</div>`);});

// tests: spawn a (slow) star, tap it, open the telescope, connect stars, tap chips
X.st={state:stS,fly:()=>stFly,shower:stShowerNow,next:stNextSh,
  spawn(o){return!!stSpawn(o||{});},reset(v){stNext=v||0;stRoomT=-9;},
  head(){const s=stFly.find(s=>s.room===S.room&&!s.hit);if(!s)return null;const [hx,hy]=stHead(s,(now()-s.t0)/s.dur);return stScr(s,hx,hy);},
  tap(){const p=X.st.head();return p?!!hk("hit",p[0],p[1]):false;},
  scope:stScope,
  link(id,i,j){const c=ST_C.find(c=>c.id===id),q=G.st,px=q.pmax>0?q.pan:q.px0;for(const k of[i,j]){const x=(c.P[k][0]-px)*q.fs,y=q.top+c.P[k][1]*q.fs;G.held=true;G.def.down(G,x,y,now());G.held=false;G.def.up(G);}},
  solve(id){const c=ST_C.find(c=>c.id===id),q=G.st;if(q.pmax>0)q.pan=clamp((c.bb[0]+c.bb[2])/2-G.W/q.fs/2,0,q.pmax);for(const [a,b] of c.e)X.st.link(id,a,b);},
  chip(i){const b=G.st.chips[i];G.def.down(G,b.x+b.w/2,b.y+b.h/2,now());G.def.up(G);},
  pan(v){G.st.pan=clamp(v,0,G.st.pmax);}};
}
