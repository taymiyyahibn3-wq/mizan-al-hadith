"use client";

import { ArrowUpRight, BookOpen } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

export type FeaturedBook = {
  id: number;
  arabic: string;
  english: string;
  author: string;
  short: string;
  cover: string;
};

// Prefer Wikimedia Commons for the covers because the previous implementation
// hot-linked several commercial/retail image hosts. Those hosts can block
// hotlinking, change URLs, or disappear without notice.
export const SIX_BOOKS: FeaturedBook[] = [
  {
    id: 1,
    arabic: "صحيح البخاري",
    english: "Sahih al-Bukhari",
    author: "Imam al-Bukhari",
    short: "BUKHARI",
    cover: "https://commons.wikimedia.org/wiki/Special:Redirect/file/SaheehAlBukhari.png",
  },
  {
    id: 2,
    arabic: "صحيح مسلم",
    english: "Sahih Muslim",
    author: "Imam Muslim",
    short: "MUSLIM",
    cover: "https://commons.wikimedia.org/wiki/Special:Redirect/file/SahihMuslimCover.jpg",
  },
  {
    id: 3,
    arabic: "جامع الترمذي",
    english: "Jamiʿ al-Tirmidhi",
    author: "Imam al-Tirmidhi",
    short: "TIRMIDHI",
    cover: "https://commons.wikimedia.org/wiki/Special:Redirect/file/سنن_الترمذي.jpg",
  },
  {
    id: 4,
    arabic: "سنن أبي داود",
    english: "Sunan Abi Dawud",
    author: "Imam Abu Dawud",
    short: "ABU DAWUD",
    cover: "https://commons.wikimedia.org/wiki/Special:Redirect/file/SunanAbiDaoud.jpg",
  },
  {
    id: 5,
    arabic: "سنن النسائي",
    english: "Sunan al-Nasa'i",
    author: "Imam al-Nasa'i",
    short: "NASAI",
    // Wikimedia's source here is a public-domain scan; this is the first-page
    // image preview of the Arabic edition rather than a PDF loaded into <img>.
    cover: "https://commons.wikimedia.org/wiki/Special:Redirect/file/سنن_النسائي_(المكتبة_التجارية،_1348هـ).pdf/page1-377px-سنن_النسائي_(المكتبة_التجارية،_1348هـ).pdf.jpg",
  },
  {
    id: 6,
    arabic: "سنن ابن ماجه",
    english: "Sunan Ibn Majah",
    author: "Imam Ibn Majah",
    short: "IBN MAJAH",
    cover: "https://commons.wikimedia.org/wiki/Special:Redirect/file/کتاب_حدیث_سنن_ابن_ماجه.jpg",
  },
];

function CoverFallback({ book }: { book: FeaturedBook }) {
  return (
    <div className="book-cover-fallback" aria-label={`${book.english} cover fallback`}>
      <div className="fallback-arabic">{book.arabic}</div>
      <div className="fallback-rule" />
      <div className="fallback-english">{book.english}</div>
      <div className="fallback-author">{book.author}</div>
    </div>
  );
}

function BookCover({ book }: { book: FeaturedBook }) {
  const [failed, setFailed] = useState(false);

  return failed ? (
    <CoverFallback book={book} />
  ) : (
    <img
      src={book.cover}
      alt={`${book.arabic} cover`}
      loading="lazy"
      decoding="async"
      referrerPolicy="no-referrer"
      onError={() => setFailed(true)}
    />
  );
}

export function BookShowcase({ compact = false }: { compact?: boolean }) {
  return (
    <div className={`showcase-grid ${compact ? "compact" : ""}`}>
      {SIX_BOOKS.map((book, index) => (
        <Link href={`/books/${book.id}`} className="showcase-card" key={book.id}>
          <div className="book-3d" style={{ ["--delay" as string]: `${index * 55}ms` }}>
            <div className="book-spine" />
            <div className="book-pages" />
            <BookCover book={book} />
            <div className="book-shine" />
          </div>
          <div className="showcase-info">
            <div className="showcase-index">0{book.id} · {book.short}</div>
            <div className="arabic showcase-arabic">{book.arabic}</div>
            <div className="showcase-english">{book.english}</div>
            <div className="showcase-author">{book.author}</div>
            <span className="open-book"><BookOpen size={14} /> Open collection <ArrowUpRight size={14} /></span>
          </div>
        </Link>
      ))}
    </div>
  );
}
