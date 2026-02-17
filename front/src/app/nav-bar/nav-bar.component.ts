
import { Component, OnInit, inject } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { RouterModule } from '@angular/router';
import {LoginStatus, LoginStatusService} from '../login-status.service';
import { AuthService } from '../auth/auth.service';

@Component({
    selector: 'app-nav-bar',
    imports: [NgbModule, RouterModule],
    templateUrl: './nav-bar.component.html',
    styleUrls: ['./nav-bar.component.scss'],
    
})
export class NavBarComponent implements OnInit {
  private statusService = inject(LoginStatusService);
  private authService = inject(AuthService);

  public isCollapsed: boolean;
  public status: LoginStatus;

  ngOnInit() {
    this.isCollapsed = true;
    this.status = null;
    this.statusService.getLoggedInStatus()
        .subscribe((status: LoginStatus) => {
          this.status = status;
        });
  }

  logout(): void {
    this.authService.logout().subscribe({
      next: () => {
        window.location.href = '/';
      },
      error: () => {
        window.location.href = '/';
      }
    });
  }

}
