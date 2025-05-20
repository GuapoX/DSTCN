foc=4236.6
real_hight_dust=27.56
def detect_distance_dust(h):
    dis_inch=(real_hight_dust * foc) / (h-2)
    dis_cm=dis_inch * 2.54
    dis_cm=int(dis_cm)
    dis_m=dis_cm/100
    return dis_m
# def detect_location_dust(angle,dis):
    
