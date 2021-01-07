object_names = ['Intensidad','SemiEjeX','SemiEjeY','CentroX','CentroY','Inclinacion']
object_names_type = ['float','int','int','int','int','float']

radon_object_names = ['RadonDesde','RadonPaso','RadonHasta','RadonAngulo']
radon_object_names_type = ['int','float','int','float']
iradon_object_names = ['iRadonDesde','iRadonPaso','iRadonHasta']
iradon_object_names_type = ['int','float','int']

object_names_push = ['Agregar','Borrar']


arg_str = ""
for el in object_names:
    arg_str += el+","

arg_str = arg_str[:-1]

print(f"def __init__(self,{arg_str}):")
for el in object_names:
    print(f"\tself.{el} = {el}".expandtabs(4))
print("")

print(f"def update(self):")
for el in object_names:
    print(f"\t{el} = self.displayed_elipse.{el}".expandtabs(4))
print(f"\tnew_elipse = elipse({arg_str})".expandtabs(4))
print(f"\tself.elipse_list.append(new_elipse)".expandtabs(4))
# borro todo y vuelvo a escribir la elipse list en la caja de texto
print("\ttableStr = \"\"".expandtabs(4))
print("\tfor elip in self.elipse_list:".expandtabs(4))
print(f"\t\ttableStr+= elip.str_with_params()+ \"\\n\" ".expandtabs(4))
print(f"\tself.textEditParametersChart.setText(tableStr)".expandtabs(4))
print(f"")

print(" ")
print("def __init__(self):")
for el in object_names:
    print(f"\tself.{el} = None".expandtabs(4))

print("")


print(" ")
print("def __init__(self):")
for el in radon_object_names:
    print(f"\tself.{el} = None".expandtabs(4))

print("")

arg_str = ""
for el in radon_object_names:
    arg_str += el+","

arg_str = arg_str[:-1]

print(f"def __init__(self,{arg_str}):")
for el in radon_object_names:
    print(f"\tself.{el} = {el}".expandtabs(4))
print("")


print("#asignamos la funcion asociada al evento textChanged")
for el in object_names:
    print(f"self.lineEdit{el}.textChanged.connect(self.textChanged{el})".expandtabs(4))
for el in radon_object_names:
    print(f"self.lineEdit{el}.textChanged.connect(self.textChanged{el})".expandtabs(4))
for el in iradon_object_names:
    print(f"self.lineEdit{el}.textChanged.connect(self.textChanged{el})".expandtabs(4))
print("")





print("#asignamos la funcion asociada al evento clicked en push buttons")
for el in object_names_push:
    print(f"self.pushButton{el}.clicked.connect(self.onClick{el})".expandtabs(4))
print("")


print("#escribimos la funcion asociada al evento clicked en push buttons")
for el in object_names_push:
    print(f"def onClick{el}(self):".expandtabs(4))
    print(f"\tpass".expandtabs(4))  
print("")




print("#asignamos la funcion asociada al evento textChanged")
for el in object_names:
    print(f"self.lineEdit{el}.textChanged.connect(self.textChanged{el})".expandtabs(4))
print("")

print("#escribimos la validacion del numero de la funcion asociada al evento textChanged")
for el in object_names:
    print(f"def validateNumber{el}(self):".expandtabs(4))
    print(f"\t#sobreescribir".expandtabs(4))
    print(f"\treturn True".expandtabs(4))
            
print("")


print("#escribimos la funcion asociada al evento textChanged")
for i,el in enumerate(object_names):
    print(f"def textChanged{el}(self):".expandtabs(4))
    print(f"\tif(self.lineEdit{el}.text()==\'.\'):".expandtabs(4))
    print(f"\t\tself.displayed_elipse.{el} = 0".expandtabs(4))
    print(f"\telse:".expandtabs(4))
    print(f"\t\tif(len(self.lineEdit{el}.text())!=0):".expandtabs(4))
    print(f"\t\t\tinput_number = {object_names_type[i]}(self.lineEdit{el}.text())".expandtabs(4))
    print(f"\t\t\tself.displayed_elipse.{el} = input_number".expandtabs(4))   

print("")

for i,el in enumerate(radon_object_names):
    print(f"def textChanged{el}(self):".expandtabs(4))
    print(f"\tif(self.lineEdit{el}.text()==\'.\'):".expandtabs(4))
    print(f"\t\tself.displayed_radon.{el} = 0".expandtabs(4))
    print(f"\telse:".expandtabs(4))
    print(f"\t\tif(len(self.lineEdit{el}.text())!=0):".expandtabs(4))
    print(f"\t\t\tinput_number = {radon_object_names_type[i]}(self.lineEdit{el}.text())".expandtabs(4))
    print(f"\t\t\tself.displayed_radon.{el} = input_number".expandtabs(4))   


for i,el in enumerate(iradon_object_names):
    print(f"def textChanged{el}(self):".expandtabs(4))
    print(f"\tif(self.lineEdit{el}.text()==\'.\'):".expandtabs(4))
    print(f"\t\tself.displayed_iradon.{el} = 0".expandtabs(4))
    print(f"\telse:".expandtabs(4))
    print(f"\t\tif(len(self.lineEdit{el}.text())!=0):".expandtabs(4))
    print(f"\t\t\tinput_number = {iradon_object_names_type[i]}(self.lineEdit{el}.text())".expandtabs(4))
    print(f"\t\t\tself.displayed_iradon.{el} = input_number".expandtabs(4))   

