import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { ApiService } from './service/api.service';
import { forkJoin, map } from 'rxjs';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule, // Import CommonModule
    MatFormFieldModule, 
    MatInputModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatCardModule,
    MatButtonModule
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  selectedDate: Date | null = null;
  hideElement: boolean = true;
  prediction: string = 'Mateo';
  predictionSemana: string = 'Luis';
  predictionMes: string = 'Fernando';
  showCards: boolean = false;
  isLoading: boolean = false;

  constructor(private apiService: ApiService) { }

  onDateChange(event: any) {
    this.selectedDate = event.value;
  }

  getPredictionForDate(formattedDate: string): any {
    this.apiService.getPrediction(formattedDate).subscribe(
      (response: any) => {
        this.prediction = response.yhat.toFixed(2);
      },
      (error) => {
        console.error('Error al obtener la predicción', error);
      }
    );
  }

  onPredictClick() {
    if (this.selectedDate) {
      this.isLoading = true;
      const formattedDate = this.selectedDate.toISOString().split('T')[0];
      this.getPredictionForDate(formattedDate);

      forkJoin({
        week: this.weekPredict(this.selectedDate),
        month: this.monthPredict(this.selectedDate)
      }).subscribe({
        next: ({ week, month }) => {
          this.predictionSemana = week.toFixed(2);
          this.predictionMes = month.toFixed(2);

          this.showCards = true;
          this.hideElement = false;
          this.selectedDate = null;
          this.isLoading = false;
        },
        error: (error) => {
          console.error('Error al obtener las predicciones', error);
          this.isLoading = false;
        }
      });
    }
  }
  
  weekPredict(date: Date) {
    const dateObj = new Date(date);
    const dates = [];
    for (let i = -3; i <= 3; i++) {
      const newDate = new Date(dateObj);
      newDate.setDate(dateObj.getDate() + i);
      dates.push(newDate.toISOString().split('T')[0]);
    }
  
    const requests = dates.map(d => this.apiService.getPrediction(d));
  
    return forkJoin(requests).pipe(
      map((responses: any[]) => responses.reduce((sum, res) => sum + res.yhat, 0))
    );
  }
  
  monthPredict(date: Date) {
    const dateObj = new Date(date);
    const dates = [];
    for (let i = -15; i <= 15; i++) {
      const newDate = new Date(dateObj);
      newDate.setDate(dateObj.getDate() + i);
      dates.push(newDate.toISOString().split('T')[0]);
    }
  
    const requests = dates.map(d => this.apiService.getPrediction(d));
  
    return forkJoin(requests).pipe(
      map((responses: any[]) => responses.reduce((sum, res) => sum + res.yhat, 0))
    );
  }
  newPredict(){
    this.showCards = false;
    this.hideElement = true;
  }
}
