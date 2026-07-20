/**
 * Top of Mind Desk — TypingMind-shaped menus, black/gold chrome.
 * Purpose: match apps/Pics menu layout (rail, sidebars, card pages).
 * Date: 2026-07-20 | codex/cursor | TESTED: build
 */
import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { NUMBERING, topOfMindApi } from './lib/api/topOfMindApi';
import { Rail } from './components/tm/Rail';
import { ChatsSide } from './components/tm/ChatsSide';
import { PromptsPanel } from './components/prompts/PromptsPanel';
import { AgentsPage } from './components/agents/AgentsPage';
import { ModelsPage } from './components/models/ModelsPage';
import { PluginsPage } from './components/plugins/PluginsPage';
import { KnowledgePanel } from './components/knowledge/KnowledgePanel';
import { SettingsPanel } from './components/settings/SettingsPanel';
import { ClipboardWorkspace } from './components/ClipboardWorkspace';
import { Paperclip, Mic, Send, Volume2 } from 'lucide-react';
import './theme.css';

const ACTIVE_AGENT_KEY = 'topOfMind.activeAgentId';
const CUSTOM_AGENTS_KEY = 'topOfMind.customAgents.v1';
const COMMAND_FAVORITES_KEY = 'topOfMind.commandFavorites.v1';
const COMMAND_RECENTS_KEY = 'topOfMind.commandRecents.v1';

const fallbackSources = [
  { id: 'clipboard', name: 'Clipboard', status: 'online', source_code: NUMBERING.sources.clipboard },
  { id: 'ahk', name: 'AutoHotkey', status: 'online', source_code: NUMBERING.sources.ahk },
  { id: 'codex', name: 'Codex', status: 'online', source_code: NUMBERING.sources.codex },
  { id: 'kimi', name: 'Kimi CLI', status: 'online', source_code: NUMBERING.sources.kimi },
  { id: 'claude', name: 'Claude', status: 'online', source_code: NUMBERING.sources.claude },
  { id: 'gemini', name: 'Gemini', status: 'online', source_code: NUMBERING.sources.gemini },
  { id: 'cursor', name: 'Cursor', status: 'online', source_code: NUMBERING.sources.cursor },
];

const starterFolders = [
  {
    id: 'local-inbox',
    name: 'Codex smoke folder',
    folder_code: NUMBERING.folders.inbox,
    children: [{ id: 'local-active', name: 'Active', folder_code: NUMBERING.folders.active }],
  },
];

const srcName = (s) => s?.name || s?.label || s?.source_id || s?.id || 'source';
const srcId = (s) => s?.id || s?.source_id || s?.name || s?.label;
const arr = (d, key) => (Array.isArray(d) ? d : d?.[key] || []);

