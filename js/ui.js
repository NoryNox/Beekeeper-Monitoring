// js/ui.js
// UI-Hilfsfunktionen
function drawBox(ctx, x, y, w, h, color, label, score) {
  ctx.strokeStyle = color;
  ctx.lineWidth = 5;
  ctx.strokeRect(x, y, w, h);
  ctx.fillStyle = color;
  ctx.fillText(`${label} ${Math.round(score * 100)}%`, x, y - 10);
}
