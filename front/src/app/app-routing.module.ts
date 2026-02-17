import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { LoginComponent } from './auth/login/login.component';
import { SignupComponent } from './auth/signup/signup.component';
import { VerifyEmailComponent } from './auth/verify-email/verify-email.component';
import { PasswordResetComponent } from './auth/password-reset/password-reset.component';
import { PasswordResetConfirmComponent } from './auth/password-reset-confirm/password-reset-confirm.component';
import { PasswordChangeComponent } from './auth/password-change/password-change.component';
import { authGuard } from './auth/auth.guard';


const routes: Routes = [
  { path: '',
    pathMatch: 'full',
    component: LandingPageComponent },
  { path: 'login', component: LoginComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'verify-email', component: VerifyEmailComponent },
  { path: 'verify-email/:key', component: VerifyEmailComponent },
  { path: 'password-reset', component: PasswordResetComponent },
  { path: 'password-reset/key/:key', component: PasswordResetConfirmComponent },
  { path: 'password-change', component: PasswordChangeComponent, canActivate: [authGuard] },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
