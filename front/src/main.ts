import { enableProdMode, importProvidersFrom, provideZoneChangeDetection } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';


import { environment } from './environments/environment';
import { provideHttpClient, withInterceptors, withInterceptorsFromDi } from '@angular/common/http';
import { BrowserModule, bootstrapApplication } from '@angular/platform-browser';
import { AppRoutingModule } from './app/app-routing.module';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AppComponent } from './app/app.component';
import { csrfInterceptor } from './app/auth/csrf.interceptor';

if (environment.production) {
  enableProdMode();
}

bootstrapApplication(AppComponent, {
    providers: [
        provideZoneChangeDetection(),importProvidersFrom(BrowserModule, AppRoutingModule, NgbModule),
        provideHttpClient(withInterceptors([csrfInterceptor]))
    ]
})
  .catch(err => console.error(err));
