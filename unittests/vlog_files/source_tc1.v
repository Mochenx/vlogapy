`timescale 1ns/1ps
/* Some
** comments
** in
** different lines **/
module _test_source (
     // input
     in0,

     // clk output
     clkout,

     // clk input, from VCO
     ckin0 ,   //1.2GHz clock input from PLL

     ckin1,      // [4:0] Divider K for Main Clock

`ifdef POWER
     //power
     pw,
`endif

     // output
     out0 ,
     out1
    );

output       out0;

`ifdef POWER
`else
// power
input        in0;
`endif

// output
output     out1;

//==========================================================================
//==========================================================================
//==========================================================================
endmodule
