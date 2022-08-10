# Magic RSVP

The goal of this tool is to scrape Disney's dining reservation API periodically to determine when new availability occurs. This was made for education purposes. It will query Disney's APIs to determine and compare restaurant availability to determine if restaurants have new availability notifying me (for now) if there are any changes.

## Overview

This core of this service is a python script wrapped in a docker container ran periodically on AWS lambda. It uses AWS S3 to store past queries and AWS SES to dispatch updates via email.

## Work In Progress

These are the current features which are under progress

- Creating a front end for this application and hosting a server to make requests.
- Supporting more rich filtering
  - Dates or times
  - Locations, costs
  - Specifying which restaurants in particalar to watch
- Reach: auto booking once available, this is on hold because it involves holding CC data and I don't mess with that (yet)

## Outstanding Issues

The cookie it uses was ripped off my browser and I am not sure if it will expire. Also the email provider can only email me, better notification support is needed

# Disney Dining API Notes

Below are some notes for key endpoints used to make this work

## Dining Data

> url: https://disneyland.disney.go.com/finder/api/v1/explorer-service/list-ancestor-entities/dlr/80008297;entityType=destination/{TARGET_DATE}/dining

This contains a lot of rich information about all dining locations on property. This returns the following and some extraneous data. Some fields that could be of interest but are not shown is enums for reasons why a place has no reservations, all times available and what their map uses for rendering.

```Python
{
    "locations": [...]
    "results": [...]
    "filters": {...}
}
```

### Locations

The Locations returns a list of regions in the park from the parks themselves to downtown disney and the resorts. Each location includes the following data:

```Python
{
    "id": "330339;entityType=theme-park",
    "title": "Disneyland Park",
    "urlFriendlyId": "disneyland",
    "locationType": "theme-park"
}
```

### Results

The Results data includes rich data for every kind of dining location. The fields I found most interesting are included. Other ones are not relevant for example CDN targets for content, latitude and longitude. Some fields of interest for future use such as supporting their filters on the site is the `facets` field not shown below which includes things like cuisine, discounts, cost estimates, etc.

```Python
{
"id": "19629820;entityType=restaurant",
"name": "Lamplight Lounge - Boardwalk Dining",
"parkIds": ["336894;entityType=theme-park"],
"schedule": {
    "schedules": [
        {
            "startTime": "11:30:00",
            "endTime": "17:00:00",
            "date": "2022-08-09",
            "timeZone": "PDT"
        }
    ]
    },
},
```

### Filters: Meal Periods

The meal periods dictionary mapping, this tells us the codes used for searching for blocks of time like `Dinner` or `Lunch`. This at time of writing looked like:

```Python
"mealPeriods": [
{
    "key": "80000712",
    "value": "Breakfast"
},
{
    "key": "80000713",
    "value": "Brunch"
},
{
    "key": "80000714",
    "value": "Dinner"
},
{
    "key": "80000717",
    "value": "Lunch"
}
],
```

## Dining Availability List

> url: https://disneyland.disney.go.com/finder/api/v1/explorer-service/dining-availability-list/{13019931-306C-4B87-AFAD-050364842981}/dlr/80008297;entityType=destination/2022-08-12/5/?mealPeriod=80000717

This is actually what we are here for. Notice that this url takes some parameters at the end, the date, the party size, then in this case which meal period to query availability for. This Endpoint returns a dictionary which under `availability` returns a list of all restaurants. Each restaurant is keyed by its id (use the endpoint above to convert back to a name) and includes the following if there are no spots:

```Python
"354450;entityType=restaurant": {
    "hasAvailability": false,
    "singleLocation": {
        "unavailableReason": "No times available."
    }
},
```

or the following if there is spots available:

```Python
"354450;entityType=restaurant": {
"hasAvailability": true,
"availabilitySearchDate": "2022-08-12",
"singleLocation": {
    "title": "Reserve a table at",
    "offers": [
        {
            "date": "2022-08-12",
            "time": "13:00:00",
            "label": "1:00 PM",
            "url": "/dining-reservation/setup-order/table-service/?offerId[]=https://availability.service.wdprapps.disney.com/availability-service/table-service-availability/d936ccba-653f-4775-9685-b6918f1cdffe/offers/753f5f58-5a6c-46cc-bc83-d7355a671a58",
            "productType": "DINING_TABLE_SERVICE"
        },
    ]
}
```

Note that this will blend in restaurants with eventsso you need to filter on whether or not the `singleLocation` keyword is in the data.
