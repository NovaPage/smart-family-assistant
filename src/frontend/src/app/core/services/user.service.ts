import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UserProfile } from '../../models/user.model';

@Injectable({ providedIn: 'root' })
export class UserService {
  private readonly API = 'http://localhost:8000/api/v1/user';

  constructor(private http: HttpClient) {}

  getProfile(): Observable<UserProfile> {
    return this.http.get<UserProfile>(`${this.API}/profile`);
  }
}
