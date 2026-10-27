-- ==============================================================
-- Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
-- Tool Version Limit: 2025.11
-- Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
-- Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
-- 
-- ==============================================================
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.NUMERIC_STD.all;

entity qgpu_ga_sequential_top_control_s_axi is
generic (
    C_S_AXI_ADDR_WIDTH    : INTEGER := 8;
    C_S_AXI_DATA_WIDTH    : INTEGER := 32);
port (
    ACLK                  :in   STD_LOGIC;
    ARESET                :in   STD_LOGIC;
    ACLK_EN               :in   STD_LOGIC;
    AWADDR                :in   STD_LOGIC_VECTOR(C_S_AXI_ADDR_WIDTH-1 downto 0);
    AWVALID               :in   STD_LOGIC;
    AWREADY               :out  STD_LOGIC;
    WDATA                 :in   STD_LOGIC_VECTOR(C_S_AXI_DATA_WIDTH-1 downto 0);
    WSTRB                 :in   STD_LOGIC_VECTOR(C_S_AXI_DATA_WIDTH/8-1 downto 0);
    WVALID                :in   STD_LOGIC;
    WREADY                :out  STD_LOGIC;
    BRESP                 :out  STD_LOGIC_VECTOR(1 downto 0);
    BVALID                :out  STD_LOGIC;
    BREADY                :in   STD_LOGIC;
    ARADDR                :in   STD_LOGIC_VECTOR(C_S_AXI_ADDR_WIDTH-1 downto 0);
    ARVALID               :in   STD_LOGIC;
    ARREADY               :out  STD_LOGIC;
    RDATA                 :out  STD_LOGIC_VECTOR(C_S_AXI_DATA_WIDTH-1 downto 0);
    RRESP                 :out  STD_LOGIC_VECTOR(1 downto 0);
    RVALID                :out  STD_LOGIC;
    RREADY                :in   STD_LOGIC;
    interrupt             :out  STD_LOGIC;
    opcode                :out  STD_LOGIC_VECTOR(31 downto 0);
    dma_len               :out  STD_LOGIC_VECTOR(31 downto 0);
    a_address0            :in   STD_LOGIC_VECTOR(2 downto 0);
    a_ce0                 :in   STD_LOGIC;
    a_q0                  :out  STD_LOGIC_VECTOR(31 downto 0);
    b_address0            :in   STD_LOGIC_VECTOR(2 downto 0);
    b_ce0                 :in   STD_LOGIC;
    b_q0                  :out  STD_LOGIC_VECTOR(31 downto 0);
    c_address0            :in   STD_LOGIC_VECTOR(2 downto 0);
    c_ce0                 :in   STD_LOGIC;
    c_we0                 :in   STD_LOGIC;
    c_d0                  :in   STD_LOGIC_VECTOR(31 downto 0);
    status                :in   STD_LOGIC_VECTOR(31 downto 0);
    status_ap_vld         :in   STD_LOGIC;
    ap_start              :out  STD_LOGIC;
    ap_done               :in   STD_LOGIC;
    ap_ready              :in   STD_LOGIC;
    ap_idle               :in   STD_LOGIC
);
end entity qgpu_ga_sequential_top_control_s_axi;

-- ------------------------Address Info-------------------
-- Protocol Used: ap_ctrl_hs
--
-- 0x00 : Control signals
--        bit 0  - ap_start (Read/Write/COH)
--        bit 1  - ap_done (Read/COR)
--        bit 2  - ap_idle (Read)
--        bit 3  - ap_ready (Read/COR)
--        bit 7  - auto_restart (Read/Write)
--        bit 9  - interrupt (Read)
--        others - reserved
-- 0x04 : Global Interrupt Enable Register
--        bit 0  - Global Interrupt Enable (Read/Write)
--        others - reserved
-- 0x08 : IP Interrupt Enable Register (Read/Write)
--        bit 0 - enable ap_done interrupt (Read/Write)
--        bit 1 - enable ap_ready interrupt (Read/Write)
--        others - reserved
-- 0x0c : IP Interrupt Status Register (Read/TOW)
--        bit 0 - ap_done (Read/TOW)
--        bit 1 - ap_ready (Read/TOW)
--        others - reserved
-- 0x10 : Data signal of opcode
--        bit 31~0 - opcode[31:0] (Read/Write)
-- 0x14 : reserved
-- 0x18 : Data signal of dma_len
--        bit 31~0 - dma_len[31:0] (Read/Write)
-- 0x1c : reserved
-- 0x80 : Data signal of status
--        bit 31~0 - status[31:0] (Read)
-- 0x84 : Control signal of status
--        bit 0  - status_ap_vld (Read/COR)
--        others - reserved
-- 0x20 ~
-- 0x3f : Memory 'a' (8 * 32b)
--        Word n : bit [31:0] - a[n]
-- 0x40 ~
-- 0x5f : Memory 'b' (8 * 32b)
--        Word n : bit [31:0] - b[n]
-- 0x60 ~
-- 0x7f : Memory 'c' (8 * 32b)
--        Word n : bit [31:0] - c[n]
-- (SC = Self Clear, COR = Clear on Read, TOW = Toggle on Write, COH = Clear on Handshake)

