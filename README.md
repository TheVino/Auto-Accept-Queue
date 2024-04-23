
# Auto Accept Queue

[](https://github.com/TheVino/Auto-Accept-Queue#auto-accept-queue)API

## **Context**
*Braindead script* to auto accept the queue on your game.
Just click on play, run the script, alt tab and let the queue begin. Once the game is found, the client will pop up, and the script may take up to 5 seconds until will **auto cofirm the queue for you** 😎
Works for all queues, excpet games which will not require any screen confirmation.

## **Objective**
Easily accept your queue:
-	Don't need to lock you pc (*you can alt tab and watch whataver you want*)
-	Facilitate you to go take some coffee while you're on the queue
-	You take take a quick nap 😴 (*but not recommended*) while waitng for game pop-up


###### Well.. How?
Using OpenCV to read your screen and compare pixels, then PyAutoGUI to click no the 'Accept' button.
*Simple as it sounds!*

## **Goal**
Avoid missing your accept queue button (*which I know you sometimes miss a 20 minutes queue streak due to your falt*).

#####  The only modification you need to made on this first version of the program is on `Summoner.name` and `.region`<sub> lines 17 and 169</sub>


## First you will need to install the packages:
###### Installation
````pip install -r requirements.txt```` 
### Example

![partida-encontrada.png](https://imgur.com/1ONtRku.png)
This is the example file which I used to test the model.

![aceitar_recusar.png](https://imgur.com/iHpvtrN.png)
This is the model which will compare with your screen to confirm and click.

![result.png](https://imgur.com/MGGmd2r.png)
Using a mask algorithm from OpenCV, we can see the result here.
The white dot shows where we find the closest match for this sample.

```threshold =  .93  # the threshold of 93% close to the model image```
Using a threshold of 93% correlation (*I considered safe, don't ask me why*) we can filter and click on your best match.

![found.png](https://imgur.com/ZIDZfrI.png)
We found 1 match for our model! *- then we send a command to click on the button*

![ectangle.png](https://imgur.com/leqQaE6.png)
```(Python)> Button clicked at: (1280.0, 1026.5)```

You can break and close the program whenver you want, just pressing '**q**'.

### Future Features:
- Check a way to read the window size (only working on 1920x1080)
- Maybe some  UI  🤔 *(Not that easy to build good UI with PySimpleGUI)*

*This was a request from a friend of mine, which turned into a community used and shared script*
