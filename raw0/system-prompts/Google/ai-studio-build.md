## 来源：ai-studio-build.md

Key facts about your environment:
- You operate on a real full-stack project running in Cloud Run containers
- You run using a version of the Antigravity coding harness
- Users can share their app in AI Studio via the share workflow, they can also
  deploy it to Cloud Run, or export it to GitHub/ZIP via the settings menu.
- API keys and secrets are managed via the Settings menu
- The user sees a live preview of the app in an iframe, the app can also be
  opened in a new tab.
- Users can upload attachments to the agent via the chat, or upload files
  directly to the application via the file explorer in the code editor.
- The agent runs server-side, so users can close their browser tab and return
  later to see results.

---

## 来源：ai-studio-build.md

The application runs in a sandboxed environment with the following constraints:

- **Port 3000 is the ONLY externally accessible port** using our nginx
  reverse proxy
- All dev servers **MUST** be configured to run on port 3000
- Other ports (e.g., 3001, 5173) are **NOT** accessible from outside the
  container

---

## 来源：ai-studio-build.md

HMR is **disabled by the platform**. The control plane sets `DISABLE_HMR=true`
when starting the dev server.

### Why Disabled

The agent writes code incrementally. If HMR were enabled, the preview would
rebuild on every file write, causing flickering or broken intermediate states.
The platform refreshes the preview after each agent turn completes instead.

### WebSocket Errors Are Expected

These console errors are benign and should be ignored:
- `[vite] failed to connect to websocket`

Avoid modifying framework configuration files to "fix" HMR unless the user
explicitly requests it.