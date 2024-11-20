// >> 21/11/2022
const currentDate = window.document.querySelector(".current-date"),
    days = window.document.querySelector(".days"),
    icons = window.document.querySelectorAll(".icons span")

let selectedItem = null;

let date = new Date()
let currentYear = date.getFullYear()
let currentMonth = date.getMonth()
const month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", 'October', "November", "December"]
let scheduled_date = '';

function getDMY(str) {
    // Split the string into parts based on comma and space
    const parts = str.split(", ");
    // Extract the day, month, and year from the parts
    const yearPart = parts[1];
    const monthYearPart = parts[0];

    // Get the month and year from the monthYearPart
    const [monthString, dayPart] = monthYearPart.split(" ");
    const monthPart = new Date(`${monthString} 1, 2000`).getMonth();
    return [dayPart, monthPart, yearPart];
}


const renderCalandar = () => {
    let lastDayOfMonth = new Date(currentYear, currentMonth + 1, 0).getDate(),
        lastDayOfLastMonth = new Date(currentYear, currentMonth, 0).getDate(),
        lastDay_OfMonth = new Date(currentYear, currentMonth, lastDayOfMonth).getDay(),
        firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();


    const [dayPart, monthPart, yearPart] = getDMY(scheduled_date);
    console.log(getDMY(scheduled_date));

    let lists = ""
    for (let i = firstDayOfMonth; i > 0; i--) {
        lists += `<li class="inactive">${lastDayOfLastMonth - i + 1}</li>`
    }
    for (let i = 1; i <= lastDayOfMonth; i++) {
        let isDay = i === date.getDate() && currentMonth == new Date().getMonth() && currentYear === new Date().getFullYear() ? "today" : "";
        let isScheduled = i == dayPart && currentMonth == monthPart && currentYear == yearPart ? "active" : "";
        if (
            (currentYear === new Date().getFullYear() && currentMonth === new Date().getMonth() && i < date.getDate()) ||
            (currentYear === new Date().getFullYear() && currentMonth < new Date().getMonth()) ||
            currentYear < new Date().getFullYear()
        )
            lists += `<li class="inactive ${isDay}">${i}</li>`
        else
            lists += `<li x-on:click="OnClickedSelectedDate(${i})" class="item ${isDay} ${isScheduled}">${i}</li>`
    }
    for (let i = lastDay_OfMonth; i < 6; i++) {
        lists += `<li class="inactive">${i - lastDay_OfMonth + 1}</li>`
    }
    currentDate.innerHTML = `${month[currentMonth]} ${currentYear}`
    days.innerHTML = lists;

    window.document.querySelectorAll(".item").forEach(item => {
        item.addEventListener("click", (event) => {
            if (selectedItem != null)
                selectedItem.classList.remove("active");
            selectedItem = item;
            item.classList.add("active");

            let day = item.innerHTML || element;
            const year = currentYear;
            const month = 8 < currentMonth ? currentMonth + 1 : `0${currentMonth + 1}`;
            day = day > 9 ? day : `0${day}`;
            window.document.getElementById("id_date").value = `${year}-${month}-${day}`;
        })
    })
}


let selectedTime = null;

function _24format(time) {
    var splitTime = time.split(':');
    var hours = parseInt(splitTime[0]);
    var minutes = parseInt(splitTime[1]);

    if (time.includes('PM') && hours !== 12) {
        hours += 12;
    }
    return ('00' + hours).slice(-2) + ':' + ('00' + minutes).slice(-2);
}

document.addEventListener('DOMContentLoaded', function () {
    const dates = window.document.getElementById('dates').value;
    renderCalandar(dates)
    icons.forEach((icon) => {
        icon.addEventListener("click", () => {
            if (icon.id === 'prev') {
                currentMonth = currentMonth - 1
            } else {
                currentMonth = currentMonth + 1
            }
            if (currentMonth < 0 || currentMonth > 11) {
                date = new Date(currentYear, currentMonth)
                currentYear = date.getFullYear()
                currentMonth = date.getMonth()
            } else {
                date = new Date()
            }
            renderCalandar(dates)
        })
    })


    /*
    window.document.querySelectorAll(".time-slot-item").forEach((item, i) => {
        item.addEventListener("click", () => {
            if (selectedTime != null) {
                selectedTime.classList.remove("active");
            }
            selectedTime = item;
            selectedTime.classList.add("active");

            window.document.getElementById("id_time").value = _24format(item.getAttribute("data"));
        })
    })
     */

});