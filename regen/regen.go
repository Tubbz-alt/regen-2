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

import (
	"encoding/json"
	"io/ioutil"
	"os"
	"strings"
	"text/template"
)

func ParseJSON(filename string) error {

	// Read JSON file
	b, err := ioutil.ReadFile(filename)
	if err != nil {
		return err
	}

	// Unmarshal the JSON string into storage data
	data := Storage{}
	err = json.Unmarshal(b, &data)
	if err != nil {
		return err
	}

	// Preprocess storage data
	data.Sort()

	// Helper functions during render template
	funcMap := template.FuncMap{
		"ToLower": strings.ToLower,
		"ToUpper": strings.ToUpper,
		"add": func(x int, y int) int {
			return x + y
		},
	}
	// Create template from template file
	tpl := template.New("axi4l.v.template").Funcs(funcMap)
	_, err = tpl.ParseFiles("./template/axi4l.v.template")
	if err != nil {
		return err
	}

	// Render template
	// TODO: save into file
	err = tpl.ExecuteTemplate(os.Stdout, "axi4l.v.template", data)
	if err != nil {
		return err
	}

	return nil
}
