import pandas as pd
import numpy as np
import json as js
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mplcyberpunk
import cv2 as cv

times=[]
drivers=[]

plt.style.use("cyberpunk")

#fig, (ax1,ax2)=plt.subplots(nrows=2,ncols=1)
fig, ((ax1,ax2),(ax3,ax4))=plt.subplots(nrows=2,ncols=2)

def animate(m):
    while True:
        try:
            times=pd.read_json("Times.txt")
            fuels=pd.read_json("Fuels.txt")
            #drivers=pd.read_json("Drivers.txt")
            with open("Drivers.txt", "r") as file1:
                drivers=js.loads(file1.readline().strip())
            with open("Total_Laps.txt", "r") as file1:
                track_length=float(file1.readline().strip())
                lap_total=float(file1.readline().strip())
                player_index=int(file1.readline().strip())
            with open("Current_Lap.txt", "r") as file1:
                current_lap=dict(zip(drivers,js.loads(file1.readline().strip())))
                lap_distance=dict(zip(drivers,js.loads(file1.readline().strip())))
            break
        except:
            pass
    # _drivers=[]
    # for i in drivers[0]:
    #     _drivers.append(i)
    # drivers=_drivers.copy()

    player_index=drivers[player_index]
    times.columns=drivers
    fuels.columns=drivers
    try:
        times=times.drop(labels=[0])
        times=times.drop(labels=[-1])
        times=times.drop(columns='')
        fuels=fuels.drop(columns='')
    except:
        pass
        #fuels=fuels.drop(labels=[0,-1])


    Race_Time_Passed=0
    Drivers_Average_Time={}
    Drivers_Race_Distance={}
    Drivers_Pace={}
    Drivers_Estimated_Race_Progress={}
    Drivers_Current_Lap_Number={}
    Pit_Stop_Offset=27*1000
    Drivers_Estimated_Race_Progress_Pit_Stop={}
    for i in times:
        Race_Time_Passed=0
        Drivers_Average_Time[i]=0
        Drivers_Race_Distance[i]=0
        Drivers_Current_Lap_Number[i]=0
        for j in times[i]:
            if not np.isnan(j):
                Drivers_Current_Lap_Number[i]+=1
                Drivers_Average_Time[i]+=j
        Race_Time_Passed=Drivers_Average_Time[i]
        #Drivers_Average_Time[i]/=Drivers_Current_Lap_Number[i]-1+lap_distance[i]/track_length
        Drivers_Average_Time[i]/=(Drivers_Current_Lap_Number[i]-1)*track_length+lap_distance[i]
        if Drivers_Average_Time[i]==0:
            Drivers_Average_Time[i]=99999999
        Drivers_Race_Distance[i]=(Drivers_Current_Lap_Number[i]-1)*track_length+lap_distance[i]
        Drivers_Pace[i]=Drivers_Race_Distance[i]/Drivers_Average_Time[i]
        Drivers_Estimated_Race_Progress[i]=Drivers_Pace[i]*Race_Time_Passed/(lap_total*track_length)
        
        Drivers_Average_Time[i]=Race_Time_Passed+Pit_Stop_Offset
        Drivers_Average_Time[i]/=(Drivers_Current_Lap_Number[i]-1)*track_length+lap_distance[i]
        if Drivers_Average_Time[i]==0:
            Drivers_Average_Time[i]=99999999
        Drivers_Pace[i]=Drivers_Race_Distance[i]/Drivers_Average_Time[i]
        Drivers_Estimated_Race_Progress_Pit_Stop[i]=Drivers_Pace[i]*Race_Time_Passed/(lap_total*track_length)
    #print(lap_distance)
    lap_distance=dict(sorted(lap_distance.items(), key=lambda item: item[1]))
    try:
        lap_distance.pop("")
    except:
        pass
    #print(lap_distance)
    Drivers_Order={i:j for i,j in sorted(lap_distance.items(),key=lambda lap:lap[1], reverse=False)}
    Drivers_Order=[i for i in Drivers_Order]
    player_fuel_status={"Current":0,"Average_Consume":[],"Range":0}
    player_fuels_consume=[]
    for i in fuels[player_index]:
        player_fuel_status["Current"]=i
        player_fuels_consume.append(i)
    #print("--")
    player_fuel_status["Current"]-=0.2 #LOW FUEL MODE
    #print(player_fuel_status["Current"])
    try:
        player_fuel_status["Average_Consume"]=np.diff(player_fuels_consume).tolist()#[player_fuels_consume[i+1]-player_fuels_consume[i] for i in range(len(player_fuels_consume)-1)]
        #player_fuel_status["Average_Consume"]=-1*(sum(player_fuel_status["Average_Consume"])/((Drivers_Current_Lap_Number[player_index]-1)+lap_distance[player_index]/track_length))
        player_fuel_status["Average_Consume"]=-1*min(player_fuel_status["Average_Consume"])
        player_fuel_status["Range"]=player_fuel_status["Current"]/player_fuel_status["Average_Consume"]-(lap_total)+Drivers_Current_Lap_Number[player_index]+lap_distance[player_index]/track_length
        #print(player_fuel_status["Range"])
    except:
        player_fuel_status["Range"]=69

    #print(Drivers_Current_Lap_Number[player_index])
    while "" in drivers:
        drivers.remove("")

    #print(lap_distance["STROLL"])

    plt.cla()
    ax1.cla()
    ax2.cla()
    ax3.cla()
    ax4.cla()
    # ax1.set_ylim((-1.8, 1.8))
    # ax2.set_ylim((-1.8, 1.8))
    # ax1.set_xlim((-1.8, 1.8))
    # ax2.set_xlim((-1.8, 1.8))
    #ax1.plot([times[i] for i in drivers[:10]],marker='o')
    #ax1.plot(times,marker='o')
    ax1.plot(times.iloc[:,:10],marker='o')
    ax1.plot(times.iloc[:,10:],marker='^')
    ax1.legend([i for i in drivers[:10]],loc="upper left")
    ax1.set_ylim((0, 200000))
    #ax1.plot([times[i] for i in drivers[10:]],marker='^')
    #print([fuels[i] for i in drivers[:10]])
    #ax2.plot([fuels[i] for i in drivers[:10]],marker='^')
    #ax2.plot(fuels,marker='o')
    ax2.plot(fuels.iloc[:,:10],marker='o',label="_nolegend_")
    ax2.plot(fuels.iloc[:,10:],marker='^')
    ax2.legend([i for i in drivers[10:]],loc="upper right")
    ax2_img=fig.add_axes([0.75, 0.75, 0.2, 0.2], zorder=10)
    blank_image = np.zeros((50,50,3), np.uint8)
    blank_image=cv.putText(blank_image,str(player_fuel_status["Range"]),(0,25),cv.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),1,cv.LINE_AA)
    #ax2_img.imshow(cv.imread("image.png"))
    ax_ax=ax2_img.imshow(blank_image)
    ax2_img.axis("off")
    ax_ax.axes.get_xaxis().set_visible(False)
    ax_ax.axes.get_yaxis().set_visible(False)
    #ax2.imshow(cv.imread("image.png"))
    
    #ax2.plot([fuels[i] for i in drivers[10:]],marker='o')
    #ax2.plot(fuels,marker='^')
    #print(Drivers_Estimated_Race_Progress["STROLL"],Drivers_Estimated_Race_Progress_Pit_Stop["STROLL"])
    #print([k for k in Drivers_Estimated_Race_Progress.keys()])
    bars=ax4.bar([i[:3] for i in Drivers_Order],[Drivers_Estimated_Race_Progress[k] for k in Drivers_Order],color=[dict(zip(drivers,['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21']))[i] for i in Drivers_Order],zorder=4,width=0.5)
    bars2=ax4.bar([i[:3] for i in Drivers_Order],[Drivers_Estimated_Race_Progress_Pit_Stop[k] for k in Drivers_Order],color=[dict(zip(drivers,['C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31', 'C32', 'C33', 'C34', 'C35', 'C36', 'C37', 'C38', 'C39', 'C40', 'C41', 'C42', 'C43']))[i] for i in Drivers_Order],zorder=5,width=0.5)
    Drivers_Order=[i for i,j in sorted(lap_distance.items(),key=lambda lap:lap[1]+Drivers_Current_Lap_Number[lap[0]]*track_length, reverse=False)]
    #print(Drivers_Order)
    #bars3=ax4.barh(Drivers_Order,[Drivers_Race_Distance[k] for k in Drivers_Order],color=[dict(zip(drivers,['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21']))[i] for i in Drivers_Order],zorder=4)
    bars3=ax3.barh(Drivers_Order,[Drivers_Race_Distance[k] for k in Drivers_Order],color=[dict(zip(drivers,['C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31', 'C32', 'C33', 'C34', 'C35', 'C36', 'C37', 'C38', 'C39', 'C40', 'C41', 'C42', 'C43']))[i] for i in Drivers_Order],zorder=5)
    ax3.set_xlim((0,lap_total*track_length))
    for item in ([ax4.title, ax4.xaxis.label, ax4.yaxis.label] + ax4.get_xticklabels() + ax4.get_yticklabels()):
        item.set_fontsize(9)
    # bars=ax3.barh([k for k in Drivers_Estimated_Race_Progress.keys()],[k for k in Drivers_Estimated_Race_Progress.values()],color=['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21'],zorder=4)
    # bars2=ax3.barh([k for k in Drivers_Estimated_Race_Progress.keys()],[k for k in Drivers_Estimated_Race_Progress_Pit_Stop.values()],color=['C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31', 'C32', 'C33', 'C34', 'C35', 'C36', 'C37', 'C38', 'C39', 'C40', 'C41', 'C42', 'C43'],zorder=5)
    #mplcyberpunk.add_bar_gradient(bars=bars2)
    #ax1.legend(drivers,loc="lower left")
    #mplcyberpunk.add_glow_effects()
    #mplcyberpunk.make_lines_glow(ax1)
    mplcyberpunk.add_underglow(ax1)
    #mplcyberpunk.add_glow_effects(gradient_fill=True)
    #mplcyberpunk.add_gradient_fill(ax1,alpha_gradientglow=(0.5,1),gradient_start="zero")
    #plt.tight_layout()
# while True:
#     try:
#         ani = animation.FuncAnimation(plt.gcf(), animate, interval=1000)
#     except:
#         pass
#     #plt.tight_layout()
#     plt.show()


ani = animation.FuncAnimation(plt.gcf(), animate, interval=1000)
plt.show()
# sns.set(style="ticks")
# sns.lineplot(data=data, palette="tab10", linewidth=2.5)
# sns.show()