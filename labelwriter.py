import labels
from reportlab.graphics import shapes
#Label Printing Functionality
def createAvery5160Spec():

    f = 25.4 # conversion factor from inch to mm

    # Compulsory arguments.
    sheet_width  =  8.5 * f
    sheet_height = 11.0 * f
    columns =  3
    rows    = 10
    label_width  = 2.63 * f
    label_height = 1.00 * f
    
    # Optional arguments; missing ones will be computed later.
    left_margin   = 0.19 * f
    column_gap    = 0.12 * f
    right_margin  = 0
    top_margin    = 0.50 * f
    row_gap       = 0
    bottom_margin = 0
    
    # Optional arguments with default values.
    left_padding   = 1
    right_padding  = 1
    top_padding    = 1
    bottom_padding = 1
    corner_radius  = 2
    padding_radius = 0
    specs = labels.Specification(
        sheet_width, sheet_height,
        columns, rows,
        label_width, label_height,

        left_margin    = left_margin    ,
        column_gap     = column_gap     ,
        top_margin     = top_margin     ,
        row_gap        = row_gap        ,
        left_padding   = left_padding   ,
        right_padding  = right_padding  ,
        top_padding    = top_padding    ,
        bottom_padding = bottom_padding ,
        corner_radius  = corner_radius  ,
        padding_radius = padding_radius 
    )
    return specs

def write_date(label,width,height,date):
    #Write the expirationString, centered and near the top
    expirationString="Best By:"
    title= shapes.String(width/2,height-30,expirationString,textAnchor="middle")
    title.fontName = "Helvetica"
    title.fontSize= 30
    label.add(title)
    #write the dateString
    labelDate= shapes.String(width/2,2,date,fontName="Helvetica",fontSize=30,textAnchor="middle")
    label.add(labelDate)

def save_from_tuples(expiration_tuples,name="labels.pdf"): #save date/quant tuples to a file
    specs =createAvery5160Spec()
    sheet = labels.Sheet(specs, write_date, border=False)
    for date,quant in expiration_tuples:
        dateString=date.strftime('%m/%d/%Y')
        for label_quant in range(quant):
            sheet.add_label(dateString)
    sheet.save(name)