function CommandPalette({ open, onClose, setActive, setInput, sources, folders, setNotice }) {
  const [query, setQuery] = useState('');
  const [cursor, setCursor] = useState(0);
  const [favorites, setFavorites] = useState(() => {
    try { return JSON.parse(localStorage.getItem(COMMAND_FAVORITES_KEY) || '[]'); } catch { return []; }
  });
  const [recents, setRecents] = useState(() => {
    try { return JSON.parse(localStorage.getItem(COMMAND_RECENTS_KEY) || '[]'); } catch { return []; }
  });

  const actions = useMemo(() => {
    const staticActions = [
      { id: 'nav.chats', title: 'Open chats', description: 'Message wall and composer', category: 'Navigation', handler: () => setActive('chats') },
      { id: 'nav.agents', title: 'Open agents', description: 'Agent library', category: 'Navigation', handler: () => setActive('agents') },
      { id: 'nav.prompts', title: 'Open prompts', description: 'Prompt library', category: 'Navigation', handler: () => setActive('prompts') },
      { id: 'nav.plugins', title: 'Open plugins', description: 'Plugin store', category: 'Navigation', handler: () => setActive('plugins') },
      { id: 'nav.models', title: 'Open models', description: 'Model catalog', category: 'Navigation', handler: () => setActive('models') },
      { id: 'nav.kb', title: 'Open knowledge base', description: 'KB / memories', category: 'Navigation', handler: () => setActive('memory') },
      { id: 'nav.settings', title: 'Open settings', description: 'API + storage', category: 'Navigation', handler: () => setActive('settings') },
      { id: 'nav.clipboard', title: 'Open clipboard', description: 'Clipboard workspace', category: 'Navigation', handler: () => setActive('clipboard') },
      { id: 'nav.operator', title: 'Open operator', description: 'Review-gated actions', category: 'Navigation', handler: () => setActive('operator') },
      { id: 'nav.markdown', title: 'Open markdown workspace', description: 'Notes editor', category: 'Navigation', handler: () => setActive('markdown') },
    ];
    const sourceActions = (sources || []).map((source) => ({
      id: `agent.${srcId(source)}`,
      title: `Chat with ${srcName(source)}`,
      description: 'Focus this source in chats',
      category: 'Agents',
      handler: () => { setActive('chats'); setNotice?.(`Active source: ${srcName(source)}`); },
    }));
    const folderActions = (folders || []).map((folder) => ({
      id: `folder.${folder.id || folder.name}`,
      title: `Open folder ${folder.name}`,
      description: 'Folder from workspace tree',
      category: 'Folders',
      handler: () => setNotice?.(`Folder: ${folder.name}`),
    }));
    return [...staticActions, ...sourceActions, ...folderActions];
  }, [sources, folders, setActive, setNotice]);

  const matches = useMemo(() => {
    const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    return actions
      .filter((action) => {
        const hay = `${action.title} ${action.description} ${action.category}`.toLowerCase();
        return terms.every((t) => hay.includes(t));
      })
      .sort((a, b) => favorites.includes(b.id) - favorites.includes(a.id) || recents.indexOf(a.id) - recents.indexOf(b.id));
  }, [actions, query, favorites, recents]);

  useEffect(() => {
    if (!open) return undefined;
    const onKey = (event) => {
      if (event.key === 'Escape') onClose();
      if (event.key === 'ArrowDown') { event.preventDefault(); setCursor((v) => Math.min(v + 1, matches.length - 1)); }
      if (event.key === 'ArrowUp') { event.preventDefault(); setCursor((v) => Math.max(v - 1, 0)); }
      if (event.key === 'Enter' && matches[cursor]) {
        event.preventDefault();
        const action = matches[cursor];
        action.handler();
        const next = [action.id, ...recents.filter((id) => id !== action.id)].slice(0, 10);
        setRecents(next);
        localStorage.setItem(COMMAND_RECENTS_KEY, JSON.stringify(next));
        onClose();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, matches, cursor, onClose, recents]);

  if (!open) return null;
  return (
    <div className="command-backdrop" role="dialog" aria-modal="true">
      <div className="command-palette">
        <input
          autoFocus
          value={query}
          onChange={(e) => { setQuery(e.target.value); setCursor(0); }}
          placeholder="Search chats, agents, prompts, plugins, models, KB, settings…"
        />
        <div className="command-list">
          {matches.map((action, index) => (
            <div
              key={action.id}
              className={`command-row ${index === cursor ? 'active' : ''}`}
              onMouseEnter={() => setCursor(index)}
              onClick={() => {
                action.handler();
                const next = [action.id, ...recents.filter((id) => id !== action.id)].slice(0, 10);
                setRecents(next);
                localStorage.setItem(COMMAND_RECENTS_KEY, JSON.stringify(next));
                onClose();
              }}
            >
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  const next = favorites.includes(action.id)
                    ? favorites.filter((id) => id !== action.id)
                    : [...favorites, action.id];
                  setFavorites(next);
                  localStorage.setItem(COMMAND_FAVORITES_KEY, JSON.stringify(next));
                }}
              >
                {favorites.includes(action.id) ? '★' : '☆'}
              </button>
              <div>
                <b>{action.title}</b>
                <p>{action.description}</p>
                <small>{action.category}</small>
              </div>
            </div>
          ))}
          {!matches.length && <div className="command-row"><div><b>No matches</b></div></div>}
        </div>
      </div>
    </div>
  );
}

