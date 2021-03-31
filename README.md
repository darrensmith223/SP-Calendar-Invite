# Sending Calendar Invites with SparkPost

SparkPost supports a wide range of different message types, from marketing and bulk mailings, to transactional or trigger-based messages - even time sensitive messages such as those used for two factor authentication.  But how do you send a calendar invitation?  The trick is to send the invitation as an email message where the invitation is a specially formatted attachment, called an [iCalendar file](https://en.wikipedia.org/wiki/ICalendar).  

The following project aims to serve two purposes: 
1. A guide for how to successfully send a calendar invitation through SparkPost using the [Transmissions API](https://developers.sparkpost.com/api/transmissions/).
2. A Python application that will accept the invitation details and recipient information, construct the calendar event, and send the invite to the attendee.

## Steps
The steps for sending a calendar invite through SparkPost are:
1. Create calendar invite
2. Base64 encode the invite
3. Include the encoded invite as an attachment in the Transmissions API call
4. Send the transmission

### Creating a Calendar Invitation
To create a calendar invitation, you will need to create an iCalendar file.  For this example, the vCalendar format is used, of which an example can be found in the Samples folder.  The iCalendar file is where we define the attributes of the meeting, such as the start and end time. 

In the Python application, the function `genCalInvite` is used to construct an invitation from the sample using the event and recipient details that are passed into the script.  The function then outputs the constructed invitation.

It is important to ensure that a unique UID is assigned for the event.  In the Python application, a unique UID is generated for the calendar event by leveraging the `uuid` package in Python, which is then included in the iCalendar file.

```Python
import uuid

uuidVal = str(uuid.uuid4())  # Create unique ID for calendar event
```


### Encoding the Invitation
The next step is to base64 encode the calendar invitation.  In this project, the `base64` package in Python is used to encode the invitation object.

:Relevant Code Here
```Python
import base64

calInviteBytes = calInvite.encode('ascii')  # Convert calendar invite into bytes
base64Bytes = base64.b64encode(calInviteBytes)  # Base64 encode the invite bytes
calObj = base64Bytes.decode('ascii')  # Convert encode back into ASCII, store as calendar object
```


### Sending the Transmission
We are now ready to send the invite through SparkPost.  To do this, we will use the Transmissions API and include the base64 encoded invitation as an attachment.  An example of the Transmissions API payload can be found in the Samples folder.


### Message Received!
And now we’re done!  The message will be received by each of the recipients included in the Transmissions API with the calendar invitation that we sent.


## Using the InviteEmailer Python application

To use the Python application, you can clone this repo and call the `sendInvite` function from `InviteEmailer.py`.  The application accepts the following parameters:

* apiKey (string):  SparkPost API Key
* recipient:  A dictionary of recipient / attendee details
  * attendeeName (string):  The name of the recipient
  * attendeeEmail (string):  The eamil address of the recipient
* event:  A ditionary of event details
  * eventTitle (string):  The title of the event
  * eventDescription (string):  The description of the event
  * eventDate (datetime.date):  The date of the event
  * eventStartTime (datetime.time):  The start time of the event (in UTC)
  * eventEndTime (datetime.time):  The end time of the event (in UTC)
  * organizerName (string):  The name of the event organizer
  * organizerEmail (string):  The email address of the event organizer
  * msgFromAddress (string):  The from address that should be used when sending the message from SparkPost

An example can be found below (make sure to update to use your API key):

```Python
import InviteEmailer
import datetime

apiKey = "SPARKPOST_API_KEY"

recipient = {
    "attendeeName": "Jane Doe",
    "attendeeEmail": "jane.doe@example.com"
}

event = {
    "eventTitle": "Awesome Sales Demo",
    "eventDescription": "This is a meeting with our Sales team.",
    "eventDate": datetime.date(2021, 4, 15),
    "eventStartTime": datetime.time(22, 00, 00),  # Time in UTC
    "eventEndTime": datetime.time(23, 00, 00),  # Time in UTC
    "organizerName": "Sales Team",
    "organizerEmail": "sales@company.com",
    "msgFromAddress": "sales@sparkpost.sendingdomain.com"
}

uuid = InviteEmailer.sendInvite(
    apiKey=apiKey,
    recipient=recipient,
    event=event
)
```

