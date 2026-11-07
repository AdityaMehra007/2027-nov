// ============================================================================
// PROJECT AETHER-OMEGA (2027) — PROMETHEUS SYSTOLIC TENSOR ISA PROCESSING ELEMENT
// File: src/silicon/prometheus_tensor_isa.sv
// Standard: IEEE 1800-2017 Synthesizable SystemVerilog RTL
// Features: 64-bit Accumulator, Fused Single-Cycle Multiply-Accumulate (MMA),
//           Reversible Landauer-Safe Toffoli CCNOT ALU, Parametric ReLU Clipping,
//           and 2D Systolic Array Propagations (West-to-East, North-to-South)
// ============================================================================

`timescale 1ns / 1ps

module prometheus_systolic_tensor_pe #(
    parameter int DATA_W = 16,
    parameter int ACC_W  = 64
) (
    input  logic                     clk,
    input  logic                     rst_n,
    input  logic [1:0]               opcode,
    input  logic signed [DATA_W-1:0] act_in_west,
    input  logic signed [DATA_W-1:0] weight_in_north,
    input  logic [2:0]               q_bits_in,

    output logic signed [DATA_W-1:0] act_out_east,
    output logic signed [DATA_W-1:0] weight_out_south,
    output logic signed [ACC_W-1:0]  acc_out,
    output logic [2:0]               q_bits_out
);

    // Instruction Set Encoding definitions
    localparam logic [1:0] OP_NOP          = 2'b00; // Hold state, forward systolic streams
    localparam logic [1:0] OP_SYSTOLIC_MMA = 2'b01; // Fused Multiply-Accumulate
    localparam logic [1:0] OP_REV_TOFFOLI  = 2'b10; // Reversible Landauer CCNOT gate
    localparam logic [1:0] OP_RELU_CLIP    = 2'b11; // Non-linear activation clamp

    // Intermediate multiply product (signed extension to avoid overflow)
    logic signed [(2*DATA_W)-1:0] mult_product;
    assign mult_product = act_in_west * weight_in_north;

    // Synchronous execution block
    always_ff @(posedge clk) begin
        if (!rst_n) begin
            // Synchronous active-low reset: clear internal registers
            act_out_east     <= '0;
            weight_out_south <= '0;
            acc_out          <= '0;
            q_bits_out       <= '0;
        end else begin
            // 1. Systolic spatial data propagation (pipeline registers)
            act_out_east     <= act_in_west;
            weight_out_south <= weight_in_north;

            // 2. ISA execution based on 2-bit opcode
            case (opcode)
                OP_NOP: begin
                    // Maintain current accumulator value, pass quantum bits
                    acc_out    <= acc_out;
                    q_bits_out <= q_bits_in;
                end

                OP_SYSTOLIC_MMA: begin
                    // Single-cycle signed multiply-accumulate: acc <= acc + (act * weight)
                    acc_out    <= acc_out + $signed({{ (ACC_W - 2*DATA_W){mult_product[(2*DATA_W)-1]} }, mult_product});
                    q_bits_out <= q_bits_in;
                end

                OP_REV_TOFFOLI: begin
                    // Landauer-safe zero-entropy reversible Toffoli CCNOT gate:
                    // q0' = q0 ^ (q2 & q1)
                    // q1' = q1
                    // q2' = q2
                    q_bits_out[2] <= q_bits_in[2];
                    q_bits_out[1] <= q_bits_in[1];
                    q_bits_out[0] <= q_bits_in[0] ^ (q_bits_in[2] & q_bits_in[1]);
                    acc_out       <= acc_out;
                end

                OP_RELU_CLIP: begin
                    // Parametric ReLU: clamp negative accumulated values to zero
                    if (acc_out < '0) begin
                        acc_out <= '0;
                    end else begin
                        acc_out <= acc_out;
                    end
                    q_bits_out <= q_bits_in;
                end

                default: begin
                    acc_out    <= acc_out;
                    q_bits_out <= q_bits_in;
                end
            endcase
        end
    end

endmodule
