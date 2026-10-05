{
// «Ткацкий станок» (prefix ht): a taka-bata floor loom in the kura. Tap → a hidden full-screen game: pick the warp and weft
// dyes and a traditional pattern, weave 24 rows with rhythmic taps (throw the shuttle — beat with the reed), then sew the
// bolt into a kimono for Musya. One bolt a day (the thread dries overnight). Up to 3 own kimonos; only their parameters
// are saved, the 232×216 kimono cell is rebuilt at boot from assets/wear/ht_base.webp (art/loom_art.py: the shading of
// a white kimono painted by art/wear/kimono.py + where the pattern is sampled on the curved body + region masks),
// multiplied with the woven pattern. The cells are appended to the kimono atlas (DIMG.kimono_atlas becomes a 936×872
// canvas: the bought kimonos on top, ours in a 4th row) and registered in KATLAS.r / WSPR / WEAR.body, so the kimono3d
// block wraps them onto Musya exactly like the bought ones.
const HT_DY=[["ai","Индиго","#2b4573",["синий","синяя","синее","синие"]],["beni","Сафлор","#b42c3c",["алый","алая","алое","алые"]],
  ["kihada","Кихада","#d6ac2c",["жёлтый","жёлтая","жёлтое","жёлтые"]],["sumi","Сажа","#201d20",["чёрный","чёрная","чёрное","чёрные"]],
  ["murasaki","Мурасаки","#5f3b80",["лиловый","лиловая","лиловое","лиловые"]],["cha","Чай","#7b4c2c",["коричневый","коричневая","коричневое","коричневые"]],
  ["shiro","Белый","#ebe5d6",["белый","белая","белое","белые"]],["matcha","Маття","#6a8a3c",["зелёный","зелёная","зелёное","зелёные"]],
  ["sakura","Сакура","#e6a0b3",["розовый","розовая","розовое","розовые"]]];
const HT_D=Object.fromEntries(HT_DY.map(d=>[d[0],d]));
// id, name, kanji, tile w,h, the kimono's noun and its gender (0 m, 1 f, 2 n, 3 pl)
const HT_P=[["asanoha","Асаноха","麻の葉",24,42,"звёзды",3],["seigaiha","Сэйгайха","青海波",26,26,"волны",3],["ichimatsu","Итимацу","市松",24,24,"клетка",1],
  ["yagasuri","Ягасури","矢絣",24,32,"стрелы",3],["kikko","Кикко","亀甲",36,42,"соты",3],["shippo","Сиппо","七宝",20,20,"кольца",3],
  ["kasuri","Касури","絣",48,48,"брызги",3],["shima","Сима","縞",24,24,"полоски",3]];
const HT_PI=Object.fromEntries(HT_P.map(p=>[p[0],p]));
const HT_IDS=["ht_k1","ht_k2","ht_k3"],HT_R={ht_k1:[0,656,232,216],ht_k2:[234,656,232,216],ht_k3:[468,656,232,216]},HT_ROWS=24;
const HT_LOOM={x:1160,w:380,y:1235};   // kura floor, right of Musya, in front of the sake barrels (image px; Musya's line ≈1293)
function htS(){const z=S.ext.loom||(S.ext.loom={k:[],d:"",cl:null,n:0,last:{w:"ai",f:"shiro",p:"seigaiha"},seen:0});z.k=z.k||[];return z;}
const htOpen=()=>!!(ROOMX.kura&&S.ext.rooms&&S.ext.rooms.open&&S.ext.rooms.open.kura);
const htDry=()=>htS().d===dayKey();
const htCv=(w,h)=>{const c=document.createElement("canvas");c.width=w;c.height=h;return c;};
const htRGB=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16));
function htName(c){const p=HT_PI[c.p],d=HT_D[c.w==="shiro"&&c.f!=="shiro"?c.f:c.w],a=d[3][p[6]];return`Кимоно „${a[0].toUpperCase()+a.slice(1)} ${p[5]}“`;}

