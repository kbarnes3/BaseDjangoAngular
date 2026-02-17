import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Observable, BehaviorSubject, of} from 'rxjs';
import {catchError, tap} from 'rxjs/operators';

export class LoginStatus {
  loggedIn: boolean;
  firstName?: string;
  lastName?: string;
}

@Injectable({
  providedIn: 'root'
})
export class LoginStatusService {
  private http = inject(HttpClient);
  private apiUrl: string = '/api/account/logged_in/';

  private statusSubject = new BehaviorSubject<LoginStatus | null>(null);
  public status$ = this.statusSubject.asObservable();

  refreshStatus(): void {
    this.http.get<LoginStatus>(this.apiUrl).pipe(
        catchError((): Observable<LoginStatus> => {
          return of<LoginStatus>({ loggedIn: false });
        })
    ).subscribe(status => this.statusSubject.next(status));
  }

  getLoggedInStatus(): Observable<LoginStatus> {
    return this.http.get<LoginStatus>(this.apiUrl).pipe(
        catchError((): Observable<LoginStatus> => {
          return of<LoginStatus>({ loggedIn: false });
        })
    );
  }

}
