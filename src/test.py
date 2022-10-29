
import os
from routes.utils.PaymentPDF import PaymentPDF
from models.Ticket import CATEGORIES, PRICES, DATE_FORMAT

def print_rx():
   PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
   PATH_FILE = os.path.join(PROJECT_ROOT, "src", "file")
   loPdf = PaymentPDF(PATH_FILE, "00000001")
   loPdf.setData({"name": "JUAN PAZ", "id": "00000001"})
   loPdf.setDatos([{'categoryid':'P'}, {'categoryid': 'O'}, {'categoryid': 'P'}])
   loPdf.mxprint(CATEGORIES, PRICES, DATE_FORMAT)
   
if __name__ == '__main__':
    print_rx()