# Fake SMTP Server

Lightweight disposable email server with a REST API.

⚠️This project is meant for testing purposes only. Do not expose it publicly. Do not use it for production needs.⚠️

## Why ?

Some applications need to send emails. When implementing automatics tests, email features are often mocked and 
don't send real email, and it's a good thing to do !

However, sometimes, real email tests are needed. In this condition, receiving it in order to test what happens in 
real use cases can be a challenge. And like every test, it's better if it's automated. This project let you create a 
fake email server, and be able to read every email sent to it.

## Requirements

- A domain name (ex: `company.com`)
- A server with 25 port allowed to be used and exposed on Internet
- Docker / docker-compose

## Setup

1. Set the MX DNS field of the mail domain you want to use (ex: `fakemail.company.com`) to the IP address / hostname of 
   your server.
2. Clone this project on your server.
3. Edit the `docker-compose.yml` file, especially the `SS2A_APIKEY` value and the `ports` section if you want to use 
   a reverse proxy (see limitations).
4. `docker-compose up -d`
5. You should be able to receive any email sent to `*@fakemail.company.com` (where `*` is a wildcard)
6. The web API is accessible on `HTTP/5000` port. You should use a 

## Usage

All HTTP API endpoint are protected by a secret API key configured in `SS2A_APIKEY` environment variable (provided 
by the `docker-compose.yml`).

In order to perform any HTTP request, simply add a `SS2A-APIKEY` HTTP header, with corresponding value in all your 
requests.

### SMTP Server

Once started, the SMTP is not started by default and won't receive any email. The following API endpoints let you 
control the SMTP server:

- `GET /smtp/status/` returns a `status` providing SMTP server status.
- `POST /smtp/start/` start the SMTP server. Email should be received and store. A 3600s delay is then started before 
  auto stopping itself.
- `POST /smtp/stop/` stop the SMTP server.

## Retrieve emails

- `GET /emails/<email>/` (ex: `/emails/foobar@fakemail.company.com/`) returns an array with at most, the last 10 
  emails sent to this address.

## Limitations

- HTTPS is not provided by this application. If you need it (and you should !), put it behind a reverse proxy 
  enabling this feature (ex: [Traefik](https://doc.traefik.io/traefik/)).
- No persistent storage. If you restart the server, all data will be lost.
- Only last 10 messages per email address will be kept in memory.
- Due to Unix limited user permission, the docker file does not expose `25` but `2525`. You should translate the 
  port using `-p 25:2525` in Docker command line. This option is already implemented in the provided
 `docker-compose.yml` file.
