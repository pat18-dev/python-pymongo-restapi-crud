
from routes.utils.PaymentPDF import PaymentPDF
from models.Ticket import CATEGORIES, PRICES, DATE_FORMAT

def print_rx():
   loPdf = PaymentPDF("C:\\Users\\patrickfuentes\\Documents\\python-pymongo-restapi-crud\\file", "00000001")
   loPdf.setData({"name": "JUAN PAZ", "id": "00000001"})
   loPdf.setDatos([{'categoryid':'P'}, {'categoryid': 'O'}, {'categoryid': 'P'}])
   loPdf.mxprint(CATEGORIES, PRICES, DATE_FORMAT)
   
if __name__ == '__main__':
    print_rx()