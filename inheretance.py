#blood sugar level
import time 

class parent(object):
    def __init__(self, FIRST_NAME, mother):
        self.FIRST_NAME = FIRST_NAME
        self.mother = mother


class child(object):
    def __init__(self, brother, LAST_NAME):
        self.LAST_NAME = LAST_NAME
        self.brother = brother


class family(parent, child):
    def __init__(self, FIRST_NAME, mother, brother, LAST_NAME, blood_sugar):
        self.blood_sugar = blood_sugar
        parent.__init__(self, FIRST_NAME, mother)
        child.__init__(self, brother, LAST_NAME)
        print('  ')
        print('{+} =====THIS IS YOUR BLOOD_SUGAR RESULT!!===== {+}')
        print('   ')
        print("EXAMPLE ==>> FIRST_NAME: {}, LAST_NAME: {}, blood_sugar: {}".format(self.FIRST_NAME, self.LAST_NAME, self.blood_sugar))
        print('  ')
        input('{+} ENTER YOUR FRIST_NAME:: ')
        print('  ')
        input('{+} ENTER YOUR LAST_NAME:: ')
        print(' ')
        print(' Saving Record...............')
        time.sleep(3)
        print(' ')
        print('==> PATIENT DETAILS SUCESSEFULLY REGISTERED!!!!')
        time.sleep(3)
        print(' ')
        print(' ')
        print(' ')
        print('{+}============= RESULIT DETAILS AND MEDICAL ADVICE ============={+}')
CANDIDATE = family('MAXWELL', 'chika', 'favour', 'ONYIA', 125)
print('  ')
print("  ")
try:
    blood_sugar = int(input('{+} ENTER YOUR BLOOD_SUGAR RESULT:: '))
except:
    ValueError = print("TYPE ONLY NUMBERS!!")
    raise
finally:
    print("BLOOD_SUGAR: ", blood_sugar)
    try:
        if (blood_sugar > 150) or (blood_sugar < 100):
            print(' ')
            print("[+] Medical Advice:\n" + "-->you need a doctor too prescribe some medication\n-->some medication for you write now would give you a better health status!!")
    except (blood_sugar <= 150) or (blood_sugar >= 100):
        print(' ')
        print(f'{blood_sugar} is on a good scale!!')
        print(' ')
        print("Medical Advice: ", "keep the good work going!!\n your health is your wealth")
        raise

if (blood_sugar < 100) or (blood_sugar > 150):
    print("  ")
    print("YOUR BLOOD_SUGAR IS  ABOVE SCALE!!!\n{+} YOUR BLOOD_SUGAR CAN NOT BE BELOW 100\n{+} IF YOUR BLOOD_SUGAR IS ABOVE 150 OR LESS THAN 100-->> PLEASE SEE A DOCTOR!!!...")

elif blood_sugar == int(input('{+} PLEASE RE-ENTER THE NUMBER  AGAIN IF IT BETWEEN 100-150: ')):
     if (blood_sugar >= 130):
        print(' ')
        print('YOUR SUGAR LEVEL IS HIGH!!!!')

     elif (blood_sugar <= 130):
        print(' ')
        print('YOUR BLOOD_SUGAR IS OKAY!!!\n-->HURRY!! HURRY!! HURRY!!\n-->KEEP THE GOOD WORK UP, YOUR HEALTH IS YOUR WEALTH!!')

     if (blood_sugar <= 125):
        print(' ')
        print('YOUR BLOOD_SUGAR IS OKAY!!!\n-->HURRY!! HURRY!! HURRY!!\n-->KEEP THE GOOD WORK UP, YOUR HEALTH IS YOUR WEALTH!!')
else:
   print(f"please enter the correct input for your BLOOD_SUGAR: ", blood_sugar)
   print(ValueError == "WRONG INPUT!!")









