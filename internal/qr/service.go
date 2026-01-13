package qr

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

type Service struct {
	BaseURL string
	Client  *http.Client
}

func New(baseURL string) *Service {
	return &Service{
		BaseURL: baseURL,
		Client:  http.DefaultClient,
	}
}

func (s *Service) Generate(text string) ([]byte, error) {
	payload := map[string]string{"text": text}
	body, err := json.Marshal(payload)
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest(
		http.MethodPost,
		s.BaseURL+"/generate-qr",
		bytes.NewBuffer(body),
	)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := s.Client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("qr service returned %s", resp.Status)
	}

	return io.ReadAll(resp.Body)
}
