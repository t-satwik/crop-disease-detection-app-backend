fp_rain=open('./rainfall-AllStates.csv')
lines=fp_rain.readlines()
temp_dr_dict={}
for line in lines[2:]:
    line_data=line.strip().split(',')
    if line_data[1] not in temp_dr_dict.keys():
        if line_data[-1]!="N.A.":
            temp_dr_dict[line_data[1]]=[float(line_data[-1])]
    else:
        if line_data[-1]!="N.A.":
            temp_dr_dict[line_data[1]].append(float(line_data[-1]))

district_rainfall={}
for district in temp_dr_dict.keys():
    district_rainfall[district]=sum(temp_dr_dict[district])/len(temp_dr_dict[district])
# print(district_rainfall)

fp_loc=open('./location-AllDistricts.csv')
lines=fp_loc.readlines()
district_location={}
for line in lines[1:]:
    # print(line)
    line_data=line.strip().split(',')
    if line_data[5] in district_rainfall.keys():
        district_location[line_data[5]]=(float(line_data[-2]), float(line_data[-1]))

data=[]
for key in district_location.keys():
    data.append([key, district_location[key], district_rainfall[key]])
    # print("{},{},{},{}".format(key, district_location[key][0], district_location[key][1], district_rainfall[key]))
print(data)
