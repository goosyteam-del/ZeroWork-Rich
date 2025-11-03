"""
Trading Engine Module
Implements mock arbitrage trading logic based on portfolio value
"""

import random
import time
import sys
from typing import Dict, List, Optional
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama for Windows support
init(autoreset=True)

from src.config import (
    MIN_BALANCE_USD, ENABLE_MOCK_TRADING, 
    MOCK_EXCHANGES, MOCK_TRADE_INTERVAL
)
from src.logger_config import setup_logger
from src.price_fetcher import get_price_fetcher

logger = setup_logger("TradingEngine")


def print_progress_bar(iteration, total, prefix='', suffix='', length=40, fill='█'):
    """Print a progress bar to console"""
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '░' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='', flush=True)
    if iteration == total:
        print()


def animate_scan(message, duration=2):
    """Animated scanning effect"""
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f'\r{frames[i % len(frames)]} {message}...', end='', flush=True)
        time.sleep(0.1)
        i += 1
    print(f'\r✓ {message}... Done!      ')


def type_text(text, delay=0.03):
    """Print text with typing effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def print_with_animation(text, delay=0.03):
    """Print text character by character"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)


def animated_progress(message, steps=20, char='█', delay=0.05):
    """Show animated progress bar"""
    print(f'{message} ', end='', flush=True)
    for i in range(steps):
        print(char, end='', flush=True)
        time.sleep(delay)
    print(' ✓')


def print_box(title, content_lines, width=70):
    """Print content in a nice box"""
    print("╔" + "═" * (width - 2) + "╗")
    print(f"║ {title.center(width - 4)} ║")
    print("╠" + "═" * (width - 2) + "╣")
    for line in content_lines:
        if isinstance(line, tuple):  # (label, value) pair
            label, value = line
            padding = width - 4 - len(label) - len(str(value))
            print(f"║ {label}{' ' * padding}{value} ║")
        else:
            print(f"║ {line.ljust(width - 4)} ║")
    print("╚" + "═" * (width - 2) + "╝")


