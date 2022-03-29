from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime
import random
import logging
import sys

logger = logging.getLogger("My_first_logger")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.ERROR)
file_handler = logging.FileHandler("./logger/DB_logger.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.debug("Logger created and configured!")

engine = create_engine('postgresql://egor:krasnov@Localhost:5432/dockerHW_db')
Base = declarative_base()
# logger.info("DataBase created!")


class Heroes(Base):
    __tablename__ = "heroes"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    side = Column(String(30))
    birthday = Column(DateTime(timezone=True))
    moto = relationship("Motos", cascade="all, delete")
    story = relationship("Stories", uselist=False, cascade="all, delete")

    def __repr__(self):
        return f"{self.id}: {self.name} {self.side}"


class Motos(Base):
    __tablename__ = "motos"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    hero_id = Column(Integer, ForeignKey("heroes.id"))
    moto_id = Column(Integer)
    moto = Column(String(400))

    def __repr__(self):
        return f"{self.moto_id}: {self.moto}"


class Stories(Base):
    __tablename__ = "stories"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    hero_id = Column(Integer, ForeignKey("heroes.id"))
    story = Column(String(1000))

    def __repr__(self):
        return f"{self.id}: {self.story}"


class Fights(Base):
    __tablename__ = "hero_fights"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)

    hero_1_id = Column(Integer, ForeignKey("heroes.id", ondelete='SET NULL'), nullable=True)
    hero_2_id = Column(Integer, ForeignKey("heroes.id", ondelete='SET NULL'), nullable=True)
    hero_1_moto_id = Column(Integer, ForeignKey("motos.id", ondelete='SET NULL'), nullable=True)
    hero_2_moto_id = Column(Integer, ForeignKey("motos.id", ondelete='SET NULL'), nullable=True)
    winner = Column(Integer)

    hero_1 = relationship("Heroes", foreign_keys=[hero_1_id])
    hero_2 = relationship("Heroes", foreign_keys=[hero_2_id])
    hero_1_moto = relationship("Motos", foreign_keys=[hero_1_moto_id])
    hero_2_moto = relationship("Motos", foreign_keys=[hero_2_moto_id])

    def __repr__(self):
        return f"{self.hero_1} with moto {self.hero_1_moto} vs {self.hero_2} " \
               f"with moto {self.hero_2_moto} and winner {self.winner} "


def autoincriment_for_moto(hero_id):
    with Session() as session:
        tmp = session.query(func.max(Motos.moto_id)).filter(Motos.hero_id == hero_id).scalar()
        session.commit()
        if tmp is None:
            return 1
        else:
            return 1 + tmp


