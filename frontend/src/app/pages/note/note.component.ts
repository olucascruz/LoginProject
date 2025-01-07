import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService, NoteResponse } from '../../service/api.service'
import { Router } from '@angular/router';

@Component({
  selector: 'app-note',
  templateUrl: './note.component.html',
  styleUrls: ['./note.component.css']
})
export class NoteComponent implements OnInit{
  notes$!: Observable<NoteResponse[]> | null;
  constructor(private service: ApiService,  private router: Router) {}
  ngOnInit(): void {
    console.log(localStorage.getItem("accessToken"))
     this.notes$ = this.service.getNotes()
     console.log(this.notes$)
  }
  goToNoteDetail(id:number):void{
    this.router.navigate([`/note/${id}`]);
  }

  createNote(noteTitle:string):void{
    const formData = new FormData();
    formData.append('note_title', noteTitle);
    console.log(formData)
    const response = this.service.createNote(formData).subscribe(
      (response: any) => {
        console.log('Resposta do servidor:', response);
        this.notes$ = this.service.getNotes()
        this.notes$?.subscribe((response)=>{
          console.log(response)
          const endIndex = response.length - 1
          // this.goToNoteDetail(response[endIndex].id)
        }, (err)=>{
          console.warn(err)
        })

      },
      (error:any) => {
        console.error('Erro ao enviar os dados:', error);
      }
    );
  }

  deleteNote(id:number):void{
    this.service.deleteNote(id).subscribe(
      (response: any) => {
        console.log('Resposta do servidor:', response);
        this.notes$ = this.service.getNotes()
        this.notes$?.subscribe((response)=>{
          console.log(response)
        }, (err)=>{
          console.warn(err)
        })

      },
      (error:any) => {
        console.error('Erro ao enviar os dados:', error);
      }
    );
  }


}
