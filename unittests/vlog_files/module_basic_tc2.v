module xxx_tx_phy_digital (
     // input
     ch0_d,
     ch1_d,
     ch2_d,
     ch3_d,
     ch4_d,
     ch5_d,
     ch6_d,
     ch7_d,
     ch8_d,
     ch9_d,
     ch10_d,
     ch11_d,
     ch12_d,
     ch13_d,
     ch14_d,
     ch15_d,
     ch16_d,
     ch17_d,
     ch18_d,
     ch19_d,
     ch20_d,
     ch21_d,
     ch22_d,
     ch23_d,
     ch24_d,
     ch25_d,
     ch26_d,

     // clk output
     tx_ck_sync_0,
     tx_ck_sync_1,

     // clk input, from VCO
     tx_ck ,   //1.2GHz clock input from PLL

     k_div,      // [4:0] Divider K for Main Clock
     resetn,

     rterm,      // [5:0] terminal resistor control signal
     tx_boost,   // pre_emphsis enable
     reg_pd_ch,  // [26:0] Power down signal of TX PHY CH. 1 : Power down 0 : Power On
     reg_vcm,    // [2:0] common mode voltage control signal
     reg_vod,    // [2:0] differential Voltage"Vtop-Vbot"
     pd_bias,    // Power down signal of TX PHY Bias circuits. 1 : Power down, 0 : Power On
     test_en,     // test enable signal
     test_bit,    // [2:0] test control signal
     reserved,    // [7:0] reserved0<7:0>

     // analog pin
     ic25u_in,
     ipp25u_in,
     dc_tp,

     //power
     dvdd_10,
     dvss_10,
     avdd18,
     avss18,
     avdd18_xxx,  //pad
     avss18_xxx,  //pad
     avdd10_xxx,  //pad
     avss10_xxx,  //pad

     // output
     pad_tx_0p ,
     pad_tx_0m ,
     pad_tx_1p ,
     pad_tx_1m ,
     pad_tx_2p ,
     pad_tx_2m ,
     pad_tx_3p ,
     pad_tx_3m ,
     pad_tx_4p ,
     pad_tx_4m ,
     pad_tx_5p ,
     pad_tx_5m ,
     pad_tx_6p ,
     pad_tx_6m ,
     pad_tx_7p ,
     pad_tx_7m ,
     pad_tx_8p ,
     pad_tx_8m ,
     pad_tx_9p ,
     pad_tx_9m ,
     pad_tx_10p,
     pad_tx_10m,
     pad_tx_11p,
     pad_tx_11m,
     pad_tx_12p,
     pad_tx_12m,
     pad_tx_13p,
     pad_tx_13m,
     pad_tx_14p,
     pad_tx_14m,
     pad_tx_15p,
     pad_tx_15m,
     pad_tx_16p,
     pad_tx_16m,
     pad_tx_17p,
     pad_tx_17m,
     pad_tx_18p,
     pad_tx_18m,
     pad_tx_19p,
     pad_tx_19m,
     pad_tx_20p,
     pad_tx_20m,
     pad_tx_21p,
     pad_tx_21m,
     pad_tx_22p,
     pad_tx_22m,
     pad_tx_23p,
     pad_tx_23m,
     pad_tx_24p,
     pad_tx_24m,
     pad_tx_25p,
     pad_tx_25m,
     pad_tx_26p,
     pad_tx_26m
    );

input [3:0]  ch0_d;
input [3:0]  ch1_d;
input [3:0]  ch2_d;
input [3:0]  ch3_d;
input [3:0]  ch4_d;
input [3:0]  ch5_d;
input [3:0]  ch6_d;
input [3:0]  ch7_d;
input [3:0]  ch8_d;
input [3:0]  ch9_d;
input [3:0]  ch10_d;
input [3:0]  ch11_d;
input [3:0]  ch12_d;
input [3:0]  ch13_d;
input [3:0]  ch14_d;
input [3:0]  ch15_d;
input [3:0]  ch16_d;
input [3:0]  ch17_d;
input [3:0]  ch18_d;
input [3:0]  ch19_d;
input [3:0]  ch20_d;
input [3:0]  ch21_d;
input [3:0]  ch22_d;
input [3:0]  ch23_d;
input [3:0]  ch24_d;
input [3:0]  ch25_d;
input [3:0]  ch26_d;

