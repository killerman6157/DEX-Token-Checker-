# DEX Trade Checker Bot

Wannan bot ɗin zai taimaka maka wajen tantance amincin sababbin token a kasuwar crypto kafin ka saka hannun jari. Yana haɗe da Telegram bot don sauƙin amfani da kuma Web Dashboard don zurfafa bincike da monitoring.

## Fasali

* **Telegram Bot Interface:**
    * Umurni mai sauƙi: `/check_all <contract_address>`
    * Binciken haɗarin **Rug Pull Risk**.
    * Tabbatar da **Ownership Renounced**.
    * Binciken ko **LP (Liquidity Pool) An Kulle**.
    * Nuna ƙarin bayanai kamar **Token Name, Holders Count, Verified Supply**.
    * Goyon bayan Blockchain: **BNB Smart Chain, Ethereum, Polygon, Solana, Sui, Ton**.

* **Web Dashboard:**
    * Cikakken tarihin binciken token.
    * Ganin bayanai mai zurfi tare da graf da taswirar bayanai.
    * Saita faɗakarwa ta atomatik (Automated Alerts) don canje-canje a token.
    * Kula da token da yawa (Watchlist).

* **Real-time API Integration:** Yana amfani da API's na zamani don samun bayanan blockchain kai tsaye.

## Yadda Ake Girka (Installation)

1.  **Clone repository (idan baka da shi a kwamfutar ka):**
    ```bash
    git clone [https://github.com/yourusername/your-repo-name.git](https://github.com/yourusername/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Ƙirƙiri Virtual Environment (Shawara mai kyau):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # A Linux/macOS
    # venv\Scripts\activate   # A Windows
    ```

3.  **Girka Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Saita Environment Variables:**
    Ƙirƙiri fayil mai suna `.env` a cikin babban directory (`your-repo-name/`) kuma saka API keys da sauran saitunan a ciki.
    ```
    # .env (ka cika waɗannan da nawa keys da URLs)
    TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN_HERE"
    ETHERSCAN_API_KEY="YOUR_ETHERSCAN_API_KEY_HERE"
    BSCSCAN_API_KEY="YOUR_BSCSCAN_API_KEY_HERE"
    POLYGONSCAN_API_KEY="YOUR_POLYGONSCAN_API_KEY_HERE"
    # Da sauran API keys kamar na Solana, Sui, Ton, da kuma general data providers.

    ETH_RPC_URL="[https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID](https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID)" # Ko wani RPC provider
    BSC_RPC_URL="[https://bsc-dataseed.binance.org/](https://bsc-dataseed.binance.org/)"
    POLYGON_RPC_URL="[https://polygon-rpc.com/](https://polygon-rpc.com/)"
    # Da sauran RPC URLs na blockchain daban-daban.

    FLASK_SECRET_KEY="YOUR_STRONG_RANDOM_SECRET_KEY" # Ka samar da tsayayyen secret key!
    ```
    **Lura:** Kada ka sanya fayil ɗin `.env` a cikin GitHub ko wani wuri na jama'a!

## Yadda Ake Gudanarwa (Usage)

1.  **Gudanar da Telegram Bot:**
    ```bash
    python bot/main.py
    ```
    Bot ɗin zai fara aiki. Sai ka je Telegram ka yi amfani da shi.

2.  **Gudanar da Web Dashboard:**
    ```bash
    python web_dashboard/app.py
    ```
    Dashboard ɗin zai fara aiki a `http://127.0.0.1:5000` (ko wani port idan ka canza saitunan).

## Ci Gaban Nan Gaba (Future Enhancements)

* Cikakken hadaka da API na Solana, Sui, da Ton.
* Ƙarin ingantaccen logic na gano "rug pull risk" ta hanyar nazarin contract code.
* Hadaka da database mai ƙarfi (PostgreSQL/MySQL) don dashboard.
* Tsarin authentication da user accounts a dashboard.
* Faɗakarwa ta Email da Telegram daga dashboard.

