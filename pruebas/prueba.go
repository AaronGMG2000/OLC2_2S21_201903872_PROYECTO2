package main

import (
	"fmt"
)

var t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11 float64
var P, H float64
var stack [30101999]float64
var heap [30101999]float64

/*----native functions----*/
func F_print() {
	t2 = P + 1
	t0 = stack[int(t2)]
L5:
	t1 = heap[int(t0)]
	if t1 == -1 {
		goto L4
	}
	fmt.Printf("%c", int(t1))
	t0 = t0 + 1
	goto L5
L4:
	return
}

func BoundsError() {
	fmt.Printf("%c", int(66))
	fmt.Printf("%c", int(111))
	fmt.Printf("%c", int(117))
	fmt.Printf("%c", int(110))
	fmt.Printf("%c", int(100))
	fmt.Printf("%c", int(115))
	fmt.Printf("%c", int(69))
	fmt.Printf("%c", int(114))
	fmt.Printf("%c", int(114))
	fmt.Printf("%c", int(111))
	fmt.Printf("%c", int(114))
	fmt.Printf("%c", int(10))
	return
}

/*----functions----*/
func contratar() {
	/* Iniciando Struct */
	t0 = H
	t1 = H
	H = H + 2
	t3 = P + 1
	t2 = stack[int(t3)]
	heap[int(t1)] = t2
	t1 = t1 + 1
	t2 = P + 2
	t3 = stack[int(t2)]
	heap[int(t1)] = t3
	t1 = t1 + 1
	/* terminando Struct */
	stack[int(P)] = t0
	goto L0
L0:
	return
}

func crearActor() {
	/* Iniciando Struct */
	t2 = H
	t3 = H
	H = H + 2
	t0 = P + 1
	t1 = stack[int(t0)]
	heap[int(t3)] = t1
	t3 = t3 + 1
	t1 = P + 2
	t0 = stack[int(t1)]
	heap[int(t3)] = t0
	t3 = t3 + 1
	/* terminando Struct */
	stack[int(P)] = t2
	goto L1
L1:
	return
}

func crearPelicula() {
	/* Iniciando Struct */
	t1 = H
	t0 = H
	H = H + 2
	t2 = P + 1
	t3 = stack[int(t2)]
	heap[int(t0)] = t3
	t0 = t0 + 1
	t3 = P + 2
	t2 = stack[int(t3)]
	heap[int(t0)] = t2
	t0 = t0 + 1
	/* terminando Struct */
	stack[int(P)] = t1
	goto L2
L2:
	return
}

func imprimir() {
	t3 = H
	heap[int(H)] = 65
	H = H + 1
	heap[int(H)] = 99
	H = H + 1
	heap[int(H)] = 116
	H = H + 1
	heap[int(H)] = 111
	H = H + 1
	heap[int(H)] = 114
	H = H + 1
	heap[int(H)] = 58
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	/* *****GUARDANDO TEMPORALES*********** */
	/* ************************************ */
	t2 = P + 2
	t2 = t2 + 1
	stack[int(t2)] = t3
	P = P + 2
	F_print()
	P = P - 2
	/* *****SACANDO TEMPORALES*********** */
	/* ************************************ */
	t1 = P + 1
	t0 = stack[int(t1)]
	t0 = t0 + 0
	t0 = heap[int(t0)]
	t0 = t0 + 0
	t0 = heap[int(t0)]
	/* *****GUARDANDO TEMPORALES*********** */
	/* ************************************ */
	t3 = P + 2
	t3 = t3 + 1
	stack[int(t3)] = t0
	P = P + 2
	F_print()
	P = P - 2
	/* *****SACANDO TEMPORALES*********** */
	/* ************************************ */
	t2 = H
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 69
	H = H + 1
	heap[int(H)] = 100
	H = H + 1
	heap[int(H)] = 97
	H = H + 1
	heap[int(H)] = 100
	H = H + 1
	heap[int(H)] = 58
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	/* *****GUARDANDO TEMPORALES*********** */
	/* ************************************ */
	t1 = P + 2
	t1 = t1 + 1
	stack[int(t1)] = t2
	P = P + 2
	F_print()
	P = P - 2
	/* *****SACANDO TEMPORALES*********** */
	/* ************************************ */
	t3 = P + 1
	t0 = stack[int(t3)]
	t0 = t0 + 0
	t0 = heap[int(t0)]
	t0 = t0 + 1
	t0 = heap[int(t0)]
	fmt.Printf("%d", int(t0))
	fmt.Printf("%c", int(10))
	t2 = H
	heap[int(H)] = 80
	H = H + 1
	heap[int(H)] = 101
	H = H + 1
	heap[int(H)] = 108
	H = H + 1
	heap[int(H)] = 105
	H = H + 1
	heap[int(H)] = 99
	H = H + 1
	heap[int(H)] = 117
	H = H + 1
	heap[int(H)] = 108
	H = H + 1
	heap[int(H)] = 97
	H = H + 1
	heap[int(H)] = 58
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	/* *****GUARDANDO TEMPORALES*********** */
	/* ************************************ */
	t1 = P + 2
	t1 = t1 + 1
	stack[int(t1)] = t2
	P = P + 2
	F_print()
	P = P - 2
	/* *****SACANDO TEMPORALES*********** */
	/* ************************************ */
	t0 = P + 1
	t3 = stack[int(t0)]
	t3 = t3 + 1
	t3 = heap[int(t3)]
	t3 = t3 + 0
	t3 = heap[int(t3)]
	/* *****GUARDANDO TEMPORALES*********** */
	/* ************************************ */
	t2 = P + 2
	t2 = t2 + 1
	stack[int(t2)] = t3
	P = P + 2
	F_print()
	P = P - 2
	/* *****SACANDO TEMPORALES*********** */
	/* ************************************ */
	t1 = H
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 71
	H = H + 1
	heap[int(H)] = 101
	H = H + 1
	heap[int(H)] = 110
	H = H + 1
	heap[int(H)] = 101
	H = H + 1
	heap[int(H)] = 114
	H = H + 1
	heap[int(H)] = 111
	H = H + 1
	heap[int(H)] = 58
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	/* *****GUARDANDO TEMPORALES*********** */
	/* ************************************ */
	t0 = P + 2
	t0 = t0 + 1
	stack[int(t0)] = t1
	P = P + 2
	F_print()
	P = P - 2
	/* *****SACANDO TEMPORALES*********** */
	/* ************************************ */
	t2 = P + 1
	t3 = stack[int(t2)]
	t3 = t3 + 1
	t3 = heap[int(t3)]
	t3 = t3 + 1
	t3 = heap[int(t3)]
	fmt.Printf("%d", int(t3))
	fmt.Printf("%c", int(10))
	return
}

