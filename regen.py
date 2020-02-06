from mako.template import Template
from typing import List
from typing import Union


class Field:
    """
    Field class model the **Field** in **Register**. Field is the atom object in Register Map generation, usually for
    one configuration/statistics parameter. One field can span multi-bits or at least one bit in Register. One
    Register can contain one or more fields.
    """

    def __init__(self, name: str, bit_offset=0, bit_width=1, access_type='RW', reset=0, description: str = None,
                 _parent: 'Register' = None) -> None:
        # Unique identify
        self._name = name
        self._bit_offset = bit_offset
        self._bit_width = bit_width

        # Mandatory attributes
        self.access_type = access_type
        self.reset = reset

        # Optional attributes
        self.description = description

        # Data storage
        self._parent = _parent

    def __cmp__(self, other) -> int:
        if self.bit_offset < other.bit_offset:
            return -1
        elif self.bit_offset > other.bit_offset:
            return 1
        else:
            return 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def bit_offset(self) -> int:
        return self._bit_offset

    @property
    def bit_width(self) -> int:
        return self._bit_width

    @property
    def left_bit(self) -> int:
        return self.bit_offset + self.bit_width - 1

    @property
    def right_bit(self) -> int:
        return self.bit_offset

    @property
    def self_range(self) -> str:
        """
        Get the string of range in "[BIT_WIDTH-1:0]" format
        :param: None
        :return: The range in string
        """
        if self.bit_width == 1:
            return ''
        else:
            return f'[{self.bit_width - 1}:0]'

    @property
    def full_range(self) -> str:
        """
        Get the string of range in [BIT_WIDTH+BIT_OFFSET-1:BIT_OFFSET] format
        :param: None
        :return: The full range in string
        """
        if self.bit_width == 1:
            return f'[{self.bit_offset + self.bit_width - 1}]'
        else:
            return f'[{self.bit_offset + self.bit_width - 1}:{self.bit_offset}]'

    @property
    def full_name(self) -> str:
        """
        Get the string of field name in "REGISTER.FIELD" format
        :param delimiter: The delimiter character that separates Register name and Filed name
        :return: The full name of field in string
        """
        if self._parent:
            return self._parent.name + '_' + self.name
        else:
            return self.name

    @staticmethod
    def from_dict(d: dict) -> "Field":
        """
        Build a Field object from a dict object (for easy parameter passing). Remember
        :param d: A dict object stores attribute information.
        :return: A Field object
        """
        if d.get('name'):
            ret = Field(name=d['name'])
        else:
            raise ValueError("'name' must be specified in dict's keys")

        # Override default values
        for a in ['bit_offset', 'bit_width', 'access_type', 'reset', 'description']:
            if d.get(a):
                setattr(ret, a, d[a])

        return ret


