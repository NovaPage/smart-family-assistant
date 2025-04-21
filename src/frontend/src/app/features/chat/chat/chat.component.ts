import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AssistantService } from '../../../core/services/assistant.service';
import { ChatMessage } from '../../../models/interaction.model';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.component.html'
})
export class ChatComponent {
  messages: ChatMessage[] = [];
  inputMessage = '';
  isLoading = false;

  constructor(private assistantService: AssistantService) {}

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
