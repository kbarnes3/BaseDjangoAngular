import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService, LoginData } from '../auth.service';

@Component({
  selector: 'app-login',
  imports: [FormsModule, RouterModule],
  templateUrl: './login.component.html',
})
export class LoginComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  email = '';
  password = '';
  errorMessage = '';
  loading = false;

  onSubmit(): void {
    this.loading = true;
    this.errorMessage = '';
    const data: LoginData = { email: this.email, password: this.password };
    this.authService.login(data).subscribe({
      next: () => {
        this.router.navigate(['/']);
      },
      error: (err) => {
        this.loading = false;
        if (err.status === 401 && err.error?.data?.flows) {
          const flows = err.error.data.flows;
          if (flows.some((f: { id: string }) => f.id === 'verify_email')) {
            this.errorMessage = 'Please verify your email address before logging in.';
            return;
          }
        }
        if (err.error?.errors?.length) {
          this.errorMessage = err.error.errors.map((e: { message: string }) => e.message).join(' ');
        } else {
          this.errorMessage = 'Login failed. Please check your credentials.';
        }
      }
    });
  }
}
