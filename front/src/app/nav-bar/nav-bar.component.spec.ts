import { waitForAsync, ComponentFixture, getTestBed, TestBed } from '@angular/core/testing';
import { NEVER, Observable, of, BehaviorSubject } from 'rxjs';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { RouterModule } from '@angular/router';

import { NavBarComponent } from './nav-bar.component';
import { LoginStatus, LoginStatusService } from '../login-status.service';
import { AuthService } from '../auth/auth.service';
import { ConfigService, AccountCreationMode } from '../config.service';

class MockLoginStatusService {
  status!: LoginStatus;
  returnStatus = false;
  getLoggedInStatusCalls: number;
  private statusSubject = new BehaviorSubject<LoginStatus | null>(null);
  status$ = this.statusSubject.asObservable();

  constructor() {
    this.getLoggedInStatusCalls = 0;
  }

  refreshStatus(): void {
    this.getLoggedInStatusCalls++;
    if (this.returnStatus) {
      this.statusSubject.next(this.status);
    }
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

class MockAuthService {
  logout(): Observable<Record<string, never>> {
    return of({});
  }
}

class MockConfigService {
  private modeSubject = new BehaviorSubject<AccountCreationMode>('default');
  accountCreationMode$ = this.modeSubject.asObservable();

  refreshConfig(): void {
    // no-op for test mock
  }

  getAccountCreationMode(): Observable<AccountCreationMode> {
    return of('default');
  }

  get signupEnabled(): boolean {
    return this.modeSubject.value !== 'disabled';
  }

  setMode(mode: AccountCreationMode): void {
    this.modeSubject.next(mode);
  }
}

describe('NavBarComponent', () => {
  let injector: TestBed;
  let component: NavBarComponent;
  let fixture: ComponentFixture<NavBarComponent>;
  let service: MockLoginStatusService;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      imports: [NoopAnimationsModule, RouterModule.forRoot([])],
      providers: [
        { provide: LoginStatusService, useClass: MockLoginStatusService },
        { provide: AuthService, useClass: MockAuthService },
        { provide: ConfigService, useClass: MockConfigService },
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    injector = getTestBed();
    fixture = TestBed.createComponent(NavBarComponent);
    service = injector.inject(LoginStatusService) as unknown as MockLoginStatusService;
    component = fixture.componentInstance;
  });

  it('should create', () => {
    fixture.detectChanges();
    expect(component).toBeTruthy();
  });

  it('should render title', () => {
    fixture.detectChanges();
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('.app-brand').textContent).toContain('NewDjangoSite');
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
    const displayName = 'John';
    service.status = {
      loggedIn: true,
      displayName,
    };
    service.returnStatus = true;
    fixture.detectChanges();
    const compiled = fixture.debugElement.nativeElement;
    const loggedInEls = Array.from(compiled.querySelectorAll('.loggedIn')) as HTMLElement[];
    expect(loggedInEls.length).toBeGreaterThan(0);
    expect(loggedInEls.some(el => el.textContent?.includes(displayName))).toBe(true);
    expect(compiled.querySelector('.loading')).toBeFalsy();
    expect(compiled.querySelector('.loggedOut')).toBeFalsy();
  });
});
