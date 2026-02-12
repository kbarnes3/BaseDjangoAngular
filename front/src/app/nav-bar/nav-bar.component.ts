
import { Component, OnInit, inject, DOCUMENT } from '@angular/core';
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
  private document = inject(DOCUMENT);

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
    const form = this.document.createElement('form');
    form.method = 'POST';
    form.action = '/account/logout/';

    const csrfInput = this.document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    const match = this.document.cookie.match(/csrftoken=([^;]+)/);
    csrfInput.value = match ? match[1] : '';

    form.appendChild(csrfInput);
    this.document.body.appendChild(form);
    form.submit();
  }

}
