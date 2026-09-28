// Uji ujung-ke-ujung halaman unggah di Chrome sungguhan (via Chrome DevTools Protocol).
// Pakai: node artefak_fix/tools/uji_browser.mjs <url-halaman> [tile]
// Klik "Tile <tile>" lalu "Proses citra", pantau #status sampai selesai/gagal (maks 8 menit).
import { spawn } from "node:child_process";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const URL_HAL = process.argv[2], TILE = process.argv[3] || "00000195";
const CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe";
const port = 9333, profil = mkdtempSync(join(tmpdir(), "cdp-"));
const ch = spawn(CHROME, ["--headless=new", "--disable-gpu", `--remote-debugging-port=${port}`, `--user-data-dir=${profil}`,
  "--window-size=1440,2200", "about:blank"], { stdio: "ignore" });
const tidur = (ms) => new Promise((r) => setTimeout(r, ms));

let target;
for (let i = 0; i < 40 && !target; i++) {
  try { target = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find((t) => t.type === "page"); } catch { await tidur(250); }
}
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r));
let id = 0; const tunggu = new Map();
ws.addEventListener("message", (e) => {
  const m = JSON.parse(e.data);
  if (m.id && tunggu.has(m.id)) { tunggu.get(m.id)(m); tunggu.delete(m.id); }
  if (m.method === "Runtime.consoleAPICalled") console.log("  konsol:", m.params.args.map((a) => a.value ?? a.description).join(" ").slice(0, 500));
  if (m.method === "Runtime.exceptionThrown") console.log("  EXCEPTION:", m.params.exceptionDetails?.exception?.description?.slice(0, 500));
});
const kirim = (method, params = {}) => new Promise((r) => { const i = ++id; tunggu.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const nilai = async (expr) => (await kirim("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true })).result?.result?.value;

await kirim("Page.enable"); await kirim("Runtime.enable");
await kirim("Page.navigate", { url: URL_HAL });
await tidur(4000);
console.log("halaman:", await nilai("document.title"));
await nilai(`document.querySelector('#contoh [data-t="${TILE}"]').click()`);
await tidur(800);
await nilai(`document.getElementById("proses").click()`);
const mulai = Date.now(); let st = "";
while (Date.now() - mulai < 480000) {
  await tidur(5000);
  const s = await nilai(`document.getElementById("status").innerText`);
  if (s !== st) { st = s; console.log(`[${Math.round((Date.now() - mulai) / 1000)} s]`, s); }
  if (/Selesai|gagal|Kuota|beberapa menit lagi|dinyalakan ulang|tanpa gambar/i.test(s)) break;
}
console.log("gambar overlay:", await nilai(`!!document.querySelector("#hasil img.result-img")`));
console.log("tabel:", await nilai(`(document.querySelector("#hasil tbody")||{}).innerText`));
ws.close(); ch.kill();
process.exit(0);
