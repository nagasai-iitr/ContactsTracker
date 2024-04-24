# Contacts Tracker API

Welcome to the Contacts Tracker API! This Django application provides a simple API endpoint for identifying contacts based on email and phone number inputs.

## API Endpoint

The API endpoint is exposed at:

https://contactstracker.onrender.com/identify


## Input

The API accepts JSON input with two variables:

1. `email`: Email address of the contact.
2. `phoneNumber`: Phone number of the contact.

Example input JSON:
```json
{
    "email": "example@example.com",
    "phoneNumber": "+1234567890"
}
```

## Output

The API returns a JSON object with the following format:
```
{
    "contact": {
        "primaryContactId": number,
        "emails": string[], // First element being the email of the primary contact.
        "phoneNumbers": string[], // First element being the phone number of the primary contact.
        "secondaryContactIds": number[] // Array of all contact IDs that are "secondary" to the primary contact.
    }
}
```

## Example Response

Example response JSON:

```json
{
    "contact": {
        "primaryContactId": 1,
        "emails": ["example@example.com", "secondary@example.com"],
        "phoneNumbers": ["+1234567890", "+0987654321"],
        "secondaryContactIds": [2, 3]
    }
}
```

## Usage

You can use any HTTP client to send a POST request to the API endpoint mentioned above. Include the input JSON in the request body. Here's an example using cURL:
```
curl -X POST -H "Content-Type: application/json" -d '{"email": "example@example.com", "phoneNumber": "+1234567890"}' https://contactstracker.onrender.com/identify
```


