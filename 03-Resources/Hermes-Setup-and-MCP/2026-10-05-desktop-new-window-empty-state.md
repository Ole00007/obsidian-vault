---
title: "Hermes Desktop — new window opens on empty state (not a bug)"
created: 2026-10-05
tags: [hermes, desktop, ui, troubleshooting]
status: active
---

# Hermes Desktop — new window opens on empty state

## Verdict: EXPECTED BEHAVIOR — no fix needed

Opening a second window (⌘⇧N / "New window", or right-click a profile → *Open in new window*)
produces a window whose main pane shows the empty state ("No project open"). This is **correct**
— a new window is a **fresh workspace**, not a clone of the window you were in.

## Why it looks "blank"

A **new window** and a **new tab** do different things:

| Gesture | What it does | Result |
|---------|--------------|--------|
| **⌘N** (New session) / ⌘-click a session | Creates/opens a session **in the current window** | Composer appears immediately |
| **⌘⇧N** (New window) | Opens a **fresh peer workspace** on the same backend | Empty state — you pick a session |

The peer window deliberately does **not** restore the primary window's last session, so nothing
is selected and the workspace pane renders its empty state.

## Code trail (for future reference)

- `apps/desktop/src/store/windows.ts:219-225` — `openNewWindow()` → `hermesDesktop.openWindow(route)`
- `apps/desktop/electron/main.ts:15365-15369` — `hermes:window:openInstance` IPC → `createInstanceWindow()`
- `apps/desktop/electron/session-windows.ts:90-100` — `buildInstanceWindowUrl()` emits `?peer=1`
- `apps/desktop/src/store/windows.ts:120-126` — `isPeerInstanceWindow()` matches `?peer=1`
- `apps/desktop/src/app/gateway/hooks/use-gateway-boot.ts:611-627` — peer window skips
  `desktop.profile?.getDefault?.()`, so no session is auto-selected
- `apps/desktop/src/store/session.ts:922` — `$selectedStoredSessionId` starts `null`
- `apps/desktop/src/app/right-sidebar/index.tsx:154-155` — "No project open" empty state

Note: `$layoutTree` is nulled only for `isSecondaryWindow()` / `isBrowserWindow()`
(`components/pane-shell/tree/store.ts:78`) — a **peer** window keeps its persisted tree, so the
layout itself is fine. The empty pane is purely "no session selected".

## What to do instead

In the new window: click **New session**, press **⌘N**, or click any session in the sidebar.

## Practical guidance for multi-agent work

- To talk to a **different agent** → the **BOTS** tab (roster of all profiles), or the
  bottom-left profile dropdown (currently `smoothy_op_dir`).
- To run **two agents side by side** → ⌘⇧N, then pick that agent's session in the new window.
- The active agent is always readable at the **bottom-left of the status bar**.

## Links

- Parent: [[Hermes-Setup-and-MCP]]
- Related: [[2026-10-05]]
- See also: [[2026-10-05-canva-fronty-intake-and-d1-15-fix]]
