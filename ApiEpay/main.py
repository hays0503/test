import requests
from EpaymentHalyk import ApiEpaymentHalyk
import random

if __name__ == "__main__":
    


    base_url_auth = 'https://testoauth.homebank.kz' # Тестовый прод для авторизации URL auth
    base_url = 'https://testepay.homebank.kz' # Тестовый прод для авторизации URL auth
    username = 'cthtufgbv@mail.ru'
    password = 'UaJuSSK9QheUz4G!'
    client_id = 'web'
    client_secret = 'h$PvhiWrLn*d)B5I'

    epayment = ApiEpaymentHalyk(base_url_auth,base_url,username, password, client_id, client_secret)
    
    try:
        token_response = epayment.get_token()
        print(f'Данные авторизации токена: {token_response}\n')
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err}")


    #shop_id тестовый 
    shop_id="04f25a4b-d2bd-4dd8-b3a7-9390be4774c4" #ID магазина, выдается системой при регистрации магазина, обязательное
    
    account_id="001" #- номер счета магазина в системе epay, генериурется коммерсантом, обязательное
    invoice_id="002" #- уникальный идентификатор номера в системе магазина, генериурется коммерсантом, обазательное
    amount=9990 # - сумма счета, обязательное
    recipient_contact="cthtufgbv@mail.ru" # - электронный адрес получателя счета, обязательное
    recipient_contact_sms="+77763419116" # - номер мобильного телефона получателя счета в формате "+7XXXXXXXXXX", обязательное
    success_back_link="http://pimenov.kz:3000/" # - URL, на который будет перенаправлен пользователь после оплаты
    failure_back_link="http://pimenov.kz:3000/" # - URL, на который будет перенаправлен пользователь при ошибке оплаты
    try:

        link_response = epayment.create_payment_link(
            shop_id=shop_id,
            account_id=account_id,
            invoice_id=invoice_id,
            amount=amount,
            recipient_contact=recipient_contact,
            recipient_contact_sms=recipient_contact_sms,
            success_back_link=success_back_link,
            failure_back_link=failure_back_link
        )

        print(f'Данные ответа при создании ссылки на оплату: {link_response}\n')
        
        print(f'\033[1;32;40m Ссылка на оплату: {link_response["invoice_url"]} \033[0m\n\n')

    except requests.exceptions.HTTPError as err:
        print(f"Error: {err}")
