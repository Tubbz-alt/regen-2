import regen as rg

# Instance the Register Map
GPIO = rg.RegisterMap('GPIO')

# Registers
GPIO[0] = 'REG_VERSION'
GPIO['REG_VERSION'].description = 'Version register'

GPIO[1] = 'REG_ID'
GPIO['REG_ID'].description = 'ID register'

GPIO[2] = 'REG_SCRATCH'
GPIO['REG_SCRATCH'].description = 'Scratch register'

GPIO[7] = 'REG_INFO'
GPIO['REG_INFO'].description = 'FPGA device information'

# 'VERSION' Register
GPIO['REG_VERSION'][31:0] = 'VERSION'

# 'ID' Register
GPIO['REG_ID'][31:0] = 'ID'

# 'SCRATCH' Register
GPIO['REG_SCRATCH'][31:0] = 'SCRATCH'

# 'INFO' Register
GPIO['REG_INFO'][31:24] = 'FPGA_TECHNOLOGY'
GPIO['REG_INFO'][23:16] = 'FPGA_FAMILY'
GPIO['REG_INFO'][15: 8] = 'SPEED_GRADE'
GPIO['REG_INFO'][ 7: 0] = 'DEV_PACKAGE'

# Generate the verilog file
GPIO.gen_verilog()