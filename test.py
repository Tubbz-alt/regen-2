import regen as rg
from mako.template import Template

GPIO = rg.RegisterMap('GPIO')

GPIO[0] = 'CTRL'
GPIO[1] = 'STAT'
GPIO['STAT2'] = 3

print(GPIO)