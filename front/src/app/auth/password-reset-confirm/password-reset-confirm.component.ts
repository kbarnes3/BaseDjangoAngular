import { Component, inject, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-password-reset-confirm',
  imports: [FormsModule, RouterModule],
  templateUrl: './password-reset-confirm.component.html',
})
export class PasswordResetConfirmComponent implements OnInit {
  private authService = inject(AuthService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  key = '';
  password = '';
  successMessage = '';
  errorMessage = '';
  loading = false;
  keyValid = false;
  keyChecking = true;

  ngOnInit(): void {
    this.key = this.route.snapshot.paramMap.get('key') || '';
    if (this.key) {
      this.authService.getPasswordResetInfo(this.key).subscribe({
        next: () => {
          this.keyValid = true;
          this.keyChecking = false;
        },
        error: () => {
          this.keyChecking = false;
          this.errorMessage = 'This password reset link is invalid or has expired.';
        }
      });
    } else {
      this.keyChecking = false;
      this.errorMessage = 'No reset key provided.';
    }
  }

  onSubmit(): void {
    this.loading = true;
    this.errorMessage = '';
    this.authService.resetPassword({ key: this.key, password: this.password }).subscribe({
      next: () => {
        this.successMessage = 'Your password has been reset successfully!';
        this.loading = false;
      },
      error: (err) => {
        this.loading = false;
        if (err.error?.errors?.length) {
          this.errorMessage = err.error.errors.map((e: { message: string }) => e.message).join(' ');
        } else {
          this.errorMessage = 'Failed to reset password. The link may have expired.';
        }
      }
    });
  }
}
