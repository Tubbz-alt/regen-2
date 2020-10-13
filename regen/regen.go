package regen

import (
	"encoding/json"
	"io/ioutil"
	"os"
	"text/template"
)

func ParseJSON(filename string) error {

	b, err := ioutil.ReadFile(filename)
	if err != nil {
		return err
	}

	data := Storage{}
	err = json.Unmarshal(b, &data)
	if err != nil {
		return err
	}

	tpl, err := template.ParseFiles("./template/axi4l.v.template")
	if err != nil {
		return err
	}
	err = tpl.ExecuteTemplate(os.Stdout, "axi4l.v.template", data)
	if err != nil {
		return err
	}

	return nil
}
