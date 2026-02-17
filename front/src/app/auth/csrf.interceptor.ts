import { HttpInterceptorFn } from '@angular/common/http';
import { inject, DOCUMENT } from '@angular/core';

// Django requires a CSRF token on all mutating requests. This interceptor
// reads the token from the "csrftoken" cookie (set by Django) and attaches
// it as the "X-CSRFToken" header so that Django's CsrfViewMiddleware accepts
// requests made by the Angular app.
export const csrfInterceptor: HttpInterceptorFn = (req, next) => {
  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(req.method)) {
    const document = inject(DOCUMENT);
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    const csrfToken = match ? match[1] : '';
    if (csrfToken) {
      req = req.clone({
        setHeaders: { 'X-CSRFToken': csrfToken }
      });
    }
  }
  return next(req);
};
