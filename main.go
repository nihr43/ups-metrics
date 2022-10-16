package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gorilla/mux"
	g "github.com/gosnmp/gosnmp"
)

type ups struct {
	Name  string
	Watts int
	Temp  int
}

func HomeHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("HomeHandler")

	fmt.Fprintf(w, "see /ups")
}

func UpsHandler(snmp_address string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		log.Println("UpsHandler")

		g.Default.Target = snmp_address
		err := g.Default.Connect()
		if err != nil {
			log.Fatalf("Connect() err: %v", err)
		}
		defer g.Default.Conn.Close()

		this_ups := &ups{Name: snmp_address, Watts: 300, Temp: 30}
		this_ups_json, err := json.Marshal(this_ups)
		if err != nil {
			log.Println(err)
			return
		}

		fmt.Fprintf(w, string(this_ups_json))
	}
}

func main() {
	r := mux.NewRouter()
	http.Handle("/", r)

	snmp_address := os.Getenv("SNMP_ADDRESS")

	r.HandleFunc("/", HomeHandler)
	r.HandleFunc("/ups", UpsHandler(snmp_address))

	srv := &http.Server{
		Addr: "0.0.0.0:8080",
		// Good practice to set timeouts to avoid Slowloris attacks.
		WriteTimeout: time.Second * 15,
		ReadTimeout:  time.Second * 15,
		IdleTimeout:  time.Second * 60,
		Handler:      r, // Pass our instance of gorilla/mux in.
	}

	if err := srv.ListenAndServe(); err != nil {
		log.Println(err)
	}
}
