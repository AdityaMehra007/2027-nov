// ============================================================================
// PROJECT AETHER-OMEGA (2027) — NEUROMORPHIC SPIKE-TIMING-DEPENDENT PLASTICITY CORE
// File: src/neuromorphic/stdp_crossbar_core.sv
// Standard: IEEE 1800-2017 Synthesizable SystemVerilog RTL
// Features: Multiplierless Leaky Integrate-and-Fire (LIF) Membrane Potential,
//           Exponential Eligibility Trace Decay, Hebbian STDP Long-Term
//           Potentiation (LTP) Learning, and Ceiling-Clamped Synaptic Weight
// ============================================================================

`timescale 1ns / 1ps

module lif_stdp_neuron_core #(
    parameter int                 V_WIDTH    = 16,
    parameter signed [15:0]       V_REST     = -16'sd700, // Resting potential (-70.0 mV in fixed-point)
    parameter signed [15:0]       V_RESET    = -16'sd750, // Hyperpolarization reset potential (-75.0 mV)
    parameter signed [15:0]       V_THRESH   = -16'sd500, // Action potential threshold (-50.0 mV)
    parameter int                 LEAK_SHIFT = 4,         // Division by 2^4 = 16 for passive leak conductance
    parameter signed [15:0]       W_INITIAL  = 16'sd100,  // Baseline synaptic weight
    parameter signed [15:0]       W_MAX      = 16'sd1024, // Synaptic saturation ceiling
    parameter signed [15:0]       W_MIN      = 16'sd0     // Minimum synaptic weight floor
) (
    input  logic                          clk,
    input  logic                          rst_n,
    input  logic                          pre_synaptic_spike,
    input  logic signed [15:0]            external_current,

    output logic                          post_synaptic_spike,
    output logic signed [15:0]            synaptic_weight,
    output logic signed [V_WIDTH-1:0]     v_membrane,
    output logic [7:0]                    pre_spike_trace
);

    // Internal calculation signals
    logic signed [15:0] i_synaptic;
    logic signed [15:0] v_leak;
    logic signed [15:0] v_next;
    logic signed [15:0] delta_w;

    // Multiplierless synaptic current gating
    assign i_synaptic = pre_synaptic_spike ? synaptic_weight : 16'sd0;

    // Arithmetic right-shift for leak conductance calculation (multiplierless)
    assign v_leak = (v_membrane - V_REST) >>> LEAK_SHIFT;

    // Potential evaluation for next clock edge
    assign v_next = v_membrane - v_leak + i_synaptic + external_current;

    // Weight increment derived from active eligibility trace (scaled by 2^-3)
    assign delta_w = $signed({11'b0, pre_spike_trace[7:3]});

    always_ff @(posedge clk) begin
        if (!rst_n) begin
            // Synchronous active-low reset
            post_synaptic_spike <= 1'b0;
            synaptic_weight     <= W_INITIAL;
            v_membrane          <= V_REST;
            pre_spike_trace     <= 8'd0;
        end else begin
            // ----------------------------------------------------------------
            // 1. Eligibility Trace Update (Exponential Decay)
            // ----------------------------------------------------------------
            if (pre_synaptic_spike) begin
                // Pre-synaptic spike refreshes eligibility trace to maximum
                pre_spike_trace <= 8'd255;
            end else if (pre_spike_trace > 8'd0) begin
                // Exponential decay: trace <= trace - (trace >> 3) - 1
                pre_spike_trace <= pre_spike_trace - (pre_spike_trace >> 3) - 8'd1;
            end

            // ----------------------------------------------------------------
            // 2. Membrane Potential & STDP Weight Update
            // ----------------------------------------------------------------
            if (v_next >= V_THRESH) begin
                // Action potential fired: emit spike and reset membrane
                post_synaptic_spike <= 1'b1;
                v_membrane          <= V_RESET;

                // Hebbian STDP Long-Term Potentiation (LTP):
                // If pre-synaptic spike occurred within the eligibility window (trace > 16)
                if (pre_spike_trace > 8'd16 && synaptic_weight < W_MAX) begin
                    if (synaptic_weight + delta_w > W_MAX) begin
                        synaptic_weight <= W_MAX;
                    end else begin
                        synaptic_weight <= synaptic_weight + delta_w;
                    end
                end
            end else begin
                // Subthreshold integration
                post_synaptic_spike <= 1'b0;
                v_membrane          <= v_next;
            end
        end
    end

endmodule
