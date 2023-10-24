squad_data = """
Afghanistan squad: Hashmatullah Shahidi (c), Rahmanullah Gurbaz, Ibrahim Zadran, Reyaz Hassan, Rahmat Shah Zurmati, Najibullah Zadran, Mohammad Nabi Eisakhil, Ikram Ali Khil, Azmatullah Omarzai, Rashid Khan Arman, Mujeeb ur Rahman, Noor Ahmad Lakanwal, Fazalhaq Farooqi, Abdul Rahman Rahmani, Naveen ul Haq Murid
Australia squad: Pat Cummins (c), Steve Smith, Alex Carey, Josh Inglis, Sean Abbott, Cameron Green, Josh Hazlewood, Travis Head, Marnus Labuschagne, Mitch Marsh, Glenn Maxwell, Marcus Stoinis, David Warner, Adam Zampa, Mitchell Starc
Bangladesh squad: Shakib Al Hasan (c), Litton Kumer Das, Tanzid Hasan Tamim, Najmul Hossain Shanto (vc), Tawhid Hridoy, Mushfiqur Rahim, Mahmudullah Riyad, Mehidy Hasan Miraz, Nasum Ahmed, Shak Mahedi Hasan, Taskin Ahmed, Mustafizur Rahman, Hasan Mahmud, Shoriful Islam, Tanzim Hasan Sakib
England squad: Jos Buttler (c), Moeen Ali, Gus Atkinson, Jonny Bairstow, Harry Brook, Sam Curran, Liam Livingstone, Dawid Malan, Adil Rashid, Joe Root, Ben Stokes, Reece Topley, David Willey, Mark Wood, Chris Woakes
India squad: Rohit Sharma (c), Hardik Pandya (vc), Shubman Gill, Virat Kohli, Shreyas Iyer, KL Rahul, Ravindra Jadeja, Ravichandran Ashwin, Shardul Thakur, Jasprit Bumrah, Mohammed Siraj, Kuldeep Yadav, Mohammed Shami, Ishan Kishan, Surya Kumar Yadav
Netherlands squad: Scott Edwards (c), Max O'Dowd, Bas de Leede, Vikram Singh, Teja Nidamanuru, Paul van Meekeren, Colin Ackermann, Roelof van der Merwe, Logan van Beek, Aryan Dutt, Ryan Klein, Wesley Barresi, Saqib Zulfiqar, Shariz Ahmad, Sybrand Engelbrecht
New Zealand squad: Kane Williamson (c), Trent Boult, Mark Chapman, Devon Conway, Lockie Ferguson, Matt Henry, Tom Latham, Daryl Mitchell, Jimmy Neesham, Glenn Phillips, Rachin Ravindra, Mitch Santner, Ish Sodhi, Tim Southee, Will Young
Pakistan squad: Babar Azam (c), Shadab Khan, Fakhar Zaman, Imam-ul-Haq, Abdullah Shafique, Mohammad Rizwan, Saud Shakeel, Iftikhar Ahmed, Salman Ali Agha, Mohammad Nawaz, Usama Mir, Haris Rauf, Hasan Ali, Shaheen Afridi, Mohammad Wasim
South Africa squad: Temba Bavuma (c), Gerald Coetzee, Quinton de Kock, Reeza Hendricks, Marco Jansen, Heinrich Klaasen, Andile Phehlukwayo, Keshav Maharaj, Aiden Markram, David Miller, Lungi Ngidi, Kagiso Rabada, Tabraiz Shamsi, Rassie van der Dussen, Lizaad Williams
Sri Lanka squad: Dasun Shanaka (c), Kusal Mendis (vc), Kusal Perera, Pathum Nissanka, Dimuth Karunaratne, Sadeera Samarawickrama, Charith Asalanka, Dhananjaya de Silva, Dushan Hemantha, Maheesh Theekshana, Dunith Wellalage, Kasun Rajitha, Matheesha Pathirana, Lahiru Kumara, Dilshan Madushanka
"""

team_data = {}

squad_data = squad_data.split('\n')
squad_data = [line for line in squad_data if line != '']

for line in squad_data:
    team_name = line.split('squad:')[0].strip()
    team_data[team_name] = []

    players = line.split('squad:')[1].strip().split(', ')
    for player in players:
        player = player.split('(')[0].strip()
        team_data[team_name].append(player)
    
# Write to csv file
with open('gathering_data/player_names.csv', 'w') as f:
    f.write('team_name,player_name\n')
    for team_name in team_data:
        for player in team_data[team_name]:
            f.write(f'{team_name},{player}\n')


