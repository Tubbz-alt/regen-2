import regen as rg
from mako.template import Template

GPIO = rg.RegisterMap('GPIO')

GPIO[0] = 'CTRL'

GPIO.CTRL[0] = ('DIR', 'RW')
GPIO.CTRL[2:1] = ('VAR', 'RW')

GPIO.verilog("tmp/output.v")