import discord, random, asyncio, youtube_dl, time

client = discord.Client()
players = {}
queue = []
COR = 0xF7FE2E
musicatual = ''


async def check_queue(id, sv, message):
    global musicatual
    if len(queue) == 0: return
    del queue[0]
    if len(queue) != 0:
        voice = client.voice_client_in(sv)
        player = await voice.create_ytdl_player(queue[0])
        players[id].stop()
        players[id] = player
        player.start()
        if message.content.lower() == '-s' or message.content.lower() == '-skip':
            matual = musicatual
            musicatual = player.title
            mscskip = discord.Embed(
                title="\n",
                color=COR,
                description='A música **{}** foi pulada e agora está a tocar a música **{}**'.format(matual, musicatual)
            )
            await client.send_message(message.channel, embed=mscskip)
        await asyncio.sleep(player.duration + 3)
        await check_queue(id, sv, message)
    else:
        can = client.voice_client_in(sv)
        players[id].stop()
        await can.disconnect()


def randcor():
    global COR
    COR = random.randint(0x00000, 0xFFFFFF)
    return COR


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='D4rkB', type=3))
    print('Bot Online!')
    print(client.user.name)
    print(client.user.id)
    print('------------------')


@client.event
async def on_member_join(member):
    canal = client.get_channel('ID')
    msg = f'Bem Vindo! {member.mention}'
    await client.send_message(canal, msg)


@client.event
async def on_member_remove(member):
    canal = client.get_channel('ID')
    msg = f'Adeus! {member.mention}'
    await client.send_message(canal, msg)


