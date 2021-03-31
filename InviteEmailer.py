from sparkpost import SparkPost
import uuid
import base64
import datetime
from icalendar import Calendar, Event


def genCalInvite(startDate, endDate, organizerName, organizerEmail, attendeeName, attendeeEmail
                 , createdDate, uuidVal, eventTitle, eventDescription):
    cal = Calendar()
    cal.add("VERSION", "2.0")
    cal.add("CALSCALE", "GREGORIAN")
    cal.add("METHOD", "REQUEST")

    event = Event()
    event['dtstart'] = startDate
    event['dtend'] = endDate
    event.add('organizer', 'MAILTO:' + organizerEmail, parameters={"CN": organizerName})
    event['uid'] = uuidVal
    event.add('attendee', 'MAILTO:' + attendeeEmail,
              parameters={
                  "CUTYPE": "INDIVIDUAL",
                  "ROLE": "REQ-PARTICIPANT",
                  "PARTSTAT": "NEEDS-ACTION",
                  "RSVP": "TRUE",
                  "CN": attendeeName,
                  "X-NUM-GUESTS": "0"
               })
    event.add('attendee', 'MAILTO:' + organizerEmail,
              parameters={
                  "CUTYPE": "INDIVIDUAL",
                  "ROLE": "REQ-PARTICIPANT",
                  "PARTSTAT": "NEEDS-ACTION",
                  "RSVP": "TRUE",
                  "CN": organizerName,
                  "X-NUM-GUESTS": "0"
              })
    event.add('created', createdDate)
    event.add('description', eventDescription)
    event.add('last-modified', createdDate)
    event.add('sequence', "0")
    event.add('status', "CONFIRMED")
    event.add("summary", eventTitle)
    event.add("transp", "OPAQUE")
    event.add("X-APPLE-TRAVEL-ADVISORY-BEHAVIOR", "AUTOMATIC")

    cal.add_component(event)

    return cal.to_ical()


def sendMessage(apiKey, eventTitle, eventDescription, attendeeName, attendeeEmail, calendarObj, msgFromAddress):
    sp = SparkPost(apiKey)

    sp.transmissions.send(
        recipients=[{'address': {'name': attendeeName, 'email': attendeeEmail}}],
        text=eventDescription,
        html="<html><body><p>" + eventDescription + "</p></body></html>",
        from_email=msgFromAddress,
        subject=eventTitle,
        attachments=[{
                "name": "invite.ics",
                "type": "application/ics; name=\"invite.ics\"",
                "data": calendarObj
            }]
    )


def sendInvite(apiKey, recipient, event):
    """
    :param apiKey: <String> SparkPost API Key
    :param recipient:  <Dict> A dictionary of recipient / attendee details containing:
        recipient = {
            "attendeeName":  <String> The name of the recipient
            "attendeeEmail":  <String> The eamil address of the recipient
        }
    :param event:  <Dict> A ditionary of event details containing:
        event = {
            "eventTitle": <String>  The title of the event
            "eventDescription": <String>  The description of the event
            "eventDate": <datetime.date>  The date of the event
            "eventStartTime": <datetime.time>  The start time of the event (in UTC)
            "eventEndTime": <datetime.time>  The end time of the event (in UTC)
            "organizerName": <String>  The name of the event organizer
            "organizerEmail": <String>  The email address of the event organizer
            "msgFromAddress": <String>  The from address that should be used when sending the message from SparkPost
        }
    :return:
    """
    # Unpack Variables
    attendeeName = recipient["attendeeName"]
    attendeeEmail = recipient["attendeeEmail"]
    eventTitle = event["eventTitle"]
    eventDescription = event["eventDescription"]
    eventDate = event["eventDate"]
    eventStartTime = event["eventStartTime"]
    eventEndTime = event["eventEndTime"]
    organizerName = event["organizerName"]
    organizerEmail = event["organizerEmail"]
    msgFromAddress = event["msgFromAddress"]
    uuidVal = str(uuid.uuid4())  # Create unique ID for calendar event

    # Construct Dates
    startDate = eventDate.strftime("%Y%m%dT") + eventStartTime.strftime("%H%M%SZ")
    endDate = eventDate.strftime("%Y%m%dT") + eventEndTime.strftime("%H%M%SZ")
    currentDate = datetime.datetime.now()

    # Generate Calendar Invitation
    calInvite = genCalInvite(startDate, endDate, organizerName, organizerEmail, attendeeName, attendeeEmail, currentDate
                             , uuidVal, eventTitle, eventDescription)

    # Base64 encode calendar invite
    base64Bytes = base64.b64encode(calInvite)  # Base64 encode the invite bytes
    calObj = base64Bytes.decode('ascii')  # Convert encode back into ASCII, store as calendar object

    # Send Calendar Invite
    sendMessage(apiKey, eventTitle, eventDescription, attendeeName, attendeeEmail, calObj, msgFromAddress)

    return uuidVal
