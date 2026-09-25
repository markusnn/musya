{id:"yukionna",scary:true,n:"Юки-онна",tag:"雪女 · Снежная женщина",bg:"field",lives:null,time:40,icon:"❄️",
 lore:"Юки-онна — снежная женщина из горных легенд. Она приходит в метель, и её дыхание замораживает насмерть. Лафкадио Хирн записал историю дровосека Минокити, которого она пощадила — с условием молчать.",
 how:"Не дай огню в жаровне погаснуть: касайся тлеющих угольков, чтобы раздуть пламя. Продержись 40 секунд.",
 init(G,t){const S=G.st;S.fire=1;S.embers=[];S.next=t;S.sparks=[];S.flakes=Array.from({length:90},()=>({x:Math.random(),y:Math.random(),s:rand(.6,1.4)}));},
 step(G,t,dt){const S=G.st,el=40-G.time;S.fire=Math.max(0,S.fire-dt*(.075+el*.0035));
   if(t>S.next){S.next=t+Math.max(.35,.7-el*.008);const a=rand(-Math.PI,0);S.embers.push({x:G.W/2+Math.cos(a)*rand(20,70)*G.s,y:G.H*.8+Math.sin(a)*rand(6,26)*G.s,t});}
   S.embers=S.embers.filter(e=>t-e.t<1.5&&!e.hit);for(const f of S.flakes){f.y+=dt*.12*f.s;f.x+=dt*(.04+.05*Math.sin(t+f.s*9));if(f.y>1){f.y=0;f.x=Math.random();}if(f.x>1)f.x-=1;}
   G.score=Math.floor(el);if(S.fire<=0){scare(t);G.lives=0;G.def.lives=null;setTimeout(gEnd,600);S.fire=.0001;}},
 draw(G,g,t){const S=G.st,s=G.s,W=G.W,H=G.H,f=S.fire,near=1-f;
   drawYurei(g,W*(.5+.18*Math.sin(t*.4)),mix(H*.3,H*.02,near),mix(H*.2,H*.95,near),.55+.4*near,near>.45,near>.75);
   g.fillStyle=`rgba(180,200,230,${.15+.25*near})`;g.fillRect(0,0,W,H);
   const bx=W/2,by=H*.8;g.fillStyle="#1d1917";g.beginPath();g.ellipse(bx,by,95*s,30*s,0,0,Math.PI*2);g.fill();g.fillStyle="#2b2522";g.fillRect(bx-95*s,by,190*s,40*s);g.beginPath();g.ellipse(bx,by+40*s,95*s,26*s,0,0,Math.PI);g.fill();
   const gl=g.createRadialGradient(bx,by-10*s,0,bx,by-10*s,(80+220*f)*s);gl.addColorStop(0,`rgba(255,150,60,${.55*f})`);gl.addColorStop(1,"rgba(255,120,40,0)");g.fillStyle=gl;g.fillRect(0,0,W,H);
   for(let i=0;i<5;i++){const x=bx+(i-2)*22*s,hh=(20+60*f)*s*(1+.2*Math.sin(t*9+i));g.fillStyle=`rgba(255,${150+i*15},60,${.35+.5*f})`;g.beginPath();g.moveTo(x-10*s,by);g.quadraticCurveTo(x,by-hh*1.3,x+10*s,by);g.fill();}
   for(const e of S.embers){const a=(t-e.t)/1.5;g.fillStyle=`rgba(255,${120+80*Math.sin(t*12)},40,${1-a})`;g.beginPath();g.arc(e.x,e.y,7*s,0,Math.PI*2);g.fill();}
   for(const sp of S.sparks){const a=(t-sp.t)/.6;if(a<1){g.fillStyle=`rgba(255,200,120,${1-a})`;g.beginPath();g.arc(sp.x,sp.y-a*40*s,2*s,0,Math.PI*2);g.fill();}}
   drawCatG(g,f<.3?"hide":"rest",f<.3?3:0,bx-150*s+(f<.35?Math.sin(t*40)*1.5:0),H-14*s,.5*s);
   g.fillStyle="rgba(240,245,255,.85)";for(const fl of S.flakes){g.beginPath();g.arc(fl.x*W,fl.y*H,1.6*fl.s*s,0,Math.PI*2);g.fill();}},
 down(G,x,y,t){const S=G.st,e=S.embers.find(e=>Math.hypot(e.x-x,e.y-y)<30*G.s);if(e){e.hit=1;S.fire=Math.min(1,S.fire+.13);S.sparks.push({x:e.x,y:e.y,t});tone(300+Math.random()*200,.1,"triangle",.05);}},
 stat:G=>`❄️ ${G.score} с · огонь ${Math.round((G.st.fire||0)*100)}%`},

