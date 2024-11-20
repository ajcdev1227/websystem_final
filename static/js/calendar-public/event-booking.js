// (function () {
//     const calElem = document.getElementById('event-calendar')
//     const cal = jsCalendar.new(calElem)
//
//     const now = new Date()
//     cal.min(`${now.getDate()}/${now.getMonth() + 1}/${now.getFullYear()}`)
//
//     PetiteVue.createApp({
//         isLoadingAvailableTimes: false,
//
//         /**
//          * @type {Date[]}
//          */
//         availableTimes: [],
//
//         /**
//          * The currently selected date.
//          * While the object may contain time data, it should be ignored.
//          */
//         selectedDate: new Date(),
//
//         /**
//          * The currently selected time.
//          * While the object may contain date data, it should be ignored.
//          * Only hours and minutes should be taken into account; ignore all other time values.
//          *
//          * @type {Date | undefined}
//          */
//         selectedTime: undefined,
//
//         /**
//          * The name that will be associated with the booking
//          */
//         bookingName: '',
//
//         /**
//          * The email that will be used to create the booking
//          */
//         bookingEmail: '',
//
//         /**
//          * Whether the meeting is currently being booked
//          */
//         isBooking: false,
//
//         /**
//          * The current booking error (or empty for none)
//          */
//         bookingError: '',
//
//         /**
//          * Whether booking was successful
//          */
//         bookingSuccess: false,
//
//         /**
//          * Returns a {@link Date} object containing the current selected date and time.
//          * If either the date or time is not selected, `undefined` will be returned.
//          *
//          * @returns {Date | undefined} The selected date and time, or undefined if either are unselected.
//          */
//         getSelectedDateTime() {
//             if (this.selectedDate == null || this.selectedTime == null)
//                 return undefined;
//
//             const d = this.selectedDate
//             const t = this.selectedTime
//
//             return new Date(d.getFullYear(), d.getMonth(), d.getDate(), t.getHours(), t.getMinutes())
//         },
//
//         /**
//          * Fetches available times on the specified date.
//          * Only the date portion of {@link date} is used; the time portion is ignored.
//          *
//          * The returned times include both the date and time. The date portions will be the same as the specified date.
//          * @param {Date} date The date to fetch availabilities for
//          * @returns {Promise<Date[]>}
//          */
//         async fetchAvailableTimes(date) {
//             // TODO We'll actually fetch availabilities from the API later, but we'll generate it automatically for now
//
//             const startHour = 8
//             const endHour = 20
//             const minInterval = 15
//
//             const dateYear = date.getFullYear()
//             const dateMonth = date.getMonth()
//             const dateDate = date.getDate()
//
//             /** @type {Date[]} */
//             const res = []
//
//             for (let hour = startHour; hour < endHour; hour++) {
//                 const steps = Math.floor(60 / minInterval)
//
//                 for (let step = 0; step < steps && (hour * 60) + (minInterval * step) + eventTypeDurationMinutes < endHour * 60; step++) {
//                     res.push(new Date(dateYear, dateMonth, dateDate, hour, minInterval * step))
//                 }
//             }
//
//             return res
//         },
//
//         /**
//          * Selects a date.
//          * When this is called, the currently selected time will be cleared.
//          * @param {Date} date
//          * @returns {Promise<void>}
//          */
//         async selectDate(date) {
//             cal.set(date)
//             this.selectedDate = new Date(date.getFullYear(), date.getMonth(), date.getDate())
//
//             try {
//                 this.availableTimes = []
//                 this.selectedTime = undefined
//                 this.isLoadingAvailableTimes = true
//
//                 // TODO Remove waiting time once there's actual network activity to wait on
//                 await new Promise(res => setTimeout(res, 100))
//
//                 this.availableTimes = await this.fetchAvailableTimes(date)
//             } catch (err) {
//                 console.error('Failed to fetch available times:', err)
//                 alert('Failed to fetch available times')
//                 return
//             } finally {
//                 this.isLoadingAvailableTimes = false
//             }
//         },
//
//         /**
//          * Selects a time.
//          * Only hours and minutes are taken into account.
//          * @param {Date} time The time
//          * @returns {Promise<void>}
//          */
//         async selectTime(time) {
//             this.selectedTime = new Date(0, 0, 0, time.getHours(), time.getMinutes())
//         },
//
//         async bookMeeting() {
//             if (this.isBooking || this.bookingName.length < 1 || this.bookingEmail.length < 3)
//                 return
//
//             try {
//                 this.bookingError = ''
//                 this.isBooking = true
//
//                 const reqRes = await fetch('?action=book', {
//                     method: 'POST',
//                     credentials: 'include',
//                     headers: {
//                         'Accept': 'application/json',
//                         'Content-Type': 'application/json',
//                     },
//                     body: JSON.stringify({
//                         start_ts: this.getSelectedDateTime(),
//                         name: this.bookingName,
//                         email: this.bookingEmail,
//                     })
//                 })
//
//                 /** @type {Record<string, any>} */
//                 let res
//                 try {
//                     res = await reqRes.json()
//                 } catch (err) {
//                     console.error('Failed to fetch JSON response:', err)
//                     this.bookingError = 'Failed to book meeting because server returned an error'
//                     return
//                 }
//
//                 if (reqRes.status < 200 || reqRes.status > 299) {
//                     this.bookingError = res.message ?? `Unknown error (status ${reqRes.status})`
//                     return
//                 }
//
//                 // Everything went well
//                 this.bookingSuccess = true
//             } catch (err) {
//                 console.error('Error creating booking:', err)
//             } finally {
//                 this.isBooking = false
//             }
//         },
//
//         mounted() {
//             cal.onDateClick((event, date) => {
//                 this.selectDate(date)
//             })
//
//             this.selectDate(new Date())
//         },
//     }).mount('#event-booking-container')
// })()


