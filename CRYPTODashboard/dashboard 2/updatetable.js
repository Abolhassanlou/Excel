const fetchCryptoData = async (coin, interval = '1d') => {

    const apiUrl = `https://api.binance.com/api/v3/klines?symbol=${coin}USDT&interval=${interval}`;
    const response = await fetch(apiUrl);
    const data = await response.json();
    
    const currentPrice = parseFloat(data[data.length - 1][4]);
    const previousPrice = parseFloat(data[data.length - 2][4]);

    const priceChange = currentPrice - previousPrice;
    const priceChangePercent = ((priceChange / previousPrice) * 100).toFixed(2);

    return { currentPrice, priceChange, priceChangePercent };
};
const cryptocurrencies = ['BTC', 'ETH', 'BNB', 'ADA', 'FTM', 'PEPE'];

const updateTable=async()=> {
    const selectedInterval = document.getElementById('Interval').value;
    

    for (const crypto of cryptocurrencies){
        //construct Ids for table cells
        const priceCellId=`${crypto}_price`;
        const intervalCellId = `${crypto}_interval`;
        const changeCellId = `${crypto}_change`;
        const changePercentCellId = `${crypto}_change_percent`;

        const { currentPrice, priceChange, priceChangePercent } = await fetchCryptoData(crypto, selectedInterval);

        document.getElementById(priceCellId).textContent = currentPrice;
        document.getElementById(intervalCellId).textContent = selectedInterval;
        document.getElementById(changeCellId).textContent = priceChange;
        document.getElementById(changePercentCellId).textContent = priceChangePercent + '%';
  }

};

// Update the table with the default interval when the script is executed
updateTable();

document.getElementById('send').addEventListener('click', function(){
   // document.getElementById('Interval').addEventListener('change', function() {
    const selectedInterval = this.value;
    updateTable(selectedInterval);
  });
