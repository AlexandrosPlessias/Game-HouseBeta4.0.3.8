import viz
import vizact
import vizcam
import vizinfo
import vizshape
import vizproximity
import steve


#viz.phys.enable()
viz.setMultiSample(4)
viz.fov(60)
viz.go(viz.FULLSCREEN)
#viz.go(viz.STEREO_3DTV_SIDE_BY_SIDE)
#viz.collision(viz.ON)

house=viz.addChild('HOUSEmeHxeia.osgb')
viz.addChild('sky_night.osgb')
house.getChild('Grass').setScale(3,0,3)

# Add vizinfo panel to display instructions.
info = vizinfo.InfoPanel("Navigate with WASD keys \nClick with LEFT mouse button to open and close doors",align=viz.ALIGN_RIGHT_TOP)

inrange=False
#ftiaxnei ton navigator
tracker = vizcam.addWalkNavigate()
tracker.setPosition([-0.41606, 1.47256, -2.92022])
viz.mouse.setVisible(True)
viz.link(tracker,viz.MainView)
viz.mouse.setTrap(viz.ON)

#ftiaxnei thn o8onh
tv = vizshape.addBox(size=(1.7,0.968,0))
tv.setEuler(89.5,0,0)
tv.setPosition([-6.15906,1.05,-3.33788])
tvtexture=viz.addTexture('tvTexture.jpg')
tv.texture(tvtexture)

sitcampos=[-3.28772, 1.20024, -3.31066]
sitcameuler=[-90.50000, 12.50000, 0.00000]

#sunarthsh gia na sikwnetai apo ton kanape
def getup():
	viz.link(tracker,viz.MainView)
	info2.visible(state=viz.OFF)
	tracker.setPosition([-4,1.47256,-1.31066])
	
#stamataei ola ta video kai ton hxo
def stopVideoAndSound():
	sound1.stop()
	sound2.stop()
	sound3.stop()
	sound4.stop()
	sound5.stop()
	sound6.stop()
	video1.stop()
	video2.stop()
	video3.stop()
	
#initialize hxvn kai video
video1 = viz.addVideo('Videos/ＭＡＣＩＮＤＯＧ ＰＬＵＳ.wmv')
video2 = viz.addVideo('Videos/The Sound of Silence.wmv')
video3 = viz.addVideo('Videos/He Isnt One With The Force.wmv')
sound1=house.playsound('VideoAudio/ＭＡＣＩＮＤＯＧ ＰＬＵＳ.wav',node='speaker1')
sound2=house.playsound('VideoAudio/ＭＡＣＩＮＤＯＧ ＰＬＵＳ.wav',node='speaker2')
sound3=house.playsound('VideoAudio/The Sound of Silence.wav',node='speaker1')
sound4=house.playsound('VideoAudio/The Sound of Silence.wav',node='speaker2')
sound5=house.playsound('VideoAudio/He Isnt One With The Force.wav',node='speaker1')
sound6=house.playsound('VideoAudio/He Isnt One With The Force.wav',node='speaker2')
stopVideoAndSound()

#proximity manager
manager = vizproximity.Manager()
manager.addTarget(vizproximity.Target(tracker))

#sunarthseis gia na allazeis kanalia
def press1():
	global inrange
	if inrange==True:
		stopVideoAndSound()
		video1.play()
		video1.volume(0)
		sound1.play()
		sound2.play()
		tv.texture(video1)

def press2():
	global inrange
	if inrange==True:
		stopVideoAndSound()
		video2.play()
		video2.volume(0)
		sound3.play()
		sound4.play()
		tv.texture(video2)

def press3():
	global inrange
	if inrange==True:
		stopVideoAndSound()
		video3.play()
		video3.volume(0)
		sound5.play()
		sound6.play()
		tv.texture(video3)

def press4():
	stopVideoAndSound()
	tv.texture(tvtexture)
	
#initialize proximity sensor tou kanape
couch=house.getChild('Cube')
sensor = vizproximity.addBoundingBoxSensor(couch,scale=(1.5,4,1.5))
manager.addSensor(sensor)

#info panels me plhrofories gia ton xeirhsmo
info1=vizinfo.InfoPanel("Press F to sit on the couch\nPress 1,2,3 to turn on tv and change channels\nPress 4 to turn off the tv",align=viz.ALIGN_CENTER_TOP)
info2=vizinfo.InfoPanel("Press G to get up from the couch\nPress 1,2,3 to turn on tv and change channels\nPress 4 to turn off the tv",align=viz.ALIGN_CENTER_TOP)
info1.visible(state=viz.OFF)
info2.visible(state=viz.OFF)

