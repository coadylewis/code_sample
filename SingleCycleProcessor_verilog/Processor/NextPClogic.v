module NextPClogic (NextPC, CurrentPC, SignExtImm64, Branch, ALUZero, Uncondbranch);
    //inputs
    input [63:0] CurrentPC, SignExtImm64;
    input Branch, ALUZero, Uncondbranch;
    //output (reg to use <= operator below)
    output reg [63:0] NextPC;
    always @ (*) begin //update every time a value changes
        if (Uncondbranch || (Branch && ALUZero)) //Handled as described in the text
          NextPC <= #3 CurrentPC + (SignExtImm64 << 2); //add offset to the program counter
        else
            NextPC <= #2 CurrentPC + 4; //standard: move to next instruction
    end
endmodule

