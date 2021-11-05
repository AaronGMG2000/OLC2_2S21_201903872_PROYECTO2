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
	t7 = P + 1
	t9 = stack[int(t7)]
L3:
	t10 = heap[int(t9)]
	if t10 == -1 {
		goto L2
	}
	fmt.Printf("%c", int(t10))
	t9 = t9 + 1
	goto L3
L2:
	return
}

func main() {
	P = 0
	H = 0
	/* Asignación de variable a */
	/* Iniciando Struct */
	t0 = H
	t1 = H
	H = H + 1
	t2 = H
	heap[int(H)] = 82
	H = H + 1
	heap[int(H)] = 117
	H = H + 1
	heap[int(H)] = 100
	H = H + 1
	heap[int(H)] = 121
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	heap[int(t1)] = t2
	t1 = t1 + 1
	/* terminando Struct */
	stack[int(0)] = t0
	/* Terminando asignación de variable a */
	/* Asignación de variable b */
	t1 = H
	t0 = t1 + 1
	heap[int(H)] = 3
	H = H + 4

	t3 = stack[int(0)]
	heap[int(t0)] = t3
	t0 = t0 + 1
	t4 = stack[int(0)]
	heap[int(t0)] = t4
	t0 = t0 + 1
	t5 = stack[int(0)]
	heap[int(t0)] = t5
	t0 = t0 + 1
	stack[int(1)] = t1
	/* Terminando asignación de variable b */
	t0 = stack[int(1)]
	/* inicio de impresión array */
	t1 = heap[int(t0)]
	t7 = t1 + t0
	t6 = t7 - 1
	fmt.Printf("%c", int(91))
	t8 = t0 + 1
L0:
	if t8 > t6 {
		goto L1
	}
	fmt.Printf("%c", int(112))
	fmt.Printf("%c", int(97))
	fmt.Printf("%c", int(100))
	fmt.Printf("%c", int(114))
	fmt.Printf("%c", int(101))
	fmt.Printf("%c", int(40))
	t0 = t8 + 0
	fmt.Printf("%c", int(34))
	t1 = heap[int(t0)]
	t11 = P + 2
	t11 = t11 + 1
	stack[int(t11)] = t1
	P = P + 2
	F_print()
	t1 = stack[int(P)]
	P = P - 2
	fmt.Printf("%c", int(34))
	fmt.Printf("%c", int(41))
	fmt.Printf("%c", int(44))
	t8 = t8 + 1
	goto L0
L1:
	fmt.Printf("%c", int(93))
	/* final de impresión array */
	fmt.Printf("%c", int(10))

}
