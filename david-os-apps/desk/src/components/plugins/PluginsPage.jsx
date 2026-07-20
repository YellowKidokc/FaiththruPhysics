import { useMemo, useState } from 'react';
import { Search, Check } from 'lucide-react';

const INSTALLED = {
  'Model tools': ['Web Browser', 'Code Sandbox'],
  MCP: ['Cloudflare Workers', 'Cloudflare Docs', 'Mermaid Chart', 'David OS Hub', 'SiYuan Notes'],
  Plugins: [
    'Yi Jing Reader', 'Render Highcharts', 'Mermaid Diagram', 'GPT Image Editor',
    'Web Search', 'Deep Research', 'Simple Calculator', 'Render Chart',
    'Web App Builder', 'DALL-E 3', 'Stable Diffusion v3 Image', 'Jina Grounding',
  ],
};

const STORE = [
  { id: 'calc', name: 'Simple Calculator', desc: 'Helps the assistant with precise math.', installed: true, group: 'Utility' },
  { id: 'webapp', name: 'Web App Builder', desc: 'Build simple web apps with HTML/CSS/JS.', installed: true, group: 'Builder' },
  { id: 'chart', name: 'Render Chart', desc: 'Visualize data by drawing charts.', installed: true, group: 'Viz' },
  { id: 'img', name: 'GPT Image Editor', desc: 'Generate and edit images with GPT Image.', installed: true, group: 'Image' },
  { id: 'research', name: 'Deep Research', desc: 'Multi-step research packets with citations.', installed: true, group: 'Research' },
  { id: 'perp', name: 'Perplexity Search', desc: 'Live web answers via Perplexity.', installed: true, group: 'Search' },
  { id: 'canvas', name: 'Interactive Canvas', desc: 'Forms and interactive canvases.', installed: true, group: 'Builder' },
  { id: 'sd3', name: 'Stable Diffusion v3 Image', desc: 'Image generation lane.', installed: true, group: 'Image' },
  { id: 'mermaid', name: 'Mermaid Diagram', desc: 'Generate diagrams with Mermaid.js.', installed: true, group: 'Viz' },
  { id: 'html', name: 'Render HTML', desc: 'Preview HTML snippets safely.', installed: true, group: 'Dev' },
  { id: 'firecrawl', name: 'Read Web Page (Firecrawl)', desc: 'Scrape and analyze web pages.', installed: true, group: 'Search' },
  { id: 'serp', name: 'Web Search (Serp)', desc: 'Real-time internet search.', installed: true, group: 'Search' },
  { id: 'sd2', name: 'Stable Diffusion v2 Image', desc: 'Earlier image generation lane.', installed: false, group: 'Image' },
  { id: 'slack', name: 'Slack Message Notifier', desc: 'Push notes into Slack.', installed: false, group: 'Comm' },
  { id: 'todo', name: 'Todo List', desc: 'Lightweight task list plugin.', installed: false, group: 'Utility' },
  { id: 'grok-img', name: 'Generate Image Grok', desc: 'xAI image generation.', installed: false, group: 'Image' },
];

export function PluginsPage() {
  const [q, setQ] = useState('');
  const [installed, setInstalled] = useState(() => Object.fromEntries(STORE.map((p) => [p.id, !!p.installed])));

  const list = useMemo(() => STORE.filter((p) => {
    if (!q) return true;
    return `${p.name} ${p.desc} ${p.group}`.toLowerCase().includes(q.toLowerCase());
  }), [q]);

  return (
    <section className="tm-page">
      <div className="tm-page-head">
        <div>
          <h1>Plugins</h1>
          <p>Store on the left, gallery on the right — same menu shape as TypingMind Plugins.</p>
        </div>
        <div className="tm-head-actions">
          <button type="button" className="btn-primary">Create plugin</button>
        </div>
      </div>

      <div className="plugins-layout">
        <aside className="plugins-side">
          <div className="group-title">Store</div>
          <button type="button" className="tm-nav-item on">Plugins</button>
          <button type="button" className="tm-nav-item">MCP connectors</button>
          <button type="button" className="tm-nav-item">Skills</button>

          {Object.entries(INSTALLED).map(([group, items]) => (
            <div key={group}>
              <div className="group-title">{group} ({items.length})</div>
              {items.map((name) => (
                <button key={name} type="button" className="installed-row">{name}</button>
              ))}
            </div>
          ))}
        </aside>

        <div>
          <div className="tm-toolbar">
            <div className="grow">
              <Search size={15} />
              <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search plugins" />
            </div>
          </div>
          <div className="tm-card-grid">
            {list.map((p) => (
              <article key={p.id} className="tm-card">
                <div className="tm-card-top">
                  <div className="tm-avatar">{p.name.slice(0, 2)}</div>
                  <div>
                    <h3>
                      {p.name}
                      {installed[p.id] && <Check size={14} color="var(--ok)" style={{ marginLeft: 8, verticalAlign: 'middle' }} />}
                    </h3>
                    <p>{p.desc}</p>
                  </div>
                </div>
                <div className="tm-card-foot">
                  <div className="tm-tags"><span>{p.group}</span></div>
                  <button
                    type="button"
                    className={installed[p.id] ? 'use-now' : 'btn-primary'}
                    style={installed[p.id] ? undefined : { padding: '6px 12px', borderRadius: 999, fontSize: 12 }}
                    onClick={() => setInstalled((s) => ({ ...s, [p.id]: !s[p.id] }))}
                  >
                    {installed[p.id] ? 'Installed' : 'Install'}
                  </button>
                </div>
              </article>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
