// Lê o histórico do Kling (aba nova) e baixa SÓ os Lip Sync dos números pedidos (entrada vNN.mp4) como <dir>/ksNN.mp4.
// Uso: node kling_lipsync_baixar.mjs <dir> <nn> [<nn> ...]   (sem filtro ele baixaria trabalhos antigos com o mesmo padrão de nome)

import { chromium } from 'playwright'; // npm i playwright (só a lib; o navegador é o seu, logado)
import { existsSync, writeFileSync } from 'node:fs';
const [, , dir, ...quero] = process.argv;
const browser = await chromium.connectOverCDP('http://127.0.0.1:9333');
const ctx = browser.contexts()[0];
const page = await ctx.newPage();
const hist = [];
page.on('response', async (r) => {
  try { if (r.url().includes('/api/user/works/personal/feeds')) hist.push(...(JSON.parse(await r.text()).data?.history || [])); } catch {}
});
await page.goto('https://kling.ai/app/lip-sync/new', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(15000);
const vistos = new Set();
for (const h of hist) {
  const ins = h.task?.taskInfo?.inputs || [];
  const v = ins.find(i => i.name === 'video')?.url || '';
  const m = v.match(/\/v(\d\d)\.mp4/); if (!m) continue;
  const nn = m[1]; if (!quero.includes(nn) || vistos.has(nn)) continue; vistos.add(nn);
  const w = h.works?.[0]; const url = w?.resource?.resource;
  if (h.task.status !== 99 || !url) { console.log(nn, 'pendente status', h.task.status); continue; }
  const dest = `${dir}/ks${nn}.mp4`;
  if (existsSync(dest)) { console.log(nn, 'ja baixado'); continue; }
  const r = await ctx.request.get(url);
  writeFileSync(dest, await r.body());
  console.log(nn, 'baixado', (await r.body()).length);
}
await page.close();
process.exit(0);
