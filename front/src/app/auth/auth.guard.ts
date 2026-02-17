import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { LoginStatusService } from '../login-status.service';
import { map } from 'rxjs/operators';

export const authGuard: CanActivateFn = () => {
  const loginStatusService = inject(LoginStatusService);
  const router = inject(Router);

  return loginStatusService.getLoggedInStatus().pipe(
    map(status => {
      if (status.loggedIn) {
        return true;
      }
      return router.createUrlTree(['/login']);
    })
  );
};
