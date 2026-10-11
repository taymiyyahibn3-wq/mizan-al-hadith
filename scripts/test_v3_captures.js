const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const OUT_DIR = path.join(__dirname, '..', 'video', 'v3_raw_captures');
if (!fs.existsSync(OUT_DIR)) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
}

async function main() {
  console.log('Launching Puppeteer to audit running Mizan app...');
  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1920,1080'],
    defaultViewport: { width: 1920, height: 1080, deviceScaleFactor: 2 } // 2x Retina for crisp presentation
  });

  const page = await browser.newPage();

  const routes = [
    { name: '1_home', url: 'http://localhost:3000/' },
    { name: '2_search', url: 'http://localhost:3000/search?q=%D8%A5%D9%86%D9%85%D8%A7+%D8%A7%D9%84%D8%A3%D8%B9%D9%85%D8%A7%D9%84+%D8%A8%D8%A7%D9%84%D9%86%D9%8A%D8%A7%D8%AA' },
    { name: '3_hadith_detail', url: 'http://localhost:3000/hadith/1' },
    { name: '4_isnad_network', url: 'http://localhost:3000/isnad?book_id=1&view=network' },
    { name: '5_isnad_timeline', url: 'http://localhost:3000/isnad?book_id=1&view=timeline' },
    { name: '6_isnad_map', url: 'http://localhost:3000/isnad?book_id=1&view=map' },
    { name: '7_isnad_3d', url: 'http://localhost:3000/isnad?book_id=1&view=3d' },
    { name: '8_ask_mizan', url: 'http://localhost:3000/ask?query=Explain%20Sahih%20al-Bukhari%201%20and%20its%20classical%20commentary' },
    { name: '9_matn_visualizer', url: 'http://localhost:3000/hadith-visualizer' }
  ];

  for (const r of routes) {
    console.log(`Navigating to ${r.url}...`);
    try {
      await page.goto(r.url, { waitUntil: 'networkidle2', timeout: 25000 });
      await new Promise(res => setTimeout(res, 2500)); // allow renders & canvas to stabilize
      const filePath = path.join(OUT_DIR, `${r.name}.png`);
      await page.screenshot({ path: filePath });
      console.log(`Saved: ${filePath}`);
    } catch (e) {
      console.error(`Failed ${r.name}:`, e.message);
    }
  }

  await browser.close();
  console.log('Done auditing live app screens!');
}

main().catch(console.error);
