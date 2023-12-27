import sqlite3
import sys

conn = sqlite3.connect(sys.argv[1])

c = conn.cursor()

def login():
    # Ask user for username and password
    # Check if username and password are valid
    # If valid, go to main menu
    # If invalid, go back to login page

    print("*" * 20)
    print("Login page")
    print("*" * 20 + "\n")
    username = input("User ID: ")
    password = input("Password: ")

    c.execute("SELECT * FROM users WHERE usr = ? AND pwd = ?", (username, password))
    user = c.fetchone()

    if user is None:
        print("Invalid username or password")
        print("Do you want to register? (y/n)")
        option = input("Enter option: ")
        if option.lower() == "y":
            register()
        elif option.lower() == "n":
            main()
        else:
            print("Invalid option")
            main()
    else:
        print("\n" + "Welcome, " + user[2] + "\n")
        main_menu(user[0])

def register():
    # Ask user for name, email, city, timezone, and password
    # Generate unique user id
    # Add user to database
    # Go to main menu

    print("*" * 20)
    print("Register page")
    print("*" * 20 + "\n")
    name = input("Name: ")
    email = input("Email: ")
    city = input("City: ")
    timezone = input("Timezone: ")
    password = input("Password: ")

    c.execute("select max(usr) from users")
    max_id = c.fetchone()[0]
    if max_id is None:
        max_id = 0
    user_id = max_id + 1

    c.execute("insert into users values (?, ?, ?, ?, ?, ?)", (user_id, password, name, email, city, timezone))
    conn.commit()

    print("Welcome, " + name)
    main_menu(user_id)

# def populate_data(user_id):
#   # View all tweets, retweets, and replies of the current user sorted by date in descending order.
#   print("\n" + "My tweets" + "\n")
#   c.execute("select distinct t.tid, t.writer, t.tdate, t.text, t.replyto from tweets t where t.writer = ? order by t.tdate desc", (user_id,))
#   tweets = c.fetchall()
#   for tweet in tweets:
#       print("Tweet ID: " + str(tweet[0]))
#       print("Writer: " + str(tweet[1]))
#       print("Date: " + str(tweet[2]))
#       print("Text: " + str(tweet[3]))
#       print("Reply to: " + str(tweet[4]))
#       print()

#   print("\n" + "My retweets" + "\n")
#   c.execute("select distinct r.usr, r.tid, r.rdate from retweets r where r.usr = ? order by r.rdate desc", (user_id,))
#   retweets = c.fetchall()
#   for retweet in retweets:
#       print("User: " + str(retweet[0]))
#       print("Tweet ID: " + str(retweet[1]))
#       print("Date: " + str(retweet[2]))
#       print()

#       print("Want to delete? (y/n)")
#       option = input("Enter option: ")
#       if option == "y":
#           c.execute("delete from retweets where usr = ? and tid = ?", (retweet[0], retweet[1]))
#           conn.commit()
#           print("Retweet deleted!")

#       elif option == "n":
#           print("Retweet not deleted!")


#   print("\n" + "My replies" + "\n")
#   c.execute("select distinct t.tid, t.writer, t.tdate, t.text, t.replyto from tweets t where t.writer = ? and t.replyto is not null order by t.tdate desc", (user_id,))
#   replies = c.fetchall()
#   for reply in replies:
#       print("Tweet ID: " + str(reply[0]))
#       print("Writer: " + str(reply[1]))
#       print("Date: " + str(reply[2]))
#       print("Text: " + str(reply[3]))
#       print("Reply to: " + str(reply[4]))
#       print()

#       print("Want to delete? (y/n)")
#       option = input("Enter option: ")
#       if option == "y":
#           c.execute("delete from tweets where tid = ?", (reply[0],))
#           conn.commit()
#           print("Reply deleted!")

#       elif option == "n":
#           print("Reply not deleted!")

  
#   # Write a tweet.
#   print("\n" + "Write a tweet? (y/n)")
#   option = input("Enter option: ")
#   if option == "y":
#       c.execute("select max(tid) from tweets")
#       max_id = c.fetchone()[0]
#       if max_id is None:
#           max_id = 0
#       tweet_id = max_id + 1
#       text = input("Enter tweet: ")
#       c.execute("insert into tweets (tid, writer, tdate, text) values (?, ?, date('now'), ?)", (tweet_id, user_id, text))
#       conn.commit()
#       print("Tweet successful!")

#   elif option == "n":
#       print("Tweet not written!")

