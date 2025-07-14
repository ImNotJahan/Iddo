module add8(sum, carry, in1, in2, carry_in);
    input [7:0] in1, in2;
    input carry_in;
    output [7:0] sum;
    output carry;

    wire [6:0] adder_carry;

    full_adder fa1 (sum[0], adder_carry[0], in1[0], in2[0], carry_in);
    full_adder fa2 (sum[1], adder_carry[1], in1[1], in2[1], adder_carry[0]);
    full_adder fa3 (sum[2], adder_carry[2], in1[2], in2[2], adder_carry[1]);
    full_adder fa4 (sum[3], adder_carry[3], in1[3], in2[3], adder_carry[2]);
    full_adder fa5 (sum[4], adder_carry[4], in1[4], in2[4], adder_carry[3]);
    full_adder fa6 (sum[5], adder_carry[5], in1[5], in2[5], adder_carry[4]);
    full_adder fa7 (sum[6], adder_carry[6], in1[6], in2[6], adder_carry[5]);
    full_adder fa8 (sum[7], carry, in1[7], in2[7], adder_carry[6]);
endmodule