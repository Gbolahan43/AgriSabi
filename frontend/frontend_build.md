# AI MASTER PROMPT: AgriSabi Engineering & Architecture Build
> **SYSTEM ROLE:** Act as an elite Senior Next.js 14 Web Engineer. Your objective is to build a robust, edge-ready, progressive web application (PWA) using React Server Components, Zustand, and strict TypeScript syncing with a FastAPI backend.

## 1. Core Stack Instructions
- **Framework**: Next.js 14 (App Router exclusively). No `pages/` directory.
- **Language**: TypeScript (`strict: true`). You MUST define interfaces for all API contracts before implementing components.
- **Styling**: Tailwind CSS configuration utilizing CSS variables for dynamic theming.
- **State**: `zustand` for global state (User Preferences, Offline Queues, WebSocket Live Audio State).
- **Data Fetching**: Use standard `fetch` API inside React Server Components where possible; use `react-query` or standard Axios hooks for heavy client-side mutations (like Image Uploads).

## 2. Directory Architecture & Routing execution
Execute the directory structure exactly as follows:
```text
src/
├── app/
│   ├── layout.tsx         # Injects RootProviders, Zustand Hydration, PWA Manifest
│   ├── globals.css        # Core Tailwind/Shadcn variables
│   ├── page.tsx           # Landing Screen (Server Component)
│   ├── (main)/            # Route Group sharing the MainNav + Floating Assistant FAB
│   │   ├── feed/page.tsx
│   │   ├── diagnose/page.tsx
│   │   ├── chat/page.tsx
│   │   └── market/page.tsx
├── components/
│   ├── ui/                # Raw Shadcn primitives
│   ├── shared/            # Cross-page components (e.g., WeatherPill.tsx, AudioVisualizer.tsx)
│   └── forms/             # Client-side form handlers heavily utilizing react-hook-form
├── store/
│   └── useNovaSonic.ts    # Zustand store tracking audio buffer arrays and WebRTC/WebSocket states
├── lib/
│   └── api.ts             # Axios interceptor configured to hit http://localhost:8000
```

## 3. Critical Engineering Tasks for AI

### Task A: The Diagnosis Uploader (`/diagnose`)
- **Requirement**: Use standard HTML5 `<input type="file" accept="image/jpeg, image/png" capture="environment" />` to trigger the native mobile camera seamlessly.
- **Handling**: Compress the image using a lightweight canvas script *before* sending via `FormData` to `/diagnose`, saving the user's mobile data bandwidth.
- **Hook**: Create `useDiagnoseMutation()` which posts to the proxy API and returns the rigorous `DiagnosisResponse` schema.

### Task B: Offline PWA Strategy
- **Requirement**: Implement `next-pwa` in `next.config.js`. 
- **Caching**: Configure Workbox strategies: `NetworkFirst` for `/api/market`, `CacheFirst` for JS/CSS assets, and `StaleWhileRevalidate` for user history. 
- **Graceful Degradation**: If the user loses internet during a `/chat` request, the app should save the payload to localForage (IndexedDB) and display a distinct "Pending Internet Connection" toast.

### Task C: Nova Sonic WebSocket Hook (`useNovaSonic.ts`)
- **Requirement**: Build a custom React hook that manages a raw `WebSocket` connection to `ws://backend/assistant/stream`.
- **Web Audio API**: It must request browser `getUserMedia({ audio: true })`. Chunk the PCM audio stream into Base64 or binary frames and emit them over the socket.
- **Lifecycle**: Ensure the WebSocket cleans up automatically `onUnmount` or when the user closes the global Drawer overlay to prevent massive memory leaks on Android devices.

## 4. Coding Standards
1. **Client vs Server**: Default all components to Server Components. Only add `"use client"` at the very leaf node of the component tree (e.g., inside the specific `<button onClick>` component, not the whole layout).
2. **Error Boundaries**: Every nested route segment must have an `error.tsx` file capturing API failures gracefully with an elegant "Retry" button.
