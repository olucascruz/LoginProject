import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService, NoteResponse } from '../../service/api.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-note-detail',
  templateUrl: './note-detail.component.html',
  styleUrls: ['./note-detail.component.css']
})
export class NoteDetailComponent {
  note$!: Observable<NoteResponse>;

  constructor(
    private route: ActivatedRoute,
    private service: ApiService
  ) {}

  ngOnInit(): void {
    const noteId = Number(this.route.snapshot.paramMap.get('id'));
    this.note$ = this.service.getNoteById(noteId);

  }

  saveNote(id:number, noteTitle:string, noteContent:string){
    const formData = new FormData();
    formData.append('note_title', noteTitle);
    formData.append('note_content', noteContent);

    this.service.updateNote(id, formData).subscribe(
      (response: any) => {
        console.log('Resposta do servidor:', response);
      },
      (error:any) => {
        console.error('Erro ao enviar os dados:', error);
      }
    );
  }

}
