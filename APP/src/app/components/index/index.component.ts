import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { IndexService } from 'src/app/services/index.service';
import {Pestaña} from 'src/app/models/pestaña';
import 'codemirror/mode/go/go';
import 'codemirror/mode/markdown/markdown';
import 'codemirror/mode/xml/xml';
import 'codemirror/addon/fold/xml-fold';
import 'codemirror/mode/julia/julia';
import 'codemirror/mode/go/go';

import 'codemirror/mode/javascript/javascript';
import 'codemirror/addon/fold/foldgutter';
import 'codemirror/addon/fold/brace-fold';
import 'codemirror/lib/codemirror';
import 'codemirror/addon/edit/closebrackets';
import 'codemirror/addon/edit/matchbrackets';
import 'codemirror/addon/lint/lint';
import 'codemirror/addon/lint/json-lint';
import 'codemirror/addon/fold/xml-fold';
import {graphviz} from 'd3-graphviz'
import { COMPILADORService } from 'src/app/services/compilador.service';
import { Contenido } from 'src/app/models/contenido';


@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.scss']
})
export class IndexComponent implements OnInit {
  
  @ViewChild('graphContainer', { static: false }) graph: ElementRef;

  Pestanas: Array<Pestaña> = [];
  NumTab = 0;
  NumError = 1;
  AST = ''
  ContenidoTab = '';
  actual:any = undefined;
  showSecondPopup2 = false;
  showSecondPopup3 = false;
  showSecondPopup = false;
  CONTENT = '';
  CONSOLA = '';
  errores: any;
  simbolos:any;
  buttons: Array<any> = [
    {
      location: 'after',
      widget: 'dxButton',
      options: {
        icon: 'plus',
        hint: 'Agregar',
        stylingMode: 'contained',
        onClick: this.AnadirPestana.bind(this),
      },
    },
    {
      location: 'after',
      widget: 'dxButton',
      options: {
        icon: 'image',
        hint: 'AST',
        stylingMode: 'contained',
        onClick: this.GRAFICAR.bind(this),
      },
    },
    {
      location: 'after',
      widget: 'dxButton',
      options: {
        icon: 'contentlayout',
        hint: 'ERROR',
        stylingMode: 'contained',
        onClick: this.GRAFICAR2.bind(this),
      },
    },
    {
      location: 'after',
      widget: 'dxButton',
      options: {
        icon: 'contentlayout',
        hint: 'SIMBOLOS',
        stylingMode: 'contained',
        onClick: this.GRAFICAR3.bind(this),
      },
    },
    {
      location: 'after',
      widget: 'dxButton',
      options: {
        icon: 'video',
        hint: 'Compilar',
        stylingMode: 'contained',
        onClick: this.Compilar.bind(this),
      },
    },
    {
      location: 'after',
      widget: 'dxButton',
      options: {
        icon: 'save',
        hint: 'Guardar',
        stylingMode: 'contained',
        onClick: this.saveAsProject.bind(this),
      },
    },
    {
      location: 'after',
      widget: 'dxButton',
      options: {
        icon: 'refresh',
        hint: 'Refrescar',
        stylingMode: 'contained',
        onClick: this.EliminarTodas.bind(this),
      },
    }
  ];
  constructor(
    private Interacion: IndexService,
    public compilador: COMPILADORService
  ) { }

  ngOnInit(): void {
    this.Pestanas = [];
    this.NumTab = 0;
    this.CONTENT = '';
    this.actual = undefined;
    this.ContenidoTab = 'Pestaña 0';
  }

  AnadirPestana(): void{
    if (this.Pestanas.length === 0) {
      this.NumTab = 0;
    }
    this.Pestanas.push(new Pestaña('Pestaña ' + String(this.NumTab++)));
  }

  async upload(e: any) {
    console.log(e);
    let files = e.srcElement.files;
    let input = e.target;
    let reader = new FileReader();
    reader.readAsText(input.files[0]);
    reader.onload = async () => {
      let nueva = new Pestaña('TAB_' + (this.NumTab++) + ' ' + files[0].name);
      this.Pestanas.push(nueva);
      this.ContenidoTab = nueva.name;
      nueva.content = (reader.result as string);
      nueva.consola = '';
    };
  }

  async removerPestana(): Promise<void>{
    if (!this.Pestanas.length) {
      await this.Interacion.Notificacion('No hay pestañas para remover');
      return;
    }
    const p = await this.Interacion.confirmacion('¿Eliminar Pestaña ' + this.ContenidoTab + '?');
    if (!p) {
      return;
    }
    this.errores = [];
    this.simbolos = [];
    this.Pestanas = this.Pestanas.filter((obj) => {
      return obj.name !== this.ContenidoTab;
    });
  }

  async EliminarTodas(): Promise<void>{
    const p = await this.Interacion.confirmacion('¿Desea eliminar todas las Pestañas?');
    if (p) {
      this.errores = [];
      this.simbolos = [];
      this.ngOnInit();
    }
  }

  showCloseButton(): boolean {
    return this.Pestanas.length >= 1;
  }

  saveAsProject() {
    //you can enter your own file name and extension
    if (this.NumTab!=0) {
      this.writeContents(this.CONTENT, this.ContenidoTab + ".jl", "text/plain");
    }
  }

  writeContents(content:string, fileName:string, contentType:string) {
    var a = document.createElement("a");
    var file = new Blob([content], { type: contentType });
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
  }

  seleccionarPestana(e: any): void {
    this.ContenidoTab = e.addedItems[0].name;
    this.CONSOLA = e.addedItems[0].consola;
    this.CONTENT = e.addedItems[0].content;
    this.actual = e.addedItems[0];
    this.errores = e.addedItems[0].errores;
    this.simbolos = e.addedItems[0].simbolo;
  }

  LlenarContent(text: string): void{
    this.CONTENT = text;
  }

  getNumero():number{
    return this.NumError++;
  }

  Compilar(): void{
    const cont: Contenido = {
      Contenido: this.CONTENT
    };
    this.compilador.COMPILAR(cont).subscribe(
      (res: any) => {
        this.CONSOLA = '';
        this.NumError = 1;
        this.CONSOLA = res.consola;
        this.actual.consola = this.CONSOLA;
        this.AST = res.AST;
        this.errores = res.Errores;
        this.simbolos = res.Simbolo;
        this.actual.simbolo = res.Simbolo;
        this.actual.errores = res.Errores;
      },
      (err: any) => console.log(err)
    );
  }

  reports() {
    let width = this.graph.nativeElement.offsetWidth;
    let height = this.graph.nativeElement.offsetHeight;
    graphviz('#graph')
      .width(width)
      .height(height)
      .fit(true)
      .scale(1)
      .renderDot(this.AST);
  }

  GRAFICAR(): void{
    this.showSecondPopup = true
  }

  GRAFICAR2(): void{
    this.showSecondPopup2 = true
  }

  GRAFICAR3(): void{
    this.showSecondPopup3 = true
  }

}