{id:"hoichi",scary:true,n:"Сутра для Хоити",tag:"耳なし芳一 · Хоити Безухий",bg:"temple",lives:3,time:null,icon:"📿",
 lore:"Слепого певца Хоити каждую ночь уводили петь для призраков погибшего рода Тайра. Чтобы спрятать его от мёртвых, настоятель исписал всё тело Хоити сутрой — но забыл про уши. Призрак-самурай нашёл только уши и унёс их.",
 how:"Покрой Мусю сутрой: касайся каждой светящейся точки, пока не пришёл призрак. Не забудь про уши!",
 spots:[[97,160],[97,100],[132,72],[80,26],[116,26],[158,32],[62,120],[68,182],[126,182]],
 init(G,t){G.st.round=0;this.round(G,t);},
 round(G,t){const S=G.st;S.round++;const n=Math.min(9,3+S.round),body=[0,1,2,3,4,5,6].sort(()=>Math.random()-.5).slice(0,Math.max(1,n-2));S.todo=[...body,7,8].map(i=>({i,done:false}));S.from=t;S.dur=Math.max(3.2,7.5-S.round*.45);S.phase="paint";},
 step(G,t){const S=G.st;if(S.phase==="paint"){if(S.todo.every(q=>q.done)){G.score++;S.phase="ok";S.from=t;sfx("chime");}else if(t-S.from>S.dur){S.phase="lost";S.from=t;S.miss=S.todo.filter(q=>!q.done).map(q=>q.i);hurt(t);}}
   else if(t-S.from>1.2){if(S.round>=8||G.lives<=0){gEnd();return;}this.round(G,t);}},
 draw(G,g,t){const S=G.st,s=G.s,W=G.W,H=G.H,sc=.95*s,cx=W/2,floor=H*.86,p=S.phase==="paint"?clamp((t-S.from)/S.dur,0,1):1;
   drawYurei(g,W*.5,mix(H*.1,-H*.05,p),mix(H*.25,H*.7,p),.25+.4*p,false,false);
   drawCatG(g,"rest",0,cx,floor,sc);
   const pt=i=>{const [x,y]=this.spots[i];return[cx+(x-96)*sc,floor-(y-13)*sc];};
   for(const q of S.todo){const [x,y]=pt(q.i);if(q.done){g.save();g.globalAlpha=.85;jpText(g,"般若",x,y,14*s,"#140f0c");g.restore();}
     else{const pul=.6+.4*Math.sin(t*6+q.i),miss=S.phase==="lost";g.fillStyle=miss?`rgba(220,60,50,${pul})`:`rgba(230,200,110,${.55*pul})`;g.beginPath();g.arc(x,y,(q.i>=7?9:12)*s,0,Math.PI*2);g.fill();}}
   g.fillStyle="rgba(16,21,19,.85)";g.fillRect(16,H*.05,W-32,6);g.fillStyle="#c26a5a";g.fillRect(16,H*.05,(W-32)*(1-p),6);
   if(S.phase==="lost"&&(S.miss||[]).some(i=>i>=7))textC(g,"Уши забыли…",W/2,H*.12,18*s,"#c26a5a","italic 600");},
 down(G,x,y,t){const S=G.st;if(S.phase!=="paint")return;const sc=.95*G.s,cx=G.W/2,floor=G.H*.86;
   for(const q of S.todo){if(q.done)continue;const [sx,sy]=this.spots[q.i],px=cx+(sx-96)*sc,py=floor-(sy-13)*sc;if(Math.hypot(px-x,py-y)<26*G.s){q.done=true;tone(700+q.i*40,.15,"sine",.05);break;}}},
 stat:G=>`📿 ${G.score} · раунд ${G.st.round||0}/8${hearts()}`},

