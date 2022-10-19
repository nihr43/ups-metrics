package main

import (
	"log"
	"time"
	"net/http"
	"io/ioutil"
	"encoding/json"

	"../models"
)

func main() {
	// mostly copypasta from https://blog.alexellis.io/golang-json-api-client/
	url := "http://10.0.100.6:8080/ups"
	log.Println(url)

	client := http.Client{
		Timeout: time.Second * 2,
	}

	req, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
		log.Fatal(err)
	}

	res, getErr := client.Do(req)
	if getErr != nil {
		log.Fatal(getErr)
	}

	if res.Body != nil {
		defer res.Body.Close()
	}

	body, readErr := ioutil.ReadAll(res.Body)
	if readErr != nil {
		log.Fatal(readErr)
	}

	this_ups := models.Ups{}
	jsonErr := json.Unmarshal(body, &this_ups)
	if jsonErr != nil {
		log.Fatal(jsonErr)
	}

	log.Println(this_ups.Model)
	log.Println(this_ups.Load)
}
