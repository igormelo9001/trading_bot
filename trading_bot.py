import ccxt
import time
import config  # Arquivo onde você armazena suas chaves API de testnet

def run_bot():
    # Configuração do cliente da Binance Futures no testnet
    exchange = ccxt.binance({
        'apiKey': config.api_key,
        'secret': config.api_secret,
        'enableRateLimit': True,  # Habilita limitador de taxa
        'options': {
            'defaultType': 'future',
            'adjustForTimeDifference': True,
            'urls': {
                'api': 'https://testnet.binancefuture.com',
                'ws': 'wss://stream.binancefuture.com/ws',
            }
        }
    })

    # Teste de conexão
    print('Conectando à Binance Futures Testnet...')
    exchange.load_markets()

    symbol = 'BTC/USDT'
    timeframe = '1m'

    while True:
        try:
            # Obtém o ticker mais recente
            ticker = exchange.fetch_ticker(symbol)
            print(f"Ticker Data:\n{ticker}")

            # Lógica para decisão de operação contrária
            current_price = ticker['close']
            previous_price = ticker['open']

            if current_price > previous_price:
                # Se o preço atual for maior que o preço anterior, vende
                print(f"Preço atual ({current_price}) é maior que o preço anterior ({previous_price}). Venda iniciada.")
                order = exchange.create_market_sell_order(symbol, amount=0.001)
                print('Ordem de venda executada:', order)
            elif current_price < previous_price:
                # Se o preço atual for menor que o preço anterior, compra
                print(f"Preço atual ({current_price}) é menor que o preço anterior ({previous_price}). Compra iniciada.")
                order = exchange.create_market_buy_order(symbol, amount=0.001)
                print('Ordem de compra executada:', order)
            else:
                print("Preço atual é igual ao preço anterior. Nenhuma operação realizada.")

            # Aguarda 1 minuto antes de verificar novamente
            time.sleep(60)

        except Exception as e:
            print(f"Erro ao executar operação: {e}")
            time.sleep(10)  # Aguarda 10 segundos antes de tentar novamente

if __name__ == '__main__':
    run_bot()
