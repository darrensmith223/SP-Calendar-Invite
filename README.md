#Sending Calendar Invites with SparkPost



SparkPost supports a wide range of different message types, from marketing and bulk mailings, to transactional or trigger-based messages - even time sensitive messages such as those used for two factor authentication.  But how do you send a calendar invitation?   The trick is to send an email message with the invitation as a specially formatted attachment, called an iCalendar file, and this can be easily accomplished by using SparkPost.
The following document is a guide for how to send a calendar invite through SparkPost using the Transmissions API. 

##Steps
The steps for sending a calendar invite through SparkPost are:
Create calendar invite
Base64 encode the invite
Include the encoded invite as an attachment in the Transmissions API call
Send the transmission

###Creating a Calendar Invitation
To create a calendar invitation, you will need to create an iCalendar file.  For this example, we are using the vCalendar format, which can be found below:
```BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:REQUEST
BEGIN:VEVENT
DTSTART:20201119T220000Z
DTEND:20201119T230000Z
DTSTAMP:20190109T212441Z
ORGANIZER;CN=Jane Doe:mailto:Jane@example.com
UID:204A3CA6-8CC5-432E-9778-3418CA467AB3
ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE
 ;CN=John Doe;X-NUM-GUESTS=0:mailto:John@example.com
ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=
 TRUE;CN=Jane Doe;X-NUM-GUESTS=0:mailto:Jane@example.com
CREATED:20201119T212402Z
DESCRIPTION:Your event content
LAST-MODIFIED:20201119T212402Z
LOCATION:
SEQUENCE:0
STATUS:CONFIRMED
SUMMARY:Test
TRANSP:OPAQUE
X-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC
END:VEVENT
END:VCALENDAR
```

###Encoding the Invitation
The next step is to base64 encode the calendar invitation.  For this example, I used https://www.base64encode.net/ to encode and received the following output:
```QkVHSU46VkNBTEVOREFSDQpWRVJTSU9OOjIuMA0KQ0FMU0NBTEU6R1JFR09SSUFODQpNRVRIT0Q6UkVRVUVTVA0KQkVHSU46VkVWRU5UDQpEVFNUQVJUOjIwMjAxMTE5VDIyMDAwMFoNCkRURU5EOjIwMjAxMTE5VDIzMDAwMFoNCkRUU1RBTVA6MjAxOTAxMDlUMjEyNDQxWg0KT1JHQU5JWkVSO0NOPUphbmUgRG9lOm1haWx0bzpKYW5lQGV4YW1wbGUuY29tDQpVSUQ6MjA0QTNDQTYtOENDNS00MzJFLTk3NzgtMzQxOENBNDY3QUIzDQpBVFRFTkRFRTtDVVRZUEU9SU5ESVZJRFVBTDtST0xFPVJFUS1QQVJUSUNJUEFOVDtQQVJUU1RBVD1BQ0NFUFRFRDtSU1ZQPVRSVUUNCiA7Q049Sm9obiBEb2U7WC1OVU0tR1VFU1RTPTA6bWFpbHRvOkpvaG5AZXhhbXBsZS5jb20NCkFUVEVOREVFO0NVVFlQRT1JTkRJVklEVUFMO1JPTEU9UkVRLVBBUlRJQ0lQQU5UO1BBUlRTVEFUPU5FRURTLUFDVElPTjtSU1ZQPQ0KIFRSVUU7Q049SmFuZSBEb2U7WC1OVU0tR1VFU1RTPTA6bWFpbHRvOkphbmVAZXhhbXBsZS5jb20NCkNSRUFURUQ6MjAyMDExMTlUMjEyNDAyWg0KREVTQ1JJUFRJT046WW91ciBldmVudCBjb250ZW50DQpMQVNULU1PRElGSUVEOjIwMjAxMTE5VDIxMjQwMloNCkxPQ0FUSU9OOg0KU0VRVUVOQ0U6MA0KU1RBVFVTOkNPTkZJUk1FRA0KU1VNTUFSWTpUZXN0DQpUUkFOU1A6T1BBUVVFDQpYLUFQUExFLVRSQVZFTC1BRFZJU09SWS1CRUhBVklPUjpBVVRPTUFUSUMNCkVORDpWRVZFTlQNCkVORDpWQ0FMRU5EQVI=
```

###Sending the Transmission
We are now ready to send the invite through SparkPost.  To do this, we will use the Transmissions API and include the base64 encoded invitation as an attachment.  An example transmission can be found below: 
```{
    "options": {
        "open_tracking": true,
        "click_tracking": true
    },
    "campaign_id": "test",
    "recipients": [
        {
            "address": {
                "email": "recipient@example.com",
                "name": "test recipient"
            }
        }
    ],
    "content": {
        "from": {
            "email": "organizer@example.com"
        },
        "subject": "Testing Invite",
        "text": "Sample Calendar Invite",
        "html": "<html><p>Here is a sample calendar invite</p></html>",
        "attachments": [
            {
                "name": "invite.ics",
                "type": "application/ics; name=\"invite.ics\"",
                "data": "QkVHSU46VkNBTEVOREFSDQpWRVJTSU9OOjIuMA0KQ0FMU0NBTEU6R1JFR09SSUFODQpNRVRIT0Q6UkVRVUVTVA0KQkVHSU46VkVWRU5UDQpEVFNUQVJUOjIwMjAxMTE5VDIyMDAwMFoNCkRURU5EOjIwMjAxMTE5VDIzMDAwMFoNCkRUU1RBTVA6MjAxOTAxMDlUMjEyNDQxWg0KT1JHQU5JWkVSO0NOPUphbmUgRG9lOm1haWx0bzpKYW5lQGV4YW1wbGUuY29tDQpVSUQ6MjA0QTNDQTYtOENDNS00MzJFLTk3NzgtMzQxOENBNDY3QUIzDQpBVFRFTkRFRTtDVVRZUEU9SU5ESVZJRFVBTDtST0xFPVJFUS1QQVJUSUNJUEFOVDtQQVJUU1RBVD1BQ0NFUFRFRDtSU1ZQPVRSVUUNCiA7Q049Sm9obiBEb2U7WC1OVU0tR1VFU1RTPTA6bWFpbHRvOkpvaG5AZXhhbXBsZS5jb20NCkFUVEVOREVFO0NVVFlQRT1JTkRJVklEVUFMO1JPTEU9UkVRLVBBUlRJQ0lQQU5UO1BBUlRTVEFUPU5FRURTLUFDVElPTjtSU1ZQPQ0KIFRSVUU7Q049SmFuZSBEb2U7WC1OVU0tR1VFU1RTPTA6bWFpbHRvOkphbmVAZXhhbXBsZS5jb20NCkNSRUFURUQ6MjAyMDExMTlUMjEyNDAyWg0KREVTQ1JJUFRJT046WW91ciBldmVudCBjb250ZW50DQpMQVNULU1PRElGSUVEOjIwMjAxMTE5VDIxMjQwMloNCkxPQ0FUSU9OOg0KU0VRVUVOQ0U6MA0KU1RBVFVTOkNPTkZJUk1FRA0KU1VNTUFSWTpUZXN0DQpUUkFOU1A6T1BBUVVFDQpYLUFQUExFLVRSQVZFTC1BRFZJU09SWS1CRUhBVklPUjpBVVRPTUFUSUMNCkVORDpWRVZFTlQNCkVORDpWQ0FMRU5EQVI="
            }
        ]
    }
}
```

###Message Received!
And now we’re done!  The message will be received by each of the recipients included in the Transmissions API with the calendar invitation that we sent.