def fill_base():
    with Session() as session:
        session.add(Heroes(name="Albus Dumbledore", side="Order of the Phoenix", birthday=datetime.date(1881, 8, 25)))
        session.add(Heroes(name="Sirius Black III", side="Order of the Phoenix", birthday=datetime.date(1959, 11, 3)))
        session.add(Heroes(name="Hary Potter", side="Order of the Phoenix", birthday=datetime.date(1980, 7, 30)))
        session.commit()
        session.add(Stories(hero_id=1,
                            story="He was the son of Percival and Kendra Dumbledore, and the elder brother of "
                                  "Aberforth and Ariana. His father died in Azkaban when Albus was young, while "
                                  "his mother and sister were later accidentally killed. His early losses greatly "
                                  "affected him early on, even at his death many years later, but, in turn, made him "
                                  "a better person."))
        session.add(Stories(hero_id=2,
                            story="He was an English pure-blood wizard, the older son of Orion and Walburga Black, the"
                                  " brother of Regulus Black, and godfather of Harry Potter. Although he was the heir "
                                  "of the House of Black, Sirius disagreed with his family's belief in blood purity and"
                                  " defied tradition when he was Sorted into Gryffindor House instead of Slytherin at "
                                  "Hogwarts School of Witchcraft and Wizardry, which he attended from 1971 to 1978. "
                                  "As the rest of his family had been in Slytherin, he was the odd one out."))
        session.add(Stories(hero_id=3,
                            story="The majority of the books' plot covers seven years in the life of the orphan Harry, "
                                  "who, on his eleventh birthday, learns he is a wizard. Thus, he attends "
                                  "Hogwarts School of Witchcraft and Wizardry to practise magic under the guidance of "
                                  "the kindly headmaster Albus Dumbledore and other school professors along with his "
                                  "best friends Ron Weasley and Hermione Granger. "))

        session.add(Motos(hero_id=1, moto="It does not do to dwell on dreams and forget to live.",
                          moto_id=autoincriment_for_moto(1)))
        session.commit()
        session.add(Motos(hero_id=1,
                          moto="It takes a great deal of bravery to stand up to our enemies, "
                               "but just as much to stand up to our friends.",
                          moto_id=autoincriment_for_moto(1)))
        session.commit()
        session.add(Motos(hero_id=1, moto="One can never have enough socks.", moto_id=autoincriment_for_moto(1)))
        session.add(Motos(hero_id=2,
                          moto="If you want to know what a man’s like, take a good look at "
                               "how he treats his inferiors, not his equals.",
                          moto_id=autoincriment_for_moto(2)))
        session.commit()
        session.add(
            Motos(hero_id=2, moto="The ones that love us never really leave us. You can always find them in here.",
                  moto_id=autoincriment_for_moto(2)))
        session.add(
            Motos(hero_id=3, moto="There’s no need to call me ‘sir,’ Professor.", moto_id=autoincriment_for_moto(3)))

        session.add(Heroes(name="Lord Voldemort", side="Death Eaters", birthday=datetime.date(1926, 12, 6)))
        session.add(
            Heroes(name="Bellatrix \"Bella\" Lestrange", side="Death Eaters", birthday=datetime.date(1951, 1, 1)))
        session.add(Heroes(name="Peter Pettigrew", side="Death Eaters", birthday=datetime.date(1959, 9, 1)))

        session.add(Stories(hero_id=4,
                            story="Voldemort is the archenemy of Harry Potter, who according to a prophecy "
                                  "has the power to vanquish the Dark Lord. He attempts to murder the boy, but "
                                  "instead kills his parents, Lily and James Potter, and leaves Harry with a scar "
                                  "on his forehead in the shape of a lightning bolt."))
        session.add(Stories(hero_id=5,
                            story="British witch, the eldest daughter of Cygnus and Druella Black, cousin of Regulus"
                                  " and Sirius Black, and the elder sister of Andromeda Tonks and Narcissa Malfoy."
                                  " She was a member of the House of Black, an old wizarding family and one of the "
                                  "Sacred Twenty-Eight. Bellatrix started her education at Hogwarts School of "
                                  "Witchcraft and Wizardry in the early sixties (either 1962 or 1963), and was "
                                  "Sorted into Slytherin House."))
        session.add(Stories(hero_id=6,
                            story="He was a wizard and the son of Mr and Mrs Pettigrew. He began attending Hogwarts "
                                  "School of Witchcraft and Wizardry in 1971 and was sorted into Gryffindor House "
                                  "after the Sorting Hat pondered over which house he belonged in for over five minutes"
                                  ", making him a true Hatstall. During his years at Hogwarts, he became one of the "
                                  "Marauders; he was best friends with Sirius Black, James Potter, and Remus Lupin, "
                                  "and together they created the Marauder's Map."))

        session.add(Motos(hero_id=4, moto="I'm going to kill you, Harry Potter.", moto_id=autoincriment_for_moto(4)))
        session.commit()
        session.add(Motos(hero_id=4, moto="There is no good and evil.", moto_id=autoincriment_for_moto(4)))
        session.add(Motos(hero_id=5, moto="How dare you defy your master!", moto_id=autoincriment_for_moto(5)))
        session.commit()
        session.add(Motos(hero_id=5, moto="My Lord, I'd like to volunteer for this task.",
                          moto_id=autoincriment_for_moto(5)))
        session.add(Motos(hero_id=6, moto="Remus, S-Sirius? My old friends!", moto_id=autoincriment_for_moto(6)))
        session.commit()
        logger.info("DataBase filled with standart heroes!")


