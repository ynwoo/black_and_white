import discord
import time
from utils import num2korean
from active_games import active_games

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

async def start_round(current_game):
    time.sleep(1)
    game_room = current_game['game_room']
    game_status = current_game['game_status']
    
    if game_status.scores[game_room.members[0]] == 5:
        embed = discord.Embed(title=f"{game_room.members[0].name}님이 승점 {game_status.scores[game_room.members[0]]}점으로 이기셨습니다.")
        embed.add_field(name=f"게임을 종료하겠습니다.", 
                        value=f"""{game_room.members[1].name} 패
    {game_room.members[0].name} 승""", inline=False)

        embed.add_field(name=f"게임 기록", value=f"""{game_room.members[0]} 님: {game_status.game_results[game_room.members[0]]}
        {game_room.members[1].name} 님: {game_status.game_results[game_room.members[1]]}""", inline=False)
        await game_room.main_channel.send(embed=embed)

        print(game_status.game_results[game_room.members[0]])
        print(game_status.game_results[game_room.members[1]])
        del active_games[game_room.main_channel.channel.id]
        return

    if game_status.scores[game_room.members[1]] == 5:
        embed = discord.Embed(title=f"{game_room.members[1].name}님이 승점 {game_status.scores[game_room.members[1]]}점으로 이기셨습니다.")
        embed.add_field(name=f"게임을 종료하겠습니다.", 
                        value=f"""{game_room.members[0].name} 패
    {game_room.members[1].name} 승""", inline=False)
        embed.add_field(name=f"게임 기록", value=f"""{game_room.members[0]} 님: {game_status.game_results[game_room.members[0]]}
        {game_room.members[1].name} 님: {game_status.game_results[game_room.members[1]]}""", inline=False)
        await game_room.main_channel.send(embed=embed)

        print(game_status.game_results[game_room.members[0]])
        print(game_status.game_results[game_room.members[1]])
        del active_games[game_room.main_channel.channel.id]
        return

    if game_status.round > 8:
        # 전체 라운드가 끝난 상황, 스코어 비교해서 최종 승자 보여주기
        if game_status.scores[game_room.members[0]] < game_status.scores[game_room.members[1]]:
            embed = discord.Embed(title=f"{game_room.members[1].name}님이 승점 {game_status.scores[game_room.members[1]]}점으로 이기셨습니다.")
            embed.add_field(name=f"게임을 종료하겠습니다.", 
                            value=f"""{game_room.members[0].name} 패
        {game_room.members[1].name} 승""", inline=False)
            await game_room.main_channel.send(embed=embed)
            
        elif game_status.scores[game_room.members[0]] > game_status.scores[game_room.members[1]]:
            embed = discord.Embed(title=f"{game_room.members[0].name}님이 승점 {game_status.scores[game_room.members[0]]}점으로 이기셨습니다.")
            embed.add_field(name=f"게임을 종료하겠습니다.", 
                            value=f"""{game_room.members[1].name} 패
        {game_room.members[0].name} 승""", inline=False)
            await game_room.main_channel.send(embed=embed)
            
        else:
            embed = discord.Embed(title="무승부입니다. 게임을 종료하겠습니다.")
            await game_room.main_channel.send(embed=embed)
        
        embed = discord.Embed(title=f"""게임 결과
        {game_room.members[0].name} 님: {game_status.game_results[game_room.members[0]]}
        {game_room.members[1].name} 님: {game_status.game_results[game_room.members[1]]}""")
        await game_room.main_channel.send(embed=embed)

        print(game_status.game_results[game_room.members[0]])
        print(game_status.game_results[game_room.members[1]])
        del active_games[game_room.main_channel.channel.id]
        return
            
        
    game_status.round += 1
    
    embed = discord.Embed(title=f"{game_room.members[0].name} {game_status.scores[game_room.members[0]]} {game_status.round}R {game_status.scores[game_room.members[1]]} {game_room.members[1].name}")
    embed.add_field(name=f"현재 선플레이어는 {game_status.first_player.name}님입니다.", 
                    value=f"""{num2korean(game_status.round)} 번째 라운드 타일을 제시해주십시오.
타일 제시는 DM으로 입력해주시면 됩니다.""", inline=False)

    await game_room.main_channel.send(embed=embed)
    await decide_tile(game_room, game_status)