class Register:
    """
    Register class models **Registers** in **Register Map**. Register holds one or more fields. There can be one or
    more Registers in one Register Map. Registers in Register Map should have unique name and address offset. Fields
    in one Registers should not overlap with each other. Fields in one Register should have unique name. Bits not
    occupied by any fields are considered to be "reserved" (not writeable, reading returns zero).
    """

    def __init__(self, name: str, address_offset=0, description: str = None, _parent: 'RegisterMap' = None):
        # Unique identifier
        self._name = name
        self._address_offset = address_offset

        # Mandatory attributes

        # Optional attributes
        self.description = description

        # Data storage
        self._fields = list()
        self._parent = _parent

    def __len__(self):
        return self._fields.__len__()

    def __iter__(self):
        return iter(self._fields)

    def __getitem__(self, item: str) -> Field:
        """
        Get the field in Register using field's `name`.

        :param: Field's name.
        :return The required Field object.
        """

        if self.has_field(item):
            return self.get_field(item)
        else:
            raise KeyError

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
                print("Register slice with none 1 step is not supported!\n")
                raise KeyError
            bit_offset = key.stop
            bit_width = key.start - key.stop + 1
        else:
            raise KeyError

        # Create a new Field
        field = Field(name=value, bit_offset=bit_offset, bit_width=bit_width)

        # Add the filed to Register
        self.add_field(field)

    def __cmp__(self, other):
        if self.address_offset < other.address_offset:
            return -1
        elif self.address_offset > other.address_offset:
            return 1
        else:
            return 0

    @property
    def name(self):
        return self._name

    @property
    def address_offset(self):
        return self._address_offset

    @property
    def fields(self):
        return self._fields

    @property
    def fields_name_list(self):
        return [f.name for f in self._fields]

    @staticmethod
    def from_tuple(t):
        """
        Build a Register from a tuple. The tuple should be in format:
        (name, description)
        """
        if len(t) > 0:
            ret = Register(name=t(0), description=t(1))
        else:
            raise ValueError

        for i, a in enumerate(['address_offset', 'description']):
            if len(t) > i + 1:
                setattr(ret, a, t[i])

        return ret

    @staticmethod
    def from_dict(d):
        """
        Build a Register Object from a dict.
        :param d: A dict object holds the information in attributes
        :return: A Register object
        """
        if d.get('name'):
            ret = Register(name=d['name'])
        else:
            raise ValueError

        for a in ['address_offset', 'description']:
            if d.get(a):
                setattr(ret, a, d[a])

        return ret

    def has_field(self, name: str) -> bool:
        """
        Test if given name of the field is exists in register

        :param name: The name of the field
        :return: True if the field with given name exists, else False
        """

        # Check if name exists
        if type(name) is str:
            return name in [f.name for f in self._fields]
        else:
            raise TypeError('field name should in str')

    def get_field(self, name: str) -> Field:
        """
        Get the field in Register by name

        :param name: The name of the field
        :return: The field with the given name
        """

        if type(name) is str:
            nl = [f.name for f in self._fields]
            if name in nl:
                idx = nl.index(name)
                return self._fields[idx]
            else:
                raise KeyError('no field with given name')
        else:
            raise TypeError('field name should in str')

    def remove_field(self, name: str) -> None:
        """
        Remove Field from this Register

        :param name: The name of the field to be removed
        :return: None
        """

        f = self.get_field(name)
        if f:
            self._fields.remove(f)
        else:
            raise ValueError('nothing to remove')

    def clear_fields(self) -> None:
        """
        Clear all fields without touching other parameters

        :return: None
        """
        self._fields.clear()

    def add_field(self, field: Field) -> None:
        """
        Add a Field object to this Register

        :param field: The Field object to be add
        :return: If add operation is success
        """

        # Check if field name is occupy
        if self.has_field(field.name):
            raise ValueError('duplicate name of field')

        # Check if overlap with existing fields
        overlapped_field: Union[Field, None] = None
        for f in self._fields:
            if not (field.bit_offset > (f.bit_offset + f.bit_width - 1) or
                    f.bit_offset > (field.bit_offset + field.bit_width - 1)):
                overlapped_field = f
                break
        if overlapped_field:
            raise ValueError(f'Overlap with existing field {overlapped_field.full_name}')

        # Check pass, add this field
        field._parent = self
        self._fields.append(field)
        self._fields.sort(key=lambda x: x.bit_offset, reverse=True)

    def drc(self) -> bool:
        """
        DRC (Design Rule Check) function

        :return: True if the DRC is pass, false if and DRC is violated
        """

        # TODO
        raise SystemError('drc function is not implemented')


