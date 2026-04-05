# AI MASTER PROMPT: AgriSabi UI/UX Design System
> **SYSTEM ROLE:** Act as an elite UI/UX Developer and Designer. Your objective is to translate this design specification into flawless, responsive Tailwind CSS and Shadcn UI components optimized primarily for mobile device form factors (smallholder farmers) while elegantly scaling to desktop.

## 1. Global Aesthetic & Responsiveness
**Theme:** Vibrant Glassmorphism.
**Colors (CSS Variables):**
- `--primary`: `142 70% 29%` (Canopy Green)
- `--secondary`: `38 92% 50%` (Harvest Amber)
- `--background`: `0 0% 100%` (Light) / `222 47% 11%` (Dark)
- `--surface`: `0 0% 100% / 0.7` (Frosted Glass)

**Breakpoints (Mobile-First Strictness):**
Design everything default for mobile (screens < 640px). 
- `sm:` (640px) - Large phones/small tablets.
- `md:` (768px) - iPads. Shift stacked vertical cards into 2-column grids.
- `lg:` (1024px) - Desktop. Shift to 3-column grids, persistent sidebars instead of bottom tabs.

## 2. Screen-by-Screen UI Specification

### 2.1 The Welcome/Landing Page (`/`)
- **Mobile View**: Full-viewport height (`h-screen`). 60% of the upper screen is a rich agricultural illustration mask. The bottom 40% is a frosted glass card containing the title, subtitle, and a massive, glowing `w-full` primary CTA button: "Enter AgriSabi".
- **Desktop (`lg:`) View**: Split screen (`grid-cols-2`). Left side contains typography and CTA (left-aligned). Right side contains the illustration.

### 2.2 The Main Dashboard (`/feed`)
- **Top Nav**: Sticky glass header (`sticky top-0 backdrop-blur-md`). Contains a small "Weather Pill" showing temperature and an icon.
- **Content Grid**: 
  - Mobile: A vertical scroll of massive, tap-friendly feature cards (Diagnose Crop, Market Prices, AI Chat). 
  - Desktop: A `md:grid-cols-3` layout.
- **Market Ticker**: A continuous CSS-animated marquee (`overflow-hidden whitespace-nowrap`) pinned just below the header. Amber numbers for rising prices, Green for stable.

### 2.3 The Diagnosis Hub (`/diagnose`)
- **Upload Zone**: A `min-h-[250px]` container with `border-dashed border-2 rounded-3xl`. 
  - *Interaction*: When a user drags a file (or taps to open native camera roll), the border glows `--primary` and scales up `scale-105` using Tailwind `transition-transform duration-300`.
- **Results View**: Once diagnosed, the upload zone shrinks. A Shadcn `Accordion` appears.
  - *Mobile*: The "Confidence Meter" (circular SVG progress bar) is sticky at the bottom of the screen.
  - *Desktop*: Confidence Meter sits in a right-hand sidebar.

### 2.4 The Live Assistant Overlay (Global)
- **Component Type**: Mobile uses Shadcn `Drawer` (slides up from bottom, snap points at 50% and 100%). Desktop uses Shadcn `Dialog` (centered floating modal).
- **Audio Visualizer**: Three vertical bars centered on the screen. 
  - *Animation*: Use CSS keyframes to animate `height` randomly when the bot is speaking (`animate-pulse` mixed with scale transforms).
- **Controls**: A massive, circular, floating action button (FAB) painted in a `--primary-glow` radial gradient to mute/unmute the microphone.

## 3. Strict UI Rules for AI Generation
1. **Zero Layout Shift**: Never allow a loading state to collapse the DOM height. Always use `Skeleton` components sized exactly to the final data dimensions.
2. **Touch Targets**: All interactive elements (buttons, links, dropzones) must have a minimum `min-h-[44px]` and `min-w-[44px]` to satisfy mobile accessibility standards.
3. **Typography Scaling**: Use fluid typography scaling (`text-sm md:text-base lg:text-lg`) to ensure readability outdoors in bright sunlight.
4. **Dark Mode Native**: Every single Tailwind class must have a `dark:` variant considered. Do not hardcode `bg-white`, use `bg-background`.
