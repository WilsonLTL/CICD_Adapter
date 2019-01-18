from pocha import it,describe
import requests

@describe('connection test')
def _():
    @it('connect test1')
    def test1():
        url = "https://c68547c1.ngrok.io/push_message"
        payload = "{\n\t\"message\":\"somethings\"\n}"
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "7759277d-6293-49e5-b194-5b0a2085b1e1"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        assert(response.text == "...")

    @it('connect test2')
    def test2():
        url = "https://c68547c1.ngrok.io/push_message"
        payload = "{\n\t\"message\":\"somethings\"\n}"
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "7759277d-6293-49e5-b194-5b0a2085b1e1"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        assert (response.text == "...")