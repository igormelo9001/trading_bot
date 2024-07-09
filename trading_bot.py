import ccxt
import pandas as pd
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

    try:
        # Teste de conexão
        print("Conectando à Binance Futures Testnet...")
        exchange.load_markets()

        symbol = 'BTC/USDT'

        # Obtém o ticker mais recente
        ticker = exchange.fetch_ticker(symbol)

        # Organiza os dados do ticker em um DataFrame do Pandas
        df = pd.DataFrame([ticker])
        df = df[['symbol', 'timestamp', 'datetime', 'open', 'close', 'high', 'low', 'last', 'change', 'percentage', 'baseVolume', 'quoteVolume']]

        # Imprime os dados do ticker de forma organizada
        print("\nDados do Ticker:")
        print(df.to_string(index=False))

        # Lógica para decisão de operação contrária
        current_price = ticker['close']
        previous_price = ticker['open']

        if current_price > previous_price:
            # Se o preço atual for maior que o preço anterior, vende
            print("\nPreço atual é maior que o preço anterior. Venda iniciada.")
            order = exchange.create_market_sell_order(symbol, amount=0.001)
            print('Ordem de venda executada com sucesso!')
        elif current_price < previous_price:
            # Se o preço atual for menor que o preço anterior, compra
            print("\nPreço atual é menor que o preço anterior. Compra iniciada.")
            order = exchange.create_market_buy_order(symbol, amount=0.001)
            print('Ordem de compra executada com sucesso!')
        else:
            print("\nPreço atual é igual ao preço anterior. Nenhuma operação realizada.")

    except Exception as e:
        print(f"Erro ao executar operação: {e}")

if __name__ == '__main__':
    run_bot()
    # Lógica para decisão de operação de short/long
    current_price = ticker['close']
    previous_price = ticker['open']

    if current_price > previous_price:
        # Se o preço atual for maior que o preço anterior, vende
        print("\nPreço atual é maior que o preço anterior. Venda iniciada.")
        order = exchange.create_market_sell_order(symbol, amount=0.001)
        print('Ordem de venda executada com sucesso!')
    elif current_price < previous_price:
        # Se o preço atual for menor que o preço anterior, compra
        print("\nPreço atual é menor que o preço anterior. Compra iniciada.")
        order = exchange.create_market_buy_order(symbol, amount=0.001)
        print('Ordem de compra executada com sucesso!')
    else:
        print("\nPreço atual é igual ao preço anterior. Nenhuma operação realizada.")
        