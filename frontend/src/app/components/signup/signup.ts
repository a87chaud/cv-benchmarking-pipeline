import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-signup',
  templateUrl: './signup.html',
  imports: [FormsModule],
  styleUrls: ['./signup.css']
})
export class SignupComponent {
  constructor(private router: Router) {}

  onSubmit() {
    alert("Signup submitted!");
    // Replace with real signup logic
  }

  navigateTo(page: string) {
    this.router.navigate([`/${page}`]);
  }
}
