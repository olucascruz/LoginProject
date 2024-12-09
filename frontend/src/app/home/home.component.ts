import { Component } from '@angular/core';
import { ApiService } from '../service/api.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  data = { nome: 'Lucas', idade: 25 };

  constructor(private service: ApiService) {}

  enviar(user: string, password: string, photo: FileList | null) {
    if (!photo || photo.length === 0) {
      console.error('Nenhuma foto selecionada!');
      return;
    }

    const file = photo[0];
    const formData = new FormData();
    formData.append('user', user);
    formData.append('password', password);
    formData.append('photo', file);

    this.service.sendData(formData).subscribe(
      response => {
        console.log('Resposta do servidor:', response);
      },
      error => {
        console.error('Erro ao enviar os dados:', error);
      }
    );
  }
}
