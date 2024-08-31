import xlrd
import xlwt

from fuzzywuzzy import process

# Only contain name
originExcelFilePath = "originPoi.xlsx"

# Contain detail message
referenceExcelFilePath = "referencePoi.xls"

# Where result saved
dataFile = "primer.xls"

# Nums of fuzzy matching result
choice_limit = 5


def read_poi_text(file_name, index_of_origin_data_sheet_of_file, col_of_name_of_sheet):
    _wb = xlrd.open_workbook(filename=file_name)
    _sheet_necessary = _wb.sheet_by_index(index_of_origin_data_sheet_of_file)
    return _sheet_necessary.col_values(col_of_name_of_sheet)


# Get origin name list
poi_of_we_have_list = read_poi_text(originExcelFilePath, 4, 0)

# Get reference data list
wb = xlrd.open_workbook(filename=referenceExcelFilePath)
sheet_necessary = wb.sheet_by_index(0)
poi_of_reference_list_id = sheet_necessary.col_values(0)
poi_of_reference_list_name = sheet_necessary.col_values(1)
poi_of_reference_list_longitude = sheet_necessary.col_values(3)
poi_of_reference_list_latitude = sheet_necessary.col_values(4)

# To assure the size of all list is the same
print("id size is " + str(len(poi_of_reference_list_id)))
print("name size is " + str(len(poi_of_reference_list_name)))
print("longitude size is " + str(len(poi_of_reference_list_longitude)))
print("latitude size is " + str(len(poi_of_reference_list_latitude)))

writePoi = xlwt.Workbook(encoding='utf-8')
sheetWrite = writePoi.add_sheet('data')

for index_of_origin_poi in range(1, len(poi_of_we_have_list)):
 poiName = poi_of_we_have_list[index_of_origin_poi]
 print("Matching for position " + str(index_of_origin_poi) + ", Poi name：" + poiName)
 result = process.extract(poiName, poi_of_reference_list_name, limit=choice_limit)

for index_of_match_size in range(0, choice_limit):
    matchName = result[index_of_match_size][0]
    matchValue = result[index_of_match_size][1]
        # print("matchName is "+str(matchName))
        # print("matchValue is "+str(matchValue))
    for name_index in range(0, len(poi_of_reference_list_name)):
            # This is a workaround to solve the problem that progress does not provide the index of matching result.
        if poi_of_reference_list_name[name_index] == matchName:
                # print(name_index)
            writeOriginName = poiName
            writeMatchValue = matchValue
            writeReferenceId = poi_of_reference_list_id[name_index]
            writeReferenceName = poi_of_reference_list_name[name_index]
            writeReferenceLongitude = poi_of_reference_list_longitude[name_index]
            writeReferenceLatitude = poi_of_reference_list_latitude[name_index]

            position_of_row = choice_limit * index_of_origin_poi + index_of_match_size
            sheetWrite.write(position_of_row, 0, writeOriginName)
            sheetWrite.write(position_of_row, 1, writeMatchValue)
            sheetWrite.write(position_of_row, 2, writeReferenceId)
            sheetWrite.write(position_of_row, 3, writeReferenceName)
            sheetWrite.write(position_of_row, 4, writeReferenceLongitude)
            sheetWrite.write(position_of_row, 5, writeReferenceLatitude)
            break

writePoi.save(dataFile)
print("Data saved successfully! ")