function ChatsHome({ sources, onPick }) {
  const cards = (sources.length ? sources : fallbackSources).slice(0, 8);
  return (
    <div className="chats-home">
      <div className="chats-brand">
        <div className="logo">ToM</div>
        <h1>Top of Mind</h1>
        <p>Your unified AI command desk. All your agents in one surface — TypingMind menus, black/gold chrome.</p>
      </div>
      <div className="tm-side-section" style={{ margin: '0 0 12px' }}>Your AI agents</div>
      <div className="agent-home-grid">
        {cards.map((s) => (
          <button key={srcId(s)} type="button" className="agent-home-card" onClick={() => onPick(s)}>
            <div className="tm-avatar">{srcName(s).slice(0, 2).toUpperCase()}</div>
            <h3>{srcName(s)}</h3>
            <p>{s.status || 'online'} · tap to focus this lane in the wall</p>
          </button>
        ))}
      </div>
    </div>
  );
}

function MessageWall({ messages, online, selectedSource, input, setInput, onSend, apiBase }) {
  return (
    <div className="chat-wall">
      <div className="chat-wall-head">
        <div>
          <h2>All Messages</h2>
          <span>{messages.length} messages</span>
        </div>
        <div className="inline">
          <button type="button" className="btn-secondary"><Volume2 size={14} /> Read aloud</button>
          <button type="button" className="btn-secondary">Clear selection</button>
        </div>
      </div>
      <div className="chat-wall-body">
        {!messages.length && (
          <div className="kb-empty">
            <div className="tm-avatar lg">🤖</div>
            <div>
              <b style={{ color: 'var(--text)' }}>Welcome to Top of Mind</b>
              <p>Start typing below to send a message through the API.</p>
            </div>
          </div>
        )}
        {messages.map((m) => {
          const id = m.id || m.message_id || m.created_at;
          return (
            <article key={id} className="msg">
              <header>
                <b>{m.source_label || m.source_id || m.source || 'Source'}</b>
                <span>{m.created_at || m.timestamp || ''}</span>
              </header>
              <p>{m.body || m.content || m.text || m.message || JSON.stringify(m)}</p>
            </article>
          );
        })}
      </div>
      <div className="chat-composer-bar">
        <div className="composer-box">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message… (Shift + Enter for new line)"
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                onSend();
              }
            }}
          />
          <div className="composer-actions">
            <div className="left">
              <button type="button" title="Attach"><Paperclip size={16} /></button>
              <button type="button" title="Voice"><Mic size={16} /></button>
            </div>
            <div className="right">
              <button type="button" className="send" onClick={onSend}><Send size={14} /> Send</button>
            </div>
          </div>
        </div>
        <div className="composer-meta">
          <span>API: {apiBase} · source: {srcName(selectedSource)}</span>
          <span className={online ? 'status ok' : 'status bad'}>{online ? '● online' : '○ offline'}</span>
        </div>
      </div>
    </div>
  );
}

function OperatorPage({ setNotice }) {
  const [action, setAction] = useState('write');
  const [path, setPath] = useState('/path/to/file.txt');
  const [content, setContent] = useState('');
  const [review, setReview] = useState(true);

  return (
    <section className="tm-page op-page">
      <h1 style={{ marginTop: 0 }}>Operator</h1>
      <div className="op-actions">
        {['write', 'append', 'command', 'delete'].map((a) => (
          <button key={a} type="button" className={action === a ? 'on' : ''} onClick={() => setAction(a)}>
            {a[0].toUpperCase() + a.slice(1)}
          </button>
        ))}
      </div>
      <div className="op-form">
        <label>File path<input value={path} onChange={(e) => setPath(e.target.value)} /></label>
        <label>Content<textarea value={content} onChange={(e) => setContent(e.target.value)} placeholder="Enter file content…" /></label>
        <label style={{ textTransform: 'none', letterSpacing: 0, display: 'flex', alignItems: 'center', gap: 8 }}>
          <input type="checkbox" checked={review} onChange={(e) => setReview(e.target.checked)} />
          Require review before executing
        </label>
        <button
          type="button"
          className="op-queue"
          onClick={() => setNotice(review
            ? `Queued dry-run ${action} → ${path} (review required)`
            : `Draft only — wire to /operator/file-actions for ${action}`)}
        >
          Queue Action
        </button>
      </div>
    </section>
  );
}