{id:"okiku",scary:true,n:"Тарелки Окику",tag:"番町皿屋敷 · Банчо Сараясики",bg:"temple",lives:3,time:null,icon:"🍽",
 lore:"Служанку Окику обвинили в пропаже одной из десяти драгоценных тарелок и бросили в колодец. Каждую ночь её призрак пересчитывает тарелки — до девяти, — а потом раздаётся страшный крик.",
 how:"Считай тарелки, которые Окику достаёт из колодца, и выбери правильное число.",
 kana:["いちまい","にまい","さんまい","よんまい","ごまい","ろくまい","ななまい","はちまい","きゅうまい","じゅうまい","じゅういち","じゅうに","じゅうさん"],
 init(G,t){G.st.round=0;this.round(G,t);},
 round(G,t){const S=G.st;S.round++;S.count=Math.floor(rand(4,Math.min(13,7+S.round)));S.phase="show";S.from=t+.6;S.step=Math.max(.32,.75-S.round*.05);S.pos=Array.from({length:S.count},()=>[rand(.18,.82),rand(.18,.55)]);S.ans=null;},
 step(G,t){const S=G.st;if(S.phase==="show"&&t-S.from>S.count*S.step+.6){S.phase="ask";S.from=t;const o=new Set([S.count]);while(o.size<4){const v=S.count+Math.floor(rand(-3,4));if(v>0)o.add(v);}S.opts=[...o].sort((a,b)=>a-b);}
   if(S.phase==="show"){const k=Math.floor((t-S.from)/S.step);if(k>=0&&k<S.count&&S.lastK!==k){S.lastK=k;tone(880+k*30,.12,"sine",.04);}}
   if(S.phase==="res"&&t-S.from>1.2){if(S.round>=8||G.lives<=0){gEnd();return;}S.lastK=-1;this.round(G,t);}},
 draw(G,g,t){const S=G.st,s=G.s,W=G.W,H=G.H,wx=W/2,wy=H*.74;
   g.fillStyle="#2e2c28";g.beginPath();g.ellipse(wx,wy,120*s,38*s,0,0,Math.PI*2);g.fill();g.fillStyle="#050606";g.beginPath();g.ellipse(wx,wy,96*s,28*s,0,0,Math.PI*2);g.fill();
   g.fillStyle="#3a3732";g.fillRect(wx-120*s,wy,240*s,60*s);g.fillStyle="#26241f";for(let i=0;i<6;i++)g.fillRect(wx-120*s+i*42*s,wy+2*s,2*s,58*s);
   g.fillStyle="#1f1712";g.fillRect(wx-130*s,wy-190*s,10*s,190*s);g.fillRect(wx+120*s,wy-190*s,10*s,190*s);g.fillRect(wx-150*s,wy-200*s,300*s,16*s);
   const rise=S.phase==="show"?clamp((t-S.from+.6)/.8,0,1):S.phase==="res"&&S.ans!==S.count?1:.4;
   g.save();g.beginPath();g.rect(0,0,W,wy);g.clip();g.fillStyle="#050404";g.beginPath();g.ellipse(wx,wy-rise*60*s,40*s,70*s*rise+4,0,0,Math.PI*2);g.fill();
   for(let i=-5;i<=5;i++){g.beginPath();g.moveTo(wx+i*7*s,wy-rise*120*s);g.quadraticCurveTo(wx+i*14*s,wy-rise*40*s,wx+i*10*s,wy);g.lineWidth=3*s;g.strokeStyle="#050404";g.stroke();}g.restore();
   if(S.phase==="show"){const k=Math.floor((t-S.from)/S.step);for(let i=0;i<S.count;i++){const a=t-S.from-i*S.step;if(a<0||a>S.step*1.4)continue;const al=clamp(Math.min(a/.1,(S.step*1.4-a)/.2),0,1),[px,py]=S.pos[i];
       g.save();g.globalAlpha=al;g.fillStyle="#e9e6dc";g.beginPath();g.ellipse(px*W,py*H,34*s,12*s,0,0,Math.PI*2);g.fill();g.strokeStyle="#2c4a7a";g.lineWidth=3*s;g.beginPath();g.ellipse(px*W,py*H,26*s,8*s,0,0,Math.PI*2);g.stroke();g.restore();}
     if(k>=0&&k<S.count)jpText(g,this.kana[k]||"",W/2,H*.1,20*s,"rgba(216,210,195,.75)");}
   if(S.phase==="ask"||S.phase==="res"){textC(g,"Сколько было тарелок?",W/2,H*.1,18*s);const bw=Math.min(70*s,(W-60)/4),gap=10;S.btn=S.opts.map((v,i)=>({v,x:W/2-(bw*4+gap*3)/2+i*(bw+gap),y:H*.2,w:bw,h:bw*.8}));
     for(const b of S.btn)btnRect(g,b.x,b.y,b.w,b.h,String(b.v),S.phase==="res"&&b.v===S.count);}
   drawCatG(g,S.phase==="res"&&S.ans!==S.count?"hide":"gaze10",S.phase==="res"&&S.ans!==S.count?3:1,W*.16,H-10*s,.45*s);},
 down(G,x,y,t){const S=G.st;if(S.phase!=="ask")return;const b=(S.btn||[]).find(b=>x>=b.x&&x<=b.x+b.w&&y>=b.y&&y<=b.y+b.h);if(!b)return;S.ans=b.v;S.phase="res";S.from=t;
   if(b.v===S.count){G.score++;sfx("chime");}else hurt(t,"yurei");},
 stat:G=>`🍽 ${G.score} · ${G.st.round||0}/8${hearts()}`},