def enterSensor(e):
	global inrange
	info1.visible(state=viz.ON)
	inrange=True

def exitSensor(e):
	global inrange
	info1.visible(state=viz.OFF)
	inrange=False

def sit():
	global inrange
	if inrange==True:
		sitcam=vizcam.addWalkNavigate(moveScale=0)
		sitcam.setPosition(sitcampos)
		sitcam.setEuler(sitcameuler)
		viz.link(sitcam,viz.MainView)
		info1.visible(state=viz.OFF)
		info2.visible(state=viz.ON)

vizact.onkeydown( 'g', getup)
vizact.onkeydown( 'f', sit)

vizact.onkeydown( '1', press1)
vizact.onkeydown( '2', press2)
vizact.onkeydown( '3', press3)
vizact.onkeydown( '4', press4)


manager.onEnter(sensor,enterSensor)
manager.onExit(sensor,exitSensor)

def addReflection(node, mat=None, eye=viz.BOTH_EYE, resolution=[-1,-1]):

	#If reflection matrix is not specifed, use matrix of node object
	if mat is None:
		mat = node.getMatrix()

	#Position of node
	pos = viz.Vector(mat.getPosition())

	#Direction node is pointing
	dir = viz.Vector(mat.getForward())
	dir.normalize()

	#Quaternion rotation of node
	quat = mat.getQuat()

	#Create render texture
	tex = viz.addRenderTexture()

	#Create render node for rendering reflection
	lens = viz.addRenderNode(size=resolution)
	lens.attachTexture(tex)
	lens.setInheritView(True,viz.POST_MULT)
	#lens.disable(viz.CULL_FACE,op=viz.OP_OVERRIDE)
	lens.enable(viz.FLIP_POLYGON_ORDER,op=viz.OP_OVERRIDE)
	lens.renderToEye(eye)
	node.renderToEye(eye)
	node.renderToAllRenderNodesExcept([lens])

	#Setup reflection matrix
	rot = viz.Matrix.quat(quat)
	invRot = rot.inverse()
	lens.setMatrix(viz.Matrix.translate(-pos)*invRot*viz.Matrix.scale(1,1,-1)*rot*viz.Matrix.translate(pos))

	#Setup reflection clip plane
	s = viz.sign(viz.Vector(dir) * viz.Vector(pos))
	plane = viz.Plane(pos=pos,normal=dir)
	dist = plane.distance([0,0,0])
	lens.clipPlane([dir[0],dir[1],dir[2],s*dist-0.01])

	#Project reflection texture onto node
	node.texture(tex)
	node.texGen(viz.TEXGEN_PROJECT_EYE)

	return lens

# Position/scale for 1st mirror
bb = house.getBoundingBox(node='mirror_Zitti')
scale = [bb.size[2]-0.07,bb.size[1]-0.09,bb.size[0]]
pos = bb.center
pos[0] += 0.009

# Position/scale for 2nd mirror
bb2 = house.getBoundingBox(node='mirror_tall_Zitti')
scale2 = [bb2.size[2]-0.07,bb2.size[1]-0.09,bb2.size[0]]
pos2 = bb2.center
pos2[0] += 0.009

# Position/scale for 3rd mirror
bb3 = house.getBoundingBox(node='sirtariera-ka8refths_001 2')
scale3 = [bb3.size[2],bb3.size[1],bb3.size[0]]
pos3 = bb3.center
pos3[0] -= 0.009

# Position/scale for 4th mirror
bb4 = house.getBoundingBox(node='sirtariera-ka8refths 2')
scale4 = [bb4.size[0],bb4.size[1],bb4.size[2]]
pos4 = bb4.center
##pos4[0] -= 0.009


# Create reflection for left eye
leftEyeQuad = viz.addTexQuad(scale=scale, pos=pos, euler=(90,0,0))
leftEyeQuad.disable(viz.LIGHTING)
addReflection(leftEyeQuad,eye=viz.LEFT_EYE)
# Create reflection for right eye
rightEyeQuad = viz.addTexQuad(scale=scale,pos=pos, euler=(90,0,0))
rightEyeQuad.disable(viz.LIGHTING)
addReflection(rightEyeQuad,eye=viz.RIGHT_EYE)


