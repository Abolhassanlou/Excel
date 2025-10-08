(() => {
  'use strict';
  const fetchHistoricalData = (coin ='BTC', interval ='1d') => {
    //const currentUnixTimestamp = Math.floor(Date.now() / 1000);
    //console.log(currentUnixTimestamp); // Log the current Unix timestamp  
    
    // Construct the API URL with the updated parameters
    fetch(`https://api.binance.com/api/v3/klines?symbol=${coin}USDT&interval=${interval}`)

      .then(response => response.json())
      .then(data => {
        const dataPastYear=data.slice(-365);
        const labels = dataPastYear.map(item =>{
          const date =new Date(item[0]);
          const day=date.getDate();
          const month=date.toLocaleString('default', {month:'short'});
          const year=date.getFullYear().toString().slice(-2);
          return `${day} ${month} ${year}`;
        
        } );
        const closePrices = dataPastYear.map(item => parseFloat(item[4]));
        myChart.data.labels = labels;
        myChart.data.datasets[0].data = closePrices;
        myChart.update();
      })
      .catch(error => {
        console.error('Error fetching historical Data:', error);
      });
  };

  // Graphs
  const ctx = document.getElementById('myChart');
  // eslint-disable-next-line no-unused-vars
  const myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],

      datasets: [{
        label: 'Close Price',
        data: [],

        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          boxPadding: 3
        }
      }
    }
  });
  
  document.getElementById('send').addEventListener('click', function(){
    const coin=document.getElementById('Coin').value;
    const interval=document.getElementById('Interval').value;
    fetchHistoricalData(coin,interval);

  })
  fetchHistoricalData(); // Call the function to fetch data when the script is executed
})();
