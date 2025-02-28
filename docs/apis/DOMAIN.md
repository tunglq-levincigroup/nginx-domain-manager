# Domain Integrations
## Variables

| Variable          | Description                           |
| -------------     | ------------------------              |
| `SERVER_IP`       | IP address of the server              |
| `SERVER_PORT`     | Port number for the API               |
| `API-KEY`         | API key for authorization             |
| `ERROR`           | The message error                     |
| `BASE_DOMAIN_NAME`| The base domain of goright            |
| `OLD_DOMAIN_NAME` | The old domain client choosing before |
| `DOMAIN_NAME`     | The main domain to apply change       |

## Add Domain

Endpoint: POST /domain/add

Request:
```bash
curl -X POST http://{SERVER_IP}:{SERVER_PORT}/domain/add \
     -H "Content-Type: application/json" \
     -H "X-API-KEY: {API-KEY}" \
     -d '{"base_domain": {BASE_DOMAIN_NAME}, "domain": {DOMAIN_NAME}'
```

Response:
- Success: Status Code = 200
```json
{
    "message": "Domain added successfully"
}
```

- Fail: Status Code = 400
```json
{
    "message": {ERROR}
}
```

## Edit Domain

Endpoint: PUT /domain/edit

Request:
```bash
curl -X PUT http://{SERVER_IP}:{SERVER_PORT}/domain/edit \
     -H "Content-Type: application/json" \
     -H "X-API-KEY: {API-KEY}" \
     -d '{"base_domain": {BASE_DOMAIN_NAME}, "old_domain": {DOMAIN_NAME}, "domain": {DOMAIN_NAME}'
```

Response:
- Success: Status Code = 200
```json
{
    "message": "Domain edited successfully"
}
```

- Fail: Status Code = 400
```json
{
    "message": {ERROR}
}
```

## Remove Domain

Endpoint: DELETE /domain/remove

Request:
```bash
curl -X DELETE http://{SERVER_IP}:{SERVER_PORT}/domain/remove \
     -H "Content-Type: application/json" \
     -H "X-API-KEY: {API-KEY}" \
     -d '{"domain": {DOMAIN_NAME}'
```

Response:
- Success: Status Code = 200
```json
{
    "message": "Domain removed successfully"
}
```

- Fail: Status Code = 400
```json
{
    "message": {ERROR}
}
```