@client.event
async def on_message(message):
    global musicatual
    if message.content.lower() == '-help' or message.content.lower() == '-ajuda':
        mschelp = discord.Embed(
            title='---------------------Ajuda---------------------',
            color=randcor(),
            description='-moeda - Jogar cara/coroa comigo \n'
                        '-ping - Vê o meu ping\n'
                        '-entrar - Entro no teu canal de voz \n'
                        '-sair - Saio do canal de voz em que estou \n'
                        '-play - Procura uma música no youtube e toca-a \n'
                        '-pause - Pausa a música que estiver a dar \n'
                        '-resume - Tira o pause da música\n'
                        '-skip - Salta a música\n'
                        '-info - Informações sobre mim\n'
                        '-clear <número> - Apaga um determinado nº de mensagens\n'
                        '-kick @<nome> - Kicka alguém\n'
                        '-ban @<nome> - Bane alguém\n'
                        '-unban @<nome> - Tira o ban a alguém\n'
                        '-invite - Cria um link de convite do servidor\n'
                        '-sugestao - Envia uma sugestao\n'
                        '-bugs - Reporta algum bug do bot'
        )
        await client.send_message(message.channel, embed=mschelp)
    elif message.content.lower() == '-moeda':
        choice = random.randint(1, 2)
        if choice == 1:
            await client.add_reaction(message, '😀')
        else:
            await client.add_reaction(message, '👑')

    elif message.content.lower() == '-entrar':
        try:
            canal = message.author.voice.voice_channel
            await client.join_voice_channel(canal)
        except discord.InvalidArgument:
            await client.send_message(message.channel, 'Precisas de estar num canal de voz para usar este comando!')

    elif message.content.lower() == '-sair':
        try:
            canal = client.voice_client_in(message.server)
            await canal.disconnect()
            queue.clear()
        except AttributeError:
            await client.send_message(message.channel, 'Eu não estou em nenhum canal de voz!')

    elif message.content.lower().startswith('-play ') or message.content.lower().startswith('-p '):
        if message.content.lower().startswith('-play'):
            yt_url = message.content[6:]
        else:
            yt_url = message.content[3:]
        if client.is_voice_connected(message.server):
            try:
                voice = client.voice_client_in(message.server)
                if yt_url.startswith('http'):
                    player = await voice.create_ytdl_player(yt_url)
                    queue.append(yt_url)
                else:
                    player = await voice.create_ytdl_player('ytsearch: {}'.format(yt_url))
                    queue.append('ytsearch: {}'.format(yt_url))
                await client.send_message(message.channel, f'**A procurar** `{yt_url}`  :mag:')
                if len(queue) == 0:
                    players[message.server.id].stop()
                    players[message.server.id] = player
                    player.start()
                    musicatual = player.title
                    mscemb = discord.Embed(
                        title="Música para tocar:",
                        color=randcor()
                    )
                    mscemb.add_field(name="Nome:", value="`{}`".format(player.title))
                    mscemb.add_field(name="Visualizações:", value="`{}`".format(player.views))
                    mscemb.add_field(name="Enviado em:", value="`{}`".format(player.upload_date))
                    mscemb.add_field(name="Enviado por:", value="`{}`".format(player.uploader))
                    mscemb.add_field(name="Duraçao:", value="`{}`".format(player.duration))
                    mscemb.add_field(name="Likes:", value="`{}`".format(player.likes))
                    mscemb.add_field(name="Dislikes:", value="`{}`".format(player.dislikes))
                    await client.send_message(message.channel, embed=mscemb)
                else:
                    mscemb3 = discord.Embed(
                        title="Música adicionada na lista:",
                        color=randcor()
                    )
                    mscemb3.add_field(name="Nome:", value="`{}`".format(player.title))
                    mscemb3.add_field(name="Visualizações:", value="`{}`".format(player.views))
                    mscemb3.add_field(name="Enviado em:", value="`{}`".format(player.upload_date))
                    mscemb3.add_field(name="Enviado por:", value="`{}`".format(player.uploader))
                    mscemb3.add_field(name="Duraçao:", value="`{}`".format(player.duration))
                    mscemb3.add_field(name="Likes:", value="`{}`".format(player.likes))
                    mscemb3.add_field(name="Dislikes:", value="`{}`".format(player.dislikes))
                    await client.send_message(message.channel, embed=mscemb3)
            except discord.InvalidArgument:
                await client.send_message(message.channel, 'Precisas de estar num canal de voz para usar este comando!')
            except youtube_dl.utils.ExtractorError:
                await client.send_message(message.channel, 'Atualiza o youtube-dl!')
            except Exception as e:
                await client.send_message(message.server, "Erro: [{error}]".format(error=e))

        if not client.is_voice_connected(message.server):
            if len(queue) != 0:
                if yt_url.startswith('http'):
                    queue.append(yt_url)
                else:
                    queue.append('ytsearch: {}'.format(yt_url))
                return
            try:
                channel = message.author.voice.voice_channel
                voice = await client.join_voice_channel(channel)
                if yt_url.startswith('http'):
                    player = await voice.create_ytdl_player(yt_url)
                    queue.append(yt_url)
                else:
                    player = await voice.create_ytdl_player('ytsearch: {}'.format(yt_url))
                    queue.append('ytsearch: {}'.format(yt_url))
                players[message.server.id] = player
                player.start()
                await client.send_message(message.channel, f'**A procurar** `{yt_url}`  :mag:')
                musicatual = player.title
                mscemb2 = discord.Embed(
                    title="Música para tocar:",
                    color=randcor()
                )
                mscemb2.add_field(name="Nome:", value="`{}`".format(player.title))
                mscemb2.add_field(name="Visualizações:", value="`{}`".format(player.views))
                mscemb2.add_field(name="Enviado em:", value="`{}`".format(player.upload_date))
                mscemb2.add_field(name="Enviado por:", value="`{}`".format(player.uploader))
                mscemb2.add_field(name="Duraçao:", value="`{}`".format(player.duration))
                mscemb2.add_field(name="Likes:", value="`{}`".format(player.likes))
                mscemb2.add_field(name="Dislikes:", value="`{}`".format(player.dislikes))
                await client.send_message(message.channel, embed=mscemb2)
                await asyncio.sleep(player.duration + 3)
                if musicatual == player.title:
                    await check_queue(message.server.id, message.server, message)
            except discord.InvalidArgument:
                await client.send_message(message.channel, 'Precisas de estar num canal de voz para usar este comando!')
            except youtube_dl.utils.ExtractorError:
                await client.send_message(message.channel, 'Atualiza o youtube-dl!')
            except Exception as error:
                await client.send_message(message.channel, f"Erro: [{error}]")
    elif message.content.lower().startswith('-pause'):
        try:
            players[message.server.id].pause()
            mscpause = discord.Embed(
                title="\n",
                color=COR,
                description="Musica pausada com sucesso!"
            )
            await client.send_message(message.channel, embed=mscpause)
        except KeyError:
            await client.send_message(message.channel, "Não há nenhuma música a tocar!")
        except Exception as error:
            await client.send_message(message.channel, f"Erro: [{error}]")
    elif message.content.lower().startswith('-resume'):
        if client.is_voice_connected(message.server) and len(queue) != 0:
            try:
                mscresume = discord.Embed(
                    title="\n",
                    color=COR,
                    description="Musica a continuar!"
                )
                await client.send_message(message.channel, embed=mscresume)
                players[message.server.id].resume()
            except Exception as error:
                await client.send_message(message.channel, f"Erro: [{error}]")
        else:
            mcresume2 = discord.Embed(
                title="\n",
                color=COR,
                description="Não há nenhuma música a tocar!"
            )
            await client.send_message(message.channel, embed=mcresume2)
    elif message.content.lower() == '-s' or message.content.lower() == '-skip':
        if client.voice_client_in(message.server):
            await check_queue(message.server.id, message.server, message)
        else:
            await client.send_message(message.channel, 'Eu não estou em nenhum canal de voz!')

    elif message.content.lower() == '-info' or message.content.lower() == '-credits':
        mscinfo = discord.Embed(
            title='Info',
            color=COR,
            description='Linguagem de programação usada - **Python 3.6**\n'
                        'Bibliotecas usadas - **discord.py**, **random**, **asyncio**\n'
                        'Autor - **D4rkB**\n'
                        'Meu source-code: **https://github.com/D4rkB/D4rkBotPy/blob/master/d4rkbot.py**\n'                                              
                        '-help para **ver todos os comandos**'
        )
        await client.send_message(message.channel, embed=mscinfo)
    elif message.content.lower().startswith('-kick'):
        kicker = message.author
        if not kicker.server_permissions.kick_members:
            await client.send_message(message.channel, 'Não tens permissão :frowning2:')
            return
        if len(message.content.lower()) <= 6:
            await client.send_message(message.channel, '**Usa**: -kick <@nome>')
            return
        cmd = message.content.split()
        kicked = cmd[1]
        try:
            if len(cmd) == 2:
                await client.kick(message.server.get_member(kicked[2:-1]))
                await client.send_message(message.channel, f'O {kicked} foi kickado pelo {kicker.mention}.')
        except discord.Forbidden:
            await client.send_message(message.channel, f'Não tenho permissão para kickar o {kicked}.')
        except discord.HTTPException:
            await client.send_message(message.channel, 'Erro ao kickar. :frowning2:')
        except AttributeError:
            await client.send_message(message.channel, 'Utilizador não encontrado. :frowning2:')
    elif message.content.lower().startswith('-ban'):
        banner = message.author
        if not banner.server_permissions.ban_members:
            await client.send_message(message.channel, 'Não tens permissão :frowning2:')
        if len(message.content.lower()) <= 5:
            await client.send_message(message.channel, '**Usa**: -ban <@nome>')
            return
        cmd = message.content.split()
        banned = cmd[1]
        try:
            if len(cmd) == 2:
                await client.ban(message.server.get_member(banned[2:-1]), 0)
                await client.send_message(message.channel, f'O {banned} foi banido pelo {banner.mention}.')
        except discord.Forbidden:
            await client.send_message(message.channel, f'Não tenho permissão para banir o {banned}')
        except discord.HTTPException:
            await client.send_message(message.channel, 'Erro ao banir. :frowning2:')
        except AttributeError:
            await client.send_message(message.channel, 'Utilizador não encontrado :frowning2:')
    elif message.content.lower().startswith('-unban'):
        unbanner = message.author
        if not unbanner.server_permissions.ban_members:
            await client.send_message(message.channel, 'Não tens permissão :frowning2:')
        if len(message.content.lower()) <= 7:
            await client.send_message(message.channel, '**Usa**: -unban <@nome>')
            return
        cmd = message.content.split()
        unbanned = cmd[1]
        unbanned2 = await client.get_user_info(unbanned[2:-1])
        try:
            if len(cmd) == 2:
                await client.unban(message.server, unbanned2)
                await client.send_message(message.channel, f'O {unbanned} foi desbanido pelo {unbanner.mention}.')
        except discord.Forbidden:
            await client.send_message(message.channel, f'Não tens permissão para banir o {unbanned}')
        except discord.HTTPException:
            await client.send_message(message.channel, 'Erro ao banir. :frowning2:')
        except AttributeError:
            await client.send_message(message.channel, 'Utilizador não encontrado :frowning2:')
    elif message.content.lower().startswith('-invite') or message.content.lower().startswith('-convite'):
        cmd = message.content.split()
        try:
            if len(cmd) == 1:
                await client.send_message(message.channel, '**Usa**: -invite <duração do convite (0 é ilimitado)> ')
            else:
                invite = await client.create_invite(message.channel, max_age=int(cmd[1])*3600)
                if int(cmd[1]) == 0:
                    await client.send_message(message.channel, f'Convite criado com duração ilimitada: Link: {invite}')
                else:
                    await client.send_message(message.channel, f'Convite criado por {cmd[1]} hora(s)! Link: {invite}')
        except discord.HTTPException:
            await client.send_message(message.channel, 'Erro ao criar o convite. :frowning2:')
        except discord.errors.HTTPException:
            await client.send_message(message.channel, 'Introduz um valor válido!')
    elif message.content.lower().startswith('-clear') or message.content.lower().startswith('-limpar'):
        if not message.author.server_permissions.manage_messages:
            await client.send_message(message.channel, 'Não tens permissão :frowning2:')
        cmd = message.content.split()
        if len(cmd) == 1:
            await client.send_message(message.channel, '**Usa**: -clear <nº de mensagens para limpar>')
            return
        try:
            amount = int(cmd[1]) + 1 if len(cmd) > 1 else 2
        except Exception:
            await client.send_message(message.channel, 'Introduz um valor válido!')
            return
        except discord.errors.HTTPException:
            await client.send_message(message.channel, 'Não podes apagar mensagens com mais de 14 dias')
            return
        except discord.errors.ClientException:
            await client.send_message(message.channel, 'Só podes apagar entre 1 a 99 mensagens!')
        messages = list()
        async for m in client.logs_from(message.channel, limit=amount):
            messages.append(m)
        await client.delete_messages(messages)
        mscclear = discord.Embed(
            title='Limpeza',
            color=randcor(),
            description=f'Foram apagadas {amount} mensagens!'
        )
        await client.send_message(message.channel, embed=mscclear)
    elif message.content.lower().startswith('-ping'):
        time1 = time.monotonic()
        message1 = await client.send_message(message.channel, 'A calcular o ping....')
        ping = (time.monotonic() - time1) * 1000
        await client.edit_message(message1, f'O meu ping é de {round(ping/2)}ms.')
    elif message.content.lower().startswith('-sugestao'):
        sugestao = message.content.lower().split()
        if len(sugestao) == 1:
            await client.send_message(message.channel, '**Usa**: -sugestao <sugestao>')
            return
        canal = await client.get_user_info('334054158879686657')
        await client.send_message(canal, ' '.join(sugestao[1:]))
        await client.send_message(message.channel, 'Sugestão registada! Obrigado. :grinning:')
    elif message.content.lower().startswith('-bug'):
        bug = message.content.lower().split()
        if len(bug) == 1:
            await client.send_message(message.channel, '**Usa**: -bugs <bug>')
            return
        canal = await client.get_user_info('334054158879686657')
        await client.send_message(canal, ' '.join(bug[1:]))
        await client.send_message(message.channel, 'Bug reportado! Obrigado. :grinning:')
client.run('TOKEN')
