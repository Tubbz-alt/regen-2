from mako.template import Template


class Field:
    # Name of the field
    name = ""
    # Bit width of the field
    bit_width = 1
    # Bit offset of the field
    bit_offset = 0
    reset = 0
    type = 'RW'  # 'RW', 'RO', 'CONST'

    def __init__(self, name):
        self.name = name


class Register:
    name = ""
    address_offset = 0
    reg_type = 'NORMAL'  # 'NORMAL', 'MEMORY'
    description = ""
    fields = list()

    def __init__(self, name, address_offset=0, reg_type='NORMAL'):
        self.name = name
        self.address_offset = address_offset
        self.reg_type = reg_type

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index < len(self.fields):
            ret = self.fields[self.__index]
            self.__index += 1
            return ret
        raise StopIteration

    def __getitem__(self, item):
        print(item)


class RegisterMap:

    # Mandatory attributes
    name = ""
    base_address = 0

    # Optional attributes
    description = ""

    # Data storage
    _registers = []

    def __init__(self, name, base_address=0):
        self.name = name
        self.base_address = base_address

    def __iter__(self):
        return iter(self._registers)

    def __setitem__(self, key, value):
        if type(key) is str and type(value) is int:
            pass
        elif type(key) is int and type(value) is str:
            key, value = value, key
        else:
            raise KeyError

        reg = Register(key, value)
        self.add(reg)

    def __getitem__(self, name_or_addr):
        return self.get(name_or_addr)

    def __len__(self):
        return self._registers.__len__()

    def has(self, name_or_addr):
        """
        Test if register with given name or address offset exists in map
        :param name_or_addr:
        :return:
        """
        if type(name_or_addr) is str:
            return name_or_addr in {r.name for r in self._registers}
        elif type(name_or_addr) is int:
            return name_or_addr in {r.address_offset for r in self._registers}
        else:
            raise TypeError

    def get(self, name_or_addr):
        """
        Get the register with given name or address offset in map
        :param name_or_addr:
        :return:
        """
        if self.has(name_or_addr):
            if type(name_or_addr) is str:
                idx = [r.name for r in self._registers].index(name_or_addr)
                return self._registers[idx]
            elif type(name_or_addr) is int:
                idx = [r.address_offset for r in self._registers].index(name_or_addr)
                return self._registers[idx]
            else:
                raise TypeError
        else:
            # No register with name or address offset
            raise ValueError

    def remove(self, name_or_addr):
        """
        Remove register in current map
        """
        t = self.get(name_or_addr)
        self._registers.remove(t)

    def clear(self) -> None:
        """
        Remove all registers in current map, leave name and other attributes untouched
        """
        self._registers.clear()

    def add(self, reg, dup_check=True):
        if dup_check:
            if self.has(reg.name):
                self.remove(reg.name)
            if self.has(reg.address_offset):
                self.remove(reg.address_offset)
        # Append the new register to register list
        self._registers.append(reg)

    def gen_verilog(self, temp_file="template.v") -> str:
        # Render template
        t = Template(filename=temp_file)
        s = t.render(rm=self)
        return s
