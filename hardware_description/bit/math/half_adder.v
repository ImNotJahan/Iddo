module half_adder(sum, carry, in1, in2);
    input in1, in2;
    output sum, carry;

    xor xor1 (sum, in1, in2);
    and and1 (carry, in1, in2);
endmodule