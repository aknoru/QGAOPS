`timescale 1ns / 1ps

module tb_test_readback;
    logic ap_clk = 0;
    logic ap_rst_n = 0;
    logic s_axi_control_AWVALID = 0;
    logic s_axi_control_AWREADY;
    logic [7:0] s_axi_control_AWADDR = 0;
    logic s_axi_control_WVALID = 0;
    logic s_axi_control_WREADY;
    logic [31:0] s_axi_control_WDATA = 0;
    logic [3:0] s_axi_control_WSTRB = 0;
    logic s_axi_control_ARVALID = 0;
    logic s_axi_control_ARREADY;
    logic [7:0] s_axi_control_ARADDR = 0;
    logic s_axi_control_RVALID;
    logic s_axi_control_RREADY = 0;
    logic [31:0] s_axi_control_RDATA;
    logic [1:0] s_axi_control_RRESP;
    logic s_axi_control_BVALID;
    logic s_axi_control_BREADY = 0;
    logic [1:0] s_axi_control_BRESP;
    logic interrupt;

    seq_gpu u_dut (
        .ap_clk(ap_clk),
        .ap_rst_n(ap_rst_n),
        .s_axi_control_AWVALID(s_axi_control_AWVALID),
        .s_axi_control_AWREADY(s_axi_control_AWREADY),
        .s_axi_control_AWADDR(s_axi_control_AWADDR),
        .s_axi_control_WVALID(s_axi_control_WVALID),
        .s_axi_control_WREADY(s_axi_control_WREADY),
        .s_axi_control_WDATA(s_axi_control_WDATA),
        .s_axi_control_WSTRB(s_axi_control_WSTRB),
        .s_axi_control_ARVALID(s_axi_control_ARVALID),
        .s_axi_control_ARREADY(s_axi_control_ARREADY),
        .s_axi_control_ARADDR(s_axi_control_ARADDR),
        .s_axi_control_RVALID(s_axi_control_RVALID),
        .s_axi_control_RREADY(s_axi_control_RREADY),
        .s_axi_control_RDATA(s_axi_control_RDATA),
        .s_axi_control_RRESP(s_axi_control_RRESP),
        .s_axi_control_BVALID(s_axi_control_BVALID),
        .s_axi_control_BREADY(s_axi_control_BREADY),
        .s_axi_control_BRESP(s_axi_control_BRESP),
        .interrupt(interrupt)
    );

    always #5.0 ap_clk = ~ap_clk;

    task automatic write_reg(input [7:0] addr, input [31:0] val);
        @(posedge ap_clk);
        s_axi_control_AWADDR <= addr;
        s_axi_control_AWVALID <= 1'b1;
        s_axi_control_WDATA <= val;
        s_axi_control_WSTRB <= 4'hF;
        s_axi_control_WVALID <= 1'b1;
        s_axi_control_BREADY <= 1'b1;
        
        while (!(s_axi_control_AWREADY && s_axi_control_AWVALID)) @(posedge ap_clk);
        s_axi_control_AWVALID <= 1'b0;

        while (!(s_axi_control_WREADY && s_axi_control_WVALID)) @(posedge ap_clk);
        s_axi_control_WVALID <= 1'b0;

        while (!s_axi_control_BVALID) @(posedge ap_clk);
        @(posedge ap_clk);
        s_axi_control_BREADY <= 1'b0;
    endtask

    task automatic read_reg(input [7:0] addr, output [31:0] val);
        @(posedge ap_clk);
        s_axi_control_ARADDR <= addr;
        s_axi_control_ARVALID <= 1'b1;
        s_axi_control_RREADY <= 1'b1;

        while (!(s_axi_control_ARREADY && s_axi_control_ARVALID)) @(posedge ap_clk);
        s_axi_control_ARVALID <= 1'b0;

        while (!s_axi_control_RVALID) @(posedge ap_clk);
        val = s_axi_control_RDATA;
        @(posedge ap_clk);
        s_axi_control_RREADY <= 1'b0;
    endtask

    initial begin
        logic [31:0] rd;
        ap_rst_n = 0;
        repeat(10) @(posedge ap_clk);
        ap_rst_n = 1;
        repeat(5) @(posedge ap_clk);

        $display("Testing write to a[0] (0x20)...");
        write_reg(8'h20, 32'h12345678);
        read_reg(8'h20, rd);
        $display("Read back from 0x20: 0x%08h (Expected: 0x12345678)", rd);

        $display("Testing write to b[0] (0x40)...");
        write_reg(8'h40, 32'hAABBCCDD);
        read_reg(8'h40, rd);
        $display("Read back from 0x40: 0x%08h (Expected: 0xAABBCCDD)", rd);

        $display("Testing write to opcode (0x10)...");
        write_reg(8'h10, 32'h00000001);
        read_reg(8'h10, rd);
        $display("Read back from 0x10: 0x%08h (Expected: 0x00000001)", rd);

        $display("Starting operation...");
        write_reg(8'h00, 32'h1);
        while (1) begin
            read_reg(8'h00, rd);
            if (rd & 32'h2) break;
        end
        $display("Operation done!");
        read_reg(8'h60, rd);
        $display("Result c[0] (0x60): 0x%08h", rd);

        $finish;
    end
endmodule
