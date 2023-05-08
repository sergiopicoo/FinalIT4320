def get_seating():
    with open('reservations.txt', 'r') as seatf:
        flight = []
        for x in range(1, 13):
            flight_row = ['O', 'O', 'O', 'O']
            flight.append(flight_row)

        line = seatf.readline()
        while line:
            line = line.strip() 
            line = line.split(', ')
            row = int(line[1])
            seat = int(line[2])
            flight[row][seat] = 'X'

            line = seatf.readline()
        return flight

def get_ticket(first_name):
    ITclass = "INFOTC4320"
    ITclass_length = len(ITclass)
    firstnamelength = len(first_name)
    if firstnamelength > ITclass_length:
       # firststr = ITclass
        longername = first_name
    else:
       # firststr = first_name
        longername = ITclass

    tickets = []

    for count in range(len(first_name)):
        tickets.append(first_name[count])
        tickets.append(ITclass[count])

    if len(longername) > len(first_name):
        for count in range(len(first_name), len(longername)):
            if longername == ITclass:
                tickets.append(ITclass[count])
            elif longername == first_name:
                tickets.append(first_name[count])
            count += 1
        
    ticket = ''.join(tickets)

    return ticket