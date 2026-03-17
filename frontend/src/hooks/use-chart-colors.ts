"use client";

import { useTheme } from "next-themes";

/**
 * Returns resolved color values for Recharts SVG elements.
 * Recharts tick/stroke props need actual color strings (not CSS vars with oklch).
 */
export function useChartColors() {
  const { resolvedTheme } = useTheme();
  const isDark = resolvedTheme === "dark";

  return {
    text: isDark ? "#e5e5e5" : "#1a1a1a",
    textMuted: isDark ? "#a3a3a3" : "#737373",
    grid: isDark ? "#333" : "#e5e5e5",
    tooltipBg: isDark ? "#262626" : "#ffffff",
    tooltipBorder: isDark ? "#404040" : "#e5e5e5",
    primary: isDark ? "#818cf8" : "#4f46e5",
  };
}
