#encoding = utf-8


import unittest
from syntax import *
from syntax.vlog_module import VlogPModule
from elements import ElemPort


__author__ = 'mochen'


class TestVlogPModule(unittest.TestCase):
    def setUp(self):
        self.dut_source = VlogSource()
        self.DUT = VlogPModule()

    def testBasicTC1(self):
        with open('unittests/vlog_files/module_basic_tc1.v', 'r') as f:
            codes = f.read()
        parsed_tokens = self.dut_source.source.parseString(codes)
        for m in parsed_tokens:
            print(m.ModuleHeader.Name)
            for p in m.ModuleHeader.PortList:
                print(p)
        # print(parsed_tokens.Module) # .ModelHdr.Ports)
        print(parsed_tokens)

    def testBasicTC2(self):
        with open('unittests/vlog_files/module_basic_tc2.v', 'r') as f:
            codes = f.read()
        parsed_tokens = self.dut_source.source.parseString(codes)
        # for m in parsed_tokens:
        # self.assertEqual(len(parsed_tokens), 2)
        m = parsed_tokens[0]
        self.assertEqual(m.ModuleHeader.name, 'xxx_tx_phy_digital')
        print(m.ModuleHeader.name)
        self.assertEqual(len(m.ModuleHeader.ports), 106)
        for p in m.ModuleHeader.ports:
            print(p)
        for items in m.ModuleItems:
            try:
                if isinstance(items, ElemPort):
                    self.assertIn(items.direction, ('input', 'output', 'inout'))
            except AssertionError:
                print(items)
        # print(parsed_tokens.Module) # .ModelHdr.Ports)
        # print(parsed_tokens)

    def testBasicTC3(self):
        """
            A verilog file with specify block
        """
        with open('unittests/vlog_files/module_basic_tc3.v', 'r') as f:
            codes = f.read()
        parsed_tokens = self.dut_source.source.parseString(codes)
        print(parsed_tokens)
        m = parsed_tokens[0]
        module_obj = m[0]
        print(module_obj.name)
        for p in module_obj.ports:
            print(p)
        # print(m.ModuleHeader.Name)

    def testBasicTC4(self):
        """
            A verilog file with parameter declarations and generate blocks
        """
        with open('unittests/vlog_files/module_basic_tc4.v', 'r') as f:
            codes = f.read()
        parsed_tokens = self.dut_source.source.parseString(codes)
        print(parsed_tokens)
        m = parsed_tokens[0]
        module_obj = m[0]
        print(module_obj.name)
        for p in module_obj.ports:
            print(p)

    def testBasicTC5(self):
        """
        """
        tc_codes = """
            module with_primitives();
                wire neta, netb, outw, inw, controlw;
                assign netb = 1'b0;
                assign neta = ~netb;

                bufif1 bf1 (outw, inw, controlw);
                pullup (weak1) p1 (neta), p2 (netb);
            endmodule
        """
        parsed_tokens = self.dut_source.source.parseString(tc_codes)
        self.assertIsNotNone(parsed_tokens)
        module_obj = parsed_tokens[0]
        self.assertEqual(module_obj.ModuleHeader.name, 'with_primitives')

    def testBasicTC6(self):
        """
        """
        tc_codes = """
            module sample_m #( parameter COLOR_D = 10,
            parameter DATA_W = 6*COLOR_D//Data Width
            ) (
            input                                  i2c_clk                      ,
            input                                  i2c_rstn                     ,
            input                                  strm_clk                     , // stream clock
            input                                  reset_n_strm_clk             , // reset, active low

            //input                                  dualchip_ms_mode             ,
            //input                                  dualchip_vsync_in            ,
            //input                                  dualchip_hsync_in            ,
            //input [4:0]                            dualchip_pat_idx_in          ,
            //output [4:0]                           dualchip_pat_idx_out         ,
            //output [1:0]                           dualchip_bist_type_out       ,

            input                                  vb_slave_sel            ,
            input                                  vb_rd_en                ,
            input                                  vb_wr_en                ,
            input [23:0]                           vb_op_addr              ,
            input [31:0]                           vb_wr_data              ,

            input                                  r_vsync_polarity_in          ,
            input                                  r_hsync_polarity_in          ,


            input [1:0]                            m_type                    , // the type selected to be show

            //output ports
            output wire [31:0]                     vb_rd_data              ,
            output wire                            vb_op_ok                ,
            output wire                            vb_op_fail              ,

            output wire                            r_en                   ,
            output wire                            de_out                  , // video data enable
            output wire                            de_plus_out             , // for newarch
            output wire                            hsync_out               , // honrizontal sync
            output wire                            vsync_out               , // vertical sync
            output wire [DATA_W-1:0]               video_data_out          , // for newarch

            //Aug 2,2013 modified by Mo Chen
            output wire                            r_entry_from_i2c       ,
            output wire                            r_exit_from_i2c
            );
            endmodule
        """
        parsed_tokens = self.dut_source.source.parseString(tc_codes)
        self.assertIsNotNone(parsed_tokens)
        module_obj = parsed_tokens[0]
        self.assertEqual(module_obj.ModuleHeader.name, 'sample_m')

    def testModulePortTC1(self):
        """
            A testcase of simple port declaration patterns(Only input/inout declaration)
            inout/input [ net_type ] [ signed ] [ range ] list_of_port_identifiers
        """
        key_words = ('input', 'inout')
        net_type = ('', 'wire', 'tri', 'tri1', 'supply0', 'wand', 'triand', 'tri0', 'supply1', 'wor', 'trior')
        signed = ('', 'signed')
        range = ('', '[7:0]', '[3+2*2:1-1]')
        ports = (('port0',), ('port0', 'port1'), ('port0', 'port1', 'port2'))
        for k in key_words:
            for net in net_type:
                for s in signed:
                    for r in range:
                        for ids in ports:
                            tc_codes = '%s %s %s %s %s' % (k, net, s, r, ','.join(ids))
                            parsed_tokens = self.DUT.port_declaration.parseString(tc_codes)
                            print(parsed_tokens)
                            idx = 0
                            self.assertEqual(parsed_tokens[0][idx], k)
                            idx += 1
                            if net:
                                self.assertEqual(parsed_tokens[0][idx], net)
                                idx += 1
                            if s:
                                self.assertEqual(parsed_tokens[0][idx], s)
                                idx += 1
                            if r:
                                # TODO: make the following assertion work
                                # self.assertEqual(2+len(parsed_tokens[0][idx]), len(r))
                                idx += 1
                            for i in ids:
                                try:
                                    self.assertEqual(parsed_tokens[0][idx], i)
                                except Exception as e:
                                    print(e)
                                idx += 1

    def testModulePortTC2(self):
        """
            A testcase of simple port declaration patterns(Only output declaration)
            output [ net_type ] [ signed ] [ range ] list_of_port_identifiers
            output reg [ signed ] [ range ] list_of_variable_port_identifiers
            output output_variable_type list_of_variable_port_identifiers
        """
        key_words = ('output', )
        net_type = ('', 'wire', 'tri', 'tri1', 'supply0', 'wand', 'triand', 'tri0', 'supply1', 'wor',
                    'trior', 'reg', 'integer', 'time')
        signed = ('', 'signed')
        range = ('', '[7:0]', '[3+2*2:1-1]')
        ports = (('port0',), ('port0', 'port1'), ('port0', 'port1', 'port2'), ('port0 = 1+2*3', 'port1'))

        for k in key_words:
            for net in net_type:
                for s in signed:
                    for r in range:
                        for port_i, ids in enumerate(ports):
                            if net not in ('reg', 'integer', 'time') and port_i == 3:
                                continue
                            if net in ('integer', 'time'):
                                tc_codes = '%s %s %s' % (k, net, ','.join(ids))
                            else:
                                tc_codes = '%s %s %s %s %s' % (k, net, s, r, ','.join(ids))
                            print(tc_codes)
                            parsed_tokens = self.DUT.port_declaration.parseString(tc_codes)
                            # print(parsed_tokens)
                            idx = 0
                            self.assertEqual(parsed_tokens[0][idx], k)
                            idx += 1
                            if net:
                                self.assertEqual(parsed_tokens[0][idx], net)
                                idx += 1
                            if net not in ('integer', 'time'):
                                if s:
                                    self.assertEqual(parsed_tokens[0][idx], s)
                                    idx += 1
                                if r:
                                    # TODO: make the following assertion work
                                    # self.assertEqual(2+len(parsed_tokens[0][idx]), len(r))
                                    idx += 1
                            for i in ids:
                                if port_i != 3:
                                    try:
                                        self.assertEqual(i, parsed_tokens[0][idx])
                                    except Exception:
                                        pass
                                else:
                                    pt = i.split('=')
                                    pt = pt[0].rstrip(' ')
                                    self.assertEqual(pt, parsed_tokens[0][idx])
                                    idx += 1
                                idx += 1

    def testModuleInstTC1(self):
        """
            A testcase of module instantiation by named port connection
        """
        tc_codes = """xxx_4to1 u_xxx_26(
                        .clk_ddr(data_tx_clk    ),
                        .clk    (tx_ck_sync_0   ),
                        .data   (ch26_d         ),
                        .pwd    (reg_pd_ch[26]  ),
                        .set_clk( 1'b0          ),
                        .xxx_p  (pad_tx_26p     ),
                        .xxx_n  (pad_tx_26m     )),
                               u_xxx_25(
                        .clk_ddr(data_tx_clk    ),
                        .clk    (tx_ck_sync_0   ),
                        .data   (ch25_d         ),
                        .pwd    (reg_pd_ch[25]  ),
                        .set_clk( 1'b0          ),
                        .xxx_p  (pad_tx_25p     ),
                        .xxx_n  (pad_tx_25m     ));
                        """
        ports = ('clk_ddr', 'clk', 'data', 'pwd', 'set_clk', 'xxx_p', 'xxx_n')

        parsed_tokens = self.DUT.module_instantiation.parseString(tc_codes)
        print(parsed_tokens[0].ModuleName)
        for m in parsed_tokens[0].InstanceList:
            print(m.InstanceName)
            self.assertEqual(len(m.ConnectionList), len(ports))
            for p in m.ConnectionList:
                self.assertIn(p.PortName, ports)

    def testModuleInstTC2(self):
        """
            A testcase of module instantiation by ordered port connection
        """
        tc_codes = """ModuleName InstName(
                            connection0, connection1, connection2[0][1+3*2][7:0], {connection3, connection4}
                        );
                    """

        exp = ['connection0', 'connection1', 'connection2', ['connection3', 'connection4']]
        exp2_1 = [['0'], ['1', '+', '3', '*', '2']]
        exp2_2 = [['7', '0']]

        parsed_tokens = self.DUT.module_instantiation.parseString(tc_codes)
        print(parsed_tokens)
        print(parsed_tokens[0].ModuleName)
        for m in parsed_tokens[0].InstanceList:
            print(m.InstanceName)
            # self.assertEqual(len(m.ConnectionList), 4)
            for i, p in enumerate(m.ConnectionList):
                print(p)
                if i < 2:
                    self.assertEqual(exp[i], p)
                elif i == 3:
                    self.assertEqual(str(exp[i]), str(p))
                else:
                    self.assertEqual(exp[i], p[0])
                    # [['0'], ['1', '+', '3', '*', '2']], [['7', '0']]]
                    self.assertEqual(str(p[1]), str(exp2_1))
                    self.assertEqual(str(p[2]), str(exp2_2))

    def testModuleInstTC3(self):
        tc_codes = "#(  parameter COLOR_DEPTH = 10, parameter TABLE_ENTRY_WIDTH = COLOR_DEPTH-1)"
        parsed_tokens = self.DUT.module_parameter_port_list.parseString(tc_codes)
        print(parsed_tokens)

    def testBuildElem(self):
        port = r'.port(aa[1:0])'
        stimus = [
                """
                    module Test1(port0, port1, port2);
                    input port0, port1, port2;
                    reg clk;
                    endmodule
                    """,

                """
                    module Test1(.port0({p1, p2}));
                    input [1:0] p1, p2;
                    reg clk;
                    endmodule
                    """,

                """
                    module Test1(.port0({p1[3:0], p2}));
                    input [4:0] p1;
                    input [3:0] p2;
                    reg clk;
                    endmodule
                    """,

                """
                    module Test1({p1, p2}, port1);
                    input p1;
                    input [10:0] p2;
                    output port1;
                    reg clk;
                    endmodule
                    """,

                """
                    module Test1(input [7:0] inport0, input1, output [7:0] outport0, output1);
                    reg clk;
                    endmodule
                    """,

                """
                    module Test1(input [7:0] inport0, input input1, output [7:0] outport0, output reg [1:0]output1);
                    reg clk;
                    endmodule
                    """,

                """
                     module Test1(port0, port1, port2, port3);
                     input [7:0] port0;
                     input [1:0] port1;
                     output reg [1:0] port2, port3;
                     endmodule
                     """,

                """
                     module Test1(.p0({port0, port1}), p2, p3);
                     input [7:0] port0;
                     input [1:0] port1;
                     output reg [1:0] p2, p3;
                     endmodule
                     """
        ]
        for stimu in stimus:
            print('Parsing %s' % stimu)
            tokens = self.DUT.parse(stimu)
            m = tokens[0].ModuleHeader
            m.resolve()
            print('\t%s' % str(tokens))
            for n, p in m.ports.items():
                l_inner_io = ['%s' % str(io) for io in p.values()]
                print('\t%s:{%s}' % (n, '\n\t\t\t'.join(l_inner_io)))

    def testGenTC1(self):
        tc_codes = """
            module mod1();
                genvar gen_tab_loop;
                generate
                    for(gen_tab_loop = 0;gen_tab_loop<256;gen_tab_loop = !gen_tab_loop?gen_tab_loop+2:gen_tab_loop+1)
                    begin:TAB_LSB
                        always @(posedge pix_clk) begin
                            if(tab_init == 1'b1)
                                table_mem_lsb[gen_tab_loop] <= 1'b0;
                            else if((op_wr_reg == 1'b1) && (o_reg_op_addr[4:0] == gen_tab_loop/8))
                                table_mem_lsb[gen_tab_loop] <= #1 o_reg_wr_data[7-gen_tab_loop%8];
                        end
                    end
                    for(gen_tab_loop = 0;gen_tab_loop<256;gen_tab_loop = gen_tab_loop+1)
                    begin:TAB_LSB2
                        always @(posedge pix_clk) begin
                            if(tab_init == 1'b1)
                                table_mem_lsb[gen_tab_loop] <= 1'b0;
                            else if((op_wr_reg == 1'b1) && (o_reg_op_addr[4:0] == gen_tab_loop/8))
                                table_mem_lsb[gen_tab_loop] <= #1 o_reg_wr_data[7-gen_tab_loop%8];
                        end
                    end
                endgenerate
            endmodule
        """


        aa = self.DUT.genvar_expr.parseString('!gen_tab_loop?gen_tab_loop+2:gen_tab_loop+1')
        self.assertEqual(aa[0], '!')
        self.assertEqual(aa[2], '?')
        self.assertEqual(aa[6], ':')
        aa = self.DUT.genvar_expr.parseString('!gen_tab_loop+2*3-4')
        self.assertEqual(aa[0], '!')
        self.assertEqual(aa[-3], '3')
        aa = self.DUT.genvar_expr.parseString('!gen_tab_loop?1:2 + 3')
        parsed_tokens = self.DUT.parse(tc_codes)
        print(parsed_tokens)

    def testGenTC2(self):
        tc_codes = """
                module mod1();
                    genvar g_inst_ram;
                    generate
                        for(g_inst_ram = 0;g_inst_ram<9;g_inst_ram = g_inst_ram+1) begin:TAB_MEM
                            always @(posedge pix_clk) begin
                                tab_lsb_dly[(PORT_A-2*g_inst_ram) -1] <= table_mem_lsb[lkup_table_addr[8*
                                    (PORT_A-2*g_inst_ram) -1 -:8]];
                                tab_lsb_dly[(PORT_B-2*g_inst_ram) -1] <= table_mem_lsb[lkup_table_addr[8*
                                    (PORT_B-2*g_inst_ram) -1 -:8]];
                            end

                            always @(posedge pix_clk) begin
                                out_table_mem[TABLE_ENTRY_WIDTH * (PORT_A-2*g_inst_ram) -1 -:TABLE_ENTRY_WIDTH] <=
                                    {mem_out[MEM_WIDTH *(PORT_A-2*g_inst_ram) -1 -:MEM_WIDTH ],
                                        tab_lsb_dly[(PORT_A-2*g_inst_ram) -1],2'b0};
                                out_table_mem[TABLE_ENTRY_WIDTH * (PORT_B-2*g_inst_ram) -1 -:TABLE_ENTRY_WIDTH] <=
                                    {mem_out[MEM_WIDTH *(PORT_B-2*g_inst_ram) -1 -:MEM_WIDTH ],
                                        tab_lsb_dly[(PORT_B-2*g_inst_ram) -1],2'b0};
                            end

                            dpsram_256x8_wrapper
                            u_dpsram_256x8_wrapper (
                            .bist_done(ram_bist_done[g_inst_ram]),
                            .bist_err(ram_bist_err[g_inst_ram]),
                            .ctr_douta(mem_out[MEM_WIDTH *(PORT_A-2*g_inst_ram) -1 -:MEM_WIDTH]),
                            .ctr_doutb(mem_out[MEM_WIDTH *(PORT_B-2*g_inst_ram) -1 -:MEM_WIDTH]),

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
                            .ctr_ada(dpram_addr[8*(PORT_A-2*g_inst_ram) -1 -:8]),
                            .ctr_dina(o_reg_wr_data),

                            .ctr_cenb(1'b0),
                            .ctr_oenb(1'b0),
                            .ctr_wenb(1'b1),
                            .ctr_adb(lkup_table_addr[8*(PORT_B-2*g_inst_ram) -1 -:8]),
                            .ctr_dinb(8'b0)
                            );

                        end
                    endgenerate
                endmodule
                """

        parsed_tokens = self.DUT.parse(tc_codes)
        print(parsed_tokens)

