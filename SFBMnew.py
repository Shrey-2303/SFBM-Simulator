# Original owner of the entire code is SHREY SHAH 19BME134

# IMPORTANT NOTE - I initially calculated inverted Bending moment diagram so to reverse(correct) the sign convention I just add a minus sign in front of Y co-ordinates.


# Gets the required libraries for this entire program.
# matplotlib is a library used for all graphical uses in programing in python.
# numpy is a library made as a support to handle and perform operations on multidimensional arrays and matrices.
# Another such support library can be used such as "Scipy" or "panda".


import matplotlib as mplt
import matplotlib.pyplot as plt
import numpy as np

m= -1000000

# A function for calculating BM from left side (default is right side).
def reversepointloadBM(forces,x):
	currentBM=0
	i=0
	while True:
		
		if forces[i][1]<x:
			if forces[i][0]!="moment":
				currentBM=currentBM + (forces[i][2]*(forces[i][1]-x))
				
				i=i+1
			else:
				currentBM=currentBM-forces[i][2]
				i=i+1
				
		else: 
			break
	return currentBM,i

# A function for calculating BM for Uniformly varying load.
def UVLBM(i,forces):

	w1=forces[i][6]
	l=forces[i][5]
	w2=forces[i][7]
	XcordTemp1 = np.linspace(0,l,500)
	XcordTemp1 = XcordTemp1.tolist()
	j=0

	while j<len(XcordTemp1):
		currentBM = pointloadBM(i+1,forces,forces[i][3]+XcordTemp1[j])
		Wx= w1 + ((XcordTemp1[j]*(w2-w1))/l)
		if (Wx==0 and w2==0):
			force=0
			distance=0
		else:
			force=(l-XcordTemp1[j])/2 * (Wx + w2)
			distance=((l-XcordTemp1[j])/3) * ((Wx + 2*w2)/(Wx + w2))
		y=force*distance + currentBM
		XcordTemp1[j]=XcordTemp1[j] + forces[i][3]
		YcordTemp1.append(-y)
		j=j+1
	return XcordTemp1,YcordTemp1 

# A function for calculating BM for points loads and concentrated loads.
def pointloadBM(i,forces,x):
	currentBM=0
	for j in range(i,len(forces)) :
		if forces[j][0]!="moment":
			currentBM=currentBM + ( forces[j][2]*(forces[j][1]-x) )
		else: 
			currentBM=currentBM+forces[j][2]
	return currentBM

# A function for calculating BM for Uniformly distributed load.
def UDLBM(i,forces):
	w=forces[i][4]
	l=forces[i][5]
	XcordTemp1 = np.linspace(0,forces[i][5], 500)
	XcordTemp1 = XcordTemp1.tolist()
	j=0
	while j<len(XcordTemp1):
		currentBM=pointloadBM(i+1,forces,forces[i][3]+XcordTemp1[j])
		y=w*((l-XcordTemp1[j])**2)/2 + currentBM
		XcordTemp1[j]=XcordTemp1[j] + forces[i][3]
		YcordTemp1.append(-y)
		j=j+1
	return XcordTemp1,YcordTemp1

#declaring initial total of SF and BM.
totalforce=0
totalBM=0

# Choosing the type of support.
print("Choose a support which you would like - \n 1) Cantilever\n 2) simply supported\n 3) Overhanging \n\n")
while True:
	supporttype=int(input("Enter here - "))
	if supporttype<4 and supporttype>0: break
	else:
		print("Please enter valid Beam number.")
		continue

beam=float(input("Enter length of beam - "))

# Takes input of support locations if it is Overhanging Beam.
if supporttype==3:
	while True:
		num1,num2 = input("Enter positions of First and second roller/pin support from measured from left side - ").split()
		num1=float(num1)
		num2=float(num2)
		if num1>beam or num2>beam:
			print("Please enter within beam's length. Try again.\n")
			continue
		if num1>num2: 
			t=num1
			num1=num2
			num2=t
		break

# All user data for number of types of forces.
number=int(input("Enter no. of point forces - "))
UDL=int(input("Enter no. of Distributed forces - "))
UVL = int(input("Enter no. of Undistributed load - "))
moment=int(input("Enter no. of Moments - "))

