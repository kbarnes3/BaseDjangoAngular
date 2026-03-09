import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Observable, BehaviorSubject, of} from 'rxjs';
import {catchError} from 'rxjs/operators';
import { AuthResponse } from './auth/auth.service';

export class LoginStatus {
  loggedIn: boolean;
  displayName?: string;
}

@Injectable({
  providedIn: 'root'
})
export class LoginStatusService {
  private http = inject(HttpClient);
  private sessionUrl = '/_allauth/browser/v1/auth/session';

  private statusSubject = new BehaviorSubject<LoginStatus | null>(null);
  public status$ = this.statusSubject.asObservable();

  refreshStatus(): void {
    this.http.get<AuthResponse>(this.sessionUrl).pipe(
        catchError((): Observable<AuthResponse | null> => {
          return of(null);
        })
    ).subscribe(resp => {
      if (resp?.meta?.is_authenticated) {
        this.statusSubject.next({
          loggedIn: true,
          displayName: resp.data?.user?.display || '',
        });
      } else {
        this.statusSubject.next({ loggedIn: false });
      }
    });
  }

  getLoggedInStatus(): Observable<LoginStatus> {
    return new Observable(subscriber => {
      this.http.get<AuthResponse>(this.sessionUrl).pipe(
        catchError((): Observable<AuthResponse | null> => of(null))
      ).subscribe(resp => {
        if (resp?.meta?.is_authenticated) {
          subscriber.next({
            loggedIn: true,
            displayName: resp.data?.user?.display || '',
          });
        } else {
          subscriber.next({ loggedIn: false });
        }
        subscriber.complete();
      });
    });
  }

}
