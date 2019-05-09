function init() {
    let tHeads = document.querySelectorAll('th');
    let currentDay = document.getElementById('current-day');
    for (let head of tHeads) {
        head.style.backgroundColor = 'aqua';
        if (head.textContent === currentDay.value) {
            head.style.backgroundColor = 'blue';
            break
        }
    }


}

document.addEventListener('DOMContentLoaded', function () {
    init();
    fetch('api/day-scales')
        .then(response => {
            return response.json()
        })
        .then(data => {
            let dayScales = data['day_scales'];
            for (let scale of dayScales) {
                let tdContent = document.getElementById(scale['num_of_day']);
                tdContent.textContent = scale['scales'];

            }
        })

});
