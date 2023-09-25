const ctx = document.getElementById('myChart').getContext('2d');
const ctx2 = document.getElementById('myChart2').getContext('2d');

const data = {
    labels: genres,
    datasets: [{
        label: 'Music Genre 2021',
        data: probability,
        backgroundColor: [
            'rgb(108, 16, 244)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)',
            'rgb(137, 19, 141)',
            'rgb(201, 42, 42)'
        ],
        hoverOffset: 4
    }]
};

const config = {
    type: 'doughnut',
    data: data,
};

const data2 = {
    labels: [
      'Danceability',
      'Energy',
      'Speechiness',
      'Acousticness',
      'Instrumentalness',
      'Valence',
    ],
    datasets: [{
      label: '',
      data: features,
      fill: true,
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      borderColor: 'rgb(255, 99, 132)',
      pointBackgroundColor: 'rgb(255, 99, 132)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgb(255, 99, 132)'
    }]
  };

  const config2 = {
    type: 'radar',
    data: data2,
    options: {
      elements: {
        line: {
          borderWidth: 3
        }
      }
    },
  };

const myChart = new Chart(ctx, config)
const myChart2 = new Chart(ctx2, config2)