import { HttpInterceptorFn } from '@angular/common/http';
import { inject, DOCUMENT } from '@angular/core';

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
