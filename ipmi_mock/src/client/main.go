package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

var _interface, address, user, password, port string

func main() {
	ipmiMockConfigAddress := os.Getenv("IPMI_MOCK_CONFIG_ADDRESS")
	if ipmiMockConfigAddress == "" {
		ipmiMockConfigAddress = "127.0.0.1:41000"
	}
	flag.StringVar(&_interface, "I", "", "")
	flag.StringVar(&address, "H", "", "Remote server address, can be IP address or hostname. This option is required for lan and lanplus interfaces.")
	flag.StringVar(&user, "U", "", "")
	flag.StringVar(&password, "P", "", "")
	flag.StringVar(&port, "p", "41000", "")
	flag.Parse()
	if len(flag.Args()) > 0 {
		resp, err := http.Get(
			fmt.Sprintf(
				"http://%s/%s?ip=%s",
				ipmiMockConfigAddress,
				flag.Args()[0],
				address,
			),
		)
		if err != nil {
			log.Fatal(err)
		}
		if flag.Args()[0] == "status" {
			data, err := ioutil.ReadAll(resp.Body)
			if err != nil {
				log.Fatal(err)
			}
			fmt.Printf("Chassis Power is %s\n", data)
		}
	}
}
