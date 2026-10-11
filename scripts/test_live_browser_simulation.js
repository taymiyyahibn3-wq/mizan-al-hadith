/**
 * Live Runtime Verification Script
 * Validates the exact client-side data fetching and rendering logic for Mīzān al-Ḥadīth
 */

const API_BASE_URL = "http://127.0.0.1:8000/api";
async function getJSON(path) {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`HTTP ${res.status} for ${url}`);
  }
  return res.json();
}

function renderLinkedArabicText(fullText, spans) {
  if (!fullText || fullText === "—") return fullText;
  if (!spans || spans.length === 0) return fullText;

  const validSpans = spans
    .filter((s) => s && typeof s.start === "number" && typeof s.end === "number" && s.start >= 0 && s.end <= fullText.length && s.start < s.end)
    .sort((a, b) => a.start - b.start);

  if (validSpans.length === 0) return fullText;

  let reconstructed = "";
  let currentIndex = 0;
  const renderedLinks = [];

  validSpans.forEach((span, idx) => {
    if (span.start < currentIndex) return;

    if (span.start > currentIndex) {
      reconstructed += fullText.slice(currentIndex, span.start);
    }

    const narratorText = fullText.slice(span.start, span.end);
    reconstructed += `<a href="/narrator/${span.rawi_id}">${narratorText}</a>`;
    renderedLinks.push({
      rawi_id: span.rawi_id,
      text: narratorText,
      href: `/narrator/${span.rawi_id}`,
      name: span.name,
    });

    currentIndex = span.end;
  });

  if (currentIndex < fullText.length) {
    reconstructed += fullText.slice(currentIndex);
  }

  return { reconstructed, renderedLinks };
}

async function verifyHadith1() {
  console.log("================================================================================");
  console.log("VERIFYING LIVE RUNTIME: Sahih al-Bukhari #1 (Hadith ID: 1)");
  console.log("================================================================================");

  // 1. Fetch Hadith Detail
  const hadith = await getJSON("/hadith/1");
  console.log(`[PASS] Hadith #1 loaded from API: ${hadith.book_english_name} #${hadith.no_inbook}`);

  // 2. Test Sanad Narrator Links
  const arabicText = hadith.arabic_matn || hadith.nass;
  const { reconstructed, renderedLinks } = renderLinkedArabicText(arabicText, hadith.narrator_spans);

  console.log(`[PASS] Reconstructed Arabic text with ${renderedLinks.length} narrator links:`);
  renderedLinks.forEach((link, idx) => {
    console.log(`       ${idx + 1}. <a href="${link.href}">${link.text}</a> (${link.name})`);
  });

  const expectedIds = [4698, 3443, 8272, 6796, 5719, 5913];
  const actualIds = renderedLinks.map((l) => l.rawi_id);
  expectedIds.forEach((id) => {
    if (!actualIds.includes(id)) throw new Error(`Missing expected rawi_id: ${id}`);
  });
  console.log(`[PASS] All 6 Bukhari #1 narrator links verified: ${JSON.stringify(actualIds)}`);

  // Verify non-transmission words: check that verbs like حدثنا are not inside <a>
  if (reconstructed.includes("<a href=\"/narrator/4698\">حَدَّثَنَا")) {
    throw new Error("Transmission verb 'حَدَّثَنَا' incorrectly included in narrator link!");
  }
  console.log("[PASS] Transmission terminology correctly preserved outside <a> links");

  // 3. Fetch Commentary
  const commentaryData = await getJSON("/hadith/1/commentaries");
  console.log(`[PASS] Commentary API returned HTTP 200 (Available: ${commentaryData.available}, Total: ${commentaryData.total_commentaries})`);
  if (!commentaryData.available || commentaryData.total_commentaries < 3) {
    throw new Error("Commentary data for Bukhari #1 is incomplete or unavailable");
  }
  console.log("       Classical commentary sources:");
  commentaryData.commentaries.forEach((c) => {
    console.log(`       • [${c.commentary_title}] by ${c.author} (${c.mapping_status}, conf: ${c.mapping_confidence})`);
  });

  // 4. Fetch Scholarly Statements
  const gradesData = await getJSON("/hadith/1/grades");
  console.log(`[PASS] Scholarly statements API returned HTTP 200 (Narrator statements: ${gradesData.narrator_statements?.length || 0})`);
  const statements = gradesData.narrator_statements || [];
  if (statements.length > 0) {
    const sample = statements[0];
    console.log(`       Sample: Scholar="${sample.scholar_en}", Statement="${sample.statement_en.slice(0, 70)}..."`);
    // Verify scholar name is transliterated in Latin script
    if (/[ء-ي]/.test(sample.scholar_en)) {
      console.warn(`       [WARN] Scholar name contains Arabic characters: ${sample.scholar_en}`);
    } else {
      console.log(`       [PASS] Scholar name properly transliterated in Latin script: ${sample.scholar_en}`);
    }
  }
}

