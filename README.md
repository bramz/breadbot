# BreadBot

<img src="breadbot.png" alt="BreadBot Logo" width="1024px" height="640px">

"Empowering your crypto journey, one trade at a time."

## Introduction

BreadBot is a Python-based cryptocurrency trading bot designed to automate trading operations across multiple exchanges. It leverages the `web3` and `requests` libraries for blockchain interactions and API requests, providing users with a powerful tool for executing trades, backtesting strategies, and optimizing their cryptocurrency trading activities.

## Features

- **Automated Trading:** BreadBot facilitates automated trading of popular cryptocurrencies such as Ethereum (ETH), Bitcoin (BTC), USDT, Solana (SOL), Monero (XMR), and Bitcoin Cash (BCH).
- **Exchange Integration:** It integrates seamlessly with major cryptocurrency exchanges including Binance, Coinbase, Kraken, CoinGecko, Robinhood, Gemini, MXC Global, CoinStats, Bitstamp, and Bitfinex.
- **Historical Data Retrieval:** BreadBot retrieves historical data from supported APIs, enabling users to backtest strategies and optimize trading algorithms.
- **Risk Management:** The bot supports stop-loss and profit-taking strategies, allowing users to manage risks and maximize gains.
- **Customization:** Users can customize wallet addresses, API keys, and endpoints for each supported exchange, providing flexibility and control over trading operations.
- **Easy Configuration:** BreadBot's configuration is user-friendly, with settings conveniently managed through the `config.py` file.

## Setup

To set up BreadBot, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/bramz/breadbot.git
   cd breadbot
   ```

2. **Install Dependencies:**
`pip install -r requirements.txt`

3. **Configuration:**

- Open config.py in a text editor.
- Update INFURA_URL with your Infura Project URL for Ethereum interactions.
- Define wallet addresses and private keys under the WALLETS section.
- Configure API endpoints, keys, and secrets for each supported exchange in the EXCHANGES section.

## Usage

After configuring BreadBot, you can start using it with the following steps:

1. Run BreadBot: `python main.py`
2. Monitor and Manage:

- BreadBot will initiate automated trading based on your configurations.
- Monitor trades, check balances, and review logs to manage your trading activities.

## Contributing

Contributions to BreadBot are welcome! If you'd like to contribute, follow these steps:

1. Fork the Repository: Fork the BreadBot repository on GitHub.
2. Create a Branch: Create a new branch for your feature or bug fix.
3. Make Changes: Implement your changes and commit them with descriptive messages.
4. Push Changes: Push your changes to your fork.
5. Create a Pull Request: Submit a pull request to the main BreadBot repository for review.

## Support

For questions, issues, or feedback, please open an issue on the [BreadBot GitHub repository](https://github.com/bramz/breadbot/issues).
Feel free to contact me directly at [brockramz@gmail.com](brockramz@gmail.com) for any inquiries or assistance.

## License

BreadBot is licensed under the [MIT License](https://opensource.org/license/mit). Feel free to use, modify, and distribute it according to the terms of the license.

## Disclaimer

**The information provided by BreadBot is for educational and experimental purposes only. If you do not have any experience trading crypto currencies, this project is not recommended.**

I, Brock Ramsey, do not guarantee the accuracy, completeness, or reliability of any information or functionality provided by BreadBot. Users of BreadBot acknowledge that cryptocurrency trading involves inherent risks, including the risk of financial loss. I am not liable for any legal issues or losses incurred as a result of using BreadBot. By using BreadBot, you agree to waive any claims or liabilities against me, Brock Ramsey, arising from your use of BreadBot. It is recommended that users conduct their own research and exercise caution when using BreadBot for trading purposes. Good Luck!
