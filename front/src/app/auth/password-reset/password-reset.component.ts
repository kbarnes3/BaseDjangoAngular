import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-password-reset',
  imports: [FormsModule, RouterModule, MatCardModule, MatFormFieldModule, MatInputModule, MatButtonModule],
  templateUrl: './password-reset.component.html',
  styleUrls: ['../auth-form.scss'],
})
export class PasswordResetComponent {
  private authService = inject(AuthService);

  email = '';
  successMessage = '';
  errorMessage = '';
  loading = false;

  onSubmit(): void {
    this.loading = true;
    this.errorMessage = '';
    this.successMessage = '';
    this.authService.requestPasswordReset({ email: this.email }).subscribe({
      next: () => {
        this.loading = false;
        this.successMessage = 'If an account exists with that email, a password reset link has been sent.';
      },
      error: (err) => {
        this.loading = false;
        // allauth returns 200 even for non-existent emails to prevent enumeration
        // but handle errors just in case
        if (err.error?.errors?.length) {
          this.errorMessage = err.error.errors.map((e: { message: string }) => e.message).join(' ');
        } else {
          this.successMessage = 'If an account exists with that email, a password reset link has been sent.';
        }
      }
    });
  }
}
