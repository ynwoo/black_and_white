import random
import discord
from game_status import Game_status


async def ready_game(current_game):
    room_info = current_game['game_room']
    current_game['game_status'] = Game_status()
    game_status = current_game['game_status']
    
    random.shuffle(room_info.members)
    game_status.first_player = room_info.members[0]
    game_status.second_player = room_info.members[1]

    game_status.scores[room_info.members[0]] = 0
    game_status.scores[room_info.members[1]] = 0
    game_status.numeric_tiles[room_info.members[0]] = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    game_status.numeric_tiles[room_info.members[1]] = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    game_status.game_results[room_info.members[0]] = []
    game_status.game_results[room_info.members[1]] = []
        
    embed = discord.Embed(title=f"선 플레이어 {game_status.first_player.name}", description=f"""
    각 플레이어의 초기 타일은 다음과 같습니다.\n""")

    file = discord.File("src/tiles.png", filename="tiles.png")
    embed.set_image(url="attachment://tiles.png")
    await room_info.main_channel.send(file=file, embed=embed)
    print("ready")