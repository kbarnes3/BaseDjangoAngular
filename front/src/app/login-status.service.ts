import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable, of} from 'rxjs';
import {catchError} from 'rxjs/operators';

export class LoginStatus {
  loggedIn: boolean;
  givenName?: string;
  surname?: string;
}

@Injectable({
  providedIn: 'root'
})
export class LoginStatusService {

  constructor(
      private http: HttpClient
  ) { }

  private apiUrl: string = '/api/account/logged_in/';

  getLoggedInStatus(): Observable<LoginStatus> {
    return this.http.get<LoginStatus>(this.apiUrl).pipe(
        catchError((): Observable<LoginStatus> => {
          const errorStatus: LoginStatus = {
            loggedIn: false
          };

          return of<LoginStatus>(errorStatus);
        })
    );
  }

}
