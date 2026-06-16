import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-password-change',
  imports: [FormsModule, RouterModule, MatCardModule, MatFormFieldModule, MatInputModule, MatButtonModule],
  templateUrl: './password-change.component.html',
  styleUrls: ['../auth-form.scss'],
})
export class PasswordChangeComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  currentPassword = '';
  newPassword = '';
  successMessage = '';
  errorMessage = '';
  loading = false;

  onSubmit(): void {
    this.loading = true;
    this.errorMessage = '';
    this.successMessage = '';
    this.authService.changePassword({
      current_password: this.currentPassword,
      new_password: this.newPassword,
    }).subscribe({
      next: () => {
        this.loading = false;
        this.successMessage = 'Your password has been changed successfully!';
        this.currentPassword = '';
        this.newPassword = '';
      },
      error: (err) => {
        this.loading = false;
        if (err.error?.errors?.length) {
          this.errorMessage = err.error.errors.map((e: { message: string }) => e.message).join(' ');
        } else {
          this.errorMessage = 'Failed to change password.';
        }
      }
    });
  }
}