// ── the woven pattern: one tileable tile per (pattern, warp = ground, weft = figure, seed) ──
function htTile(p,w,f,seed){const P=HT_PI[p],tw=P[3],th=P[4],c=htCv(tw,th),g=c.getContext("2d");g.fillStyle=HT_D[w][2];g.fillRect(0,0,tw,th);
  const F=HT_D[f][2],W=HT_D[w][2],R=rng(seed||1);g.fillStyle=F;g.strokeStyle=F;g.lineCap="round";
  const wrap=fn=>{for(const dx of[-tw,0,tw])for(const dy of[-th,0,th]){g.save();g.translate(dx,dy);fn();g.restore();}};
  const hex=(x,y,r,a0)=>{g.beginPath();for(let k=0;k<6;k++){const a=a0+k*Math.PI/3;g.lineTo(x+Math.cos(a)*r,y+Math.sin(a)*r);}g.closePath();};
  if(p==="ichimatsu")wrap(()=>{g.fillRect(0,0,12,12);g.fillRect(12,12,12,12);});
  else if(p==="shima")wrap(()=>{g.fillRect(0,0,7,th);g.fillRect(11,0,2,th);g.globalAlpha=.55;g.fillRect(17,0,1.2,th);g.globalAlpha=1;});
  else if(p==="yagasuri")wrap(()=>{for(const [x,y] of[[0,16],[12,0]]){g.beginPath();g.moveTo(x,y);g.lineTo(x+6,y+6);g.lineTo(x+12,y);g.lineTo(x+12,y+10);g.lineTo(x+6,y+16);g.lineTo(x,y+10);g.closePath();g.fill();}
    g.globalAlpha=.35;g.fillRect(11.5,0,1,th);g.globalAlpha=1;});
  else if(p==="seigaiha"){for(let r=-2;r<4;r++)for(let c=-1;c<3;c++){const x=c*26+(r&1?13:0),y=r*13;[15,11,7,3].forEach((rad,i)=>{g.fillStyle=i&1?W:F;g.beginPath();g.moveTo(x,y);g.arc(x,y,rad,Math.PI,2*Math.PI);g.closePath();g.fill();});}}
  else if(p==="asanoha")wrap(()=>{g.lineWidth=1.1;const r=24/Math.sqrt(3);for(const [x,y] of[[0,0],[12,21],[24,0],[0,42],[24,42]]){hex(x,y,r,Math.PI/6);g.stroke();
    for(let k=0;k<6;k++){const a=Math.PI/6+k*Math.PI/3;g.beginPath();g.moveTo(x,y);g.lineTo(x+Math.cos(a)*r,y+Math.sin(a)*r);g.stroke();}}});
  else if(p==="kikko")wrap(()=>{for(const [x,y] of[[0,0],[0,21],[18,10.5],[18,31.5],[36,0],[36,21],[0,42],[36,42]]){g.lineWidth=2;hex(x,y,12,0);g.stroke();g.lineWidth=1;hex(x,y,7.4,0);g.stroke();}});
  else if(p==="shippo")wrap(()=>{g.lineWidth=1.5;for(const [x,y] of[[0,0],[20,0],[0,20],[20,20],[10,10]]){g.beginPath();g.arc(x,y,10,0,Math.PI*2);g.stroke();}
    for(const [x,y] of[[10,0],[0,10],[20,10],[10,20]]){g.beginPath();g.arc(x,y,1.6,0,Math.PI*2);g.fill();}});
  else if(p==="kasuri"){const M=[];for(let i=0;i<7;i++)M.push([R()*tw,R()*th,5+R()*6,R()<.25,[R(),R(),R()].map(v=>(v-.5)*2.2)]);
    wrap(()=>{for(const [x,y,l,cr,J] of M){for(let j=0;j<3;j++){const o=(j-1)*1.1,jit=J[j];g.globalAlpha=.85-Math.abs(j-1)*.25;g.fillRect(x-l/2+jit,y+o,l,1.1);}
      if(cr){g.globalAlpha=.8;g.fillRect(x-.7,y-l/2,1.4,l);}g.globalAlpha=1;}});}
  return c;}

// ── the kimono cell: shade × (pattern | obi | cord | obiage | collar | hem lining | juban white) ──
const HT={kim:null,bd:null,atl:null,cell:{},url:{}};
function htParts(k){const W=htRGB(HT_D[k.w][2]),F=htRGB(HT_D[k.f][2]),d=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1],a[2]-b[2]);
  let ob=null,best=-1;for(const id of["beni","sumi","kihada","ai","murasaki","matcha","cha"]){if(id===k.w||id===k.f)continue;const c=htRGB(HT_D[id][2]),v=Math.min(d(c,W),d(c,F));if(v>best){best=v;ob=c;}}
  const cord=htRGB(ob[0]>180&&ob[1]>150?"#b42c3c":"#d8b048"),obiage=F.map(v=>v+(255-v)*.45),eri=W.map(v=>Math.min(255,v*(v<70?1.25:1)+(v<70?8:0)));
  return{ob,cord,obiage,eri,fuki:F.map(v=>v*.85),jub:[242,237,226]};}
