import ccxt
import time
from config import api_key, api_secret  # Importa as credenciais do arquivo config.py

# Configurações da API da Binance
symbol = 'BTC/USDT'

# Configuração da exchange (Binance Testnet)
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,  # Habilita limitação de taxa (rate limit)
    'options': {
        'defaultType': 'future',  # Configura para operar no modo future
    }
})

def run_bot():
    # Entrar no mercado comprando no preço de mercado
    print("Entrando no mercado...")
    order = exchange.create_market_buy_order(symbol, amount=0.001)
    print("Ordem de compra executada:", order)

    # Loop principal para monitorar e decidir operações
    while True:
        try:
            # Obter dados do ticker
            ticker = exchange.fetch_ticker(symbol)
            print("\nTicker Data:")
            print(ticker)

            # Simulação de lógica para decidir entre long ou short
            if should_enter_long(ticker):
                print("\nIdentificado um bom momento para Long.")
                # Criar operação de Long
                order = exchange.create_market_buy_order(symbol, amount=0.001)
                print("Ordem de compra (Long) executada:", order)
            elif should_enter_short(ticker):
                print("\nIdentificado um bom momento para Short.")
                # Criar operação de Short
                order = exchange.create_market_sell_order(symbol, amount=0.001)
                print("Ordem de venda (Short) executada:", order)

            # Exibir saldo em tempo real
            balance = exchange.fetch_balance()
            print("\nSaldo em tempo real:")
            print(balance['total'])

            # Esperar antes de verificar novamente (por exemplo, a cada 5 segundos)
            time.sleep(5)

        except Exception as e:
            print(f"Erro encontrado: {e}")
            time.sleep(10)  # Esperar antes de tentar novamente

def should_enter_long(ticker):
    # Lógica para determinar se deve entrar em Long
    # Exemplo simplificado: baseado em uma condição fictícia
    return ticker['change'] > 0.5  # Exemplo fictício de condição

def should_enter_short(ticker):
    # Lógica para determinar se deve entrar em Short
    # Exemplo simplificado: baseado em uma condição fictícia
    return ticker['change'] < -0.5  # Exemplo fictício de condição

# Executar o bot
run_bot()
