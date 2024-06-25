# Travelpicker Backend API

# Build

```
docker build -t travelpicker:test -f docker/Dockerfile .
```

# Setup Env file

```
touch .env
```

아래 링크에서 환경 변수 값들을 복사하여 .env 파일에 저장하기  
https://www.notion.so/0b61d8bdd174426fadefc4f35e4170bc

# Run

```
docker-compose -f docker/compose.yaml --env-file .env up -d
```

아래 swagger 문서 접속되는지 확인  
http://localhost:8000/docs

# Stop

```
docker-compose -f docker/compose.yaml down
```
