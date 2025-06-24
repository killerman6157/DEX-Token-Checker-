# config/settings.py
# Wannan fayil din zai kula da saitunan bot da kuma API keys.
# Ana ba da shawarar amfani da environment variables don tsaro.

import os
from dotenv import load_dotenv

load_dotenv()  # ← Wannan zai ɗora duk `.env` variables

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")

# API Keys for Blockchain Data Providers
# Zaka buƙaci samun waɗannan keys daga kowane sabis.
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "YOUR_ETHERSCAN_API_KEY")
BSCSCAN_API_KEY = os.getenv("BSCSCAN_API_KEY", "YOUR_BSCSCAN_API_KEY")
POLYGONSCAN_API_KEY = os.getenv("POLYGONSCAN_API_KEY", "YOUR_POLYGONSCAN_API_KEY")
# A nan zaka ƙara keys don Solana (Solscan/Solana RPC), Sui, Ton, da kuma general data providers.
# Misali:
# SOLSCAN_API_KEY = os.getenv("SOLSCAN_API_KEY", "YOUR_SOLSCAN_API_KEY")
# COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "YOUR_COINGECKO_API_KEY") # Don farashi ko holders (idan suna bayarwa)

# RPC URLs (Don hulda da nodes na blockchain)
# Zaka iya amfani da Infura, Alchemy, QuickNode, ko sauransu
ETH_RPC_URL = os.getenv("ETH_RPC_URL", "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID")
BSC_RPC_URL = os.getenv("BSC_RPC_URL", "https://bsc-dataseed.binance.org/")
POLYGON_RPC_URL = os.getenv("POLYGON_RPC_URL", "https://polygon-rpc.com/")
# Sauran RPC URLs
# SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
# SUI_RPC_URL = os.getenv("SUI_RPC_URL", "https://fullnode.mainnet.sui.io/")
# TON_RPC_URL = os.getenv("TON_RPC_URL", "https://toncenter.com/api/v2/jsonRPC")

# Flask Secret Key for Web Dashboard
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your_strong_random_secret_key_here')
# Zaka iya samar da strong key kamar haka: os.urandom(24).hex()

# Sauran saitunan (misali, Database URLs, Loggings settings)
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./web_dashboard/app.db") # Misali ga database
