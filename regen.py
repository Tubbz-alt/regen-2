from mako.template import Template


class Field:
    # Unique identify
    name = ""
    bit_width = 1
    bit_offset = 0

    # Mandatory attributes
    reset = 0
    access_type = 'RW'
    _parent = None

    # Optional attributes
    description = ""

    def __init__(self, name, access_type='RW', bit_offset=0, bit_width=1, reset=0, parent=None):
        self.name = name
        self.access_type = access_type
        self.bit_width = bit_width
        self.bit_offset = bit_offset
        self.reset = reset
        self._parent = parent

    @staticmethod
    def from_dict(d: dict):
        ret = Field(name=d['name'])

        # Override default values
        if d.get('access_type'):
            ret.access_type = d['access_type']
        if d.get('bit_offset'):
            ret.bit_offset = d['bit_offset']

        return ret

    def full_name(self, delimiter='.'):
        """
        Get the string of field name in REGISTER.FIELD format
        """
        if self._parent:
            return self._parent.name + delimiter + self.name
        else:
            return self.name

    def self_range(self):
        """
        Get the string of range in [BIT_WIDTH-1:0] format
        """
        if self.bit_width == 1:
            return ""
        else:
            return "[" + str(self.bit_width - 1) + ":" + "0]"

    def full_range(self):
        """
        Get the string of range in [BIT_WIDTH+BIT_OFFSET-1:BIT_OFFSET] format
        """
        if self.bit_width == 1:
            return "[" + str(self.bit_width + self.bit_offset - 1) + "]"
        else:
            return "[" + str(self.bit_width + self.bit_offset - 1) + ":" + str(self.bit_offset - 1) + "]"


class Register:
    # Unique identifier
    name = None
    address_offset = None

    # Mandatory attributes
    _parent = None

    # Optional attributes
    description = None

    # Data storage
    _fields = None

    def __init__(self, name, address_offset=0, description='', parent=None):
        self.name = name
        self.address_offset = address_offset
        self._parent = parent
        self.description = description
        self._fields = list()

    def __len__(self):
        return self._fields.__len__()

    def __iter__(self):
        return iter(self._fields)

    def __getitem__(self, item):
        """
        Get the field in Register using the API:
        REG['FIELD_NAME']
        """
        return self.get_field(item)

    def __setitem__(self, key, value):
        """
        Add a new field in Register using the API:
        REG[31:0] = 'FIELD'
        """
        # Check different types of key
        if type(key) is int:
            # REG[0] = 'FIELD'
            bit_offset = key
            bit_width = 1
        elif type(key) is slice:
            if key.step:
                print("Reigster slice with none 1 step is not supported!\n")
                raise KeyError
            bit_offset = key.stop
            bit_width = key.start - key.stop + 1
        else:
            raise KeyError

        # Create a new Field
        field = Field(name=value, bit_offset=bit_offset, bit_width=bit_width, parent=self)

        # Add the filed to Register
        self.add_field(field)

    @staticmethod
    def from_tuple(t):
        """
        Build a Register from a tuple. The tuple should be in format:
        (name, description)
        """
        ret = Register(name=t(0), description=t(1))
        return ret

    @staticmethod
    def from_dict(d):
        """
        Build a Register Object from a dict. The dict should be in format:
        { 'name': name_of_register, 'description'=description_of_register }
        """
        ret = Register(name=d['name'], description=d['description'])
        return ret

    def add_field(self, field: Field):
        """
        Add a Field object to this Register
        """
        # Check if field name is occupy
        if self.has_field(field.name):
            raise ValueError

        # Check if overlap existing fields
        overlap = 0
        overlaped_field = None
        for f in self._fields:
            if not (field.bit_offset > (f.bit_offset + f.bit_width - 1) or
                    f.bit_offset > (field.bit_offset + field.bit_width - 1)):
                overlap = 1
                overlaped_field = f
                break
        if overlap:
            print("Overlap with field {0}".format(overlaped_field.full_name()))
            raise ValueError

        # Check pass, add this field
        self._fields.append(field)

    def has_field(self, name: str):
        """
        Test if given name of the field is exists in register
        """
        if type(name) is str:
            return name in {f.name for f in self._fields}
        else:
            raise TypeError

    def get_field(self, name: str):
        """
        Get the field in Register by name
        """
        if type(name) is str:
            idx = [f.name for f in self._fields].index(name)
            return self._fields[idx]
        else:
            raise TypeError


class RegisterMap:
    # Unique identifier
    name = ""

    # Required attributes
    base_address = 0
    data_width = 32
    address_width = 10

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
        """
        Provides a simplified API to instance Register in RegisterMap
        The format should like:
        REG_MAP[0] = 'CTRL'
        """
        if type(key) is not int:
            raise KeyError

        if type(value) is not str:
            raise ValueError

        # Create a new Register
        reg = Register(name=value, address_offset=key, parent=self)
        # Add it to the RegisterMap
        self.add_register(reg)

    def __getitem__(self, name_or_addr):
        return self.get_register(name_or_addr)

    def __len__(self):
        return self._registers.__len__()

    def has_register(self, name_or_addr):
        """
        Test if the given register exists in this RegisterMap, using the unique attribute `name` or `address_offset`
        """
        # Check if name exists
        if type(name_or_addr) is str:
            return name_or_addr in {r.name for r in self._registers}
        # Check if address offset exists
        elif type(name_or_addr) is int:
            return name_or_addr in {r.address_offset for r in self._registers}
        else:
            raise TypeError

    def get_register(self, name_or_addr):
        """
        Get the register with given name or address offset in map
        :param name_or_addr:
        :return:
        """
        if self.has_register(name_or_addr):
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

    def remove_register(self, name_or_addr):
        """
        Remove register in current map
        """
        t = self.get_register(name_or_addr)
        self._registers.remove(t)

    def clear_registers(self):
        """
        Remove all registers in current map, leave name and other attributes untouched
        """
        self._registers.clear()

    def add_register(self, reg: Register):
        if self.has_register(reg.name) or self.has_register(reg.address_offset):
            # Duplicate register
            raise ValueError
        # Append the new register to register list
        self._registers.append(reg)

    def drc(self):
        """
        DRC (Design Rule Check) function
        """
        # TODO
        print("Function \"drc\" not implemented!")

    def gen_verilog(self, output_file=None, template_file="template/bram.v"):
        # Render template
        t = Template(filename=template_file)
        s = t.render(regMap=self)

        # Output to file
        if not output_file:
            output_file = 'output/' + self.name + '.v'

        f = open(output_file, 'w')
        f.write(s)
        f.close()
