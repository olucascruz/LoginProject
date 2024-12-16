import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface RegisterResponse {
  success: boolean;
  message: string;
  data: {
    id: number;
    user: string;
  };
}




@Injectable({
  providedIn: 'root'
})

export class ApiService {
  // URL do endpoint para onde os dados serão enviados
  private apiUrl = 'http://127.0.0.1:8000/';  // Substitua com o URL real

  constructor(private http: HttpClient) {}

  register(data: FormData): Observable<RegisterResponse> {
    const url = this.apiUrl+'register'
    return this.http.post<RegisterResponse>(this.apiUrl, data);
  }

  createNote(formTitle:str): Observable<any>{
    return null
  }

}
