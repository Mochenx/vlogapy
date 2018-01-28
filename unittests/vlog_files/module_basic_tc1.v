
module BasicTC1_0(
    port1,
    port2,
    port3);

input port1;
input port2;
input port3;
always @(posedge clk or negedge rst_n) begin
    if(!rst_n) blah blah;
    else begin
        blah blah blah;
    end
end

endmodule


module BasicTC1_1(
    port1,

    port2);

@;

endmodule


module
BasicTC1_2
();

@;

endmodule


module
BasicTC1_3
(inout [1:0] port1, input [2:0] port2, output [3:  0] port3,
inout signed [4:  0]port4, input signed [  5 :0] port5,
output signed [6+0:0] port6);

input [1:0] port_in_1;
@;
wakaka = wahaha;
output reg [2:0] port_out_2;
xxx_4to1 u_xxx_13(
.clk_ddr(data_tx_clk    ),
.clk    (tx_ck_sync_1   ),
.data   (ch13_d         ),
.pwd    (reg_pd_ch[13]  ),
.set_clk( 1'b0          ),
.xxx_p  (pad_tx_13p     ),
.xxx_n  (pad_tx_13m     ));

always@(*) begin
    if(~resetn)
        clk_out = 1'b0;
    else begin
        case(k_div)
            5'b0_0000: clk_out = clk_in;
            5'b0_0001: clk_out = clk_in;
            5'b0_0010: clk_out = clk_cnt[0];
            5'b0_0100: clk_out = clk_cnt[1];
            5'b0_1000: clk_out = clk_cnt[2];
            5'b1_0000: clk_out = clk_cnt[3];
            default  : clk_out = 1'b0;
        endcase
    end
end

endmodule
