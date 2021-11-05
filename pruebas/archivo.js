const express = require('express')
const mysql = require('mysql2')
const cors = require('cors')

const app = express()
app.use(express.urlencoded({ extended: true}))
app.use(express.json())
app.use(cors({ origin: true }))

let cont = null

app.get('/connect', (req, res)=> {
  if(cont) {
    return res.send('Ya se encuentra conectado');
  }

  cont = mysql.createConnection({
    host: 'myql_bd',
    user: 'Ale',
    password: '1234',
    database: 'bd1_ejemplo'
  });

  cont.connect((err) => {
    if (err) throw err;
    res.send('Se conecto')
  })
})

app.get('/getProducts', (req, res) =>{
    con.connect((err) => {
        if (err) throw err
        const command = "SELECT * FROM PRODUCTOS"
        con.query(command, (err, filas) =>{
            res.json(filas)
        })
    })
})

app.listen(3000, () => console.log("Servidor en puerto 3000"))