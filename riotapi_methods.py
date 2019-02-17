import cassiopeia as cass
from datetime import timedelta

cass.set_riot_api_key('RGAPI-34eb3716-5499-481a-a05c-1eeeabdd500b')
region = 'NA'

def gold_diff_for_jg_at_x_min(ign, reg=region, game_num=20, x=10):
    me = cass.get_summoner(region = reg, name = ign)
    matches = me.match_history(begin_index = 0, end_index = game_num)
    d = timedelta(minutes=x)
    
    gold_diff_list = []
    my_gold = 0
    enemy_gold = 0
    
    for match in matches:
        mee = match.participants[me]
        my_lane = mee.lane
        my_id = mee.id
        my_champ = mee.champion.name
        enemy = 0
        
        if mee.summoner_spell_d.name != "Smite" and mee.summoner_spell_f.name != "Smite":
            continue
        
        for p in match.participants:
            if (p.summoner_spell_d.name == "Smite" or p.summoner_spell_f.name == "Smite") and p.id is not my_id and p.team is not mee.team:
                enemy = p.summoner
                
        enemy_p = match.participants[enemy]
        enemy_ign = enemy.name
        enemy_id = enemy_p.id
        enemy_champ = enemy_p.champion.name
        
        timeline = match.timeline
        for frame in timeline.frames:
            if frame.timestamp >= d:
                my_gold = 0
                enemy_gold = 0
                my_gold = frame.participant_frames[my_id].gold_earned
                enemy_gold = frame.participant_frames[enemy_id].gold_earned
                gold_diff_list.append((my_lane, my_gold - enemy_gold, enemy_ign, my_champ, enemy_champ))
                break
    print(f'\nThe gold difference at {x}min between {ign} and enemy JUNGLER in the last {game_num} games:')
    print(''.join([f"  {b} gold difference at {a} playing {d} against {c}'s {e}\n" for a,b,c,d,e in gold_diff_list]))
    avg = sum([t[1] for t in gold_diff_list])/len(gold_diff_list)
    print(f"{ign}'s average GD at {x}min in the last {game_num} games is {avg}")

def gold_diff_at_x_min(ign, reg=region, game_num=20, x = 10):
    me = cass.get_summoner(region = reg, name = ign)
    matches = me.match_history(begin_index = 0, end_index = game_num)
    d = timedelta(minutes=x)
    
    gold_diff_list = []
    my_gold = 0
    enemy_gold = 0
    
    for match in matches:
        mee = match.participants[me]
        my_lane = mee.lane
        my_id = mee.id
        my_champ = mee.champion.name
        enemy = 0
        
        for p in match.participants:
            if p.lane is my_lane and p.id is not my_id and p.team is not mee.team:
                enemy = p.summoner
                
        enemy_p = match.participants[enemy]
        enemy_ign = enemy.name
        enemy_id = enemy_p.id
        enemy_champ = enemy_p.champion.name
        
        timeline = match.timeline
        for frame in timeline.frames:
            if frame.timestamp >= d:
                my_gold = 0
                enemy_gold = 0
                my_gold = frame.participant_frames[my_id].gold_earned
                enemy_gold = frame.participant_frames[enemy_id].gold_earned
                gold_diff_list.append((my_lane, my_gold - enemy_gold, enemy_ign, my_champ, enemy_champ))
                print(enemy_p.lane, enemy_p.champion.name)
                break
    print(f'\nThe gold difference at {x}min between {ign} and enemy laner in the last {game_num} games:')
    print(''.join([f"  {b} gold difference at {a} playing {d} against {c}'s {e}\n" for a,b,c,d,e in gold_diff_list]))
    avg = sum([t[1] for t in gold_diff_list])/len(gold_diff_list)
    print(f"{ign}'s average GD at {x}min in the last {game_num} games is {avg}")

def first_blood_stats(ign, reg=region, game_num=30):
    me = cass.get_summoner(region = reg, name = ign)
    matches = me.match_history(begin_index = 0, end_index = game_num)
    
    fb_and_win_list = []
    game_count = 0
    
    for match in matches:
        game_count += 1
        mee = match.participants[me]
        my_side = mee.side
        ally_first_blood = False
        i_got_fb = mee.stats.first_blood_kill
        i_got_fb_assist = mee.stats.first_blood_assist
        for team in match.teams:
            if team.first_blood:
                if my_side is team.side:
                    ally_first_blood = True
                break
        fb_and_win_list.append((ally_first_blood, mee.stats.win, i_got_fb, i_got_fb_assist))
    
        
    win_count = sum([1 for t in fb_and_win_list if t[1]])
    fb_count = sum([1 for t in fb_and_win_list if t[0]])
    fb_and_win = sum([1 for t in fb_and_win_list if t[0] and t[1]])
    #fb_and_lose = abs(fb_count - fb_and_win)
    not_fb_count = game_count - fb_count
    not_fb_and_win = sum([1 for t in fb_and_win_list if not t[0] and t[1]])
    #not_fb_and_lose = abs(not_fb_count - not_fb_and_win)
    my_fb_count = sum([1 for t in fb_and_win_list if t[2]])
    my_fb_ass_count = sum([1 for t in fb_and_win_list if t[3]])
    
    print(f"\nOut of {game_count} mathces for {ign}:")
    print(f'Won: {win_count} games --> {win_count/game_count *100}% win rate')
    print(f"    Ally first blood: {fb_count}")
    print(f'        Ally first blood percentage: {fb_count/game_count *100}%')
    print(f'            {ign} got {my_fb_count} first bloods --> {my_fb_count/game_count *100}% first blood rate')
    print(f"            {ign} got {my_fb_count/fb_count*100}% of team's first blood")
    print(f'            {ign} assisted in {my_fb_ass_count} first blood')
    print(f'    First blood and win: {fb_and_win}')
    print(f'        Won {fb_and_win/fb_count *100}% of the game your team got first blood.')
    print(f'    Not first blood and win: {not_fb_and_win}')
    print(f'        Won {not_fb_and_win/not_fb_count *100}% of the game enemy team got first blood.')

