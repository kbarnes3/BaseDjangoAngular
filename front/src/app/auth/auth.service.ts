import { Injectable, inject, DOCUMENT } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const BASE_URL = '/_allauth/browser/v1';

export interface AuthResponse {
  status: number;
  data?: {
    user?: {
      id: number;
      display: string;
      email: string;
      first_name?: string;
      last_name?: string;
    };
    methods?: { method: string; at: number; email?: string }[];
    flows?: { id: string; [key: string]: unknown }[];
  };
  meta?: {
    is_authenticated: boolean;
    session_token?: string;
    access_token?: string;
  };
  errors?: { message: string; code: string; param?: string }[];
}

export interface SignupData {
  email: string;
  first_name: string;
  last_name: string;
  password: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface PasswordResetData {
  email: string;
}

export interface PasswordResetKeyData {
  key: string;
  password: string;
}

export interface PasswordChangeData {
  current_password: string;
  new_password: string;
}

export interface VerifyEmailData {
  key: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private document = inject(DOCUMENT);

  getSession(): Observable<AuthResponse> {
    return this.http.get<AuthResponse>(`${BASE_URL}/auth/session`);
  }

  login(data: LoginData): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${BASE_URL}/auth/login`, data);
  }

  signup(data: SignupData): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${BASE_URL}/auth/signup`, data);
  }

  logout(): Observable<AuthResponse> {
    return this.http.delete<AuthResponse>(`${BASE_URL}/auth/session`);
  }

  requestPasswordReset(data: PasswordResetData): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${BASE_URL}/auth/password/request`, data);
  }

  resetPassword(data: PasswordResetKeyData): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${BASE_URL}/auth/password/reset`, data);
  }

  getPasswordResetInfo(key: string): Observable<AuthResponse> {
    return this.http.get<AuthResponse>(`${BASE_URL}/auth/password/reset`, {
      headers: { 'X-Password-Reset-Key': key }
    });
  }

  changePassword(data: PasswordChangeData): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${BASE_URL}/account/password/change`, data);
  }

  verifyEmail(data: VerifyEmailData): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${BASE_URL}/auth/email/verify`, data);
  }

  getEmailVerificationInfo(key: string): Observable<AuthResponse> {
    return this.http.get<AuthResponse>(`${BASE_URL}/auth/email/verify`, {
      params: { key }
    });
  }

  getCsrfToken(): string {
    const match = this.document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
  }
}
