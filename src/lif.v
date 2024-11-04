`default_nettype none

module lif (
    input wire [7:0] current,
    input wire clk,
    input wire rst_n,
    output reg[7:0] state,
    output wire  spike
);

wire [7:0] next_state;
reg[7:0] threshold;

always @(posedge clk) begin
    if (!rst_n) begin
        state <= 0;
        threshold <= 200;
    end else begin
        state <= next_state;
    end
end
assign next_state = current + (state >> 1);
assign spike = (state >= threshold);

endmodule