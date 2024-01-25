package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

func main() {
	url := "https://lms.itaucultural.org.br/api/v1/courses?page=1&per_page=24&course_type=with_mediator"

	// Create a new HTTP client with custom headers
	client := &http.Client{}
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		log.Fatal(err)
	}

	req.Header.Set("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0")
	req.Header.Set("Accept", "application/json, text/plain, */*")
	req.Header.Set("Accept-Language", "en-US,en;q=0.5")
	req.Header.Set("Accept-Encoding", "gzip, deflate, br")
	req.Header.Set("Referer", "https://escola.itaucultural.org.br/")
	req.Header.Set("X-Organization-Name", "escola_ic")
	req.Header.Set("Origin", "https://escola.itaucultural.org.br")
	req.Header.Set("Sec-Fetch-Dest", "empty")
	req.Header.Set("Sec-Fetch-Mode", "cors")
	req.Header.Set("Sec-Fetch-Site", "same-site")
	req.Header.Set("Connection", "keep-alive")
	req.Header.Set("If-None-Match", "W/\"a535e7011691118f7a9ece9cf7178f13\"")

	// Make the HTTP request
	resp, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	// Check if the request was successful (status code 200)
	if resp.StatusCode == http.StatusOK {
		// Process JSON response
		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatal(err)
		}

		// Unmarshal JSON data
		var data map[string]interface{}
		err = json.Unmarshal(body, &data)
		if err != nil {
			log.Fatal(err)
		}

		// Process 'data' as needed
		fmt.Println("Request successful!")
		fmt.Println(data)
	} else {
		fmt.Printf("Request failed with status code: %d\n", resp.StatusCode)
		return
	}
}