# Create 2nd reflection
# Create reflection for left eye
leftEyeQuad = viz.addTexQuad(scale=scale2, pos=pos2, euler=(90,0,0))
leftEyeQuad.disable(viz.LIGHTING)
addReflection(leftEyeQuad,eye=viz.LEFT_EYE)
# Create reflection for right eye
rightEyeQuad = viz.addTexQuad(scale=scale2,pos=pos2, euler=(90,0,0))
rightEyeQuad.disable(viz.LIGHTING)
addReflection(rightEyeQuad,eye=viz.RIGHT_EYE)


# Create 3rd reflection
# Create reflection for left eye
leftEyeQuad = viz.addTexQuad(scale=scale3, pos=pos3, euler=(-90,0,0))
leftEyeQuad.disable(viz.LIGHTING)
addReflection(leftEyeQuad,eye=viz.LEFT_EYE)
# Create reflection for right eye
rightEyeQuad = viz.addTexQuad(scale=scale3,pos=pos3, euler=(-90,0,0))
rightEyeQuad.disable(viz.LIGHTING)
addReflection(rightEyeQuad,eye=viz.RIGHT_EYE)


# Create 4th reflection
# Create reflection for left eye
leftEyeQuad = viz.addTexQuad(scale=scale4, pos=pos4, euler=(0,0,0))
leftEyeQuad.disable(viz.LIGHTING)
addReflection(leftEyeQuad,eye=viz.LEFT_EYE)
# Create reflection for right eye
rightEyeQuad = viz.addTexQuad(scale=scale4,pos=pos4, euler=(0,0,0))
rightEyeQuad.disable(viz.LIGHTING)
addReflection(rightEyeQuad,eye=viz.RIGHT_EYE)

# Add avatar to represent self
avatar = steve.Steve()
avatar.setTracker(viz.MainView)
avatar.renderToAllRenderNodes(excludeMainPass=True)
avatar.collideMesh()


#######################################################

# Select doors, define centers(aka center of 'mentese') and set flags to FALSE or TRUE.
door_front = house.getChild('door_front') 
door_front.center(-1.87,1.17,-5.65)
door_frontIsOpen = False

door_pantry = house.getChild('door_pantry')
door_pantry.center(1.73, 1.21, 2.42)
door_pantryIsOpen = False

door_bedrm = house.getChild('door_bedrm')
door_bedrm.center(3.19,1.17,0.59)
door_bedrmIsOpen = False

door_bedrm_001 = house.getChild('door_bedrm_001')
door_bedrm_001.center(3.21,1.17,-1.06)
door_bedrm_001IsOpen = False

door_clkrm = house.getChild('door_clkrm')
door_clkrm.center(2.82,1.16,-1.64)
door_clkrmIsOpen = False

door_back = house.getChild('Back_door')
door_back.center(1.72,1.14,4.54)
door_backIsOpen = False

door_washrm = house.getChild('door_washrm');
door_washrm.center(-3.87,1.16,0.23)
door_washrmIsOpen = True

door_mstbed = house.getChild('door_mstbed');
door_mstbed.center(-2.33,1.17,-1.11)
door_mstbedIsOpen = False

door_cupbrd = house.getChild('door_cupbrd')
door_cupbrd.center(2.01,1.17,-5.51)
door_cupbrdIsOpen =False

door_bathrm = house.getChild('door_bathrm')
door_bathrm.center(-5.02,1.17,0.39)
door_bathrmIsOpen = True

door_wrdrbe = house.getChild('door_wrdrbe')
door_wrdrbe.center(-3.63,1.17,0.41)
door_wrdrbeIsOpen = False

door_bathrm_1 = house.getChild('door_bathrm_1')
door_bathrm_1.center(4.12,1.22,0.41)
door_bathrm_1IsOpen = False

door_wrdrbe_r = house.getChild('door_wrdrbe_r')
door_wrdrbe_r.center(3.00,1.17,-4.27)
door_wrdrbe_rIsOpen = False

door_wrdrbe_l = house.getChild('door_wrdrbe_l')
door_wrdrbe_l.center(3.00,1.17,-3.08)
door_wrdrbe_lIsOpen = False

door_wrdrbe_r_001 = house.getChild('door_wrdrbe_r_001')
door_wrdrbe_r_001.center (3.07,1.17,2.87)
door_wrdrbe_r_001IsOpen = False

door_wrdrbe_l_001 = house.getChild('door_wrdrbe_l_001')
door_wrdrbe_l_001.center(3.05,1.17,4.08)
door_wrdrbe_l_001IsOpen = False


# Create a spinning action for OPEN and CLOSE the door, vizact.spin(X,Y,Z,ROTATION,SPEED) must be ROTATION*SPEED= 90 degrees or -90 degrees.
openYinLessDoor = vizact.spin(0,1,0,-17.1,5)
closeYinLessDoor = vizact.spin(0,1,0,17.1,5)