architecture behave of qgpu_ga_sequential_top_control_s_axi is
attribute DowngradeIPIdentifiedWarnings : STRING;
attribute DowngradeIPIdentifiedWarnings of behave : architecture is "yes";
    type states is (wridle, wrdata, wrresp, wrreset, rdidle, rddata, rdreset);  -- read and write fsm states
    signal wstate  : states := wrreset;
    signal rstate  : states := rdreset;
    signal wnext, rnext: states;
    constant ADDR_AP_CTRL        : INTEGER := 16#00#;
    constant ADDR_GIE            : INTEGER := 16#04#;
    constant ADDR_IER            : INTEGER := 16#08#;
    constant ADDR_ISR            : INTEGER := 16#0c#;
    constant ADDR_OPCODE_DATA_0  : INTEGER := 16#10#;
    constant ADDR_OPCODE_CTRL    : INTEGER := 16#14#;
    constant ADDR_DMA_LEN_DATA_0 : INTEGER := 16#18#;
    constant ADDR_DMA_LEN_CTRL   : INTEGER := 16#1c#;
    constant ADDR_STATUS_DATA_0  : INTEGER := 16#80#;
    constant ADDR_STATUS_CTRL    : INTEGER := 16#84#;
    constant ADDR_A_BASE         : INTEGER := 16#20#;
    constant ADDR_A_HIGH         : INTEGER := 16#3f#;
    constant ADDR_B_BASE         : INTEGER := 16#40#;
    constant ADDR_B_HIGH         : INTEGER := 16#5f#;
    constant ADDR_C_BASE         : INTEGER := 16#60#;
    constant ADDR_C_HIGH         : INTEGER := 16#7f#;
    constant ADDR_BITS         : INTEGER := 8;

    signal AWREADY_t           : STD_LOGIC;
    signal WREADY_t            : STD_LOGIC;
    signal ARREADY_t           : STD_LOGIC;
    signal RVALID_t            : STD_LOGIC;
    signal BVALID_t            : STD_LOGIC;
    signal waddr               : UNSIGNED(ADDR_BITS-1 downto 0);
    signal wmask               : UNSIGNED(C_S_AXI_DATA_WIDTH-1 downto 0);
    signal aw_hs               : STD_LOGIC;
    signal w_hs                : STD_LOGIC;
    signal rdata_data          : UNSIGNED(C_S_AXI_DATA_WIDTH-1 downto 0);
    signal ar_hs               : STD_LOGIC;
    signal raddr               : UNSIGNED(ADDR_BITS-1 downto 0);
    -- internal registers
    signal int_ap_idle         : STD_LOGIC := '0';
    signal int_ap_ready        : STD_LOGIC := '0';
    signal task_ap_ready       : STD_LOGIC;
    signal int_ap_done         : STD_LOGIC := '0';
    signal task_ap_done        : STD_LOGIC;
    signal int_task_ap_done    : STD_LOGIC := '0';
    signal int_ap_start        : STD_LOGIC := '0';
    signal int_interrupt       : STD_LOGIC := '0';
    signal int_auto_restart    : STD_LOGIC := '0';
    signal auto_restart_status : STD_LOGIC := '0';
    signal auto_restart_done   : STD_LOGIC;
    signal int_gie             : STD_LOGIC := '0';
    signal int_ier             : UNSIGNED(1 downto 0) := (others => '0');
    signal int_isr             : UNSIGNED(1 downto 0) := (others => '0');
    signal int_opcode          : UNSIGNED(31 downto 0) := (others => '0');
    signal int_dma_len         : UNSIGNED(31 downto 0) := (others => '0');
    signal int_status_ap_vld   : STD_LOGIC;
    signal int_status          : UNSIGNED(31 downto 0) := (others => '0');
    -- memory signals
    signal int_a_address0      : UNSIGNED(2 downto 0);
    signal int_a_ce0           : STD_LOGIC;
    signal int_a_q0            : UNSIGNED(31 downto 0);
    signal int_a_address1      : UNSIGNED(2 downto 0);
    signal int_a_ce1           : STD_LOGIC;
    signal int_a_be1           : UNSIGNED(3 downto 0);
    signal int_a_we1           : STD_LOGIC;
    signal int_a_d1            : UNSIGNED(31 downto 0);
    signal int_a_q1            : UNSIGNED(31 downto 0);
    signal int_a_read          : STD_LOGIC;
    signal int_a_write         : STD_LOGIC;
    signal int_b_address0      : UNSIGNED(2 downto 0);
    signal int_b_ce0           : STD_LOGIC;
    signal int_b_q0            : UNSIGNED(31 downto 0);
    signal int_b_address1      : UNSIGNED(2 downto 0);
    signal int_b_ce1           : STD_LOGIC;
    signal int_b_be1           : UNSIGNED(3 downto 0);
    signal int_b_we1           : STD_LOGIC;
    signal int_b_d1            : UNSIGNED(31 downto 0);
    signal int_b_q1            : UNSIGNED(31 downto 0);
    signal int_b_read          : STD_LOGIC;
    signal int_b_write         : STD_LOGIC;
    signal int_c_address0      : UNSIGNED(2 downto 0);
    signal int_c_ce0           : STD_LOGIC;
    signal int_c_be0           : UNSIGNED(3 downto 0);
    signal int_c_d0            : UNSIGNED(31 downto 0);
    signal int_c_address1      : UNSIGNED(2 downto 0);
    signal int_c_ce1           : STD_LOGIC;
    signal int_c_q1            : UNSIGNED(31 downto 0);
    signal int_c_read          : STD_LOGIC;
    signal int_c_write         : STD_LOGIC;

    component qgpu_ga_sequential_top_control_s_axi_ram is
        generic (
            MEM_STYLE : STRING :="auto";
            MEM_TYPE  : STRING :="S2P";
            BYTE_WIDTH : INTEGER :=8;
            WIDTH   : INTEGER :=32;
            BYTES   : INTEGER :=4;
            DEPTH   : INTEGER :=256;
            AWIDTH  : INTEGER :=8);
        port (
            clk0    : in  STD_LOGIC;
            address0: in  UNSIGNED(AWIDTH-1 downto 0);
            ce0     : in  STD_LOGIC;
            we0     : in  UNSIGNED(BYTES-1 downto 0);
            d0      : in  UNSIGNED(WIDTH-1 downto 0);
            q0      : out UNSIGNED(WIDTH-1 downto 0);
            clk1    : in  STD_LOGIC;
            address1: in  UNSIGNED(AWIDTH-1 downto 0);
            ce1     : in  STD_LOGIC;
            we1     : in  UNSIGNED(BYTES-1 downto 0);
            d1      : in  UNSIGNED(WIDTH-1 downto 0);
            q1      : out UNSIGNED(WIDTH-1 downto 0));
    end component qgpu_ga_sequential_top_control_s_axi_ram;

    function log2 (x : INTEGER) return INTEGER is
        variable n, m : INTEGER;
    begin
        n := 1;
        m := 2;
        while m < x loop
            n := n + 1;
            m := m * 2;
        end loop;
        return n;
    end function log2;

