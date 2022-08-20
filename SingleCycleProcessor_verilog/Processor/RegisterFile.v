module RegisterFile(BusA, BusB, BusW, RA, RB, RW, RegWr, Clk);
    //outputs
    output [63:0] BusA;
    output [63:0] BusB;
    //inputs
    input [63:0] BusW;
    input [4:0] RW, RA, RB;
    input RegWr;
    input Clk;
    //registers
    reg [63:0] registers [31:0];


    //give the output busses the respective values at the
    //indices of RA and RB in registers
    assign #2 BusA = registers[RA];
    assign #2 BusB = registers[RB];
    //at all times, registers[31] is 0


    //at the falling edge of Clk and when the RW index
    // is not 31, BusW is written to registers[RW]
    always @ (negedge Clk) begin
        if(RegWr && RW!=31)
            registers[RW] <= #3 BusW;
        registers[31] <= 64'b0;
    end

endmodule