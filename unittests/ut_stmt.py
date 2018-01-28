#encoding = utf-8


import unittest
from parser.vlog_stmt import VlogStmt


__author__ = 'mochen'


class TestVlogStmt(unittest.TestCase):
    def setUp(self):
        self.DUT = VlogStmt()

    def get_eq(self, i, v):
        return lambda e: self.assertEqual(e[i], v)

    def get_nest_eq(self, v, *args):
        def _chk(e):
            nxt_layer = e
            for i in args:
                nxt_layer = nxt_layer[i]
            try:
                self.assertEqual(nxt_layer, v)
            except Exception:
                raise
            return True
        return _chk

    def testCondStmtTC1(self):
        """
            4 tests of the following patterns:
                if ...
                if ... else ...
                if ... else if ...
                if ... else if ... else ...
                if ... else if ... else if ... else ...
        """
        if_stmt = '''if((1+2)*3 > 100) begin
                         a = 1+2*3/4-5;
                         b = 'h1234_5678_9ABC_DEF;
                     end
                  '''
        else_if_stmt = """else if(1'h1) begin\nk = 4'hF + 100;\nend\n"""
        else_stmt = """else begin\nc = 12'hA5A5_A5A5_A5A5;\nend\n"""
        if_else_stmt = u'{0}\n{1}'.format(if_stmt, else_stmt)
        if_only_elseif_stmt = u'{0}\n{1}'.format(if_stmt, else_if_stmt)
        if_elseif_stmt = u'{0}\n{1}\n{2}'.format(if_stmt, else_if_stmt, else_stmt)
        if_2elseif_stmt = u'{0}\n{1}\n{2}\n{3}'.format(if_stmt, else_if_stmt, else_if_stmt, else_stmt)


        def chk_if(stmts):
            self.assertEqual(len(stmts), 2)
            self.assertEqual(stmts[0][0], 'a')
            self.assertEqual(len(stmts[0]), 11)
            self.assertEqual(stmts[1][0], 'b')
            self.assertEqual(len(stmts[1]), 3)
        def chk_elif(stmts, n=1):
            self.assertEqual(len(stmts), n)
            for s in stmts:
                stmt = s.ElseIfStatement.StatementList
                self.assertEqual(len(stmt), 1)
                self.assertEqual(stmt[0][0], 'k')
                self.assertEqual(len(stmt[0]), 5)

        def chk_else(stmts):
            self.assertEqual(len(stmts), 1)
            self.assertEqual(stmts[0][0], 'c')
            self.assertEqual(len(stmts[0]), 3)

        print('Testing if ...')
        parsed_tkns = self.DUT.conditional_statement.parseString(if_stmt)
        print(parsed_tkns)
        chk_if(parsed_tkns[0].IfStatement.StatementList)

        print('Testing if ... else ...')
        parsed_tkns = self.DUT.conditional_statement.parseString(if_else_stmt)
        print(parsed_tkns)
        chk_if(parsed_tkns[0].IfStatement.StatementList)
        chk_else(parsed_tkns[0].ElseStatement.StatementList)


        print('Testing if ... else if ... ')
        parsed_tkns = self.DUT.conditional_statement.parseString(if_only_elseif_stmt)
        print(parsed_tkns)
        chk_if(parsed_tkns[0].IfStatement.StatementList)
        chk_elif(parsed_tkns[0].ElseIfStatementList)

        print('Testing if ... else if ... else ...')
        parsed_tkns = self.DUT.conditional_statement.parseString(if_elseif_stmt)
        print(parsed_tkns)
        chk_if(parsed_tkns[0].IfStatement.StatementList)
        chk_elif(parsed_tkns[0].ElseIfStatementList)
        chk_else(parsed_tkns[0].ElseStatement.StatementList)

        print('Testing if ... else if ... else if ... else ...')
        parsed_tkns = self.DUT.conditional_statement.parseString(if_2elseif_stmt)
        print(parsed_tkns)
        chk_if(parsed_tkns[0].IfStatement.StatementList)
        chk_elif(parsed_tkns[0].ElseIfStatementList, 2)
        chk_else(parsed_tkns[0].ElseStatement.StatementList)

    def testCondStmtTC2(self):
        """
            Nested if ... else if ... else ... relationship
            Test1: if ...
                        if ...
            Test2: if ... begin
                        if ...
                        else ...
                   end
            Test3: if ...
                   else begin
                        if ...
                        else ...
                   end
        """

        if_if_stmt ='if((1+2)*3 > 100) begin\n if((1+2)*3 > 100) a = 1;\nend'
        if_if_else_stmt ='if((1+2)*3 > 100) begin\n if((1+2)*3 > 100) a = 1;else b = 2;\nend'
        if_else_if_else_stmt ='if((1+2)*3 > 100) a = 1;else begin\n if((1+2)*3 > 100) b = 1;else c = 2;\nend'

        print('Testing if ... if ... ')
        parsed_tkns = self.DUT.conditional_statement.parseString(if_if_stmt)
        print(parsed_tkns)
        inner_if = parsed_tkns[0].IfStatement.StatementList
        inner_if_stmts = inner_if[0].IfStatement
        self.assertEqual(inner_if_stmts[0], 'a')
        self.assertEqual(len(inner_if_stmts), 3)

        print('Testing if ... if ... else ...')
        parsed_tkns = self.DUT.conditional_statement.parseString(if_if_else_stmt)
        print(parsed_tkns)
        inner_if = parsed_tkns[0].IfStatement.StatementList
        inner_if_stmts = inner_if[0].IfStatement
        inner_else_stmts = inner_if[0].ElseStatement
        self.assertEqual(inner_if_stmts[0], 'a')
        self.assertEqual(len(inner_if_stmts), 3)
        self.assertEqual(inner_else_stmts[0], 'b')
        self.assertEqual(len(inner_else_stmts), 3)

        print('Testing if ... else ... if ... else ...')
        parsed_tkns = self.DUT.conditional_statement.parseString(if_else_if_else_stmt)
        print(parsed_tkns)

        # Checking if
        self.assertEqual(parsed_tkns[0].IfStatement[0], 'a')
        self.assertEqual(len(parsed_tkns[0].IfStatement), 3)

        # Checking else begin if
        inner_if = parsed_tkns[0].ElseStatement.StatementList
        inner_if_stmts = inner_if[0].IfStatement
        inner_else_stmts = inner_if[0].ElseStatement
        self.assertEqual(inner_if_stmts[0], 'b')
        self.assertEqual(len(inner_if_stmts), 3)
        self.assertEqual(inner_else_stmts[0], 'c')
        self.assertEqual(len(inner_else_stmts), 3)

    def testLoopTC1(self):
        """
            A simple testcase for testing
                forever/while/repeat/for
                    b <= 1 + 1;
                    or
                forever/while/repeat/for begin
                    a = 2 + 1;
                    b <= 3 + 1;
                end
        """
        keywords = (('forever', ''), ('while', '(2 > 1)'),
                    ('repeat', '( (1 + 2) > 3)'), ('for', '(a = 0; 1 < 100; a = 1 + 101)'))
        stmts = (('b <= 1 + 1;', lambda e: self.assertEqual(e[0], 'b')),
                 ('begin a = 2 + 1; b <= 3 + 1;end',
                  lambda e: self.assertEqual(e.StatementList[0][0], 'a') and
                            self.assertEqual(e.StatementList[1][0], 'b')))

        for kw, expr in keywords:
            for stmt, chk_f in stmts:
                tc_codes = '%s %s %s' % (kw, expr, stmt)
                print('Testing : %s' % tc_codes)
                parsed_tkns = self.DUT.loop_statement.parseString(tc_codes)
                chk_f(parsed_tkns[0].Body)
                print(parsed_tkns)

    def testLoopTC2(self):
        """
            A testcase of combining loop with simple if statement
                forever/while/repeat/for
                    if ...
                    else ...
                Or
                forever/while/repeat/for begin
                    if  ...
                    blk_assign
                end
        """
        def chk_if(stmts, val):
            self.assertEqual(len(stmts), 3)
            self.assertEqual(stmts[0], val)
            return True


        keywords = (('forever', ''), ('while', '(2 > 1)'),
                    ('repeat', '( (1 + 2) > 3)'), ('for', '(a = 0; 1 < 100; a = 1 + 101)'))
        stmts = (('if(2>=1) a = 1; else b = 2;',
                  lambda e: self.assertTrue(chk_if(e.IfStatement, 'a') and chk_if(e.ElseStatement, 'b'))),
                 ('begin if(2>=1) a = 1; b <= 3 + 1;end',
                  lambda e: (chk_if(e.StatementList[0].IfStatement, 'a') and
                            self.assertEqual(e.StatementList[1][0], 'b'))))

        for kw, expr in keywords:
            for stmt, chk_f in stmts:
                tc_codes = '%s %s %s' % (kw, expr, stmt)
                print('Testing : %s' % tc_codes)
                parsed_tkns = self.DUT.loop_statement.parseString(tc_codes)
                chk_f(parsed_tkns[0].Body)
                print(parsed_tkns)

    def testCaseTC1(self):
        """
            A testcase of combining loop with simple if statement
                case/casez/casex
                1: a = 1;
                1,2: begin b = 2;end
                1,2+3: c = 1*2;
                default:;
                endcase
        """
        def chk_case(items):
            for i, an_item in enumerate(items):
                print('Verifying %s' % an_item.Body)
                if i == 0:
                    self.assertEqual(an_item.Body[0], 'a')
                elif i == 1:
                    self.assertEqual(an_item.Body.StatementList[0][0], 'b')
                elif i == 2:
                    self.assertEqual(an_item.Body[0], 'c')

        keywords = (('case', '(1 + 2)'), ('casez', "((100-'h1)*3)"), ('casex', '(3)'))
        body = [("""
               1: a = 1;
               1,2: begin b = 2;end
               1,2+3: c = 1*2;
               default:;
               """, chk_case)]

        for kw, expr in keywords:
            for stmt, chk_f in body:
                tc_codes = '%s %s %s endcase' % (kw, expr, stmt)
                print('Testing : %s' % tc_codes)
                parsed_tkns = self.DUT.case_statement.parseString(tc_codes)
                chk_f(parsed_tkns[0].BodyList)
                print(parsed_tkns)

    def testSeqTC1(self):
        tc_codes = """
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
        """
        parsed_tkns = self.DUT.seq_block.parseString(tc_codes)
        # [['begin',  [......, ['nextCRC16_D8', '=', 'newcrc']], 'end']]
        self.assertEqual('begin', parsed_tkns[0][0])
        self.assertEqual('nextCRC16_D8', parsed_tkns[0][-2][-1][0])
        self.assertEqual('newcrc', parsed_tkns[0][-2][-1][-1])
        self.assertEqual('end', parsed_tkns[0][-1])
        print(parsed_tkns)

    def testParTC1(self):
        tc_seq_codes = """
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
        """
        tc_par_codes = 'fork %s %s join' % (tc_seq_codes, tc_seq_codes)
        parsed_tkns = self.DUT.statement.parseString(tc_par_codes)
        self.assertEqual(parsed_tkns[0][0], 'fork')
        self.assertEqual(parsed_tkns[0][1][0][1][-1][0], 'nextCRC16_D8')
        self.assertEqual(parsed_tkns[0][1][0][1][-1][-1], 'newcrc')
        self.assertEqual(parsed_tkns[0][-1], 'join')
        print(parsed_tkns)

    def testDisable(self):
        """
           disable_statement ::= disable hierarchical_task_identifier ;
                                | disable hierarchical_block_identifier ;
        """
        tc_codes = ['disable U_AA.U_SUB_AA.reg_a;', 'disable aa;']
        for codes in tc_codes:
            tkns = self.DUT.statement.parseString(codes)
            self.assertEqual(tkns[0], 'disable')

    def testTrigger(self):
        """
           event_trigger ::= -> hierarchical_event_identifier { [ expression ] } ;
        """
        tc_codes = ['-> U_AA.U_SUB_AA.reg_a;', '-> aa;']
        for codes in tc_codes:
            tkns = self.DUT.statement.parseString(codes)
            self.assertEqual(tkns[0][0], '->')

    def testWait(self):
        """
           wait_statement ::= wait ( expression ) statement_or_null
        """
        tc_codes = ["wait(an_id) begin a <= 3'h3;end;", 'wait(an_id);']
        for codes in tc_codes:
            tkns = self.DUT.statement.parseString(codes)
            try:
                self.assertEqual(tkns[0][0], 'wait')
            except (IndexError, AssertionError) as e:
                self.assertEqual(tkns[0], 'wait')

    def testTimingCtrlTC1(self):
        """
            A simple testcase of testing the following patterns:
            Delay control:
                # 100, # (100 + 200)
            Event control:
                @clk , @*, @(*),
                @(100), @(posedge 100), @(negedge 100), @(posedge 100, negedge 100),
                @(posedge 100 or negedge 200), @(100 or negedge 200), @(100, 200), repeat (10) @(10)
                @(clk), @(posedge clk), @(negedge clk), @(posedge clk, negedge rst_n),
                @(posedge clk or negedge rst_n), @(clk or negedge rst_n), @(clk, rst_n), repeat (10) @(clk)
        """


        stimus = [('# 100', lambda e: self.assertEqual(e, '100')),
                  # ('# (100 + 200)', lambda e: self.assertEqual(e[0], '100') and self.assertEqual(e[2], '200')),
                  ('@clk', self.get_eq(0, 'clk')),
                  ('@*', self.get_eq(0, '*')),
                  ('@(*)', self.get_eq(0, '*')),
                  ('@(100)', self.get_nest_eq('100', 0, 0)),
                  ('@(posedge 100)', self.get_nest_eq('100', 0, 1)),
                  ('@(negedge 100)', self.get_nest_eq('100', 0, 1)),
                  ('@(posedge 100 or negedge 200)', lambda e: self.get_nest_eq('100', 0, 1)(e) and
                                                              self.get_nest_eq('200', 0, 3, 1)(e)),
                  ('@(posedge 100, negedge 100)', lambda e: self.get_nest_eq('100', 0, 1)(e) and
                                                            self.get_nest_eq('100', 0, 3, 1)(e)),
                  ('@(100 or negedge 200)', lambda e: self.get_nest_eq('100', 0, 0)(e) and
                                                      self.get_nest_eq('200', 0, 2, 1)(e)),
                  ('@(100 , 200)', lambda e: self.get_nest_eq('100', 0, 0)(e) and
                                             self.get_nest_eq('200', 0, 2, 0)(e)),
                  ('repeat (10) @(10)', lambda e: self.get_nest_eq('10', 1)(e) and
                                                  self.get_nest_eq('10', 2, 0, 0)(e)),
                  ('@(posedge clk)', self.get_nest_eq('clk', 0, 1)),
                  ('@(negedge clk)', self.get_nest_eq('clk', 0, 1)),
                  ('@(posedge clk or negedge rst_n)', lambda e: self.get_nest_eq('clk', 0, 1)(e) and
                                                                self.get_nest_eq('rst_n', 0, 3, 1)(e)),
                  ('@(posedge clk, negedge rst_n)', lambda e: self.get_nest_eq('clk', 0, 1)(e) and
                                                              self.get_nest_eq('rst_n', 0, 3, 1)(e)),
                  ('@(clk or negedge rst_n)', lambda e: self.get_nest_eq('clk', 0, 0)(e) and
                                                        self.get_nest_eq('rst_n', 0, 2, 1)(e)),
                  ('@(clk , rst_n)', lambda e: self.get_nest_eq('clk', 0, 0)(e) and
                                               self.get_nest_eq('rst_n', 0, 2, 0)(e)),
                  ('repeat (10) @(clk)', lambda e: self.get_nest_eq('10', 1)(e) and
                                                  self.get_nest_eq('clk', 2, 0, 0)(e)),
                  ]
        for tc_codes, chk_f in stimus:
            print('Testing : %s' % tc_codes)
            parsed_tkns = self.DUT.delay_or_event_control.parseString(tc_codes)
            print(parsed_tkns)
            if chk_f:
                chk_f(parsed_tkns[0])

    def testAssignTC1(self):
        """
        """
        duts = [self.DUT.blk_assign, self.DUT.nonblk_assign]
        stimus = [[('a = #2 100', self.get_eq(3, '100')),
                   ('a = @(posedge 100) 125 + 200', self.get_eq(3, '125')),
                   ('{a, b}= @(posedge 100) 125 + 200', self.get_eq(3, '125'))],
                  [('a <= #2 100', self.get_eq(3, '100')),
                   ('a <= @(posedge 100) 125 + 200', self.get_eq(3, '125')),
                   ('{a, b} <= @(posedge 100) 125 + 200', self.get_eq(3, '125'))]
        ]

        for i, dut in enumerate(duts):
            for tc_codes, chk_f in stimus[i]:
                print('Testing : %s' % tc_codes)
                parsed_tkns = dut.parseString(tc_codes)
                print(parsed_tkns)
                if chk_f:
                    print('Verifying: %s' % parsed_tkns[0])
                    chk_f(parsed_tkns[0])

    def testAssignTC2(self):
        """
            A testcase of continuous assignment
            assign #100 var0 = expr , {var0, var1} = expr;
        """

        chk_var0 = lambda e: (self.get_nest_eq('var0', 1, 0, 0)(e) and
                              self.get_nest_eq('expr0', 1, 0, 2)(e) and
                              self.get_nest_eq('1', 1, 0, 4)(e))
        duts = [self.DUT.continuous_assign]
        stimus = [[('assign var0 = expr0 + 1;', chk_var0),
                   ('assign var0 = expr0 + 1, var1=var0;', lambda e: (chk_var0(e) and
                                                                      self.get_nest_eq('var1', 1, 1, 0)(e) and
                                                                      self.get_nest_eq('var0', 1, 1, 2)(e))),
                   ('assign var0 = expr0 + 1 , {var0, var1} = expr0 + expr1 + 2;', lambda e: (
                       self.get_nest_eq('var0', 1, 1, 0, 0)(e) and self.get_nest_eq('var1', 1, 1, 0, 1)(e)) and
                   self.get_nest_eq('2', 1, 1, 6)(e)),
                   ('assign #100 var0 = expr0 + 1 , {var0, var1} = expr0 + expr1 + 2;', lambda e: (
                       self.get_nest_eq('var0', 2, 1, 0, 0)(e) and self.get_nest_eq('var1', 2, 1, 0, 1)(e)) and
                   self.get_nest_eq('2', 2, 1, 6)(e)), ]]

        for i, dut in enumerate(duts):
            for tc_codes, chk_f in stimus[i]:
                print('Testing : %s' % tc_codes)
                parsed_tkns = dut.parseString(tc_codes)
                print(parsed_tkns)
                if chk_f:
                    print('Verifying: %s' % parsed_tkns[0])
                    chk_f(parsed_tkns[0])

    def testProcAssignTC1(self):
        """
        """
        stimus = [
            ('assign a = 100 + (a + b);', self.get_nest_eq('a', 1, 0)),
            # ('assign a = 100 + a;', None),
            ('deassign a;', self.get_nest_eq('a', 1)),
            ('force a = 100 + a;', self.get_nest_eq('a', 1, 0)),
            ('release a;', self.get_nest_eq('a', 1)),
            ]

        for tc_codes, chk_f in stimus:
            print('Testing : %s' % tc_codes)
            parsed_tkns = self.DUT.statement.parseString(tc_codes)
            print(parsed_tkns)
            if chk_f:
                print('Verifying: %s' % parsed_tkns)
                chk_f(parsed_tkns)

    def testTaskCall(self):
        stimus = [
            ('task_call;', None),
            ('task_call(a);', None),
            ('task_call(a, b);', None),
            ('task_call(a, b+c);', None),
            ('$task_call;', None),
            ('$task_call(a);', None),
            ('$task_call();', None),
            ('$task_call(a, b);', None),
            ('$task_call(a, b+c);', None),
        ]

        for tc_codes, chk_f in stimus:
            print('Testing : %s' % tc_codes)
            # self.DUT.statement.setDebug(True)
            parsed_tkns = self.DUT.statement.parseString(tc_codes)
            print(parsed_tkns)
            if chk_f:
                print('Verifying: %s' % parsed_tkns)
                chk_f(parsed_tkns)