var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
var days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
var timesAvailable = ["9:00am", "10:00am", "11:00am", "2:00pm", "3:00pm"];

var event = JSON.parse(sessionStorage.getItem("eventObj"));
console.log(event);

document.getElementById("event").textContent = event.name;
document.getElementById("scheduler").textContent = event.organizer;
document.getElementById("duration").textContent = event.duration + "min";
document.getElementById("description").textContent = event.description;


// Calendar
document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        height: 'auto',
        showNonCurrentDates: false,
        selectable: true,
        select: function(info) {
            var currentDay = new Date();
            var daySelected = info.start;
            if (daySelected >= currentDay) {

                var timeDiv = document.getElementById("available-times-div");

                while (timeDiv.firstChild) {
                    timeDiv.removeChild(timeDiv.lastChild);
                }

                //Heading - Date Selected
                var h4 = document.createElement("h4");
                var h4node = document.createTextNode(
                    days[daySelected.getDay()] + ", " +
                    months[daySelected.getMonth()] + " " +
                    daySelected.getDate());
                h4.appendChild(h4node);

                timeDiv.appendChild(h4);

                //Time Buttons
                for (var i = 0; i < timesAvailable.length; i++) {
                    var timeSlot = document.createElement("div");
                    timeSlot.classList.add("time-slot");

                    var timeBtn = document.createElement("button");

                    var btnNode = document.createTextNode(timesAvailable[i]);
                    timeBtn.classList.add("time-btn");

                    timeBtn.appendChild(btnNode);
                    timeSlot.appendChild(timeBtn);

                    timeDiv.appendChild(timeSlot);

                    // When time is selected
                    var last = null;
                    timeBtn.addEventListener("click", function() {
                        if (last != null) {
                            console.log(last);
                            last.parentNode.removeChild(last.parentNode.lastChild);
                        }
                        var confirmBtn = document.createElement("button");
                        var confirmTxt = document.createTextNode("Confirm");
                        confirmBtn.classList.add("confirm-btn");
                        confirmBtn.appendChild(confirmTxt);
                        this.parentNode.appendChild(confirmBtn);
                        event.time = this.textContent;
                        confirmBtn.addEventListener("click", function() {
                            event.date =
                                days[daySelected.getDay()] + ", " +
                                months[daySelected.getMonth()] + " " +
                                daySelected.getDate();
                            sessionStorage.setItem("eventObj", JSON.stringify(event));
                            console.log(event);
                            window.location.href = "register.html";
                        });
                        last = this;
                    });
                }

                var containerDiv = document.getElementsByClassName("container")[0];
                containerDiv.classList.add("time-div-active");

                document.getElementById("calendar-section").style.flex = "2";

                timeDiv.style.display = "initial";

            } else {alert("Sorry that date has already past. Please select another date.");}
        },
    });
    calendar.render();
});

