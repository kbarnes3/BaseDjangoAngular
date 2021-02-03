import { async, ComponentFixture, getTestBed, TestBed } from '@angular/core/testing';
import { NEVER, Observable, of } from 'rxjs';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { NavBarComponent } from './nav-bar.component';
import { LoginStatus, LoginStatusService } from '../login-status.service';

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

describe('NavBarComponent', () => {
  let injector: TestBed;
  let component: NavBarComponent;
  let fixture: ComponentFixture<NavBarComponent>;
  let service: MockLoginStatusService;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NavBarComponent ],
      imports: [NgbModule],
      providers: [
        { provide: LoginStatusService, useClass: MockLoginStatusService }
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    injector = getTestBed();
    fixture = TestBed.createComponent(NavBarComponent);
    service = injector.inject(LoginStatusService) as any as MockLoginStatusService;
    component = fixture.componentInstance;
  });

  it('should create', () => {
    fixture.detectChanges();
    expect(component).toBeTruthy();
  });

  it('should render title', () => {
    fixture.detectChanges();
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('.navbar-brand').textContent).toContain('NewDjangoSite');
  });

  it('should call LoginStatusService.getLoggedInService', () => {
    fixture.detectChanges();
    expect(service.getLoggedInStatusCalls).toBe(1);
  });

  it('should display loading content while waiting for results', () => {
    service.returnStatus = false;
    fixture.detectChanges();
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('.loading')).toBeTruthy();
    expect(compiled.querySelector('.loggedOut')).toBeFalsy();
    expect(compiled.querySelector('.loggedIn')).toBeFalsy();
  });

  it('should display logged out content when logged out', () => {
    service.status = {
      loggedIn: false
    };
    service.returnStatus = true;
    fixture.detectChanges();
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('.loggedOut')).toBeTruthy();
    expect(compiled.querySelector('.loading')).toBeFalsy();
    expect(compiled.querySelector('.loggedIn')).toBeFalsy();
  });

  it('should display logged in content when logged in', () => {
    const givenName: string = 'John';
    service.status = {
      loggedIn: true,
      givenName,
      surname: 'Doe'
    };
    service.returnStatus = true;
    fixture.detectChanges();
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('.loggedIn').textContent).toContain(givenName);
    expect(compiled.querySelector('.loading')).toBeFalsy();
    expect(compiled.querySelector('.loggedOut')).toBeFalsy();
  });
});
