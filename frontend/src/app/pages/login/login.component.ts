import { Component } from '@angular/core';
import { ApiService } from '../../service/api.service';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  constructor(private service: ApiService) {}

    sendData(user: string, password: string) {
      // if (!photo || photo.length === 0) {
      //   console.error('Nenhuma foto selecionada!');
      //   return;
      // }
      // const file = photo[0];

      const formData = new FormData();
      formData.append('user', user);
      formData.append('password', password);
      // formData.append('photo', file);

      this.service.register(formData).subscribe(
        (response: any) => {
          console.log('Resposta do servidor:', response);
        },
        (error:any) => {
          console.error('Erro ao enviar os dados:', error);
        }
      );
    }
}
