/*
Copyright (c) 2019 Chengdu JinZhiLi Technology Co., Ltd.
All rights reserved.
*/

`timescale 1 ns / 1 ps
`default_nettype none

module ${regMap.name} #(
    parameter C_ADDR_WIDTH = 10,
    parameter C_DATA_WIDTH = 32,
    parameter C_BASE_ADDR  = ${ regMap.base_address }
) (
    // BRAM Interface
    //===============

    // Common clock & reset
    //---------------------
    input  wire                    clk    ,
    input  wire                    rst    ,

    // Write interface
    //----------------
    input  wire [C_ADDR_WIDTH-1:0] wr_addr,
    input  wire                    wr_en  ,
    input  wire [C_DATA_WIDTH-1:0] wr_data,

    // Read interface
    //----------------
    input  wire [C_ADDR_WIDTH-1:0] rd_addr,
    input  wire                    rd_en ,
    output wire [C_DATA_WIDTH-1:0] rd_data,

    // Register interface
    //===================

    % for reg in regMap:
    // ${ reg.name }
    //------------------------
        % for field in reg:
            % if field.access_type == 'RW':
    output wire [${field.bit_width-1}:0] ${reg.name}_${field.name},
            % elif field.access_type == 'RO':
    input  wire ${field.self_range()} ${field.full_name('_')},
            % endif
        % endfor

    % endfor
);




    always @ (posedge clk) begin
        if (rst) begin

        end else begin

        end
    end


endmodule

`default_nettype wire
