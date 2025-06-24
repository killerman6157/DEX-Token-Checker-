from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
import os
import asyncio

# Import daga core module don binciken token
from core.checker import check_token_details
from core.blockchain_data import get_token_name, get_token_supply, get_token_holders

# Kwashe TOKEN daga environment variable
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context) -> None:
    """Amsa umurnin /start. Nuna maraba da button 'Yadda Bot din Ke Aiki'."""
    keyboard = [
        [InlineKeyboardButton("🛠 Yadda Bot ɗin Ke Aiki", callback_data='how_it_works')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        'Barka da zuwa DEX Trade Checker Bot! Zan taimaka maka wajen tantance amincin token.',
        reply_markup=reply_markup
    )

async def how_it_works(update: Update, context) -> None:
    """Nuna yadda ake amfani da bot da kuma button Komawa Menu."""
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("⬅️ Komawa Menu", callback_data='back_to_menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "Liƙa **contract ɗin token** ta hanyar amfani da `/check_all` sannan kuma **contract address** ɗin a gefe."
        "\n\nMisali: `/check_all 0x1234567890abcdef...`",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def back_to_menu(update: Update, context) -> None:
    """Koma zuwa main menu (start)."""
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("🛠 Yadda Bot ɗin Ke Aiki", callback_data='how_it_works')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        'Barka da zuwa DEX Trade Checker Bot! Zan taimaka maka wajen tantance amincin token.',
        reply_markup=reply_markup
    )

async def check_all_command(update: Update, context) -> None:
    """Kula da umurnin /check_all."""
    args = context.args
    if not args or len(args) != 1:
        await update.message.reply_text(
            "Don Allah ka yi amfani da umurnin daidai: `/check_all <contract_address>`",
            parse_mode='Markdown'
        )
        return

    contract_address = args[0]
    await update.message.reply_text(f"Muna binciken token mai contract address: `{contract_address}`...\n"
                                    "Da fatan za a jira na ɗan lokaci.",
                                    parse_mode='Markdown')

    try:
        # Kaddamar da bincike daga core module
        result = await check_token_details(contract_address)

        if result:
            response_message = (
                f"**Sakamakon Binciken Token:**\n"
                f"**Sunan Token:** `{result.get('token_name', 'N/A')}`\n"
                f"**Contract Address:** `{contract_address}`\n"
                f"**Rug Pull Risk:** {'✅ LOW' if result.get('rug_pull_risk', False) == 'LOW' else '⚠️ HIGH'}\n"
                f"**Ownership Renounced:** {'✅ E Haka Ne' if result.get('ownership_renounced') else '❌ A'a'}\n"
                f"**LP Locked:** {'✅ E Haka Ne' if result.get('lp_locked') else '❌ A\'a'}\n"
                f"**Adadin Masu Riƙe (Holders):** `{result.get('holders_count', 'N/A')}`\n"
                f"**Verified Supply:** `{result.get('total_supply', 'N/A')}`\n\n"
                f"Don cikakken bayani da saita faɗakarwa, ziyarci Web Dashboard ɗin mu."
            )
        else:
            response_message = "An kasa samun bayanan token ko contract address ɗin ba daidai bane."

        await update.message.reply_text(response_message, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"An samu kuskure yayin bincike: {e}")

def main() -> None:
    """Fara aikin bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Umurnai
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("check_all", check_all_command))

    # Callback Queries daga buttons
    application.add_handler(CallbackQueryHandler(how_it_works, pattern='how_it_works'))
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern='back_to_menu'))

    # Run the bot until the user presses Ctrl-C
    print("Bot din yana gudana...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
                                            