openYinDoor = vizact.spin(0,1,0,-18,5)
closeYinDoor = vizact.spin(0,1,0,18,5)

openYinMoreDoor = vizact.spin(0,1,0,-19.5,5)
closeYinMoreDoor = vizact.spin(0,1,0,19.5,5)

openYoutLessDoor = vizact.spin(0,1,0,17.1,5)
closeYoutLessDoor = vizact.spin(0,1,0,-17.1,5)

openYoutDoor = vizact.spin(0,1,0,18,5)
closeYoutDoor = vizact.spin(0,1,0,-18,5)


# Used for Open and Close doors.
def mouseclick(button):

	global door_frontIsOpen
	global door_pantryIsOpen
	global door_bedrmIsOpen
	global door_bedrm_001IsOpen
	global door_clkrmIsOpen
	global door_backIsOpen
	global door_washrmIsOpen
	global door_mstbedIsOpen
	global door_cupbrdIsOpen
	global door_bathrmIsOpen
	global door_wrdrbeIsOpen
	global door_bathrm_1IsOpen
	global door_wrdrbe_rIsOpen
	global door_wrdrbe_lIsOpen
	global door_wrdrbe_r_001IsOpen
	global door_wrdrbe_l_001IsOpen

	if button == viz.MOUSEBUTTON_LEFT:
		pickObj = viz.pick()	# Get selected object.

		if pickObj == door_front:	# Case door_front.
			if (door_frontIsOpen == False):	# Open door.
				door_front.addAction(openYinDoor)
				door_frontIsOpen=True
			else:	# Close door.
				door_front.addAction(closeYinDoor)
				door_frontIsOpen=False
		elif pickObj == door_pantry :	# Case door_pantry.
			if (door_pantryIsOpen == False):	# Open door.
				door_pantry.addAction(openYinDoor)
				door_pantryIsOpen=True
			else:	# Close door.
				door_pantry.addAction(closeYinDoor)
				door_pantryIsOpen=False
		elif pickObj == door_bedrm :	# Case door_bedrm.
			if (door_bedrmIsOpen == False):	# Open door.
				door_bedrm.addAction(openYinDoor)
				door_bedrmIsOpen=True
			else:	# Close door.
				door_bedrm.addAction(closeYinDoor)
				door_bedrmIsOpen=False
		elif pickObj == door_bedrm_001 :	# Case door_bedrm_001.
			if (door_bedrm_001IsOpen == False):	# Open door.
				door_bedrm_001.addAction(openYoutDoor)
				door_bedrm_001IsOpen=True
			else:	# Close door.
				door_bedrm_001.addAction(closeYoutDoor)
				door_bedrm_001IsOpen=False
		elif pickObj == door_clkrm :	# Case door_clkrm.
			if (door_clkrmIsOpen == False):	# Open door.
				door_clkrm.addAction(openYoutDoor)
				door_clkrmIsOpen=True
			else:	# Close door.
				door_clkrm.addAction(closeYoutDoor)
				door_clkrmIsOpen=False
		elif pickObj == door_back :	# Case door_back.
			if (door_backIsOpen == False):	# Open door.
				door_back.addAction(openYinDoor)
				door_backIsOpen=True
			else:	# Close door.
				door_back.addAction(closeYinDoor)
				door_backIsOpen=False
		elif pickObj == door_washrm :	# Case door_washrm.
			if (door_washrmIsOpen == False):	# Open door.
				door_washrm.addAction(openYinMoreDoor)
				door_washrmIsOpen=True
			else:	# Close door.
				door_washrm.addAction(closeYinMoreDoor)
				door_washrmIsOpen=False
		elif pickObj == door_mstbed :	# Case door_mstbed.
			if (door_mstbedIsOpen == False):	# Open door.
				door_mstbed.addAction(openYoutDoor)
				door_mstbedIsOpen=True
			else:	# Close door.
				door_mstbed.addAction(closeYoutDoor)
				door_mstbedIsOpen=False
		elif pickObj == door_cupbrd :	# Case door_cupbrd.
			if (door_cupbrdIsOpen == False):	# Open door.
				door_cupbrd.addAction(openYinDoor)
				door_cupbrdIsOpen=True
			else:	# Close door.
				door_cupbrd.addAction(closeYinDoor)
				door_cupbrdIsOpen=False
		elif pickObj == door_bathrm :	# Case door_bathrm.
			if (door_bathrmIsOpen == False):	# Open door.
				door_bathrm.addAction(openYinLessDoor)
				door_bathrmIsOpen=True
			else:	# Close door.
				door_bathrm.addAction(closeYinLessDoor)
				door_bathrmIsOpen=False
		elif pickObj == door_wrdrbe :	# Case door_wrdrbe.
			if (door_wrdrbeIsOpen == False):	# Open door.
				door_wrdrbe.addAction(openYoutDoor)
				door_wrdrbeIsOpen=True
			else:	# Close door.
				door_wrdrbe.addAction(closeYoutDoor)
				door_wrdrbeIsOpen=False
		elif pickObj == door_bathrm_1 :	# Case door_bathrm_1.
			if (door_bathrm_1IsOpen == False):	# Open door.
				door_bathrm_1.addAction(openYinDoor)
				door_bathrm_1IsOpen=True
			else:	# Close door.
				door_bathrm_1.addAction(closeYinDoor)
				door_bathrm_1IsOpen=False
		elif pickObj == door_wrdrbe_r :	# Case door_wrdrbe_r.
			if (door_wrdrbe_rIsOpen == False):	# Open door.
				door_wrdrbe_r.addAction(openYoutLessDoor)
				door_wrdrbe_rIsOpen=True
			else:	# Close door.
				door_wrdrbe_r.addAction(closeYoutLessDoor)
				door_wrdrbe_rIsOpen=False
		elif pickObj == door_wrdrbe_l :	# Case door_wrdrbe_l.
			if (door_wrdrbe_lIsOpen == False):	# Open door.
				door_wrdrbe_l.addAction(openYinDoor)
				door_wrdrbe_lIsOpen=True
			else:	# Close door.
				door_wrdrbe_l.addAction(closeYinDoor)
				door_wrdrbe_lIsOpen=False
		elif pickObj == door_wrdrbe_r_001 :	# Case door_wrdrbe_r_001.
			if (door_wrdrbe_r_001IsOpen == False):	# Open door.
				door_wrdrbe_r_001.addAction(openYoutDoor)
				door_wrdrbe_r_001IsOpen=True
			else:	# Close door.
				door_wrdrbe_r_001.addAction(closeYoutDoor)
				door_wrdrbe_r_001IsOpen=False
		elif pickObj == door_wrdrbe_l_001 :	# Case door_wrdrbe_l_001.
			if (door_wrdrbe_l_001IsOpen == False):	# Open door.
				door_wrdrbe_l_001.addAction(openYinDoor)
				door_wrdrbe_l_001IsOpen=True
			else:	# Close door.
				door_wrdrbe_l_001.addAction(closeYinDoor)
				door_wrdrbe_l_001IsOpen=False
	return;

