from serpapi import GoogleSearch

params = {
  "engine": "google_jobs_listing",
  "q": "eyJqb2JfdGl0bGUiOiJDYWZmZSBNYWNzIEJhcmlzdGEiLCJodGlkb2NpZCI6Ik5wTmJiSmw2aVJTUXJRYk9BQUFBQUE9PSIsImZjIjoiRW93Q0Nzd0JRVXhQYm5CWlYyRkJXalZ2WmpGNE1GOUdkMVpNWms1Zk9HbFBOMHhNWHpZNFJERnlSR1pMU0d0dmFHVXlRbHA2ZUVWUmRGaHZjVEZWWVRWbmEzaDJaSEpzYUdZNVFUaHlWRXRoTjNKUFpUWXdSRTVVTTJsbWRUSjJZMkZYVDE5T2NHRm1ORlI1WWxOWGQyUkhWMlZRVlRWWmFXdFNVbUV0TVU1TldUbFVXRU51YlRSak9ISnJWR3RTWlhSaE5IcGFNMkZsWldVMGJtTXpiaTFUWm0xYVJ6RnNaRUZtY1VkUlZqQTRUVVJHVjFWNmMxWlFUVE5HY1hOTlNUWnljbGhpV0ZVeldqTkxiR1J2YzNOVkVoZGFVVk5UV21GZlNFTmtiWE0xVG05UWRUaHBUakpCV1JvaVFVcDNheTA0WlRkNWIxQmZVblUyT1Raa04zZzNWRVUwYTNCTE1VTkdSMVp0UVEiLCJmY3YiOiIzIiwiZmNfaWQiOiJmY18xIiwiYXBwbHlfbGluayI6eyJ0aXRsZSI6Ii5uRmcyZWJ7Zm9udC13ZWlnaHQ6NTAwfS5CaTZEZGN7Zm9udC13ZWlnaHQ6NTAwfUFwcGx5IG9uIENhcmVlcnMgQXQgQXBwbGUiLCJsaW5rIjoiaHR0cHM6Ly9qb2JzLmFwcGxlLmNvbS9lbi11cy9kZXRhaWxzLzIwMDUwNTM4MC9jYWZmZS1tYWNzLWJhcmlzdGE/dXRtX2NhbXBhaWduPWdvb2dsZV9qb2JzX2FwcGx5XHUwMDI2dXRtX3NvdXJjZT1nb29nbGVfam9ic19hcHBseVx1MDAyNnV0bV9tZWRpdW09b3JnYW5pYyJ9fQ==",
  "api_key": "secret_api_key"
}

search = GoogleSearch(params)
results = search.get_dict()