#   # Follow a user
#   print("\n" + "Follow a user? (y/n)")
#   option = input("Enter option: ")
#   if option == "y":
#       followee = input("Enter user ID of user you want to follow: ")
#       c.execute("insert into follows values (?, ?, date('now'))", (user_id, followee))
#       conn.commit()
#       print("Follow successful!")


def retweet(usr,tid):
    # insert retweet into retweets table
    c.execute('''INSERT INTO retweets (usr, tid, rdate) 
                   VALUES (:usrid, :tweetid, DATE('now'))''',{'usrid':usr, 'tweetid':tid})
    conn.commit()

def composetweet(usr,reply_to=None):    
    # inserting into table tweets
    if reply_to == None:
        text =input("Compose a tweet: ")
        c.execute('''INSERT INTO tweets (tid, writer, tdate, text, replyto)
        VALUES ((SELECT COALESCE(MAX(tid), 0) + 1 FROM tweets), :usrid, DATE('now'), :data, NULL);''',{"usrid":usr,"data":text})
        
        print("Successfully Tweeted!")
    else: 
        #if it is a reply
        text = input("Compose a reply: ")
        c.execute('''INSERT INTO tweets (tid, writer, tdate, text, replyto)
        VALUES ((SELECT COALESCE(MAX(tid), 0) + 1 FROM tweets), :usrid, DATE('now'), :data, :reply_to);''',{"usrid":usr,"data":text,"reply_to":reply_to})

        print("Successfully Replied!")
    #now inserting in table mentions and hashtags if required
    c.execute("SELECT last_insert_rowid()")
    # fetching the tid 
    tid = c.fetchone()[0]
    
    c.execute('SELECT * FROM hashtags;')
    hashtags  = c.fetchall()
    hashtags_list = [item[0].lower() for item in hashtags if item[0].startswith('#')]
  
    for i in text.split():    
        if i[0] == '#':
             #now inserting in table mentions and hashtags if required
            c.execute('''INSERT INTO mentions (tid,term) 
                           VALUES (:tid, :hashtag) ''',{"tid":tid, "hashtag":i})
            # this means it is a hashtag
            # we need to insert into table mentions
            if i.lower() not in hashtags_list:
                c.execute('''INSERT OR IGNORE INTO hashtags(term) 
                            VALUES(:term)''',{"term":i})
            
    conn.commit()
         

def searchingtweets(usr):
    # this function allows users to search for tweets based on the keywords they provide. This function takes only user_ID as an argument.
    keywords = input("Please enter one or more keywords: ").strip().split() # contains all the keywords

    if len(keywords) == 0:
        print("No keywords entered")
        main_menu(usr)
        return
    # now we need to find all the tweets with any of the keywords 

    #making a list with just the hashtags
    hashtags = []
    keywords_updated = []
    count =1 
    for i in keywords:
        count+=1
        if i[0] == '#':
            hashtags.append("'"+i.strip()+"'")
        keywords_updated.append("'"+'%'+i.strip() +'%'+"'")
    
    # This query will compare all the tweets from the tweets table and the mentions table to the keywords and select all of them
    c.execute(f'''
            SELECT DISTINCT t.tid, t.writer, t.text, t.tdate, 
                (SELECT COUNT(*) FROM retweets WHERE tid = t.tid) AS retweets_count,
                (SELECT COUNT(*) FROM tweets AS r WHERE r.replyto = t.tid) AS replies_count
            FROM tweets AS t
            LEFT JOIN mentions AS m ON t.tid = m.tid
            WHERE (
                t.text LIKE {' OR  t.text LIKE '.join(keywords_updated)}
                OR
                m.term IN ({', '.join(hashtags)}) 
            )
            ORDER BY t.tdate DESC
            
        ''')
    
    matching_tweets = c.fetchall()
    
    
    for i,j in enumerate(matching_tweets,1):
        
        print("Tweet ID: " + str(j[0]))
        print("Writer: " + str(j[1]))
        print("Date: " + str(j[3]))
        print("Text: " + str(j[2]))
        print()
        if i%5 == 0:
           #printed 5, asking user if user wants to see more
           print(f"Displaying {i} of {len(matching_tweets)} tweets. Do you want to see more? (y/n): ") 
           response = input().strip().lower()
           if response != 'y':
               break
        
    
    # Displaying statistics:
    response = input("Do you wish to see statistics for a tweet? (y/n): ")
    if response == 'y':
        print("Which tweet among these do you wish to learn more about?")
        selected_tweet = int(input("Enter the Tweet ID: "))
        for i in matching_tweets:
            if i[0] == selected_tweet:
                print(f"Retweets count: {i[4]}, Replies count: {i[5]}")

        

    response = input("Do you wish to reply to a tweet or retweet? (reply/retweet/no): ")
    #replying
    if response.strip().lower() == 'reply':
        selected_tweet = int(input("Enter the tid: "))
        
        composetweet(usr,selected_tweet) #change usr = 10000 to the current logged in user
        print("Successfully replied!")
    elif response.strip().lower() == 'retweet':
        selected_tweet = int(input("Enter the tid: "))
        retweet(usr,selected_tweet)
        print("Sucessfully retweeted!")

    main_menu(usr)
    conn.commit()


