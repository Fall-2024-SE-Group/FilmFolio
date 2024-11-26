## [The Login Page](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/templates/login.html)

The Login page is where users have the ability to log into an account they have created. If you do not have an account you can create an account on this page by clicking the signup button, and inputting an email, username, and password.

## [The Landing Page](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/templates/landing_page.html)

Ah, the Landing Page! This is where the magic begins, where users take their first steps into the world of PopcornPicks. It's like the red carpet of your website - without the flashbulbs and paparazzi. 

This template sets the stage for what's to come, the info on contributors and it better be good because the popcorn is popping, and the audience is waiting. 🍿

---

## [Search Page](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/templates/search.html)

The Search Page, where movie dreams come true! Imagine this as your movie-loving detective's office, equipped with a magnifying glass to help users find their cinematic gems.

Whether you're hunting for action-packed blockbusters, heartwarming rom-coms, or mind-bending sci-fi, this template's got your back. It's where the movie hunt begins. 🔍

After the search, if you click on predict you would be presented with recommended movies

---

## [Review Page](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/templates/review.html)

The Review Page, where users can praise or rant about movies they recently watched! 
All reviews submitted will appear on the Wall!

---

## [The Profile Page](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/templates/profile.html)

The profile page is a hub for the user where they can see their recently rated movies. Send messages to the friends.

---

## [Movie Chat Page](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/templates/movie_chat.html)

Welcome to the Movie Chat Page, where movie lovers unite to discuss the latest films, share opinions, and recommend hidden gems! 🎬🍿 This page is your digital movie theater, complete with a live chat feature where users can send messages in real-time. Whether you're looking to debate the best plot twist or share your excitement about an upcoming release, this is the place to be.

The chat interface is intuitive and easy to use—just type your message, hit send, and watch the conversation unfold. Conversations are powered by Socket.IO, which ensures that every message appears instantly for everyone in the chat, no delays!


---
## [Movie Page](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/templates/movie.html)

The Movie Page is the ultimate destination to explore detailed information about the movies that users have been watching, reviewing, and discussing! 🎬✨ This page is perfect for movie enthusiasts who want to dive deep into each film's plot, runtime, and reviews.

Each movie card displays key details like the title, runtime, and a brief overview, along with a handy IMDb link for those who want to discover even more. Below the movie details, you'll find a section dedicated to user reviews—where fellow film lovers share their thoughts and opinions on the movie. This is a great place to see how others are reacting to the latest blockbusters or hidden gems!

---

## [New Movies Page](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/templates/new_movies.html)

Welcome to the New Movies Page, where movie buffs can stay ahead of the curve and discover the latest film releases! 🍿✨ This page is dedicated to showcasing the newest upcoming movies and providing you with all the essential details to keep you in the loop.

At the top of the page, you'll find buttons that link to popular streaming platforms like Netflix, HBO Max, Amazon Prime Video, Disney+, and Hulu. Simply click on any of the icons to explore content directly on these platforms!

---

## [Trends Page](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/templates/trends.html)

Welcome to the Trending Movies Page, where you can discover the hottest and most popular films taking the entertainment world by storm! 🎬🔥 This page is your go-to place to explore what’s currently trending and see which movies are getting all the buzz.

Each movie card showcases key details like the movie title, a brief overview, and its average rating from users. Plus, there’s an image of the movie poster to give you a sneak peek of what to expect! For those who want to dive deeper, a "More Info" button will take you directly to the movie’s page on The Movie Database (TMDb).


---

## [Signup Page](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/templates/signup.html)

The Signup Page for FilmFolio makes it easy and quick to join the fun! Just fill in your Username, First Name, Last Name, Email, and Password, and you're all set to start exploring everything FilmFolio has to offer. We've kept things simple and user-friendly, so you can create your account without any hassle. Plus, there's a handy loading spinner to let you know everything's working behind the scenes. Once you're signed up, you’ll be able to dive into trending movies, share reviews, and connect with fellow movie lovers. FilmFolio is ready to welcome you to the ultimate movie experience—sign up and start your cinematic adventure today!


---

## [Layout Page](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/templates/shared/layout.html)

