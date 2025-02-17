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
    isRegisterForm = false;

    toggleForm() {
      this.isRegisterForm = !this.isRegisterForm;
    }

    registerUser(user: string, password: string, confirmPassword:string) {
      if (password !== confirmPassword) {
        alert('As senhas não coincidem!');
        return;
      }
      const formData = new FormData();
      formData.append('user', user);
      formData.append('password', password);
      

      this.service.register(formData).subscribe({
        next:(v) => {
          console.log(v)
        },
        error:(e) => console.error(e),
        complete:() => console.info('created')
      });
    }

    login(user: string, password: string) {

      const formData = new FormData();
      formData.append('username', user);
      formData.append('password', password);

      this.service.login(formData).subscribe({
        next:(response) => {
          localStorage.setItem("accessToken", response.access_token);
        },
        error:(e) => console.error(e),
        complete:() => {
          if(localStorage.getItem("accessToken") != null){
            window.location.href = "/notes"
          }
        }
      });


    }
}
