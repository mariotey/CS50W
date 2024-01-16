const days_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
const time_list = ["0600 to 0700", "0700 to 0800", "0800 to 0900", "0900 to 1000", "1000 to 1100", "1100 to 1200", "1200 to 1300", "1300 to 1400", "1400 to 1500", "1500 to 1600", "1600 to 1700", "1700 to 1800", "1800 to 1900", "1900 to 2000", "2000 to 2100", "2100 to 2200", "2200 to 2300", "2300 to 0000"];
const month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

function render_table() {
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const day = currentDate.getDate();

    const dateHeader = document.createElement("h1");
    dateHeader.innerHTML = `${day} ${month_list[month]} ${year}`;
    document.querySelector("#header").append(dateHeader);

    for(let time = 0; time < time_list.length; time++){
        const timeDiv = document.createElement("div");
        timeDiv.innerHTML = time_list[time];
        timeDiv.className = "timeblock";
        document.querySelector("#time_container").append(timeDiv);
    }

    for(let day = 0; day < days_list.length; day++){
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
            }

            timeDivContainer.append(timeDiv);
        }

        console.log(timeDivContainer);

        document.querySelector("#timetable_container").append(timeDivContainer);
    }
}