# Overlapping forces are possible but it will take additional few hundre lines of code so I preferred if no overlap was allowed.
# However it IS possible to get the same result as overlapping with this code by breaking down the overlapped forces at the junctions of overlap. 
print("\n\n ***** Note: Input forces should not overlap with other forces (mainly UDL and UVL)!!!!! *****")
print(" ***** Note: Enter values with space between them without units *****")
print(" ***** Note: You can move the curser over the graph to view exact co=ordinates of a point shown at bottom right *****\n\n")

# Total forces and inputs.
total= UDL + number + UVL + moment
# Data of the different forces is stored in a list called Forces.
forces = []
UDLpoints=[]
UVLpoints=[]

# This loop will get the specific data of individual forces from the users.
for i in range(total):

	# First getting all point forces.
	if i<number: 
		while True:
		    load,distance=input("Enter magnitude of point force and distance from origin - ").split()
		    load=float(load)
		    distance=float(distance)
		    if distance>beam:
			    print("please enter distance within beam's length you have entered\n")
			    continue
		    break

		totalforce=totalforce + load
		totalBM=totalBM+load*distance
		forces.append(["point",distance,load,distance*load])

	# Next getting all Uniformly distributed loads.
	elif i<number+UDL: 
		while True:
			load,start,end=input("Enter Distributed load per meter, its start and end point from origin - ").split()
			load=float(load)
			start=float(start)
			end=float(end)
			if end>beam:
				print("Please enter distance within beam's length you have entered\n")
				continue
			if start>end:
				print("Error - Start point should be less than end point\n")
				continue
			break
		UDLpoints.append([start,end,load])
		mid=(start+end)/2
		totalforce=totalforce + (load*(end-start))
		totalBM=totalBM + (load*(end-start)*mid)
		forces.append(["UDL",mid,load*(end-start),start,load,end-start])

	# Now getting all Uniformly varying loads.
	elif i < total-moment:
		while True:
		    a,b,c,d = input("for Undistributed load, Enter start and end point, then enter load at start and end - ").split()
		    start=float(a)
		    end=float(b)
		    w1=float(c)
		    w2=float(d)
		    if end>beam:
		    	print("Please enter points within the length of Beam.")
		    	continue
		    if w1==w2:
		    	print("Please enter different loads at the points")
		    	continue
		    if start>end:
		    	print("Error - Start point should be less than end point")
		    	continue
		    break

		length=end-start
		if w1+w2==0:
			forces.append(["UVL",start+length/6,(w1*length)/4, start, start+length/2, length/2, w1, 0])
			forces.append(["UVL",end-length/6,(w2*length)/4, start+length/2, end, length/2, 0, w2])
			totalBM = totalBM  + ((w2*length)/4 * (end-(length/6))) + ((w1*length)/4 * (start+(length)/6))
		else:
			totalforce = totalforce + (w1+w2)*length/2
			distance = start + (length/3)*(w1 + 2*w2)/(w1 + w2)
			totalBM = totalBM +  (w1+w2)*length/2 * distance 
			forces.append(["UVL",distance,(w1+w2)*length/2, start, end, length, w1, w2])
		UVLpoints.append([start,end,w1,w2])

	# Lastly getting the moments.
	else:
		while True:
			magnitude,distance = input("Enter magnitude of moment and distance from origin - ").split()
			magnitude=float(magnitude)
			distance=float(distance)
			if distance>beam:
				print("Please anter distance within length of Beam.")
				continue
			totalBM=totalBM-magnitude
			forces.append(["moment",distance,-magnitude])
			break

# Calculates the reaction force of the Support if Simply Supported beam is chosen and is added as a point force in "forces".
if supporttype==2:
	Rb=-(totalBM/beam)
	totalforce=totalforce+Rb
	totalBM= totalBM + Rb*beam
	Ra= -totalforce
	forces.append(["point",0,Ra,Ra*beam,"support"])
	forces.append(["point",beam,Rb,Rb*beam,"support"])

# Calculates the reaction forces of roller and pin support if Overhanging beam is chosen and is added as point force in "forces".
elif supporttype==3:
	forces = sorted(forces, key = lambda x: x[1])
	reverseBM,i=reversepointloadBM(forces,num1)
	currentBM=pointloadBM(i,forces,num1)
	Rb = (reverseBM + currentBM)/(num2-num1)
	Ra = totalforce - Rb
	totalBM = totalBM + (-Rb*num2) + (-Ra*num1)
	totalforce = totalforce - Ra - Rb
	forces.append(["point",num1,-Ra,-num1*Ra,"support"])
	forces.append(["point",num2,-Rb,-num2*Rb,"support"])

# Sorts all the forces according to distance.
forces = sorted(forces, key = lambda x: x[1])

