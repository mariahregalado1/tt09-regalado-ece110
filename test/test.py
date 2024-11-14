# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")
   # clock = Clock(dut.clk, 1, units = "ns")
   # cocotb.start_soon(clock.start())
    #dut.rst_n_value = 0
    #await ClockCycles(dut.clk, 10)
    #dut.rst_n.value = 1

    #dut.ui_in.value = 0
    #await ClockCycles(dut.clk, 10)
    #dut.ui_in.value = 20
    #await ClockCycles(dut.clk, 100)

    #dut._log.info("finished test")
    # Set the clock period to 10 us (100 KHz)
   # clock = Clock(dut.clk, 10, units="us")
   # cocotb.start_soon(clock.start())

    # Reset
   # dut._log.info("Reset")
    #dut.ena.value = 1
   # dut.ui_in.value = 0
   # dut.uio_in.value = 0
   # dut.rst_n.value = 0
   # await ClockCycles(dut.clk, 10)
   # dut.rst_n.value = 1

   # dut._log.info("Test project behavior")

    # Set the input values you want to test
   # dut.ui_in.value = 20
   # dut.uio_in.value = 30

    # Wait for one clock cycle to see the output values
  #  await ClockCycles(dut.clk, 1)

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
   # assert dut.uo_out.value == 50

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
    clock = Clock(dut.clk, 1, units="ns")
    cocotb.start_soon(clock.start())

    dut.rst_n.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 2)  
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 1)  

    #apply pre_spike (ui_in[7]) followed by post_spike (uio_in[7])
    dut.ui_in.value = 0b10000000  #only ui_in[7] high
    await ClockCycles(dut.clk, 1)  
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 5)
    #post_spike (uio_in[7]) after delay
    dut.uio_in.value = 0b10000000  #only uio_in[7] high
    await ClockCycles(dut.clk, 1)
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 5) 
    potentiated_weight = int(dut.uo_out.value)
    dut._log.info(f"Weight after potentiation: {bin(potentiated_weight)}")

    #apply post_spike then pre_spike 
    dut.uio_in.value = 0b10000000  #only uio_in[7] high
    await ClockCycles(dut.clk, 1)  
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 5)
    #pre_spike after delay
    dut.ui_in.value = 0b10000000  #only ui_in[7] high
    await ClockCycles(dut.clk, 1)  
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 5) 
    depressed_weight = int(dut.uo_out.value)
    dut._log.info(f"Weight after depression: {bin(depressed_weight)}")
    #boundary tests - repeated potentiation
    for _ in range(20): 
        dut.ui_in.value = 0b10000000
        await ClockCycles(dut.clk, 1)
        dut.ui_in.value = 0
        await ClockCycles(dut.clk, 1)
        dut.uio_in.value = 0b10000000
        await ClockCycles(dut.clk, 1)
        dut.uio_in.value = 0
        await ClockCycles(dut.clk, 1)
    assert int(dut.uo_out.value) <= 0b11111111, f"Weight exceeded maximum: {bin(dut.uo_out.value)}"
    #repeated depression
    for _ in range(20): 
        dut.uio_in.value = 0b10000000
        await ClockCycles(dut.clk, 1)
        dut.uio_in.value = 0
        await ClockCycles(dut.clk, 1)
        dut.ui_in.value = 0b10000000
        await ClockCycles(dut.clk, 1)
        dut.ui_in.value = 0
        await ClockCycles(dut.clk, 1)
    assert int(dut.uo_out.value) >= 0b00000000, f"Weight dropped below minimum: {bin(dut.uo_out.value)}"

    dut._log.info("Test completed!!! Yay :D")