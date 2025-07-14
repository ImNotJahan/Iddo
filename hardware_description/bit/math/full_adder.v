module full_adder(sum, carry, in1, in2, in3);
    input in1, in2, in3;
    output sum, carry;

    half_adder ha1 (ha2_in1, ha1_carry, in1, in2);
    half_adder ha2 (sum, ha2_carry, ha2_in1, in3);
    or or1 (carry, ha1_carry, ha2_carry);
endmodule