function htCell(k){const key=[k.w,k.f,k.p,k.s].join("|");if(HT.cell[k.id]&&HT.cell[k.id].key===key)return HT.cell[k.id].c;
  const D=HT.bd,tile=htTile(k.p,k.w,k.f,k.s),tw=tile.width,th=tile.height,T=tile.getContext("2d").getImageData(0,0,tw,th).data,Q=htParts(k);
  const c=htCv(232,216),g=c.getContext("2d"),out=g.createImageData(232,216),O=out.data,RW=696*4;
  const smp=(s,t,ch)=>{s=((s%tw)+tw)%tw;t=((t%th)+th)%th;const x0=Math.floor(s),y0=Math.floor(t),fx=s-x0,fy=t-y0,x1=(x0+1)%tw,y1=(y0+1)%th;
    const a=T[(y0*tw+x0)*4+ch],b=T[(y0*tw+x1)*4+ch],cc=T[(y1*tw+x0)*4+ch],dd=T[(y1*tw+x1)*4+ch];return(a*(1-fx)+b*fx)*(1-fy)+(cc*(1-fx)+dd*fx)*fy;};
  for(let y=0;y<216;y++)for(let x=0;x<232;x++){const i=y*RW+x*4,a=D[i+3];if(!a)continue;const o=(y*232+x)*4;
    const L=D[i]/255*1.3,s=D[i+1]*352/255-16,t=D[i+2],j=i+928,m=i+1856;
    const cl=D[j]/255,ob=D[j+1]/255,co=D[j+2]/255,oa=D[m]/255,er=D[m+1]/255,fk=D[m+2]/255,rest=Math.max(0,1-cl-ob-co-oa-er-fk);
    const wv=cl?((Math.floor(t*1.5)&1)?.965:1.025):1;
    for(let ch=0;ch<3;ch++){const al=(cl?cl*smp(s,t,ch)*wv:0)+ob*Q.ob[ch]+co*Q.cord[ch]+oa*Q.obiage[ch]+er*Q.eri[ch]+fk*Q.fuki[ch]+rest*Q.jub[ch];
      O[o+ch]=Math.min(255,al*L+Math.max(0,L-1)*(255-al)*.45);}
    O[o+3]=a;}
  g.putImageData(out,0,0);HT.cell[k.id]={key,c};HT.url[k.id]=null;return c;}
const htThumb=id=>{const e=HT.cell[id];if(!e)return"";return HT.url[id]||(HT.url[id]=e.c.toDataURL());};
// the kimono atlas with our cells in a 4th row; kimono3d reads DIMG.kimono_atlas + KATLAS.r[id]
function htCompose(){if(!HT.kim||!HT.bd)return;if(!HT.atl)HT.atl=htCv(936,872);const g=HT.atl.getContext("2d");g.clearRect(0,0,936,872);g.drawImage(HT.kim,0,0);
  for(const k of htS().k){const r=HT_R[k.id];g.drawImage(htCell(k),r[0],r[1]);}
  DIMG.kimono_atlas=HT.atl;const C=X.kimono3d&&X.kimono3d.cache;if(C)for(const key of[...C.keys()])if(key.startsWith("ht_"))C.delete(key);
  if(S.room==="wardrobe"&&S.trayMode.wardrobe!=="decor")ui();}
function htReg(k){KATLAS.r[k.id]=HT_R[k.id];WSPR[k.id]={im:k.id,dx:0,dy:205,w:220};S.owned.add(k.id);const w=WEAR.body.find(q=>q.id===k.id);if(w)w.n=k.n;else WEAR.body.push({id:k.id,n:k.n,p:0});}
function htUnreg(k){const i=WEAR.body.findIndex(q=>q.id===k.id);if(i>=0)WEAR.body.splice(i,1);delete KATLAS.r[k.id];S.owned.delete(k.id);if(S.wear.body===k.id)S.wear.body=null;delete HT.cell[k.id];
  const C=X.kimono3d&&X.kimono3d.cache;if(C)for(const key of[...C.keys()])if(key.startsWith(k.id+":"))C.delete(key);}
for(const k of htS().k)htReg(k);hook("boot",()=>{for(const k of htS().k)htReg(k);});   // again at boot, in case a kimono block re-set KATLAS.r after us
loadWear.kimono_atlas=1;   // we load the bought-kimono atlas ourselves and hand kimono3d the extended canvas
ldImg("assets/wear/kimono.webp",im=>{HT.kim=im;htCompose();});
ldImg("assets/wear/ht_base.webp",im=>{const c=htCv(696,216),g=c.getContext("2d",{willReadFrequently:true});g.drawImage(im,0,0);HT.bd=g.getImageData(0,0,696,216).data;htCompose();});

