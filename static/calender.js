document.addEventListener("DOMContentLoaded", function () {
    const calendarGrid = document.querySelector(".calendar-grid");
    const currentMonthDisplay = document.getElementById("current-month");

    const today = new Date();
    let currentMonth = today.getMonth();
    let currentYear = today.getFullYear();

    function renderCalendar(year, month) {
        calendarGrid.innerHTML = `
            <div class="calendar-day">Sun</div>
            <div class="calendar-day">Mon</div>
            <div class="calendar-day">Tue</div>
            <div class="calendar-day">Wed</div>
            <div class="calendar-day">Thu</div>
            <div class="calendar-day">Fri</div>
            <div class="calendar-day">Sat</div>
        `;

        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        for (let i = 0; i < firstDay; i++) {
            calendarGrid.innerHTML += `<div></div>`;
        }

        for (let date = 1; date <= daysInMonth; date++) {
            const dateDiv = document.createElement("div");
            dateDiv.className = "calendar-date";
            dateDiv.textContent = date;
            dateDiv.dataset.date = `${year}-${String(month + 1).padStart(2, "0")}-${String(date).padStart(2, "0")}`;
            dateDiv.addEventListener("click", () => alert(`Selected date: ${dateDiv.dataset.date}`));
            calendarGrid.appendChild(dateDiv);
        }

        currentMonthDisplay.textContent = `${year}-${String(month + 1).padStart(2, "0")}`;
    }

    document.getElementById("prev-month").addEventListener("click", () => {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        renderCalendar(currentYear, currentMonth);
    });

    document.getElementById("next-month").addEventListener("click", () => {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        renderCalendar(currentYear, currentMonth);
    });

    renderCalendar(currentYear, currentMonth);
});
