
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';
import {FormsModule} from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ReactiveFormsModule } from '@angular/forms';
import { DevExtremeModule } from 'devextreme-angular';
import { DxPopupModule, DxButtonModule, DxTemplateModule } from 'devextreme-angular';
import { IndexComponent } from './components/index/index.component';
import { CodemirrorModule } from '@ctrl/ngx-codemirror';
import { HomeComponent } from './components/home/home.component';

@NgModule({
  declarations: [
    AppComponent,
    IndexComponent,
    HomeComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    DevExtremeModule,
    DxPopupModule,
    DxButtonModule,
    DxTemplateModule,
    HttpClientModule,
    FormsModule,
    CodemirrorModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
