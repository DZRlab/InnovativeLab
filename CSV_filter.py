import pandas as pd
import io
with open("D:\\test\InnovativeLab\Contracts.csv", 'rb') as f:
    bom = f.read(2)

if bom == b'\xff\xfe':
    print('File is encoded as UTF-16-LE')
elif bom == b'\xfe\xff':
    print('File is encoded as UTF-16-BE')
else:
    print('File does not have a BOM, so the version of UTF-16 is unknown')

with open("D:\\test\InnovativeLab\Contracts.csv", 'rb') as f:
    data = f.read()
    decoded_data = data.decode('utf-16-le', errors='ignore')

df = pd.read_csv(io.StringIO(decoded_data), sep=';')
 
# REmove cols you don't need (give column names)
cols_for_removal = ['CIAddress', 'CICity', 'CICPostalCode','ShipmentLocationDescription','IsSectorAgreement','CentralInstitution',
                    'ZPJN','AgreementStartDate','AgreementEndDate','HighestOfferValue','LowestOfferValue','VendorAddress','VendorCity','VendorState']
df = df.drop(columns=cols_for_removal)
 
# Save the modified CSV-file
df.to_csv("D:\\test\InnovativeLab\Contracts1.csv", index=False, encoding='utf-16', sep=';')