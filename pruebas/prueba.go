package main

import (
	"fmt"
)

var t0, t1, t2, t3, t4, t5, t6, t7 float64
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
	heap[int(H)] = 2
	H = H + 3

	t2 = H
	t3 = t2 + 1
	heap[int(H)] = 4
	H = H + 5

	heap[int(t3)] = 11
	t3 = t3 + 1
	heap[int(t3)] = 22
	t3 = t3 + 1
	heap[int(t3)] = 33
	t3 = t3 + 1
	heap[int(t3)] = 44
	t3 = t3 + 1
	heap[int(t1)] = t2
	t1 = t1 + 1
	t3 = H
	t4 = t3 + 1
	heap[int(H)] = 4
	H = H + 5

	heap[int(t4)] = 55
	t4 = t4 + 1
	heap[int(t4)] = 66
	t4 = t4 + 1
	heap[int(t4)] = 77
	t4 = t4 + 1
	heap[int(t4)] = 88
	t4 = t4 + 1
	heap[int(t1)] = t3
	t1 = t1 + 1
	stack[int(0)] = t0
	/* Terminando asignación de variable a */
	/* Inicio de llamado de array */
	/* iniciando obtención valor dentro de array */
	t4 = stack[int(0)]
	t1 = heap[int(t4)]
	t0 = t4 + t1
	t5 = t4 + 0
	if t5 < 1 {
		goto L2
	}
	if t5 <= t0 {
		goto L1
	}
L2:
	t4 = -1
	BoundsError()
	goto L0
L1:
	t4 = heap[int(t5)]
	/* terminando obtención valor dentro de array */
	/* iniciando obtención valor dentro de array */
	t1 = heap[int(t4)]
	t6 = t4 + t1
	t7 = t4 + 4
	if t7 < 1 {
		goto L4
	}
	if t7 <= t6 {
		goto L3
	}
L4:
	t4 = -1
	BoundsError()
	goto L0
L3:
	t4 = heap[int(t7)]
	/* terminando obtención valor dentro de array */
L0:
	/* Fin de llamado de array */
	fmt.Printf("%d", int(t4))
	fmt.Printf("%c", int(10))

}