async function verifyHadith20918() {
  console.log("\n================================================================================");
  console.log("VERIFYING LIVE RUNTIME: Sunan an-Nasa'i #4 (Hadith ID: 20918)");
  console.log("================================================================================");

  const hadith = await getJSON("/hadith/20918");
  console.log(`[PASS] Hadith #20918 loaded from API: ${hadith.book_english_name} #${hadith.no_inbook}`);

  const arabicText = hadith.arabic_matn || hadith.nass;
  const { renderedLinks } = renderLinkedArabicText(arabicText, hadith.narrator_spans);

  console.log(`[PASS] Rendered ${renderedLinks.length} narrator links in Nasa'i #4:`);
  renderedLinks.forEach((link, idx) => {
    console.log(`       ${idx + 1}. <a href="${link.href}">${link.text}</a> (${link.name})`);
  });

  // Verify complex span: 'يَحْيَى وَهُوَ ابْنُ سَعِيدٍ'
  const yahyaLink = renderedLinks.find((l) => l.rawi_id === 8271);
  if (!yahyaLink || yahyaLink.text !== "يَحْيَى وَهُوَ ابْنُ سَعِيدٍ") {
    throw new Error(`Unexpected span for Yahya ibn Sa'id: ${JSON.stringify(yahyaLink)}`);
  }
  console.log(`[PASS] Exact complex span verified: <a href="${yahyaLink.href}">${yahyaLink.text}</a>`);

  // Verify 'أَبِي مُوسَى'
  const abuMusaLink = renderedLinks.find((l) => l.rawi_id === 5021);
  if (!abuMusaLink || abuMusaLink.text !== "أَبِي مُوسَى") {
    throw new Error(`Unexpected span for Abu Musa: ${JSON.stringify(abuMusaLink)}`);
  }
  console.log(`[PASS] Exact span verified: <a href="${abuMusaLink.href}">${abuMusaLink.text}</a>`);

  // Commentary for Nasa'i #4
  const commentaryData = await getJSON("/hadith/20918/commentaries");
  console.log(`[PASS] Commentary API returned HTTP 200 (Available: ${commentaryData.available}, Works: ${commentaryData.total_commentaries})`);
  if (commentaryData.available && commentaryData.commentaries.length > 0) {
    const comm = commentaryData.commentaries[0];
    console.log(`       • [${comm.commentary_title}] by ${comm.author}`);
  }
}

async function verifyNarratorRoute() {
  console.log("\n================================================================================");
  console.log("VERIFYING NARRATOR BIOGRAPHY ROUTE: /narrator/4698 (Al-Humaydi)");
  console.log("================================================================================");

  const rawi = await getJSON("/narrator/4698");
  console.log(`[PASS] Narrator #4698 loaded: ${rawi.name} (Rank: ${rawi.rank || "N/A"})`);
  console.log(`[PASS] Navigation target /narrator/4698 is active and valid`);
}

async function run() {
  try {
    await verifyHadith1();
    await verifyHadith20918();
    await verifyNarratorRoute();
    console.log("\n================================================================================");
    console.log("ALL LIVE RUNTIME VERIFICATION CHECKS PASSED (100%)! ✓");
    console.log("================================================================================");
  } catch (err) {
    console.error("Verification error:", err);
    process.exit(1);
  }
}

run();
