import { useMemo, useState } from 'react';
import { Search, Star, Copy, Pencil, Trash2, Check } from 'lucide-react';

const PROMPTS = [
  { id: 'p1', title: 'AA Lossless Summarization Meta-Prompt', blurb: 'Compress long threads without dropping claims, citations, or open questions.', tags: ['Meta', 'Summary'] },
  { id: 'p2', title: 'Content Analyzer Meta-Prompt', blurb: 'Score coherence, contradiction risk, and next-action clarity on any draft.', tags: ['Meta', 'Audit'] },
  { id: 'p3', title: 'Physics of Faith Framing', blurb: 'Translate a technical claim into the Master Equation vocabulary without losing rigor.', tags: ['Theophysics', 'Writing'] },
  { id: 'p4', title: 'Grant Paragraph Builder', blurb: 'Impact → evidence → ask. Templeton-ready tone.', tags: ['Grant', 'Templeton'] },
  { id: 'p5', title: 'Steel-man Opposition', blurb: 'Build the strongest counter-case before you answer.', tags: ['Debate'] },
  { id: 'p6', title: 'Code Review Strict', blurb: 'Bugs, perf, naming, tests — no fluff.', tags: ['Code', 'Review'] },
  { id: 'p7', title: 'Decision Matrix', blurb: 'Options × criteria × recommendation with kill conditions.', tags: ['Strategy'] },
  { id: 'p8', title: 'Workbook Quiz Generator', blurb: 'Turn a note into graded comprehension checks.', tags: ['QUIZ', 'Workbook'] },
  { id: 'p9', title: 'Python Notebook Scaffold', blurb: 'Cells, assertions, and a short README for reproducible runs.', tags: ['Python', 'Code'] },
];

export function PromptsPanel({ onCopyToComposer }) {
  const [q, setQ] = useState('');
  const [stars, setStars] = useState(() => new Set(['p1', 'p3']));
  const [copied, setCopied] = useState(null);
  const [sort, setSort] = useState('title');

  const list = useMemo(() => {
    const needle = q.trim().toLowerCase();
    let rows = PROMPTS.filter((p) => {
      if (!needle) return true;
      return [p.title, p.blurb, ...(p.tags || [])].join(' ').toLowerCase().includes(needle);
    });
    rows = [...rows].sort((a, b) => {
      if (sort === 'starred') return (stars.has(b.id) ? 1 : 0) - (stars.has(a.id) ? 1 : 0);
      return a.title.localeCompare(b.title);
    });
    return rows;
  }, [q, sort, stars]);

  const useNow = (p) => {
    const text = `${p.title}\n\n${p.blurb}`;
    onCopyToComposer?.(text);
    navigator.clipboard?.writeText?.(text).catch(() => {});
    setCopied(p.id);
    setTimeout(() => setCopied(null), 1200);
  };

  return (
    <section className="tm-page">
      <div className="tm-page-head">
        <div>
          <h1>Prompt Library</h1>
          <p>Reusable operators for the desk. Gold actions only — no blue chrome.</p>
        </div>
        <div className="tm-head-actions">
          <button type="button" className="btn-primary">Add prompt</button>
          <button type="button" className="btn-secondary">Browse prompts</button>
        </div>
      </div>

      <div className="tm-toolbar">
        <div className="grow">
          <Search size={15} />
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search your prompts" />
        </div>
        <select value={sort} onChange={(e) => setSort(e.target.value)} aria-label="Sort">
          <option value="title">Title</option>
          <option value="starred">Starred</option>
        </select>
      </div>

      <div className="tm-card-grid">
        {list.map((p) => (
          <article key={p.id} className="tm-card">
            <div className="tm-card-top">
              <div style={{ flex: 1, minWidth: 0 }}>
                <h3>{p.title}</h3>
                <p>{p.blurb}</p>
              </div>
              <div className="tm-tags" style={{ flexDirection: 'column', alignItems: 'flex-end' }}>
                {p.tags.map((t) => <span key={t}>{t}</span>)}
              </div>
            </div>
            <div className="tm-card-foot">
              <div className="icon-row">
                <button
                  type="button"
                  title="Favorite"
                  onClick={() => setStars((s) => {
                    const n = new Set(s);
                    if (n.has(p.id)) n.delete(p.id); else n.add(p.id);
                    return n;
                  })}
                >
                  <Star size={14} fill={stars.has(p.id) ? 'currentColor' : 'none'} color={stars.has(p.id) ? 'var(--gold)' : 'currentColor'} />
                </button>
                <button type="button" title="Copy" onClick={() => navigator.clipboard?.writeText?.(`${p.title}\n${p.blurb}`)}>
                  <Copy size={14} />
                </button>
                <button type="button" title="Edit"><Pencil size={14} /></button>
                <button type="button" title="Delete"><Trash2 size={14} /></button>
              </div>
              <button type="button" className="use-now" onClick={() => useNow(p)}>
                {copied === p.id ? <><Check size={12} /> Copied</> : 'Use now'}
              </button>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
