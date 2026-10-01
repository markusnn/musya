# «Мусин дом»: how an add-on is built (read fully before starting)

The game is ONE file, `index.html` (~450 KB): HTML + CSS + one big `(()=>{"use strict"; … })()` script.
Several people work in parallel, so **nobody edits `index.html`**. Each add-on is delivered as:

1. `feat/<name>.js` — one JS block, the whole file wrapped in `{ … }` (a block scope: in strict mode the
   `function`s and `const`s inside it are private to the block, so names never clash with other add-ons).
   At integration all blocks are pasted into index.html right before the line
   `// ───────────────────────── Boot ─────────────────────────`, i.e. AFTER all core code and BEFORE boot.
   The block sees every core name (S, pet, goRoom, toast, drawMon, …) and plugs in through hooks (below).
2. `art/<name>.py` — procedural painting script(s) (PIL/numpy, like the existing art/*.py) that write the
   pictures into `assets/…`. Run it yourself and keep the produced files. Previews → `art/out/` (git-ignored).
3. Your final message = a report (see the end).

If you truly need a change in core code, do NOT edit index.html: describe the exact change in your report
(file position + old → new) and, if it is needed for your tests, apply it only inside your test run via
`--pre` (e.g. reassigning a core function: `someCoreFn=function(){…}` works because function declarations
are mutable bindings). Prefer hooks.

## Speed rules (the player wants results fast)
- Get it WORKING first, polish after. Test on phone 480×900 only (the lead checks wide screens at assembly).
- At most 4 runs of tools/shot.py, re-render art at most twice; render art at the needed size only.
- Report as soon as the feature works — aim for ~60–75 minutes. Read skills notes for known pitfalls:
  /Users/markvozdvizenskij/work/claude-brain/skills/playwright-game-shots.md, musya-art-toolkit.md, musya-room-layers.md.
- Already built into index.html (feat/READY): rooms, rooms2, story2, return, lanterns, visitors, rumors, haunt, dreams,
  candles, trust, travel, sakura, gacha, kimono3d, ema, parade, forest, seasons (real weather), birthday, pet2 (a kitten
  that follows Musya), zen (a zen garden patch in the courtyard) — look at their hub cards, tray buttons and hit zones
  so you don't overlap them (feat/<name>.js).

## Look & tone
- Dark painterly Japan at night, muted colours, film grain; rare pink sakura. «Говорящая Анджела 2» without ads.
  Musya is a real-looking tabby kitten (photo-like sprite frames). She **never talks** — only wordless emoji
  bubbles (`react("😸",1.6)`). Other characters (yōkai) do talk, in short, warm, slightly eerie sentences.
- Real Japanese folklore only (Toriyama Sekien, Lafcadio Hearn, regional legends). No copyrighted characters.
- All player-facing text is **Russian**, literate, natural (not machine-translated). Code comments in English,
  short, in the same dense style as the core (one-line functions, compact).
- The balance of coins is infinite (∞): nothing is about grinding money. Things hook the player through
  curiosity, anticipation (something will be ready tomorrow), collections and attachment to Musya.
- **Do not clutter the main screen.** The player asked for the story to be moved off the main screen because
  it got in the way. So: never auto-open panels (the only exception is idea #1, the «while you were away»
  postcard on return), no permanent chips/banners over the room. Use: a dot on the «家» button (hook
  `hubDot`), a dot on a room tab (hook `tabDot`), a short toast (one line, ≤ 45 chars — toasts are
  `white-space:nowrap`), and things that live *inside the painted room* (a lantern, a figure, a glow).

## Core things you will use (all in scope inside your block)
State and time
- `S` — game state. **Your persistent state goes in `S.ext.<yourName>`** (JSON-serializable). `save()` runs every
  5 s and on page hide; call `save()` right after important changes. `saved` = the state loaded at start
  (`saved.t` = ms timestamp of the last save → how long the player was away).
- `S.room` current room id; `ROOMS` list; `goRoom(id)`; rooms: entrance 門 Вход, engawa 縁側 Веранда,
  courtyard 中庭 Дворик, kitchen 台所 Кухня, onsen 温泉 Онсэн, bedroom 寝室 Спальня, wardrobe 衣装 Гардероб,
  games 遊び Игры, matsuri 祭 Ярмарка.
- `S.needs` {food,clean,energy,joy} 0..100. `S.owned` Set of owned item ids. `S.placed` {itemId:{r:room,x,y}} —
  things the player put into rooms (image coords). `S.wear` {head,body,mask,eyes,neck}.
- `today()` Date (respects `?date=YYYY-MM-DD`), `dayKey()` "2026-09-30" — use it for everything daily.
  `hourNow()` fractional hour (respects `?hour=2.5`), `dayTint()[1]` true at night. `now()` seconds (performance
  clock, for animation), `Date.now()` for real time spans.
- `weather.on` (rain), `festNow()`, `festOn(id)`, `scene.on` (a story scene is playing — stay invisible then),
  `overlaysOpen()` (a full-screen panel/game is open), `petAway()` (Musya is travelling, see below).

Musya
- `pet` (x on stage, action…), `start(action)` — actions: idle, sleep, purr, yarn, treat, highfive, stretch, groom,
  knead, house, butterfly, box, gift, hide, sulk, meow, music, peek, zoomies, firefly, petals, cursor, beg, poke,
  walkto (`walkTo(it,after,face)` with it={x}), refuse. `react(emoji,sec)` a wordless bubble. `burst(n)` sakura
  petals from her. `pet.action==="sleep"` while she sleeps. Needs change with `S.needs.joy=clamp(S.needs.joy+5,0,100)`.
- `petAway()` is `!!S.ext.away`. While true, Musya is not drawn, cannot be tapped, `start()` refuses, needs stand
  still. Only the travel add-on sets `S.ext.away`; everyone else must check `petAway()` before making her act.

Drawing inside a room (called from hook `draw`)
- Rooms are paintings 1800×1400 in **image coords**, projected in 3D. `imgToStage(ix,iy,d)` → screen [x,y];
  `d` is the depth of the layer you stand on (Musya is `CAT_D`=.8; floor things usually `CAT_D`).
  `BGM.k` = image→screen scale. `visX(ix,margin)` clamps an x into what is visible on a narrow phone.
  `catLineY()` = image y of Musya's floor line: things with y > catLineY()+6 are in front of her.
  Hook `draw(t,front)` is called twice per frame: `front=false` behind Musya, `true` in front of her — draw each
  thing in exactly one of the two passes (compare its y with catLineY()+6).
- `drawMon(id,ix,iy,hImg,d,alpha,anchor="b",rot=0,flipX=false)` draws a painted character from `assets/mon/<id>.webp`
  standing at (ix,iy) with height hImg (image px). Register new ones: `MON.m_x=[w,h]` (their pixel size) at block
  top-level — the loader picks up everything in MON at boot. Bestiary: `BESTIARY.push([key,"m_x","Имя","Описание"])`,
  mark seen with `if(!ST.seen.includes(key))ST.seen.push(key)`.
- `ctx` = the stage 2D context (already scaled to CSS px). `view` {W,H,s}. Keep draw hooks cheap: no new canvases
  per frame, cache images/gradients where possible.
- Existing props/decor: `roomThings()` gives what stands in the current room ({id,x,y,…}); `spriteBox(it)`.
- Taps on the room: hook `hit(x,y)` (stage px) → return true if you consumed the tap.
- Sound: `tone(freq,dur,type,vol)`, `chime([f1,f2,…])`, `sfx("pop"|"coin"|"chime"|"bad"|"eat"|"splash")`, `knock()`,
  `scareSound()`. Visual fx: `floatFx.push({g:"✨",x,y,t:now()})` (stage px), `fxAt(it,["✨"],3)`.

Things (collectible items)
- `ITEMS` / `IT[id]` / `ICATS`. Add yours with `addItems(list, {atlasKey:[atlasW,atlasH]})` at block top-level.
  Item: `{id,n:"Название",c:"Категория",w,h,a:"b"|"t",p:price,at:[atlasKey,x,y],src:"🐾 находка",hint:"Как получить…"}`
  — w,h = the picture's size inside the atlas (px), `a:"b"` stands on the floor, `"t"` hangs from above.
  Pictures live in `assets/items/atlas_<atlasKey>.webp` (pack all your item pictures into 1–2 atlases).
  `src` makes it locked in the shop («???», dark silhouette) until the player owns it; `hint` is the toast shown when
  they tap a locked one. Give things with `S.owned.add(id)`. The player then places them from «🧺 Вещи» in any room.
  Categories appear automatically in «🧺 Вещи» and in the album collection. Look at existing item art sizes
  (`ITEMS` entries in index.html) — typical 100–240 px.
- Pantry food: `FOOD` ids (i_*, v_*, u_*, ds_*), `have(id)`, `give(id,n)`, `take(id)`, `fThumb(id,w,h)` html,
  `fDraw(ctx,id,x,y,size)`. New food/dish pictures: add `FATL.<key>={w,h,r:{id:[x,y,w,h]}}` (→ assets/items/atlas_<key>.webp)
  and `FOOD.<id>={n,k:"dish",food,joy}`; new recipes: `RECIPES.push(…)` (see the COOK code). Guests: `GUESTS`, `S.guest`, `S.friends`.
- Stamps: `STAMPS.push([id,"漢","Название","Как получить"])`, `award(id)` gives it once with a toast.
- `itemThumb(IT[id],w,h)` html thumbnail for panels.

Hooks — `hook(name, fn)` at block top-level
| name | args → return | when |
|---|---|---|
| `boot` | () | once, after the game started (rooms, story, festivals ready) |
| `sec` | () | every second |
| `tick` | (t,dt) | every frame (keep tiny) |
| `ev` | (ev,d) | game events: place(a) lantern(on) food(id) eat(id) bath towel lamp(off) kaidan(i) game({id,score}) put({id,room,c}) act(action) tick wish cook({id,…}) harvest({id}) plant({id}) water guest({id}) wear({slot,id}) — see `qev(` calls in index.html |
| `draw` | (t,front) | every frame, twice |
| `overlay` | (t) | every frame, on top of everything in the room |
| `hit` | (x,y) → true | a tap on the room |
| `sleepTap` | () → true | the player taps Musya while she sleeps |
| `room` | (id) | after moving to another room |
| `gate` | (id) → true | before moving: return true to stop (e.g. a locked room) |
| `tray` | (trayEl,room) | after the bottom tray was rebuilt: add your buttons, e.g. `if((S.trayMode[room]\|\|"play")==="play"&&room==="courtyard")trayEl.querySelector(".items")?.insertAdjacentHTML("afterbegin",'<button class="item wide" data-x="tree:water"><span class="ico">🌸</span><span class="nm">Полить сакуру</span></button>')` |
| `click` | (key,btn) → true | any `[data-x="key"]` button in the tray, the shared panel or the hub. Prefix your keys: `tree:water` |
| `hub` | () → html | your card in the «家 Дом» panel: `<div class="hubc"><h4>🌸 Сакура <i>桜</i></h4><p>…</p><div class="row"><button class="btn" data-x="…">…</button></div></div>` |
| `hubDot` | () → true | something waits for the player (lights a dot on 家) |
| `tabDot` | (room) → true | a dot on that room's tab |
| `tabLock` | (room) → text | the room is closed (tab shows 🔒); rebuild tabs with `buildTabs()` after unlocking |
| `away` | (ms) → {i:"🎴",t:"…"} | a line for the «Пока тебя не было» postcard (only if something happened) |
| `album` | (el) | append your section to the album (`el.insertAdjacentHTML("beforeend",…)`), use classes `bh`, `lead`, `coll`, `ci` |
| `disc` | (kind,id) | someone discovered something (see below) |
| `panelClose` | (id) | the shared panel was closed |
| `drawBody` | (g,st,f,k,id) → true | draw the kimono yourself (kimono add-on only) |
| `itemTap` | (it,I,t) → true | the player tapped a placed thing (custom reaction for your items) |
| `weather` | () → "rain"\|"clear"\|null | only while the weather button is on «авто»: force rain or clear (real weather) |
| `fx` | (k) → true | turn on a festival effect outside festivals: snow, peach, momiji, sakura, moon, stars, koinobori, spirits, yuzu, shobu |

Shared UI
- `openPanel(title,html,id)` — full-screen panel like the album (classes: `lead`, `bh`, `hubc`, `coll`, `ci`, `btn`,
  `btn primary`, `qtasks`, `fest-now`, `guest`, `stamps`…). Re-calling it with the same id keeps the scroll.
  `panelIs(id)`, `closePanel()`. Buttons inside with `data-x` go to hook `click`.
- `dlg({head,text,img,ok,no,onOk,onNo})` — a small dialog over the top of the room (like the guest's). `dlgClose()`.
- `toast("…")` one short line.
- Mini-games / full-screen scenes: `GAMES.push({id,hidden:true,n,tag,icon,bg,lives:null,time:null,lore,how,
  init(G,t),step(G,t,dt),draw(G,g,t),down(G,x,y,t),move(G,x,y,held),up(G),stat:G=>"…",card(G,rec,coins)→html,after(G)})`
  then `openPlace(id)` (starts at once) or `openGame(id)` (with an intro card). `G.W,G.H,G.s`, `G.st` your state,
  `gEnd()` finishes. Background `bg`: a style for `gPaint()` or your own: set `G.bgc` in init. Helpers:
  `drawCatG(g,strip,frame,x,floorY,scale,alpha)` draws Musya (strips: rest, sleep, play, purr, moveRight, moveLeft,
  groom, stretch, knead, yarn, box, gift, hide, sulk, highfive, treat, house, butterfly, gaze9, gaze10; 8 frames each),
  `textC(g,txt,x,y,size,color,weight)`, `btnRect(g,x,y,w,h,label,hot)`, `sceneBg(room,topShare)` → [canvas,ctx].
  Examples: GARDEN, FISHING, COOK in index.html.
- Story books (only the second-story add-on): `BOOKS.push({id,title,lead,fin,ch:[chapters],st:state,gate(st)→text|null,after(k),end()})`
  chapters use the same format as `STORY` in index.html (title, room, reward, intro{p,chars,fx}, tasks[{t,ev,test,n}],
  outro{p,chars}); state `{ch:0,prog:[],started:false,done:false,seen:-1,ready:false}` kept in `S.ext`.
  Everything is played from the «物語 Сюжет» tab.
- Rooms (only the rooms add-on): `addRoom({id,jp,ru,hint,label,layers:[[name,depth]…],l3:{name:{g:groundY}|{ext:.3}|{on:"wall",dz:.05}},fog,tint,mote,focus,cat,outdoor,tray:()=>html})`
  — pictures `assets/layers/<id>_<name>.webp`, 1800×1400 each, same rules as the existing rooms (see `LAYERS`, `L3`
  in index.html and `art/layers.py`, `art/matsuri.py`).

Discoveries and the hundred candles
- Call `disc(kind,id)` the FIRST time the player gets/meets each collectible thing of yours (it returns true only
  the first time). The «Сто свечей» add-on counts all discoveries as candles. Kinds in use:
  `find` (Musya's finds) · `rareguest` · `ema` · `parade` · `forest` · `season` · `birthday` · `pet` · `star` · `hanafuda` · `craft` · `crane` · `bird` · `koi` · `serial` · `ryokan` · `kanji` · `visitor` (yōkai lured by things) · `rumor` (rumours solved) · `chapter2`
  (second story chapters) · `dream` · `haunt` · `postcard` · `souvenir` · `room` (rooms opened) · `figure`
  (gachapon figurines) · `bloom` · `trust` (trust levels). `discN(kind)` counts.

## Names (to avoid clashes between parallel add-ons)
Use ONLY your own prefix (given in your task) for: item ids, atlas keys, MON ids (`m_<prefix>_…`), stamp ids,
`data-x` keys (`<prefix>:…`), S.ext key, X key, CSS classes, asset file names. Need CSS? Inject it once from your
block: `document.head.insertAdjacentHTML("beforeend","<style>…</style>")` with prefixed class names.
Do not touch files of other add-ons, `index.html`, `tools/`. The machine is a fanless MacBook Air shared by ~12
parallel workers: keep test runs short, don't run many Chrome instances at once, render art at the needed size only.

## Pictures
- Look at `art/paint.py`, `art/items.py`, `art/monsters.py`, `art/story_art.py`, `art/guests_art.py`, `art/matsuri.py`,
  `art/food.py`, `art/room_items2.py` and at the existing webp files in `assets/` to match the style: soft painted
  volumes, dark outlines only where needed, muted palette, warm lantern light. Characters: `assets/mon/*.webp`
  (e.g. m_kitsune 400×450, m_tanuki 340×470), transparent background.
- **File budget**: the Claude copy of the game allows ~500 files in total and ~240 are used. Pack small pictures into
  atlases (one webp + a JSON rect map embedded in your JS). Keep each add-on within the budget given in your task.
- webp quality ~88, transparent where needed. Keep single pictures ≤ ~300 KB.

## Testing (required)
```
PY=/Users/markvozdvizenskij/work/tg-channels/.venv/bin/python
cd /Users/markvozdvizenskij/work/musya/codex-workspace/work/musya-site
$PY tools/shot.py --blocks feat/<name>.js --out /tmp/<name>_shots --steps '[{"js":"goRoom(\"courtyard\")"},{"wait":1500},{"shot":"a"}]'
```
Read `tools/shot.py` (steps: js / log / wait / click / clickSel / shot; `--hour`, `--date`, `--size 1280x800`,
`--state`, `--fresh`, `--pre`). Code in `js` steps runs inside the game closure but NOT inside your block — expose
test handles from your block if needed, e.g. `X.myName={…}` (the shared object `X` below).
Use a separate `--out` folder of your own. Look at the screenshots yourself (Read the png). Check: phone 480×900
AND wide 1280×800; night (`--hour 23`) and day; no console errors (the script prints them and exits 1).
3D in headless is slow (swiftshader): allow waits of 1.5–3 s after goRoom.

Shared object for cross-add-on handles: at block top-level write `X.<name>={…}` (X is created in index.html).

## Report (your final message)
- files created (code, art scripts, assets — with the count of new asset files)
- S.ext keys, hooks used, disc kinds and how many things of each exist, items added (count, categories), MON ids,
  stamps, bestiary entries
- any core change you need (exact old → new), known issues
- 3–5 screenshot paths that show the feature best
