//@version=5
indicator("SMC + Multi-EMA + FVG + MACD + Trendline + RSI + ADX + Volume Strategy", overlay=true, max_lines_count=500, max_boxes_count=500)

// ═════════════════════════════════════════════════════════════════════════════
// INPUTS
// ═════════════════════════════════════════════════════════════════════════════

// EMA Settings
ema9_len = input.int(9, "EMA 9 Length", group="EMA Settings")
ema50_len = input.int(50, "EMA 50 Length", group="EMA Settings")
ema200_len = input.int(200, "EMA 200 Length", group="EMA Settings")

// SMC Settings
show_swing_points = input.bool(true, "Show Swing High/Low", group="SMC Settings")
swing_length = input.int(5, "Swing Lookback", group="SMC Settings")
show_order_blocks = input.bool(true, "Show Order Blocks", group="SMC Settings")
ob_lookback = input.int(5, "Order Block Lookback", group="SMC Settings")

// FVG Settings
show_fvg = input.bool(true, "Show Fair Value Gaps", group="FVG Settings")
fvg_lookback = input.int(50, "FVG Lookback", group=# Robotic-ai.02
sk-emergent-dB47c5eCf3fF4EfBf4
