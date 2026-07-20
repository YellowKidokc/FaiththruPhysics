import { useState } from 'react';
import { Plus, Clock, Loader2, FolderPlus } from 'lucide-react';

const SAMPLE = [
  { id: '1', name: 'Wall notes.md', type: 'markdown' },
  { id: '2', name: 'Research packet.pdf', type: 'pdf' },
  { id: '3', name: 'Screenshot capture.png', type: 'image' },
  { id: '4', name: 'Meeting transcript', type: 'transcript' },
];

export function KnowledgePanel({ online }) {
  const [loading, setLoading] = useState(false);
  const [items, setItems] = useState([]);

  const addMemories = () => {
    setLoading(true);
    setTimeout(() => {
      setItems(SAMPLE);
      setLoading(false);
    }, 600);
  };

  return (
    <section className="tm-page" style={{ position: 'relative', minHeight: '70vh' }}>
      <div className="tm-page-head">
        <div>
          <h1>Knowledge Base</h1>
          <p>Connect data sources to create a knowledge base for your AI agents.</p>
        </div>
        <div className="tm-head-actions">
          <button type="button" className="btn-secondary">How it works</button>
        </div>
      </div>

      {loading && (
        <div className="kb-empty">
          <Loader2 size={28} className="spin" style={{ animation: 'spin 1s linear infinite' }} />
        </div>
      )}

      {!loading && items.length === 0 && (
        <div className="kb-empty">
          <FolderPlus size={40} strokeWidth={1.25} />
          <div>
            <b style={{ color: 'var(--text)' }}>No sources yet</b>
            <p style={{ margin: '6px 0 0' }}>
              {online ? 'Hub is reachable — attach folders, notes, or files.' : 'Hub offline — you can still stage local memories.'}
            </p>
          </div>
        </div>
      )}

      {!loading && items.length > 0 && (
        <div className="tm-card-grid">
          {items.map((f) => (
            <article key={f.id} className="tm-card" style={{ minHeight: 100 }}>
              <div className="tm-card-top">
                <div className="tm-avatar">{f.type.slice(0, 2).toUpperCase()}</div>
                <div>
                  <h3>{f.name}</h3>
                  <p>{f.type}</p>
                </div>
              </div>
            </article>
          ))}
        </div>
      )}

      <div className="kb-fab">
        <button type="button" className="add" onClick={addMemories}>
          <Plus size={14} /> Add Memories
        </button>
        <button type="button" className="clock" title="History">
          <Clock size={18} />
        </button>
      </div>

      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </section>
  );
}
