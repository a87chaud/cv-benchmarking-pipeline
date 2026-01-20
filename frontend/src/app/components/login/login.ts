import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.html',
  imports: [FormsModule],
  styleUrls: ['./login.css']
})
export class LoginComponent {
  constructor(private router: Router) {}

  onSubmit() {
    alert("Login submitted!");
    // Replace with real login logic
  }

  navigateTo(page: string) {
    this.router.navigate([`/${page}`]);
  }
}
