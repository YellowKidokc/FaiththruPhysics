# NotebookLM Studio Rename Workflow

Use this when cleaning up **pinned** Audio Overview items in NotebookLM Studio.
Run from **Cursor on your desktop with browser access** after you are logged into NotebookLM.

## Prefix rules

| Corner label in Studio | Prefix to add at start of title |
| --- | --- |
| **Deep Dive** | `DD` |
| **Debate** | `AD` |
| **Critique** | `AC` |

Optional (not requested yet — confirm before using):

| Corner label | Suggested prefix |
| --- | --- |
| Brief | `AB` |
| Video Overview | `VO` |
| Slide Deck | `SD` |

## Steps (per pinned audio item)

1. Open the notebook (Duality Project part, MDA part, one-page story, etc.).
2. In **Studio** (right panel), find each **pinned** output card.
3. Read the small corner label: **Deep Dive**, **Debate**, or **Critique**.
4. Click the **three dots** (⋮) on that card.
5. Choose **Rename**.
6. Put the prefix at the **front** of the title (no space required, but readable with a space is fine):
   - Deep Dive → `DD The Physics of...` or `DDThe Physics of...`
   - Debate → `AD ...`
   - Critique → `AC ...`
7. **Take a screenshot** of the Studio panel after renaming (for audit trail).
8. Save screenshots under:
   ```
   \\192.168.2.50\h_hp\Desktop\Notebook LM\Cursor - NotebookLM\<notebook-name>\
   ```

## Scope: Duality Project

For each **Duality Project** notebook that has pinned Studio outputs:

- [ ] Rename every Deep Dive → `DD` prefix
- [ ] Rename every Debate → `AD` prefix
- [ ] Rename every Critique → `AC` prefix
- [ ] Screenshot Studio panel after renames
- [ ] Note notebook URL in checklist below

### Duality notebooks checklist

| Notebook | Pinned items | DD | AD | AC | Screenshot saved |
| --- | --- | --- | --- | --- | --- |
| (fill in from NotebookLM) | | ☐ | ☐ | ☐ | ☐ |

## Matches existing download naming

When files are exported/downloaded, the repo already uses similar tags in filenames:

- `something__DD__Title.m4a` — Deep Dive audio
- Debate / Critique exports should follow `__AD__` and `__AC__` if you adopt the same pattern on disk later.

## Who can run this

| Environment | Can click NotebookLM? |
| --- | --- |
| **This cloud agent** | No — no browser, no LAN, no Google login |
| **Cursor desktop + browser / computer use** | Yes — log in once, then agent can walk notebooks |
| **You manually** | Yes — follow steps above |

## Quick copy for agent prompt (desktop session)

```
For each Duality Project notebook in NotebookLM:
1. Open Studio panel.
2. For every PINNED audio card, read the corner type (Deep Dive / Debate / Critique).
3. Three dots → Rename → prefix: DD / AD / AC.
4. Screenshot Studio after each notebook.
5. Save to \\192.168.2.50\h_hp\Desktop\Notebook LM\Cursor - NotebookLM\duality\
```
