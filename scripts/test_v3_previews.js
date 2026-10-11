const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const OUT_DIR = path.join(__dirname, '..', 'video', 'screenshots');
if (!fs.existsSync(OUT_DIR)) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
}

async function main() {
  console.log('Rendering V3 preview frames...');
  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--window-size=1920,1080'],
    defaultViewport: { width: 1920, height: 1080, deviceScaleFactor: 1 }
  });

  const page = await browser.newPage();
  const htmlPath = 'file://' + path.resolve(__dirname, '..', 'video', 'index_v3.html').replace(/\\/g, '/');
  console.log('Loading composition:', htmlPath);
  await page.goto(htmlPath);

  await page.waitForFunction('window.isAssetsReady === true', { timeout: 30000 });
  await new Promise(r => setTimeout(r, 2000));

  const testFrames = [
    { name: 'v3_scene1_opening', frame: 90 },      // 3.0s (Brand & Sacred Geometry)
    { name: 'v3_scene2_scale', frame: 315 },        // 10.5s (Sequential Telemetry Cards)
    { name: 'v3_scene3_search', frame: 690 },       // 23.0s (Search Results & Bukhari #1 Focus)
    { name: 'v3_scene4_detail', frame: 960 },       // 32.0s (Hadith Detail, Matn Spans, Sahih Grade)
    { name: 'v3_scene5_isnad_net', frame: 1380 },   // 46.0s (Isnād Network & Narrator Drawer)
    { name: 'v3_scene6_isnad_map', frame: 1650 },   // 55.0s (Geographic Map & Diffusion Routes)
    { name: 'v3_scene7_isnad_time', frame: 1950 },  // 65.0s (Historical Timeline & Tabaqāt)
    { name: 'v3_scene8_isnad_3d', frame: 2280 },    // 76.0s (3D Spatial Graph & Coordinates)
    { name: 'v3_scene9_ask_mizan', frame: 2580 },   // 86.0s (Ask Mīzān AI Research Synthesis)
    { name: 'v3_scene10_hero', frame: 2880 }        // 96.0s (Complete Ecosystem Convergence)
  ];

  for (const tf of testFrames) {
    console.log(`Rendering frame ${tf.frame} (${tf.name})...`);
    await page.evaluate((f) => {
      window.renderVideoFrame(f);
    }, tf.frame);

    const filePath = path.join(OUT_DIR, `${tf.name}.png`);
    const canvas = await page.$('#videoCanvas');
    await canvas.screenshot({ path: filePath });
    console.log(`Saved: ${filePath}`);
  }

  await browser.close();
  console.log('All 10 V3 preview frames rendered successfully!');
}

main().catch(console.error);
