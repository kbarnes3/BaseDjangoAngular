import { Component, inject, ChangeDetectionStrategy, signal } from '@angular/core';
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
  changeDetection: ChangeDetectionStrategy.OnPush,
  styleUrls: ['../auth-form.scss'],
})
export class PasswordChangeComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  currentPassword = '';
  newPassword = '';
  successMessage = signal('');
  errorMessage = signal('');
  loading = signal(false);

  onSubmit(): void {
    this.loading.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');
    this.authService.changePassword({
      current_password: this.currentPassword,
      new_password: this.newPassword,
    }).subscribe({
      next: () => {
        this.loading.set(false);
        this.successMessage.set('Your password has been changed successfully!');
        this.currentPassword = '';
        this.newPassword = '';
      },
      error: (err) => {
        this.loading.set(false);
        if (err.error?.errors?.length) {
          this.errorMessage.set(err.error.errors.map((e: { message: string }) => e.message).join(' '));
        } else {
          this.errorMessage.set('Failed to change password.');
        }
      }
    });
  }
}
