import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginLinksComponent } from './login-links.component';
import {LoginStatus} from '../login-status.service';
import {Observable, of} from 'rxjs';

class MockLoginStatusService {
  private status: LoginStatus;

  getLoggedInStatus(): Observable<LoginStatus> {
    return of<LoginStatus>(this.status);
  }

  setLoggedInStatus(status: LoginStatus): void {
    this.status = status;
  }
}

describe('LoginLinksComponent', () => {
  let component: LoginLinksComponent;
  let fixture: ComponentFixture<LoginLinksComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LoginLinksComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LoginLinksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