output       tx_ck_sync_0;
output       tx_ck_sync_1;

input        tx_ck ;
input [4:0]  k_div;
input        resetn; //divider
input [5:0]  rterm;
input        tx_boost;
input [26:0] reg_pd_ch;
input [2:0]  reg_vcm;
input [2:0]  reg_vod;
input        pd_bias;
input        test_en;
input [2:0]  test_bit;
input [7:0]  reserved;

input        ic25u_in;
input        ipp25u_in;
output       dc_tp;

// power
input        dvdd_10;
input        dvss_10;
input        avdd18;
input        avss18;
input        avdd18_xxx;
input        avss18_xxx;
input        avdd10_xxx;
input        avss10_xxx;

// output
output     pad_tx_0p;
output     pad_tx_0m;
output     pad_tx_1p;
output     pad_tx_1m;
output     pad_tx_2p;
output     pad_tx_2m;
output     pad_tx_3p;
output     pad_tx_3m;
output     pad_tx_4p;
output     pad_tx_4m;
output     pad_tx_5p;
output     pad_tx_5m;
output     pad_tx_6p;
output     pad_tx_6m;
output     pad_tx_7p;
output     pad_tx_7m;
output     pad_tx_8p;
output     pad_tx_8m;
output     pad_tx_9p;
output     pad_tx_9m;
output     pad_tx_10p;
output     pad_tx_10m;
output     pad_tx_11p;
output     pad_tx_11m;
output     pad_tx_12p;
output     pad_tx_12m;
output     pad_tx_13p;
output     pad_tx_13m;
output     pad_tx_14p;
output     pad_tx_14m;
output     pad_tx_15p;
output     pad_tx_15m;
output     pad_tx_16p;
output     pad_tx_16m;
output     pad_tx_17p;
output     pad_tx_17m;
output     pad_tx_18p;
output     pad_tx_18m;
output     pad_tx_19p;
output     pad_tx_19m;
output     pad_tx_20p;
output     pad_tx_20m;
output     pad_tx_21p;
output     pad_tx_21m;
output     pad_tx_22p;
output     pad_tx_22m;
output     pad_tx_23p;
output     pad_tx_23m;
output     pad_tx_24p;
output     pad_tx_24m;
output     pad_tx_25p;
output     pad_tx_25m;
output     pad_tx_26p;
output     pad_tx_26m;

reg        tx_ck_sync_0;
reg        tx_ck_sync_1;

wire       pad_tx_0p;
wire       pad_tx_0m;
wire       pad_tx_1p;
wire       pad_tx_1m;
wire       pad_tx_2p;
wire       pad_tx_2m;
wire       pad_tx_3p;
wire       pad_tx_3m;
wire       pad_tx_4p;
wire       pad_tx_4m;
wire       pad_tx_5p;
wire       pad_tx_5m;
wire       pad_tx_6p;
wire       pad_tx_6m;
wire       pad_tx_7p;
wire       pad_tx_7m;
wire       pad_tx_8p;
wire       pad_tx_8m;
wire       pad_tx_9p;
wire       pad_tx_9m;
wire       pad_tx_10p;
wire       pad_tx_10m;
wire       pad_tx_11p;
wire       pad_tx_11m;
wire       pad_tx_12p;
wire       pad_tx_12m;
wire       pad_tx_13p;
wire       pad_tx_13m;
wire       pad_tx_14p;
wire       pad_tx_14m;
wire       pad_tx_15p;
wire       pad_tx_15m;
wire       pad_tx_16p;
wire       pad_tx_16m;
wire       pad_tx_17p;
wire       pad_tx_17m;
wire       pad_tx_18p;
wire       pad_tx_18m;
wire       pad_tx_19p;
wire       pad_tx_19m;
wire       pad_tx_20p;
wire       pad_tx_20m;
wire       pad_tx_21p;
wire       pad_tx_21m;
wire       pad_tx_22p;
wire       pad_tx_22m;
wire       pad_tx_23p;
wire       pad_tx_23m;
wire       pad_tx_24p;
wire       pad_tx_24m;
wire       pad_tx_25p;
wire       pad_tx_25m;
wire       pad_tx_26p;
wire       pad_tx_26m;




