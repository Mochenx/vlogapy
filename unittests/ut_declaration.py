#encoding = utf-8


import unittest
from parser.vlog_stmt import VlogStmt
from parser.vlog_declaration import VlogDeclaration
from pyparsing import cStyleComment, cppStyleComment


__author__ = 'mochen'


class TestVlogStmt(unittest.TestCase):
    def setUp(self):
        self.DUT = VlogDeclaration(statement=VlogStmt())

    def testRegDecl(self):
        key_words = ('reg', )
        signed = ('', 'signed')
        range = ('', '[7:0]', '[6*6:5*6+1]')
        names = (('var0',), ('var0', 'var1'), ('var0', 'var1', 'var2'), ('var0[7:0]', 'var1', 'var2 = 1+2*3'))
        name_idx_map = {3: (('[', 0), ('[', 2), ('=', 3))}

        for k in key_words:
            for s in signed:
                for r in range:
                    for j, n in enumerate(names):
                        tc_codes = '%s %s %s %s;' % (k, s, r, ','.join(n))
                        print(tc_codes)
                        parsed_tokens = self.DUT.reg_declaration.parseString(tc_codes)
                        # print(parsed_tokens)
                        idx = 0
                        self.assertEqual(k, parsed_tokens[0][idx])
                        idx += 1
                        if s:
                            self.assertEqual(s, parsed_tokens[0][idx])
                            idx += 1
                        if r:
                            # self.assertEqual(len(r), 2+len(parsed_tokens[0][idx]))
                            idx += 1
                        for i, name in enumerate(n):
                            if j in name_idx_map.keys():
                                name = name.split(name_idx_map[j][i][0])
                                name = name[0].rstrip(' ')
                                self.assertEqual(name, parsed_tokens[0][idx][name_idx_map[j][i][1]])
                                print(parsed_tokens)
                            else:
                                self.assertEqual(name, parsed_tokens[0][idx][i])

    def testNetDecl(self):
        key_words = ('wire', 'tri', 'tri1', 'supply0', 'wand', 'triand', 'tri0', 'supply1', 'wor', 'trior', 'trireg')
        signed = ('', 'signed')
        range = ('', '[7:0]', '[6*6:5*6+1]')
        delay = ('', '#100', '#U_DLY')
        names = (('var0',), ('var0', 'var1'), ('var0', 'var1', 'var2'), ("var0 = 'h1_23",), ('var2 = 1+2*3',))
        name_idx_map = {3: (('=', 0),), 4: (('=', 0), )}

        for k in key_words:
            for s in signed:
                for r in range:
                    for d in delay:
                        for j, n in enumerate(names):
                            tc_codes = '%s %s %s %s %s;' % (k, s, r, d, ','.join(n))
                            print(tc_codes)
                            parsed_tokens = self.DUT.net_declaration.parseString(tc_codes)
                            print(parsed_tokens)
                            idx = 0
                            self.assertEqual(k, parsed_tokens[0][idx])
                            idx += 1
                            if s:
                                self.assertEqual(s, parsed_tokens[0][idx])
                                idx += 1
                            if r:
                                # self.assertEqual(len(r), 2+len(parsed_tokens[0][idx]))
                                idx += 1
                            if d:
                                self.assertEqual(d, '#'+parsed_tokens[0][idx][0])
                                idx += 1
                            for i, name in enumerate(n):
                                if j in name_idx_map.keys():
                                    name = name.split(name_idx_map[j][i][0])
                                    name = name[0].rstrip(' ')
                                    self.assertEqual(name, parsed_tokens[0][idx][name_idx_map[j][i][1]])
                                    print(parsed_tokens)
                                else:
                                    self.assertEqual(name, parsed_tokens[0][idx][i])

    def testFuncDeclTC1(self):
        """
            Testing the first branch in BNF of function declaration
        """
        auto = ['', 'automatic']
        _type = ['[15:0] ', 'signed [15:0]', 'integer', 'real', 'realtime', 'time']
        tc_codes = """
        function %s %s nextCRC16_D8 ;
            input [7:0] Data           ;
            input [15:0] crc           ;
            reg [7:0] d                ;
            reg [15:0] c               ;
            reg [15:0] newcrc          ;
            begin
                d = Data                 ;
                c = crc                  ;
                newcrc[0] = d[4] ^ d[0] ^ c[8] ^ c[12];
                newcrc[1] = d[5] ^ d[1] ^ c[9] ^ c[13];
                newcrc[2] = d[6] ^ d[2] ^ c[10] ^ c[14];
                newcrc[3] = d[7] ^ d[3] ^ c[11] ^ c[15];
                newcrc[4] = d[4] ^ c[12];
                newcrc[5] = d[5] ^ d[4] ^ d[0] ^ c[8] ^ c[12] ^ c[13];
                newcrc[6] = d[6] ^ d[5] ^ d[1] ^ c[9] ^ c[13] ^ c[14];
                newcrc[7] = d[7] ^ d[6] ^ d[2] ^ c[10] ^ c[14] ^ c[15];
                newcrc[8] = d[7] ^ d[3] ^ c[0] ^ c[11] ^ c[15];
                newcrc[9] = d[4] ^ c[1] ^ c[12];
                newcrc[10] = d[5] ^ c[2] ^ c[13];
                newcrc[11] = d[6] ^ c[3] ^ c[14];
                newcrc[12] = d[7] ^ d[4] ^ d[0] ^ c[4] ^ c[8] ^ c[12] ^ c[15];
                newcrc[13] = d[5] ^ d[1] ^ c[5] ^ c[9] ^ c[13];
                newcrc[14] = d[6] ^ d[2] ^ c[6] ^ c[10] ^ c[14];
                newcrc[15] = d[7] ^ d[3] ^ c[7] ^ c[11] ^ c[15];
                nextCRC16_D8 = newcrc;
            end
        endfunction
        """
        for a in auto:
            for t in _type:
                parsed_tokens = self.DUT.function_declaration.parseString(tc_codes % (a, t))
                print('parsing %s %s' % (a, t))
                self.assertEqual('nextCRC16_D8', parsed_tokens.FuncName)
                self.assertEqual('nextCRC16_D8', parsed_tokens[-2][-2][-1][0])
                self.assertEqual('newcrc', parsed_tokens[-2][-2][-1][-1])
                self.assertEqual('endfunction', parsed_tokens[-1])
        # print(parsed_tokens)

    def testFuncDeclTC2(self):
        """
            Testing the second branch in BNF of function declaration
        """
        auto = ['', 'automatic']
        _type = ['[15:0] ', 'signed [15:0]', 'integer', 'real', 'realtime', 'time']
        tc_codes = """
        function %s %s nextCRC16_D8(input [7:0] Data, input [15:0] crc, dummy_arg);
            reg [7:0] d                ;
            reg [15:0] c               ;
            reg [15:0] newcrc          ;
            begin
                d = Data                 ;
                c = crc                  ;
                newcrc[0] = d[4] ^ d[0] ^ c[8] ^ c[12];
                newcrc[1] = d[5] ^ d[1] ^ c[9] ^ c[13];
                newcrc[2] = d[6] ^ d[2] ^ c[10] ^ c[14];
                newcrc[3] = d[7] ^ d[3] ^ c[11] ^ c[15];
                newcrc[4] = d[4] ^ c[12];
                newcrc[5] = d[5] ^ d[4] ^ d[0] ^ c[8] ^ c[12] ^ c[13];
                newcrc[6] = d[6] ^ d[5] ^ d[1] ^ c[9] ^ c[13] ^ c[14];
                newcrc[7] = d[7] ^ d[6] ^ d[2] ^ c[10] ^ c[14] ^ c[15];
                newcrc[8] = d[7] ^ d[3] ^ c[0] ^ c[11] ^ c[15];
                newcrc[9] = d[4] ^ c[1] ^ c[12];
                newcrc[10] = d[5] ^ c[2] ^ c[13];
                newcrc[11] = d[6] ^ c[3] ^ c[14];
                newcrc[12] = d[7] ^ d[4] ^ d[0] ^ c[4] ^ c[8] ^ c[12] ^ c[15];
                newcrc[13] = d[5] ^ d[1] ^ c[5] ^ c[9] ^ c[13];
                newcrc[14] = d[6] ^ d[2] ^ c[6] ^ c[10] ^ c[14];
                newcrc[15] = d[7] ^ d[3] ^ c[7] ^ c[11] ^ c[15];
                nextCRC16_D8 = newcrc;
            end
        endfunction
        """
        for a in auto:
            for t in _type:
                parsed_tokens = self.DUT.function_declaration.parseString(tc_codes % (a, t))
                print('parsing %s %s' % (a, t))
                self.assertEqual('nextCRC16_D8', parsed_tokens.FuncName)
                self.assertEqual('nextCRC16_D8', parsed_tokens[-2][-2][-1][0])
                self.assertEqual('newcrc', parsed_tokens[-2][-2][-1][-1])
                self.assertEqual('endfunction', parsed_tokens[-1])
                # print(parsed_tokens)

    def testTaskDeclTC1(self):
        """
            Testing the first branch in BNF of task declaration
        """
        tc_codes = """
                    task Get_a_Byte;
                      begin
                        NO_ACK_flag = 0;
                        shift_in = 1;
                        repeat (8) begin
                          @ (posedge SCL);
                        end
                      end
                    endtask
                """
        parsed_tokens = self.DUT.task_declaration.parseString(tc_codes)
        print(parsed_tokens)

    def testTaskDeclTC2(self):
        """
            Testing the first branch in BNF of task declaration
        """
        tc_codes = """
                    task Parse_the_Address_Byte_and_Read_or_Write_if_Valid;
                    begin
                        @ (negedge SCL)
                        shift_in = 0;
                        NO_ACK_flag = 0;
                        Check_for_Valid_Address;
                        if (Valid_Address_flag) begin:  Got_Address_Match
                        end // Got_Address_Match
                        if (VERBOSE) $display ("Address_Match");
                        case (S_Byte_Shft_Reg[0]) 	// LSB = 1 for write, 0 for read
                            0: Write_or_Dummy_Write_with_Random_Read;
                            1: Current_Address_and_Sequential_Read;
                            default: if (VERBOSE) $display("Invalid device address");
                        endcase
                    end
                    endtask
                """
        self.DUT.task_declaration.ignore(cStyleComment)
        self.DUT.task_declaration.ignore(cppStyleComment)
        parsed_tokens = self.DUT.task_declaration.parseString(tc_codes)
        print(parsed_tokens)

    def testParamDecl(self):
        key_words = ('parameter', 'localparam')
        signed = ('', 'signed')
        range = ('', '[7:0]', '[6*6:5*6+1]')
        signed_range_types = ['%s %s' % (s, r) for s in signed for r in range]
        signed_range_types.extend(['integer', 'time', 'real', 'realtime'])
        names = ("var0 = 'h1_23", 'var2 = 1+2*3')

        for k in key_words:
            for sr in signed_range_types:
                for n in names:
                    tc_codes = '%s %s %s;' % (k, sr, n)
                    print('Verifying %s' % tc_codes)
                    parsed_tokens = self.DUT.block_item_declaration.parseString(tc_codes)
                    try:
                        self.assertEqual(parsed_tokens[0], k)
                    except Exception:
                        print(parsed_tokens)
