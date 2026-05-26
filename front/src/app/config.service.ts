import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

export type AccountCreationMode = 'default' | 'notify' | 'disabled';

interface SiteConfig {
  account_creation_mode: AccountCreationMode;
}

@Injectable({
  providedIn: 'root'
})
export class ConfigService {
  private http = inject(HttpClient);

  private modeSubject = new BehaviorSubject<AccountCreationMode>('disabled');
  public accountCreationMode$ = this.modeSubject.asObservable();

  refreshConfig(): void {
    this.http.get<SiteConfig>('/api/config/').pipe(
      catchError(() => {
        return [{ account_creation_mode: 'disabled' as AccountCreationMode }];
      })
    ).subscribe(config => {
      this.modeSubject.next(config.account_creation_mode);
    });
  }

  getAccountCreationMode(): Observable<AccountCreationMode> {
    return this.http.get<SiteConfig>('/api/config/').pipe(
      map(config => config.account_creation_mode),
      catchError(() => ['disabled' as AccountCreationMode])
    );
  }

  get signupEnabled(): boolean {
    return this.modeSubject.value !== 'disabled';
  }
}