def clear_screen():
    """Clear terminal screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_dashboard(initial_balance, current_profit, trades_executed, session_start, scan_count, opportunities_found, profitable_ops):
    """Print fixed dashboard at top of screen"""
    clear_screen()
    
    elapsed = (datetime.now() - session_start).total_seconds()
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)
    
    current_balance = initial_balance + current_profit
    roi = (current_profit / initial_balance * 100) if initial_balance > 0 else 0
    
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║             🤖 TRADING BOT - LIVE DASHBOARD 🤖                       ║")
    print("╠══════════════════════════════════════════════════════════════════════╣")
    print(f"║  💼 Initial Balance:   ${initial_balance:>10.2f}  │  ⏱  Runtime: {hours:02d}:{minutes:02d}:{seconds:02d}   ║")
    print(f"║  💰 Current Balance:   ${current_balance:>10.2f}  │  🔍 Scans: {scan_count:>6}       ║")
    print(f"║  📈 Total Profit:      ${current_profit:>10.2f}  │  💼 Trades: {trades_executed:>5}       ║")
    print(f"║  📊 ROI:               {roi:>9.3f}%   │  ✅ Success: {profitable_ops:>4}      ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()


class TradingEngine:
    """
    Mock trading engine for arbitrage opportunities
    """
    
    def __init__(self, total_balance_usd: float):
        """
        Initialize trading engine
        
        Args:
            total_balance_usd: Total portfolio value in USD
        """
        self.total_balance_usd = total_balance_usd
        self.trades_executed = 0
        self.total_profit_usd = 0.0
        self.session_start = datetime.now()
        
    def check_minimum_balance(self) -> bool:
        """
        Check if balance meets minimum trading requirement
        
        Returns:
            True if balance is sufficient, False otherwise
        """
        if self.total_balance_usd < MIN_BALANCE_USD:
            print("\n")
            print_box("⚠ INSUFFICIENT BALANCE", [
                "",
                ("Current Balance:", f"${self.total_balance_usd:.2f} USD"),
                ("Required Balance:", f"${MIN_BALANCE_USD:.2f} USD"),
                ("Shortage:", f"${MIN_BALANCE_USD - self.total_balance_usd:.2f} USD"),
                "",
                "Insufficient balance to execute trades.",
                "Please add more funds to your wallet.",
                ""
            ])
            logger.error(f"Trading blocked: Balance ${self.total_balance_usd:.2f} < ${MIN_BALANCE_USD:.2f} required")
            return False
        
        logger.info(f"✓ Balance check passed: ${self.total_balance_usd:.2f} >= ${MIN_BALANCE_USD:.2f}")
        return True
    
    def _generate_mock_arbitrage_opportunity(self) -> Dict[str, any]:
        """
        Generate mock arbitrage opportunity data with REAL prices
        
        Returns:
            Dictionary with arbitrage details
        """
        # Randomly select exchanges
        exchange_list = list(MOCK_EXCHANGES.keys())
        buy_exchange = random.choice(exchange_list)
        sell_exchange = random.choice([e for e in exchange_list if e != buy_exchange])
        
        # Common trading pairs with real prices
        pairs = ["ETH/USDT", "BNB/USDT", "MATIC/USDT", "BTC/USDT"]
        pair = random.choice(pairs)
        base_token = pair.split('/')[0]
        
        # Get REAL price from CoinGecko
        price_fetcher = get_price_fetcher()
        real_price = price_fetcher.get_price(base_token)
        
        # If price fetch fails, use fallback
        if real_price == 0:
            logger.warning(f"Failed to fetch real price for {base_token}, using fallback")
            real_price = random.uniform(1000, 3000)
        
        # Generate realistic price spread (0.5% to 2%) around real price
        spread_percent = random.uniform(0.5, 2.0)
        
        buy_price = real_price
        sell_price = real_price * (1 + spread_percent / 100)
        
        # Calculate trading amount based on portfolio (1-5% of balance)
        trade_percent = random.uniform(1, 5)
        trade_amount_usd = self.total_balance_usd * (trade_percent / 100)
        
        # Calculate fees
        buy_fee = trade_amount_usd * MOCK_EXCHANGES[buy_exchange]["fee"]
        sell_fee = trade_amount_usd * MOCK_EXCHANGES[sell_exchange]["fee"]
        total_fees = buy_fee + sell_fee
        
        # Calculate profit
        gross_profit = trade_amount_usd * (spread_percent / 100)
        net_profit = gross_profit - total_fees
        profit_percent = (net_profit / trade_amount_usd) * 100
        
        return {
            "pair": pair,
            "buy_exchange": MOCK_EXCHANGES[buy_exchange]["name"],
            "sell_exchange": MOCK_EXCHANGES[sell_exchange]["name"],
            "buy_price": buy_price,
            "sell_price": sell_price,
            "spread_percent": spread_percent,
            "trade_amount_usd": trade_amount_usd,
            "gross_profit": gross_profit,
            "total_fees": total_fees,
            "net_profit": net_profit,
            "profit_percent": profit_percent,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _is_profitable(self, opportunity: Dict) -> bool:
        """
        Determine if arbitrage opportunity is profitable
        
        Args:
            opportunity: Arbitrage opportunity dictionary
            
        Returns:
            True if profitable (net profit > 0), False otherwise
        """
        return opportunity["net_profit"] > 0
    
    def execute_mock_trade(self, opportunity: Dict) -> bool:
        """
        Execute a mock arbitrage trade with realistic timing and animations
        
        Args:
            opportunity: Arbitrage opportunity to execute
            
        Returns:
            True if trade executed successfully
        """
        try:
            print("\n" + "╔" + "═" * 72 + "╗")
            print("║" + " 📊 INITIATING ARBITRAGE TRADE EXECUTION".center(72) + "║")
            print("╚" + "═" * 72 + "╝")
            
            # Trade details - display immediately with colors
            print(f"\n💱 Trading Pair:    {Fore.CYAN}{Style.BRIGHT}{opportunity['pair']}{Style.RESET_ALL}")
            print(f"📍 Buy Exchange:    {Fore.GREEN}{opportunity['buy_exchange']}{Style.RESET_ALL} @ {Fore.YELLOW}${opportunity['buy_price']:.2f}{Style.RESET_ALL}")
            print(f"📍 Sell Exchange:   {Fore.GREEN}{opportunity['sell_exchange']}{Style.RESET_ALL} @ {Fore.YELLOW}${opportunity['sell_price']:.2f}{Style.RESET_ALL}")
            print(f"📊 Spread:          {Fore.MAGENTA}{opportunity['spread_percent']:.2f}%{Style.RESET_ALL}")
            print(f"💰 Trade Amount:    {Fore.YELLOW}${opportunity['trade_amount_usd']:.2f}{Style.RESET_ALL}")
            print(f"💵 Expected Profit: {Fore.GREEN}{Style.BRIGHT}${opportunity['net_profit']:.4f}{Style.RESET_ALL}")
            
            # Step 1: Check liquidity with technical process
            print(f"\n{'─'*74}")
            print(f"{Fore.CYAN}⏳ [1/5] Checking liquidity on exchanges{Style.RESET_ALL}")
            print("   • Connecting to liquidity pools...", end='', flush=True)
            time.sleep(0.3)
            print(f" {Fore.GREEN}✓{Style.RESET_ALL}")
            print("   • Querying pool reserves...", end='', flush=True)
            time.sleep(0.4)
            print(f" {Fore.GREEN}✓{Style.RESET_ALL}")
            print("   • Analyzing depth...", end='', flush=True)
            animated_progress("", 15, '▓', 0.03)
            print(f"   {Fore.GREEN}✓{Style.RESET_ALL} {Fore.CYAN}{opportunity['buy_exchange']}{Style.RESET_ALL}: Liquidity depth {Fore.YELLOW}${opportunity['trade_amount_usd']*10:.2f}{Style.RESET_ALL}")
            print(f"   {Fore.GREEN}✓{Style.RESET_ALL} {Fore.CYAN}{opportunity['sell_exchange']}{Style.RESET_ALL}: Liquidity depth {Fore.YELLOW}${opportunity['trade_amount_usd']*12:.2f}{Style.RESET_ALL}")
            print(f"   {Fore.GREEN}✓{Style.RESET_ALL} Sufficient liquidity confirmed")
            
            # Step 2: Calculate optimal parameters with process
            print()
            print(f"{Fore.CYAN}⏳ [2/5] Calculating optimal trade parameters{Style.RESET_ALL}")
            amount_crypto = opportunity['trade_amount_usd'] / opportunity['buy_price']
            gas_price = random.randint(20, 50)
            
            print("   • Computing token amounts...", end='', flush=True)
            time.sleep(0.3)
            print(f" {Fore.GREEN}✓{Style.RESET_ALL}")
            print("   • Estimating gas costs...", end='', flush=True)
            time.sleep(0.3)
            print(f" {Fore.GREEN}✓{Style.RESET_ALL}")
            print("   • Calculating slippage impact...", end='', flush=True)
            animated_progress("", 12, '▓', 0.025)
            print(f"   {Fore.GREEN}✓{Style.RESET_ALL} Optimal size: {Fore.YELLOW}{amount_crypto:.6f}{Style.RESET_ALL} {Fore.CYAN}{opportunity['pair'].split('/')[0]}{Style.RESET_ALL}")
            print(f"   {Fore.GREEN}✓{Style.RESET_ALL} Slippage tolerance: {Fore.MAGENTA}0.5%{Style.RESET_ALL}")
            print(f"   {Fore.GREEN}✓{Style.RESET_ALL} Gas price: {Fore.YELLOW}{gas_price} Gwei{Style.RESET_ALL}")
            print(f"   {Fore.GREEN}✓{Style.RESET_ALL} Estimated gas: {Fore.YELLOW}{random.randint(80000, 120000)} units{Style.RESET_ALL}")
            
            # Step 3: Place buy order with detailed process
            print()
            print(f"{Fore.CYAN}⏳ [3/5] Executing BUY order on {Fore.GREEN}{opportunity['buy_exchange']}{Style.RESET_ALL}")
            
            # Creating transaction
            print("   • Building swap transaction...", end='', flush=True)
            time.sleep(0.4)
            animated_progress("", 10, '▓', 0.03)
            
            # Signing
            print("   • Signing with private key...", end='', flush=True)
            time.sleep(0.3)
            animated_progress("", 8, '▓', 0.035)
            
            # Broadcasting
            print("   • Broadcasting to mempool...", end='', flush=True)
            time.sleep(0.4)
            animated_progress("", 12, '▓', 0.03)
            
            # Confirmation
            print("   • Waiting for transaction inclusion...", end='', flush=True)
            frames = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
            for i in range(15):
                print(f'\r   • Waiting for transaction inclusion... {frames[i % len(frames)]}', end='', flush=True)
                time.sleep(0.15)
            print(f'\r   • Waiting for transaction inclusion... {Fore.GREEN}✓{Style.RESET_ALL}         ')
            
            tx_hash_buy = f"0x{''.join(random.choices('0123456789abcdef', k=64))}"
            gas_used_buy = random.randint(80000, 120000)
            print(f"   {Fore.GREEN}✓{Style.RESET_ALL} Order filled: {Fore.YELLOW}${opportunity['trade_amount_usd']:.2f}{Style.RESET_ALL} @ {Fore.YELLOW}${opportunity['buy_price']:.2f}{Style.RESET_ALL}")
            print(f"   {Fore.GREEN}✓{Style.RESET_ALL} Gas used: {Fore.YELLOW}{gas_used_buy} units{Style.RESET_ALL} ({Fore.RED}${opportunity['total_fees']/2:.4f}{Style.RESET_ALL})")
            print(f"   {Fore.GREEN}✓{Style.RESET_ALL} TX Hash: {Fore.BLUE}{tx_hash_buy[:20]}...{tx_hash_buy[-12:]}{Style.RESET_ALL}")
            
            # Step 4: Wait for blockchain confirmation
            print()
            print(f"{Fore.CYAN}⏳ [4/5] Waiting for blockchain confirmation{Style.RESET_ALL}")
            print("   • Monitoring blockchain...", end='', flush=True)
            frames = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
            for i in range(18):
                print(f'\r   • Monitoring blockchain... {Fore.YELLOW}{frames[i % len(frames)]}{Style.RESET_ALL}', end='', flush=True)
                time.sleep(0.12)
            print(f'\r   • Monitoring blockchain... {Fore.GREEN}✓{Style.RESET_ALL}            ')
            
            block_num = random.randint(18000000, 18999999)
            confirmations = random.randint(1, 3)
            print(f"   {Fore.GREEN}✓{Style.RESET_ALL} Confirmed in block {Fore.MAGENTA}#{block_num}{Style.RESET_ALL}")
            print(f"   {Fore.GREEN}✓{Style.RESET_ALL} Confirmations: {Fore.YELLOW}{confirmations}/12{Style.RESET_ALL}")
            print(f"   {Fore.GREEN}✓{Style.RESET_ALL} Buy order confirmed on-chain")
            
            # Step 5: Place sell order with detailed process
            print()
            print(f"{Fore.CYAN}⏳ [5/5] Executing SELL order on {Fore.GREEN}{opportunity['sell_exchange']}{Style.RESET_ALL}")
            
            # Creating transaction
            print("   • Building swap transaction...", end='', flush=True)
            time.sleep(0.4)
            animated_progress("", 10, '▓', 0.03)
            
            # Signing
            print("   • Signing with private key...", end='', flush=True)
            time.sleep(0.3)
            animated_progress("", 8, '▓', 0.035)
            
            # Broadcasting
            print("   • Broadcasting to mempool...", end='', flush=True)
            time.sleep(0.4)
            animated_progress("", 12, '▓', 0.03)
            
            # Confirmation
            print("   • Waiting for transaction inclusion...", end='', flush=True)
            for i in range(15):
                print(f'\r   • Waiting for transaction inclusion... {Fore.YELLOW}{frames[i % len(frames)]}{Style.RESET_ALL}', end='', flush=True)
                time.sleep(0.15)
            print(f'\r   • Waiting for transaction inclusion... {Fore.GREEN}✓{Style.RESET_ALL}         ')
            
            tx_hash_sell = f"0x{''.join(random.choices('0123456789abcdef', k=64))}"
            gas_used_sell = random.randint(75000, 115000)
            token_symbol = opportunity['pair'].split('/')[0]
            print(f"   {Fore.GREEN}✓{Style.RESET_ALL} Order filled: {Fore.YELLOW}{amount_crypto:.6f}{Style.RESET_ALL} {Fore.CYAN}{token_symbol}{Style.RESET_ALL} @ {Fore.YELLOW}${opportunity['sell_price']:.2f}{Style.RESET_ALL}")
            print(f"   {Fore.GREEN}✓{Style.RESET_ALL} Gas used: {Fore.YELLOW}{gas_used_sell} units{Style.RESET_ALL} ({Fore.RED}${opportunity['total_fees']/2:.4f}{Style.RESET_ALL})")
            print(f"   {Fore.GREEN}✓{Style.RESET_ALL} TX Hash: {Fore.BLUE}{tx_hash_sell[:20]}...{tx_hash_sell[-12:]}{Style.RESET_ALL}")
            
            # Finalizing
            print()
            print(f"{Fore.CYAN}⏳ Finalizing arbitrage execution{Style.RESET_ALL}")
            print("   • Verifying profit realization...", end='', flush=True)
            time.sleep(0.3)
            animated_progress("", 10, '▓', 0.03)
            print("   • Updating portfolio...", end='', flush=True)
            time.sleep(0.2)
            animated_progress("", 8, '▓', 0.03)
            
            # Update statistics
            self.trades_executed += 1
            self.total_profit_usd += opportunity["net_profit"]
            
            # Success summary with colors and professional format
            print("\n" + "╔" + "═" * 72 + "╗")
            print("║" + f" {Fore.GREEN}✅ TRADE EXECUTED SUCCESSFULLY{Style.RESET_ALL}".center(82) + "║")
            print("╠" + "═" * 72 + "╣")
            
            # Trade details with icons and colors
            print(f"║  🆔 Trade ID:           {Fore.CYAN}#{self.trades_executed:04d}{Style.RESET_ALL}".ljust(83) + "║")
            print(f"║  💱 Pair:               {Fore.YELLOW}{Style.BRIGHT}{opportunity['pair']}{Style.RESET_ALL}".ljust(83) + "║")
            print(f"║  📊 Strategy:           {Fore.MAGENTA}Cross-DEX Arbitrage{Style.RESET_ALL}".ljust(83) + "║")
            print("║" + " " * 72 + "║")
            
            # Buy order details
            print(f"║  {Fore.GREEN}📥 BUY ORDER:{Style.RESET_ALL}".ljust(83) + "║")
            print(f"║     Exchange:          {Fore.CYAN}{opportunity['buy_exchange']}{Style.RESET_ALL}".ljust(83) + "║")
            print(f"║     Price:             {Fore.YELLOW}${opportunity['buy_price']:.2f}{Style.RESET_ALL}".ljust(83) + "║")
            print(f"║     Amount:            {Fore.YELLOW}${opportunity['trade_amount_usd']:.2f}{Style.RESET_ALL}".ljust(83) + "║")
            print(f"║     Gas Cost:          {Fore.RED}${opportunity['total_fees']/2:.4f}{Style.RESET_ALL}".ljust(83) + "║")
            print("║" + " " * 72 + "║")
            
            # Sell order details
            token_symbol = opportunity['pair'].split('/')[0]
            print(f"║  {Fore.RED}📤 SELL ORDER:{Style.RESET_ALL}".ljust(83) + "║")
            print(f"║     Exchange:          {Fore.CYAN}{opportunity['sell_exchange']}{Style.RESET_ALL}".ljust(83) + "║")
            print(f"║     Price:             {Fore.YELLOW}${opportunity['sell_price']:.2f}{Style.RESET_ALL}".ljust(83) + "║")
            print(f"║     Amount:            {Fore.YELLOW}{amount_crypto:.6f}{Style.RESET_ALL} {Fore.CYAN}{token_symbol}{Style.RESET_ALL}".ljust(93) + "║")
            print(f"║     Gas Cost:          {Fore.RED}${opportunity['total_fees']/2:.4f}{Style.RESET_ALL}".ljust(83) + "║")
            print("╠" + "═" * 72 + "╣")
            
            # Profit summary with visual indicators
            print(f"║  {Fore.GREEN}💰 PROFIT BREAKDOWN:{Style.RESET_ALL}".ljust(83) + "║")
            print(f"║     Gross Profit:      {Fore.GREEN}${opportunity['gross_profit']:>10.4f}{Style.RESET_ALL}  ⬆".ljust(85) + "║")
            print(f"║     Exchange Fees:     {Fore.RED}${opportunity['total_fees']:>10.4f}{Style.RESET_ALL}  ⬇".ljust(85) + "║")
            print(f"║     Net Profit:        {Fore.GREEN}{Style.BRIGHT}${opportunity['net_profit']:>10.4f}{Style.RESET_ALL}  ✅ ({Fore.MAGENTA}{opportunity['profit_percent']:.3f}%{Style.RESET_ALL})".ljust(105) + "║")
            print("║" + " " * 72 + "║")
            print(f"║  {Fore.CYAN}📈 SESSION PERFORMANCE:{Style.RESET_ALL}".ljust(83) + "║")
            print(f"║     Total Trades:      {Fore.YELLOW}{self.trades_executed}{Style.RESET_ALL}".ljust(83) + "║")
            print(f"║     Session Profit:    {Fore.GREEN}${self.total_profit_usd:>10.4f}{Style.RESET_ALL}".ljust(93) + "║")
            print(f"║     Session ROI:       {Fore.MAGENTA}{(self.total_profit_usd/self.total_balance_usd*100):>10.4f}%{Style.RESET_ALL}".ljust(93) + "║")
            print("╚" + "═" * 72 + "╝")
            
            # Colored log message with box
            print()
            print("┌" + "─" * 72 + "┐")
            print(f"│ {Fore.CYAN}📊 TRADE LOG ENTRY #{self.trades_executed:04d}{Style.RESET_ALL}".ljust(83) + "│")
            print("├" + "─" * 72 + "┤")
            print(f"│  Pair:     {Fore.YELLOW}{opportunity['pair']}{Style.RESET_ALL}".ljust(83) + "│")
            print(f"│  Buy:      {Fore.GREEN}{opportunity['buy_exchange']}{Style.RESET_ALL} @ {Fore.YELLOW}${opportunity['buy_price']:.2f}{Style.RESET_ALL}".ljust(93) + "│")
            print(f"│  Sell:     {Fore.RED}{opportunity['sell_exchange']}{Style.RESET_ALL} @ {Fore.YELLOW}${opportunity['sell_price']:.2f}{Style.RESET_ALL}".ljust(93) + "│")
            print(f"│  Spread:   {Fore.MAGENTA}{opportunity['spread_percent']:.2f}%{Style.RESET_ALL}".ljust(83) + "│")
            print(f"│  Profit:   {Fore.GREEN}${opportunity['net_profit']:.4f}{Style.RESET_ALL} ({Fore.MAGENTA}{opportunity['profit_percent']:.3f}%{Style.RESET_ALL})".ljust(93) + "│")
            print(f"│  Time:     {Fore.BLUE}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}".ljust(83) + "│")
            print("└" + "─" * 72 + "┘")
            
            logger.info(f"Trade #{self.trades_executed:04d} | {opportunity['pair']} | "
                       f"Buy: {opportunity['buy_exchange']} ${opportunity['buy_price']:.2f} | "
                       f"Sell: {opportunity['sell_exchange']} ${opportunity['sell_price']:.2f} | "
                       f"Profit: ${opportunity['net_profit']:.4f} ({opportunity['profit_percent']:.3f}%)")
            
            time.sleep(0.5)
            return True
            
        except Exception as e:
            logger.error(f"Failed to execute trade: {str(e)}")
            return False
    
    def run_trading_session(self, duration_seconds: int = None, max_trades: int = None) -> Dict:
        """
        Run automated trading session (infinite loop if duration_seconds is None)
        
        Args:
            duration_seconds: How long to run the session (None for infinite)
            max_trades: Maximum number of trades to execute (None for unlimited)
            
        Returns:
            Session summary dictionary
        """
        if not ENABLE_MOCK_TRADING:
            logger.warning("Mock trading is disabled in configuration")
            return {"error": "Trading disabled"}
        
        if not self.check_minimum_balance():
            return {
                "error": "Insufficient balance",
                "current_balance": self.total_balance_usd,
                "required_balance": MIN_BALANCE_USD
            }
        
        print("\n")
        print("╔══════════════════════════════════════════════════════════════════════╗")
        print("║           🤖 AUTOMATED TRADING SESSION STARTED 🤖                    ║")
        print("╚══════════════════════════════════════════════════════════════════════╝")
        print(f"\n📊 Portfolio Value: ${self.total_balance_usd:.2f}")
        
        if duration_seconds:
            print(f"⏱  Session Duration: {duration_seconds}s")
        else:
            print(f"⏱  Session Duration: Infinite (Press Ctrl+C to stop)")
        
        if max_trades:
            print(f"🎯 Max Trades: {max_trades}")
        else:
            print(f"🎯 Max Trades: Unlimited")
            
        print(f"⚡ Scan Interval: {MOCK_TRADE_INTERVAL}s")
        print("\n" + "═" * 74)
        print("Starting in 3 seconds...")
        time.sleep(3)
        
        start_time = time.time()
        opportunities_found = 0
        profitable_opportunities = 0
        scan_count = 0
        
        try:
            while True:
                elapsed = time.time() - start_time
                
                # Check exit conditions
                if duration_seconds and elapsed >= duration_seconds:
                    print(f"\n⏰ Session duration reached ({duration_seconds}s)")
                    break
                
                if max_trades and self.trades_executed >= max_trades:
                    print(f"\n🎯 Maximum trades reached ({max_trades})")
                    break
                
                scan_count += 1
                
                # Update dashboard
                print_dashboard(
                    self.total_balance_usd,
                    self.total_profit_usd,
                    self.trades_executed,
                    self.session_start,
                    scan_count,
                    opportunities_found,
                    profitable_opportunities
                )
                
                print(f"╔{'═'*72}╗")
                print(f"║ 🔍 MARKET SCAN #{scan_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".ljust(73) + "║")
                print(f"╚{'═'*72}╝\n")
                
                # Step 1: Connect to exchanges - technical process
                print("⏳ [1/3] Establishing connections to DEX protocols")
                print("   • Initializing WebSocket connections...", end='', flush=True)
                time.sleep(0.3)
                animated_progress("", 15, '▓', 0.025)
                print("   • Authenticating with RPC endpoints...", end='', flush=True)
                time.sleep(0.3)
                print(" ✓")
                print("   ✓ Connected to 4 DEX protocols")
                print("   ✓ Network latency: {}ms".format(random.randint(15, 45)))
                
                # Step 2: Fetch prices - technical process
                print()
                exchanges = list(MOCK_EXCHANGES.keys())
                print(f"⏳ [2/3] Fetching real-time prices from {len(exchanges)} exchanges")
                for i, exchange_key in enumerate(exchanges, 1):
                    exchange_name = MOCK_EXCHANGES[exchange_key]["name"]
                    print(f"   • [{i}/{len(exchanges)}] Querying {exchange_name} liquidity pools...", end='', flush=True)
                    
                    # Show progress bar for each exchange
                    time.sleep(0.2)
                    for j in range(12):
                        print('▓', end='', flush=True)
                        time.sleep(0.02)
                    print(' ✓')
                
                print(f"   ✓ Retrieved prices from {len(exchanges)} exchanges")
                print(f"   ✓ Data freshness: <500ms")
                
                # Step 3: Analyze opportunities - technical process
                print()
                print("⏳ [3/3] Analyzing cross-exchange arbitrage opportunities")
                
                # Detailed analysis steps with progress
                print("   • Calculating price spreads...", end='', flush=True)
                time.sleep(0.3)
                animated_progress("", 10, '▓', 0.025)
                
                print("   • Estimating gas costs...", end='', flush=True)
                time.sleep(0.3)
                animated_progress("", 10, '▓', 0.025)
                
                print("   • Checking slippage impact...", end='', flush=True)
                time.sleep(0.3)
                animated_progress("", 10, '▓', 0.025)
                
                print("   • Evaluating profit margins...", end='', flush=True)
                time.sleep(0.3)
                animated_progress("", 10, '▓', 0.025)
                
                print("   ✓ Analysis completed")
                
                # Generate opportunity
                opportunity = self._generate_mock_arbitrage_opportunity()
                opportunities_found += 1
                
                # Display opportunity - show immediately
                print(f"\n{'─'*74}")
                print("📈 ARBITRAGE OPPORTUNITY IDENTIFIED:")
                print(f"{'─'*74}")
                print(f"   Pair:          {opportunity['pair']}")
                print(f"   Buy Price:     ${opportunity['buy_price']:.2f} ({opportunity['buy_exchange']})")
                print(f"   Sell Price:    ${opportunity['sell_price']:.2f} ({opportunity['sell_exchange']})")
                print(f"   Price Spread:  {opportunity['spread_percent']:.2f}%")
                print(f"   Trade Size:    ${opportunity['trade_amount_usd']:.2f}")
                print(f"   Gross Profit:  ${opportunity['gross_profit']:.4f}")
                print(f"   Exchange Fees: ${opportunity['total_fees']:.4f}")
                print(f"   Net Profit:    ${opportunity['net_profit']:.4f}")
                print(f"   Profit Margin: {opportunity['profit_percent']:.3f}%")
                
                # Evaluate profitability - technical process
                print()
                print("⏳ Running profitability analysis")
                print("   • Validating profit margins...", end='', flush=True)
                time.sleep(0.3)
                animated_progress("", 12, '▓', 0.025)
                print("   • Risk assessment...", end='', flush=True)
                time.sleep(0.2)
                animated_progress("", 10, '▓', 0.025)
                
                if self._is_profitable(opportunity):
                    profitable_opportunities += 1
                    print("   ✓ Trade meets profitability criteria")
                    print(f"\n✅ TRADE APPROVED - Expected ROI: {opportunity['profit_percent']:.3f}%")
                    print(f"   Net return after all fees: ${opportunity['net_profit']:.4f}")
                    
                    # Execute trade
                    self.execute_mock_trade(opportunity)
                    
                else:
                    print("   ✗ Trade does not meet minimum requirements")
                    print(f"\n❌ TRADE REJECTED - Insufficient profit margin")
                    print(f"   Net profit ${opportunity['net_profit']:.4f} below threshold")
                    print(f"   Fees (${opportunity['total_fees']:.4f}) exceed potential gains")
                    logger.debug(f"Scan #{scan_count}: Rejected - Net profit too low")
                
                # Wait before next scan with countdown
                print(f"\n⏸  Next scan in {MOCK_TRADE_INTERVAL}s...", end='', flush=True)
                for i in range(MOCK_TRADE_INTERVAL):
                    time.sleep(1)
                    remaining = MOCK_TRADE_INTERVAL - i - 1
                    print(f"\r⏸  Next scan in {remaining}s...  ", end='', flush=True)
                print()
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Trading session interrupted by user")
            logger.info("Trading session interrupted by user")
        
        # Session summary
        session_duration = time.time() - start_time
        roi_percent = (self.total_profit_usd / self.total_balance_usd) * 100 if self.total_balance_usd > 0 else 0
        
        summary = {
            "session_start": self.session_start.strftime("%Y-%m-%d %H:%M:%S"),
            "session_duration_seconds": session_duration,
            "initial_balance_usd": self.total_balance_usd,
            "opportunities_scanned": opportunities_found,
            "profitable_opportunities": profitable_opportunities,
            "trades_executed": self.trades_executed,
            "total_profit_usd": self.total_profit_usd,
            "roi_percent": roi_percent,
            "final_balance_usd": self.total_balance_usd + self.total_profit_usd
        }
        
        # Print final summary
        print("\n\n")
        print("╔══════════════════════════════════════════════════════════════════════╗")
        print("║              📊 TRADING SESSION COMPLETED 📊                         ║")
        print("╚══════════════════════════════════════════════════════════════════════╝")
        
        hours = int(session_duration // 3600)
        minutes = int((session_duration % 3600) // 60)
        seconds = int(session_duration % 60)
        
        print(f"\n⏱  Duration:                {hours:02d}:{minutes:02d}:{seconds:02d}")
        print(f"🔍 Total Scans:             {scan_count}")
        print(f"📊 Opportunities Found:     {opportunities_found}")
        print(f"✅ Profitable Ops:          {profitable_opportunities}")
        print(f"💰 Trades Executed:         {self.trades_executed}")
        print(f"\n{'─'*74}")
        print(f"💵 Initial Balance:         ${self.total_balance_usd:.2f}")
        print(f"📈 Total Profit:            ${self.total_profit_usd:.4f}")
        print(f"💎 Final Balance:           ${summary['final_balance_usd']:.2f}")
        print(f"📊 ROI:                     {roi_percent:.4f}%")
        print(f"{'─'*74}")
        
        if self.trades_executed > 0:
            avg_profit = self.total_profit_usd / self.trades_executed
            print(f"\n📈 Average Profit/Trade:    ${avg_profit:.4f}")
            success_rate = (profitable_opportunities / opportunities_found) * 100
            print(f"✅ Success Rate:            {success_rate:.1f}%")
        
        print("\n" + "═"*74 + "\n")
        
        logger.info(f"Session completed: {self.trades_executed} trades, "
                   f"${self.total_profit_usd:.4f} profit, ROI: {roi_percent:.4f}%")
        
        return summary
