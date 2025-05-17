# utils/targeting_utils.py


def dist_to_monster(monster, pos):
    if monster.facing_right:
        monster_closest_pos = (max(monster.rect.left, min(pos[0], monster.rect.left + monster.width)),
                               max(monster.rect.top, min(pos[1], monster.rect.bottom)))
    else:
        monster_closest_pos = (max(monster.rect.right - monster.width, min(pos[0], monster.rect.right)),
                               max(monster.rect.top, min(pos[1], monster.rect.bottom)))
    return pos.distance_to(monster_closest_pos)