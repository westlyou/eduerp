# -*- coding: utf-8 -*-
###############################################################################
#
###############################################################################

import base64
from reportlab.graphics.barcode import createBarcodeDrawing
import time
from openerp import models
from openerp.exceptions import ValidationError
from openerp.report import report_sxw


class BookBarcodeParser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        self.ids_to_print = []
        self.ids_to_print = context.get('active_ids', False)
        self.model_name = context.get('active_model', False)
        super(BookBarcodeParser, self).__init__(
            cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_books': self.get_books,
            'get_barcode': self.get_barcode,
        })

    def get_books(self):
        book_list = []
        for book_id in self.ids_to_print:
            book_obj = self.pool.get(self.model_name).browse(
                self.cr, self.uid, book_id)
            book_data = {
                'name': book_obj.name,
                'unit': book_obj.unit_ids,
                'isbn': book_obj.isbn
            }
            book_list.append(book_data)
        return book_list

    def get_barcode(self, type, value, width=350, height=60, hr=1):
        """ genrating image for barcode """
        options = {}
        if width:
            options['width'] = width
        if height:
            options['height'] = height
        if hr:
            options['humanReadable'] = hr
        try:
            ret_val = createBarcodeDrawing(
                type, value=str(value), **options)
        except Exception, e:
            raise ValidationError('Error in barcode generation', e)
        image_data = ret_val.asString('png')
        return base64.encodestring(image_data)


class ReportBookBarcode(models.AbstractModel):
    _name = 'report.eduerp_library.report_book_barcode'
    _inherit = 'report.abstract_report'
    _template = 'eduerp_library.report_book_barcode'
    _wrapped_report_class = BookBarcodeParser


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
