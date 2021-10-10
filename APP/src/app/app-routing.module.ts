import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { IndexComponent } from './components/index/index.component';
import { HomeComponent } from './components/home/home.component';

const routes: Routes = [
  { path: 'Home',component: HomeComponent},
  { path: 'Analizador',component: IndexComponent},
  { path: '', redirectTo: '/Home', pathMatch: 'full' },
  { path: '**', redirectTo: '/Home', pathMatch: 'full' },
];

@NgModule({
  imports: [
    RouterModule.forRoot(
      routes,
    {
      useHash: true,
      onSameUrlNavigation: 'ignore',
    }),
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
