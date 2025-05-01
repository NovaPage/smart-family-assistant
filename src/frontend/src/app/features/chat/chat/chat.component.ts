import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AssistantService } from '../../../core/services/assistant.service';
import { ChatMessage } from '../../../models/interaction.model';
import { NavbarComponent } from "../../../shared/navbar.component";
import { Send, LucideAngularModule } from 'lucide-angular';
import { UserService } from '../../../core/services/user.service';
import { UserProfile } from '../../../models/user.model'; 

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, NavbarComponent, LucideAngularModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss']
})
export class ChatComponent implements OnInit {
  Send = Send;
  messages: ChatMessage[] = [];
  inputMessage = '';
  isLoading = false;

  user: UserProfile | null = null;
  userName = '';

  constructor(
    private assistantService: AssistantService,
    private userService: UserService
  ) {}

  ngOnInit(): void {
    this.userService.getProfile().subscribe({
      next: (user) => {
        this.user = user;
        this.userName = user?.name ?? 'User';
      },
      error: (err) => {
        console.error('Error getting user:', err);
        this.userName = 'User';
      }
    });
    
    this.userName = this.user?.name ?? 'User';
  }

  sendMessage(): void {
    if (!this.inputMessage.trim()) return;

    const userMessage: ChatMessage = {
      sender: 'user',
      content: this.inputMessage
    };

    this.messages.push(userMessage);
    this.isLoading = true;

    this.assistantService.sendMessage({
      message: this.inputMessage,
      source: 'web'
    }).subscribe({
      next: (response) => {
        this.messages.push({
          sender: 'assistant',
          content: response.response
        });
        this.isLoading = false;
      },
      error: (err) => {
        this.messages.push({
          sender: 'assistant',
          content: '❌ Error getting response.'
        });
        this.isLoading = false;
        console.error(err);
      }
    });

    this.inputMessage = '';
  }
}
