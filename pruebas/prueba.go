package main

import (
	"fmt"
)

var t0, t1, t2, t3, t4 float64
var P, H float64
var stack [30101999]float64
var heap [30101999]float64

/*----native functions----*/
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

func main() {
	P = 0
	H = 0
	/* Asignación de variable a */
	t0 = H
	t1 = t0 + 1
	heap[int(H)] = 1
	H = H + 2

	heap[int(t1)] = 0
	t1 = t1 + 1
	stack[int(0)] = t0
	/* Terminando asignación de variable a */
	/* Asignación de variable aux */
	t1 = H
	t0 = t1 + 1
	heap[int(H)] = 1
	H = H + 2

	heap[int(t0)] = 1
	t0 = t0 + 1
	stack[int(1)] = t1
	/* Terminando asignación de variable aux */
	t0 = stack[int(1)]
	/* Asignación de variable aux[n] */
	/* Inicio de llamado de array */
	/* iniciando obtención valor dentro de array */
	t1 = stack[int(t0)]
	t2 = heap[int(t1)]
	t3 = t1 + t2
	t0 = t1 + 1
	if t0 < 1 {
		goto L2
	}
	if t0 <= t3 {
		goto L1
	}
L2:
	t0 = -1
	BoundsError()
	goto L0
L1:
	heap[int(t0)] = 2
L0:
	/* Fin de llamado de array */
	/* Terminando asignación de variable aux */
	t1 = stack[int(1)]
	/* inicio de impresión array */
	t2 = heap[int(t1)]
	t3 = t2 + t1
	t0 = t3 - 1
	fmt.Printf("%c", int(91))
	t4 = t1 + 1
L3:
	if t4 > t0 {
		goto L4
	}
	t1 = heap[int(t4)]
	fmt.Printf("%d", int(t1))
	fmt.Printf("%c", int(44))
	t4 = t4 + 1
	goto L3
L4:
	t2 = heap[int(t4)]
	fmt.Printf("%d", int(t2))
	fmt.Printf("%c", int(93))
	/* final de impresión array */
	fmt.Printf("%c", int(10))
	t3 = stack[int(0)]
	/* inicio de impresión array */
	t1 = heap[int(t3)]
	t0 = t1 + t3
	t2 = t0 - 1
	fmt.Printf("%c", int(91))
	t4 = t3 + 1
L5:
	if t4 > t2 {
		goto L6
	}
	t3 = heap[int(t4)]
	fmt.Printf("%d", int(t3))
	fmt.Printf("%c", int(44))
	t4 = t4 + 1
	goto L5
L6:
	t1 = heap[int(t4)]
	fmt.Printf("%d", int(t1))
	fmt.Printf("%c", int(93))
	/* final de impresión array */
	fmt.Printf("%c", int(10))

}
