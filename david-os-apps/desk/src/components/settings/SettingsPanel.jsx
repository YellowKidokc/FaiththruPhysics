import { useState } from 'react';
import { topOfMindApi } from '../../lib/api/topOfMindApi';

const NAV = {
  'Account & Data': ['App Data & Storage', 'Cloud Sync & Backup', 'API Keys', 'License Key'],
  Preferences: ['General', 'Appearance', 'Keyboard Shortcuts', 'Text-to-speech', 'Voice Input'],
  'Advanced Settings': ['Model Context Protocol', 'Internal prompts', 'Extensions', 'Proxy & Org ID', 'Integrations'],
};

export function SettingsPanel({ online, setOnline, notice, setNotice }) {
  const [section, setSection] = useState('App Data & Storage');
  const [url, setUrl] = useState(topOfMindApi.baseUrl);

  async function test() {
    topOfMindApi.setBaseUrl(url);
    try {
      await topOfMindApi.test();
      setOnline(true);
      setNotice?.('Connection ok');
    } catch (e) {
      setOnline(false);
      setNotice?.(e.message || 'Failed to load sources');
    }
  }

  return (
    <div className="tm-settings">
      <nav className="tm-settings-nav" aria-label="Settings">
        {Object.entries(NAV).map(([group, items]) => (
          <div key={group}>
            <h4>{group}</h4>
            {items.map((item) => (
              <button
                key={item}
                type="button"
                className={`tm-nav-item ${section === item ? 'on' : ''}`}
                onClick={() => setSection(item)}
              >
                {item}
              </button>
            ))}
          </div>
        ))}
      </nav>

      <div className="tm-settings-body">
        {section === 'App Data & Storage' && (
          <>
            <h1>App Data & Storage</h1>
            <p className="lead">→ Click to calculate your data usage</p>
            <div className="settings-actions">
              <button type="button" className="btn-primary">Export</button>
              <button type="button" className="btn-primary">Import</button>
              <button type="button" className="btn-danger">Delete All Local Data</button>
              <button type="button" className="btn-secondary">Import From OpenAI</button>
            </div>
            <div className="integ-card">
              <b>Archived Chats</b>
              <button type="button" className="btn-secondary" style={{ width: 'fit-content' }}>View Archived Chats</button>
            </div>
            <div className="integ-card">
              <b>Shared Data</b>
              <button type="button" className="btn-secondary" style={{ width: 'fit-content' }}>Manage Shared Links</button>
            </div>
            <div className="integ-card">
              <b>Storage stats</b>
              <p className="muted">All of your data is stored locally in your browser (and optionally synced via the hub).</p>
              <div>
                <div className="storage-row"><span>Local Storage: 0.20 MB (3.94%)</span><span>Limit: 5.00 MB</span></div>
                <div className="storage-bar"><span style={{ width: '4%' }} /></div>
              </div>
              <div>
                <div className="storage-row"><span>IndexedDB: 178.08 MB</span><span>Limit: 10.92 GB</span></div>
                <div className="storage-bar"><span style={{ width: '2%' }} /></div>
              </div>
              <p style={{ color: 'var(--bad)', fontSize: 13 }}>Please export and backup your chats regularly to avoid data lost.</p>
            </div>
          </>
        )}

        {(section === 'API Keys' || section === 'Integrations' || section === 'General') && (
          <>
            <h1>{section === 'Integrations' ? 'Settings & Integrations' : section}</h1>
            <p className="lead">Top of Mind · Multi-AI command desk · API port 10000</p>
            <div className="integ-card">
              <b>BASE URL</b>
              <div className="api-row">
                <input value={url} onChange={(e) => setUrl(e.target.value)} placeholder="http://127.0.0.1:10000" />
                <button type="button" className="btn-primary" onClick={() => { topOfMindApi.setBaseUrl(url); test(); }}>Save</button>
                <button type="button" className="btn-secondary" onClick={test}>Test Connection</button>
                <span className={`status-pill ${online ? 'ok' : 'bad'}`}>{online ? 'online' : 'offline'}</span>
              </div>
              <small className="muted">Override with env: VITE_TOP_OF_MIND_API</small>
            </div>
            <div className="integ-card">
              <header><b>Syncthing</b><span className="active">Active</span></header>
              <span className="muted">http://127.0.0.1:8384</span>
              <div className="inline">
                <button type="button" className="btn-secondary">status</button>
                <button type="button" className="btn-secondary">folders</button>
                <button type="button" className="btn-secondary">refresh</button>
                <button type="button" className="btn-secondary">web-ui</button>
              </div>
            </div>
            {['Synology', 'Cloudflare R2', 'AutoHotkey Bridge'].map((name) => (
              <div key={name} className="integ-card">
                <header><b>{name}</b><span className="muted">Not configured</span></header>
              </div>
            ))}
            {notice && <p className="muted">{notice}</p>}
          </>
        )}

        {section === 'Appearance' && (
          <>
            <h1>Appearance</h1>
            <p className="lead">Black desk · gold accents. Blue chrome is retired.</p>
            <div className="integ-card">
              <b>Theme</b>
              <span className="muted">Fixed: charcoal background, gold primary actions.</span>
            </div>
          </>
        )}

        {section === 'Model Context Protocol' && (
          <>
            <h1>Model Context Protocol</h1>
            <p className="lead">Local MCP Hub defaults to http://127.0.0.1:8787</p>
            <div className="integ-card">
              <b>david_os</b>
              <span className="muted">stdio · mcp-hub-stdio · SiYuan + remote MCP proxy</span>
            </div>
          </>
        )}

        {!['App Data & Storage', 'API Keys', 'Integrations', 'General', 'Appearance', 'Model Context Protocol'].includes(section) && (
          <>
            <h1>{section}</h1>
            <p className="lead">Menu placeholder matching TypingMind’s settings tree. Wire controls here next.</p>
          </>
        )}
      </div>
    </div>
  );
}
