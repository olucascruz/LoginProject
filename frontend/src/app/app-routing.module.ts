import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { NoteComponent } from './pages/note/note.component';
import { LoginComponent } from './pages/login/login.component';
import { NoteDetailComponent } from './pages/note-detail/note-detail.component';

const routes: Routes = [
  {path:'', component: LoginComponent},
  {path: 'note/:id', component: NoteDetailComponent},
  {path:'notes', component:NoteComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
