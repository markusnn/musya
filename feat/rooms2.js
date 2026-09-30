{
// ───────── Rooms 2 (idea #10): the tea house 茶室 and the forest shrine 祠 — painted depth layers (art/rooms2_art.py),
// ~30 things each (atlases cha/hok), tray actions: matcha and the scroll; the bell and an offering for the stone foxes.
// The lock system (feat/rooms.js) finds both rooms through ROOMX. State: S.ext.rooms2 {v,bell,fox,gift:{day,id},tea,scroll}
const R2M={"cha":{"kama":[1119,1216],"ro":[1119,1218],"andon":[300,1000],"scroll":[682,196,808,824],"vase":[610,1060],"window":[1190,560,190]},"hok":{"bell":[860,750],"rope":[860,880],"offer":[978,900],"hokora":[750,600,1050,930],"eyes":[[672,876],[1128,876]],"lanterns":[[330,859],[1470,859]],"foxes":[[560,800,720,1102],[1080,800,1240,1102]]},"atlas":{"cha":[1400,1014],"hok":[1400,988]}};
addItems([{"id":"ch_matcha","n":"Чаван со взбитым маття","c":"Чайный домик","w":170,"h":120,"a":"b","p":60,"at":["cha",858,664]},{"id":"ch_ido","n":"Корейский чаван идо","c":"Чайный домик","w":170,"h":120,"a":"b","p":90,"at":["cha",1030,664]},{"id":"ch_egaratsu","n":"Чаван с осенними травами","c":"Чайный домик","w":160,"h":116,"a":"b","p":70,"at":["cha",0,836]},{"id":"ch_pawbowl","n":"Чаван с отпечатком лапки","c":"Чайный домик","w":160,"h":116,"a":"b","p":80,"at":["cha",162,836]},{"id":"ch_chaire","n":"Чайница тяирэ в шёлковом мешочке","c":"Чайный домик","w":170,"h":150,"a":"b","p":90,"at":["cha",232,664]},{"id":"ch_natsume","n":"Нацумэ с золотыми журавлями","c":"Чайный домик","w":130,"h":120,"a":"b","p":110,"at":["cha",1202,664]},{"id":"ch_chasen","n":"Бамбуковый венчик часэн","c":"Чайный домик","w":110,"h":170,"a":"b","p":40,"at":["cha",982,432]},{"id":"ch_chashaku","n":"Ложечка тясяку и её футляр","c":"Чайный домик","w":150,"h":190,"a":"b","p":50,"at":["cha",446,432]},{"id":"ch_kama","n":"Чугунный котёл кама","c":"Чайный домик","w":190,"h":180,"a":"b","p":160,"at":["cha",790,432]},{"id":"ch_furo","n":"Бронзовая жаровня фуро с котлом","c":"Чайный домик","w":230,"h":290,"a":"b","p":240,"at":["cha",528,0]},{"id":"ch_mizusashi","n":"Кувшин для воды мидзусаси","c":"Чайный домик","w":140,"h":200,"a":"b","p":120,"at":["cha",304,432]},{"id":"ch_hishaku","n":"Черпак хисяку на подставке","c":"Чайный домик","w":250,"h":130,"a":"b","p":60,"at":["cha",606,664]},{"id":"ch_kensui","n":"Чаша для слива кэнсуй","c":"Чайный домик","w":160,"h":100,"a":"b","p":40,"at":["cha",818,836]},{"id":"ch_ichigo","n":"Свиток «Одна встреча — одна жизнь»","c":"Чайный домик","w":130,"h":430,"a":"t","p":130,"at":["cha",0,0]},{"id":"ch_hibi","n":"Свиток «Каждый день — хороший день»","c":"Чайный домик","w":130,"h":430,"a":"t","p":130,"at":["cha",132,0]},{"id":"ch_kissako","n":"Свиток «Выпей чаю»","c":"Чайный домик","w":130,"h":430,"a":"t","p":130,"at":["cha",264,0]},{"id":"ch_tsuki","n":"Свиток «Луна и осенние травы»","c":"Чайный домик","w":130,"h":430,"a":"t","p":140,"at":["cha",396,0]},{"id":"ch_tsubaki","n":"Камелия в бамбуковой вазе","c":"Чайный домик","w":120,"h":250,"a":"b","p":80,"at":["cha",872,0]},{"id":"ch_kago","n":"Корзинка с полевыми цветами","c":"Чайный домик","w":180,"h":250,"a":"b","p":90,"at":["cha",994,0]},{"id":"ch_kakebana","n":"Висячая ваза с вьюнком","c":"Чайный домик","w":110,"h":280,"a":"t","p":70,"at":["cha",760,0]},{"id":"ch_wagashi","n":"Вагаси на лаковой тарелке","c":"Чайный домик","w":190,"h":110,"a":"b","p":50,"at":["cha",324,836]},{"id":"ch_higashi","n":"Сухие сладости хигаси","c":"Чайный домик","w":180,"h":90,"a":"b","p":40,"at":["cha",980,836]},{"id":"ch_sensu","n":"Чайный веер сэнсу","c":"Чайный домик","w":170,"h":60,"a":"b","p":30,"at":["cha",0,954]},{"id":"ch_tatami","n":"Половинка татами","c":"Чайный домик","w":300,"h":110,"a":"b","p":60,"at":["cha",516,836]},{"id":"ch_andon","n":"Андон чайного домика","c":"Чайный домик","w":130,"h":250,"a":"b","p":100,"glow":[65,124],"at":["cha",1176,0]},{"id":"ch_teshoku","n":"Свеча на подставке тэсёку","c":"Чайный домик","w":80,"h":220,"a":"b","p":60,"glow":[40,34],"at":["cha",222,432]},{"id":"ch_furosaki","n":"Низкая ширма фуросаки","c":"Чайный домик","w":260,"h":170,"a":"b","p":140,"at":["cha",1094,432]},{"id":"ch_tana","n":"Полочка для утвари","c":"Чайный домик","w":220,"h":230,"a":"b","p":160,"at":["cha",0,432]},{"id":"ch_tetsubin","n":"Чугунный чайник тэцубин","c":"Чайный домик","w":190,"h":190,"a":"b","p":110,"at":["cha",598,432]},{"id":"ch_sumitori","n":"Корзинка для угля с пером","c":"Чайный домик","w":200,"h":150,"a":"b","p":60,"at":["cha",404,664]},{"id":"ch_kogo","n":"Коробочка для благовоний «Кошка»","c":"Чайный домик","w":140,"h":90,"a":"b","p":70,"at":["cha",1162,836]},{"id":"ch_tsukubai","n":"Каменный умывальник цукубай","c":"Чайный домик","w":230,"h":170,"a":"b","p":150,"at":["cha",0,664]},{"id":"hk_torii_moss","n":"Мшистые каменные тории","c":"Святилище","w":240,"h":250,"a":"b","p":150,"at":["hok",578,0]},{"id":"hk_senbon","n":"Коридор красных тории","c":"Святилище","w":280,"h":250,"a":"b","p":200,"at":["hok",820,0]},{"id":"hk_fox_scroll","n":"Лиса со свитком","c":"Святилище","w":170,"h":250,"a":"b","p":150,"at":["hok",1102,0]},{"id":"hk_fox_ine","n":"Лиса с рисовым колосом","c":"Святилище","w":170,"h":250,"a":"b","p":150,"at":["hok",0,302]},{"id":"hk_fox_small","n":"Фарфоровые лисички","c":"Святилище","w":200,"h":130,"a":"b","p":70,"at":["hok",424,746]},{"id":"hk_ema_fox","n":"Стойка с лисьими эма","c":"Святилище","w":250,"h":220,"a":"b","p":70,"at":["hok",952,302]},{"id":"hk_ema_cat","n":"Эма с котёнком","c":"Святилище","w":130,"h":120,"a":"t","p":40,"at":["hok",626,746]},{"id":"hk_omikuji_tree","n":"Деревце с омикудзи","c":"Святилище","w":170,"h":250,"a":"b","p":90,"at":["hok",172,302]},{"id":"hk_saisen","n":"Ящик для подношений с лисьим гербом","c":"Святилище","w":210,"h":160,"a":"b","p":80,"at":["hok",1000,554]},{"id":"hk_gohei_gold","n":"Золотой жезл гохэй","c":"Святилище","w":110,"h":250,"a":"b","p":70,"at":["hok",344,302]},{"id":"hk_toro","n":"Мшистый каменный фонарь","c":"Святилище","w":150,"h":260,"a":"b","p":170,"glow":[75,110],"at":["hok",426,0]},{"id":"hk_suzu","n":"Бубенцы судзу на шнуре","c":"Святилище","w":100,"h":290,"a":"t","p":90,"at":["hok",122,0]},{"id":"hk_heishi","n":"Кувшинчики сакэ хэйси","c":"Святилище","w":140,"h":150,"a":"b","p":50,"at":["hok",1212,554]},{"id":"hk_mochi","n":"Моти-подношение на подставке","c":"Святилище","w":170,"h":180,"a":"b","p":60,"at":["hok",494,554]},{"id":"hk_kitsune_mask","n":"Маска лисы-невесты","c":"Святилище","w":130,"h":180,"a":"t","p":70,"at":["hok",666,554]},{"id":"hk_kakehi","n":"Бамбуковый жёлоб с водой","c":"Святилище","w":260,"h":190,"a":"b","p":120,"at":["hok",0,554]},{"id":"hk_sugi","n":"Саженец криптомерии","c":"Святилище","w":150,"h":250,"a":"b","p":70,"at":["hok",456,302]},{"id":"hk_moss","n":"Мшистые камни","c":"Святилище","w":220,"h":110,"a":"b","p":50,"at":["hok",950,746]},{"id":"hk_iwakura","n":"Священный камень ивакура","c":"Святилище","w":230,"h":190,"a":"b","p":130,"at":["hok",262,554]},{"id":"hk_minihokora","n":"Маленькая хокора","c":"Святилище","w":200,"h":250,"a":"b","p":180,"at":["hok",608,302]},{"id":"hk_aburaage","n":"Абураагэ для лисы","c":"Святилище","w":160,"h":90,"a":"b","p":30,"at":["hok",0,898]},{"id":"hk_inari","n":"Инари-суси на подносе","c":"Святилище","w":180,"h":100,"a":"b","p":40,"at":["hok",1172,746]},{"id":"hk_senbazuru","n":"Гирлянда бумажных журавликов","c":"Святилище","w":120,"h":300,"a":"t","p":60,"at":["hok",0,0]},{"id":"hk_ofuda","n":"Талисман офуда","c":"Святилище","w":70,"h":200,"a":"t","p":30,"at":["hok",1204,302]},{"id":"hk_nobori","n":"Красные флажки Инари","c":"Святилище","w":200,"h":290,"a":"b","p":70,"at":["hok",224,0]},{"id":"hk_fern","n":"Папоротник у камня","c":"Святилище","w":200,"h":170,"a":"b","p":30,"at":["hok",798,554]},{"id":"hk_lantern_fox","n":"Фонарь с лисьим гербом","c":"Святилище","w":110,"h":200,"a":"t","p":60,"glow":[55,110],"at":["hok",1276,302]},{"id":"hk_yomeiri","n":"Фигурки «Лисья свадьба»","c":"Святилище","w":300,"h":150,"a":"b","p":190,"at":["hok",0,746]},{"id":"hk_kagura","n":"Бубенцы кагура с лентами","c":"Святилище","w":140,"h":230,"a":"b","p":80,"at":["hok",810,302]},{"id":"hk_shinsen","n":"Рис, соль и вода для ками","c":"Святилище","w":190,"h":120,"a":"b","p":40,"at":["hok",758,746]},{"id":"hk_kusudama","n":"Бумажный шар кусудама","c":"Святилище","w":120,"h":150,"a":"b","p":50,"at":["hok",302,746]}],{cha:R2M.atlas.cha,hok:R2M.atlas.hok});
DTINT.chashitsu="rgba(34,22,10,.18)";DTINT.hokora="rgba(10,20,16,.3)";
STAMPS.push(["ro2_tea","茶","Первая чашка маття","Завари маття в чайном домике"],["ro2_fox","狐","Угощение для лис","Оставь подношение у святилища"]);
const r2=()=>S.ext.rooms2||(S.ext.rooms2={}),R2={tea:-99,swing:-99,glint:-99,peek:-99,puff:-99,offer:false,cup:null,fire:null,nextFire:now()+20};
const r2btn=(k,i,n,pr="")=>`<button class="item wide" data-x="ro2:${k}"><span class="ico">${i}</span><span class="nm">${n}</span>${pr}</button>`;
addRoom({id:"chashitsu",jp:"茶室",ru:"Чайный домик",label:"Чайная",cat:"Чайный домик",
  hint:"Завари маття — Муся любит смотреть на пар над котлом. А в нише висит свиток: полюбуйся им.",
  layers:[["wall",0.4],["alcove",0.5],["floor",0.8],["near",1.4]],l3:{wall:{g:1140},alcove:{on:"wall",dz:.05},floor:{g:1140},near:{ext:.22}},
  mote:[1,.86,.62],tint:"rgba(22,18,10,.26)",
  tray:()=>r2btn("tea","🍵","Заварить маття")+r2btn("scroll","📜","Полюбоваться свитком")});
addRoom({id:"hokora",jp:"祠",ru:"Святилище",label:"У святилища",cat:"Святилище",outdoor:true,
  hint:"Позвони в колокол и поклонись — раз в день ками дарят маленькое благословение. Лисы любят угощение.",
  layers:[["sky",0.06],["trees",0.22],["shrine",0.45],["floor",0.8],["near",1.5]],l3:{trees:{ext:.35},shrine:{ext:.25},floor:{g:1100}},
  fog:[[14,.45],[8,.3]],tint:"rgba(10,16,14,.3)",
  tray:()=>{if(!R2.offer)return r2btn("bell","🔔","Позвонить и поклониться")+r2btn("offer","🍙","Оставить подношение");
    const own=["i_aburaage",...pantryEats()];
    return r2btn("offer","↩","Назад")+own.map(id=>`<button class="item" data-x="ro2:give:${id}"><span class="ico">${fThumb(id,56,32)}</span><span class="nm">${FOOD[id].n}</span><span class="pr own">${id==="i_aburaage"?"лисам":"×"+S.pantry[id]}</span></button>`).join("");}});

// ── helpers: a point on a painted plane → stage; row = the image y where the thing stands (its depth)
function r2pt(ix,iy,d,row){curD=d;curRow=row??null;const p=imgToStage(ix,iy,d);curD=CAT_D;curRow=null;return p;}
function r2in(x,y,box,d,row){const [ax,ay]=r2pt(box[0],box[1],d,row),[bx,by]=r2pt(box[2],box[3],d,row);return x>=Math.min(ax,bx)&&x<=Math.max(ax,bx)&&y>=Math.min(ay,by)&&y<=Math.max(ay,by);}
function r2glow(x,y,r,rgb,a){if(a<=.003||r<=1)return;const g=ctx.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,`rgba(${rgb},${a})`);g.addColorStop(1,`rgba(${rgb},0)`);ctx.fillStyle=g;ctx.fillRect(x-r,y-r,r*2,r*2);}
function r2steam(x,y,t,k,n,rise,boost){for(let i=0;i<n;i++){const ph=(t*.3*(boost?1.8:1)+i/n)%1,sx=x+Math.sin(t*1.3+i*2+ph*5)*14*k*3*ph,sy=y-ph*rise*k,r=(12+34*ph)*k*2;r2glow(sx,sy,r,"236,234,226",.16*Math.sin(Math.PI*ph)*(boost?1.8:1));}}
function r2sprite(id,x,y,sc,alpha=1){if(!DIMG[id]||!DMETA[id])return;curD=CAT_D;curRow=y;drawSprite(ctx,id,x,y,0,null,alpha,sc,true);curD=CAT_D;curRow=null;}
function r2watch(ix,iy,d,row,sec){if(petAway()||scene.on)return;const [x,y]=r2pt(ix,iy,d,row);pointer.x=x;pointer.y=y;pointer.known=true;pet.gazeUntil=now()+sec;if(pet.action!=="sleep")start("idle");}
const joy=(n,e=0)=>{S.needs.joy=clamp(S.needs.joy+n,0,100);S.needs.energy=clamp(S.needs.energy+e,0,100);};