STAMPS.push(["ht_first","織","Своё кимоно","Сотки ткань на станке в куре и сшей Мусе кимоно"],["ht_three","縫","Три своих кимоно","Сшей Мусе три кимоно своими лапами"],
  ["ht_all","紋","Все узоры","Сотки ткань каждым из восьми узоров"]);
const htSnd={throw(){tone(330,.16,"sine",.025);tone(520,.1,"triangle",.012);},beat(){tone(150,.08,"triangle",.13);tone(96,.12,"sine",.09);setTimeout(()=>tone(210,.05,"triangle",.05),70);}};

// ── the weaving screen ──
const HT_SW=480,HT_SH=800;
function htL(G){const k=Math.min(G.W/HT_SW,G.H/HT_SH);return{k,ox:(G.W-HT_SW*k)/2,oy:(G.H-HT_SH*k)/2};}
function htPatFill(g,tile,sc,x,y,w,h,oy=0){const P=g.createPattern(tile,"repeat");P.setTransform(new DOMMatrix([sc,0,0,sc,x,y+oy]));g.fillStyle=P;g.fillRect(x,y,w,h);}
function htWood(g,x,y,w,h){const gr=g.createLinearGradient(x,y,w>h?x:x+w,w>h?y+h:y);gr.addColorStop(0,"#8a6444");gr.addColorStop(.45,"#5d3f27");gr.addColorStop(1,"#2e1d12");g.fillStyle=gr;g.fillRect(x,y,w,h);}
const HT_SWX=i=>40+i*50,HT_PT=i=>[20+(i%4)*112,452+Math.floor(i/4)*118];
function htTileOf(q){const key=[q.p,q.w,q.f,q.s].join("|");if(q.tk!==key){q.tk=key;q.tile=htTile(q.p,q.w,q.f,q.s);}return q.tile;}
const HT_G={id:"ht_loom",hidden:true,n:"Ткацкий станок",tag:"高機 · Ткацкий станок",bg:"room",lives:null,time:null,icon:"🧵",lore:"",how:"",
 init(G,t){const z=htS(),L=z.last||{};const q=G.st;Object.assign(q,{clk:0,mode:z.cl?"done":"pick",w:L.w||"ai",f:L.f||"shiro",p:L.p||"seigaiha",s:(Math.random()*1e9)|0,
   row:0,ph:0,dir:1,thr:null,beat:-9,last:-9,taps:0,even:0,rep:HT.rep||null,kid:null,thumbs:{}});HT.rep=null;
   if(z.cl){Object.assign(q,z.cl,{row:HT_ROWS});if(!q.rep&&z.k.length>=3)q.rep=z.k[0].id;}G.score=0;},
 step(G,t,dt){G.st.clk+=dt;},
 draw(G,g,t){const q=G.st,{k,ox,oy}=htL(G),c=q.clk;g.save();g.translate(ox,oy);g.scale(k,k);
   g.fillStyle="rgba(10,8,6,.45)";g.fillRect(-ox/k,-oy/k,G.W/k,G.H/k);
   const tile=htTileOf(q),P=HT_PI[q.p];
   if(q.mode==="pick"){textC(g,"Выбери нитки и узор",240,30,20,"#efe3c8",600);
     g.save();g.beginPath();g.roundRect(100,56,280,170,10);g.clip();htPatFill(g,tile,2.2,100,56,280,170);g.fillStyle="rgba(0,0,0,.06)";for(let y=56;y<226;y+=3)g.fillRect(100,y,280,1);
     const v=g.createLinearGradient(100,0,380,0);v.addColorStop(0,"rgba(0,0,0,.28)");v.addColorStop(.5,"rgba(255,255,255,.05)");v.addColorStop(1,"rgba(0,0,0,.3)");g.fillStyle=v;g.fillRect(100,56,280,170);g.restore();
     textC(g,`${P[1]} ${P[2]} · ${HT_D[q.w][1].toLowerCase()} и ${HT_D[q.f][1].toLowerCase()}`,240,246,14,"#d8cdb4",500);
     for(const [row,y,lab] of[["w",292,"Основа — нити вдоль ткани (фон)"],["f",370,"Уток — нить в челноке (узор)"]]){textC(g,lab,240,y-24,13,"#a99f8c",500);
       HT_DY.forEach((d,i)=>{const x=HT_SWX(i),on=q[row]===d[0];g.fillStyle=d[2];g.beginPath();g.arc(x,y+6,on?19:16,0,Math.PI*2);g.fill();g.lineWidth=on?3:1.2;g.strokeStyle=on?"#f3d9a0":"rgba(216,210,195,.35)";g.stroke();});
       textC(g,HT_D[q[row]][1],HT_SWX(HT_DY.findIndex(d=>d[0]===q[row])),y+36,11,"#f3d9a0",600);}
     const D=(S.ext.disc||{}).loom||{};
     HT_P.forEach((p,i)=>{const [x,y]=HT_PT(i),on=q.p===p[0];const tl=q.thumbs[p[0]+q.w+q.f]||(q.thumbs[p[0]+q.w+q.f]=htTile(p[0],q.w,q.f,7));
       g.save();g.beginPath();g.roundRect(x,y,100,74,8);g.clip();htPatFill(g,tl,1.6,x,y,100,74);g.restore();g.lineWidth=on?3:1;g.strokeStyle=on?"#f3d9a0":"rgba(216,210,195,.3)";g.beginPath();g.roundRect(x,y,100,74,8);g.stroke();
       textC(g,(D[p[0]]?"":"• ")+p[1],x+50,y+88,12,on?"#f3d9a0":D[p[0]]?"#d8d2c3":"#eea3bb",on?700:500);});
     const same=q.w===q.f;if(q.rep){const o=htS().k.find(x=>x.id===q.rep);if(o)textC(g,`Освободим место: распустим ${o.n.replace("Кимоно ","")}`,240,712,12,"#eea3bb",500);}
     btnRect(g,150,724,180,50,same?"Нужны разные нити":"Ткать",!same);}
   else{// the loom, front view: warp beam, threads through the heddles and the reed, the cloth growing towards the warp
     const rowH=14,fell=650-q.row*rowH,sh=q.ph===1?9:-9,bt=c-q.beat,sw=bt<.22?Math.sin(bt/.22*Math.PI):0,ry=fell-38+sw*30;
     htWood(g,70,40,22,700);htWood(g,388,40,22,700);htWood(g,60,92,360,22);
     const wg=g.createLinearGradient(0,112,0,136);const W=htRGB(HT_D[q.w][2]);wg.addColorStop(0,`rgb(${W.map(v=>Math.min(255,v+50))})`);wg.addColorStop(1,`rgb(${W.map(v=>v*.55|0)})`);g.fillStyle=wg;g.fillRect(104,114,272,22);
     for(let i=0;i<66;i++){const x=110+i*4,up=(i&1)?sh:-sh;g.strokeStyle=(i&1)?HT_D[q.w][2]:`rgb(${W.map(v=>Math.min(255,v*1.15+14)|0)})`;g.lineWidth=1.5;
       g.beginPath();g.moveTo(x,136);g.lineTo(x,220+up);g.lineTo(x,fell);g.stroke();}
     g.fillStyle="#2e2014";g.fillRect(96,206-9,288,4);g.fillRect(96,230+9,288,4);
     // the woven cloth (rows appear from the breast beam up), the fresh row glows a moment
     if(q.row>0){g.save();g.beginPath();g.rect(108,fell,264,650-fell);g.clip();htPatFill(g,tile,2,108,fell,264,650-fell,650-fell);g.fillStyle="rgba(0,0,0,.07)";for(let y=650;y>fell;y-=rowH/3)g.fillRect(108,y-1,264,1);
       const fr=clamp(1-bt/.6,0,1);if(fr>0){g.fillStyle=`rgba(255,240,200,${.25*fr})`;g.fillRect(108,fell,264,rowH);}
       const sd=g.createLinearGradient(108,0,372,0);sd.addColorStop(0,"rgba(0,0,0,.3)");sd.addColorStop(.5,"rgba(0,0,0,0)");sd.addColorStop(1,"rgba(0,0,0,.3)");g.fillStyle=sd;g.fillRect(108,fell,264,650-fell);g.restore();}
     // the reed (beater) hangs from above and swings to the fell on each beat
     g.strokeStyle="rgba(40,28,18,.8)";g.lineWidth=2;g.beginPath();g.moveTo(98,114);g.lineTo(98,ry);g.moveTo(382,114);g.lineTo(382,ry);g.stroke();
     htWood(g,94,ry-16,292,8);htWood(g,94,ry+6,292,8);g.fillStyle="rgba(30,22,14,.55)";for(let x=100;x<382;x+=4)g.fillRect(x,ry-8,1,14);
     htWood(g,56,650,368,24);
     // the cloth roll under the breast beam
     g.save();g.beginPath();g.roundRect(100,676,280,40,18);g.clip();htPatFill(g,tile,2,100,676,280,40);const rg=g.createLinearGradient(0,676,0,716);rg.addColorStop(0,"rgba(0,0,0,.35)");rg.addColorStop(.35,"rgba(255,255,255,.08)");rg.addColorStop(1,"rgba(0,0,0,.55)");g.fillStyle=rg;g.fillRect(100,676,280,40);g.restore();
     // the shuttle: flies through the open shed, rests at the side
     const th_=q.thr?clamp((c-q.thr.t0)/.32,0,1):1,dir=q.thr?q.thr.dir:-q.dir,sx=q.thr?(dir>0?mix(52,428,smooth(th_)):mix(428,52,smooth(th_))):(q.dir>0?52:428),sy=fell-16;
     g.save();g.translate(sx,sy);g.fillStyle="#8a5a2e";g.beginPath();g.moveTo(-26,0);g.quadraticCurveTo(-12,-7,0,-7);g.quadraticCurveTo(12,-7,26,0);g.quadraticCurveTo(12,7,0,7);g.quadraticCurveTo(-12,7,-26,0);g.fill();
     g.fillStyle=HT_D[q.f][2];g.fillRect(-8,-3,16,6);g.fillStyle="rgba(255,240,210,.35)";g.fillRect(-20,-4,40,1.5);g.restore();
     if(q.thr&&th_<1){g.strokeStyle=HT_D[q.f][2];g.lineWidth=1.4;g.beginPath();g.moveTo(dir>0?108:372,sy);g.lineTo(sx,sy);g.stroke();}
     // Musya watches from the front, the tail twitching with every pass
     const fr_=Math.floor(c*3)%8;drawCatG(g,q.mode==="sewn"?"purr":"rest",fr_,412,790,.5);
     textC(g,`${P[1]} ${P[2]}`,240,22,15,"#efe3c8",600);
     if(q.mode==="weave"){textC(g,`Ряд ${q.row} из ${HT_ROWS}`,240,48,13,"#d8cdb4",500);
       const pulse=.5+.5*Math.cos(c/.55*Math.PI*2);g.fillStyle=`rgba(243,217,160,${.25+.5*pulse})`;g.beginPath();g.arc(120,762,6+3*pulse,0,Math.PI*2);g.fill();
       textC(g,q.ph===0?"Тап — бросить челнок":"Тап — прибить бёрдом",240,762,16,"#efe3c8",600);}
     else if(q.mode==="done"){g.fillStyle="rgba(10,8,6,.55)";g.fillRect(20,150,440,120);textC(g,"Ткань готова!",240,182,22,"#f3d9a0",700);
       textC(g,q.ev>.65?"Легла ровно, нитка к нитке":"Кое-где неровно — зато своими лапами",240,214,14,"#d8cdb4",500);
       const o=q.rep&&htS().k.find(x=>x.id===q.rep);textC(g,o?`Чтобы сшить, распустим ${o.n.replace("Кимоно ","")}`:"Нить сохнет до завтра",240,242,12,o?"#eea3bb":"#a99f8c",500);
       btnRect(g,140,724,200,50,"Сшить кимоно",true);}
     else if(q.mode==="sewn"){const kk=htS().k.find(x=>x.id===q.kid);g.fillStyle="rgba(10,8,6,.8)";g.fillRect(0,0,480,800);
       const e=X.kimono3d&&kk&&IMG.rest?X.kimono3d.build(q.kid,"rest",0):null,sc=1.15,bx=240-192*sc,by=170;
       if(IMG.rest){const gl=g.createRadialGradient(240,400,10,240,400,260);gl.addColorStop(0,"rgba(243,217,160,.22)");gl.addColorStop(1,"rgba(243,217,160,0)");g.fillStyle=gl;g.fillRect(0,120,480,520);
         g.save();g.translate(bx,by);g.scale(sc,sc);g.drawImage(IMG.rest,0,0,384,416,0,0,384,416);if(e)g.drawImage(e.c,e.ox,e.oy);g.restore();}
       textC(g,kk?kk.n:"",240,96,20,"#f3d9a0",700);textC(g,"Сшито! Кимоно ждёт в Гардеробе",240,128,14,"#d8cdb4",500);
       btnRect(g,70,690,160,50,"Надеть",true);btnRect(g,250,690,160,50,"Готово",false);}}
   g.restore();},
 down(G,x,y,t){const q=G.st,{k,ox,oy}=htL(G),X_=(x-ox)/k,Y_=(y-oy)/k,c=q.clk;audioInit();
   if(q.mode==="pick"){for(const [row,yy] of[["w",298],["f",376]])if(Math.abs(Y_-yy)<24){const i=Math.round((X_-40)/50);if(i>=0&&i<HT_DY.length){q[row]=HT_DY[i][0];tone(440+i*40,.12,"sine",.04);}return;}
     for(let i=0;i<HT_P.length;i++){const [px,py]=HT_PT(i);if(X_>px&&X_<px+100&&Y_>py&&Y_<py+96){q.p=HT_P[i][0];q.s=(Math.random()*1e9)|0;tone(520,.1,"triangle",.04);return;}}
     if(Y_>720&&Y_<780&&X_>140&&X_<340&&q.w!==q.f){q.mode="weave";q.row=0;q.ph=0;htS().last={w:q.w,f:q.f,p:q.p};save();sfx("pop");}return;}
   if(q.mode==="weave"){if(c-q.last<.15)return;const gap=c-q.last;if(q.taps&&gap>.3&&gap<.95)q.even++;q.taps++;q.last=c;
     if(q.ph===0){q.ph=1;q.thr={t0:c,dir:q.dir};q.dir*=-1;htSnd.throw();}
     else{q.ph=0;q.beat=c;q.row++;htSnd.beat();if(q.row>=HT_ROWS)htDone(q);}return;}
   if(q.mode==="done"){if(Y_>720&&Y_<780&&X_>140&&X_<340)htSew(q);return;}
   if(q.mode==="sewn"&&Y_>686&&Y_<744){if(X_>70&&X_<230){htWear(q.kid);closeGame();}else if(X_>250&&X_<410)closeGame();}},
 stat:G=>G.st.mode==="weave"?`Ряд ${G.st.row} из ${HT_ROWS}`:"高機 · Ткацкий станок",
 card(){return"";},after(){ui();}};
