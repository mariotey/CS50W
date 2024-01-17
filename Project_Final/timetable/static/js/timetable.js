const days_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
const time_list = ["06:00 to 07:00", "07:00 to 08:00", "08:00 to 09:00", "09:00 to 10:00", "10:00 to 11:00", "11:00 to 12:00", "12:00 to 13:00", "13:00 to 14:00", "14:00 to 15:00", "15:00 to 16:00", "16:00 to 17:00", "17:00 to 18:00", "18:00 to 19:00", "19:00 to 20:00", "20:00 to 21:00", "21:00 to 22:00", "22:00 to 23:00", "23:00 to 00:00"];
const month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

function render_table(start_date, end_date, events) {
    const dateHeader = document.createElement("h1");
    dateHeader.innerHTML = `${start_date.getDate()} ${month_list[start_date.getMonth()]} ${start_date.getFullYear()} <em> to </em> ${end_date.getDate()} ${month_list[end_date.getMonth()]} ${end_date.getFullYear()}`;
    document.querySelector("#header").append(dateHeader);

    for(let time = 0; time < time_list.length; time++) {
        const timeDiv = document.createElement("div");
        timeDiv.innerHTML = time_list[time];
        timeDiv.className = "timeblock";
        document.querySelector("#time_container").append(timeDiv);
    }

    for(let day = 0; day < days_list.length; day++) {
        const timeDivContainer = document.createElement("div");
        timeDivContainer.style.display = "flex";
        timeDivContainer.style.justifyContent = "center";
        timeDivContainer.style.textAlign = "center";

        for(let time_div = 0; time_div < document.querySelector("#time_container").querySelectorAll("div").length; time_div++){
            const timeDiv = document.createElement("div");

            if (time_div == 0){
                timeDiv.className = "dayCol timeblock";
                timeDiv.innerHTML = days_list[day];
            }
            else{
                timeDiv.className = "timeblock";
                timeDiv.id = `timeslot_${day}_${time_div - 1}`;

            }

            timeDivContainer.append(timeDiv);
        }

        document.querySelector("#timetable_container").append(timeDivContainer);
    }

    for(let idx = 0; idx < events.length; idx++){
        var event_start_day = new Date(events[idx].fields.start_datetime).getDay();
        var event_start_time = events[idx].fields.start_time.split(":").slice(0, 2).join(":");

        var event_end_day = new Date(events[idx].fields.end_datetime).getDay();
        var event_end_time = events[idx].fields.end_time.split(":").slice(0, 2).join(":");

        console.log(`${event_start_day}(${event_start_time}) until ${event_end_day}(${event_end_time})`);

        var start_idx = time_list.findIndex(item => item.includes(`${event_start_time} to`));
        var end_idx = time_list.findIndex(item => item.includes(`${event_end_time} to`));

        console.log(`${start_idx} to ${end_idx}`);

        for (let dayslot = event_start_day; dayslot <= event_end_day; dayslot++){
            for (let timeslot = start_idx; timeslot < end_idx; timeslot++) {
                var timeSlotElm = document.querySelector(`#timeslot_${(dayslot-1).toString()}_${timeslot.toString()}`);

                console.log(timeSlotElm);

                var timeDiv = document.createElement("div");
                timeDiv.innerHTML = events[idx].fields.name;
                timeDiv.style.backgroundColor = "green";

                timeSlotElm.append(timeDiv);
            }
        }

    }
}
