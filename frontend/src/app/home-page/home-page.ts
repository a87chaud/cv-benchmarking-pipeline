import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home-page',
  imports: [],
  templateUrl: './home-page.html',
  styleUrl: './home-page.css'
})
export class HomePage {
  private router = inject(Router)
  
  navigateTo(page: string) {
    this.router.navigate([`/${page}`]);
  }
}
