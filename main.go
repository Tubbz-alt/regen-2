package main

import (
	"flag"
	"regen/regen"
)

func main() {

	flag.Parse()

	for _, file := range flag.Args() {
		err := regen.ParseJSON(file)
		if err != nil {
			panic(err)
		}
	}
}
