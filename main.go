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

	"github.com/nihr43/ups-metrics/models"
)

func snmp_get(address string, oid string) g.SnmpPDU {
	g.Default.Target = address
	g.Default.Version = g.Version1
	err := g.Default.Connect()
	if err != nil {
		log.Fatalf("Connect() err: %v", err)
	}
	defer g.Default.Conn.Close()

	oids := []string{oid}
	result, err2 := g.Default.Get(oids) // Get() accepts up to g.MAX_OIDS
	if err2 != nil {
		log.Fatalf("Get() err: %v", err2)
	}

	fmt.Printf("oid: %s ", result.Variables[0].Name)

	// the Value of each variable returned by Get() implements
	// interface{}. You could do a type switch...
	switch result.Variables[0].Type {
	case g.OctetString:
		bytes := result.Variables[0].Value.([]byte)
		fmt.Printf("string: %s\n", string(bytes))
	default:
		// ... or often you're just interested in numeric values.
		// ToBigInt() will return the Value as a BigInt, for plugging
		// into your calculations.
		fmt.Printf("number: %d\n", g.ToBigInt(result.Variables[0].Value))
	}
	return result.Variables[0]
}

func HomeHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("HomeHandler")

	fmt.Fprintf(w, "see /ups")
}

func UpsHandler(snmp_address string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		log.Println("UpsHandler")

		// TODO: figure out more elegant way to handle two possible return types
		this_ups := &ups{Model: string(snmp_get(snmp_address, "1.3.6.1.2.1.33.1.1.2.0").Value.([]byte)),
			Load:       g.ToBigInt(snmp_get(snmp_address, "1.3.6.1.2.1.33.1.4.4.1.5.1").Value),
			Temp:       g.ToBigInt(snmp_get(snmp_address, "1.3.6.1.2.1.33.1.2.7.0").Value),
			Ac_voltage: g.ToBigInt(snmp_get(snmp_address, "1.3.6.1.2.1.33.1.3.3.1.3.1").Value)}
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
