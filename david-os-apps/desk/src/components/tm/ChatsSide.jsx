import { Plus, Search, Star } from 'lucide-react';

const SAMPLE_CHATS = [
  { id: 'c1', title: 'API smoke — Mattermost / Codex', starred: true },
  { id: 'c2', title: 'Overlay bridge test', starred: true },
  { id: 'c3', title: 'Key rotated · kimi lane', starred: false },
  { id: 'c4', title: 'DeepSeek router enablement', starred: false },
];

export function ChatsSide({
  folders = [],
  selectedFolder,
  setSelectedFolder,
  createFolder,
  search,
  setSearch,
  onNewChat,
}) {
  return (
    <aside className="tm-side" aria-label="Chats sidebar">
      <div className="tm-side-pad">
        <button type="button" className="tm-new-chat" onClick={onNewChat}>
          <Plus size={16} /> New Chat
        </button>
        <div className="tm-search-wrap">
          <Search size={15} />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search chats"
          />
        </div>
      </div>

      <div className="tm-side-section">
        <span>Folders</span>
        <button type="button" className="btn-secondary" style={{ padding: '4px 8px', fontSize: 11 }} onClick={createFolder}>
          +
        </button>
      </div>
      <div className="tm-side-scroll">
        {(folders.length ? folders : [{ id: 'smoke', name: 'Codex smoke folder', children: [] }]).map((f) => {
          const id = f.id || f.folder_id || f.name;
          const selected = (selectedFolder?.id || selectedFolder?.name) === id || selectedFolder?.name === f.name;
          return (
            <button
              key={id}
              type="button"
              className={`tm-folder ${selected ? 'on' : ''}`}
              onClick={() => setSelectedFolder(f)}
            >
              <span>📁</span>
              <span style={{ overflow: 'hidden', textOverflow: 'ellipsis' }}>{f.name || f.title}</span>
              <small>{(f.children || []).length || f.folder_code || ''}</small>
            </button>
          );
        })}

        <div className="tm-side-section" style={{ marginLeft: 6 }}>Starred</div>
        {SAMPLE_CHATS.filter((c) => !search || c.title.toLowerCase().includes(search.toLowerCase())).map((c) => (
          <button key={c.id} type="button" className="tm-chat-item">
            {c.starred ? <Star size={13} className="tm-star" fill="currentColor" /> : <span style={{ width: 13 }} />}
            <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{c.title}</span>
          </button>
        ))}
      </div>
    </aside>
  );
}