function MarkdownPage({ setNotice }) {
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('# start writing markdown...\n\n*italic*, **bold**, `code`, and more.');
  return (
    <div className="md-workspace">
      <div className="md-toolbar">
        <b>Markdown Workspace</b>
        <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Note title…" />
        <select defaultValue=""><option value="">No folder</option><option>Codex smoke folder</option></select>
        <label className="inline" style={{ color: 'var(--text-mute)', fontSize: 12 }}>
          <input type="checkbox" /> Embed after save
        </label>
        <span style={{ flex: 1 }} />
        <button type="button" className="btn-secondary">Preview</button>
        <button type="button" className="btn-secondary">Copy</button>
        <button type="button" className="btn-secondary">Attach</button>
        <button type="button" className="btn-primary" onClick={() => setNotice(`Saved draft: ${title || 'untitled'}`)}>Save</button>
      </div>
      <div className="md-split">
        <textarea value={body} onChange={(e) => setBody(e.target.value)} />
        <div className="md-preview">{body || 'Preview will appear here.'}</div>
      </div>
    </div>
  );
}

function TeamsPage() {
  return (
    <section className="tm-page">
      <div className="tm-page-head">
        <div>
          <h1>Teams</h1>
          <p>TypingMind Teams menu slot — shared desks and agent packs land here.</p>
        </div>
        <button type="button" className="btn-primary">Create team</button>
      </div>
      <div className="kb-empty"><p>No teams yet.</p></div>
    </section>
  );
}

