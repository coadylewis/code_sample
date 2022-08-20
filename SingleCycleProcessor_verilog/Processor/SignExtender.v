module SignExtender(BusImm, Imm32, Ctrl);
    //output
    output [63:0] BusImm;
    //inputs
    input [31:0] Imm32;
    input Ctrl;
    //intermediate var
    wire extBit;
    reg [31:0] temp;
    integer n;
    reg s;
    reg [97:0] temp2;
    always @ (Imm32) begin
        casex(Imm32[31:21])
            11'b11111000010: begin
                temp <= Imm32 << 11;
                n <= 23;
            end
            11'b11111000000: begin
                temp <= Imm32 << 11;
                n <= 23;
            end
            11'b10110100xxx: begin
                temp <= Imm32 << 8;
                n <= 13;
            end
            11'b000101xxxxx: begin
                temp <= Imm32 << 6;
                n <= 6;
            end
        endcase
    end
    //assign bit to append
    assign #1 extBit = (Ctrl ? 1'b0 : temp[31]);
    //append 32 of the above bit to the left of Imm32
  assign #2 temp2 = {{(66){extBit}}, temp} >> n;
  assign #3 BusImm = temp2[63:0];
endmodule