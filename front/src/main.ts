import { enableProdMode, importProvidersFrom, provideZoneChangeDetection } from '@angular/core';

import { environment } from './environments/environment';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { BrowserModule, bootstrapApplication } from '@angular/platform-browser';
import { provideAnimations } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app/app-routing.module';
import { AppComponent } from './app/app.component';
import { csrfInterceptor } from './app/auth/csrf.interceptor';

if (environment.production) {
  enableProdMode();
}

bootstrapApplication(AppComponent, {
    providers: [
        provideZoneChangeDetection(),importProvidersFrom(BrowserModule, AppRoutingModule),
        provideAnimations(),
        provideHttpClient(withInterceptors([csrfInterceptor]))
    ]
})
  .catch(err => console.error(err));
