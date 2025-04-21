import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { AuthResponse } from '../../models/auth.model';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly API = 'http://localhost:8000/api/v1/auth';

  constructor(private http: HttpClient) {}

  login(formEncodedBody: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.API}/login`, formEncodedBody, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).pipe(
      tap((res) => localStorage.setItem('token', res.access_token))
    );
  }

  register(payload: { name: string; email: string; password: string }): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.API}/register`, payload).pipe(
      tap((res) => localStorage.setItem('token', res.access_token))
    );
  }

  logout(): void {
    localStorage.removeItem('token');
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }
}
