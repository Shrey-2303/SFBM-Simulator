This program is made of 540 lines of code and hardowrk.
Thank you in advance.

The following program will calulate and plot the SFBM diagram visually and show it to the user. The beam diagram 
will also be shown in another figure for reference.

Beam diagram - the bream diagram will represent the types of forces and show how they act on the selected beam.
               (different forces have different colors for better view.)
SF diagram - This will show the shear force diagram varying form 0 to beam length.
BM diagram - this will show the Bending moment diagram similar to SF diagram.

This program can calculate for 3 types of beams - Cantilever, Simply Supported and Overhanging beam.

1) How to run?
THIS IS A ".py" FILE, IT WON"T WORK IF U OPEN IT WITHOUT PYTHON INSTALLED. Click on the python file and run it
(should have python). This program requires 2 libraries namely - Matplotlib and numpy.

2) How to enter inputs?
The program will ask the inputs for things enter all in number ONLY. If more than 2 numbers are to be inputed,
give a space between them. If the number of inputs you entered does not match the no. pf inputs required or similar
then the program will show error and will END. So read carefully while entering what is asked.

3) How to navigate the graph?
Once the SFBM graph is shown. you can point your curser to a space in graph and in the bottom right the coordinates
of that point will be displayed. There are other tools such as magnify or move which you know what they are by name.

4) How to locate SFBM at a specified point (distance) ?
Once you are done with viewing the initial graph, close both the windows - Beam and SFBM diagram. the program will
then promt you to answer if you want to find SFBM at a point, type 'y' or 'Y' to say yes. Note - presing any other
key will result in ending the program meaning you do not want to find at specified point.
After cicking yes it will promt you to specify the point at which you wan tto calculate, after it is done calculating
the progrqam will print the values in below and show the  diagrams again HIGHLIGHTING the specified point with a 
marker with coordinates.


***** DRAWBACKS *****

1) THIS PROGRAM CANNOT CALCULATE OVERLAPPING FORCES !!!! meaning if you entered 2 forces at same place (eg - UDL 
   from 2m to 5m and UVL from 3m to 6m) thought it will calculate SOMETHING but it wont be the correct graph.
   Overlap should not be present between different AND same kind of forces including support force.

   It is possible to remove this drawback but it will be a ton of work as the program already has 500 lines of code

SOLUTION - Althought this program cannot calculate overlappping forces on its own it can still produce the same result
           as an Overlapped result by breaking down or splitting the overlapping forces and adding as seperate entries.
           example (1) - if you want to add a UDL form 3m to 7m but there is a support at 4 m then you can add 2 UDL(s)
                         from 3m to 4m AND 4m to 7m. then it will produce same result.
           example (2) - if you want to add  UVL form 3m to 6m and a force at 5m then you can split UVL form 3m to 5m
                         and 5m to 6m and later add force at 5m. This will again produce the same result as it should.