def search_users(keyword, user_id):
    # Search for users whose names or cities contain the keyword
    c.execute("SELECT DISTINCT usr, name, email, city, timezone FROM users WHERE lower(name) LIKE ? OR lower(city) LIKE ?", ('%' + keyword.lower() + '%', '%' + keyword.lower() + '%',))
    users = c.fetchall()
    if users:
        matching_users = [user for user in users if keyword.lower() in user[1].lower()]
        matching_city = [user for user in users if keyword.lower() not in user[1].lower() and keyword.lower() in user[3].lower()]
        sorted_users = sorted(matching_users, key=lambda user: len(user[1]))
        sorted_city = sorted(matching_city, key=lambda user: len(user[3]))
        combined_sorted_users = sorted_users + sorted_city
        combined_sorted_users1 = combined_sorted_users
        print("Matching Users:")
        while len(combined_sorted_users) > 0:
            num_users_to_display = min(5, len(combined_sorted_users))
            
            for user in combined_sorted_users[:num_users_to_display]:
                usr, name, email, city, timezone = user
                print(f"User ID: {usr}")
                print(f"Name: {name}")
                print("---------------------")
            combined_sorted_users = combined_sorted_users[num_users_to_display:]  # Remove displayed users
            if len(combined_sorted_users) > 0:
                see_more = input("1: See more Users, 0: Exit: ")
                if see_more == '0':
                    break
                elif see_more != '1':
                    print("Invalid input. Please enter 1 or 0.")
            else:
                break  # No more users to display, exit the loop
        while True:
            option = int(input("Enter the User ID to view details or enter 0 to go to the main menu: \n"))
            if option == 0:
                 print('Returning to the main menu.')  # Go back to the main menu
                 break
            else:
                result = [True for item in combined_sorted_users1 if option == item[0]]
                if result:
                    view_follower_details(option, user_id)
                    break  # If details are viewed, break the loop to avoid repetition
                else:
                    print("Invalid user number. Please try again.")

    else:
        print("No matching users found.")
        main_menu(user_id)

                
def list_followers(user_id):
    # Retrieve a list of all users who follow the logged-in user
    c.execute("SELECT u.usr, u.name FROM users AS u "
              "INNER JOIN follows AS f ON u.usr = f.flwer "
              "WHERE f.flwee = ?", (user_id,))
    followers = c.fetchall()
    if not followers:
        print("You don't have any followers yet.")
    print("Followers:")
    for i, follower in enumerate(followers):
        follower_id, follower_name = follower
        print(f"{i + 1}. {follower_name} (User ID: {follower_id})")
    while True:  # Loop starts here
        option = int(input("\nEnter the follower number to view details or enter 0 to go to the main menu: \n"))
        if option == 0:
            print('Returning to the main menu.')  # Go back to the main menu
            break
        elif option:
            result = [True for item in followers if option in item]
            if result:
                view_follower_details(option, user_id)
                break
            else:
                print("Invalid follower number. Please try again.")

