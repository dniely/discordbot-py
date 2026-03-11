import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

user_db = {}

tier_names = {
    0: "Unrated",
    1: "Bronze V",
    2: "Bronze IV",
    3: "Bronze III",
    4: "Bronze II",
    5: "Bronze I",
    6: "Silver V",
    7: "Silver IV",
    8: "Silver III",
    9: "Silver II",
    10: "Silver I",
    11: "Gold V",
    12: "Gold IV",
    13: "Gold III",
    14: "Gold II",
    15: "Gold I",
    16: "Platinum V",
    17: "Platinum IV",
    18: "Platinum III",
    19: "Platinum II",
    20: "Platinum I",
    21: "Diamond V",
    22: "Diamond IV",
    23: "Diamond III",
    24: "Diamond II",
    25: "Diamond I",
    26: "Ruby V",
    27: "Ruby IV",
    28: "Ruby III",
    29: "Ruby II",
    30: "Ruby I"
}

tier_code_map = {
    "b1": 5,
    "b2": 4,
    "b3": 3,
    "b4": 2,
    "b5": 1,
    "s1": 10,
    "s2": 9,
    "s3": 8,
    "s4": 7,
    "s5": 6,
    "g1": 15,
    "g2": 14,
    "g3": 13,
    "g4": 12,
    "g5": 11,
    "p1": 20,
    "p2": 19,
    "p3": 18,
    "p4": 17,
    "p5": 16,
    "d1": 25,
    "d2": 24,
    "d3": 23,
    "d4": 22,
    "d5": 21,
    "r1": 30,
    "r2": 29,
    "r3": 28,
    "r4": 27,
    "r5": 26
}

tag_list = [
    "implementation", "greedy", "dp", "math", "graphs", "bfs", "binary_search",
    "string", "bruteforcing", "data_structures", "segment_tree", "trees",
    "sorting", "dfs", "dijkstra", "shortest_path", "prefix_sum", "two_pointer",
    "stack", "queue", "deque", "priority_queue", "hash_map", "union_find",
    "topological_sorting", "bellman_ford", "floyd_warshall", "mst", "bitmask",
    "backtracking", "divide_and_conquer", "number_theory", "combinatorics",
    "geometry", "simulation", "recursion", "sparse_table", "monotone_stack",
    "sliding_window", "trie", "knapsack", "lis", "lcs", "flow",
    "bipartite_matching", "euler_tour", "hld", "sqrt_decomposition",
    "offline_queries", "convex_hull"
]

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(str(bot.user) + " 봇이 시작됐습니다!")


@bot.command()
async def 도움말(ctx):
    msg = "명령어 목록\n"
    msg = msg + "\n"
    msg = msg + "!등록 [백준아이디] - 아이디 등록\n"
    msg = msg + "!내정보 - 내 solved.ac 정보 보기\n"
    msg = msg + "!설정 [티어코드] [태그1] [태그2] ... - 추천 설정\n"
    msg = msg + "!내설정 - 현재 설정 확인\n"
    msg = msg + "!추천 - 설정한 티어/태그로 문제 추천\n"
    msg = msg + "!쉬운문제 - 내 티어보다 쉬운 문제 추천\n"
    msg = msg + "!어려운문제 - 내 티어보다 어려운 문제 추천\n"
    msg = msg + "!오늘의문제 - 오늘의 랜덤 문제 추천\n"
    msg = msg + "!검색 [검색어] - 문제 검색\n"
    msg = msg + "!태그목록 - 사용 가능한 태그 목록\n"
    msg = msg + "\n"
    msg = msg + "티어 코드: b1~b5(브론즈), s1~s5(실버), g1~g5(골드), p1~p5(플래), d1~d5(다이아), r1~r5(루비)"
    await ctx.send(msg)