GAMES.push(HT_G);
function htDone(q){const z=htS();q.ev=q.taps>1?q.even/(q.taps-1):1;z.cl={w:q.w,f:q.f,p:q.p,s:q.s,ev:q.ev};z.d=dayKey();z.n=(z.n||0)+1;q.mode="done";
  chime([523,659,784,1047]);if(disc("loom",q.p)&&HT_P.every(p=>(S.ext.disc.loom||{})[p[0]]))award("ht_all");if(!q.rep&&z.k.length>=3)q.rep=z.k[0].id;save();}
function htSew(q){const z=htS(),c=z.cl;if(!c)return;if(z.k.length>=3){const o=z.k.find(k=>k.id===q.rep)||z.k[0];z.k.splice(z.k.indexOf(o),1);htUnreg(o);}
  const id=HT_IDS.find(i=>!z.k.some(k=>k.id===i)),k={id,w:c.w,f:c.f,p:c.p,s:c.s,n:htName(c),d:dayKey()};z.k.push(k);z.cl=null;htReg(k);htCompose();
  q.mode="sewn";q.kid=id;sfx("chime");award("ht_first");if(z.k.length>=3)award("ht_three");save();}
function htWear(id){if(!id)return;S.wear.body=id;stat("wears",id);qev("wear",{slot:"body",id});save();if(!petAway()){react("😻",2);burst(8);}toast("Муся в новом кимоно");}
function htOpenLoom(){const z=htS();if(!htOpen()){toast("Станок ждёт в запертой куре");return;}if(G.id)return;closePanel();audioInit();z.seen=1;
  if(z.cl){openPlace("ht_loom");return;}
  if(htDry()){toast("Нить сохнет до завтра");if(!petAway())react("😺",1.4);return;}
  if(z.k.length>=3){const o=z.k[0];dlg({head:"Сундук полон",text:`Своих кимоно уже три. Распустить самое старое — ${o.n.replace("Кимоно","кимоно")} — и соткать новое?`,ok:"Распустить и ткать",no:"Не сейчас",onOk:()=>{HT.rep=o.id;openPlace("ht_loom");}});return;}
  openPlace("ht_loom");}

