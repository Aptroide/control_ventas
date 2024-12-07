// main.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideHttpClient } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations'; // Importa provideAnimations

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(),
    provideAnimations() // Añade provideAnimations aquí
  ]
}).catch(err => console.error(err));