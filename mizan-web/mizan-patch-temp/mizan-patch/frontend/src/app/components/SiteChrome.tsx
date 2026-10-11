"use client";

import { BookOpen, Home, Info, Library, Mail, Menu, Search, Users, X } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

export function SiteChrome({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);

  const close = () => setOpen(false);

  useEffect(() => {
    if (!open) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") close();
    };
    document.addEventListener("keydown", onKeyDown);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKeyDown);
      document.body.style.overflow = "";
    };
  }, [open]);

  return (
    <main className="site-shell">
      <a className="skip-link" href="#main-content">Skip to content</a>
      <header className="topbar">
        <div className="container nav">
          <button className="icon-btn menu-trigger" onClick={() => setOpen(true)} aria-label="Open navigation menu" aria-expanded={open}>
            <Menu size={21} />
          </button>

          <Link href="/" className="brand" aria-label="Mīzān al-Hadīth home">
            <span className="brand-mark"><BookOpen size={20} /></span>
            <span className="brand-copy">
              <strong>Mīzān al-Hadīth</strong>
              <small>Hadith Research Library</small>
            </span>
          </Link>

          <nav className="desktop-nav" aria-label="Primary navigation">
            <Link href="/books"><Library size={15} /> Library</Link>
            <Link href="/search"><Search size={15} /> Search</Link>
            <Link href="/narrators"><Users size={15} /> Narrators</Link>
          </nav>
        </div>
      </header>

      {open && (
        <div className="drawer-backdrop" onClick={close} role="presentation">
          <aside className="drawer" onClick={(e) => e.stopPropagation()} aria-label="Navigation drawer">
            <div className="drawer-head">
              <Link href="/" className="brand" onClick={close}>
                <span className="brand-mark"><BookOpen size={18} /></span>
                <span className="brand-copy"><strong>Mīzān</strong><small>Research Library</small></span>
              </Link>
              <button className="icon-btn" onClick={close} aria-label="Close navigation menu"><X size={20} /></button>
            </div>

            <nav className="drawer-nav" aria-label="Main navigation">
              <Link href="/" onClick={close}><Home size={18} /> Home</Link>
              <Link href="/books" onClick={close}><Library size={18} /> Hadith Library</Link>
              <Link href="/search" onClick={close}><Search size={18} /> Search Hadith</Link>
              <Link href="/narrators" onClick={close}><Users size={18} /> Narrators</Link>
              <Link href="/info" onClick={close}><Info size={18} /> About Mīzān</Link>
              <Link href="/contact" onClick={close}><Mail size={18} /> Contact</Link>
            </nav>

            <div className="drawer-note">
              Search Arabic hadith text, browse the Six Books, follow isnād chains and inspect narrator and scholarly data.
            </div>
          </aside>
        </div>
      )}

      <div id="main-content">{children}</div>
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
