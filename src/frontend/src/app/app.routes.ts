import { Routes } from '@angular/router';
import { LoginComponent } from './features/auth/login/login.component';
import { RegisterComponent } from './features/auth/register/register.component';
import { ProfileComponent } from './features/profile/profile/profile.component';
import { ChatComponent } from './features/chat/chat/chat.component';

export const routes: Routes = [
    { path: 'auth/login', component: LoginComponent },
    { path: 'auth/register', component: RegisterComponent },
    { path: 'profile', component: ProfileComponent },
    { path: 'chat', component: ChatComponent },
    { path: '', redirectTo: 'auth/login', pathMatch: 'full' },
    { path: '**', redirectTo: 'auth/login' }
];
