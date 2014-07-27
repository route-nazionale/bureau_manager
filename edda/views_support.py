from django.http import HttpResponse
import json

#--------------------------------------------------------------------------------

HttpJSONResponse = lambda x : HttpResponse(
    json.dumps(x), content_type="application/json"
)