func contratos() {
	t4 = 1 * 1
	t5 = t4 + 2
	t6 = H
	heap[int(H)] = 1
	H = H + 1
	heap[int(H)] = t5
	H = H + 1
	t7 = heap[int(t6)]
	t6 = t6 + 1
	t8 = heap[int(t6)]
	t9 = P + 1
L7:
	if t7 > t8 {
		goto L8
	}
	stack[int(t9)] = t7
	/* Asignación de variable contrato */
	/* Iniciando Struct */
	t1 = H
	t0 = H
	H = H + 2
	/* Iniciando Struct */
	t2 = H
	t3 = H
	H = H + 2
	t10 = H
	heap[int(H)] = -1
	H = H + 1
	heap[int(t3)] = t10
	t3 = t3 + 1
	heap[int(t3)] = 0
	t3 = t3 + 1
	/* terminando Struct */
	heap[int(t0)] = t2
	t0 = t0 + 1
	/* Iniciando Struct */
	t10 = H
	t3 = H
	H = H + 2
	t2 = H
	heap[int(H)] = -1
	H = H + 1
	heap[int(t3)] = t2
	t3 = t3 + 1
	heap[int(t3)] = 0
	t3 = t3 + 1
	/* terminando Struct */
	heap[int(t0)] = t10
	t0 = t0 + 1
	/* terminando Struct */
	t2 = P + 2
	stack[int(t2)] = t1
	/* Terminando asignación de variable contrato */
	t10 = P + 1
	t3 = stack[int(t10)]
	if t3 < 4 {
		goto L10
	}
	goto L11
L10:
	/* Asignación de variable actor */
	/* *****GUARDANDO TEMPORALES*********** */
	/* ************************************ */
	t0 = P + 2
	t0 = t0 + 1
	t2 = stack[int(0)]
	/* Inicio de llamado de array */
	t10 = P + 1
	t1 = stack[int(t10)]
	/* iniciando obtención valor dentro de array */
	t3 = heap[int(t2)]
	t10 = t2 + t3
	t11 = t2 + t1
	if t11 < 1 {
		goto L18
	}
	if t11 <= t10 {
		goto L17
	}
L18:
	t2 = -1
	BoundsError()
	goto L16
L17:
	t2 = heap[int(t11)]
	/* terminando obtención valor dentro de array */
L16:
	/* Fin de llamado de array */
	stack[int(t0)] = t2
	t0 = t0 + 1
	t11 = P + 1
	t3 = stack[int(t11)]
	t10 = t3 + 38
	stack[int(t0)] = t10
	P = P + 2
	crearActor()
	t1 = stack[int(P)]
	P = P - 2
	/* *****SACANDO TEMPORALES*********** */
	/* ************************************ */
	t2 = P + 3
	stack[int(t2)] = t1
	/* Terminando asignación de variable actor */
	/* Asignación de variable pelicula */
	/* *****GUARDANDO TEMPORALES*********** */
	/* ************************************ */
	t11 = P + 3
	t11 = t11 + 1
	t3 = stack[int(1)]
	/* Inicio de llamado de array */
	t0 = P + 1
	t10 = stack[int(t0)]
	/* iniciando obtención valor dentro de array */
	t2 = heap[int(t3)]
	t1 = t3 + t2
	t0 = t3 + t10
	if t0 < 1 {
		goto L24
	}
	if t0 <= t1 {
		goto L23
	}
L24:
	t3 = -1
	BoundsError()
	goto L22
L23:
	t3 = heap[int(t0)]
	/* terminando obtención valor dentro de array */
L22:
	/* Fin de llamado de array */
	stack[int(t11)] = t3
	t11 = t11 + 1
	t0 = P + 1
	t2 = stack[int(t0)]
	stack[int(t11)] = t2
	P = P + 3
	crearPelicula()
	t1 = stack[int(P)]
	P = P - 3
	/* *****SACANDO TEMPORALES*********** */
	/* ************************************ */
	t10 = P + 4
	stack[int(t10)] = t1
	/* Terminando asignación de variable pelicula */
	/* Asignación de variable contrato */
	/* *****GUARDANDO TEMPORALES*********** */
	/* ************************************ */
	t3 = P + 4
	t3 = t3 + 1
	t2 = P + 3
	t0 = stack[int(t2)]
	stack[int(t3)] = t0
	t3 = t3 + 1
	t10 = P + 4
	t11 = stack[int(t10)]
	stack[int(t3)] = t11
	P = P + 4
	contratar()
	t1 = stack[int(P)]
	P = P - 4
	/* *****SACANDO TEMPORALES*********** */
	/* ************************************ */
	t2 = P + 2
	stack[int(t2)] = t1
	/* Terminando asignación de variable contrato */
L11:
	/* *****GUARDANDO TEMPORALES*********** */
	/* ************************************ */
	t0 = P + 4
	t0 = t0 + 1
	t11 = P + 2
	t10 = stack[int(t11)]
	stack[int(t0)] = t10
	P = P + 4
	imprimir()
	t3 = stack[int(P)]
	P = P - 4
	/* *****SACANDO TEMPORALES*********** */
	/* ************************************ */
	goto L9
L9:
	t7 = t7 + 1
	goto L7
L8:
	return
}

