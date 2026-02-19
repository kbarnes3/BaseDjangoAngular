
import { Component, OnInit, inject } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { RouterModule } from '@angular/router';
import {LoginStatus, LoginStatusService} from '../login-status.service';
import { AuthService } from '../auth/auth.service';
import { ConfigService } from '../config.service';

@Component({
    selector: 'app-nav-bar',
    imports: [NgbModule, RouterModule],
    templateUrl: './nav-bar.component.html',
    styleUrls: ['./nav-bar.component.scss'],
    
})
export class NavBarComponent implements OnInit {
  private statusService = inject(LoginStatusService);
  private authService = inject(AuthService);
  private configService = inject(ConfigService);

  public isCollapsed: boolean;
  public status: LoginStatus;
  public signupEnabled = true;

  ngOnInit() {
    this.isCollapsed = true;
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
