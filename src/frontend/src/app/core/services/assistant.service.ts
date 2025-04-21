import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AssistantRequest, AssistantResponse } from '../../models/interaction.model';
import { environment } from '../../environment';

@Injectable({ providedIn: 'root' })
export class AssistantService {
  private readonly API = `${environment.API_BASE_URL}/assistant/message`;

  constructor(private http: HttpClient) {}

  sendMessage(payload: AssistantRequest): Observable<AssistantResponse> {
    return this.http.post<AssistantResponse>(this.API, payload);
  }
}