//==========================================================================
//==========================================================================
wire data_tx_clk;
tx_clk_div u_tx_clk_div_sync(
    .resetn ( resetn    ),
    .clk_in ( tx_ck  ),
    .k_div  ( k_div     ),
    .clk_out( data_tx_clk)
);


//==========================================================================
initial begin tx_ck_sync_0 = 0 ; tx_ck_sync_1 = 0 ; end

always @ (posedge data_tx_clk) begin
  tx_ck_sync_0 <= ~tx_ck_sync_0 ;
  tx_ck_sync_1 <= ~tx_ck_sync_1 ;
end

//==========================================================================
xxx_4to1 u_xxx_0(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_0   ),
      .data   (ch0_d          ),
      .pwd    (reg_pd_ch[0]   ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_0p      ),
      .xxx_n  (pad_tx_0m      ));

xxx_4to1 u_xxx_1(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_0   ),
      .data   (ch1_d          ),
      .pwd    (reg_pd_ch[1]   ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_1p      ),
      .xxx_n  (pad_tx_1m      ));

xxx_4to1 u_xxx_2(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_0   ),
      .data   (ch2_d          ),
      .pwd    (reg_pd_ch[2]   ),
      .set_clk( 1'b0      ),
      .xxx_p  (pad_tx_2p      ),
      .xxx_n  (pad_tx_2m      ));

xxx_4to1 u_xxx_3(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_0   ),
      .data   (ch3_d          ),
      .pwd    (reg_pd_ch[3]   ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_3p      ),
      .xxx_n  (pad_tx_3m      ));

xxx_4to1 u_xxx_4(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_0   ),
      .data   (ch4_d          ),
      .pwd    (reg_pd_ch[4]   ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_4p      ),
      .xxx_n  (pad_tx_4m      ));

xxx_4to1 u_xxx_5(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_0   ),
      .data   (ch5_d          ),
      .pwd    (reg_pd_ch[5]   ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_5p      ),
      .xxx_n  (pad_tx_5m      ));

xxx_4to1 u_xxx_6(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_0   ),
      .data   (ch6_d          ),
      .pwd    (reg_pd_ch[6]   ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_6p      ),
      .xxx_n  (pad_tx_6m      ));

xxx_4to1 u_xxx_7(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_0   ),
      .data   (ch7_d          ),
      .pwd    (reg_pd_ch[7]   ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_7p      ),
      .xxx_n  (pad_tx_7m      ));

//====
xxx_4to1 u_xxx_8(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_1   ),
      .data   (ch8_d          ),
      .pwd    (reg_pd_ch[8]   ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_8p      ),
      .xxx_n  (pad_tx_8m      ));

xxx_4to1 u_xxx_9(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_1   ),
      .data   (ch9_d          ),
      .pwd    (reg_pd_ch[9]   ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_9p      ),
      .xxx_n  (pad_tx_9m      ));

xxx_4to1 u_xxx_10(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_1   ),
      .data   (ch10_d         ),
      .pwd    (reg_pd_ch[10]  ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_10p     ),
      .xxx_n  (pad_tx_10m     ));