def view_follower_details(selected_follower_id, user_id):
    # Retrieve more information about the selected follower
    c.execute("SELECT name, email, city, timezone FROM users WHERE usr = ?", (selected_follower_id,))
    follower_info = c.fetchone()
    if follower_info:
        follower_name = follower_info[0]
        print(f"Follower Details:")
        print(f"Name: {follower_name}")
        # Retrieve the number of tweets by the selected follower
        c.execute("SELECT COUNT(DISTINCT tid) FROM tweets WHERE writer = ?", (selected_follower_id,))
        tweet_count = c.fetchone()[0]
        print(f"Number of Tweets: {tweet_count}")
        # Retrieve the number of users the selected follower is following
        c.execute("SELECT COUNT(f.flwee) FROM follows AS f WHERE f.flwer = ?", (selected_follower_id,))
        following_count = c.fetchone()[0]
        print(f"Number of Users Being Followed: {following_count}")
        # Retrieve the number of followers of the selected follower
        c.execute("SELECT COUNT(f.flwer) FROM follows AS f WHERE f.flwee = ?", (selected_follower_id,))
        followers_count = c.fetchone()[0]
        print(f"Number of Followers: {followers_count}\n")
        # Retrieve up to 3 most recent tweets by the selected follower
        c.execute("SELECT DISTINCT tid, writer, tdate, text, replyto FROM tweets WHERE writer = ? "
          "ORDER BY tdate DESC", (selected_follower_id,))
        all_tweets = c.fetchall()
        # Get the 3 most recent tweets
        if len(all_tweets) <= 3:
            for tweet in all_tweets:
                print(tweet)
                print("Tweet ID: " + str(tweet[0]))
                print("Writer: " + str(tweet[1]))
                print("Date: " + str(tweet[2]))
                print("Text: " + str(tweet[3]))
                print("Reply to: " + str(tweet[4]))
                print()

            print("Do you want to follow this user? (y/n)")
            option = input("Enter option: ")
            if option == "y":
                follow_user(user_id, selected_follower_id)
            
        else:
            recent_tweets = all_tweets[:3]
            print('Three Recent Tweets: ')
            for tweet in recent_tweets:
                print("Tweet ID: " + str(tweet[0]))
                print("Writer: " + str(tweet[1]))
                print("Date: " + str(tweet[2]))
                print("Text: " + str(tweet[3]))
                print("Reply to: " + str(tweet[4]))
                print()
            print("Want to see more tweets? (y/n)")
            option = input("Enter option: ")
            if option == "y":
                older_tweets = all_tweets[3:]
                i = 0
                while i < len(older_tweets):
                    for tweet in older_tweets[i:i+3]:
                        print("Tweet ID: " + str(tweet[0]))
                        print("Writer: " + str(tweet[1]))
                        print("Date: " + str(tweet[2]))
                        print("Text: " + str(tweet[3]))
                        print("Reply to: " + str(tweet[4]))
                        print()
                    
                    i += 3

                    if i >= len(older_tweets):
                        break
                    else:
                        print("Next 3 tweets? (y/n)")
                        option = input("Enter option: ")
                        if option == "y":
                            continue
                        elif option == "n":
                            break
                        else:
                            print("Invalid option")

                print("Do you want to follow this user? (y/n)")
                option = input("Enter option: ")
                if option == "y":
                    follow_user(user_id, selected_follower_id)

            elif option == "n":
                print("Do you want to follow this user? (y/n)")
                option = input("Enter option: ")
                if option == "y":
                    follow_user(user_id, selected_follower_id)
            
        

def follow_user(user_id, selected_follower_id):
    # Follow a user
    if user_id == selected_follower_id:
        print("You can't follow yourself!")
    # Check if the user is already following the selected follower
    c.execute("SELECT 1 FROM follows WHERE flwer = ? AND flwee = ?", (user_id, selected_follower_id))
    existing_follow = c.fetchone()
    
    if existing_follow:
        print("You are already following this user.")
    else:
        # Allow the user to follow the selected follower
        c.execute("INSERT INTO follows (flwer, flwee, start_date) VALUES (?, ?, DATE('now'))", (user_id, selected_follower_id))
        conn.commit()
        print("You are now following this user.\n")



