import { Component, OnInit } from '@angular/core';
import { LoginStatusService } from '../login-status.service';

@Component({
  selector: 'app-login-links',
  templateUrl: './login-links.component.html',
  styleUrls: ['./login-links.component.scss']
})
export class LoginLinksComponent implements OnInit {

  constructor(private statusService: LoginStatusService) { }

  ngOnInit() {
  }

}
