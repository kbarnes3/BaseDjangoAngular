import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService, SignupData } from '../auth.service';

@Component({
  selector: 'app-signup',
  imports: [FormsModule, RouterModule],
  templateUrl: './signup.component.html',
})
export class SignupComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  email = '';
  firstName = '';
  lastName = '';
  password = '';
  errorMessage = '';
  loading = false;

  onSubmit(): void {
    this.loading = true;
    this.errorMessage = '';
    const data: SignupData = {
      email: this.email,
      first_name: this.firstName,
      last_name: this.lastName,
      password: this.password,
    };
    this.authService.signup(data).subscribe({
      next: () => {
        this.router.navigate(['/']);
      },
      error: (err) => {
        this.loading = false;
        if (err.status === 401 && err.error?.data?.flows) {
          const flows = err.error.data.flows;
          if (flows.some((f: { id: string }) => f.id === 'verify_email')) {
            this.router.navigate(['/verify-email']);
            return;
          }
        }
        if (err.error?.errors?.length) {
          this.errorMessage = err.error.errors.map((e: { message: string }) => e.message).join(' ');
        } else {
          this.errorMessage = 'Signup failed. Please try again.';
        }
      }
    });
  }
}
