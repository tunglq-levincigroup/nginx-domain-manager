# A Record Integrations

## Add Domain

Registers a new domain and configures SSL using Certbot.

```json
Endpoint: POST /domain/add

Request:

curl -X POST http://{SERVER_IP}:{SERVER_PORT}/domain/add \
     -H "Content-Type: application/json" \
     -d '{"domain": {DOMAIN_NAME}}'

Response:
{
    "message": "Domain added successfully"
}
```

## Update Domain

Renames an existing domain.

```json
Endpoint: PUT /domain/edit

Request:

curl -X PUT http://{SERVER_IP}:{SERVER_PORT}/domain/edit \
     -H "Content-Type: application/json" \
     -d '{"new_domain": {DOMAIN_NAME}, "old_domain": {OLD_DOMAIN_NAME}}'

Response:

{
  "message": "Domain updated successfully",
  "old_domain": {OLD_DOMAIN_NAME},
  "new_domain": {DOMAIN_NAME}
}
```

## Remove Domain

Deletes an existing domain and its associated SSL configuration.

```json
Endpoint: DELETE /domain/remove

Request:

curl -X DELETE http://{SERVER_IP}:{SERVER_PORT}/domain/remove \
     -H "Content-Type: application/json" \
     -d '{"domain": {DOMAIN_NAME}}'

Response:

{
  "message": "Domain removed successfully",
  "domain": {DOMAIN_NAME}
}
```