# Several lists for containing the points to plot in SF and BM diagrams are declared below
# Where the below 4 are primary lists and 4 after those are temporary lists. 
XcordSF=[]
YcordSF=[]
XcordBM=[]
YcordBM=[]

XcordTemp=[]
YcordTemp=[]
XcordTemp1=[]
YcordTemp1=[]

# The next lines are to add the total force and moment to respective plots.
XcordTemp1.append(0)
YcordTemp1.append(0)
XcordTemp1.append(0)
YcordTemp1.append(-totalBM)
XcordTemp.append(0)
YcordTemp.append(0)
XcordTemp.append(0)
YcordTemp.append(totalforce)
i=0

# THIS IS A MAJOR LOOP CALCULATING THE GRAPH AND ITS POINTS FOR ALL FORCES.
for element in forces:
	
	# Adding the location of points for points forces.
	if element[0]=="point":

		if element[1]==0 and supporttype==2: 
			i=i+1
			continue
		# Calculates bending moment from right side and adds to the list as current bending moment.
		currentBM=pointloadBM(i+1,forces,element[1])
		XcordTemp1.append(element[1])
		YcordTemp1.append(-currentBM)

		# Calculates shear force at this point force by subtracting its force from total for all forces.
		XcordTemp.append(element[1])
		YcordTemp.append(totalforce)
		totalforce=totalforce-element[2]
		XcordTemp.append(element[1])
		YcordTemp.append(totalforce)
	
	# This will add the points to plot for UNiformly distributed load.
	elif element[0]=="UDL":

		# Adds the point for current BM and resets the temporary list to add all points for Uniformy distributed load.
		# Before resetting the list the list is passed on to the main list of SF anf BM.
		currentBM=pointloadBM(i,forces,element[3])
		XcordTemp1.append(element[3])
		YcordTemp1.append(-currentBM)
		XcordBM.append(XcordTemp1)
		YcordBM.append(YcordTemp1)
		XcordTemp1=[]
		YcordTemp1=[]
		
		# This UDL is passed on to the function to get the points to plot for BM of Uniformly distributed load which are added to the Temp list.
		XcordTemp1,YcordTemp1=UDLBM(i,forces)
		
		# The new Temporary list is again added to the main list before resetting and its last points are added to new Temp list for continuation. 
		XcordBM.append(XcordTemp1)
		YcordBM.append(YcordTemp1)		
		a=XcordBM[len(XcordBM)-1][len(XcordBM[len(XcordBM)-1])-1]
		b=YcordBM[len(YcordBM)-1][len(YcordBM[len(YcordBM)-1])-1]
		XcordTemp1=[]
		YcordTemp1=[]
		XcordTemp1.append(a)
		YcordTemp1.append(b)

		# Adds the points for SF diagram for UDL.
		XcordTemp.append(element[3])
		YcordTemp.append(totalforce)
		totalforce=totalforce-element[2]
		XcordTemp.append(element[3]+element[5])
		YcordTemp.append(totalforce)

	# This condition is for the Uniformly varying load.
	elif element[0]=="UVL":

		# Same as UDL.
		# Adds the point for current BM and resets the temporary list to add all points for Uniformy varying load.
		# Before resetting the list the list is passed on to the main list of SF anf BM.
		XcordTemp1.append(element[3])
		currentBM=pointloadBM(i,forces,element[3])
		YcordTemp1.append(-currentBM)
		XcordBM.append(XcordTemp1)
		YcordBM.append(YcordTemp1)
		XcordTemp1=[]
		YcordTemp1=[]

		# This UVL is passed on to the function to get the points to plot for BM of Uniformly varying load which are added to the Temp list.
		XcordTemp1,YcordTemp1=UVLBM(i,forces)
		
		# The new Temporary list is again added to the main list before resetting and its last points are added to new Temp list for continuation.
		XcordBM.append(XcordTemp1)
		YcordBM.append(YcordTemp1)
		a=XcordBM[len(XcordBM)-1][len(XcordBM[len(XcordBM)-1])-1]
		b=YcordBM[len(YcordBM)-1][len(YcordBM[len(YcordBM)-1])-1]
		XcordTemp1=[]
		YcordTemp1=[]
		XcordTemp1.append(a)
		YcordTemp1.append(b)

		# These lines are for the start of points force for UVL
		XcordTemp.append(element[3])
		YcordTemp.append(totalforce)
		XcordSF.append(XcordTemp)
		YcordSF.append(YcordTemp)

		# These set of lines are to get the points for the SHear force of the UVL
		XcordTemp=[]
		YcordTemp=[]
		XcordTemp = np.linspace(0,element[5], 500)
		XcordTemp = XcordTemp.tolist()
		j=0
		while j<len(XcordTemp):
			Wx= element[6] + XcordTemp[j]*(element[7]-element[6])/element[5]
			y=(element[5]-XcordTemp[j])/2 * (Wx + element[7]) + totalforce - element[2]
			XcordTemp[j]=XcordTemp[j] + element[3]
			YcordTemp.append(y)
			j=j+1
		

		totalforce=totalforce-element[2]

		# The new Temporary list is again added to the main list before resetting and its last points are added to new Temp list for continuation.
		XcordSF.append(XcordTemp)
		YcordSF.append(YcordTemp)
		a=XcordSF[len(XcordSF)-1][len(XcordSF[len(XcordSF)-1])-1]
		b=YcordSF[len(YcordSF)-1][len(YcordSF[len(YcordSF)-1])-1]
		XcordTemp=[]
		YcordTemp=[]
		XcordTemp.append(a)
		YcordTemp.append(b)

	# This condition is for the moments, if added.
	else:

		# Calculates current BM and subtracts this moment from current.
		currentBM=pointloadBM(i+1,forces,element[1])
		currentBM=currentBM+element[2]
		XcordTemp1.append(element[1])
		YcordTemp1.append(-currentBM)
		currentBM=currentBM - element[2]
		XcordTemp1.append(element[1])
		YcordTemp1.append(-currentBM)
	i=i+1	

