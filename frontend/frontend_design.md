# AgriSabi Professional Frontend Design System

## 1. Design Aesthetic & Philosophy
The AgriSabi frontend must completely bridge the gap between "local agricultural utility" and "enterprise-grade digital experience". We will use a **Vibrant Glassmorphism** aesthetic tailored to agrarian themes yet universally premium.

- **Vibrant Yet Grounded Palette**: Moving away from flat, generic "tech green", we will utilize rich, harmonious gradients. HSL tailored greens mixed with warm, earthy undertones (amber/ochre) to signify soil and growth, set against a sleek UI.
- **Dynamic Interactivity**: The interface must feel alive. Hover states will feature fluid, 150ms-300ms transitions. The UI will prominently feature micro-animations (e.g., pulsing mic icons, shimmering skeleton loaders during RAG retrieval) to maintain the user's focus and reduce perceived latency.
- **Premium Typography**: We will utilize **Outfit** (for bold, highly readable headers) and **Inter** (for crisp, dense data tables and chat interfaces).

## 2. Global Color System (Tailwind + CSS Variables)
Instead of static hex codes, the application will lean heavily into semantic CSS variables injected directly into `index.css`, allowing for fluid theming (including a deep, premium Dark Mode) without rewriting utility classes.

### Primary Accents
- `primary`: Lush Canopy Green (e.g., `hsl(142, 70%, 29%)`)
- `primary-glow`: Soft, diffused neon green for active states (Nova Sonic connection).
- `secondary`: Harvest Amber (e.g., `hsl(38, 92%, 50%)`) for warnings, high-priority actions, and market price spikes.

### Base & Surfaces
- `background`: True clean white in Light Mode, deep midnight slate (`hsl(222, 47%, 11%)`) in Dark Mode.
- `surface`: Frosted glass panels using `backdrop-blur-md` heavily across floating cards (like the Assistant overlay or Weather pill).

## 3. Core Component Designs

### 3.1 The Nova Sonic Live Assistant (Voice Interface)
- **Visualizer Overlay**: When the user taps the persistent "Live Assistant" floating action button, a bottom-sheet (mobile) or floating modal (desktop) slides up with a smooth cubic-bezier curve.
- **State Animations**: 
  - *Listening*: A subtle, breathing radial gradient underneath the microphone ring.
  - *Thinking*: A horizontal, shimmering gradient across the UI.
  - *Speaking*: Dynamic audio wavelength bars corresponding to the TTS volume.

### 3.2 The Two-Stage Diagnosis Hub (Camera/Upload)
- **Dropzone**: A large, rounded (e.g., `rounded-3xl`) dashed container that glows green upon dragging an image.
- **Diagnostic Result Card**: 
  - *Symptom Chips*: Small, rounded pills highlighting extracted keywords from Stage 1.
  - *Confidence Meter*: A circular progress bar animating from 0 to the Bedrock confidence score (e.g., 85%).
  - *Treatment Sections*: Accordions expanding smoothly to reveal Chemical vs. Organic treatments, heavily utilizing Shadcn UI's `Accordion` primitives customized with fluid entry animations.

### 3.3 Dashboard / Feed
- **Weather Pill**: Glass-effect pill showing immediate temperature and weather conditions, pinned to the top nav.
- **Market Ticker**: A continuously scrolling marquee of crop prices, color-coded (Amber for rising, Green for stable).

## 4. Typography & Spacing
- **Headers**: Minimal weight differences. `font-medium` or `font-semibold` with tight tracking (`tracking-tight`) for an editorial, app-like feel.
- **Gradients**: Text gradients on primary calls-to-action (e.g., "Diagnose Crop") to draw the eye immediately.

## 5. UI/UX Guiding Principles
- **No Placeholders**: We will rely on beautifully styled generic SVGs (Lucide React) if active data isn't available, never raw broken structures.
- **Zero-Layout-Shift**: Skeletons will be sized exactly to the data they replace to prevent the screen from jumping when AWS returns data.
- **Progressive Disclosure**: Detailed agricultural data (like pesticide mixing instructions) will be hidden behind smooth "View More" toggles to avoid overwhelming smallholder farmers on small local devices.
