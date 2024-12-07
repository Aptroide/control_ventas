// api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

interface PredictionResponse {
  prediction: string;
  prediction1: string;
  prediction2: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private urlAPI = environment.API_URL || 'http://127.0.0.1:8000/predict';

  constructor(private http: HttpClient) { }

  public getPrediction(date: string): Observable<PredictionResponse> {
    const body = { fecha: date };
    return this.http.post<PredictionResponse>(this.urlAPI, body);
  }
}