function App() {
  const [sources, setSources] = useState(fallbackSources);
  const [folders, setFolders] = useState(starterFolders);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [active, setActive] = useState('chats');
  const [selectedFolder, setSelectedFolder] = useState(starterFolders[0]);
  const [online, setOnline] = useState(false);
  const [notice, setNotice] = useState('');
  const [sideSearch, setSideSearch] = useState('');
  const [showWall, setShowWall] = useState(false);
  const [commandOpen, setCommandOpen] = useState(false);
  const [activeAgentId, setActiveAgentIdState] = useState(() => localStorage.getItem(ACTIVE_AGENT_KEY) || 'kimi');

  const setActiveAgentId = (id) => {
    setActiveAgentIdState(id);
    localStorage.setItem(ACTIVE_AGENT_KEY, id);
  };

  useEffect(() => {
    const onKey = (event) => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault();
        setCommandOpen(true);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  useEffect(() => {
    topOfMindApi.getSources()
      .then((d) => {
        const s = arr(d, 'sources');
        const custom = JSON.parse(localStorage.getItem(CUSTOM_AGENTS_KEY) || '[]');
        if (s.length || custom.length) setSources([...s, ...custom]);
        setOnline(true);
      })
      .catch((e) => {
        const custom = JSON.parse(localStorage.getItem(CUSTOM_AGENTS_KEY) || '[]');
        if (custom.length) setSources((current) => [...current, ...custom]);
        setOnline(false);
        setNotice(e.message || 'Failed to load sources');
      });
    topOfMindApi.getFolders().then((d) => {
      const f = arr(d, 'folders');
      if (f.length) setFolders(f);
    }).catch(() => {});

    const loadMessages = () => topOfMindApi.getMessages(75)
      .then((d) => { setMessages(arr(d, 'messages')); setOnline(true); })
      .catch(() => setOnline(false));
    loadMessages();
    const timer = setInterval(loadMessages, 4000);
    return () => clearInterval(timer);
  }, []);

  const selectedSource = sources.find((s) => srcId(s) === activeAgentId) || sources[0] || fallbackSources[0];

  async function send() {
    if (!input.trim()) return;
    const payload = {
      source_id: srcId(selectedSource),
      source_label: srcName(selectedSource),
      body: input,
      role: 'user',
      wall: 'main',
      folder: selectedFolder?.name || 'Main',
    };
    setInput('');
    setShowWall(true);
    try {
      const saved = await topOfMindApi.createMessage(payload);
      setMessages((m) => [...m, saved]);
    } catch {
      setMessages((m) => [...m, { ...payload, id: `local-${Date.now()}`, created_at: new Date().toISOString() }]);
      setNotice('Draft shown locally; API post failed.');
    }
  }

  async function createFolder() {
    const name = prompt('Folder name?');
    if (!name) return;
    try {
      const f = await topOfMindApi.createFolder({ name, parent_id: selectedFolder?.id || selectedFolder?.folder_id });
      setFolders((fs) => [...fs, f]);
    } catch {
      setFolders((fs) => [...fs, { id: `local-${Date.now()}`, name, children: [] }]);
      setNotice('Folder staged locally; API create failed.');
    }
  }

  const copyPromptToComposer = useCallback((text) => {
    setActive('chats');
    setShowWall(true);
    setInput((current) => (current ? `${current}\n\n${text}` : text));
  }, []);

  const withSide = active === 'chats' || active === 'settings';

  return (
    <div className={`app ${withSide && active === 'chats' ? 'with-side' : ''}`}>
      <Rail active={active} setActive={(id) => { setActive(id); if (id === 'chats') setShowWall(messages.length > 0); }} />

      {active === 'chats' && (
        <ChatsSide
          folders={folders}
          selectedFolder={selectedFolder}
          setSelectedFolder={setSelectedFolder}
          createFolder={createFolder}
          search={sideSearch}
          setSearch={setSideSearch}
          onNewChat={() => { setShowWall(false); setInput(''); setNotice('New chat'); }}
        />
      )}

      <main className="tm-main">
        {active === 'chats' && !showWall && messages.length === 0 && (
          <ChatsHome
            sources={sources}
            onPick={(s) => { setActiveAgentId(srcId(s)); setShowWall(true); }}
          />
        )}
        {active === 'chats' && (showWall || messages.length > 0) && (
          <MessageWall
            messages={messages}
            online={online}
            selectedSource={selectedSource}
            input={input}
            setInput={setInput}
            onSend={send}
            apiBase={topOfMindApi.baseUrl}
          />
        )}
        {active === 'agents' && (
          <AgentsPage
            sources={sources}
            onChat={(a) => {
              setActive('chats');
              setShowWall(true);
              setNotice(`Chat with ${a.name}`);
            }}
          />
        )}
        {active === 'prompts' && <PromptsPanel onCopyToComposer={copyPromptToComposer} />}
        {active === 'plugins' && <PluginsPage />}
        {active === 'models' && <ModelsPage />}
        {active === 'memory' && <KnowledgePanel online={online} />}
        {active === 'clipboard' && (
          <section className="tm-page">
            <ClipboardWorkspace onSendToComposer={copyPromptToComposer} setNotice={setNotice} />
          </section>
        )}
        {active === 'markdown' && <MarkdownPage setNotice={setNotice} />}
        {active === 'operator' && <OperatorPage setNotice={setNotice} />}
        {active === 'teams' && <TeamsPage />}
        {active === 'settings' && (
          <SettingsPanel online={online} setOnline={setOnline} notice={notice} setNotice={setNotice} />
        )}
      </main>

      <CommandPalette
        open={commandOpen}
        onClose={() => setCommandOpen(false)}
        setActive={setActive}
        setInput={setInput}
        sources={sources}
        folders={folders}
        setNotice={setNotice}
      />

      {notice && (
        <div className="notice-toast" onClick={() => setNotice('')}>{notice}</div>
      )}
    </div>
  );
}

createRoot(document.getElementById('root')).render(<App />);
