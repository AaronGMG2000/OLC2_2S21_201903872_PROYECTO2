package main

import (
	"fmt"
)

var t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, t21, t22 float64
var P, H float64
var stack [30101999]float64
var heap [30101999]float64

/*----native functions----*/
func concat_string() {
	t1 = H
	stack[int(P)] = t1
	t0 = P + 1
	t1 = P + 2
	t5 = stack[int(t0)]
L1:
	t0 = heap[int(t5)]
	if t0 == -1 {
		goto L2
	}
	heap[int(H)] = t0
	H = H + 1
	t5 = t5 + 1
	goto L1
L2:
	t6 = stack[int(t1)]
L3:
	t1 = heap[int(t6)]
	if t1 == -1 {
		goto L0
	}
	heap[int(H)] = t1
	H = H + 1
	t6 = t6 + 1
	goto L3
L0:
	heap[int(H)] = -1
	H = H + 1
	return
}

func F_print() {
	t16 = P + 1
	t21 = stack[int(t16)]
L11:
	t18 = heap[int(t21)]
	if t18 == -1 {
		goto L10
	}
	fmt.Printf("%c", int(t18))
	t21 = t21 + 1
	goto L11
L10:
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

	heap[int(t3)] = 104
	t3 = t3 + 1
	heap[int(t3)] = 111
	t3 = t3 + 1
	heap[int(t3)] = 108
	t3 = t3 + 1
	heap[int(t3)] = 97
	t3 = t3 + 1
	heap[int(t1)] = t2
	t1 = t1 + 1
	t3 = H
	t4 = t3 + 1
	heap[int(H)] = 5
	H = H + 6

	heap[int(t4)] = 109
	t4 = t4 + 1
	heap[int(t4)] = 117
	t4 = t4 + 1
	heap[int(t4)] = 110
	t4 = t4 + 1
	heap[int(t4)] = 100
	t4 = t4 + 1
	heap[int(t4)] = 111
	t4 = t4 + 1
	heap[int(t1)] = t3
	t1 = t1 + 1
	stack[int(0)] = t0
	/* Terminando asignación de variable a */
	t4 = stack[int(0)]
	/* inicio de to_string(array) */
	t7 = heap[int(t4)]
	t9 = t7 + t4
	t8 = t9 - 1
	t10 = H
	heap[int(H)] = 91
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t11 = t4 + 1
L4:
	if t11 > t8 {
		goto L5
	}
	t4 = heap[int(t11)]
	t7 = heap[int(t4)]
	t9 = t7 + t4
	t12 = t9 - 1
	t7 = H
	heap[int(H)] = 91
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t9 = P + 1
	t9 = t9 + 1
	stack[int(t9)] = t10
	t9 = t9 + 1
	stack[int(t9)] = t7
	P = P + 1
	concat_string()
	t9 = stack[int(P)]
	P = P - 1
	t7 = t4 + 1
L6:
	if t7 > t12 {
		goto L7
	}
	t4 = H
	heap[int(H)] = 39
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t13 = P + 1
	t13 = t13 + 1
	stack[int(t13)] = t9
	t13 = t13 + 1
	stack[int(t13)] = t4
	P = P + 1
	concat_string()
	t13 = stack[int(P)]
	P = P - 1
	t4 = heap[int(t7)]
	t14 = H
	heap[int(H)] = t4
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t15 = P + 1
	t15 = t15 + 1
	stack[int(t15)] = t13
	t15 = t15 + 1
	stack[int(t15)] = t14
	P = P + 1
	concat_string()
	t15 = stack[int(P)]
	P = P - 1
	t14 = H
	heap[int(H)] = 39
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t13 = P + 1
	t13 = t13 + 1
	stack[int(t13)] = t15
	t13 = t13 + 1
	stack[int(t13)] = t14
	P = P + 1
	concat_string()
	t13 = stack[int(P)]
	P = P - 1
	t14 = H
	heap[int(H)] = 44
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t15 = P + 1
	t15 = t15 + 1
	stack[int(t15)] = t13
	t15 = t15 + 1
	stack[int(t15)] = t14
	P = P + 1
	concat_string()
	t15 = stack[int(P)]
	P = P - 1
	t7 = t7 + 1
	goto L6
L7:
	t14 = H
	heap[int(H)] = 39
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t13 = P + 1
	t13 = t13 + 1
	stack[int(t13)] = t15
	t13 = t13 + 1
	stack[int(t13)] = t14
	P = P + 1
	concat_string()
	t13 = stack[int(P)]
	P = P - 1
	t14 = heap[int(t7)]
	t16 = H
	heap[int(H)] = t14
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t17 = P + 1
	t17 = t17 + 1
	stack[int(t17)] = t13
	t17 = t17 + 1
	stack[int(t17)] = t16
	P = P + 1
	concat_string()
	t17 = stack[int(P)]
	P = P - 1
	t16 = H
	heap[int(H)] = 39
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t13 = P + 1
	t13 = t13 + 1
	stack[int(t13)] = t17
	t13 = t13 + 1
	stack[int(t13)] = t16
	P = P + 1
	concat_string()
	t13 = stack[int(P)]
	P = P - 1
	t16 = H
	heap[int(H)] = 93
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t17 = P + 1
	t17 = t17 + 1
	stack[int(t17)] = t13
	t17 = t17 + 1
	stack[int(t17)] = t16
	P = P + 1
	concat_string()
	t17 = stack[int(P)]
	P = P - 1
	t11 = t11 + 1
	t15 = H
	heap[int(H)] = 44
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t12 = P + 1
	t12 = t12 + 1
	stack[int(t12)] = t17
	t12 = t12 + 1
	stack[int(t12)] = t15
	P = P + 1
	concat_string()
	t12 = stack[int(P)]
	P = P - 1
	goto L4
L5:
	t7 = heap[int(t11)]
	t16 = heap[int(t7)]
	t13 = t16 + t7
	t15 = t13 - 1
	t16 = H
	heap[int(H)] = 91
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t13 = P + 1
	t13 = t13 + 1
	stack[int(t13)] = t12
	t13 = t13 + 1
	stack[int(t13)] = t16
	P = P + 1
	concat_string()
	t13 = stack[int(P)]
	P = P - 1
	t16 = t7 + 1
L8:
	if t16 > t15 {
		goto L9
	}
	t7 = H
	heap[int(H)] = 39
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t18 = P + 1
	t18 = t18 + 1
	stack[int(t18)] = t13
	t18 = t18 + 1
	stack[int(t18)] = t7
	P = P + 1
	concat_string()
	t18 = stack[int(P)]
	P = P - 1
	t7 = heap[int(t16)]
	t19 = H
	heap[int(H)] = t7
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t20 = P + 1
	t20 = t20 + 1
	stack[int(t20)] = t18
	t20 = t20 + 1
	stack[int(t20)] = t19
	P = P + 1
	concat_string()
	t20 = stack[int(P)]
	P = P - 1
	t19 = H
	heap[int(H)] = 39
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t18 = P + 1
	t18 = t18 + 1
	stack[int(t18)] = t20
	t18 = t18 + 1
	stack[int(t18)] = t19
	P = P + 1
	concat_string()
	t18 = stack[int(P)]
	P = P - 1
	t19 = H
	heap[int(H)] = 44
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t20 = P + 1
	t20 = t20 + 1
	stack[int(t20)] = t18
	t20 = t20 + 1
	stack[int(t20)] = t19
	P = P + 1
	concat_string()
	t20 = stack[int(P)]
	P = P - 1
	t16 = t16 + 1
	goto L8
L9:
	t19 = H
	heap[int(H)] = 39
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t18 = P + 1
	t18 = t18 + 1
	stack[int(t18)] = t20
	t18 = t18 + 1
	stack[int(t18)] = t19
	P = P + 1
	concat_string()
	t18 = stack[int(P)]
	P = P - 1
	t19 = heap[int(t16)]
	t21 = H
	heap[int(H)] = t19
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t22 = P + 1
	t22 = t22 + 1
	stack[int(t22)] = t18
	t22 = t22 + 1
	stack[int(t22)] = t21
	P = P + 1
	concat_string()
	t22 = stack[int(P)]
	P = P - 1
	t21 = H
	heap[int(H)] = 39
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t18 = P + 1
	t18 = t18 + 1
	stack[int(t18)] = t22
	t18 = t18 + 1
	stack[int(t18)] = t21
	P = P + 1
	concat_string()
	t18 = stack[int(P)]
	P = P - 1
	t21 = H
	heap[int(H)] = 93
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t22 = P + 1
	t22 = t22 + 1
	stack[int(t22)] = t18
	t22 = t22 + 1
	stack[int(t22)] = t21
	P = P + 1
	concat_string()
	t22 = stack[int(P)]
	P = P - 1
	t20 = H
	heap[int(H)] = 93
	H = H + 1
	heap[int(H)] = -1
	H = H + 1
	t15 = P + 1
	t15 = t15 + 1
	stack[int(t15)] = t22
	t15 = t15 + 1
	stack[int(t15)] = t20
	P = P + 1
	concat_string()
	t15 = stack[int(P)]
	P = P - 1
	/* final to_string(array) */
	t20 = P + 1
	t20 = t20 + 1
	stack[int(t20)] = t15
	P = P + 1
	F_print()
	t8 = stack[int(P)]
	P = P - 1
	fmt.Printf("%c", int(10))

}
