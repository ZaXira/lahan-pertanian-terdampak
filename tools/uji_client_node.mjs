// Uji @gradio/client (versi yang sama dengan situs) dari Node untuk memisahkan masalah browser vs pustaka.
import { Client, handle_file } from "@gradio/client";

const SPACE = "ZaXira/lahan-pertanian-terdampak";
const url = (f) => `https://huggingface.co/datasets/ZaXira/palu-tsunami-lahan-pertanian/resolve/main/tif/palu-tsunami_00000195_${f}_disaster.tif`;
const t0 = Date.now(), dt = () => `${Math.round((Date.now() - t0) / 1000)} s`;

const app = await Client.connect(SPACE, { events: ["data", "status", "log"] });
console.log(dt(), "terhubung; endpoint:", Object.keys((await app.view_api()).named_endpoints));
const job = app.submit("/proses", [handle_file(url("pre")), handle_file(url("post")), 0.4984]);
for await (const ev of job) {
  console.log(dt(), ev.type, JSON.stringify(ev).slice(0, 300));
  if (ev.type === "data") break;
}
console.log(dt(), "selesai iterasi");
process.exit(0);
