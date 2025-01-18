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
  }
  goToNoteDetail(id:number):void{
    this.router.navigate([`/note/${id}`]);
  }

  createNote(noteTitle:string):void{
    const formData = new FormData();
    formData.append('note_title', noteTitle);

    this.service.createNote(formData).subscribe({
      next: (v) => console.log(v),
      error: (e) => console.error(e),
      complete: () => {
        this.notes$ = this.service.getNotes()
        console.info('complete')
      }
  });


  }

  deleteNote(id:number):void{
    this.service.deleteNote(id).subscribe({
      next:(response) => {
        console.log('Resposta do servidor:', response);
        },
      error:(e)=> console.error(e),
      complete: () => {
        this.notes$ = this.service.getNotes()
        console.info('complete')
      }
    });
  }


}