@bot.command()
async def 태그목록(ctx):
    msg = "사용 가능한 태그 목록\n"
    msg = msg + "\n"
    msg = msg + "implementation, greedy, dp, math, graphs, bfs, binary_search, string, bruteforcing\n"
    msg = msg + "data_structures, segment_tree, trees, sorting, dfs, dijkstra, shortest_path\n"
    msg = msg + "prefix_sum, two_pointer, stack, queue, deque, priority_queue, hash_map\n"
    msg = msg + "union_find, topological_sorting, bellman_ford, floyd_warshall, mst\n"
    msg = msg + "bitmask, backtracking, divide_and_conquer, number_theory, combinatorics\n"
    msg = msg + "geometry, simulation, recursion, sparse_table, monotone_stack\n"
    msg = msg + "sliding_window, trie, knapsack, lis, lcs, flow, bipartite_matching\n"
    msg = msg + "euler_tour, hld, sqrt_decomposition, offline_queries, convex_hull\n"
    msg = msg + "\n"
    msg = msg + "사용 예시: !설정 g3 dp math segment_tree"
    await ctx.send(msg)


@bot.command()
async def 등록(ctx, handle=None):
    if handle == None:
        await ctx.send("사용법: !등록 [백준아이디]")
        return

    res = requests.get("https://solved.ac/api/v3/user/show?handle=" + handle,
                       timeout=5)
    data = res.json()

    if "handle" not in data:
        await ctx.send("존재하지 않는 아이디입니다!")
        return

    if ctx.author.id not in user_db:
        user_db[ctx.author.id] = {}

    user_db[ctx.author.id]["bj_id"] = handle

    tier_num = data["tier"]
    name = tier_names[tier_num]
    await ctx.send("" + handle + " 등록 완료! 현재 티어: " + name + "")


@bot.command()
async def 내정보(ctx):
    if ctx.author.id not in user_db:
        await ctx.send("먼저 !등록 [아이디] 로 등록해주세요!")
        return
    if "bj_id" not in user_db[ctx.author.id]:
        await ctx.send("먼저 !등록 [아이디] 로 등록해주세요!")
        return

    bj_id = user_db[ctx.author.id]["bj_id"]
    res = requests.get("https://solved.ac/api/v3/user/show?handle=" + bj_id,
                       timeout=5)
    data = res.json()

    tier_num = data["tier"]
    name = tier_names[tier_num]

    msg = "" + data["handle"] + " 의 정보\n"
    msg = msg + "티어: " + name + "\n"
    msg = msg + "레이팅: " + str(data["rating"]) + "\n"
    msg = msg + "랭킹: " + str(data["rank"]) + "위\n"
    msg = msg + "푼 문제 수: " + str(data["solvedCount"]) + "개\n"
    msg = msg + "클래스: Class " + str(data["class"]) + "\n"
    msg = msg + "최장 스트릭: " + str(data["maxStreak"]) + "일"
    await ctx.send(msg)


@bot.command()
async def 설정(ctx, tier_code=None, *tags):
    if ctx.author.id not in user_db or "bj_id" not in user_db[ctx.author.id]:
        await ctx.send("먼저 !등록 [아이디] 로 등록해주세요!")
        return

    if tier_code == None:
        await ctx.send("사용법: !설정 [티어코드] [태그1] [태그2] ...\n예시: !설정 g3 dp math")
        return

    if tier_code not in tier_code_map:
        await ctx.send(
            "티어 코드가 잘못됐어요!\n예시: b1~b5, s1~s5, g1~g5, p1~p5, d1~d5, r1~r5")
        return

    if len(tags) == 0:
        await ctx.send("태그를 1개 이상 입력해주세요! !태그목록 에서 확인하세요.")
        return

    if len(tags) > 3:
        await ctx.send("태그는 최대 3개까지만 입력 가능해요!")
        return

    for t in tags:
        if t not in tag_list:
            await ctx.send("" + t + " 는 없는 태그예요! !태그목록 에서 확인하세요.")
            return

    user_db[ctx.author.id]["tier_code"] = tier_code
    user_db[ctx.author.id]["tags"] = list(tags)

    tier_num = tier_code_map[tier_code]
    tier_str = tier_names[tier_num]
    tags_str = ""
    for t in tags:
        if tags_str != "":
            tags_str = tags_str + ", "
        tags_str = tags_str + t

    await ctx.send("설정 완료! 티어: " + tier_str + " | 태그: " + tags_str + "")


