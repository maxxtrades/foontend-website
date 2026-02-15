<!-- frontend/dashboard.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deriv Pro Trading Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');
        
        * { font-family: 'Inter', sans-serif; }
        .mono { font-family: 'JetBrains Mono', monospace; }
        
        .glass-panel {
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(148, 163, 184, 0.1);
        }
        
        .gradient-text {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .pulse-dot {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: .5; transform: scale(0.9); }
        }
        
        .slide-in { animation: slideIn 0.3s ease-out; }
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .notification-toast {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 100;
            max-width: 400px;
        }
        
        /* Auth screens */
        .auth-container {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        }
    </style>
</head>
<body class="bg-slate-950 text-white min-h-screen">
    <!-- Auth Screen -->
    <div id="authScreen" class="auth-container min-h-screen flex items-center justify-center p-4">
        <div class="glass-panel rounded-2xl p-8 w-full max-w-md">
            <div class="text-center mb-8">
                <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <i class="fas fa-shield-alt text-2xl text-white"></i>
                </div>
                <h1 class="text-2xl font-bold gradient-text">Secure Login</h1>
                <p class="text-slate-400 mt-2">Deriv Pro Trading System</p>
            </div>
            
            <form id="loginForm" class="space-y-4">
                <div>
                    <label class="block text-sm text-slate-400 mb-1">Username</label>
                    <input type="text" id="loginUsername" class="w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500 transition-colors" placeholder="Enter username" required>
                </div>
                <div>
                    <label class="block text-sm text-slate-400 mb-1">Password</label>
                    <input type="password" id="loginPassword" class="w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500 transition-colors" placeholder="Enter password" required>
                </div>
                <div class="flex items-center justify-between text-sm">
                    <label class="flex items-center text-slate-400">
                        <input type="checkbox" class="mr-2 rounded bg-slate-800 border-slate-600"> Remember me
                    </label>
                    <a href="#" class="text-blue-400 hover:text-blue-300">Forgot password?</a>
                </div>
                <button type="submit" class="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-3 rounded-lg transition-all transform hover:scale-[1.02]">
                    Sign In
                </button>
            </form>
            
            <div id="loginError" class="hidden mt-4 p-3 bg-red-500/20 border border-red-500/50 rounded-lg text-red-400 text-sm text-center"></div>
        </div>
    </div>

    <!-- Main Dashboard (Hidden until auth) -->
    <div id="mainDashboard" class="hidden">
        <!-- Navigation -->
        <nav class="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-40">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between h-16 items-center">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                            <i class="fas fa-robot text-white text-sm"></i>
                        </div>
                        <span class="text-xl font-bold gradient-text">Deriv Pro</span>
                        <span class="px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded-full border border-green-500/30 ml-2">
                            <span class="w-1.5 h-1.5 bg-green-400 rounded-full inline-block mr-1 pulse-dot"></span>
                            Live
                        </span>
                    </div>
                    
                    <div class="flex items-center gap-4">
                        <!-- Notifications Bell -->
                        <button onclick="toggleNotifications()" class="relative p-2 text-slate-400 hover:text-white transition-colors">
                            <i class="fas fa-bell text-lg"></i>
                            <span id="notifBadge" class="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full hidden"></span>
                        </button>
                        
                        <button onclick="toggleAutoTrading()" id="autoTradeBtn" class="px-4 py-2 bg-blue-600/20 border border-blue-500/50 hover:bg-blue-600/30 rounded-lg text-sm font-medium transition-colors flex items-center gap-2">
                            <i class="fas fa-pause"></i>
                            <span>Pause Auto</span>
                        </button>
                        
                        <button onclick="openManualTrade()" class="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg text-sm font-medium transition-colors flex items-center gap-2">
                            <i class="fas fa-plus"></i>
                            <span>Quick Trade</span>
                        </button>
                        
                        <div class="relative group">
                            <button class="w-10 h-10 rounded-full bg-gradient-to-br from-slate-700 to-slate-600 flex items-center justify-center border border-slate-500 hover:border-slate-400 transition-colors">
                                <i class="fas fa-user text-slate-300"></i>
                            </button>
                            <!-- Dropdown -->
                            <div class="absolute right-0 mt-2 w-48 bg-slate-800 border border-slate-700 rounded-lg shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
                                <div class="p-3 border-b border-slate-700">
                                    <p class="text-sm font-medium" id="userDisplayName">Admin</p>
                                    <p class="text-xs text-slate-500">Pro Trader</p>
                                </div>
                                <button onclick="openSettings()" class="w-full text-left px-4 py-2 text-sm hover:bg-slate-700 flex items-center gap-2">
                                    <i class="fas fa-cog text-slate-400"></i> Settings
                                </button>
                                <button onclick="logout()" class="w-full text-left px-4 py-2 text-sm hover:bg-slate-700 text-red-400 flex items-center gap-2">
                                    <i class="fas fa-sign-out-alt"></i> Logout
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Notifications Panel -->
        <div id="notifPanel" class="hidden fixed top-16 right-4 w-80 bg-slate-800 border border-slate-700 rounded-lg shadow-2xl z-50 max-h-96 overflow-hidden">
            <div class="p-4 border-b border-slate-700 flex justify-between items-center">
                <h3 class="font-semibold">Notifications</h3>
                <button onclick="markAllRead()" class="text-xs text-blue-400 hover:text-blue-300">Mark all read</button>
            </div>
            <div id="notifList" class="overflow-y-auto max-h-64">
                <!-- Populated by JS -->
            </div>
        </div>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <!-- Account Overview -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div class="glass-panel rounded-xl p-5 relative overflow-hidden group hover:border-blue-500/30 transition-colors">
                    <div class="absolute top-0 right-0 w-24 h-24 bg-blue-500/10 rounded-full -mr-12 -mt-12 blur-xl group-hover:bg-blue-500/20 transition-all"></div>
                    <div class="flex justify-between items-start mb-2">
                        <p class="text-slate-400 text-sm">Balance</p>
                        <i class="fas fa-wallet text-blue-400"></i>
                    </div>
                    <h3 class="text-2xl font-bold mono" id="balance">$0.00</h3>
                    <p class="text-xs text-slate-500 mt-1" id="accountType">Demo Account</p>
                </div>
                
                <div class="glass-panel rounded-xl p-5 relative overflow-hidden group hover:border-purple-500/30 transition-colors">
                    <div class="absolute top-0 right-0 w-24 h-24 bg-purple-500/10 rounded-full -mr-12 -mt-12 blur-xl group-hover:bg-purple-500/20 transition-all"></div>
                    <div class="flex justify-between items-start mb-2">
                        <p class="text-slate-400 text-sm">Daily P&L</p>
                        <i class="fas fa-chart-line text-purple-400"></i>
                    </div>
                    <h3 class="text-2xl font-bold mono" id="dailyPnl">$0.00</h3>
                    <p class="text-xs mt-1" id="pnlPercent">0.00%</p>
                </div>
                
                <div class="glass-panel rounded-xl p-5 relative overflow-hidden group hover:border-orange-500/30 transition-colors">
                    <div class="absolute top-0 right-0 w-24 h-24 bg-orange-500/10 rounded-full -mr-12 -mt-12 blur-xl group-hover:bg-orange-500/20 transition-all"></div>
                    <div class="flex justify-between items-start mb-2">
                        <p class="text-slate-400 text-sm">Open Positions</p>
                        <i class="fas fa-briefcase text-orange-400"></i>
                    </div>
                    <h3 class="text-2xl font-bold mono" id="openPositions">0</h3>
                    <p class="text-xs text-slate-500 mt-1" id="totalExposure">$0.00 exposure</p>
                </div>
                
                <div class="glass-panel rounded-xl p-5 relative overflow-hidden group hover:border-red-500/30 transition-colors cursor-pointer" onclick="openRiskDetails()">
                    <div class="absolute top-0 right-0 w-24 h-24 bg-red-500/10 rounded-full -mr-12 -mt-12 blur-xl group-hover:bg-red-500/20 transition-all"></div>
                    <div class="flex justify-between items-start mb-2">
                        <p class="text-slate-400 text-sm">Risk Status</p>
                        <i class="fas fa-shield-alt text-red-400"></i>
                    </div>
                    <h3 class="text-lg font-bold text-green-400" id="riskStatus">HEALTHY</h3>
                    <div class="w-full bg-slate-700 rounded-full h-1.5 mt-2">
                        <div class="bg-gradient-to-r from-green-500 to-emerald-500 h-1.5 rounded-full transition-all" style="width: 15%" id="riskBar"></div>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Main Content -->
                <div class="lg:col-span-2 space-y-6">
                    <!-- Chart -->
                    <div class="glass-panel rounded-xl p-6">
                        <div class="flex justify-between items-center mb-4">
                            <div class="flex items-center gap-3">
                                <h3 class="font-semibold">Price Chart</h3>
                                <span class="px-2 py-1 bg-slate-700 rounded text-xs mono" id="currentPrice">---.--</span>
                            </div>
                            <div class="flex gap-2">
                                <select id="symbolSelect" onchange="changeSymbol()" class="bg-slate-800 border border-slate-600 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:border-blue-500">
                                    <option value="R_50">Volatility 50</option>
                                    <option value="R_25">Volatility 25</option>
                                    <option value="R_100">Volatility 100</option>
                                    <option value="R_10">Volatility 10</option>
                                    <option value="R_75">Volatility 75</option>
                                </select>
                                <div class="flex bg-slate-800 rounded-lg p-1">
                                    <button class="px-3 py-1 rounded text-xs bg-blue-600 text-white">1m</button>
                                    <button class="px-3 py-1 rounded text-xs text-slate-400 hover:text-white">5m</button>
                                    <button class="px-3 py-1 rounded text-xs text-slate-400 hover:text-white">15m</button>
                                </div>
                            </div>
                        </div>
                        <div class="h-80 bg-slate-900/50 rounded-lg relative">
                            <canvas id="priceChart"></canvas>
                            <!-- Live indicator -->
                            <div class="absolute top-4 left-4 flex items-center gap-2 bg-slate-800/80 px-3 py-1.5 rounded-full border border-slate-700">
                                <span class="w-2 h-2 bg-green-500 rounded-full pulse-dot"></span>
                                <span class="text-xs text-slate-300">Live</span>
                            </div>
                        </div>
                    </div>

                    <!-- Positions Table -->
                    <div class="glass-panel rounded-xl p-6">
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="font-semibold">Active Positions</h3>
                            <button onclick="closeAllPositions()" class="text-xs text-red-400 hover:text-red-300 border border-red-500/30 px-3 py-1 rounded-lg hover:bg-red-500/10 transition-colors">
                                Close All
                            </button>
                        </div>
                        <div class="overflow-x-auto">
                            <table class="w-full text-sm">
                                <thead>
                                    <tr class="text-slate-400 border-b border-slate-700 text-left">
                                        <th class="pb-3 font-medium">Symbol</th>
                                        <th class="pb-3 font-medium">Type</th>
                                        <th class="pb-3 font-medium">Stake</th>
                                        <th class="pb-3 font-medium">Entry</th>
                                        <th class="pb-3 font-medium">Current</th>
                                        <th class="pb-3 font-medium">Expiry</th>
                                        <th class="pb-3 font-medium">Action</th>
                                    </tr>
                                </thead>
                                <tbody id="positionsTable" class="mono text-xs">
                                    <tr>
                                        <td colspan="7" class="py-8 text-center text-slate-500">No open positions</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Recent Activity -->
                    <div class="glass-panel rounded-xl p-6">
                        <h3 class="font-semibold mb-4">Recent Signals</h3>
                        <div class="space-y-3" id="signalsList">
                            <!-- Populated by JS -->
                        </div>
                    </div>
                </div>

                <!-- Sidebar -->
                <div class="space-y-6">
                    <!-- Quick Stats -->
                    <div class="glass-panel rounded-xl p-6">
                        <h3 class="font-semibold mb-4 flex items-center gap-2">
                            <i class="fas fa-tachometer-alt text-blue-400"></i>
                            Performance
                        </h3>
                        <div class="space-y-4">
                            <div class="flex justify-between items-center p-3 bg-slate-800/50 rounded-lg">
                                <span class="text-sm text-slate-400">Win Rate</span>
                                <span class="font-bold text-green-400" id="winRate">--%</span>
                            </div>
                            <div class="flex justify-between items-center p-3 bg-slate-800/50 rounded-lg">
                                <span class="text-sm text-slate-400">Profit Factor</span>
                                <span class="font-bold text-blue-400">--</span>
                            </div>
                            <div class="flex justify-between items-center p-3 bg-slate-800/50 rounded-lg">
                                <span class="text-sm text-slate-400">Avg Trade</span>
                                <span class="font-bold text-slate-300" id="avgTrade">$--</span>
                            </div>
                            <div class="flex justify-between items-center p-3 bg-slate-800/50 rounded-lg">
                                <span class="text-sm text-slate-400">Best Streak</span>
                                <span class="font-bold text-purple-400">--</span>
                            </div>
                        </div>
                    </div>

                    <!-- Risk Management -->
                    <div class="glass-panel rounded-xl p-6">
                        <h3 class="font-semibold mb-4 flex items-center gap-2">
                            <i class="fas fa-shield-alt text-green-400"></i>
                            Risk Controls
                        </h3>
                        
                        <div class="space-y-4">
                            <div>
                                <div class="flex justify-between text-sm mb-2">
                                    <span class="text-slate-400">Daily Risk</span>
                                    <span class="text-white font-medium" id="dailyRiskText">0/5%</span>
                                </div>
                                <div class="w-full bg-slate-700 rounded-full h-2 overflow-hidden">
                                    <div id="dailyRiskBar" class="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-500" style="width: 0%"></div>
                                </div>
                            </div>
                            
                            <div>
                                <div class="flex justify-between text-sm mb-2">
                                    <span class="text-slate-400">Consecutive Losses</span>
                                    <span class="text-white font-medium" id="consecLossesText">0/3</span>
                                </div>
                                <div class="flex gap-1">
                                    <div id="lossInd1" class="h-2 flex-1 bg-slate-700 rounded transition-colors"></div>
                                    <div id="lossInd2" class="h-2 flex-1 bg-slate-700 rounded transition-colors"></div>
                                    <div id="lossInd3" class="h-2 flex-1 bg-slate-700 rounded transition-colors"></div>
                                </div>
                            </div>

                            <div class="pt-4 border-t border-slate-700">
                                <div class="flex justify-between text-sm mb-3">
                                    <span class="text-slate-400">Kelly Fraction</span>
                                    <span class="text-white font-medium">25%</span>
                                </div>
                                <div class="flex justify-between text-sm mb-3">
                                    <span class="text-slate-400">Max Position</span>
                                    <span class="text-white font-medium">2%</span>
                                </div>
                                <button onclick="openRiskSettings()" class="w-full py-2.5 border border-slate-600 hover:bg-slate-700 rounded-lg text-sm transition-colors flex items-center justify-center gap-2">
                                    <i class="fas fa-sliders-h"></i>
                                    Adjust Parameters
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Live Feed -->
                    <div class="glass-panel rounded-xl p-6">
                        <h3 class="font-semibold mb-4">Market Feed</h3>
                        <div class="space-y-2 max-h-48 overflow-y-auto text-xs mono" id="tickFeed">
                            <!-- Populated by WebSocket -->
                        </div>
                    </div>

                    <!-- System Status -->
                    <div class="glass-panel rounded-xl p-6">
                        <h3 class="font-semibold mb-4">System Health</h3>
                        <div class="space-y-3">
                            <div class="flex items-center justify-between p-2 bg-slate-800/50 rounded-lg">
                                <div class="flex items-center gap-2">
                                    <span class="w-2 h-2 bg-green-500 rounded-full pulse-dot"></span>
                                    <span class="text-sm">WebSocket</span>
                                </div>
                                <span class="text-xs text-green-400">Connected</span>
                            </div>
                            <div class="flex items-center justify-between p-2 bg-slate-800/50 rounded-lg">
                                <div class="flex items-center gap-2">
                                    <span class="w-2 h-2 bg-green-500 rounded-full"></span>
                                    <span class="text-sm">API Latency</span>
                                </div>
                                <span class="text-xs text-slate-400 mono" id="latency">24ms</span>
                            </div>
                            <div class="flex items-center justify-between p-2 bg-slate-800/50 rounded-lg">
                                <div class="flex items-center gap-2">
                                    <span class="w-2 h-2 bg-blue-500 rounded-full"></span>
                                    <span class="text-sm">Strategy</span>
                                </div>
                                <span class="text-xs text-blue-400">Mean Reversion</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Manual Trade Modal -->
    <div id="tradeModal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="glass-panel rounded-2xl p-6 w-full max-w-md border border-slate-600 shadow-2xl transform transition-all scale-100">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-xl font-bold">Execute Trade</h3>
                <button onclick="closeModal()" class="text-slate-400 hover:text-white">
                    <i class="fas fa-times text-xl"></i>
                </button>
            </div>
            
            <div class="space-y-5">
                <div>
                    <label class="block text-sm text-slate-400 mb-2">Market</label>
                    <select id="manualSymbol" class="w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500 transition-colors">
                        <option value="R_50">Volatility 50 Index</option>
                        <option value="R_25">Volatility 25 Index</option>
                        <option value="R_100">Volatility 100 Index</option>
                        <option value="R_10">Volatility 10 Index</option>
                        <option value="R_75">Volatility 75 Index</option>
                    </select>
                </div>
                
                <div>
                    <label class="block text-sm text-slate-400 mb-2">Direction</label>
                    <div class="grid grid-cols-2 gap-3">
                        <button onclick="selectDirection('CALL')" id="btnCall" class="py-4 border-2 border-slate-600 rounded-xl hover:border-green-500 hover:bg-green-500/10 transition-all flex flex-col items-center gap-2 group">
                            <i class="fas fa-arrow-up text-2xl text-slate-400 group-hover:text-green-400"></i>
                            <span class="font-semibold text-slate-300 group-hover:text-white">CALL</span>
                            <span class="text-xs text-slate-500">Price Up</span>
                        </button>
                        <button onclick="selectDirection('PUT')" id="btnPut" class="py-4 border-2 border-slate-600 rounded-xl hover:border-red-500 hover:bg-red-500/10 transition-all flex flex-col items-center gap-2 group">
                            <i class="fas fa-arrow-down text-2xl text-slate-400 group-hover:text-red-400"></i>
                            <span class="font-semibold text-slate-300 group-hover:text-white">PUT</span>
                            <span class="text-xs text-slate-500">Price Down</span>
                        </button>
                    </div>
                </div>
                
                <div>
                    <label class="block text-sm text-slate-400 mb-2">Stake Amount</label>
                    <div class="relative">
                        <span class="absolute left-4 top-3.5 text-slate-400 text-lg">$</span>
                        <input type="number" id="manualStake" class="w-full bg-slate-800 border border-slate-600 rounded-lg pl-10 pr-4 py-3 text-lg font-bold focus:outline-none focus:border-blue-500 transition-colors" placeholder="0.00" step="0.01" min="1" max="1000">
                    </div>
                    <div class="flex justify-between mt-2 text-xs">
                        <span class="text-slate-500">Min: $1.00</span>
                        <span class="text-slate-500" id="maxStakeDisplay">Max: $20.00 (2%)</span>
                    </div>
                    <!-- Quick amounts -->
                    <div class="flex gap-2 mt-3">
                        <button onclick="setStake(10)" class="flex-1 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs transition-colors">$10</button>
                        <button onclick="setStake(25)" class="flex-1 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs transition-colors">$25</button>
                        <button onclick="setStake(50)" class="flex-1 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs transition-colors">$50</button>
                        <button onclick="setStake(100)" class="flex-1 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs transition-colors">$100</button>
                    </div>
                </div>

                <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
                    <div class="flex justify-between text-sm mb-1">
                        <span class="text-slate-400">Potential Payout</span>
                        <span class="text-green-400 font-bold" id="potentialPayout">$0.00</span>
                    </div>
                    <div class="flex justify-between text-sm">
                        <span class="text-slate-400">Risk/Reward</span>
                        <span class="text-slate-300">1 : 0.85</span>
                    </div>
                </div>
                
                <button onclick="submitManualTrade()" id="executeBtn" disabled class="w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold rounded-xl transition-all transform hover:scale-[1.02] flex items-center justify-center gap-2">
                    <i class="fas fa-bolt"></i>
                    Execute Trade
                </button>
            </div>
        </div>
    </div>

    <!-- Risk Settings Modal -->
    <div id="riskModal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="glass-panel rounded-2xl p-6 w-full max-w-lg">
            <h3 class="text-xl font-bold mb-6">Risk Management Settings</h3>
            
            <div class="space-y-5">
                <div>
                    <label class="block text-sm text-slate-400 mb-2">Max Position Size (% of balance)</label>
                    <input type="range" id="settingMaxPosition" min="0.5" max="10" step="0.5" value="2" class="w-full mb-2" oninput="updateSettingDisplay('position', this.value)">
                    <div class="flex justify-between text-sm">
                        <span class="text-slate-500">0.5%</span>
                        <span class="text-white font-bold" id="displayPosition">2%</span>
                        <span class="text-slate-500">10%</span>
                    </div>
                </div>

                <div>
                    <label class="block text-sm text-slate-400 mb-2">Daily Risk Limit (%)</label>
                    <input type="range" id="settingDailyRisk" min="1" max="20" step="1" value="5" class="w-full mb-2" oninput="updateSettingDisplay('daily', this.value)">
                    <div class="flex justify-between text-sm">
                        <span class="text-slate-500">1%</span>
                        <span class="text-white font-bold" id="displayDaily">5%</span>
                        <span class="text-slate-500">20%</span>
                    </div>
                </div>

                <div>
                    <label class="block text-sm text-slate-400 mb-2">Kelly Fraction</label>
                    <input type="range" id="settingKelly" min="0.1" max="1" step="0.05" value="0.25" class="w-full mb-2" oninput="updateSettingDisplay('kelly', this.value)">
                    <div class="flex justify-between text-sm">
                        <span class="text-slate-500">10% (Conservative)</span>
                        <span class="text-white font-bold" id="displayKelly">25%</span>
                        <span class="text-slate-500">100% (Full)</span>
                    </div>
                </div>

                <div class="flex gap-3 pt-4">
                    <button onclick="closeRiskModal()" class="flex-1 py-3 border border-slate-600 hover:bg-slate-700 rounded-xl transition-colors">Cancel</button>
                    <button onclick="saveRiskSettings()" class="flex-1 py-3 bg-blue-600 hover:bg-blue-700 rounded-xl font-semibold transition-colors">Save Changes</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Toast Notifications Container -->
    <div id="toastContainer" class="fixed top-4 right-4 z-50 space-y-2"></div>

    <script>
        // Global State
        let authToken = localStorage.getItem('authToken');
        let refreshToken = localStorage.getItem('refreshToken');
        let ws = null;
        let selectedDirection = null;
        let priceChart = null;
        let priceData = [];
        let currentBalance = 0;
        let reconnectAttempts = 0;
        const MAX_RECONNECT_ATTEMPTS = 5;

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            if (authToken) {
                showDashboard();
            } else {
                showAuth();
            }
        });

        // Auth Functions
        function showAuth() {
            document.getElementById('authScreen').classList.remove('hidden');
            document.getElementById('mainDashboard').classList.add('hidden');
        }

        function showDashboard() {
            document.getElementById('authScreen').classList.add('hidden');
            document.getElementById('mainDashboard').classList.remove('hidden');
            initChart();
            connectWebSocket();
            fetchAccountData();
            fetchPositions();
            fetchNotifications();
            
            // Refresh intervals
            setInterval(fetchAccountData, 5000);
            setInterval(fetchPositions, 10000);
            setInterval(fetchNotifications, 30000);
            
            // Token refresh
            setInterval(refreshAccessToken, 25 * 60 * 1000); // Every 25 minutes
        }

        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;
            
            try {
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    authToken = data.access_token;
                    refreshToken = data.refresh_token;
                    localStorage.setItem('authToken', authToken);
                    localStorage.setItem('refreshToken', refreshToken);
                    localStorage.setItem('username', username);
                    
                    showDashboard();
                    showToast('Welcome back!', 'success');
                } else {
                    const error = await response.json();
                    document.getElementById('loginError').textContent = error.detail || 'Login failed';
                    document.getElementById('loginError').classList.remove('hidden');
                }
            } catch (e) {
                document.getElementById('loginError').textContent = 'Network error';
                document.getElementById('loginError').classList.remove('hidden');
            }
        });

        async function refreshAccessToken() {
            try {
                const response = await fetch('/api/auth/refresh', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ refresh_token: refreshToken })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    authToken = data.access_token;
                    refreshToken = data.refresh_token;
                    localStorage.setItem('authToken', authToken);
                    localStorage.setItem('refreshToken', refreshToken);
                }
            } catch (e) {
                console.error('Token refresh failed');
            }
        }

        function logout() {
            fetch('/api/auth/logout', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${authToken}` }
            });
            localStorage.clear();
            authToken = null;
            refreshToken = null;
            ws?.close();
            showAuth();
        }

        // WebSocket with Auth
        function connectWebSocket() {
            if (reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
                showToast('Connection failed. Please refresh.', 'error');
                return;
            }

            const wsUrl = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws/live`;
            ws = new WebSocket(wsUrl);
            
            ws.onopen = () => {
                console.log('WebSocket connected');
                reconnectAttempts = 0;
                // Authenticate
                ws.send(JSON.stringify({ token: authToken }));
            };
            
            ws.onmessage = (event) => {
                const msg = JSON.parse(event.data);
                handleWebSocketMessage(msg);
            };
            
            ws.onclose = () => {
                reconnectAttempts++;
                setTimeout(connectWebSocket, 3000 * reconnectAttempts);
            };
            
            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        }

        function handleWebSocketMessage(msg) {
            if (msg.type === 'auth_success') {
                document.getElementById('userDisplayName').textContent = msg.user;
            } else if (msg.type === 'account_update') {
                updateAccountDisplay(msg.data);
            } else if (msg.type === 'tick') {
                addTick(msg);
                updateChart(msg);
                document.getElementById('currentPrice').textContent = msg.price.toFixed(2);
            } else if (msg.type === 'notification') {
                showNotification(msg.data);
            }
        }

        // Chart Functions
        function initChart() {
            const ctx = document.getElementById('priceChart').getContext('2d');
            priceChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Price',
                        data: [],
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: true,
                        pointRadius: 0,
                        pointHoverRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                            backgroundColor: 'rgba(15, 23, 42, 0.9)',
                            titleColor: '#94a3b8',
                            bodyColor: '#fff',
                            borderColor: 'rgba(148, 163, 184, 0.2)',
                            borderWidth: 1
                        }
                    },
                    scales: {
                        x: { 
                            display: false,
                            grid: { display: false }
                        },
                        y: { 
                            grid: { color: 'rgba(148, 163, 184, 0.1)' },
                            ticks: { 
                                color: '#94a3b8',
                                callback: function(value) { return value.toFixed(2); }
                            }
                        }
                    },
                    interaction: {
                        mode: 'nearest',
                        axis: 'x',
                        intersect: false
                    }
                }
            });
        }

        function updateChart(tick) {
            priceData.push(tick.price);
            if (priceData.length > 100) priceData.shift();
            
            priceChart.data.labels = Array(priceData.length).fill('');
            priceChart.data.datasets[0].data = priceData;
            priceChart.update('none');
        }

        // UI Updates
        function updateAccountDisplay(data) {
            currentBalance = data.balance;
            document.getElementById('balance').textContent = '$' + data.balance.toFixed(2);
            document.getElementById('dailyPnl').textContent = (data.daily_pnl >= 0 ? '+' : '') + '$' + data.daily_pnl.toFixed(2);
            document.getElementById('dailyPnl').className = 'text-2xl font-bold mono ' + (data.daily_pnl >= 0 ? 'text-green-400' : 'text-red-400');
            document.getElementById('openPositions').textContent = data.open_positions_count;
            document.getElementById('totalExposure').textContent = '$' + data.total_exposure.toFixed(2) + ' exposure';
            document.getElementById('accountType').textContent = data.is_virtual ? 'Demo Account' : 'Real Account';
            
            // Update max stake display
            const maxStake = (data.balance * 0.02).toFixed(2);
            document.getElementById('maxStakeDisplay').textContent = `Max: $${maxStake} (2%)`;
        }

        function addTick(tick) {
            const feed = document.getElementById('tickFeed');
            const div = document.createElement('div');
            const prevPrice = priceData.length > 1 ? priceData[priceData.length - 2] : tick.price;
            const isUp = tick.price >= prevPrice;
            
            div.className = 'flex justify-between items-center py-2 border-b border-slate-700/50';
            div.innerHTML = `
                <span class="text-slate-400">${tick.symbol}</span>
                <span class="${isUp ? 'text-green-400' : 'text-red-400'} font-bold">
                    ${isUp ? '▲' : '▼'} ${tick.price.toFixed(2)}
                </span>
                <span class="text-slate-500 text-xs">${new Date().toLocaleTimeString()}</span>
            `;
            feed.insertBefore(div, feed.firstChild);
            if (feed.children.length > 20) feed.removeChild(feed.lastChild);
        }

        // API Functions
        async function fetchAccountData() {
            try {
                const response = await fetch('/api/account', {
                    headers: { 'Authorization': `Bearer ${authToken}` }
                });
                if (response.ok) {
                    const data = await response.json();
                    updateAccountDisplay(data);
                } else if (response.status === 401) {
                    logout();
                }
            } catch (e) {
                console.error('Fetch account error:', e);
            }
        }

        async function fetchPositions() {
            try {
                const response = await fetch('/api/positions', {
                    headers: { 'Authorization': `Bearer ${authToken}` }
                });
                if (response.ok) {
                    const positions = await response.json();
                    updatePositionsTable(positions);
                }
            } catch (e) {
                console.error('Fetch positions error:', e);
            }
        }

        function updatePositionsTable(positions) {
            const tbody = document.getElementById('positionsTable');
            if (positions.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" class="py-8 text-center text-slate-500">No open positions</td></tr>';
                return;
            }
            
            tbody.innerHTML = positions.map(pos => `
                <tr class="border-b border-slate-700/50 hover:bg-slate-800/30 transition-colors">
                    <td class="py-3 text-slate-300">${pos.symbol}</td>
                    <td class="py-3">
                        <span class="px-2 py-1 rounded text-xs ${pos.type === 'CALL' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}">
                            ${pos.type}
                        </span>
                    </td>
                    <td class="py-3">$${pos.stake.toFixed(2)}</td>
                    <td class="py-3 text-slate-400">${pos.entry_price.toFixed(2)}</td>
                    <td class="py-3">
                        <span class="${pos.current_pnl_indicator ? 'text-green-400' : 'text-red-400'}">
                            ${pos.current_pnl_indicator ? '▲ In Profit' : '▼ Losing'}
                        </span>
                    </td>
                    <td class="py-3 text-slate-400">${new Date(pos.expiry_time).toLocaleTimeString()}</td>
                    <td class="py-3">
                        <button onclick="closePosition('${pos.id}')" class="text-red-400 hover:text-red-300 text-xs border border-red-500/30 px-2 py-1 rounded hover:bg-red-500/10 transition-colors">
                            Close
                        </button>
                    </td>
                </tr>
            `).join('');
        }

        async function fetchNotifications() {
            try {
                const response = await fetch('/api/notifications?unread_only=true', {
                    headers: { 'Authorization': `Bearer ${authToken}` }
                });
                if (response.ok) {
                    const notifs = await response.json();
                    updateNotificationBadge(notifs.length);
                }
            } catch (e) {}
        }

        // Trading Functions
        function openManualTrade() {
            document.getElementById('tradeModal').classList.remove('hidden');
            updatePotentialPayout();
        }

        function closeModal() {
            document.getElementById('tradeModal').classList.add('hidden');
            selectedDirection = null;
            document.getElementById('btnCall').classList.remove('border-green-500', 'bg-green-500/10');
            document.getElementById('btnPut').classList.remove('border-red-500', 'bg-red-500/10');
            document.getElementById('executeBtn').disabled = true;
        }

        function selectDirection(dir) {
            selectedDirection = dir;
            document.getElementById('btnCall').classList.toggle('border-green-500', dir === 'CALL');
            document.getElementById('btnCall').classList.toggle('bg-green-500/10', dir === 'CALL');
            document.getElementById('btnPut').classList.toggle('border-red-500', dir === 'PUT');
            document.getElementById('btnPut').classList.toggle('bg-red-500/10', dir === 'PUT');
            document.getElementById('executeBtn').disabled = false;
        }

        function setStake(amount) {
            document.getElementById('manualStake').value = amount;
            updatePotentialPayout();
        }

        function updatePotentialPayout() {
            const stake = parseFloat(document.getElementById('manualStake').value) || 0;
            const payout = stake * 1.85; // 85% return
            document.getElementById('potentialPayout').textContent = '$' + payout.toFixed(2);
        }

        document.getElementById('manualStake').addEventListener('input', updatePotentialPayout);

        async function submitManualTrade() {
            if (!selectedDirection) return;
            
            const stake = parseFloat(document.getElementById('manualStake').value);
            if (!stake || stake < 1) {
                showToast('Minimum stake is $1.00', 'error');
                return;
            }

            const btn = document.getElementById('executeBtn');
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Executing...';

            try {
                const response = await fetch('/api/trade', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${authToken}`
                    },
                    body: JSON.stringify({
                        symbol: document.getElementById('manualSymbol').value,
                        direction: selectedDirection,
                        stake: stake,
                        duration: 5
                    })
                });

                if (response.ok) {
                    const data = await response.json();
                    closeModal();
                    showToast(`Trade executed! Risk: ${data.risk_percent.toFixed(1)}%`, 'success');
                    fetchPositions();
                    fetchAccountData();
                } else {
                    const error = await response.json();
                    showToast(error.detail || 'Trade failed', 'error');
                }
            } catch (e) {
                showToast('Network error', 'error');
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-bolt"></i> Execute Trade';
            }
        }

        // Risk Settings
        function openRiskSettings() {
            document.getElementById('riskModal').classList.remove('hidden');
        }

        function closeRiskModal() {
            document.getElementById('riskModal').classList.add('hidden');
        }

        function updateSettingDisplay(type, value) {
            document.getElementById(`display${type.charAt(0).toUpperCase() + type.slice(1)}`).textContent = 
                type === 'kelly' ? `${Math.round(value * 100)}%` : `${value}%`;
        }

        async function saveRiskSettings() {
            const settings = {
                max_position_size: parseFloat(document.getElementById('settingMaxPosition').value),
                max_daily_risk: parseFloat(document.getElementById('settingDailyRisk').value),
                kelly_fraction: parseFloat(document.getElementById('settingKelly').value)
            };

            try {
                const response = await fetch('/api/risk/settings', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${authToken}`
                    },
                    body: JSON.stringify(settings)
                });

                if (response.ok) {
                    closeRiskModal();
                    showToast('Risk settings updated', 'success');
                }
            } catch (e) {
                showToast('Failed to update settings', 'error');
            }
        }

        // Notifications
        function toggleNotifications() {
            document.getElementById('notifPanel').classList.toggle('hidden');
        }

        function updateNotificationBadge(count) {
            const badge = document.getElementById('notifBadge');
            if (count > 0) {
                badge.classList.remove('hidden');
            } else {
                badge.classList.add('hidden');
            }
        }

        function showNotification(data) {
            showToast(data.body, data.priority === 'high' ? 'warning' : 'info');
            updateNotificationBadge(1);
        }

        // Toast System
        function showToast(message, type = 'info') {
            const container = document.getElementById('toastContainer');
            const toast = document.createElement('div');
            
            const colors = {
                success: 'bg-green-500',
                error: 'bg-red-500',
                warning: 'bg-orange-500',
                info: 'bg-blue-500'
            };
            
            const icons = {
                success: 'fa-check-circle',
                error: 'fa-exclamation-circle',
                warning: 'fa-exclamation-triangle',
                info: 'fa-info-circle'
            };
            
            toast.className = `${colors[type]} text-white px-6 py-4 rounded-lg shadow-2xl flex items-center gap-3 slide-in min-w-[300px]`;
            toast.innerHTML = `
                <i class="fas ${icons[type]} text-xl"></i>
                <span class="font-medium">${message}</span>
                <button onclick="this.parentElement.remove()" class="ml-auto text-white/80 hover:text-white">
                    <i class="fas fa-times"></i>
                </button>
            `;
            
            container.appendChild(toast);
            setTimeout(() => {
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(100%)';
                setTimeout(() => toast.remove(), 300);
            }, 5000);
        }

        // Utility Functions
        function changeSymbol() {
            const symbol = document.getElementById('symbolSelect').value;
            priceData = [];
            showToast(`Switched to ${symbol}`, 'info');
        }

        async function closePosition(positionId) {
            // Implementation for early close if supported
            showToast('Close position request sent', 'info');
        }

        function closeAllPositions() {
            if (confirm('Close all open positions?')) {
                showToast('Closing all positions...', 'warning');
            }
        }

        function openRiskDetails() {
            // Show detailed risk modal
        }

        function openSettings() {
            openRiskSettings();
        }

        function toggleAutoTrading() {
            const btn = document.getElementById('autoTradeBtn');
            const isPaused = btn.innerHTML.includes('Resume');
            
            fetch(`/api/system/${isPaused ? 'resume' : 'pause'}`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${authToken}` }
            });
            
            btn.innerHTML = isPaused ? 
                '<i class="fas fa-pause"></i><span>Pause Auto</span>' : 
                '<i class="fas fa-play"></i><span>Resume Auto</span>';
            btn.classList.toggle('bg-yellow-600/20', !isPaused);
            btn.classList.toggle('border-yellow-500/50', !isPaused);
            btn.classList.toggle('text-yellow-400', !isPaused);
            
            showToast(isPaused ? 'Auto trading resumed' : 'Auto trading paused', 'info');
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeModal();
                closeRiskModal();
            }
            if (e.key === 'n' && e.ctrlKey) {
                e.preventDefault();
                openManualTrade();
            }
        });
    </script>
</body>
</html>

