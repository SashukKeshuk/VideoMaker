# Video Maker Bot

Telegram bot where you can create a video simply by entering a video topic, choosing a language, and specifying the duration. Upon request, the bot will use APIs to generate a video on the given topic using neural networks:

**ChatGPT-4 API:** Generates the video script in the selected language based on the provided topic.
**ElevenLabs API:** A multilingual neural network that voices the text (the script created in GPT).
**Pictory AI API:** A neural network that selects suitable video clips based on the script and assembles them into a video sequence.
**No API Available:** The neural network is parsed.
Once the bot retrieves all these resources, it will overlay the audio onto the video sequence, automatically adjusting for length and volume, add a watermark, and send the video to the user in the chat as a response to their topic request. The user can then choose a social network/platform from the bot's database where the bot will publish the video (currently supported platforms are YouTube, Instagram, and TikTok). The current version of the bot supports 6 languages: English, Russian, Spanish, Hindi, and Arabic.

An example of a video created by the bot: example.mp4 Screenshots of user interactions with the bot: *scr1/2.../.png*

In the future, it is planned to integrate the bot into production sectors and subsequently commercialize it.
