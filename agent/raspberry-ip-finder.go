package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
//	"io/ioutil"
	"log"
	"net"
	"net/http"
	"os"
)

type RaspberryStatus struct {
	IP   string
	Host string
	MAC  string
}

func main() {
	//url := "raspberry-pi.seoultechsciety.org"
	url := flag.String("url", "http://localhost:8080", "A URL to server")
	flag.Parse()

	var hostname, _ = getHostname()
	var mac, ip, _ = getLocalIP()
	log.Printf("Host: %v\n  IP: %v MAC: %s\n", hostname, ip.String(), mac)

	message := &RaspberryStatus{ip.String(), hostname, mac.String()}
	message.sendToServer(*url)
}

func (status *RaspberryStatus) sendToServer(url string) {
	json, err := json.Marshal(status)
	if err != nil {
		log.Fatal("Unable to marshal RaspberryStatus: %v\n", status)
	}
	//log.Printf("Sening JSON: %s", json)

	resp, err := http.Post(url+"/ip.post", "application/json", bytes.NewReader(json))
	if err != nil {
		// TODO(alex): handle error - wait and re-try
		log.Fatal("Request to server failed: ", err)
		return
	}
	defer resp.Body.Close()
	//body, err := ioutil.ReadAll(resp.Body)
	//log.Printf("%s", body)
}

func getLocalIP() (net.HardwareAddr, net.IP, error) {
	interfaces, err := net.Interfaces()
	if err != nil {
		return nil, nil, err
	}
	for _, inter := range interfaces {
		aa, err := inter.Addrs()
		if err != nil {
			return nil, nil, err
		}
		for _, a := range aa {
			ipnet, ok := a.(*net.IPNet)
			if !ok {
				continue
			}
			v4 := ipnet.IP.To4()
			if v4 == nil || v4[0] == 127 { // loopback address
				continue
			}
			return inter.HardwareAddr, v4, nil
		}
	}
	return nil, nil, errors.New("cannot find local IP address")
}

func getHostname() (string, error) {
	host, err := os.Hostname()
	if err != nil {
		fmt.Printf("Oops: %v\n", err)
		return "", errors.New("cannot find local hostname")
	}
	return host, nil
}
