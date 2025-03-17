# Domain Integrations
## Variables

| Variable          | Description                           |
| -------------     | ------------------------              |
| `SERVER_IP`       | IP address of the server              |
| `SERVER_PORT`     | Port number for the API               |
| `API-KEY`         | API key for authorization             |
| `ERROR`           | The message error                     |
| `BASE_DOMAIN`     | The base domain of goright            |
| `TARGET_DOMAIN`   | The target domain to apply change     |
| `REDIRECT_DOMAIN` | The redirect domain to apply change   |
| `LIST_DOMAINS`    | List string pf domains to check dns   |

## check_dns

Endpoint: POST /dns/check

Request:
```bash
curl -X POST http://{SERVER_IP}:{SERVER_PORT}/dns/check \
     -H "Content-Type: application/json" \
     -H "X-API-KEY: {API-KEY}" \
     -d '{
            "domains": {LIST_DOMAINS}
        }'
```

Example:
```bash
curl -X POST http://68.183.228.52:8000/dns/check \
     -H "Content-Type: application/json" \
     -H "X-API-KEY: {API-KEY}" \
     -d '{
            "domains": ["brandlevinci.test88.info", "brandlevinci.test88.info"]
        }'
```

Example:
```bash
curl -X POST http://165.232.167.175:8000/dns/check \
     -H "Content-Type: application/json" \
     -H "X-API-KEY: {API-KEY}" \
     -d '{
            "domains": ["test4.levincitest.com", "www.test4.levincitest.com"]
        }'
```

Response:
- Success: Status Code = 200
```json
{
    "message": "All DNS records are correct."
}
```

- Fail: Status Code = 400
```json
{
    "message": {ERROR}
}
```

## Add config

Endpoint: POST /config/add

Request:
```bash
curl -X POST http://{SERVER_IP}:{SERVER_PORT}/config/add \
     -H "Content-Type: application/json" \
     -H "X-API-KEY: {API-KEY}" \
     -d '{
            "base_domain": {BASE_DOMAIN}, 
            "target_domain": {TARGET_DOMAIN}, 
            "redirect_domain": {REDIRECT_DOMAIN}
        }'
```

Example:
```bash
curl -X POST http://68.183.228.52:8000/config/add \
     -H "Content-Type: application/json" \
     -H "X-API-KEY: {API-KEY}" \
     -d '{
            "base_domain": "mobilezone.gorightstage.com", 
            "target_domain": "brandlevinci.test88.info", 
            "redirect_domain": "www.brandlevinci.test88.info"
        }'
```

Example:
```bash
curl -X POST http://165.232.167.175:8000/config/add  \
     -H "Content-Type: application/json" \
     -H "X-API-KEY: {API-KEY}" \
     -d '{
            "base_domain": "test4.test88.info", 
            "target_domain": "test4.levincitest.com", 
            "redirect_domain": "www.test4.levincitest.com"
        }'
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

## Remove Config

Endpoint: DELETE /config/remove

Request:
```bash
curl -X DELETE http://{SERVER_IP}:{SERVER_PORT}/config/remove \
     -H "Content-Type: application/json" \
     -H "X-API-KEY: {API-KEY}" \
     -d '{"target_domain": {TARGET_DOMAIN}}'
```

Example:
```bash
curl -X DELETE http://68.183.228.52:8000/config/remove  \
     -H "Content-Type: application/json" \
     -H "X-API-KEY: {API-KEY}" \
     -d '{
            "target_domain": "brandlevinci.test88.info"
        }'
```

Example:
```bash
curl -X DELETE http://165.232.167.175:8000/config/remove  \
     -H "Content-Type: application/json" \
     -H "X-API-KEY: {API-KEY}" \
     -d '{
            "target_domain": "test4.levincitest.com"
        }'
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