// ── 茶室: a tiny tea moment — the kettle breathes, a bowl appears on the tatami, the whisk dances, Musya watches
function brew(){const t=now();if(t-R2.tea<7)return;R2.tea=t;const M=R2M.cha;
  r2watch(M.kama[0],M.kama[1]-120,CAT_D,M.kama[1],6);if(!petAway())react("👀",1.4);tone(196,1.2,"sine",.035);
  const ix=(pet.x-BGM.dx)/BGM.k+(pet.x<view.W*.62?150:-150);R2.cup={t:t+1.2,x:visX(ix,70),y:catLineY()+46};
  for(let i=0;i<9;i++)setTimeout(()=>tone(2600+Math.random()*900,.035,"triangle",.012),1500+i*190);
  setTimeout(()=>{const d=r2();d.tea=(d.tea||0)+1;chime([523,659,784]);
    if(petAway()){toast("Маття готов, но Муси нет дома");save();return;}
    react("😻",2.2);joy(10,4);award("ro2_tea");const c=R2.cup;if(c){c.done=now();r2watch(c.x,c.y-40,CAT_D,c.y,4);const [x,y]=r2pt(c.x,c.y-60,CAT_D,c.y);floatFx.push({g:"✨",x,y,t:now()});}
    toast(d.tea===1?"Первая чашка маття — Муся в восторге":"Маття готов — Муся греется у чаши");save();},3700);
}
function admireScroll(){const M=R2M.cha,d=r2(),first=d.scroll!==dayKey();d.scroll=dayKey();
  r2watch((M.scroll[0]+M.scroll[2])/2,480,.5,null,7);chime([392,523,587]);
  const [x,y]=r2pt((M.scroll[0]+M.scroll[2])/2,420,.5);floatFx.push({g:"✨",x,y,t:now()});
  dlg({head:"一期一会 · Итиго итиэ",text:"«Одна встреча — один раз в жизни». Мастера чая заваривают каждую чашку так, будто этот вечер не повторится. Этот вечер с Мусей тоже не повторится.",ok:"Помолчать вместе",
    onOk:()=>{if(petAway())return;react("😌",2.4);if(first){joy(6,6);save();}}});
}
function drawTea(t,front){const M=R2M.cha,k=BGM.k,night=dayTint()[1];
  if(!front){const fl=.88+.08*Math.sin(t*5.1)+.05*Math.sin(t*12.7);
    const [ax,ay]=r2pt(M.andon[0],M.andon[1],CAT_D,1150);r2glow(ax,ay,760*k,"240,180,100",(night?.17:.1)*fl);
    const [rx,ry]=r2pt(M.ro[0],M.ro[1],CAT_D,M.ro[1]);r2glow(rx,ry,150*k,"255,110,40",.2+.07*Math.sin(t*2.3)+.04*Math.sin(t*7.1));
    r2sprite("ch_kama",M.kama[0],M.kama[1],.6);
    const [sx,sy]=r2pt(M.kama[0]+8,M.kama[1]-150,CAT_D,M.kama[1]),brewing=t-R2.tea<4||t-R2.puff<2.5;r2steam(sx,sy,t,k,brewing?7:4,brewing?260:170,brewing);}
  const c=R2.cup;if(!c||t<c.t)return;const age=t-c.t,al=clamp(Math.min(age/.5,(40-age)/2),0,1);if(al<=0){R2.cup=null;return;}
  if((c.y>catLineY()+6)!==front)return;
  r2sprite("ch_matcha",c.x,c.y,.55,al);
  if(!c.done){const [wx,wy]=r2pt(c.x+Math.sin(age*26)*14,c.y-44,CAT_D,c.y),s=k*1.1;ctx.save();ctx.lineCap="round";ctx.strokeStyle="#b8a468";ctx.lineWidth=5*s;ctx.beginPath();ctx.moveTo(wx,wy-78*s);ctx.lineTo(wx,wy-26*s);ctx.stroke();
    ctx.strokeStyle="#ddd0a0";ctx.lineWidth=1.2*s;for(let i=0;i<13;i++){const u=i/12-.5;ctx.beginPath();ctx.moveTo(wx+u*8*s,wy-28*s);ctx.quadraticCurveTo(wx+u*44*s,wy-14*s,wx+u*20*s,wy+6*s);ctx.stroke();}ctx.restore();}
  const [bx,by]=r2pt(c.x,c.y-70,CAT_D,c.y);r2steam(bx,by,t,k*.55,3,150,false);
}

