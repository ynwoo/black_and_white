from active_games import active_games

# def is_bot(author_id, game_room):
# 	for member in game_room.members:
# 		if member.id == author_id:
# 			return False
# 	return True

async def is_open(ctx):
    if ctx.channel.id not in active_games:
        await ctx.send("시작한 게임이 존재하지 않습니다.")
        return

    room_info = active_games[ctx.channel.id]['game_room']
    if not room_info.can_join:
        await ctx.send("참가가 이미 마감되었습니다.")
        return

    if len(room_info.members) >= 2:
        await ctx.send("제한 인원(2명)을 초과하였습니다.")
        return

    return room_info

def get_current_game(user_id):
    for channel_id in active_games:
        for member in active_games[channel_id]['game_room'].members:
            if user_id == member.id:
                return active_games[channel_id]
    return None

def num2korean(n):
    n2k ={
    1 : '첫',
    2 : '두',
    3 : '세',
    4 : '네',
    5 : '다섯',
    6 : '여섯',
    7 : '일곱',
    8 : '여덟',
    9 : '아홉'}
    return n2k[n]