def main_menu(user_id):
    print("Start? (y/n)")
    option = input("Enter option: ")
    if option == "y":
        while True:
          print("*" * 20)
          print("Main menu")
          print("*" * 20 + "\n")

          # View all tweets, retweets, and replies of the current user sorted by date in descending order.
          print("Tweets" + "\n")
          c.execute("select distinct t.tid, t.writer, t.tdate, t.text, t.replyto from tweets t, follows f where f.flwer = ? and f.flwee = t.writer order by t.tdate desc", (user_id,))
          tweets = c.fetchall()
          if len(tweets) <= 5:
              for tweet in tweets:
                print("Tweet ID: " + str(tweet[0]))
                print("Writer: " + str(tweet[1]))
                print("Date: " + str(tweet[2]))
                print("Text: " + str(tweet[3]))
                print("Reply to: " + str(tweet[4]))
                print()

          else:
              # display only 5 tweets at a time. Ask the user if they want to see the next 5 tweets or go back to the main menu.
              i = 0
              while i < len(tweets):
                  for tweet in tweets[i:i+5]:
                      print("Tweet ID: " + str(tweet[0]))
                      print("Writer: " + str(tweet[1]))
                      print("Date: " + str(tweet[2]))
                      print("Text: " + str(tweet[3]))
                      print("Reply to: " + str(tweet[4]))
                      print()
                  
                  i += 5

                  if i >= len(tweets):
                      break
                  else:
                      print("Next 5 tweets? (y/n)")
                      option = input("Enter option: ")
                      if option == "y":
                          continue
                      elif option == "n":
                          break
                      else:
                          print("Invalid option")

          print ("Retweets" + "\n")
          c.execute("select distinct r.usr, r.tid, r.rdate from retweets r, follows f where f.flwer = ? and f.flwee = r.usr order by r.rdate desc", (user_id,))
          retweets = c.fetchall()
          if len(retweets) <= 5:
              for retweet in retweets:
                  print("User: " + str(retweet[0]))
                  print("Tweet ID: " + str(retweet[1]))
                  print("Date: " + str(retweet[2]))
                  print()
          
          else:
              # display only 5 retweets at a time. Ask the user if they want to see the next 5 retweets or go back to the main menu.
              i = 0
              while i < len(retweets):
                  for retweet in retweets[i:i+5]:
                      print("User: " + str(retweet[0]))
                      print("Tweet ID: " + str(retweet[1]))
                      print("Date: " + str(retweet[2]))
                      print()
                  
                  i += 5

                  if i >= len(retweets):
                      break
                  else:
                      print("Next 5 retweets? (y/n)")
                      option = input("Enter option: ")
                      if option == "y":
                          continue
                      elif option == "n":
                          break
                      else:
                          print("Invalid option")
        


          # Select a tweet to display the number of retweets and replies to the tweet.

          print("Do you want to select a tweet? (y/n)")
          option = input("Enter option: ")
          if option == "y":
              print("Select a tweet to display the number of retweets and replies to the tweet.")
              tweet_id = input("Enter tweet ID: ")
              if tweet_id in [str(tweet[0]) for tweet in tweets]:
                  c.execute("select count(*) from retweets where tid = ?", (tweet_id,))
                  retweets = c.fetchone()[0]
                  print("Number of retweets: " + str(retweets))
                  c.execute("select count(*) from tweets where replyto = ?", (tweet_id,))
                  replies = c.fetchone()[0]
                  print("Number of replies: " + str(replies))

                  # Ask the user if they want to retweet or reply to their selected tweet.

                  print("\n" + "Do you want to retweet or reply to your selected tweet? (y/n)")
                  option = input("Enter option: ")
                  if option == "y":
                      print("\n" + "1. Retweet")
                      print("2. Reply" + "\n")
                      option = input("Enter option: ")
                      if option == "1":
                        c.execute("insert into retweets values (?, ?, date('now'))", (user_id, tweet_id))
                        conn.commit()
                        print("Retweet successful!" + "\n")
                      elif option == "2":
                          c.execute("select max(tid) from tweets")
                          max_id = c.fetchone()[0]
                          if max_id is None:
                              max_id = 0
                          reply_id = max_id + 1
                          text = input("Enter reply: ")
                          c.execute("insert into tweets (tid, writer, tdate, text, replyto) values (?, ?, date('now'), ?, ?)", (reply_id, user_id, text, tweet_id))
                          conn.commit()
                          print("Reply successful!" + "\n")
                  elif option == "n":
                      print("No retweet or reply!" + "\n")

              else:
                  print("You don't follow that user or that tweet doesn't exist!")

          elif option == "n":
              print("No tweet selected!" + "\n")

          else:
              print("Invalid option")
              continue
        
          # Search for tweets
          print("Please select an option:")
          print("1. Search for tweets")
          print("2. Search for users")
          print("3. Compose a tweet")
          print("4. List followers")
          print("5. Logout")
          option = str(input("Enter option: "))
          if option == '1':
              searchingtweets(user_id)
          elif option == '2':
              keyword = input("Enter search keyword: ")
              search_users(keyword, user_id) 
          elif option == '3':
              composetweet(user_id)
          elif option == '4':
              list_followers(user_id)
          elif option == "5":
              main()
          else:
              print("Invalid option")

    elif option == "n":
        print("Goodbye!")
        main()

    else:
        print("Invalid option")
        main()


def main():
    # Login page
    # Ask user if they want to login, register, or exit

    # If login, Registered users should be able to login using a valid user id and password, respectively referred to as usr and pwd in table users.
    # If register, New users should provide a name, email, city, timezone and password. The user id (i.e. the field usr in table users) should be provided by the system and be unique.
    # If exit, exit the program

    print("*" * 20)
    print("Welcome to Twitter!")
    print("*" * 20 + "\n")
    print("Please select an option:")
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    option = input("Enter option: ")
    
    if option == "1":
        login()

    elif option == "2":
        register()

    elif option == "3":
        print("Goodbye!")
        exit()

    else:
        print("Invalid option")
        main()

main()
