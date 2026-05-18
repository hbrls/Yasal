# Claude-In-Chrome.md

## 来源：claude-in-chrome_20260328.md

### 文件说明

This content was obtained via inspecting network traffic for the offscreen.html service worker within Claude for Chrome Chrome extension, rather than prompt manipulation.

It is contained in the HTTP GET response to: https://api.anthropic.com/api/bootstrap/features/claude_in_chrome, which gets made from the sidebar.html task upon initialization.

The system prompt components appear to be contextual based on what page the user is on and what actions are requested.

Obtained 2026-03-28.

### Model Configuration

```json
{
  "default": "claude-sonnet-4-6",
  "default_model_override_id": "launch-2026-02-17-1",
  "quick_mode_default_model": "claude-opus-4-6[fast]",
  "options": [
    { "model": "claude-opus-4-6[fast]", "name": "Opus 4.6 (fast mode)", "description": "Our fastest and most capable model. Billed as extra usage at a premium rate.", "effort_options": ["low", "medium", "high"] },
    { "model": "claude-opus-4-6", "name": "Opus 4.6", "description": "Most capable for ambitious work", "effort_options": ["low", "medium", "high"] },
    { "model": "claude-sonnet-4-6", "name": "Sonnet 4.6", "description": "Most efficient for everyday tasks", "effort_options": ["low", "medium", "high"] },
    { "model": "claude-haiku-4-5-20251001", "name": "Haiku 4.5", "description": "Fastest for quick answers" }
  ],
  "quick_mode": {
    "fast_model": "claude-opus-4-6[fast]",
    "standard_model": "claude-haiku-4-5-20251001",
    "available_models": ["claude-opus-4-6[fast]", "claude-sonnet-4-6", "claude-haiku-4-5-20251001"]
  },
  "modelFallbacks": {
    "claude-haiku-4-5-20251001": { "currentModelName": "Haiku 4.5", "fallbackModelName": "claude-sonnet-4-20250514", "fallbackDisplayName": "Sonnet 4", "learnMoreUrl": "https://support.claude.com/en/articles/12436559-understanding-sonnet-4-5-s-safety-filters" },
    "claude-opus-4-6": { "currentModelName": "Opus 4.6", "fallbackModelName": "claude-sonnet-4-20250514", "fallbackDisplayName": "Sonnet 4", "learnMoreUrl": "https://support.claude.com/en/articles/12436559-understanding-sonnet-4-5-s-safety-filters" },
    "claude-opus-4-6[fast]": { "currentModelName": "Opus 4.6", "fallbackModelName": "claude-sonnet-4-20250514", "fallbackDisplayName": "Sonnet 4", "learnMoreUrl": "https://support.claude.com/en/articles/12436559-understanding-sonnet-4-5-s-safety-filters" },
    "claude-sonnet-4-6": { "currentModelName": "Sonnet 4.6", "fallbackModelName": "claude-sonnet-4-20250514", "fallbackDisplayName": "Sonnet 4", "learnMoreUrl": "https://support.claude.com/en/articles/12436559-understanding-sonnet-4-5-s-safety-filters" }
  }
}
```

### Version Info

```json
{
  "latest_version": "1.0.12",
  "min_supported_version": "1.0.11"
}
```

### Domain Skills Mapping

```json
{
  "mail.google.com": "crochet_gmail",
  "docs.google.com": "crochet_google_docs",
  "calendar.google.com": "crochet_google_calendar",
  "app.slack.com": "crochet_slack",
  "linkedin.com": "crochet_linkedin",
  "github.com": "crochet_github"
}
```

### PURL Configuration

```json
{
  "effort": "medium",
  "pageSettleMs": 100,
  "imageFormat": "jpeg",
  "imageQuality": 75,
  "maxImageDimension": 1568,
  "screenshotHistory": 1
}
```

### Bad Hostnames

```json
{
  "hostnames": [
    "mcp.slack.com",
    "mcp-outline-production"
  ]
}
```