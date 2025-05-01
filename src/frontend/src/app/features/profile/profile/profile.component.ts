import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { UserProfile } from '../../../models/user.model';
import { environment } from '../../../environment';
import { NavbarComponent } from "../../../shared/navbar.component";
import { Link, LucideAngularModule } from 'lucide-angular';


@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, NavbarComponent, LucideAngularModule],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  Link = Link;
  user: UserProfile | null = null;
  telegramLink = '';
  readonly botUsername = 'EvanaFamilYBot';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.http.get<UserProfile>(`${environment.API_BASE_URL}/user/profile`).subscribe({
      next: (profile) => {
        this.user = profile;
        this.telegramLink = `https://t.me/${this.botUsername}?start=${profile.telegram_token}`;
      },
      error: (err) => {
        console.error('Error loading profile', err);
      }
    });
  }
}
