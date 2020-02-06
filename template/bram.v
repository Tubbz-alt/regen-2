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
    input  wire                    rd_en  ,
    output wire [C_DATA_WIDTH-1:0] rd_data,

    // Register interface
    //===================

    % for reg in regMap:
    // ${ reg.name }
        % for field in reg:
            % if not (loop.index == len(reg) - 1 and loop.parent.index == len(regMap) - 1):
                ## Ports list, with ',' ending
                % if field.access_type == 'RW':
    output wire ${field.self_range} ${field.full_name},
                % elif field.access_type == 'RO':
    input  wire ${field.self_range} ${field.full_name},
                % endif
            % else:
                % if field.access_type == 'RW':
    output wire ${field.self_range} ${field.full_name}
                % elif field.access_type == 'RO':
    input  wire ${field.self_range} ${field.full_name}
                % endif
            % endif
        % endfor

    % endfor
);

    // Internal FFs

    % for reg in regMap:
    // ${ reg.name }
        % for field in reg:
            % if field.access_type == 'RW' or field.access_type == 'RO':
    reg ${field.self_range} ${field.full_name}_reg;
            % endif
        % endfor

    % endfor

    // Registers/fields update

    % for reg in regMap:
    // ${ reg.name }
        % for field in reg:
            % if field.access_type == 'RW':
    always @ (posedge clk) begin
        if (rst) begin
            ${field.full_name}_reg <= 'd${field.reset};
        end else if (wr_en == 1'b1 && wr_addr == 'd${reg.address_offset}) begin
            ${field.full_name}_reg <= wr_data${field.full_range};
        end
    end

    assign ${field.full_name} = ${field.full_name}_reg;

            % elif field.access_type == 'RW':
    always @ (posedge clk) begin
        if (rst) begin
            ${field.full_name}_reg <= 'd${field.reset};
        end else begin
            ${field.full_name}_reg <= ${field.full_name};
        end
    end

            % endif
        % endfor
    % endfor

    // Register Reading

    always @ (posedge clk) begin
        if (rst) begin
            rd_data <= 'd0;
        end else if (rd_en) begin
            rd_data <= 'd0;
            case(rd_addr)
                % for reg in regMap:
                // ${reg.name}
                ${reg.address_offset}: begin
                    % for field in reg:
                    rd_data${field.full_range} <= ${field.full_name}_reg;
                    % endfor
                end
                % endfor
            endcase
        end
    end


endmodule

`default_nettype wire
