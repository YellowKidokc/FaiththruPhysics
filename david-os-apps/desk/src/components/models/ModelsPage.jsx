import { useMemo, useState } from 'react';
import { Search, Check } from 'lucide-react';

const PROVIDERS = [
  { id: 'all', label: 'All models', total: 895 },
  { id: 'openai', label: 'OpenAI', total: 26 },
  { id: 'anthropic', label: 'Anthropic', total: 13 },
  { id: 'google', label: 'Google', total: 23 },
  { id: 'openrouter', label: 'OpenRouter', total: 120 },
  { id: 'xai', label: 'xAI', total: 8 },
  { id: 'deepseek', label: 'Deepseek', total: 12 },
  { id: 'mistral', label: 'Mistral', total: 18 },
  { id: 'groq', label: 'Groq', total: 15 },
  { id: 'local', label: 'Local / Ollama', total: 4 },
];

const MODELS = [
  { id: 'claude-opus-4-6', name: 'Claude Opus 4.6', provider: 'anthropic', context: '1M', enabled: true, isDefault: true, desc: "Anthropic's most intelligent model for building agents and coding.", pricing: { in: '$5', out: '$25', cin: '$6.25', cout: '$0.50' }, features: ['Plugins', 'Vision', 'Prompt caching', 'System role', 'Streaming', 'Thinking mode'], tools: ['Web Browser', 'Code Sandbox'], cutoff: '2025-08-01', released: '2026-02-06' },
  { id: 'claude-opus-4-7', name: 'Claude Opus 4.7', provider: 'anthropic', context: '1M', enabled: true, desc: 'Next Opus lane for long-horizon agent work.', pricing: { in: '$5', out: '$25' }, features: ['Plugins', 'Vision', 'Streaming', 'Thinking mode'] },
  { id: 'gpt-5-4-pro', name: 'GPT-5.4 Pro', provider: 'openai', context: '1M', enabled: true, desc: 'Frontier OpenAI lane for complex professional synthesis.', pricing: { in: '$2.5', out: '$15' }, features: ['Plugins', 'Vision', 'System role', 'Streaming'] },
  { id: 'gpt-5-3-chat', name: 'GPT-5.3 Chat', provider: 'openai', context: '128K', enabled: true, desc: 'Fast chat-optimized GPT lane.', pricing: { in: '$1', out: '$5' }, features: ['Streaming', 'System role'] },
  { id: 'gemini-3-1-pro', name: 'Gemini 3.1 Pro', provider: 'google', context: '1M', enabled: true, desc: 'Google research / multimodal lane.', pricing: { in: 'configured', out: 'configured' }, features: ['Vision', 'Long context'] },
  { id: 'grok-4', name: 'Grok 4', provider: 'xai', context: '256K', enabled: true, desc: 'xAI general model.', pricing: { in: 'configured', out: 'configured' }, features: ['Streaming'] },
  { id: 'deepseek-2', name: 'DeepSeek 2', provider: 'deepseek', context: '128K', enabled: false, desc: 'Station / pipeline model — needs DEEPSEEK_API_KEY on 2828.', pricing: { in: 'configured', out: 'configured' }, features: ['Streaming'] },
  { id: 'ollama-local', name: 'Ollama Local', provider: 'local', context: '128K', enabled: false, desc: 'Private local inference when the NAS endpoint is up.', pricing: { in: 'local', out: 'local' }, features: ['Local', 'Private'] },
];

