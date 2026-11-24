/* Web build only: real, zoomable map (Leaflet + street/satellite tiles) replaces the drawn SVG map. */
let LM = null, LG = null, LMK = {};
const LMAP_LAYERS = () => ({
  "街道": L.tileLayer("https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png", {maxZoom: 19, subdomains: "abcd", attribution: "© OpenStreetMap © CARTO"}),
  "卫星": L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {maxZoom: 18, attribution: "Imagery © Esri"})
});
let LMAP_BASE = "街道";
function drawMap(resetView){
  const box = $("#mapbox"); if(!box || typeof L === "undefined") return;
  let el = box.querySelector("#lmap"), keep = null;
  if(!el){
    box.querySelector("#mapsvg")?.remove(); box.querySelector(".mapctl")?.remove(); box.querySelector(".maplegend")?.remove();
    el = document.createElement("div"); el.id = "lmap"; box.prepend(el);
  }
  if(!LM || LM.getContainer() !== el){
    if(LM){ keep = {c: LM.getCenter(), z: LM.getZoom()}; LM.remove(); }
    LM = L.map(el, {zoomControl: true, attributionControl: true, tap: false});
    const layers = LMAP_LAYERS(); layers[LMAP_BASE].addTo(LM);
    L.control.layers(layers, null, {position: "topright", collapsed: false}).addTo(LM);
    LM.on("baselayerchange", e => { LMAP_BASE = e.name; });
    LG = L.layerGroup().addTo(LM);
    if(keep && !resetView) LM.setView(keep.c, keep.z); else resetView = true;
  }
  LG.clearLayers(); LMK = {};
  const pts = mapPoints(); window.__mpts = pts;
  const byDay = {};
  pts.filter(p => p.kind === "place" && p.day > 0).forEach(p => (byDay[p.day] = byDay[p.day] || []).push(p));
  Object.entries(byDay).forEach(([d, list]) => {
    const ordered = sortPlaces(list.map(x => x.o)).map(o => coordsOf(o));
    if(ordered.length > 1){
      L.polyline(ordered, {color: "#ffffff", weight: 7, opacity: .9}).addTo(LG);
      L.polyline(ordered, {color: dayColor(Number(d)), weight: 4, opacity: .95, dashArray: "1 8", lineCap: "round"}).addTo(LG);
    }
  });
  pts.forEach((p, i) => {
    const sel = mapSel && mapSel.id === p.o.id, isB = p.kind === "booking";
    const col = isB ? "#1d1d1f" : dayColor(p.day);
    const txt = isB ? bookingGlyph(p.o) : (p.day > 0 ? p.day : "?");
    const icon = L.divIcon({className: "lmk", html: `<span class="lmk-b ${isB ? "sq" : ""} ${sel ? "sel" : ""}" style="--c:${col}">${txt}</span>`, iconSize: [28, 28], iconAnchor: [14, 14]});
    const m = L.marker(p.c, {icon, zIndexOffset: sel ? 1000 : isB ? 0 : 100}).addTo(LG);
    m.bindTooltip(esc(shortName(p.o.name || p.o.title || p.o.location)), {direction: "right", offset: [12, 0], className: "lmk-tip"});
    m.on("click", () => { mapSel = {kind: p.kind, id: p.o.id}; drawMap(false); $("#mapinfo")?.scrollIntoView({block: "nearest", behavior: "smooth"}); });
    LMK[p.o.id] = m;
  });
  if(resetView){
    if(pts.length) LM.fitBounds(L.latLngBounds(pts.map(p => p.c)).pad(0.15), {maxZoom: 12});
    else LM.setView([-44, 170.5], 6);
  }
  setTimeout(() => LM && LM.invalidateSize(), 0);
  const pl = $("#plist");
  if(pl){
    const sorted = pts.slice().sort((a, b) => ptKey(a).localeCompare(ptKey(b)));
    pl.innerHTML = sorted.length ? sorted.map(p => `<button class="p" data-pick="${pts.indexOf(p)}"><span class="bub" style="${p.kind === "booking" ? "background:#1d1d1f;color:#fff" : "background:" + dayColor(p.day)}">${p.kind === "booking" ? bookingGlyph(p.o) : (p.day || "?")}</span><span style="min-width:0;overflow-wrap:anywhere">${esc(p.o.name || p.o.title)}</span><span class="sub" style="white-space:nowrap">${p.kind === "booking" ? (p.o.start ? fmtDate(parseDate(p.o.start)) : (BK_TYPES[p.o.type] || BK_TYPES.other)[0]) : (p.day ? "第" + p.day + "天" : "未安排")}</span></button>`).join("") : `<div class="empty">这一天还没有带坐标的地点。</div>`;
  }
  renderMapInfo();
}
function bindMap(){}
document.addEventListener("click", e => {
  const t = e.target.closest("[data-pick]"); if(!t || !window.__mpts) return;
  e.stopImmediatePropagation(); e.preventDefault();
  const p = window.__mpts[Number(t.dataset.pick)]; if(!p) return;
  mapSel = {kind: p.kind, id: p.o.id};
  if(LM) LM.setView(p.c, Math.max(LM.getZoom(), 11));
  drawMap(false); $("#mapbox")?.scrollIntoView({block: "nearest", behavior: "smooth"});
}, true);
