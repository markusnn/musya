{
// ───────────────────────── «Настоящая погода и времена года»: the real weather outside (Open-Meteo) and the seasons by the real month ─────────────────────────
// S.ext.wx = {city:"nn"|…|"off", w:{code,temp,pr,sn,day,at,city}|null}. The weather hook drives rain only while the 🌦 button is on «авто».
// No pictures: snow caps are computed at runtime from each layer's own silhouette and added to the 3D scene right above that layer.
const WX_CITY={nn:["Нижний Новгород","в Нижнем Новгороде",56.3269,44.0059],msk:["Москва","в Москве",55.7558,37.6173],spb:["Санкт-Петербург","в Санкт-Петербурге",59.9343,30.3351],
  kzn:["Казань","в Казани",55.7963,49.1088],ekb:["Екатеринбург","в Екатеринбурге",56.8389,60.6057],nsk:["Новосибирск","в Новосибирске",55.0084,82.9357],
  sochi:["Сочи","в Сочи",43.5855,39.7231],tokyo:["Токио","в Токио",35.6762,139.6503],kyoto:["Киото","в Киото",35.0116,135.7681]};
const WX_TXT={0:"ясно",1:"почти ясно",2:"переменная облачность",3:"пасмурно",45:"туман",48:"туман с изморозью",51:"морось",53:"морось",55:"сильная морось",56:"ледяная морось",57:"ледяная морось",
  61:"небольшой дождь",63:"дождь",65:"сильный дождь",66:"ледяной дождь",67:"ледяной дождь",71:"небольшой снег",73:"снег",75:"сильный снег",77:"снежная крупа",80:"ливень",81:"ливень",82:"сильный ливень",
  85:"снегопад",86:"сильный снегопад",95:"гроза",96:"гроза с градом",99:"гроза с градом"};
const WX_ICO={clear:"☀️",cloud:"⛅",fog:"🌫",drizzle:"🌦",rain:"🌧",snow:"🌨",thunder:"⛈"};
// season: [name, kanji, icon, what is special now]
const WX_SEA={winter:["Зима","冬","❄️","На веранде, камнях и тории лежит снег, порой идёт снежок, а на улице у Муси видно дыхание."],
  spring:["Весна","春","🌸","Ветер приносит лепестки, а ночами у воды перекликаются лягушки."],
  tsuyu:["Цую, сезон дождей","梅雨","☔","Дожди идут чаще обычного, сад в сине-лиловом свете гортензий, после дождя выползают улитки."],
  summer:["Лето","夏","🎐","Днём звенят цикады и дрожит зной, а ночами светлячков вдвое больше."],
  autumn:["Осень","秋","🍁","Во дворе кружат кленовые листья момидзи, ночами поют сверчки."]};
const wxS=()=>S.ext.wx||(S.ext.wx={city:"nn",w:null});
const wxSt={wet:false,wetT:0,flake:false,flakeT:0,gust:false,gustT:0,fest:false,rainWas:null,seaKey:null,cic:false,cicT:0,puffs:[],puffT:0,snailX:0};
let wxTry=0,wxBusy=0,wxFail=0;
function wxKind(c){return c<=1?"clear":c<=3?"cloud":c===45||c===48?"fog":c>=51&&c<=57?"drizzle":c>=61&&c<=67||c>=80&&c<=82?"rain":c>=71&&c<=77||c===85||c===86?"snow":c>=95?"thunder":"cloud";}
function wxSeason(){if(wxSt.sea)return wxSt.sea;const m=today().getMonth()+1;return m===12||m<=2?"winter":m<=5?"spring":m===6?"tsuyu":m<=8?"summer":"autumn";}
function wxSeaKey(){const T=today(),s=wxSeason();return s+"-"+(s==="winter"&&T.getMonth()<2?T.getFullYear()-1:T.getFullYear());}
// the cached real weather counts while it is fresh (90 min) and belongs to the chosen city
function wxReal(){const W=wxS(),w=W.w;return WX_CITY[W.city]&&w&&w.city===W.city&&Date.now()-w.at<90*60e3?w:null;}
function wxRealK(){const w=wxReal();return w?wxKind(w.code):null;}
function wxFetch(force){const W=wxS(),C=WX_CITY[W.city];if(!C||wxBusy)return;const w=W.w;
  if(!force&&(w&&w.city===W.city&&Date.now()-w.at<20*60e3||Date.now()-wxTry<20*60e3))return;
  wxTry=Date.now();wxBusy=1;const city=W.city;
  fetch(`https://api.open-meteo.com/v1/forecast?latitude=${C[2]}&longitude=${C[3]}&current=weather_code,precipitation,snowfall,temperature_2m,is_day`)
    .then(r=>r.ok?r.json():null).then(j=>{const c=j&&j.current;if(!c||typeof c.weather_code!=="number"){wxFail=1;return;}
      if(wxS().city!==city)return;wxFail=0;W.w={code:c.weather_code,temp:c.temperature_2m,pr:c.precipitation,sn:c.snowfall,day:c.is_day,at:Date.now(),city};save();if(panelIs("hub"))openHub();})
    .catch(()=>{wxFail=1;}).finally(()=>{wxBusy=0;});}
const wxDeg=t=>{const v=Math.round(t);return(v>0?"+":v<0?"−":"")+Math.abs(v)+"°";};
function wxIcon(w){const k=wxKind(w.code);return k==="clear"&&!w.day?"🌙":w.code===3?"☁️":WX_ICO[k];}
const wxRainK=k=>k==="rain"||k==="drizzle"||k==="thunder";
// snow lies all winter, unless the real city is warm and not snowing (Sochi, Tokyo…)
function wxSnowLies(){if(wxSeason()!=="winter")return false;const w=wxReal();return !w||w.temp<=3||wxKind(w.code)==="snow";}
function wxSnowFall(){if(S.weather!=="auto")return false;const k=wxRealK();if(k)return k==="snow";return wxSeason()==="winter"&&wxSt.flake;}
const wxOut=()=>OUTDOOR.includes(S.room);
function wxFestFall(){const F=festNow();return !!F&&F.fx.some(k=>["snow","peach","momiji","sakura"].includes(k));}

// ── hooks: weather and festival-style effects (a festival always leads)
hook("weather",()=>{const k=wxRealK();if(k)return wxRainK(k)?"rain":"clear";const s=wxSeason();
  if(s==="winter")return"clear";if(s==="tsuyu")return wxSt.wet?"rain":"clear";return null;});
hook("fx",k=>{if(wxSt.fest)return false;if(k==="snow")return wxSnowFall();const s=wxSeason();
  if(k==="peach")return s==="spring"&&wxSt.gust&&!weather.on;if(k==="momiji")return s==="autumn"&&wxSt.gust&&!weather.on;return false;});

// ── every second: schedules (snow at times, tsuyu showers, gusts), real-weather refresh, toasts, season discovery, sounds
function wxFlip(on,tKey,flag,a,b,c,d){const t=now();if(t<wxSt[tKey])return;wxSt[flag]=!wxSt[flag];wxSt[tKey]=t+(wxSt[flag]?rand(a,b):rand(c,d));}
hook("sec",()=>{const t=now(),s=wxSeason();wxSt.fest=wxFestFall();
  wxFlip(1,"flakeT","flake",70,180,90,240);wxFlip(1,"wetT","wet",120,260,60,140);
  if(s==="spring")wxFlip(1,"gustT","gust",25,50,45,100);else wxFlip(1,"gustT","gust",50,110,30,70);
  wxFetch(false);
  const k=wxRealK(),rain=k?wxRainK(k)||k==="snow":null;
  if(wxSt.rainWas===false&&rain&&S.weather==="auto"&&!document.hidden&&!scene.on){const C=WX_CITY[wxS().city];toast(`${k==="snow"?"🌨":"🌧"} ${C[1][0].toUpperCase()+C[1].slice(1)} ${k==="snow"?"пошёл снег":"пошёл дождь"}`);}
  wxSt.rainWas=rain;
  const key=wxSeaKey();if(key!==wxSt.seaKey){wxSt.seaKey=key;if(disc("season",key)){const A=WX_SEA[s];setTimeout(()=>toast(`${A[2]} ${A[0]} ${A[1]} — загляни в 家`),4000);save();}}
  wxSounds(t,s);wxSnowVis();
});
hook("boot",()=>{wxSt.fest=wxFestFall();wxSt.seaKey=null;wxFetch(false);});
hook("tick",t=>{const k=S.weather==="auto"?wxRealK():null,sea=wxSeason();
  if((sea==="winter"||sea==="autumn")&&!wxSt.fest&&t>sakura.next-5&&t>sakura.until){sakura.next=t+rand(60,140);if(sea==="autumn"){wxSt.gust=true;wxSt.gustT=t+rand(30,60);}}   // real rain without a thunderstorm, and tsuyu drizzle: no lightning
  if(weather.on&&(k&&k!=="thunder"||!k&&wxSeason()==="tsuyu"))weather.nextBolt=t+30;});

// ── sounds: cicadas (summer days), frogs (spring nights), crickets (autumn nights)
const wxAu={g:null};
function wxCicada(on){const c=snd.ctx;if(!c)return;if(on&&!wxAu.g){try{const b=c.createBuffer(1,c.sampleRate*2,c.sampleRate),d=b.getChannelData(0);for(let i=0;i<d.length;i++)d[i]=Math.random()*2-1;
    const src=c.createBufferSource();src.buffer=b;src.loop=true;const f=c.createBiquadFilter();f.type="bandpass";f.frequency.value=5200;f.Q.value=5;
    const am=c.createGain();am.gain.value=.5;const lfo=c.createOscillator();lfo.frequency.value=42;const lg=c.createGain();lg.gain.value=.5;lfo.connect(lg);lg.connect(am.gain);
    const g=c.createGain();g.gain.value=0;src.connect(f);f.connect(am);am.connect(g);g.connect(c.destination);src.start();lfo.start();wxAu.g=g;}catch(e){return;}}
  if(wxAu.g)wxAu.g.gain.setTargetAtTime(on?.02:0,c.currentTime,on?1.6:.5);}
function wxSounds(t,s){const h=hourNow(),night=dayTint()[1],ok=snd.on&&snd.ctx&&wxOut()&&!document.hidden&&!overlaysOpen()&&!weather.on;
  if(s==="summer"){if(t>wxSt.cicT){wxSt.cic=!wxSt.cic;wxSt.cicT=t+(wxSt.cic?rand(7,14):rand(5,12));}wxCicada(!!(ok&&h>=8.5&&h<18.5&&wxSt.cic));}else if(wxAu.g)wxCicada(false);
  if(!ok||!night)return;
  if(s==="spring"&&Math.random()<.4){const f=rand(170,210);tone(f,.07,"square",.025);setTimeout(()=>tone(f*.88,.09,"square",.025),120);if(Math.random()<.5)setTimeout(()=>{tone(f*1.05,.07,"square",.02);setTimeout(()=>tone(f*.9,.09,"square",.02),120);},380);}
  if(s==="autumn"&&Math.random()<.55){const f=rand(4100,4700);for(let i=0;i<3;i++)setTimeout(()=>tone(f,.045,"sine",.012),i*75);}
}

// ── snow on the paintings: caps along every upward edge of a layer's silhouette, a drift along the veranda edge, patches on the ground
const wxSC=new Map();   // room → {ln: canvas|null}
function wxNoise(W,H,cw,ch,r){const gw=Math.ceil(W/cw)+2,gh=Math.ceil(H/ch)+2,v=new Float32Array(gw*gh);for(let i=0;i<v.length;i++)v[i]=r();
  return(x,y)=>{const fx=x/cw,fy=y/ch,ix=fx|0,iy=fy|0,ux=fx-ix,uy=fy-iy,sx=ux*ux*(3-2*ux),sy=uy*uy*(3-2*uy),i=iy*gw+ix;return mix(mix(v[i],v[i+1],sx),mix(v[i+gw],v[i+gw+1],sx),sy);};}
// generic: the snow of one picture drawn into a W×H canvas; th = cap thickness factor, gy = canvas row below which it is ground (thicker drift, patches if dust)
function wxCapCv(im,W,H,th0,gy,dust,seed){
  const c=document.createElement("canvas");c.width=W;c.height=H;
  const g=c.getContext("2d",{willReadFrequently:true});g.drawImage(im,0,0,W,H);const A=g.getImageData(0,0,W,H).data,img=g.createImageData(W,H),o=img.data,r=rng(seed);
  const al=(x,y)=>A[(y*W+x)*4+3];let any=false;
  const put=(x,y,a,sh)=>{if(a<=.01)return;const i=(y*W+x)*4,v=Math.min(255,a*255);if(v<=o[i+3])return;o[i]=232-56*sh;o[i+1]=238-50*sh;o[i+2]=244-40*sh;o[i+3]=v;any=true;};
  for(let x=3;x<W-3;x++){const nx=Math.sin(x*.13/th0)+.8*Math.sin(x*.047/th0+1.3)+.4*Math.sin(x*.31+.4);
    for(let y=4;y<H-1;y++){if(al(x,y)<170||al(x,y-3)>40)continue;
      const flat=(al(x-3,y+2)>120)+(al(x+3,y+2)>120),k=flat===2?1:flat===1?.55:.3,gr=y>gy;
      const th=Math.max(1,(2.6+nx*.9)*th0*k*(gr?3.4:1));
      for(let j=-1;j<=th;j++){const yy=y+j;if(j>=0&&al(x,yy)<100)break;const u=(j+1)/(th+1);put(x,yy,(j<0?.5:1)*(u>.75?(1-u)*4:1)*k*.95,u*.8);}}}
  if(dust){const n1=wxNoise(W,H,38,9,r),n2=wxNoise(W,H,11,4,r),y0=Math.max(4,Math.ceil(gy+6));
    for(let y=y0;y<H-1;y++){const fade=Math.min(1,(y-y0)/18);for(let x=0;x<W-1;x++){const a=al(x,y);if(a<60)continue;const n=n1(x,y)*.72+n2(x,y)*.28,v=clamp((n-.5)/.2,0,1);
      if(v>0)put(x,y,v*v*(3-2*v)*.8*fade*a/255,.25+.5*(1-v));}}}
  if(!any)return null;g.clearRect(0,0,W,H);g.putImageData(img,0,0);return c;}
function wxSnowCv(room,ln){const im=LIMG[room+"_"+ln];if(!im||ln==="sky")return null;
  const o3=(L3[room]||{})[ln]||{},gy=o3.g?o3.g/2:ln==="path"?470:1e9;
  return wxCapCv(im,900,700,ln==="near"?.6:ln==="pool"?.5:1,gy,gy<1e9&&ln!=="pool"&&!(room==="engawa"&&ln==="floor"),room.length*131+ln.length*17);}
// stone lanterns, rocks and pillars of the room (core PROPS) get their own caps, drawn with drawSprite exactly over them
function wxPropSnow(front){if(!wxSnowLies())return;const oD=curD,oR=curRow;
  for(const it of roomThings()){if(!it.prop)continue;const iid=it.imgId||it.id,m=DMETA[iid],im=DIMG[iid];if(!m||!im||!im.width)continue;
    const sid="wx_"+iid;if(!(sid in DIMG)){const f=Math.min(1,600/m[0]),W=Math.max(8,Math.round(m[0]*f)),H=Math.max(8,Math.round(m[1]*f));DIMG[sid]=wxCapCv(im,W,H,2.2*f,1e9,false,iid.length*7)||0;DMETA[sid]=m;}
    if(!DIMG[sid])continue;const P=ipos(it);if(isFront(P)!==front)continue;curD=it.d;curRow=P.y;drawSprite(ctx,sid,P.x,P.y,0,[P.x,P.y],1,P.sc,true);}
  curD=oD;curRow=oR;}
function wxSnowSet(room){let m=wxSC.get(room);if(m)return m;m={};wxSC.set(room,m);if(wxSC.size>3)wxSC.delete(wxSC.keys().next().value);return m;}
// one layer per frame: compute its snow and put a mesh with the same projection right above each of the layer's meshes
function wxSnow3D(){
  if(!G3.on||!wxOut()||!wxSnowLies())return;const name=bgName(),R=G3.rooms[name];if(!R||R.wxDone)return;const L=LAYERS[name];if(!L)return;
  const set=wxSnowSet(name),T=G3.T;R.wxM=R.wxM||[];R.wxL=R.wxL||{};
  const next=L.find(([ln])=>!R.wxL[ln]);if(!next){R.wxDone=1;return;}const [ln,d]=next;R.wxL[ln]=1;
  if(!(ln in set))set[ln]=wxSnowCv(name,ln);const cv=set[ln];if(!cv)return;
  const img=LIMG[name+"_"+ln];let tex=null;
  for(const grp of [R.back,R.front])for(const m of grp.children.slice()){const u=m.material&&m.material.uniforms;if(!u||!u.HV||!u.map||u.map.value.image!==img)continue;
    if(!tex){tex=new T.CanvasTexture(cv);tex.premultiplyAlpha=true;tex.minFilter=T.LinearMipmapLinearFilter;}
    const s=new T.Mesh(m.geometry,new T.ShaderMaterial({uniforms:{map:{value:tex},HV:{value:G3.HV},dark:{value:u.dark.value},ym:{value:u.ym.value}},vertexShader:VS3,fragmentShader:FS3,transparent:true,premultipliedAlpha:true,depthTest:false,depthWrite:false}));
    s.position.copy(m.position);s.rotation.copy(m.rotation);s.renderOrder=m.renderOrder+.5;s.frustumCulled=false;grp.add(s);R.wxM.push(s);}}
function wxSnowVis(){const R=G3.on&&G3.rooms[bgName()];if(!R||!R.wxM)return;const on=wxSnowLies();for(const m of R.wxM)m.visible=on;}
// without WebGL the layers are flat pictures: lay the same caps over them (back layers behind Musya, front ones on top)
function wxSnow2D(front){if(G3.on||!wxOut()||!wxSnowLies())return;const name=bgName(),L=LAYERS[name];if(!L)return;const set=wxSnowSet(name);
  for(const [ln,d] of L){if(front!==(d>CAT_D))continue;if(!(ln in set))set[ln]=wxSnowCv(name,ln);const cv=set[ln];if(!cv)continue;const [ox,oy]=camOff(d);
    ctx.drawImage(cv,BGM.dx+ox,BGM.dy+oy,1800*BGM.k,1400*BGM.k);}}

// ── little things drawn in the room
let wxFly=null;function wxFlyCv(){if(wxFly)return wxFly;const c=document.createElement("canvas");c.width=c.height=32;const g=c.getContext("2d"),gr=g.createRadialGradient(16,16,0,16,16,16);
  gr.addColorStop(0,"rgba(240,255,190,1)");gr.addColorStop(.18,"rgba(214,242,122,.75)");gr.addColorStop(1,"rgba(214,242,122,0)");g.fillStyle=gr;g.fillRect(0,0,32,32);return wxFly=c;}
const wxFlies=Array.from({length:14},()=>({u:Math.random(),v:Math.random(),ph:Math.random()*6}));
function wxPuffs(t){   // breath steam from Musya's mouth in the frost
  if(petAway()||scene.on||["sleep","hide","box","house"].includes(pet.action))return;
  if(t>wxSt.puffT){wxSt.puffT=t+rand(1.6,2.8);const [x,y]=cellToStage(96,110);wxSt.puffs.push({x,y,t0:t,dx:(Math.random()<.5?-1:1)*rand(6,12)});}
  wxSt.puffs=wxSt.puffs.filter(p=>t-p.t0<2);const s=view.s;
  for(const p of wxSt.puffs){const u=(t-p.t0)/2,a=.75*Math.sin(Math.PI*Math.min(1,u*1.6))*(1-u);if(a<=0)continue;
    for(let i=0;i<3;i++){const x=p.x+(p.dx*u*3+i*5*u*Math.sign(p.dx))*s,y=p.y+(4-18*u-i*3)*s,r=(8+22*u+i*3)*s,gr=ctx.createRadialGradient(x,y,0,x,y,r);
      gr.addColorStop(0,`rgba(238,242,246,${a})`);gr.addColorStop(.45,`rgba(238,242,246,${a*.5})`);gr.addColorStop(1,"rgba(238,242,246,0)");ctx.fillStyle=gr;ctx.fillRect(x-r,y-r,r*2,r*2);}}}
const WX_SNAIL={engawa:[1268,.9],courtyard:[1330,.8]};
function wxSnail(t,front){const P=WX_SNAIL[S.room];if(!P||scene.on)return;const iy=P[0];if(front!==(iy>catLineY()+6))return;
  const ix=visX(560+((t*P[1])%520),90),oc=curRow;curRow=iy;const [x,y]=imgToStage(ix,iy,CAT_D),[,y2]=imgToStage(ix,iy-100,CAT_D);curRow=oc;const k=(y-y2)/100,s=k*2.6,w=Math.sin(t*1.3)*.08;
  ctx.save();ctx.translate(x,y);ctx.scale(s,s);ctx.fillStyle="rgba(196,186,160,.95)";ctx.beginPath();ctx.ellipse(2,-2,14+w*10,3.4,0,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle="rgba(196,186,160,.95)";ctx.lineWidth=1.2;ctx.beginPath();ctx.moveTo(13,-3);ctx.lineTo(17,-11);ctx.moveTo(11,-3);ctx.lineTo(13,-10);ctx.stroke();
  const gr=ctx.createRadialGradient(-3,-11,1,-1,-9,9);gr.addColorStop(0,"#d2ae7c");gr.addColorStop(1,"#7a5636");ctx.fillStyle=gr;ctx.beginPath();ctx.arc(-1,-9,8,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle="rgba(40,28,18,.7)";ctx.beginPath();for(let i=0;i<26;i++){const a=i*.5,r=7.5*(1-i/28);ctx.lineTo(-1+Math.cos(a)*r,-9+Math.sin(a)*r);}ctx.stroke();ctx.restore();}
function wxFog(t,a){if(!fogTex)return;const {W,H,s}=view,[ox]=camOff(.5),fw=900*s*1.4,fh=300*s*1.4,off=(((t*14*s)-ox)%fw+fw)%fw;ctx.save();ctx.globalAlpha=a;
  for(let x=-off-fw;x<W;x+=fw){ctx.drawImage(fogTex,x,H*.28,fw,fh);ctx.drawImage(fogTex,x+fw*.4,H*.5,fw,fh*.8);}ctx.restore();}
function wxShimmer(t){const c=ctx.canvas,dpr=view.dpr,{W,H}=view,y0=H*.36,n=26,sh=4;   // heat haze: strips of the frame redrawn with a tiny wobble
  for(let i=0;i<n;i++){const y=y0+i*sh,off=Math.sin(t*2.6+i*.9)*.9*Math.sin(Math.PI*i/n);ctx.drawImage(c,0,Math.round(y*dpr),c.width,Math.round(sh*dpr),off,y,W,sh);}}
const WX_TINT={winter:"rgba(190,205,228,.05)",tsuyu:"rgba(92,98,196,.08)",autumn:"rgba(176,72,28,.06)",summer:"rgba(255,206,128,.04)"};

hook("draw",(t,front)=>{if(!wxOut())return;if(!front)wxSnow2D(false);wxPropSnow(front);
  const s=wxSeason();if(!front&&wxRealK()==="fog")wxFog(t,.45);
  if(s==="tsuyu"&&(weather.on||wxSt.wet||wxRealK()==="rain"))wxSnail(t,front);
  if(front&&s==="winter")wxPuffs(t);});
hook("overlay",t=>{if(!wxOut()||overlaysOpen())return;const s=wxSeason(),night=dayTint()[1],h=hourNow();
  if(!G3.on)wxSnow2D(true);
  if(s==="summer"&&!weather.on){if(night){const im=wxFlyCv(),{W,H}=view;for(const f of wxFlies){const x=W*((f.u+.05*Math.sin(t*.35+f.ph))%1),y=H*(.42+.45*((f.v+.05*Math.sin(t*.45+f.ph*2))%1)),a=.3+.7*Math.max(0,Math.sin(t*1.5+f.ph)),r=10*view.s;
      ctx.globalAlpha=a;ctx.drawImage(im,x-r,y-r,r*2,r*2);}ctx.globalAlpha=1;}
    else if(h>=11&&h<17.5)wxShimmer(t);}
  if(wxRealK()==="fog")wxFog(t,.18);
  const tn=WX_TINT[s];if(tn&&!wxSt.fest){ctx.fillStyle=s==="autumn"&&night?"rgba(150,60,30,.035)":tn;ctx.fillRect(0,0,view.W,view.H);}});
hook("tick",()=>{wxSnow3D();});
hook("room",()=>{wxSt.puffs.length=0;});

// ── the hub card and the city chooser
document.head.insertAdjacentHTML("beforeend","<style>.wx-cities{display:flex;flex-wrap:wrap;gap:8px}.wx-cities .btn{flex:1 1 44%}.story-body .hubc p.wx-now{color:#d9e4ec}</style>");
function wxLine(){const W=wxS(),C=WX_CITY[W.city];if(!C)return"Настоящая погода выключена: дождь приходит сам, когда ему вздумается.";
  const w=wxReal();if(!w)return wxFail?`Погоду ${C[1]} узнать не удалось — пока погода в игре своя.`:`Узнаём, какая погода ${C[1]}…`;
  return`${wxIcon(w)} За окном ${C[1]}: ${wxDeg(w.temp)}, ${WX_TXT[w.code]||"облачно"}`;}
hook("hub",()=>{const s=wxSeason(),A=WX_SEA[s],W=wxS(),C=WX_CITY[W.city],off=S.weather!=="auto"&&C;
  return`<div class="hubc"><h4>${A[2]} Погода и сезон <i>${A[1]}</i></h4><p><b>${A[0]}.</b> ${A[3]}</p><p class="wx-now">${wxLine()}</p>`+
    (off?`<p>Кнопка 🌦 сейчас на «${S.weather==="rain"?"дождь":"ясно"}» — поставь «авто», и в игре будет погода как за окном.</p>`:"")+
    `<div class="row"><button class="btn" data-x="wx:city">📍 ${C?C[0]:"Город за окном"}</button></div></div>`;});
hook("click",k=>{if(!k.startsWith("wx:"))return;
  if(k==="wx:city"){const W=wxS();openPanel("Город за окном",`<p class="lead">Погода в игре будет как за окном в этом городе — когда кнопка 🌦 стоит на «авто».</p><div class="wx-cities">`+
      Object.entries(WX_CITY).map(([id,c])=>`<button class="btn${W.city===id?" primary":""}" data-x="wx:c:${id}">${c[0]}</button>`).join("")+
      `<button class="btn${W.city==="off"?" primary":""}" data-x="wx:c:off">не брать настоящую погоду</button></div>`,"wxcity");return true;}
  if(k.startsWith("wx:c:")){const id=k.slice(5),W=wxS();W.city=WX_CITY[id]?id:"off";wxTry=0;wxFail=0;wxSt.rainWas=null;save();wxFetch(true);toast(WX_CITY[id]?"📍 Погода: "+WX_CITY[id][0]:"Погода снова своя");openHub();return true;}});

// test handle: X.wx.force(code,temp,isDay) fakes a fresh reading for the chosen city
X.wx={sea(v){wxSt.sea=v||null;},st:wxS,real:wxReal,season:wxSeason,fetch:()=>wxFetch(true),snowLies:wxSnowLies,snowFall:wxSnowFall,sc:wxSC,flags:wxSt,
  force(code,temp=5,day=1){const W=wxS();if(!WX_CITY[W.city])W.city="nn";W.w={code,temp,pr:0,sn:0,day,at:Date.now(),city:W.city};wxTry=Date.now();}};
}
