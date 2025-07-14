module test;
    initial begin
        $dumpfile("test.vcd");
        $dumpvars(0, test);
    end

    reg [7:0] in1, in2;
    wire [7:0] sum;
    wire carry;

    reg carry_in = 0;

    add8 add (sum, carry, in1, in2, carry_in);

    initial begin
        assign in1 = 0;
        assign in2 = 0;
        #1 assign in1 = 5;
        #1 assign in2 = 65;
        #1 assign in1 = 255;
        #1 assign in2 = 100;
        #1 $finish;
    end

    initial
        $monitor("%d + %d = sum %d, carry %d",
            in1, in2, sum, carry);
endmodule