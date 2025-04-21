import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Interaction } from '../../models/interaction.model';

@Injectable({ providedIn: 'root' })
export class AssistantService {
  private readonly API = 'http://localhost:8000/api/v1/assistant';

  constructor(private http: HttpClient) {}

  sendMessage(message: string): Observable<Interaction> {
    return this.http.post<Interaction>(`${this.API}/message`, { message });
  }
}
