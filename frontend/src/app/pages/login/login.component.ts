import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../service/api.service';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit{
  constructor(private service: ApiService) {}
  ngOnInit(): void {
    localStorage.removeItem("accessToken")
  }
    isRegisterForm = false; // Inicialmente exibe o formulário de Login

    toggleForm() {
      this.isRegisterForm = !this.isRegisterForm; // Alterna entre true e false
    }

    registerUser(user: string, password: string, confirmPassword:string) {
      if (password !== confirmPassword) {
        alert('As senhas não coincidem!');
        return;
      }
      const formData = new FormData();
      formData.append('user', user);
      formData.append('password', password);
      this.service.register(formData).subscribe(
        (response: any) => {
          console.log('Resposta do servidor:', response);
        },
        (error:any) => {
          console.error('Erro ao enviar os dados:', error);
        }
      );
    }

    login(user: string, password: string) {

      const formData = new FormData();
      formData.append('username', user);
      formData.append('password', password);
      this.service.login(formData).subscribe(
        (response: any) => {
          console.log('Resposta do servidor:', response);
          // Salvar o token no localStorage
          localStorage.setItem("accessToken", response.access_token);
          if(localStorage.getItem("accessToken") != null){
            window.location.href = "/notes"
          }
        },
        (error:any) => {
          console.error('Erro ao enviar os dados:', error);
        }
      );


    }
}
