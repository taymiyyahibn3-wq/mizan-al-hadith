const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const OUTPUT_DIR = path.join(__dirname, '..', 'video', 'screenshots');

if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

async function capture() {
  console.log('Launching Chrome via puppeteer-core...');
  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1920,1080'],
    defaultViewport: { width: 1920, height: 1080, deviceScaleFactor: 1.5 }
  });

  const page = await browser.newPage();

  // 1. Homepage Hero & Stats
  console.log('Capturing 1_homepage_hero.png...');
  await page.goto('http://localhost:3000', { waitUntil: 'networkidle0', timeout: 30000 });
  await page.waitForSelector('.stats');
  // Wait a moment for stats to fetch & render
  await new Promise(r => setTimeout(r, 2000));
  await page.screenshot({ path: path.join(OUTPUT_DIR, '1_homepage_hero.png') });

  // 2. Search Results for "إنما الأعمال بالنيات"
  console.log('Capturing 2_search_results.png...');
  const searchInput = await page.$('.searchbox input');
  if (searchInput) {
    await searchInput.type('إنما الأعمال بالنيات', { delay: 40 });
    const searchBtn = await page.$('.searchbox button[type="submit"]');
    if (searchBtn) {
      await searchBtn.click();
      await new Promise(r => setTimeout(r, 3000));
      await page.screenshot({ path: path.join(OUTPUT_DIR, '2_search_results.png') });
    }
  }

  // 3. Hadith Detail Page (Hadith 1 - Bukhari)
  console.log('Capturing 3_hadith_detail.png...');
  await page.goto('http://localhost:3000/hadith/1', { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise(r => setTimeout(r, 2500));
  await page.screenshot({ path: path.join(OUTPUT_DIR, '3_hadith_detail.png') });

  // 4. Hadith 1 - Sanad tab
  console.log('Capturing 4_hadith_sanad_tab.png...');
  // Find tab with text 'sanad' or click sanad tab
  const tabs = await page.$$('button');
  for (const tab of tabs) {
    const text = await page.evaluate(el => el.textContent, tab);
    if (text && (text.includes('Sanad') || text.includes('Chain') || text.includes('سند') || text.toLowerCase().includes('sanad'))) {
      await tab.click();
      await new Promise(r => setTimeout(r, 1500));
      break;
    }
  }
  await page.screenshot({ path: path.join(OUTPUT_DIR, '4_hadith_sanad_tab.png') });

  // 5. Cross-Collection Hadith Visualizer (Bukhari 1 network)
  console.log('Capturing 5_hadith_visualizer.png...');
  await page.goto('http://localhost:3000/hadith-visualizer?book_id=1&hadith_number=1', { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise(r => setTimeout(r, 3000));
  await page.screenshot({ path: path.join(OUTPUT_DIR, '5_hadith_visualizer.png') });

  // 6. Isnād Network (Narrator Graph)
  console.log('Capturing 6_isnad_network.png...');
  await page.goto('http://localhost:3000/isnad?book_id=1&limit=40', { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise(r => setTimeout(r, 3500));
  await page.screenshot({ path: path.join(OUTPUT_DIR, '6_isnad_network.png') });

  // 7. Narrator Profile (Imam al-Bukhari rawi 6817)
  console.log('Capturing 7_narrator_profile.png...');
  await page.goto('http://localhost:3000/narrator/6817', { waitUntil: 'networkidle0', timeout: 30000 }).catch(async () => {
    // If route doesn't exist directly, try /narrators
    await page.goto('http://localhost:3000/isnad?rawi_id=6817', { waitUntil: 'networkidle0' });
  });
  await new Promise(r => setTimeout(r, 2500));
  await page.screenshot({ path: path.join(OUTPUT_DIR, '7_narrator_profile.png') });

  console.log('All real UI screenshots captured successfully in:', OUTPUT_DIR);
  await browser.close();
}

capture().catch(err => {
  console.error('Capture failed:', err);
  process.exit(1);
});
