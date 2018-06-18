package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strings"
)

var relIPServerName map[string]string // ServerIP / ServerName
var configFile string

func loadConfig() {
	relIPServerName = make(map[string]string)
	log.Printf("Load %s config file", configFile)
	content, err := ioutil.ReadFile(configFile)
	if err != nil {
		log.Panic(err)
	}
	for _, line := range strings.Split(string(content), "\n") {
		line = strings.Trim(line, " ")
		if line == "" {
			continue
		}
		splited := strings.Split(line, " ")
		relIPServerName[splited[0]] = splited[1]
	}

}

func callVagrantAction(state string, serverName string) error {
	log.Printf("callVagrantAction state=%s serverName=%s", state, serverName)
	path, err := exec.LookPath("vagrant")
	if err != nil {
		return err
	}
	var cmd *exec.Cmd
	switch {
	case state == "on":
		log.Printf("Execute: %s up %s --no-provision", path, serverName)
		cmd = exec.Command(path, "up", serverName, "--no-provision")
	case state == "off" || state == "cycle":
		log.Printf("Execute: %s halt %s", path, serverName)
		cmd = exec.Command(path, "halt", serverName)
	default:
		return nil
	}
	log.Println(strings.Join(cmd.Args, " "))
	err = cmd.Start()
	if err != nil {
		return err
	}
	go func() {
		err = cmd.Wait()
		if err != nil {
			log.Print(err)
		}
		if state == "cycle" {
			err = callVagrantAction("on", serverName)
			if err != nil {
				log.Print(err)
			}
		}
	}()

	return nil
}

func getVagrantStatus(serverName string) (string, error) {
	path, err := exec.LookPath("vagrant")
	if err != nil {
		return "", err
	}
	cmd := exec.Command(path, "status", serverName, "--machine-readable")
	output, err := cmd.Output()
	if err != nil {
		return "", err
	}
	for _, line := range strings.Split(string(output), "\n") {
		splited := strings.Split(line, ",")
		if splited[1] == serverName {
			if splited[2] == "state" {
				if splited[3] == "running" {
					return "on", nil
				} else {
					return "off", nil
				}
			}
		}
	}
	return "off", nil
}

func handler(w http.ResponseWriter, r *http.Request) {
	action := strings.Trim(r.URL.Path, "/")
	ip := r.URL.Query().Get("ip")
	serverName, ok := relIPServerName[ip]
	if !ok {
		log.Printf("Server %s not found", ip)
	}
	if ok {
		log.Printf("Execute IPMI %s on %s", action, ip)
		if action == "status" {
			response, err := getVagrantStatus(serverName)
			if err != nil {
				log.Fatal(err)
			}
			fmt.Println(response)
			fmt.Fprintf(w, response)
		} else {
			err := callVagrantAction(action, serverName)
			if err != nil {
				log.Fatal(err)
			}
		}
	}
}

func main() {
	configFile = os.Getenv("CONFIG_FILE")
	if configFile == "" {
		log.Fatal("You must set CONFIG_FILE variable env")
	}
	loadConfig()
	listenAddress := os.Getenv("LISTEN_ADDRESS")
	if listenAddress == "" {
		listenAddress = "0.0.0.0:41000"
	}
	http.HandleFunc("/", handler)
	log.Printf("Listen on %s\n", listenAddress)
	log.Fatal(http.ListenAndServe(listenAddress, nil))
}
