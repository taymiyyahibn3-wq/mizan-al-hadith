"use client";

import { ChevronRight, Search } from "lucide-react";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { SiteChrome } from "../components/SiteChrome";
import { BookShowcase, SIX_BOOKS } from "../components/BookShowcase";

const API = process.env.NEXT_PUBLIC_API_URL!;

type Book = { id:number; name:string; author_name?:string; author_death_year?:number; tasnif?:string; hadith_qty?:number };

export default function BooksPage() {
  const [books, setBooks] = useState<Book[]>([]);
  const [q, setQ] = useState("");

  useEffect(() => {
    fetch(`${API}/books`, { cache: "no-store" }).then(r => r.json()).then(d => setBooks(d.books || [])).catch(() => {});
  }, []);

  const filtered = useMemo(() => {
    const x = q.trim().toLocaleLowerCase();
    return x ? books.filter(b => `${b.name} ${b.author_name || ""} ${b.tasnif || ""}`.toLocaleLowerCase().includes(x)) : books;
  }, [books, q]);

  return (
    <SiteChrome>
      <section className="page-hero library-hero">
        <div className="container">
          <div className="section-kicker">THE LIBRARY</div>
          <h1>Hadith Collections</h1>
          <p>Start with the Six Books, or search the complete indexed catalogue.</p>
          <div className="mini-search"><Search size={18}/><input value={q} onChange={e => setQ(e.target.value)} placeholder="Filter books by title, author or classification…" /></div>
        </div>
      </section>

      <section className="container section">
        <div className="section-intro"><div><div className="section-kicker">الكتب الستة</div><h2>Six Books</h2><p>The main collections are presented as their Arabic book covers.</p></div></div>
        <BookShowcase compact />
      </section>

      <section className="container section catalogue-section">
        <div className="section-head"><div><div className="section-kicker">COMPLETE CATALOGUE</div><h2>{filtered.length} books</h2></div><span className="muted">425 indexed collections</span></div>
        <div className="book-grid">
          {filtered.map(b => {
            const featured = SIX_BOOKS.find(x => x.id === b.id);
            return <Link href={`/books/${b.id}`} className="book-card card" key={b.id}>
              {featured ? <div className="mini-cover"><img src={featured.cover} alt="" /></div> : <div className="book-icon"><span>{String(b.id).padStart(3,"0")}</span></div>}
              <div className="book-number">BOOK {String(b.id).padStart(3,"0")}</div>
              <h3 className="arabic book-name">{featured?.arabic || b.name}</h3>
              <p>{featured?.author || b.author_name || "Unknown author"}</p>
              <div className="book-bottom"><span>{b.hadith_qty ? `${b.hadith_qty.toLocaleString()} hadiths` : "Open collection"}</span><ChevronRight size={17}/></div>
            </Link>;
          })}
        </div>
      </section>
    </SiteChrome>
  );
}
