import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  // URL do endpoint para onde os dados serão enviados
  private apiUrl = 'http://127.0.0.1:8000/data';  // Substitua com o URL real

  constructor(private http: HttpClient) {}

  // Método para enviar dados com POST
  sendData(dados: any): Observable<any> {
    return this.http.post(this.apiUrl, dados);
  }

}