begin
-- ----------------------- Instantiation------------------
-- int_a
int_a : qgpu_ga_sequential_top_control_s_axi_ram
generic map (
     MEM_STYLE  => "auto",
     MEM_TYPE   => "2P",
     BYTE_WIDTH => 8,
     WIDTH      => 32,
     BYTES      => 4,
     DEPTH      => 8,
     AWIDTH     => log2(8))
port map (
     clk0       => ACLK,
     address0   => int_a_address0,
     ce0        => int_a_ce0,
     we0        => (others=>'0'),
     d0         => (others=>'0'),
     q0         => int_a_q0,
     clk1       => ACLK,
     address1   => int_a_address1,
     ce1        => int_a_ce1,
     we1        => int_a_be1,
     d1         => int_a_d1,
     q1         => int_a_q1);
-- int_b
int_b : qgpu_ga_sequential_top_control_s_axi_ram
generic map (
     MEM_STYLE  => "auto",
     MEM_TYPE   => "2P",
     BYTE_WIDTH => 8,
     WIDTH      => 32,
     BYTES      => 4,
     DEPTH      => 8,
     AWIDTH     => log2(8))
port map (
     clk0       => ACLK,
     address0   => int_b_address0,
     ce0        => int_b_ce0,
     we0        => (others=>'0'),
     d0         => (others=>'0'),
     q0         => int_b_q0,
     clk1       => ACLK,
     address1   => int_b_address1,
     ce1        => int_b_ce1,
     we1        => int_b_be1,
     d1         => int_b_d1,
     q1         => int_b_q1);
