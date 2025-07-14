module test;
    initial begin
        $dumpfile("test.vcd");
        $dumpvars(0, test);
    end

    reg in1, in2, in3;
    wire sum, carry;

    full_adder fa (sum, carry, in1, in2, in3);

    initial begin
        assign in1 = 0;
        assign in2 = 0;
        assign in3 = 0;
        #1 assign in1 = 1;
        #1 assign in2 = 1;
        #1 assign in3 = 1;
        #1 assign in1 = 0;
        #1 assign in2 = 0;
        #1 assign in2 = 1;
        assign in3 = 0;
        #1 $finish;
    end

    initial
        $monitor("%d + %d + %d = sum %d, carry %d",
            in1, in2, in3, sum, carry);
endmodule