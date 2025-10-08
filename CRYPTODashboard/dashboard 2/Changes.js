const fetchCryptoDataAtTime = async (coin, time) => {
    const apiUrl = `https://api.binance.com/api/v3/klines?symbol=${coin}USDT&interval=1d&startTime=${time}&endTime=${time + 86400000}`;
    const response = await fetch(apiUrl);
    const data = await response.json();

    if (data.length === 0) {
        throw new Error('No data available for the specified time.');
    }

    const priceAtTime = parseFloat(data[0][4]); // Closing price of the first entry
    return priceAtTime;
};

document.getElementById('calculate_change').addEventListener('click', async function() {
    const coin = document.getElementById('Coin1').value;
    const fromTime = new Date(document.getElementById('fromTime').value).getTime();
    const toTime = new Date(document.getElementById('toTime').value).getTime();

    try {
        const priceAtStartTime = await fetchCryptoDataAtTime(coin, fromTime);
        const priceAtEndTime = await fetchCryptoDataAtTime(coin, toTime);

        const priceChange = priceAtEndTime - priceAtStartTime;
        const priceChangePercent = ((priceChange / priceAtStartTime) * 100).toFixed(2);

        document.getElementById('difference').innerText = `Start Time Price: ${priceAtStartTime}, End Time Price: ${priceAtEndTime}, Price Change: ${priceChange}, Change Percent: ${priceChangePercent}%`;
    } catch (error) {
        console.error('Error fetching crypto data:', error);
        document.getElementById('difference').innerText = 'Error fetching data. Please check inputs.';
    }
});