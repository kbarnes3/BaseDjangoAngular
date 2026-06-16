
import { Component, OnInit, inject } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { BreakpointObserver } from '@angular/cdk/layout';
import { RouterModule } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { map } from 'rxjs/operators';
import {LoginStatus, LoginStatusService} from '../login-status.service';
import { AuthService } from '../auth/auth.service';
import { ConfigService } from '../config.service';
import { ThemeSwitcherComponent } from '../theme-switcher/theme-switcher.component';

@Component({
    selector: 'app-nav-bar',
    imports: [
        RouterModule,
        MatToolbarModule,
        MatButtonModule,
        MatIconModule,
        MatSidenavModule,
        MatListModule,
        MatProgressSpinnerModule,
        ThemeSwitcherComponent,
    ],
    templateUrl: './nav-bar.component.html',
    styleUrls: ['./nav-bar.component.scss'],

})
export class NavBarComponent implements OnInit {
  private breakpointObserver = inject(BreakpointObserver);
  private statusService = inject(LoginStatusService);
  private authService = inject(AuthService);
  private configService = inject(ConfigService);

  public status: LoginStatus;
  public signupEnabled = true;

  // True on narrow viewports where the inline nav collapses into a hamburger menu.
  isHandset = toSignal(
    this.breakpointObserver
      .observe('(max-width: 1023.98px)')
      .pipe(map(result => result.matches)),
    { initialValue: false }
  );

  ngOnInit() {
    this.status = null;
    this.statusService.status$.subscribe((status: LoginStatus) => {
      this.status = status;
    });
    this.statusService.refreshStatus();
    this.configService.accountCreationMode$.subscribe(mode => {
      this.signupEnabled = mode !== 'disabled';
    });
    this.configService.refreshConfig();
  }

  logout(): void {
    this.authService.logout().subscribe({
      next: () => {
        this.statusService.refreshStatus();
        window.location.href = '/';
      },
      error: () => {
        this.statusService.refreshStatus();
        window.location.href = '/';
      }
    });
  }

}
