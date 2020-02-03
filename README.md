# regen

Register map generator. Easy generate a Verilog register map block, using Python.

## Data Structure

* *Object* **RegisterMap** - Data object to store all the registers, will generate to a Verilog module.
  * *String* **name** - Name of this register map.
  * *Integer* **base_address** - Default base address of module. Can be override via parameter.
  * *String* **description** - Optional description of this module.
  * *List* **_registers** - Private list to store the registers in the map.


## Template

* **AXI-4 Lite** - AXI-4 Lite
  *  no **RSTRB** support
  *  no **AWPROT** and **ARPROT** support
* **BRAM**: BRAM like interface
  *  Common clock
  * Write interface with *wr_data*, *wr_en*, *wr_addr*
  * Read interface with *rd_addr*, *rd_en*, *rd_data* 