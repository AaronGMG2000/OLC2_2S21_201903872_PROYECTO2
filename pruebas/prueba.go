package main

import (
	"fmt"
)

var t0, t1, t2, t3 float64
var P, H float64
var stack [30101999]float64
var heap [30101999]float64

/*----functions----*/
func ackerman() {
	t1 = P + 1
	t0 = stack[int(t1)]
	if t0 == 0 {
		goto L1
	}
	goto L2
L1:
	t0 = P + 2
	t1 = stack[int(t0)]
	t0 = t1 + 1
	stack[int(P)] = t0
	goto L0
	goto L3
L2:
	t0 = P + 1
	t1 = stack[int(t0)]
	if t1 > 0 {
		goto L6
	}
	goto L5
L6:
	t1 = P + 2
	t0 = stack[int(t1)]
	if t0 == 0 {
		goto L4
	}
	goto L5
L4:
	t1 = P + 3
	t1 = t1 + 1
	t2 = P + 1
	t0 = stack[int(t2)]
	t2 = t0 - 1
	stack[int(t1)] = t2
	t1 = t1 + 1
	stack[int(t1)] = 1
	P = P + 3
	ackerman()
	t0 = stack[int(P)]
	P = P - 3
	stack[int(P)] = t0
	goto L0
	goto L3
L5:
	t2 = P + 3
	t2 = t2 + 1
	t0 = P + 1
	t1 = stack[int(t0)]
	t0 = t1 - 1
	stack[int(t2)] = t0
	t2 = t2 + 1
	/* *****GUARDANDO TEMPORALES*********** */
	t1 = P + 4
	stack[int(t1)] = t2
	t1 = t1 + 1
	P = P + 1
	/* ************************************ */
	t0 = P + 4
	t0 = t0 + 1
	t3 = P + 0
	t1 = stack[int(t3)]
	stack[int(t0)] = t1
	t0 = t0 + 1
	t1 = P + 1
	t3 = stack[int(t1)]
	t1 = t3 - 1
	stack[int(t0)] = t1
	P = P + 4
	ackerman()
	t3 = stack[int(P)]
	P = P - 4
	/* *****SACANDO TEMPORALES*********** */
	P = P - 1
	t1 = P + 5
	t1 = t1 - 1
	t2 = stack[int(t1)]
	/* ************************************ */
	stack[int(t2)] = t3
	P = P + 3
	ackerman()
	t0 = stack[int(P)]
	P = P - 3
	stack[int(P)] = t0
	goto L0
L3:
L0:
	return
}

func main() {
	P = 0
	H = 0
	t1 = P + 0
	t1 = t1 + 1
	stack[int(t1)] = 3
	t1 = t1 + 1
	stack[int(t1)] = 5
	P = P + 0
	ackerman()
	t3 = stack[int(P)]
	P = P - 0
	fmt.Printf("%d", int(t3))
	fmt.Printf("%c", int(10))

}
