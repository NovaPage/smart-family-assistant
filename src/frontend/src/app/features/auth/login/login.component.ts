import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { LucideAngularModule, Mail, Lock, Eye, EyeOff, Loader } from 'lucide-angular';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    LucideAngularModule
  ],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  form: FormGroup;
  error: string | null = null;
  isLoading = false;


  // Icon references
  Mail = Mail;
  Lock = Lock;
  Eye = Eye;
  EyeOff = EyeOff;
  Loader = Loader;


  showPassword = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.form = this.fb.group({
      username: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
  }

  onSubmit(): void {
    if (this.form.invalid) return;

    this.isLoading = true;
    this.error = null;

    const body = new URLSearchParams();
    body.set('username', this.form.value.username);
    body.set('password', this.form.value.password);

    this.authService.login(body.toString()).subscribe({
      next: () => this.router.navigate(['/profile']),
      error: () => {
        this.error = 'Login failed. Please check your credentials.';
        this.isLoading = false;
      }
    });
  }


  get passwordInputType(): 'text' | 'password' {
    return this.showPassword ? 'text' : 'password';
  }

  togglePasswordVisibility(): void {
    this.showPassword = !this.showPassword;
  }
}
