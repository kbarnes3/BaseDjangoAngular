
import { Component, OnInit, inject } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import {LoginStatus, LoginStatusService} from '../login-status.service';

@Component({
    selector: 'app-nav-bar',
    imports: [NgbModule],
    templateUrl: './nav-bar.component.html',
    styleUrls: ['./nav-bar.component.scss'],
    
})
export class NavBarComponent implements OnInit {
  private statusService = inject(LoginStatusService);

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

}
