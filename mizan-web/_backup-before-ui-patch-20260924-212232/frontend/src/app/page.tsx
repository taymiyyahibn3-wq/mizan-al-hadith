"use client";

import { ChevronRight, Library, Search, ShieldCheck, Sparkles } from "lucide-react";
import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";
import { SiteChrome } from "./components/SiteChrome";
import { BookShowcase } from "./components/BookShowcase";

const API = process.env.NEXT_PUBLIC_API_URL!;

type Stats = { hadiths: number; books: number; narrators: number; sanads: number };
type Hadith = { id:number; book_id:number; no_inbook?:number; matn?:string; nass?:string; taraf_nass?:string; book_name?:string; author_name?:string };

function fmt(n?: number) { return typeof n === "number" ? n.toLocaleString() : "—"; }

export default function Home() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Hadith[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API}/stats`, { cache: "no-store" }).then(r => r.json()).then(setStats).catch(() => {});
  }, []);

  async function searchHadith(e?: FormEvent) {
    e?.preventDefault();
    const q = query.trim();
    if (!q) return;
    setLoading(true); setSearched(true); setError("");
    try {
      const r = await fetch(`${API}/hadith/search?q=${encodeURIComponent(q)}&limit=20&offset=0`, { cache: "no-store" });
      if (!r.ok) throw new Error();
      const data = await r.json();
      setResults(data.results || []);
    } catch { setError("Backend se connection nahi ho pa raha."); setResults([]); }
    finally { setLoading(false); }
  }

  return (
    <SiteChrome>
      <section className="hero hero-home">
        <div className="hero-glow hero-glow-one" /><div className="hero-glow hero-glow-two" />
        <div className="container hero-inner">
          <div className="eyebrow"><Sparkles size={14} /> THE HADITH RESEARCH LIBRARY</div>
          <h1>Read the tradition.<br /><em>Trace the chain.</em></h1>
          <p>Search Arabic hadith text, open the six canonical collections, follow isnād chains, study narrators and inspect connected research data.</p>
          <form className="searchbox hero-search" onSubmit={searchHadith}>
            <Search size={21} className="search-icon" />
            <input value={query} onChange={e => setQuery(e.target.value)} placeholder="ابحث في الحديث…  Search hadith text" dir="auto" />
            <button className="primary" disabled={loading}>{loading ? "Searching…" : "Search"}</button>
          </form>
          {error && <div className="error">{error}</div>}
          <div className="hero-hint"><span>Try Arabic text</span><span>•</span><span>Search by collection</span><span>•</span><span>Follow narrators</span></div>
        </div>
      </section>

      <section className="container stats-wrap">
        <div className="stats">
          <Stat label="Hadith" value={fmt(stats?.hadiths)} />
          <Stat label="Books" value={fmt(stats?.books)} />
          <Stat label="Narrators" value={fmt(stats?.narrators)} />
          <Stat label="Sanads" value={fmt(stats?.sanads)} />
        </div>
      </section>

      {searched && (
        <section className="container section search-section">
          <div className="section-head"><div><div className="section-kicker">SEARCH RESULTS</div><h2>{results.length} results</h2></div><Link href="/search" className="text-back">Advanced search <ChevronRight size={15}/></Link></div>
          <div className="results">
            {results.map(h => <Link href={`/hadith/${h.id}`} className="result-card" key={h.id}>
              <div className="result-meta"><span className="pill">#{h.id}</span>{h.book_name && <span className="pill green">{h.book_name}</span>}{h.no_inbook != null && <span className="pill">Hadith {h.no_inbook}</span>}</div>
              <div className="arabic result-arabic">{h.taraf_nass || h.nass || "—"}</div>
              <div className="result-footer"><span>{h.author_name || "Unknown author"}</span><ChevronRight size={17}/></div>
            </Link>)}
            {!results.length && <div className="card empty">No Arabic matches found.</div>}
          </div>
        </section>
      )}

      <section className="container section six-books-section" id="six-books">
        <div className="section-intro">
          <div>
            <div className="section-kicker">الكتب الستة · THE SIX BOOKS</div>
            <h2>The core collections</h2>
            <p>Open a collection to browse its hadiths, search by Arabic text, or jump directly to a hadith number.</p>
          </div>
          <Link href="/books" className="outline-link"><Library size={16}/> Full library <ChevronRight size={15}/></Link>
        </div>
        <BookShowcase />
      </section>

      <section className="container section research-strip">
        <div className="research-card">
          <div className="research-icon"><ShieldCheck size={22}/></div>
          <div><div className="section-kicker">BUILT FOR RESEARCH</div><h2>More than a reading app.</h2><p>Every hadith can lead you into its isnād, narrators, scholarly data, groups, topics and available English translation.</p></div>
          <Link href="/info" className="primary light-primary">Explore the system <ChevronRight size={16}/></Link>
        </div>
      </section>

      <footer className="footer"><div className="container">Mīzān al-Hadīth <span>•</span> Hadith research and library platform</div></footer>
    </SiteChrome>
  );
}

function Stat({ label, value }: { label:string; value:string }) { return <div className="card stat"><div className="stat-label">{label}</div><div className="stat-value">{value}</div></div>; }
