import { Component, inject, ChangeDetectionStrategy, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { AuthService, SignupData } from '../auth.service';

@Component({
  selector: 'app-signup',
  imports: [FormsModule, RouterModule, MatCardModule, MatFormFieldModule, MatInputModule, MatButtonModule],
  templateUrl: './signup.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  styleUrls: ['../auth-form.scss'],
})
export class SignupComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  email = '';
  firstName = '';
  lastName = '';
  password = '';
  errorMessage = signal('');
  loading = signal(false);

  onSubmit(): void {
    this.loading.set(true);
    this.errorMessage.set('');
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
        this.loading.set(false);
        if (err.status === 401 && err.error?.data?.flows) {
          const flows = err.error.data.flows;
          if (flows.some((f: { id: string }) => f.id === 'verify_email')) {
            this.router.navigate(['/verify-email']);
            return;
          }
        }
        if (err.error?.errors?.length) {
          this.errorMessage.set(err.error.errors.map((e: { message: string }) => e.message).join(' '));
        } else {
          this.errorMessage.set('Signup failed. Please try again.');
        }
      }
    });
  }
}