// ── 祠: the bell (a daily blessing), offerings for the stone foxes, lantern flames, rare foxfire at night
const R2VEG=["v_kyuri","v_daikon","v_nasu","v_kabocha","v_imo","v_edamame","v_shiitake","v_negi","v_ichigo"];
function ringBell(){const t=now();if(t-R2.swing<1.4)return;R2.swing=t;const d=r2();
  chime([1568,2093,1760,2349,2093]);setTimeout(()=>{tone(180,.09,"triangle",.07);setTimeout(()=>tone(180,.09,"triangle",.07),240);},1100);
  if(!petAway()){start("hide");react("🙏",2.4);}
  setTimeout(()=>{if(d.bell===dayKey()){toast("Колокол звенит — ками уже слышали тебя");return;}d.bell=dayKey();
    if(Math.random()<.5){const id=pick(R2VEG);give(id);toast(`У ступенек нашлось: ${FOOD[id].n}`);}
    else{joy(12);toast("Тёплый ветер из-за кедров — Муся сияет");}
    if(!petAway())setTimeout(()=>{react("😸",2);burst(6);},900);save();tabDots();},1500);
  qev("place","ro2_bell");
}
function giveFox(id){if(id!=="i_aburaage"&&!have(id))return;take(id);const d=r2(),first=d.fox!==dayKey();d.fox=dayKey();d.gift={day:dayKey(),id};
  R2.offer=false;R2.glint=now();tone(988,.14,"sine",.04);setTimeout(()=>{tone(1318,.09,"triangle",.03);setTimeout(()=>tone(1175,.12,"triangle",.03),130);},600);
  if(!petAway()){react("😸",2.2);joy(first?(id==="ds_inari"||id==="i_aburaage"?16:12):3);}
  award("ro2_fox");toast(first?"Глаза каменных лис блеснули в темноте":"Лисы снова довольны угощением");save();ui();
}
function drawShrine(t,front){if(front)return;const M=R2M.hok,k=BGM.k,night=dayTint()[1];
  M.lanterns.forEach(([lx,ly],i)=>{const fl=.8+.12*Math.sin(t*6.3+i*2)+.08*Math.sin(t*13.1+i),[x,y]=r2pt(lx,ly,CAT_D,1104);r2glow(x,y,190*k,"255,170,80",(night?.24:.12)*fl);r2glow(x,y,22*k,"255,230,170",.5*fl);});
  // the suzu bell and its red-and-white rope swing when rung
  const e=t-R2.swing,a=e<6?.42*Math.sin(e*7.5)*Math.exp(-e*.9):.03*Math.sin(t*1.1),[ax,ay]=r2pt(M.bell[0],M.bell[1]-14,.45),L=150;
  const [ex,ey]=r2pt(M.bell[0]+Math.sin(a)*L,M.bell[1]+Math.cos(a)*L,.45),[bx,by]=r2pt(M.bell[0],M.bell[1],.45),lw=Math.max(2,8*k);
  ctx.save();ctx.lineCap="round";ctx.strokeStyle="#e9e3d6";ctx.lineWidth=lw;ctx.beginPath();ctx.moveTo(bx,by);ctx.lineTo(ex,ey);ctx.stroke();
  ctx.setLineDash([lw*1.1,lw*1.1]);ctx.strokeStyle="#b8302a";ctx.stroke();ctx.setLineDash([]);
  ctx.fillStyle="#b8302a";ctx.beginPath();ctx.ellipse(ex,ey+lw,lw*.9,lw*1.6,0,0,Math.PI*2);ctx.fill();
  const br=17*k,g=ctx.createRadialGradient(bx-br*.35,by-br*.35,br*.1,bx,by,br);g.addColorStop(0,"#fff0b0");g.addColorStop(.5,"#d8a840");g.addColorStop(1,"#6a4a18");
  ctx.fillStyle=g;ctx.beginPath();ctx.arc(bx+Math.sin(a)*br*.6,by,br,0,Math.PI*2);ctx.fill();ctx.restore();
  if(e<1.6)r2glow(bx,by,90*k,"255,220,140",.25*(1-e/1.6));
  // today's offering on the stand; the foxes' eyes glint for a while after it
  const gf=r2().gift;if(gf&&gf.day===dayKey()){const [ox,oy]=r2pt(M.offer[0],M.offer[1]-16,.45);fDraw(ctx,gf.id,ox,oy,58*k);}
  const ge=Math.max(0,5-(t-R2.glint)),pe=Math.max(0,1.4-(t-R2.peek)),gl=Math.min(1,ge)+pe*.5;
  if(gl>0)M.eyes.forEach(([ex2,ey2],i)=>{const [x,y]=r2pt(ex2,ey2,CAT_D,1102),p=gl*(.75+.25*Math.sin(t*9+i));r2glow(x,y,30*k,"255,210,110",.7*p);r2glow(x,y,7*k,"255,250,220",.95*p);});
  // kitsunebi: now and then at night a pale fox-fire drifts between the cedars
  if(night&&!weather.on&&!R2.fire&&t>R2.nextFire)R2.fire={t,x:pick([380,620,1180,1420]),y:rand(700,820)};
  const f=R2.fire;if(f){const u=(t-f.t)/7;if(u>=1){R2.fire=null;R2.nextFire=t+rand(35,70);}else{const [x,y]=r2pt(f.x+u*120*Math.sin(f.x),f.y-u*60+Math.sin(t*2)*12,.45),al=Math.sin(Math.PI*u)*(.7+.3*Math.sin(t*11));r2glow(x,y,40*k,"120,200,255",.35*al);r2glow(x,y,10*k,"220,245,255",.8*al);}}
}

