import { Component, OnInit } from '@angular/core';
import {LoginStatus, LoginStatusService} from '../login-status.service';

@Component({
  selector: 'app-nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.scss']
})
export class NavBarComponent implements OnInit {
  public isCollapsed: boolean;
  public status: LoginStatus;

  constructor(private statusService: LoginStatusService) { }

  ngOnInit() {
    this.isCollapsed = true;
    this.status = null;
    this.statusService.getLoggedInStatus()
        .subscribe((status: LoginStatus) => {
          this.status = status;
        });
  }

}