-- int_c
int_c : qgpu_ga_sequential_top_control_s_axi_ram
generic map (
     MEM_STYLE  => "auto",
     MEM_TYPE   => "S2P",
     BYTE_WIDTH => 8,
     WIDTH      => 32,
     BYTES      => 4,
     DEPTH      => 8,
     AWIDTH     => log2(8))
port map (
     clk0       => ACLK,
     address0   => int_c_address0,
     ce0        => int_c_ce0,
     we0        => int_c_be0,
     d0         => int_c_d0,
     q0         => open,
     clk1       => ACLK,
     address1   => int_c_address1,
     ce1        => int_c_ce1,
     we1        => (others=>'0'),
     d1         => (others=>'0'),
     q1         => int_c_q1);


-- ----------------------- AXI WRITE ---------------------
    AWREADY_t <=  '1' when wstate = wridle else '0';
    AWREADY   <=  AWREADY_t;
    WREADY_t  <=  '1' when wstate = wrdata and ar_hs = '0' else '0';
    WREADY    <=  WREADY_t;
    BVALID_t  <=  '1' when wstate = wrresp else '0';
    BVALID    <=  BVALID_t;
    BRESP     <=  "00";  -- OKAY
    wmask     <=  (31 downto 24 => WSTRB(3), 23 downto 16 => WSTRB(2), 15 downto 8 => WSTRB(1), 7 downto 0 => WSTRB(0));
    aw_hs     <=  AWVALID and AWREADY_t;
    w_hs      <=  WVALID and WREADY_t;

    -- write FSM
    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                wstate <= wrreset;
            elsif (ACLK_EN = '1') then
                wstate <= wnext;
            end if;
        end if;
    end process;

    process (wstate, AWVALID, w_hs, BREADY, BVALID_t)
    begin
        case (wstate) is
        when wridle =>
            if (AWVALID = '1') then
                wnext <= wrdata;
            else
                wnext <= wridle;
            end if;
        when wrdata =>
            if (w_hs = '1') then
                wnext <= wrresp;
            else
                wnext <= wrdata;
            end if;
        when wrresp =>
            if (BREADY = '1' and BVALID_t = '1') then
                wnext <= wridle;
            else
                wnext <= wrresp;
            end if;
        when others =>
            wnext <= wridle;
        end case;
    end process;

    waddr_proc : process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ACLK_EN = '1') then
                if (aw_hs = '1') then
                    waddr <= UNSIGNED(AWADDR(ADDR_BITS-1 downto 2) & (1 downto 0 => '0'));
                end if;
            end if;
        end if;
    end process;