xxx_4to1 u_xxx_11(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_1   ),
      .data   (ch11_d         ),
      .pwd    (reg_pd_ch[11]  ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_11p     ),
      .xxx_n  (pad_tx_11m     ));

xxx_4to1 u_xxx_12(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_1   ),
      .data   (ch12_d         ),
      .pwd    (reg_pd_ch[12]  ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_12p     ),
      .xxx_n  (pad_tx_12m     ));

xxx_4to1 u_xxx_13(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_1   ),
      .data   (ch13_d         ),
      .pwd    (reg_pd_ch[13]  ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_13p     ),
      .xxx_n  (pad_tx_13m     ));

xxx_4to1 u_xxx_14(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_1   ),
      .data   (ch14_d         ),
      .pwd    (reg_pd_ch[14]  ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_14p     ),
      .xxx_n  (pad_tx_14m     ));

xxx_4to1 u_xxx_15(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_1   ),
      .data   (ch15_d         ),
      .pwd    (reg_pd_ch[15]  ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_15p     ),
      .xxx_n  (pad_tx_15m     ));

xxx_4to1 u_xxx_16(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_0   ),
      .data   (ch16_d         ),
      .pwd    (reg_pd_ch[16]  ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_16p     ),
      .xxx_n  (pad_tx_16m     ));

xxx_4to1 u_xxx_17(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_0   ),
      .data   (ch17_d         ),
      .pwd    (reg_pd_ch[17]  ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_17p      ),
      .xxx_n  (pad_tx_17m     ));

//====
xxx_4to1 u_xxx_18(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_1   ),
      .data   (ch18_d         ),
      .pwd    (reg_pd_ch[18]  ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_18p     ),
      .xxx_n  (pad_tx_18m    ));

xxx_4to1 u_xxx_19(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_1   ),
      .data   (ch19_d          ),
      .pwd    (reg_pd_ch[19]   ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_19p      ),
      .xxx_n  (pad_tx_19m      ));

xxx_4to1 u_xxx_20(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_1   ),
      .data   (ch20_d          ),
      .pwd    (reg_pd_ch[20]  ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_20p     ),
      .xxx_n  (pad_tx_20m     ));

xxx_4to1 u_xxx_21(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_0   ),
      .data   (ch21_d         ),
      .pwd    (reg_pd_ch[21]  ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_21p     ),
      .xxx_n  (pad_tx_21m     ));

xxx_4to1 u_xxx_22(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_0   ),
      .data   (ch22_d         ),
      .pwd    (reg_pd_ch[22]  ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_22p     ),
      .xxx_n  (pad_tx_22m     ));

xxx_4to1 u_xxx_23(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_0   ),
      .data   (ch23_d         ),
      .pwd    (reg_pd_ch[23]  ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_23p     ),
      .xxx_n  (pad_tx_23m     ));

xxx_4to1 u_xxx_24(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_0   ),//need check
      .data   (ch24_d         ),
      .pwd    (reg_pd_ch[24]  ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_24p     ),
      .xxx_n  (pad_tx_24m     ));

xxx_4to1 u_xxx_25(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_0   ),//need check
      .data   (ch25_d         ),
      .pwd    (reg_pd_ch[25]  ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_25p     ),
      .xxx_n  (pad_tx_25m     ));

xxx_4to1 u_xxx_26(
      .clk_ddr(data_tx_clk    ),
      .clk    (tx_ck_sync_0   ),//need check
      .data   (ch26_d         ),
      .pwd    (reg_pd_ch[26]  ),
      .set_clk( 1'b0          ),
      .xxx_p  (pad_tx_26p     ),
      .xxx_n  (pad_tx_26m     ));

endmodule

//==========================================================================
//==========================================================================
//==========================================================================
module tx_clk_div(
    input resetn,
    input clk_in,
    input [4:0] k_div,
    output reg clk_out
    );

reg [3:0] clk_cnt;
initial clk_cnt = 4'b0;
always @ (posedge clk_in)
    clk_cnt <= clk_cnt + 1'b1;

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
