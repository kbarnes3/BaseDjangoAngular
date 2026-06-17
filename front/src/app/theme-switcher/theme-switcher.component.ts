import { Component, inject, ChangeDetectionStrategy } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { CommonModule } from '@angular/common';
import { MatMenuModule } from '@angular/material/menu';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ThemeService, Theme } from './theme.service';

@Component({
  selector: 'app-theme-switcher',
  standalone: true,
  imports: [CommonModule, MatMenuModule, MatButtonModule, MatIconModule],
  templateUrl: './theme-switcher.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  styleUrls: ['./theme-switcher.component.scss']
})
export class ThemeSwitcherComponent {
  private themeService = inject(ThemeService);

  currentTheme = toSignal(this.themeService.theme$, { initialValue: 'auto' as Theme });

  setTheme(theme: Theme): void {
    this.themeService.setTheme(theme);
  }

  getThemeIcon(): string {
    switch (this.currentTheme()) {
      case 'light':
        return 'light_mode';
      case 'dark':
        return 'dark_mode';
      case 'auto':
      default:
        return 'contrast';
    }
  }
}
