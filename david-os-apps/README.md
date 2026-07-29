# David-OS apps (portable package)

Synced from `YellowKidokc/David-OS` `apps/` for cloud work on the faiththruphysics agent
(that repo is not pushable from this environment).

## Desk UI goal

Black / gold chrome, **TypingMind menu layout** from `Pics/`:

- Left icon rail: Chats · Agents · Prompts · Plugins · Models · KB · Teams · Settings
- Chats: gold **+ New Chat**, search, Folders, starred threads, message wall + composer
- Agents / Prompts / Plugins: category or store side + card grids + Use now / Chat now
- Models: providers | catalog | detail (three-pane)
- KB: empty state + **+ Add Memories** FAB
- Settings: TypingMind settings tree (Account & Data / Preferences / Advanced)

## Run desk

```bash
cd david-os-apps/desk
npm install
npm run dev
```

Default API: `http://127.0.0.1:10000` (`VITE_TOP_OF_MIND_API`).

## Sync back to David-OS

Copy `david-os-apps/desk` → `David-OS/apps/desk` (and keep `Pics/` as visual reference).
