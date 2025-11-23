import requests
import json
from datetime import datetime
import time

class CryptoPortfolio:
    def __init__(self):
        self.api_url = "https://api.binance.com/api/v3"
        # 在这里设置你的加密货币持仓量
        self.holdings = {
            "BTC": 5,    # 示例：0.5 BTC
            "ETH": 200,   # 示例：2.0 ETH
            "SOL": 50,  # 示例：10.0 SOL
            "BNB": 1,   # 示例：5.0 BNB
            "USDT": 400000,  # 示例：1000.0 USDT
            "USDC": 200000  # 示例：1000.0 USDC
        }

    def get_crypto_prices(self):
        prices = {}
        try:
            # 获取所有交易对的价格
            response = requests.get(f"{self.api_url}/ticker/price")
            response.raise_for_status()
            all_prices = response.json()
            
            # 处理每个持仓的加密货币
            for crypto in self.holdings.keys():
                if crypto == "USDT" or crypto == "USDC":
                    # 稳定币价格约等于1美元
                    prices[crypto] = 1.0
                    continue
                
                # 查找对USDT的交易对价格
                symbol = f"{crypto}USDT"
                price_info = next((item for item in all_prices if item["symbol"] == symbol), None)
                
                if price_info:
                    prices[crypto] = float(price_info["price"])
                else:
                    print(f"警告：未找到{crypto}的价格信息")
                    prices[crypto] = 0.0
                    
            return prices
        except requests.exceptions.RequestException as e:
            print(f"获取价格时发生错误: {e}")
            return None

    def calculate_portfolio_value(self):
        prices = self.get_crypto_prices()
        if not prices:
            return None

        total_value = 0
        print("\n当前投资组合价值 ({}):"
              .format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print("-" * 50)
        print(f"{'币种':<10} {'持仓量':<12} {'价格(USD)':<12} {'总价值(USD)':<12}")
        print("-" * 50)

        for crypto, amount in self.holdings.items():
            if crypto in prices:
                price = prices[crypto]
                value = amount * price
                total_value += value
                print(f"{crypto:<10} {amount:<12.4f} ${price:<11.2f} ${value:<11.2f}")

        print("-" * 50)
        print(f"总资产价值: ${total_value:.2f} USD")
        return total_value
    
    def monitor_portfolio(self, interval=60):
        """定期监控投资组合价值"""
        try:
            while True:
                self.calculate_portfolio_value()
                print(f"\n等待{interval}秒后更新...")  
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n监控已停止")

if __name__ == "__main__":
    portfolio = CryptoPortfolio()
    portfolio.calculate_portfolio_value()
    
    # 如果你想启动自动更新功能，取消下面的注释
    # portfolio.monitor_portfolio(interval=60)  # 每60秒更新一次