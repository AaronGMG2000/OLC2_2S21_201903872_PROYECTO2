package main

import (
	"fmt"
	"math"
)

var t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10 float64
var P, H float64
var stack [30101999]float64
var heap [30101999]float64

/*----native functions----*/
func to_string() {
	t1 = H
	t2 = P + 1
	t3 = stack[int(t2)]
	if t3 > 0 {
		goto L1
	}
	heap[int(H)] = 45
	H = H + 1
	t3 = 0 - t3
L1:
	if t3 < 1 {
		goto L2
	}
	if t3 < 10 {
		goto L2
	}
	t4 = 1
	t2 = math.Mod(t3, 1)
	t2 = t3 - t2
L3:
	if t2 < 10 {
		goto L4
	}
	t2 = t2 / 10
	t5 = math.Mod(t2, 1)
	t2 = t2 - t5
	t4 = t4 * 10
	goto L3
L4:
	t5 = t2 + 48
	heap[int(H)] = t5
	t2 = t2 * t4
	t3 = t3 - t2
	goto L1
L2:
	t4 = math.Mod(t3, 1)
	t5 = t3 - t4
	t4 = t5 + 48
	t3 = t3 - t5
	heap[int(H)] = t4
	H = H + 1
	if t3 == 0 {
		goto L0
	}
	heap[int(H)] = 46
	H = H + 1
	t6 = 0
L5:
	if t3 == 0 {
		goto L0
	}
	if t6 == 6 {
		goto L0
	}
	t3 = t3 * 10
	t4 = math.Mod(t3, 1)
	t4 = t3 - t4
	t5 = t4 + 48
	heap[int(H)] = t5
	H = H + 1
	t3 = t3 - t4
	t6 = t6 + 1
	goto L5
L0:
	heap[int(H)] = -1
	H = H + 1
	stack[int(P)] = t1
	return
}

func F_print() {
	t8 = P + 1
	t9 = stack[int(t8)]
L7:
	t8 = heap[int(t9)]
	if t8 == -1 {
		goto L6
	}
	fmt.Printf("%c", int(t8))
	t9 = t9 + 1
	goto L7
L6:
	return
}

func main() {
	P = 0
	H = 0
	t0 = 0 - 3.2
	t7 = P + 0
	t7 = t7 + 1
	stack[int(t7)] = t0
	P = P + 0
	to_string()
	t7 = stack[int(P)]
	P = P - 0
	t10 = P + 0
	t10 = t10 + 1
	stack[int(t10)] = t7
	P = P + 0
	F_print()
	t7 = stack[int(P)]
	P = P - 0
	fmt.Printf("%c", int(10))

}
