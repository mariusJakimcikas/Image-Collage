import image
import math

#defining necessary tools and measurements
originalImage = image.FileImage("flower.jpg")
width = originalImage.getWidth()
height = originalImage.getHeight()
imageWindow = image.ImageWin(width * 3, height * 3, "Image Collage")

def Collage(originalImage, width, height):

	#creating image that is horizontally flipped
	def horizontallyFlippedImage(originalImage, width, height):
		lastPixel = width - 1

		flippedImage = image.EmptyImage(width, height)

		for col in range(width):
			for row in range(height):
				pixel = originalImage.getPixel(lastPixel - col, row)
				flippedImage.setPixel(col, row, pixel)
		return flippedImage

	#creating Sepia Image
	def sepiaImage(originalImage, width, height):

		def sepiaPixel(oldPixel):
			newRed = int((oldPixel.getRed() * .393) + (oldPixel.getGreen() *.769) + (oldPixel.getBlue() * .189))
			newGreen = int((oldPixel.getRed() * .349) + (oldPixel.getGreen() *.686) + (oldPixel.getBlue() * .168))
			newBlue = int((oldPixel.getRed() * .272) + (oldPixel.getGreen() *.534) + (oldPixel.getBlue() * .131))

			if newRed > 255:
				newRed = 255
			if newGreen > 255:
				newGreen = 255
			if newBlue > 255:
				newBlue = 255

			newPixel = image.Pixel(newRed, newGreen, newBlue)
			return newPixel

		sepiaImage = image.EmptyImage(width, height)

		for row in range(height):
			for col in range(width):
				oldPixel = originalImage.getPixel(col, row)
				newPixel = sepiaPixel(oldPixel)
				sepiaImage.setPixel(col, row, newPixel)

		return sepiaImage 

	# creating image that is horizontally mirrored through the middle
	def horizontalMirrorImage(originalImage, width, height):
		lastPixel = width - 1

		mirroredImage = image.EmptyImage(width, height)

		for col in range(width):
			if col == width // 2:
				break

			for row in range(height):
				pixel = originalImage.getPixel(col, row)
				mirroredImage.setPixel(col, row, pixel)
				mirroredImage.setPixel(lastPixel - col, row, pixel)

		return mirroredImage

	#creating grayscale 
	def grayscaleImage(originalImage, width, height):

		def grayPixel(oldPixel):
			averageRGB = (oldPixel.getRed() + oldPixel.getGreen() + oldPixel.getBlue()) // 3
			newPixel   = image.Pixel(averageRGB, averageRGB, averageRGB)
			return newPixel

		grayscaleImage = image.EmptyImage(width, height)

		for row in range(height):
			for col in range(width):
				oldPixel = originalImage.getPixel(col, row)
				newPixel = grayPixel(oldPixel)
				grayscaleImage.setPixel(col, row, newPixel)
		return grayscaleImage

	# 9th image for extra credit (instead of original image)
	def convolve(originalImage, pixelRow, pixelCol, kernel):
			kernelColBase = pixelCol - 1
			kernelRowBase = pixelRow - 1
			total = 0
			for row in range(kernelRowBase, kernelRowBase+3):
				for col in range(kernelColBase, kernelColBase+3):
					kColIndex = col - kernelColBase
					kRowIndex = row - kernelRowBase
					pixel     = originalImage.getPixel(col, row)
					intensity = pixel.getRed()
					total     = total + intensity * kernel[kRowIndex][kColIndex]
		
			return total

	def extraCreditImage(originalImage, width, height):

		def edgeDetectRed(originalImage, width, height):

			gray = grayscaleImage

			extraCreditImg = image.EmptyImage(width, height)
			blazingYellow  = image.Pixel(254, 231, 21)
			#pantoneBlack = image.Pixel(16, 24, 32)
			red   = image.Pixel(255, 0 ,0)
			xMask = [ [-1, -2, -1], [0, 0, 0], [1,2,1] ]
			yMask = [ [1, 0, -1], [2, 0, -2], [1,0,-1] ]

			for row in range(1, height-1):
				for col in range(1, width-1):
					gX = convolve(gray, row, col, xMask)
					gY = convolve(gray, row, col, yMask)
					g  = math.sqrt(gX**2 + gY**2)
					if g > 175:
						extraCreditImg.setPixel(col, row, red)
					else:
						extraCreditImg.setPixel(col, row, blazingYellow) 	
			return extraCreditImg

		return edgeDetectRed(originalImage, width, height)

	#creating negative image 
	def negativeImage(originalImage, width, height):

		def negativePixel(oldPixel):
			newRed   = 255 - oldPixel.getRed()
			newGreen = 255 - oldPixel.getGreen()
			newBlue  = 255 - oldPixel.getBlue()
			newPixel = image.Pixel(newRed, newGreen, newBlue)
			return newPixel

		negativeImage = image.EmptyImage(width, height)

		for row in range(height):
			for col in range(width):
				oldPixel = originalImage.getPixel(col, row)
				newPixel = negativePixel(oldPixel)
				negativeImage.setPixel(col, row, newPixel)

		return negativeImage


	# creating edge detection filter
	def edgeDetectionImage(originalImage, width, height):

		def edgeDetect(originalImage, width, height):
			grayscale = grayscaleImage

			edgeImage = image.EmptyImage(width, height)

			black = image.Pixel(0, 0, 0)
			white = image.Pixel(255, 255, 255)
			xMask = [ [-1, -2, -1], [0, 0, 0], [1,2,1] ]
			yMask = [ [1, 0, -1], [2, 0, -2], [1,0,-1] ]

			for row in range(1, height-1):
				for col in range(1, width-1):
					gX = convolve(grayscale, row, col, xMask)
					gY = convolve(grayscale, row, col, yMask)
					g  = math.sqrt(gX**2 + gY**2)
					if g > 175:
						edgeImage.setPixel(col, row, white)
					else:
						edgeImage.setPixel(col, row, black) 	
			return edgeImage

		return edgeDetect(originalImage, width, height)

	# creating my own filter which will only leave the green color
	def blueImage(originalImage, width, height):

		def bluePixel(oldPixel):
			newRed   = 0
			newGreen = 0
			newBlue  = oldPixel.getBlue()        
			newPixel = image.Pixel(newRed, newGreen, newBlue)
			return newPixel	

		blueImage = image.EmptyImage(width, height)

		for row in range(height):
			for col in range(width):
				oldPixel = originalImage.getPixel(col, row)
				newPixel = bluePixel(oldPixel)
				blueImage.setPixel(col, row, newPixel)

		return blueImage
	# creating my own filter which will only leave the green color
	def blueImage(originalImage, width, height):

		def bluePixel(oldPixel):
			newRed   = 0
			newGreen = 0
			newBlue  = oldPixel.getBlue()        
			newPixel = image.Pixel(newRed, newGreen, newBlue)
			return newPixel	

		blueImage = image.EmptyImage(width, height)

		for row in range(height):
			for col in range(width):
				oldPixel = originalImage.getPixel(col, row)
				newPixel = bluePixel(oldPixel)
				blueImage.setPixel(col, row, newPixel)

		return blueImage


	#creating blur Image
	def blurImage(originalImage, width, height):

		blurredImage = image.EmptyImage(width, height)

		mask         = [[1, 2, 1], [2, 1, 2], [1, 2, 1]]
		mask_length  = len(mask)
		mask_offset  = mask_length // 2

		for pixel_x in range(1, width - 1):
			for pixel_y in range(1, height - 1):
				red   = 0
				green = 0
				blue  = 0
				#using the mask to calculate total colors
				for mask_x in range(mask_length):
					for mask_y in range(mask_length):

						#here I hardcoded to go through all the pixels around pixel(pixel_x, pixel_y)
						#then used the mask to calculate red, green and blue values and added them up
						#to blur the pixel
						if mask_x == 0 and mask_y == 0:
							pixel = originalImage.getPixel(pixel_x - 1, pixel_y - 1)
							red   += mask[0][0] * pixel.getRed()
							green += mask[0][0] * pixel.getGreen()
							blue  += mask[0][0] * pixel.getBlue()
						if mask_x == 0 and mask_y == 1:
							pixel = originalImage.getPixel(pixel_x - 1, pixel_y)
							red   += mask[0][1] * pixel.getRed()
							green += mask[0][1] * pixel.getGreen()
							blue  += mask[0][1] * pixel.getBlue()

						if mask_x == 0 and mask_y == 2:
							pixel = originalImage.getPixel(pixel_x - 1, pixel_y + 1)
							red   += mask[0][2] * pixel.getRed()
							green += mask[0][2] * pixel.getGreen()
							blue  += mask[0][2] * pixel.getBlue()

						if mask_x == 1 and mask_y == 0:
							pixel = originalImage.getPixel(pixel_x, pixel_y - 1)
							red   += mask[1][0] * pixel.getRed()
							green += mask[1][0] * pixel.getGreen()
							blue  += mask[1][0] * pixel.getBlue()

						if mask_x == 1 and mask_y == 1:
							pixel = originalImage.getPixel(pixel_x, pixel_y)
							red   += mask[1][1] * pixel.getRed()
							green += mask[1][1] * pixel.getGreen()
							blue  += mask[1][1] * pixel.getBlue()

						if mask_x == 1 and mask_y == 2:
							pixel = originalImage.getPixel(pixel_x, pixel_y + 1)
							red   += mask[1][2] * pixel.getRed()
							green += mask[1][2] * pixel.getGreen()
							blue  += mask[1][2] * pixel.getBlue()

						if mask_x == 2 and mask_y == 0:
							pixel = originalImage.getPixel(pixel_x + 1, pixel_y - 1)
							red   += mask[2][0] * pixel.getRed()
							green += mask[2][0] * pixel.getGreen()
							blue  += mask[2][0] * pixel.getBlue()

						if mask_x == 2 and mask_y == 1:
							pixel = originalImage.getPixel(pixel_x + 1, pixel_y)
							red   += mask[2][1] * pixel.getRed()
							green += mask[2][1] * pixel.getGreen()
							blue  += mask[2][1] * pixel.getBlue()

						if mask_x == 2 and mask_y == 2:
							pixel = originalImage.getPixel(pixel_x + 1, pixel_y + 1)
							red   += mask[2][2] * pixel.getRed()
							green += mask[2][2] * pixel.getGreen()
							blue  += mask[2][2] * pixel.getBlue()

				newPixel = image.Pixel(red // 13, green // 13, blue // 13)
				blurredImage.setPixel(pixel_x, pixel_y, newPixel)

		#filling the pixels on the edge of the image which I skipped when bluring because
		#algortihm would not work for these pixels since
		for x in range(width):
			for y in range(height):
				if x == 0:
					blurredImage.setPixel(x, y, originalImage.getPixel(x, y))
				if x == width - 1:
					blurredImage.setPixel(x, y, originalImage.getPixel(x, y))
				if y == 0:	
					blurredImage.setPixel(x, y, originalImage.getPixel(x, y))
				if y == height - 1:
					blurredImage.setPixel(x, y, originalImage.getPixel(x, y))

		return blurredImage

#putting everything in one collage


	#creating all 9 images
	horizontallyFlippedImage = horizontallyFlippedImage(originalImage, width, height)
	sepiaImage               = sepiaImage(originalImage, width, height)
	horizontalMirrorImage    = horizontalMirrorImage(originalImage, width, height)
	grayscaleImage           = grayscaleImage(originalImage, width, height)
	extraCreditImage 		 = extraCreditImage(originalImage, width, height)
	negativeImage 			 = negativeImage(originalImage, width, height)
	edgeDetectionImage 		 = edgeDetectionImage(originalImage, width, height)
	blueImage 				 = blueImage(originalImage, width, height)
	blurImage 				 = blurImage(originalImage, width, height)

	#setting each image in the right spot based on the order on Blackboard
	horizontallyFlippedImage.setPosition(0, 0)
	sepiaImage.setPosition(width, 0)
	horizontalMirrorImage.setPosition(width * 2, 0)
	grayscaleImage.setPosition(0, height)
	extraCreditImage.setPosition(width, height)
	negativeImage.setPosition(width * 2, height)
	edgeDetectionImage.setPosition(0, height * 2)
	blueImage.setPosition(width, height * 2)
	blurImage.setPosition(width * 2, height * 2)

	#drawing each image on the screen
	horizontallyFlippedImage.draw(imageWindow)
	sepiaImage.draw(imageWindow)
	horizontalMirrorImage.draw(imageWindow)
	grayscaleImage.draw(imageWindow)
	extraCreditImage.draw(imageWindow)
	negativeImage.draw(imageWindow)
	edgeDetectionImage.draw(imageWindow)
	blueImage.draw(imageWindow)
	blurImage.draw(imageWindow)
	imageWindow.exitOnClick()

Collage(originalImage, width, height)
