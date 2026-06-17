import { Component, inject, OnInit, ChangeDetectionStrategy, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-password-reset-confirm',
  imports: [FormsModule, RouterModule, MatCardModule, MatFormFieldModule, MatInputModule, MatButtonModule, MatProgressSpinnerModule],
  templateUrl: './password-reset-confirm.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  styleUrls: ['../auth-form.scss'],
})
export class PasswordResetConfirmComponent implements OnInit {
  private authService = inject(AuthService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  key = '';
  password = '';
  successMessage = signal('');
  errorMessage = signal('');
  loading = signal(false);
  keyValid = signal(false);
  keyChecking = signal(true);

  ngOnInit(): void {
    this.key = this.route.snapshot.paramMap.get('key') || '';
    if (this.key) {
      this.authService.getPasswordResetInfo(this.key).subscribe({
        next: () => {
          this.keyValid.set(true);
          this.keyChecking.set(false);
        },
        error: () => {
          this.keyChecking.set(false);
          this.errorMessage.set('This password reset link is invalid or has expired.');
        }
      });
    } else {
      this.keyChecking.set(false);
      this.errorMessage.set('No reset key provided.');
    }
  }

  onSubmit(): void {
    this.loading.set(true);
    this.errorMessage.set('');
    this.authService.resetPassword({ key: this.key, password: this.password }).subscribe({
      next: () => {
        this.successMessage.set('Your password has been reset successfully!');
        this.loading.set(false);
      },
      error: (err) => {
        this.loading.set(false);
        // 401 means password was reset but user is not auto-logged in
        if (err.status === 401) {
          this.successMessage.set('Your password has been reset successfully! Please log in.');
          return;
        }
        if (err.error?.errors?.length) {
          this.errorMessage.set(err.error.errors.map((e: { message: string }) => e.message).join(' '));
        } else {
          this.errorMessage.set('Failed to reset password. The link may have expired.');
        }
      }
    });
  }
}
