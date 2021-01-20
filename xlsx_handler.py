import xlsxwriter

def main():
    row_number = -1
    workbook = xlsxwriter.Workbook("links.xlsx")
    worksheet1 = workbook.add_worksheet()

    lengths = [[], [], [], [], []]
    max_lenghts = []

    with open("links.tsv") as f:
        for line in f.readlines():
            row_number = row_number + 1
            column_number = -1
            columns = line.split("\t")
            for column in columns:
                column_number = column_number + 1
                worksheet1.write(row_number, column_number, column)

            for idx, column in enumerate(columns):
                lengths[idx].append(len(column))

    for element in lengths:
        # print(lengths)
        max_lenghts.append(max(element))
    
    for idx, ele in enumerate(max_lenghts):
        worksheet1.set_column(idx, idx, ele)
        print(str(idx) + ', ' + str(ele/2))

    workbook.close()

if __name__ == '__main__':
    main()
    