The Layout Page for FilmFolio is the backbone of the site, keeping everything looking sleek and consistent. It includes links to cool resources like Bootstrap for responsive design and Font Awesome for those awesome icons. The top navigation bar adjusts based on whether you're logged in or not—logged in? You’ll see links to Movie Chat 🎬, Latest Reviews 🌟, New Movies 🍿, Trends 🔥, and more! If you’re not logged in, you’ll get quick access to Sign Up ✍️ and Login 🔑.

This layout keeps the site tidy while giving room for custom content on each page, making FilmFolio fun and easy to navigate!


---

### And now, the real show-stoppers:

---

## [Script.js](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/static/js/script.js)

Script.js, the conductor of the orchestra! This JavaScript file keeps things moving, making sure your website performs its movie-magic smoothly.

With a bit of code wizardry, it handles user interactions, animations, and ensures everything runs like a well-choreographed dance scene in a musical.

---
## [chat.js](https://github.com/brwali/PopcornPicks/blob/master/src/recommenderapp/static/script.js)

Chat.js is the lifeline of your FilmFolio movie discussions! Think of it as the backstage pass to the live movie chat experience.

With this script, users can chat in real-time while watching their favorite flicks. It connects to the server using socket.io and listens for incoming messages. When someone types a message, it grabs their username and message, then creates a fresh list item in the chatbox, keeping the conversation flowing smoothly.

This file makes sure that no movie moment is missed, and your chats are just as lively as the action on-screen! 🎥💬

---

## [movie.js](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/static/js/movie.js)

Movie.js is the behind-the-scenes hero that brings movie posters to life! 🌟

This script is like the director calling the shots, fetching movie posters and displaying them in your movie list. When you click on a movie, it grabs the IMDb ID and makes an AJAX call to fetch the poster URL. Once the poster is ready, it updates the movie element on the page—bringing that flick to your screen in style!

It’s like having a personal assistant to add posters for every movie, giving your movie collection a polished, professional touch. 🎬✨

---


## [predict.js](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/static/js/movie.js)

Predict.js is the script that handles user reviews like a pro! 🎬🌟

When you click on a movie, this script helps open a modal window where you can leave a review. It gathers all the important details about the movie—like its title, runtime, genre, and poster—and sends that info to the server using AJAX when you submit your review. 🎥

It even ensures your review gets saved and lets you know with a quick success message. Plus, if something goes wrong, it helps by displaying an error message.

So, Predict.js is your review partner, making sure every movie gets its moment in the spotlight and every review is saved smoothly! 🍿✨

---

## [profile.js](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/static/js/profile.js)

Profile.js is like the personal assistant of your user account. It handles everything from fetching movie posters to updating your profile and even sending and managing messages. 🎬💬

It starts by fetching movie posters using AJAX whenever you view a list of movies. Just click on a movie ID, and voila! The poster appears, giving you an immersive experience while you scroll through your profile. 🎥🍿

Next, it powers the profile editing feature. Click on the "Edit Profile" button, and you can easily update your information through a simple modal. No fuss, no hassle—just smooth, real-time updates. 🛠️✨

And if you're a chatterbox, Profile.js has a whole messaging system built right in. You can send messages, view received and sent ones, and even delete old ones with a click. It's like a built-in chatroom for users to interact. 📲

So, whether you're updating your profile or chatting away, Profile.js ensures that your experience is smooth and intuitive. 🌟

---

## [search.js](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/static/js/search.js)

Search.js is like your personal movie critic assistant. It handles the review submission process with ease, allowing users to interact with movie details and share their thoughts—all with just a few clicks! 🎬✨

When you click on a movie in the search results, it pulls up a modal window where you can add your review. With a little AJAX magic, it sends your review data to the server, saving it in a flash! 🚀 Once your review is saved, it automatically closes the modal and shows a confirmation message. Easy peasy!

And if anything goes wrong? Search.js has you covered with error handling, making sure you always get a clear message if something doesn’t go as planned. 💡

In a nutshell, Search.js ensures that movie reviews are quick, smooth, and seamlessly integrated into your movie search experience. 🌟

---

## [Stylesheet.css](https://github.com/brwali/PopcornPicks/blob/master/src/recommenderapp/static/stylesheet.css)

Stylesheet.css, the fashion designer for your website! This file makes sure your website looks as stylish as a Hollywood star on the red carpet.

It's where colors, fonts, and layouts are chosen to give your website its unique look and feel. Whether it's classic black and white or a colorful extravaganza, this file sets the tone.

