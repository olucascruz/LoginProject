import { Component } from '@angular/core';

@Component({
  selector: 'app-note',
  templateUrl: './note.component.html',
  styleUrls: ['./note.component.css']
})
export class NoteComponent {
  items: string[] = ['Item 1', 'Item 2', 'Item 3', 'Item 4'];
}
