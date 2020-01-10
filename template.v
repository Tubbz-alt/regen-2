/*
Copyright (c) 2019 Chengdu JinZhiLi Technology Co., Ltd.
All rights reserved.
*/

`timescale 1 ns / 1 ps
`default_nettype none

module ${ name } #(
    parameter C_ADDR_WIDTH = 10,
    parameter C_BASE_ADDR  = ${ regMap.base_address }
) (
    input  wire                    up_clk    ,
    input  wire                    up_rst    ,
    //
    input  wire [C_ADDR_WIDTH-1:0] up_wr_addr,
    input  wire                    up_wr_req ,
    input  wire [            31:0] up_wr_data,
    output wire                    up_wr_ack ,
    //
    input  wire [C_ADDR_WIDTH-1:0] up_rd_addr,
    input  wire                    up_rd_req ,
    output wire [            31:0] up_rd_data,
    output wire                    up_rd_ack ,
    % for reg in regMap:
    // Register ${ reg.name } at ${ hex(reg.address_offset) }
        % for field in reg:
            % if field.type == 'RW':
    output wire [${ field.bit_width - 1 }:0] ${reg.name}_${field.name},
            % endif
        % endfor
    % endfor
);


endmodule

`default_nettype wire
