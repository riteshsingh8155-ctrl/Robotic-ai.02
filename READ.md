# 🌸 Robotic AI Trading Dashboard 🌸

Ye meri free trading dashboard website hai.

### Features:
- 📈 Live BTC, GOLD, SILVER Charts
- 📊 Robotic AI Trade Strategy 
- 🤖 Claude AI Access

### Website Link:
https://riteshsingh8155-ctrl.github.io/Robotic-ai.02/

Made by Ritesh
# Angel se LTP nikalne ka code
def get_ltp(obj, symboltoken):
    try:
        ltp_data = obj.ltpData(exchange="NSE", tradingsymbol="NIFTY 50", symboltoken="99926000")
        return ltp_data['data']['ltp']
    except:
        return 0
<select id="symbol">
  <option value="AAPL">NIFTY</option>  <!-- YE GALAT HAI -->
  <option value="TSLA">BANKNIFTY</option>
</select>
<select id="symbol">
  <option value="99926000">NIFTY 50</option>  <!-- Angel ka token -->
  <option value="99926009">BANKNIFTY</option> <!-- Angel ka token -->
  <option value="3045">RELIANCE</option>      <!-- Angel ka token -->
<
