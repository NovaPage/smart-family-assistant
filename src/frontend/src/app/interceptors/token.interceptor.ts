import { HttpInterceptorFn } from '@angular/common/http';
import { HttpRequest, HttpHandlerFn } from '@angular/common/http';

export const tokenInterceptor: HttpInterceptorFn = (req: HttpRequest<unknown>, next: HttpHandlerFn) => {
  const token = localStorage.getItem('token');
  const cloned = token
    ? req.clone({
        headers: req.headers.set('Authorization', `Bearer ${token}`),
      })
    : req;

  return next(cloned);
};