// ── in the kura: the painted loom right of Musya, in front of the barrels ──
let htIm=null;hook("boot",()=>atlasImg("ht",im=>{htIm=im;}));
function htQuad(){if(S.room!=="kura"||!htIm||!htOpen())return null;curRow=null;const x=visX(HT_LOOM.x,HT_LOOM.w/2+16),y=HT_LOOM.y,[x0,y0]=imgToStage(x-HT_LOOM.w/2,y,CAT_D),[x1]=imgToStage(x+HT_LOOM.w/2,y,CAT_D),w=x1-x0,h=w*360/300;return{x:x0,y:y0-h*.96,w,h,iy:y};}
const htWaits=()=>htOpen()&&(!!htS().cl||!htS().seen);
function htDraw(t,front){if(scene.on||front)return;const q=htQuad();if(!q)return;ctx.drawImage(htIm,0,0,300,360,q.x,q.y,q.w,q.h);
  if(htWaits()){const a=.45+.35*Math.sin(t*2.4);drawEmoji(ctx,"✨",q.x+q.w*.55,q.y+q.h*.5-5*Math.sin(t*1.3),16*view.s,Math.max(0,a));}}
// big furniture at the back: draw it before the other add-ons' room things (the hide-and-seek ears behind the barrels stay on top)
hook("draw",htDraw);hook("boot",()=>{const h=HK.draw,i=h.indexOf(htDraw);if(i>0)h.unshift(h.splice(i,1)[0]);});
hook("hit",(x,y)=>{if(scene.on)return;const q=htQuad();if(!q||x<q.x+q.w*.08||x>q.x+q.w*.92||y<q.y+q.h*.05||y>q.y+q.h*.95)return;tone(300,.08,"triangle",.06);htOpenLoom();return true;});
hook("tray",(tray,room)=>{
  if(room==="kura"&&(S.trayMode[room]||"play")==="play"&&htOpen()&&!tray.querySelector('[data-x="ht:open"]')){const b=`<button class="item wide" data-x="ht:open"><span class="ico">🧵</span><span class="nm">${htS().cl?"Сшить кимоно":"Ткацкий станок"}</span></button>`,row=tray.querySelector(".items");
    if(row)row.insertAdjacentHTML("afterbegin",b);}
  if(room==="wardrobe"&&S.wearTab==="body")tray.querySelectorAll('[data-wear^="ht_"]').forEach(b=>{const u=htThumb(b.dataset.wear),ic=b.querySelector(".ico"),pr=b.querySelector(".pr");
    if(ic&&u)ic.innerHTML=`<img src="${u}" alt="" style="width:37px;height:34px">`;if(pr&&S.wear.body!==b.dataset.wear)pr.textContent="соткано";});});
