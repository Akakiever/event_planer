To run  a project in a standard mode run 
1. Install docker
2. Install docker compose
3. Start database
```bash
docker compose up -d db redis
```
4. Build images
```bash
docker compose build
```
5. Apply migrations
```bash
docker compose run --rm app python3 manage.py migrate
```
6. Run application 
```bash
docker compose up app worker
```

To access the service go to http://127.0.0.1:8000/

To run tests 
```bash
docker compose run --rm app pytest
```