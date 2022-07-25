import xlrd
import matplotlib.pyplot as plt

reports = ["banknote-authentication_nf_4","shuttle-landing-control_nf_6", "hls4ml_lhc_jets_hlf_nf_16", "climate-model-simulation-crashes_nf_20"]#, "mnist_784_nf_784"]

features = []
luts = []
luts_ram  = []
ffs = []
brams =  []

resources = ["LUT", "LUTRAM", "FF", "BRAM"]

board = "ebaz4205"
part = "xc7z010clg400-1"


lut_thresholds = {
    "ebaz4205": {
        "LUT": 17700,
        "LUTRAM": 6000,
        "FF": 35200,
        "BRAM": 60
    },
    "pynqz2": {
        "LUT": 53200
    },
}

model = "nn_mod_2"

for r in reports:

    workbook = xlrd.open_workbook("reports/"+model+"/"+r+"/xc7z010clg400-1/Table.xlsx")
    worksheet = workbook.sheet_by_index(0)

    lut = 0
    lut_ram = 0
    ff = 0
    bram = 0

    for i in range(0, 5):
        for j in range(0, 4):
            if worksheet.cell_value(i, j) in resources:
                if worksheet.cell_value(i, j) == "LUT":
                    lut = worksheet.cell_value(i, j+1)
                elif worksheet.cell_value(i, j) == "LUTRAM":
                    lut_ram = worksheet.cell_value(i, j+1)
                elif worksheet.cell_value(i, j) == "FF":
                    ff = worksheet.cell_value(i, j+1)
                elif worksheet.cell_value(i, j) == "BRAM":
                    bram = worksheet.cell_value(i, j+1)

    features.append(r[r.rindex("_")+1:len(r)])
    luts.append(lut)
    luts_ram.append(lut_ram)
    ffs.append(ff)
    brams.append(bram)

for r in resources:

    if r == "LUT":
        fig, ax = plt.subplots()
        ax.plot(luts, features, linewidth=2.0)
        plt.axvline(x = lut_thresholds[board][r], color = 'r', linestyle = '-')
        plt.xlabel("Luts (all luts consumed in the design)")
    elif r == "LUTRAM":
        fig, ax = plt.subplots()
        ax.plot(luts_ram, features, linewidth=2.0)
        plt.axvline(x = lut_thresholds[board][r], color = 'r', linestyle = '-')
        plt.xlabel("Lut ram (lut in the slicem) ")
    elif r == "FF":
        fig, ax = plt.subplots()
        ax.plot(ffs, features, linewidth=2.0)
        plt.axvline(x = lut_thresholds[board][r], color = 'r', linestyle = '-')
        plt.xlabel("flip flop")
    elif r == "BRAM":
        fig, ax = plt.subplots()
        ax.plot(brams, features, linewidth=2.0)
        plt.axvline(x = lut_thresholds[board][r], color = 'r', linestyle = '-')
        plt.xlabel("block ram")

    
    plt.ylabel("Features")
    plt.show()