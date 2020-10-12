package regen

import "encoding/json"

type FieldType string

const (
	RW  FieldType = "RW"  // Read write
	RO  FieldType = "RO"  // Read only
	SC  FieldType = "SC"  // Self clear
	CR  FieldType = "CR"  // Clear on read
	GET FieldType = "GET" // FIFO Read like interface
	SET FieldType = "SET" // FIFO Write like interface
)

type Field struct {
	Name    string
	Type    FieldType
	Offset  int
	Width   int
	Comment string
}

type Register struct {
	Name    string
	Address int
	Comment string
	Fields  []Field
}

type Block struct {
	Name        string
	BaseAddress int
	Registers   []Register
}

func FromJSON(jsonBlob []byte) (*Block, error) {
	blk := &Block{}

	err := json.Unmarshal(jsonBlob, blk)
	if err != nil {
		return nil, err
	}

	return blk, nil
}

