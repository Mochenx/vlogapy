module o_table_mem
    #(  parameter COLOR_DEPTH = 10,
        parameter TABLE_ENTRY_WIDTH = COLOR_DEPTH-1)
        (
        input                               pix_clk,
        input                               tab_init,
        input                               color_depth_8bit,
        input [1:0]                         dither_mode,
        input                               bist_clk               ,
        input                               bist_rstn              ,
        input                               bist_mode              ,
        input                               scan_mode              ,
        input                               iddq_mode              ,
        output                              bist_done              ,
        output                              bist_err               ,

        //IOs for ODC Boost lookup process
        //input                               lkup_table_en,
        input  [8*18-1:0]                       lkup_table_addr,
        //output reg [TABLE_ENTRY_WIDTH*18-1:0]   out_table_mem,
        //-------------------------------------------------------

        //IOs for o_reg operation
        input                               o_reg_sel,
        input                               o_reg_wr,
        input  [8:0]                        o_reg_op_addr,
        input  [7:0]                        o_reg_wr_data,
        output reg [7:0]                    table_mem_rd_data,
        output reg                          table_mem_rd_ok
    );
parameter PORT_A = 18;
parameter PORT_B = 17;
parameter MEM_WIDTH = TABLE_ENTRY_WIDTH-3;

wire [MEM_WIDTH *18 -1:0] mem_out;
reg [255:0] table_mem_lsb;

assign op_wr_reg = o_reg_sel & o_reg_wr & (o_reg_op_addr[8] == 1'b1);
assign op_wr_mem = o_reg_sel & o_reg_wr & (o_reg_op_addr[8] == 1'b0);
assign op_rd = o_reg_sel & ~o_reg_wr;

//write into
genvar gen_tab_loop;
generate
    for(gen_tab_loop = 0;gen_tab_loop<256;gen_tab_loop = gen_tab_loop+1) begin:TAB_LSB
    always @(posedge pix_clk) begin
        if(tab_init == 1'b1)
            table_mem_lsb[gen_tab_loop] <= 1'b0;
        else if((op_wr_reg == 1'b1) && (o_reg_op_addr[4:0] == gen_tab_loop/8))
            table_mem_lsb[gen_tab_loop] <= #1 o_reg_wr_data[7-gen_tab_loop%8];
        //In other conditions: HOLD
    end//EOA
end
endgenerate

//read out

reg  [8:0] o_reg_op_addr_dly;


always @(posedge pix_clk) begin
    table_mem_rd_ok <= op_rd;
    o_reg_op_addr_dly <= o_reg_op_addr;
end


always@(posedge pix_clk) begin
    if(table_mem_rd_ok)begin
        if(o_reg_op_addr_dly[8] == 1'b1)
            table_mem_rd_data <= {
                            table_mem_lsb[{o_reg_op_addr_dly[4:0],3'd0}],
                            //table_mem_lsb[{o_reg_op_addr_dly[4:0],3'd1}],
                            //table_mem_lsb[{o_reg_op_addr_dly[4:0],3'd2}],
                            //table_mem_lsb[{o_reg_op_addr_dly[4:0],3'd3}],
                            //table_mem_lsb[{o_reg_op_addr_dly[4:0],3'd4}],
                            //table_mem_lsb[{o_reg_op_addr_dly[4:0],3'd5}],
                            //table_mem_lsb[{o_reg_op_addr_dly[4:0],3'd6}],
                            table_mem_lsb[{o_reg_op_addr_dly[4:0],3'd7}]};
        else
            table_mem_rd_data <= mem_out[2*MEM_WIDTH -1 -:MEM_WIDTH];//11-3:8 Bit Width
     end
end


//--------------------------------------------------------------------------------//
// Instances of 9 X 256*8 RAM
//
reg [17:0] tab_lsb_dly;
wire [8*18 -1:0] dpram_addr;
wire [8:0] ram_bist_done;
wire [8:0] ram_bist_err ;

assign bist_done = &ram_bist_done;
assign bist_err = |ram_bist_err;

genvar g_inst_ram;
generate
    for(g_inst_ram = 0;g_inst_ram<9;g_inst_ram = g_inst_ram+1) begin:TAB_MEM
        //To synchronize with the output timing of RAM
        always @(posedge pix_clk) begin
            tab_lsb_dly[(PORT_A-2*g_inst_ram) -1] <= table_mem_lsb[lkup_table_addr[8*(PORT_A-2*g_inst_ram) -1 -:8]];
            tab_lsb_dly[(PORT_B-2*g_inst_ram) -1] <= table_mem_lsb[lkup_table_addr[8*(PORT_B-2*g_inst_ram) -1 -:8]];
        end
        //lkup_table_addr[8*(PORT_A-2*g_inst_ram) -1 -:8]
        //lkup_table_addr[8*(PORT_B-2*g_inst_ram) -1 -:8]

        //Bus Selection Starting Index:8*(18-i*2) -1
        always @(posedge pix_clk) begin
            //Port A
            out_table_mem[TABLE_ENTRY_WIDTH * (PORT_A-2*g_inst_ram) -1 -:TABLE_ENTRY_WIDTH] <=
                    {mem_out[MEM_WIDTH *(PORT_A-2*g_inst_ram) -1 -:MEM_WIDTH ], tab_lsb_dly[(PORT_A-2*g_inst_ram) -1],2'b0};
            //Port B
            out_table_mem[TABLE_ENTRY_WIDTH * (PORT_B-2*g_inst_ram) -1 -:TABLE_ENTRY_WIDTH] <=
                    {mem_out[MEM_WIDTH *(PORT_B-2*g_inst_ram) -1 -:MEM_WIDTH ], tab_lsb_dly[(PORT_B-2*g_inst_ram) -1],2'b0};
        end

        assign dpram_addr[8*(PORT_A-2*g_inst_ram) -1 -:8] = ((o_reg_sel)&&(o_reg_op_addr[8] == 1'b0))?o_reg_op_addr[7:0]:lkup_table_addr[8*(PORT_A-2*g_inst_ram) -1 -:8];

        dpsram_256x8_wrapper u_dpsram_256x8_wrapper (
            //output
            .bist_done(ram_bist_done[g_inst_ram]),
            .bist_err(ram_bist_err[g_inst_ram]),
            .ctr_douta(mem_out[MEM_WIDTH *(PORT_A-2*g_inst_ram) -1 -:MEM_WIDTH]),
            .ctr_doutb(mem_out[MEM_WIDTH *(PORT_B-2*g_inst_ram) -1 -:MEM_WIDTH]),

            //input
            .mclk(bist_clk),
            .rst_n(bist_rstn),

            .clka(pix_clk),
            .clkb(pix_clk),

            .bist_mode(bist_mode),
            .scan_mode(scan_mode),
            .iddq_mode(iddq_mode),

            .ctr_cena(1'b0),
            .ctr_oena(1'b0),
            .ctr_wena(~op_wr_mem),
            .ctr_ada(dpram_addr[8*(PORT_A-2*g_inst_ram) -1 -:8]),//Pay Attention Please !!!!!!
            .ctr_dina(o_reg_wr_data),

            .ctr_cenb(1'b0),
            .ctr_oenb(1'b0),
            .ctr_wenb(1'b1),
            .ctr_adb(lkup_table_addr[8*(PORT_B-2*g_inst_ram) -1 -:8]),
            .ctr_dinb(8'b0)
        );
    end
endgenerate
//
//--------------------------------------------------------------------------------//

endmodule
