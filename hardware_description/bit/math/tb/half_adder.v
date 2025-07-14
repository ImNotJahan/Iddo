module test;
    initial begin
        $dumpfile("test.vcd");
        $dumpvars(0, test);
    end

    reg in1, in2;
    wire sum, carry;

    half_adder ha (sum, carry, in1, in2);

    initial begin
        assign in1 = 0;
        assign in2 = 0;
        #1 assign in1 = 1;
        #1 assign in2 = 1;
        #1 assign in1 = 0;
        #1 $finish;
    end

    initial
        $monitor("%d + %d = sum %d, carry %d",
            in1, in2, sum, carry);
endmodule