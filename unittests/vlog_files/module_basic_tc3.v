// Library - xxx_tx, Cell - xxx_tx_phy_timingmodel, View - schematic
// LAST TIME SAVED: Dec  2 10:23:20 2013
// NETLIST TIME: Dec  2 10:27:49 2013
`timescale 1ns / 1ns 

module xxx_tx_phy ( dc_tp, tx_ck_sync_0, tx_ck_sync_1,
     avdd10_usi, avdd18, avdd18_usi, avss10_usi, avss18, avss18_usi,
     dvdd_10, dvss_10, pad_tx_0m, pad_tx_0p, pad_tx_1m, pad_tx_1p,
     pad_tx_2m, pad_tx_2p, pad_tx_3m, pad_tx_3p, pad_tx_4m, pad_tx_4p,
     pad_tx_5m, pad_tx_5p, pad_tx_6m, pad_tx_6p, pad_tx_7m, pad_tx_7p,
     pad_tx_8m, pad_tx_8p, pad_tx_9m, pad_tx_9p, pad_tx_10m,
     pad_tx_10p, pad_tx_11m, pad_tx_11p, pad_tx_12m, pad_tx_12p,
     pad_tx_13m, pad_tx_13p, pad_tx_14m, pad_tx_14p, pad_tx_15m,
     pad_tx_15p, pad_tx_16m, pad_tx_16p, pad_tx_17m, pad_tx_17p,
     pad_tx_18m, pad_tx_18p, pad_tx_19m, pad_tx_19p, pad_tx_20m,
     pad_tx_20p, pad_tx_21m, pad_tx_21p, pad_tx_22m, pad_tx_22p,
     pad_tx_23m, pad_tx_23p, pad_tx_24m, pad_tx_24p, pad_tx_25m,
     pad_tx_25p, pad_tx_26m, pad_tx_26p, ch0_d, ch1_d, ch2_d, ch3_d,
     ch4_d, ch5_d, ch6_d, ch7_d, ch8_d, ch9_d, ch10_d, ch11_d, ch12_d,
     ch13_d, ch14_d, ch15_d, ch16_d, ch17_d, ch18_d, ch19_d, ch20_d,
     ch21_d, ch22_d, ch23_d, ch24_d, ch25_d, ch26_d, ic25u_in,
     ipp25u_in, k_div, pd_bias, reg_pd_ch, reg_vcm, reg_vod, reserved,
     resetn, rterm, test_bit, test_en, tx_boost, tx_ck );

output  dc_tp, tx_ck_sync_0, tx_ck_sync_1;

inout  avdd10_usi, avdd18, avdd18_usi, avss10_usi, avss18, avss18_usi,
     dvdd_10, dvss_10, pad_tx_0m, pad_tx_0p, pad_tx_1m, pad_tx_1p,
     pad_tx_2m, pad_tx_2p, pad_tx_3m, pad_tx_3p, pad_tx_4m, pad_tx_4p,
     pad_tx_5m, pad_tx_5p, pad_tx_6m, pad_tx_6p, pad_tx_7m, pad_tx_7p,
     pad_tx_8m, pad_tx_8p, pad_tx_9m, pad_tx_9p, pad_tx_10m,
     pad_tx_10p, pad_tx_11m, pad_tx_11p, pad_tx_12m, pad_tx_12p,
     pad_tx_13m, pad_tx_13p, pad_tx_14m, pad_tx_14p, pad_tx_15m,
     pad_tx_15p, pad_tx_16m, pad_tx_16p, pad_tx_17m, pad_tx_17p,
     pad_tx_18m, pad_tx_18p, pad_tx_19m, pad_tx_19p, pad_tx_20m,
     pad_tx_20p, pad_tx_21m, pad_tx_21p, pad_tx_22m, pad_tx_22p,
     pad_tx_23m, pad_tx_23p, pad_tx_24m, pad_tx_24p, pad_tx_25m,
     pad_tx_25p, pad_tx_26m, pad_tx_26p;

input  ic25u_in, ipp25u_in, pd_bias, resetn, test_en, tx_boost, tx_ck;

input [3:0]  ch24_d;
input [3:0]  ch25_d;
input [3:0]  ch26_d;
input [3:0]  ch23_d;
input [3:0]  ch22_d;
input [3:0]  ch18_d;
input [3:0]  ch20_d;
input [3:0]  ch21_d;
input [3:0]  ch19_d;
input [3:0]  ch16_d;
input [3:0]  ch13_d;
input [3:0]  ch14_d;
input [3:0]  ch12_d;
input [3:0]  ch17_d;
input [3:0]  ch15_d;
input [3:0]  ch8_d;
input [3:0]  ch7_d;
input [3:0]  ch9_d;
input [3:0]  ch6_d;
input [3:0]  ch10_d;
input [3:0]  ch11_d;
input [3:0]  ch2_d;
input [3:0]  ch4_d;
input [3:0]  ch0_d;
input [3:0]  ch5_d;
input [3:0]  ch3_d;
input [3:0]  ch1_d;
input [5:0]  rterm;
input [2:0]  reg_vcm;
input [2:0]  reg_vod;
input [2:0]  test_bit;
input [4:0]  k_div;
input [26:0]  reg_pd_ch;
input [7:0]  reserved;

// Buses in the design

wire  [0:1]  qd0;

wire  [0:1]  qb0;

wire  [0:1]  ckdiv4;

wire  [0:1]  qb1;

wire  [0:1]  qd1;

wire  [1:0]  sla_slice;

wire  [2:0]  vod_ctl_hv;

wire  [2:0]  vcm_sel_hv;

wire  [2:0]  test_bit_hv;

wire  [5:0]  rtm;

wire  [2:0]  ic25u;

wire  [2:0]  ipp25u;

wire  [1:0]  clkdiv4;

wire  [0:26]  ckout;

wire  [0:26]  clkout;

wire  [0:26]  ckdiv4a;


specify
    specparam CDS_LIBNAME  = "xxx_tx";
    specparam CDS_CELLNAME = "xxx_tx_phy_timingmodel";
    specparam CDS_VIEWNAME = "schematic";
endspecify

  tx_green_top_null_block I_NULL_0 (.null_clk(clk_left));
  tx_green_top_null_block I_NULL_1 (.null_clk(clk_right));

DFQRM4NA  I66_3_ ( .Q(net561), .CK(ckdiv4a[25]), .D(ch25_d[3]),
     .RB(pdb));
DFQRM4NA  I66_2_ ( .Q(net561), .CK(ckdiv4a[25]), .D(ch25_d[2]),
     .RB(pdb));
DFQRM4NA  I66_1_ ( .Q(net561), .CK(ckdiv4a[25]), .D(ch25_d[1]),
     .RB(pdb));
DFQRM4NA  I66_0_ ( .Q(net561), .CK(ckdiv4a[25]), .D(ch25_d[0]),
     .RB(pdb));
DFQRM4NA  I65_3_ ( .Q(net562), .CK(ckdiv4a[24]), .D(ch24_d[3]),
     .RB(pdb));
DFQRM4NA  I65_2_ ( .Q(net562), .CK(ckdiv4a[24]), .D(ch24_d[2]),
     .RB(pdb));
DFQRM4NA  I65_1_ ( .Q(net562), .CK(ckdiv4a[24]), .D(ch24_d[1]),
     .RB(pdb));
DFQRM4NA  I65_0_ ( .Q(net562), .CK(ckdiv4a[24]), .D(ch24_d[0]),
     .RB(pdb));
DFQRM4NA  I64_3_ ( .Q(net557), .CK(ckdiv4a[26]), .D(ch26_d[3]),
     .RB(pdb));
DFQRM4NA  I64_2_ ( .Q(net557), .CK(ckdiv4a[26]), .D(ch26_d[2]),
     .RB(pdb));
DFQRM4NA  I64_1_ ( .Q(net557), .CK(ckdiv4a[26]), .D(ch26_d[1]),
     .RB(pdb));
DFQRM4NA  I64_0_ ( .Q(net557), .CK(ckdiv4a[26]), .D(ch26_d[0]),
     .RB(pdb));
DFQRM4NA  I800_3_ ( .Q(net575), .CK(ckdiv4a[9]), .D(ch9_d[3]),
     .RB(pdb));
DFQRM4NA  I800_2_ ( .Q(net575), .CK(ckdiv4a[9]), .D(ch9_d[2]),
     .RB(pdb));
DFQRM4NA  I800_1_ ( .Q(net575), .CK(ckdiv4a[9]), .D(ch9_d[1]),
     .RB(pdb));
DFQRM4NA  I800_0_ ( .Q(net575), .CK(ckdiv4a[9]), .D(ch9_d[0]),
     .RB(pdb));
DFQRM4NA  I695_3_ ( .Q(net605), .CK(ckdiv4a[23]), .D(ch23_d[3]),
     .RB(pdb));
DFQRM4NA  I695_2_ ( .Q(net605), .CK(ckdiv4a[23]), .D(ch23_d[2]),
     .RB(pdb));
DFQRM4NA  I695_1_ ( .Q(net605), .CK(ckdiv4a[23]), .D(ch23_d[1]),
     .RB(pdb));
DFQRM4NA  I695_0_ ( .Q(net605), .CK(ckdiv4a[23]), .D(ch23_d[0]),
     .RB(pdb));
DFQRM4NA  I735_3_ ( .Q(net589), .CK(ckdiv4a[15]), .D(ch15_d[3]),
     .RB(pdb));
DFQRM4NA  I735_2_ ( .Q(net589), .CK(ckdiv4a[15]), .D(ch15_d[2]),
     .RB(pdb));
DFQRM4NA  I735_1_ ( .Q(net589), .CK(ckdiv4a[15]), .D(ch15_d[1]),
     .RB(pdb));
DFQRM4NA  I735_0_ ( .Q(net589), .CK(ckdiv4a[15]), .D(ch15_d[0]),
     .RB(pdb));
DFQRM4NA  I795_3_ ( .Q(net564), .CK(ckdiv4a[8]), .D(ch8_d[3]),
     .RB(pdb));
DFQRM4NA  I795_2_ ( .Q(net564), .CK(ckdiv4a[8]), .D(ch8_d[2]),
     .RB(pdb));
DFQRM4NA  I795_1_ ( .Q(net564), .CK(ckdiv4a[8]), .D(ch8_d[1]),
     .RB(pdb));
DFQRM4NA  I795_0_ ( .Q(net564), .CK(ckdiv4a[8]), .D(ch8_d[0]),
     .RB(pdb));
DFQRM4NA  I805_3_ ( .Q(net568), .CK(ckdiv4a[10]), .D(ch10_d[3]),
     .RB(pdb));
DFQRM4NA  I805_2_ ( .Q(net568), .CK(ckdiv4a[10]), .D(ch10_d[2]),
     .RB(pdb));
DFQRM4NA  I805_1_ ( .Q(net568), .CK(ckdiv4a[10]), .D(ch10_d[1]),
     .RB(pdb));
DFQRM4NA  I805_0_ ( .Q(net568), .CK(ckdiv4a[10]), .D(ch10_d[0]),
     .RB(pdb));
DFQRM4NA  I810_3_ ( .Q(net584), .CK(ckdiv4a[11]), .D(ch11_d[3]),
     .RB(pdb));
DFQRM4NA  I810_2_ ( .Q(net584), .CK(ckdiv4a[11]), .D(ch11_d[2]),
     .RB(pdb));
DFQRM4NA  I810_1_ ( .Q(net584), .CK(ckdiv4a[11]), .D(ch11_d[1]),
     .RB(pdb));
DFQRM4NA  I810_0_ ( .Q(net584), .CK(ckdiv4a[11]), .D(ch11_d[0]),
     .RB(pdb));
DFQRM4NA  I715_3_ ( .Q(net600), .CK(ckdiv4a[19]), .D(ch19_d[3]),
     .RB(pdb));
DFQRM4NA  I715_2_ ( .Q(net600), .CK(ckdiv4a[19]), .D(ch19_d[2]),
     .RB(pdb));
DFQRM4NA  I715_1_ ( .Q(net600), .CK(ckdiv4a[19]), .D(ch19_d[1]),
     .RB(pdb));
DFQRM4NA  I715_0_ ( .Q(net600), .CK(ckdiv4a[19]), .D(ch19_d[0]),
     .RB(pdb));
DFQRM4NA  I745_3_ ( .Q(net592), .CK(ckdiv4a[13]), .D(ch13_d[3]),
     .RB(pdb));
DFQRM4NA  I745_2_ ( .Q(net592), .CK(ckdiv4a[13]), .D(ch13_d[2]),
     .RB(pdb));
DFQRM4NA  I745_1_ ( .Q(net592), .CK(ckdiv4a[13]), .D(ch13_d[1]),
     .RB(pdb));
DFQRM4NA  I745_0_ ( .Q(net592), .CK(ckdiv4a[13]), .D(ch13_d[0]),
     .RB(pdb));
DFQRM4NA  I730_3_ ( .Q(net585), .CK(ckdiv4a[16]), .D(ch16_d[3]),
     .RB(pdb));
DFQRM4NA  I730_2_ ( .Q(net585), .CK(ckdiv4a[16]), .D(ch16_d[2]),
     .RB(pdb));
DFQRM4NA  I730_1_ ( .Q(net585), .CK(ckdiv4a[16]), .D(ch16_d[1]),
     .RB(pdb));
DFQRM4NA  I730_0_ ( .Q(net585), .CK(ckdiv4a[16]), .D(ch16_d[0]),
     .RB(pdb));
DFQRM4NA  I720_3_ ( .Q(net566), .CK(ckdiv4a[18]), .D(ch18_d[3]),
     .RB(pdb));
DFQRM4NA  I720_2_ ( .Q(net566), .CK(ckdiv4a[18]), .D(ch18_d[2]),
     .RB(pdb));
DFQRM4NA  I720_1_ ( .Q(net566), .CK(ckdiv4a[18]), .D(ch18_d[1]),
     .RB(pdb));
DFQRM4NA  I720_0_ ( .Q(net566), .CK(ckdiv4a[18]), .D(ch18_d[0]),
     .RB(pdb));
DFQRM4NA  I740_3_ ( .Q(net593), .CK(ckdiv4a[14]), .D(ch14_d[3]),
     .RB(pdb));
DFQRM4NA  I740_2_ ( .Q(net593), .CK(ckdiv4a[14]), .D(ch14_d[2]),
     .RB(pdb));
DFQRM4NA  I740_1_ ( .Q(net593), .CK(ckdiv4a[14]), .D(ch14_d[1]),
     .RB(pdb));
DFQRM4NA  I740_0_ ( .Q(net593), .CK(ckdiv4a[14]), .D(ch14_d[0]),
     .RB(pdb));
DFQRM4NA  I750_3_ ( .Q(net595), .CK(ckdiv4a[12]), .D(ch12_d[3]),
     .RB(pdb));
DFQRM4NA  I750_2_ ( .Q(net595), .CK(ckdiv4a[12]), .D(ch12_d[2]),
     .RB(pdb));
DFQRM4NA  I750_1_ ( .Q(net595), .CK(ckdiv4a[12]), .D(ch12_d[1]),
     .RB(pdb));
DFQRM4NA  I750_0_ ( .Q(net595), .CK(ckdiv4a[12]), .D(ch12_d[0]),
     .RB(pdb));
DFQRM4NA  I770_3_ ( .Q(net586), .CK(ckdiv4a[3]), .D(ch3_d[3]),
     .RB(pdb));
DFQRM4NA  I770_2_ ( .Q(net586), .CK(ckdiv4a[3]), .D(ch3_d[2]),
     .RB(pdb));
DFQRM4NA  I770_1_ ( .Q(net586), .CK(ckdiv4a[3]), .D(ch3_d[1]),
     .RB(pdb));
DFQRM4NA  I770_0_ ( .Q(net586), .CK(ckdiv4a[3]), .D(ch3_d[0]),
     .RB(pdb));
DFQRM4NA  I705_3_ ( .Q(net567), .CK(ckdiv4a[21]), .D(ch21_d[3]),
     .RB(pdb));
DFQRM4NA  I705_2_ ( .Q(net567), .CK(ckdiv4a[21]), .D(ch21_d[2]),
     .RB(pdb));
DFQRM4NA  I705_1_ ( .Q(net567), .CK(ckdiv4a[21]), .D(ch21_d[1]),
     .RB(pdb));
DFQRM4NA  I705_0_ ( .Q(net567), .CK(ckdiv4a[21]), .D(ch21_d[0]),
     .RB(pdb));
DFQRM4NA  I755_3_ ( .Q(net620), .CK(ckdiv4a[0]), .D(ch0_d[3]),
     .RB(pdb));
DFQRM4NA  I755_2_ ( .Q(net620), .CK(ckdiv4a[0]), .D(ch0_d[2]),
     .RB(pdb));
DFQRM4NA  I755_1_ ( .Q(net620), .CK(ckdiv4a[0]), .D(ch0_d[1]),
     .RB(pdb));
DFQRM4NA  I755_0_ ( .Q(net620), .CK(ckdiv4a[0]), .D(ch0_d[0]),
     .RB(pdb));
DFQRM4NA  I780_3_ ( .Q(net591), .CK(ckdiv4a[5]), .D(ch5_d[3]),
     .RB(pdb));
DFQRM4NA  I780_2_ ( .Q(net591), .CK(ckdiv4a[5]), .D(ch5_d[2]),
     .RB(pdb));
DFQRM4NA  I780_1_ ( .Q(net591), .CK(ckdiv4a[5]), .D(ch5_d[1]),
     .RB(pdb));
DFQRM4NA  I780_0_ ( .Q(net591), .CK(ckdiv4a[5]), .D(ch5_d[0]),
     .RB(pdb));
DFQRM4NA  I785_3_ ( .Q(net574), .CK(ckdiv4a[6]), .D(ch6_d[3]),
     .RB(pdb));
DFQRM4NA  I785_2_ ( .Q(net574), .CK(ckdiv4a[6]), .D(ch6_d[2]),
     .RB(pdb));
DFQRM4NA  I785_1_ ( .Q(net574), .CK(ckdiv4a[6]), .D(ch6_d[1]),
     .RB(pdb));
DFQRM4NA  I785_0_ ( .Q(net574), .CK(ckdiv4a[6]), .D(ch6_d[0]),
     .RB(pdb));
DFQRM4NA  I725_3_ ( .Q(net577), .CK(ckdiv4a[17]), .D(ch17_d[3]),
     .RB(pdb));
DFQRM4NA  I725_2_ ( .Q(net577), .CK(ckdiv4a[17]), .D(ch17_d[2]),
     .RB(pdb));
DFQRM4NA  I725_1_ ( .Q(net577), .CK(ckdiv4a[17]), .D(ch17_d[1]),
     .RB(pdb));
DFQRM4NA  I725_0_ ( .Q(net577), .CK(ckdiv4a[17]), .D(ch17_d[0]),
     .RB(pdb));
DFQRM4NA  I765_3_ ( .Q(net613), .CK(ckdiv4a[2]), .D(ch2_d[3]),
     .RB(pdb));
DFQRM4NA  I765_2_ ( .Q(net613), .CK(ckdiv4a[2]), .D(ch2_d[2]),
     .RB(pdb));
DFQRM4NA  I765_1_ ( .Q(net613), .CK(ckdiv4a[2]), .D(ch2_d[1]),
     .RB(pdb));
DFQRM4NA  I765_0_ ( .Q(net613), .CK(ckdiv4a[2]), .D(ch2_d[0]),
     .RB(pdb));
DFQRM4NA  I710_3_ ( .Q(net603), .CK(ckdiv4a[20]), .D(ch20_d[3]),
     .RB(pdb));
DFQRM4NA  I710_2_ ( .Q(net603), .CK(ckdiv4a[20]), .D(ch20_d[2]),
     .RB(pdb));
DFQRM4NA  I710_1_ ( .Q(net603), .CK(ckdiv4a[20]), .D(ch20_d[1]),
     .RB(pdb));
DFQRM4NA  I710_0_ ( .Q(net603), .CK(ckdiv4a[20]), .D(ch20_d[0]),
     .RB(pdb));
DFQRM4NA  I700_3_ ( .Q(net596), .CK(ckdiv4a[22]), .D(ch22_d[3]),
     .RB(pdb));
DFQRM4NA  I700_2_ ( .Q(net596), .CK(ckdiv4a[22]), .D(ch22_d[2]),
     .RB(pdb));
DFQRM4NA  I700_1_ ( .Q(net596), .CK(ckdiv4a[22]), .D(ch22_d[1]),
     .RB(pdb));
DFQRM4NA  I700_0_ ( .Q(net596), .CK(ckdiv4a[22]), .D(ch22_d[0]),
     .RB(pdb));
DFQRM4NA  I790_3_ ( .Q(net576), .CK(ckdiv4a[7]), .D(ch7_d[3]),
     .RB(pdb));
DFQRM4NA  I790_2_ ( .Q(net576), .CK(ckdiv4a[7]), .D(ch7_d[2]),
     .RB(pdb));
DFQRM4NA  I790_1_ ( .Q(net576), .CK(ckdiv4a[7]), .D(ch7_d[1]),
     .RB(pdb));
DFQRM4NA  I790_0_ ( .Q(net576), .CK(ckdiv4a[7]), .D(ch7_d[0]),
     .RB(pdb));
DFQRM4NA  I775_3_ ( .Q(net611), .CK(ckdiv4a[4]), .D(ch4_d[3]),
     .RB(pdb));
DFQRM4NA  I775_2_ ( .Q(net611), .CK(ckdiv4a[4]), .D(ch4_d[2]),
     .RB(pdb));
DFQRM4NA  I775_1_ ( .Q(net611), .CK(ckdiv4a[4]), .D(ch4_d[1]),
     .RB(pdb));
DFQRM4NA  I775_0_ ( .Q(net611), .CK(ckdiv4a[4]), .D(ch4_d[0]),
     .RB(pdb));
DFQRM4NA  I760_3_ ( .Q(net612), .CK(ckdiv4a[1]), .D(ch1_d[3]),
     .RB(pdb));
DFQRM4NA  I760_2_ ( .Q(net612), .CK(ckdiv4a[1]), .D(ch1_d[2]),
     .RB(pdb));
DFQRM4NA  I760_1_ ( .Q(net612), .CK(ckdiv4a[1]), .D(ch1_d[1]),
     .RB(pdb));
DFQRM4NA  I760_0_ ( .Q(net612), .CK(ckdiv4a[1]), .D(ch1_d[0]),
     .RB(pdb));
DFQSM4NA  I69 ( .Q(net215), .CK(clkout[26]), .D(ckdiv4[1]), .SB(pdb));
DFQSM4NA  I68 ( .Q(net219), .CK(clkout[25]), .D(ckdiv4[1]), .SB(pdb));
DFQSM4NA  I67 ( .Q(net223), .CK(clkout[24]), .D(ckdiv4[1]), .SB(pdb));
DFQSM4NA  I804 ( .Q(net227), .CK(clkout[10]), .D(ckdiv4[0]), .SB(pdb));
DFQSM4NA  I794 ( .Q(net231), .CK(clkout[8]), .D(ckdiv4[0]), .SB(pdb));
DFQSM4NA  I799 ( .Q(net235), .CK(clkout[9]), .D(ckdiv4[0]), .SB(pdb));
DFQSM4NA  I789 ( .Q(net571), .CK(clkout[7]), .D(ckdiv4[0]), .SB(pdb));
DFQSM4NA  I704 ( .Q(net243), .CK(clkout[21]), .D(ckdiv4[1]), .SB(pdb));
DFQSM4NA  I739 ( .Q(net247), .CK(clkout[14]), .D(ckdiv4[0]), .SB(pdb));
DFQSM4NA  I809 ( .Q(net251), .CK(clkout[11]), .D(ckdiv4[0]), .SB(pdb));
DFQSM4NA  I744 ( .Q(net255), .CK(clkout[13]), .D(ckdiv4[0]), .SB(pdb));
DFQSM4NA  I699 ( .Q(net259), .CK(clkout[22]), .D(ckdiv4[1]), .SB(pdb));
DFQSM4NA  I729 ( .Q(net263), .CK(clkout[16]), .D(ckdiv4[0]), .SB(pdb));
DFQSM4NA  I709 ( .Q(net267), .CK(clkout[20]), .D(ckdiv4[1]), .SB(pdb));
DFQSM4NA  I734 ( .Q(net271), .CK(clkout[15]), .D(ckdiv4[0]), .SB(pdb));
DFQSM4NA  I749 ( .Q(net275), .CK(clkout[12]), .D(ckdiv4[0]), .SB(pdb));
DFQSM4NA  I724 ( .Q(net279), .CK(clkout[17]), .D(ckdiv4[0]), .SB(pdb));
DFQSM4NA  I754 ( .Q(net283), .CK(clkout[0]), .D(ckdiv4[1]), .SB(pdb));
DFQSM4NA  I714 ( .Q(net287), .CK(clkout[19]), .D(ckdiv4[1]), .SB(pdb));
DFQSM4NA  I764 ( .Q(net291), .CK(clkout[2]), .D(ckdiv4[1]), .SB(pdb));
DFQSM4NA  I719 ( .Q(net580), .CK(clkout[18]), .D(ckdiv4[1]), .SB(pdb));
DFQSM4NA  I779 ( .Q(net299), .CK(clkout[5]), .D(ckdiv4[1]), .SB(pdb));
DFQSM4NA  I774 ( .Q(net303), .CK(clkout[4]), .D(ckdiv4[1]), .SB(pdb));
DFQSM4NA  I784 ( .Q(net569), .CK(clkout[6]), .D(ckdiv4[0]), .SB(pdb));
DFQSM4NA  I759 ( .Q(net311), .CK(clkout[1]), .D(ckdiv4[1]), .SB(pdb));
DFQSM4NA  I684 ( .Q(net315), .CK(clk_dn), .D(qb0[1]), .SB(resetn));
DFQSM4NA  I683 ( .Q(net319), .CK(clk_dn), .D(net541), .SB(resetn));
DFQSM4NA  I674 ( .Q(net323), .CK(clk_up), .D(qb0[0]), .SB(resetn));
DFQSM4NA  I671 ( .Q(net327), .CK(clk_up), .D(net544), .SB(resetn));
DFQSM4NA  I694 ( .Q(net331), .CK(clkout[23]), .D(ckdiv4[1]), .SB(pdb));
DFQSM4NA  I769 ( .Q(net335), .CK(clkout[3]), .D(ckdiv4[1]), .SB(pdb));
INVM2N  I78 ( .Z(ckdiv4a[24]), .A(net347));
INVM2N  I77 ( .Z(net341), .A(net349));
INVM2N  I76 ( .Z(net343), .A(net347));
INVM2N  I75 ( .Z(ckdiv4a[25]), .A(net349));
INVM2N  I74 ( .Z(net347), .A(clk_left));
INVM2N  I73 ( .Z(net349), .A(clk_left));
INVM2N  I72 ( .Z(net351), .A(net353));
INVM2N  I71 ( .Z(net353), .A(clk_left));
INVM2N  I70 ( .Z(ckdiv4a[26]), .A(net353));
INVM2N  I781 ( .Z(net357), .A(clk_right));
INVM2N  I733 ( .Z(net359), .A(net361));
INVM2N  I731 ( .Z(net361), .A(clk_left));
INVM2N  I783 ( .Z(net363), .A(net357));
INVM2N  I741 ( .Z(net365), .A(clk_left));
INVM2N  I736 ( .Z(net367), .A(clk_left));
INVM2N  I743 ( .Z(net369), .A(net365));
INVM2N  I727 ( .Z(ckdiv4a[17]), .A(net385));
INVM2N  I748 ( .Z(net373), .A(net469));
INVM2N  I706 ( .Z(net375), .A(clk_left));
INVM2N  I718 ( .Z(tx_ck_sync_1), .A(net393));
INVM2N  I758 ( .Z(ckdiv4a[0]), .A(net387));
INVM2N  I728 ( .Z(net381), .A(net385));
INVM2N  I703 ( .Z(ckdiv4a[22]), .A(net487));
INVM2N  I726 ( .Z(net385), .A(clk_left));
INVM2N  I756 ( .Z(net387), .A(clk_right));
INVM2N  I723 ( .Z(net389), .A(net397));
INVM2N  I771 ( .Z(net391), .A(clk_right));
INVM2N  I716 ( .Z(net393), .A(clk_left));
INVM2N  I713 ( .Z(ckdiv4a[20]), .A(net417));
INVM2N  I721 ( .Z(net397), .A(clk_left));
INVM2N  I708 ( .Z(net399), .A(net375));
INVM2N  I768 ( .Z(net401), .A(net433));
INVM2N  I808 ( .Z(net403), .A(net439));
INVM2N  I786 ( .Z(net405), .A(clk_right));
INVM2N  I717 ( .Z(ckdiv4a[19]), .A(net393));
INVM2N  I732 ( .Z(ckdiv4a[16]), .A(net361));
INVM2N  I702 ( .Z(net411), .A(net487));
INVM2N  I782 ( .Z(ckdiv4a[5]), .A(net357));
INVM2N  I742 ( .Z(ckdiv4a[14]), .A(net365));
INVM2N  I712 ( .Z(net417), .A(clk_left));
INVM2N  I757 ( .Z(net419), .A(net387));
INVM2N  I752 ( .Z(ckdiv4a[12]), .A(net497));
INVM2N  I767 ( .Z(ckdiv4a[2]), .A(net433));
INVM2N  I812 ( .Z(net425), .A(net465));
INVM2N  I802 ( .Z(net427), .A(net473));
INVM2N  I772 ( .Z(ckdiv4a[3]), .A(net391));
INVM2N  I797 ( .Z(net431), .A(net479));
INVM2N  I766 ( .Z(net433), .A(clk_right));
INVM2N  I707 ( .Z(ckdiv4a[21]), .A(net375));
INVM2N  I787 ( .Z(tx_ck_sync_0), .A(net405));
INVM2N  I806 ( .Z(net439), .A(clk_right));
INVM2N  I722 ( .Z(ckdiv4a[18]), .A(net397));
INVM2N  I747 ( .Z(ckdiv4a[13]), .A(net469));
INVM2N  I793 ( .Z(ckdiv4a[7]), .A(net449));
INVM2N  I792 ( .Z(net447), .A(net449));
INVM2N  I791 ( .Z(net449), .A(clk_right));
INVM2N  I778 ( .Z(net451), .A(net455));
INVM2N  I777 ( .Z(ckdiv4a[4]), .A(net455));
INVM2N  I776 ( .Z(net455), .A(clk_right));
INVM2N  I763 ( .Z(ckdiv4a[1]), .A(net461));
INVM2N  I762 ( .Z(net459), .A(net461));
INVM2N  I761 ( .Z(net461), .A(clk_right));
INVM2N  I737 ( .Z(ckdiv4a[15]), .A(net367));
INVM2N  I811 ( .Z(net465), .A(clk_right));
INVM2N  I773 ( .Z(net467), .A(net391));
INVM2N  I746 ( .Z(net469), .A(clk_left));
INVM2N  I692 ( .Z(net471), .A(net530));
INVM2N  I801 ( .Z(net473), .A(clk_right));
INVM2N  I711 ( .Z(net475), .A(net417));
INVM2N  I798 ( .Z(ckdiv4a[8]), .A(net479));
INVM2N  I796 ( .Z(net479), .A(clk_right));
INVM2N  I697 ( .Z(net481), .A(net503));
INVM2N  I807 ( .Z(ckdiv4a[10]), .A(net439));
INVM2N  I753 ( .Z(net485), .A(net497));
INVM2N  I701 ( .Z(net487), .A(clk_left));
INVM2N  I788 ( .Z(ckdiv4a[6]), .A(net405));
INVM2N  I813 ( .Z(ckdiv4a[11]), .A(net465));
INVM2N  I679 ( .Z(net493), .A(net527));
INVM2N  I677 ( .Z(net495), .A(qd1[0]));
INVM2N  I751 ( .Z(net497), .A(clk_left));
INVM2N  I738 ( .Z(net499), .A(net367));
INVM2N  I698 ( .Z(ckdiv4a[23]), .A(net503));
INVM2N  I696 ( .Z(net503), .A(clk_left));
INVM2N  I803 ( .Z(ckdiv4a[9]), .A(net473));
INVM2N  I689 ( .Z(net507), .A(qd1[1]));
INVM1N  I686 ( .Z(qd1[1]), .A(qb1[1]));
INVM1N  I687 ( .Z(qb0[1]), .A(net315));
INVM1N  I688 ( .Z(qd0[1]), .A(qb0[1]));
INVM1N  I672 ( .Z(qb1[0]), .A(net327));
INVM1N  I676 ( .Z(qd0[0]), .A(qb0[0]));
INVM1N  I685 ( .Z(qb1[1]), .A(net319));
INVM1N  I675 ( .Z(qb0[0]), .A(net323));
INVM1N  I673 ( .Z(qd1[0]), .A(qb1[0]));
ND2M2N  I681 ( .A(qd1[0]), .B(qd0[0]), .Z(net527));
ND2M2N  I691 ( .A(qd1[1]), .B(qd0[1]), .Z(net530));
INVM4N  I690 ( .Z(ckdiv4[1]), .A(net507));
INVM4N  I693 ( .Z(net533), .A(net471));
INVM4N  I678 ( .Z(ckdiv4[0]), .A(net495));
INVM4N  I680 ( .Z(net537), .A(net493));
XOR2M1NA  I682 ( .B(qd1[1]), .A(qd0[1]), .Z(net541));
XOR2M1NA  I670 ( .B(qd1[0]), .A(qd0[0]), .Z(net544));
CKINVM12N  I60 ( .Z(net635), .A(net737));
CKINVM12N  I59 ( .Z(clk_dn), .A(net635));
CKINVM12N  I5 ( .Z(net639), .A(net667));
CKINVM12N  I4 ( .Z(net641), .A(net667));
CKINVM12N  I7 ( .Z(net643), .A(net667));
CKINVM12N  I6 ( .Z(net645), .A(net667));
CKINVM12N  I8 ( .Z(ckout[26]), .A(net641));
CKINVM12N  I14 ( .Z(ckout[20]), .A(net643));
CKINVM12N  I15 ( .Z(ckout[19]), .A(net643));
CKINVM12N  I13 ( .Z(ckout[21]), .A(net645));
CKINVM12N  I12 ( .Z(ckout[22]), .A(net645));
CKINVM12N  I11 ( .Z(ckout[23]), .A(net639));
CKINVM12N  I2 ( .Z(net659), .A(net743));
CKINVM12N  I58 ( .Z(clk_up), .A(net669));
CKINVM12N  I10 ( .Z(ckout[24]), .A(net639));
CKINVM12N  I9 ( .Z(ckout[25]), .A(net641));
CKINVM12N  I3 ( .Z(net667), .A(net659));
CKINVM12N  I57 ( .Z(net669), .A(net737));
CKINVM12N  I33 ( .Z(net671), .A(net753));
CKINVM12N  I34 ( .Z(net673), .A(net671));
CKINVM12N  I35 ( .Z(net675), .A(net753));
CKINVM12N  I36 ( .Z(net677), .A(net675));
CKINVM12N  I46 ( .Z(ckout[4]), .A(net697));
CKINVM12N  I41 ( .Z(ckout[10]), .A(net689));
CKINVM12N  I40 ( .Z(ckout[11]), .A(net689));
CKINVM12N  I45 ( .Z(ckout[6]), .A(net715));
CKINVM12N  I43 ( .Z(ckout[9]), .A(net711));
CKINVM12N  I37 ( .Z(net689), .A(net673));
CKINVM12N  I47 ( .Z(ckout[5]), .A(net697));
CKINVM12N  I48 ( .Z(ckout[0]), .A(net707));
CKINVM12N  I49 ( .Z(ckout[3]), .A(net703));
CKINVM12N  I50 ( .Z(net697), .A(net677));
CKINVM12N  I51 ( .Z(ckout[2]), .A(net703));
CKINVM12N  I52 ( .Z(ckout[1]), .A(net707));
CKINVM12N  I53 ( .Z(net703), .A(net677));
CKINVM12N  I42 ( .Z(ckout[8]), .A(net711));
CKINVM12N  I54 ( .Z(net707), .A(net677));
CKINVM12N  I44 ( .Z(ckout[7]), .A(net715));
CKINVM12N  I38 ( .Z(net711), .A(net673));
CKINVM12N  I1 ( .Z(net713), .A(net737));
CKINVM12N  I39 ( .Z(net715), .A(net673));
CKINVM12N  I0 ( .Z(net717), .A(net737));
CKINVM12N  I16 ( .Z(ckout[12]), .A(net739));
CKINVM12N  I17 ( .Z(ckout[13]), .A(net739));
CKINVM12N  I18 ( .Z(ckout[14]), .A(net741));
CKINVM12N  I19 ( .Z(ckout[15]), .A(net741));
CKINVM12N  I20 ( .Z(ckout[16]), .A(net745));
CKINVM12N  I621 ( .Z(net729), .A(ck_k_div));
CKINVM12N  I21 ( .Z(ckout[17]), .A(net745));
CKINVM12N  I22 ( .Z(ckout[18]), .A(net747));
CKINVM12N  I23 ( .Z(net735), .A(net747));
CKINVM12N  I622 ( .Z(net737), .A(net729));
CKINVM12N  I24 ( .Z(net739), .A(net751));
CKINVM12N  I25 ( .Z(net741), .A(net751));
CKINVM12N  I623 ( .Z(net743), .A(net717));
CKINVM12N  I26 ( .Z(net745), .A(net751));
CKINVM12N  I27 ( .Z(net747), .A(net751));
CKINVM12N  I28 ( .Z(net749), .A(net743));
CKINVM12N  I29 ( .Z(net751), .A(net749));
CKINVM12N  I626 ( .Z(net753), .A(net713));

endmodule
