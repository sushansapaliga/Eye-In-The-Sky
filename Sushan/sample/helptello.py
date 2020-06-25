
data = "ALT: 11 | SPD:  0 | BAT: 47 | WIFI: 90 | CAM:  0 | MODE:  6"
wifi = int(str(data).split("WIFI: ")[1].split(" ")[0])
alt = int(str(data).split("ALT: ")[1].split(" ")[0])
print(wifi)
print(alt)