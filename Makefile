.PHONY: docker gofmt

image:
	docker build . --tag=images.local:5000/ups-metrics
	docker push images.local:5000/ups-metrics

docker: main
	docker-compose build && docker-compose up

go.mod:
	go mod init github.com/nihr43/ups-metrics

go.sum: go.mod
	go mod tidy

gofmt:
	gofmt main.go | sponge main.go

main: go.sum gofmt
	GO111MODULE=off CGO_ENABLED=0 go build main.go