@bot.command()
async def 내설정(ctx):
    if ctx.author.id not in user_db or "bj_id" not in user_db[ctx.author.id]:
        await ctx.send("먼저 !등록 [아이디] 로 등록해주세요!")
        return

    data = user_db[ctx.author.id]
    msg = "현재 설정\n"
    msg = msg + "아이디: " + data["bj_id"] + "\n"

    if "tier_code" in data:
        tier_num = tier_code_map[data["tier_code"]]
        msg = msg + "티어: " + tier_names[tier_num] + "\n"
    else:
        msg = msg + "티어: 설정 안됨\n"

    if "tags" in data and len(data["tags"]) > 0:
        tags_str = ""
        for t in data["tags"]:
            if tags_str != "":
                tags_str = tags_str + ", "
            tags_str = tags_str + t
        msg = msg + "태그: " + tags_str + ""
    else:
        msg = msg + "태그: 설정 안됨"

    await ctx.send(msg)


@bot.command()
async def 추천(ctx):
    if ctx.author.id not in user_db or "bj_id" not in user_db[ctx.author.id]:
        await ctx.send("먼저 !등록 [아이디] 로 등록해주세요!")
        return

    data = user_db[ctx.author.id]

    if "tier_code" not in data:
        await ctx.send("먼저 !설정 [티어코드] [태그] 로 설정해주세요!")
        return
    if "tags" not in data or len(data["tags"]) == 0:
        await ctx.send("먼저 !설정 [티어코드] [태그] 로 설정해주세요!")
        return

    bj = data["bj_id"]
    tn = tier_code_map[data["tier_code"]]
    tags = data["tags"]

    tag_q = "("
    for i in range(len(tags)):
        if i > 0:
            tag_q = tag_q + "|"
        tag_q = tag_q + "tag:" + tags[i]
    tag_q = tag_q + ")"

    url = "https://solved.ac/api/v3/search/problem?query=tier:" + str(
        tn) + " " + tag_q + " !solved_by:" + bj + "&sort=random&direction=desc"
    res = requests.get(url, timeout=5)
    result = res.json()

    await send_probs(ctx, result, "사용자 지정 추천")


@bot.command()
async def 쉬운문제(ctx):
    if ctx.author.id not in user_db or "bj_id" not in user_db[ctx.author.id]:
        await ctx.send("먼저 !등록 [아이디] 로 등록해주세요!")
        return

    bj_id = user_db[ctx.author.id]["bj_id"]
    res = requests.get("https://solved.ac/api/v3/user/show?handle=" + bj_id,
                       timeout=5)
    u_info = res.json()
    my_tier = u_info["tier"]

    low = my_tier - 4
    high = my_tier - 1
    if low < 1:
        low = 1
    if high < 1:
        high = 1

    url = "https://solved.ac/api/v3/search/problem?query=tier:" + str(
        low) + ".." + str(
            high) + " !solved_by:" + bj_id + "&sort=random&direction=desc"
    res2 = requests.get(url, timeout=5)
    result = res2.json()

    title = "Easy 추천 (" + tier_names[low] + " ~ " + tier_names[high] + ")"
    await send_probs(ctx, result, title)