So, there you have it! Your templates and static files are the behind-the-scenes stars of PopcornPicks, working together to create a blockbuster website experience. 🎬🍿

---

## [chat.css](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/static/css/chat.css)

This CSS file works behind the scenes to give the chat page a clean, modern, and polished look. It centers the chat area perfectly, ensuring everything is balanced and easy to view. The chat cards have a subtle shadow and rounded corners, adding an elegant touch. Each message is styled for clarity, with a soft background and rounded edges, making it easy to read and interact with. It’s all about making the chat experience sleek, smooth, and user-friendly! 🖥️✨

---

## [login.css](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/static/css/login.css)

This login.css file creates a polished, user-friendly experience with a modern, professional touch. The login form is neatly centered on the page, making it easy to focus on, and surrounded by soft, rounded edges for a smooth look. The form is enhanced with a subtle shadow effect, adding depth without feeling too heavy.

For any login issues, a stylish red alert box gently appears, catching the user's attention without being too intrusive. The clean layout and thoughtful spacing guide users through the process with ease, making logging in a breeze.

The design balances simplicity with elegance, ensuring a seamless and pleasant experience for anyone visiting the page. Perfect for anyone looking for a sleek and approachable login interface! 💻🎨

---

## [movie.css](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/static/css/movie.css)

The movie.css file brings your movie cards to life with a clean, modern design. Each card stands out with a crisp white background, smooth rounded corners, and a subtle shadow, giving it a professional look. The cards are designed to stand apart from the page, but with a touch of elegance that’s easy on the eyes.

When users hover over a movie card, it gently lifts with a slight animation, adding an interactive and dynamic feel. The box-shadow intensifies on hover, making each movie feel more inviting to click on.

The hidden .imdbId ensures that the design stays clutter-free while still storing the essential movie ID information.

Perfect for showcasing movies in style—each card feels interactive and gives your site a polished, smooth feel! 🎬✨



---

## [predict.css](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/static/css/predict.css)

The predict.css file ensures a neat, organized layout that makes movie browsing a breeze. The movie-grid-row creates space at the top, giving your movie grid a nice, clean separation from other content. Each movie-card is thoughtfully spaced out, with margins to keep things looking balanced and accessible.

The alert styling adds a touch of urgency with noticeable margins, making important notifications stand out just the right amount.

The reviewModalLabel makes sure that the text within the modal pops with a clear, black color for easy reading. And with the boxsizingBorder rule, every element sizes up predictably without any surprises—keeping everything looking sharp and clean.

Overall, this file ensures that users have a smooth and visually appealing experience while navigating through movie predictions and reviews! 🎥✨



---

## [profile.css](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/static/css/profile.css)

The profile.css file creates a stylish user profile page with a modern, clean look ✨. It features a sleek profile card with smooth hover effects 🖱️, along with organized user details that are accompanied by easy-to-understand icons 🧑‍💻. The profile picture is circular and fits perfectly, giving it a polished feel 👤.

User interaction is seamless, with modals and input fields designed to be user-friendly. Clear buttons and labels guide users effortlessly 🔘✏️. The message modals pop with a darkened background for better focus 📩, while buttons use a consistent color scheme for easy identification 🎨.

Text is crisp and readable for accessibility 📝, and the friend list features interactive links that invite engagement 🤝. Overall, this design ensures a polished and responsive experience for all users 📱💻.



---

## [search.css](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/static/css/search.css)

The search.css file is designed to enhance the layout of movie search results 🎥. The movie grid row is neatly spaced to ensure a clean presentation, with each movie card styled to stand out with clear, readable text 🖤.

Alerts are styled to draw attention ⚠️, while review labels are clearly defined for a polished look 📝. The box-sizing rule ensures consistent spacing and layout across different browsers 📏.

This CSS ensures the search page looks great, feels intuitive, and works seamlessly across devices 📱💻.



---

## [signup.css](https://github.com/Fall-2024-SE-Group/FilmFolio/blob/master/app/src/static/css/signup.css)

The signup.css file ensures a clean and centered signup form for a smooth user experience 📝✨. The form is automatically aligned to the center of its container, providing a neat and professional look 🎯.

In case of errors, the failed_sign_in message appears with clear spacing to grab attention ⚠️. It is initially hidden and only shown when necessary, keeping the form uncluttered 📭.

This design enhances both functionality and visual appeal, ensuring users can easily navigate the signup process 🔑💻.



---