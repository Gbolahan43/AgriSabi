import type { Metadata } from "next";
import { Inter, Outfit } from "next/font/google";
import "./globals.css";
import BottomNav from "@/components/BottomNav";
import TopNav from "@/components/TopNav";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const outfit = Outfit({ subsets: ["latin"], variable: "--font-outfit" });

export const metadata: Metadata = {
  title: "AgriSabi - AI Agricultural Extension",
  description: "Transforming complex agricultural data into actionable insights.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${outfit.variable} font-sans antialiased bg-surface text-on_surface flex flex-col min-h-screen`}>
        <TopNav />
        <main className="flex-1 overflow-x-hidden pb-24 md:pb-0 relative">
          <div className="absolute top-0 left-0 w-full h-[50vh] bg-glass-shimmer pointer-events-none opacity-20 -z-10" />
          {children}
        </main>
        <BottomNav />
      </body>
    </html>
  );
}
