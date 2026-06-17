import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ThemeSwitcherComponent } from './theme-switcher.component';
import { ThemeService } from './theme.service';

describe('ThemeSwitcherComponent', () => {
  let component: ThemeSwitcherComponent;
  let fixture: ComponentFixture<ThemeSwitcherComponent>;
  let themeService: ThemeService;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ThemeSwitcherComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(ThemeSwitcherComponent);
    component = fixture.componentInstance;
    themeService = TestBed.inject(ThemeService);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should set theme when setTheme is called', () => {
    spyOn(themeService, 'setTheme');
    component.setTheme('dark');
    expect(themeService.setTheme).toHaveBeenCalledWith('dark');
  });

  it('should return correct icon for light theme', () => {
    themeService.setTheme('light');
    expect(component.getThemeIcon()).toBe('light_mode');
  });

  it('should return correct icon for dark theme', () => {
    themeService.setTheme('dark');
    expect(component.getThemeIcon()).toBe('dark_mode');
  });

  it('should return correct icon for auto theme', () => {
    themeService.setTheme('auto');
    expect(component.getThemeIcon()).toBe('contrast');
  });
});
