package main

import (
	"fmt"
)

var t0, t1, t2, t3, t4, t5 float64
var P, H float64
var stack [30101999]float64
var heap [30101999]float64

/*----native functions----*/
func potencia() {
	t1 = P + 1
	t2 = P + 2
	t3 = stack[int(t1)]
	t4 = stack[int(t2)]
	if t4 >= 0 {
		goto L2
	}
	t4 = t4 * -1
L2:
	t2 = 1
	t5 = 1
L1:
	if t2 >= t4 {
		goto L0
	}
	t3 = stack[int(t1)]
	t5 = t5 * t3
	t2 = t2 + 1
	goto L1
L0:
	stack[int(P)] = t5
	return
}

func main() {
	P = 0
	H = 0
	/* Asignación de variable var3 */
	t0 = 0 - 5
	t1 = P + 0
	t1 = t1 + 1
	stack[int(t1)] = t0
	t1 = t1 + 1
	stack[int(t1)] = 3
	P = P + 0
	potencia()
	t3 = stack[int(P)]
	if 3 >= 0 {
		goto L3
	}
	t3 = 1 / t3
L3:
	P = P - 0
	stack[int(0)] = t3
	/* Terminando asignación de variable var3 */
	t4 = stack[int(0)]
	fmt.Printf("%d", int(t4))
	fmt.Printf("%c", int(10))

}
