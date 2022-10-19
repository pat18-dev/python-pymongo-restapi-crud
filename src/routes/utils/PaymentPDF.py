#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from pathlib import Path
from .decorators import exception_handler

from .PYFPDF import PYFPDF


class PaymentPDF:
    def __init__(self, p_cPath, p_cCodigo):
        self.lcPath = p_cPath
        Path(p_cPath).mkdir(parents=True, exist_ok=True)
        self.paData = None
        self.paDatos = None
        self.error = None
        self.l_w = 0
        self.l_h = 0.4

    def setData(self, data):
        self.paData = data

    def setDatos(self, datos):
        self.paDatos = datos

    def setWidth(self, w):
        self.l_w = w

    def setHeigth(self, h):
        self.l_h = h

    @exception_handler(False)
    def mxprint(self, CATEGORIES, PRICES, DATE_FORMAT):
        if self.paData is None:
            raise ValueError("DATA NO DEFINIDA")
        loPdf = PYFPDF()
        loPdf.alias_nb_pages()
        loPdf.add_page()
        loPdf.setHeader("BOLETA")
        loPdf.set_margins(1, 1.6, 1)
        self.setWidth(loPdf._width)
        w1 = self.l_w * 0.1
        w3 = self.l_w * 0.3
        w4 = self.l_w * 0.4
        w6 = self.l_w * 0.6
        loPdf.set_border(1)
        loPdf.row(["COMPROBANTE:", self.paData["id"]], [w1, w4])
        loPdf.row(["FECHA:", datetime.now().strftime(DATE_FORMAT)], [w1, w4])
        loPdf.row(["NOMBRE", self.paData["name"]], [w1, w4])
        if self.paDatos is not None:
            cat = item["category"]
            for i, item in enumerate(self.paDatos):
                loPdf.row([i, CATEGORIES[cat], PRICES[cat]], [w1, w6, w3])
            loPdf.set_border(0)
