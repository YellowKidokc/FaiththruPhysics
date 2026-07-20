import { useMemo, useState } from 'react';
import { Search, Copy, Pencil, Share2, Trash2, Pin } from 'lucide-react';

const CATEGORIES = [
  'Uncategorized',
  'Education',
  'Faith',
  'Physics',
  'Excel',
  'Coding',
  'Research',
];

const AGENTS = [
  { id: 'truth', name: 'Truth', category: 'Uncategorized', desc: 'Contradiction hunter. Quiet until invited; then ruthless about claims vs evidence.', initials: 'Tr' },
  { id: 'gemini', name: 'Gemini the one', category: 'Uncategorized', desc: 'Long-context research partner for notebooks, sources, and synthesis.', initials: 'Ge' },
  { id: 'life', name: 'Life Coach Claude', category: 'Uncategorized', desc: "I'm your personal insight companion, David — video analysis and daily framing.", initials: 'LC' },
  { id: 'academic', name: 'Academic Researcher', category: 'Education', desc: 'Paper structure, citations, and grant-ready prose without fluff.', initials: 'AR' },
  { id: 'pof', name: 'The Physics of Faith Guide', category: 'Faith', desc: 'THE PHYSICS OF FAITH: unify knowledge under the Master Equation framework.', initials: 'PF' },
  { id: 'coder', name: 'Pro Coder', category: 'Coding', desc: 'Write code without overexplaining. Internal knowledge only unless tools are on.', initials: 'PC' },
  { id: 'logos', name: 'LOGOS', category: 'Research', desc: 'Reflective analytical lane for axiom checks and definitional clarity.', initials: 'LG' },
  { id: 'theo', name: 'Unassigned AI THEOPHYSICS Research', category: 'Physics', desc: 'Research partner for Master Equation work and quantum-consciousness notes.', initials: 'Th' },
  { id: 'plugin-gen', name: 'TypingMind Plugin Generator', category: 'Uncategorized', desc: 'Scaffold plugins carefully. Prefer one canonical generator — no duplicate blue twin.', initials: 'PG' },
];

export function AgentsPage({ onChat, sources = [] }) {
  const [cat, setCat] = useState('Uncategorized');
  const [q, setQ] = useState('');

  const live = useMemo(() => {
    const fromApi = (sources || []).slice(0, 6).map((s, i) => ({
      id: `src-${s.id || s.name || i}`,
      name: s.name || s.label || s.id,
      category: 'Uncategorized',
      desc: `Live hub source · status ${s.status || 'online'}`,
      initials: String(s.name || s.id || '?').slice(0, 2).toUpperCase(),
      live: true,
    }));
    return [...fromApi, ...AGENTS];
  }, [sources]);

  const visible = live.filter((a) => {
    const inCat = cat === 'All' || a.category === cat;
    const hay = `${a.name} ${a.desc}`.toLowerCase();
    return inCat && (!q || hay.includes(q.toLowerCase()));
  });

  const byCat = CATEGORIES.map((c) => ({
    name: c,
    count: live.filter((a) => a.category === c).length,
  }));

  return (
    <section className="tm-page" style={{ display: 'grid', gridTemplateColumns: '220px 1fr', gap: 18, alignItems: 'start' }}>
      <aside className="plugins-side">
        <div className="group-title">Categories</div>
        <button type="button" className={`tm-nav-item ${cat === 'All' ? 'on' : ''}`} onClick={() => setCat('All')}>
          All agents <small>{live.length}</small>
        </button>
        {byCat.map((c) => (
          <button key={c.name} type="button" className={`tm-nav-item ${cat === c.name ? 'on' : ''}`} onClick={() => setCat(c.name)}>
            {c.name} <small>{c.count}</small>
          </button>
        ))}
      </aside>

      <div>
        <div className="tm-page-head">
          <div>
            <h1>Your AI agents</h1>
            <p>Working identities for the black desk. One card per role — no duplicate blue twins.</p>
          </div>
          <div className="tm-head-actions">
            <button type="button" className="btn-primary">Create AI agent</button>
            <button type="button" className="btn-secondary">Browse agents</button>
          </div>
        </div>

        <div className="tm-toolbar">
          <div className="grow">
            <Search size={15} />
            <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search AI agents…" />
          </div>
          <select defaultValue="title" aria-label="Sort">
            <option value="title">Title</option>
          </select>
        </div>

        {CATEGORIES.filter((c) => cat === 'All' || cat === c).map((section) => {
          const items = visible.filter((a) => a.category === section);
          if (!items.length) return null;
          return (
            <div key={section} style={{ marginBottom: 22 }}>
              <h2 style={{ fontSize: 14, color: 'var(--text-mute)', letterSpacing: '0.08em', textTransform: 'uppercase' }}>{section}</h2>
              <div className="tm-card-grid" style={{ marginTop: 10 }}>
                {items.map((a) => (
                  <article key={a.id} className="tm-card">
                    <div className="tm-card-top">
                      <div className="tm-avatar">{a.initials}</div>
                      <div style={{ minWidth: 0 }}>
                        <h3>{a.name}</h3>
                        <p>{a.desc}</p>
                      </div>
                    </div>
                    <div className="tm-card-foot">
                      <div className="icon-row">
                        <button type="button" title="Copy"><Copy size={14} /></button>
                        <button type="button" title="Edit"><Pencil size={14} /></button>
                        <button type="button" title="Share"><Share2 size={14} /></button>
                        <button type="button" title="Delete"><Trash2 size={14} /></button>
                        <button type="button" title="Pin"><Pin size={14} /></button>
                      </div>
                      <button type="button" className="use-now" onClick={() => onChat?.(a)}>Chat now</button>
                    </div>
                  </article>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