hook("draw",(t,front)=>{if(S.room==="chashitsu")drawTea(t,front);else if(S.room==="hokora")drawShrine(t,front);});
hook("hit",(x,y)=>{
  if(S.room==="chashitsu"){const M=R2M.cha;
    if(r2in(x,y,[M.kama[0]-90,M.kama[1]-170,M.kama[0]+90,M.kama[1]],CAT_D,M.kama[1])){R2.puff=now();tone(262,.5,"sine",.03);if(!petAway())react("😮",1.2);return true;}
    if(r2in(x,y,M.scroll,.5)){admireScroll();return true;}}
  if(S.room==="hokora"){const M=R2M.hok;
    if(r2in(x,y,[M.bell[0]-40,M.bell[1]-30,M.bell[0]+40,M.bell[1]+160],.45)){ringBell();return true;}
    if(M.foxes.some(b=>r2in(x,y,b,CAT_D,1102))){R2.peek=now();tone(1245,.08,"triangle",.03);return true;}
    if(R2.fire){const f=R2.fire,[fx,fy]=r2pt(f.x,f.y,.45);if(Math.hypot(x-fx,y-fy)<60*BGM.k){R2.fire=null;R2.nextFire=now()+rand(35,70);tone(740,.4,"sine",.03);if(!petAway())react("🙀",1.4);return true;}}}
});
hook("click",k=>{if(!k.startsWith("ro2:"))return;const [,a,id]=k.split(":");
  if(a==="tea")brew();else if(a==="scroll")admireScroll();else if(a==="bell")ringBell();else if(a==="offer"){R2.offer=!R2.offer;ui();}else if(a==="give")giveFox(id);return true;});
hook("room",id=>{R2.offer=false;if(id==="chashitsu"||id==="hokora"){const d=r2();if(!d.v){d.v=1;save();}}});
hook("tabDot",r=>r==="hokora"&&r2().v&&r2().bell!==dayKey()&&!hk("tabLock",r));
hook("boot",()=>{for(const id of ["ch_kama","ch_matcha","ch_chasen"])loadItem(id);});
X.rooms2={brew,admireScroll,ringBell,giveFox,M:R2M,st:R2};
}
