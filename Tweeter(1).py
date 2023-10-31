import random

from neo4j import GraphDatabase
import streamlit as st
import datetime
import numpy as np
import re
class HelloWorldExample:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.uri = uri
        self.user = user
        self.password = password

    def close(self):
        self.driver.close()

    def print_greeting(self, message, create=True):
        with self.driver.session() as session:
            if create:
                greeting = session.write_transaction(self._create_and_return_greeting, message)
            else:
                greeting = session.write_transaction(self._match_and_return_greeting, message)
            print(greeting)

    # Generate a random timestamp

    # Generate a random sentence
    def generate_sentence(self):
        subjects = ["I", "You", "We", "They", "He", "She", "It", "John", "Mary", "The team", "The company"]
        verbs = ["ate", "ran", "walked", "slept", "jumped", "wrote", "spoke", "built", "created", "played"]
        objects = ["apple", "car", "book", "dog", "cat", "ball", "house", "tree", "computer", "table"]
        subject = random.choice(subjects)
        verb = random.choice(verbs)
        obj = random.choice(objects)
        return f"{subject} {verb} the {obj}."

    def generate_url(self):
        subjects = ["I", "You", "We", "They", "He", "She", "It", "John", "Mary", "The team", "The company"]
        verbs = ["ate", "ran", "walked", "slept", "jumped", "wrote", "spoke", "built", "created", "played"]
        objects = ["apple", "car", "book", "dog", "cat", "ball", "house", "tree", "computer", "table"]
        subject = random.choice(subjects)
        verb = random.choice(verbs)
        obj = random.choice(objects)
        return f"https://{subject}{obj}.com"

    def generate_random_timestamp(self):
        start = datetime.datetime(2022, 1, 1)
        end = datetime.datetime.now()
        delta = end - start
        total_seconds = int(delta.total_seconds())
        random_seconds = random.randint(0, total_seconds)
        return start + datetime.timedelta(seconds=random_seconds)

    # CREATE OR ADD NEW ENTRIES(POST)
    def adduser(self,name,bio,usertag,mail,year,month,date):
        with self.driver.session() as session:
            result=session.write_transaction(self._add_user,name,bio,usertag,mail,year,month,date)
            return result
    def addpost(self, user,tags,mentions,content):
        with self.driver.session() as session:
            session.write_transaction(self._add_post, user,tags,mentions,content)

    def likepost(self, user, post_id):
        with self.driver.session() as session:
            session.write_transaction(self._like_post, user, post_id)

    def addrepost(self, user, post_id):
        with self.driver.session() as session:
            session.write_transaction(self._add_repost, user, post_id)

    def addquote(self, user1, post_id,content,media):
        with self.driver.session() as session:
            session.write_transaction(self._add_quote, user1, post_id,content,media)

    def addreply(self, user1, post_id,content,media):
        with self.driver.session() as session:
            session.write_transaction(self._add_reply, user1, post_id,content,media)

    def followuser(self, user1, user2):
        with self.driver.session() as session:
            session.write_transaction(self._follow_user, user1, user2)

    # DELETE ENTRIES
    def deluser(self, user):
        with self.driver.session() as session:
            session.write_transaction(self._del_user, user)

    def delpost(self, postid):
        with self.driver.session() as session:
            session.write_transaction(self._del_post, postid)

    def dellikepost(self, user, post_id):
        with self.driver.session() as session:
            session.write_transaction(self._del_like_post, user, post_id)

    def delrepost(self, user, post_id):
        with self.driver.session() as session:
            session.write_transaction(self._del_repost, user, post_id)

    def delquote(self, user1, post_id):
        with self.driver.session() as session:
            session.write_transaction(self._del_quote, user1, post_id)

    def delreply(self, user1, post_id):
        with self.driver.session() as session:
            session.write_transaction(self._del_reply, user1, post_id)

    def delfollowuser(self, user1, user2):
        with self.driver.session() as session:
            session.write_transaction(self._del_follow_user, user1, user2)

    # READING EXISTING ENTRIES (GET)

    def getuser(self, name):
        with self.driver.session() as session:
            user = session.write_transaction(self._get_user, name)
            return user

    def getpost(self, postid):
        with self.driver.session() as session:
            post = session.write_transaction(self._get_post, postid)
            return post

    def getnumlikes(self, postid):
        with self.driver.session() as session:
            post = session.write_transaction(self._get_numlikes, postid)
            return post

    def getlikedposts(self, user):
        with self.driver.session() as session:
            liked = session.write_transaction(self._get_liked, user)
            return liked

    def getfollowing(self, user):
        with self.driver.session() as session:
            follow = session.write_transaction(self._get_following, user)
            return follow
    def getfollowers(self, user):
        with self.driver.session() as session:
            follow = session.write_transaction(self._get_followers, user)
            return follow

    def getrepost(self, user, postid):
        with self.driver.session() as session:
            repost = session.write_transaction(self._get_reposts, user, postid)
            print(repost)

    def getquote(self, user, postid):
        with self.driver.session() as session:
            quote = session.write_transaction(self._get_quote, user, postid)
            return quote

    def getreplies(self, postid):
        with self.driver.session() as session:
            quote = session.write_transaction(self._get_replies, postid)
            return quote

    def updateuser(self, olduser):
        with self.driver.session() as session:
            session.write_transaction(self._update_user, olduser)

    # Advanced Features
    #     Follower Recommendation system

    def recommendfollowers(self, user, num=5, distance=2):
        with self.driver.session() as session:
            quote = session.write_transaction(self._get_recommend, user, num, distance)
            return quote

    def FollowingFeed(self, user, num=5):
        with self.driver.session() as session:
            quote = session.write_transaction(self._get_foll_feed, user)
            return quote

    def ForYouFeed(self, user, num=5):
        with self.driver.session() as session:
            quote = session.write_transaction(self._get_foryou_feed, user)
            return quote

    #     Creating the database

    def create_rel(self):
        with self.driver.session() as session:
            session.write_transaction(self._create_and_return_relations)

    def create_follow(self):
        with self.driver.session() as session:
            session.write_transaction(self._create_follow)

    def create_reposts(self):
        with self.driver.session() as session:
            session.write_transaction(self._create_reposts)

    def create_quotes(self):
        with self.driver.session() as session:
            session.write_transaction(self._create_quotes)

    def create_replies(self):
        with self.driver.session() as session:
            session.write_transaction(self._create_reply)

    def create_likes(self):
        with self.driver.session() as session:
            session.write_transaction(self._create_liked)

    # QUERIES FOR RESPECTIVE FUNCTIONS

    def is_valid_email(self,email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def is_valid_age(self,created, DOB):
        DOB_string = DOB.strftime("%Y-%m-%d")
        dob = datetime.datetime.strptime(DOB_string, "%Y-%m-%d")
        # created = datetime.strptime(created, "%Y-%m-%d")
        age = created.year - dob.year - ((created.month, created.day) < (dob.month, dob.day))
        return age >= 12

    def _add_user(self, tx,name,bio,usertag,registered_mail,DOB_year,DOB_month,DOB_date):
        # name = input("Enter name: ")
        # bio = input("Enter bio: ")
        # usertag = input("Enter unique tag: ")
        # registered_mail = input("Enter your registered mail: ")
        # DOB_year = int(input("Enter the year of birth"))
        # DOB_month = int(input("Enter the month of birth"))
        # DOB_date = int(input("Enter the date of birth"))
        DOB = datetime.date(DOB_year, DOB_month, DOB_date)
        created = datetime.datetime.now()
        if(self.is_valid_email(registered_mail) and self.is_valid_age(created,DOB)):

            tx.run(
                "CREATE (n:User{name:$name,user_tag:$usertag,Bio:$bio,registered_mail:$reg_mail,created:$created,Dob:$DOB})"
                "RETURN n", name=name, usertag=usertag, bio=bio, reg_mail=registered_mail, created=created, DOB=DOB
                )
            return True
        else:
            st.write(":red[Invalid Email]")
            return False

    def _add_post(self, tx, user,tags,mentions,content):
        created = datetime.datetime.now()
        # tags = input("Enter tags of the post: ")
        # mentions = input("Enter who you want to mention: ")
        # content = input("Enter body of the post: ")
        id1 = str(len(self.get_all_posts()) + 1)
        #         content=self.generate_sentence()
        tx.run("MATCH (n:User{name:$user})"
               "CREATE (n)-[:POSTED{timestamp:$time}]->(p:Post{hash_tags:$tags,mentions:$mentioned,postid:$id1,tweet_content:$content})",
               user=user, time=created, tags=tags, mentioned=mentions, id1=id1, content=content
               )

    def _like_post(self, tx, user, id1):
        likedat = datetime.datetime.now()
        print(id1)
        tx.run(
            "MATCH (n:User {name: $user}), (p:Post {postid: $id1}) "
            "CREATE (n)-[:LIKES {timestamp: $time}]->(p)",
            user=user, id1=id1, time=likedat
        )

    def _follow_user(self, tx, user1, user2):
        tx.run("MATCH (n:User{name:$user1}),(m:User{name:$user2})"
               "CREATE (n)-[:FOLLOWS]->(m)", user1=user1, user2=user2
               )

    def _add_repost(self, tx, user, id1):
        likedat = datetime.datetime.now()
        print(id1)
        tx.run(
            "MATCH (n:User {name: $user}), (p:Post {postid: $id1}) "
            "CREATE (n)-[:REPOSTED {timestamp: $time}]->(p)",
            user=user, id1=id1, time=likedat
        )

    def _add_quote(self, tx, user, id1,content,media):
        likedat = datetime.datetime.now()
        print(id1)
        # content = input("Enter the content of quote: ")
        # media = input("Enter media link: ")
        tx.run(
            "MATCH (n:User {name: $user}), (p:Post {postid: $id1}) "
            "CREATE (n)-[:QUOTES {timestamp: $time,content:$content,media:$media}]->(p)",
            user=user, id1=id1, time=likedat, content=content, media=media
        )

    def _add_reply(self, tx, user, id1,content,media):
        likedat = datetime.datetime.now()
        print(id1)
        # content = input("Enter the content of quote: ")
        # media = input("Enter media link: ")
        tx.run(
            "MATCH (n:User {name: $user}), (p:Post {postid: $id1}) "
            "CREATE (n)-[:REPLIED {timestamp: $time,content:$content,media:$media}]->(p)",
            user=user, id1=id1, time=likedat, content=content, media=media
        )

    def _get_user(self, tx, name):
        result = tx.run("MATCH (a:User{name:$name}) "
                        "RETURN a", name=name)
        return result.single()[0]

    def _get_post(self, tx, postid):
        result = tx.run("MATCH (a:Post{postid:$name}) "
                        "RETURN a", name=postid)
        return result.single()[0]

    def _get_liked(self, tx, user):
        with self.driver.session() as session:
            result = session.run("MATCH (u:User {name: $user})-[:LIKES]->(p:Post) RETURN p.postid, p.tweet_content",
                                 user=user)
            return [record for record in result]

    def _get_following(self, tx, user):
        result = tx.run("MATCH (u:User {name: $user})-[:FOLLOWS]->(p:User) RETURN p", user=user)
        return [record['p'] for record in result]

    def _get_followers(self, tx, user):
        result = tx.run("MATCH (u:User {name: $user})<-[:FOLLOWS]-(p:User) RETURN p", user=user)
        return [record['p'] for record in result]

    def _get_reposts(self, tx, user, postid):
        print('HI')
        result = tx.run("MATCH (u:User{name:$user})-[r:REPOSTED]->(p:Post) RETURN p.postid", user=user)
        return [record for record in result]

    def _get_quote(self, tx, user, postid):
        print('HI')
        result = tx.run("MATCH (u:User{name:$user})-[r:QUOTES]->(p:Post{postid:$postid}) RETURN r", user=user,
                        postid=postid)
        print(result)
        return [record for record in result]

    def _get_replies(self, tx, postid):
        print('HI')
        result = tx.run("MATCH (u:User)-[r:REPLIED]->(p:Post{postid:$postid}) RETURN u.name,r",
                        postid=postid)
        return [record for record in result]

    def _del_user(self, tx, user):
        result = tx.run('MATCH (u:User {name:$name})'
                        'OPTIONAL MATCH (u)-[r1]-()'
                        'OPTIONAL MATCH (p:Post)<-[r2:POSTED]-(u)'
                        'OPTIONAL MATCH (p)-[r3]-()'
                        'DETACH DELETE u, p, r1, r2', name=user
                        )

    def _del_post(self, tx, postid):
        result = tx.run('MATCH (p:Post{postid:$postid})'
                        'DETACH DELETE p', postid=postid
                        )

    def _del_like_post(self, tx, user, postid):
        result = tx.run('MATCH (n:User{name:$name})-[r:LIKES]->(p:Post{postid:$postid})'
                        'DELETE r', name=user, postid=postid
                        )

    def _del_repost(self, tx, user, postid):
        result = tx.run('MATCH (n:User{name:$name})-[r:REPOSTED]->(p:Post{postid:$postid})'
                        'DELETE r', name=user, postid=postid
                        )

    def _del_quote(self, tx, user, postid):
        result = tx.run('MATCH (n:User{name:$name})-[r:QUOTES]->(p:Post{postid:$postid})'
                        'DELETE r', name=user, postid=postid
                        )
    def _del_reply(self, tx, user, postid):
        result = tx.run('MATCH (n:User{name:$name})-[r:REPLIED]->(p:Post{postid:$postid})'
                        'DELETE r', name=user, postid=postid
                        )

    def _del_follow_user(self, tx, user1, user2):
        result = tx.run('MATCH (u1:User{name:$user1})-[r:FOLLOWS]->(u2:User{name:$user2})'
                        'DELETE r', user1=user1, user2=user2
                        )

    def _get_numlikes(self, tx, postid):
        result = tx.run('match (p:Post{postid:$id1}) <-[:LIKES]- (m:User) '
                        'return size(collect(m))', id1=postid
                        )
        return result.single()[0]

    def _update_user(self, tx, olduser):
        upt = input("What do you want to update(Username/Bio/DOB)")
        if (upt == 'Username'):
            newuser = input('Enter new username: ')
            result = tx.run('MATCH (p:User {name:$olduser})'
                            'SET p.name = $newuser', olduser=olduser, newuser=newuser
                            )
        elif (upt == 'Bio'):
            bio = input('Enter your new bio: ')
            result = tx.run('MATCH (p:User {name: $user})'
                            'SET p.Bio=$bio', user=olduser, bio=bio)

    #         elif(upt=='DOB'):

    # Advanced functions Implementation
    def _get_recommend(self, tx, user, num, distance):
        result = tx.run(
            "MATCH (n:User {name: $user})-[:FOLLOWS*2..2]->(mutual:User) "
            "WITH mutual AS mutuals, COUNT(*) AS NumOfMutuals, n.name as Me "
            "RETURN mutuals "
            "ORDER BY NumOfMutuals DESC "
            "LIMIT $num",
            user=user, num=num
        )
        return [record['mutuals'] for record in result]

    def _get_foll_feed(self, tx, user):
        result = tx.run(
            "MATCH (n:User {name: $name})-[:FOLLOWS]->(m:User) "
            "OPTIONAL MATCH (m)-[:POSTED]->(p:Post) "
            "RETURN p AS posts",
            name=user
        )
        return [record['posts'] for record in result]

    #     def _get_foryou_feed(self,txt,user):
    #         result=tx.run("MATCH (p1:User {name: 'Daniel Moore'})-[:LIKES]->(posts:Post)<-[:LIKES]-(p2:User)"
    #                 "WHERE p2 <> p1"
    #                 "WITH p2, count(posts) as likedCount,p1"
    #                 "ORDER BY likedCount DESC"
    #                 "RETURN p2.name, likedCount,p1.name"
    #                 "LIMIT 5",
    #                 )
    #         return [record[''] for record in result

    def _get_foryou_feed(self, tx, user):
        result = tx.run(
            "MATCH (p1:User {name: $user})-[:LIKES]->(posts:Post)<-[:LIKES]-(p2:User)-[:LIKES]->(similarPosts:Post) "
            "WHERE p1.name > p2.name "
            "WITH p2, COLLECT(DISTINCT similarPosts) AS recommendations "
            "MATCH (p2)-[:LIKES]->(recommendedPosts:Post) "
            "WHERE NOT recommendedPosts IN recommendations "
            "RETURN p2.name AS User, COLLECT(DISTINCT recommendedPosts) AS RecommendedPosts",
            user=user
        )
        return [record['RecommendedPosts'] for record in result]

    # BULK FUNCTIONS( Don't reuse it to avoid reinclusions)

    def get_all_posts(self):
        with self.driver.session() as session:
            result = session.run("MATCH (p:Post) RETURN p")
            return [record['p'] for record in result]

    def get_all_users(self):
        with self.driver.session() as session:
            result = session.run("MATCH (u:User) RETURN u")
            return [record['u'] for record in result]

    def postbyuser(self, name):
        with self.driver.session() as session:
            result = session.run("MATCH (u:User{name:$name1})-[:POSTED]->(m:Post) RETURN m", name1=name)
            return [record['m'] for record in result]

    def quotebyuser(self, name):
        with self.driver.session() as session:
            result = session.run("MATCH (u:User{name:$name1})-[q:QUOTES]->(m:Post) RETURN q,m", name1=name)
            return [(record['q'], record['m']) for record in result]

    def repostbyuser(self, name):
        with self.driver.session() as session:
            result = session.run("MATCH (u:User{name:$name1})-[q:REPOSTED]->(m:Post) RETURN m,q", name1=name)
            return [(record['q'], record['m']) for record in result]

    def replybyuser(self, name):
        with self.driver.session() as session:
            result = session.run("MATCH (u:User{name:$name1})-[r:REPLIED]->(m:Post) RETURN r, m.postid", name1=name)
            return [(record['r'], record['m.postid']) for record in result]

    def _create_follow(self, tx):
        users = self.get_all_users()
        for i in users:
            num = np.random.randint(10, size=1)[0]  # Retrieve the integer value from the NumPy array
            follows = random.sample(users, k=num)
            for user in follows:
                if user['name'] != i['name']:  # To prevent a user from following themselves
                    #                     print(user['name'])
                    tx.run("MATCH (u1:User {name: $name1}), (u2:User {name: $name2}) "
                           "CREATE (u1)-[:FOLLOWS]->(u2)", name1=i['name'], name2=user['name'])

    def _create_liked(self, tx):
        users = self.get_all_users()
        posts = self.get_all_posts()
        for i in users:
            num = np.random.randint(15, size=1)[0]  # Retrieve the integer value from the NumPy array
            likes = random.sample(posts, k=num)
            for user in likes:
                if user['name'] != i['name']:  # To prevent a user from following themselves
                    #                     print(user['name'])
                    time = self.generate_random_timestamp()
                    tx.run("MATCH (u1:User {name: $name1}), (u2:Post {postid: $name2}) "
                           "CREATE (u1)-[:LIKES{timestamp:$time}]->(u2)", name1=i['name'], name2=user['postid'],
                           time=time)

    def _create_reposts(self, tx):
        posts = self.get_all_posts()
        users = self.get_all_users()
        for i in users:
            p1 = self.postbyuser(i['name'])
            s = set(p1)
            temp3 = [x for x in posts if x not in s]
            num = np.random.randint(8, size=1)[0]  # Retrieve the integer value from the NumPy array
            reposts = random.sample(temp3, k=num)
            for j in reposts:
                time = self.generate_random_timestamp()
                tx.run("MATCH (u1:User {name: $name1}), (u2:Post {postid:$postid}) "
                       "CREATE (u1)-[:REPOSTED{timestamp:$times}]->(u2)", name1=i['name'], postid=j['postid'],
                       times=time)

    def _create_reply(self, tx):
        posts = self.get_all_posts()
        users = self.get_all_users()
        for i in users:
            p1 = self.postbyuser(i['name'])
            s = set(p1)
            temp3 = [x for x in posts if x not in s]
            num = np.random.randint(3, size=1)[0]  # Retrieve the integer value from the NumPy array
            replies = random.sample(posts, k=num)
            for j in replies:
                time = self.generate_random_timestamp()
                tx.run("MATCH (u1:User {name: $name1}), (u2:Post {postid:$postid}) "
                       "CREATE (u1)-[:REPLIED{timestamp:$times,content:$content,media:$media}]->(u2)", name1=i['name'],
                       postid=j['postid'], times=time, content=self.generate_sentence(), media=self.generate_url())

    def _create_quotes(self, tx):
        posts = self.get_all_posts()
        users = self.get_all_users()
        for i in users:
            p1 = self.postbyuser(i['name'])
            s = set(p1)
            temp3 = [x for x in posts if x not in s]
            num = np.random.randint(3, size=1)[0]  # Retrieve the integer value from the NumPy array
            quotes = random.sample(temp3, k=num)
            for j in quotes:
                time = self.generate_random_timestamp()
                tx.run("MATCH (u1:User {name: $name1}), (u2:Post {postid:$postid}) "
                       "CREATE (u1)-[:QUOTES{timestamp:$times,content:$content,media:$media}]->(u2)", name1=i['name'],
                       postid=j['postid'], times=time, content=self.generate_sentence(), media=self.generate_url())


    def _create_and_return_greeting(self, tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

    def _create_and_return_relations(self, tx):
        posts = self.get_all_posts()
        users = self.get_all_users()
        print(posts)
        for i in posts:
            k = random.choice(users)
            print(k['name'], i['postid'])
            result = tx.run("MATCH (n:User {name: $name}), (m:Post {postid: $postid}) "
                            "CREATE (n)-[:POSTED]->(m)", name=k['name'], postid=i['postid'])
        return

    @staticmethod
    def _match_and_return_greeting(self, tx, message):
        result = tx.run("MATCH (a:User) "
                        "RETURN a.name", message=message)
        return result.single()[0]


if __name__ == "__main__":
    greeter = HelloWorldExample("bolt://localhost:7687", "neo4j", "cypher@123")
    # greeter.print_greeting("hello, world", create=True)  # Call the _create_and_return_greeting method
    #     greeter.print_greeting("hello, world", create=False)  # Call the _match_and_return_greeting method
    #     greeter.create_rel()
    #     greeter.create_follow()
    #     greeter.create_reposts()
    #     greeter.create_quotes()
    #     greeter.create_likes()
    #     greeter.adduser()
    #     greeter.addpost('Loki')
    #     greeter.likepost('Loki','74')
    #     greeter.followuser('Rishith','William Garcia')
    #     greeter.addrepost('Rishith','80')
    #     greeter.addquote('Rishith','81')
    #     print(greeter.getuser('Rishith'))
    #     print(greeter.getpost('101'))
    #     print(greeter.get_liked_posts('William Garcia'))
    #     print(greeter.getfollowers('Rishith'))
    #     print(greeter.getrepost('William Garcia','80'))
    #     print(greeter.getquote('Rishith','81'))
    #     print(greeter.recommendfollowers('Rishith'))
    #     print(greeter.ForYouFeed('William Garcia'))
    #     greeter.deluser('Loki')
    #     greeter.delpost('42')
    #     greeter.dellikepost('Joshua Anderson','52')
    #     greeter.delfollowuser('Joshua Anderson','Susan Thomas')
    #     print(greeter.getnumlikes('27'))
    st.title('Tweeter')
    tab0,tab1, tab2, tab3,tab4,tab5 = st.tabs(["Home","Basic Functions ", "Follower Recommendations", "For You Page","Following Page","User Profile"])
    una=""


    # insert_button_clicked = st.sidebar.button('Insert')
    # ins=insert_button_clicked
    # if ins:
    with tab1:
        st.subheader('Insertion Tasks', divider='rainbow')
        add_selectbox = st.selectbox(
            'What Insertion task would you like to perform?',
            ('None', 'NewUser', 'NewPost', 'LikePost', 'FollowUser', 'NewRepost', 'NewQuote', 'NewReply')
        )
        if add_selectbox == 'NewUser':
            st.write('Create a new user')
            title = st.text_input('User name', '')
            title4 = st.text_input('Bio', '')
            title5=st.text_input('Enter email')
            title3 = st.text_input('User Tag', '')
            title2 = st.text_input('DOB year', '')
            title1 = st.text_input('DOB month', '')
            title0 = st.text_input('DOB date', '')
            create_button_clicked = st.button('Create User')
            if create_button_clicked:
                x=greeter.adduser(title, title4, title3,title5, int(title2), int(title1), int(title0))
                if(x):
                    st.write(':blue[User created successfully!]')
                else:
                    st.write('Incorrect details')
        elif add_selectbox == 'NewPost':
            st.write('Create a new post')
            title = st.text_input('User name', '')
            title4 = st.text_input('Tags', '')
            title5=st.text_input('Enter mentions')
            title3 = st.text_input('Enter Content of Post', '')
            # title2 = st.text_input('DOB year', '')
            # title1 = st.text_input('DOB month', '')
            # title0 = st.text_input('DOB date', '')
            create_button_clicked = st.button('Create Post')
            if create_button_clicked:
                greeter.addpost(title, title4, title5,title3)
                st.write(':blue[Post created successfully!]')
        elif add_selectbox == 'LikePost':
            st.write('Like a post')
            title = st.text_input('User name', '')
            title4 = st.text_input('Post Id', '')
            create_button_clicked = st.button('Like Post')
            if create_button_clicked:
                greeter.likepost(title, title4)
                st.write(':blue[Liked Post successfully!]')
        elif add_selectbox == 'FollowUser':
            st.write('Follow a User')
            title = st.text_input('Username 1', '')
            title4 = st.text_input('Username 2', '')
            create_button_clicked = st.button('Follow User')
            if create_button_clicked:
                greeter.followuser(title, title4)
                st.write(f':blue[Following {title4} successfully!]')
        elif add_selectbox == 'NewRepost':
            st.write('Added a Repost')
            title = st.text_input('Username', '')
            title4 = st.text_input('Post Id', '')
            create_button_clicked = st.button('Add Repost')
            if create_button_clicked:
                greeter.addrepost(title, title4)
                st.write(':blue[Added Repost successfully!]')
        elif add_selectbox == 'NewQuote':
            st.write('Added a Quote')
            title = st.text_input('Username', '')
            title4 = st.text_input('Post Id', '')
            title2=st.text_input('Content','')
            title3=st.text_input('Media','')
            create_button_clicked = st.button('Add Quote')
            if create_button_clicked:
                greeter.addquote(title, title4,title2,title3)
                st.write(':blue[Added Quote successfully!]')
        elif add_selectbox == 'NewReply':
            st.write('Added a Reply')
            title = st.text_input('Username', '')
            title4 = st.text_input('Post Id', '')
            title2=st.text_input('Content','')
            title3=st.text_input('Media','')
            create_button_clicked = st.button('Reply')
            if create_button_clicked:
                greeter.addreply(title, title4,title2,title3)
                st.write(':blue[Added Reply successfully!]')
        elif add_selectbox == 'None':
            pass
        st.subheader('Fetching Tasks', divider='rainbow')
        get_selectbox = st.selectbox(
            'What Insertion task would you like to perform?',
            ('None','GetUser', 'GetPost', 'GetLikedPosts', 'GetFollowers', 'GetReposts', 'GetQuote','GetReplies','GetAllUsers','GetAllPosts','PostByUser')
        )

        # insert_button_clicked = st.sidebar.button('Insert')
        # ins=insert_button_clicked
        # if ins:
        if get_selectbox == 'GetUser':
            st.write('View profile of User')
            title_n = st.text_input('Username', '')
            get_button_clicked = st.button('Get User')
            if get_button_clicked:
                try:
                    x = greeter.getuser(title_n)
                    if(len(x)>0):
                        st.write('**Username:** '+ x['name'])
                        st.write('**User Tag:** ' + x['user_tag'])
                        st.write('**Date Of Birth:** ' +str( x['Dob']))
                        st.write('**Email:** ' + x['registered_mail'])
                        st.write('**Bio:** ' + x['Bio'])
                        st.write('**Profile created on:** ' + str(x['created']))
                        # st.write(type(greeter.getuser(title_n)))
                        st.write(':blue[User Read successfully!]')
                    else:
                        st.write('No such user present')
                except:
                    st.write("Cannot retrieve user"+ title_n)
        elif get_selectbox == 'GetPost':
            st.write('View post')
            title_n = st.text_input('Post Id', '')
            # title2 = st.text_input('DOB year', '')
            # title1 = st.text_input('DOB month', '')
            # title0 = st.text_input('DOB date', '')
            get_button_clicked = st.button('View Post')
            if get_button_clicked:
                # print(title_n)
                try:

                    x = greeter.getpost(title_n)
                    # st.write(x)
                    if(len(x)>0):
                        st.write('**Postid:** ' + x['postid'])
                        st.write('**HashTags:** '+x['hash_tags'])
                        st.write('**Mentions:** '+x['mentions'])
                        st.write('**Tweet Content:** '+x['tweet_content'])
                        st.write(':blue[Post Read successfully!]')
                    else:
                        st.write('No posts yet')
                except:
                    st.write('Cannot retrieve Post')
        elif get_selectbox == 'GetLikedPosts':
            st.write('Posts Liked By User')
            title_n = st.text_input('User name', '')
            # title4_n = st.text_input('Post Id', '')
            get_button_clicked = st.button('View Liked Posts')
            st.write(title_n)
            if get_button_clicked:
                try:
                    x = greeter.getlikedposts(title_n)
                    # st.write(x)
                    # st.write(len(x))
                    if(len(x)>0):
                        for i in range(len(x)):
                            st.write("**Postid** " + x[i][0])
                            st.write("**Content:** " + x[i][1])
                        st.write(':blue[Liked Post Read successfully!]')
                    else:
                        st.write('No Liked posts yet!')
                except:
                    st.write('Cannot retrieve Liked Posts of user:'+ title_n)
        elif get_selectbox == 'GetFollowers':
            st.write('Get Followers')
            title_n = st.text_input('Username 1', '')
            # title4_n = st.text_input('Username 2', '')
            get_button_clicked = st.button('Get Following')
            st.write(title_n + " followers are")
            if get_button_clicked:
                try:
                    x = greeter.getfollowers(title_n)
                    # st.write(x)
                    if(x>0):
                        for i in range(len(x)):
                            st.write(x[i]['name'])
                        st.write(f':blue[Showing Followers {title_n} successfully!]')
                    else:
                        st.write('No One Following '+ title_n)
                except:
                    st.write('Cannot retrieve followers')
        elif get_selectbox == 'GetReposts':#there is a diffrence between add and get
            st.write('Get Repost')
            title_n = st.text_input('Username', '')
            title4_n = st.text_input('Post Id', '')
            get_button_clicked = st.button('Get Repost')
            if get_button_clicked:
                try:
                    x = greeter.getrepost(title_n, title4_n)
                    if(x>0):
                        st.write(x)
                        st.write(':blue[Fetched Repost successfully!]')
                    else:
                        st.write('No reposts by '+title_n)
                except:
                    st.write('Cannot retrieve Repsots')
        elif get_selectbox == 'GetQuote':
            st.write('Added a Quote')
            title_n = st.text_input('Username', '')
            title4_n = st.text_input('Post Id', '')
            get_button_clicked = st.button('Get Quote')
            if get_button_clicked:
                try:
                    x = greeter.getquote(title_n, title4_n)
                    if(x>0):
                        st.write(x)
                        st.write(':blue[Added Quote successfully!]')
                    else:
                        st.write('No Quotes by '+ title_n)
                except:
                    st.write('Cannot retrieve Quotes')
        elif get_selectbox == 'GetReplies':
            st.write('View Replies for a post')
            title_n = st.text_input('Username', '')
            title4_n = st.text_input('Post Id', '')
            get_button_clicked = st.button('Get Replies')
            if get_button_clicked:
                try:
                    x= greeter.getreplies(title4_n)
                    if(x>0):
                        st.write()
                        st.write(':blue[Fetched Reply successfully!]')
                    else:
                        st.write('No Replies By '+title_n)
                except:
                    st.write('Cannot retrieve Replies')
        elif get_selectbox == 'GetAllUsers':
            st.write('View All Users')
            get_button_clicked = st.button('Get Users')
            if get_button_clicked:
                try:
                    x=greeter.get_all_users()
                    if(x>0):
                        st.write(':red[Read Users successfully!]')
                        for i in x:
                            with st.expander(f':green[User: {i["user_tag"]}]'):
                                # st.write(f':green[User: {i["user_tag"]}] ')
                                st.write('**Username:** ' + i['name'])
                                st.write('**User Tag:** ' + i['user_tag'])
                                st.write('**Date Of Birth:** ' + str(i['Dob']))
                                st.write('**Email:** ' + i['registered_mail'])
                                st.write('**Bio:** ' + i['Bio'])
                                st.write('**Profile created on:** ' + str(i['created']))
                    else:
                        st.write('No Users yet in the application')
                except:
                    st.write('Cannot retrieve Users')
        elif get_selectbox == 'GetAllPosts':
            st.write('View All Posts')
            get_button_clicked = st.button('Get Posts')
            if get_button_clicked:
                try:
                    y=greeter.get_all_posts()
                    if(y>0):
                        for i in y:
                            with st.expander(f':green[Post Id: {i["postid"]}]'):
                                # st.write(f':green[User: {i["user_tag"]}] ')
                                # st.write('**Postid:** ' + i['postid'])
                                st.write('**HashTags:** ' + i['hash_tags'])
                                st.write('**Mentions:** ' + i['mentions'])
                                st.write('**Tweet Content:** ' + i['tweet_content'])
                        st.write(':blue[Read Posts successfully!]')
                    else:
                        st.write('No posts yet in the application')
                except:
                    st.write('Cannot retrieve Posts')
        elif get_selectbox == 'PostByUser':
            st.write('View All Posts By User')
            title_n = st.text_input('Username', '')
            get_button_clicked = st.button('Get Posts')
            if get_button_clicked:
                try:
                    y=greeter.postbyuser(title_n)
                    if len(y)==0:
                        st.write(":red[User hasn't posted Anything Yet]")
                    for i in y:
                        with st.expander(f':green[Post Id: {i["postid"]}]'):
                            # st.write(f':green[User: {i["user_tag"]}] ')
                            # st.write('**Postid:** ' + i['postid'])
                            st.write('**HashTags:** ' + i['hash_tags'])
                            st.write('**Mentions:** ' + i['mentions'])
                            st.write('**Tweet Content:** ' + i['tweet_content'])
                    st.write(':blue[Read Posts successfully!]')
        # elif add_selectbox =='GetAllUsers':
                except:
                    st.write('Cannot retrieve Posts of' + title_n)
        #
        elif get_selectbox == 'None':
            pass
        st.subheader('Deletion Tasks', divider='rainbow')
        delete_selectbox = st.selectbox(
            'What Deleting task would you like to perform?',
            ('None', 'DeleteUser', 'DeletePost', 'RemoveLikes', 'StopFollowing', 'DeleteReposts', 'DeleteQuote','DeleteReply')
        )

        # insert_button_clicked = st.sidebar.button('Insert')
        # ins=insert_button_clicked
        # if ins:
        if delete_selectbox == 'DeleteUser':
            st.write('DELETE User')
            title_n = st.text_input('Username', '')
            get_button_clicked = st.button('Delete User')
            if get_button_clicked:
                # if()
                try:
                    x=greeter.getuser(title_n)
                    name=x['name']
                    greeter.deluser(title_n)
                    st.write(':blue[User Deleted successfully!]')
                except:
                    st.write('User not present')
                # greeter.deluser(title_n)
                # st.write(':blue[User Deleted successfully!]')
        elif delete_selectbox == 'DeletePost':
            st.write('Delete post')
            title_n = st.text_input('Post Id', '')
            # title2 = st.text_input('DOB year', '')
            # title1 = st.text_input('DOB month', '')
            # title0 = st.text_input('DOB date', '')
            get_button_clicked = st.button('Delete Post')
            if get_button_clicked:
                try:
                    greeter.delpost(title_n)
                    st.write(':blue[Post Deleted successfully!]')
                except:
                    st.write('Cannot delete Post :'+ title_n)
        elif delete_selectbox == 'RemoveLikes':
            st.write('Stop Liking a Post')
            title_n = st.text_input('User name', '')
            title4_n = st.text_input('Post Id', '')
            get_button_clicked = st.button('Remove Liked Post')
            if get_button_clicked:
                try:
                    greeter.dellikepost(title_n,title4_n)
                    st.write(':blue[Post Like Removed successfully!]')
                except:
                    st.write('Cannot remove like of the post :'+title4_n)
        elif delete_selectbox == 'StopFollowing':
            st.write('Stop Followers')
            title_n = st.text_input('Username 1', '')
            # title4_n = st.text_input('Username 2', '')
            get_button_clicked = st.button('Stop Following')
            if get_button_clicked:
                try:
                    greeter.delfollowuser(title_n)
                    st.write(f':blue[Showing Followers {title_n} successfully!]')
                except:
                    st.write('Unable to unfollow')
        elif delete_selectbox == 'DeleteReposts':
            st.write('Get Repost')
            title_n = st.text_input('Username', '')
            title4_n = st.text_input('Post Id', '')
            get_button_clicked = st.button('Delete Repost')
            if get_button_clicked:
                try:
                    greeter.delrepost(title_n, title4_n)
                    st.write(':blue[Added Repost successfully!]')
                except:
                    st.write('Unable to Delete Reposts')
        elif delete_selectbox == 'DeleteQuote':
            st.write('Added a Quote')
            title_n = st.text_input('Username', '')
            title4_n = st.text_input('Post Id', '')
            get_button_clicked = st.button('Delete Quote')
            if get_button_clicked:
                try:
                    st.write(greeter.delquote(title_n, title4_n))
                    st.write(':blue[Added Quote successfully!]')
                except:
                    st.write('Unable to Delete Quote')
        elif delete_selectbox == 'DeleteReply':
            st.write('View Replies for a post')
            title_n = st.text_input('Username', '')
            title4_n = st.text_input('Post Id', '')
            get_button_clicked = st.button('Delete Replies')
            if get_button_clicked:
                try:
                    st.write(greeter.delreply(title_n,title4_n))
                    st.write(':blue[Read Reply successfully!]')
                except:
                    st.write('Unable to Delete Reply')
        # elif add_selectbox =='GetAllUsers':
        #
        elif delete_selectbox == 'None':
            pass

        st.subheader('Updating Tasks', divider='rainbow')
        update_selectbox = st.selectbox(
            'What Updating task would you like to perform?',
            ('None', 'DeleteUser', 'DeletePost', 'RemoveLikes', 'StopFollowing', 'DeleteReposts', 'DeleteQuote',
             'DeleteReply')
        )

    with tab2:
        name=st.text_input('Enter your Username','')
        buttona=st.button("Recommend Followers")
        if(buttona):
            try:
                x=greeter.recommendfollowers(name)
                for i in x:
                    with st.expander(f':green[You might know {i["name"]} ]'):
                        # st.write(f':green[User: {i["user_tag"]}] ')
                        st.write('**Username:** ' + i['name'])
                        st.write('**User Tag:** ' + i['user_tag'])
                        st.write('**Date Of Birth:** ' + str(i['Dob']))
                        st.write('**Email:** ' + i['registered_mail'])
                        st.write('**Bio:** ' + i['Bio'])
                        st.write('**Profile created on:** ' + str(i['created']))
            except:
                st.write('Cannot Retrieve Recommend Followers')
    with tab3:
        name = st.text_input('Enter Username', '')
        buttona = st.button("Get Foryou feed")
        if (buttona):
            try:
                import time
                progress_text = "Operation in progress. Please wait."
                my_bar = st.progress(0, text=progress_text)

                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1, text=progress_text)
                time.sleep(1)
                my_bar.empty()
                x=greeter.ForYouFeed(name)

                # x=list(ias)
                # st.write(type(x))
                lst=[]
                for k in x:
                    lst.append(k[0])
                lst=set(lst)
                # st.write(lst)
                for j in lst:

                    # st.write(i)
                        with st.expander(f':green[Post Id: {j["postid"]}]'):
                            # st.write(f':green[User: {i["user_tag"]}] ')
                            st.write('**Postid:** ' + j['postid'])
                            st.write('**HashTags:** ' + j['hash_tags'])
                            st.write('**Mentions:** ' + j['mentions'])
                            st.write('**Tweet Content:** ' + j['tweet_content'])
            except:
                st.write('Cannot retrieve Posts ')
    with tab4:
        name = st.text_input('Enter UserName', '')
        buttona = st.button("Get Following feed")
        if (buttona):
            try:
                x = greeter.FollowingFeed(name)

                # x=list(ias)
                # st.write(type(x))
                # lst = []
                # for k in x:
                #     lst.append(k[0])
                # lst = set(lst)
                # st.write(x)
                for j in x:

                    if j is None:
                        # st.write(j)
                        pass
                    else:
                        with st.expander(f':green[Post Id: {j["postid"]}]'):
                            # st.write(f':green[User: {i["user_tag"]}] ')
                            st.write('**Postid:** ' + j['postid'])
                            st.write('**HashTags:** ' + j['hash_tags'])
                            st.write('**Mentions:** ' + j['mentions'])
                            st.write('**Tweet Content:** ' + j['tweet_content'])
            except:
                st.write('Cannot retrieve posts')

    # else:
    #     st.write('Goodbye')

    # greeter.updateuser('Joshua Anderson')
    # greeter.create_replies()
    with tab0:
        import streamlit as st
        import numpy as np

        una = st.text_input("Userid", "")
        with st.chat_message("user"):

            st.write("""
Our choice of Neo4j as the database for our application is primarily due to its effectiveness in managing social media networks. Neo4j's strength lies in its ability to handle a substantial number of connections and relationships, particularly with properties. This flexibility is crucial for our database modeling, as it differs from traditional relational databases, which are more rigid in their schema design, and it is mainly used for organized data.

Functionality Highlights:

- Adding and Managing User Accounts: Users can easily create accounts using their email, ensuring a seamless onboarding process. Additionally, they can delete their accounts if they choose to leave the platform, with a secure login feature providing an extra layer of authentication and security.

- Following Page: Users have access to a centralized feed displaying posts from the accounts they follow, facilitating easy access to the latest updates from their network.

- ForYou Page Recommendations: Our application offers a personalized "ForYou" page that recommends content based on the likes of their followers, as well as their posts, reposts, and replies. This feature enhances the user experience by providing tailored content suggestions.

- Follow Recommendations: Users can explore new accounts to follow through recommendations that extend 1-2 hops from their followers, expanding their network and introducing them to potentially interesting content.

- Profile View: Users can explore other users' profiles by typing in their names. This feature allows users to view typed posts, reposts, replies, quotes, likes, and more, offering a comprehensive view of their activity on the platform.

- Followers and Following: Our application allows users to see who is following a particular user, as well as whom that user is following. This transparency promotes stronger connections within the network.

- Birthday Balloons: A unique and delightful feature where balloons pop up on a user's profile on their birthday, adding a fun and personal touch to the application, making it more engaging and interactive.

- Creating and Managing Posts: Users can create posts, reply to, repost, and quote posts made by other users. This interactive feature fosters lively conversations and information sharing within the platform.
"""
                     )

    with tab5:
        # name = st.text_input('UserName', '')
        # st.write(una)
        name=una
        buttona = True
        if (buttona):
            st.subheader('User Details', divider='rainbow')
            try:
                x = greeter.getuser(name)
                st.write('**Username:** ' + x['name'])
                st.write('**User Tag:** ' + x['user_tag'])
                st.write('**Date Of Birth:** ' + str(x['Dob']))
                st.write('**Email:** ' + x['registered_mail'])
                st.write('**Bio:** ' + x['Bio'])
                st.write('**Profile created on:** ' + str(x['created']))
                # st.write(str(x['Dob'].month) +" "+ str(x['Dob'].day))
                if(x['Dob'].month==datetime. datetime. today().month and x['Dob'].day==datetime. datetime. today().day):
                    st.balloons()
                # st.write(type(greeter.getuser(title_n)))
                st.write(':blue[User Read successfully!]')
            except:
                st.write("no such user present")
            st.subheader('Following', divider='rainbow')
            try:
                x=greeter.getfollowing(name)
                for i in x:
                    with st.expander(f':green[User:{i["name"]}]'):
                        # st.write('**Username:** ' + i['name'])
                        st.write('**User Tag:** ' + i['user_tag'])
                        st.write('**Date Of Birth:** ' + str(i['Dob']))
                        st.write('**Email:** ' + i['registered_mail'])
                        st.write('**Bio:** ' + i['Bio'])
                        st.write('**Profile created on:** ' + str(i['created']))
            except:
                st.write("not following anyone- loser")
            st.subheader('Followers', divider='rainbow')
            try:
                x=greeter.getfollowers(name)
                for i in x:
                    with st.expander(f':green[User:{i["name"]}]'):
                        # st.write('**Username:** ' + i['name'])
                        st.write('**User Tag:** ' + i['user_tag'])
                        st.write('**Date Of Birth:** ' + str(i['Dob']))
                        st.write('**Email:** ' + i['registered_mail'])
                        st.write('**Bio:** ' + i['Bio'])
                        st.write('**Profile created on:** ' + str(i['created']))
            except:
                st.write("no one will ever follow you- loser")
                # print(e)
            st.subheader('User Posts', divider='rainbow')
            try:
                x = greeter.postbyuser(name)
                # st.write(x)
                for i in x:
                    with st.expander(f':green[Post Id: {i["postid"]}]'):
                        # st.write(f':green[User: {i["user_tag"]}] ')
                        st.write('**Postid:** ' + i['postid'])
                        st.write('**HashTags:** ' + i['hash_tags'])
                        st.write('**Mentions:** ' + i['mentions'])
                        st.write('**Tweet Content:** ' + i['tweet_content'])
            except:
                st.write('No such post')
            st.subheader('User Quotes', divider='rainbow')
            try:
                x = greeter.quotebyuser(name)
                # st.write(x)
                for i in x:
                    with st.expander(f':green[Quoted the Post: {i[1]["postid"]} ]'):
                        # st.write(f':green[User: {i["user_tag"]}] ')
                        # st.write('**Postid:** ' + i['postid'])
                        st.write('**Content:** ' + i[0]['content'])
                        st.write('**Media:** ' + i[0]['media'])
                        # st.write('**Tweet Content:** ' + i['tweet_content'])
            except:
                st.write('No such quotes')
            st.subheader('User Reposts', divider='rainbow')
            try:
                # st.write("asd")
                x = greeter.repostbyuser(name)
                # st.write(x)
                for i in x:
                    # st.write(i)
                    with st.expander(f':green[Repost to Post: {i[1]["postid"]}]'):
                        # st.write(f':green[User: {i["user_tag"]}] ')
                        # st.write('**Postid:** ' + i['postid'])
                        st.write('**Postid:** ' + i[1]['postid'])
                        st.write('**HashTags:** ' + i[1]['hash_tags'])
                        st.write('**Mentions:** ' + i[1]['mentions'])
                        st.write('**Tweet Content:** ' + i[1]['tweet_content'])
                        # st.write('**Tweet Content:** ' + i['tweet_content'])
            except Exception as e:
                print(e)
                st.write('No such reposts')
            st.subheader('User Replies', divider='rainbow')
            try:
                x = greeter.replybyuser(name)
                # st.write(x)
                for i in x:
                    # st.write(i)
                    with st.expander(f':green[Reply To Post {i[1]}]'):
                        # st.write(f':green[User: {i["user_tag"]}] ')
                        # st.write('**Postid:** ' + i['postid'])
                        st.write('**Content:** ' + i[0]['content'])
                        st.write('**Media:** ' + i[0]['media'])
                        # st.write('**Tweet Content:** ' + i['tweet_content'])
            except:
                st.write('No such reposts')

            # st.toast('Warming up...')
        # import time
        # with st.spinner('Wait for it...'):
        #     time.sleep(5)
        # st.success('Done!')
        # st.snow()
        # with st.chat_message("assistant"):
        #     st.write("Hello human")
        # st.line_chart(np.random.randn(30, 3))

    greeter.close()