import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';

export interface RegisterResponse {
  success: boolean;
  message: string;
  data: {
    id: number;
    user: string;
  };
}

export interface NoteResponse {
  id: number;
  title: string;
  content: string;
  created_at: string;
  updated_at: string;
}



@Injectable({
  providedIn: 'root'
})

export class ApiService {
  // URL do endpoint para onde os dados serão enviados
  private apiUrl = 'http://127.0.0.1:8000/';  // Substitua com o URL real

  tryGetTokenAccess(){
    const token = localStorage.getItem("accessToken");
    if(!token){
      window.location.href = "/";
      return null;
    }
    return token
  }

  getHeaders(): HttpHeaders {
    const token = this.tryGetTokenAccess()
    if(token==null){
      throw new Error("Token de acesso não encontrado. Faça login novamente.");
    }
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  }
  constructor(private http: HttpClient) {}

  register(data: FormData): Observable<RegisterResponse> {
    const url = this.apiUrl+'register'
    return this.http.post<RegisterResponse>(url, data);
  }

  login(data: FormData): Observable<any> {
    const url = this.apiUrl+'login'
    return this.http.post<any>(url, data);
  }

  createNote(formTitle:FormData): Observable<any>{
    const url = this.apiUrl+'note'
    const headers = this.getHeaders()
    return this.http.post<any>(url, formTitle, {headers});
  }

  updateNote(id:number, dataNote:FormData): Observable<any>{
    const url = this.apiUrl+'note/'+id.toString()
    const headers = this.getHeaders()
    return this.http.put<any>(url, dataNote, {headers});
  }

  getNotes(): Observable<NoteResponse[]>{
    const url = this.apiUrl+'note'
    const headers = this.getHeaders()
    return this.http.get<NoteResponse[]>(url, {headers});
  }

  getNoteById(id: number): Observable<NoteResponse> {
    const url = `${this.apiUrl}note/${id}`;
    const headers = this.getHeaders()
    return this.http.get<NoteResponse>(url, {headers});
  }
}
