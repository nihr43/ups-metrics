.PHONY: docker gofmt

docker: main
	docker-compose build && docker-compose up

go.mod:
	go mod init ups-metrics

go.sum: go.mod
	go mod tidy

gofmt:
	gofmt main.go | sponge main.go

main: go.sum gofmt
	CGO_ENABLED=0 go build main.go
