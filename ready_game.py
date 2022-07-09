import random
import discord
from discord import Color
from game_status import Game_status


# async def first(first_player):
#     embed = discord.Embed(title="당신은 선공 플레이어입니다.",
#                           description="1라운드에 타일을 먼저 제시합니다. 2라운드부터는 전 라운드에 승리한 플레이어가 선플레이어가 됩니다.",
#                           color=Color.blue())
#     await first_player.send(embed=embed)


# async def second(second_player):
#     embed = discord.Embed(title="당신은 후공 플레이어입니다.",
#                           description="1라운드에 타일을 나중에 제시합니다. 2라운드부터는 전 라운드에 승리한 플레이어가 선플레이어가 됩니다.",
#                           color=Color.red())
#     await second_player.send(embed=embed)

# async def show_roles(room_info, game_info, roles):
#     for member in room_info.members:
#         if game_info.first_player == member:
#             await first(member)
#         else:
#             await second(member)

async def ready_game(current_game):
    room_info = current_game['game_room']
    current_game['game_status'] = Game_status()
    game_status = current_game['game_status']
    
    random.shuffle(room_info.members)
    print(room_info.members)
    game_status.first_player = room_info.members[0]
    game_status.second_player = room_info.members[1]

    game_status.scores[room_info.members[0]] = 0
    game_status.scores[room_info.members[1]] = 0
    game_status.numeric_tiles[room_info.members[0]] = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    game_status.numeric_tiles[room_info.members[1]] = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    game_status.game_results[room_info.members[0]] = []
    game_status.game_results[room_info.members[1]] = []
    # tmp = random.choice(room_info.members)
    # game_status.first_player = tmp
    # for player in room_info.members:
    #     if player != game_status.first_player:
    #         game_status.second_player = player
    #         break
        
    embed = discord.Embed(title=f"선 플레이어 {game_status.first_player.name}", description=f"""
    각 플레이어의 초기 타일은 다음과 같습니다.\n""")

    file = discord.File("src/tiles.png", filename="tiles.png")
    embed.set_image(url="attachment://tiles.png")
    await room_info.main_channel.send(file=file, embed=embed)
    print("ready")