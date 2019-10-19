import {async, ComponentFixture, getTestBed, TestBed} from '@angular/core/testing';

import { LoginLinksComponent } from './login-links.component';
import {LoginStatus, LoginStatusService} from '../login-status.service';
import {NEVER, Observable, of} from 'rxjs';

class MockLoginStatusService {
  status: LoginStatus;
  returnStatus: boolean;
  getLoggedInStatusCalls: number;

  constructor() {
    this.getLoggedInStatusCalls = 0;
  }

  getLoggedInStatus(): Observable<LoginStatus> {
    this.getLoggedInStatusCalls++;
    if (this.returnStatus) {
      return of<LoginStatus>(this.status);
    } else {
      return NEVER;
    }
  }
}

describe('LoginLinksComponent', () => {
  let injector: TestBed;
  let component: LoginLinksComponent;
  let fixture: ComponentFixture<LoginLinksComponent>;
  let service: MockLoginStatusService;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LoginLinksComponent ],
      providers: [
        { provide: LoginStatusService, useClass: MockLoginStatusService }
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    injector = getTestBed();
    fixture = TestBed.createComponent(LoginLinksComponent);
    service = injector.get(LoginStatusService);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    fixture.detectChanges();
    expect(component).toBeTruthy();
  });

  it('should call LoginStatusService.getLoggedInService', () => {
    fixture.detectChanges();
    expect(service.getLoggedInStatusCalls).toBe(1);
  });
});
