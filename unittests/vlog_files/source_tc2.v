`celldefine
module CELLU ( Q, TE, CPN, E );
    input TE, CPN, E;
    output Q;
    reg notifier;

        wire TE_d, CPN_d, E_d;
        buf (_TE, TE_d);
        buf (_CPN, CPN_d);
        buf (_E, E_d);
        or (_G001, _E, _TE);

endmodule
`endcelldefine