class RegisterMap:
    """
    **RegisterMap** models the Register Map. A Register Map is a "block" which will generate a Verilog module. One
    Register Map contains one or more Registers. Registers in one Map should have unique name and address offset.
    """

    def __init__(self, name: str, base_address=0, data_width=32, address_width=0, description: str = None) -> None:
        # Unique identifier
        self._name = name

        # Required attributes
        self.base_address = base_address
        self.data_width = data_width
        self.address_width = address_width

        # Optional attributes
        self.description = description

        # Data storage
        self._registers = list()

    def __iter__(self):
        return iter(self._registers)

    def __setitem__(self, key: int, value: str) -> None:
        """
        Provides a simplified API to instance Register in RegisterMap
        The format should like:
        REG_MAP[0] = 'CTRL'

        :param key: The address offset of new Register
        :param value: The name of new Register
        :return: None
        """

        # Create a new Register
        reg = Register(name=value, address_offset=key)

        # Add it to the RegisterMap
        self.add_register(reg)

    def __getitem__(self, name_or_addr):
        if self.has_register(name_or_addr):
            return self.get_register(name_or_addr)
        else:
            raise KeyError(name_or_addr)

    def __len__(self):
        return self._registers.__len__()

    @property
    def name(self):
        return self._name

    @property
    def registers(self):
        return self._registers

    @property
    def registers_name_list(self):
        return [r.name for r in self._registers]

    def has_register(self, name_or_addr: Union[str, int]) -> bool:
        """
        Test if the given register exists in this RegisterMap, using the unique attribute `name` or `address_offset`.

        :param name_or_addr: The name or the address offset of the register
        :return: True if the map has the desired register, else False
        """

        # Check if name exists
        if type(name_or_addr) is str:
            return name_or_addr in {r.name for r in self._registers}
        # Check if address offset exists
        elif type(name_or_addr) is int:
            return name_or_addr in {r.address_offset for r in self._registers}
        else:
            raise TypeError('name_or_addr should be str or int')

    def get_register(self, name_or_addr: Union[str, int]) -> Register:
        """
        Get the register with given `name` or `address offset` in map

        :param name_or_addr: The name or address offset of the register
        :return: The desired register with given name or address offset
        """

        if type(name_or_addr) is str:
            nl = [r.name for r in self._registers]
            if name_or_addr in nl:
                idx = nl.index(name_or_addr)
                return self._registers[idx]
            else:
                raise KeyError('no register with given name')
        elif type(name_or_addr) is int:
            al = [r.address_offset for r in self._registers]
            if name_or_addr in al:
                idx = al.index(name_or_addr)
                return self._registers[idx]
            else:
                raise ValueError('no register with given address offset')
        else:
            raise TypeError('name_or_addr should be str or int')

    def remove_register(self, name_or_addr: Union[str, int]) -> None:
        """
        Remove register in current map

        :param name_or_addr: The name or the address of the Register to be removed
        :return: None
        """

        t = self.get_register(name_or_addr)
        if t:
            self._registers.remove(t)
        else:
            raise ValueError('nothing to remove')

    def clear_registers(self) -> None:
        """
        Remove all registers in current map, leave name and other attributes untouched

        :return: None
        """

        self._registers.clear()

    def add_register(self, reg: Register) -> None:
        """
        Add a Register object to internal register list. If duplicate identity (`name`, `address_offset`) found,
        an error is raise.

        :param reg: The Register object to be added
        :return: None
        """

        # Duplicate check
        if self.has_register(reg.name):
            raise ValueError('duplicate name of register')

        if self.has_register(reg.address_offset):
            raise ValueError('duplicate address offset of register')

        # Append the new register to register list
        reg._parent = self
        self._registers.append(reg)
        self._registers.sort(key=lambda x: x.address_offset)

    def drc(self) -> bool:
        """
        DRC (Design Rule Check) function

        :return: True if the DRC is pass, false if any DRC is violated
        """

        # TODO
        raise SystemError('drc function is not implemented')

    def gen_verilog(self, output_file: str = None, template_file="template/bram.v") -> None:
        """
        Generate the Verilog file from the Register Map.

        :param output_file: Path of output file.
        :param template_file: The template file to use when generating the Verilog file
        :return: None
        """

        # Render template
        t = Template(filename=template_file)
        s = t.render(regMap=self)

        # Output to file
        if not output_file:
            output_file = 'output/' + self.name + '.v'

        f = open(output_file, 'w')
        f.write(s)
        f.close()