@bot.command()
async def 어려운문제(ctx):
    if ctx.author.id not in user_db or "bj_id" not in user_db[ctx.author.id]:
        await ctx.send("먼저 !등록 [아이디] 로 등록해주세요!")
        return

    bj_id = user_db[ctx.author.id]["bj_id"]
    res = requests.get("https://solved.ac/api/v3/user/show?handle=" + bj_id,
                       timeout=5)
    u_info = res.json()
    my_tier = u_info["tier"]

    low = my_tier + 1
    high = my_tier + 4
    if high > 30:
        high = 30

    url = "https://solved.ac/api/v3/search/problem?query=tier:" + str(
        low) + ".." + str(
            high) + " !solved_by:" + bj_id + "&sort=random&direction=desc"
    res2 = requests.get(url, timeout=5)
    result = res2.json()

    title = "Hard 추천 (" + tier_names[low] + " ~ " + tier_names[high] + ")"
    await send_probs(ctx, result, title)


@bot.command()
async def 오늘의문제(ctx):
    if ctx.author.id not in user_db or "bj_id" not in user_db[ctx.author.id]:
        await ctx.send("먼저 !등록 [아이디] 로 등록해주세요!")
        return

    bj_id = user_db[ctx.author.id]["bj_id"]
    res = requests.get("https://solved.ac/api/v3/user/show?handle=" + bj_id,
                       timeout=5)
    u_info = res.json()
    my_tier = u_info["tier"]

    low = my_tier - 2
    high = my_tier + 2
    if low < 1:
        low = 1
    if high > 30:
        high = 30

    url = "https://solved.ac/api/v3/search/problem?query=tier:" + str(
        low) + ".." + str(
            high) + " !solved_by:" + bj_id + "&sort=random&direction=desc"
    res2 = requests.get(url, timeout=5)
    result = res2.json()

    await send_probs(ctx, result, "오늘의 추천 문제")


@bot.command()
async def 검색(ctx, *, keyword=None):
    if keyword == None:
        await ctx.send("사용법: !검색  [검색어]")
        return

    url = "https://solved.ac/api/v3/search/problem?query=" + keyword + "&sort=solved&direction=desc"
    res = requests.get(url, timeout=5)
    result = res.json()

    await send_probs(ctx, result, "'" + keyword + "' 검색 결과")


async def send_probs(ctx, data, title):
    items = data.get("items", [])

    if len(items) == 0:
        await ctx.send("조건에 맞는 문제가 없습니다.")
        return

    msg = "" + title + "\n\n"
    count = 0

    for p in items:
        if count >= 3:
            break
        t_name = tier_names[p["level"]]
        solved_count = p["acceptedUserCount"]
        msg = msg + "" + p["titleKo"] + " (" + t_name + ")\n"
        msg = msg + "https://www.acmicpc.net/problem/" + str(
            p["problemId"]) + " | 맞은 사람: " + str(solved_count) + "명\n"
        msg = msg + "\n"
        count = count + 1

    await ctx.send(msg)


@bot.command()
async def 시작(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    try:
        await ctx.author.send(
            "명령어 목록\n"
            "\n"
            "!등록 [백준아이디] - 아이디 등록\n"
            "!내정보 - 내 solved.ac 정보 보기\n"
            "!설정 [티어코드] [태그1] [태그2] ... - 추천 설정\n"
            "!내설정 - 현재 설정 확인\n"
            "!추천 - 설정한 티어/태그로 문제 추천\n"
            "!쉬운문제 - 내 티어보다 쉬운 문제 추천\n"
            "!어려운문제 - 내 티어보다 어려운 문제 추천\n"
            "!오늘의문제 - 오늘의 랜덤 문제 추천\n"
            "!검색 [검색어] - 문제 검색\n"
            "!태그목록 - 사용 가능한 태그 목록\n"
            "\n"
            "티어 코드: b1~b5(브론즈), s1~s5(실버), g1~g5(골드), p1~p5(플래), d1~d5(다이아), r1~r5(루비)"
        )
    except:
        await ctx.send(ctx.author.mention + " DM을 열어두셔야 도움말을 받을 수 있어요!",
                       delete_after=5)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return


bot.run(TOKEN)
