def tank_collide(map_data,tank_self,grids_size,height):
    if tank_self.direction=='up':
        if tank_self.pos[0]%grids_size==0:
            if map_data[pos_translate(tank_self.pos[0],tank_self.pos[1]-tank_self.speed,grids_size,width)]['can_pass']:
                return True
            else:
                return False
        else:
            if map_data[pos_translate(tank_self.pos[0],tank_self.pos[1]-tank_self.speed,grids_size,width)]['can_pass'] and map_data[pos_translate(tank_self.pos[0]+grids_size,tank_self.pos[1]-tank_self.speed,grids_size,width)]['can_pass']:
                return True
            else:
                return False    
    if tank_self.direction=='down':
        if tank_self.pos[0]%grids_size==0:
            if map_data[pos_translate(tank_self.pos[0],tank_self.pos[1]+tank_self.speed+(grids_size//2),grids_size,width)]['can_pass']:
                return True
            else:
                return False
        else:
            if map_data[pos_translate(tank_self.pos[0],tank_self.pos[1]+tank_self.speed+(grids_size//2),grids_size,width)]['can_pass'] and map_data[pos_translate(tank_self.pos[0]+grids_size,tank_self.pos[1]+tank_self.speed+(grids_size//2),grids_size,width)]['can_pass']:
                return True
            else:
                return False
    if tank_self.direction=='left':
        if tank_self.pos[1]%grids_size==0:
            if map_data[pos_translate(tank_self.pos[0]-tank_self.speed,tank_self.pos[1],grids_size,width)]['can_pass']:
                return True
            else:
                return False
        else:
            if map_data[pos_translate(tank_self.pos[0]-tank_self.speed,tank_self.pos[1],grids_size,width)]['can_pass'] and map_data[pos_translate(tank_self.pos[0]-tank_self.speed,tank_self.pos[1]+grids_size,grids_size,width)]['can_pass']:
                return True
            else:
                return False
    if tank_self.direction=='right':
        if tank_self.pos[1]%grids_size==0:
            if map_data[pos_translate(tank_self.pos[0]+tank_self.speed+(grids_size//2),tank_self.pos[1],grids_size,width)]['can_pass']:
                return True
            else:
                return False
        else:
            if map_data[pos_translate(tank_self.pos[0]+tank_self.speed+(grids_size//2),tank_self.pos[1],grids_size,width)]['can_pass'] and map_data[pos_translate(tank_self.pos[0]+tank_self.speed+(grids_size//2),tank_self.pos[1]+grids_size,grids_size,width)]['can_pass']:
                return True
            else:
                return False