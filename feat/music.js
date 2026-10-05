{
// ───────────────────────── «Музыка дома» 音楽: quiet procedural Japanese music (WebAudio synth, no audio files) ─────────────────────────
// Moods by room and time: koto (yo) by day, shakuhachi (in-sen) at night, shamisen (miyako-bushi) in the kitchen, a koto lullaby in the
// bedroom at night, taiko + fue at the fair, bell + drone at the shrine; crossfaded on room change. Sparse phrases, long silences, reverb.
// Seven traditional tunes unlock one per visited day (+3 by events); the gramophone (og_gramo) plays the chosen one on tap.
const OG_SC={in:[0,1,5,7,10],yo:[0,2,5,7,9],mi:[0,1,5,7,8]};          // semitones from D: in-sen, yo, miyako-bushi
const OG_VOL=[.06,.12,.2],OG_VN=["тихо","средне","погромче"];
// tunes: notes "A4:1" (quarter = 1 beat), "r:1" rest; i instrument, b seconds per beat, tr transpose (semitones)
const OG_T=[
 {id:"sakura",n:"Сакура, сакура",jp:"さくら さくら",d:"песня эпохи Эдо о вишне в весенней дымке; кото",i:"koto",b:.62,tr:0,
  s:"A4:1 A4:1 B4:2 A4:1 A4:1 B4:2 A4:1 B4:1 C5:1 B4:1 A4:1 B4:.5 A4:.5 F4:2 E4:1 C4:1 E4:1 F4:1 E4:1 E4:.5 C4:.5 B3:2 A4:1 B4:1 C5:1 B4:1 A4:1 B4:.5 A4:.5 F4:2 E4:1 C4:1 E4:1 F4:1 E4:1 E4:.5 C4:.5 B3:2 A4:1 A4:1 B4:2 A4:1 A4:1 B4:2 E4:1 F4:1 B4:.5 A4:.5 F4:1 E4:4"},
 {id:"takeda",n:"Колыбельная Такэда",jp:"竹田の子守唄",d:"песня маленьких нянек из Киото; ночью в спальне Муся под неё засыпает",i:"koto",b:.66,tr:0,soft:1,
  s:"E4:1 G4:.5 A4:1.5 A4:.5 C5:.5 A4:.5 G4:.5 A4:2 C5:1.5 D5:.5 C5:1 A4:1 G4:.5 A4:.5 G4:.5 E4:.5 E4:2 E4:1 G4:.5 A4:1.5 C5:.5 A4:.5 G4:.5 E4:.5 G4:2 A4:1 G4:.5 E4:.5 D4:1 E4:1 D4:1 E4:3"},
 {id:"hotaru",n:"Хотару-кои",jp:"ほたるこい",d:"«Светлячок, лети сюда» — летняя детская песенка; флейта фуэ",i:"fue",b:.5,tr:7,
  s:"G4:1 r:.5 G4:1 r:.5 G4:.5 A4:.5 G4:.5 E4:1.5 A4:.5 A4:.5 G4:.5 A4:.5 C5:.5 A4:.5 G4:1 A4:.5 G4:.5 E4:2 A4:.5 A4:.5 G4:.5 A4:.5 C5:.5 A4:.5 G4:1 A4:.5 C5:.5 A4:2 G4:1 r:.5 G4:1 r:.5 G4:.5 A4:.5 G4:.5 E4:2.5"},
 {id:"kagome",n:"Кагомэ-кагомэ",jp:"かごめかごめ",d:"игра в кругу: «Кто стоит у тебя за спиной?»; сямисэн",i:"sham",b:.42,tr:0,
  s:"A4:.5 A4:.5 G4:1 A4:.5 A4:.5 G4:1 A4:.5 A4:.5 G4:.5 A4:.5 C5:.5 A4:.5 G4:.5 E4:.5 G4:2 A4:.5 A4:.5 G4:.5 A4:.5 C5:.5 A4:.5 G4:1 A4:.5 A4:.5 G4:.5 E4:.5 G4:1 A4:1 C5:.5 C5:.5 A4:.5 C5:.5 D5:.5 C5:.5 A4:.5 G4:.5 A4:2 G4:.5 A4:.5 C5:.5 A4:.5 G4:.5 E4:.5 G4:.5 A4:1.5 r:.5 C5:1 A4:3"},
 {id:"toryanse",n:"Торянсэ",jp:"通りゃんせ",d:"«Пройди, пройди» — узкая тропа к святилищу Тэндзина; кото",i:"koto",b:.55,tr:0,
  s:"A4:1 A4:1 G4:1 A4:2 r:1 A4:1 A4:1 G4:1 A4:2 r:1 G4:.5 G4:.5 A4:.5 G4:.5 E4:.5 G4:.5 A4:1 G4:.5 E4:.5 D4:1 E4:2 C5:.5 C5:.5 A4:.5 C5:.5 A4:.5 G4:.5 A4:1 G4:.5 E4:.5 G4:.5 A4:.5 E4:2 A4:.5 A4:.5 G4:.5 A4:.5 C5:1 A4:1 G4:.5 G4:.5 E4:.5 G4:.5 A4:1 E4:1 G4:.5 A4:.5 G4:.5 E4:.5 D4:1 E4:1 A4:1 A4:1 G4:1 A4:2 r:1 A4:1 A4:1 G4:1 E4:3"},
 {id:"edo",n:"Эдо-комориута",jp:"江戸子守唄",d:"«Нэн-нэн корори-ё» — старая колыбельная Эдо; сякухати",i:"shaku",b:.7,tr:0,soft:1,
  s:"A4:1 A4:1 B4:1 A4:1 F4:1 E4:1 F4:2 A4:1 B4:1 C5:1 B4:.5 A4:.5 A4:2 B4:1 B4:1 A4:1 B4:1 A4:1 F4:.5 E4:.5 E4:2 F4:1 E4:1 C4:1 B3:1 E4:4"},
 {id:"kojo",n:"Кодзё-но цуки",jp:"荒城の月",d:"«Луна над разрушенным замком», Таки Рэнтаро, 1901; сякухати",i:"shaku",b:.72,tr:5,
  s:"E4:1 E4:1 A4:1 B4:1 C5:1 B4:1 A4:2 F4:1 F4:1 E4:1 D4:1 E4:4 E4:1 E4:1 A4:1 B4:1 C5:1 B4:1 A4:2 F4:1 D4:1 E4:1 E4:1 A3:4 C5:1 C5:1 B4:1 A4:1 F4:1 F4:1 E4:2 D4:1 D4:1 E4:1 F4:1 E4:4 E4:1 E4:1 A4:1 B4:1 C5:1 B4:1 A4:2 F4:1 D4:1 E4:1 E4:1 A3:4"}];
const OG_ORD=["sakura","takeda","hotaru","kagome","toryanse","edo","kojo"];
const OG_MOOD={   // generative moods: scale, base Hz (deg 0), degree range, instrument, beat s, rhythm (beats), notes per phrase, rest s, velocity
 day:{sc:"yo",base:293.66,lo:-2,hi:7,k:"koto",beat:.42,rh:[1,1,1,2,2,3,1.5],n:[4,8],rest:[3.5,8],v:.55,n2:"кото — светлый дневной напев"},
 night:{sc:"in",base:293.66,lo:0,hi:6,k:"shaku",beat:.95,rh:[1.2,1.5,2,2.5,3],n:[3,6],rest:[5,11],v:.42,n2:"сякухати — ночная песня бамбука"},
 kitchen:{sc:"mi",base:220,lo:0,hi:8,k:"sham",beat:.3,rh:[1,1,1,2,.5,.5,3],n:[5,8],rest:[3,7],v:.62,n2:"тёплый сямисэн на кухне"},
 lullaby:{sc:"in",base:293.66,lo:-2,hi:5,k:"koto",beat:.75,rh:[1,1,2,2,3],n:[4,6],rest:[6,12],v:.4,lp:1500,n2:"тихая колыбельная кото"},
 fest:{sc:"yo",base:587.33,lo:0,hi:7,k:"fue",beat:.27,rh:[1,1,2,2,1,4],n:[6,10],rest:[4,8],v:.3,n2:"тайко и флейта фуэ"},
 shrine:{n2:"колокол и гул святилища"}};
const M=S.ext.music||(S.ext.music={on:1,v:1,got:[],sel:"",day:"",nw:"",hello:0,lull:0});
const og={c:null,out:null,mix:null,ch:null,mood:"",tune:null,next:0,L:-1,n:0,tq:[],auto:0,fx:0};
const ogT=id=>OG_T.find(x=>x.id===id);
const ogW=(n,f)=>{const a=n%10,b=n%100;return n+" "+(a===1&&b!==11?f[0]:a>=2&&a<=4&&(b<12||b>14)?f[1]:f[2]);};
addItems([{id:"og_gramo",n:"Граммофон",c:"Музыка дома",w:210,h:250,a:"b",p:0,at:["og",0,0],src:"🎵 первая мелодия",hint:"Граммофон появится вместе с первой мелодией дома"}],{og:[210,250]});
STAMPS.push(["og_first","曲","Первая мелодия","Услышь первую мелодию «Музыки дома»"],["og_all","楽","Все мелодии","Собери все семь мелодий «Музыки дома»"]);
document.head.insertAdjacentHTML("beforeend",`<style>
.og-l{display:grid;gap:7px;margin:10px 0 2px}.og-r{display:flex;gap:10px;align-items:center}.og-r .btn{min-width:42px;padding:6px 0;flex:none}
.og-r div{display:flex;flex-direction:column;line-height:1.3}.og-r b{font-weight:600;color:var(--paper);font-size:14px}.og-r span{color:var(--muted);font-size:12px}
.og-r.on b{color:var(--sakura)}.og-r b i{font-style:normal;font-weight:400;color:var(--muted);font-size:12px;margin-left:3px}:is(.story-body .hubc,.card) p.og-s{color:var(--muted);font-size:12.5px}
</style>`);

// ── synth (every voice takes its own context c, so tests can render offline) ──
function ogNoise(c){if(c._ogN)return c._ogN;const b=c.createBuffer(1,c.sampleRate*2,c.sampleRate),d=b.getChannelData(0);for(let i=0;i<d.length;i++)d[i]=Math.random()*2-1;return c._ogN=b;}
function ogIR(c){const sr=c.sampleRate,len=Math.floor(sr*2.8),b=c.createBuffer(2,len,sr);   // a soft wooden-hall reverb: decaying noise, darker towards the tail
  for(let ch=0;ch<2;ch++){const d=b.getChannelData(ch);let lp=0;for(let i=0;i<len;i++){const u=i/len;lp+=((Math.random()*2-1)-lp)*(.18+.6*(1-u));d[i]=lp*Math.pow(1-u,3.2)*Math.min(1,i/(sr*.015));}}return b;}
const ogKS={};
// Karplus–Strong string rendered once per period length: koto (soft, long) or shamisen (bright, short); returns [buffer, playbackRate]
function ogPluck(c,f,kind){const sr=22050,sh=kind==="s",Sx=sh?.3:.5,P=Math.max(6,Math.round(sr/f+Sx)),key=kind+P+"|"+sr;let b=ogKS[key];
  if(!b){const len=Math.floor(sr*(sh?1.3:2.4)),B=c.createBuffer(1,len,sr),d=B.getChannelData(0),buf=new Float32Array(P),rho=sh?.991:.9972;let lp=0,m=0;
    for(let i=0;i<P;i++){lp+=((Math.random()*2-1)-lp)*(sh?.92:.5);buf[i]=lp;m+=lp;}m/=P;for(let i=0;i<P;i++)buf[i]-=m;
    for(let i=0,j=0;i<len;i++){const a=buf[j],nx=buf[j+1===P?0:j+1];d[i]=a;buf[j]=rho*((1-Sx)*a+Sx*nx);j=j+1===P?0:j+1;}
    const fo=Math.floor(sr*.1);for(let i=0;i<fo;i++)d[len-1-i]*=i/fo;b=ogKS[key]=B;}
  return[b,f*(P-Sx)/sr];}
function ogKoto(c,out,t,f,dur,v,o){const sh=o.s,[b,r]=ogPluck(c,f,sh?"s":"k"),s=c.createBufferSource(),lp=c.createBiquadFilter(),g=c.createGain(),pr=s.playbackRate;s.buffer=b;
  pr.setValueAtTime(r*(sh?1.012:1),t);pr.exponentialRampToValueAtTime(r,t+(sh?.05:.02));
  if(o.bend){const k=Math.pow(2,o.bend/12);pr.setValueAtTime(r,t+.2);pr.linearRampToValueAtTime(r*k,t+.45);if(o.back)pr.linearRampToValueAtTime(r,t+.95);}   // oshi: press the string behind the bridge
  lp.type="lowpass";lp.frequency.value=o.lp||(sh?4200:2600);lp.Q.value=.3;const ring=Math.min(b.duration/r,Math.max(dur*1.8,sh?.7:1.6));
  g.gain.setValueAtTime(v*(sh?.9:1.1),t);g.gain.setTargetAtTime(0,t+ring,.18);s.connect(lp);lp.connect(g);g.connect(out);s.start(t);s.stop(t+ring+1);
  if(sh){const n=c.createBufferSource(),hp=c.createBiquadFilter(),ng=c.createGain();n.buffer=ogNoise(c);hp.type="bandpass";hp.frequency.value=2400;hp.Q.value=1.4;   // bachi click
    ng.gain.setValueAtTime(v*.5,t);ng.gain.exponentialRampToValueAtTime(.0001,t+.035);n.connect(hp);hp.connect(ng);ng.connect(out);n.start(t,Math.random());n.stop(t+.05);}}
function ogFlute(c,out,t,f,dur,v,o){v*=.35;const fue=o.fue,a=fue?.07:.24,rel=fue?.16:.42,end=t+Math.max(dur,a+.12),st=end+rel*2.5;   // shakuhachi / fue: sine+triangle, breath, slow vibrato
  const o1=c.createOscillator(),o2=c.createOscillator(),g2=c.createGain(),env=c.createGain(),lfo=c.createOscillator(),lg=c.createGain();o2.type="triangle";g2.gain.value=fue?.3:.16;
  for(const x of [o1,o2]){x.frequency.setValueAtTime(f*(fue?.985:.962),t);x.frequency.exponentialRampToValueAtTime(f,t+(fue?.06:.18));}
  lfo.frequency.value=fue?5.8:4.4;lg.gain.setValueAtTime(0,t);lg.gain.linearRampToValueAtTime(f*(fue?.005:.008),t+Math.min(dur,1));lfo.connect(lg);lg.connect(o1.frequency);lg.connect(o2.frequency);
  const n=c.createBufferSource(),bp=c.createBiquadFilter(),ng=c.createGain();n.buffer=ogNoise(c);n.loop=true;bp.type="bandpass";bp.frequency.value=f*(fue?2:1.6);bp.Q.value=fue?2.2:1.1;
  ng.gain.setValueAtTime(0,t);ng.gain.linearRampToValueAtTime(v*(fue?.22:.55),t+a*.6);ng.gain.setTargetAtTime(v*(fue?.05:.13),t+a,.2);ng.gain.setTargetAtTime(0,end,rel/3);
  env.gain.setValueAtTime(0,t);env.gain.linearRampToValueAtTime(v,t+a);env.gain.setTargetAtTime(v*.8,t+a,.5);env.gain.setTargetAtTime(0,end,rel/3);
  o1.connect(env);o2.connect(g2);g2.connect(env);env.connect(out);n.connect(bp);bp.connect(ng);ng.connect(out);
  for(const x of [o1,o2,lfo])x.start(t);n.start(t,Math.random()*1.5);for(const x of [o1,o2,lfo,n])x.stop(st);}
function ogBell(c,out,t,f,v){for(const [r,a,d] of [[.5,.35,7],[1,1,6],[1.004,.6,6.5],[2.76,.36,3.2],[5.4,.14,1.6],[8.93,.05,.7]]){   // temple bell: hum, beating fundamental, inharmonic partials
  const o=c.createOscillator(),g=c.createGain();o.frequency.value=f*r;g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(v*a*.45,t+.012);g.gain.exponentialRampToValueAtTime(.0001,t+d);o.connect(g);g.connect(out);o.start(t);o.stop(t+d+.05);}}
function ogDrone(c,out,t,f){const g=c.createGain(),lp=c.createBiquadFilter(),L=c.createOscillator(),lg=c.createGain(),os=[L];lp.type="lowpass";lp.frequency.value=360;
  for(const [r,a,ty] of [[1,.5,"sine"],[1.004,.3,"sine"],[1.5,.2,"sine"],[2,.1,"triangle"]]){const o=c.createOscillator(),gg=c.createGain();o.type=ty;o.frequency.value=f*r;gg.gain.value=a;o.connect(gg);gg.connect(lp);o.start(t);os.push(o);}
  L.frequency.value=.07;lg.gain.value=.1;L.connect(lg);lg.connect(g.gain);L.start(t);g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(.3,t+5);lp.connect(g);g.connect(out);
  return{stop(at){for(const o of os)try{o.stop(at);}catch(e){}}};}
function ogTaiko(c,out,t,v,k){v*=.6;const n=c.createBufferSource(),fl=c.createBiquadFilter(),ng=c.createGain();n.buffer=ogNoise(c);
  if(k==="ka"){fl.type="bandpass";fl.frequency.value=2600;fl.Q.value=3;ng.gain.setValueAtTime(v*.6,t);ng.gain.exponentialRampToValueAtTime(.0001,t+.05);n.connect(fl);fl.connect(ng);ng.connect(out);n.start(t,Math.random());n.stop(t+.07);return;}
  const big=k==="don",o=c.createOscillator(),g=c.createGain();o.frequency.setValueAtTime(big?135:330,t);o.frequency.exponentialRampToValueAtTime(big?52:190,t+(big?.32:.1));
  g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(v,t+.004);g.gain.exponentialRampToValueAtTime(.0001,t+(big?.75:.2));o.connect(g);g.connect(out);o.start(t);o.stop(t+.8);
  fl.type="lowpass";fl.frequency.value=big?600:1800;ng.gain.setValueAtTime(v*.35,t);ng.gain.exponentialRampToValueAtTime(.0001,t+.08);n.connect(fl);fl.connect(ng);ng.connect(out);n.start(t,Math.random());n.stop(t+.1);}
function ogPlay(c,out,e){og.n++;const k=e.k,o=e.o||{};
  if(k==="koto")ogKoto(c,out,e.t,e.f,e.d,e.v,o);else if(k==="sham")ogKoto(c,out,e.t,e.f,e.d,e.v,Object.assign({s:1},o));
  else if(k==="shaku")ogFlute(c,out,e.t,e.f,e.d,e.v,o);else if(k==="fue")ogFlute(c,out,e.t,e.f,e.d,e.v,{fue:1});
  else if(k==="bell")ogBell(c,out,e.t,e.f,e.v);else ogTaiko(c,out,e.t,e.v,k);}

// ── generative phrases ──
const ogHz=(m,deg)=>{const sc=OG_SC[m.sc],n=sc.length,o=Math.floor(deg/n),i=((deg%n)+n)%n;return m.base*Math.pow(2,(o*12+sc[i])/12);};
function ogPhrase(m,t0,q,vk=1){const n=m.n[0]+Math.floor(Math.random()*(m.n[1]-m.n[0]+1));let deg=clamp(pick([0,2,3,3,4,5]),m.lo,m.hi),t=t0;
  for(let i=0;i<n;i++){const last=i===n-1;if(last){const ends=[0,3,5].filter(x=>x>=m.lo&&x<=m.hi);deg=ends.reduce((a,b)=>Math.abs(b-deg)<Math.abs(a-deg)?b:a);}
    const dur=(last?Math.max(...m.rh)*1.3:pick(m.rh))*m.beat,o={};if(m.lp)o.lp=m.lp;
    if(m.k==="koto"&&dur>=m.beat*2&&Math.random()<.25){o.bend=pick([1,2]);o.back=Math.random()<.6;}
    q.push({t,k:m.k,f:ogHz(m,deg),d:m.k==="shaku"?dur*1.06:dur,v:m.v*vk*(.85+Math.random()*.3),o});
    if(i===0&&m.k==="koto"&&Math.random()<.5)q.push({t:t+.01,k:"koto",f:ogHz(m,deg)/2,d:dur,v:m.v*vk*.5,o:{lp:1400}});   // a low octave under the first note
    t+=dur;if(!last){let s=pick([-2,-1,-1,-1,1,1,1,2,0]);if(deg+s<m.lo||deg+s>m.hi)s=-s;deg=clamp(deg+s,m.lo,m.hi);}}
  return t;}
function ogGen(ch,w,t0){const q=ch.q,m=OG_MOOD[w];let end=t0;
  if(w==="shrine"){q.push({t:t0,k:"bell",f:pick([293.66,220]),v:.5});if(Math.random()<.3)q.push({t:t0+2.6,k:"bell",f:440,v:.22});og.next=t0+rand(9,16);return;}
  if(w==="lullaby"&&M.got.includes("takeda")&&Date.now()-og.auto>240e3&&Math.random()<.4){og.auto=Date.now();ogTune("takeda","l");return;}
  if(w==="fest"){const P="d..dd.k.d..dk.kk",b8=m.beat,bars=2+Math.floor(Math.random()*2);   // light taiko pattern under a fue phrase
    for(let br=0;br<bars;br++)for(let i=0;i<16;i++){const x=P[i];if(x===".")continue;q.push({t:t0+(br*16+i)*b8,k:x==="d"?"don":"ka",v:x==="d"?(i%8?.32:.45):.22});}
    end=Math.max(t0+bars*16*b8,ogPhrase(m,t0+8*b8,q));}
  else end=ogPhrase(m,t0,q);
  q.sort((a,b)=>a.t-b.t);og.next=end+rand(m.rest[0],m.rest[1]);}
function ogMood(){const r=S.room,n=dayTint()[1];
  return r==="matsuri"?"fest":r==="hokora"?"shrine":r==="kitchen"?"kitchen":r==="bedroom"&&n?"lullaby":r==="chashitsu"||n?"night":"day";}

// ── engine ──
function ogInit(){const c=snd.ctx;if(!c)return false;if(og.c===c)return true;
  try{og.c=c;og.out=c.createGain();og.out.gain.value=0;og.mix=c.createGain();const cv=c.createConvolver(),wet=c.createGain(),lp=c.createBiquadFilter();
    cv.buffer=ogIR(c);wet.gain.value=.45;lp.type="lowpass";lp.frequency.value=5200;og.mix.connect(lp);lp.connect(og.out);og.mix.connect(cv);cv.connect(wet);wet.connect(og.out);og.out.connect(c.destination);}
  catch(e){og.c=null;return false;}
  og.next=c.currentTime+2.5;ogDaily();return true;}
function ogChan(){const g=og.c.createGain();g.gain.value=0;g.connect(og.mix);return{g,q:[],drone:null};}
function ogRetire(ch,tc=.7){if(!ch||!og.c)return;const t=og.c.currentTime;ch.q.length=0;ch.g.gain.cancelScheduledValues(t);ch.g.gain.setTargetAtTime(0,t,tc);if(ch.drone)ch.drone.stop(t+tc*7);
  setTimeout(()=>{try{ch.g.disconnect();}catch(e){}},tc*8000+600);}
function ogLevel(){if(!snd.on||document.hidden)return 0;let v=OG_VOL[M.v]??.12;if(scene.on||!$("game").hidden)v*=.3;if(snd.cur)v*=.4;return v;}   // duck under games, story scenes, purr/snore
function ogFeed(ch,ct){const q=ch.q;while(q.length&&q[0].t<ct+.4){const e=q.shift();if(e.t<ct-.05)continue;try{ogPlay(og.c,ch.g,e);}catch(err){}}}
function ogRun(){if(!ogInit())return;const c=og.c,ct=c.currentTime,L=ogLevel();
  if(Math.abs(L-og.L)>.001){og.out.gain.cancelScheduledValues(ct);og.out.gain.setTargetAtTime(L,ct,L<og.L?.15:.6);og.L=L;}
  if(c.state!=="running"||!L)return;
  if(!M.hello&&M.on){M.hello=1;og.tq.unshift(["🎵 В доме тихо играет музыка — выключить можно в 家"]);save();}
  const T=og.tune;if(T){ogFeed(T.ch,ct);if(ct>T.end){ogRetire(T.ch,.5);og.tune=null;og.next=ct+3;}}
  const w=og.tune||!M.on?"":ogMood();
  if(w!==og.mood){ogRetire(og.ch,.8);og.ch=null;og.mood=w;if(w){const ch=og.ch=ogChan();ch.g.gain.setValueAtTime(0,ct);ch.g.gain.linearRampToValueAtTime(1,ct+2.5);og.next=Math.max(og.next,ct+.8);
    if(w==="shrine")ch.drone=ogDrone(c,ch.g,ct,73.42);}}
  if(og.ch){if(!og.ch.q.length&&ct+.5>=og.next)ogGen(og.ch,w,Math.max(ct+.05,og.next));if(og.ch)ogFeed(og.ch,ct);}}
function ogTune(id,src="h"){if(!ogInit())return false;const T=ogT(id);if(!T)return false;ogStop(1);
  const c=og.c,ct=c.currentTime,ch=ogChan(),t0=ct+.5,k=T.i,vk=src==="l"?.7:1;ch.g.gain.setValueAtTime(1,ct);
  for(const [b,m,d] of ogParse(T))ch.q.push({t:t0+b*T.b,k,f:440*Math.pow(2,(m-69)/12),d:d*T.b*(k==="shaku"||k==="fue"?.97:1),v:(k==="koto"?.62:k==="sham"?.55:k==="fue"?.32:.48)*vk*(.92+Math.random()*.12),o:T.soft&&k==="koto"?{lp:1900}:{}});
  ogRetire(og.ch,.6);og.ch=null;og.mood="";og.tune={id,ch,t0,end:t0+T.len*T.b+2.5,src,slept:0};return true;}
function ogStop(q){const T=og.tune;if(!T)return;ogRetire(T.ch,q?.25:.4);og.tune=null;if(og.c)og.next=og.c.currentTime+2.5;}
function ogParse(T){if(T.ev)return T.ev;const ev=[],PC={C:0,D:2,E:4,F:5,G:7,A:9,B:11};let b=0;
  for(const tok of T.s.trim().split(/\s+/)){const [nm,du]=tok.split(":"),d=+du;if(nm!=="r"){const m=/^([A-G])(b|#)?(\d)$/.exec(nm);ev.push([b,12*(+m[3]+1)+PC[m[1]]+(m[2]==="b"?-1:m[2]==="#"?1:0)+(T.tr||0),d]);}b+=d;}
  T.len=b;return T.ev=ev;}
const ogTuneLen=T=>(ogParse(T),T.len*T.b);

// ── collection ──
function ogGot(id){if(M.got.includes(id))return false;M.got.push(id);M.nw=id;if(!M.sel)M.sel=id;disc("music",id);S.owned.add("og_gramo");
  const first=M.got.length===1,all=M.got.length>=OG_T.length;og.tq.push([`🎵 Новая мелодия: «${ogT(id).n}»`,()=>{if(first)award("og_first");if(all)award("og_all");}]);save();
  if(panelIs("hub"))openHub();return true;}
function ogDaily(){if(M.day===dayKey())return;M.day=dayKey();const nx=OG_ORD.find(id=>!M.got.includes(id));if(nx)ogGot(nx);else save();}
function ogStatus(){if(!M.on)return"Музыка выключена";if(!snd.on)return"Музыка молчит: звук игры выключен 🔇";if(!og.c)return"Музыка заиграет от первого касания";
  if(og.tune)return`Сейчас играет: «${ogT(og.tune.id).n}»`+(og.tune.src==="g"?" · граммофон":"");return"Сейчас играет: "+OG_MOOD[ogMood()].n2;}
function ogNotes(){const q=S.placed&&S.placed.og_gramo;if(!q||q.r!==S.room||overlaysOpen()||!DMETA.og_gramo)return;
  const it=ipos({id:"og_gramo",x:q.x,y:q.y,item:true});curD=DECOR_D.og_gramo??CAT_D;curRow=it.y;const [x0,y0,w,h]=spriteBox(it),[sx,sy]=imgToStage(x0+w*.32,y0+h*.14);curD=CAT_D;curRow=null;
  floatFx.push({g:++og.fx%2?"♪":"♫",x:sx+rand(-16,16)*view.s,y:sy+rand(-6,6)*view.s,t:now()});}
function ogLullaby(){const T=og.tune;if(!T||T.id!=="takeda"||T.slept||!og.c)return;if(og.c.currentTime<T.t0+ogTuneLen(ogT("takeda"))*.55)return;T.slept=1;
  if(S.room!=="bedroom"||!dayTint()[1]||petAway()||scene.on||overlaysOpen()||pet.action!=="idle"||Date.now()-M.lull<20*60e3)return;
  M.lull=Date.now();start("sleep");pet.napUntil=now()+rand(45,75);save();}

// ── hooks ──
hook("tick",()=>{try{ogRun();}catch(e){}});
hook("sec",()=>{if(!og.c)return;ogDaily();ogLullaby();if(og.tune&&og.c.currentTime>og.tune.t0)ogNotes();
  if(og.tq.length&&!$("toast").classList.contains("on")&&!scene.on){const [tx,fn]=og.tq.shift();toast(tx);if(fn)setTimeout(fn,2100);}});
document.addEventListener("visibilitychange",()=>{if(!og.c)return;const ct=og.c.currentTime;og.out.gain.cancelScheduledValues(ct);
  if(document.hidden){og.out.gain.setValueAtTime(0,ct);og.L=0;}else{og.L=-1;og.next=Math.max(og.next,ct+2);}});
hook("ev",(e,d)=>{if(e==="lamp"&&d&&dayTint()[1])ogGot("takeda");});
hook("room",id=>{if(id==="matsuri")ogGot("kagome");else if(id==="hokora")ogGot("toryanse");});
hook("itemTap",it=>{if(it.id!=="og_gramo")return;audioInit();
  if(!snd.on){toast("🔇 Звук игры выключен — включи 🔈");return true;}
  if(og.tune&&og.tune.src==="g"){ogStop();toast("🎵 Граммофон затих");return true;}
  const id=M.got.includes(M.sel)?M.sel:M.got[0];if(!id){toast("🎵 Пока нет ни одной пластинки");return true;}
  if(ogTune(id,"g")){toast(`🎵 Граммофон: «${ogT(id).n}»`);if(!petAway()&&pet.action==="idle")react("🎶",1.6);}return true;});
hook("click",k=>{if(!k.startsWith("og:"))return;audioInit();
  if(k==="og:tog"){M.on=M.on?0:1;if(!M.on)ogStop();toast(M.on?"🎵 Музыка снова играет":"🎵 Музыка выключена");}
  else if(k==="og:vol")M.v=(M.v+1)%3;
  else if(k.startsWith("og:p:")){const id=k.slice(5);if(og.tune&&og.tune.id===id)ogStop();else{M.sel=id;if(!snd.on)toast("🔇 Звук игры выключен — включи 🔈");else ogTune(id,"h");}}
  save();if(panelIs("hub"))openHub();return true;});
hook("hub",()=>{M.nw="";const got=OG_T.filter(T=>M.got.includes(T.id)),left=OG_T.length-got.length,pl=og.tune&&og.tune.id;
  return`<div class="hubc"><h4>🎵 Музыка дома <i>音楽</i></h4><p>${ogStatus()}</p>
<p class="og-s">Днём — кото, ночью — сякухати, на кухне — сямисэн, в спальне — колыбельная, на ярмарке — тайко и флейта, в святилище — колокол. Каждый день в доме открывается новая мелодия. Граммофон из «🧺 Вещи» играет выбранную.</p>
<div class="row"><button class="btn${M.on?"":" primary"}" data-x="og:tog">${M.on?"Выключить":"Включить музыку"}</button><button class="btn" data-x="og:vol">Громкость: ${OG_VN[M.v]}</button></div>
<div class="og-l">${got.map(T=>`<div class="og-r${M.sel===T.id?" on":""}"><button class="btn${pl===T.id?" primary":""}" data-x="og:p:${T.id}">${pl===T.id?"■":"▶"}</button><div><b>${T.n} <i>${T.jp}</i></b><span>${T.d}</span></div></div>`).join("")}</div>
${left?`<p class="og-s">${left===OG_T.length?"Первая мелодия зазвучит, как только в доме заиграет музыка":"Ещё "+ogW(left,["мелодия откроется","мелодии откроются","мелодий откроются"])+" в следующие дни"}</p>`:""}</div>`;});
hook("hubDot",()=>!!M.nw);
hook("album",el=>{el.insertAdjacentHTML("beforeend",`<h3 class="bh">Музыка дома</h3><p class="lead">Мелодий: ${M.got.length} из ${OG_T.length}. Их играет граммофон.</p><div class="coll">${OG_T.map(T=>{const on=M.got.includes(T.id);
  return`<div class="ci${on?" on":""}"${on?"":' style="opacity:.45"'}><span style="font-size:20px;line-height:52px">${on?"🎵":"？"}</span><span style="font-size:11px">${on?T.n:"???"}</span></div>`;}).join("")}</div>`);});

// ── test handles ──
X.og={M,st:()=>({c:!!og.c,state:og.c&&og.c.state,mood:og.mood,tune:og.tune&&og.tune.id,n:og.n,L:+og.L.toFixed(3),q:og.ch&&og.ch.q.length,got:M.got.slice(),status:ogStatus(),tq:og.tq.length}),
  tune:ogTune,stop:ogStop,got:ogGot,mood:ogMood,len:id=>+ogTuneLen(ogT(id)).toFixed(1),
  // estimate the pitch of one synth note offline (autocorrelation) → X.og.res
  pitch(f,k="koto"){const sr=22050,c=new OfflineAudioContext(1,sr,sr);ogPlay(c,c.destination,{t:0,k,f,d:.9,v:.6,o:{}});X.og.res=null;
    c.startRendering().then(b=>{const d=b.getChannelData(0).slice(sr*.25|0,sr*.65|0);let best=0,bl=0;for(let L=Math.floor(sr/2000);L<sr/60;L++){let s=0;for(let i=0;i+L<d.length;i++)s+=d[i]*d[i+L];if(s>best){best=s;bl=L;}}
      let y0=0,y1=0,y2=0;for(let i=0;i+bl+1<d.length;i++){y0+=d[i]*d[i+bl-1];y1+=d[i]*d[i+bl];y2+=d[i]*d[i+bl+1];}const off=(y0-y2)/(2*(y0-2*y1+y2)||1);
      X.og.res={f,k,est:+(sr/(bl+off)).toFixed(1)};});},
  // render a tune (or a mood phrase) offline → peak / rms, to check the synth without speakers
  render(id,sec=8){const sr=22050,c=new OfflineAudioContext(2,sr*sec,sr),out=c.createGain(),cv=c.createConvolver(),wet=c.createGain();cv.buffer=ogIR(c);wet.gain.value=.45;out.connect(c.destination);out.connect(cv);cv.connect(wet);wet.connect(c.destination);
    const q=[];if(ogT(id)){const T=ogT(id);for(const [b,m,d] of ogParse(T))if(b*T.b<sec-1)q.push({t:.1+b*T.b,k:T.i,f:440*Math.pow(2,(m-69)/12),d:d*T.b,v:.6,o:{}});}
    else if(id==="shrine"){q.push({t:.1,k:"bell",f:293.66,v:.5});ogDrone(c,out,0,73.42);}else{const ch={q};og.next=0;ogGen(ch,id,.1);}
    for(const e of q)ogPlay(c,out,e);X.og.res=null;c.startRendering().then(b=>{let pk=0,s=0,nan=0;for(let ch=0;ch<2;ch++){const d=b.getChannelData(ch);for(let i=0;i<d.length;i++){const v=d[i];if(v!==v)nan++;else{pk=Math.max(pk,Math.abs(v));s+=v*v;}}}
      X.og.res={id,notes:q.length,peak:+pk.toFixed(3),rms:+Math.sqrt(s/(2*sr*sec)).toFixed(4),nan};});}};
}
