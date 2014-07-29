from django.http import HttpResponse
from django.template.context import Context
from django.template.loader import get_template

import json
import StringIO
from xhtml2pdf import pisa


#--------------------------------------------------------------------------------

HttpJSONResponse = lambda x : HttpResponse(
    json.dumps(x), content_type="application/json"
)


def make_pdf_response(context, template):

    context = Context(context)
    template = get_template(template)
    html = template.render(context)

    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
                                        dest=result,
                                        encoding='UTF-8')
    if not pdf.err:

        filename = 'badge.pdf'

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="'+filename+'"'
        response.write(result.getvalue())
    else:
        raise "andrebbe in eccezione"

    return response
