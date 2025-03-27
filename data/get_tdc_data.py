from tdc.single_pred import HTS
data = HTS(name = 'SARSCoV2_3CLPro_Diamond')
df = data.get_data()
splits = data.get_split()