func main() {
	P = 0
	H = 0
	/* Asignación de variable actores */
	t0 = H
	t1 = t0 + 1
	heap[int(H)] = 4
	H = H + 5

	t2 = H
	heap[int(H)] = 69
	H = H + 1
	heap[int(H)] = 108
	H = H + 1
	heap[int(H)] = 105
	H = H + 1
	heap[int(H)] = 122
	H = H + 1
	heap[int(H)] = 97
	H = H + 1
	heap[int(H)] = 98
	H = H + 1
	heap[int(H)] = 101
	H = H + 1
	heap[int(H)] = 116
	H = H + 1
	heap[int(H)] = 104
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 79
	H = H + 1
	heap[int(H)] = 108
	H = H + 1
	heap[int(H)] = 115
	H = H + 1
	heap[int(H)] = 101
	H = H + 1
	heap[int(H)] = 110
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	heap[int(t1)] = t2
	t1 = t1 + 1
	t2 = H
	heap[int(H)] = 65
	H = H + 1
	heap[int(H)] = 100
	H = H + 1
	heap[int(H)] = 97
	H = H + 1
	heap[int(H)] = 109
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 83
	H = H + 1
	heap[int(H)] = 97
	H = H + 1
	heap[int(H)] = 110
	H = H + 1
	heap[int(H)] = 100
	H = H + 1
	heap[int(H)] = 108
	H = H + 1
	heap[int(H)] = 101
	H = H + 1
	heap[int(H)] = 114
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	heap[int(t1)] = t2
	t1 = t1 + 1
	t2 = H
	heap[int(H)] = 67
	H = H + 1
	heap[int(H)] = 104
	H = H + 1
	heap[int(H)] = 114
	H = H + 1
	heap[int(H)] = 105
	H = H + 1
	heap[int(H)] = 115
	H = H + 1
	heap[int(H)] = 116
	H = H + 1
	heap[int(H)] = 105
	H = H + 1
	heap[int(H)] = 97
	H = H + 1
	heap[int(H)] = 110
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 66
	H = H + 1
	heap[int(H)] = 97
	H = H + 1
	heap[int(H)] = 108
	H = H + 1
	heap[int(H)] = 101
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	heap[int(t1)] = t2
	t1 = t1 + 1
	t2 = H
	heap[int(H)] = 74
	H = H + 1
	heap[int(H)] = 101
	H = H + 1
	heap[int(H)] = 110
	H = H + 1
	heap[int(H)] = 110
	H = H + 1
	heap[int(H)] = 105
	H = H + 1
	heap[int(H)] = 102
	H = H + 1
	heap[int(H)] = 101
	H = H + 1
	heap[int(H)] = 114
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 65
	H = H + 1
	heap[int(H)] = 110
	H = H + 1
	heap[int(H)] = 105
	H = H + 1
	heap[int(H)] = 115
	H = H + 1
	heap[int(H)] = 116
	H = H + 1
	heap[int(H)] = 111
	H = H + 1
	heap[int(H)] = 110
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	heap[int(t1)] = t2
	t1 = t1 + 1
	stack[int(0)] = t0
	/* Terminando asignación de variable actores */
	/* Asignación de variable peliculas */
	t2 = H
	t1 = t2 + 1
	heap[int(H)] = 4
	H = H + 5

	t0 = H
	heap[int(H)] = 65
	H = H + 1
	heap[int(H)] = 118
	H = H + 1
	heap[int(H)] = 101
	H = H + 1
	heap[int(H)] = 110
	H = H + 1
	heap[int(H)] = 103
	H = H + 1
	heap[int(H)] = 101
	H = H + 1
	heap[int(H)] = 114
	H = H + 1
	heap[int(H)] = 115
	H = H + 1
	heap[int(H)] = 58
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 65
	H = H + 1
	heap[int(H)] = 103
	H = H + 1
	heap[int(H)] = 101
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 111
	H = H + 1
	heap[int(H)] = 102
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 85
	H = H + 1
	heap[int(H)] = 108
	H = H + 1
	heap[int(H)] = 116
	H = H + 1
	heap[int(H)] = 114
	H = H + 1
	heap[int(H)] = 111
	H = H + 1
	heap[int(H)] = 110
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	heap[int(t1)] = t0
	t1 = t1 + 1
	t0 = H
	heap[int(H)] = 77
	H = H + 1
	heap[int(H)] = 114
	H = H + 1
	heap[int(H)] = 46
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 68
	H = H + 1
	heap[int(H)] = 101
	H = H + 1
	heap[int(H)] = 101
	H = H + 1
	heap[int(H)] = 100
	H = H + 1
	heap[int(H)] = 115
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	heap[int(t1)] = t0
	t1 = t1 + 1
	t0 = H
	heap[int(H)] = 66
	H = H + 1
	heap[int(H)] = 97
	H = H + 1
	heap[int(H)] = 116
	H = H + 1
	heap[int(H)] = 109
	H = H + 1
	heap[int(H)] = 97
	H = H + 1
	heap[int(H)] = 110
	H = H + 1
	heap[int(H)] = 58
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 84
	H = H + 1
	heap[int(H)] = 104
	H = H + 1
	heap[int(H)] = 101
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 68
	H = H + 1
	heap[int(H)] = 97
	H = H + 1
	heap[int(H)] = 114
	H = H + 1
	heap[int(H)] = 107
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 75
	H = H + 1
	heap[int(H)] = 110
	H = H + 1
	heap[int(H)] = 105
	H = H + 1
	heap[int(H)] = 103
	H = H + 1
	heap[int(H)] = 104
	H = H + 1
	heap[int(H)] = 116
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	heap[int(t1)] = t0
	t1 = t1 + 1
	t0 = H
	heap[int(H)] = 77
	H = H + 1
	heap[int(H)] = 97
	H = H + 1
	heap[int(H)] = 114
	H = H + 1
	heap[int(H)] = 108
	H = H + 1
	heap[int(H)] = 101
	H = H + 1
	heap[int(H)] = 121
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 38
	H = H + 1
	heap[int(H)] = 32
	H = H + 1
	heap[int(H)] = 77
	H = H + 1
	heap[int(H)] = 101
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	heap[int(t1)] = t0
	t1 = t1 + 1
	stack[int(1)] = t2
	/* Terminando asignación de variable peliculas */
	/* *****GUARDANDO TEMPORALES*********** */
	/* ************************************ */
	t2 = P + 2
	P = P + 2
	contratos()
	t1 = stack[int(P)]
	P = P - 2
	/* *****SACANDO TEMPORALES*********** */
	/* ************************************ */

}
