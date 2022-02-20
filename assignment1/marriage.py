
import readline
import sys

def get_data():
                 try:
        with open(sys.argv[1], 'r') as file:
            n=file.readline()
            num = int(n)
            maleranking = dict()
            femaleranking = dict()
            for i in range(num):
                line, *lines = file.readline().split()
                maleranking[line] = lines
            for i in range(num):
                line, *lines = file.readline().split()
                femaleranking[line] = lines

            lines = [line.split() for line in file]
            return num,maleranking, femaleranking
    except IndexError:
        exit(1)
    except ValueError:
        exit(1)
        

def getList(dict):
    list = []
    for key in dict.keys():
        list.append(key)
          
    return list

def make_dict(people):
    d = {}
    for i in people:
        d[i] = None
    return d

def match(n,malerankings,femalerankings):
    #Invariant: all bachelors are unmarried
    #All married couples are the best possible fit for each other of those that have also already been married
    #No lady has been proposed to by any individual knight more than once
    #These invariants hold throughout the loops as spouses are changed in a specific order.

    bachelors = getList(malerankings)
    bachelorettes = getList(femalerankings)
    current_wives = make_dict(bachelors)
    current_husbands = make_dict(bachelorettes)
    while bachelors:
        current_man = bachelors[0]
        current_m_preferences = malerankings[current_man]
        potential_fiance = current_m_preferences[0]
        current_f_preferences = femalerankings[potential_fiance]
        current_husband = current_husbands[potential_fiance]
        if current_husband == None:
            current_husbands[potential_fiance] = current_man
            current_wives[current_man] = potential_fiance
            malerankings[current_man] = malerankings[current_man][1:]
            bachelors.pop(0)
        else:
            current_ranking = current_f_preferences.index(current_husband)
            new_mans_ranking = current_f_preferences.index(current_man)
            if current_ranking > new_mans_ranking:
                current_wives[current_husband] = None
                current_husbands[potential_fiance] = current_man
                current_wives[current_man] = potential_fiance
                malerankings[current_man] = malerankings[current_man][1:]
                bachelors.pop(0)
                bachelors.insert(0,current_husband)
            else:
                malerankings[current_man] = malerankings[current_man][1:]
    return current_wives


def main():
    n, malerankings,femalerankings = get_data()
    wives = match(n,malerankings,femalerankings)
    for key,value in wives.items():
        print(key,value)


main()