hook("click",k=>{if(!k.startsWith("ht:"))return;closePanel();if(k==="ht:open"){if(!htOpen()){toast("Кура пока заперта");return true;}
  if(S.room!=="kura"){goRoom("kura");setTimeout(htOpenLoom,900);}else htOpenLoom();}return true;});
hook("hubDot",htWaits);hook("tabDot",r=>r==="kura"&&htWaits());
hook("hub",()=>{const z=htS(),D=(S.ext.disc||{}).loom||{},m=HT_P.filter(p=>D[p[0]]).length;
  const st=!htOpen()?"Станок ждёт в запертой куре — сначала открой её":z.cl?"Ткань готова — осталось сшить кимоно":htDry()?"Нить сохнет — завтра можно ткать снова":"Станок в куре ждёт: можно соткать ткань";
  return`<div class="hubc"><h4>🧵 Ткацкий станок <i>高機</i></h4><p>${st}</p><p>Выбери нитки природных красок и узор, сотки ткань в ритм челнока и сшей Мусе кимоно. Одна ткань в день: нить должна высохнуть. Своих кимоно: ${z.k.length} из 3${z.k.length?` (${z.k.map(k=>k.n.replace("Кимоно ","")).join(", ")})`:""}. Узоров испробовано: ${m} из ${HT_P.length}.</p>${htOpen()?`<div class="row"><button class="btn primary" data-x="ht:open">${z.cl?"Сшить кимоно":"К станку"}</button></div>`:""}</div>`;});