viz.callback(viz.MOUSEDOWN_EVENT,mouseclick)

#######################################################

# Map
#"""

# Create a new window in the upper left corner.
UpperLeftWindow = viz.addWindow(pos=(0,1.0),size=(0.2,0.2))
#pos=(0.8,1.0) upper right corner

# Create pseudo-birds eye.
box2 = viz.add('box2.osgb',pos=[0,10,0])  # Add a box.
box2.setScale(14,1,12) # Make it look more door like.

# Create a new viewpoint.
BirdView = viz.addView()

#Attach the bird's eye view to the upper left window.
UpperLeftWindow.setView(BirdView)

#Move the view above the center of the room.
BirdView.setPosition([0,25,0])

#Rotate the view so that it looks down.
BirdView.setEuler([0,90,0])

#Create another viewpoint.
RearView = viz.addView()

#Increase the field-of-view for both windows.
UpperLeftWindow.fov(60)


#Add an arrow marker to bird's eye view window to represent our current position/orientation.
arrow = viz.addTexQuad(parent=viz.ORTHO,scene=UpperLeftWindow,size=15)
arrow.texture(viz.add('arrow.tif'))

def UpdateViews():

	#Get the current head orientation and position
	yaw,pitch,roll = viz.MainView.getEuler()
	pos = viz.MainView.getPosition()

	#Move the rear view to the current position
	RearView.setPosition(pos)

	#Rotate the rear view so that it faces behind us
	RearView.setEuler([yaw+180,0,0])

	#Move arrow to our current location
	x,y,z = UpperLeftWindow.worldToScreen(pos,mode=viz.WINDOW_PIXELS)
	arrow.setPosition([x,y,0])
	arrow.setEuler([0,0,-yaw])

vizact.ontimer(0,UpdateViews)

#"""
