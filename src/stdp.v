module stdp (
    input wire clk,
    input wire reset,
    input wire pre_spike,
    input wire post_spike,
    output reg [7:0] weight
);

parameter [15:0] B_POTENTIATION = 16'b0000101000000000; //can change
parameter [15:0] B_DEPRESSION = 16'b0000010100000000;   //can change
parameter [7:0] WEIGHT_MAX = 8'b11111111; 
parameter [7:0] WEIGHT_MIN = 8'b00000000; 


reg [15:0] trace_u; 
reg [15:0] delta_t; 


reg pre_spike_detected;
reg post_spike_detected;


always @(posedge clk) begin
    if (reset) begin
        pre_spike_detected <= 0;
        post_spike_detected <= 0;
        delta_t <= 0;
        trace_u <= 16'b0;
        weight <= 8'b10000000; //can change
    end else begin
        pre_spike_detected <= pre_spike;
        post_spike_detected <= post_spike;
    end
end


always @(posedge clk or posedge reset) begin
    if (reset) begin
        trace_u <= 16'b0;
    end else if (pre_spike_detected && !post_spike_detected) begin
        trace_u <= ((B_POTENTIATION * trace_u) >> 12) + 16'b0000100000000000; 
    end else if (!pre_spike_detected && post_spike_detected) begin   
        trace_u <= ((B_DEPRESSION * trace_u) >> 12) - 16'b0000100000000000; 
    end
end

always @(posedge clk) begin
    if (reset) begin
        weight <= 8'b10000000; 
    end else if (pre_spike_detected && post_spike_detected) begin
        if (delta_t > 0) begin
            if ((weight + (trace_u >> 8)) > WEIGHT_MAX) begin
                weight <= WEIGHT_MAX;
            end else begin
                weight <= weight + (trace_u >> 8);
            end
        end else if (delta_t < 0) begin
            if ((weight - (trace_u >> 8)) < WEIGHT_MIN) begin
                weight <= WEIGHT_MIN;
            end else begin
                weight <= weight - (trace_u >> 8);
            end
        end
        delta_t <= 0;
        trace_u <= 0; 
    end
end

endmodule