import { MessageSquare, Bot, Sparkles, Plug, BrainCircuit, Folder, Users, Settings, Clipboard, FileText, Terminal } from 'lucide-react';

const NAV = [
  { id: 'chats', label: 'Chats', icon: MessageSquare },
  { id: 'agents', label: 'Agents', icon: Bot },
  { id: 'prompts', label: 'Prompts', icon: Sparkles },
  { id: 'plugins', label: 'Plugins', icon: Plug },
  { id: 'models', label: 'Models', icon: BrainCircuit },
  { id: 'memory', label: 'KB', icon: Folder },
  { id: 'clipboard', label: 'Clip', icon: Clipboard },
  { id: 'markdown', label: 'Notes', icon: FileText },
  { id: 'operator', label: 'Ops', icon: Terminal },
  { id: 'teams', label: 'Teams', icon: Users },
  { id: 'settings', label: 'Settings', icon: Settings },
];

export function Rail({ active, setActive }) {
  return (
    <nav className="tm-rail" aria-label="Primary">
      <div className="brand" title="Top of Mind">ToM</div>
      {NAV.map(({ id, label, icon: Icon }) => (
        <button
          key={id}
          type="button"
          className={active === id ? 'on' : ''}
          title={label}
          onClick={() => setActive(id)}
        >
          <Icon size={18} strokeWidth={1.75} />
          <small>{label}</small>
        </button>
      ))}
      <div className="rail-spacer" />
      <div className="rail-foot" title="David OS">F</div>
    </nav>
  );
}
