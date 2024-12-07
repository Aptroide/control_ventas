import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private urlAPI = 'http://localhost:5000/api/predict';

  constructor(private http: HttpClient) { }

  public getPrediction(date: string) {
    return this.http.get(this.urlAPI + '?date=' + date);
  }

}