def avg_kda(ign, reg=region, game_num = 50):
    me = cass.get_summoner(region = reg, name = ign)
    matches = me.match_history(begin_index = 0, end_index = game_num)
    kda_list = []
    kill_list = []
    death_list = []
    assist_list = []
    for match in matches:
        mee = match.participants[me]
        kda_list.append(mee.stats.kda)
        kill_list.append(mee.stats.kills)
        death_list.append(mee.stats.deaths)
        assist_list.append(mee.stats.assists)
    print(f"\n{ign}'s average kda in the last {game_num} games is:")
    print(f"    {sum([k for k in kda_list])/len(kda_list)}")
    print(f"Total kills: {sum([k for k in kill_list])}    Avg kills: {sum([k for k in kill_list])/len(kill_list)}")
    print(f"Total deaths: {sum([k for k in death_list])}    Avg deaths: {sum([k for k in death_list])/len(death_list)}")
    print(f"Total assists: {sum([k for k in assist_list])}    Avg assists: {sum([k for k in assist_list])/len(assist_list)}")
    
def dragon_stats(ign, reg=region, game_num = 30):
    me = cass.get_summoner(region = reg, name = ign)
    matches = me.match_history(begin_index = 0, end_index = game_num)
    got_first_drag = []
    dragon_kills = []
    for match in matches:
        mee = match.participants[me]
        for team in match.teams:
            if team.side is mee.side:
                got_first_drag.append((team.first_dragon,team.win))
                dragon_kills.append(team.dragon_kills)
                break
    print(f"\n{ign}'s dragon stats in the last {game_num} games:")
    print(f"    Got first dragon {sum([1 for k in got_first_drag if k[0]])} times")
    print(f"        Won {sum([1 for k in got_first_drag if k[0] and k[1]])} of the times ally got first dragon")
    print(f"    Average dragon kills/game: {sum(k for k in dragon_kills)/len(dragon_kills)}")

def ward_stats(ign, reg=region, game_num = 30):
    me = cass.get_summoner(region = reg, name = ign)
    matches = me.match_history(begin_index = 0, end_index = game_num)
    my_wards = []
    teams_wards = []
    enemy_wards = []
    for match in matches:
        mee = match.participants[me]
        my_wards.append(mee.stats.wards_placed)
        for team in match.teams:
            if team.side is mee.side:
                teams_wards.append(sum([p.stats.wards_placed for p in team.participants]))
            else:
                enemy_wards.append(sum([p.stats.wards_placed for p in team.participants]))
    print(f"\n{ign}'s ward stats in the last {game_num} games:")
    print(f"    {ign} placed average of {sum([k for k in my_wards])/len(my_wards)} wards")
    print(f"    {ign}'s team placed average of {sum([k for k in teams_wards])/len(teams_wards)} wards")
    print(f"    Enemy team placed average of {sum([k for k in enemy_wards])/len(enemy_wards)} wards")

def simple_menu():
    ign = input("Enter a summoner name: ")
    print("\nFunction list: ")
    print("0. Gold difference for jungle at x minutes")
    print("1. Gold difference at x minutes")
    print("2. First blood stats")
    print("3. Average KDA")
    print("4. Dragon stats")
    print("5. Ward stats")
    while True:
        try:
            choice = int(input("Choose a function number: "))
            break
        except:
            print("a NUMBER")
    if choice == 0:
        gold_diff_for_jg_at_x_min(ign)
    elif choice == 1:
        gold_diff_at_x_min(ign)
    elif choice == 2:
        first_blood_stats(ign)
    elif choice == 3:
        avg_kda(ign)
    elif choice == 4:
        dragon_stats(ign)
    elif choice == 5:
        ward_stats(ign)

def normal_menu():
    ign = input("Enter a summoner name: ")
    print("\nFunction list: ")
    print("0. Gold difference for jungle at x minutes")
    print("1. Gold difference at x minutes")
    print("2. First blood stats")
    print("3. Average KDA")
    print("4. Dragon stats")
    print("5. Ward stats")
    while True:
        try:
            choice = int(input("Choose a function number: "))
            break
        except:
            print("a NUMBER")
    while True:
        game_num = input("How many games do you want to see (max 100): ")
        try:
            game_num = int(game_num)
            break
        except:
            print("Error")
    while choice in [0,1]:
        x = input("At what minutes do you want to check GD: ")
        try:
            x = int(x)
            break
        except:
            print("Error")
    if choice == 0: 
        gold_diff_for_jg_at_x_min(ign, game_num = game_num, x = x)
    elif choice == 1: 
        gold_diff_at_x_min(ign, game_num = game_num, x=x)
    elif choice == 2:
        first_blood_stats(ign, game_num = game_num)
    elif choice == 3:
        avg_kda(ign, game_num = game_num)
    elif choice == 4:
        dragon_stats(ign, game_num = game_num)
    elif choice == 5:
        ward_stats(ign, game_num = game_num)


        
        
            
        