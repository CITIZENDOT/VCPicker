import json
try:
    import requests
except ModuleNotFoundError:
    print("requests Module Not Found")
    print("Installing it...")
    from os import system
    system("pip3 install requests")
    import requests
import random

"""
Section 1: Getting User Details     : Start
"""

print("Enter the number of users: ")
users_count = int(input())
user_list = []

for i in range(users_count):
    print("User " + str(i + 1) + ": ", end=' ')
    handle = input()
    if 3 <= len(handle) <= 24:
        user_list.append(handle)
    else:
        print("Handle should contain between 3 and 24 characters, inclusive")
        print("User Count reduced by one")

"""
Section 2: Getting Contest Details  : Start
"""

r = requests.get("https://codeforces.com/api/contest.list")
contests_info = json.loads(r.text)['result']
contests_Ids = [contest['id'] for contest in contests_info]
contest_Names = [contest['name'] for contest in contests_info]
contests = dict(zip(contests_Ids, contest_Names))
getId = dict(zip(contest_Names, contests_Ids))

"""
Section 3: Filtering Contests
"""

for user in user_list:
    r = requests.get("https://codeforces.com/api/user.status?handle=" + user)
    response = json.loads(r.text)
    if response['status'] != 'OK':
        print("\nIt seems like User: " + user + " doesn't exist.", "Continuing with remaining Users", sep='\n')
        continue
    subs = response['result']       # Submissions
    subs_ids = []                   # Contest Ids of Submissions
    for sub in subs:
        if 'contestId' not in sub.keys():
            continue
        subs_ids.append(sub['contestId'])
    for Id in subs_ids:
        if Id in contests.keys():
            del contests[Id]

"""
Section 4: Segregating into Div. 1, 2, 3
"""

div1 = []
div2 = []
div3 = []
contest_names = list(contests.values())
for contest in contest_names:
    if 'Div. 1' in contest:
        div1.append(contest)

    if 'Div. 2' in contest:
        div2.append(contest)        

    if 'Div. 3' in contest:
        div3.append(contest)

"""
Section 5: Final Result
"""

print(
    """
    Choose one of the below:
    0) Random
    1) Div. 1
    2) Div. 2
    3) Div. 3
    
    4) Print All Div. 1
    5) Print All Div. 2
    6) Print All Div. 3
    7) Show this Menu Again
    8) Exit
    """
    )
print("Choose your choice: ", end='')
choice = int(input())

while(True):
    if choice == 8:
        print("Bye")
        print("See you next time...")
        print("Wish you high rating")
        exit(0)
    
    elif choice == 7:
        print(
        """
        Choose one of the below:
        0) Random
        1) Div. 1
        2) Div. 2
        3) Div. 3
        
        4) Print All Div. 1
        5) Print All Div. 2
        6) Print All Div. 3
        7) Show this Menu Again
        8) Exit
        """
        )

    if(0 <= choice <= 3):
        if choice == 0:
            choice = random.randint(1, 3)

        if choice == 1:
            div = div1

        elif choice == 2:
            div = div2
        
        elif choice == 3:
            div = div3

        index = random.randint(0, len(div) - 1)
        name = div[index]
        Id = getId[name]
        url = "https://codeforces.com/contest/" + str(Id)
        print(
            "I am picking a Random Div. " + str(choice) + " Contest.",
            "\n" + name,
            "\nContest URL:\n" + url,
            "\n\nAll the Best",
            sep='\n'
        )
    elif 4 <= choice <= 6:
        choice -= 3
        if choice == 1:
            div = div1

        elif choice == 2:
            div = div2
        
        elif choice == 3:
            div = div3
        
        print("{:<60}".format("CONTEST"), " | ", "URL")
        print("-" * 90)
        for contest in div:
            print("{:<60}".format(contest), " | ", "https://codeforces.com/contest/" + str(getId[contest]), end='\n\n')
    print("Choose your choice: ", end='')
    choice = int(input())
