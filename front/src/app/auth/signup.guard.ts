import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { ConfigService } from '../config.service';
import { map } from 'rxjs/operators';

export const signupGuard: CanActivateFn = () => {
  const configService = inject(ConfigService);
  const router = inject(Router);

  return configService.getAccountCreationMode().pipe(
    map(mode => {
      if (mode === 'disabled') {
        return router.createUrlTree(['/login']);
      }
      return true;
    })
  );
};