# Whichever will be the last Temporary list will be added to the main list for assurance.
XcordBM.append(XcordTemp1)
YcordBM.append(YcordTemp1)
XcordSF.append(XcordTemp)
YcordSF.append(YcordTemp)

# The next 6 lines just plot the beam length and get the farthest points.
lastSF=XcordSF[len(XcordSF)-1][len(XcordSF[len(XcordSF)-1])-1]
lastBM=XcordBM[len(XcordBM)-1][len(XcordBM[len(XcordBM)-1])-1]

XcordTemp.append(beam)
YcordTemp.append(0)
XcordTemp1.append(beam)
YcordTemp1.append(0)

# This is some trash value assigned which will be used as a tool for checking.
leftundef = m
rightundef = m
result = m
result2 = m

# THIS IS MAJOR FUNCTION WHICH DOES THE FINAL PLOTTING OF GRAPH FROM THE POINTS WE CALCULATED.
# Target, result1 and result2 are for finding SFBM at specific point if user desires it.
def plot(target=None,result1=None,result2=None):

	#mplt.style.use("dark_background")
	# Defines the graphes named as described and adds the usual labels for main Figure.
	fig,(ax1,ax2) = plt.subplots(2,1,num="SFBM Diagram", sharex=True , figsize = (8,6))
	fig1,ax0 = plt.subplots(1,1,num="Beam Diagram",figsize= (8,6))
	# Draws the hinge for cantilever beam.
	if supporttype==1 :
		ax0.plot([0,0],[-20,20],'k')
		for i in np.linspace(-20,20,15):
			ax0.plot([0,-0.1],[i,i+2.5],'k') 
	
	# Title, legends and beam for beam diagram.
	ax0.grid()
	ax0.set_ylabel("Force")
	ax0.plot([0,beam],[0,0], "-k")
	if any("point" in sublist for sublist in forces) is True : ax0.plot([],[],color='b' ,label="Point force")
	if any("UDL" in sublist for sublist in forces) is True : ax0.plot([],[],color='g' ,label="UDL")
	if any("UVL" in sublist for sublist in forces) is True : ax0.plot([],[],color='r' ,label="UVL")
	if any("moment" in sublist for sublist in forces) is True : ax0.plot([],[] ,color='c',label="Moment")
	if supporttype==2 or supporttype==3: ax0.plot([],[],color='m' ,label="Support force")
	ax0.legend(loc="upper left")

	# Plots the arrows for all Points forces.
	for elements in forces:
		if elements[0]=="point":
			edgecolor='b'
			if len(elements)==5: edgecolor='m'
			arrlen=elements[2]/10
			if elements[2]<0: arrlen= (-arrlen)
			ax0.arrow(elements[1],elements[2],0,-9*elements[2]/10, head_width=elements[2]/90, head_length=arrlen, fc='k', ec=edgecolor)

	# Funtion to plot the UDL for beam diagram.
	def UDLplot(start,end,load):
		Xcordudl = np.linspace(start,end, 10)
		Xcordudl = Xcordudl.tolist()
		y=[load]*10
		ax0.plot([start,end],[load,load],'k')
		for i in range(10):
			arrlen=load/10
			if load<0: arrlen= (-arrlen)
			ax0.arrow(Xcordudl[i],load,0,-9*load/10, head_width=load/90, head_length=arrlen, fc='k', ec='g')	
	
	# Function to plot the UVL for beam diagram.
	def UVLplot(start,end,w1,w2):
		Xcorduvl = np.linspace(0,end-start,10)
		Xcorduvl = Xcorduvl.tolist()
		ax0.plot([start,end],[w1,w2],'k')
		for i in range(10):
			Wx= w1 + (Xcorduvl[i])*((w2-w1)/(end-start))
			arrlen=Wx/10
			if Wx<0: arrlen= (-arrlen)
			ax0.arrow(start+Xcorduvl[i],Wx,0,-9*Wx/10, head_width=Wx/90, head_length=arrlen, fc='k', ec='r')
	
	# The funcitn is used here.
	for i in UDLpoints: UDLplot(i[0],i[1],i[2])
	for i in UVLpoints: UVLplot(i[0],i[1],i[2],i[3])
	
	# This draws the moment curving arrow for moments.
	for i in forces : 
		if i[0]=='moment' :
			if i[2]<0:
				name=r'$\circlearrowleft$'
			else: name =r'$\circlearrowright$'
			ax0.plot([i[1]],[0],ms=30,marker=name,color='c',mew=0.1)

	# Writes the title and labels for SF diagram.
	ax1.set_title("Shear Force Diagram")
	ax1.grid()
	ax1.plot([0,lastSF],[0,0],"-k")
	ax1.set_ylabel("Force")

	# Plots the COMPLETE SF diagram.
	for i in range(len(XcordSF)):	
		ax1.plot(XcordSF[i],YcordSF[i], "-b")

	# Writes the title and labels for BM diagram.
	ax2.set_title("Bending Moment diagram")
	ax2.grid()
	ax2.plot([0,lastBM],[0,0],"-k")
	ax2.set_ylabel("Moment") 

	# Plots the COMPLETE BM diagram.
	for i in range(len(XcordBM)):	
		ax2.plot(XcordBM[i],YcordBM[i], "-b")

	# locates the point as per the user's needs and highlights it in graph.
	if target is not None:
		ax1.plot([target],[result1],'x',color='green',ms=10)
		ax2.plot([target],[result2],'x',color='green',ms=10)
		ax1.plot([0,target,target],[result1,result1,0],'--m')
		ax2.plot([0,target,target],[result2,result2,0],'--m')
		ax1.plot([],[],linestyle='None' ,marker='x',markeredgecolor='green' ,label=(target,result1))
		ax2.plot([],[],linestyle='None' ,marker='x',markeredgecolor='green' ,label=(target,result2))
		ax1.legend(loc="upper right")
		ax2.legend(loc="upper right")
	
	# Shows the graph
	fig.tight_layout()
	fig1.tight_layout()
	plt.show()

# This calls the function (for doing the work).
plot()

# The following statements are specifically for the user if they desire to find SFBM at a specific point
while True:
	# here Target is the point where user wants to find SFBM and result and resul2 are calculated data.
	answer=input("Do you want to find SFBM at a specific point ? (Y/N) - ")
	if answer =='y' or answer=='Y':
		target=float(input("Enter a target value that you want to find SF and BM at - "))
		for i in range(len(XcordSF)):
			if result == m:
				result=np.interp(target,XcordSF[i],YcordSF[i],right=rightundef,left=leftundef)
		for i in range(len(XcordBM)):
			if result2 == m:
				result2=np.interp(target,XcordBM[i],YcordBM[i],right=rightundef,left=leftundef)
		if result == m and result2==m:
			print("You entered a point beyond the beam's length")
		else :
			print("your Shear force points are (",target, round(result,3),")")
			print("your Bending moment points are (",target, round(result2,3),")\n\n")
			
			# Plots again with the specified point.
			plot(target,round(result,3),round(result2,3))
		
		result=m
		result2=m
			
	elif answer =='n' or 'N' : break
	else : 
		print("Please enter Valid letter.")
		continue





# Original owner of the entire code is SHREY SHAH 19BME134