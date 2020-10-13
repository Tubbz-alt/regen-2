package regen

// Storage represents data storage of the file
type Storage struct {
	JSONVersion int         `json:"json_version"` // JSON file Version
	RegisterMap RegisterMap `json:"register_map"` // The register map
}

// RegisterMap represents one register map (block)
type RegisterMap struct {
	Name        string     `json:"name"`         // Name of the register map
	Description string     `json:"description"`  // Description of the register map
	Width       int        `json:"width"`        // Data width of register map
	BaseAddress int        `json:"base_address"` // Default base address of register map in system address space
	Registers   []Register `json:"registers"`    // Registers in register map
}

// Register represents one register in register map
type Register struct {
	Type          RegisterType `json:"type"`           // Type of the register, could be "REGISTER", "MEMORY" or "ARRAY"
	Name          string       `json:"name"`           // Name of the register
	Description   string       `json:"description"`    // Description of the register
	AddressOffset int          `json:"address_offset"` // Address offset of the register
	MemoryDepth   int          `json:"memory_depth"`   // Memory depth of the register, only applicable to "MEMORY" type register
	ArrayLength   int          `json:"array_length"`   // Array length of register, only applicable to "ARRAY" type register
	ArrayStep     int          `json:"array_step"`     // Array step of register, only applicable to "ARRAY" type register
	Fields        []Field      `json:"fields"`         // Fields in register
}

type RegisterType string

const (
	RegisterTypeRegister  RegisterType = "NORMAL"    // Normal register
	RegisterTypeArray                  = "ARRAY"     // Array of normal register
	RegisterTypeMemory                 = "MEMORY"    // Shared memory
	RegisterTypeInterrupt              = "INTERRUPT" // Interrupt register
)

// Field represents one field in register, one filed can span multiple bits
type Field struct {
	Type        FieldType   `json:"type"`        // Type of the field, can be any of FieldType
	Name        string      `json:"name"`        // Name of the field
	Description string      `json:"description"` // Description of the field
	BitOffset   int         `json:"bit_offset"`  // Bit offset of the filed
	BitWidth    int         `json:"bit_width"`   // Bit width of the field
	ResetValue  int         `json:"reset_value"` // Reset value of the field
	EnumValues  []EnumValue `json:"enum_values"` // Enumerated value of the field
}

// EnumValue represents the enumerated value of the field
type EnumValue struct {
	Name  string `json:"name"`
	Value int    `json:"value"`
}

type FieldType string

const (
	FieldTypeReadWrite    FieldType = "RW"  // Read write
	FieldTypeReadOnly               = "RO"  // Read only
	FieldTypeSelfClear              = "SC"  // Self clear
	FieldTypeClearOnRead            = "CR"  // Clear on read
	FieldTypeClearOnWrite           = "CW"  // Clear on write
	FieldTypeCommand                = "CMD" // Command
	FieldTypeGet                    = "GET" // FIFO Read like interface
	FieldTypeSet                    = "SET" // FIFO Write like interface
)
