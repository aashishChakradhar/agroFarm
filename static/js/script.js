function generateDateList(startDate, endDate) {
  const dateList = [];
  let currentDate = new Date(startDate);

  while (currentDate <= new Date(endDate)) {
    // Format the date as "day short-month"
    const day = currentDate.getDate();
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const month = monthNames[currentDate.getMonth()];

    // Add formatted date to the list
    dateList.push(`${day} ${month}`);

    // Increment the current date by 1 day
    currentDate.setDate(currentDate.getDate() + 1);
  }

  return dateList;
}

document.addEventListener("DOMContentLoaded", () => {
  let data = {};

  document.querySelectorAll('.order-date-list li').forEach((item) => {
    const amount = item.querySelector('.tprice').innerHTML;
    const date = item.querySelector('.cdate').innerHTML.split(',')[0];

    if (!data[date]) {
      data[date] = [];
    }
    data[date].push(amount);
  });

  let amounts = [];
  Object.keys(data).forEach((item) => {
    let q = 0;
    data[item].forEach((e) => {
      q+=parseFloat(e);
    })
    amounts.push(q);
  })

  if(document.getElementById('myChart')){
    const xValues = Object.keys(data);
    const yValues = amounts;

    new Chart("myChart", {
      type: "line",
      data: {
        labels: xValues,
        datasets: [{
          fill: false,
          lineTension: 0,
          backgroundColor: "rgba(0,0,255,1.0)",
          borderColor: "rgba(0,0,255,0.1)",
          data: yValues
        }]
      },
      options: {
        legend: {display: false},
        scales: {
          yAxes: [{ticks: {min: 0, max:2000, stepSize: 100 }}],
        }
      }
    });
  }

  if(document.getElementById('editorContent') && document.querySelector('#editor .ql-editor')){
    document.querySelector('#editor .ql-editor').innerHTML = document.getElementById('editorContent').value;
  }
});