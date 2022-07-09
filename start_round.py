from discord import player
import asyncio
import discord
import random
from discord import activity
from discord.abc import User
import time
from utils import num2korean

async def decide_tile(game_room, game_status):
    if game_status.turn == -1:
        player = game_status.first_player
    else:
        player = game_status.second_player

    embed = discord.Embed(title=f"{player.name}님께서는 타일을 제시해주십시오.",
                          description=f"""타일을 제시하면 타일의 색만 공개가 됩니다.
제시하고 싶은 숫자의 이모티콘을 눌러주세요!
다음 라운드에는 전 라운드에 승리한 플레이어가 선플레이어가 됩니다.""")
                                     
    message = await player.send(embed=embed)
    for emoji in game_room.emojis:
        if game_room.emojis[emoji] in game_status.numeric_tiles[player]:
            await message.add_reaction(emoji)

    print('decide tile')

async def start_round(current_game):
    game_room = current_game['game_room']
    game_status = current_game['game_status']
    
    if game_status.scores[game_room.members[0]] == 5:
        embed = discord.Embed(title=f"{game_room.members[0].name}님이 승점 {game_status.scores[game_room.members[0]]}점으로 이기셨습니다.")
        embed.add_field(name=f"게임을 종료하겠습니다.", 
                        value=f"""{game_room.members[1].name} 패
    {game_room.members[0].name} 승""", inline=False)

        await game_room.main_channel.send(embed=embed)
        return

    if game_status.scores[game_room.members[1]] == 5:
        embed = discord.Embed(title=f"{game_room.members[1].name}님이 승점 {game_status.scores[game_room.members[1]]}점으로 이기셨습니다.")
        embed.add_field(name=f"게임을 종료하겠습니다.", 
                        value=f"""{game_room.members[0].name} 패
    {game_room.members[1].name} 승""", inline=False)

        await game_room.main_channel.send(embed=embed)
        return

    if game_status.round > 8:
        # 전체 라운드가 끝난 상황, 스코어 비교해서 최종 승자 보여주기
        if game_status.scores[game_room.members[0]] < game_status.scores[game_room.members[1]]:
            embed = discord.Embed(title=f"{game_room.members[1].name}님이 승점 {game_status.scores[game_room.members[1]]}점으로 이기셨습니다.")
            embed.add_field(name=f"게임을 종료하겠습니다.", 
                            value=f"""{game_room.members[0].name} 패
        {game_room.members[1].name} 승""", inline=False)

            await game_room.main_channel.send(embed=embed)
            return
        
        elif game_status.scores[game_room.members[0]] > game_status.scores[game_room.members[1]]:
            embed = discord.Embed(title=f"{game_room.members[0].name}님이 승점 {game_status.scores[game_room.members[0]]}점으로 이기셨습니다.")
            embed.add_field(name=f"게임을 종료하겠습니다.", 
                            value=f"""{game_room.members[1].name} 패
        {game_room.members[0].name} 승""", inline=False)

            await game_room.main_channel.send(embed=embed)
            return
        
        else: # 비긴 경우 연장라운드 돌입
            game_status.extended_round +=1
            game_status.round = 0
            game_status.numeric_tiles[game_room.members[0]] = [0, 1, 2, 3, 4, 5, 6, 7, 8]
            game_status.numeric_tiles[game_room.members[1]] = [0, 1, 2, 3, 4, 5, 6, 7, 8]
            embed = discord.Embed(title="연장 라운드 진행하도록 하겠습니다.")
            await game_room.main_channel.send(embed=embed)
        
    game_status.round += 1
    # game_status.results_of_round.append([game_status.round])
    if game_status.extended_round >= 2:
        embed = discord.Embed(title=f"{game_room.members[0].name} {game_status.scores[game_room.members[0]]} 연장 {game_status.round}R {game_status.scores[game_room.members[1]]} {game_room.members[1].name}")
    else:
        embed = discord.Embed(title=f"{game_room.members[0].name} {game_status.scores[game_room.members[0]]} {game_status.round}R {game_status.scores[game_room.members[1]]} {game_room.members[1].name}")
    # embed = discord.Embed(title=f"{game_status.round}라운드가 시작되었습니다!")
    embed.add_field(name=f"현재 선플레이어는 {game_status.first_player.name}님입니다.", 
                    value=f"""{num2korean(game_status.round)} 번째 라운드 타일을 제시해주십시오.
타일 제시는 DM으로 입력해주시면 됩니다.""", inline=False)

    await game_room.main_channel.send(embed=embed)
    await decide_tile(game_room, game_status)
