# AgriSabi Expert Frontend Architecture & Build Plan

## 1. Technology Stack
To support the high-scale AWS Bedrock backend and the visually rich design system, the frontend will be built on the latest standard for enterprise React applications:

- **Core Framework**: Next.js 14+ (App Router). Crucial for aggressive edge caching, SEO optimization, and seamless API route proxying.
- **Language**: TypeScript (Strict Mode). Ensures type safety syncing directly with our OpenAPI backend schemas (e.g., `DiagnosisResponse`).
- **Styling**: Tailwind CSS + standard CSS modules for isolated micro-animations.
- **Component Library**: shadcn/ui. We will extract the raw Radix UI primitives and aggressively customize them to match our "Vibrant Glassmorphism" design system.
- **State Management**: Zustand. Used exclusively for managing the global state of the Nova Sonic WebSocket and User Preferences (Language/Location).
- **Data Fetching**: React Query (TanStack) for caching market data, weather data, and offline mutations.

## 2. Directory Structure (App Router)

```text
frontend/
├── src/
│   ├── app/                    # Next.js 14 App Router
│   │   ├── (dashboard)/        # Route Group (requires auth/layout)
│   │   │   ├── diagnose/       # Image upload & RAG result page
│   │   │   ├── market/         # Realtime market prices
│   │   │   └── page.tsx        # Main Feed & Weather
│   │   ├── api/                # Next.js API Routes (BFF proxies to FastAPI)
│   │   ├── layout.tsx          # Root Layout (Nav, Global Context)
│   │   └── globals.css         # Tailwind & Shadcn variable overrides
│   ├── components/             # Reusable UI
│   │   ├── ui/                 # Shadcn primitives (Buttons, Cards, Modals)
│   │   ├── features/           # Complex blocks (VoiceVisualizer, DiagnosisDropzone)
│   │   └── svgs/               # Custom icons & illustrations
│   ├── hooks/                  # Custom React Hooks
│   │   ├── useNovaSonic.ts     # WebSocket bidirectional audio manager
│   │   └── useDiagnosis.ts     # Multipart form data uploader
│   ├── lib/                    # Utilities & API Clients
│   │   ├── api.ts              # Axios/Fetch interceptors wrapping the FastAPI backend
│   │   └── utils.ts            # Tailwind `cn` merger utilities
│   └── store/                  # Zustand Global State
│       └── useStore.ts         # User language, offline queue
```

## 3. Key Implementation Details

### 3.1 Next.js Backend-For-Frontend (BFF)
Instead of exposing the FastAPI endpoints (`localhost:8000/diagnose`) directly to the browser, the Next.js App Router will proxy requests via `src/app/api/...`. This provides a critical security layer hiding AWS interactions and allows us to aggressively cache static data (like the offline Knowledge Base manifest) at the Next.js Edge.

### 3.2 WebSocket Streaming Hook (`useNovaSonic.ts`)
The true difficulty of the frontend build lies in the Live Assistant feature.
- **Audio Worklets**: We will rely on browser Web Audio API to capture raw microphone PCM data, chunk it, and stream it over the WebSocket to our `ws://backend/assistant/stream` endpoint.
- **Responsive State**: The hook will expose active states (`isConnecting`, `isListening`, `isVocalizing`) so the UI can instantly respond with the correct glowing/pulsing animations designed in `frontend_design.md`.

### 3.3 Tailoring Shadcn UI
When deploying Shadcn UI components, we will intercept and modify `components.json` to leverage CSS variables (e.g., `bg-primary`, `text-primary-foreground`). We will strictly avoid hardcoding colors inside the components themselves to guarantee Dark Mode compatibility seamlessly.

### 3.4 SEO and PWA Configurations
- **Manifest**: Automatic injection of `manifest.json` turning the web app into an installable PWA for Android users (crucial for Nigerian smallholder adoption).
- **Offline Fallback**: Utilizing Service Workers (via `next-pwa`) to cache the core application shell, allowing users to view cached weather or market data even on 2G/3G network drops in rural zones.

## 4. Build Phase Readiness
Do **not** initiate `npx create-next-app` until the User explicitly greenlights the initialization. Upon approval, the build script will be executed with non-interactive flags conforming precisely to this architecture.
