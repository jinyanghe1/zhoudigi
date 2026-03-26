"""
种子数据：预置经典古文到数据库
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base
from app.models import Dynasty, Author, Article

Base.metadata.create_all(bind=engine)

DYNASTIES = [
    {"name": "先秦", "period": "远古-前221", "description": "诸子百家争鸣的时代"},
    {"name": "秦", "period": "前221-前207", "description": "大一统帝国"},
    {"name": "汉", "period": "前206-220", "description": "两汉经学鼎盛"},
    {"name": "三国", "period": "220-280", "description": "魏蜀吴三分天下"},
    {"name": "晋", "period": "265-420", "description": "士族文学兴盛"},
    {"name": "南北朝", "period": "420-589", "description": "文学自觉时代"},
    {"name": "唐", "period": "618-907", "description": "诗歌的黄金时代"},
    {"name": "宋", "period": "960-1279", "description": "词与散文的巅峰"},
    {"name": "元", "period": "1271-1368", "description": "戏曲文学勃兴"},
    {"name": "明", "period": "1368-1644", "description": "小说与散文繁荣"},
    {"name": "清", "period": "1644-1912", "description": "集大成与新变"},
]

ARTICLES = [
    {
        "author": "孔子及弟子", "dynasty": "先秦", "bio": "儒家学派创始人",
        "title": "论语·学而篇", "category": "语录",
        "content": (
            "子曰：「学而时习之，不亦说乎？有朋自远方来，不亦乐乎？"
            "人不知而不愠，不亦君子乎？」\n"
            "有子曰：「其为人也孝弟，而好犯上者，鲜矣；不好犯上，"
            "而好作乱者，未之有也。君子务本，本立而道生。"
            "孝弟也者，其为仁之本与！」\n"
            "子曰：「巧言令色，鲜矣仁！」\n"
            "曾子曰：「吾日三省吾身：为人谋而不忠乎？"
            "与朋友交而不信乎？传不习乎？」"
        ),
        "is_selected": True,
        "selection_reason": "儒学经典开篇，千古名篇"
    },
    {
        "author": "老子", "dynasty": "先秦", "bio": "道家学派创始人",
        "title": "道德经·第一章", "category": "哲学",
        "content": (
            "道可道，非常道；名可名，非常名。"
            "无名，天地之始；有名，万物之母。"
            "故常无欲，以观其妙；常有欲，以观其徼。"
            "此两者同出而异名，同谓之玄。玄之又玄，众妙之门。"
        ),
        "is_selected": True,
        "selection_reason": "道家思想根基，中国哲学基石"
    },
    {
        "author": "屈原", "dynasty": "先秦", "bio": "战国时期楚国诗人",
        "title": "离骚（节选）", "category": "诗赋",
        "content": (
            "帝高阳之苗裔兮，朕皇考曰伯庸。"
            "摄提贞于孟陬兮，惟庚寅吾以降。"
            "皇览揆余初度兮，肇锡余以嘉名。"
            "名余曰正则兮，字余曰灵均。"
            "纷吾既有此内美兮，又重之以修能。"
            "扈江离与辟芷兮，纫秋兰以为佩。"
            "汩余若将不及兮，恐年岁之不吾与。"
            "朝搴阰之木兰兮，夕揽洲之宿莽。"
            "日月忽其不淹兮，春与秋其代序。"
            "惟草木之零落兮，恐美人之迟暮。"
        ),
        "is_selected": True,
        "selection_reason": "中国浪漫主义文学的源头"
    },
    {
        "author": "庄子", "dynasty": "先秦", "bio": "道家学派代表人物",
        "title": "逍遥游（节选）", "category": "散文",
        "content": (
            "北冥有鱼，其名为鲲。鲲之大，不知其几千里也；"
            "化而为鸟，其名为鹏。鹏之背，不知其几千里也；"
            "怒而飞，其翼若垂天之云。是鸟也，海运则将徙于南冥。"
            "南冥者，天池也。齐谐者，志怪者也。谐之言曰："
            "「鹏之徙于南冥也，水击三千里，"
            "抟扶摇而上者九万里，去以六月息者也。」"
        ),
        "is_selected": True,
        "selection_reason": "庄子代表作，想象力雄奇"
    },
    {
        "author": "司马迁", "dynasty": "汉", "bio": "西汉史学家、文学家",
        "title": "报任安书（节选）", "category": "书信",
        "content": (
            "古者富贵而名摩灭，不可胜记，唯倜傥非常之人称焉。"
            "盖文王拘而演周易；仲尼厄而作春秋；屈原放逐，乃赋离骚；"
            "左丘失明，厥有国语；孙子膑脚，兵法修列；"
            "不韦迁蜀，世传吕览；韩非囚秦，说难孤愤；"
            "诗三百篇，大底圣贤发愤之所为作也。"
        ),
        "is_selected": True,
        "selection_reason": "司马迁的精神宣言，论述逆境与创作"
    },
    {
        "author": "贾谊", "dynasty": "汉", "bio": "西汉初年政论家、文学家",
        "title": "过秦论（上篇节选）", "category": "政论",
        "content": (
            "秦孝公据崤函之固，拥雍州之地，"
            "君臣固守以窥周室，有席卷天下，包举宇内，"
            "囊括四海之意，并吞八荒之心。当是时也，商君佐之，"
            "内立法度，务耕织，修守战之具；外连衡而斗诸侯。"
            "于是秦人拱手而取西河之外。"
        ),
        "is_selected": True,
        "selection_reason": "千古政论名篇"
    },
    {
        "author": "诸葛亮", "dynasty": "三国", "bio": "蜀汉丞相",
        "title": "出师表", "category": "奏章",
        "content": (
            "先帝创业未半而中道崩殂，今天下三分，益州疲弊，"
            "此诚危急存亡之秋也。然侍卫之臣不懈于内，"
            "忠志之士忘身于外者，盖追先帝之殊遇，"
            "欲报之于陛下也。诚宜开张圣听，以光先帝遗德，"
            "恢弘志士之气，不宜妄自菲薄，引喻失义，以塞忠谏之路也。\n"
            "宫中府中，俱为一体；陟罚臧否，不宜异同。"
            "若有作奸犯科及为忠善者，宜付有司论其刑赏，"
            "以昭陛下平明之理，不宜偏私，使内外异法也。"
        ),
        "is_selected": True,
        "selection_reason": "千古忠臣典范，感人至深"
    },
    {
        "author": "曹操", "dynasty": "三国", "bio": "政治家、军事家、诗人",
        "title": "短歌行", "category": "诗歌",
        "content": (
            "对酒当歌，人生几何！譬如朝露，去日苦多。\n"
            "慨当以慷，忧思难忘。何以解忧？唯有杜康。\n"
            "青青子衿，悠悠我心。但为君故，沉吟至今。\n"
            "呦呦鹿鸣，食野之苹。我有嘉宾，鼓瑟吹笙。\n"
            "明明如月，何时可掇？忧从中来，不可断绝。\n"
            "越陌度阡，枉用相存。契阔谈讌，心念旧恩。\n"
            "月明星稀，乌鹊南飞。绕树三匝，何枝可依？\n"
            "山不厌高，海不厌深。周公吐哺，天下归心。"
        ),
        "is_selected": True,
        "selection_reason": "建安风骨代表，气魄宏大"
    },
    {
        "author": "陶渊明", "dynasty": "晋", "bio": "田园诗派开创者",
        "title": "桃花源记", "category": "散文",
        "content": (
            "晋太元中，武陵人捕鱼为业。缘溪行，忘路之远近。"
            "忽逢桃花林，夹岸数百步，中无杂树，芳草鲜美，落英缤纷。"
            "渔人甚异之，复前行，欲穷其林。\n"
            "林尽水源，便得一山，山有小口，仿佛若有光。"
            "便舍船，从口入。初极狭，才通人。复行数十步，豁然开朗。"
            "土地平旷，屋舍俨然，有良田美池桑竹之属。"
            "阡陌交通，鸡犬相闻。其中往来种作，男女衣着，悉如外人。"
            "黄发垂髫，并怡然自乐。"
        ),
        "is_selected": True,
        "selection_reason": "千古名篇，理想社会的文学想象"
    },
    {
        "author": "王羲之", "dynasty": "晋", "bio": "书圣",
        "title": "兰亭集序", "category": "序",
        "content": (
            "永和九年，岁在癸丑，暮春之初，会于会稽山阴之兰亭，修禊事也。"
            "群贤毕至，少长咸集。此地有崇山峻岭，茂林修竹，"
            "又有清流激湍，映带左右，引以为流觞曲水，列坐其次。"
            "虽无丝竹管弦之盛，一觞一咏，亦足以畅叙幽情。\n"
            "是日也，天朗气清，惠风和畅。仰观宇宙之大，俯察品类之盛，"
            "所以游目骋怀，足以极视听之娱，信可乐也。"
        ),
        "is_selected": True,
        "selection_reason": "天下第一行书序文，文书双绝"
    },
    {
        "author": "韩愈", "dynasty": "唐", "bio": "古文运动领袖",
        "title": "师说", "category": "散文",
        "content": (
            "古之学者必有师。师者，所以传道受业解惑也。"
            "人非生而知之者，孰能无惑？惑而不从师，其为惑也，终不解矣。"
            "生乎吾前，其闻道也固先乎吾，吾从而师之；"
            "生乎吾后，其闻道也亦先乎吾，吾从而师之。"
            "吾师道也，夫庸知其年之先后生于吾乎？"
            "是故无贵无贱，无长无少，道之所存，师之所存也。"
        ),
        "is_selected": True,
        "selection_reason": "论从师之道，唐宋八大家名篇"
    },
    {
        "author": "柳宗元", "dynasty": "唐", "bio": "唐宋八大家之一",
        "title": "小石潭记", "category": "游记",
        "content": (
            "从小丘西行百二十步，隔篁竹，闻水声，如鸣珮环，心乐之。"
            "伐竹取道，下见小潭，水尤清冽。全石以为底，近岸，"
            "卷石底以出，为坻，为屿，为嵁，为岩。青树翠蔓，"
            "蒙络摇缀，参差披拂。\n"
            "潭中鱼可百许头，皆若空游无所依，日光下澈，影布石上。"
            "佁然不动，俶尔远逝，往来翕忽，似与游者相乐。\n"
            "潭西南而望，斗折蛇行，明灭可见。"
            "其岸势犬牙差互，不可知其源。\n"
            "坐潭上，四面竹树环合，寂寥无人，凄神寒骨，悄怆幽邃。"
            "以其境过清，不可久居，乃记之而去。"
        ),
        "is_selected": True,
        "selection_reason": "永州八记名篇，山水小品典范"
    },
    {
        "author": "杜牧", "dynasty": "唐", "bio": "晚唐诗人",
        "title": "阿房宫赋", "category": "赋",
        "content": (
            "六王毕，四海一，蜀山兀，阿房出。"
            "覆压三百余里，隔离天日。骊山北构而西折，直走咸阳。"
            "二川溶溶，流入宫墙。五步一楼，十步一阁；"
            "廊腰缦回，檐牙高啄；各抱地势，钩心斗角。"
            "盘盘焉，囷囷焉，蜂房水涡，矗不知其几千万落。"
            "长桥卧波，未云何龙？复道行空，不霁何虹？"
            "高低冥迷，不知西东。歌台暖响，春光融融；"
            "舞殿冷袖，风雨凄凄。一日之内，一宫之间，而气候不齐。"
        ),
        "is_selected": True,
        "selection_reason": "晚唐赋体名篇，以古鉴今"
    },
    {
        "author": "苏轼", "dynasty": "宋", "bio": "唐宋八大家之一",
        "title": "前赤壁赋", "category": "赋",
        "content": (
            "壬戌之秋，七月既望，苏子与客泛舟游于赤壁之下。"
            "清风徐来，水波不兴。举酒属客，诵明月之诗，歌窈窕之章。"
            "少焉，月出于东山之上，徘徊于斗牛之间。"
            "白露横江，水光接天。纵一苇之所如，凌万顷之茫然。"
            "浩浩乎如冯虚御风，而不知其所止；"
            "飘飘乎如遗世独立，羽化而登仙。"
        ),
        "is_selected": True,
        "selection_reason": "苏轼黄州杰作，哲理与文采并重"
    },
    {
        "author": "苏轼", "dynasty": "宋", "bio": "唐宋八大家之一",
        "title": "记承天寺夜游", "category": "散文",
        "content": (
            "元丰六年十月十二日夜，解衣欲睡，月色入户，欣然起行。"
            "念无与为乐者，遂至承天寺寻张怀民。怀民亦未寝，相与步于中庭。"
            "庭下如积水空明，水中藻荇交横，盖竹柏影也。"
            "何夜无月？何处无竹柏？但少闲人如吾两人者耳。"
        ),
        "is_selected": True,
        "selection_reason": "小品文经典，寥寥数语意境无穷"
    },
    {
        "author": "范仲淹", "dynasty": "宋", "bio": "北宋政治家、文学家",
        "title": "岳阳楼记", "category": "记",
        "content": (
            "庆历四年春，滕子京谪守巴陵郡。越明年，政通人和，百废具兴，"
            "乃重修岳阳楼，增其旧制，刻唐贤今人诗赋于其上。"
            "属予作文以记之。\n"
            "予观夫巴陵胜状，在洞庭一湖。衔远山，吞长江，"
            "浩浩汤汤，横无际涯；朝晖夕阴，气象万千。"
            "此则岳阳楼之大观也，前人之述备矣。"
            "然则北通巫峡，南极潇湘，迁客骚人，多会于此，"
            "览物之情，得无异乎？"
        ),
        "is_selected": True,
        "selection_reason": "先天下之忧而忧的千古名篇"
    },
    {
        "author": "欧阳修", "dynasty": "宋", "bio": "唐宋八大家之一",
        "title": "醉翁亭记", "category": "记",
        "content": (
            "环滁皆山也。其西南诸峰，林壑尤美，望之蔚然而深秀者，琅琊也。"
            "山行六七里，渐闻水声潺潺而泻出于两峰之间者，酿泉也。"
            "峰回路转，有亭翼然临于泉上者，醉翁亭也。"
            "作亭者谁？山之僧智仙也。名之者谁？太守自谓也。"
            "太守与客来饮于此，饮少辄醉，而年又最高，故自号曰醉翁也。"
            "醉翁之意不在酒，在乎山水之间也。山水之乐，得之心而寓之酒也。"
        ),
        "is_selected": True,
        "selection_reason": "欧阳修代表作，文风从容典雅"
    },
    {
        "author": "刘基", "dynasty": "明", "bio": "明初政治家、文学家",
        "title": "卖柑者言", "category": "寓言",
        "content": (
            "杭有卖果者，善藏柑，涉寒暑不溃。出之烨然，玉质而金色。"
            "置于市，贾十倍，人争鬻之。予贸得其一，剖之，"
            "如有烟扑口鼻，视其中，干若败絮。"
        ),
        "is_selected": True,
        "selection_reason": "寓言名篇，讽刺金玉其外败絮其中"
    },
    {
        "author": "袁枚", "dynasty": "清", "bio": "清代诗人、散文家",
        "title": "黄生借书说", "category": "散文",
        "content": (
            "黄生允修借书。随园主人授以书，而告之曰：\n"
            "书非借不能读也。子不闻藏书者乎？"
            "七略、四库，天子之书，然天子读书者有几？"
            "汗牛塞屋，富贵家之书，然富贵人读书者有几？"
            "其他祖父积、子孙弃者无论焉。"
        ),
        "is_selected": True,
        "selection_reason": "论读书之道，见解独到"
    },
    {
        "author": "龚自珍", "dynasty": "清", "bio": "清代思想家、文学家",
        "title": "病梅馆记", "category": "散文",
        "content": (
            "江宁之龙蟠，苏州之邓尉，杭州之西溪，皆产梅。"
            "或曰：「梅以曲为美，直则无姿；以欹为美，正则无景；"
            "以疏为美，密则无态。」固也。"
            "此文人画士，心知其意，未可明诏大号以绳天下之梅也；"
            "又不可以使天下之民斫直，删密，锄正，"
            "以夭梅病梅为业以求钱也。"
        ),
        "is_selected": True,
        "selection_reason": "以梅喻人，批判束缚个性的社会风气"
    },
]


def seed():
    db = SessionLocal()
    try:
        if db.query(Dynasty).count() > 0:
            print("数据库已有数据，跳过种子数据导入")
            print(f"  朝代: {db.query(Dynasty).count()}")
            print(f"  作者: {db.query(Author).count()}")
            print(f"  文章: {db.query(Article).count()}")
            return

        # 导入朝代
        dynasty_map = {}
        for d in DYNASTIES:
            dynasty = Dynasty(name=d["name"], period=d["period"], description=d["description"])
            db.add(dynasty)
            db.flush()
            dynasty_map[d["name"]] = dynasty.id
            print(f"  + 朝代: {d['name']}")

        # 导入作者和文章
        author_cache = {}
        article_count = 0
        for entry in ARTICLES:
            dynasty_id = dynasty_map.get(entry["dynasty"])
            author_key = entry["author"]

            if author_key not in author_cache:
                author = Author(
                    name=entry["author"],
                    dynasty_id=dynasty_id,
                    bio=entry.get("bio", "")
                )
                db.add(author)
                db.flush()
                author_cache[author_key] = author.id
                print(f"  + 作者: {entry['author']} ({entry['dynasty']})")

            article = Article(
                title=entry["title"],
                content=entry["content"],
                category=entry.get("category", ""),
                author_id=author_cache[author_key],
                dynasty_id=dynasty_id,
                is_selected=entry.get("is_selected", False),
                selection_reason=entry.get("selection_reason", ""),
                word_count=len(entry["content"]),
                source="seed_data"
            )
            db.add(article)
            article_count += 1

        db.commit()
        print(f"\n  种子数据导入完成!")
        print(f"  朝代: {len(DYNASTIES)}, 作者: {len(author_cache)}, 文章: {article_count}")

    except Exception as e:
        db.rollback()
        print(f"  导入失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("  导入找到古籍种子数据...\n")
    seed()
