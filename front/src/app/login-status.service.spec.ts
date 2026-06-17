import { getTestBed, TestBed } from '@angular/core/testing';

import {LoginStatus, LoginStatusService} from './login-status.service';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient, withInterceptorsFromDi, withXhr } from '@angular/common/http';

describe('LoginStatusService', () => {
  let injector: TestBed;
  let service: LoginStatusService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
    imports: [],
    providers: [LoginStatusService, provideHttpClient(withXhr(), withInterceptorsFromDi()), provideHttpClientTesting()]
});

    injector = getTestBed();
    service = injector.inject(LoginStatusService);
    httpMock = injector.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should return an Observable<LoginStatus>', () => {
    const sessionResponse = {
      status: 200,
      data: { user: { id: 1, display: 'John', email: 'john@example.com' } },
      meta: { is_authenticated: true }
    };

    service.getLoggedInStatus().subscribe((status: LoginStatus)  => {
      expect(status.loggedIn).toBeTrue();
      expect(status.displayName).toBe('John');
    });

    const req = httpMock.expectOne('/_allauth/browser/v1/auth/session');
    expect(req.request.method).toBe('GET');
    req.flush(sessionResponse);
  });

  it('should return loggedIn = false when a bad response is returned', () => {
    const mockErrorResponse = { status: 400, statusText: 'Bad Request' };

    service.getLoggedInStatus().subscribe((status: LoginStatus)  => {
      expect(status.loggedIn).toBeFalsy();
    });

    const req = httpMock.expectOne('/_allauth/browser/v1/auth/session');
    req.flush('BAD', mockErrorResponse);
  });
});