hook("album",el=>{const D=(S.ext.disc||{}).loom||{};if(!Object.keys(D).length&&!htS().k.length)return;
  el.insertAdjacentHTML("beforeend",`<h3 class="bh">Ткацкий станок</h3><p class="lead">Узоров: ${HT_P.filter(p=>D[p[0]]).length} из ${HT_P.length}. Своих кимоно: ${htS().k.length}.</p><div class="coll">${HT_P.map(p=>{const on=!!D[p[0]],u=on?htTile(p[0],"ai","shiro",7).toDataURL():"";
    return`<div class="ci${on?" on":""}"${on?"":' style="opacity:.45"'}>${on?`<span style="display:block;width:52px;height:52px;margin:0 auto;border-radius:6px;background:url(${u}) 0 0/${p[3]*1.4}px ${p[4]*1.4}px"></span>`:'<span style="font-size:17px;line-height:52px">？</span>'}<span style="font-size:11px">${on?p[1]:"？？？"}</span></div>`;}).join("")}</div>`);});
X.loom={S:htS,open:htOpenLoom,cell:htCell,compose:htCompose,tile:htTile,HT,
  tap(n=1,gap=.5){for(let i=0;i<n;i++){if(G.id!=="ht_loom")return;G.def.down(G,G.W/2,G.H/2,now());this.ff(gap);}},
  ff(sec){for(let i=0;i<sec*60;i++)G.def.step(G,now(),1/60);},
  pick(w,f,p){Object.assign(G.st,{w,f,p});},
  btn(sx,sy){const {k,ox,oy}=htL(G);G.def.down(G,ox+sx*k,oy+sy*k,now());}};
}
