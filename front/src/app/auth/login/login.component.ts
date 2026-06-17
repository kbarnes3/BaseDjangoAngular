import { Component, inject, OnInit, ChangeDetectionStrategy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { AuthService, LoginData } from '../auth.service';
import { LoginStatusService } from '../../login-status.service';
import { ConfigService } from '../../config.service';

@Component({
  selector: 'app-login',
  imports: [FormsModule, RouterModule, MatCardModule, MatFormFieldModule, MatInputModule, MatButtonModule],
  templateUrl: './login.component.html',
  changeDetection: ChangeDetectionStrategy.Eager,
  styleUrls: ['../auth-form.scss'],
})
export class LoginComponent implements OnInit {
  private authService = inject(AuthService);
  private loginStatusService = inject(LoginStatusService);
  private configService = inject(ConfigService);
  private router = inject(Router);

  email = '';
  password = '';
  errorMessage = '';
  loading = false;
  signupEnabled = true;

  ngOnInit(): void {
    this.configService.getAccountCreationMode().subscribe(mode => {
      this.signupEnabled = mode !== 'disabled';
    });
  }

  onSubmit(): void {
    this.loading = true;
    this.errorMessage = '';
    const data: LoginData = { email: this.email, password: this.password };
    this.authService.login(data).subscribe({
      next: () => {
        this.loginStatusService.refreshStatus();
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
