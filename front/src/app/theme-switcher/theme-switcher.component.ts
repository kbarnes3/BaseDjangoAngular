import { Component, OnInit, OnDestroy, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgbDropdownModule } from '@ng-bootstrap/ng-bootstrap';
import { ThemeService, Theme } from './theme.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-theme-switcher',
  standalone: true,
  imports: [CommonModule, NgbDropdownModule],
  templateUrl: './theme-switcher.component.html',
  styleUrls: ['./theme-switcher.component.scss']
})
export class ThemeSwitcherComponent implements OnInit, OnDestroy {
  private themeService = inject(ThemeService);

  currentTheme: Theme = 'auto';
  private subscription?: Subscription;


  ngOnInit(): void {
    this.subscription = this.themeService.theme$.subscribe(theme => {
      this.currentTheme = theme;
    });
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }

  setTheme(theme: Theme): void {
    this.themeService.setTheme(theme);
  }

  getThemeIcon(): string {
    switch (this.currentTheme) {
      case 'light':
        return 'bi bi-sun-fill';
      case 'dark':
        return 'bi bi-moon-fill';
      case 'auto':
      default:
        return 'bi bi-circle-half';
    }
  }
}