-- ----------------------- AXI READ ----------------------
    ARREADY_t <= '1' when (rstate = rdidle) else '0';
    ARREADY <= ARREADY_t;
    RDATA   <= STD_LOGIC_VECTOR(rdata_data);
    RRESP   <= "00";  -- OKAY
    RVALID_t  <= '1' when (rstate = rddata) and (int_a_read = '0') and (int_b_read = '0') and (int_c_read = '0') else '0';
    RVALID    <= RVALID_t;
    ar_hs   <= ARVALID and ARREADY_t;
    raddr   <= UNSIGNED(ARADDR(ADDR_BITS-1 downto 0));

    -- read FSM
    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                rstate <= rdreset;
            elsif (ACLK_EN = '1') then
                rstate <= rnext;
            end if;
        end if;
    end process;

    process (rstate, ARVALID, RREADY, RVALID_t)
    begin
        case (rstate) is
        when rdidle =>
            if (ARVALID = '1') then
                rnext <= rddata;
            else
                rnext <= rdidle;
            end if;
        when rddata =>
            if (RREADY = '1' and RVALID_t = '1') then
                rnext <= rdidle;
            else
                rnext <= rddata;
            end if;
        when others =>
            rnext <= rdidle;
        end case;
    end process;

    rdata_proc : process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ACLK_EN = '1') then
                if (ar_hs = '1') then
                    rdata_data <= (others => '0');
                    case (TO_INTEGER(raddr)) is
                    when ADDR_AP_CTRL =>
                        rdata_data(9) <= int_interrupt;
                        rdata_data(7) <= int_auto_restart;
                        rdata_data(3) <= int_ap_ready;
                        rdata_data(2) <= int_ap_idle;
                        rdata_data(1) <= int_task_ap_done;
                        rdata_data(0) <= int_ap_start;
                    when ADDR_GIE =>
                        rdata_data(0) <= int_gie;
                    when ADDR_IER =>
                        rdata_data(1 downto 0) <= int_ier;
                    when ADDR_ISR =>
                        rdata_data(1 downto 0) <= int_isr;
                    when ADDR_OPCODE_DATA_0 =>
                        rdata_data <= RESIZE(int_opcode(31 downto 0), 32);
                    when ADDR_DMA_LEN_DATA_0 =>
                        rdata_data <= RESIZE(int_dma_len(31 downto 0), 32);
                    when ADDR_STATUS_DATA_0 =>
                        rdata_data <= RESIZE(int_status(31 downto 0), 32);
                    when ADDR_STATUS_CTRL =>
                        rdata_data(0) <= int_status_ap_vld;
                    when others =>
                        NULL;
                    end case;
                elsif (int_a_read = '1') then
                    rdata_data <= RESIZE(int_a_q1, 32);
                elsif (int_b_read = '1') then
                    rdata_data <= RESIZE(int_b_q1, 32);
                elsif (int_c_read = '1') then
                    rdata_data <= RESIZE(int_c_q1, 32);
                end if;
            end if;
        end if;
    end process;

