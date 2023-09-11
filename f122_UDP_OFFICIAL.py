from f1_22_telemetry.listener import TelemetryListener#,CarMotionData
from f1_22_telemetry.packets import CarMotionData
import json

listener = TelemetryListener(port=20777, host='127.0.0.1')
counter=0
while True:
    packet = listener.get()
    #print(packet)
    kol=packet.to_dict()
    #print(kol.keys())
    try:
        #print(type(kol),type(kol["car_telemetry_data"]))
        #print(kol["car_status_data"])
        #print(type(kol["car_telemetry_data"]))
        #break
        with open("OHEMGEE.txt", "w") as file1:
            #file1.writelines(json.dumps(kol["car_telemetry_data"].to_dict()))
            file1.writelines(json.dumps(kol["car_telemetry_data"][19]))
        #print(kol["car_telemetry_data"])
        #print(counter)
        counter+=1
        if counter>50:
            break
    except:
        pass
    # with open("OHEMGEE.txt", "w") as file1:
    #     file1.writelines(json.dumps(kol))
    #print(kol)

#car=CarMotionData(packet)

#print(car)
#print(packet)

#print(type(packet))
#print(packet.values)