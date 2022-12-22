# tonie-audio-match

This is a fork of @croesnick toniebox-audio-match. I moved the original functionality of @croesnick repo to /audiobooks when launching the app. Instead the root url launches a site where you can update the content of your creative tonies by quickly deleting and uploading files from your PC.

Your easy management solution for your [creative tonies](https://tonies.com).

![Example](sample.png)


So yet another UI to access from your laptop? 
Not at all! 
Put it onto a RaspberryPi and voilà -- accessible from your mobile whenever you need it! 🙂

## Configuration & Start

Place an `.env` file in this project's root to configure your service (like credentials for [tonies.de](https://tonies.de)).
Please see [.env.sample](.env.sample) for a sample configuration.

Once configured, start the whole application with `docker-compose up` and, after some initial processing of your media library, access your album covers locally at [http://localhost](http://localhost).
