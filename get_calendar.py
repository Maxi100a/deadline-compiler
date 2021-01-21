from ics import Calendar
import requests

# Get ICS calendar and create Calendar object from it
url = "https://canvas.jmu.edu/feeds/calendars/user_4xRFx9LoErxmg0AFYuOW5XdSUjDkXIBrG2h6uxJf.ics"
c = Calendar(requests.get(url).text)

# Empty calendar dictionary
eventsCalendar = {}
for event in c.events:
    eventsCalendar[event.name] = event.begin.date()

sortedCalendar = sorted(eventsCalendar.items(), key=lambda item: item[1])