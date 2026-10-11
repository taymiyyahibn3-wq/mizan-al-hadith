"use client";

import { BookOpen, Home, Info, Library, Mail, Menu, Search, Users, X } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

export function SiteChrome({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);

  const close = () => setOpen(false);

  return (
    <main className="site-shell">
      <header className="topbar">
        <div className="container nav">
          <button className="icon-btn" onClick={() => setOpen(true)} aria-label="Open navigation menu">
            <Menu size={22} />
          </button>
          <Link href="/" className="brand" aria-label="Mīzān al-Hadīth home">
            <span className="brand-mark"><BookOpen size={21} /></span>
            <span>Mīzān al-Hadīth</span>
          </Link>
          <Link href="/books" className="nav-link"><Library size={16} /> Library</Link>
        </div>
      </header>

      {open && (
        <div className="drawer-backdrop" onClick={close}>
          <aside className="drawer" onClick={(e) => e.stopPropagation()}>
            <div className="drawer-head">
              <Link href="/" className="brand" onClick={close}>
                <span className="brand-mark"><BookOpen size={19} /></span>Mīzān
              </Link>
              <button className="icon-btn" onClick={close} aria-label="Close navigation menu"><X size={20} /></button>
            </div>

            <nav className="drawer-nav" aria-label="Main navigation">
              <Link href="/" onClick={close}><Home size={18} /> Home</Link>
              <Link href="/books" onClick={close}><Library size={18} /> Hadith Library</Link>
              <Link href="/narrators" onClick={close}><Users size={18} /> Narrators</Link>
              <Link href="/search" onClick={close}><Search size={18} /> Search</Link>
              <Link href="/info" onClick={close}><Info size={18} /> Info</Link>
              <Link href="/contact" onClick={close}><Mail size={18} /> Contact</Link>
            </nav>

            <div className="drawer-note">
              Explore hadith collections, isnād chains, narrator biographies, scholarly grades and related topics.
            </div>
          </aside>
        </div>
      )}

      {children}
    </main>
  );
}

export function PageHeader({ title, subtitle, backHref = "/" }: { title: string; subtitle?: string; backHref?: string }) {
  return (
    <section className="page-hero">
      <div className="container">
        <div className="section-kicker">MĪZĀN AL-HADĪTH</div>
        <h1>{title}</h1>
        {subtitle && <p>{subtitle}</p>}
        {backHref !== undefined && <Link href={backHref} className="text-back">← Back</Link>}
      </div>
    </section>
  );
}
