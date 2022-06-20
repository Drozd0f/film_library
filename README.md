# REST-API сервис для управления фильмотекой
[![Dev Linter](https://github.com/Drozd0f/film_library/actions/workflows/linter.yml/badge.svg)](https://github.com/Drozd0f/film_library/actions/workflows/linter.yml)
[![Tests](https://github.com/Drozd0f/film_library/actions/workflows/tests.yml/badge.svg)](https://github.com/Drozd0f/film_library/actions/workflows/tests.yml)

## Practice project

> **Note**
> Dependencies

* Docker
* docker-compose
* Make

### Quick start

> **Note**
> First of all create .env file with next variables

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
SECRET_KEY="A SECRET KEY"
```

---
Run
```shell
make
```

> **Note**
> Application will be hosted on http://localhost

> **Note**
> Swagger documentation will be hosted on http://localhost/api-docs

---
Remove containers
```shell
make rm
```

---
To display container logs by name service
```shell
make log-"service-name"
```

### Run tests
```shell
make test-app
```

### Run tests without docker-compose.test
> **Note**
> Before run test set next variables

```
TEST_DB_URI="postgresql://test:test@localhost:5433/test"
SECRET_KEY="A SECRET KEY"
```

> **Warning**
> Expose port test database **5433**

---
First of all run container with test DB
```shell
make setup-testenv
```
* Run test by python

---
Stop test DB
```shell
make cleanup-testenv
```