-- ----------------------- Register logic ----------------
    interrupt            <= int_interrupt;
    ap_start             <= int_ap_start;
    task_ap_done         <= (ap_done and not auto_restart_status) or auto_restart_done;
    task_ap_ready        <= ap_ready and not int_auto_restart;
    auto_restart_done    <= auto_restart_status and (ap_idle and not int_ap_idle);
    opcode               <= STD_LOGIC_VECTOR(int_opcode);
    dma_len              <= STD_LOGIC_VECTOR(int_dma_len);

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_interrupt <= '0';
            elsif (ACLK_EN = '1') then
                if (int_gie = '1' and (int_isr(0) or int_isr(1)) = '1') then
                    int_interrupt <= '1';
                else
                    int_interrupt <= '0';
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_ap_start <= '0';
            elsif (ACLK_EN = '1') then
                if (w_hs = '1' and waddr = ADDR_AP_CTRL and WSTRB(0) = '1' and WDATA(0) = '1') then
                    int_ap_start <= '1';
                elsif (ap_ready = '1') then
                    int_ap_start <= int_auto_restart; -- clear on handshake/auto restart
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_ap_done <= '0';
            elsif (ACLK_EN = '1') then
                if (true) then
                    int_ap_done <= ap_done;
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_task_ap_done <= '0';
            elsif (ACLK_EN = '1') then
                if (task_ap_done = '1') then
                    int_task_ap_done <= '1';
                elsif (ar_hs = '1' and raddr = ADDR_AP_CTRL) then
                    int_task_ap_done <= '0'; -- clear on read
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_ap_idle <= '0';
            elsif (ACLK_EN = '1') then
                if (true) then
                    int_ap_idle <= ap_idle;
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_ap_ready <= '0';
            elsif (ACLK_EN = '1') then
                if (task_ap_ready = '1') then
                    int_ap_ready <= '1';
                elsif (ar_hs = '1' and raddr = ADDR_AP_CTRL) then
                    int_ap_ready <= '0';
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_auto_restart <= '0';
            elsif (ACLK_EN = '1') then
                if (w_hs = '1' and waddr = ADDR_AP_CTRL and WSTRB(0) = '1') then
                    int_auto_restart <= WDATA(7);
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                auto_restart_status <= '0';
            elsif (ACLK_EN = '1') then
                if (int_auto_restart = '1') then
                    auto_restart_status <= '1';
                elsif (ap_idle = '1') then
                    auto_restart_status <= '0';
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_gie <= '0';
            elsif (ACLK_EN = '1') then
                if (w_hs = '1' and waddr = ADDR_GIE and WSTRB(0) = '1') then
                    int_gie <= WDATA(0);
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_ier <= (others=>'0');
            elsif (ACLK_EN = '1') then
                if (w_hs = '1' and waddr = ADDR_IER and WSTRB(0) = '1') then
                    int_ier <= UNSIGNED(WDATA(1 downto 0));
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_isr(0) <= '0';
            elsif (ACLK_EN = '1') then
                if (int_ier(0) = '1' and ap_done = '1') then
                    int_isr(0) <= '1';
                elsif (w_hs = '1' and waddr = ADDR_ISR and WSTRB(0) = '1') then
                    int_isr(0) <= int_isr(0) xor WDATA(0); -- toggle on write
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_isr(1) <= '0';
            elsif (ACLK_EN = '1') then
                if (int_ier(1) = '1' and ap_ready = '1') then
                    int_isr(1) <= '1';
                elsif (w_hs = '1' and waddr = ADDR_ISR and WSTRB(0) = '1') then
                    int_isr(1) <= int_isr(1) xor WDATA(1); -- toggle on write
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_opcode(31 downto 0) <= (others => '0');
            elsif (ACLK_EN = '1') then
                if (w_hs = '1' and waddr = ADDR_OPCODE_DATA_0) then
                    int_opcode(31 downto 0) <= (UNSIGNED(WDATA(31 downto 0)) and wmask(31 downto 0)) or ((not wmask(31 downto 0)) and int_opcode(31 downto 0));
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_dma_len(31 downto 0) <= (others => '0');
            elsif (ACLK_EN = '1') then
                if (w_hs = '1' and waddr = ADDR_DMA_LEN_DATA_0) then
                    int_dma_len(31 downto 0) <= (UNSIGNED(WDATA(31 downto 0)) and wmask(31 downto 0)) or ((not wmask(31 downto 0)) and int_dma_len(31 downto 0));
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_status <= (others => '0');
            elsif (ACLK_EN = '1') then
                if (status_ap_vld = '1') then
                    int_status <= UNSIGNED(status);
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_status_ap_vld <= '0';
            elsif (ACLK_EN = '1') then
                if (status_ap_vld = '1') then
                    int_status_ap_vld <= '1';
                elsif (ar_hs = '1' and raddr = ADDR_STATUS_CTRL) then
                    int_status_ap_vld <= '0'; -- clear on read
                end if;
            end if;
        end if;
    end process;


