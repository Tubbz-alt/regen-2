//------------------------------------------------------------------------------
//
//  Copyright (C) 2020 kele14x
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU Affero General Public License as published
//  by the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU Affero General Public License for more details.
//
//  You should have received a copy of the GNU Affero General Public License
//  along with this program.  If not, see <https://www.gnu.org/licenses/>.
//
//------------------------------------------------------------------------------

package regen

import "sort"

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
	FieldTypeReadWrite    FieldType = "RW"  // Read write, output
	FieldTypeReadOnly               = "RO"  // Read only, input
	FieldTypeSelfClear              = "SC"  // Self clear, output
	// TODO: reverse for further implementation
	//FieldTypeReadWrite2Way          = "RW2"  // Read write, output
	//FieldTypeClearOnRead            = "CR"  // Clear on read, input
	//FieldTypeClearOnWrite           = "CW"  // Clear on write, input
	//FieldTypeCommand                = "CMD" // Command, output
	//FieldTypeGet                    = "GET" // FIFO Read like interface, input
	//FieldTypeSet                    = "SET" // FIFO Write like interface, output
)

// SortFields sort the fields in register
func (r *Register) SortFields() {
	sort.Slice(r.Fields, func(i, j int) bool {
		return r.Fields[i].BitOffset < r.Fields[j].BitOffset
	})
}

// SortRegisters sort the registers in register map
func (rm *RegisterMap) SortRegisters() {
	sort.Slice(rm.Registers, func(i, j int) bool {
		return rm.Registers[i].AddressOffset < rm.Registers[j].AddressOffset
	})
}

// Sort sorts all register and fields
func (s *Storage) Sort() {
	s.RegisterMap.SortRegisters()
	for _, r := range s.RegisterMap.Registers {
		r.SortFields()
	}
}
