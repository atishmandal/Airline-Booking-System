from tkinter import *
from tkinter import ttk
from datetime import date
import mysql.connector as mc
cc=mc.connect(host='localhost',user='root',password='my_password',database='project')
cr=cc.cursor()
cr.execute('use project')

#Basic intro page
class main_scr(Tk):
    def __init__(self):
        super().__init__()
        self.title('Airline Ticket Booking System')
        self.geometry('400x225')
        Label(self,text='Welcome to Online Air Ticket Booking System').pack()
        Button(self,text='Book Flight',command=self.bookflight).pack()
        Button(self,text='Cancel Ticket',command=self.cancelflight).pack()
        Button(self,text='View Bill',command=self.viewbill).pack()
    def bookflight(self):
        win1=Book_Ticket(self)
        win1.grab_set()
    def cancelflight(self):
        win2 = Cancel_Ticket(self)
        win2.grab_set()
    def viewbill(self):
        win3=View_Bill(self)
        win3.grab_set()

#Ticket Booking
class Book_Ticket(Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.title("Flight booking")
        self.geometry('500x500')
        arrive=StringVar()
        depart=StringVar()
        fno = StringVar()
        pid=StringVar()
        pname=StringVar()
        dob=StringVar()
        sety=StringVar()
        bdate=StringVar()
        food=StringVar()
        lg=StringVar()
        print("Food options:")
        print('None, Regular 6% of base cost, Premium 15% of base cost')
        print("Seat options:")
        print('Economy, Business 35% of base cost, Suite 60% of base cost')
        print("Luggage Rates:")
        print('Less than 15 kg no additional charge')
        print('Between 15 and 20 kg, 7% of base cost')
        print('More than 20 kg, 12% of base cost')
        Label(self,text='Place of Departure',font=("Calibri",12)).place(x=10,y=40)
        Entry(self,width=30,textvariable=depart).place(x=140,y=40)
        Label(self,text='Place of Arrival',font=("Calibri",12)).place(x=10,y=70)
        Entry(self,width=30,textvariable=arrive).place(x=140,y=70)
        Button(self,text='Show available flights',command= lambda: self.show_flights(arrive.get(), depart.get())).place(x=120,y=100)
        Label(self,text='Flight Number',font=("Calibri",12)).place(x=10,y=130)
        Entry(self,width=30,textvariable=fno).place(x=140,y=130)
        Label(self,text='Passenger ID',font=("Calibri",12)).place(x=10,y=160)
        Entry(self,width=30,textvariable=pid).place(x=140,y=160)
        Label(self,text='Passenger Name',font=("Calibri",12)).place(x=10,y=190)
        Entry(self,width=30,textvariable=pname).place(x=140,y=190)
        Label(self,text='DOB',font=("Calibri",12)).place(x=10,y=220)
        Entry(self,width=30,textvariable=dob).place(x=140,y=220)
        Label(self,text='Seat type',font=("Calibri",12)).place(x=10,y=250)
        Entry(self,width=30,textvariable=sety).place(x=140,y=250)
        Label(self,text='Book date',font=("Calibri",12)).place(x=10,y=280)
        Entry(self,width=30,textvariable=bdate).place(x=140,y=280)
        Label(self,text='Food',font=("Calibri",12)).place(x=10,y=310)
        Entry(self,width=30,textvariable=food).place(x=140,y=310)
        Label(self,text='Luggage Weight',font=("Calibri",12)).place(x=10,y=340)
        Entry(self,width=30,textvariable=lg).place(x=140,y=340)
        Button(self,text='Book Ticket',command=lambda:self.add_ticket(fno.get(),pid.get(),pname.get(),dob.get(),sety.get(),bdate.get(),food.get(),lg.get())).place(x=120,y=370)
    def add_ticket(self,a,b,c,d,e,f,g,h):
        qry6=f"select count(*) from passenger where flightno={a} and seattype='{e}'"
        cr.execute(qry6)
        d4=cr.fetchall()
        if d4[0][0]>=5:print("All available seats for this seat type in this flight have been booked. Please select another seattype and restart the booking process")
        else:
            qry = f"insert into passenger values({a},{b},'{c}','{d}','{e}','{f}','{g}',{h})"
            cr.execute(qry)
            print("Ticket booked")
            cc.commit()
            #Flight bill
            window=Tk()
            window.geometry('400x400')
            window.title('Flight Bill')
            qry2=f'select basecost from details where flightno={a}'
            cr.execute(qry2)
            d1=cr.fetchall()
            base=d1[0][0]
            fc=0;seatc=0;luggc=0
            if g=='none':fc=0
            elif g=='regular':fc=0.06*float(base)
            elif g=='premium':fc=0.15*float(base)
            if e=='economy':seatc=0
            elif e=='business':seatc=0.35*float(base)
            elif e=='suite':seatc=0.6*float(base)
            if int(h)<15:luggc=0
            elif int(h)>=15 and int(h)<=20:luggc=float(base)*0.07
            elif int(h)>20:luggc=float(base)*0.12

            qry3=f"select count(*) from passenger where flightno={a} and seattype='{e}'"
            cr.execute(qry3)
            d2=cr.fetchall()
            avc=0
            if d2[0][0]<3:avc=0
            elif d2[0][0]==3 or d2[0][0]==4:avc=float(base)*0.09
            elif d2[0][0]==5:avc=float(base)*0.2
            totalc=float(base)+float(fc)+float(seatc)+float(luggc)+float(avc)
            qry4=f"insert into cancellation values({a},{b},{base},{fc},{luggc},{seatc},{avc})"
            cr.execute(qry4)
            cc.commit()
            Label(window,text='FlightNo',font=("Calibri",12)).place(x=10,y=60)
            Label(window,text=a,font=("Calibri",12)).place(x=140,y=60)
            Label(window,text='Base Cost:',font=("Calibri",12)).place(x=10,y=90)
            Label(window,text=str(base),font=("Calibri",12)).place(x=140,y=90)
            Label(window,text='Food Cost:',font=("Calibri",12)).place(x=10,y=120)
            Label(window,text=str(fc),font=('Calibri',12)).place(x=140,y=120)
            Label(window,text='Seat Cost:',font=('Calibri',12)).place(x=10,y=150)
            Label(window,text=str(seatc),font=('Calibri',12)).place(x=140,y=150)
            Label(window,text='Luggage Cost',font=('Calibri',12)).place(x=10,y=180)
            Label(window,text=str(luggc),font=('Calibri',12)).place(x=140,y=180)
            Label(window,text='Availability Cost',font=('Calibri',12)).place(x=10,y=210)
            Label(window,text=str(avc),font=('Calibri',12)).place(x=140,y=210)
            Label(window,text='Total cost',font=('Calibri',12)).place(x=10,y=240)
            Label(window,text=str(totalc),font=('Calibri',12)).place(x=140,y=240)
    def show_flights(self,a,b):
        win3  = flightlist(self, a,b)

#Ticket Cancellation
class Cancel_Ticket(Toplevel):
    def __init__(self,parent):
        super().__init__(parent)    
        self.title("Flight Cancellation")
        self.geometry('400x200')
        fno2=StringVar()
        pid2=StringVar()
        Label(self,text='FlightNo',font=('Calibri',12)).place(x=10,y=30)
        Entry(self,width=30,textvariable=fno2).place(x=140,y=30)
        Label(self,text='Passenger ID',font=('Calibri',12)).place(x=10,y=60)
        Entry(self,width=30,textvariable=pid2).place(x=140,y=60)
        print("Cancellation policy:")
        print("If the ticket is cancelled more than 45 days in advance, entire amount is refundable")
        print("If the ticket is cancelled between 45 and 15 days in advance,20% of the base cost will be deducted")
        print("If the ticket is cancelled less than 15 days in advance, 35% of the base cost will be deducted")
        Button(self,text='Cancel ticket',command=lambda:self.cancel_tkt(fno2.get(),pid2.get())).place(x=130,y=90)
    def cancel_tkt(self,u,v):
        window2=Tk()
        window2.geometry('400x400')
        window2.title("Cancellation Bill")
        qry7=f"select basecost,foodcost,luggagecost,seatcost,availabilitycost from cancellation where flightno={u} and passengerid={v}"
        cr.execute(qry7)
        d7=cr.fetchall()
        if d7==[]:Label(window2,text='No such records exist',font=('Calibri',12)).place(x=10,y=40)
        else:
            tot=d7[0][0]+d7[0][1]+d7[0][2]+d7[0][3]+d7[0][4]
            Label(window2,text='Base Cost',font=('Calibri',12)).place(x=10,y=30)
            Label(window2,text=str(d7[0][0]),font=('Calibri',12)).place(x=140,y=30)
            Label(window2,text='Food Cost',font=('Calibri',12)).place(x=10,y=60)
            Label(window2,text=str(d7[0][1]),font=('Calibri',12)).place(x=140,y=60)
            Label(window2,text='Luggage Cost',font=('Calibri',12)).place(x=10,y=90)
            Label(window2,text=str(d7[0][2]),font=('Calibri',12)).place(x=140,y=90)
            Label(window2,text='Seat cost',font=('Calibri',12)).place(x=10,y=120)
            Label(window2,text=str(d7[0][3]),font=('Calibri',12)).place(x=140,y=120)
            Label(window2,text='Availability Cost',font=('Calibri',12)).place(x=10,y=150)
            Label(window2,text=str(d7[0][4]),font=('Calibri',12)).place(x=140,y=150)
            Label(window2,text='Amount Paid',font=('Calibri',12)).place(x=10,y=180)
            Label(window2,text=str(tot),font=('Calibri',12)).place(x=140,y=180)
            qry8="select sysdate()"
            cr.execute(qry8)
            currdate=str(cr.fetchall()[0][0])
            qry9=f"select datedepart from details where flightno={u}"
            cr.execute(qry9)
            datedep=str(cr.fetchall()[0][0])
            currdate1=date(int(currdate[0:4]),int(currdate[6]),int(currdate[8:10]))
            datedep1=date(int(datedep[0:4]),int(datedep[6]),int(datedep[8:10]))
            datdiff=datedep1-currdate1
            datdiff1=datdiff.days
            datdiff2=0
            qry11=f"Select basecost from details where flightno={u}"
            cr.execute(qry11)
            basese=cr.fetchall()[0][0]
            if datdiff1>45:datdiff2=0
            elif datdiff1<45 and datdiff1>15:datdiff2=float(basese)*0.2
            elif datdiff1<15:datdiff2=float(basese)*0.35
            refund=float(tot)-datdiff2
            Label(window2,text='Amount deduced',font=('Calibri',12)).place(x=10,y=210)
            Label(window2,text=str(datdiff2),font=('Calibri',12)).place(x=140,y=210)
            Label(window2,text='Amount refundable',font=('Calibri',12)).place(x=10,y=240)
            Label(window2,text=str(refund),font=('Calibri',12)).place(x=140,y=240)
            qry12=f"delete from passenger where flightno={u} and passengerid={v}"
            cr.execute(qry12)
            cc.commit()
            qry13=f"delete from cancellation where flightno={u} and passengerid={v}"
            cr.execute(qry13)
            cc.commit()
        
#Relevant flights
class flightlist(Toplevel):
    def __init__(self,parent,a,b):
        super().__init__(parent)
        self.geometry('1000x300')
        self.title('Available flights')
        columns=('FlightNo','Airline','From','To','DateDepart','DateArrival','TimeDep','TimeArrive','Duration','BaseCost')
        tree=ttk.Treeview(self,columns=columns,show='headings')
        tree.heading('FlightNo',text='FlightNo')
        tree.heading('Airline',text='Airline')
        tree.heading('From',text='From')
        tree.heading('To',text='To')
        tree.heading('DateDepart',text='DateDepart')
        tree.heading('DateArrival',text='DateArrival')
        tree.heading('TimeDep',text='TimeDep')
        tree.heading('TimeArrive',text='TimeArrive')
        tree.heading('Duration',text='Duration')
        tree.heading('BaseCost',text='BaseCost')
        tree.column('FlightNo',width=100)
        tree.column('Airline',width=100)
        tree.column('From',width=100)
        tree.column('To',width=100)
        tree.column('DateDepart',width=100)
        tree.column('DateArrival',width=100)
        tree.column('TimeDep',width=100)
        tree.column('TimeArrive',width=100)
        tree.column('Duration',width=100)
        tree.column('BaseCost',width=100)
        tree.grid(row=0,column=0)
        qry=f"Select * from details where Departure ='{b}' and Arrival='{a}';"
        cr.execute(qry)
        d=cr.fetchall()
        for x in d:
            tree.insert(parent='',index='end',values=x)
        tree.pack()

class View_Bill(Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.title('Enter details')
        self.geometry('500x300')
        pidd=StringVar()
        flnoo=StringVar()
        Label(self,text='Enter passenger ID',font=('Calibri',12)).place(x=10,y=30)
        Entry(self,width=30,textvariable=pidd).place(x=140,y=30)
        Label(self,text='Enter flight number',font=('Calibri',12)).place(x=10,y=60)
        Entry(self,width=30,textvariable=flnoo).place(x=140,y=60)
        Button(self,text='View bill',command=lambda:self.view_billl(pidd.get(),flnoo.get())).place(x=40,y=90)
    def view_billl(self,xx,yy):
        window7=Tk()
        window7.title('Bill')
        window7.geometry('500x300')
        qry15=f"select * from cancellation where passengerid={xx} and flightno={yy}"
        cr.execute(qry15)
        d9=cr.fetchall()
        if d9==[]:Label(window7,text='No such records exist',font=('Calibri',12)).place(x=10,y=40)
        else:
            total2=d9[0][2]+d9[0][3]+d9[0][4]+d9[0][5]+d9[0][6]
            Label(window7,text='FlightNo',font=("Calibri",12)).place(x=10,y=60)
            Label(window7,text=yy,font=("Calibri",12)).place(x=140,y=60)
            Label(window7,text='Base Cost:',font=("Calibri",12)).place(x=10,y=90)
            Label(window7,text=d9[0][2],font=("Calibri",12)).place(x=140,y=90)
            Label(window7,text='Food Cost:',font=("Calibri",12)).place(x=10,y=120)
            Label(window7,text=d9[0][3],font=('Calibri',12)).place(x=140,y=120)
            Label(window7,text='Seat Cost:',font=('Calibri',12)).place(x=10,y=150)
            Label(window7,text=d9[0][5],font=('Calibri',12)).place(x=140,y=150)
            Label(window7,text='Luggage Cost',font=('Calibri',12)).place(x=10,y=180)
            Label(window7,text=d9[0][4],font=('Calibri',12)).place(x=140,y=180)
            Label(window7,text='Availability Cost',font=('Calibri',12)).place(x=10,y=210)
            Label(window7,text=d9[0][6],font=('Calibri',12)).place(x=140,y=210)
            Label(window7,text='Total cost',font=('Calibri',12)).place(x=10,y=240)
            Label(window7,text=str(total2),font=('Calibri',12)).place(x=140,y=240)
            
App = main_scr()
App.mainloop()








               



