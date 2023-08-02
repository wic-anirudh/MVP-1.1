master_data = []
f_o_list = [['A', 'Agilent Technologies Inc', 'INSTRUMENTS FOR MEAS & TESTING OF ELECTRICITY & ELEC SIGNALS', '30.5']]
f_m_bs_list = [['A', '5305000000', '3600000036000000273300000036000000None2769000000']]
f_m_is_list = [['A', '-84000000', '1254000000']]

total_no_stocks = len(f_o_list)

for i in f_o_list:
    master_data.append(i)

for i in range(len(f_o_list)):
    if(f_m_bs_list[i][0]==master_data[i][0]):
        for j in range(len(f_m_bs_list[i])):
            if(j!=0):
                master_data[i].append(f_m_bs_list[i][j])
    if(f_m_is_list[i][0]==master_data[i][0]):
        for j in range(len(f_m_is_list[i])):
            if(j!=0):
                master_data[i].append(f_m_is_list[i][j])

print(master_data)
