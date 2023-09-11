from f1_22_telemetry.listener import TelemetryListener#,CarMotionData
from f1_22_telemetry.packets import CarMotionData
import json
import pandas as pd

class lap_data():
    def __init__(self):
        self.total=0
        self.drivers=[]
        self.times={}
        self.fuel={}
        self.current_lap=[]
        self.lap_distance=[]
        self.laps={}
        self.track_length=0
lap_data=lap_data()
listener = TelemetryListener(port=20777, host='127.0.0.1')
counter=0
while True:
    packet = listener.get()
    #print(packet)
    kol=packet.to_dict()
    player_index=kol["header"]["player_car_index"]
    try:
        for i in kol["car_telemetry_data"][player_index]["brakes_temperature"]:
            if i>=600:
                pass#print("release")
            # else:
            #     print("good")
    except:
        pass
    try:
        lap_data.total=kol["total_laps"]
        #print("BB")
        #print(kol.keys())
        lap_data.track_length=kol["track_length"]#["track_length"]
        #print("AA")
        #print(lap_data.total,lap_data.track_length)
        with open("Total_Laps.txt", "w") as file1:
            #file1.writeline(["AYAWKOL"])
            # file1.writeline(json.dumps(lap_data.track_length))
            # file1.writeline(json.dumps(lap_data.total))
            file1.writelines([json.dumps(lap_data.track_length),'\n',json.dumps(lap_data.total),'\n',json.dumps(player_index)])
            # file1.write(json.dumps(lap_data.track_length))
            # file1.write(json.dumps(lap_data.total))
            #file1.writeline()
    except:
        pass
    try:
        if len(lap_data.times)==0:# and lap_data.total>0:
            lap_data.drivers=[i["name"] for i in kol["participants"]]
            lap_data.lap_distance=[None for i in kol["participants"]]
            lap_data.current_lap=[None for i in kol["participants"]]
            for i in range(len(lap_data.drivers)):
                lap_data.times[i]={}
                if len(lap_data.fuel)<len(lap_data.drivers):
                    lap_data.fuel[i]={}
                #lap_data.laps[i]={_:{"Fuel":None,"Last_Lap_Time":None} for _ in range(lap_data.total)}
            with open("Drivers.txt", "w") as file1:
                file1.writelines(json.dumps(lap_data.drivers))
        #print(lap_data.times)
    except:
        pass
    try:
        for i in range(len(kol["lap_data"])):    
            #if kol["lap_data"][i]["current_lap_num"] not in lap_data.times[i]:
            lap_data.times[i][kol["lap_data"][i]["current_lap_num"]]=kol["lap_data"][i]["current_lap_time_in_ms"]
            lap_data.times[i][kol["lap_data"][i]["current_lap_num"]-1]=kol["lap_data"][i]["last_lap_time_in_ms"]
            #print("TEST")
            lap_data.current_lap[i]=kol["lap_data"][i]["current_lap_num"]
            lap_data.lap_distance[i]=kol["lap_data"][i]["lap_distance"]
            #print("AS")

            #lap_data.laps[i][kol["lap_data"][i]["current_lap_num"]-1]["Last_Lap_Time"]=kol["lap_data"][i]["last_lap_time_in_ms"]


        with open("Times.txt", "w") as file1:
            file1.writelines(json.dumps(lap_data.times))
        with open("Current_Lap.txt", "w") as file1:
            #file1.writelines(json.dumps(lap_data.current_lap))
            file1.writelines([json.dumps(lap_data.current_lap),'\n',json.dumps(lap_data.lap_distance)])
        with open("Lap_Number.txt", "w") as file1:
            file1.writelines(json.dumps(lap_data.lap_distance))
    except:
        pass
    try:
        for i in range(len(kol["car_status_data"])):    
            lap_data.fuel[i][lap_data.current_lap[i]]=kol["car_status_data"][i]["fuel_in_tank"]
            #lap_data.laps[i][lap_data.current_lap[i]]["Fuel"]=kol["car_status_data"][i]["fuel_in_tank"]
            #lap_data.times[i][kol["lap_data"][i]["current_lap_num"]-1]=kol["car_status_data"][i]["fuel_in_tank"]
        with open("Fuels.txt", "w") as file1:
            file1.writelines(json.dumps(lap_data.fuel))
    except:
        pass
    try:
        pass
        # print("BB")
        # #print(kol.keys())
        # lap_data.track_length=kol["track_length"]#["track_length"]
        # print("AA")
        # with open("Laps.txt", "w") as file1:
        #     file1.writeline(json.dumps(lap_data.track_length))
        #     file1.writeline(json.dumps(lap_data.total))
        # for i in range(len(kol["session_uid"])):
        #     pass
        # with open("Laps.txt", "w") as file1:
        #     file1.writelines(json.dumps(lap_data.laps))
    except:
        pass
    try:
        pass
    except:
        pass
    # try:
    #     pd.DataFrame(lap_data., [i for i in range(len(lap_data.final))], columns=["A", "B", "C", "D"])
    # except:
    #     pass
    # with open("OHEMGEE.txt", "w") as file1:
    #     file1.writelines(json.dumps(kol))
    #print(kol)