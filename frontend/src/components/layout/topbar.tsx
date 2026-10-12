"use client";

import { useAuth } from "@/providers/auth-provider";
import { Button } from "@/components/ui/button";
import { LogOut, Menu, Moon, Sun, User } from "lucide-react";
import { AppSidebar } from "./app-sidebar";
import { useTheme } from "next-themes";

export function Topbar() {
  const { userInfo, authenticated, login, logout } = useAuth();
  const { theme, setTheme } = useTheme();

  return (
    <header className="flex h-14 items-center justify-between border-b bg-background px-4 sm:px-6" role="banner" aria-label="Top bar">
      <div className="text-sm text-muted-foreground">
        <details className="relative md:hidden" onKeyDown={(event) => {
          if (event.key === "Escape") {
            event.currentTarget.open = false;
            event.currentTarget.querySelector("summary")?.focus();
          }
        }}>
          <summary aria-label="Toggle navigation" className="flex h-11 w-11 cursor-pointer list-none items-center justify-center rounded-md hover:bg-accent focus-visible:outline-2 focus-visible:outline-ring [&::-webkit-details-marker]:hidden">
            <Menu className="h-5 w-5" aria-hidden="true" />
          </summary>
          <div className="absolute -left-4 top-12 z-50 shadow-xl" onClick={(event) => {
            if ((event.target as HTMLElement).closest("a")) {
              event.currentTarget.closest("details")?.removeAttribute("open");
            }
          }}>
            <AppSidebar mobile />
          </div>
        </details>
      </div>
      <div className="flex items-center gap-3">
        <Button
          variant="ghost"
          size="icon"
          aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        >
          <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" aria-hidden="true" />
          <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" aria-hidden="true" />
        </Button>
        {authenticated ? (
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 text-sm">
              <User className="h-4 w-4" aria-hidden="true" />
              <span className="max-w-32 truncate sm:max-w-xs">{userInfo?.name || userInfo?.email}</span>
            </div>
            <Button variant="ghost" size="icon" onClick={logout} aria-label="Log out">
              <LogOut className="h-4 w-4" aria-hidden="true" />
            </Button>
          </div>
        ) : (
          <Button size="sm" onClick={() => login()}>
            Sign In
          </Button>
        )}
      </div>
    </header>
  );
}
