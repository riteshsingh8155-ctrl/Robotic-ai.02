<!DOCTYPE html>
<html>
<head>
<title>AI Signal Bot Dashboard</title>
<script src="https://s3.tradingview.com/tv.js"></script>
</head>
<body>
<h1>AI Signal Bot Dashboard</h1>

<select id="symbol" style="padding:10px; border-radius:5px; background:#00FF7F; border:none;">
  <option value="NSE:NIFTY 50">NIFTY 50</option>
  <option value="NSE:NIFTY BANK">BANKNIFTY</option>
</select>

<div id="tradingview_chart"></div>

<script>
function loadChart(symbol) {
  new TradingView.widget({
    "symbol": symbol,
    "container_id": "tradingview_chart",
    "interval": "1",
    "theme": "dark"
  });
}
loadChart("NSE:NIFTY 50");
</script>

</body>
</html>
