# FEMA Incident Map: Incidents per State

More detail to come. In the meantime, please browse through the code and see it in action! 

You can also explore the API by sending queries to '/api' specifying an incident 'kind' along with 'start' and 'end' dates in the form of 'YYYY-MM-DD'. If the 'kind' requested is not a recognized FEMA incident type (ie: not an option in the drop-down menu), the result will not be filtered by incident (ie: it will contain data for all incidents). Similarly, if the 'start' and/or 'end' dates are not dates (or are outside the range of the data), the result will not be filtered by either or both of the dates.
For example:
  HTTP request '<server>/api?kind=Tornado&start=2017-01-01&end=2017-01-31' will return JSON containing 27 incidents;
  HTTP request '<server>/api?kind=ksdjfhs&start=2017-01-01&end=2017-01-31' will return JSON containing 36 incidents; and
  HTTP requests '<server>/api?kind=Tornado&start=2017-01-01' and '<server>/api?kind=dfgdg&start=2017-01-01&end=sdfgs' will return the same 1847 events.
