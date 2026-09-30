{
// Volumetric kimono. art/wear/kimono.py paints each kimono per pixel onto a body model measured from the sitting frames
// (cell = frame px 84..316 × 176..392, 1:1). Here, once per (kimono, strip, frame): the cell is fitted to the frame,
// cut by the kitten's own eroded alpha (the fur fringe stays on top), shaded at the real contour (inner rim shadow,
// head and paw shadows), then the head, raised paws, tail and knead cushion are cut out so they stay in front. Cached.
const K3={x:84,y:176,w:232,h:216,max:24};
Object.assign(KATLAS,{w:936,h:654,r:{k_sakura:[0,0,232,216],k_seigaiha:[234,0,232,216],k_tsuru:[468,0,232,216],k_asagao:[702,0,232,216],k_momiji:[0,218,232,216],k_yagasuri:[234,218,232,216],k_ichimatsu:[468,218,232,216],k_kiku:[702,218,232,216],k_asanoha:[0,436,232,216],k_hotaru:[234,436,232,216],k_fuji:[468,436,232,216],k_miko:[702,436,232,216]}});
// body shift of each frame against the model (median body centre, rows 268..306)
const K3DX={rest:[0,2,1,2,0,1,2,1],purr:[-2,1,-1,0,0,2,0,0],treat:[0,1,4,0,0,2,3,3],highfive:[2,2,-1,0,0,2,-2,0],knead:[-1,1,-1,-1,-1,4,-3,0],groom:[0,4,0,-2,-2,-1,0,-4],gaze9:[0,0,0,0,0,-2,0,-2],gaze10:[-2,0,1,0,0,0,1,0]};
// raised paws that stay in front of the cloth: [cx,cy,rx,ry] in frame px
const K3PAW={treat:{0:[133,240,26,24],1:[135,180,22,22],2:[150,190,20,22],3:[133,268,26,24]},
  highfive:{1:[150,250,26,26],2:[125,205,22,26],3:[148,195,24,24],4:[125,160,26,32],5:[135,170,26,30],6:[152,238,26,26]},
  groom:{1:[150,254,24,24],2:[146,238,24,28],3:[198,200,22,26],4:[228,170,22,24],5:[238,165,22,22],6:[146,272,24,24]}};
const K3TAIL=[[222,372],[228,357],[250,347],[280,330],[299,318],[316,325],[323,350],[317,373],[297,389],[250,393],[220,391]];
const K3KNEAD=[[[293,262],[320,252],[350,280],[352,332],[338,368],[300,368],[293,322]],   // tail
  [[0,416],[0,322],...Array.from({length:25},(_,i)=>[i*16,313+((i*16-192)/100)**2*9]),[384,416]]];   // cushion in front of the lap
const k3cache=new Map();let k3out=null;
function k3cv(w,h){const c=document.createElement("canvas");c.width=w;c.height=h;return c;}
// head ellipse from the detected eyes, else from the crown anchor
function k3head(st,f){const E=EYES[st]&&EYES[st][f];if(E){const d=Math.hypot(E[2]-E[0],E[3]-E[1]);return[(E[0]+E[2])/2,(E[1]+E[3])/2,1.33*d,.9*d,Math.atan2(E[3]-E[1],E[2]-E[0])];}
  const A=ANCH[st][f];return[A[0]*2,A[1]*2+64,76,52,0];}
function k3soft(q,cx,cy,rx,ry,a,col,fe){q.save();q.translate(cx,cy);q.rotate(a);q.scale(rx,ry);const gr=q.createRadialGradient(0,0,0,0,0,1);gr.addColorStop(0,col);gr.addColorStop(Math.max(0,1-fe),col);gr.addColorStop(1,"rgba(0,0,0,0)");q.fillStyle=gr;q.beginPath();q.arc(0,0,1,0,Math.PI*2);q.fill();q.restore();}
function k3poly(q,pts){q.beginPath();pts.forEach(([x,y],i)=>i?q.lineTo(x,y):q.moveTo(x,y));q.closePath();q.fill();}
function k3build(id,st,f){
  const im=DIMG.kimono_atlas,fr=IMG[st],r=KATLAS.r[id];if(!im||!fr||!r)return null;
  const dx=(K3DX[st]||[])[f]||0,ox=K3.x-4+dx,oy=K3.y,c=k3cv(K3.w+8,K3.h),q=c.getContext("2d");q.translate(-ox,-oy);
  q.drawImage(im,r[0],r[1],r[2],r[3],K3.x+dx,K3.y,r[2],r[3]);
  // cloth only inside the fur silhouette, eroded ~2px so fur tufts show at the contour
  q.globalCompositeOperation="destination-in";for(const [ex,ey] of[[-2,0],[2,0],[0,-2],[0,2]])q.drawImage(fr,f*384,0,384,416,ex,ey,384,416);
  // shading at the real contour: inner shadow from the outside of the silhouette (light from the upper left)
  if(!k3out)k3out=k3cv(384,416);const o=k3out.getContext("2d");o.globalCompositeOperation="source-over";o.clearRect(0,0,384,416);o.fillStyle="#000";o.fillRect(0,0,384,416);
  o.globalCompositeOperation="destination-out";o.drawImage(fr,f*384,0,384,416,0,0,384,416);
  q.globalCompositeOperation="source-atop";q.save();q.shadowColor="rgba(8,6,12,.62)";q.shadowBlur=9;q.shadowOffsetX=-3;q.shadowOffsetY=2;q.drawImage(k3out,0,0);q.restore();
  const [hx,hy,hrx,hry,ha]=k3head(st,f),paw=(K3PAW[st]||{})[f];
  k3soft(q,hx+5,hy+hry*.9+6,hrx*.74,hry*.5,ha,"rgba(10,6,10,.5)",.9);                    // the head's shadow on the collar
  if(paw)k3soft(q,paw[0]+4,paw[1]+6,paw[2]*1.05,paw[3]*1.05,0,"rgba(10,6,10,.42)",.6);    // the paw's shadow on the cloth
  // what stays in front of the kimono
  q.globalCompositeOperation="destination-out";k3soft(q,hx,hy,hrx,hry,ha,"#000",.12);if(paw)k3soft(q,paw[0],paw[1],paw[2],paw[3],0,"#000",.2);
  q.fillStyle="#000";q.shadowColor="#000";q.shadowBlur=3;for(const p of st==="knead"?K3KNEAD:[K3TAIL])k3poly(q,p);
  return {c,ox,oy};}
hook("drawBody",(g,st,f,k,id)=>{
  if(!KATLAS.r[id])return;if(!DIMG.kimono_atlas){loadWear(id);return true;}
  const key=id+":"+st+":"+f;let e=k3cache.get(key);
  if(e)k3cache.delete(key);else{e=k3build(id,st,f);if(!e)return true;}
  k3cache.set(key,e);if(k3cache.size>K3.max)k3cache.delete(k3cache.keys().next().value);   // LRU
  g.save();g.scale(k/2,k/2);g.drawImage(e.c,e.ox,e.oy);g.restore();return true;});
X.kimono3d={cache:k3cache,build:k3build};
}
