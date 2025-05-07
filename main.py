import image
import text
model_name = "tunedModels/outfitsuggestiongenerator-usqw4b296kfe"
prompt=input("Enter your style idea : ")
gender=input("press 1 for male model and 0 for female model : ")
ethynicity=input("Enter your Ethynicity of wearer : ")
age=input("Enter your age of the wearer : ")
skin_color=input("Enter your Skin color of the wearer : ")
Season =input("Enter the season in which they will wear this dress : ")
Acessories=input("do you want acessories or not 1 for yes 0 for no : ")
occasion=input("Enter the Occasion on whhich the attire is to be worne : ")
if Acessories=="1":Acessories="" 
else:Acessories="no"
if gender=="1":
    gender="male"
    prompt=f"a complete {ethynicity} attire for male of age {age} skin color{skin_color} to be worne in {Season} season with {Acessories}Acessories to be worne on {occasion} occasion considering the designe idea" + prompt +"With matching footware"
else:
    gender="female"
    prompt=f"a complete {ethynicity} attire for female of age {age} skin color{skin_color} to be worne in {Season} season with {Acessories}Acessories to be worne on {occasion} occasion considering the designe idea" + prompt +"With matching footware"

prompt2=text.generate_output(model_name,prompt)
print(prompt2)

if gender=="male":
    prompt2=f"Full body image of A {skin_color} skinned male model of age {age} wearing" + prompt2 + "facing the camera"
else:
    prompt2=f"Full body image of A {skin_color} skinned female model of age {age} wearing" + prompt2 + "facing the camera"


images=image.generate_image(prompt2)
images.show()