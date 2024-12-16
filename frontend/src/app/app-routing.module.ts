import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { NoteComponent } from './pages/note/note.component';
import { LoginComponent } from './pages/login/login.component';

const routes: Routes = [
  {path:'', component: LoginComponent},
  {path:'notes', component:NoteComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
