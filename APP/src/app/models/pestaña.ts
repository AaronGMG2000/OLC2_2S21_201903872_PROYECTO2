export class Pestaña {
  name!: string;
  content = '';
  consola = '';
  simbolo = [];
  errores = [];
  opti = [];
  constructor(name: string, content: string = '') {
    this.name = name;
  }
}
