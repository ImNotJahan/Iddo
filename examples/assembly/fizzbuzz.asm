// loop through numbers 1-100. if divisible by 3, output 0; if divisible by 7, output 1; if divisible by both, output 2
const i R0
MOVE 1 i

const temp R1

label loop

MOVE i OUTPUT

MOD i 3 temp
EQ temp 0 fizz
MOD i 7 temp
EQ temp 0 buzz
JUMP loopend

label fizz
MOD i 7 temp
EQ temp 0 fizzbuzz
MOVE 0 OUTPUT
JUMP loopend

label buzz
MOVE 1 OUTPUT
JUMP loopend

label fizzbuzz
MOVE 2 OUTPUT

label loopend
ADD 1 i i
NEQ i 101 loop