module ALUControl(ALUCtrl, ALUop, Opcode);
    //inputs
    input [1:0] ALUop;
    input [10:0] Opcode;
    //output (reg to use <= operator below)
    output reg [3:0] ALUCtrl;
    always @ (*) begin //update every time a value changes
        case(ALUop) //Handle the 3 possible inputs
            2'b00: begin
                ALUCtrl <= #2 4'b0010; //STUR and LDUR
            end
            2'b01: begin
                ALUCtrl <= #2 4'b0111; //CBZ
            end
            2'b10: begin
                case(Opcode) //Handle Opcode for 4 R-types
                    11'b10001011000: begin
                        ALUCtrl <= #2 4'b0010; //ADD
                    end
                    11'b11001011000: begin
                        ALUCtrl <= #2 4'b0110; //SUB
                    end
                    11'b10001010000: begin
                        ALUCtrl <= #2 4'b0000; //AND
                    end
                    11'b10101010000: begin
                        ALUCtrl <= #2 4'b0001; //OR
                    end
                endcase
            end
        endcase
    end
endmodule