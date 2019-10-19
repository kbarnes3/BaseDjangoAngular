import { Component, OnInit } from '@angular/core';
import {LoginStatus, LoginStatusService} from '../login-status.service';

@Component({
  selector: 'app-login-links',
  templateUrl: './login-links.component.html',
  styleUrls: ['./login-links.component.scss']
})
export class LoginLinksComponent implements OnInit {
  private status: LoginStatus;

  constructor(private statusService: LoginStatusService) { }

  ngOnInit() {
    this.status = null;
    this.statusService.getLoggedInStatus()
        .subscribe((status: LoginStatus) => {
          this.status = status;
        });
  }

}
