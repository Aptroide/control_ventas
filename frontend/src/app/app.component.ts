import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';

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
  prediction1: string = 'Luis';
  prediction2: string = 'Fernando';
  showCards: boolean = false;

  onDateChange(event: any) {
    this.selectedDate = event.value;
  }
  onPredictClick() {
    if (this.selectedDate) {
      
      this.showCards = true;
      this.hideElement = false;
      // Put date on format YYYY-MM-DD
      let date = this.selectedDate.toISOString().split('T')[0];
      console.log('Selected Date:', date);
      this.selectedDate = null
    } else {
      console.log('No date selected');
    }
  }

  newPredict(){
    this.showCards = false;
    this.hideElement = true;
  }
}