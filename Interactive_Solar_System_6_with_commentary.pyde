# Step 1: Our original goal is to position the planets in semi-random places around the Sun and make them orbit the Sun at certain speeds as compared to one another. 
# For this reason, set the angles (i.e. thetas) each planet will rotate around the Sun from.
# Make sure the angles are different, so the planets appear to start out in "random" positions around the Sun.
# Make sure to float the values so that the planets can actually move (i.e. the value of the angles can actually change).
# Furthermore, the values themselves should be in descending order. Mercury travels fastest around the Sun, Venus second fastest, and so on.
theta_Mercury=9.87654321
float(theta_Mercury)
theta_Venus=8.7654321
float(theta_Venus)
theta_Earth=7.654321
float(theta_Earth)
theta_Mars=6.54321
float(theta_Mars)
theta_Jupiter=5.4321
float(theta_Jupiter)
theta_Saturn=4.321
float(theta_Saturn)
theta_Uranus=3.21
float(theta_Uranus)
theta_Neptune=2.1
float(theta_Neptune)
theta_Pluto=1
float(theta_Pluto)

# Step 2: Our next goal is to make this model of our solar system interactive. 
# We will do this by defining a couple of new variables and changing them over the course of time in opposite ways, so that when opposite arrow keys are pressed, opposite functions occur in the program.
# For this reason, define a the radius, r, between each planet's orbital path, which we will use to either decrease or increase each planet's distance to the Sun.
# Likewise, define the the variable, v, that we will make either decrease or increase over time in order to make each planet orbit the Sun either more slowly or more quickly over time.
r=25
v=0.001

# Step 3: Define your set up function and the parameters for your window. 
def setup():
    size(720,720)

