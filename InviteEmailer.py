from sparkpost import SparkPost
import uuid
import base64
import datetime


def genCalInvite(startDate, endDate, organizerName, organizerEmail, attendeeName, attendeeEmail
                 , createdDate, uuidVal, eventTitle, eventDescription):
    calInvite = "" \
                "BEGIN:VCALENDAR" + "\n" \
                "VERSION:2.0" + "\n" \
                "CALSCALE:GREGORIAN" + "\n" \
                "METHOD:REQUEST" + "\n" \
                "BEGIN:VEVENT" + "\n" \
                "DTSTART:" + startDate + "\n" \
                "DTEND:" + endDate + "\n" \
                "DTSTAMP:20190109T212441Z" + "\n" \
                "ORGANIZER;CN=" + organizerName + ":mailto:" + organizerEmail + "\n" \
                "UID:" + uuidVal + "\n" \
                "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE" + "\n" \
                ";CN=" + attendeeName + ";X-NUM-GUESTS=0:mailto:" + attendeeEmail + "\n" \
                "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE" + "\n" \
                ";CN=" + organizerName + ";X-NUM-GUESTS=0:mailto:" + organizerEmail + "\n" \
                "CREATED:" + createdDate + "\n" \
                "DESCRIPTION:" + eventDescription + "\n" \
                "LAST-MODIFIED:" + createdDate + "\n" \
                "LOCATION:" + "\n" \
                "SEQUENCE:0" + "\n" \
                "STATUS:CONFIRMED" + "\n" \
                "SUMMARY:" + eventTitle + "\n" \
                "TRANSP:OPAQUE" + "\n" \
                "X-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC" + "\n" \
                "END:VEVENT" + "\n" \
                "END:VCALENDAR"
    return calInvite


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
    startDate = '{:02d}{:02d}{:02d}T{:02d}{:02d}{:02d}Z'.format(eventDate.year, eventDate.month, eventDate.day,
                                                          eventStartTime.hour, eventStartTime.minute, eventStartTime.second)
    endDate = '{:02d}{:02d}{:02d}T{:02d}{:02d}{:02d}Z'.format(eventDate.year, eventDate.month, eventDate.day,
                                                          eventEndTime.hour, eventEndTime.minute, eventEndTime.second)
    currentDate = datetime.datetime.now()
    createdDate = '{:02d}{:02d}{:02d}T{:02d}{:02d}{:02d}Z'.format(currentDate.year, currentDate.month, currentDate.day,
                                                          currentDate.hour, currentDate.minute, currentDate.second)

    # Generate Calendar Invitation
    calInvite = genCalInvite(startDate, endDate, organizerName, organizerEmail, attendeeName, attendeeEmail, createdDate
                             , uuidVal, eventTitle, eventDescription)

    # Base64 encode calendar invite
    calInviteBytes = calInvite.encode('ascii')  # Convert calendar invite into bytes
    base64Bytes = base64.b64encode(calInviteBytes)  # Base64 encode the invite bytes
    calObj = base64Bytes.decode('ascii')  # Convert encode back into ASCII, store as calendar object

    # Send Calendar Invite
    sendMessage(apiKey, eventTitle, eventDescription, attendeeName, attendeeEmail, calObj, msgFromAddress)

    return uuidVal