{id:"hyakki",scary:true,n:"Ночной парад",tag:"百鬼夜行 · Хякки яко",bg:"temple",lives:3,time:45,icon:"🏮",
 lore:"Хякки яко — «ночной парад ста демонов»: в особые ночи ёкаи шествуют по улицам, и того, кто их увидит, ждёт беда. Самый известный свиток с парадом нарисован в эпоху Муромати.",
 how:"Собирай онигири касанием. Когда загремят барабаны — зажми кнопку «Спрятаться» и держи, пока парад не пройдёт.",
 init(G,t){const S=G.st;S.items=[];S.next=t+.5;S.parade=null;S.nextParade=t+rand(4,6);S.hide=false;},
 btn(G){const r=46*G.s;return{x:G.W-r-18,y:G.H-r-18,r};},
 step(G,t){const S=G.st,el=45-G.time;
   if(t>S.next&&!S.parade){S.next=t+.75;S.items.push({x:rand(.12,.88)*G.W,y:rand(.3,.62)*G.H,t});}
   S.items=S.items.filter(i=>t-i.t<2.6&&!i.got);
   if(!S.parade&&t>S.nextParade){S.parade={t0:t,warn:1.3,dur:2.8,hit:false};}
   if(S.parade){const p=S.parade,e=t-p.t0;if(e<p.warn&&Math.floor(e*6)!==p.beat){p.beat=Math.floor(e*6);tone(65,.14,"triangle",.14);}
     if(e>p.warn&&e<p.warn+p.dur&&!S.hide&&!p.hit){p.hit=true;hurt(t,"oni");}
     if(e>p.warn+p.dur){S.parade=null;S.nextParade=t+Math.max(2.4,rand(3.5,6.5)-el*.04);}}},
 draw(G,g,t){const S=G.st,s=G.s,W=G.W,H=G.H,p=S.parade,e=p?t-p.t0:0;
   for(const i of S.items){const a=(t-i.t)/2.6;drawEmoji(g,"🍙",i.x,i.y,28*s,Math.min(1,(1-a)*3));}
   if(p){if(e<p.warn){g.fillStyle=`rgba(120,0,0,${.12*Math.abs(Math.sin(e*18))})`;g.fillRect(0,0,W,H);textC(g,"Барабаны!",W/2,H*.12,20*s,"#c26a5a","italic 700");}
     else{const u=(e-p.warn)/p.dur;g.fillStyle="rgba(0,0,0,.45)";g.fillRect(0,0,W,H);const row=["🏮","👹","☂️","👺","🦊","💀","👻","🏮","👹","🐍"];
       row.forEach((m,i)=>{const x=mix(-W*.9,W*1.1,u)+i*44*s,y=H*.48+Math.sin(t*5+i)*8*s;const gr=g.createRadialGradient(x,y,0,x,y,40*s);gr.addColorStop(0,"rgba(200,60,40,.25)");gr.addColorStop(1,"rgba(200,60,40,0)");g.fillStyle=gr;g.fillRect(x-40*s,y-40*s,80*s,80*s);drawEmoji(g,m,x,y,34*s);});}}
   const lx=W*.2,ly=H-16*s;drawCatG(g,S.hide?"hide":"rest",S.hide?3:0,lx,S.hide?ly+30*s:ly,.46*s);
   g.fillStyle="#3a3f3b";g.fillRect(lx+30*s,ly-70*s,44*s,70*s);g.fillStyle="#454b47";g.beginPath();g.moveTo(lx+18*s,ly-70*s);g.lineTo(lx+52*s,ly-94*s);g.lineTo(lx+86*s,ly-70*s);g.fill();
   const b=this.btn(G);g.fillStyle=S.hide?"rgba(238,163,187,.9)":"rgba(16,21,19,.9)";g.strokeStyle="rgba(216,210,195,.4)";g.beginPath();g.arc(b.x,b.y,b.r,0,Math.PI*2);g.fill();g.stroke();textC(g,"Спрятаться",b.x,b.y,11*s,S.hide?"#0d1210":"#d8d2c3",700);},
 down(G,x,y,t){const S=G.st,b=this.btn(G);if(Math.hypot(x-b.x,y-b.y)<b.r+6){S.hide=true;return;}
   if(S.hide)return;const it=S.items.find(i=>Math.hypot(i.x-x,i.y-y)<30*G.s);if(it){it.got=1;G.score++;sfx("coin");}},
 up(G){G.st.hide=false;},
 stat:G=>`🍙 ${G.score}${hearts()} · ${Math.ceil(Math.max(0,G.time))} с`},

