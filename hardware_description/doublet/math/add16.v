module add16(sum, carry, in1, in2);
    input[15:0] in1, in2;
    output[15:0] sum;
    output carry;

    wire adder1carry;

    add8 adder1 (sum[7:0], adder1carry, in1[7:0], in2[7:0], 0);
    add8 adder2 (sum[15:8], carry, in1[15:8], in2[15:8], adder1carry);
endmodule