# Step 4: Define your draw function and everything you want to be drawn in an eternal loop. 
# Make sure every theta value is global so the planets can actually move aorund the window. 
# Make sure to set your background to 0 so the solar system looks real.
# A new addition to this model of our solar system is the beginning varied distances between each planet instead of a uniform distane.
# Now each planet is a certain distance from one another that is fairly proportional to the distances they are from one another in the real solar system.
def draw():
    background(0)
    global r,v,theta_Mercury,theta_Venus,theta_Earth,theta_Mars,theta_Jupiter,theta_Saturn,theta_Uranus,theta_Neptune,theta_Pluto
   
    # Step 5: Our goal here is to make each planet orbit the Sun. 
    # Without each built-in translate function, they'll be located all over the place.
    # Without each built-in pushMatrix and popMatrix functions, they'll be orbiting each other.
    # Without each built-in rotate function, they won't orbit at all.
    # Therefore, we are going to use each of these functions for each of the planets in different ways, so that our solar system looks fairly accurate compared to our real one.
    translate(width/2, height/2) # This is the location of the Sun.
    fill(255,104,0) # Deep orange
    noStroke()
    ellipse(0,0,30,30)
    
    pushMatrix() # pushMatrix() saves the original coordinate system. Thus, when the translate function is used, each planet will start orbiting the Sun a certain amount of pixels away, as specified below, and not each other.
    rotate(theta_Mercury*1.987654321) # The built-in rotate function ensures each planet rotates by a specified angle parameter. Mercury rotates (i.e. orbits the Sun) the fastest, so its angle parameter should be the greatest.
    translate(r,0) # Now the new origin is the center of Mercury, translated 25 pixels away from the Sun.
    fill(255,204,0) # Darkish yellow
    noStroke()
    ellipse(0,0,8,8) # Smallest planet!
    popMatrix() # popMatrix restores the prior coordinate system. Used with each pushMatrix function, this enures each planet orbits the Sun and not each other (and are also not exponentially far away from each other once the translate function is used for each planet).
    
    pushMatrix() 
    rotate(theta_Venus*1.87654321) # Second fastest
    translate(r*1.7,0) # 42.5 pixels away from the Sun
    fill(255,154,0) # Darkish orange!
    noStroke()
    ellipse(0,0,12,12) # Third smallest planet!
    popMatrix()
    
    pushMatrix()
    rotate(theta_Earth*1.7654321) # Third fastest
    translate(r*2.7,0) # 67.5 pixels away from the Sun
    fill(0,100,204) # Deep blue
    noStroke()
    ellipse(0,0,13,13) # Fourth smallest planet
    popMatrix()
    
    pushMatrix()
    rotate(theta_Mars*1.654321) # Fourth fastest
    translate(r*3.8,0) # 95 pixels away from the Sun
    fill(204,10,10) # Deep red
    noStroke()
    ellipse(0,0,10,10) # Second smallest planet
    popMatrix()
    
    pushMatrix()
    rotate(theta_Jupiter*1.54321) # Fifth fastest
    translate(r*7.1,0) # 177.5 pixels away from the Sun
    fill(204,64,10) # Dark orange
    noStroke()
    ellipse(0,0,21,21) # Largest planet
    popMatrix()
    
    pushMatrix()
    rotate(theta_Saturn*1.4321) #Sixth fastest!
    translate(r*9,0) #225 pixels away from the Sun!
    fill(244,204,10) #Yellow!
    noStroke()
    ellipse(0,0,17,17) #Second largest planet!
    popMatrix()
    
    pushMatrix()
    rotate(theta_Uranus*1.321) # Seventh fastest
    translate(r*11.2,0) # 280 pixels away from the Sun
    fill(0,224,224) # Bright blue
    noStroke()
    ellipse(0,0,16,16) # Third largest planet
    popMatrix()
    
    pushMatrix()
    rotate(theta_Neptune*1.21) # Eighth fastest
    translate(r*12.4,0) # 310 pixels away from the Sun
    fill(0,55,255) # Dark blue
    noStroke()
    ellipse(0,0,15,15) # Fourth largest planet
    popMatrix()
    
    pushMatrix()
    rotate(theta_Pluto*1.1) # Ninth fastest
    translate(r*13.6,0) # 340 pixels away from the Sun
    fill(150,50,0) # Redish-brown
    noStroke()
    ellipse(0,0,3,3) # Dwarf planet
    popMatrix() # One final popMatrix to close it off and ensure correct orbiting paths, correct locations of each planet, correct distances between each planet, etc.
    
    # Step 6: Our goal is to make the planets move in an elliptical fashion. 
    # We can achieve this by constantly adding small increments to each planet's theta value each time the draw function is performed in this program. 
    # We'll do this based on how fast they orbit the Sun in the real solar system in comparison with one another. 
    # Again, as explained above, the addition of the variable v ensures that this digital art model of the solar system is interactive; if you press the left arrow key, the planets will gradually slow down, and the right arrow key performs the opposite function.
    theta_Mercury+=0.010987654321+v # fastest orbiting the sun
    theta_Venus+=0.00987654321+v # Venus second fastest
    theta_Earth+=0.0087654321+v # Earth third
    theta_Mars+=0.007654321+v # Mars fourth
    theta_Jupiter+=0.00654321+v # Jupiter fifth
    theta_Saturn+=0.0054321+v # Saturn sixth
    theta_Uranus+=0.004321+v # Uranus seventh
    theta_Neptune+=0.00321+v # Neptune eigth
    theta_Pluto+=0.0021+v # Pluto ninth
    
    # Step 7: Our second to last goal is to officially make this model of our solar system interactive. 
    # We can achieve this by using a number of if statements.
    if (keyPressed==True): # This first if statement makes sure that when a key is pressed, something tangible happens in the program.
        if (key==CODED): # This second if statement ensures that when certain keys are pressed, certain tangible things happen in the program.
            if (keyCode==UP): # This third if statement ensures that when the up arrow key is pressed, it causes tangible change to the r variable, as with the if statements below.
                r=r/1.01 # This then statement means that when the up arrow key is pressed, the planets look like they're moving in closer to the Sun, as the distance between each of them is divided by 1.01 each time the up arrow key is pressed.
            if (keyCode==DOWN): 
                r=r/.99
            if (keyCode==LEFT): # This fourth if statement ensures that when the left arrow key is pressed, the speed that is added to each planet's velocity as they orbit the Sun decreases by a small increment.
                v-=0.0001 # Notice that if you keep on pressing or holding down the left arrow key, eventually the direction of the planets as they orbit the Sun will switch, and their velocities will continue to increase as they orbit in that new direction each time the left arrow key is pressed.
            if (keyCode==RIGHT):
                v+=0.0001
    # Step 8: Our final goal is to write a few lines of text that explain to people that want interact with this solar system model how they can actually interact with it by pressing all of the arrow keys to make different things happen, as specified above.
    # We can achieve this by using the built-in fill and text functions.
    fill(255,204,0)
    text("Space Adventure!", -60, -345)
    fill(255,154,0)
    text("Interact with our solar system!", -355, -345)
    fill(0,155,255)
    text("Press left and right arrow keys", -355, -333)
    fill(204,10,10)
    text("to make planets slow down or speed up!", -355, -321) 
    fill(244,204,10)
    text("Press up and down arrow keys", -355, -309)
    fill(0,255,255)
    text("to make planets move towards", -355, -297)
    fill(0,255,25)
    text("or away from the Sun!", -355, -285)
    
    # Disclaimer: This interactive model of our solar system is not drawn precisely to scale for artistic purposes.
