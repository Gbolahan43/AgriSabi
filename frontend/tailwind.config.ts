import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        surface: "#0F172A",
        "surface-container-lowest": "#070A13",
        "surface-container-low": "#1E293B",
        "surface-container": "#151C2C",
        "surface-container-high": "#334155",
        "surface-variant": "#475569",
        primary: "#79DB8D",
        "primary-container": "#15803D",
        secondary: "#FFB95F",
        on_surface: "#F8FAFC",
      },
      boxShadow: {
        "ambient-glow": "0 0 40px -5px rgba(121, 219, 141, 0.06)",
        "ambient-glow-high": "0 0 60px -10px rgba(121, 219, 141, 0.15)",
      },
      backgroundImage: {
        "glass-shimmer": "linear-gradient(45deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.05) 50%, rgba(255,255,255,0) 100%)",
        "primary-glow": "linear-gradient(135deg, #79DB8D, #15803D)",
      },
    },
  },
  plugins: [],
};
export default config;
