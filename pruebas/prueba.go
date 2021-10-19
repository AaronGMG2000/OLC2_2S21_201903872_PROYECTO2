package main

import (
	"fmt"
)

var t0, t1, t2, t3, t4, t5, t6, t7, t8, t9 float64
var P, H float64
var stack [30101999]float64
var heap [30101999]float64

func main() {
	P = 0
	H = 0
	/* Asignación de variable multi */
	t0 = H
	t1 = t0 + 1
	heap[int(H)] = 1
	H = H + 2

	t2 = H
	t3 = t2 + 1
	heap[int(H)] = 1
	H = H + 2

	t4 = H
	t5 = t4 + 1
	heap[int(H)] = 4
	H = H + 5

	heap[int(t5)] = 1
	t5 = t5 + 1
	heap[int(t5)] = 2
	t5 = t5 + 1
	heap[int(t5)] = 3
	t5 = t5 + 1
	heap[int(t5)] = 4
	t5 = t5 + 1
	heap[int(t3)] = t4
	t3 = t3 + 1
	heap[int(t1)] = t2
	t1 = t1 + 1
	stack[int(0)] = t0
	/* Terminando asignación de variable multi */
	t5 = stack[int(0)]
	/* inicio de impresión array */
	t3 = heap[int(t5)]
	t0 = t3 + t5
	t1 = t0 - 1
	fmt.Printf("%c", int(91))
	t6 = t5 + 1
L0:
	if t6 > t1 {
		goto L1
	}
	/* inicio de impresión array interno */
	t5 = heap[int(t6)]
	t3 = heap[int(t5)]
	t0 = t3 + t5
	t7 = t0 - 1
	fmt.Printf("%c", int(91))
	t3 = t5 + 1
L2:
	if t3 > t7 {
		goto L3
	}
	/* inicio de impresión array interno */
	t0 = heap[int(t3)]
	t5 = heap[int(t0)]
	t8 = t5 + t0
	t9 = t8 - 1
	fmt.Printf("%c", int(91))
	t5 = t0 + 1
L4:
	if t5 > t9 {
		goto L5
	}
	t8 = heap[int(t5)]
	fmt.Printf("%d", int(t8))
	fmt.Printf("%c", int(44))
	t5 = t5 + 1
	goto L4
L5:
	t0 = heap[int(t5)]
	fmt.Printf("%d", int(t0))
	fmt.Printf("%c", int(93))
	/* fin de impresión array interno */
	t3 = t3 + 1
	goto L2
L3:
	fmt.Printf("%c", int(93))
	/* fin de impresión array interno */
	t6 = t6 + 1
	fmt.Printf("%c", int(44))
	goto L0
L1:
	/* inicio de impresión array interno */
	t8 = heap[int(t6)]
	t0 = heap[int(t8)]
	t9 = t0 + t8
	t5 = t9 - 1
	fmt.Printf("%c", int(91))
	t7 = t8 + 1
L6:
	if t7 > t5 {
		goto L7
	}
	/* inicio de impresión array interno */
	t3 = heap[int(t7)]
	t0 = heap[int(t3)]
	t9 = t0 + t3
	t8 = t9 - 1
	fmt.Printf("%c", int(91))
	t0 = t3 + 1
L8:
	if t0 > t8 {
		goto L9
	}
	t9 = heap[int(t0)]
	fmt.Printf("%d", int(t9))
	fmt.Printf("%c", int(44))
	t0 = t0 + 1
	goto L8
L9:
	t3 = heap[int(t0)]
	fmt.Printf("%d", int(t3))
	fmt.Printf("%c", int(93))
	/* fin de impresión array interno */
	t7 = t7 + 1
	goto L6
L7:
	fmt.Printf("%c", int(93))
	/* fin de impresión array interno */
	fmt.Printf("%c", int(93))
	/* final de impresión array */
	fmt.Printf("%c", int(10))

}
