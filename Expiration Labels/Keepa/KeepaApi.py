import keepa
import reffeedict

accesskey = 'INSERT KEY HERE'
api = keepa.Keepa(accesskey)


def pullproduct(prodid):
	global api
	if prodid.startswith('B'):
		product = api.query(prodid,stats = 180,offers =20)
	else:
		product = api.query(prodid,stats = 180,offers = 20,product_code_is_asin=False)
	return product

def getfbafee(product):
	try:
		return(product[0]['fbaFees']['pickAndPackFee']/100)
	except: return(0)

def getcurrentnewprice(product):
	return product[0]['current'][1]

def get90daybsr(product):
	return(product[0]['stats']['avg90'][3])

def get90daynewprice(product):
	return(product[0]['stats']['avg90'][1])

def get180daybsr(product):
	return(product[0]['stats']['avg180'][3])

def getcurrentbsr(product):
	ranklist = product[0]['csv'][3]
	currentbsr = ranklist[len(ranklist)-1]
	return currentbsr

def getcurrentbuybox(product):
	return product[0]['stats']['current']#[10]/100

def get90daybuybox(product):
	return product[0]['stats']['avg90'][7]/100

def gettopcategory(product):
	category = product[0]['categoryTree'][0]['name']
	return category

def getref(product):
	category  = gettopcategory(product)
	refpercent = reffeedict.reffees[category][0]/100
	percentfee = refpercent * getcurrentbuybox(product)
	flatfee = reffeedict.reffees[category][1]
	if percentfee > flatfee:
		return percentfee
	else:
		return flatfee
