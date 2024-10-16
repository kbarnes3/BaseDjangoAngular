import { getTestBed, TestBed } from '@angular/core/testing';

import {LoginStatus, LoginStatusService} from './login-status.service';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';

describe('LoginStatusService', () => {
  let injector: TestBed;
  let service: LoginStatusService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
    imports: [],
    providers: [LoginStatusService, provideHttpClient(withInterceptorsFromDi()), provideHttpClientTesting()]
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
    const sampleStatus: LoginStatus = {
      loggedIn: true,
      givenName: 'John',
      surname: 'Doe'
    };

    service.getLoggedInStatus().subscribe((status: LoginStatus)  => {
      expect(status).toEqual(sampleStatus);
    });

    const req = httpMock.expectOne('/api/account/logged_in/');
    expect(req.request.method).toBe('GET');
    req.flush(sampleStatus);
  });

  it('should return loggedIn = false when a bad response is returned', () => {
    const mockErrorResponse = { status: 400, statusText: 'Bad Request' };

    service.getLoggedInStatus().subscribe((status: LoginStatus)  => {
      expect(status.loggedIn).toBeFalsy();
    });

    const req = httpMock.expectOne('/api/account/logged_in/');
    req.flush('BAD', mockErrorResponse);
  });
});
