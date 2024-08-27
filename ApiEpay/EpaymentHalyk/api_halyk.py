import requests


class ApiEpaymentHalyk:
    def __init__(
        self, base_url_auth, base_url, username, password, client_id, client_secret
    ):
        self.base_url_auth = base_url_auth
        self.base_url = base_url
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret

    def get_token(self, referer="https://test-epay.homebank.kz/"):
        """
        Получает OAuth2 токен для дальнейших запросов к API.

        :param referer: URL, который будет указан в заголовке Referer.
        :return: json {
                "access_token": "string",
                "expires_in": number,
                "scope": "текущий скоп где этот токен может использоваться",
                "token_type": "Bearer"
            }.
        """
        url = f"{self.base_url_auth}/epay2/oauth2/token"
        headers = {
            "Accept": "*/*",
            "Accept-Language": "ru,en;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded",
            "Sec-CH-UA": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "Sec-CH-UA-Mobile": "?1",
            "Sec-CH-UA-Platform": '"Android"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Referer": referer,
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }

        data = {
            "grant_type": "password",
            "scope": "webapi usermanagement email_send verification statement statistics payment",
            "username": self.username,
            "password": self.password,
            "client_id": "web",
            "client_secret": "h$PvhiWrLn*d)B5I",
        }

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            json = response.json()
            self.token = json["access_token"]
            print(f'\033[1;32;40m Token {self.token} \033[0m')
            return json
        else:
            print(response.text)
            response.raise_for_status()

    def create_payment_link(
        self,
        shop_id:str,
        account_id:str,
        invoice_id:str,
        amount:int,
        recipient_contact:str,
        recipient_contact_sms:str,
        success_back_link:str,
        failure_back_link:str,
        description:str="Тестовый заказ",
        language:str="rus",
        currency:str="KZT",
        expire_period:str="3d",
        postLink:str="",
        failurePostLink:str="",
        referer:str="https://test-epay.homebank.kz/",
    ):
        """
        Создает ссылку на оплату.
        """
        if not self.token:
            raise ValueError("Access token is missing. Please authenticate first.")

        url = f"{self.base_url}/api/invoice"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Sec-CH-UA": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "Sec-CH-UA-Mobile": "?1",
            "Sec-CH-UA-Platform": '"Android"',
            "Referer": referer,
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }
        
        data = {
            "shop_id": shop_id,
            "account_id": account_id,
            "invoice_id": invoice_id,
            "amount": amount,
            "language": language,
            "description": description,
            "expire_period": expire_period,
            "recipient_contact": recipient_contact,
            "recipient_contact_sms": recipient_contact_sms,
            "notifier_contact_sms": recipient_contact_sms,
            "currency": currency,
            "post_link": postLink,
            "failure_post_link": failurePostLink,
            "back_link": success_back_link,
            "failure_back_link": failure_back_link,
        }

        print(data)

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'\033[1;31;41m {response.text} \033[0m\n\n')
            response.raise_for_status()