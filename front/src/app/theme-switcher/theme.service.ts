import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

export type Theme = 'light' | 'dark' | 'auto';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  private readonly STORAGE_KEY = 'theme-preference';
  private themeSubject = new BehaviorSubject<Theme>(this.getStoredTheme());

  theme$ = this.themeSubject.asObservable();

  constructor() {
    this.applyTheme(this.getStoredTheme());
    this.listenToSystemThemeChanges();
  }

  private getStoredTheme(): Theme {
    const stored = localStorage.getItem(this.STORAGE_KEY) as Theme;
    return stored || 'auto';
  }

  setTheme(theme: Theme): void {
    localStorage.setItem(this.STORAGE_KEY, theme);
    this.themeSubject.next(theme);
    this.applyTheme(theme);
  }

  getCurrentTheme(): Theme {
    return this.themeSubject.value;
  }

  private applyTheme(theme: Theme): void {
    const effectiveTheme = theme === 'auto' ? this.getSystemTheme() : theme;
    const root = document.documentElement;
    if (effectiveTheme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    root.style.colorScheme = effectiveTheme;
  }

  private getSystemTheme(): 'light' | 'dark' {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  private listenToSystemThemeChanges(): void {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      if (this.getCurrentTheme() === 'auto') {
        this.applyTheme('auto');
      }
    });
  }
}
