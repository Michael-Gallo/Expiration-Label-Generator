import csv
import sys
from datetime import datetime
# fba_listing_and_shipment.py - Take a template file and fill out an FBA Uploader and an FBA-shipment template based on it 
# takes in an All Listings report as the first argument

today = datetime.today().strftime("%m-%d-%Y")
def main():
    in_file_name = "newproductinput.csv"
    with open(in_file_name, newline = '') as infile:
        make_uploaders(infile)




def make_uploaders(infile):
    global today
    listing_out_file_name = "FBA-upload_template-"+today+".txt"
    shipment_out_file_name = "FBA-Shipment-Template-"+today+".txt"
    make_fba_uploader(infile,listing_out_file_name)
    make_shipment_uploader(infile,shipment_out_file_name)



def make_fba_uploader(infile,outfile_name):
    infile.seek(0)
    listing_static_fields = {
    "product-id-type":"1",
    "item-condition":"11",
    "add-delete":"a",
    "batteries_required":"no",
    "supplier_declared_dg_hz_regulation1":"not_applicable",
    "fulfillment_center_id":"AMAZON_NA",
    "price":"1921"
    }

    with open(outfile_name,'w',newline ='') as outfile:
        listing_report = sys.argv[1]
        created_skus = pull_current_skus(listing_report)
        reader = csv.DictReader(infile, delimiter = ',')
        listing_writer = csv.DictWriter(outfile,delimiter ='\t',fieldnames = list(listing_static_fields.keys())+["product-id","sku"])
        listing_writer.writeheader()
        for row in reader:
            data = get_fields(row)
            if data["SKU"] in created_skus:
                continue
            outrow = listing_static_fields
            outrow["product-id"] = data["ASIN"]
            outrow["sku"] = data["SKU"]
            try:
                outrow["price"] = data['price']
            except:
                pass
            listing_writer.writerow(outrow)

def make_shipment_uploader(infile,outfile_name):
    infile.seek(0)
    with open (outfile_name, 'w', newline='') as outfile:
        writer = csv.writer(outfile,delimiter = '\t')
        write_shipping_header(outfile,writer)
        reader = csv.DictReader(infile,delimiter = ',')
        for row in reader:
            data = get_fields(row)
            if data["quant"] is "":
                writer.writerow([data["SKU"],"1"])

            else:
                writer.writerow([data["SKU"],data["quant"]])

def write_shipping_header(outfile,writer):
    global today
    template_fields = ["PlanName","ShipToCountry","AddressName","AddressFieldOne","AddressFieldTwo","AddressCity","AddressCountryCode","AddressStateOrRegion","AddressPostalCode","AddressDistrict"]
    planName ="Test-Shipment-"+today
    template_values = [planName,"US","Michael Gallo","21 Vernon Street","","Parlin","US","NJ","08859",""]
    out_file_name = "shipment_creator "+today+'.txt'
    for field,value in zip(template_fields,template_values):
        writer.writerow([field,value])
    writer.writerow("")
    writer.writerow(["MerchantSKU","Quantity"])

def get_fields(row):
    quantity = row["Quantity"]
    productid = row["ASIN"]
    sku  = row["SKU"]
    if row["price"]:
        price = row["price"]
        return {"quant":quantity,"ASIN":productid,"SKU":sku,"price":price}
    else:
        return {"quant":quantity,"ASIN":productid,"SKU":sku}


#takes in a listing report from amazon and appends the Amazon fulfilled skus to a list
def pull_current_skus(tab_file):
    sku_list = []
    with open(tab_file,newline = '',encoding = "utf-8-sig",errors = 'ignore') as f:
        for row in csv.DictReader (f, delimiter = '\t'):
            if row['fulfillment-channel'] == "AMAZON_NA":
                sku_list.append(row['seller-sku'])     
    return(sku_list)

if __name__ == '__main__':
    main()