def hero_adder(name_input, side_input, date_input):
    with Session() as session:
        birthday_date = date_input.split(".")
        session.add(Heroes(name=name_input, side=side_input,
                           birthday=datetime.date(int(birthday_date[0]), int(birthday_date[1]), int(birthday_date[2]))))
        session.commit()
        logger.info('Hero %s added', name_input)
        print('Hero added!')


def moto_adder(info):
    tmp = info.split()
    with Session() as session:
        if hero_checker(tmp[0]):
            return 1
        session.add(Motos(hero_id=tmp[0], moto=tmp[1:], moto_id=autoincriment_for_moto(tmp[0])))
        session.commit()
        logger.info('Moto %s for Hero %s added', tmp[1:], tmp[0])
        print('Moto added!')


def story_adder(info):
    tmp = info.split()
    with Session() as session:
        if hero_checker(tmp[0]):
            return 1
        session.add(Stories(hero_id=tmp[0], story=tmp[1:]))
        session.commit()
        logger.info('Story for Hero %s added', tmp[0])
        print('Story added!')


def fight_adder():
    with Session() as session:
        first_hero = session.query(Heroes).order_by(func.random()).first()
        first_hero_moto = session.query(Motos).filter(Motos.hero_id == first_hero.id).order_by(func.random()).first()

        second_hero = session.query(Heroes).filter(Heroes.side != first_hero.side).order_by(func.random()).first()
        second_hero_moto = session.query(Motos).filter(Motos.hero_id == second_hero.id).order_by(func.random()).first()
        random_winner = random.randint(0, 2)
        session.add(Fights(hero_1_id=first_hero.id, hero_2_id=second_hero.id,
                           hero_1_moto_id=first_hero_moto.id, hero_2_moto_id=second_hero_moto.id,
                           winner=random_winner))
        session.commit()
        if random_winner != 0:
            logger.info('Fight between Hero with id %s and id %s added. Winner is %s', first_hero.id, second_hero.id,
                        random_winner)


def hero_deleter(info):
    with Session() as session:
        if hero_checker(info):
            return 1
        tmp = session.query(Heroes).filter(Heroes.id == info).one()
        session.delete(tmp)
        session.commit()
        print(f'Hero with id {info} deleted!')
        logger.info('Hero with id %s deleted!', info)


def hero_checker(hero_id_input):
    with Session() as session:
        tmp = session.query(Heroes).filter(Heroes.id == hero_id_input).count()
        if tmp == 0:
            error = 'No such Hero in Database!'
            logger.error(error)
            print(error)
            session.commit()
            return 1
        session.commit()


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

if len(sys.argv) > 1:
    fill_base()

mode_description = "Please select mode: \n1 - add Hero \n2 - add Moto \n3 - add random Fight! \n" \
                   "4 - add Story \n5 - delete Hero \n6 or q - save & exit\nhelp - for repeat info\n" \
                    "heroes - to get id's\nfights - to get all fights\nmotos - to get all motos"
print("You are welcome in HP database.", mode_description)
mode = input()
while mode != '6' and mode != 'q':
    match mode.split():
        case ['1']:
            name = input("Enter the hero's name\n")
            side = input("Enter the hero's side\n")
            date = input("Enter the hero's date of birth (YYYY.MM.DD)\n")
            hero_adder(name, side, date)
        case ['2']:
            tmp = input("Enter the hero's id and moto\n")
            moto_adder(tmp)
        case ['3']:
            fight_adder()
            print('Fight added!')
        case ['4']:
            tmp = input("Enter the hero's id and story\n")
            story_adder(tmp)
        case ['5']:
            tmp = input("Enter the hero's id\n")
            hero_deleter(tmp)
        case ['help']:
            print(mode_description)
        case ["heroes"]:
            with Session() as session:
                for hero in session.query(Heroes).all():
                    print(hero)
                session.commit()
        case ["fights"]:
            with Session() as session:
                for fight in session.query(Fights).all():
                    print(fight)
                session.commit()
        case ["motos"]:
            with Session() as session:
                for moto in session.query(Motos).all():
                    print(moto)
                session.commit()
        case ["fill"]:
            fill_base()
    mode = input()
print('Goodbye!')
