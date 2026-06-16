import { Component, inject, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-verify-email',
  imports: [RouterModule, MatCardModule, MatButtonModule, MatProgressSpinnerModule],
  templateUrl: './verify-email.component.html',
  styleUrls: ['../auth-form.scss'],
})
export class VerifyEmailComponent implements OnInit {
  private authService = inject(AuthService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  message = '';
  errorMessage = '';
  loading = false;
  verified = false;
  pendingVerification = false;

  ngOnInit(): void {
    const key = this.route.snapshot.paramMap.get('key');
    if (key) {
      this.verify(key);
    } else {
      this.pendingVerification = true;
      this.message = 'A verification email has been sent. Please check your inbox and click the link to verify your email address.';
    }
  }

  verify(key: string): void {
    this.loading = true;
    this.authService.verifyEmail({ key }).subscribe({
      next: () => {
        this.verified = true;
        this.message = 'Your email has been verified successfully!';
        this.loading = false;
      },
      error: (err) => {
        this.loading = false;
        if (err.status === 401) {
          // Email verified but user not auto-logged in
          this.verified = true;
          this.message = 'Your email has been verified. Please log in.';
          return;
        }
        if (err.error?.errors?.length) {
          this.errorMessage = err.error.errors.map((e: { message: string }) => e.message).join(' ');
        } else {
          this.errorMessage = 'Invalid or expired verification link.';
        }
      }
    });
  }
}
