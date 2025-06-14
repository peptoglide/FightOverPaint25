import random
import math
from enum import Enum
#Hello world guys lol

from battlecode25.stubs import *

# This is NOT an example bot written by the developers!
# DON'T use this to help write your own code.
# Please only run it against your bot to see how well you can do!

class MessageType(Enum):
    SAVE_CHIPS = 0

# Globals
turn_count = 0
directions = [
    Direction.NORTH,
    Direction.NORTHEAST,
    Direction.EAST,
    Direction.SOUTHEAST,
    Direction.SOUTH,
    Direction.SOUTHWEST,
    Direction.WEST,
    Direction.NORTHWEST,
]
direction_indices = {
    Direction.NORTH : 0,
    Direction.NORTHEAST : 1,
    Direction.EAST : 2,
    Direction.SOUTHEAST : 3,
    Direction.SOUTH : 4,
    Direction.SOUTHWEST : 5,
    Direction.WEST : 6,
    Direction.NORTHWEST : 7,
}

# Pathfinding
prev_dest = MapLocation(100000, 100000)
line = set()
obstacle_start_dist = 0
tracing_dir = None
tracing = False

def sign(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    return 0

def get_direction_to(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    return (sign(dx), sign(dy))

def create_line(a, b):
    locations = set()
    x, y = a.x, a.y
    dx = b.x - a.x
    dy = b.y - a.y
    sx = int(sign(dx))
    sy = int(sign(dy))
    dx = abs(dx)
    dy = abs(dy)
    d = d = dx if dx > dy else dy
    r = d // 2

    if dx > dy:
        for i in range(d):
            locations.add(MapLocation(x, y))
            x += sx
            r += dy
            if r >= dx:
                locations.add(MapLocation(x, y))
                y += sy
                r -= dx
    else:
        for i in range(d):
            locations.add(MapLocation(x, y))
            y += sy
            r += dx
            if r >= dy:
                locations.add(MapLocation(x, y))
                x += sx
                r -= dy

    locations.add(MapLocation(x, y))
    return locations
# well played gg guys
def bug2(target):
    global prev_dest, line, tracing, obstacle_start_dist, tracing_dir

    if get_location() == target:
        return

    if target.compare_to(prev_dest) != 0:
        prev_dest = target
        line = create_line(get_location(), target)

    if not tracing:
        dir = Direction(get_direction_to(get_location(), target))

        if can_move(dir):
            move(dir)
        else:
            tracing = True
            obstacle_start_dist = get_location().distance_squared_to(target)
            tracing_dir = dir
    else:
        if (get_location() in line 
                and get_location().distance_squared_to(target) < obstacle_start_dist):
            tracing = False
            return

        for i in range(9):
            if can_move(tracing_dir):
                move(tracing_dir)
                tracing_dir = tracing_dir.rotate_right()
                tracing_dir = tracing_dir.rotate_right()
                break
            else:
                tracing_dir = tracing_dir.rotate_left()

# Should add up to 100
buildable_towers = [UnitType.LEVEL_ONE_MONEY_TOWER, UnitType.LEVEL_ONE_PAINT_TOWER, UnitType.LEVEL_ONE_DEFENSE_TOWER]
bot_chance = {UnitType.SOLDIER : 40, UnitType.MOPPER : 25, UnitType.SPLASHER : 35}
tower_chance = {UnitType.LEVEL_ONE_MONEY_TOWER : 65, UnitType.LEVEL_ONE_PAINT_TOWER : 25, UnitType.LEVEL_ONE_DEFENSE_TOWER : 10}
bot_name = {UnitType.SOLDIER : "SOLDIER", UnitType.MOPPER : "MOPPER", UnitType.SPLASHER : "SPLASHER"}
paint_capacity = {UnitType.SOLDIER : 200, UnitType.MOPPER : 100, UnitType.SPLASHER : 300}
direction_distribution = {
    Direction.NORTH : None,
    Direction.NORTHEAST: None,
    Direction.EAST: None,
    Direction.SOUTHEAST: None,
    Direction.SOUTH: None,
    Direction.SOUTHWEST: None,
    Direction.WEST: None,
    Direction.NORTHWEST: None,
}

CORRECT = 23
SEMICORRECT = 17
NEUTRAL = 13
SEMIWRONG = 7
WRONG = 3

LEFT = {
    Direction.NORTH : NEUTRAL,
    Direction.NORTHEAST: SEMIWRONG,
    Direction.EAST: WRONG,
    Direction.SOUTHEAST: SEMIWRONG,
    Direction.SOUTH: NEUTRAL,
    Direction.SOUTHWEST: SEMICORRECT,
    Direction.WEST: CORRECT,
    Direction.NORTHWEST: SEMICORRECT,
}

RIGHT = {
    Direction.NORTH : NEUTRAL,
    Direction.NORTHEAST: SEMICORRECT,
    Direction.EAST: CORRECT,
    Direction.SOUTHEAST: SEMICORRECT,
    Direction.SOUTH: NEUTRAL,
    Direction.SOUTHWEST: SEMIWRONG,
    Direction.WEST: WRONG,
    Direction.NORTHWEST: SEMIWRONG,
}

DOWN = {
    Direction.NORTH : WRONG,
    Direction.NORTHEAST: SEMIWRONG,
    Direction.EAST: NEUTRAL,
    Direction.SOUTHEAST: SEMICORRECT,
    Direction.SOUTH: CORRECT,
    Direction.SOUTHWEST: SEMICORRECT,
    Direction.WEST: NEUTRAL,
    Direction.NORTHWEST: SEMIWRONG,
}

UP = {
    Direction.NORTH : CORRECT,
    Direction.NORTHEAST: SEMICORRECT,
    Direction.EAST: NEUTRAL,
    Direction.SOUTHEAST: SEMIWRONG,
    Direction.SOUTH: WRONG,
    Direction.SOUTHWEST: SEMIWRONG,
    Direction.WEST: NEUTRAL,
    Direction.NORTHWEST: SEMICORRECT,
}

UNIFORM = {
    Direction.NORTH : NEUTRAL,
    Direction.NORTHEAST: NEUTRAL+1,
    Direction.EAST: NEUTRAL,
    Direction.SOUTHEAST: NEUTRAL+1,
    Direction.SOUTH: NEUTRAL,
    Direction.SOUTHWEST: NEUTRAL+1,
    Direction.WEST: NEUTRAL,
    Direction.NORTHWEST: NEUTRAL+1,
}

def update_bot_chance(soldier, mopper, splasher):
    global bot_chance
    bot_chance[UnitType.SOLDIER] = soldier
    bot_chance[UnitType.MOPPER] = mopper
    bot_chance[UnitType.SPLASHER] = splasher

def update_tower_chance(money, paint, defense):
    global tower_chance
    tower_chance[UnitType.LEVEL_ONE_MONEY_TOWER] = money
    tower_chance[UnitType.LEVEL_ONE_PAINT_TOWER] = paint
    tower_chance[UnitType.LEVEL_ONE_DEFENSE_TOWER] = defense

factor = 2
def update_direction_distribution():
    global direction_distribution
    cur_loc = get_location()
    left = cur_loc.x
    right = get_map_width() - left - 1
    down = cur_loc.y
    up = get_map_height() - down - 1
    left = left ** factor
    right = right ** factor
    up = up ** factor
    down = down ** factor
    total = left+right+down+up
    left = int(left/total*50)
    right = int(right/total*50)
    down = int(down/total*50)
    up = int(up/total*50)
    total = left+right+down+up
    leftover = 50-total
    if left > right: left += leftover
    else: right += leftover
    ul = (up + left)//2
    ur = (up + right)//2
    dl = (down + left)//2
    dr = (down + right)//2
    total = ul + ur + dl + dr
    leftover = 50 - total
    if left > right:
        if up > down:
            ul += leftover
        else:
            dl += leftover
    else:
        if up > down:
            ur += leftover
        else:
            dr += leftover
    direction_distribution[Direction.NORTH] = up
    direction_distribution[Direction.NORTHEAST] = ur
    direction_distribution[Direction.EAST] = right
    direction_distribution[Direction.SOUTHEAST] = dr
    direction_distribution[Direction.SOUTH] = down
    direction_distribution[Direction.SOUTHWEST] = dl
    direction_distribution[Direction.WEST] = left
    direction_distribution[Direction.NORTHWEST] = ul

def update_direction_distribution_2():
    global direction_distribution
    cur_loc = get_location()
    left = cur_loc.x
    right = get_map_width() - left - 1
    down = cur_loc.y
    up = get_map_height() - down - 1
    left = left ** factor
    right = right ** factor
    up = up ** factor
    down = down ** factor
    if left <= 5: left = 0
    if right <= 5: right = 0
    if down <= 5: down = 0
    if up <= 5: up = 0
    total = left + right + up + down
    temp = random.randint(1, total)
    if temp <= left:
        direction_distribution = LEFT
    elif temp <= left + right:
        direction_distribution = RIGHT
    elif temp <= left + right + down:
        direction_distribution = DOWN
    else:
        direction_distribution = UP

def get_random_dir():
    n = random.randint(1, 100)
    for (direction, prob) in direction_distribution.items():
        if n <= prob: return direction
        n -= prob

def get_random_unit(probabilities):
    n = random.randint(1, 100)
    for (unit, prob) in probabilities.items():
        if n <= prob: return unit
        n -= prob

# Determine build delays between each bot spawned by a tower
buildDelay = 15 # Tune
buildDeviation = 3

# When we're trying to build, how long should we save
save_turns = 45 # Tune

# How many turns after does a messenger repeats its tasks
messenger_work_distribution = 25

# How many turns after does a soldier senses towers
sense_tower_delay = 1

# Threshold for returning to ruin (splashers)
return_to_paint = {UnitType.SOLDIER : 0, UnitType.MOPPER : 0, UnitType.SPLASHER : 25}
back_to_aggresion = {UnitType.SOLDIER : 75, UnitType.MOPPER : 75, UnitType.SPLASHER : 85}
# Random constant walk chance
const_walk_chance = {UnitType.SOLDIER : 0, UnitType.MOPPER : 0, UnitType.SPLASHER : 0}
# Paint per transfer
paint_per_transfer = 50
# Min splashable squares to attack
splash_threshold = 5
# Duration of starting turns we don't paint
non_painting_turns = 25
# Starting point and max boost of build speed of paint towers
fast_build_paint_percentage = 50
fast_build_max_speed = 2 # Linear 
# Starting turns we spawn ASAP
frenzy_turns = 25
# Time till we change direction again
change_dir_delay = 12
change_dir_dev = 2
# This determines the area percentage of the circle where we build defense towers
defense_area_percentage = 0.08
# Time for each money tower before disintegrating
money_tower_existence = 50
# Chips to immediately disintegrate
flicker_chips_threshold = 2000

# Privates
buildCooldown = 0
is_messenger = False # We designate half of moppers to be messangers
known_towers = []
known_paint_towers = []
should_save = False
savingTurns = 0
updated = 0
early_game = 200
mid_game = 800
tower_upgrade_minimum = 8000
closest_paint_tower = None
is_refilling = False
paintingSRP = False
tower_upgrade_threshold = 1
next_spawn = UnitType.SOLDIER
cur_tile = None
is_early_game = False
is_mid_game = False
is_late_game = False
nearby_tiles = []
const_dir = None
is_const_walk = False
is_frenzy = True
non_painting = non_painting_turns
time_till_next_dir = 0
defense_radius_squared = 0
game_area = 0
is_starting_tower = -1 # -1 means unset. 0 means False and 1 means True
active_turns = 0 # Turns this unit has existed
center_loc = None
SRP = get_resource_pattern()
PAINT_PATTERN = get_tower_pattern(UnitType.LEVEL_ONE_PAINT_TOWER)
MONEY_PATTERN = get_tower_pattern(UnitType.LEVEL_ONE_MONEY_TOWER)
DEFENSE_PATTERN = get_tower_pattern(UnitType.LEVEL_ONE_DEFENSE_TOWER)
size_state = 0 # 0 small, 1 med, 2 big

def can_repeat_cooldowned_action(time_delay):
    return (get_id() % time_delay == turn_count % time_delay)

def turn():
    """
    MUST be defined for robot to run
    This function will be called at the beginning of every turn and should contain the bulk of your robot commands
    """
    global turn_count
    global is_messenger
    global updated
    global direction_distribution
    global buildDelay
    global is_early_game, is_mid_game, is_late_game
    global non_painting_turns
    global non_painting
    global is_const_walk
    global is_frenzy
    global time_till_next_dir
    global game_area
    global defense_radius_squared
    global center_loc

    # HOW DID NO ONE REALIZE TURN COUNT IS NOT COUNTING FROM THE START
    turn_count = get_round_num()
    if turn_count > frenzy_turns:
        is_frenzy = False

    game_area = get_map_width() * get_map_height()
    defense_radius_squared = game_area * defense_area_percentage / 3.14159
    center_loc = MapLocation(math.floor((get_map_width() + 1) / 2), math.floor((get_map_height() + 1) / 2))

    thisisavariableforchoosingmethodofrandomwalking = random.randint(1, 100)
    if direction_distribution[Direction.NORTH] == None:
        if thisisavariableforchoosingmethodofrandomwalking <= 35:
            update_direction_distribution_2()
        elif thisisavariableforchoosingmethodofrandomwalking <= 95:
            update_direction_distribution()
        else:
            direction_distribution = UNIFORM

    # Prioritize chips in early game
    # Seems like chips are a bit too popular
    if turn_count >= 0 and updated == 0:
        update_phases()
        is_early_game = True
        is_mid_game = False
        is_late_game = False
        update_tower_chance(60, 40, 0)
        if size_state == 0:
            update_bot_chance(60, 5, 35)
        elif size_state == 1:
            update_bot_chance(70, 3, 27)
        else:
            update_bot_chance(80, 1, 19)
        updated = 1
        buildDelay = 14
    if turn_count >= early_game and updated == 1:
        is_early_game = False
        is_mid_game = True
        is_late_game = False
        update_tower_chance(55, 45, 0)
        if size_state == 0:
            update_bot_chance(35, 8, 57)
        elif size_state == 1:
            update_bot_chance(40, 5, 55)
        else:
            update_bot_chance(50, 3, 47)
        updated = 2
        buildDelay = 15
    if turn_count >= mid_game and updated == 2:
        is_early_game = False
        is_mid_game = False
        is_late_game = True
        
        update_tower_chance(50, 50, 0)
        if size_state == 0:
            update_bot_chance(25, 10, 65)
        elif size_state == 1:
            update_bot_chance(30, 6, 64)
        else:
            update_bot_chance(35, 4, 61)
        updated = 3


    if not get_type().is_tower_type():
        if updated == 0 and random.randint(1, 100) < const_walk_chance[get_type()]:
            is_const_walk = True
        if get_paint() == 0:
            disintegrate() # WASTING TOO MUCH RESOURCES

    if get_type() == UnitType.SOLDIER:
        if get_paint() < 5:
            disintegrate() # WASTING TOO MUCH RESOURCES
        run_soldier()
    elif get_type() == UnitType.MOPPER:
        if get_id() % 2 == 0: is_messenger = True
        run_mopper()
    elif get_type() == UnitType.SPLASHER:
        run_splasher()
    elif get_type().is_tower_type():
        run_tower()
    else:
        pass  # Other robot types?

    non_painting = non_painting_turns - turn_count
    time_till_next_dir -= 1

def update_phases():
    global early_game
    global non_painting_turns
    global mid_game
    global size_state
    global frenzy_turns
    game_area = get_map_height() * get_map_width()
    if game_area >= 400 and game_area < 900: 
        early_game = 85
        mid_game = 500
        non_painting_turns = 30
        frenzy_turns = 5
        size_state = 0
    elif game_area < 2000: 
        early_game = 115
        mid_game = 675
        non_painting_turns = 55
        frenzy_turns = 5
        size_state = 1
    else:
        early_game = 150
        mid_game = 850
        non_painting_turns = 85
        frenzy_turns = 5
        size_state = 2

def next_tower(cur_ruin: MapInfo):
    return UnitType.LEVEL_ONE_MONEY_TOWER

# Get paint color at current location. Will return -1 if already correct / out of ruin range. 0 if primary and 1 if secondary
def get_pattern_at_tile(tower_type, cur_ruin, cur_tile):
    tower_patterns = {UnitType.LEVEL_ONE_PAINT_TOWER: PAINT_PATTERN, UnitType.LEVEL_ONE_MONEY_TOWER: MONEY_PATTERN, UnitType.LEVEL_ONE_DEFENSE_TOWER: DEFENSE_PATTERN}
    if cur_tile.has_ruin(): return -1
    paint_of_tile = cur_tile.get_paint()
    if paint_of_tile.is_enemy(): return -1 # Skip if enemy paint

    ruin_loc = cur_ruin.get_map_location()
    tile_loc = cur_tile.get_map_location()
    dst = ruin_loc.distance_squared_to(tile_loc)
    if dst > 8: return -1 # If out of range
    # Get indices of rows and columns
    row = 2 + tile_loc.x - ruin_loc.x
    col = 2 - tile_loc.y + ruin_loc.y
    pattern_at_tile = tower_patterns[tower_type][row][col]
    if (pattern_at_tile == (paint_of_tile == PaintType.ALLY_SECONDARY)) and paint_of_tile != PaintType.EMPTY: # If ally paint
        return -1
    else:
        # Return correct paint
        if pattern_at_tile: return 1
        else: return 0

def lerp(a, b, t):
    # Linear interpolation
    return (1 - t) * a + t * b

def run_tower():
    global buildCooldown
    global savingTurns
    global should_save
    global next_spawn
    global buildDelay
    global is_starting_tower
    global nearby_tiles
    global active_turns
    global buildDeviation

    progress = 1
    
    if is_starting_tower == -1:
        if turn_count <= 3:
            is_starting_tower = True
        else: is_starting_tower = False
    
    # Pick a direction to build in.
    dir = get_random_dir()
    
    loc = get_location()
    next_loc = loc.add(dir)
    nearby_robots = sense_nearby_robots(center=loc)
    nearby_tiles = sense_nearby_map_infos(center=loc, radius_squared=8)
    if True:
        buildDelay = 0
        buildDeviation = 0

    # Ability for towers to attack
    if(is_action_ready() and len(nearby_robots) != 0):
        # Pick a random target to attack
        for random_enemy in nearby_robots:
            if random_enemy.get_team() == get_team(): continue
            loc2 = random_enemy.get_location()
            if can_attack(random_enemy.get_location()):
                attack(loc2)
                break

    # Pick a random robot type to build.
    # Should hold off on building since we're gonna end up with all moppers!
    if savingTurns <= 0:
        should_save = False
        if is_frenzy or buildCooldown <= 0: 
            robot_type = next_spawn
            
            if get_type().get_base_type() != UnitType.LEVEL_ONE_PAINT_TOWER and paint_capacity[robot_type] > get_paint():
                next_spawn = get_random_unit(bot_chance)
            if get_paint() >= 200 and get_paint() < 300:
                robot_type = UnitType.SOLDIER
            # Test every building direction
            if can_build_robot(robot_type, next_loc):
                build_robot(robot_type, next_loc)
                next_spawn = get_random_unit(bot_chance)
                buildCooldown = buildDelay + random.randint(-buildDeviation, buildDeviation)
                log("BUILT A " + bot_name[robot_type])

    if (get_paint() <= 100) and (not is_starting_tower and (get_chips() >= flicker_chips_threshold or active_turns >= money_tower_existence)):
        if can_complete_tower(loc, nearby_robots): disintegrate()

    if buildCooldown > 0: buildCooldown -= progress
    if savingTurns > 0: 
        savingTurns -= 1
        log("Saving for " + str(savingTurns) + " more turns")

    # Read incoming messages
    messages = read_messages()
    for m in messages:
        log(f"Tower received message: '#{m.get_sender_id()}: {m.get_bytes()}'")

        # If we are not currently saving and we receive the save chips message, start saving
        if not should_save and m.get_bytes() == 0:
            if can_broadcast_message():
                broadcast_message(0) # Let other towers know we're saving up for a tower
            savingTurns = save_turns
            should_save = True

    active_turns += 1
    
    # TODO: can we attack other bots?

def can_complete_tower(loc: MapLocation, nearby_robots):
    tower_patterns = {UnitType.LEVEL_ONE_PAINT_TOWER: PAINT_PATTERN, UnitType.LEVEL_ONE_MONEY_TOWER: MONEY_PATTERN, UnitType.LEVEL_ONE_DEFENSE_TOWER: DEFENSE_PATTERN}
    tower_type = get_type().get_base_type()

    # Check for correctness, allies and enemy paint
    correct = 0 # Tower is complete if correct = 24
    for tile in nearby_tiles:
        if tile.has_ruin(): continue
        tile_paint = tile.get_paint()

        if tile_paint.is_enemy(): # Immediately can't complete if there's enemy paint
            return False

        tile_loc = tile.get_map_location()
        row = 2 + tile_loc.x - loc.x
        col = 2 - tile_loc.y + loc.y
        pattern_at_tile = tower_patterns[tower_type][row][col]
        if tile_paint != PaintType.EMPTY and ((tile_paint == PaintType.ALLY_SECONDARY) == pattern_at_tile):
            correct += 1

    has_soldier = False
    has_other_robots = False
    for robot in nearby_robots:
        if robot.get_team() != get_team(): continue
        if robot.get_type() == UnitType.SOLDIER: has_soldier = True
        else: has_other_robots = True

    if has_soldier:
        return True # Soldiers can recomplete tower
    if has_other_robots and correct == 24:
        #return True # Rely on other robots to activate the tower
        pass
    return False

def run_soldier():
    # Soldiers hold 200 paint
    paint_percentage = get_paint() / 2
    if len(known_paint_towers) == 0: run_aggresive_soldier()
    else:
        if not is_refilling and paint_percentage > return_to_paint[UnitType.SOLDIER]:
            run_aggresive_soldier()
        else:
            try_refill_paint(paint_percentage, UnitType.SOLDIER)

def run_aggresive_soldier():
    global paintingSRP
    global nearby_tiles
    global const_dir
    global known_paint_towers
    global time_till_next_dir

    loc = get_location()

    # Sense information about all visible nearby tiles.
    nearby_tiles = sense_nearby_map_infos(center=loc)
    nearby_ruins = [] # Stores positions of unfinished ruins

    cur_ruin = None
    dir = None
    cur_dist = 999999
    cur_dir = None
    cur_dist2 = 999999
    dir_paint_count = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
    for tile in nearby_tiles:
        tile_loc = tile.get_map_location()
        if can_complete_resource_pattern(tile_loc):
            complete_resource_pattern(tile_loc)
        if tile.has_ruin():
            nearby_ruins.append(tile_loc)
            ruin = sense_robot_at_location(tile_loc)
            if ruin != None and ruin.get_team() != get_team(): # If enemy tower, attack
                if can_attack(tile_loc):
                    attack(tile_loc)
                    dir = Direction.opposite(loc.direction_to(tile_loc))
                else:
                    dir = loc.direction_to(tile_loc)
                if not can_move(dir): continue
                if can_attack(tile_loc):
                    attack(tile_loc)
                dst = loc.distance_squared_to(tile_loc)
                idx = direction_indices[dir]
                dir_paint_count[idx] = dir_paint_count[idx] + 100
            elif ruin == None: # If not enemy tower, try to complete
                
                check_dist = tile_loc.distance_squared_to(loc)

                if check_dist < cur_dist:
                    cur_dist = check_dist
                    cur_ruin = tile
        elif not tile.is_wall() and tile.get_paint() == PaintType.EMPTY: # Movement priority
            dir = loc.direction_to(tile_loc)
            if not can_move(dir): continue
            dst = loc.distance_squared_to(tile_loc)
            idx = direction_indices[dir]
            dir_paint_count[idx] = dir_paint_count[idx] + 1/dst/dst/dst/dst
            dst = loc.distance_squared_to(tile_loc)
            if can_move(dir) and dst < cur_dist2:
                cur_dist2 = dst
                cur_dir = dir
    update_paint_towers()

    if cur_ruin != None:
        target_loc = cur_ruin.get_map_location()
        has_enemy_paint = False
        has_ally_paint = False
        for tile2 in nearby_tiles:
            tile2_loc = tile2.get_map_location()
            if tile2.get_paint().is_enemy() and cur_ruin.get_map_location().distance_squared_to(tile2.get_map_location()) <= 8: 
                has_enemy_paint = True
            if tile2.get_paint().is_ally() and cur_ruin.get_map_location().distance_squared_to(tile2.get_map_location()) <= 8: 
                has_ally_paint = True
        if has_enemy_paint and has_ally_paint: cur_ruin = None # If can't complete, impede the progress of the opponent team

        if cur_ruin != None:
            tower_type = next_tower(cur_ruin)
            if True:
                # Should circle around tower to be able to paint all tiles
                # Complete the ruin if we can.
                if can_complete_tower_pattern(tower_type, target_loc):
                    complete_tower_pattern(tower_type, target_loc)
                    # Maybe try to remove mark
                    set_timeline_marker("Tower built", 0, 255, 0)
                    log("Built a tower at " + str(target_loc) + "!")
                    cur_ruin = None
                if cur_ruin != None:
                    dir = loc.direction_to(target_loc)
                    # Circling
                    if can_move(dir):
                        move(dir)
                    else:
                        # Circle to be able to color every tile
                        if dir == Direction.SOUTH: dir = Direction.SOUTHEAST
                        elif dir == Direction.EAST: dir = Direction.NORTHEAST
                        elif dir == Direction.NORTH: dir = Direction.NORTHWEST
                        elif dir == Direction.WEST: dir = Direction.SOUTHWEST
                        elif dir == Direction.SOUTHEAST: dir = Direction.EAST
                        elif dir == Direction.NORTHEAST: dir = Direction.NORTH
                        elif dir == Direction.NORTHWEST: dir = Direction.WEST
                        elif dir == Direction.SOUTHWEST: dir = Direction.SOUTH
                        if can_move(dir):
                            move(dir)

                    # Mark the pattern we need to draw to build a tower here if we haven't already.
                    target_loc = cur_ruin.get_map_location()
                    # should_mark = target_loc.subtract(dir)
                    # if can_sense_location(should_mark):
                    #     if sense_map_info(should_mark).get_mark() == PaintType.EMPTY and can_mark_tower_pattern(tower_type, target_loc):
                    #         mark_tower_pattern(tower_type, target_loc)
                    #         log("Trying to build a tower at " + str(target_loc))

                    # Try to paint without marking
                    if is_action_ready():
                        for tile in nearby_tiles:
                            if not can_attack(tile.get_map_location()): continue
                            pattern = get_pattern_at_tile(tower_type, cur_ruin, tile)
                            if pattern == -1: continue
                            attack(tile.get_map_location(), pattern)

                    # Fill in any spots in the pattern with the appropriate paint.
                    # TODO: paint with putting minimal marks
                    # paint_nearby_marks()


    # Fill in any spots in the pattern with the appropriate paint.
    paint_nearby_marks()
    

    # Upgrade towers
    if can_repeat_cooldowned_action(sense_tower_delay):
        try_to_upgrade_towers()

    # Make sure we go to empty square
    # While exploring, move in one direction till impossible
    if non_painting > 0 or is_const_walk:
        if const_dir == None:
            const_dir = get_random_dir()
        if not can_move(const_dir):
            const_dir = get_random_dir()
        if can_move(const_dir):
            move(const_dir)
    else:
        if const_dir == None:
            optimal_dir = -1
            optimal = 0
            for (test_dir, paint_count) in dir_paint_count.items():
                if paint_count > optimal:
                    optimal = paint_count
                    optimal_dir = test_dir
            if optimal_dir != -1:
                const_dir = directions[optimal_dir]
                time_till_next_dir = change_dir_delay + random.randint(-change_dir_dev, change_dir_dev)
        elif time_till_next_dir <= 0:
            optimal_dir = -1
            optimal = 0
            for (test_dir, paint_count) in dir_paint_count.items():
                if paint_count > optimal:
                    optimal = paint_count
                    optimal_dir = test_dir
            if optimal_dir != -1:
                const_dir = directions[optimal_dir]
                time_till_next_dir = change_dir_delay + random.randint(-change_dir_dev, change_dir_dev)
        if const_dir == None:
            const_dir = get_random_dir()
        if const_dir != None:
            if can_move(const_dir):
                move(const_dir)
            else:
                const_dir = None

    loc = get_location()

    # Try to paint beneath us as we walk to avoid paint penalties.
    # Avoiding wasting paint by re-painting our own tiles.
    nearby_tiles = sense_nearby_map_infos(center=loc)
    nearby_ruins = [] # Stores positions of unfinished ruins
    for tile in nearby_tiles:
        if tile.has_ruin(): nearby_ruins.append(tile.get_map_location())
    nearest_tile = None
    nearest_dst = 999999
    if non_painting <= 0 and is_action_ready():
        for tile in nearby_tiles:
            # Only paint in radius 2
            tile_loc = tile.get_map_location()
            if tile_loc.distance_squared_to(loc) > 4: continue
            if not can_attack(tile_loc): continue # Skip if can't attack
            if tile.get_paint() != PaintType.EMPTY:
                if tile.get_paint().is_ally():
                    if ((tile.get_paint() == PaintType.ALLY_SECONDARY) == get_pattern_at_loc(tile_loc)): continue # No need to override
                    # Can override if not in range of any ruins
                    can_override = True
                    for ruin in nearby_ruins:
                        dst = ruin.distance_squared_to(tile_loc)
                        if dst <= 8:
                            can_override = False
                            break
                    if not can_override: continue
                elif tile.get_paint().is_enemy(): continue # Can't override enemy paint
            dst = loc.distance_squared_to(tile_loc)
            if dst < nearest_dst:
                nearest_dst = dst
                nearest_tile = tile
        if nearest_tile != None:
            nearest_tile_loc = nearest_tile.get_map_location()
            if can_attack(nearest_tile_loc):
                attack(nearest_tile_loc, get_pattern_at_loc(nearest_tile_loc)) # SRP tiling

def run_mopper():
    global is_refilling
    # Prioritize where without ally paint
    # Splashers have max paint of 300
    paint_percentage = get_paint()
    if len(known_paint_towers) == 0: run_aggresive_mopper()
    else:
        if not is_refilling and paint_percentage > return_to_paint[UnitType.MOPPER]:
            run_aggresive_mopper()
        else:
            try_refill_paint(paint_percentage, UnitType.MOPPER)
# this is how the story goes
def run_aggresive_mopper():
    global nearby_tiles
    global const_dir
    global time_till_next_dir
    
    loc = get_location()
    nearby_tiles = sense_nearby_map_infos(center=loc)
    enemy_robots = sense_nearby_robots(center=loc, team=get_team().opponent())
    ally_robots = sense_nearby_robots(center=loc, team=get_team())
    update_paint_towers()

    if is_messenger:
        set_indicator_dot(loc, 255, 0, 0)

    if should_save and len(known_towers) > 0:
        # Move to first known tower if we are saving
        dir = loc.direction_to(known_towers[0])
        set_indicator_string(f"Returning to {known_towers[0]}")
        if can_move(dir):
            move(dir)

    # Get best direction based on heuristic
    # We shouldn't move to directions with non-painted tiles
    this_tile = sense_map_info(loc)
    is_on_unsafe = False
    nearest_safe = None
    if not this_tile.get_paint().is_ally():
        is_on_unsafe = True
        # Retreat
        cur_dist = 999999
        for tile in nearby_tiles:
            if tile.get_paint().is_ally():
                dst = tile.get_map_location().distance_squared_to(loc)
                if dst < cur_dist:
                    cur_dist = dst
                    nearest_safe = tile

    dir_priority = {dir: 0 for dir in directions}
    has_nearby_enemy_paint = False # Adjacent
    detect_nearby_enemy_paint = False # Seeable
    for tile in nearby_tiles:
        if tile.has_ruin() or tile.is_wall(): continue
        tile_loc = tile.get_map_location()
        dir = loc.direction_to(tile_loc)
        dst = loc.distance_squared_to(tile.get_map_location())
        paint = tile.get_paint()
        if dst <= 2 and paint.is_enemy():
            has_nearby_enemy_paint = True
            break
        if not can_move(dir): continue
        next_loc = loc.add(dir)
        if can_sense_location(next_loc) and not sense_map_info(next_loc).get_paint().is_ally():
            dir_priority[dir] = -50
        
        if paint.is_enemy():
            dir_priority[dir] = dir_priority[dir] + 500 / dst / dst / dst / dst  # 1st priority: enemy paint
            detect_nearby_enemy_paint = True

    if is_on_unsafe:
        if nearest_safe != None:
            bug2(nearest_safe.get_map_location())
        else:
            const_dir = get_random_dir()
    elif not detect_nearby_enemy_paint:
        # 2nd priority should be fellow moppers
        # Mopper together stronk
        for ally in ally_robots:
            if ally.get_type() != UnitType.MOPPER: continue
            dir = loc.direction_to(ally.get_location())
            if not can_move(dir): continue
            next_loc = loc.add(dir)
            if can_sense_location(next_loc) and not sense_map_info(next_loc).get_paint().is_ally():
                dir_priority[dir] = -50

            dir_priority[dir] = dir_priority[dir] + 35  # 2nd priority: ally mopper
        for enemy in enemy_robots:
            dir = loc.direction_to(enemy.get_location())
            if not can_move(dir): continue
            next_loc = loc.add(dir)
            if can_sense_location(next_loc) and not sense_map_info(next_loc).get_paint().is_ally():
                dir_priority[dir] = -50

            dir_priority[dir] = dir_priority[dir] + 1  # 2nd priority: enemy

    # Freeze if detect nearby paint
    if (not has_nearby_enemy_paint) or (is_on_unsafe):
        # Make sure we go to empty square
        optimal_dir = None
        optimal = 0
        for (test_dir, prio) in dir_priority.items():
            if prio > optimal:
                optimal = prio
                optimal_dir = test_dir
        if const_dir == None:
            if optimal_dir != None:
                const_dir = optimal_dir
                time_till_next_dir = change_dir_delay + random.randint(-change_dir_dev, change_dir_dev)
        elif time_till_next_dir <= 0:
            if optimal_dir != None:
                const_dir = optimal_dir
                time_till_next_dir = change_dir_delay + random.randint(-change_dir_dev, change_dir_dev)
        if const_dir == None:
            const_dir = get_random_dir()
        if const_dir != None:
            if can_move(const_dir):
                next_loc = loc.add(const_dir)
                if can_sense_location(next_loc) and sense_map_info(next_loc).get_paint().is_ally():
                    move(const_dir)
                else:
                    const_dir = None
            else:
                const_dir = None

    loc = get_location()


    if is_action_ready():
        # Only attacks when sees enemy
        for enemy in enemy_robots:
            target_loc = enemy.get_location()
            dst = loc.distance_squared_to(target_loc)
            if dst > 2: continue
            swingDir = loc.direction_to(target_loc)
            if can_mop_swing(swingDir):
                mop_swing(swingDir)
                log("Mop Swing! Booyah!")
                break

        for tile in nearby_tiles:
            dst = loc.distance_squared_to(tile.get_map_location())
            if dst > 2: continue
            if tile.get_paint().is_enemy():
                mop_dir = loc.direction_to(tile.get_map_location())
                mop_loc = loc.add(mop_dir)
                if can_attack(mop_loc): 
                    attack(mop_loc)
                    break

    will_do_messenger = (get_id() % messenger_work_distribution == turn_count % messenger_work_distribution) # Split the work over many turns
    if will_do_messenger and is_messenger:
        check_nearby_ruins()
        update_friendly_towers()

    if can_repeat_cooldowned_action(sense_tower_delay):
        try_to_upgrade_towers()

    # We can also move our code into different methods or classes to better organize it!
    # update_enemy_robots()

#TODO (LITERALLY THE BIGGEST TODO YET)
def run_splasher():
    global is_refilling
    # Prioritize where without ally paint
    # Splashers have max paint of 300
    paint_percentage = get_paint() / 3
    if len(known_paint_towers) == 0: run_aggresive_splasher()
    else:
        if not is_refilling and paint_percentage > return_to_paint[UnitType.SPLASHER]:
            run_aggresive_splasher()
        else:
            try_refill_paint(paint_percentage, UnitType.SPLASHER)

def run_aggresive_splasher():
    global known_paint_towers
    global nearby_tiles
    global const_dir
    global time_till_next_dir
    nearby_tiles = sense_nearby_map_infos(center=get_location())
    loc = get_location()
    # Get all tiles we're gonna paint over to avoid painting on marked tiles 
    # Total splashed tiles = 13. We're gonna splash if splash_threshold+ tiles are splashable
    to_attack = None
    best_splash = splash_threshold
    if is_action_ready():
        attackable_tiles = get_all_locations_within_radius_squared(center=loc, radius_squared=4)
        for tile in attackable_tiles:
            if not can_attack(tile): continue
            local_nearby_tiles = sense_nearby_map_infos(center=tile, radius_squared=4)
            splashables = 0
            for splashed in local_nearby_tiles:
                dst = tile.distance_squared_to(splashed.get_map_location())
                if splashed.has_ruin():
                    tower = sense_robot_at_location(splashed.get_map_location())
                    if tower != None and tower.get_team() != get_team(): splashables += 1000
                else:
                    if dst > 2:
                        if (not splashed.is_wall()) and (splashed.get_paint() == PaintType.EMPTY): splashables += 1
                    else:
                        if (not splashed.is_wall()) and (not splashed.get_paint().is_ally()): splashables += 1
            if splashables >= best_splash: 
                best_splash = splashables
                to_attack = tile
            
        if can_attack(to_attack): attack(to_attack)

    # Prioritize moving to empty squares
    dir_paint_count = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
    # Moppers should prioritize: cnt paint -> cnt enemy -> cnt ally. Each square has radius squared of 9
    for tile in nearby_tiles:
        tile_loc = tile.get_map_location()
        if tile.has_ruin():
            tower = sense_robot_at_location(tile_loc)
            if (tower != None) and tower.get_team() == get_team(): # Is ally tower
                if is_paint_tower(tower.get_type()): # Is paint tower
                    if not (tile_loc in known_paint_towers):
                        known_paint_towers.append(tile_loc)
        else:
            dir = loc.direction_to(tile_loc)
            if not can_move(dir): continue
            idx = direction_indices[dir]
            if not tile.is_wall() and not tile.get_paint().is_ally(): 
                dir_paint_count[idx] = dir_paint_count[idx] + 25
                
    nearby_robots = sense_nearby_robots(center=loc, team=get_team().opponent())
    for robot in nearby_robots:
        robot_loc = robot.get_location()
        dir = loc.direction_to(robot_loc)
        if not can_move(dir): continue
        idx = direction_indices[dir]
        # Move to places with enemies
        dir_paint_count[idx] = dir_paint_count[idx] + 1

    if is_const_walk:
        if const_dir == None:
            const_dir = get_random_dir()
        if not can_move(const_dir):
            const_dir = get_random_dir()
        if can_move(const_dir):
            move(const_dir)
    else:
        optimal_dir = -1
        optimal = 0
        for (test_dir, paint_count) in dir_paint_count.items():
            if paint_count > optimal:
                optimal = paint_count
                optimal_dir = test_dir

        if const_dir == None:
            if optimal_dir != -1:
                const_dir = directions[optimal_dir]
                time_till_next_dir = change_dir_delay + random.randint(-change_dir_dev, change_dir_dev)
        elif time_till_next_dir <= 0:
            if optimal_dir != -1:
                const_dir = directions[optimal_dir]
                time_till_next_dir = change_dir_delay + random.randint(-change_dir_dev, change_dir_dev)
        if const_dir == None:
            const_dir = get_random_dir()
        if const_dir != None:
            if can_move(const_dir):
                move(const_dir)
            else:
                const_dir = None

    if can_repeat_cooldowned_action(sense_tower_delay):
        try_to_upgrade_towers()

def check_nearby_ruins():
    global should_save
    nearby_tiles = sense_nearby_map_infos(center=get_location())

    # Search for a nearby ruin to complete.
    for tile in nearby_tiles:
        tile_loc = tile.get_map_location()
        if not tile.has_ruin() or sense_robot_at_location(tile_loc) != None:
            continue
        
        # Heuristic to see if the ruin is trying to be built on
        mark_loc = tile_loc.add(tile_loc.direction_to(get_location()))
        mark_info = sense_map_info(mark_loc)
        if not mark_info.get_mark().is_ally():
            continue

        should_save = True

        # Return early
        return

def update_friendly_towers():
    global should_save

    # Search for all nearby robots
    ally_robots  = sense_nearby_robots(team=get_team())
    for ally in ally_robots:
        # Only consider tower type
        if not ally.get_type().is_tower_type():
            continue

        ally_loc = ally.location
        if ally_loc in known_towers:
            # Send a message to the nearby tower
            if should_save and can_send_message(ally_loc):
                send_message(ally_loc, 0)
                should_save = False

            # Skip adding to the known towers array
            continue

        # Add to our known towers array
        known_towers.append(ally_loc)
        set_indicator_string(f"Found tower {ally.get_id()}")


def try_to_upgrade_towers():
    return

def try_refill_paint(paint_percentage, unitType):
    global known_paint_towers
    global is_refilling
    if len(known_paint_towers) == 0:
        is_refilling = False
        return
    if paint_percentage > back_to_aggresion[unitType]:
        is_refilling = False
    else:
        tower_loc = known_paint_towers[0]
        is_refilling = True
        bug2(tower_loc)
        if can_sense_location(tower_loc):
            paint_tower = sense_robot_at_location(tower_loc)
            if paint_tower == None:
                known_paint_towers.pop(0)
            else:
                # Ensure we refill as much as possible
                missing_paint = paint_capacity[unitType] - get_paint()
                tower_paint = paint_tower.get_paint_amount()
                transfer_amount = 0
                if missing_paint > tower_paint:
                    transfer_amount = tower_paint
                else:
                    transfer_amount = missing_paint
                if can_transfer_paint(tower_loc, -transfer_amount):
                    transfer_paint(tower_loc, -transfer_amount)

# Ensure marked squares are painted the right color if encountered
def paint_nearby_marks():
    if not is_action_ready(): return
    for pattern_tile in nearby_tiles:
        if pattern_tile.get_paint().is_enemy(): continue
        if pattern_tile.get_mark() != pattern_tile.get_paint() and pattern_tile.get_mark() != PaintType.EMPTY:
            use_secondary = (pattern_tile.get_mark() == PaintType.ALLY_SECONDARY)
            if can_attack(pattern_tile.get_map_location()):
                attack(pattern_tile.get_map_location(), use_secondary)
                return

# Complete SRP
def complete_SRP():
    global paintingSRP
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            tile = MapLocation(get_location().x+dx, get_location().y+dy)
            if not on_the_map(tile): continue
            info = sense_map_info(tile)
            # Abort if sees enemy paint
            if info.get_paint().is_enemy():
                paintingSRP = False
                #remove_mark(get_location())
                break
            if info.get_paint() == PaintType.EMPTY or ((info.get_paint() == PaintType.ALLY_SECONDARY) != SRP[dx+2][dy+2]):
                if can_attack(tile):
                    attack(tile, SRP[dx+2][dy+2])

# Check whether we can build an SRP here. Returns false if one is already present
def can_SRP_here():
    check_squares = sense_nearby_map_infos(get_location())
    for tile in check_squares:
        if get_location().distance_squared_to(tile.get_map_location()) == 16:
            continue
        if tile.get_mark() != PaintType.EMPTY:
            return False
    correct_count = 0
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            tiles = MapLocation(get_location().x+dx, get_location().y+dy)
            if not on_the_map(tiles):
                return False
            tile = sense_map_info(tiles)
            if tile.is_wall() or tile.has_ruin():
                return False
            if tile.get_paint().is_enemy() or ((tile.get_mark() == PaintType.ALLY_SECONDARY) != SRP[dx+2][dy+2] and tile.get_mark() != PaintType.EMPTY):
                return False
            if tile.get_mark() != PaintType.EMPTY and tile.get_mark() == tile.get_paint(): correct_count += 1
    return True if correct_count < 25 else False

def is_paint_tower(type):
    return type in {UnitType.LEVEL_ONE_PAINT_TOWER, UnitType.LEVEL_TWO_PAINT_TOWER, UnitType.LEVEL_THREE_PAINT_TOWER}

def update_paint_towers():
    global known_paint_towers
    # Store every known towers
    for tile in nearby_tiles:
        tile_loc = tile.get_map_location()
        if tile.has_ruin():
            tower = sense_robot_at_location(tile_loc)
            if (tower != None) and tower.get_team() == get_team(): # Is ally tower
                if is_paint_tower(tower.get_type()): # Is paint tower
                    if not (tile_loc in known_paint_towers):
                        known_paint_towers.append(tile_loc)

# SRP pattern tile!
def get_pattern_at_loc(loc: MapLocation):
    row = get_map_height() - loc.y # One indexed
    if loc.x % 4 == 0:
        if row % 4 == 3: return False # Primary
        return True # Secondary
    elif loc.x % 4 == 1:
        if row % 4 == 1: return True
        return False
    elif loc.x % 4 == 2:
        if row % 4 == 3: return True
        return False
    else:
        if row % 4 == 1: return True
        return False