-- ----------------------- Memory logic ------------------
    -- a
    int_a_address0       <= RESIZE(UNSIGNED(a_address0), 3);
    int_a_ce0            <= a_ce0;
    a_q0                 <= STD_LOGIC_VECTOR(RESIZE(int_a_q0, 32));
    int_a_address1       <= raddr(4 downto 2) when ar_hs = '1' else waddr(4 downto 2);
    int_a_ce1            <= '1' when ar_hs = '1' or (int_a_write = '1' and WVALID  = '1') else '0';
    int_a_we1            <= '1' when int_a_write = '1' and w_hs = '1' else '0';
    int_a_be1            <= UNSIGNED(WSTRB) when int_a_we1 = '1' else (others=>'0');
    int_a_d1             <= UNSIGNED(WDATA);
    -- b
    int_b_address0       <= RESIZE(UNSIGNED(b_address0), 3);
    int_b_ce0            <= b_ce0;
    b_q0                 <= STD_LOGIC_VECTOR(RESIZE(int_b_q0, 32));
    int_b_address1       <= raddr(4 downto 2) when ar_hs = '1' else waddr(4 downto 2);
    int_b_ce1            <= '1' when ar_hs = '1' or (int_b_write = '1' and WVALID  = '1') else '0';
    int_b_we1            <= '1' when int_b_write = '1' and w_hs = '1' else '0';
    int_b_be1            <= UNSIGNED(WSTRB) when int_b_we1 = '1' else (others=>'0');
    int_b_d1             <= UNSIGNED(WDATA);
    -- c
    int_c_address0       <= RESIZE(UNSIGNED(c_address0), 3);
    int_c_ce0            <= c_ce0;
    int_c_be0            <= (others => c_we0);
    int_c_d0             <= RESIZE(UNSIGNED(c_d0), 32);
    int_c_address1       <= raddr(4 downto 2);
    int_c_ce1            <= '1' when ar_hs = '1' else '0';

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_a_read <= '0';
            elsif (ACLK_EN = '1') then
                if (ar_hs = '1' and raddr >= ADDR_A_BASE and raddr <= ADDR_A_HIGH) then
                    int_a_read <= '1';
                else
                    int_a_read <= '0';
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_a_write <= '0';
            elsif (ACLK_EN = '1') then
                if (aw_hs = '1' and UNSIGNED(AWADDR(ADDR_BITS-1 downto 0)) >= ADDR_A_BASE and UNSIGNED(AWADDR(ADDR_BITS-1 downto 0)) <= ADDR_A_HIGH) then
                    int_a_write <= '1';
                elsif (w_hs = '1') then
                    int_a_write <= '0';
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_b_read <= '0';
            elsif (ACLK_EN = '1') then
                if (ar_hs = '1' and raddr >= ADDR_B_BASE and raddr <= ADDR_B_HIGH) then
                    int_b_read <= '1';
                else
                    int_b_read <= '0';
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_b_write <= '0';
            elsif (ACLK_EN = '1') then
                if (aw_hs = '1' and UNSIGNED(AWADDR(ADDR_BITS-1 downto 0)) >= ADDR_B_BASE and UNSIGNED(AWADDR(ADDR_BITS-1 downto 0)) <= ADDR_B_HIGH) then
                    int_b_write <= '1';
                elsif (w_hs = '1') then
                    int_b_write <= '0';
                end if;
            end if;
        end if;
    end process;

    process (ACLK)
    begin
        if (ACLK'event and ACLK = '1') then
            if (ARESET = '1') then
                int_c_read <= '0';
            elsif (ACLK_EN = '1') then
                if (ar_hs = '1' and raddr >= ADDR_C_BASE and raddr <= ADDR_C_HIGH) then
                    int_c_read <= '1';
                else
                    int_c_read <= '0';
                end if;
            end if;
        end if;
    end process;


end architecture behave;

library IEEE;
USE IEEE.std_logic_1164.all;
USE IEEE.numeric_std.all;

entity qgpu_ga_sequential_top_control_s_axi_ram is
    generic (
        MEM_STYLE  : STRING :="auto";
        MEM_TYPE   : STRING :="S2P";
        BYTE_WIDTH : INTEGER :=8;
        WIDTH   : INTEGER :=32;
        DEPTH   : INTEGER :=256;
        BYTES   : INTEGER :=4;
        AWIDTH  : INTEGER :=8);
    port (
        clk0    : in  STD_LOGIC;
        address0: in  UNSIGNED(AWIDTH-1 downto 0);
        ce0     : in  STD_LOGIC;
        we0     : in  UNSIGNED(BYTES-1 downto 0);
        d0      : in  UNSIGNED(WIDTH-1 downto 0);
        q0      : out UNSIGNED(WIDTH-1 downto 0);
        clk1    : in  STD_LOGIC;
        address1: in  UNSIGNED(AWIDTH-1 downto 0);
        ce1     : in  STD_LOGIC;
        we1     : in  UNSIGNED(BYTES-1 downto 0);
        d1      : in  UNSIGNED(WIDTH-1 downto 0);
        q1      : out UNSIGNED(WIDTH-1 downto 0));

end entity qgpu_ga_sequential_top_control_s_axi_ram;

architecture behave of qgpu_ga_sequential_top_control_s_axi_ram is
    signal address0_tmp : UNSIGNED(AWIDTH-1 downto 0);
    signal address1_tmp : UNSIGNED(AWIDTH-1 downto 0);
    type RAM_T is array (0 to DEPTH - 1) of UNSIGNED(WIDTH - 1 downto 0);
    shared variable mem : RAM_T := (others => (others => '0'));
    attribute ram_style: string;
    attribute ram_style of mem: variable is MEM_STYLE;

    function port_type_gen( MEM_TYPE: STRING; MEM_STYLE: STRING; PORT_NAME: STRING) return STRING is
    begin
        if (MEM_TYPE = "S2P") and (PORT_NAME = "PORT0") then
            return "WO";
        elsif((MEM_TYPE = "S2P") and (PORT_NAME = "PORT1")) or ((MEM_TYPE = "2P") and (PORT_NAME = "PORT0")) then
            return "RO";
        elsif (MEM_STYLE = "hls_ultra") then
            return "RWNC";
        else
            return "RWRF";
        end if;
    end port_type_gen;
    constant PORT0 :STRING := port_type_gen(MEM_TYPE, MEM_STYLE, "PORT0");
    constant PORT1 :STRING := port_type_gen(MEM_TYPE, MEM_STYLE, "PORT1");

    function or_reduce( V: UNSIGNED) return std_logic is
    variable result: std_logic;
    begin
        for i in V'range loop
            if i = V'left then
                result := V(i);
            else
                result := result OR V(i);
            end if;
            exit when result = '1';
        end loop;
        return result;
    end or_reduce;

begin

    process (address0)
    begin
    address0_tmp <= address0;
    --synthesis translate_off
        if (address0 > DEPTH-1) then
            address0_tmp <= (others => '0');
        else
            address0_tmp <= address0;
        end if;
    --synthesis translate_on
    end process;

    process (address1)
    begin
    address1_tmp <= address1;
    --synthesis translate_off
        if (address1 > DEPTH-1) then
            address1_tmp <= (others => '0');
        else
            address1_tmp <= address1;
        end if;
    --synthesis translate_on
    end process;

    --read port 0
    read_p0_rf : if (PORT0 = "RO" or PORT0 = "RWRF") generate
        process (clk0) begin
            if (clk0'event and clk0 = '1') then
                if (ce0 = '1') then
                    q0 <= mem(to_integer(address0_tmp));
                end if;
            end if;
        end process;
    end generate read_p0_rf;

    read_p0_nc : if (PORT0 = "RWNC") generate
        process (clk0) begin
            if (clk0'event and clk0 = '1') then
                if (ce0 = '1') then
                    if (we0 = (we0'range => '0')) then
                        q0 <= mem(to_integer(address0_tmp));
                    end if;
                end if;
            end if;
        end process;
    end generate read_p0_nc;

    --read port 1
    read_p1_rf : if (PORT1 = "RO" or PORT1 = "RWRF") generate
        process (clk1) begin
            if (clk1'event and clk1 = '1') then
                if (ce1 = '1') then
                    q1 <= mem(to_integer(address1_tmp));
                end if;
            end if;
        end process;
    end generate read_p1_rf;

    read_p1_nc : if (PORT1 = "RWNC") generate
        process (clk1) begin
            if (clk1'event and clk1 = '1') then
                if (ce1 = '1') then
                    if (we1 = (we1'range => '0')) then
                        q1 <= mem(to_integer(address1_tmp));
                    end if;
                end if;
            end if;
        end process;
    end generate read_p1_nc;

    --write port 0
    write_p0 : if (PORT0 /= "RO") generate
        process (clk0)
        begin
            if (clk0'event and clk0 = '1') then
                if (ce0 = '1') then
                for i in 0 to BYTES - 1 loop
                    if (we0(i) = '1') then
                        mem(to_integer(address0_tmp))((i+1)*BYTE_WIDTH-1 downto i*BYTE_WIDTH) := d0((i+1)*BYTE_WIDTH-1 downto i*BYTE_WIDTH);
                    end if;
                end loop;
                end if;
            end if;
        end process;
    end generate write_p0;

    --write port 1
    write_p1 : if (PORT1 /= "RO") generate
        process (clk1)
        begin
            if (clk1'event and clk1 = '1') then
                if (ce1 = '1') then
                for i in 0 to BYTES - 1 loop
                    if (we1(i) = '1') then
                        mem(to_integer(address1_tmp))((i+1)*BYTE_WIDTH-1 downto i*BYTE_WIDTH) := d1((i+1)*BYTE_WIDTH-1 downto i*BYTE_WIDTH);
                    end if;
                end loop;
                end if;
            end if;
        end process;
    end generate write_p1;

end architecture behave;