export function ModelsPage() {
  const [provider, setProvider] = useState('anthropic');
  const [q, setQ] = useState('');
  const [enabled, setEnabled] = useState(() => Object.fromEntries(MODELS.map((m) => [m.id, !!m.enabled])));
  const [selectedId, setSelectedId] = useState('claude-opus-4-6');

  const counts = useMemo(() => {
    const map = { all: 0 };
    MODELS.forEach((m) => {
      map.all += enabled[m.id] ? 1 : 0;
      map[m.provider] = (map[m.provider] || 0) + (enabled[m.id] ? 1 : 0);
    });
    return map;
  }, [enabled]);

  const list = MODELS.filter((m) => {
    if (provider !== 'all' && m.provider !== provider) return false;
    if (!q) return true;
    return `${m.name} ${m.desc}`.toLowerCase().includes(q.toLowerCase());
  });

  const selected = MODELS.find((m) => m.id === selectedId) || list[0] || MODELS[0];

  return (
    <section className="tm-page">
      <div className="tm-page-head">
        <div>
          <h1>Models</h1>
          <p>Providers on the left, catalog in the middle, detail on the right — TypingMind layout, black/gold chrome.</p>
        </div>
        <div className="tm-head-actions">
          <button type="button" className="btn-primary">Add custom model</button>
        </div>
      </div>

      <div className="tm-tri">
        <aside className="tm-pane">
          {PROVIDERS.map((p) => (
            <button
              key={p.id}
              type="button"
              className={`tm-provider ${provider === p.id ? 'on' : ''}`}
              onClick={() => setProvider(p.id)}
            >
              <b>{p.label}</b>
              <small>{counts[p.id] || 0} / {p.total}</small>
            </button>
          ))}
        </aside>

        <section className="tm-pane">
          <div className="tm-toolbar" style={{ marginBottom: 10 }}>
            <div className="grow">
              <Search size={15} />
              <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search models" />
            </div>
          </div>
          {list.map((m) => (
            <button
              key={m.id}
              type="button"
              className={`tm-model-row ${selected?.id === m.id ? 'on' : ''}`}
              onClick={() => setSelectedId(m.id)}
            >
              <span>{enabled[m.id] ? <Check size={14} color="var(--ok)" /> : <span style={{ width: 14 }} />}</span>
              <span>
                <b>{m.name}</b>
                {m.isDefault && <span className="badge" style={{ marginLeft: 8 }}>Default</span>}
              </span>
              <span className="ctx">{m.context}</span>
              <span
                className={`toggle ${enabled[m.id] ? 'on' : ''}`}
                role="switch"
                aria-checked={!!enabled[m.id]}
                onClick={(e) => {
                  e.stopPropagation();
                  setEnabled((s) => ({ ...s, [m.id]: !s[m.id] }));
                }}
              />
            </button>
          ))}
        </section>

        <aside className="tm-pane tm-detail">
          {selected && (
            <>
              <h2>
                {selected.name}
                {selected.isDefault && <span className="badge">Default</span>}
              </h2>
              <p style={{ color: 'var(--text-dim)', marginTop: 0 }}>{selected.desc}</p>
              <div className="tm-meta">
                <div><span className="k">Model ID</span><code>{selected.id}</code></div>
                <div><span className="k">Context</span><span>{selected.context}</span></div>
                {selected.released && <div><span className="k">Release</span><span>{selected.released}</span></div>}
                {selected.cutoff && <div><span className="k">Cutoff</span><span>{selected.cutoff}</span></div>}
                {selected.pricing && (
                  <div>
                    <span className="k">Pricing / 1M</span>
                    <span>In {selected.pricing.in} · Out {selected.pricing.out}</span>
                  </div>
                )}
              </div>
              <h3 style={{ fontSize: 13, color: 'var(--text-mute)', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Features</h3>
              <div className="tm-feat">
                {(selected.features || []).map((f) => (
                  <label key={f}><Check size={14} color="var(--ok)" /> {f}</label>
                ))}
              </div>
              {selected.tools?.length > 0 && (
                <>
                  <h3 style={{ fontSize: 13, color: 'var(--text-mute)', textTransform: 'uppercase', letterSpacing: '0.1em', marginTop: 16 }}>Provider tools</h3>
                  <div className="tm-tags" style={{ marginTop: 8 }}>
                    {selected.tools.map((t) => <span key={t}>{t}</span>)}
                  </div>
                </>
              )}
            </>
          )}
        </aside>
      </div>
    </section>
  );
}
