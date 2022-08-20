`define AND 4'b0000
`define OR 4'b0001
`define ADD 4'b0010
`define LSL 4'b0011
`define LSR 4'b0100
`define SUB 4'b0110
`define PassB 4'b0111


module ALU(BusW, Zero, BusA, BusB, ALUCtrl);

    parameter n = 64;
    //outputs
    output  [n-1:0] BusW;
    output  Zero;
    //inputs
    input   [n-1:0] BusA, BusB;
    input   [3:0] ALUCtrl;

    //write Bus
    reg     [n-1:0] BusW;

  always @(*) begin
        case(ALUCtrl)
            `AND: begin
                BusW <= #20 BusA & BusB; //bitwise and
            end
            `OR: begin
                BusW <= #20 BusA | BusB;  //bitwise or
            end
            `ADD: begin
                BusW <= #20 BusA + BusB;  //add
            end
            `LSL: begin
              BusW <= #20 BusA << BusB; //shift BusA left by BusB bits
            end
            `LSR: begin
                BusW <= #20 BusA >> BusB; //shift BusA right by BusB bits
            end
            `SUB: begin
                BusW <= #20 BusA - BusB; //subtract
            end
            `PassB: begin
                BusW <= #20 BusB; //write BusB to Bus W
            end
        endcase
    end
    //assign Zero's val based on BusW
  assign #1 Zero = (BusW)? 0:1;
endmodule