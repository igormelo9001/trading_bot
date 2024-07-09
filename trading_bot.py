import ccxt
import config
import time
import pandas as pd

# Configurar a corretora (usando a Binance Testnet)
exchange = ccxt.binance({
    'apiKey': config.API_KEY,
    'secret': config.API_SECRET,
    'enableRateLimit': True,
    'urls': {
        'api': {
            'public': 'https://testnet.binance.vision/api/v3',
            'private': 'https://testnet.binance.vision/api/v3',
        },
    },
})

# Verificar se as chaves de API são carregadas corretamente
print(f"API Key: {exchange.apiKey}")
print(f"API Secret: {exchange.secret}")

# Definir a estratégia de trading (exemplo simples de média móvel)
def trading_strategy(ticker_data):
    closes = [ticker_data['close']]
    if len(closes) < 20:
        return None

    short_ma = sum(closes[-5:]) / 5
    long_ma = sum(closes[-20:]) / 20

    if short_ma > long_ma:
        return 'long'
    elif short_ma < long_ma:
        return 'short'
    return None

def print_trade_details(order, balance):
    print(f"\nOrdem Executada:")
    print(f"ID: {order['id']}")
    print(f"Tipo: {order['side']}")
    print(f"Preço: {order['price']}")
    print(f"Quantidade: {order['amount']}")
    print(f"Margem: {order['cost']}")
    print(f"Saldo: {balance}")

def display_ticker_info(ticker):
    ticker_data = {
        'Symbol': ticker['symbol'],
        'Timestamp': ticker['timestamp'],
        'Datetime': ticker['datetime'],
        'High': ticker['high'],
        'Low': ticker['low'],
        'Bid': ticker['bid'],
        'Bid Volume': ticker['bidVolume'],
        'Ask': ticker['ask'],
        'Ask Volume': ticker['askVolume'],
        'VWAP': ticker['vwap'],
        'Open': ticker['open'],
        'Close': ticker['close'],
        'Last': ticker['last'],
        'Previous Close': ticker['previousClose'],
        'Change': ticker['change'],
        'Percentage': ticker['percentage'],
        'Average': ticker['average'],
        'Base Volume': ticker['baseVolume'],
        'Quote Volume': ticker['quoteVolume']
    }
    df = pd.DataFrame([ticker_data])
    print("\nTicker Data:")
    print(df)

# Monitorar o mercado e executar ordens
def run_bot():
    previous_position = None
    while True:
        try:
            ticker = exchange.fetch_ticker('BTC/USDT')  # Ajuste para o par de moedas desejado
            display_ticker_info(ticker)
            
            position = trading_strategy(ticker)
            print(f"Nova posição: {position}")

            if position != previous_position:
                if position == 'long':
                    order = exchange.create_market_buy_order('BTC/USDT', 0.001)  # Ajuste a quantidade
                    print("Ordem de COMPRA executada")
                elif position == 'short':
                    order = exchange.create_market_sell_order('BTC/USDT', 0.001)  # Ajuste a quantidade
                    print("Ordem de VENDA executada")
                
                balance = exchange.fetch_balance()
                print_trade_details(order, balance)
                previous_position = position
            else:
                print("Nenhuma alteração na posição")

            # Evitar loop infinito rápido
            time.sleep(60)  # Esperar um minuto antes de verificar novamente

        except ccxt.NetworkError as e:
            print(f"Erro de rede: {str(e)}. Tentando novamente...")
            time.sleep(60)
        except ccxt.ExchangeError as e:
            print(f"Erro na exchange: {str(e)}. Tentando novamente...")
            time.sleep(60)
        except Exception as e:
            print(f"Erro inesperado: {str(e)}. Tentando novamente...")
            time.sleep(60)

if __name__ == "__main__":
    run_bot()
